import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

df = pd.read_csv("data/base_analisis.csv")
# Use the same transformations as in the model
X = pd.DataFrame()
X['GM'] = df['gasto_militar_pib']
X['MI'] = df['migracion_neta']
X['HO'] = np.log(df['tasa_homicidios'])
X['FL'] = np.log(df['fuerza_laboral'])
X = sm.add_constant(X)

vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

print(vif_data)
