"""
APE1 MASTER BUILD ORCHESTRATOR
Unified pipeline for Applied Econometrics 2026.
Nomenclature: M01-U1-APE-Master_Build
"""

import sys
import importlib.util
from pathlib import Path
from loguru import logger
from core.exceptions import DataIntegrityError, RegistryOverwriteDataError, CIEError

# Configurar ROOT del proyecto
PROJECT_ROOT = Path(__file__).parents[2]
sys.path.append(str(PROJECT_ROOT / "src"))

def import_task(task_name):
    """Importa dinámicamente tareas con nombres estandarizados (soportando guiones)."""
    spec = importlib.util.find_spec(f"tasks.{task_name}")
    if spec is None:
        raise ImportError(f"No se encontró la tarea: tasks.{task_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_pipeline():
    logger.info("🎬 Iniciando MASTER BUILD PIPELINE (Unidad 1)")
    
    try:
        # T01: Base de Homicidios y Controles (APE)
        logger.info("--- [T01-U1-APE] Homicidios y Controles Económicos ---")
        t01 = import_task("T01-U1-APE-Homicidios_Ecuador")
        t01.run_task()
        
        # T02: Consolidado de Equipo (ACD)
        logger.info("--- [T02-U1-ACD] Consolidado Final de Equipo ---")
        try:
            import_task("T02-U1-ACD-Consolidado_Equipo")
            # t02.run()  # Comentado hasta verificar si tiene entrypoint 'run' o 'run_task'
        except Exception as e:
            logger.warning(f"Salto de T02: {e}")

        # T03: Panel Ambiental (AA)
        logger.info("--- [T03-U1-AA] Panel Ambiental LATAM ---")
        try:
            import_task("T03-U1-AA-Panel_Ambiental_Latam")
            # t03.task_ape1_panel() 
        except Exception as e:
            logger.warning(f"Salto de T03: {e}")

        logger.success("✅ M01 MASTER BUILD completado exitosamente.")
        
    except DataIntegrityError as e:
        logger.critical(f"🛑 VIOLACIÓN DE INTEGRIDAD DE DATOS: {e}")
        logger.error("El pipeline se detuvo para proteger la validez científica de la investigación.")
        sys.exit(1)
    except RegistryOverwriteDataError as e:
        logger.critical(f"🛡️ ERROR DE CONFIGURACIÓN DE REGISTRO: {e}")
        sys.exit(1)
    except CIEError as e:
        logger.error(f"❌ Error interno en la infraestructura CIE: {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"💥 Error inesperado en la orquestación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
