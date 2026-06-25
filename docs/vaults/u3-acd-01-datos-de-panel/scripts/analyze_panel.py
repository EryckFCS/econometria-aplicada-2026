"""
Script de análisis de Datos de Panel para el dataset de América del Sur (panel_data.xlsx).
Propuesta 2: Vulnerabilidad Financiera Externa y Presión Fiscal.
Usa variables de 2 letras en mayúscula (VE, PF, IE, AN, RI).
Realiza estimación de Efectos Fijos (FE), Efectos Aleatorios (RE) y el test de Hausman.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, RandomEffects
from loguru import logger

# Configurar rutas
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(VAULT_DIR, "data", "panel_data.xlsx")
ASSETS_DIR = os.path.join(VAULT_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

def analyze_south_america_panel():
    logger.info("Cargando datos de panel de América del Sur (VE, PF, IE, AN, RI)...")
    df = pd.read_excel(DATA_PATH, sheet_name="data")
    
    # Aplicar logaritmos para estimar en elasticidades
    df["log_VE"] = np.log(df["VE"])
    df["log_PF"] = np.log(df["PF"])
    df["log_IE"] = np.log(df["IE"])
    df["log_AN"] = np.log(df["AN"])
    # RI es un índice con valores negativos, se modela en niveles
    df["val_RI"] = df["RI"]
    
    # Configurar multi-índice para linearmodels
    df = df.set_index(["country", "year"])
    
    dependent = df["log_VE"]
    exogenous = sm.add_constant(df[[
        "log_PF", "log_IE", "log_AN", "val_RI"
    ]])
    
    logger.info("Estimando Modelo de Efectos Fijos (FE)...")
    model_fe = PanelOLS(dependent, exogenous, entity_effects=True).fit()
    print("\n==============================================")
    print("MODELO DE EFECTOS FIJOS (FE) - AMÉRICA DEL SUR")
    print("==============================================")
    print(model_fe.summary)
    
    logger.info("Estimando Modelo de Efectos Aleatorios (RE)...")
    model_re = RandomEffects(dependent, exogenous).fit()
    print("\n==============================================")
    print("MODELO DE EFECTOS ALEATORIOS (RE) - AMÉRICA DEL SUR")
    print("==============================================")
    print(model_re.summary)
    
    # Test de Hausman manual
    logger.info("Calculando el Test de Hausman...")
    b_fe = model_fe.params.drop("const")
    b_re = model_re.params.drop("const")
    
    cov_fe = model_fe.cov.drop("const", axis=0).drop("const", axis=1)
    cov_re = model_re.cov.drop("const", axis=0).drop("const", axis=1)
    
    b_diff = b_fe - b_re
    cov_diff = cov_fe - cov_re
    
    try:
        chi2 = np.dot(np.dot(b_diff.T, np.linalg.inv(cov_diff)), b_diff)
        dof = b_diff.shape[0]
        from scipy import stats
        p_val = 1 - stats.chi2.cdf(chi2, dof)
        
        print("\n==============================================")
        print("TEST DE ESPECIFICACIÓN DE HAUSMAN")
        print("==============================================")
        print(f"Estadístico Chi2: {chi2:.4f}")
        print(f"Grados de libertad: {dof}")
        print(f"P-valor: {p_val:.4f}")
        if p_val < 0.05:
            print("Resultado: Rechaza H0 (Efectos Aleatorios son consistentes).")
            print("Conclusión: Se prefiere el modelo de EFECTOS FIJOS (FE).")
        else:
            print("Resultado: No rechaza H0.")
            print("Conclusión: Se prefiere el modelo de EFECTOS ALEATORIOS (RE).")
        print("==============================================")
    except np.linalg.LinAlgError:
        logger.warning("Error de matriz singular al calcular el Test de Hausman.")
        
    # Visualización
    plt.figure(figsize=(10, 6))
    coef_fe = model_fe.params.drop("const")
    coef_re = model_re.params.drop("const")
    err_fe = model_fe.std_errors.drop("const")
    err_re = model_re.std_errors.drop("const")
    
    x = np.arange(len(coef_fe))
    width = 0.35
    
    plt.bar(x - width/2, coef_fe, width, yerr=err_fe, label='Efectos Fijos (FE)', color='#2b5c8f', capsize=5)
    plt.bar(x + width/2, coef_re, width, yerr=err_re, label='Efectos Aleatorios (RE)', color='#d95f02', capsize=5)
    
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.xticks(x, coef_fe.index)
    plt.title('Comparación de Coeficientes: Vulnerabilidad Externa (FE vs RE)', fontsize=12)
    plt.ylabel('Valor del Coeficiente')
    plt.legend()
    plt.tight_layout()
    plot_path = os.path.join(ASSETS_DIR, "coef_comparison.png")
    plt.savefig(plot_path)
    logger.info(f"Gráfico comparativo guardado en {plot_path}")

if __name__ == "__main__":
    analyze_south_america_panel()
