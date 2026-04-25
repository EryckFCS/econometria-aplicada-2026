import logging
from pathlib import Path
from ecs_quantitative.ingestion import PanelEngine
from ecs_quantitative.reporting import AcademicExporter
from lib.catalog import PAISES_LATAM, load_catalog
from ecs_quantitative.core import load_pipeline_profile_from_env

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
OUTPUT_DIR = PROJECT_ROOT / "data" / "exports"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Consolidado_Final_Equipo")


def task_merge_api_local():
    """
    Orquestador final:
    1. Descarga datos de API para completar vacíos.
    2. Usa archivos normalizados del equipo como fallback o fuente primaria según corresponda.
    3. Rango extendido: 1990-2024.
    """
    logger.info("--- Iniciando Fusión API + Datos Locales (1990-2024) ---")

    # Unir catálogos evitando duplicaciones nominales
    # Priorizamos la definición de catalog_equipo que tiene los fallbacks configurados
    series_equipo = load_catalog("equipo")
    series_ape1 = load_catalog("ape1")
    nombres_grupo = {s["nombre_raw"] for s in series_equipo}
    catalog_full = series_equipo + [
        s for s in series_ape1 if s["nombre_raw"] not in nombres_grupo
    ]

    # Configurar motor (1990-2024)
    countries = list(PAISES_LATAM.keys())

    engine = PanelEngine(
        countries=countries, start_year=1990, end_year=2024, countries_dict=PAISES_LATAM
    )

    # Perfil para la ejecución (Asegurar que intente descarga de API)
    profile = load_pipeline_profile_from_env("ape1_latam")
    # Forzar el rango en el perfil también
    profile = profile.__class__(
        name="master_fusion",
        scope="global",
        countries=tuple(countries),
        start_year=1990,
        end_year=2024,
        allowed_scopes=("global",),
        default_source="world_bank",
        source_priority=(
            "world_bank",
            "local_file",
        ),  # Buscar en API primero, luego local
        allow_partial=True,
        description="Fusión maestra de datos del equipo con completitud vía API WDI/WGI.",
        metadata={},
    )

    df, manifest = engine.build_panel(catalog_full, profile=profile)

    # Exportar resultados
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Excel con Diccionario para el equipo
    exporter = AcademicExporter(output_base=PROJECT_ROOT / "data" / "raw")
    exporter.to_academic_excel(
        df, catalog_full, filename="MASTER_FINAL_CONSOLIDADO_API_LOCAL.xlsx"
    )

    # 2. CSV para Stata
    csv_path = PROJECT_ROOT / "data" / "raw" / "csv" / "panel_final_equipo_api.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    logger.info(f"✅ Proceso finalizado. Archivo generado en: {csv_path}")


if __name__ == "__main__":
    task_merge_api_local()
