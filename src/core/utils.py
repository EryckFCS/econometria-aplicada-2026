"""Core utilities for shared download and parsing helpers."""
import logging
import time
import pandas as pd
import numpy as np
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

ISO3_TO_ISO2 = {
    "ARG": "AR", "BOL": "BO", "BRA": "BR", "CHL": "CL", "COL": "CO", "CRI": "CR", "CUB": "CU",
    "ECU": "EC", "SLV": "SV", "GTM": "GT", "HTI": "HT", "HND": "HN", "MEX": "MX", "NIC": "NI",
    "PAN": "PA", "PRY": "PY", "PER": "PE", "DOM": "DO", "URY": "UY", "VEN": "VE",
}


def create_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504)):
    """Crea una `requests.Session` con retry/backoff apropiado."""
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_wb(indicator_code, countries_str, start, end, session=None, timeout=30):
    """
    Descarga un indicador del World Bank API v2.
    Retorna (df, meta) donde df tiene columnas ['iso2','year','value'].
    """
    url_base = (
        f"https://api.worldbank.org/v2/country/{countries_str}/indicator/{indicator_code}"
        f"?format=json&per_page=1000&date={start}:{end}"
    )
    session = session or create_session()
    records = []
    errors = []
    total_downloaded = 0
    page = 1

    while True:
        try:
            r = session.get(url_base + f"&page={page}", timeout=timeout)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            logger.exception("Error descargando %s p%d", indicator_code, page)
            errors.append(str(e))
            break

        if not isinstance(data, list) or len(data) < 2 or not data[1]:
            break

        for entry in data[1]:
            total_downloaded += 1
            iso_raw = (entry.get("countryiso3code") or entry.get("country", {}).get("id", "")) or ""
            iso2 = ""
            if iso_raw:
                iso2 = ISO3_TO_ISO2.get(iso_raw.upper(), iso_raw[:2].upper())
            else:
                iso2 = entry.get("country", {}).get("id", "")
            val = entry.get("value")
            records.append({
                "iso2": iso2,
                "year": int(entry["date"]),
                "value": float(val) if val is not None else np.nan,
            })

        meta = data[0]
        if page >= meta.get("pages", 1):
            break
        page += 1
        time.sleep(0.1)

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.drop_duplicates(["iso2", "year"])

    meta_info = {
        "codigo_api": indicator_code,
        "endpoint_consultado": url_base,
        "fecha_hora_descarga_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "parametros_consulta": f"countries={countries_str}&date={start}:{end}&per_page=1000",
        "total_registros_descargados": total_downloaded,
        "total_registros_validos": int(df["value"].notna().sum()) if not df.empty else 0,
        "errores": "; ".join(errors) if errors else "",
    }

    return df, meta_info
