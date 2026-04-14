"""
ORQUESTADOR UNIDAD 1: Series de Tiempo y Modelos Dinámicos
Enfoque modular: Orquestación de Librerías.
"""
import logging
import os
from pathlib import Path
from lib.engine import WECPanelEngine
from lib.exporters import AcademicExporter
from lib.catalog import SERIES_APE1, PAISES_LATAM
from core.pipeline_config import load_pipeline_profile_from_env

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data" / "raw"
CSV_DIR = DATA_DIR / "csv"
EXCEL_DIR = DATA_DIR / "excel"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Unidad1_Orchestrator")

def task_ape1_panel():
    """Genera el Panel para APE1 (20 países, 2000-2023)."""
    profile = load_pipeline_profile_from_env("ape1_latam")
    logger.info(
        "--- Iniciando Tarea APE1 (Panel Dinámico) %s-%s ---",
        profile.start_year,
        profile.end_year,
    )

    countries_dict = {code: PAISES_LATAM.get(code, code) for code in profile.countries}
    engine = WECPanelEngine(
        countries=list(profile.countries),
        start_year=profile.start_year,
        end_year=profile.end_year,
        countries_dict=countries_dict,
    )
    df, manifest = engine.build_panel(SERIES_APE1, profile=profile)
    
    # Exportar para Stata
    df.to_csv(CSV_DIR / "panel_ape1.csv", index=False, encoding="utf-8-sig")
    
    # Exportar para Humanos (Excel con Diccionario)
    exporter = AcademicExporter(output_base=Path("data/raw"))
    exporter.to_academic_excel(df, SERIES_APE1, filename="APE1_Modelos_Dinamicos.xlsx")
    logger.info("APE1 Panel completado.")

def task_unidad1_timeseries(country_code="EC"):
    """Genera una Serie de Tiempo para un país específico (Unidad 1: ARIMA/ARCH)."""
    logger.info(f"--- Iniciando Serie de Tiempo: {country_code} ---")

    profile = load_pipeline_profile_from_env(
        "ape1_latam",
        )
    series_start_year = int(os.getenv("PIPELINE_START_YEAR", "1990"))
    series_end_year = int(os.getenv("PIPELINE_END_YEAR", "2023"))
    profile = profile.__class__(
        name=profile.name,
        scope="ecuador_series",
        countries=(country_code,),
        start_year=series_start_year,
        end_year=series_end_year,
        allowed_scopes=("global",),
        default_source=profile.default_source,
        source_priority=profile.source_priority,
        allow_partial=profile.allow_partial,
        description="Serie temporal unitaria derivada desde el catálogo APE1.",
        metadata={**profile.metadata, "country_code": country_code},
    )

    countries_dict = {country_code: PAISES_LATAM.get(country_code, country_code)}
    engine = WECPanelEngine(
        countries=[country_code],
        start_year=profile.start_year,
        end_year=profile.end_year,
        countries_dict=countries_dict,
    )
    df, manifest = engine.build_panel(SERIES_APE1, profile=profile)
    
    # Exportar
    df.to_csv(CSV_DIR / f"timeseries_{country_code}.csv", index=False, encoding="utf-8-sig")
    
    exporter = AcademicExporter(output_base=Path("data/raw"))
    exporter.to_academic_excel(df, SERIES_APE1, filename=f"Unidad1_SeriesTiempo_{country_code}.xlsx")
    logger.info(f"Serie de tiempo {country_code} completada.")

if __name__ == "__main__":
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    EXCEL_DIR.mkdir(parents=True, exist_ok=True)
    
    task_ape1_panel()
    task_unidad1_timeseries("EC") # Ecuador como ejemplo de la Unidad 1
