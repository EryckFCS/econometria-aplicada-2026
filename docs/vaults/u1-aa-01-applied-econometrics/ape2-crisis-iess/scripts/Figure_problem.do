* ----------------------------------------------------------------------------
* Crisis del IESS - Radiografía del Problema
* Autor: Erick Fabricio Condoy Seraquive
* ----------------------------------------------------------------------------

clear all
set more off
capture log close
graph close _all

local project_path "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess"
capture cd "`project_path'"
pwd

capture mkdir "logs"
capture mkdir "assets"

log using "logs/Figure_problem.log", replace text

* 1. Carga de Datos
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

* 2. Cálculo de Variables
gen cobertura = (afiliados_iess / fuerza_laboral) * 100
label variable cobertura "Tasa de Cobertura Previsional (%)"

gen migracion_miles = migracion_neta / 1000
label variable migracion_miles "Migración Neta (Miles de personas)"

gen ln_homicidios = ln(tasa_homicidios)
label variable ln_homicidios "Log Tasa Homicidios"

gen growth_afiliados = (afiliados_iess - L.afiliados_iess) / L.afiliados_iess * 100
label variable growth_afiliados "Crecimiento Anual de Afiliados (%)"

* 3. Análisis Descriptivo y Regresión
correlate cobertura tasa_homicidios gasto_militar_pib migracion_miles
regress cobertura tasa_homicidios gasto_militar_pib migracion_miles

* 4. Normalización de Series (Base 100 = 1990)
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

* 5. Gráfico de Evolución Temporal
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

log close
