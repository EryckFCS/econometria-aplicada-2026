import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import os

def getWeights_FFD(d, thres):
    w = [1.]
    k = 1
    while True:
        w_ = -w[-1] / k * (d - k + 1)
        if abs(w_) < thres:
            break
        w.append(w_)
        k += 1
    return np.array(w[::-1]).reshape(-1, 1)

def fracDiff_FFD(series, d, thres=1e-5):
    w = getWeights_FFD(d, thres)
    width = len(w) - 1
    df = {}
    for name in series.columns:
        seriesF = series[name].ffill().dropna()
        res = []
        for i in range(width, seriesF.shape[0]):
            res.append(np.dot(w.T, seriesF.iloc[i-width:i+1])[0])
        df[name] = res
    return pd.DataFrame(df)

# Load data
base_path = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess"
file_path = os.path.join(base_path, "data/processed/iess_clean.parquet")
df = pd.read_parquet(file_path)

# Test variable
series = df[['afiliados_iess']].copy()
series['ln_afiliados'] = np.log(series['afiliados_iess'])

# Test different d values
results = []
for d in np.linspace(0, 1, 11):
    fd = fracDiff_FFD(series[['ln_afiliados']], d, thres=1e-2) # High thres due to small N
    if len(fd) > 5:
        p_val = adfuller(fd['ln_afiliados'])[1]
        results.append({'d': d, 'p_value': p_val, 'stationary': p_val < 0.05, 'n_obs': len(fd)})

results_df = pd.DataFrame(results)
print("--- Fractional Differentiation Test (López de Prado) ---")
print(results_df)

# Find minimum d
min_d = results_df[results_df['stationary']]['d'].min()
print(f"\nMinimum d for stationarity: {min_d}")
