import pandas as pd
import requests
from pathlib import Path
from loguru import logger

# Configuration
BASE_PATH = Path(
    "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess"
)
RAW_DATA_PATH = BASE_PATH / "data" / "raw"

RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)


def fetch_world_bank():
    logger.info("Fetching Vanguard indicators from World Bank API...")
    # BX.TRF.PWKR.DT.GD.ZS: Remesas (% PIB)
    # SE.TER.ENRR: Matrícula Educación Superior (%)
    # FR.INR.LNDP: Spread de tasas de interés (%)
    # NY.GDP.PCAP.PP.KD: PIB per cápita (PPP)
    indicators = {
        "BX.TRF.PWKR.DT.GD.ZS": "remesas_pib",
        "SE.TER.ENRR": "matricula_superior",
        "FR.INR.LNDP": "spread_bancario",
        "NY.GDP.PCAP.PP.KD": "gdp_pc_ppp",
    }

    results = []
    for code, name in indicators.items():
        # Fetching for Ecuador (ECU)
        url = f"https://api.worldbank.org/v2/country/ECU/indicator/{code}?format=json&date=2000:2023&per_page=100"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1:
                    records = data[1]
                    temp_df = pd.DataFrame(records)
                    temp_df = temp_df[["date", "value"]]
                    temp_df.columns = ["year", name]
                    temp_df["year"] = temp_df["year"].astype(int)
                    # Interpolate internal NaNs if any (WB data sometimes has gaps)
                    temp_df = temp_df.sort_values("year")
                    temp_df[name] = temp_df[name].interpolate(
                        method="linear", limit_direction="both"
                    )
                    results.append(temp_df.set_index("year"))
                else:
                    logger.warning(f"No data found for indicator {code}")
        except Exception as e:
            logger.error(f"Error fetching {code}: {e}")

    if results:
        df_wb = pd.concat(results, axis=1).reset_index()
        return df_wb
    return pd.DataFrame()


def main():
    wb_df = fetch_world_bank()

    if not wb_df.empty:
        # Output files
        output_file = RAW_DATA_PATH / "vanguard_strategy_vars.parquet"
        wb_df.to_parquet(output_file)
        logger.success(f"Vanguard Strategic Base saved to {output_file}")

        csv_file = RAW_DATA_PATH / "vanguard_strategy_vars.csv"
        wb_df.to_csv(csv_file, index=False)
        logger.success(f"Vanguard Strategic Base saved to {csv_file}")

        # Display summary
        print("\n--- Vanguard Strategic Base Summary (2000-2023) ---")
        print(wb_df.describe().T)
    else:
        logger.error("Failed to generate vanguard strategic base.")


if __name__ == "__main__":
    main()
