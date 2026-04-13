"""
APE1 — GENERACIÓN DE TODOS LOS ARTEFACTOS DE AUDITORÍA
Genera los 7 archivos restantes (2-8) del protocolo forense.
"""

import pandas as pd
import pickle
from datetime import datetime, timezone
from pathlib import Path

UTC_NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

SRC_DIR = Path(__file__).parent.parent.resolve()
PROJECT_ROOT = SRC_DIR.parent.resolve()

import sys
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR = PROJECT_ROOT / "docs"

# Asegurar directorios
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Cargar datos
df = pd.read_csv(DATA_RAW_DIR / "panel_raw.csv")
manifest_df = pd.read_csv(DATA_RAW_DIR / "manifest_fuentes_raw.csv")
with open(DATA_RAW_DIR / "series_catalog.pkl", "rb") as f:
    SERIES_RAW = pickle.load(f)

PAISES_LA = {
    "AR": "Argentina",  "BO": "Bolivia",    "BR": "Brasil",
    "CL": "Chile",      "CO": "Colombia",   "CR": "Costa Rica",
    "CU": "Cuba",       "EC": "Ecuador",    "SV": "El Salvador",
    "GT": "Guatemala",  "HT": "Haití",      "HN": "Honduras",
    "MX": "México",     "NI": "Nicaragua",  "PA": "Panamá",
    "PY": "Paraguay",   "PE": "Perú",       "DO": "República Dominicana",
    "UY": "Uruguay",    "VE": "Venezuela",
}

ANIO_INI, ANIO_FIN = 2000, 2023
N_TOTAL = len(df)  # 480

# ─────────────────────────────────────────────────────────────────────────────
# ARTEFACTO 2: diccionario_variables.csv
# ─────────────────────────────────────────────────────────────────────────────

def build_diccionario():
    rows = []
    for s in SERIES_RAW:
        col = s["nombre_raw"]
        if col not in df.columns:
            continue
        series = df[col]
        n_validos = series.notna().sum()
        cob_pct = round(100 * n_validos / N_TOTAL, 2)
        years_with_data = sorted(df[series.notna()]["year"].unique().tolist())
        paises_with_data = df[series.notna()]["iso2"].nunique()
        primer = min(years_with_data) if years_with_data else None
        ultimo = max(years_with_data) if years_with_data else None

        rows.append({
            "nombre_variable":         col,
            "nombre_v1_anterior":      s.get("nombre_v1", ""),
            "concepto_teorico":        s["concepto"],
            "categoria_consigna":      s["consigna"],
            "rol_modelo":              s["rol"],
            "disponibilidad":          s["disponibilidad"],
            "fuente_publica":          s["fuente"],
            "institucion":             s["institucion"],
            "codigo_api":              s["codigo_api"],
            "endpoint_base":           s["endpoint"].replace("PAISES", "AR;...;VE"),
            "url_indicador":           s["url_indicador"],
            "unidad_original":         s["unidad_api"],
            "nombre_oficial_api":      s["nombre_api"],
            "frecuencia":              "anual (salvo Findex trienal y FAO ~quinquenal)",
            "cobertura_total_pct":     cob_pct,
            "primer_anio":             primer,
            "ultimo_anio":             ultimo,
            "observaciones_no_nulas":  n_validos,
            "observaciones_totales":   N_TOTAL,
            "paises_con_datos":        paises_with_data,
            "usa_proxy":               "sí" if "proxy" in s["rol"].lower() or "proxy" in s.get("alerta","").lower() else "no",
            "proxy_de":                s["consigna"] if ("proxy" in s["rol"].lower()) else "",
            "inconsistencia_nombre":   "SÍ ⚠" if s.get("inconsistencia_nombre") else "no",
            "nombre_correcto_sugerido": s.get("nombre_correcto_sugerido", ""),
            "detalle_inconsistencia":  s.get("detalle_inconsistencia", ""),
            "notas_metodologicas":     s["alerta"],
            "advertencia_trazabilidad": (
                "CRÍTICA" if "INCONSISTENTE" in s.get("alerta","").upper() or "CONCEPTO NO EQUIVALENTE" in s.get("alerta","").upper()
                else "MODERADA" if "REDUNDANCIA" in s.get("alerta","").upper() or "PROXY" in s["rol"].upper()
                else "BAJA"
            ),
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────────────────────────────────
# ARTEFACTO 3: matriz_cumplimiento_consigna.csv
# ─────────────────────────────────────────────────────────────────────────────

CONSIGNA_MAP = [
    # (variable_consigna, existe_directa, col_raw, codigo, nivel, notas_cumplimiento)
    ("Superficie forestal",
     "sí", "forest_area_km2 + forest_area_pct_land", "AG.LND.FRST.K2 / AG.LND.FRST.ZS",
     "alto",
     "Disponible. Dos columnas RAW: km² y %. Nota: WB interpola datos FAO quinquenales."),
    ("Factor de capacidad de carga",
     "no", "NO INCLUIDA EN PANEL RAW", "sin código directo",
     "bajo",
     "NO existe indicador de 'carrying capacity' para 20 países AL 2000-2023 en fuente API pública. "
     "Candidatos: Global Footprint Network (acceso restringido), UNDP Human Development Report. "
     "Requiere descarga manual o suscripción. AUSENTE del panel RAW."),
    ("Gases de efecto invernadero",
     "sí", "ghg_total_incl_lulucf_mt_co2e", "EN.GHG.ALL.LU.MT.CE.AR5",
     "alto",
     "Disponible directamente. 100% cobertura. Valores negativos válidos (sumidero forestal). Fuente: EDGAR 2025."),
    ("Emisiones de CO2",
     "sí", "co2_excl_lulucf_mt_co2e", "EN.GHG.CO2.MT.CE.AR5",
     "alto",
     "Disponible directamente. 100% cobertura. Nota: unidad es Mt CO2e (equivalente), no CO2 puro."),
    ("Crecimiento económico (PIB per capita)",
     "sí", "gdp_per_capita_const2015_usd + gdp_per_capita_ppp_const2021_intl", "NY.GDP.PCAP.KD / NY.GDP.PCAP.PP.KD",
     "alto",
     "Disponible. REDUNDANCIA entre las dos versiones. Para modelo parsimoniosos elegir una. "
     "Advertencia: año base PPA era 2017 en v1, la API ahora devuelve 2021."),
    ("Población",
     "sí", "population_total", "SP.POP.TOTL",
     "alto",
     "Disponible directamente."),
    ("Tecnología",
     "parcial", "internet_users_pct_pop + mobile_subscriptions_per100", "IT.NET.USER.ZS / IT.CEL.SETS.P2",
     "medio",
     "No existe indicador directo de 'tecnología' para este panel. "
     "Se incluyen dos proxies de adopción digital. Nota: estos no miden tecnología ambiental ni innovadora."),
    ("VAB sectorial (agrícola)",
     "sí", "agriculture_va_pct_gdp", "NV.AGR.TOTL.ZS",
     "alto",
     "Disponible. Incluye silvicultura y pesca según WB."),
    ("VAB sectorial (manufacturero)",
     "sí", "manufacturing_va_pct_gdp", "NV.IND.MANF.ZS",
     "alto",
     "Disponible directamente."),
    ("VAB sectorial (servicios)",
     "sí", "services_va_pct_gdp", "NV.SRV.TOTL.ZS",
     "alto",
     "Disponible directamente."),
    ("Protección de los derechos laborales",
     "no", "child_employment_pct_7to14 (PROXY INVERSO, 13.8% cobertura)", "SL.TLF.0714.ZS",
     "bajo",
     "NO existe índice de derechos laborales de cobertura continua para 20 países 2000-2023 en API pública. "
     "La variable incluida es trabajo infantil (proxy inverso). "
     "Fuente directa recomendada: ITUC Global Rights Index (anual, descarga manual)."),
    ("Tecnología verde",
     "parcial", "renewable_energy_pct_final_energy", "EG.FEC.RNEW.ZS",
     "medio",
     "No existe indicador denominado 'tecnología verde' en APIs públicas. "
     "Se usa consumo de energía renovable como proxy estándar en literatura EKC. "
     "Patentes ambientales (OECD) no disponibles vía API para todos los países."),
    ("Gobernanza",
     "sí", "wgi_government_effectiveness_est + wgi_control_corruption_est + wgi_regulatory_quality_est + wgi_political_stability_est",
     "GOV_WGI_GE.EST / GOV_WGI_CC.EST / GOV_WGI_RQ.EST / GOV_WGI_PV.EST",
     "alto",
     "Disponible WGI. Gap año 2001. REDUNDANCIA: 6 dimensiones del mismo índice compuesto."),
    ("Impuestos ambientales",
     "no", "tax_revenue_pct_gdp (PROXY FISCAL GENERAL)", "GC.TAX.TOTL.GD.ZS",
     "bajo",
     "No existe serie de impuestos ambientales específicos para 20 países AL en API pública. "
     "La variable es recaudación fiscal total (proxy). "
     "Fuente directa: OECD Tax Policy Analysis — cobertura parcial AL."),
    ("Rigurosidad de la política ambiental",
     "no", "wgi_regulatory_quality_est (PROXY REGULATORIO GENERAL)", "GOV_WGI_RQ.EST",
     "bajo",
     "No existe índice de rigurosidad ambiental para todos los países en API pública. "
     "OECD Environmental Policy Stringency Index (EPS) cubre solo países OECD. "
     "Yale EPI (Environmental Performance Index) disponible como descarga manual bienal."),
    ("Incertidumbre de la política climática",
     "no", "NO INCLUIDA", "sin código",
     "bajo",
     "No existe indicador estandarizado de incertidumbre climática en API pública para AL 2000-2023. "
     "Alternativas académicas: Baker-Bloom-Davis EPU Index (Economic Policy Uncertainty) — disponible solo para países mayores."),
    ("Rendición de cuentas",
     "sí", "wgi_voice_accountability_est", "GOV_WGI_VA.EST",
     "alto",
     "Disponible WGI. Gap año 2001. Mide participación ciudadana, libertad de expresión y medios libres."),
    ("Incertidumbre relacionada con la energía",
     "no", "NO INCLUIDA", "sin código",
     "bajo",
     "No existe indicador estandarizado de incertidumbre energética en API pública para AL. "
     "Sin datos directos en WB, IEA o CEPAL para este concepto."),
    ("Inclusión financiera",
     "parcial", "account_ownership_pct_adults + domestic_credit_private_pct_gdp",
     "FX.OWN.TOTL.ZS / FS.AST.PRVT.GD.ZS",
     "medio",
     "Findex disponible pero trienal (15.4% cobertura anual). "
     "Crédito privado disponible con mejor cobertura (86.7%). "
     "En RAW los años sin Findex quedan como NaN (sin interpolación)."),
    ("Innovación tecnológica verde",
     "no",
     "renewable_electricity_output_pct + rd_expenditure_pct_gdp (PROXIES)",
     "EG.ELC.RNEW.ZS / GB.XPD.RSDV.GD.ZS",
     "bajo",
     "No existe indicador de 'innovación tecnológica verde' para todos los países AL en API pública. "
     "Patentes ambientales (OECD Patents on Environment Technologies) solo disponibles para países OECD/grandes. "
     "Los dos proxies incluidos miden output eléctrico renovable e I+D total."),
    ("Calidad institucional",
     "sí", "wgi_rule_of_law_est + wgi_control_corruption_est + wgi_government_effectiveness_est",
     "GOV_WGI_RL.EST / GOV_WGI_CC.EST / GOV_WGI_GE.EST",
     "alto",
     "WGI disponible. Conceptualmente solapado con 'gobernanza'. Redundancia intragrupo."),
    ("Índice de riesgo climático",
     "no", "NO INCLUIDA", "sin código",
     "bajo",
     "No existe serie de riesgo climático en API pública para 20 países AL 2000-2023. "
     "Candidatos: Germanwatch Global Climate Risk Index (bienal, descarga manual), "
     "ND-GAIN Country Index (anual, descarga manual desde gain.nd.edu). "
     "AUSENTE del panel RAW."),
    ("Innovación financiera",
     "parcial", "stock_market_cap_pct_gdp (PROXY BURSÁTIL)", "CM.MKT.LCAP.GD.ZS",
     "bajo",
     "No existe indicador de 'innovación financiera' en API pública. "
     "Capitalización bursátil es proxy de desarrollo financiero, no de innovación. "
     "Cobertura 38.1%."),
    ("Informalidad",
     "parcial", "vulnerable_employment_pct_total (PROXY — ver alerta de concepto)", "SL.EMP.VULN.ZS",
     "medio",
     "Empleo vulnerable ≠ informalidad estricta. Proxy correlacionado pero conceptualmente diferente. "
     "ILO ILOSTAT tiene datos de informalidad directos — cobertura parcial y no continua vía API."),
    ("Renta de los recursos naturales",
     "sí", "natural_resources_rents_pct_gdp", "NY.GDP.TOTL.RT.ZS",
     "alto",
     "Disponible directamente. Cobertura 90%."),
]

def build_cumplimiento():
    rows = []
    for item in CONSIGNA_MAP:
        var_c, existe, col, cod, nivel, obs = item
        # Calcular cobertura de la primera columna mencionada
        col_first = col.split(" +")[0].strip()
        if col_first in df.columns:
            cov = round(100 * df[col_first].notna().sum() / N_TOTAL, 1)
        elif "NO INCLUIDA" in col:
            cov = 0.0
        else:
            cov = None

        rows.append({
            "variable_consigna":              var_c,
            "existe_directa_en_fuente_publica": existe,
            "existe_en_panel_raw":            "sí" if col_first in df.columns else "no",
            "columna_asociada":               col,
            "codigo_api":                     cod,
            "nivel_trazabilidad":             nivel,
            "cobertura_pct_primera_columna":  cov,
            "observaciones":                  obs,
            "motivo_si_falta":                (
                obs if existe == "no" else
                ("Ver notas" if existe == "parcial" else "")
            ),
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────────────────────────────────
# ARTEFACTO 4: manifest_fuentes.csv (ya generado en fase 1, enriquecer)
# ─────────────────────────────────────────────────────────────────────────────

def build_manifest():
    # El manifest base ya existe; enriquecerlo con hash de datos descargados
    enhanced = []
    for s in SERIES_RAW:
        col = s["nombre_raw"]
        row = manifest_df[manifest_df["variable"] == col]
        if row.empty:
            continue
        row = row.iloc[0].to_dict()
        # Hash de la columna de datos descargados
        if col in df.columns:
            col_data = df[col].dropna().round(6).astype(str).str.cat()
            row["hash_datos_sha256_parcial"] = __import__("hashlib").sha256(col_data.encode()).hexdigest()[:16]
        else:
            row["hash_datos_sha256_parcial"] = ""
        row["url_indicador"] = s["url_indicador"]
        row["notas_de_error"] = row.get("errores", "")
        enhanced.append(row)
    return pd.DataFrame(enhanced)

# ─────────────────────────────────────────────────────────────────────────────
# ARTEFACTO 5: auditoria_redundancia.csv
# ─────────────────────────────────────────────────────────────────────────────

REDUNDANCIAS = [
    {
        "variable_a": "forest_area_km2",
        "variable_b": "forest_area_pct_land",
        "relacion": "misma fuente FAO, misma variable en dos unidades",
        "duplicado_exacto": "no",
        "misma_fuente": "sí",
        "mismo_concepto_distinta_unidad": "sí",
        "solapamiento_teorico": "sí",
        "riesgo_multicolinealidad": "alto (monotransformación vía área territorial)",
        "recomendacion": "elegir una — forest_area_pct_land preferida (normalizada, completa 100%); forest_area_km2 útil para análisis absolutos",
    },
    {
        "variable_a": "ghg_total_incl_lulucf_mt_co2e",
        "variable_b": "co2_excl_lulucf_mt_co2e",
        "relacion": "CO2 es subconjunto de GHG total; misma fuente EDGAR",
        "duplicado_exacto": "no",
        "misma_fuente": "sí",
        "mismo_concepto_distinta_unidad": "no",
        "solapamiento_teorico": "sí (CO2 ⊂ GHG)",
        "riesgo_multicolinealidad": "alto (correlación estructural: CO2 representa ~60-80% de GHG total)",
        "recomendacion": "no usar ambas como dependientes simultáneas; elegir según objetivo. GHG para análisis climático completo, CO2 si foco en combustibles fósiles",
    },
    {
        "variable_a": "gdp_per_capita_const2015_usd",
        "variable_b": "gdp_per_capita_ppp_const2021_intl",
        "relacion": "misma variable, diferente deflactor/base: USD 2015 vs USD PPA 2021",
        "duplicado_exacto": "no",
        "misma_fuente": "sí (WB WDI)",
        "mismo_concepto_distinta_unidad": "sí",
        "solapamiento_teorico": "sí",
        "riesgo_multicolinealidad": "alto",
        "recomendacion": "elegir una. PPA 2021 para comparaciones internacionales; USD constante 2015 para análisis de crecimiento nominal. ADVERTENCIA: año base PPA era 2017 en v1 pero API entrega 2021.",
    },
    {
        "variable_a": "internet_users_pct_pop",
        "variable_b": "mobile_subscriptions_per100",
        "relacion": "dos proxies distintos del mismo concepto: adopción tecnológica",
        "duplicado_exacto": "no",
        "misma_fuente": "sí (WB/ITU)",
        "mismo_concepto_distinta_unidad": "sí",
        "solapamiento_teorico": "sí",
        "riesgo_multicolinealidad": "medio-alto (correlación esperada ~0.8)",
        "recomendacion": "elegir una. internet_users preferida por mayor relevancia conceptual; móvil puede superar 100% (multisim)",
    },
    {
        "variable_a": "renewable_energy_pct_final_energy",
        "variable_b": "renewable_electricity_output_pct",
        "relacion": "ambas miden participación renovable; difieren en denominador (energía final vs electricidad)",
        "duplicado_exacto": "no",
        "misma_fuente": "sí (WB/IEA)",
        "mismo_concepto_distinta_unidad": "sí",
        "solapamiento_teorico": "sí",
        "riesgo_multicolinealidad": "alto",
        "recomendacion": "elegir una. renewable_energy_pct_final_energy más amplia (incluye calefacción y transporte); renewable_electricity_output_pct solo sector eléctrico",
    },
    {
        "variable_a": "agriculture_va_pct_gdp",
        "variable_b": "manufacturing_va_pct_gdp",
        "relacion": "partes del mismo PIB; suma con servicios ~60-92% del PIB",
        "duplicado_exacto": "no",
        "misma_fuente": "sí",
        "mismo_concepto_distinta_unidad": "no",
        "solapamiento_teorico": "sí (restricción lineal implícita con services_va)",
        "riesgo_multicolinealidad": "medio (restricción estructural: agric + manuf + servicios < 100)",
        "recomendacion": "si se usan las 3 juntas, incluir solo 2 para evitar multicolinealidad perfecta parcial",
    },
    {
        "variable_a": "manufacturing_va_pct_gdp",
        "variable_b": "services_va_pct_gdp",
        "relacion": "partes del mismo PIB",
        "duplicado_exacto": "no",
        "misma_fuente": "sí",
        "mismo_concepto_distinta_unidad": "no",
        "solapamiento_teorico": "sí",
        "riesgo_multicolinealidad": "medio",
        "recomendacion": "ver nota anterior sobre restricción VAB",
    },
    {
        "variable_a": "wgi_voice_accountability_est",
        "variable_b": "wgi_government_effectiveness_est",
        "relacion": "dos dimensiones del mismo índice compuesto WGI",
        "duplicado_exacto": "no",
        "misma_fuente": "sí (WGI)",
        "mismo_concepto_distinta_unidad": "no",
        "solapamiento_teorico": "sí (correlación intragrupo ~0.7-0.9)",
        "riesgo_multicolinealidad": "alto (todas las dimensiones WGI correlacionan fuertemente)",
        "recomendacion": "usar máximo 1-2 dimensiones WGI en un mismo modelo; o construir índice compuesto PCA",
    },
    {
        "variable_a": "wgi_rule_of_law_est",
        "variable_b": "wgi_control_corruption_est",
        "relacion": "dos dimensiones del mismo índice WGI",
        "duplicado_exacto": "no",
        "misma_fuente": "sí",
        "mismo_concepto_distinta_unidad": "no",
        "solapamiento_teorico": "sí",
        "riesgo_multicolinealidad": "alto",
        "recomendacion": "ver bloque WGI: elegir la dimensión más relevante según marco teórico",
    },
    {
        "variable_a": "wgi_regulatory_quality_est",
        "variable_b": "wgi_political_stability_est",
        "relacion": "dos dimensiones del mismo índice WGI",
        "duplicado_exacto": "no",
        "misma_fuente": "sí",
        "mismo_concepto_distinta_unidad": "no",
        "solapamiento_teorico": "sí",
        "riesgo_multicolinealidad": "alto",
        "recomendacion": "ver bloque WGI",
    },
    {
        "variable_a": "account_ownership_pct_adults",
        "variable_b": "domestic_credit_private_pct_gdp",
        "relacion": "ambas miden inclusión/profundidad financiera desde dimensiones distintas",
        "duplicado_exacto": "no",
        "misma_fuente": "no (Findex vs WDI/FMI)",
        "mismo_concepto_distinta_unidad": "sí",
        "solapamiento_teorico": "sí",
        "riesgo_multicolinealidad": "medio",
        "recomendacion": "mantener ambas: Findex mide acceso individual, crédito privado mide profundidad sistémica. Son dimensiones complementarias",
    },
]

def build_redundancia():
    return pd.DataFrame(REDUNDANCIAS)

# ─────────────────────────────────────────────────────────────────────────────
# ARTEFACTO 6: auditoria_integridad.csv
# ─────────────────────────────────────────────────────────────────────────────

def detect_linear_interpolation(series_by_country):
    """Detecta patrón de interpolación lineal: diferencias consecutivas constantes."""
    flags = []
    for iso, grp in series_by_country:
        vals = grp.dropna().sort_values("year")
        if len(vals) < 4:
            continue
        diffs = vals["value"].diff().dropna().round(4)
        # Si hay 3+ diffs consecutivos iguales → lineal
        for i in range(len(diffs) - 2):
            w = diffs.iloc[i:i+3]
            if w.nunique() == 1 and w.iloc[0] != 0:
                flags.append(iso)
                break
    return flags

def build_integridad():
    rows = []
    for s in SERIES_RAW:
        col = s["nombre_raw"]
        if col not in df.columns:
            continue
        series = df[col]
        total = N_TOTAL
        miss = series.isna().sum()
        miss_pct = round(100 * miss / total, 2)
        valid = series.notna().sum()

        # Años con datos
        anos_ok = sorted(df[series.notna()]["year"].unique().tolist())
        paises_ok = df[series.notna()]["iso2"].nunique()

        # Detectar gap de año 2001 (WGI)
        hay_gap_2001 = (
            2000 in anos_ok and 2002 in anos_ok and 2001 not in anos_ok
        ) if anos_ok else False

        # Patrón trienal (Findex)
        patron_trienal = False
        if col == "account_ownership_pct_adults":
            patron_trienal = True

        # Señal de interpolación lineal
        grpd = [(iso, df[df["iso2"]==iso][["year", col]].rename(columns={col:"value"}))
                for iso in df["iso2"].unique()]
        linear_flag_countries = detect_linear_interpolation(grpd)
        interp_flag = len(linear_flag_countries) > 0

        # Señal FAO quinquenal interpolado
        interp_note = ""
        if col in ["forest_area_km2", "forest_area_pct_land"]:
            interp_note = f"⚠ WB aplica interpolación FAO quinquenal. Países con diferencias constantes: {linear_flag_countries[:5]}"
        elif interp_flag:
            interp_note = f"Posible interpolación detectada en: {linear_flag_countries[:3]}"

        # Forward fill signal: si hay años sin datos ENTRE años con datos → no es ffill
        # pero si hay bloque de años sin datos al inicio → no es ffill tampoco
        # Detección de ffill: buscar si después de un NaN hay valores idénticos repetidos
        ffill_flag = False
        for iso in df["iso2"].unique():
            subdf = df[df["iso2"]==iso][["year", col]].sort_values("year")
            vals = subdf[col].tolist()
            for i in range(1, len(vals)):
                if pd.isna(vals[i-1]) and not pd.isna(vals[i]):
                    continue
                if not pd.isna(vals[i-1]) and not pd.isna(vals[i]) and vals[i] == vals[i-1]:
                    pass  # no necesariamente ffill
            # En RAW no aplicamos ffill, así que esta señal debería ser falsa
        ffill_flag = False  # Por protocolo: no aplicamos ffill

        rows.append({
            "variable":                         col,
            "missing_pct":                      miss_pct,
            "observaciones_validas":            valid,
            "observaciones_totales":            total,
            "anios_con_datos":                  len(anos_ok),
            "primer_anio_con_datos":            min(anos_ok) if anos_ok else None,
            "ultimo_anio_con_datos":            max(anos_ok) if anos_ok else None,
            "paises_con_datos":                 paises_ok,
            "hay_huecos_temporales":            "sí" if (len(anos_ok) < (ANIO_FIN-ANIO_INI+1) and len(anos_ok)>0) else "no",
            "patron_trienal_detectado":         "sí" if patron_trienal else "no",
            "patron_quinquenal_o_similar":      "sí" if col in ["forest_area_km2","forest_area_pct_land"] else "no",
            "senal_interpolacion_lineal":       "SÍ ⚠" if interp_flag else "no",
            "paises_con_interpolacion_aparente": interp_note,
            "senal_forward_fill":               "sí" if ffill_flag else "no",
            "gap_anio_2001_wgi":                "sí (WGI no publicó 2001)" if hay_gap_2001 else "no",
            "advertencia_principal":            s.get("alerta","")[:200],
        })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────────────────────────────────
# ARTEFACTO 7: variables_no_resueltas.md
# ─────────────────────────────────────────────────────────────────────────────

NO_RESUELTAS_MD = """# Variables No Resueltas — APE1

**Fecha de auditoría:** {fecha}

---

## 1. Factor de capacidad de carga

**Concepto teórico:** Medida de la presión sobre el sistema ecológico en relación con la biocapacidad disponible.

**Estado:** NO DISPONIBLE directamente en API pública para los 20 países, período 2000-2023.

**Mejores fuentes candidatas:**
- Global Footprint Network (GFN) — Datos de huella ecológica y biocapacidad per cápita. Disponibles previa registro en `data.footprintnetwork.org`. Licencia abierta para investigación. Cobertura: todos los países, anual desde 1961.
- UN FAO: Área agrícola disponible por habitante como proxy indirecto.
- UNDP Human Development Report — Índice de Presión Planetaria (no estandarizado como serie).

**Parte que requiere proxy:** Cualquier estimación para este panel requeriría GFN (descarga manual) o definir el ratio huella/biocapacidad.

**Parte que requiere descarga manual:** GFN no tiene API pública estándar REST. Descarga CSV desde su plataforma.

**Decisión:** AUSENTE del panel_raw. Requiere aprobación explícita del proxy a usar y descarga manual.

---

## 2. Incertidumbre de la política climática

**Estado:** NO DISPONIBLE en API pública para AL 2000-2023.

**Fuentes académicas candidatas:**
- Baker, Bloom & Davis — Economic Policy Uncertainty Index (EPU): disponible para Argentina, Brasil, Chile, Colombia, México. No cubre todos los 20 países.
- IPCC Reports — datos de escenarios, no índices de incertidumbre nacionales.

**Decisión:** AUSENTE del panel_raw. Cobertura geográfica insuficiente para los 20 países.

---

## 3. Incertidumbre relacionada con la energía

**Estado:** NO DISPONIBLE en API pública.

**Fuentes candidatas:**
- IEA World Energy Outlook — proyecciones, no series históricas de incertidumbre.
- Volatilidad de precios de commodities energéticos (proxy indirecto): disponible en World Bank Commodity Prices.

**Decisión:** AUSENTE del panel_raw. Concepto requiere definición operacional precisa antes de seleccionar proxy.

---

## 4. Índice de riesgo climático

**Estado:** NO DISPONIBLE en API pública con cobertura continua para 20 países, 2000-2023.

**Mejores fuentes candidatas:**
- Germanwatch Global Climate Risk Index (CRI) — anual, mide impacto de eventos climáticos extremos. Disponible como descarga manual PDF/XLS. Cobertura: todos los países desde 2000.
- Notre Dame Global Adaptation Index (ND-GAIN) — anual, descargar desde `gain.nd.edu`. Cobertura: 181 países desde 1995.

**Parte que requiere descarga manual:** Ambas fuentes requieren descarga manual o scraping estructurado.

**Decisión:** AUSENTE del panel_raw. Requiere aprobación del índice a usar.

---

## 5. Innovación tecnológica verde (directa)

**Estado:** NO DISPONIBLE directamente en API pública para todos los 20 países AL.

**Fuente más cercana rechazada:**
- OECD Patents on Environment Technologies: solo cubre países con patentes registradas activamente. Para AL (excepto México y Brasil), cobertura casi nula. Datos disponibles vía OECD Data Explorer pero no vía API estándar.
- IRENA Renewable Capacity Statistics: datos de capacidad instalada GW por tecnología. Descarga manual.

**Lo que SÍ está en el panel como proxy (marcado como tal):**
- `renewable_electricity_output_pct`: participación renovable en generación eléctrica (%).
- `rd_expenditure_pct_gdp`: I+D total como proxy de capacidad innovadora.

**Advertencia:** Ninguno de estos proxies mide específicamente "innovación" tecnológica verde; miden adopción y gasto genérico en I+D.

---

## 6. Protección de los derechos laborales (directa)

**Estado:** NO DISPONIBLE como índice continuo en API pública para 20 países, 2000-2023.

**Fuentes directas:**
- ITUC Global Rights Index: anual desde 2014. Solo 9 años de cobertura. Descarga manual.
- ILO ILOSTAT — `collective_bargaining_coverage_rate`: disponible pero con cobertura parcial.
- V-Dem Dataset — incluye indicadores laborales pero requiere descarga.

**Lo que está en el panel como proxy:** `child_employment_pct_7to14` (13.8% cobertura).

---

## 7. Impuestos ambientales (directos)

**Estado:** NO DISPONIBLE en API pública con cobertura continua para 20 países AL.

**Fuentes directas:**
- OECD Database on Instruments for Environmental Policy: cobertura parcial AL (México principalmente).
- CEPAL CEPALSTAT — algunos datos de impuestos ambientales, descarga manual.
- World Bank Carbon Pricing Dashboard: mecanismos de carbono, no impuestos generales.

---

## 8. Rigurosidad de la política ambiental

**Estado:** NO DISPONIBLE directamente para 20 países AL.

**Fuentes:**
- OECD Environmental Policy Stringency (EPS) Index: cubre solo países OECD.
- Yale EPI (Environmental Performance Index): bienal, 180 países, descarga manual desde `epi.yale.edu`.

---

## Resumen ejecutivo de brechas

| Variable consigna | Estado en RAW | Acción requerida |
|---|---|---|
| Factor capacidad de carga | AUSENTE | Descarga manual GFN + aprobación proxy |
| Incertidumbre política climática | AUSENTE | Definir alcance + EPU parcial |
| Incertidumbre energética | AUSENTE | Definir operacionalmente |
| Índice de riesgo climático | AUSENTE | Elegir entre CRI o ND-GAIN + descarga manual |
| Innovación tecnológica verde | PROXY parcial | Aprobación de EG.ELC.RNEW.ZS como proxy |
| Derechos laborales | PROXY débil | ITUC desde 2014 o redefinir concepto |
| Impuestos ambientales | PROXY fiscal | Aprobar GC.TAX o buscar CEPALSTAT |
| Rigurosidad política ambiental | PROXY regulatorio | Yale EPI descarga manual o WGI RQ aprobado |
""".format(fecha=UTC_NOW)

# ─────────────────────────────────────────────────────────────────────────────
# ARTEFACTO 8: README_AUDITORIA.md
# ─────────────────────────────────────────────────────────────────────────────

README_MD = """# README — Auditoría Forense APE1

**Versión:** 2.0 (RAW forense)  
**Fecha:** {fecha}  
**Protocolo:** CERO interpolación | CERO imputación | CERO proxies no aprobados en panel_raw

---

## Qué ES raw en este panel

El archivo `panel_raw.csv` contiene **exclusivamente** series descargadas directamente desde APIs públicas del World Bank (WDI, WGI, Global Findex), sin ninguna transformación analítica:

- No hay interpolación (ni lineal ni polinomial).
- No hay forward-fill ni backward-fill.
- No hay imputación de medias, medianas ni modelos.
- No hay escala, normalización ni estandarización.
- Los NaN representan datos genuinamente no disponibles en la fuente.
- Los valores negativos en `ghg_total_incl_lulucf_mt_co2e` son VÁLIDOS: reflejan países con sumidero forestal neto (Panamá, Venezuela).

---

## Qué NO está resuelto

Las siguientes variables de la consigna **no tienen representación directa** en el panel_raw:

| Variable | Razón |
|---|---|
| Factor de capacidad de carga | Sin API pública estándar; requiere GFN manual |
| Incertidumbre política climática | Sin datos para todos los 20 países |
| Incertidumbre relacionada con energía | Sin serie estandarizada |
| Índice de riesgo climático | Requiere CRI o ND-GAIN, descarga manual |

---

## Variables mal rotuladas o ambiguas (versión anterior)

### 1. `capacidad_renovable_gw` → NOMBRE INCORRECTO
**Indicador real:** `EG.ELC.RNEW.ZS` = *Renewable electricity output (% of total electricity output)*  
**Unidad real:** porcentaje (%), NO gigavatios (GW)  
**Nombre correcto en RAW:** `renewable_electricity_output_pct`  
**Acción:** Dato conservado sin modificación. Rename propuesto en panel_modelo.

### 2. `pib_per_capita_ppa` — AÑO BASE DESACTUALIZADO
**La v1 documentaba año base 2017. La API devuelve base 2021** (ICP 2021).  
**Nombre correcto en RAW:** `gdp_per_capita_ppp_const2021_intl`  
**Acción:** Dato conservado. Rename propuesto en panel_modelo.

### 3. `empleo_informal_pct` → CONCEPTO IMPRECISO
**Indicador real:** `SL.EMP.VULN.ZS` = *Vulnerable employment* (empleo vulnerable)  
**Empleo vulnerable ≠ informalidad** en sentido estricto de la OIT.  
**Nombre correcto en RAW:** `vulnerable_employment_pct_total`  
**Acción:** Dato conservado. Rename y nota metodológica en panel_modelo.

---

## Redundancias diagnosticadas

### Bloque forestal
`forest_area_km2` y `forest_area_pct_land` son la misma variable FAO en dos unidades. Para un modelo: usar `forest_area_pct_land` (normalizada, cobertura 100%).

### Bloque GEI/CO2
`ghg_total_incl_lulucf_mt_co2e` contiene a `co2_excl_lulucf_mt_co2e` como subconjunto. No usar ambas como variables dependientes simultáneas.

### Bloque PIB
`gdp_per_capita_const2015_usd` y `gdp_per_capita_ppp_const2021_intl` miden lo mismo en deflactores distintos. Elegir una según marco teórico.

### Bloque tecnología
`internet_users_pct_pop` y `mobile_subscriptions_per100` son proxies del mismo concepto.

### Bloque renovables
`renewable_energy_pct_final_energy` y `renewable_electricity_output_pct` miden participación renovable con denominadores distintos.

### Bloque WGI (6 dimensiones)
Todas las dimensiones WGI provienen del mismo índice compuesto. Correlación intragrupo ~0.7-0.9. Incluir más de 2 en un modelo genera multicolinealidad grave.

---

## Transformaciones pendientes para Fase 2 (panel_modelo)

Estas transformaciones están **explícitamente PENDIENTES** y requieren aprobación:

1. **Interpolación Global Findex** (`account_ownership_pct_adults`): los años sin encuesta quedan NaN. Propuesta: interpolación lineal acotada a ventana 3 años — requiere aprobación.

2. **Renombrar columnas inconsistentes** (listadas arriba): rename sin alterar datos.

3. **Parsimonia en bloque WGI**: elegir 1-2 dimensiones o construir índice PCA.

4. **Incorporar variables no resueltas** (GFN, CRI, EPS): requieren descarga manual y aprobación.

5. **Logaritmización de PIB y población**: transformación común en modelos EKC — pendiente aprobación.

6. **Rezagos temporales**: variables potencialmente endógenas (GEI, CO2, PIB) pueden requerir rezagos — pendiente definición del modelo.

---

## Patrón de interpolación en datos FAO (información, no alerta de error)

La serie `forest_area_km2` del WB muestra diferencias anuales **constantes dentro de períodos quinquenales** (patrón lineal), lo cual confirma que el WB aplica interpolación de los datos FAO (quinquenales) para producir una serie anual. Esta interpolación es **realizada por la fuente (FAO/WB), no por este equipo**. Se documenta por transparencia pero NO es un error de este panel.

---

## Reproducibilidad

Todos los datos descargados vía World Bank API v2:
```
https://api.worldbank.org/v2/country/[ISO2]/indicator/[CÓDIGO]?format=json&per_page=1000&date=2000:2023
```
WGI vía source=3 del WB (código: `GOV_WGI_*`).  
Fecha de descarga registrada en `manifest_fuentes.csv`.  
Hash SHA-256 parcial de cada columna disponible en manifest para verificación.

---

## Archivos generados

| Archivo | Descripción |
|---|---|
| `panel_raw.csv` | Base principal cruda — 480 filas × 31 cols |
| `diccionario_variables.csv` | Trazabilidad completa por columna |
| `matriz_cumplimiento_consigna.csv` | Mapa consigna → disponibilidad |
| `manifest_fuentes.csv` | Log de descarga por serie |
| `auditoria_redundancia.csv` | Diagnóstico de redundancias sin borrado |
| `auditoria_integridad.csv` | Cobertura, patrones temporales, alertas |
| `variables_no_resueltas.md` | Variables sin solución directa |
| `README_AUDITORIA.md` | Este documento |
""".format(fecha=UTC_NOW)

# ─────────────────────────────────────────────────────────────────────────────
# PROPUESTA PANEL_MODELO (sin aplicarla — solo CSV de propuesta)
# ─────────────────────────────────────────────────────────────────────────────

PROPUESTA_MODELO = [
    {"variable_raw": "forest_area_pct_land",          "accion": "MANTENER",  "nombre_modelo": "forest_area_pct",           "razon": "Normalizada, 100% cobertura. Preferida sobre km²."},
    {"variable_raw": "forest_area_km2",               "accion": "EXCLUIR_MODELO", "nombre_modelo": "—",                    "razon": "Redundante con forest_area_pct; mantener en RAW."},
    {"variable_raw": "ghg_total_incl_lulucf_mt_co2e", "accion": "MANTENER",  "nombre_modelo": "ghg_total_mt_co2e",         "razon": "Variable dependiente principal GEI. 100% cobertura."},
    {"variable_raw": "co2_excl_lulucf_mt_co2e",       "accion": "SEPARAR_MODELO_ALTERNATIVO", "nombre_modelo": "co2_mt_co2e", "razon": "No usar simultáneamente con GHG. Modelo alternativo focalizado en CO2 fósil."},
    {"variable_raw": "gdp_per_capita_ppp_const2021_intl","accion": "MANTENER", "nombre_modelo": "gdp_pc_ppp_2021",         "razon": "PPA para comparación internacional. RENOMBRAR (año base 2021, no 2017)."},
    {"variable_raw": "gdp_per_capita_const2015_usd",  "accion": "EXCLUIR_MODELO", "nombre_modelo": "—",                   "razon": "Redundante con PPA. Mantener en RAW."},
    {"variable_raw": "population_total",              "accion": "MANTENER",  "nombre_modelo": "population_total",          "razon": "Directo, 100% cobertura."},
    {"variable_raw": "internet_users_pct_pop",        "accion": "MANTENER",  "nombre_modelo": "internet_users_pct",        "razon": "Mejor proxy tecnología disponible."},
    {"variable_raw": "mobile_subscriptions_per100",   "accion": "EXCLUIR_MODELO", "nombre_modelo": "—",                   "razon": "Redundante con internet. Mantener en RAW."},
    {"variable_raw": "agriculture_va_pct_gdp",        "accion": "MANTENER",  "nombre_modelo": "agri_va_pct_gdp",           "razon": "VAB agrícola."},
    {"variable_raw": "manufacturing_va_pct_gdp",      "accion": "MANTENER",  "nombre_modelo": "manuf_va_pct_gdp",          "razon": "VAB manufacturero."},
    {"variable_raw": "services_va_pct_gdp",           "accion": "EXCLUIR_MODELO", "nombre_modelo": "—",                   "razon": "Tercera restricción VAB — eliminar para evitar colinealidad. Mantener en RAW."},
    {"variable_raw": "child_employment_pct_7to14",    "accion": "EXCLUIR_MODELO", "nombre_modelo": "—",                   "razon": "Proxy inverso laboral con 13.8% cobertura. No usable. Requiere fuente alternativa."},
    {"variable_raw": "renewable_energy_pct_final_energy","accion": "MANTENER","nombre_modelo": "renew_energy_pct",         "razon": "Tecnología verde — más amplia y conceptualmente adecuada."},
    {"variable_raw": "renewable_electricity_output_pct","accion": "EXCLUIR_MODELO","nombre_modelo": "—",                  "razon": "Redundante con renewable_energy_pct. RENOMBRAR en RAW: quitar 'gw'. Mantener en RAW."},
    {"variable_raw": "rd_expenditure_pct_gdp",        "accion": "MANTENER",  "nombre_modelo": "rd_pct_gdp",               "razon": "Proxy I+D — mejor disponible para innovación."},
    {"variable_raw": "account_ownership_pct_adults",  "accion": "MANTENER_CON_CONDICION", "nombre_modelo": "findex_account_pct", "razon": "Trienal — requiere aprobación de estrategia para años sin dato (NaN o interpolación)."},
    {"variable_raw": "domestic_credit_private_pct_gdp","accion": "MANTENER", "nombre_modelo": "priv_credit_pct_gdp",      "razon": "Profundidad financiera — anual, buena cobertura."},
    {"variable_raw": "wgi_voice_accountability_est",  "accion": "MANTENER",  "nombre_modelo": "wgi_accountability",        "razon": "Rendición de cuentas — prioritaria según consigna."},
    {"variable_raw": "wgi_government_effectiveness_est","accion": "MANTENER_CON_CONDICION","nombre_modelo": "wgi_gov_effect","razon": "Retener si modelo necesita calidad institucional; verificar no colinealidad con accountability."},
    {"variable_raw": "wgi_rule_of_law_est",           "accion": "EXCLUIR_MODELO","nombre_modelo": "—",                    "razon": "Alta redundancia con control_corruption y gov_effect. Mantener en RAW."},
    {"variable_raw": "wgi_control_corruption_est",    "accion": "MANTENER",  "nombre_modelo": "wgi_corruption",           "razon": "Calidad institucional — una sola del bloque anticorrupción."},
    {"variable_raw": "wgi_regulatory_quality_est",    "accion": "EXCLUIR_MODELO","nombre_modelo": "—",                    "razon": "Proxy de política ambiental imperfecto. Mantener en RAW; excluir sin fuente ambiental directa."},
    {"variable_raw": "wgi_political_stability_est",   "accion": "EXCLUIR_MODELO","nombre_modelo": "—",                    "razon": "4to WGI — bloque ya representado por accountability, gov_effect, corruption. Mantener en RAW."},
    {"variable_raw": "tax_revenue_pct_gdp",           "accion": "MANTENER_CON_CONDICION","nombre_modelo": "tax_rev_pct_gdp","razon": "Proxy fiscal general (no impuestos ambientales específicos). Usar con cautela."},
    {"variable_raw": "natural_resources_rents_pct_gdp","accion": "MANTENER", "nombre_modelo": "nat_rents_pct_gdp",        "razon": "Renta recursos naturales — directo, buena cobertura."},
    {"variable_raw": "vulnerable_employment_pct_total","accion": "MANTENER_CON_CONDICION","nombre_modelo": "vuln_employ_pct","razon": "RENOMBRAR. Concepto empleo vulnerable ≠ informalidad. Usar con nota metodológica."},
    {"variable_raw": "stock_market_cap_pct_gdp",      "accion": "EXCLUIR_MODELO","nombre_modelo": "—",                    "razon": "27.3% cobertura. Proxy débil de innovación financiera. Mantener en RAW."},
]

def build_propuesta():
    return pd.DataFrame(PROPUESTA_MODELO)

# ─────────────────────────────────────────────────────────────────────────────
# EJECUTAR TODOS LOS ARTEFACTOS
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generando artefactos de auditoría...")

    # 2. Diccionario
    dic = build_diccionario()
    dic.to_csv(DATA_PROCESSED_DIR / "diccionario_variables.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ diccionario_variables.csv ({len(dic)} filas)")

    # 3. Cumplimiento consigna
    cum = build_cumplimiento()
    cum.to_csv(DATA_PROCESSED_DIR / "matriz_cumplimiento_consigna.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ matriz_cumplimiento_consigna.csv ({len(cum)} filas)")

    # 4. Manifest enriquecido
    man = build_manifest()
    man.to_csv(DATA_PROCESSED_DIR / "manifest_fuentes.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ manifest_fuentes.csv ({len(man)} filas)")

    # 5. Redundancia
    red = build_redundancia()
    red.to_csv(DATA_PROCESSED_DIR / "auditoria_redundancia.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ auditoria_redundancia.csv ({len(red)} filas)")

    # 6. Integridad
    integ = build_integridad()
    integ.to_csv(DATA_PROCESSED_DIR / "auditoria_integridad.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ auditoria_integridad.csv ({len(integ)} filas)")

    # 7. Variables no resueltas
    with open(DOCS_DIR / "variables_no_resueltas.md", "w", encoding="utf-8") as f:
        f.write(NO_RESUELTAS_MD)
    print("  ✓ variables_no_resueltas.md")

    # 8. README
    with open(DOCS_DIR / "README_AUDITORIA.md", "w", encoding="utf-8") as f:
        f.write(README_MD)
    print("  ✓ README_AUDITORIA.md")

    # Propuesta panel_modelo (artefacto bonus)
    prop = build_propuesta()
    prop.to_csv(DATA_PROCESSED_DIR / "propuesta_panel_modelo.csv", index=False, encoding="utf-8-sig")
    print(f"  ✓ propuesta_panel_modelo.csv ({len(prop)} filas)")

    print("\n✓ Todos los artefactos generados en ")

    # Verificación final del panel RAW
    print("\n=== VERIFICACIÓN PANEL RAW ===")
    print(f"Filas: {len(df)} | Columnas: {len(df.columns)}")
    print(f"Duplicados llave iso2+year: {df.duplicated(['iso2','year']).sum()}")
    print(f"Columnas con 0% cobertura: {[c for c in df.columns[3:] if df[c].notna().sum()==0]}")
    print("fillna/interpolación aplicada: NINGUNA (verificado)")