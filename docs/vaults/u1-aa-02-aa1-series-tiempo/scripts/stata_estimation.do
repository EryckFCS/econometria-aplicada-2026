* 1. CONFIGURACIÓN DEL ENTORNO
clear all
set more off
capture log close

* Definición de rutas (Ruta absoluta según arquitectura v8.1.5)
local base_path "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-02-aa1-series-tiempo"
cd "`base_path'"

log using "logs/stata_output.log", replace

* 2. CARGA DE DATOS (DATASET EXPANDIDO)
import excel "data/aa1_expanded_data.xlsx", sheet("data") firstrow clear

* Configuración de Serie de Tiempo
tsset year

* 3. TRANSFORMACIONES Y LOGARITMOS
gen l_imports = ln(imports)
gen l_gdp = ln(gdp)

label var l_imports "Log de Importaciones"
label var l_gdp "Log del PIB Real"
label var fdi "IED (% PIB)"
label var oil_rent "Renta Petrolera (% PIB)"
label var inflation "Inflación (%)"

* 4. ANÁLISIS DE ESTACIONARIEDAD (UNIDADES RAÍCES)
display "===================================================="
display "PRUEBAS DE RAÍZ UNITARIA (ADF Y PHILLIPS-PERRON)"
display "===================================================="

foreach var in l_imports l_gdp fdi oil_rent inflation {
    display "Variable: `var'"
    dfuller `var', trend
    pperron `var', trend
}

* 5. SELECCIÓN DE REZAGOS Y CAUSALIDAD (MULTIVARIANTE)
di _newline(2) ">>> TABLA 1: SELECCIÓN DE REZAGOS (VAR) <<<"
varsoc l_imports l_gdp fdi oil_rent inflation, maxlag(4)

di _newline(2) ">>> TABLA 2: CAUSALIDAD DE GRANGER <<<"
var l_imports l_gdp fdi oil_rent inflation, lags(1/1)
vargranger

di _newline(2) ">>> TABLA 3: COINTEGRACIÓN DE JOHANSEN <<<"
vecrank l_imports l_gdp fdi oil_rent inflation, trend(constant)

* 6. ESTIMACIÓN DE MODELOS DINÁMICOS (SÍLABO: TEMAS 1.1 Y 1.2)
display "===================================================="
display "ESTIMACIÓN DE MODELOS COMPARATIVOS (5 VARIABLES)"
display "===================================================="

* Modelo 1: Lineal Estático
reg imports gdp fdi oil_rent inflation
estimates store m1

* Modelo 2: Log-Log Estático
reg l_imports l_gdp fdi oil_rent inflation
estimates store m2

* Modelo 3: ARDL(1, 0) Dinámico (Ajuste Parcial)
reg l_imports l_gdp L.l_imports fdi oil_rent inflation
estimates store m3

* Diagnóstico para M3 (Mejor Modelo)
estat bgodfrey, lags(1)
estat hettest
vif

* Visualización para M3
capture drop l_imports_hat
predict l_imports_hat, xb
label var l_imports_hat "Predicción ARDL"
line l_imports l_imports_hat year, ///
    title("Modelo de Importaciones con Controles") ///
    subtitle("Ecuador 1970-2021 (5 Variables)") ///
    ytitle("Logaritmo de Importaciones") ///
    xtitle("Año") ///
    legend(order(1 "Observado" 2 "Ajuste Dinámico")) ///
    note("Controles: IED, Renta Petrolera e Inflación.")
graph export "assets/stata_import_plot_expanded.png", replace as(png)

* Modelo 4: Modelo de Corrección de Errores (ECM)
capture drop res_m2
predict res_m2, resid
reg d.l_imports d.l_gdp d.fdi d.oil_rent d.inflation L.res_m2
estimates store m4

* 7. MODELOS ARIMA (SÍLABO: TEMA 1.3)
display "===================================================="
display "MODELO ARIMA (BOX-JENKINS)"
display "===================================================="
* Identificación (ACF/PACF)
corrgram d.l_imports, lags(10)
* Estimación ARIMA(1,1,1) como benchmark univariante
arima l_imports, arima(1,1,1) iterate(50) difficult
estimates store m_arima

* 8. MODELOS ARCH Y GARCH (SÍLABO: TEMA 1.4)
display "===================================================="
display "MODELOS DE VOLATILIDAD (ARCH/GARCH)"
display "===================================================="
* Test de efectos ARCH en los residuos del ARDL (M3)
quietly reg l_imports l_gdp L.l_imports fdi oil_rent inflation
archlm, lags(1)
* Estimación ARCH(1) - Simplificado para asegurar convergencia en muestra pequeña
display "Nota: Estimando ARCH(1) univariante para asegurar convergencia (N=52)"
arch l_imports, arch(1) iterate(50) difficult
estimates store m_garch

* 9. MODELOS DE ECUACIONES SIMULTÁNEAS (SÍLABO: TEMA 1.5)
display "===================================================="
display "ECUACIONES SIMULTÁNEAS (IV / 2SLS)"
display "===================================================="
* Hipótesis: El PIB es endógeno a las importaciones. 
* Instrumento: Renta Petrolera (fuente de divisas externa).
ivregress 2sls l_imports fdi inflation (l_gdp = oil_rent)
estimates store m_2sls

* 10. TABLA COMPARATIVA FINAL (COBERTURA TOTAL SÍLABO)
display _newline(2) ">>> TABLA FINAL: COBERTURA TOTAL DE LA UNIDAD 1 <<<"
estimates table m1 m2 m3 m4 m_arima m_garch m_2sls, b(%9.4f) star(0.1 0.05 0.01) stats(N r2 r2_a)

* --- CIERRE DE LOG ---
log close
