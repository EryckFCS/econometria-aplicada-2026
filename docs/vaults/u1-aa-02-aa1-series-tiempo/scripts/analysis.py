"""
AA1: Modelado Dinámico de la Función de Importaciones (Ecuador)
Este script realiza la estimación de un modelo ARDL para la función de importaciones
utilizando datos constantes del Banco Mundial.
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.ardl import ARDL
import matplotlib.pyplot as plt
import os
from ecs_quantitative import get_logger

# Inicializar logger
logger = get_logger("aa1_analysis")

# Configuración de rutas
BASE_DIR = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026"
DATA_PATH = os.path.join(BASE_DIR, "data/raw/external/API_ECU_DS2_es_excel_v2_2204(Data).csv")
VAULT_DIR = os.path.join(BASE_DIR, "docs/vaults/u1-aa-02-aa1-series-tiempo")
OUTPUT_DIR = os.path.join(VAULT_DIR, "assets")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def estimate_import_function():
    logger.info("Cargando datos del Banco Mundial para Ecuador...")
    
    try:
        # Cargar datos con punto y coma y decimales con coma
        df = pd.read_csv(DATA_PATH, sep=';', skiprows=3, decimal=',', encoding='latin-1')
    except Exception as e:
        logger.error(f"Error al cargar el archivo: {e}")
        return

    # Extraer indicadores
    # PIB (UMN a precios constantes): NY.GDP.MKTP.KN
    # Importaciones (UMN a precios constantes): NE.IMP.GNFS.KN
    
    gdp_row = df[df['Indicator Code'] == 'NY.GDP.MKTP.KN']
    imp_row = df[df['Indicator Code'] == 'NE.IMP.GNFS.KN']
    
    if gdp_row.empty or imp_row.empty:
        logger.error("No se encontraron los indicadores requeridos.")
        return

    # Convertir a series temporales
    years = [col for col in df.columns if col.isdigit()]
    gdp = gdp_row.iloc[0][years].astype(float)
    imports = imp_row.iloc[0][years].astype(float)
    
    data = pd.DataFrame({'GDP': gdp, 'Imports': imports})
    data.index = pd.to_numeric(data.index)
    data = data.dropna()
    
    if data.empty:
        logger.error("No hay datos suficientes después de limpiar NaNs.")
        return

    logger.info(f"Datos alineados desde {data.index.min()} hasta {data.index.max()} ({len(data)} observaciones).")

    # Estadísticos Descriptivos
    desc_stats = data[['GDP', 'Imports']].describe().transpose()
    print("\nESTADÍSTICOS DESCRIPTIVOS:")
    print(desc_stats)
    
    # Transformación logarítmica
    data['l_gdp'] = np.log(data['GDP'])
    data['l_imports'] = np.log(data['Imports'])

    # Estimación de Modelo Dinámico ARDL(1, 0)
    # log(M_t) = c + b1 * log(GDP_t) + b2 * log(M_{t-1})
    model = ARDL(data['l_imports'], 1, data[['l_gdp']], 0).fit()
    
    print("\n" + "="*60)
    print("REPORTE DE ESTIMACIÓN: FUNCIÓN DE IMPORTACIONES (ECUADOR)")
    print("="*60)
    print(model.summary())
    
    # Análisis de Multiplicadores
    # Multiplicador de Impacto (Elasticidad de corto plazo): Coeficiente de l_gdp
    # Multiplicador de Largo Plazo: beta_gdp / (1 - beta_lag_imports)
    
    params = model.params
    short_run_elasticity = params['l_gdp.L0']
    lag_coef = params['l_imports.L1']
    long_run_elasticity = short_run_elasticity / (1 - lag_coef)
    
    print("\nANÁLISIS DE ELASTICIDADES:")
    print(f"- Elasticidad Ingreso de Corto Plazo: {short_run_elasticity:.4f}")
    print(f"- Elasticidad Ingreso de Largo Plazo: {long_run_elasticity:.4f}")
    print(f"- Velocidad de Ajuste: {1 - lag_coef:.4f}")
    
    # Visualización
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['l_imports'], label='Log-Importaciones Observadas', color='#1f77b4', linewidth=2)
    plt.plot(model.fittedvalues.index, model.fittedvalues, label='Ajuste del Modelo (ARDL)', color='#d62728', linestyle='--')
    plt.title('Dinámica de las Importaciones en Ecuador (1960-2024)', fontsize=14)
    plt.xlabel('Año')
    plt.ylabel('Log(Importaciones Reales)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(OUTPUT_DIR, "import_function_ardl.png"))
    logger.info(f"Gráfico guardado en {OUTPUT_DIR}/import_function_ardl.png")

if __name__ == "__main__":
    estimate_import_function()
