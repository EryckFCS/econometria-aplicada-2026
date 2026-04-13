import yfinance as yf
import pandas as pd
from pathlib import Path
import sys

# Configuración de rutas
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "mercados"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def download_market_data():
    """
    Descarga datos de commodities y mercados usando yfinance.
    Útil para la Unidad 2 de Econometría (Modelos Dinámicos y Series de Tiempo).
    """
    symbols = {
        "CL=F": "Petroleo_WTI",
        "GC=F": "Oro",
        "HG=F": "Cobre",
        "^GSPC": "SP500",
        "DX-Y.NYB": "Indice_Dolar"
    }
    
    print(f"📈 Descargando datos de mercado en: {OUTPUT_DIR}...")
    
    all_data = []
    
    for symbol, name in symbols.items():
        try:
            print(f"  -> Obteniendo {name} ({symbol})...")
            ticker = yf.Ticker(symbol)
            # Descargamos los últimos 5 años por defecto
            df = ticker.history(period="5y")
            df = df[['Close']].rename(columns={'Close': name})
            all_data.append(df)
        except Exception as e:
            print(f"  ❌ Error con {name}: {e}")
            
    if all_data:
        master_df = pd.concat(all_data, axis=1)
        # Limpiar índice
        master_df.index = master_df.index.date
        master_df.index.name = "fecha"
        
        output_file = OUTPUT_DIR / "market_data_daily.csv"
        master_df.to_csv(output_file)
        print(f"\n✅ Datos de mercado guardados exitosamente en: {output_file}")
    else:
        print("❌ No se pudo descargar ningún dato de mercado.")

if __name__ == "__main__":
    download_market_data()
