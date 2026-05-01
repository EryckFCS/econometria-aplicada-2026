import pandas as pd
import numpy as np
from statsmodels.tsa.ardl import ARDL
from statsmodels.tsa.ardl import ardl_select_order
from scipy import interpolate
from pathlib import Path
import json
from loguru import logger

# Configuration
BASE_PATH = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess")
RAW_VANGUARD = BASE_PATH / "data" / "raw" / "vanguard_strategy_vars.parquet"
LOGS_PATH = BASE_PATH / "logs"
DATA_PATH = BASE_PATH / "data" / "processed"

LOGS_PATH.mkdir(parents=True, exist_ok=True)

def disaggregate_series(df, col, method='cubic'):
    """Interpolates annual data to quarterly."""
    # WB data might have NaNs even after linear interpolation in fetch
    df = df.dropna(subset=[col])
    years = df['year'].values
    values = df[col].values
    
    if len(years) < 2:
        return pd.DataFrame()
        
    # Create quarterly timeline
    quarters = []
    for y in range(int(years.min()), int(years.max()) + 1):
        for q in [1, 2, 3, 4]:
            quarters.append(y + (q-1)/4)
    
    f = interpolate.interp1d(years, values, kind=method, fill_value="extrapolate")
    q_values = f(quarters)
    
    return pd.DataFrame({'year_q': quarters, col: q_values})

def run_ardl_test(y, x, var_name):
    """Runs an ARDL model and returns key metrics."""
    try:
        # Standardize x to ensure it's a DataFrame with the right name
        x_df = pd.DataFrame(x)
        
        # We need to handle NaNs if any (though we interpolated)
        valid_idx = ~(y.isna() | x_df.isna().any(axis=1))
        y_valid = y[valid_idx]
        x_valid = x_df[valid_idx]
        
        if len(y_valid) < 10:
            return {"var": var_name, "status": "ERROR: Insufficient data"}

        # Automatic order selection
        # Note: we use maxlag=2 to avoid dimensionality issues in short series
        sel = ardl_select_order(y_valid, 2, x_valid, 2, ic='bic', trend='c')
        model = sel.model.fit()
        
        # Find p-value for the exogenous variable(s)
        p_vals = model.pvalues.filter(like=var_name)
        if p_vals.empty:
            p_val = 1.0
        else:
            p_val = p_vals.min()
        
        return {
            "var": var_name,
            "bic": float(model.bic),
            "p_val": float(p_val),
            "status": "SIGNIFICANT" if p_val < 0.05 else "NOT_SIGNIFICANT"
        }
    except Exception as e:
        return {"var": var_name, "status": f"ERROR: {e}"}

def main():
    logger.info("Loading baseline quarterly data...")
    df_base = pd.read_parquet(DATA_PATH / "iess_quarterly.parquet").reset_index(drop=True)
    
    # Reconstruct year_q if missing
    if 'year_q' not in df_base.columns:
        df_base['year_q'] = df_base['anio'] + (df_base['trimestre'] - 1) / 4
    
    logger.info("Loading vanguard variables...")
    df_van_annual = pd.read_parquet(RAW_VANGUARD)
    
    # Disaggregate all vanguard vars
    van_cols = ['remesas_pib', 'matricula_superior', 'embi_ecuador', 'gdp_pc_ppp']
    van_q_list = []
    for col in van_cols:
        q_df = disaggregate_series(df_van_annual, col)
        if not q_df.empty:
            # We only keep the column, we'll align by index since we know they are same periods
            # But let's be safe and join on year_q
            van_q_list.append(q_df.set_index('year_q'))
    
    df_van_q = pd.concat(van_q_list, axis=1).reset_index()
    
    # Merge with base to ensure alignment
    # df_base has year_q (decimal format)
    df_total = pd.merge(df_base, df_van_q, on='year_q', how='inner')
    
    logger.info(f"Total aligned dataset shape: {df_total.shape}")
    
    y = df_total['ln_afiliados_iess']
    results = []
    
    for var in van_cols:
        if var not in df_total.columns:
            continue
        logger.info(f"Testing variable: {var}")
        x = df_total[[var]]
        res = run_ardl_test(y, x, var)
        results.append(res)
    
    # Multivariate test
    logger.info("Running Multivariate Joint Test...")
    core_vars = ['remesas_pib', 'matricula_superior', 'embi_ecuador', 'gdp_pc_ppp']
    x_joint = df_total[core_vars]
    
    try:
        sel_joint = ardl_select_order(y, 2, x_joint, 2, ic='bic', trend='c')
        model_joint = sel_joint.model.fit()
        
        logger.success("Joint Model converged successfully.")
        print("\n--- Joint Model (Vanguard Strategy) ---")
        print(model_joint.summary().tables[1])
        
        # Save summary to logs
        with open(LOGS_PATH / "joint_model_summary.txt", 'w') as f:
            f.write(str(model_joint.summary()))
            
    except Exception as e:
        logger.error(f"Joint model failed: {e}")

    # Save logs
    output_log = LOGS_PATH / "vanguard_audit_results.json"
    with open(output_log, 'w') as f:
        json.dump(results, f, indent=4)
    
    logger.success(f"Audit results saved to {output_log}")
    
    # Display summary
    print("\n--- Vanguard Strategic Audit Summary ---")
    print(f"{'Variable':20} | {'BIC':10} | {'P-Value':10} | {'Status'}")
    print("-" * 65)
    for r in results:
        bic = f"{r.get('bic', 0):10.2f}" if 'bic' in r and isinstance(r.get('bic'), (int, float)) else "N/A"
        pval = f"{r.get('p_val', 0):10.4f}" if 'p_val' in r and isinstance(r.get('p_val'), (int, float)) else "N/A"
        print(f"{r['var']:20} | {bic} | {pval} | {r['status']}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
