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

* 1.3 Visualización de Tendencias (@fig-tendencias)
set scheme s1color
local graph_opts "msize(small) xlabel(1990(10)2024, labsize(vsmall)) ylabel(, labsize(vsmall)) xtitle("Año", size(vsmall)) graphregion(color(white)) plotregion(color(white))"

* Generación de sub-gráficos
gen af_millones = afiliados_iess / 1000000
twoway (line af_millones anio, lcolor(navy) lwidth(medium) `graph_opts'), title("Afiliados (Millones)", size(vsmall)) ytitle("Millones", size(vsmall)) name(g1, replace)

twoway (line gasto_militar_pib anio, lcolor(orange) lwidth(medium) `graph_opts'), title("Gasto Militar (% PIB)", size(vsmall)) ytitle("Porcentaje", size(vsmall)) name(g2, replace)

twoway (line tasa_homicidios anio, lcolor(red) lwidth(medium) `graph_opts'), title("Tasa de Homicidios", size(vsmall)) ytitle("Tasa", size(vsmall)) name(g3, replace)

gen mi_miles = migracion_neta / 1000
twoway (line mi_miles anio, lcolor(green) lwidth(medium) `graph_opts'), title("Migración Neta (Miles)", size(vsmall)) ytitle("Miles", size(vsmall)) name(g4, replace)

gen fl_millones = fuerza_laboral / 1000000
twoway (line fl_millones anio, lcolor(purple) lwidth(medium) `graph_opts'), title("Fuerza Laboral (Millones)", size(vsmall)) ytitle("Millones", size(vsmall)) name(g5, replace)

* Combinar y exportar
graph combine g1 g2 g3 g4 g5, cols(3) iscale(0.9) title("Determinantes de la Crisis del IESS", size(small)) graphregion(color(white))
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
line cumsum anio, title("Prueba CUSUM de Estabilidad", size(small)) yline(0, lcolor(red)) lcolor(navy) graphregion(color(white)) name(cusum_plot, replace)
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
