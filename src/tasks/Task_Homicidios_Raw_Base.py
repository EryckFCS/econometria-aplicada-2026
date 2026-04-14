import sys
import os
from pathlib import Path

# Añadir src al path para que funcionen los imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.engine import WECPanelEngine
from lib.data_doctor import DataDoctor
from lib.exporters import AcademicExporter
from core.pipeline_config import load_pipeline_profile_from_env

# --- CONFIGURACIÓN DE VARIABLES (Metadata Maestro) ---
VARIABLES_HOMICIDIOS = [
    {
        "nombre_raw": "homicidios_100k",
        "codigo_api": "VC.IHR.PSRC.P5",
        "unidad_api": "por cada 100.000 habitantes",
        "fuente": "World Bank",
        "institucion": "UNODC",
        "url_indicador": "https://data.worldbank.org/indicator/VC.IHR.PSRC.P5",
        "rol": "dependiente — seguridad",
        "concepto": "Homicidios intencionales (por cada 100.000 habitantes)",
    },
    {
        "nombre_raw": "desempleo_total_ne",
        "codigo_api": "SL.UEM.TOTL.NE.ZS",
        "unidad_api": "% participación total fuerza laboral",
        "fuente": "World Bank",
        "institucion": "OIT (estimación nacional)",
        "url_indicador": "https://data.worldbank.org/indicator/SL.UEM.TOTL.NE.ZS",
        "rol": "independiente — laboral",
        "concepto": "Desempleo, total (% de participación total en la fuerza laboral) (estimación nacional)",
    },
    {
        "nombre_raw": "uso_internet_pct",
        "codigo_api": "IT.NET.USER.ZS",
        "unidad_api": "% de la población",
        "fuente": "World Bank",
        "institucion": "World Bank",
        "url_indicador": "https://data.worldbank.org/indicator/IT.NET.USER.ZS",
        "rol": "control — digital (No tradicional)",
        "concepto": "Personas que usan Internet (% de la población)",
    },
    {
        "nombre_raw": "gasto_militar_pct_pib",
        "codigo_api": "MS.MIL.XPND.GD.ZS",
        "unidad_api": "% del PIB",
        "fuente": "World Bank",
        "institucion": "SIPRI",
        "url_indicador": "https://data.worldbank.org/indicator/MS.MIL.XPND.GD.ZS",
        "rol": "control — seguridad (No tradicional)",
        "concepto": "Gasto militar (% del PIB)",
    },
    {
        "nombre_raw": "remesas_pct_pib",
        "codigo_api": "BX.TRF.PWKR.DT.GD.ZS",
        "unidad_api": "% del PIB",
        "fuente": "World Bank",
        "institucion": "World Bank",
        "url_indicador": "https://data.worldbank.org/indicator/BX.TRF.PWKR.DT.GD.ZS",
        "rol": "control — económico (No tradicional)",
        "concepto": "Remesas personales, recibidas (% del PIB)",
    }
]

def run_task():
    profile = load_pipeline_profile_from_env("homicidios_ecuador")
    print(
        f"🚀 Iniciando construcción de la base raw LONG ECUADOR ({profile.start_year}-{profile.end_year}) - Motor KISS..."
    )
    
    # 1. Configuración
    paises_dict = {code: ("Ecuador" if code == "EC" else code) for code in profile.countries}
    paises_l = list(profile.countries)
    
    # 2. Inicializar Motor Unificado
    engine = WECPanelEngine(
        countries=paises_l,
        start_year=profile.start_year,
        end_year=profile.end_year,
        countries_dict=paises_dict,
    )
    
    # 3. Construir Panel
    df_panel, _ = engine.build_panel(VARIABLES_HOMICIDIOS, profile=profile)
    
    # 4. APLICAR CURACIÓN (Data Doctor)
    curation_path = os.getenv("CURATION_MANIFEST", "data/curation/ecuador_homicidios_manifest.json")
    doctor = DataDoctor(manifest_path=curation_path)
    df_panel = doctor.apply_cures(df_panel)
    
    # 5. Exportar usando el nuevo Exportador Unificado
    exporter = AcademicExporter(output_base=Path("data/raw"))
    
    # Excel para revisión visual
    exporter.to_academic_excel(df_panel, VARIABLES_HOMICIDIOS, filename="Base_Raw_Ecuador_Homicidios_Long.xlsx")
    
    # CSV para Stata
    exporter.to_stata_csv(df_panel, filename="Base_Raw_Ecuador_Homicidios_Long.csv")
    
    print("\n✅ Proceso completado con éxito con arquitectura simplificada.")

if __name__ == "__main__":
    run_task()
