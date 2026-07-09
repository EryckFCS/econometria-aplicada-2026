* ==============================================================================
* Script: analysis_vars_construidas.do
* Propósito: Panel cantonal con estimación robusta FGLS y diagnósticos
* Autor: Erick Condoy
* Fecha: 2026-07-02
* ==============================================================================

clear all
macro drop _all
capture log close

* 1. Configuración de rutas y logs
local base_path "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u3-acd-01-datos-de-panel-entregable"
log using "`base_path'/logs/stata_panel_vars_construidas.log", replace

* Dependencias
*capture ssc install collin
*capture ssc install xttest3
*capture ssc install estout
*capture ssc install xthst
*capture ssc install xtcdf
*capture ssc install xtdcce2
*capture net install st0039_1, from(http://www.stata-journal.com/software/sj5-1)

* 2. Importación y declaración del panel
import delimited "`base_path'/data/processed/panel_cantonal_consolidado.csv", stringcols(3) clear
encode codigo_canton, gen(canton_id_num)
encode vab_group,     gen(vab_group_num)
xtset canton_id_num anio, yearly

* 3. Construcción de variables
gen LE = ln(empleo_prom)
gen PR = ln(vab / empleo_prom)
gen PR2 = PR^2
gen TE = ln(ventas_totales / num_emp)
gen DE = ln(empleo_prom / num_emp)
gen PP = participacion_provincial

* 4. Descriptivos y diagnósticos iniciales
xtsum LE PR TE DE PP
collin PR TE DE PP
pwcorr LE PR TE DE PP, star(.01) bonferroni

* ==============================================================================
* 5. TEST DE HAUSMAN POR SUBGRUPO
* ==============================================================================

* Global
quietly xtreg LE PR TE DE PP, fe
estimates store fixed_global
quietly xtreg LE PR TE DE PP, re
estimates store random_global
hausman fixed_global random_global, sigmamore

* VAB Alto
quietly xtreg LE PR TE DE PP if vab_group_num==1, fe
estimates store fixed_alto
quietly xtreg LE PR TE DE PP if vab_group_num==1, re
estimates store random_alto
hausman fixed_alto random_alto, sigmamore

* VAB Bajo
quietly xtreg LE PR TE DE PP if vab_group_num==2, fe
estimates store fixed_bajo
quietly xtreg LE PR TE DE PP if vab_group_num==2, re
estimates store random_bajo
hausman fixed_bajo random_bajo, sigmamore

* VAB Medio
quietly xtreg LE PR TE DE PP if vab_group_num==3, fe
estimates store fixed_medio
quietly xtreg LE PR TE DE PP if vab_group_num==3, re
estimates store random_medio
hausman fixed_medio random_medio, sigmamore

* ==============================================================================
* 6. TEST DE WOOLDRIDGE Y MODELOS DE CORRECCIÓN (xtregar)
* ==============================================================================

* Global
xtserial LE PR TE DE PP
xtregar LE PR TE DE PP, fe

* VAB Alto
xtserial LE PR TE DE PP if vab_group_num==1
xtregar LE PR TE DE PP if vab_group_num==1, fe

* VAB Bajo
xtserial LE PR TE DE PP if vab_group_num==2
xtregar LE PR TE DE PP if vab_group_num==2, fe

* VAB Medio
xtserial LE PR TE DE PP if vab_group_num==3
xtregar LE PR TE DE PP if vab_group_num==3, fe

* ==============================================================================
* 7. TEST DE HETEROCEDASTICIDAD (Wald para FE)
* ==============================================================================

* Global
quietly xtreg LE PR TE DE PP, fe
xttest3

* VAB Alto
quietly xtreg LE PR TE DE PP if vab_group_num==1, fe
xttest3

* VAB Bajo
quietly xtreg LE PR TE DE PP if vab_group_num==2, fe
xttest3

* VAB Medio
quietly xtreg LE PR TE DE PP if vab_group_num==3, fe
xttest3

* ==============================================================================
* 8. MODELOS GLS CORREGIDOS (xtgls)
* ==============================================================================

* Global
xtgls LE PR PR2 TE DE PP, p(h) c(ar1)
estimates store gls_global

* VAB Alto
xtgls LE PR PR2 TE DE PP if vab_group_num==1, p(h) c(ar1)
estimates store gls_alto

* VAB Bajo
xtgls LE PR PR2 TE DE PP if vab_group_num==2, p(h) c(ar1)
estimates store gls_bajo

* VAB Medio
xtgls LE PR PR2 TE DE PP if vab_group_num==3, p(h) c(ar1)
estimates store gls_medio

* ==============================================================================
* 9. TABLA COMPARATIVA GLS Y PRUEBAS AVANZADAS
* ==============================================================================

esttab gls_global gls_alto gls_bajo gls_medio using "`base_path'/logs/Resultados_GLS.rtf", ///
    scalars(R_g r2_w r2_b r2_o r2_a F chi2) t ar2 compress label ///
    title("Tabla 2. Regresion de Panel mediante FGLS por subgrupos de VAB") ///
    nonumbers mtitles("Global" "VAB Alto" "VAB Bajo" "VAB Medio") replace

* Pruebas de Homogeneidad y CD
capture xthst LE PR TE DE PP
capture xtcdf LE PR TE DE PP
capture xtcse2 LE PR TE DE PP

log close
exit