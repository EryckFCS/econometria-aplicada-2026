import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_csv("data/base_analisis.csv")
y = np.log(df['afiliados_iess'])
X = pd.DataFrame()
X['GM'] = df['gasto_militar_pib']
X['MI'] = df['migracion_neta']
X['HO'] = np.log(df['tasa_homicidios'])
X['FL'] = np.log(df['fuerza_laboral'])
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())
