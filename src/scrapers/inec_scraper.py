"""
INEC Scraper / Backend for Applied Econometrics 2026.
Specialized logic for INEC (Instituto Nacional de Estadística y Censos).
"""

from typing import Any, Mapping
import pandas as pd
import logging
from ..core.source_backends import SourceBackendRegistry

logger = logging.getLogger(__name__)

@SourceBackendRegistry.register("inec", "ecuador_inec")
def fetch_inec(
    variable: Mapping[str, Any],
    countries_str: str,
    start_year: int,
    end_year: int,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Simulated implementation for INEC scraping.
    """
    name = variable.get("nombre_raw", "UNKNOWN")
    logger.info(f"📥 [INEC] Iniciando extracción para: {name}")
    
    data = {
        "iso2": ["EC"],
        "year": [start_year],
        "value": [0.0]
    }
    
    df = pd.DataFrame(data)
    meta = {
        "source": "INEC Ecuador",
        "method": "Auto-Scraping (Placeholder Architecture)",
        "variable": name
    }
    
    return df, meta
