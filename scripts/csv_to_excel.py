#!/usr/bin/env python3
"""
Convertir panel_raw.csv a panel_raw.xlsx en el mismo directorio.
Uso: python csv_to_excel.py
"""
import sys
from pathlib import Path

from core.config import DATA_RAW, DATA_PROCESSED, ensure_dirs

try:
    import pandas as pd
except Exception:
    print("Error: pandas no está instalado. Instala con: pip install pandas openpyxl")
    raise

ensure_dirs()

csv_path = DATA_RAW / "panel_raw.csv"
if not csv_path.exists():
    print(f"Error: {csv_path} no encontrado en {Path.cwd()}")
    sys.exit(1)

try:
    df = pd.read_csv(csv_path)
    xlsx_path = DATA_PROCESSED / csv_path.with_suffix('.xlsx').name
    df.to_excel(xlsx_path, index=False)
    print(f"Generado: {xlsx_path}")
except Exception as e:
    print("Conversión falló:", e)
    raise
