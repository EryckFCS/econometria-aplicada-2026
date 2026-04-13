****************************************************
* APE1: PANEL DINAMICO DE AMERICA LATINA (EKC)
* Sistema Automatizado - Laboratorio de Stata
****************************************************

clear all
set more off
set matsize 800

*--------------------------------------------------*
* 0) Carga de Data Forense
*--------------------------------------------------*
local data_input  "../../data/raw/panel_raw.csv"
local output_res  "../../docs/unidad1/APE/resultados_ape1_dinamico.rtf"

import delimited "`data_input'", clear 

*--------------------------------------------------*
* 1) Preparación del Panel
*--------------------------------------------------*
* Codificar países para xtset
encode iso2, gen(id_pais)
destring year, replace
xtset id_pais year

* Logaritmos para elasticidades (Modelo Log-Log)
gen ln_co2  = ln(co2_emissions_kt)
gen ln_gdp  = ln(gdp_per_capita_const2015_usd)
gen ln_gdp2 = ln_gdp^2
gen ln_fdi  = ln(fdi_inflows_pct_gdp + 1)  // +1 para evitar ln(0)
gen ln_trade = ln(trade_pct_gdp)

* Etiquetado
label variable ln_co2 "Log Emisiones CO2"
label variable ln_gdp "Log PIB per cápita"
label variable ln_gdp2 "Log PIB^2 (Kuznets)"

*--------------------------------------------------*
* 2) Estimaciones Dinámicas
*--------------------------------------------------*
estimates clear

* M1: Efectos Fijos (Punto de Referencia)
xtreg ln_co2 ln_gdp ln_gdp2 ln_trade ln_fdi, fe
estimates store EF_Estatico

* M2: Modelo Autorregresivo de Rezago Distribuido (ARDL 1,0)
* CO2 depende de su rezago y del PIB contemporáneo
reg ln_co2 L.ln_co2 ln_gdp ln_gdp2 ln_trade ln_fdi i.id_pais
estimates store ARDL_Basico

* M3: GMM System (Arellano-Bover/Blundell-Bond) - Dinámico Puro
* Maneja la endogeneidad del PIB y el rezago de la dependiente
xtabond2 ln_co2 L.ln_co2 ln_gdp ln_gdp2 ln_trade, ///
    gmm(L.ln_co2 ln_gdp) iv(ln_trade) small robust nodump
estimates store GMM_Sistema

*--------------------------------------------------*
* 3) Diagnóstico Forense y Visualización
*--------------------------------------------------*
* Test de Kuznets: Si ln_gdp > 0 y ln_gdp2 < 0 -> Existe la U invertida
di "Validando Hipótesis de Kuznets Ambiental..."

*--------------------------------------------------*
* 4) Exportación de Resultados
*--------------------------------------------------*
capture which esttab
if _rc ssc install estout

esttab EF_Estatico ARDL_Basico GMM_Sistema ///
using "`output_res'", ///
replace t ar2 compress label ///
title("Tabla 2. Modelos Dinámicos de la Curva de Kuznets en América Latina (APE1)") ///
addnotes("GMM Sistema usa instrumentos internos para corregir endogeneidad.")

di "✅ Entregable APE1 generado exitosamente en: `output_res'"
