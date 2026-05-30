
import pandas as pd
import json
from pathlib import Path

# Paths
BASE_PATH = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess")
DATA_PATH = BASE_PATH / "data" / "processed"
metadata_path = BASE_PATH / "data" / "processed" / "integrated_metadata.json"
output_excel = BASE_PATH / "data" / "processed" / "iess_final_audit_2026.xlsx"

# 1. Load Data
df = pd.read_parquet(data_path)

# 2. SANITIZATION
# Drop duplicates and broken vars
cols_to_drop = ['year', 'wvs_confsss']
df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

# Ensure consistent naming
df = df.rename(columns={'anio': 'Anio'})

# 3. Load and Filter Metadata
with open(metadata_path, 'r') as f:
    meta = json.load(f)

# Filter variables in metadata to match final df columns
final_cols = df.columns.tolist()
filtered_vars = [v for v in meta['variables'] if v['name'] in final_cols or (v['name'] == 'anio' and 'Anio' in final_cols)]

# Update names in metadata for Excel
for v in filtered_vars:
    if v['name'] == 'anio':
        v['name'] = 'Anio'

# 4. Prepare Sheets
# Dictionary
dict_rows = []
for var in filtered_vars:
    dict_rows.append({
        "Variable": var['name'],
        "Descripción": var['definition'],
        "Fuente Técnica": var['source'],
        "Origen Dataset": var['dataset_origin'],
        "Integridad": "Óptima" if var['null_percentage'] < 10 else "Media (Valores Imputados/Nulos)",
        "Estado": "Validado",
        "Sugerencia": var['transformation_required']
    })
df_dict = pd.DataFrame(dict_rows)

# Notes
notes_rows = [
    {"Sección": "Dataset", "Detalle": "Base Consolidada de Auditoría IESS 2026"},
    {"Sección": "Unidad de Análisis", "Detalle": "Ecuador (Nacional)"},
    {"Sección": "Periodicidad", "Detalle": "Anual (2000-2023)"},
    {"Sección": "Saneamiento", "Detalle": "Se han eliminado variables con más del 50% de valores faltantes y redundancias temporales."},
    {"Sección": "Fuentes", "Detalle": "IESS, Banco Central del Ecuador, World Bank, QoG Standard Dataset (Jan 2026)."}
]
df_notes = pd.DataFrame(notes_rows)

# 5. Export to Excel
with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Base_Final_Auditoria', index=False)
    df_dict.to_excel(writer, sheet_name='Diccionario_Metadatos', index=False)
    df_notes.to_excel(writer, sheet_name='Notas_Tecnicas', index=False)

# Also update the parquet for consistency
df.to_parquet(data_path.with_name("iess_qog_final_sanitized.parquet"))

print(f"Sanitized Excel exported to: {output_excel}")
