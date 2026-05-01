import pandas as pd
import numpy as np
import os
from scipy.interpolate import interp1d

# Paths
base_path = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess"
data_path = os.path.join(base_path, "data/processed/iess_clean.parquet")
output_data_path = os.path.join(base_path, "data/processed/iess_quarterly.parquet")

# Load annual data
df_annual = pd.read_parquet(data_path)

# Variables to interpolate (levels and logs)
vars_to_interp = [
    "afiliados_iess",
    "fuerza_laboral",
    "tasa_subempleo",
    "sbu",
    "num_pensionistas",
    "tasa_dependencia",
    "gasto_salud_pib",
    "precio_petroleo_wti",
]

# Create quarterly index
# 2000-2023 inclusive -> 24 years -> 24 * 4 = 96 quarters
years = df_annual["anio"].values
quarters = []
for y in years:
    for q in [1, 2, 3, 4]:
        quarters.append(pd.Timestamp(f"{int(y)}-{q * 3:02d}-01"))

df_quarterly = pd.DataFrame(index=quarters)
df_quarterly["anio"] = df_quarterly.index.year
df_quarterly["trimestre"] = df_quarterly.index.month // 3

# Time points for interpolation (annual points)
x_annual = np.arange(len(years))
x_quarterly = np.linspace(0, len(years) - 1, len(quarters))

for var in vars_to_interp:
    y_annual = df_annual[var].values
    # Cubic spline interpolation
    f = interp1d(x_annual, y_annual, kind="cubic")
    y_quarterly = f(x_quarterly)
    df_quarterly[var] = y_quarterly

    # Re-calculate logs
    df_quarterly[f"ln_{var}"] = np.log(df_quarterly[var])

# Calculate differences
for var in vars_to_interp:
    df_quarterly[f"dln_{var}"] = df_quarterly[f"ln_{var}"].diff()

# Save quarterly data
df_quarterly.to_parquet(output_data_path)

print(f"Disaggregation complete. Quarterly data saved (N={len(df_quarterly)}).")
