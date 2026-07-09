#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: analyze_panel.py
Propósito: Estimación y contrastes de datos de panel a nivel cantonal (Ecuador 2015-2024)
Usa variables construidas: LE, PR, PR2, TE, DE, PP.
Genera estimación de Efectos Fijos (FE), Efectos Aleatorios (RE), Test de Hausman y gráficos comparativos.
"""

import os
import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, RandomEffects, PooledOLS
from loguru import logger

# Configurar rutas
SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()
VAULT_DIR = SCRIPT_DIR.parent
DATA_FILE = VAULT_DIR / "data/panel_cantonal_consolidado.csv"
OUTPUT_DIR = VAULT_DIR / "logs"
ASSETS_DIR = VAULT_DIR / "assets"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

def calculate_hausman(fe_model, re_model):
    """
    Realiza el cálculo del Test de Hausman comparando Efectos Fijos y Efectos Aleatorios.
    H0: Efectos Aleatorios es consistente y eficiente.
    """
    b_fe = fe_model.params
    b_re = re_model.params
    
    # Excluir la constante en la comparación
    common_coefs = [c for c in b_fe.index if c in b_re.index and c != 'intercept' and c != 'const']
    
    b_fe = b_fe[common_coefs]
    b_re = b_re[common_coefs]
    
    v_fe = fe_model.cov.loc[common_coefs, common_coefs]
    v_re = re_model.cov.loc[common_coefs, common_coefs]
    
    b_diff = b_fe - b_re
    cov_diff = v_fe - v_re
    
    try:
        from scipy import stats
        chi2 = np.dot(np.dot(b_diff.T, np.linalg.inv(cov_diff)), b_diff)
        df = len(common_coefs)
        p_val = 1 - stats.chi2.cdf(chi2, df)
        return chi2, df, p_val
    except Exception as e:
        logger.error(f"Error al calcular Hausman: {e}")
        return np.nan, len(common_coefs), np.nan

def run_panel_analysis():
    logger.info(f"Cargando dataset cantonal de Ecuador en: {DATA_FILE}")
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"No se encontró el dataset en {DATA_FILE}")
        
    df = pd.read_csv(DATA_FILE)
    
    # Crear variables transformadas
    # [imputation] Tratamiento para asegurar valores positivos antes de log
    df = df[df["empleo_prom"] > 0]
    df = df[df["vab"] > 0]
    df = df[df["ventas_totales"] > 0]
    df = df[df["num_emp"] > 0]
    
    df["LE"] = np.log(df["empleo_prom"])
    df["PR"] = np.log(df["vab"] / df["empleo_prom"])
    df["PR2"] = df["PR"] ** 2
    df["TE"] = np.log(df["ventas_totales"] / df["num_emp"])
    df["DE"] = np.log(df["empleo_prom"] / df["num_emp"])
    df["PP"] = df["participacion_provincial"]
    
    # Formatear ID de cantón e índice de panel
    df["codigo_canton"] = df["codigo_canton"].astype(str).str.zfill(4)
    df = df.set_index(["codigo_canton", "anio"])
    
    # Definir variables dependiente e independientes
    Y = df["LE"]
    X_vars = ["PR", "TE", "DE", "PP"]
    X = df[X_vars]
    X_const = sm.add_constant(X)
    
    logger.info("Estimando Pooled OLS...")
    res_pooled = PooledOLS(Y, X_const).fit()
    
    logger.info("Estimando Efectos Fijos (FE)...")
    res_fe = PanelOLS(Y, X, entity_effects=True).fit()
    
    logger.info("Estimando Efectos Aleatorios (RE)...")
    res_re = RandomEffects(Y, X_const).fit()
    
    # Hausman
    chi2, df_h, p_val = calculate_hausman(res_fe, res_re)
    
    # Escribir log de resultados en Python
    log_file = OUTPUT_DIR / "python_panel_estimation.log"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("=== ESTIMACIÓN ECONOMÉTRICA EN PYTHON - EMPLEO CANTONAL ===\n\n")
        f.write("--- POOLED OLS ---\n")
        f.write(str(res_pooled.summary) + "\n\n")
        f.write("--- FIXED EFFECTS (FE) ---\n")
        f.write(str(res_fe.summary) + "\n\n")
        f.write("--- RANDOM EFFECTS (RE) ---\n")
        f.write(str(res_re.summary) + "\n\n")
        f.write("--- TEST DE HAUSMAN ---\n")
        f.write(f"Chi-cuadrado: {chi2:.4f}\n")
        f.write(f"Grados de libertad: {df_h}\n")
        f.write(f"p-valor: {p_val:.4e}\n")
        
    logger.info(f"Estimación econométrica finalizada. Resultados guardados en: {log_file}")
    logger.info(f"Test de Hausman: Chi2 = {chi2:.4f}, p-valor = {p_val:.4e}")
    
    # Generar gráfico comparativo de coeficientes
    plt.figure(figsize=(10, 6))
    coef_fe = res_fe.params
    coef_re = res_re.params.drop("const")
    err_fe = res_fe.std_errors
    err_re = res_re.std_errors.drop("const")
    
    x = np.arange(len(coef_fe))
    width = 0.35
    
    plt.bar(x - width/2, coef_fe, width, yerr=err_fe, label='Efectos Fijos (FE)', color='#2b5c8f', capsize=5)
    plt.bar(x + width/2, coef_re, width, yerr=err_re, label='Efectos Aleatorios (RE)', color='#d95f02', capsize=5)
    
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.xticks(x, coef_fe.index)
    plt.title('Comparación de Coeficientes: Demanda de Empleo Formal (FE vs RE)', fontsize=12)
    plt.ylabel('Coeficiente estimado')
    plt.legend()
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.tight_layout()
    
    plot_path = ASSETS_DIR / "coef_comparison.png"
    plt.savefig(plot_path)
    logger.info(f"Gráfico de coeficientes guardado en {plot_path}")

if __name__ == "__main__":
    run_panel_analysis()
