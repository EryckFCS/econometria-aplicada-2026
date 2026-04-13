import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from lib.loaders.wb_loader import WorldBankLoader

class TimeSeriesBuilder:
    def __init__(self, loader: WorldBankLoader, country: str):
        self.loader = loader
        self.country = country

    def build(self, series_catalog: List[Dict]) -> Tuple[pd.DataFrame, List[Dict]]:
        """Construye una serie de tiempo para un solo país."""
        years = range(self.loader.start_year, self.loader.end_year + 1)
        base = pd.DataFrame(years, columns=["year"])
        base["iso2"] = self.country
        # Importamos el mapa de nombres desde el catálogo o recibimos un mapper
        from lib.catalog import PAISES_LATAM
        base["pais"] = PAISES_LATAM.get(self.country, self.country)
        
        manifest = []
        
        for s in series_catalog:
            # Crear un loader temporal solo para un país
            temp_loader = WorldBankLoader([self.country], self.loader.start_year, self.loader.end_year)
            df_s, meta = temp_loader.fetch_variable(s)
            manifest.append(meta)
            
            if df_s.empty or df_s["value"].notna().sum() == 0:
                base[s["nombre_raw"]] = np.nan
            else:
                df_s = df_s.rename(columns={"value": s["nombre_raw"]})
                base = base.merge(df_s[["year", s["nombre_raw"]]], on=["year"], how="left")
                
        return base, manifest
