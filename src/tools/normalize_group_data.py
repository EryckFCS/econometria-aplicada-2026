import pandas as pd
from pathlib import Path
from core.utils import normalize_iso2

# Detección dinámica de rutas del proyecto
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PARTNERS_DIR = PROJECT_ROOT / "data" / "raw" / "partners"
OUTPUT_DIR = PROJECT_ROOT / "data" / "curation" / "group_work" / "standardized"


def main():
    print("🚀 Iniciando Normalización Robusta CIE (v4)...")

    # 1. ERICK CONDOY
    file_path = PARTNERS_DIR / "erick_condoy" / "base_v1.xlsx"
    print(f"- {file_path.name} (Erick)...")
    df = pd.read_excel(file_path)
    df["iso2"] = df["iso2"].apply(normalize_iso2)
    df.to_csv(OUTPUT_DIR / "erick_condoy_std.csv", index=False)

    # 2. ERIK MORENO
    file_path = PARTNERS_DIR / "erik_moreno" / "base_v1.xlsx"
    print(f"- {file_path.name} (Erik M)...")

    # Cargar hojas
    df_forest = pd.read_excel(file_path, sheet_name="Superficie forestal")
    df_co2 = pd.read_excel(file_path, sheet_name="Emisiones de CO2")
    df_vab = pd.read_excel(file_path, sheet_name="VAB")
    df_huella = pd.read_excel(file_path, sheet_name="Factor de capacidad de carga hu")
    df_rigor = pd.read_excel(file_path, sheet_name="Rigorosidad politica ambiental")

    # Normalizar cada una
    def std_erik(df, rename_dict):
        df["iso2"] = df["Unnamed: 1"].apply(normalize_iso2)
        df = df.rename(columns={"Año": "year", **rename_dict})
        return df[["iso2", "year"] + list(rename_dict.values())]

    df1 = std_erik(df_forest, {"Superficie forestal": "superficie_forestal"})
    df2 = std_erik(df_co2, {"Emisiones de CO2": "co2_emissions_moreno"})
    df3 = std_erik(
        df_vab,
        {
            "VAB manufacrura ": "vab_manufactura",
            "VAB agricultura": "vab_agricultura",
            "VAB Servicios": "vab_servicios",
        },
    )
    df4 = std_erik(df_huella, {"Huella ecológica": "huella_ecologica"})
    df5 = std_erik(
        df_rigor, {"Impuesto medioambiental ": "impuesto_medioambiental_moreno"}
    )

    # Unificar todas
    erik_final = (
        df1.merge(df2, on=["iso2", "year"], how="outer")
        .merge(df3, on=["iso2", "year"], how="outer")
        .merge(df4, on=["iso2", "year"], how="outer")
        .merge(df5, on=["iso2", "year"], how="outer")
    )

    erik_final.to_csv(OUTPUT_DIR / "erik_moreno_std.csv", index=False)

    # 3. MARVIN 1
    file_path = PARTNERS_DIR / "marvin_valdivieso" / "base_v1.xlsx"
    print(f"- {file_path.name} (Marvin v1)...")
    df = pd.read_excel(file_path)
    df = df.dropna(subset=["pais", "años"])
    df["iso2"] = df["pais"].apply(normalize_iso2)
    df = df.rename(columns={"años": "year"})
    df["year"] = pd.to_numeric(df["year"], errors="coerce").dropna().astype(int)
    df = df.dropna(subset=["iso2", "year"])
    df = df.drop_duplicates(subset=["iso2", "year"], keep="first")
    df[["iso2", "year", "calidad_institucional", "gobernanza", "informalidad"]].to_csv(
        OUTPUT_DIR / "marvin_v1_std.csv", index=False
    )

    # 4. MARVIN 2
    file_path = PARTNERS_DIR / "marvin_valdivieso" / "base_v2.xlsx"
    print(f"- {file_path.name} (Marvin v2)...")
    df = pd.read_excel(file_path)
    df_long = df.melt(id_vars=["Year"], var_name="country_raw", value_name="tecnologia")
    df_long["iso2"] = df_long["country_raw"].apply(normalize_iso2)
    df_long = df_long.rename(columns={"Year": "year"})
    df_long[["iso2", "year", "tecnologia"]].to_csv(
        OUTPUT_DIR / "marvin_v2_std.csv", index=False
    )

    # 5. ABEL ESPINOSA 1
    file_path = PARTNERS_DIR / "abel_espinosa" / "base_v1.xlsx"
    print(f"- {file_path.name} (Abel v1)...")
    df = pd.read_excel(file_path)
    df["iso2"] = df["codigo"].apply(normalize_iso2)
    df = df.rename(columns={"año": "year"})
    cols = [
        "iso2",
        "year",
        "indice_riesgo_climatico",
        "PIBpc",
        "renta_rec_nat",
        "impuestos_ambientales",
        "protec_der_lab",
    ]
    df[cols].to_csv(OUTPUT_DIR / "abel_std.csv", index=False)

    # 8. ABEL ESPINOSA 3 (Innovación Financiera)
    file_path = PARTNERS_DIR / "abel_espinosa" / "base_v3.csv"
    print(f"- {file_path.name} (Abel v3/Financiera)...")
    df = pd.read_csv(file_path)
    df = df[df["INDICATOR.ID"] == "FMA_IX"].copy()
    df["iso2"] = df["COUNTRY.ID"].apply(normalize_iso2)
    df = df.rename(
        columns={"TIME_PERIOD": "year", "OBS_VALUE": "innovacion_financiera_access"}
    )
    df["year"] = pd.to_numeric(df["year"], errors="coerce").dropna().astype(int)
    df = df.dropna(subset=["iso2", "year", "innovacion_financiera_access"])
    df = df.drop_duplicates(subset=["iso2", "year"], keep="first")
    df[["iso2", "year", "innovacion_financiera_access"]].to_csv(
        OUTPUT_DIR / "abel_v3_std.csv", index=False
    )

    # 9. HELEN BELTRAN
    file_path = PARTNERS_DIR / "helen_beltran" / "base_v1.xlsx"
    print(f"- {file_path.name} (Helen)...")
    df = pd.read_excel(file_path)
    df["iso2"] = df["País"].apply(normalize_iso2)
    df = df.rename(
        columns={
            "Año": "year",
            "pob": "poblacion",
            "incert_energ": "incertidumbre_energetica",
        }
    )
    df[["iso2", "year", "poblacion", "incertidumbre_energetica"]].to_csv(
        OUTPUT_DIR / "helen_std.csv", index=False
    )

    print("\n✅ Normalización finalizada exitosamente en la nueva estructura.")


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
