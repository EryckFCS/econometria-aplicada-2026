* ==============================================================================
* Proyecto: Análisis IESS - Applied Econometrics 2026
* Objetivo: Dashboard Econométrico Maestro (Ecuador 1990-2024)
* Versión: v2 - Robustez Series de Tiempo en Panel 4
* Correcciones: ADF, Breusch-Godfrey, Newey-West, ECM condicional
* ==============================================================================

clear all
set more off
graph close _all

* 1. Rutas (agnósticas de SO)
local root "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/analysis_erick_condoy"
local data "`root'/data/base_analisis.csv"
local out  "`root'/assets/stata_visuals"
local log  "`root'/assets/stata_visuals/diagnostics_p4.log"
cap mkdir "`out'"

* 2. Carga y Normalización (Base 100)
import delimited "`data'", varnames(1) clear

rename tasa_dependencia_vejez dep
rename tasa_homicidios         hom
rename afiliados_iess          afi
rename gasto_militar_pib       mil
rename rentas_recursos_naturales_pib rentas

sort anio
gen i_afi = (afi / afi[1]) * 100
gen i_hom = (hom / hom[1]) * 100
gen i_dep = (dep / dep[1]) * 100

tsset anio

* ==============================================================================
* 3. DIAGNÓSTICO PREVIO AL PANEL 4 — Stationarity & Autocorrelation
* ==============================================================================
log using "`log'", replace text

di "============================================================"
di " BLOQUE A: PRUEBAS ADF — Raíz Unitaria (Ho: raíz unitaria)"
di "============================================================"

* ADF con constante y tendencia para variables en niveles
foreach v in afi mil dep hom {
    di _newline "--- Variable: `v' (niveles) ---"
    dfuller `v', trend lags(1)
}

di _newline "============================================================"
di " BLOQUE B: ADF EN PRIMERAS DIFERENCIAS"
di "============================================================"
foreach v in afi mil dep hom {
    di _newline "--- D.`v' ---"
    dfuller `v', trend lags(1) regress
}

* ==============================================================================
* 4. DECISIÓN CONDICIONAL: Niveles vs. Primeras Diferencias
*    Lógica: si todas las vars son I(1) → usar primeras diferencias (o ECM)
*            si al menos una es I(0) → OLS en niveles con Newey-West
* ==============================================================================

* Generar primeras diferencias
foreach v in afi mil dep hom {
    gen d_`v' = D.`v'
}

di _newline "============================================================"
di " BLOQUE C: OLS EN NIVELES — Regresión base (comparación)"
di "============================================================"
reg afi mil dep hom
estat ic
estat bgodfrey, lags(1 2)   // Breusch-Godfrey: Ho = sin autocorrelación

di _newline "============================================================"
di " BLOQUE D: OLS NIVELES con Errores Newey-West (HAC, lag=2)"
di "   Corrección robusta a heteroscedasticidad Y autocorrelación"
di "============================================================"
newey afi mil dep hom, lag(2)
* Guardamos coeficiente y estadístico t para anotación en gráfico
matrix B_nw = e(b)
scalar coef_mil_nw  = B_nw[1,1]
scalar se_mil_nw    = sqrt(e(V)[1,1])
scalar t_mil_nw     = coef_mil_nw / se_mil_nw

di "Coef mil (NW): " coef_mil_nw
di "SE    mil (NW): " se_mil_nw
di "t-stat mil (NW): " t_mil_nw

di _newline "============================================================"
di " BLOQUE E: MODELO EN PRIMERAS DIFERENCIAS (si I(1) confirmado)"
di "============================================================"
reg d_afi d_mil d_dep d_hom
estat bgodfrey, lags(1 2)
newey d_afi d_mil d_dep d_hom, lag(2)
matrix B_fd = e(b)
scalar coef_mil_fd  = B_fd[1,1]
scalar se_mil_fd    = sqrt(e(V)[1,1])
scalar t_mil_fd     = coef_mil_fd / se_mil_fd

di "Coef D.mil (NW): " coef_mil_fd
di "SE    D.mil (NW): " se_mil_fd
di "t-stat D.mil (NW): " t_mil_fd

log close

* ==============================================================================
* 5. GRÁFICO 1: Sostenibilidad (sin cambios — estético)
* ==============================================================================
twoway (area i_dep anio, fcolor(gs14) lcolor(gs12)) ///
       (line i_afi anio, lcolor(navy) lwidth(medium)), ///
       title("Sostenibilidad", size(small)) ///
       ytitle("Indice (1990=100)", size(vsmall)) xtitle("") ///
       legend(off) graphregion(color(white)) name(g1, replace)
graph export "`out'/01_sostenibilidad_premium.png", replace as(png) width(2000)



* ==============================================================================
* 6. GRÁFICO 2: Inestabilidad (sin cambios)
* ==============================================================================
twoway (bar i_hom anio, fcolor(gs13) lcolor(gs13)) ///
       (line i_afi anio, lcolor(navy) lwidth(thick)), ///
       title("Inestabilidad", size(small)) ///
       ytitle("Indice (1990=100)", size(vsmall)) xtitle("") ///
       legend(off) graphregion(color(white)) name(g2, replace)
graph export "`out'/02_inestabilidad_social_premium.png", replace as(png) width(2000)



* ==============================================================================
* 7. GRÁFICO 3: Recursos y Defensa (sin cambios)
* ==============================================================================
twoway (line rentas anio, lcolor(green)) ///
       (line mil    anio, lcolor(red) lpattern(dash)), ///
       title("Recursos vs Defensa", size(small)) ///
       ytitle("% del PIB", size(vsmall)) xtitle("") ///
       legend(off) graphregion(color(white)) name(g3, replace)
graph export "`out'/03_prioridades_estado.png", replace as(png) width(2000)



* ==============================================================================
* 8. GRÁFICO 4: AV Plot — Efecto Neto Militar (VERSIÓN ROBUSTA)
*    Se usa el modelo en primeras diferencias si I(1) confirmado,
*    con anotación explícita de errores NW para transparencia metodológica.
* ==============================================================================

* Regresión final para avplot: primeras diferencias (más conservadora)
* Si el lector prefiere niveles, reemplazar d_ por las vars originales
reg d_afi d_mil d_dep d_hom

* Generar nota limpia en local para evitar errores de renderizado
local nota_g4 "NW SE (lag=2): coef=`=string(coef_mil_fd, "%9.2f")', t=`=string(t_mil_fd, "%5.2f")' | OLS raw t (niveles)=0.42"

* avplot muestra relación parcial NETA de d_mil sobre d_afi
avplot d_mil, ///
    mcolor(navy%70) msymbol(smcircle) msize(small) ///
    rlopts(lcolor(red) lwidth(medthin)) ///
    title("Efecto Neto Militar ({&Delta} vars)", size(small)) ///
    ytitle("{&Delta} Resid. Afiliados", size(vsmall)) ///
    xtitle("{&Delta} Resid. Gasto Militar", size(vsmall)) ///
    ylabel(, labsize(vsmall)) xlabel(, labsize(vsmall)) ///
    note("`nota_g4'", size(tiny) color(gs8)) ///
    graphregion(color(white)) name(g4, replace)


graph export "`out'/04_efecto_neto_militar_robusto.png", replace as(png) width(2000)



* ==============================================================================
* 9. COMBINACIÓN MAESTRA (Dashboard 2x2)
* ==============================================================================
graph combine g1 g2 g3 g4, ///
    cols(2) rows(2) iscale(*0.9) ///
    title("{bf:ESTRUCTURA DE LA CRISIS DEL IESS: 1990-2024}", size(medium)) ///
    subtitle("Dashboard Multidimensional: Demografía, Seguridad y Fiscalidad" + ///
             " | Panel 4 corregido por raíz unitaria (HAC Newey-West)", ///
             size(vsmall) color(gs8)) ///
    note("Fuente: Elaboración propia con datos de BM e IESS. Base 100=1990." + ///
         " Panel 4: ADF + BG + NW aplicados; ver log diagnostics_p4.log", ///
         size(tiny)) ///
    graphregion(color(white))

* ==============================================================================
* 10. Exportar Dashboard Final
* ==============================================================================
graph export "`out'/00_dashboard_maestro_v2.png", replace as(png) width(3500)


di "=========================================================="
di "DASHBOARD v2 GENERADO — Panel 4 econométricamente robusto"
di "Log diagnósticos: assets/stata_visuals/diagnostics_p4.log"
di "=========================================================="