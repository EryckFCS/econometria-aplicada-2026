*==============================================================================*
* ANÁLISIS DE DATOS DE PANEL - AMÉRICA DEL SUR (1994-2023)
* Propuesta 2: Vulnerabilidad Financiera Externa y Presión Fiscal
*==============================================================================*

clear all
macro drop _all

* Capturar ruta base del script y cambiar el directorio de trabajo
cd "`c(pwd)'"
capture log close

* Cambiar directorio al del script para homogeneizar entorno de ejecución
capture cd "Z:\home\erick-fcs\Documentos\universidad\07_Ciclo\septimo_ciclo\applied_econometrics_2026\docs\vaults\u3-acd-01-datos-de-panel\scripts"
capture cd "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u3-acd-01-datos-de-panel/scripts"

* Abrir log
log using "../logs/stata_panel_estimation.log", replace text

di "======================================================================"
di "INICIO DEL PROCESO DE ESTIMACIÓN DE PANEL - AMÉRICA DEL SUR (PROP 2)"
di "======================================================================"

* Importar los datos de panel balanceados de América del Sur
import excel "../data/panel_data.xlsx", sheet("data") firstrow clear

* Convertir la variable de país a numérica para el xtset de Stata
encode country, gen(country_id)

* Configurar dimensiones del panel
xtset country_id year

* Generar transformaciones logarítmicas (excepto para RI que tiene valores negativos)
gen log_VE = log(VE)
gen log_PF = log(PF)
gen log_IE = log(IE)
gen log_AN = log(AN)
gen val_RI = RI

* Describir y resumir las variables
xtdes
xtsum log_VE log_PF log_IE log_AN val_RI

*==============================================================================*
* 1. ESTIMACIÓN DEL MODELO DE EFECTOS FIJOS (FE)
*==============================================================================*
di ""
di ">>> ESTIMACIÓN DEL MODELO DE EFECTOS FIJOS (FE) <<<"
xtreg log_VE log_PF log_IE log_AN val_RI, fe
estimates store fe_model

*==============================================================================*
* 2. ESTIMACIÓN DEL MODELO DE EFECTOS ALEATORIOS (RE)
*==============================================================================*
di ""
di ">>> ESTIMACIÓN DEL MODELO DE EFECTOS ALEATORIOS (RE) <<<"
xtreg log_VE log_PF log_IE log_AN val_RI, re
estimates store re_model

*==============================================================================*
* 3. TEST DE ESPECIFICACIÓN DE HAUSMAN
*==============================================================================*
di ""
di ">>> TEST DE HAUSMAN <<<"
hausman fe_model re_model

*==============================================================================*
* 4. GRÁFICOS DE EVOLUCIÓN
*==============================================================================*
di ""
di ">>> GENERANDO GRÁFICOS DE EVOLUCIÓN TEMPORAL <<<"

* Visualizar evolución de la variable dependiente VE promedio
preserve
    collapse (mean) VE, by(year)
    twoway (line VE year, lcolor(navy) lwidth(medthick)), ///
           title("Evolución Temporal de la Vulnerabilidad Externa (VE) Promedio") ///
           xtitle("Año") ytitle("Rentas de Recursos Naturales (% del PIB)") ///
           xlabel(1994(3)2023, grid)
    graph export "../assets/evolution_dependent_stata.png", replace
restore

di "======================================================================"
di "PROCESO FINALIZADO CON ÉXITO"
di "======================================================================"

log close
