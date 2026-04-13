import pandas as pd
import numpy as np
import time
import logging
from typing import List, Dict, Tuple
from core.utils import fetch_wb

logger = logging.getLogger(__name__)

class WorldBankLoader:
    def __init__(self, countries: List[str], start_year: int, end_year: int):
        self.countries = countries
        self.countries_str = ";".join(countries)
        self.start_year = start_year
        self.end_year = end_year

    def fetch_variable(self, series_meta: Dict) -> Tuple[pd.DataFrame, Dict]:
        """Descarga un indicador específico usando su metadata."""
        code = series_meta["codigo_api"]
        name = series_meta["nombre_raw"]
        
        df, meta = fetch_wb(code, self.countries_str, self.start_year, self.end_year)
        
        # Enriquecer meta con info local del catálogo
        meta["variable_local"] = name
        meta["institucion"] = series_meta.get("institucion", "WB")
        
        # Filtrar solo países solicitados (por seguridad)
        if not df.empty:
            df = df[df["iso2"].isin(self.countries)].drop_duplicates(["iso2", "year"])
            
        return df, meta
