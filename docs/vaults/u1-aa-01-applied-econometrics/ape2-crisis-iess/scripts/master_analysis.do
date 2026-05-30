* ----------------------------------------------------------------------------
* TITULO: Crisis del IESS - Master Analysis Pipeline
* DESCRIPCIÓN: VAR/Johansen + ARDL + Diagnósticos de Robustez + Gráficos
* AUTOR: Erick Fabricio Condoy Seraquive
* FECHA: 2026-05-14
* ----------------------------------------------------------------------------

* 0. Configuración Inicial e Idempotencia
clear all
set more off
capture log close
graph close _all

* 1. Configuración de Directorio y Log
local user "/home/erick-fcs"
local project "`user'/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/analysis_erick_condoy"
cd "`project'"

capture mkdir "logs"
capture mkdir "assets"
log using "logs/master_econometric_pipeline.log", replace text

* 0.1 Instalación de Comandos Necesarios
foreach cmd in zandrews ardl estout krls {
    capture which `cmd'
    if _rc ssc install `cmd'
}

* 2. Ingesta y Preparación de Datos
local dta_file "data/base_analisis.dta"
local csv_file "data/base_analisis.csv"

capture use "`dta_file'", clear
if _rc {
    di ">>> Base .dta no encontrada. Intentando importar .csv..."
    capture import delimited "`csv_file'", clear
    if _rc {
        di ">>> Error Crítico: No se encontró ni .dta ni .csv en data/."
        exit 199
    }
    save "`dta_file'", replace
    di ">>> Base convertida y guardada en formato .dta para mayor velocidad."
}
tsset anio

* 3. Transformaciones Logarítmicas
capture drop AF GM MI HO FL
gen AF = ln(afiliados_iess)
gen GM = gasto_militar_pib
gen MI = migracion_neta
gen HO = ln(tasa_homicidios)
gen FL = ln(fuerza_laboral)

* Etiquetado profesional
label variable AF "Log Afiliados IESS"
label variable GM "Gasto Militar (% del PIB)"
label variable MI "Migración Neta"
label variable HO "Log Tasa Homicidios"
label variable FL "Log Fuerza Laboral"

* ----------------------------------------------------------------------------
* SECCIÓN 1: ANÁLISIS DESCRIPTIVO Y VISUALIZACIÓN (@tbl-resumen, @tbl-vif, @fig-tendencias)
* ----------------------------------------------------------------------------

* 1.1 Estadísticos Descriptivos
di as text "{hline}"
di as res "ESTADÍSTICOS DESCRIPTIVOS (@tbl-resumen)"
di as text "{hline}"
summarize AF GM MI HO FL, detail

* 1.2 Auditoría de Multicolinealidad (@tbl-vif)
regress AF GM MI HO FL
estat vif

* 1.3 Visualización de Tendencias en un Solo Panel (@fig-tendencias)
* Calcular índices Base 100 en 1990 para variables de escala positiva.
* Para la Migración Neta, aplicamos normalización Min-Max [0, 100].

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

graph export "assets/fig-tendencias-stata.png", replace width(3200)

* ----------------------------------------------------------------------------
* SECCIÓN 2: DIAGNÓSTICO DINÁMICO (@tbl-rezagos, @tbl-granger, @tbl-johansen)
* ----------------------------------------------------------------------------

* 2.1 Selección de Rezagos Óptimos
di _newline(2) ">>> TABLA: SELECCIÓN DE REZAGOS <<<"
varsoc AF GM MI HO FL

* 2.2 Estimación VAR (Lag 4)
var AF GM MI HO FL, lags(1/4)

* 2.3 Causalidad de Granger y Bloque de Exogeneidad
di _newline(2) ">>> TABLA: CAUSALIDAD DE GRANGER (Wald Tests) <<<"
vargranger
di "Nota: El test 'ALL' representa la Causalidad de Bloque (Block Exogeneity)."

* 2.4 Cointegración de Johansen (Rango)
di _newline(2) ">>> TABLA: COINTEGRACIÓN DE JOHANSEN (Traza) <<<"
vecrank AF GM MI HO FL, trend(constant)

* 2.5 Modelo VEC (Vector Error Correction) y Diagnósticos (G. Johansen)
di _newline(2) ">>> ESTIMACIÓN DEL MODELO VEC (r=2) <<<"
vec AF GM MI HO FL, rank(2) lags(4)
estimates store VEC_Model

* Diagnósticos de Residuos VEC
di ">>> Diagnóstico de Residuos VEC <<<"
veclmar, mlag(2)   // Autocorrelación (LM Test)
vecnorm             // Normalidad
vecstable, graph    // Estabilidad
graph export "assets/vec_stability.png", replace

* ----------------------------------------------------------------------------
* SECCIÓN 3: PRUEBAS DE RAÍZ UNITARIA CON QUIEBRE (@tbl-za)
* ----------------------------------------------------------------------------
foreach v in AF GM MI HO FL {
    di as text ">>> Variable (Levels): `v'"
    zandrews `v', break(both) lagmethod(AIC)
}

foreach v in AF GM MI HO FL {
    di as text ">>> Variable (Diffs): `v'"
    zandrews d.`v', break(both) lagmethod(AIC)
}

* ----------------------------------------------------------------------------
* SECCIÓN 4: ESTIMACIÓN ARDL Y MECANISMO DE AJUSTE (@tbl-ardl-sr, @tbl-ardl-lp)
* ----------------------------------------------------------------------------

* 4.1 Modelo ARDL Final
ardl AF GM MI HO FL, maxlags(2) aic ec
estimates store ARDL_Final

* 4.2 Estabilidad Estructural (@fig-cusum)
capture drop r_ardl cumsum
predict r_ardl, resid
gen cumsum = sum(r_ardl)
line cumsum anio, title("Prueba CUSUM de Estabilidad", size(small)) yline(0, lcolor(red)) lcolor(navy) graphregion(color(white)) name(cumsum_plot, replace)
graph export "assets/cusum_plot.png", replace width(2000)

* ----------------------------------------------------------------------------
* SECCIÓN 5: PRUEBAS DE DIAGNÓSTICO Y ROBUSTEZ (Punto 3 solicitado)
* ----------------------------------------------------------------------------

* 5.1 Normalidad de Residuos (basado en OLS para diagnóstico)
regress AF GM MI HO FL
capture drop r_ols
predict r_ols, resid
sktest r_ols

* 5.2 Autocorrelación
estat bgodfrey, lags(1 2)

* 5.3 Heterocedasticidad (White Test)
estat imtest, white

* 5.4 Especificación (Ramsey RESET)
estat ovtest

* 5.5 Prueba Complementaria KRLS (Kernel-based Regularized Least Squares)
di _newline(2) ">>> PRUEBA ALTERNATIVA: KRLS (Non-linear effects) <<<"
krls AF GM MI HO FL

* ----------------------------------------------------------------------------
* 6. FINALIZACIÓN
* ----------------------------------------------------------------------------
log close
di "Master Pipeline Finalizado con Éxito."
