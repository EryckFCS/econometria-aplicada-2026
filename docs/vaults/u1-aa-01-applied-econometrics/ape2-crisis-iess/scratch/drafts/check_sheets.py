import pandas as pd

path_wdi = "/home/erick-fcs/.capital/lake/raw_data/raw_wdi_macro_1990_2025.csv"
try:
    df_wdi = pd.read_csv(path_wdi)
    print("WDI Macro Data Columns:")
    matched = [col for col in df_wdi.columns if "debt" in col.lower() or "deuda" in col.lower()]
    print("Matched columns:", matched)
    if matched:
        print("\nPreview of matched columns:\n", df_wdi[['anio'] + matched])
except Exception as e:
    print("Error reading WDI:", e)
