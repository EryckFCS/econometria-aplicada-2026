
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
BASE_PATH = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess")
DATA_PATH = BASE_PATH / "data" / "processed"
qog_ecu_path = BASE_PATH / "data" / "raw" / "external" / "qog_ecuador.csv"
vanguard_data_path = BASE_PATH / "data" / "raw" / "vanguard_strategy_vars.parquet"

# Load
df_iess = pd.read_parquet(iess_data_path)
df_qog = pd.read_csv(qog_ecu_path)
df_van = pd.read_parquet(vanguard_data_path)

# Filter QoG for relevant years (2000-2023)
df_qog['year'] = df_qog['year'].astype(float).astype(int)
df_qog = df_qog[(df_qog['year'] >= 2000) & (df_qog['year'] <= 2023)]

# Merge IESS and Vanguard first
df_merged = pd.merge(df_iess, df_van, left_on='anio', right_on='year')

# List of interesting QoG variables (based on availability in the dataset)
# We use common ones found in QoG Standard
qog_vars = [
    'wvs_confsss', 'icrg_qog', 'wwbi_prpemp_ss', 'ilo_informal', 
    'fi_reg', 'ti_cpi', 'fh_status', 'vdem_polyarchy'
]

# Select only those that actually exist in the dataframe
available_qog_vars = [v for v in qog_vars if v in df_qog.columns]
df_qog_subset = df_qog[['year'] + available_qog_vars]

# Final Merge
df_final = pd.merge(df_merged, df_qog_subset, on='year', how='left')

# Calculate Affiliation Rate (The real KPI)
df_final['tasa_afiliacion'] = df_final['afiliados_iess'] / df_final['fuerza_laboral']

# Select variables for correlation analysis
analysis_vars = [
    'tasa_afiliacion', 'tasa_subempleo', 'embi_ecuador', 'remesas_pib', 'matricula_superior'
] + available_qog_vars

# Correlation Matrix
corr = df_final[analysis_vars].corr()

# Results
print("\n--- Correlation: Affiliation Rate vs New Variables ---")
print(corr['tasa_afiliacion'].sort_values(ascending=False))

# Descriptive Stats
print("\n--- Descriptive Stats for New Variables (Ecuador 2000-2023) ---")
print(df_final[available_qog_vars].describe().T)

# Save merged dataset for future use
df_final.to_parquet(BASE_PATH / "data" / "processed" / "iess_qog_integrated.parquet")

# Save correlation summary
with open(BASE_PATH / "logs" / "qog_integration_summary.txt", "w") as f:
    f.write("Correlation Matrix for IESS-QoG Integration\n")
    f.write(str(corr['tasa_afiliacion']))
