from pathlib import Path
from ecs_quantitative.management.intelligence import (
    IntelligenceOrchestrator,
    IntelligenceMaintenance,
)


def main():
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    base_dir = PROJECT_ROOT / "bibliography"
    config_path = PROJECT_ROOT / "config" / "intelligence_map.json"

    # 1. Pipeline Principal
    orchestrator = IntelligenceOrchestrator(
        base_dir, collection_name="applied_econometrics_2026"
    )
    orchestrator.run_pipeline()

    # 2. Mantenimiento
    maintenance = IntelligenceMaintenance(config_path)
    maintenance.launch_pending_ocr()
    maintenance.apply_excel_links("APPLIED_ECONOMETRICS_2026_Audit_Data")


if __name__ == "__main__":
    main()
