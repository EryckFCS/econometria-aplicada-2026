* ----------------------------------------------------------------------------
* Crisis del IESS - Master Analysis Pipeline
* Autor: Erick Fabricio Condoy Seraquive
* ----------------------------------------------------------------------------

clear all
set more off
capture log close
graph close _all

local user "/home/erick-fcs"
local project "`user'/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess"
cd "`project'"

capture mkdir "logs"
capture mkdir "assets"
log using "logs/master_econometric_pipeline.log", replace text

* 1. Requisitos
foreach cmd in zandrews ardl estout krls {
    capture which `cmd'
    if _rc ssc install `cmd'
}

* 2. Ingesta de Datos
local dta_file "data/base_analisis.dta"
local csv_file "data/base_analisis.csv"

capture use "`dta_file'", clear
if _rc {
    capture import delimited "`csv_file'", clear
    if _rc {
        di "ERROR: No data file found."
        exit 199
    }
    save "`dta_file'", replace
}
tsset anio

* 3. Transformaciones Logarítmicas
capture drop AF GM MI HO FL
gen AF = ln(afiliados_iess)
gen GM = gasto_militar_pib
gen MI = migracion_neta
gen HO = ln(tasa_homicidios)
gen FL = ln(fuerza_laboral)

label variable AF "Log Afiliados IESS"
label variable GM "Gasto Militar (% del PIB)"
label variable MI "Migración Neta"
label variable HO "Log Tasa Homicidios"
label variable FL "Log Fuerza Laboral"

* 4. Análisis Descriptivo y Multicolinealidad
summarize AF GM MI HO FL, detail
regress AF GM MI HO FL
estat vif

* 5. Visualización de Tendencias
set scheme s1color
local graph_opts "msize(small) xlabel(1990(10)2024, labsize(vsmall)) ylabel(, labsize(vsmall)) xtitle("Año", size(vsmall)) graphregion(color(white)) plotregion(color(white))"

gen af_millones = afiliados_iess / 1000000
twoway (line af_millones anio, lcolor(navy) lwidth(medium) `graph_opts'), title("Afiliados (Millones)", size(vsmall)) ytitle("Millones", size(vsmall)) name(g1, replace)

twoway (line gasto_militar_pib anio, lcolor(orange) lwidth(medium) `graph_opts'), title("Gasto Militar (% PIB)", size(vsmall)) ytitle("Porcentaje", size(vsmall)) name(g2, replace)

twoway (line tasa_homicidios anio, lcolor(red) lwidth(medium) `graph_opts'), title("Tasa de Homicidios", size(vsmall)) ytitle("Tasa", size(vsmall)) name(g3, replace)

gen mi_miles = migracion_neta / 1000
twoway (line mi_miles anio, lcolor(green) lwidth(medium) `graph_opts'), title("Migración Neta (Miles)", size(vsmall)) ytitle("Miles", size(vsmall)) name(g4, replace)

gen fl_millones = fuerza_laboral / 1000000
twoway (line fl_millones anio, lcolor(purple) lwidth(medium) `graph_opts'), title("Fuerza Laboral (Millones)", size(vsmall)) ytitle("Millones", size(vsmall)) name(g5, replace)

graph combine g1 g2 g3 g4 g5, cols(3) iscale(0.9) title("Determinantes de la Crisis del IESS", size(small)) graphregion(color(white))
graph export "assets/fig-tendencias-stata.png", replace width(3200)

* 6. Selección de Rezagos y VAR
varsoc AF GM MI HO FL
var AF GM MI HO FL, lags(1/4)

* 7. Causalidad de Granger
vargranger

* 8. Cointegración de Johansen y VEC
vecrank AF GM MI HO FL, trend(constant)
vec AF GM MI HO FL, rank(2) lags(4)
estimates store VEC_Model

* 9. Diagnósticos de Residuos VEC
veclmar, mlag(2)
vecnorm
vecstable, graph
graph export "assets/vec_stability.png", replace

* 10. Raíz Unitaria con Quiebre (Zivot-Andrews)
foreach v in AF GM MI HO FL {
    zandrews `v', break(both) lagmethod(AIC)
}
foreach v in AF GM MI HO FL {
    zandrews d.`v', break(both) lagmethod(AIC)
}

* 11. Modelo ARDL
ardl AF GM MI HO FL, maxlags(2) aic ec
estimates store ARDL_Final

* 12. Estabilidad CUSUM
capture drop r_ardl cumsum
predict r_ardl, resid
gen cumsum = sum(r_ardl)
line cumsum anio, title("Prueba CUSUM de Estabilidad", size(small)) yline(0, lcolor(red)) lcolor(navy) graphregion(color(white)) name(cusum_plot, replace)
graph export "assets/cusum_plot.png", replace width(2000)

* 13. Diagnósticos de Robustez
regress AF GM MI HO FL
capture drop r_ols
predict r_ols, resid
sktest r_ols
estat bgodfrey, lags(1 2)
estat imtest, white
estat ovtest

* 14. Modelo KRLS (Efectos No Lineales)
krls AF GM MI HO FL

log close
