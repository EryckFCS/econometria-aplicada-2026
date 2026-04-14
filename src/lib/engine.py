import pandas as pd
import numpy as np
import logging
from itertools import product
from typing import List, Dict, Tuple
from core.utils import fetch_wb

logger = logging.getLogger(__name__)

class WECPanelEngine:
    """
    Motor unificado para la descarga de datos del World Bank y construcción de paneles balanceados.
    Diseñado bajo principios de simplicidad radical (KISS).
    """
    def __init__(self, countries: List[str], start_year: int, end_year: int, countries_dict: Dict[str, str] = None):
        self.countries = countries
        self.countries_str = ";".join(countries)
        self.start_year = start_year
        self.end_year = end_year
        self.countries_dict = countries_dict or {c: c for c in countries}

    def build_panel(self, series_catalog: List[Dict]) -> Tuple[pd.DataFrame, List[Dict]]:
        """Construye un panel balanceado con múltiples variables descargadas de la API."""
        print(f"🏗️ Construyendo panel para {len(self.countries)} países ({self.start_year}-{self.end_year})")
        
        # 1. Crear esqueleto balanceado
        years = range(self.start_year, self.end_year + 1)
        base = pd.DataFrame(
            list(product(self.countries, years)),
            columns=["iso2", "year"]
        )
        base["pais"] = base["iso2"].map(self.countries_dict)
        base = base[["iso2", "pais", "year"]]

        manifest = []
        
        # 2. Descargar e inyectar cada variable
        for s in series_catalog:
            code = s["codigo_api"]
            name = s["nombre_raw"]
            print(f"  📥 Descargando: {name} (API: {code})")
            
            df_s, meta = fetch_wb(code, self.countries_str, self.start_year, self.end_year)
            
            # Enriquecer manifiesto
            meta["variable_local"] = name
            meta["institucion"] = s.get("institucion", "WB")
            manifest.append(meta)
            
            if df_s.empty or df_s["value"].notna().sum() == 0:
                logger.warning(f"⚠️ Sin datos para {name}")
                base[name] = np.nan
            else:
                df_s = df_s.rename(columns={"value": name})
                # Asegurar tipos antes del merge
                df_s["year"] = df_s["year"].astype(int)
                base = base.merge(df_s[["iso2", "year", name]], on=["iso2", "year"], how="left")
                
        return base, manifest
