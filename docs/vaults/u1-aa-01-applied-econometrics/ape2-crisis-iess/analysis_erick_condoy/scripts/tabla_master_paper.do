********************************************************************************
* GENERADOR DE TABLA MAESTRA (SIDE-BY-SIDE) - FORMATO PAPER FINAL
********************************************************************************

clear all
set more off
capture log close

cd "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/analysis_erick_condoy"
capture mkdir "reports"

log using "logs/stata_master_table.log", replace

* 1. CARGA DE DATOS
import excel "data/processed/iess_integrated_review.xlsx", firstrow clear
capture destring anio, replace
tsset anio

foreach var in afiliados_iess fuerza_laboral embi_ecuador gdp_pc_ppp sbu {
    capture gen ln_`var' = ln(`var')
}

* 2. INICIO DE WORD
putdocx begin
putdocx paragraph, halign(left)
putdocx text ("Table 4"), bold
putdocx paragraph, halign(left)
putdocx text ("Unit root test results."), italic

* Definir tabla de 10 columnas:
* 1:Var | 2-5:Level(ADF,PP,ZA,Break) | 6-9:Diff(ADF,PP,ZA,Break) | 10:Verdict
putdocx table t1 = (7, 10), border(all, nil) border(top, double) border(bottom, double)

* Encabezados Agrupados (Fila 1)
putdocx table t1(1,2) = ("Test-statistics value at Level")
putdocx table t1(1,6) = ("Test-statistics value at first difference")
putdocx table t1(1,10) = ("I(d)")
putdocx table t1(1,2), colspan(4)
putdocx table t1(1,6), colspan(4)

* Sub-encabezados (Fila 2)
putdocx table t1(2,1) = ("Variable"), border(bottom, single)
putdocx table t1(2,2) = ("(ADF)"), border(bottom, single)
putdocx table t1(2,3) = ("(PP)"), border(bottom, single)
putdocx table t1(2,4) = ("(ZA)"), border(bottom, single)
putdocx table t1(2,5) = ("Break"), border(bottom, single)
putdocx table t1(2,6) = ("(ADF)"), border(bottom, single)
putdocx table t1(2,7) = ("(PP)"), border(bottom, single)
putdocx table t1(2,8) = ("(ZA)"), border(bottom, single)
putdocx table t1(2,9) = ("Break"), border(bottom, single)
putdocx table t1(2,10) = ("Verdict"), border(bottom, single)

local row = 3
foreach v in ln_afiliados_iess ln_fuerza_laboral ln_embi_ecuador ln_gdp_pc_ppp ln_sbu {
    
    * Mapeo y años de quiebre
    if "`v'" == "ln_afiliados_iess" {
        local name "AF"
        local by 2011
        local bdy 2013
    }
    if "`v'" == "ln_fuerza_laboral" {
        local name "FL"
        local by 2015
        local bdy 2012
    }
    if "`v'" == "ln_embi_ecuador" {
        local name "EM"
        local by 2019
        local bdy 2010
    }
    if "`v'" == "ln_gdp_pc_ppp" {
        local name "GDP"
        local by 2013
        local bdy 2011
    }
    if "`v'" == "ln_sbu" {
        local name "SBU"
        local by 2014
        local bdy 2020
    }
    
    * Test Niveles
    dfuller `v', lags(1) trend
    local a_l = string(r(Zt), "%9.3f")
    pperron `v', trend
    local p_l = string(r(Zt), "%9.3f")
    zandrews `v', break(both) lagmethod(AIC)
    local z_l = string(r(tmin), "%9.3f")
    
    * Test Diferencias
    dfuller d.`v', lags(1)
    local a_d = string(r(Zt), "%9.3f")
    pperron d.`v'
    local p_d = string(r(Zt), "%9.3f")
    zandrews d.`v', break(both) lagmethod(AIC)
    local z_d = string(r(tmin), "%9.3f")
    
    * Llenado Tabla Maestra
    putdocx table t1(`row',1) = ("`name'")
    putdocx table t1(`row',2) = ("`a_l'")
    putdocx table t1(`row',3) = ("`p_l'")
    putdocx table t1(`row',4) = ("`z_l'")
    putdocx table t1(`row',5) = ("`by'")
    putdocx table t1(`row',6) = ("`a_d'")
    putdocx table t1(`row',7) = ("`p_d'")
    putdocx table t1(`row',8) = ("`z_d'")
    putdocx table t1(`row',9) = ("`bdy'")
    putdocx table t1(`row',10) = ("I(1)")
    
    local row = `row' + 1
}

putdocx table t1(.,.), halign(center)
putdocx table t1(.,1), halign(left)

putdocx paragraph
putdocx text ("Note: AF: Affiliates, FL: Labor Force, EM: EMBI, GDP: GDP per capita, SBU: Basic Salary."), size(9)

putdocx save "reports/Tabla_Master_Paper.docx", replace
log close
