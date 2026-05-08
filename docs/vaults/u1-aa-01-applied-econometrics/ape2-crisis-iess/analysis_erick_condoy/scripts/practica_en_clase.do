* ------------------------------------------------------------------------------
* PROYECTO: Sostenibilidad del IESS (1990-2024)
* TAREA: Secuencia Académica de Análisis Dinámico (VAR -> Granger -> Johansen)
* ------------------------------------------------------------------------------

clear all
set more off
capture log close

* 1. Entorno de Trabajo
cd "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/analysis_erick_condoy"

capture mkdir "logs"
capture mkdir "assets"
log using "logs/practica_en_clase.log", replace text

* 2. Ingesta y Curación de Datos
import delimited "data/base_analisis.csv", clear 
tsset anio

* ------------------------------------------------------------------------------
* 2.1 DIAGNÓSTICO DE RAÍZ UNITARIA (Alineado a 4 rezagos)
* ------------------------------------------------------------------------------
* Se aplican 4 rezagos para corregir autocorrelación en Homicidios y Afiliados
foreach v in afiliados_iess gasto_militar_pib migracion_neta tasa_homicidios fuerza_laboral {
    di "ADF Test (Diff) with 4 Lags: `v'"
    quietly dfuller d.`v', lags(4) trend
}

* 3. Transformaciones logarítmicas
gen AF = ln(afiliados_iess)
gen GM = gasto_militar_pib
gen MI = migracion_neta
gen HO = ln(tasa_homicidios)
gen FL = ln(fuerza_laboral)

* ------------------------------------------------------------------------------
* 3. SECUENCIA DE ESTIMACIÓN DINÁMICA
* ------------------------------------------------------------------------------

* --- PASO 1: Estimación VAR Inicial (Exploratoria) ---
var AF GM MI HO FL

* --- PASO 2: Selección de Rezagos Óptimos ---
di _newline(2) ">>> TABLA 1: SELECCIÓN DE REZAGOS <<<"
varsoc AF GM MI HO FL

* --- PASO 3: Estimación del Modelo VAR Final (Lag 4) ---
* Se utiliza el rezago sugerido por la mayoría de criterios (AIC, HQIC, SBIC)
var AF GM MI HO FL, lags(1/4)

* --- PASO 4: Diagnóstico de Residuos (Generación de Errores) ---
capture drop error
predict error, resid
label variable error "Residuos del Modelo VAR"

* --- PASO 5: Causalidad de Granger (Sistema Completo) ---
di _newline(2) ">>> TABLA 2: CAUSALIDAD DE GRANGER (MULTIVARIADA) <<<"
vargranger

* --- PASO 6: Análisis de Causalidad en Parejas (Y con cada X) ---
di _newline(2) ">>> ANÁLISIS DE CAUSALIDAD POR PAREJAS <<<"
foreach v in GM MI HO FL {
    di _newline "Análisis: AF vs `v'"
    quietly var AF `v', lags(1/4)
    vargranger
}

* --- PASO 7: Cointegración de Johansen ---
di _newline(2) ">>> TABLA 3: COINTEGRACIÓN DE JOHANSEN <<<"
vecrank AF GM MI HO FL, trend(constant)

* ------------------------------------------------------------------------------
* 4. FINALIZACIÓN
* ------------------------------------------------------------------------------
di _newline(2) "=========================================================="
di " SECUENCIA ECONOMÉTRICA FINALIZADA."
di "=========================================================="

capture log close
exit
