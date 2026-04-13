"""
ORQUESTADOR UNIDAD 1: Series de Tiempo y Modelos Dinámicos
Enfoque modular: Orquestación de Librerías.
"""
import logging
from pathlib import Path
from lib.loaders.wb_loader import WorldBankLoader
from lib.processors.panel_builder import PanelBuilder
from lib.processors.timeseries_builder import TimeSeriesBuilder
from lib.exporters.excel_exporter import AcademicExcelExporter
from lib.catalog import SERIES_APE1, PAISES_LATAM

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data" / "raw"
CSV_DIR = DATA_DIR / "csv"
EXCEL_DIR = DATA_DIR / "excel"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Unidad1_Orchestrator")

def task_ape1_panel():
    """Genera el Panel para APE1 (20 países, 2000-2023)."""
    logger.info("--- Iniciando Tarea APE1 (Panel Dinámico) ---")
    
    loader = WorldBankLoader(list(PAISES_LATAM.keys()), 2000, 2023)
    builder = PanelBuilder(loader, PAISES_LATAM)
    df, manifest = builder.build(SERIES_APE1)
    
    # Exportar para Stata
    df.to_csv(CSV_DIR / "panel_ape1.csv", index=False, encoding="utf-8-sig")
    
    # Exportar para Humanos (Excel con Diccionario)
    exporter = AcademicExcelExporter(EXCEL_DIR / "APE1_Modelos_Dinamicos.xlsx")
    exporter.export(df, SERIES_APE1)
    logger.info("APE1 Panel completado.")

def task_unidad1_timeseries(country_code="EC"):
    """Genera una Serie de Tiempo para un país específico (Unidad 1: ARIMA/ARCH)."""
    logger.info(f"--- Iniciando Serie de Tiempo: {country_code} ---")
    
    loader = WorldBankLoader([country_code], 1990, 2023) # Mayor profundidad para series de tiempo
    builder = TimeSeriesBuilder(loader, country_code)
    df, manifest = builder.build(SERIES_APE1)
    
    # Exportar
    df.to_csv(CSV_DIR / f"timeseries_{country_code}.csv", index=False, encoding="utf-8-sig")
    
    exporter = AcademicExcelExporter(EXCEL_DIR / f"Unidad1_SeriesTiempo_{country_code}.xlsx")
    exporter.export(df, SERIES_APE1)
    logger.info(f"Serie de tiempo {country_code} completada.")

if __name__ == "__main__":
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    EXCEL_DIR.mkdir(parents=True, exist_ok=True)
    
    task_ape1_panel()
    task_unidad1_timeseries("EC") # Ecuador como ejemplo de la Unidad 1
