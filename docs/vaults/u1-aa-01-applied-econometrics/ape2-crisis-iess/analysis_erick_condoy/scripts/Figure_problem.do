* ----------------------------------------------------------------------------
* TITULO: Radiografía del Problema - Sostenibilidad del IESS
* DESCRIPCIÓN: Generación de Figura Multipanel de Canales Estructurales (1990-2024)
*              - Canal A: Inestabilidad Social (Homicidios vs. Cobertura)
*              - Canal B: Prioridad Fiscal (Gasto Militar vs. Cobertura)
*              - Canal C: Drenaje Demográfico (Migración vs. Cobertura)
*              - Canal D: Trayectoria de Informalización Beckeriana
* AUTOR: Erick Fabricio Condoy Seraquive
* FECHA: 2026-05-18
* ----------------------------------------------------------------------------

* 0. Configuración Inicial e Idempotencia
clear all
set more off
capture log close
graph close _all

* 1. Directorio de Trabajo (Garantiza Reproducibilidad)
* Intentamos cambiar al directorio del proyecto de forma dinámica.
* Ancla absoluta basada en la estructura del entorno de Erick:
local project_path "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/analysis_erick_condoy"

capture cd "`project_path'"
if _rc {
    di ">>> Advertencia: No se pudo cambiar al directorio absoluto."
    di ">>> Intentando usar el directorio relativo actual..."
}
pwd

* Crear carpetas de salida si no existen
capture mkdir "logs"
capture mkdir "assets"

* Iniciar registro del log
log using "logs/Figure_problem.log", replace text

di as text "{hline}"
di as res "INICIANDO PROCESAMIENTO: RADIOGRAFÍA DE LA CRISIS DEL IESS"
di as text "{hline}"

* 2. Ingesta de Datos (Idempotente)
local dta_file "data/base_analisis.dta"
local csv_file "data/base_analisis.csv"

capture use "`dta_file'", clear
if _rc {
    di ">>> Base .dta no encontrada. Intentando importar desde .csv..."
    capture import delimited "`csv_file'", clear
    if _rc {
        di ">>> ERROR CRÍTICO: No se encontró ni .dta ni .csv en data/."
        exit 199
    }
    save "`dta_file'", replace
    di ">>> Base convertida y guardada en formato .dta."
}

* Declarar estructura de serie de tiempo
tsset anio

* 3. Construcción y Etiquetado de Indicadores Clave
* Tasa de Cobertura Previsional (Ratio de soporte alternativo según Diamond, 1965)
gen cobertura = (afiliados_iess / fuerza_laboral) * 100
label variable cobertura "Tasa de Cobertura Previsional (%)"

* Migración Neta escalada a miles para mejorar la legibilidad visual
gen migracion_miles = migracion_neta / 1000
label variable migracion_miles "Migración Neta (Miles de personas)"

* Logaritmo de la tasa de homicidios
gen ln_homicidios = ln(tasa_homicidios)
label variable ln_homicidios "Log Tasa Homicidios"

* Crecimiento anual de afiliados
gen growth_afiliados = (afiliados_iess - L.afiliados_iess) / L.afiliados_iess * 100
label variable growth_afiliados "Crecimiento Anual de Afiliados (%)"

* 4. Auditoría Analítica en el Log (Evidencia Reproducible)
di _newline(1) as res ">>> ANÁLISIS DE CORRELACIÓN Y REGRESIÓN BÁSICA <<<"
di as text "{hline}"
correlate cobertura tasa_homicidios gasto_militar_pib migracion_miles

di _newline(1) as res ">>> ESTIMACIÓN DE ASOCIACIONES (MCO de Referencia) <<<"
di as text "{hline}"
regress cobertura tasa_homicidios gasto_militar_pib migracion_miles

* 5. Diseño de Gráficos Individuales (Estilo Premium y Limpio)
* Configurar esquema básico
set scheme s1color

* Opciones generales de estilo (Se utiliza 'tiny' para optimizar la fusión de paneles)
local main_opts "xtitle("Año", size(tiny)) xlabel(1990(5)2024, labsize(tiny)) graphregion(color(white)) plotregion(color(white))"

* ----------------------------------------------------------------------------
* GRÁFICO 1: Canal de Inestabilidad Social (Homicidios vs. Cobertura)
* ----------------------------------------------------------------------------
twoway (line cobertura anio, lcolor(navy) lwidth(thick) yaxis(1)) ///
       (line tasa_homicidios anio, lcolor(cranberry) lwidth(thick) lpattern(dash) yaxis(2)), ///
       title("A. Canal de Inestabilidad Social", size(small) color(black) margin(bottom)) ///
       subtitle("Divergencia entre Cobertura IESS y Ola de Violencia (1990-2024)", size(tiny) color(gs8) margin(bottom)) ///
       ytitle("Cobertura Previsional (%)", axis(1) size(tiny) color(navy)) ///
       ytitle("Tasa de Homicidios (por 100k hab)", axis(2) size(tiny) color(cranberry)) ///
       ylabel(20(5)50, axis(1) labsize(tiny) grid glcolor(gs15) glwidth(thin) glpattern(solid)) ///
       ylabel(0(10)50, axis(2) labsize(tiny)) ///
       legend(order(1 "Cobertura (%)" 2 "Homicidios (por 100k)") size(tiny) pos(6) cols(2) ring(1)) ///
       `main_opts' name(g_social, replace)

* ----------------------------------------------------------------------------
* GRÁFICO 2: Canal de Prioridad Fiscal (Gasto Militar vs. Cobertura)
* ----------------------------------------------------------------------------
twoway (line cobertura anio, lcolor(navy) lwidth(thick) yaxis(1)) ///
       (line gasto_militar_pib anio, lcolor(sand) lwidth(thick) lpattern(dash_dot) yaxis(2)), ///
       title("B. Canal de Prioridad Fiscal (Crowding-out)", size(small) color(black) margin(bottom)) ///
       subtitle("Competencia de Recursos entre Defensa y Seguridad Social (1990-2024)", size(tiny) color(gs8) margin(bottom)) ///
       ytitle("Cobertura Previsional (%)", axis(1) size(tiny) color(navy)) ///
       ytitle("Gasto Militar (% del PIB)", axis(2) size(tiny) color(sand)) ///
       ylabel(20(5)50, axis(1) labsize(tiny) grid glcolor(gs15) glwidth(thin) glpattern(solid)) ///
       ylabel(1(0.5)3.5, axis(2) labsize(tiny)) ///
       legend(order(1 "Cobertura (%)" 2 "Gasto Militar (% PIB)") size(tiny) pos(6) cols(2) ring(1)) ///
       `main_opts' name(g_fiscal, replace)

* ----------------------------------------------------------------------------
* GRÁFICO 3: Canal de Drenaje Demográfico (Migración vs. Cobertura)
* ----------------------------------------------------------------------------
twoway (line cobertura anio, lcolor(navy) lwidth(thick) yaxis(1)) ///
       (bar migracion_miles anio, color(teal) barwidth(0.6) yaxis(2)), ///
       title("C. Canal de Drenaje Demográfico", size(small) color(black) margin(bottom)) ///
       subtitle("Impacto de la Emigración en el Soporte del Sistema (1990-2024)", size(tiny) color(gs8) margin(bottom)) ///
       ytitle("Cobertura Previsional (%)", axis(1) size(tiny) color(navy)) ///
       ytitle("Migración Neta (Miles de personas)", axis(2) size(tiny) color(teal)) ///
       ylabel(20(5)50, axis(1) labsize(tiny) grid glcolor(gs15) glwidth(thin) glpattern(solid)) ///
       ylabel(-60(20)100, axis(2) labsize(tiny)) ///
       legend(order(1 "Cobertura (%)" 2 "Migración Neta (Miles)") size(tiny) pos(6) cols(2) ring(1)) ///
       `main_opts' name(g_demog, replace)

* ----------------------------------------------------------------------------
* GRÁFICO 4: Trayectoria Dinámica (Radiografía del Colapso Previsional)
* ----------------------------------------------------------------------------
* Etiquetas limpias para no saturar el gráfico
gen label_year = ""
replace label_year = string(anio) if inlist(anio, 1990, 1995, 2000, 2008, 2015, 2020, 2024)

* Posicionamiento preciso del reloj para evitar solapamientos
gen mlab_pos = 12
replace mlab_pos = 9  if anio == 1990
replace mlab_pos = 3  if anio == 1995
replace mlab_pos = 9  if anio == 2000
replace mlab_pos = 12 if anio == 2008
replace mlab_pos = 9  if anio == 2015
replace mlab_pos = 6  if anio == 2020
replace mlab_pos = 3  if anio == 2024

twoway (connected cobertura tasa_homicidios, lcolor(navy) lwidth(thin) mcolor(navy) msize(medium) mlabel(label_year) mlabvpos(mlab_pos) mlabsize(tiny)), ///
       title("D. Radiografía Dinámica del Colapso", size(small) color(black) margin(bottom)) ///
       subtitle("Trayectoria Temporal: Cobertura vs. Tasa de Homicidios (1990-2024)", size(tiny) color(gs8) margin(bottom)) ///
       xtitle("Tasa de Homicidios (por 100,000 hab)", size(tiny)) ///
       ytitle("Cobertura Previsional (%)", size(tiny)) ///
       ylabel(20(5)50, labsize(tiny) grid glcolor(gs15) glwidth(thin) glpattern(solid)) ///
       xlabel(0(10)50, labsize(tiny)) ///
       legend(off) ///
       note("Nota: Se etiquetan hitos e hitos de quiebres estructurales detectados.", size(tiny) color(gs10)) ///
       graphregion(color(white)) plotregion(color(white)) name(g_trajectory, replace)

* ----------------------------------------------------------------------------
* 6. Fusión y Exportación del Gráfico Multipanel
* ----------------------------------------------------------------------------
di _newline(1) ">>> FUSIONANDO PANELES Y EXPORTANDO FIGURA..."

graph combine g_social g_fiscal g_demog g_trajectory, ///
              cols(2) rows(2) iscale(0.70) ///
              title("Radiografía de la Sostenibilidad del IESS en el Ecuador (1990-2024)", size(small) color(black)) ///
              subtitle("Interacción Dinámica de Canales Fiscales, Demográficos e Institucionales", size(vsmall) color(gs8)) ///
              note("Fuente: Dirección Actuarial del IESS, Banco Mundial (WDI). Elaboración propia.", size(tiny) color(gs10)) ///
              graphregion(color(white))

graph export "assets/fig-radiografia-problema.png", replace width(3200)

* Limpieza de memoria gráfica
graph close g_social g_fiscal g_demog g_trajectory

di as text "{hline}"
di as res "PROCESAMIENTO DE RADIOGRAFÍA DE LA CRISIS FINALIZADO CON ÉXITO."
di as text "La figura ha sido guardada en: assets/fig-radiografia-problema.png"
di as text "{hline}"

log close
