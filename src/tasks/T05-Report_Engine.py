import logging
import subprocess
import sys
from pathlib import Path

import os

# Configuración de Rutas
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
WRITING_DIR = PROJECT_ROOT / "writing"
OUTPUT_DIR = WRITING_DIR / "dist"
VENV_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ReportEngine")


def run_quarto_render(target_format: str = "all"):
    """
    Ejecuta el renderizado de Quarto para el formato especificado.
    """
    logger.info(f"🚀 Iniciando renderizado de Quarto (Formato: {target_format})...")

    if not WRITING_DIR.exists():
        logger.error(f"❌ No se encontró el directorio de escritura en: {WRITING_DIR}")
        return

    # Inyectar el python del venv para Quarto
    env = os.environ.copy()
    env["QUARTO_PYTHON"] = str(VENV_PYTHON)

    # Comando base
    cmd = ["quarto", "render", str(WRITING_DIR / "index.qmd")]

    if target_format != "all":
        cmd.extend(["--to", target_format])

    try:
        # Ejecutar Quarto
        result = subprocess.run(
            cmd, cwd=PROJECT_ROOT, capture_output=True, text=True, env=env
        )

        if result.returncode == 0:
            logger.info("✅ Renderizado completado con éxito.")
            logger.info(f"📂 Archivos generados en: {OUTPUT_DIR}")
        else:
            logger.error("❌ Error en el renderizado de Quarto:")
            logger.error(result.stderr)

    except FileNotFoundError:
        logger.error(
            "❌ 'quarto' no está instalado en el sistema o no está en el PATH."
        )
    except Exception as e:
        logger.error(f"❌ Ocurrió un error inesperado: {e}")


def main():
    """
    Punto de entrada para el orquestador de reportes.
    Permite pasar el formato por argumento (ej: python T05-Report_Engine.py docx)
    """
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    # Asegurar que el directorio de salida existe
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    run_quarto_render(target)


if __name__ == "__main__":
    main()
