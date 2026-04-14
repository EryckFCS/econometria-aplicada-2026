********************************************************************************
* Proyecto: Econometría Aplicada 2026
* Tarea: Selección de Rezagos Óptimos (p, q)
* Datos: Ecuador Homicidios vs Desempleo (2004-2023)
********************************************************************************

clear all
set more off
capture log close

* 0. CONFIGURACIÓN DE ENTORNO Y LOGS
cd "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/econometria-aplicada-2026"

* Iniciar log estructurado
local log_date : display %tdCCYYNNDD date(c(current_date), "DMY")
log using "logs/stata/LagSelection_Homicidios_`log_date'.log", replace

/*
   CONCLUSIÓN PREVIA (Basada en resultados presentados):
   1. Sistema Bivariado: Todos los criterios (AIC, SBIC, HQIC) sugieren 2 rezagos.
   2. Homicidios: Dinámica persistente de 2 rezagos.
   3. Desempleo: Sugiere 0 rezagos (comportamiento de ruido blanco o shocks exógenos).
   
   RECOMENDACIÓN TÉCNICA: Usar un modelo con 2 rezagos (p=2) para capturar 
   correctamente la inercia de la tasa de homicidios.
*/

* 1. IMPORTAR DATOS
local data_path "data/raw/csv/Base_Raw_Ecuador_Homicidios_Long.csv"
di "📥 Cargando base: `data_path'"
import delimited "`data_path'", clear

* 2. DECLARAR SERIE DE TIEMPO
tsset year

* 3. VALIDACIÓN DE MUESTRA Y GRADOS DE LIBERTAD
* Contamos observaciones con datos completos
quietly count if homicidios_100k != . & desempleo_total_ne != .
local n_obs = r(N)
di "📊 Muestra efectiva para análisis: `n_obs' años."

* 4. SELECCIÓN DE REZAGOS ÓPTIMOS (p y q)
/*
   Usamos 'varsoc' para obtener los criterios de información formales:
   AIC: Akaike Information Criterion
   HQIC: Hannan-Quinn Information Criterion
   SBIC: Schwarz's Bayesian Information Criterion
   FPE: Final Prediction Error
   
   IMPORTANTE: Con N=`n_obs', un maxlag(1) o maxlag(2) es lo más prudente
   para no agotar los grados de libertad.
*/

di ""
di "-----------------------------------------------------------------------"
di "🔎 CRITERIO FORMAL DE REZAGOS (VARSOC) - SISTEMA BIVARIADO"
di "-----------------------------------------------------------------------"
varsoc homicidios_100k desempleo_total_ne, maxlag(2)

di ""
di "-----------------------------------------------------------------------"
di "🔎 EVALUACIÓN INDIVIDUAL (Dinámica de p)"
di "-----------------------------------------------------------------------"
di "Homicidios (Variable Dependiente):"
varsoc homicidios_100k, maxlag(3)

di "Desempleo (Variable Independiente):"
varsoc desempleo_total_ne, maxlag(3)

di ""
di "-----------------------------------------------------------------------"
di "🔎 SELECCIÓN INCLUYENDO CONTROLES (Multivariante)"
di "-----------------------------------------------------------------------"
/*
   Aquí incluimos las variables de control no tradicionales:
   - uso_internet_pct
   - gasto_militar_pct_pib
   - remesas_pct_pib
   
   ADVERTENCIA: Al aumentar el número de variables en varsoc, se pierden 
   grados de libertad exponencialmente. Con N=18, un sistema de 5 variables
   con 2 rezagos es matemáticamente inestable.
*/

varsoc homicidios_100k desempleo_total_ne uso_internet_pct gasto_militar_pct_pib remesas_pct_pib, maxlag(1)

di ""
di "⚠️ NOTA SOBRE GRADOS DE LIBERTAD (GL):"
di "Con 5 variables y 1 rezago, estás estimando muchos parámetros para solo 18 datos."
di "En la práctica académica, se suele usar el rezago (p) hallado en el sistema"
di "bivariado y las variables de control entran de forma contemporánea o con 1 rezago fijo."

di ""
di "✅ RECOMENDACIÓN FINAL:"
di "1. Usa p=2 para Homicidios (basado en su propia inercia)."
di "2. Para los controles, usa rezago 0 o 1 para no agotar la muestra."

log close
********************************************************************************
* Fin del script
********************************************************************************
