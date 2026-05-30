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

* 5. Cálculo de Índices de Evolución Relativa (Base 100 = 1990)
* Para variables de escala estrictamente positiva, indexamos a su valor de 1990.
* Para la Migración Neta, al contener valores negativos, aplicamos normalización Min-Max [0, 100].

quietly summarize afiliados_iess if anio == 1990
local af_1990 = r(mean)
gen af_idx = (afiliados_iess / `af_1990') * 100

quietly summarize fuerza_laboral if anio == 1990
local fl_1990 = r(mean)
gen fl_idx = (fuerza_laboral / `fl_1990') * 100

quietly summarize gasto_militar_pib if anio == 1990
local gm_1990 = r(mean)
gen gm_idx = (gasto_militar_pib / `gm_1990') * 100

quietly summarize tasa_homicidios if anio == 1990
local ho_1990 = r(mean)
gen ho_idx = (tasa_homicidios / `ho_1990') * 100

quietly summarize migracion_neta
local mi_min = r(min)
local mi_max = r(max)
gen mi_idx = ((migracion_neta - `mi_min') / (`mi_max' - `mi_min')) * 100

* 6. Diseño del Gráfico Único de Evolución Temporal Homogénea
set scheme s1color

twoway (line af_idx anio, lcolor(navy) lwidth(thick)) ///
       (line fl_idx anio, lcolor(purple) lwidth(medium) lpattern(dash)) ///
       (line gm_idx anio, lcolor(orange) lwidth(medium) lpattern(dash_dot)) ///
       (line ho_idx anio, lcolor(red) lwidth(thick)) ///
       (line mi_idx anio, lcolor(teal) lwidth(medium) lpattern(shortdash)), ///
       title("Trayectoria Longitudinal Homogénea de las Series (1990-2024)", size(small) color(black)) ///
       ytitle("Índice de Evolución Relativa (Base 100 = 1990)", size(vsmall)) ///
       xtitle("Año", size(vsmall)) ///
       xlabel(1990(5)2024, labsize(vsmall)) ylabel(, labsize(vsmall)) ///
       xline(2000, lcolor(gs12) lpattern(dot)) ///
       xline(2008, lcolor(gs12) lpattern(dot)) ///
       xline(2014, lcolor(gs12) lpattern(dot)) ///
       xline(2020, lcolor(gs12) lpattern(dot)) ///
       legend(order(1 "Afiliados IESS" 2 "Fuerza Laboral" 3 "Gasto Militar % PIB" 4 "Tasa de Homicidios" 5 "Migración Neta (Min-Max)") size(vsmall) pos(6) cols(2) ring(1)) ///
       note("Fuente: Anuarios Estadísticos del IESS, Banco Mundial (WDI). Elaboración propia.", size(tiny) color(gs10)) ///
       graphregion(color(white)) plotregion(color(white))

graph export "assets/fig-evolucion-unica.png", replace width(3200)

di as text "{hline}"
di as res "PROCESAMIENTO DE EVOLUCIÓN UNIFICADA FINALIZADO CON ÉXITO."
di as text "La gráfica de panel único ha sido guardada en: assets/fig-evolucion-unica.png"
di as text "{hline}"

log close
