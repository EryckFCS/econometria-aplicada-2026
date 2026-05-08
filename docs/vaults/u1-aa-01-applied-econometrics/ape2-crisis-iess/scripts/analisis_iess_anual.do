********************************************************************************
* ANALISIS IESS - TABLAS SEPARADAS (NIVELES Y DIFERENCIAS)
********************************************************************************

clear all
set more off
capture log close

cd "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/"
capture mkdir "reports"
capture mkdir "assets"
capture mkdir "logs"

log using "logs/stata_integrated_word_export.log", replace

* 1. CARGA Y PREPARACION
import excel "data/processed/iess_integrated_review.xlsx", firstrow clear
capture destring anio, replace
tsset anio

foreach var in afiliados_iess fuerza_laboral embi_ecuador gdp_pc_ppp sbu {
    capture gen ln_`var' = ln(`var')
}

* 2. ANALISIS Y EXPORTACION
putdocx begin
putdocx paragraph, halign(left)
putdocx text ("Econometric Results: Unit Root Analysis"), bold

* TABLA 1: NIVELES
putdocx paragraph, halign(left)
putdocx text ("Table 4.1: Test-statistics value at Level"), italic
putdocx table t1 = (6, 6), border(all, nil) border(top, single) border(bottom, single)
putdocx table t1(1,1) = ("Variable"), border(bottom, single)
putdocx table t1(1,2) = ("(ADF)"), border(bottom, single)
putdocx table t1(1,3) = ("(PP)"), border(bottom, single)
putdocx table t1(1,4) = ("(ZA)"), border(bottom, single)
putdocx table t1(1,5) = ("Break Year"), border(bottom, single)
putdocx table t1(1,6) = ("Verdict"), border(bottom, single)

* TABLA 2: DIFERENCIAS
putdocx paragraph
putdocx paragraph, halign(left)
putdocx text ("Table 4.2: Test-statistics value at first difference"), italic
putdocx table t2 = (6, 6), border(all, nil) border(top, single) border(bottom, single)
putdocx table t2(1,1) = ("Variable"), border(bottom, single)
putdocx table t2(1,2) = ("(ADF)"), border(bottom, single)
putdocx table t2(1,3) = ("(PP)"), border(bottom, single)
putdocx table t2(1,4) = ("(ZA)"), border(bottom, single)
putdocx table t2(1,5) = ("Break Year"), border(bottom, single)
putdocx table t2(1,6) = ("Verdict"), border(bottom, single)

local row = 2
foreach v in ln_afiliados_iess ln_fuerza_laboral ln_embi_ecuador ln_gdp_pc_ppp ln_sbu {
    
    * Mapeo y años de quiebre (Hardcoded por evidencia de LOG)
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
    
    * Llenado Tabla 1
    putdocx table t1(`row',1) = ("`name'")
    putdocx table t1(`row',2) = ("`a_l'")
    putdocx table t1(`row',3) = ("`p_l'")
    putdocx table t1(`row',4) = ("`z_l'")
    putdocx table t1(`row',5) = ("`by'")
    putdocx table t1(`row',6) = ("I(1)")
    
    * Llenado Tabla 2
    putdocx table t2(`row',1) = ("`name'")
    putdocx table t2(`row',2) = ("`a_d'")
    putdocx table t2(`row',3) = ("`p_d'")
    putdocx table t2(`row',4) = ("`z_d'")
    putdocx table t2(`row',5) = ("`bdy'")
    putdocx table t2(`row',6) = ("I(0)")
    
    local row = `row' + 1
}

putdocx table t1(.,.), halign(center)
putdocx table t1(.,1), halign(left)
putdocx table t2(.,.), halign(center)
putdocx table t2(.,1), halign(left)

putdocx save "reports/Tabla_Paper_Final.docx", replace
log close
