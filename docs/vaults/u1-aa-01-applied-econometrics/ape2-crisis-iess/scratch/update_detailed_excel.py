
import pandas as pd
import json
from pathlib import Path

# Paths
BASE_PATH = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess")
DATA_PATH = BASE_PATH / "data" / "processed"
output_excel = BASE_PATH / "data" / "processed" / "iess_final_audit_2026.xlsx"

# 1. Load Data
df = pd.read_parquet(data_path)
if 'year' in df.columns: df = df.drop(columns=['year'])
if 'wvs_confsss' in df.columns: df = df.drop(columns=['wvs_confsss'])
df = df.rename(columns={'anio': 'Anio'})

# 2. Logic for Detailed Descriptions
def get_detailed_info(name):
    # Base Definitions
    base_info = {
        "afiliados_iess": ("Número total de afiliados cotizantes al sistema de seguridad social.", "IESS (Boletines Estadísticos)", "IESS"),
        "fuerza_laboral": ("Población Económicamente Activa (PEA) total estimada.", "INEC / Banco Central", "BCE"),
        "tasa_subempleo": ("Porcentaje de la PEA en condiciones de subempleo.", "INEC (ENEMDU)", "BCE"),
        "sbu": ("Salario Básico Unificado nominal en USD.", "Ministerio del Trabajo", "Local"),
        "num_pensionistas": ("Número total de beneficiarios de pensiones contributivas.", "IESS", "IESS"),
        "tasa_dependencia": ("Ratio de pasivos (pensionistas) sobre activos (afiliados).", "Cálculo Local", "Computed"),
        "gasto_salud_pib": ("Gasto total en salud como porcentaje del PIB.", "Banco Mundial", "World Bank"),
        "precio_petroleo_wti": ("Precio promedio anual del barril de petróleo WTI.", "EIA / Banco Central", "BCE"),
        "remesas_pib": ("Ingreso por remesas familiares como % del PIB.", "Banco Mundial", "World Bank"),
        "matricula_superior": ("Tasa bruta de matrícula en educación de tercer nivel.", "UNESCO / Banco Mundial", "World Bank"),
        "gdp_pc_ppp": ("PIB per cápita en Paridad de Poder Adquisitivo (PPA).", "Banco Mundial", "World Bank"),
        "embi_ecuador": ("Riesgo País (Emerging Markets Bond Index).", "J.P. Morgan / BCE", "BCE"),
        "icrg_qog": ("Índice de Calidad de Gobierno (ICRG) basado en corrupción, ley y burocracia.", "PRS Group / QoG", "QoG"),
        "fi_reg": ("Índice de Libertad Económica: Regulación del mercado laboral y crédito.", "Fraser Institute / QoG", "QoG"),
        "ti_cpi": ("Índice de Percepción de la Corrupción.", "Transparency International", "QoG"),
        "fh_status": ("Estatus de Libertad Política (1=Libre, 2=Parcial, 3=No Libre).", "Freedom House", "QoG"),
        "vdem_polyarchy": ("Índice de Democracia Electoral (Poliarquía).", "V-Dem Project", "QoG"),
        "tasa_afiliacion": ("Porcentaje de la fuerza laboral afiliada al IESS (Afiliados/PEA).", "Cálculo Local", "Computed"),
        "Anio": ("Eje temporal de la serie (2000-2023).", "Control Temporal", "Internal")
    }

    # Identify Prefix
    prefix = ""
    clean_name = name
    transformation = ""
    
    if name.startswith("ffd_ln_"):
        prefix = "FFD LN: "
        clean_name = name.replace("ffd_ln_", "")
        transformation = "Diferenciación Fraccional del logaritmo para corregir estacionariedad preservando memoria de largo plazo."
    elif name.startswith("dln_"):
        prefix = "DLN: "
        clean_name = name.replace("dln_", "")
        transformation = "Primera diferencia del logaritmo natural (tasa de crecimiento aproximada)."
    elif name.startswith("ln_"):
        prefix = "LN: "
        clean_name = name.replace("ln_", "")
        transformation = "Logaritmo natural aplicado para estabilizar la varianza y linealizar relaciones."
    
    # Get Base Info
    desc, src, origin = base_info.get(clean_name, ("Variable de control o análisis.", "Calculada Local", "Local"))
    
    if transformation:
        final_desc = f"{prefix}{desc} {transformation}"
        final_src = "Calculada / Análisis Local"
        final_origin = "Computed"
    else:
        final_desc = desc
        final_src = src
        final_origin = origin
        
    return final_desc, final_src, final_origin

# 3. Build Dictionary
dict_rows = []
for col in df.columns:
    desc, src, origin = get_detailed_info(col)
    dict_rows.append({
        "Variable": col,
        "Descripción Integra": desc,
        "Fuente Técnica": src,
        "Dataset Origen": origin,
        "Tipo de Dato": "Numérico (Float64)" if col != "Anio" else "Temporal (Int)",
        "Estado": "Validado / Saneado"
    })
df_dict = pd.DataFrame(dict_rows)

# 4. Export
with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Base_Final_Auditoria', index=False)
    df_dict.to_excel(writer, sheet_name='Diccionario_Integral', index=False)
    # Add methodology notes
    pd.DataFrame([
        {"Nota": "Todas las transformaciones (LN, DLN, FFD) fueron realizadas para cumplir supuestos de estacionariedad y homocedasticidad."},
        {"Nota": "La base integra datos de 5 fuentes globales y nacionales bajo un mismo eje temporal."}
    ]).to_excel(writer, sheet_name='Notas_Metodologicas', index=False)

print(f"Final Integrated Excel updated: {output_excel}")
