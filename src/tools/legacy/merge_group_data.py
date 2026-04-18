import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/econometria-aplicada-2026")
INPUT_DIR = PROJECT_ROOT / "data" / "curation" / "group_work" / "standardized"
OUTPUT_FILE = PROJECT_ROOT / "data" / "exports" / "MASTER_CONSOLIDADO_EQUIPO.xlsx"

PAISES_LATAM_ISO2 = [
    "AR", "BO", "BR", "CL", "CO", "CR", "CU", "EC", "SV", "GT", "HT", "HN", "MX", "NI", "PA", "PY", "PE", "DO", "UY", "VE"
]

def main():
    print("🔗 Iniciando Unión Maestro (Merge)...")
    
    files = list(INPUT_DIR.glob("*.csv"))
    if not files:
        print("❌ No se encontraron archivos estandarizados.")
        return

    master_df = None

    for f in sorted(files):
        print(f"  Uniendo {f.name}...")
        df = pd.read_csv(f)
        
        # Asegurar tipos
        df["iso2"] = df["iso2"].astype(str).str.upper()
        df["year"] = pd.to_numeric(df["year"], errors="coerce").dropna().astype(int)
        
        if master_df is None:
            master_df = df
        else:
            # Unión completa (outer) para no perder datos en esta fase
            master_df = master_df.merge(df, on=["iso2", "year"], how="outer")

    # Filtrar solo países de Latam definidos
    master_df = master_df[master_df["iso2"].isin(PAISES_LATAM_ISO2)]
    
    # Ordenar
    master_df = master_df.sort_values(["iso2", "year"])
    
    # Exportar individualmente a CSV para Stata y a Excel para el usuario
    csv_output = PROJECT_ROOT / "data" / "raw" / "csv" / "panel_equipo_final.csv"
    csv_output.parent.mkdir(parents=True, exist_ok=True)
    master_df.to_csv(csv_output, index=False, encoding="utf-8-sig")
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    # Usar AcademicExporter si está disponible? No, mejor directo para rapidez.
    master_df.to_excel(OUTPUT_FILE, index=False)
    
    print("\n🎉 ¡Éxito! Dataset maestro consolidado en:")
    print(f"👉 {OUTPUT_FILE}")
    print(f"👉 {csv_output}")
    
    # Resumen
    print("\nResumen del Dataset:")
    print(f"- Filas: {len(master_df)}")
    print(f"- Columnas: {list(master_df.columns)}")
    print(f"- Países: {master_df['iso2'].nunique()}")
    print(f"- Rango años: {master_df['year'].min()} - {master_df['year'].max()}")

if __name__ == "__main__":
    main()
