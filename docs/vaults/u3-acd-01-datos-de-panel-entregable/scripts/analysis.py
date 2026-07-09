#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: analysis.py
Propósito: Estimación y contrastes de datos de panel a nivel cantonal
Autor: Erick Condoy
Fecha: 2026-06-29
"""

import pathlib
import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import PooledOLS, PanelOLS, RandomEffects

# Definir rutas
BASE_DIR = pathlib.Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u3-acd-01-datos-de-panel-entregable")
DATA_FILE = BASE_DIR / "data/processed/panel_cantonal_consolidado.csv"
OUTPUT_DIR = BASE_DIR / "logs"

def calculate_hausman(fe_model, re_model):
    """
    Realiza el cálculo del Test de Hausman comparando Efectos Fijos y Efectos Aleatorios.
    H0: Efectos Aleatorios es consistente y eficiente.
    """
    # Extraer coeficientes y matrices de covarianza
    b_fe = fe_model.params
    b_re = re_model.params
    
    # Filtrar solo intercepto de b_re si existe en RE pero no en FE
    common_coefs = [c for c in b_fe.index if c in b_re.index and c != 'intercept']
    
    b_fe = b_fe[common_coefs]
    b_re = b_re[common_coefs]
    
    v_fe = fe_model.cov.loc[common_coefs, common_coefs]
    v_re = re_model.cov.loc[common_coefs, common_coefs]
    
    # Calcular estadística de Hausman
    diff_coef = b_fe - b_re
    diff_cov = v_fe - v_re
    
    try:
        from scipy import stats
        # Inversa generalizada en caso de singularidad
        chi2 = np.dot(np.dot(diff_coef.T, np.linalg.inv(diff_cov)), diff_coef)
        df = len(common_coefs)
        p_val = 1 - stats.chi2.cdf(chi2, df)
        return chi2, df, p_val
    except Exception as e:
        print(f"Error al calcular Hausman: {e}")
        return np.nan, len(common_coefs), np.nan

def main():
    print("Iniciando análisis econométrico en Python...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"No se encontró el dataset consolidado en: {DATA_FILE}")
        
    # 1. Cargar base de datos
    df = pd.read_csv(DATA_FILE)
    
    # 2. Formatear y setear índice multi-nivel para linearmodels
    df["codigo_canton"] = df["codigo_canton"].astype(str).str.zfill(4)
    df = df.set_index(["codigo_canton", "anio"])
    
    # 3. Transformación logarítmica
    # [imputation] Control de NaNs o ceros antes de aplicar logaritmos
    df["ln_vab"] = np.log(df["vab"])
    df["ln_empleo"] = np.log(df["empleo_prom"])
    df["ln_ventas"] = np.log(df["ventas_totales"])
    
    # Eliminar posibles valores infinitos o NaNs generados por la transformación
    df_clean = df.dropna(subset=["ln_vab", "ln_empleo", "ln_ventas"])
    
    # Variable dependiente e independientes
    Y = df_clean["ln_empleo"]
    X = df_clean[["ln_vab", "ln_ventas"]]
    # Añadir constante para Pooled y RE
    X_const = sm.add_constant(X)
    
    # 4. Estimaciones
    # A. Pooled OLS
    print("Estimando Pooled OLS...")
    model_pooled = PooledOLS(Y, X_const)
    res_pooled = model_pooled.fit()
    
    # B. Efectos Fijos (Within)
    print("Estimando Efectos Fijos (FE)...")
    model_fe = PanelOLS(Y, X, entity_effects=True)
    res_fe = model_fe.fit()
    
    # C. Efectos Aleatorios (RE)
    print("Estimando Efectos Aleatorios (RE)...")
    model_re = RandomEffects(Y, X_const)
    res_re = model_re.fit()
    
    # 5. Cálculo del Test de Hausman
    chi2, df_h, p_val = calculate_hausman(res_fe, res_re)
    
    # 6. Escribir logs de resultados
    log_file = OUTPUT_DIR / "python_panel_estimation.log"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("=== ESTIMACIÓN ECONOMETRICA EN PYTHON (LINEARMODELS) ===\n\n")
        f.write("--- POOLED OLS RESULTS ---\n")
        f.write(str(res_pooled) + "\n\n")
        f.write("--- FIXED EFFECTS (FE) RESULTS ---\n")
        f.write(str(res_fe) + "\n\n")
        f.write("--- RANDOM EFFECTS (RE) RESULTS ---\n")
        f.write(str(res_re) + "\n\n")
        f.write("--- TEST DE HAUSMAN ---\n")
        f.write(f"Chi-cuadrado: {chi2:.4f}\n")
        f.write(f"Grados de libertad: {df_h}\n")
        f.write(f"p-valor: {p_val:.4e}\n")
        
    print(f"Estimación econométrica finalizada. Resultados guardados en: {log_file}")
    print(f"Test de Hausman: Chi2 = {chi2:.4f}, p-valor = {p_val:.4e}")

if __name__ == "__main__":
    main()
