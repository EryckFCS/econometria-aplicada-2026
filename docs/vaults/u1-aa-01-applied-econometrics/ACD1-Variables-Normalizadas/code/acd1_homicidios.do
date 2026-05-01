****************************************************
* ACD1: MODELOS DINAMICOS - HOMICIDIOS ECUADOR
* Pipeline Automatizado - Bóveda de Evidencia
****************************************************

clear all
set more off

*--------------------------------------------------*
* 0) Configuración de Rutas (Relativas al script)
*--------------------------------------------------*
* El archivo vive en /docs/evidence/U1-Applied-Econometrics/ACD1-Variables-Normalizadas/code/
local data_input  "../../../../../data/raw/panel_raw.csv"
local output_word "../resultados_acd1.rtf"

*--------------------------------------------------*
* 1) Cargar y Filtrar Data
*--------------------------------------------------*
import delimited "`data_input'", clear 

* Filtrar solo Ecuador para este ejercicio
* Asumimos que la columna es 'iso2' o 'country'
capture keep if iso2 == "EC"

*--------------------------------------------------*
* 2) Mapeo Forense de Variables
*    Nuestro sistema ya entrega nombres limpios
*--------------------------------------------------*
* h_homicidios (VC.IHR.PSRC.P5)
* p_pobreza    (SI.POV.DDAY)
* g_gini       (SI.POV.GINI)
* i_inflacion  (FP.CPI.TOTL.ZG)

* Si los nombres vienen con el slug de la API, los normalizamos:
capture rename h_homicidios h
capture rename p_pobreza pobreza
capture rename g_gini gini
capture rename i_inflacion inflacion

*--------------------------------------------------*
* 3) Declarar Serie Temporal
*--------------------------------------------------*
destring year, replace
tsset year, yearly

*--------------------------------------------------*
* 4) Modelado
*--------------------------------------------------*
estimates clear

* M1: Autorregresivo
reg h L(1/2).h pobreza gini inflacion
estimates store Autorregresivo

* M2: Rezago Distribuido
reg h L(0/2).pobreza gini inflacion
estimates store Rezago_Distributivo

* M3: Dinámico General
reg h L(1/2).h L(0/2).pobreza gini inflacion
estimates store Dinamico_General

*--------------------------------------------------*
* 5) Exportación Automática a la "Oficina" (docs/)
*--------------------------------------------------*
capture which esttab
if _rc ssc install estout

esttab Autorregresivo Rezago_Distributivo Dinamico_General ///
using "`output_word'", ///
replace t ar2 compress label ///
title("Tabla 1. Modelos dinámicos: tasa de homicidios en Ecuador (Automatizado)") ///
nonumbers mtitles("AR(2)" "DL(2)" "General")

di "✅ Proceso completado. Reporte generado en: `output_word'"
