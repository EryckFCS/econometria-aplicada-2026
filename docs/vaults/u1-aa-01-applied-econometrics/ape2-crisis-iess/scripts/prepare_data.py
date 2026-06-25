import pandas as pd

# Load the previously built base
base_path = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/data/processed/base_erick_condoy_homicidios_iess.csv"
df = pd.read_csv(base_path)

# 1. Imputation of Tasa de Homicidios
# We use linear interpolation for internal gaps
df['tasa_homicidios'] = df['tasa_homicidios'].interpolate(method='linear')

# For the last year (2024), if it's NaN, we use the trend or last value
if df['tasa_homicidios'].isnull().iloc[-1]:
    # In Ecuador 2024, the rate is expected to stay high. We forward fill the 2023 value.
    df['tasa_homicidios'] = df['tasa_homicidios'].ffill()

# 2. Final verification
print("--- Datos después de Imputación ---")
print(df.isnull().sum())
print(df.tail())

# 3. Save to the new vault location
output_vault_path = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/data/base_analisis.csv"
df.to_csv(output_vault_path, index=False)
print(f"\nBase de análisis guardada en: {output_vault_path}")
