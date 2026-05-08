* ----------------------------------------------------------------------------
* TITULO: Crisis del IESS
* DESCRIPCIÓN: OLS, Diagnósticos Gauss-Markov, Cointegración y Quiebre Único (ZA)
* AUTOR: Erick Fabricio Condoy Seraquive
* FECHA: 2026-05-07
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

log using "logs/econometric_audit.log", replace text

* 0.1 Instalación de Comandos (Zandrews, ARDL, Estout)
foreach cmd in zandrews ardl estout {
    capture which `cmd'
    if _rc ssc install `cmd'
}

* 2. Cargar y Preparar Datos
import delimited "data/base_analisis.csv", clear 
tsset anio

* 3. Generación de Variables (Log-Transformaciones)
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
* PASO 3.1: VISUALIZACIÓN DE TENDENCIAS (STATA GRAPHICS)
* ----------------------------------------------------------------------------
set scheme s1color

* Opciones generales optimizadas
local graph_opts "msize(small) xlabel(1990(10)2024, labsize(vsmall)) ylabel(, labsize(vsmall)) xtitle("Año", size(vsmall)) graphregion(color(white)) plotregion(color(white))"

* 1. Afiliados (Millones)
gen af_millones = afiliados_iess / 1000000
twoway (line af_millones anio, lcolor(navy) lwidth(medium) `graph_opts'), title("Afiliados (Millones)", size(vsmall)) ytitle("Millones", size(vsmall)) name(g1, replace)

* 2. Gasto Militar
twoway (line gasto_militar_pib anio, lcolor(orange) lwidth(medium) `graph_opts'), title("Gasto Militar (% PIB)", size(vsmall)) ytitle("Porcentaje", size(vsmall)) name(g2, replace)

* 3. Tasa de Homicidios
twoway (line tasa_homicidios anio, lcolor(red) lwidth(medium) `graph_opts'), title("Tasa de Homicidios", size(vsmall)) ytitle("Tasa", size(vsmall)) name(g3, replace)

* 4. Migración Neta (Miles)
gen mi_miles = migracion_neta / 1000
twoway (line mi_miles anio, lcolor(green) lwidth(medium) `graph_opts'), title("Migración Neta (Miles)", size(vsmall)) ytitle("Miles", size(vsmall)) name(g4, replace)

* 5. Fuerza Laboral (Millones)
gen fl_millones = fuerza_laboral / 1000000
twoway (line fl_millones anio, lcolor(purple) lwidth(medium) `graph_opts'), title("Fuerza Laboral (Millones)", size(vsmall)) ytitle("Millones", size(vsmall)) name(g5, replace)

* Combinar las 5 variables en una matriz de 2x3 para máxima claridad
graph combine g1 g2 g3 g4 g5, cols(3) iscale(0.9) title("Determinantes de la Crisis del IESS", size(small)) graphregion(color(white))
graph export "assets/fig-tendencias-stata.png", replace width(3200)

* 3.2 Estadísticos Descriptivos y Auditoría de Correlación
* ----------------------------------------------------------------------------
di as text "{hline}"
di as res "PASO 3.2: ESTADÍSTICOS DESCRIPTIVOS Y MATRIZ DE CORRELACIÓN"
di as text "{hline}"
summarize AF GM MI HO FL, detail
correlate AF GM MI HO FL

* Auditoría de Multicolinealidad (VIF)
regress AF GM MI HO FL
estat vif

* ----------------------------------------------------------------------------
* PASO 4: PRUEBAS DE RAÍZ UNITARIA CON QUIEBRE ESTRUCTURAL (ZA)
* ----------------------------------------------------------------------------
foreach v in AF GM MI HO FL {
    di as text ">>> Variable (Levels): `v'"
    dfuller `v', trend lags(1)
    pperron `v', trend
    zandrews `v', break(both) lagmethod(AIC)
}

foreach v in AF GM MI HO FL {
    di as text ">>> Variable (Diffs): `v'"
    dfuller d.`v', trend lags(1)
    pperron d.`v', trend
    zandrews d.`v', break(both) lagmethod(AIC)
}

* 5. ESTIMACIÓN JERÁRQUICA Y DIAGNÓSTICO CLÁSICO
* ----------------------------------------------------------------------------
regress AF GM MI HO FL
estimates store Modelo_Final

* --- Diagnósticos de Residuos ---
capture drop r_ols
predict r_ols, resid
sktest r_ols
estat hettest
estat bgodfrey, lags(1 2)
estat ovtest

* 6. ANÁLISIS DE COINTEGRACIÓN ARDL (Pesaran et al., 2001)
* ----------------------------------------------------------------------------
ardl AF GM MI HO FL, maxlags(2) aic ec
capture estat btest
if _rc estat bounds

* 7. ESTABILIDAD ESTRUCTURAL (CUSUM sobre Residuos ARDL)
* ----------------------------------------------------------------------------
capture drop r_ardl cumsum
predict r_ardl, resid
gen cumsum = sum(r_ardl)
line cumsum anio, title("Prueba CUSUM de Estabilidad (Residuos ARDL)", size(small)) yline(0, lcolor(red)) lcolor(navy) graphregion(color(white)) plotregion(color(white)) xtitle("Año", size(vsmall)) ylabel(, labsize(vsmall)) xlabel(, labsize(vsmall)) name(cusum_plot, replace)
graph export "assets/cusum_plot.png", replace width(2000)

* 8. CIERRE
log close
di "Ejecución de Máxima Robustez finalizada."
