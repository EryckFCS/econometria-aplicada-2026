import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from statsmodels.tsa.ardl import ARDL
import os
import pickle

# Load all data sources
df_iess = pd.read_parquet("data/processed/iess_quarterly.parquet")
df_vanguard = pd.read_parquet("data/raw/vanguard_strategy_vars.parquet")
df_gender = pd.read_parquet("data/raw/gender_gap_data.parquet")

# Merge annual data
df_annual = pd.merge(df_vanguard, df_gender, on="year", how="outer").sort_values("year")


# Interpolate to quarterly
def interpolate_series(df_annual, target_df_quarterly, col_name):
    valid = df_annual[["year", col_name]].dropna()
    f = interp1d(valid["year"], valid[col_name], kind="cubic", fill_value="extrapolate")
    target_years = (
        target_df_quarterly["anio"] + (target_df_quarterly["trimestre"] - 1) / 4
    )
    return f(target_years)


cols_to_interp = [
    "remesas_pib",
    "matricula_superior",
    "embi_ecuador",
    "gender_participation_gap",
]
for col in cols_to_interp:
    df_iess[col] = interpolate_series(df_annual, df_iess, col)

# Feature Engineering
df_iess["ln_afiliacion"] = np.log(df_iess["afiliados_iess"])
df_iess["ln_dependencia"] = np.log(df_iess["tasa_dependencia"])
df_iess["ln_subempleo"] = np.log(df_iess["tasa_subempleo"])
df_iess["ln_wti"] = np.log(df_iess["precio_petroleo_wti"])
df_iess["ln_remesas"] = np.log(df_iess["remesas_pib"])
df_iess["ln_embi"] = np.log(df_iess["embi_ecuador"])
df_iess["ln_matricula"] = np.log(df_iess["matricula_superior"])
df_iess["ln_brecha"] = np.log(df_iess["gender_participation_gap"])

# Clean INF/NAN
df_clean = df_iess.replace([np.inf, -np.inf], np.nan).dropna()

# --- MODEL 1: BASE ---
exog_vars_1 = ["ln_dependencia", "ln_subempleo", "ln_wti"]
# Force specific lags for consistency in table
model_1 = ARDL(df_clean["ln_afiliacion"], 1, df_clean[exog_vars_1], 0, trend="ct").fit()

# --- MODEL 2: AUGMENTED (VANGUARD) ---
exog_vars_2 = [
    "ln_dependencia",
    "ln_subempleo",
    "ln_wti",
    "ln_embi",
    "ln_remesas",
    "ln_matricula",
    "ln_brecha",
]
# Force lag 0 for exog to show all of them
model_2 = ARDL(df_clean["ln_afiliacion"], 1, df_clean[exog_vars_2], 0, trend="ct").fit()

# Save results
os.makedirs("logs", exist_ok=True)
with open("logs/models_comparison.pkl", "wb") as f:
    pickle.dump({"model_1": model_1, "model_2": model_2}, f)

print("Saved forced models to logs/models_comparison.pkl")
print(model_2.summary())
