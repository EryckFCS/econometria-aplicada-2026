import os
import json
import pandas as pd
import glob

lake_dir = "/home/erick-fcs/.capital/lake/raw_data"
files = glob.glob(os.path.join(lake_dir, "*"))

print("Searching for columns matching previsional or financial keywords...")
keywords = ["masa", "salarial", "deuda", "bono", "debt", "pension", "pensionistas", "iess", "afiliado", "militar"]

for f in files:
    if f.endswith(".csv"):
        try:
            df = pd.read_csv(f, nrows=2)
            matched = [col for col in df.columns if any(kw in col.lower() for kw in keywords)]
            if matched:
                print(f"\nCSV: {os.path.basename(f)}")
                print("Matched columns:", matched)
        except Exception as e:
            pass
    elif f.endswith(".xlsx") or f.endswith(".xls"):
        try:
            xl = pd.ExcelFile(f)
            for sheet in xl.sheet_names:
                df = xl.parse(sheet, nrows=2)
                matched = [col for col in df.columns if any(kw in str(col).lower() for kw in keywords)]
                if matched:
                    print(f"\nExcel: {os.path.basename(f)} | Sheet: {sheet}")
                    print("Matched columns:", matched)
        except Exception as e:
            pass
    elif f.endswith(".parquet"):
        try:
            df = pd.read_parquet(f)
            matched = [col for col in df.columns if any(kw in col.lower() for kw in keywords)]
            if matched:
                print(f"\nParquet: {os.path.basename(f)}")
                print("Matched columns:", matched)
        except Exception as e:
            pass
