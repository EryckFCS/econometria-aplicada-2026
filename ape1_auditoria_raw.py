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
from ape1_utils import fetch_wb as utils_fetch_wb

# Rutas relativas al script
BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_PANEL = BASE_DIR / "panel_raw.csv"
OUTPUT_MANIFEST = BASE_DIR / "manifest_fuentes_raw.csv"
OUTPUT_SERIES_PICKLE = BASE_DIR / "series_catalog.pkl"

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

ISO3_TO_ISO2 = {
    "ARG":"AR","BOL":"BO","BRA":"BR","CHL":"CL","COL":"CO","CRI":"CR",
    "CUB":"CU","ECU":"EC","SLV":"SV","GTM":"GT","HTI":"HT","HND":"HN",
    "MEX":"MX","NIC":"NI","PAN":"PA","PRY":"PY","PER":"PE","DOM":"DO",
    "URY":"UY","VEN":"VE",
}

# ─── CATÁLOGO OFICIAL DE SERIES ───────────────────────────────────────────────
# Solo series directas de fuentes API públicas.
# nombre_raw = nombre que refleja EXACTAMENTE la unidad devuelta por la API.
# Si el nombre anterior era engañoso, se marca y se propone rename en AUDITORIA.

SERIES_RAW = [
    # ── DEPENDIENTES ─────────────────────────────────────────────────────────
    {
        "nombre_raw":     "forest_area_km2",
        "nombre_v1":      "superficie_forestal_km2",
        "codigo_api":     "AG.LND.FRST.K2",
        "nombre_api":     "Forest area (sq. km)",
        "unidad_api":     "km²",
        "fuente":         "World Bank WDI / FAO Global Forest Resources Assessment",
        "institucion":    "World Bank / FAO",
        "url_indicador":  "https://data.worldbank.org/indicator/AG.LND.FRST.K2",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/AG.LND.FRST.K2",
        "rol":            "dependiente",
        "concepto":       "Superficie forestal total",
        "consigna":       "Superficie forestal",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "FAO quinquenal interpolado por WB a anual. Patrón de interpolación lineal visible en serie. Ver auditoria_integridad.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "forest_area_pct_land",
        "nombre_v1":      "superficie_forestal_pct",
        "codigo_api":     "AG.LND.FRST.ZS",
        "nombre_api":     "Forest area (% of land area)",
        "unidad_api":     "% del área territorial total",
        "fuente":         "World Bank WDI / FAO",
        "institucion":    "World Bank / FAO",
        "url_indicador":  "https://data.worldbank.org/indicator/AG.LND.FRST.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/AG.LND.FRST.ZS",
        "rol":            "dependiente",
        "concepto":       "Superficie forestal como porcentaje del territorio",
        "consigna":       "Superficie forestal",
        "disponibilidad": "disponible_directa",
        "alerta":         "Misma fuente FAO que forest_area_km2. Redundante conceptualmente; difieren en unidad. REDUNDANCIA con forest_area_km2.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "ghg_total_incl_lulucf_mt_co2e",
        "nombre_v1":      "gei_total_incl_lulucf_mt",
        "codigo_api":     "EN.GHG.ALL.LU.MT.CE.AR5",
        "nombre_api":     "Total greenhouse gas emissions including LULUCF (Mt CO2e)",
        "unidad_api":     "Mt CO2 equivalente (GWP AR5)",
        "fuente":         "World Bank WDI / EDGAR Community GHG Database JRC-IEA 2025",
        "institucion":    "World Bank / JRC European Commission / IEA",
        "url_indicador":  "https://data.worldbank.org/indicator/EN.GHG.ALL.LU.MT.CE.AR5",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/EN.GHG.ALL.LU.MT.CE.AR5",
        "rol":            "dependiente / prioritaria",
        "concepto":       "Gases de efecto invernadero totales incl. cambio de uso de suelo",
        "consigna":       "Gases de efecto invernadero",
        "disponibilidad": "disponible_directa",
        "alerta":         "Incluye LULUCF: valores negativos son técnicamente válidos (sumidero forestal). Panamá y Venezuela presentan valores negativos persistentes — fenómeno esperado, no error. Fuente subyacente: EDGAR_2025_GHG.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "co2_excl_lulucf_mt_co2e",
        "nombre_v1":      "co2_excl_lulucf_mt",
        "codigo_api":     "EN.GHG.CO2.MT.CE.AR5",
        "nombre_api":     "Carbon dioxide (CO2) emissions (total) excluding LULUCF (Mt CO2e)",
        "unidad_api":     "Mt CO2 equivalente (GWP AR5)",
        "fuente":         "World Bank WDI / EDGAR JRC-IEA",
        "institucion":    "World Bank / JRC / IEA",
        "url_indicador":  "https://data.worldbank.org/indicator/EN.GHG.CO2.MT.CE.AR5",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/EN.GHG.CO2.MT.CE.AR5",
        "rol":            "dependiente",
        "concepto":       "Emisiones de CO2 (sin LULUCF)",
        "consigna":       "Emisiones de CO2",
        "disponibilidad": "disponible_directa",
        "alerta":         "Nota: la unidad es Mt CO2e (equivalente), no kt puro. Misma familia EDGAR que ghg_total. REDUNDANCIA PARCIAL con ghg_total: CO2 es un subconjunto del total GEI.",
        "inconsistencia_nombre": False,
    },
    # ── INDEPENDIENTES ────────────────────────────────────────────────────────
    {
        "nombre_raw":     "gdp_per_capita_const2015_usd",
        "nombre_v1":      "pib_per_capita_usd",
        "codigo_api":     "NY.GDP.PCAP.KD",
        "nombre_api":     "GDP per capita (constant 2015 US$)",
        "unidad_api":     "USD constantes 2015",
        "fuente":         "World Bank WDI",
        "institucion":    "World Bank",
        "url_indicador":  "https://data.worldbank.org/indicator/NY.GDP.PCAP.KD",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/NY.GDP.PCAP.KD",
        "rol":            "independiente",
        "concepto":       "Crecimiento económico — PIB per cápita",
        "consigna":       "Crecimiento económico (PIB per capita)",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Año base 2015 (confirmado API). Cuba: datos ausentes o muy limitados.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "gdp_per_capita_ppp_const2021_intl",
        "nombre_v1":      "pib_per_capita_ppa",
        "codigo_api":     "NY.GDP.PCAP.PP.KD",
        "nombre_api":     "GDP per capita, PPP (constant 2021 international $)",
        "unidad_api":     "USD internacionales constantes 2021 (PPA)",
        "fuente":         "World Bank WDI / ICP",
        "institucion":    "World Bank / International Comparison Program",
        "url_indicador":  "https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/NY.GDP.PCAP.PP.KD",
        "rol":            "independiente — alternativa PPA",
        "concepto":       "Crecimiento económico — PIB per cápita PPA",
        "consigna":       "Crecimiento económico (PIB per capita)",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta": (
            "⚠ INCONSISTENCIA DETECTADA: la columna anterior se llamaba 'pib_per_capita_ppa' con nota '2017' "
            "pero la API devuelve base 2021 (confirmado). Nombre propuesto: gdp_per_capita_ppp_const2021_intl. "
            "REDUNDANCIA con gdp_per_capita_const2015_usd: ambas miden PIB per cápita. "
            "Para modelo parsimoniosos: elegir una. PPA preferida para comparaciones internacionales."
        ),
        "inconsistencia_nombre": True,
        "nombre_correcto_sugerido": "gdp_per_capita_ppp_const2021_intl",
        "detalle_inconsistencia": "Columna previa rotulada con año base 2017; la API devuelve base 2021 (ICP 2021).",
    },
    {
        "nombre_raw":     "population_total",
        "nombre_v1":      "poblacion_total",
        "codigo_api":     "SP.POP.TOTL",
        "nombre_api":     "Population, total",
        "unidad_api":     "número de personas",
        "fuente":         "World Bank WDI / UN Population Division",
        "institucion":    "World Bank / UNPD",
        "url_indicador":  "https://data.worldbank.org/indicator/SP.POP.TOTL",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/SP.POP.TOTL",
        "rol":            "independiente",
        "concepto":       "Población",
        "consigna":       "Población",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Cuba: datos limitados post-2019.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "internet_users_pct_pop",
        "nombre_v1":      "acceso_internet_pct",
        "codigo_api":     "IT.NET.USER.ZS",
        "nombre_api":     "Individuals using the Internet (% of population)",
        "unidad_api":     "% de la población",
        "fuente":         "World Bank WDI / ITU",
        "institucion":    "World Bank / International Telecommunication Union",
        "url_indicador":  "https://data.worldbank.org/indicator/IT.NET.USER.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/IT.NET.USER.ZS",
        "rol":            "independiente — proxy tecnología",
        "concepto":       "Tecnología — adopción digital",
        "consigna":       "Tecnología",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Proxy de adopción tecnológica; no mide innovación ni tecnología verde.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "mobile_subscriptions_per100",
        "nombre_v1":      "suscripciones_movil",
        "codigo_api":     "IT.CEL.SETS.P2",
        "nombre_api":     "Mobile cellular subscriptions (per 100 people)",
        "unidad_api":     "suscripciones por 100 habitantes",
        "fuente":         "World Bank WDI / ITU",
        "institucion":    "World Bank / ITU",
        "url_indicador":  "https://data.worldbank.org/indicator/IT.CEL.SETS.P2",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/IT.CEL.SETS.P2",
        "rol":            "independiente — proxy tecnología secundario",
        "concepto":       "Tecnología — penetración móvil",
        "consigna":       "Tecnología",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "REDUNDANCIA con internet_users_pct_pop: ambas son proxies de adopción tecnológica general. Puede superar 100 (múltiples SIMs). Alta correlación esperada.",
        "inconsistencia_nombre": False,
    },
    # ── CONTROL: VAB SECTORIAL ────────────────────────────────────────────────
    {
        "nombre_raw":     "agriculture_va_pct_gdp",
        "nombre_v1":      "vab_agricola_pct_pib",
        "codigo_api":     "NV.AGR.TOTL.ZS",
        "nombre_api":     "Agriculture, forestry, and fishing, value added (% of GDP)",
        "unidad_api":     "% del PIB",
        "fuente":         "World Bank WDI",
        "institucion":    "World Bank",
        "url_indicador":  "https://data.worldbank.org/indicator/NV.AGR.TOTL.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/NV.AGR.TOTL.ZS",
        "rol":            "control — VAB sectorial",
        "concepto":       "Valor Agregado Bruto sector agrícola",
        "consigna":       "VAB sectorial (agrícola)",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Incluye silvicultura y pesca — más amplio que 'agrícola' puro.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "manufacturing_va_pct_gdp",
        "nombre_v1":      "vab_manufactura_pct_pib",
        "codigo_api":     "NV.IND.MANF.ZS",
        "nombre_api":     "Manufacturing, value added (% of GDP)",
        "unidad_api":     "% del PIB",
        "fuente":         "World Bank WDI",
        "institucion":    "World Bank",
        "url_indicador":  "https://data.worldbank.org/indicator/NV.IND.MANF.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/NV.IND.MANF.ZS",
        "rol":            "control — VAB sectorial",
        "concepto":       "Valor Agregado Bruto sector manufacturero",
        "consigna":       "VAB sectorial (manufacturero)",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "No incluye construcción ni minería. Subconjunto del sector industrial.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "services_va_pct_gdp",
        "nombre_v1":      "vab_servicios_pct_pib",
        "codigo_api":     "NV.SRV.TOTL.ZS",
        "nombre_api":     "Services, value added (% of GDP)",
        "unidad_api":     "% del PIB",
        "fuente":         "World Bank WDI",
        "institucion":    "World Bank",
        "url_indicador":  "https://data.worldbank.org/indicator/NV.SRV.TOTL.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/NV.SRV.TOTL.ZS",
        "rol":            "control — VAB sectorial",
        "concepto":       "Valor Agregado Bruto sector servicios",
        "consigna":       "VAB sectorial (servicios)",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Alta multicolinealidad potencial con los otros dos VAB (restringen como fracción del PIB).",
        "inconsistencia_nombre": False,
    },
    # ── CONTROL: DERECHOS LABORALES ───────────────────────────────────────────
    {
        "nombre_raw":     "child_employment_pct_7to14",
        "nombre_v1":      "trabajo_infantil_pct",
        "codigo_api":     "SL.TLF.0714.ZS",
        "nombre_api":     "Children in employment, total (% of children ages 7-14)",
        "unidad_api":     "% de niños de 7 a 14 años",
        "fuente":         "World Bank WDI / ILO",
        "institucion":    "World Bank / ILO",
        "url_indicador":  "https://data.worldbank.org/indicator/SL.TLF.0714.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/SL.TLF.0714.ZS",
        "rol":            "proxy — control derechos laborales",
        "concepto":       "Trabajo infantil como proxy inverso de protección laboral",
        "consigna":       "Protección de los derechos laborales",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta": (
            "⚠ CONCEPTO NO EQUIVALENTE: 'Children in employment' mide trabajo infantil, "
            "NO directamente 'protección de derechos laborales'. Es un proxy inverso. "
            "Cobertura muy baja (13.8%). La consigna pide un índice de derechos laborales. "
            "Fuente directa recomendada: ITUC Global Rights Index, ILO ILOSTAT 'collective_bargaining_coverage'. "
            "Clasificación: PROXY, no disponible directa para AL 2000-2023."
        ),
        "inconsistencia_nombre": True,
        "nombre_correcto_sugerido": "child_employment_pct_7to14",
        "detalle_inconsistencia": "El concepto 'protección derechos laborales' no se satisface con esta variable. Es proxy inverso con cobertura 13.8%.",
    },
    # ── CONTROL: TECNOLOGÍA VERDE (PRIORITARIA) ───────────────────────────────
    {
        "nombre_raw":     "renewable_energy_pct_final_energy",
        "nombre_v1":      "energia_renovable_pct",
        "codigo_api":     "EG.FEC.RNEW.ZS",
        "nombre_api":     "Renewable energy consumption (% of total final energy consumption)",
        "unidad_api":     "% del consumo final total de energía",
        "fuente":         "World Bank WDI / IEA / SE4ALL",
        "institucion":    "World Bank / IEA / Sustainable Energy for All",
        "url_indicador":  "https://data.worldbank.org/indicator/EG.FEC.RNEW.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/EG.FEC.RNEW.ZS",
        "rol":            "control — tecnología verde (prioritaria)",
        "concepto":       "Tecnología verde — adopción de energía renovable",
        "consigna":       "Tecnología verde",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Mide consumo, no inversión en tecnología verde. Proxy razonable y ampliamente usado en literatura EKC.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "renewable_electricity_output_pct",
        "nombre_v1":      "capacidad_renovable_gw",
        "codigo_api":     "EG.ELC.RNEW.ZS",
        "nombre_api":     "Renewable electricity output (% of total electricity output)",
        "unidad_api":     "% de la generación eléctrica total",
        "fuente":         "World Bank WDI / IEA",
        "institucion":    "World Bank / IEA",
        "url_indicador":  "https://data.worldbank.org/indicator/EG.ELC.RNEW.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/EG.ELC.RNEW.ZS",
        "rol":            "control — innovación tecnológica verde (prioritaria)",
        "concepto":       "Participación de electricidad renovable en generación total",
        "consigna":       "Innovación tecnológica verde",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta": (
            "⚠ NOMBRE INCONSISTENTE CRÍTICO: la columna anterior se llamaba 'capacidad_renovable_gw' "
            "pero la API devuelve PORCENTAJE (%), no gigavatios (GW). "
            "Nombre correcto: renewable_electricity_output_pct. "
            "Dato RAW conservado sin modificación. "
            "REDUNDANCIA con renewable_energy_pct_final_energy: ambas miden presencia de energía renovable, "
            "difieren en denominador (electricidad vs energía total). Alta correlación esperada."
        ),
        "inconsistencia_nombre": True,
        "nombre_correcto_sugerido": "renewable_electricity_output_pct",
        "detalle_inconsistencia": "La columna 'capacidad_renovable_gw' implica unidad GW (gigavatios). La API entrega % de output eléctrico. Error de rotulación grave.",
    },
    {
        "nombre_raw":     "rd_expenditure_pct_gdp",
        "nombre_v1":      "gasto_id_pct_pib",
        "codigo_api":     "GB.XPD.RSDV.GD.ZS",
        "nombre_api":     "Research and development expenditure (% of GDP)",
        "unidad_api":     "% del PIB",
        "fuente":         "World Bank WDI / UNESCO Institute for Statistics",
        "institucion":    "World Bank / UNESCO",
        "url_indicador":  "https://data.worldbank.org/indicator/GB.XPD.RSDV.GD.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/GB.XPD.RSDV.GD.ZS",
        "rol":            "control — innovación tecnológica verde (proxy)",
        "concepto":       "Gasto en I+D como proxy de capacidad de innovación tecnológica",
        "consigna":       "Innovación tecnológica verde",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "I+D total, no discrimina innovación verde. Cobertura 43.5%. Proxy imperfecto para 'innovación tecnológica verde'.",
        "inconsistencia_nombre": False,
    },
    # ── CONTROL: INCLUSIÓN FINANCIERA (PRIORITARIA) ───────────────────────────
    {
        "nombre_raw":     "account_ownership_pct_adults",
        "nombre_v1":      "cuenta_financiera_pct",
        "codigo_api":     "FX.OWN.TOTL.ZS",
        "nombre_api":     "Account ownership at a financial institution or with a mobile-money-service provider (% of population ages 15+)",
        "unidad_api":     "% de adultos (+15 años)",
        "fuente":         "World Bank Global Findex Database",
        "institucion":    "World Bank",
        "url_indicador":  "https://data.worldbank.org/indicator/FX.OWN.TOTL.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/FX.OWN.TOTL.ZS",
        "rol":            "control — inclusión financiera (prioritaria)",
        "concepto":       "Inclusión financiera — tenencia de cuenta",
        "consigna":       "Inclusión financiera",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta": (
            "⚠ FRECUENCIA TRIENAL: encuesta disponible solo en 2011, 2014, 2017, 2021, 2024. "
            "Cobertura 15.4% en panel anual. Los valores NO están interpolados en este RAW. "
            "Los años sin encuesta quedan como NaN. "
            "Patrón de años con datos: AR(2011,2014,2017,2021), MX(2011,2014,2017,2022)."
        ),
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "domestic_credit_private_pct_gdp",
        "nombre_v1":      "credito_privado_pct_pib",
        "codigo_api":     "FS.AST.PRVT.GD.ZS",
        "nombre_api":     "Domestic credit to private sector (% of GDP)",
        "unidad_api":     "% del PIB",
        "fuente":         "World Bank WDI / FMI IFS",
        "institucion":    "World Bank / FMI",
        "url_indicador":  "https://data.worldbank.org/indicator/FS.AST.PRVT.GD.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/FS.AST.PRVT.GD.ZS",
        "rol":            "control — inclusión financiera (profundidad)",
        "concepto":       "Profundidad del sistema financiero",
        "consigna":       "Inclusión financiera",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Mide profundidad financiera, no acceso individual. Complementa account_ownership. Serie anual continua.",
        "inconsistencia_nombre": False,
    },
    # ── CONTROL: GOBERNANZA / RENDICIÓN DE CUENTAS (WGI) (PRIORITARIA) ────────
    {
        "nombre_raw":     "wgi_voice_accountability_est",
        "nombre_v1":      "rendicion_cuentas_est",
        "codigo_api":     "GOV_WGI_VA.EST",
        "nombre_api":     "Voice and Accountability - Governance estimate (approx. -2.5 to +2.5)",
        "unidad_api":     "estimado de gobernanza (-2.5 a +2.5)",
        "fuente":         "World Bank Worldwide Governance Indicators (WGI)",
        "institucion":    "World Bank",
        "url_indicador":  "https://www.worldbank.org/en/publication/worldwide-governance-indicators",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/GOV_WGI_VA.EST",
        "rol":            "control — rendición de cuentas (prioritaria)",
        "concepto":       "Rendición de cuentas — dimensión WGI",
        "consigna":       "Rendición de cuentas",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Gap: año 2001 sin datos (WGI no publicó ese año). Cobertura 95.8%. Datos disponibles 1996-2024.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "wgi_government_effectiveness_est",
        "nombre_v1":      "gobernanza_efectividad",
        "codigo_api":     "GOV_WGI_GE.EST",
        "nombre_api":     "Government Effectiveness - Governance estimate (approx. -2.5 to +2.5)",
        "unidad_api":     "estimado de gobernanza (-2.5 a +2.5)",
        "fuente":         "World Bank WGI",
        "institucion":    "World Bank",
        "url_indicador":  "https://www.worldbank.org/en/publication/worldwide-governance-indicators",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/GOV_WGI_GE.EST",
        "rol":            "control — gobernanza / calidad institucional",
        "concepto":       "Efectividad gubernamental",
        "consigna":       "Gobernanza",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Gap año 2001. REDUNDANCIA INSTITUCIONAL con otros 5 WGI: todos vienen de la misma encuesta.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "wgi_rule_of_law_est",
        "nombre_v1":      "gobernanza_estado_derecho",
        "codigo_api":     "GOV_WGI_RL.EST",
        "nombre_api":     "Rule of Law - Governance estimate (approx. -2.5 to +2.5)",
        "unidad_api":     "estimado de gobernanza (-2.5 a +2.5)",
        "fuente":         "World Bank WGI",
        "institucion":    "World Bank",
        "url_indicador":  "https://www.worldbank.org/en/publication/worldwide-governance-indicators",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/GOV_WGI_RL.EST",
        "rol":            "control — calidad institucional",
        "concepto":       "Estado de derecho",
        "consigna":       "Calidad institucional",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Gap año 2001. BLOQUE WGI: 6 dimensiones del mismo índice — alta multicolinealidad intragrupo.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "wgi_control_corruption_est",
        "nombre_v1":      "control_corrupcion",
        "codigo_api":     "GOV_WGI_CC.EST",
        "nombre_api":     "Control of Corruption - Governance estimate (approx. -2.5 to +2.5)",
        "unidad_api":     "estimado de gobernanza (-2.5 a +2.5)",
        "fuente":         "World Bank WGI",
        "institucion":    "World Bank",
        "url_indicador":  "https://www.worldbank.org/en/publication/worldwide-governance-indicators",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/GOV_WGI_CC.EST",
        "rol":            "control — calidad institucional / gobernanza",
        "concepto":       "Control de corrupción",
        "consigna":       "Gobernanza",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Gap año 2001. BLOQUE WGI.",
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "wgi_regulatory_quality_est",
        "nombre_v1":      "calidad_regulatoria",
        "codigo_api":     "GOV_WGI_RQ.EST",
        "nombre_api":     "Regulatory Quality - Governance estimate (approx. -2.5 to +2.5)",
        "unidad_api":     "estimado de gobernanza (-2.5 a +2.5)",
        "fuente":         "World Bank WGI",
        "institucion":    "World Bank",
        "url_indicador":  "https://www.worldbank.org/en/publication/worldwide-governance-indicators",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/GOV_WGI_RQ.EST",
        "rol":            "control — política ambiental (proxy regulatorio)",
        "concepto":       "Calidad regulatoria general",
        "consigna":       "Rigurosidad de la política ambiental",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta": (
            "⚠ CONCEPTO APROXIMADO: 'Regulatory Quality' mide marco regulatorio GENERAL, "
            "no la rigurosidad específica de política ambiental. "
            "La consigna pide un índice de política ambiental. "
            "Fuente directa: OECD Environmental Policy Stringency Index (EPS) — no disponible para todos los 20 países vía API pública."
        ),
        "inconsistencia_nombre": False,
    },
    {
        "nombre_raw":     "wgi_political_stability_est",
        "nombre_v1":      "estabilidad_politica",
        "codigo_api":     "GOV_WGI_PV.EST",
        "nombre_api":     "Political Stability and Absence of Violence - Governance estimate (approx. -2.5 to +2.5)",
        "unidad_api":     "estimado de gobernanza (-2.5 a +2.5)",
        "fuente":         "World Bank WGI",
        "institucion":    "World Bank",
        "url_indicador":  "https://www.worldbank.org/en/publication/worldwide-governance-indicators",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/GOV_WGI_PV.EST",
        "rol":            "control — gobernanza",
        "concepto":       "Estabilidad política y ausencia de violencia",
        "consigna":       "Gobernanza",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Gap año 2001. BLOQUE WGI.",
        "inconsistencia_nombre": False,
    },
    # ── CONTROL: FISCAL ───────────────────────────────────────────────────────
    {
        "nombre_raw":     "tax_revenue_pct_gdp",
        "nombre_v1":      "recaudacion_impuestos_pct_pib",
        "codigo_api":     "GC.TAX.TOTL.GD.ZS",
        "nombre_api":     "Tax revenue (% of GDP)",
        "unidad_api":     "% del PIB",
        "fuente":         "World Bank WDI / FMI",
        "institucion":    "World Bank / FMI",
        "url_indicador":  "https://data.worldbank.org/indicator/GC.TAX.TOTL.GD.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/GC.TAX.TOTL.GD.ZS",
        "rol":            "control — proxy impuestos ambientales",
        "concepto":       "Carga fiscal total",
        "consigna":       "Impuestos ambientales",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta": (
            "⚠ CONCEPTO NO EQUIVALENTE: 'Tax revenue' es recaudación fiscal TOTAL. "
            "La consigna pide impuestos ambientales específicos. "
            "Fuente directa: OECD Database on Instruments used for Environmental Policy — cobertura parcial AL. "
            "Esta columna es proxy de carga fiscal, no de impuestos ambientales."
        ),
        "inconsistencia_nombre": False,
    },
    # ── CONTROL: RECURSOS NATURALES ───────────────────────────────────────────
    {
        "nombre_raw":     "natural_resources_rents_pct_gdp",
        "nombre_v1":      "renta_recursos_naturales_pct",
        "codigo_api":     "NY.GDP.TOTL.RT.ZS",
        "nombre_api":     "Total natural resources rents (% of GDP)",
        "unidad_api":     "% del PIB",
        "fuente":         "World Bank WDI",
        "institucion":    "World Bank",
        "url_indicador":  "https://data.worldbank.org/indicator/NY.GDP.TOTL.RT.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/NY.GDP.TOTL.RT.ZS",
        "rol":            "control — renta recursos naturales",
        "concepto":       "Renta de recursos naturales (petróleo + gas + carbón + minerales + forestal)",
        "consigna":       "Renta de los recursos naturales",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "Cobertura 67.1%. Cuba y Venezuela con gaps.",
        "inconsistencia_nombre": False,
    },
    # ── CONTROL: INFORMALIDAD ─────────────────────────────────────────────────
    {
        "nombre_raw":     "vulnerable_employment_pct_total",
        "nombre_v1":      "empleo_informal_pct",
        "codigo_api":     "SL.EMP.VULN.ZS",
        "nombre_api":     "Vulnerable employment, total (% of total employment) (modeled ILO estimate)",
        "unidad_api":     "% del empleo total",
        "fuente":         "World Bank WDI / ILO",
        "institucion":    "World Bank / ILO",
        "url_indicador":  "https://data.worldbank.org/indicator/SL.EMP.VULN.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/SL.EMP.VULN.ZS",
        "rol":            "control — proxy informalidad",
        "concepto":       "Empleo vulnerable como proxy de informalidad",
        "consigna":       "Informalidad",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta": (
            "⚠ NOMBRE INCONSISTENTE: la columna previa se llamaba 'empleo_informal_pct' pero la API "
            "entrega 'Vulnerable employment' (empleo vulnerable), que incluye trabajadores por cuenta propia "
            "y trabajadores familiares no remunerados. 'Vulnerable' ≠ 'Informal' en sentido estricto: "
            "informalidad mide ausencia de protección social, no fragilidad laboral. "
            "Nombre correcto: vulnerable_employment_pct_total. "
            "Fuente directa de informalidad: ILO ILOSTAT 'emp_2emp_sex_eco_dt_a' — cobertura parcial."
        ),
        "inconsistencia_nombre": True,
        "nombre_correcto_sugerido": "vulnerable_employment_pct_total",
        "detalle_inconsistencia": "'Empleo vulnerable' (ILO) ≠ 'Empleo informal'. Son proxies correlacionados pero conceptualmente distintos.",
    },
    # ── CONTROL: INNOVACIÓN FINANCIERA ───────────────────────────────────────
    {
        "nombre_raw":     "stock_market_cap_pct_gdp",
        "nombre_v1":      "capitalizacion_mercado_pct",
        "codigo_api":     "CM.MKT.LCAP.GD.ZS",
        "nombre_api":     "Market capitalization of listed domestic companies (% of GDP)",
        "unidad_api":     "% del PIB",
        "fuente":         "World Bank WDI / WFE",
        "institucion":    "World Bank / World Federation of Exchanges",
        "url_indicador":  "https://data.worldbank.org/indicator/CM.MKT.LCAP.GD.ZS",
        "endpoint":       "https://api.worldbank.org/v2/country/PAISES/indicator/CM.MKT.LCAP.GD.ZS",
        "rol":            "control — proxy innovación financiera",
        "concepto":       "Desarrollo del mercado bursátil",
        "consigna":       "Innovación financiera",
        "disponibilidad": "disponible_directa_cobertura_parcial",
        "alerta":         "⚠ CONCEPTO APROXIMADO: capitalización bursátil ≠ innovación financiera. Cobertura 27.3%. Muchos países AL sin bolsa desarrollada.",
        "inconsistencia_nombre": False,
    },
]


# ─── FUNCIÓN DE DESCARGA RAW (CERO TRANSFORMACIONES) ─────────────────────────
def fetch_raw(series_meta, countries_str, start, end, session=None):
    """Wrapper alrededor de `ape1_utils.fetch_wb` para mantener la interfaz actual.

    Retorna (df, manifest_entry) con la misma estructura esperada por build_raw_panel().
    """
    code = series_meta["codigo_api"]
    df, meta = utils_fetch_wb(code, countries_str, start, end, session=session)
    meta["variable"] = series_meta["nombre_raw"]
    meta["proveedor"] = series_meta.get("institucion", "")
    meta["url_indicador"] = series_meta.get("url_indicador", "")
    meta["parametros_consulta"] = f"countries={countries_str}&date={start}:{end}&per_page=1000"

    # Filtrar solo países relevantes (CODIGOS) siguiendo la lógica previa
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
        df_s, manifest_entry = fetch_raw(s, PAISES_STR, ANIO_INI, ANIO_FIN)
        manifest_entry["variable"] = s["nombre_raw"]
        manifest_entry["proveedor"] = s["institucion"]
        manifest.append(manifest_entry)

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
    print("APE1 — RECONSTRUCCIÓN RAW FORENSE")
    print(f"Inicio: {UTC_NOW}")
    print("=" * 70)

    panel_raw, manifest_data = build_raw_panel()

    print(f"\nPanel RAW: {panel_raw.shape[0]} filas × {panel_raw.shape[1]} columnas")

    # Exportar a ficheros en el mismo directorio del script
    panel_raw.to_csv(str(OUTPUT_PANEL), index=False, encoding="utf-8-sig")
    pd.DataFrame(manifest_data).to_csv(str(OUTPUT_MANIFEST), index=False, encoding="utf-8-sig")

    # Guardar catálogo de series para uso en auditoría
    import pickle
    with open(OUTPUT_SERIES_PICKLE, "wb") as f:
        pickle.dump(SERIES_RAW, f)

    logger.info("→ panel_raw.csv exportado: %s", OUTPUT_PANEL)
    logger.info("→ manifest_fuentes_raw.csv exportado: %s", OUTPUT_MANIFEST)
    logger.info("→ series_catalog.pkl guardado: %s", OUTPUT_SERIES_PICKLE)