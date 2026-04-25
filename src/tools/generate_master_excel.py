import pandas as pd
from pathlib import Path

# Configuración de Rutas
PROJECT_ROOT = Path(
    "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/econometria-aplicada-2026"
)
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "csv" / "panel_final_equipo_api.csv"
OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "raw" / "excel" / "MASTER_ECONOMETRIA_LATAM_2026.xlsx"
)

# Mapeo de Responsables y Colores
RESPONSABLES = {
    "Erick Condoy": {
        "variables": [
            "gei_total_exclulucf_MtCO2e",
            "renew_cons_pct_tfec",
            "wgi_va_est",
            "wgi_ge_est",
        ],
        "color": "#DCE6F1",  # Azul claro
    },
    "Marvin Valdivieso": {
        "variables": [
            "informalidad",
            "tecnologia",
            "calidad_institucional",
            "gobernanza",
        ],
        "color": "#EBF1DE",  # Verde claro
    },
    "Abel Espinosa": {
        "variables": [
            "indice_riesgo_climatico",
            "PIBpc",
            "renta_rec_nat",
            "impuestos_ambientales",
            "protec_der_lab",
            "climate_altering_land_index",
        ],
        "color": "#FDE9D9",  # Naranja claro
    },
    "Helen Beltran": {
        "variables": ["poblacion", "incertidumbre_energetica"],
        "color": "#F2DCDB",  # Rosa claro
    },
    "Erik Moreno": {
        "variables": ["superficie_forestal"],
        "color": "#E4DFEC",  # Púrpura claro
    },
    "Banco Mundial / APE1": {
        "variables": [
            "forest_area_km2",
            "ghg_total_incl_lulucf_mt_co2e",
            "gdp_per_capita_const2015_usd",
            "trade_pct_gdp",
            "fdi_inflows_pct_gdp",
            "renewable_energy_pct_final_energy",
            "domestic_credit_private_pct_gdp",
            "wgi_voice_accountability_est",
            "co2_emissions_kt",
        ],
        "color": "#F2F2F2",  # Gris claro
    },
}


def get_responsible(var_name):
    for resp, config in RESPONSABLES.items():
        if var_name in config["variables"]:
            return resp, config["color"]
    return "Global", "#FFFFFF"


def main():
    print("🎨 Generando Excel Maestro Profesional...")

    # Leer datos
    df = pd.read_csv(INPUT_FILE)

    # Crear Excel con XlsxWriter
    writer = pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter")

    # 1. Hoja de Datos
    df.to_excel(writer, sheet_name="PANEL_DATOS", index=False)
    workbook = writer.book
    worksheet_data = writer.sheets["PANEL_DATOS"]

    # Formatos
    header_format = workbook.add_format(
        {
            "bold": True,
            "text_wrap": True,
            "valign": "top",
            "fg_color": "#1F4E78",
            "font_color": "white",
            "border": 1,
        }
    )

    # Aplicar formato a cabeceras de datos
    for col_num, value in enumerate(df.columns.values):
        worksheet_data.write(0, col_num, value, header_format)

    worksheet_data.freeze_panes(1, 3)  # Congelar ISO2, Pais, Year
    worksheet_data.set_column("A:B", 10)
    worksheet_data.set_column("C:C", 8)
    worksheet_data.set_column("D:Z", 15)

    # 2. Hoja de Diccionario
    dict_rows = []
    for var in df.columns:
        if var in ["iso2", "pais", "year"]:
            continue
        resp, color = get_responsible(var)
        dict_rows.append(
            {
                "Variable": var,
                "Responsable": resp,
                "Color_HEX": color,
                "Definición": "Dato integrado en el panel maestro 2026.",
            }
        )

    df_dict = pd.DataFrame(dict_rows)
    df_dict.to_excel(writer, sheet_name="DICCIONARIO", index=False)
    worksheet_dict = writer.sheets["DICCIONARIO"]

    # Formato especial para el diccionario
    for i, row in df_dict.iterrows():
        cell_color = row["Color_HEX"]
        row_format = workbook.add_format({"fg_color": cell_color, "border": 1})
        for j, val in enumerate(row):
            worksheet_dict.write(i + 1, j, val, row_format)

    # Formato cabecera Diccionario
    for col_num, value in enumerate(df_dict.columns.values):
        worksheet_dict.write(0, col_num, value, header_format)

    worksheet_dict.set_column("A:A", 30)
    worksheet_dict.set_column("B:B", 20)
    worksheet_dict.set_column("D:D", 50)

    writer.close()
    print(f"✅ Excel Maestro generado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
