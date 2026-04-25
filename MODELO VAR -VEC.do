
tsset anios, yearly
help var

***genero los rezagos****
gen dh = D1.homicidios
gen dPIB = D1.pib

****modelo var 
var dh dPIB

*****causalidad***
vargranger

****grafico del modelo de Brigton y Candelo***
bcgcausality dPIB dh
bcgcausality dh dPIB