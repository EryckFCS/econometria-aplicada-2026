"""
NODE PACKAGING TOOL
Specialized tool to package node artifacts into a submission zip.
Nomenclature: src/tools/pack_delivery.py
"""

import sys
from pathlib import Path
from loguru import logger

# Configurar ROOT y PYTHONPATH
PROJECT_ROOT = Path(__file__).parents[2].resolve()
sys.path.append(str(PROJECT_ROOT / "src"))

try:
    from ecs_quantitative.reporting import packager
except ImportError:
    logger.error(
        "❌ ecs_quantitative no encontrada. Asegúrate de que capital-workstation-libs esté instalada."
    )
    sys.exit(1)

# Configuraciones por defecto para este Nodo
AUTHOR = "ERICK_CONDOY"
VAULT_DELIVERIES = PROJECT_ROOT / "writing" / "vault" / "deliveries"


def run_packaging(unit="U1", activity_type="APE"):
    """
    Empaqueta los productos del nodo (writing/dist y data/exports) en un ZIP.
    """
    logger.info(f"📦 Preparando empaque para {unit}-{activity_type}...")

    # Fuentes de archivos para el paquete
    source_dirs = [PROJECT_ROOT / "writing" / "dist", PROJECT_ROOT / "data" / "exports"]

    # Validar existencia de al menos una fuente
    if not any(d.exists() for d in source_dirs):
        logger.warning(
            "⚠️ No se encontraron carpetas 'dist' o 'exports'. ¿Has ejecutado el pipeline y el render?"
        )

    # Generar nombre estándar
    zip_name = packager.resolve_submission_name(
        author=AUTHOR, unit=unit, activity_type=activity_type
    )

    # Crear ZIP en la Bóveda
    final_path = packager.compress_directory(
        source_dirs=source_dirs, output_path=VAULT_DELIVERIES, zip_name=zip_name
    )

    logger.success(f"🚀 Empaque completado: {final_path}")
    return final_path


if __name__ == "__main__":
    # Soporte básico de argumentos: python pack_delivery.py U1 ACD
    u = sys.argv[1] if len(sys.argv) > 1 else "U1"
    t = sys.argv[2] if len(sys.argv) > 2 else "APE"

    run_packaging(unit=u, activity_type=t)
