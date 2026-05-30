
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

# 2. Load Metadata
with open(metadata_path, 'r') as f:
    meta = json.load(f)

# 3. Prepare Sheets
# Sheet 1: Data (df)

# Sheet 2: Dictionary
dict_rows = []
for var in meta['variables']:
    dict_rows.append({
        "Variable": var['name'],
        "Descripción": var['definition'],
        "Fuente Técnica": var['source'],
        "Origen Dataset": var['dataset_origin'],
        "Integridad (% Nulos)": f"{var['null_percentage']:.2f}%",
        "Estado": var['status'],
        "Sugerencia Transformación": var['transformation_required']
    })
df_dict = pd.DataFrame(dict_rows)

# Sheet 3: Methodology Notes
notes_rows = [
    {"Sección": "Proyecto", "Detalle": meta['project']},
    {"Sección": "Fecha de Auditoría", "Detalle": meta['audit_date']},
    {"Sección": "Total Observaciones", "Detalle": meta['total_observations']},
    {"Sección": "Resumen Integridad", "Detalle": f"{meta['integrity_summary']['viable_variables_count']} variables viables, {meta['integrity_summary']['broken_variables_count']} variables rotas."},
    {"Sección": "Nota Metodológica", "Detalle": "Las variables institucionales provienen del Quality of Government (QoG) Standard Dataset Jan 2026. Los datos del IESS corresponden a boletines estadísticos oficiales."}
]
df_notes = pd.DataFrame(notes_rows)

# 4. Export to Excel
with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Datos_Series', index=False)
    df_dict.to_excel(writer, sheet_name='Diccionario_Variables', index=False)
    df_notes.to_excel(writer, sheet_name='Notas_Metodologicas', index=False)

print(f"Excel export successful: {output_excel}")
