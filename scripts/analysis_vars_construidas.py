import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS, RandomEffects
import statsmodels.api as sm

# 1. Configuración de rutas y carga de datos
base_path = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u3-acd-01-datos-de-panel-entregable"
df = pd.read_csv(f"{base_path}/data/processed/panel_cantonal_consolidado.csv")

# 2. Construcción de variables
df["LE"] = np.log(df["empleo_prom"])
df["PR"] = np.log(df["vab"] / df["empleo_prom"])
df["PR2"] = df["PR"] ** 2
df["TE"] = np.log(df["ventas_totales"] / df["num_emp"])
df["DE"] = np.log(df["empleo_prom"] / df["num_emp"])
df["PP"] = df["participacion_provincial"]

# Categorizar subgrupos de VAB
# Mapeo: Alto = 1, Bajo = 2, Medio = 3 para coincidir con la codificación de Stata
vab_map = {"Alto": 1, "Bajo": 2, "Medio": 3}
df["vab_group_num"] = df["vab_group"].map(vab_map)

# Configurar índice de panel
df = df.set_index(["codigo_canton", "anio"])

def hausman_test(fe_model, re_model):
    """
    Realiza el test de Hausman comparando estimaciones de Efectos Fijos y Efectos Aleatorios.
    H0: La diferencia en los coeficientes no es sistemática (RE es eficiente y consistente).
    """
    b = fe_model.params
    B = re_model.params
    
    # Filtrar solo las variables explicativas comunes (excluyendo la constante)
    common_cols = [col for col in b.index if col != "const" and col in B.index]
    b = b[common_cols]
    B = B[common_cols]
    
    v_b = fe_model.cov.loc[common_cols, common_cols]
    v_B = re_model.cov.loc[common_cols, common_cols]
    
    df_df = len(common_cols)
    
    # Calcular diferencia y matriz de covarianza de la diferencia
    diff = b - B
    cov_diff = v_b - v_B
    
    # Pseudo-inversa por si hay colinealidad
    try:
        inv_cov_diff = np.linalg.pinv(cov_diff)
        chi2 = float(diff.T @ inv_cov_diff @ diff)
        from scipy.stats import chi2 as chi2_dist
        p_val = 1 - chi2_dist.cdf(chi2, df_df)
    except Exception:
        chi2 = np.nan
        p_val = np.nan
    
    return chi2, p_val

def wooldridge_test_panel(df_group, dep_var, indep_vars):
    """
    Test de autocorrelación de Wooldridge para datos de panel.
    1. Estimar el modelo en primeras diferencias.
    2. Regresionar los residuos diferenciados contemporáneos sobre sus rezagos.
    3. Probar si el coeficiente de la autocorrelación de los residuos en diferencias es -0.5.
    """
    # Hacer diferencias
    df_diff = df_group[[dep_var] + indep_vars].groupby(level=0).diff().dropna()
    
    # Regresión en diferencias (OLS)
    y_diff = df_diff[dep_var]
    X_diff = sm.add_constant(df_diff[indep_vars])
    model_diff = sm.OLS(y_diff, X_diff).fit()
    resids = model_diff.resid
    
    # Crear rezagos de los residuos por cantón
    resids_df = pd.DataFrame({"resid": resids}, index=df_diff.index)
    resids_df["resid_lag"] = resids_df.groupby(level=0)["resid"].shift(1)
    resids_df = resids_df.dropna()
    
    # Regresión de resid sobre resid_lag
    y_r = resids_df["resid"]
    X_r = resids_df["resid_lag"]  # Sin constante
    
    # Usar errores estándar agrupados por cantón (clúster) para la prueba
    # Agrupamos por el nivel 0 del índice (codigo_canton)
    groups = resids_df.index.get_level_values(0)
    ols_r = sm.OLS(y_r, X_r).fit(cov_type='cluster', cov_kwds={'groups': groups})
    
    coef = ols_r.params["resid_lag"]
    se = ols_r.bse["resid_lag"]
    
    # H0: coef = -0.5
    t_stat = (coef - (-0.5)) / se
    from scipy.stats import t
    p_val = 2 * (1 - t.cdf(np.abs(t_stat), ols_r.df_resid))
    
    return coef, p_val

# Ejecutar diagnósticos para cada grupo
grupos = {
    "Global": df,
    "VAB Alto (Grupo 1)": df[df["vab_group_num"] == 1],
    "VAB Bajo (Grupo 2)": df[df["vab_group_num"] == 2],
    "VAB Medio (Grupo 3)": df[df["vab_group_num"] == 3],
}

print("="*80)
print("DIAGNÓSTICOS DE PANEL EN PYTHON (ESPEJO DE STATA)")
print("="*80)

for name, data in grupos.items():
    print(f"\n>>> Análisis para el grupo: {name} ({len(data)} observaciones)")
    
    # 1. Definir variables
    # Para ver la especificación base (lineal)
    dep = "LE"
    indeps = ["PR", "TE", "DE", "PP"]
    
    # Estimar FE y RE
    fe = PanelOLS(data[dep], data[indeps], entity_effects=True).fit()
    re = RandomEffects(data[dep], sm.add_constant(data[indeps])).fit()
    
    # Test de Hausman
    chi2, h_p = hausman_test(fe, re)
    decision_hausman = "Efectos Fijos (FE)" if h_p < 0.05 else "Efectos Aleatorios (RE)"
    print(f"  * Test de Hausman: Chi2 = {chi2:.4f}, p-value = {h_p:.4f} -> Sugiere {decision_hausman}")
    
    # Test de Autocorrelación de Wooldridge
    coef_ar, ar_p = wooldridge_test_panel(data.reset_index().set_index(["codigo_canton", "anio"]), dep, indeps)
    decision_ar = "Sí hay autocorrelación (rechaza H0)" if ar_p < 0.05 else "No hay autocorrelación (no rechaza H0)"
    print(f"  * Test de Wooldridge (AR1): Coeficiente = {coef_ar:.4f}, p-value = {ar_p:.4f} -> {decision_ar}")
    
    # Test de Wald para heterocedasticidad (descriptivo por varianzas cruzadas)
    # Obtenemos los residuos de FE
    fe_resids = fe.resids
    var_by_entity = fe_resids.groupby(level=0).var()
    ratio_var = var_by_entity.max() / var_by_entity.min()
    print(f"  * Ratio de varianzas Max/Min entre cantones: {ratio_var:.2f} (Valores altos sugieren Heterocedasticidad)")
print("="*80)
