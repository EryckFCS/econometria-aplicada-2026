import pandas as pd
from pathlib import Path
from loguru import logger

# Configuration
BASE_PATH = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/evidence/U1-Applied-Econometrics/APE2-Crisis-IESS")
RAW_VANGUARD = BASE_PATH / "data" / "raw" / "vanguard_strategy_vars.parquet"

embi_data = {
    2000: 6100, 2001: 1200, 2002: 1600, 2003: 1000, 2004: 800,
    2005: 700, 2006: 600, 2007: 500, 2008: 1200, 2009: 1500,
    2010: 800, 2011: 700, 2012: 600, 2013: 600, 2014: 700,
    2015: 1000, 2016: 1100, 2017: 600, 2018: 700, 2019: 800,
    2020: 2250, 2021: 900, 2022: 1200, 2023: 1800
}

def main():
    logger.info("Updating Vanguard Strategy Base with EMBI data...")
    if not RAW_VANGUARD.exists():
        logger.error(f"File not found: {RAW_VANGUARD}")
        return

    df = pd.read_parquet(RAW_VANGUARD)
    
    # Map EMBI data
    df['embi_ecuador'] = df['year'].map(embi_data)
    
    # Save back
    df.to_parquet(RAW_VANGUARD)
    df.to_csv(RAW_VANGUARD.with_suffix('.csv'), index=False)
    
    logger.success("EMBI data integrated into vanguard strategy base.")
    print(df[['year', 'embi_ecuador']].tail())

if __name__ == "__main__":
    main()
