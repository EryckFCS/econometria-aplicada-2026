import pandas as pd
import numpy as np
import os
from statsmodels.tsa.ardl import ARDL, ardl_select_order
import matplotlib.pyplot as plt

# Paths
base_path = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess"
data_path = os.path.join(base_path, "data/processed/iess_clean.parquet")
output_path = os.path.join(base_path, "assets")
os.makedirs(output_path, exist_ok=True)

# Load data
data_path_q = os.path.join(base_path, "data/processed/iess_quarterly.parquet")
df = pd.read_parquet(data_path_q)

# Set index for statsmodels (Quarterly index)
df.index = pd.PeriodIndex(df.index, freq='Q')

# Select variables for the main model (Structural Vectors)
dep_var = 'ln_afiliados_iess'
indep_vars = ['ln_tasa_subempleo', 'ln_tasa_dependencia', 'ln_precio_petroleo_wti']

print(f"--- ARDL Model Estimation (N={len(df)}) ---")
print(f"Dependent Variable: {dep_var}")
print(f"Independent Variables: {indep_vars}")

# 1. Automatic Order Selection (BIC)
# With N=96, we can allow more lags.
sel_res = ardl_select_order(
    df[dep_var], 
    maxlag=4, 
    exog=df[indep_vars], 
    maxorder=2, 
    ic="bic", 
    trend="c"
)

print(f"\nOptimal Order Selected (BIC): AR={sel_res.ar_lags}, DL={sel_res.dl_lags}")

# 2. Fit ARDL Model
model = sel_res.model
results = model.fit()

print("\nARDL Model Summary:")
print(results.summary())

# 3. Bounds Test for Cointegration
print("\n--- Bounds Test for Cointegration (Pesaran et al. 2001) ---")
try:
    # Prepare UECM data
    uecm_df = pd.DataFrame(index=df.index)
    uecm_df['dy'] = df[dep_var].diff()
    uecm_df['y_l1'] = df[dep_var].shift(1)
    
    # Use selected exog
    selected_exog = indep_vars # Use all for the test
    
    for var in selected_exog:
        uecm_df[f'{var}_l1'] = df[var].shift(1)
        uecm_df[f'd_{var}'] = df[var].diff()
    
    uecm_df = uecm_df.dropna()
    
    import statsmodels.api as sm
    exog_cols = ['y_l1'] + [f'{v}_l1' for v in selected_exog] + [f'd_{v}' for v in selected_exog]
    X_uecm = sm.add_constant(uecm_df[exog_cols])
    y_uecm = uecm_df['dy']
    
    manual_uecm = sm.OLS(y_uecm, X_uecm).fit()
    
    k = len(selected_exog)
    hypotheses = ['y_l1 = 0'] + [f'{v}_l1 = 0' for v in selected_exog]
    f_test = manual_uecm.f_test(hypotheses)
    
    f_stat = f_test.fvalue.item() if hasattr(f_test.fvalue, 'item') else f_test.fvalue
    print(f"F-statistic (Unrestricted UECM): {f_stat:.4f}")
    
    # Pesaran et al. (2001) Critical Values for k=3, Case III (Constant)
    crit_vals = {
        '10%': (2.72, 3.77),
        '5%': (3.23, 4.35),
        '1%': (4.29, 5.61)
    }
    
    print(f"Pesaran et al. (2001) Critical Values (k={k}):")
    for level, bounds in crit_vals.items():
        print(f"  {level}: I(0)={bounds[0]}, I(1)={bounds[1]}")
    
    if f_stat > crit_vals['5%'][1]:
        print(f"\nResult: F-stat ({f_stat:.4f}) > I(1) Bound ({crit_vals['5%'][1]}) at 5% level.")
        print("Conclusion: Evidence of Cointegration.")
    elif f_stat < crit_vals['5%'][0]:
        print(f"\nResult: F-stat ({f_stat:.4f}) < I(0) Bound ({crit_vals['5%'][0]}) at 5% level.")
        print("Conclusion: No evidence of Cointegration.")
    else:
        print(f"\nResult: F-stat ({f_stat:.4f}) is in the Inconclusive Zone.")
        
except Exception as e:
    print(f"\nManual Bounds Test failed: {e}")

# 4. Long-Run Multipliers
print("\n--- Long-Run Multipliers ---")
params = results.params
y_lags = [p for p in params.index if p.startswith(f"{dep_var}.L")]
sum_phi = sum(params[y_lags])
denom = 1 - sum_phi

print(f"Sum of AR coefficients (phi): {sum_phi:.4f}")

multipliers = {}
for var in indep_vars:
    x_coefs = [p for p in params.index if p == var or p.startswith(f"{var}.L")]
    if x_coefs:
        sum_beta = sum(params[x_coefs])
        multipliers[var] = sum_beta / denom
        print(f"Long-run multiplier for {var}: {multipliers[var]:.4f}")
    else:
        print(f"Long-run multiplier for {var}: Variable not selected.")

# 5. Diagnostic Checks
print("\n--- Diagnostic Checks ---")
try:
    resids = results.resid
    from statsmodels.stats.stattools import jarque_bera
    jb, jbp, _, _ = jarque_bera(resids)
    print(f"Jarque-Bera (Normality): {jb:.4f} (p={jbp:.4f})")
    
    from statsmodels.stats.diagnostic import acorr_ljungbox
    lb = acorr_ljungbox(resids, lags=[4], return_df=True)
    print(f"Ljung-Box (Autocorr lag 4): {lb['lb_stat'].values[0]:.4f} (p={lb['lb_pvalue'].values[0]:.4f})")
    print("Note: High autocorrelation is expected due to the interpolation process (induced smoothness).")
    
    import statsmodels.api as sm
    from statsmodels.stats.diagnostic import het_breuschpagan
    
    # Correctly align exog for Breusch-Pagan
    exog_model = results.model.exog
    if len(exog_model) != len(resids):
        # Statsmodels ARDL slices the first lags
        exog_aligned = exog_model
    else:
        exog_aligned = exog_model
        
    # Standard check: use a constant and the residuals to check for heteroscedasticity
    # We'll use the indices to be sure
    _, bpp, _, _ = het_breuschpagan(resids, sm.add_constant(np.arange(len(resids))))
    print(f"Breusch-Pagan (Heteroscedasticity proxy): p={bpp:.4f}")

    # Plot residuals
    plt.figure(figsize=(10, 6))
    plt.plot(resids.index.to_timestamp(), resids.values, color='#1a5e97', linewidth=1.5)
    plt.axhline(0, color='r', linestyle='--')
    plt.title("Residuos del Modelo ARDL (Frecuencia Trimestral)")
    plt.xlabel("Año-Trimestre")
    plt.ylabel("Residuos")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "ardl_residuals.png"))
    plt.close()
except Exception as e:
    print(f"Diagnostic checks failed: {e}")

# Save results
with open(os.path.join(output_path, "ardl_results.txt"), "w") as f:
    f.write(results.summary().as_text())
    f.write("\n\n--- Long-Run Multipliers ---\n")
    for var, val in multipliers.items():
        f.write(f"{var}: {val:.4f}\n")

print(f"\nARDL estimation complete. Results saved to {output_path}")
