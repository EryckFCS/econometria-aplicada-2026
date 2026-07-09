* ==============================================================================
* Script: analysis.do
* Propósito: Estimación de datos de panel cantonal
*   VD: ln_empleo | VI: ln_vab
*   C1: ln_ventas  C2: num_emp  C3: participacion_provincial
* Autor: Erick Condoy | Fecha: 2026-06-29
* ==============================================================================

clear all
macro drop _all
capture log close

local base_path "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u3-acd-01-datos-de-panel-entregable"
log using "`base_path'/logs/stata_panel_estimation.log", replace

* 2. Importar base
import delimited "`base_path'/data/processed/panel_cantonal_consolidado.csv", ///
    stringcols(3) clear

* 3. Preprocesamiento
encode codigo_canton, gen(canton_id_num)
encode vab_group,     gen(vab_group_num)

* 4. Panel
xtset canton_id_num anio, yearly
label list vab_group_num
tab vab_group vab_group_num, miss

* 5. Estadísticas descriptivas
xtsum empleo_prom vab ventas_totales num_emp participacion_provincial

* 6. Transformaciones logarítmicas
gen ln_empleo = ln(empleo_prom)
gen ln_vab    = ln(vab)
gen ln_ventas = ln(ventas_totales)

* 7. Diagnóstico de colinealidad
collin ln_vab ln_ventas num_emp participacion_provincial
pwcorr ln_empleo ln_vab ln_ventas num_emp participacion_provincial, ///
    star(.01) bonferroni

* ==============================================================================
* 8. MODELO GLOBAL
* ==============================================================================

* --- HAUSMAN: FE y RE sin cluster (requerimiento del test) ---
quietly xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial, fe
estimates store fe_hausman

quietly xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial, re
estimates store re_hausman

hausman fe_hausman re_hausman, sigmamore

* --- MODELO REPORTABLE: FE con errores cluster (heteroscedasticidad confirmada) ---
xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial, ///
    fe vce(cluster canton_id_num)
estimates store fixed

* --- Two-way FE con cluster ---
xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial ///
    i.anio, fe vce(cluster canton_id_num)
estimates store fixed_twoway

* --- Test de heteroscedasticidad (sobre FE sin cluster) ---
quietly xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial, fe
xttest3

* ==============================================================================
* 9. MODELOS POR SUBGRUPO
* vab_group_num: 1=Alto  2=Bajo  3=Medio
* ==============================================================================

* --- VAB Alto ---
quietly xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial ///
    if vab_group_num==1, fe
estimates store fe_h_alto
quietly xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial ///
    if vab_group_num==1, re
estimates store re_h_alto
hausman fe_h_alto re_h_alto, sigmamore

xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial ///
    if vab_group_num==1, fe vce(cluster canton_id_num)
estimates store fixed_alto

* --- VAB Medio ---
quietly xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial ///
    if vab_group_num==3, fe
estimates store fe_h_medio
quietly xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial ///
    if vab_group_num==3, re
estimates store re_h_medio
hausman fe_h_medio re_h_medio, sigmamore

xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial ///
    if vab_group_num==3, fe vce(cluster canton_id_num)
estimates store fixed_medio

* --- VAB Bajo ---
quietly xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial ///
    if vab_group_num==2, fe
estimates store fe_h_bajo
quietly xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial ///
    if vab_group_num==2, re
estimates store re_h_bajo
hausman fe_h_bajo re_h_bajo, sigmamore

xtreg ln_empleo ln_vab ln_ventas num_emp participacion_provincial ///
    if vab_group_num==2, fe vce(cluster canton_id_num)
estimates store fixed_bajo

* ==============================================================================
* 10. TABLA COMPARATIVA (modelos FE con cluster)
* ==============================================================================
estimates table fixed fixed_twoway fixed_alto fixed_medio fixed_bajo, ///
    b(%9.4f) se stats(N r2_w r2_b r2_o)

log close
exit