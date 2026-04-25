import pandas as pd
import numpy as np
import os

# Path to the data
base_path = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/evidence/U1-Applied-Econometrics/APE2-Crisis-IESS"
file_path = os.path.join(base_path, "data/processed/iess_clean.parquet")

# Load data
df = pd.read_parquet(file_path)

# Variables to transform
vars_to_transform = [
    'afiliados_iess', 'fuerza_laboral', 'tasa_subempleo', 'sbu', 
    'num_pensionistas', 'tasa_dependencia', 'gasto_salud_pib', 'precio_petroleo_wti'
]

print("--- Data Transformation Pipeline (Standard Logs and Diffs) ---")

# Apply Logs and Standard Differences
for var in vars_to_transform:
    df[f'ln_{var}'] = np.log(df[var])
    df[f'dln_{var}'] = df[f'ln_{var}'].diff()

# Save updated parquet
df.to_parquet(file_path, index=False)
print(f"\nParquet updated with basic features for ARDL modeling: {file_path}")
