"""
APE1 — RECONSTRUCCIÓN RAW + AUDITORÍA FORENSE
Política: CERO interpolación, CERO imputación, CERO proxies en panel principal.
Columnas renombradas con nombre EXACTO que refleja la unidad real de la API.
Inconsistencias reportadas, no corregidas silenciosamente.
"""

import pandas as pd
import numpy as np
import time
from itertools import product
from datetime import datetime, timezone
from pathlib import Path
import logging
from core.ape1_utils import fetch_wb as utils_fetch_wb

# Configuración de rutas (Basado en la nueva estructura por capas)
SRC_DIR = Path(__file__).parent.parent.resolve()
PROJECT_ROOT = SRC_DIR.parent.resolve()
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Rutas de salida segmentadas (Tu petición de separación)
DATA_CSV_DIR = DATA_RAW_DIR / "csv"
DATA_EXCEL_DIR = DATA_RAW_DIR / "excel"

# Asegurar directorios
DATA_CSV_DIR.mkdir(parents=True, exist_ok=True)
DATA_EXCEL_DIR.mkdir(parents=True, exist_ok=True)

# Archivos finales
OUTPUT_CSV_PANEL = DATA_CSV_DIR / "panel_raw.csv"
OUTPUT_CSV_MANIFEST = DATA_CSV_DIR / "manifest_fuentes_raw.csv"
OUTPUT_EXCEL_MASTER = DATA_EXCEL_DIR / "APE1_Auditoria_Master.xlsx"
OUTPUT_SERIES_PICKLE = DATA_RAW_DIR / "series_catalog.pkl"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
PAISES_LA = {
    "AR": "Argentina",  "BO": "Bolivia",    "BR": "Brasil",
    "CL": "Chile",      "CO": "Colombia",   "CR": "Costa Rica",
    "CU": "Cuba",       "EC": "Ecuador",    "SV": "El Salvador",
    "GT": "Guatemala",  "HT": "Haití",      "HN": "Honduras",
    "MX": "México",     "NI": "Nicaragua",  "PA": "Panamá",
    "PY": "Paraguay",   "PE": "Perú",       "DO": "República Dominicana",
    "UY": "Uruguay",    "VE": "Venezuela",
}
CODIGOS = list(PAISES_LA.keys())
PAISES_STR = ";".join(CODIGOS)
ANIO_INI, ANIO_FIN = 2000, 2023
UTC_NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ─── CATÁLOGO OFICIAL DE SERIES ───────────────────────────────────────────────
SERIES_RAW = [
    {
        "nombre_raw":     "forest_area_km2",
        "codigo_api":     "AG.LND.FRST.K2",
        "unidad_api":     "km²",
        "fuente":         "World Bank WDI",
        "institucion":    "World Bank / FAO",
        "url_indicador":  "https://data.worldbank.org/indicator/AG.LND.FRST.K2",
        "rol":            "dependiente — ambiental",
        "concepto":       "Superficie forestal total",
    },
    {
        "nombre_raw":     "ghg_total_incl_lulucf_mt_co2e",
        "codigo_api":     "EN.GHG.ALL.LU.MT.CE.AR5",
        "unidad_api":     "Mt CO2 equivalente",
        "fuente":         "World Bank WDI / EDGAR",
        "institucion":    "World Bank / JRC",
        "url_indicador":  "https://data.worldbank.org/indicator/EN.GHG.ALL.LU.MT.CE.AR5",
        "rol":            "dependiente — ambiental",
        "concepto":       "Emisiones de GEI totales con LULUCF",
    },
    {
        "nombre_raw":     "gdp_per_capita_const2015_usd",
        "codigo_api":     "NY.GDP.PCAP.KD",
        "unidad_api":     "USD constantes 2015",
        "fuente":         "World Bank WDI",
        "institucion":    "World Bank",
        "url_indicador":  "https://data.worldbank.org/indicator/NY.GDP.PCAP.KD",
        "rol":            "independiente — económica",
        "concepto":       "PIB per cápita (Crecimiento)",
    },
    {
        "nombre_raw":     "trade_pct_gdp",
        "codigo_api":     "NE.TRD.GNFS.ZS",
        "unidad_api":     "% del PIB",
        "fuente":         "World Bank WDI",
        "institucion":    "World Bank",
        "url_indicador":  "https://data.worldbank.org/indicator/NE.TRD.GNFS.ZS",
        "rol":            "independiente — apertura",
        "concepto":       "Apertura comercial (Expo+Impo)",
    },
    {
        "nombre_raw":     "fdi_inflows_pct_gdp",
        "codigo_api":     "BX.KLT.DINV.WD.GD.ZS",
        "unidad_api":     "% del PIB",
        "fuente":         "World Bank WDI / FMI",
        "institucion":    "World Bank / FMI",
        "url_indicador":  "https://data.worldbank.org/indicator/BX.KLT.DINV.WD.GD.ZS",
        "rol":            "independiente — inversión",
        "concepto":       "Inversión Extranjera Directa (IED)",
    },
    {
        "nombre_raw":     "renewable_energy_pct_final_energy",
        "codigo_api":     "EG.FEC.RNEW.ZS",
        "unidad_api":     "% del consumo total",
        "fuente":         "World Bank WDI / IEA",
        "institucion":    "World Bank / IEA",
        "url_indicador":  "https://data.worldbank.org/indicator/EG.FEC.RNEW.ZS",
        "rol":            "control — tecnología verde",
        "concepto":       "Consumo de energía renovable",
    },
    {
        "nombre_raw":     "domestic_credit_private_pct_gdp",
        "codigo_api":     "FS.AST.PRVT.GD.ZS",
        "unidad_api":     "% del PIB",
        "fuente":         "World Bank WDI / FMI",
        "institucion":    "World Bank / FMI",
        "url_indicador":  "https://data.worldbank.org/indicator/FS.AST.PRVT.GD.ZS",
        "rol":            "control — financiero",
        "concepto":       "Profundidad financiera (Crédito privado)",
    },
    {
        "nombre_raw":     "wgi_voice_accountability_est",
        "codigo_api":     "GOV_WGI_VA.EST",
        "unidad_api":     "Índice -2.5 a +2.5",
        "fuente":         "World Bank WGI",
        "institucion":    "World Bank",
        "url_indicador":  "https://www.worldbank.org/en/publication/worldwide-governance-indicators",
        "rol":            "control — gobernanza",
        "concepto":       "Rendición de cuentas y voz",
    },
    {
        "nombre_raw":     "co2_emissions_kt",
        "codigo_api":     "EN.ATM.CO2E.KT",
        "unidad_api":     "kt de CO2",
        "fuente":         "World Bank WDI",
        "institucion":    "World Bank",
        "url_indicador":  "https://data.worldbank.org/indicator/EN.ATM.CO2E.KT",
        "rol":            "dependiente — ambiental",
        "concepto":       "Emisiones de CO2 totales",
    },
]

# ─── FUNCIÓN DE DESCARGA RAW (CERO TRANSFORMACIONES) ─────────────────────────
def fetch_raw(series_meta, countries_str, start, end, session=None):
    code = series_meta["codigo_api"]
    df, meta = utils_fetch_wb(code, countries_str, start, end, session=session)
    if not df.empty:
        df = df[df["iso2"].isin(CODIGOS)].drop_duplicates(["iso2", "year"])
    return df, meta

# ─── CONSTRUCCIÓN PANEL RAW ───────────────────────────────────────────────────
def build_raw_panel():
    base = pd.DataFrame(
        list(product(CODIGOS, range(ANIO_INI, ANIO_FIN + 1))),
        columns=["iso2", "year"]
    )
    base["pais"] = base["iso2"].map(PAISES_LA)
    base = base[["iso2", "pais", "year"]]

    manifest = []
    n = len(SERIES_RAW)

    for i, s in enumerate(SERIES_RAW, 1):
        print(f"  [{i:02d}/{n}] {s['nombre_raw']} ({s['codigo_api']})...")
        df_s, meta = fetch_raw(s, PAISES_STR, ANIO_INI, ANIO_FIN)
        
        meta["variable"] = s["nombre_raw"]
        meta["proveedor"] = s["institucion"]
        manifest.append(meta)

        if df_s.empty or df_s["value"].notna().sum() == 0:
            print("    → SIN DATOS")
            base[s["nombre_raw"]] = np.nan
        else:
            df_s = df_s.rename(columns={"value": s["nombre_raw"]})
            base = base.merge(df_s[["iso2", "year", s["nombre_raw"]]], on=["iso2", "year"], how="left")
            print(f"    → {df_s[s['nombre_raw']].notna().sum()} obs válidas")
        time.sleep(0.15)

    return base, manifest

if __name__ == "__main__":
    print("=" * 70)
    print("APE1 — GENERACIÓN DE ENTREGABLE (CSV + EXCEL MASTER)")
    print(f"Inicio: {UTC_NOW}")
    print("=" * 70)

    panel_raw, manifest_data = build_raw_panel()

    # 1. Exportar CSVs para herramientas (Carpeta Segregada)
    panel_raw.to_csv(str(OUTPUT_CSV_PANEL), index=False, encoding="utf-8-sig")
    pd.DataFrame(manifest_data).to_csv(str(OUTPUT_CSV_MANIFEST), index=False, encoding="utf-8-sig")

    # 2. Generar Excel Maestro para Humanos (Tu Hoja de Diccionario)
    print(f"\nConstruyendo Excel Maestro: {OUTPUT_EXCEL_MASTER.name}...")
    
    # Hoja de Diccionario de Variables (Petición Específica)
    diccionario = []
    for s in SERIES_RAW:
        diccionario.append({
            "Variables": s["nombre_raw"],
            "Unidad de medida": s.get("unidad_api", "N/A"),
            "Definición": s.get("concepto", "N/A"),
            "Fuente": s.get("institucion", "N/A"),
            "Link": s.get("url_indicador", "N/A")
        })
    df_diccionario = pd.DataFrame(diccionario)

    with pd.ExcelWriter(OUTPUT_EXCEL_MASTER, engine='xlsxwriter') as writer:
        # PESTAÑA 1: DICCIONARIO
        df_diccionario.to_excel(writer, sheet_name="Diccionario", index=False)
        
        # PESTAÑA 2: DATA MASTER (PANEL COMPLETO)
        panel_raw.to_excel(writer, sheet_name="Panel_Forense", index=False)

        # PESTAÑAS TEMÁTICAS (Para tu comodidad visual)
        ejes = {
            "Ecomonia": ["económica", "apertura", "inversión"],
            "Ambiental": ["ambiental", "tecnología verde"],
            "Institucional": ["gobernanza", "financiero"]
        }

        for sheet_title, keywords in ejes.items():
            cols_eje = [s['nombre_raw'] for s in SERIES_RAW if any(kw in s['rol'] for kw in keywords)]
            available_cols = ['iso2', 'pais', 'year'] + [c for c in cols_eje if c in panel_raw.columns]
            if len(available_cols) > 3:
                panel_raw[available_cols].to_excel(writer, sheet_name=sheet_title, index=False)

    # 3. Guardar catálogo pickle interno
    import pickle
    with open(OUTPUT_SERIES_PICKLE, "wb") as f:
        pickle.dump(SERIES_RAW, f)

    print("\n✅ PROCESO FINALIZADO")
    print(f"→ Herramientas (CSVs): {DATA_CSV_DIR}")
    print(f"→ Humanos (Excel): {OUTPUT_EXCEL_MASTER}")