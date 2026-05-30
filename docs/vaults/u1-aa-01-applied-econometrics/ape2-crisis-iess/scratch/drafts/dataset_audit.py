
import pandas as pd
import numpy as np
import json
from pathlib import Path

# Paths
BASE_PATH = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess")
DATA_PATH = BASE_PATH / "data" / "processed"
output_metadata = BASE_PATH / "data" / "processed" / "integrated_metadata.json"

# Load
df = pd.read_parquet(data_path)

# 1. Null Report
null_report = df.isnull().mean() * 100
broken_vars = null_report[null_report > 50].index.tolist()
clean_vars = null_report[null_report <= 50].index.tolist()

# 2. Transformation suggestions
# Variables with high skewness might need Log
skewness = df.select_dtypes(include=[np.number]).skew()
needs_log = skewness[abs(skewness) > 1].index.tolist()

# 3. Comprehensive Metadata Definition (Audit results included)
metadata = {
    "project": "Applied Econometrics 2026 - IESS Crisis Audit",
    "dataset_name": "iess_qog_integrated.parquet",
    "audit_date": "2026-04-27",
    "total_observations": len(df),
    "integrity_summary": {
        "null_percentage_avg": float(null_report.mean()),
        "broken_variables_count": len(broken_vars),
        "viable_variables_count": len(clean_vars)
    },
    "variables": []
}

# Define variable origins and definitions
definitions = {
    "anio": {"def": "Año de la observación", "src": "Control", "origin": "Internal"},
    "afiliados_iess": {"def": "Número total de afiliados al IESS", "src": "IESS Statistical Bulletins", "origin": "IESS"},
    "fuerza_laboral": {"def": "Población Económicamente Activa (PEA)", "src": "INEC/BCE", "origin": "BCE"},
    "tasa_subempleo": {"def": "Porcentaje de la PEA en subempleo", "src": "INEC (ENEMDU)", "origin": "BCE"},
    "tasa_afiliacion": {"def": "Ratio Afiliados / Fuerza Laboral", "src": "Cálculo propio", "origin": "Computed"},
    "embi_ecuador": {"def": "Riesgo País (EMBI)", "src": "J.P. Morgan / Min. Finanzas", "origin": "BCE/JP Morgan"},
    "remesas_pib": {"def": "Remesas recibidas como % del PIB", "src": "World Bank / BCE", "origin": "World Bank"},
    "matricula_superior": {"def": "Tasa bruta de matrícula en educación superior", "src": "World Bank", "origin": "World Bank"},
    "icrg_qog": {"def": "Índice de Calidad de Gobierno (ICRG)", "src": "International Country Risk Guide", "origin": "QoG Dataset"},
    "fi_reg": {"def": "Índice de Regulación del Mercado (Fraser Institute)", "src": "Economic Freedom of the World", "origin": "QoG Dataset"},
    "vdem_polyarchy": {"def": "Índice de Democracia Electoral (V-Dem)", "src": "Varieties of Democracy Project", "origin": "QoG Dataset"},
    "ti_cpi": {"def": "Índice de Percepción de la Corrupción", "src": "Transparency International", "origin": "QoG Dataset"},
    "fh_status": {"def": "Estatus de Libertad (Freedom House)", "src": "Freedom in the World", "origin": "QoG Dataset"}
}

for col in df.columns:
    info = definitions.get(col, {"def": "Variable sin descripción detallada", "src": "Desconocido", "origin": "Desconocido"})
    var_meta = {
        "name": col,
        "definition": info["def"],
        "source": info["src"],
        "dataset_origin": info["origin"],
        "null_percentage": float(null_report.get(col, 0)),
        "status": "BROKEN" if col in broken_vars else "VIABLE",
        "transformation_required": "LOG" if col in needs_log else "NONE"
    }
    metadata["variables"].append(var_meta)

# Save JSON
with open(output_metadata, 'w') as f:
    json.dump(metadata, f, indent=4)

# Print Summary for the Report
print(f"Audit Complete. Metadata saved to {output_metadata}")
print("\n--- Integrity Report ---")
print(f"Total Vars: {len(df.columns)}")
print(f"Viable Vars: {len(clean_vars)}")
print(f"Broken Vars (Nulls > 50%): {broken_vars}")
print(f"Vars needing Log: {needs_log}")
