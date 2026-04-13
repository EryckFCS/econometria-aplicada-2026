"""
World Bank API Scraper
Robust, machine-readable alternative to scraping government websites.
Source: https://data.worldbank.org/
"""
from pathlib import Path
from datetime import datetime
import polars as pl
from loguru import logger

from ecs_quantitative.ingestion.resilient_client import ResilientClient

class WorldBankScraper:
    """
    Fetches economic indicators from the World Bank API.
    Stable, JSON-based, and globally available.
    """
    
    BASE_URL = "https://api.worldbank.org/v2"
    
    INDICATORS = {
        "inflacion": "FP.CPI.TOTL.ZG",      # Inflation, consumer prices (annual %)
        "tasa_activa": "FR.INR.LEND",       # Lending interest rate (%)
        "tasa_pasiva": "FR.INR.DPST",       # Deposit interest rate (%)
        "tasa_real": "FR.INR.RINR"          # Real interest rate (%)
    }
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.client = ResilientClient()
        
    async def fetch_indicator(self, name: str, code: str, country: str = "EC") -> pl.DataFrame:
        """
        Fetch a specific indicator history.
        Endpoint: /country/{cc}/indicator/{code}?format=json
        """
        url = f"{self.BASE_URL}/country/{country}/indicator/{code}"
        params = {"format": "json", "per_page": 100, "date": "2020:2026"}
        
        logger.info(f"🌍 World Bank: Fetching {name} ({code})...")
        
        try:
            response = await self.client.get(url, params=params)
            
            # WB API returns [metadata, [data...]]
            if not response.json() or len(response.json()) < 2:
                logger.warning(f"⚠️ No data returned for {name}")
                return pl.DataFrame()
                
            raw_data = response.json()[1]
            if not raw_data:
                return pl.DataFrame()
            
            # Parse
            clean_data = []
            for entry in raw_data:
                if entry['value'] is not None:
                    clean_data.append({
                        "fecha": f"{entry['date']}-01-01", # WB data is annual for these indicators usually
                        "indicador": name,
                        "valor": float(entry['value']),
                        "pais": entry['country']['value'],
                        "origen": "World Bank API"
                    })
            
            df = pl.DataFrame(clean_data)
            
            # Save
            filename = f"wb_{name}_{datetime.now().strftime('%Y%m%d')}.parquet"
            df.write_parquet(self.output_dir / filename)
            return df
            
        except Exception as e:
            logger.error(f"❌ WB API Error ({name}): {e}")
            return pl.DataFrame()

    async def fetch_all(self):
        """Fetch all configured indicators."""
        results = {}
        for name, code in self.INDICATORS.items():
            df = await self.fetch_indicator(name, code)
            results[name] = df
        return results
        
    async def close(self):
        await self.client.close()
