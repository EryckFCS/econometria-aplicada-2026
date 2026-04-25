import pandas as pd
import json
from pathlib import Path
import sys
import os

# ROOT
PROJECT_ROOT = Path(__file__).parents[2]
sys.path.append(str(PROJECT_ROOT / "src"))

from lib.data_doctor import DataDoctor  # noqa: E402


def test_custom_entity_curation():
    # 1. Crear dataset sintético con códigos cantonales de Ecuador
    df = pd.DataFrame(
        {
            "codigo_inec": ["0101", "0102", "1701"],
            "year": [2023, 2023, 2023],
            "pobreza": [None, 0.5, 0.1],
        }
    )

    # 2. Crear manifiesto temporal
    manifest = {
        "entity_column": "codigo_inec",
        "curations": [
            {
                "target_id": "0101",
                "target_column": "pobreza",
                "year": 2023,
                "value": 0.35,
                "source": "Dummy Source",
            }
        ],
    }

    with open("temp_manifest.json", "w") as f:
        json.dump(manifest, f)

    try:
        # 3. Inicializar Doctor con columna personalizada
        doctor = DataDoctor(manifest_path="temp_manifest.json")
        df_cured = doctor.apply_cures(df)

        # 4. Validar
        val = df_cured.loc[df_cured["codigo_inec"] == "0101", "pobreza"].values[0]
        if val == 0.35:
            print("✅ TEST PASSED: DataDoctor generalized successfully.")
        else:
            print(f"❌ TEST FAILED: Expected 0.35, got {val}")
    finally:
        if os.path.exists("temp_manifest.json"):
            os.remove("temp_manifest.json")


if __name__ == "__main__":
    test_custom_entity_curation()
