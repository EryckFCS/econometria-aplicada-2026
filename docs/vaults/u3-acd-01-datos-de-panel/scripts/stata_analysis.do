clear all
macro drop _all
set more off
set graphics off
set seed 42

// Dependencias
capture ssc install collin
capture ssc install xttest3
capture ssc install estout
capture ssc install xthst
capture ssc install xtcdf

// Entorno y logs
cd "`c(pwd)'"
capture log close
capture cd "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u3-acd-01-datos-de-panel/scripts"
log using "../logs/stata_panel_estimation.log", replace text

// Importar y preparar panel balanceado (2001-2023)
import excel "../data/panel_data.xlsx", sheet("data") firstrow clear
keep if year >= 2001

encode country, gen(country_id)
xtset country_id year

// Transformación logarítmica de variables
gen log_VE = log(VE)
gen log_PF = log(PF)
gen log_IE = log(IE)
gen log_AN = log(AN)
gen log_RI = log(RI)

// Grupos por patrón de especialización primaria (1: Hidrocarburos, 2: Minero-Agropecuario)
gen grupo_especializacion = 1 if country == "Bolivia" | country == "Colombia" | country == "Ecuador" | country == "Venezuela"
replace grupo_especializacion = 2 if grupo_especializacion == . & country != ""
label define espec_lbl 1 "Hidrocarburos" 2 "Minero-Agropecuario"
label values grupo_especializacion espec_lbl

// Descriptivos y correlación global y subgrupos
xtdes
xtsum log_VE log_PF log_IE log_AN log_RI
xtsum log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 1
xtsum log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 2

collin log_PF log_IE log_AN log_RI
pwcorr log_VE log_PF log_IE log_AN log_RI, star(.01) bonferroni

collin log_PF log_IE log_AN log_RI if grupo_especializacion == 1
pwcorr log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 1, star(.01) bonferroni

collin log_PF log_IE log_AN log_RI if grupo_especializacion == 2
pwcorr log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 2, star(.01) bonferroni

// Test de Hausman: elección entre un modelo de efectos fijos y aleatorios
// Global
xtreg log_VE log_PF log_IE log_AN log_RI, fe
estimates store fe_global
xtreg log_VE log_PF log_IE log_AN log_RI, re
estimates store re_global
hausman fe_global re_global, sigmamore

// Hidrocarburos (Subgrupo 1)
xtreg log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 1, fe
estimates store fe_hidro
xtreg log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 1, re
estimates store re_hidro
hausman fe_hidro re_hidro, sigmamore

// Minero-Agropecuario (Subgrupo 2)
xtreg log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 2, fe
estimates store fe_minagro
xtreg log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 2, re
estimates store re_minagro
hausman fe_minagro re_minagro, sigmamore

// Detección de autocorrelación mediante Test de Wooldridge
xtserial log_VE log_PF log_IE log_AN log_RI
xtregar log_VE log_PF log_IE log_AN log_RI, fe

xtserial log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 1
xtregar log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 1, fe

xtserial log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 2
xtregar log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 2, fe

// Detección de heterocedasticidad mediante Test de Wald
quietly xtreg log_VE log_PF log_IE log_AN log_RI, fe
xttest3

quietly xtreg log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 1, fe
xttest3

quietly xtreg log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 2, fe
xttest3

// Estimación de modelos corregidos (FGLS)
xtgls log_VE log_PF log_IE log_AN log_RI, p(h) c(ar1)
estimates store gls_global

xtgls log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 1, p(h) c(ar1)
estimates store gls_hidro

xtgls log_VE log_PF log_IE log_AN log_RI if grupo_especializacion == 2, p(h) c(ar1)
estimates store gls_minagro

// Exportación de estimaciones corregidas
esttab gls_global gls_hidro gls_minagro using "../logs/Resultados_Paises_GLS.rtf", ///
    scalars(F chi2) t ar2 compress label ///
    title("Tabla comparativa de estimaciones FGLS: Global vs Subgrupos de Especialización") ///
    nonumbers mtitles("FGLS Global" "FGLS Hidrocarburos" "FGLS Minero-Agropecuario") replace

// Test for slope homogeneity de Pesaran y Yamagata (2008)
xthst log_VE log_PF log_IE log_AN log_RI

// Prueba de dependencia de las secciones transversales CD de Pesaran
xtcdf log_VE log_PF log_IE log_AN log_RI

// Gráficos de evolución temporal
preserve
    collapse (mean) VE, by(year)
    twoway (line VE year, lcolor(navy) lwidth(medthick)), ///
           title("Evolución Temporal de la Vulnerabilidad Externa (VE) Promedio") ///
           xtitle("Año") ytitle("Rentas de Recursos Naturales (% del PIB)") ///
           xlabel(2001(2)2023, grid)
    graph export "../assets/evolution_dependent_stata.png", replace
restore

log close
