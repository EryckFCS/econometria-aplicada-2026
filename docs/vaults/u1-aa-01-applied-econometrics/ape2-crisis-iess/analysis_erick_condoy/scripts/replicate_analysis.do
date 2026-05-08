* ----------------------------------------------------------------------------
* TITULO: Análisis Econométrico de Ultra-Robustez - Crisis del IESS
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

log using "logs/replicate_analysis_ultra_robust.log", replace text

* 0.1 Instalación de Comandos (Zandrews, ARDL, Estout)
foreach cmd in zandrews ardl estout {
    capture which `cmd'
    if _rc ssc install `cmd'
}

* 2. Cargar y Preparar Datos
import delimited "data/base_analisis.csv", clear 
tsset anio

* 3. Generación de Variables (Log-Transformaciones)
capture drop AF DE MI HO GM RN
gen AF = ln(afiliados_iess)
gen DE = ln(tasa_dependencia_vejez)
gen MI = migracion_neta
gen HO = ln(tasa_homicidios)
gen GM = ln(gasto_militar_pib)
gen RN = ln(rentas_recursos_naturales_pib)

* Etiquetado profesional
label variable AF "Log Afiliados IESS"
label variable DE "Log Tasa Dependencia Vejez"
label variable MI "Migración Neta"
label variable HO "Log Tasa Homicidios"
label variable GM "Log Gasto Militar (% PIB)"
label variable RN "Log Rentas Nat. (% PIB)"

* 4. VALIDACIÓN DE ESTACIONARIEDAD CON QUIEBRE ÚNICO (Zivot-Andrews)
* ----------------------------------------------------------------------------
* Nota: Se opta por un quiebre único para preservar grados de libertad y 
* enfocarse en el evento estructural dominante (reformas 2010).
di as text "{hline}"
di as res "PASO 4: PRUEBAS DE RAÍZ UNITARIA CON QUIEBRE ESTRUCTURAL (ZA)"
di as text "{hline}"

foreach v in AF DE MI HO GM RN {
    di as text ">>> Variable: `v'"
    dfuller `v', trend lags(1)
    pperron `v', trend
    zandrews `v', break(both) lagmethod(AIC)
}

* 5. ESTIMACIÓN JERÁRQUICA Y DIAGNÓSTICO CLÁSICO
* ----------------------------------------------------------------------------
di as text "{hline}"
di as res "PASO 5: MODELOS JERÁRQUICOS Y DIAGNÓSTICOS DE GAUSS-MARKOV"
di as text "{hline}"

regress AF DE MI HO GM RN
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
di as text "{hline}"
di as res "PASO 6: MODELO ARDL Y BOUNDS TEST (Relación de Largo Plazo)"
di as text "{hline}"

ardl AF DE MI HO GM RN, maxlags(2) aic ec
capture estat btest
if _rc estat bounds

* 7. ESTABILIDAD ESTRUCTURAL (CUSUM sobre Residuos ARDL)
* ----------------------------------------------------------------------------
capture drop r_ardl cumsum
predict r_ardl, resid
gen cumsum = sum(r_ardl)
line cumsum anio, title("Prueba CUSUM de Estabilidad (Residuos ARDL)") yline(0) name(cusum_plot, replace)

* 8. CIERRE
log close
di "Ejecución de Máxima Robustez (Quiebre Único) finalizada."
