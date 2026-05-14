import pandas as pd
import numpy as np
import os

# Rutas
BASE_DIR = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026"
DATA_SOURCE = os.path.join(BASE_DIR, "data/raw/external/API_ECU_DS2_es_excel_v2_2204(Data).csv")
VAULT_DATA_DIR = os.path.join(BASE_DIR, "docs/vaults/u1-aa-02-aa1-series-tiempo/data")
EXCEL_OUTPUT = os.path.join(VAULT_DATA_DIR, "aa1_import_function.xlsx")

def generate_excel():
    print("Extrayendo datos para el archivo Excel...")
    
    # 1. Cargar datos originales
    df = pd.read_csv(DATA_SOURCE, sep=';', skiprows=3, decimal=',', encoding='latin-1')
    
    # 2. Extraer series
    years = [col for col in df.columns if col.isdigit()]
    gdp_val = df[df['Indicator Code'] == 'NY.GDP.MKTP.KN'].iloc[0][years].values.astype(float)
    imp_val = df[df['Indicator Code'] == 'NE.IMP.GNFS.KN'].iloc[0][years].values.astype(float)
    
    data_df = pd.DataFrame({
        'year': [int(y) for y in years],
        'gdp': gdp_val,
        'imports': imp_val
    }).dropna()
    
    # 3. Crear Diccionario
    dict_df = pd.DataFrame({
        'Variable': ['year', 'gdp', 'imports'],
        'Nombre': ['Año', 'PIB Real', 'Importaciones Reales'],
        'Descripción': [
            'Año de la observación',
            'Producto Interno Bruto a precios constantes (UMN)',
            'Importaciones de bienes y servicios a precios constantes (UMN)'
        ],
        'Fuente': [
            'Banco Mundial',
            'Banco Mundial (NY.GDP.MKTP.KN)',
            'Banco Mundial (NE.IMP.GNFS.KN)'
        ],
        'Unidad': ['Año', 'Moneda Local Constante', 'Moneda Local Constante']
    })
    
    # 4. Guardar en Excel con múltiples hojas
    with pd.ExcelWriter(EXCEL_OUTPUT, engine='xlsxwriter') as writer:
        data_df.to_excel(writer, sheet_name='data', index=False)
        dict_df.to_excel(writer, sheet_name='dictionary', index=False)
        
        # Ajustar anchos de columna automáticamente
        for sheet in ['data', 'dictionary']:
            worksheet = writer.sheets[sheet]
            df_to_use = data_df if sheet == 'data' else dict_df
            for i, col in enumerate(df_to_use.columns):
                column_len = max(df_to_use[col].astype(str).str.len().max(), len(col)) + 2
                worksheet.set_column(i, i, column_len)
    
    print(f"Archivo Excel generado exitosamente en: {EXCEL_OUTPUT}")

if __name__ == "__main__":
    generate_excel()
