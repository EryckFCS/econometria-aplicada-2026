
import pandas as pd
import numpy as np
from statsmodels.tsa.ardl import ARDL, ardl_select_order
from pathlib import Path

# Paths
BASE_PATH = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess")
DATA_PATH = BASE_PATH / "data" / "processed"
vanguard_data_path = BASE_PATH / "data" / "raw" / "vanguard_strategy_vars.parquet"

# Load
df_clean = pd.read_parquet(clean_data_path)
df_vanguard = pd.read_parquet(vanguard_data_path)

# Merge
df_annual = pd.merge(df_clean, df_vanguard, left_on='anio', right_on='year')

# Prepare variables (log transform vanguard if not already)
df_annual['ln_remesas_pib'] = np.log(df_annual['remesas_pib'])
df_annual['ln_matricula_superior'] = np.log(df_annual['matricula_superior'])
df_annual['ln_embi_ecuador'] = np.log(df_annual['embi_ecuador'])

# Select variables for the model
y = df_annual['ln_afiliados_iess']
x = df_annual[['ln_embi_ecuador', 'ln_remesas_pib', 'ln_matricula_superior', 'ln_tasa_subempleo', 'ln_tasa_dependencia']]

# Run ARDL on N=24
print(f"Running ARDL on Annual Data (N={len(df_annual)})")
try:
    # Maxlag=1 because N is very small
    sel = ardl_select_order(y, 1, x, 1, ic='bic', trend='c')
    model = sel.model.fit()
    print("\n--- Annual Model Summary ---")
    print(model.summary())
    
    # Save to file
    with open(BASE_PATH / "logs" / "annual_robustness_summary.txt", "w") as f:
        f.write(str(model.summary()))
except Exception as e:
    print(f"Error: {e}")
