import sys
from pathlib import Path

# Agregar src al path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.lib.intelligence.sync import IntelligenceOrchestrator  # noqa: E402
from src.lib.intelligence.maintenance import IntelligenceMaintenance  # noqa: E402


def main():
    base_dir = PROJECT_ROOT / "bibliography"
    config_path = PROJECT_ROOT / "config" / "intelligence_map.json"

    # 1. Orquestación Normal
    orchestrator = IntelligenceOrchestrator(base_dir)
    orchestrator.run_pipeline()

    # 2. Mantenimiento (Opcional/Automático)
    maintenance = IntelligenceMaintenance(config_path)

    # Lanzar OCRs pendientes si existen
    maintenance.launch_pending_ocr()

    # Sincronizar links de Excel si es necesario
    maintenance.apply_excel_links("KOR_Audit_Data")


if __name__ == "__main__":
    main()
