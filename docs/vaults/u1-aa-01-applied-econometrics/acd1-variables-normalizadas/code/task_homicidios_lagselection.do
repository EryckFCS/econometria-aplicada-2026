********************************************************************************
* Proyecto: Econometría Aplicada 2026
* Tarea: Selección de Rezagos Óptimos (p, q)
* Bóveda de Evidencia: ACD1
********************************************************************************

clear all
set more off
capture log close

* 0. CONFIGURACIÓN DE ENTORNO Y LOGS (Rutas Relativas)
* El archivo vive en /docs/vaults/U1-Applied-Econometrics/ACD1-Variables-Normalizadas/code/

* Iniciar log estructurado
local log_date : display %tdCCYYNNDD date(c(current_date), "DMY")
log using "../../../../../logs/stata/LagSelection_Homicidios_`log_date'.log", replace

/*
   CONCLUSIÓN PREVIA (Basada en resultados presentados):
   1. Sistema Bivariado: Todos los criterios (AIC, SBIC, HQIC) sugieren 2 rezagos.
   2. Homicidios: Dinámica persistente de 2 rezagos.
   3. Desempleo: Sugiere 0 rezagos (comportamiento de ruido blanco o shocks exógenos).
   
   RECOMENDACIÓN TÉCNICA: Usar un modelo con 2 rezagos (p=2) para capturar 
   correctamente la inercia de la tasa de homicidios.
*/

* 1. IMPORTAR DATOS
local data_path "../../../../../data/raw/csv/Base_Raw_Ecuador_Homicidios_Long.csv"
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
di "✅ RECOMENDACIÓN FINAL:"
di "1. Usa p=2 para Homicidios (basado en su propia inercia)."
di "2. Para los controles, usa rezago 0 o 1 para no agotar la muestra."

log close
********************************************************************************
* Fin del script
********************************************************************************
