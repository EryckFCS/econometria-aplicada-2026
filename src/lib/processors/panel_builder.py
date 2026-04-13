import pandas as pd
import numpy as np
from itertools import product
from typing import List, Dict, Tuple
from lib.loaders.wb_loader import WorldBankLoader

class PanelBuilder:
    def __init__(self, loader: WorldBankLoader, countries_dict: Dict[str, str]):
        self.loader = loader
        self.countries_dict = countries_dict
        self.codigos = list(countries_dict.keys())

    def build(self, series_catalog: List[Dict]) -> Tuple[pd.DataFrame, List[Dict]]:
        """Construye un panel balanceado con múltiples variables."""
        # Crear base balanceada
        years = range(self.loader.start_year, self.loader.end_year + 1)
        base = pd.DataFrame(
            list(product(self.codigos, years)),
            columns=["iso2", "year"]
        )
        base["pais"] = base["iso2"].map(self.countries_dict)
        base = base[["iso2", "pais", "year"]]

        manifest = []
        
        for s in series_catalog:
            df_s, meta = self.loader.fetch_variable(s)
            manifest.append(meta)
            
            if df_s.empty or df_s["value"].notna().sum() == 0:
                base[s["nombre_raw"]] = np.nan
            else:
                df_s = df_s.rename(columns={"value": s["nombre_raw"]})
                base = base.merge(df_s[["iso2", "year", s["nombre_raw"]]], on=["iso2", "year"], how="left")
                
        return base, manifest
