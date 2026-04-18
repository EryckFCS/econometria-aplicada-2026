"""
Governance Tests: Data Contracts for Applied Econometrics 2026.
Ensures group datasets satisfy minimal metadata and formatting requirements.
"""

import pytest
import pandas as pd
from pathlib import Path

DATA_DIR = Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/econometria-aplicada-2026/data/groups")

def get_group_datasets():
    """Returns list of CSVs in the group data directory."""
    if not DATA_DIR.exists():
        return []
    return list(DATA_DIR.glob("*.csv"))

@pytest.mark.parametrize("file_path", get_group_datasets())
def test_group_data_contract(file_path):
    """
    Check if the group dataset follows the mandatory contract:
    1. Contains 'year' column.
    2. Contains 'iso_code' or 'country' column.
    3. Has no completely empty columns.
    """
    df = pd.read_csv(file_path)
    
    # Check 1: Mandatory Year
    assert 'year' in [c.lower() for c in df.columns], f"{file_path.name} is missing 'year' column."
    
    # Check 2: Entity ID
    columns = [c.lower() for c in df.columns]
    has_id = 'iso_code' in columns or 'country' in columns or 'id' in columns
    assert has_id, f"{file_path.name} must have 'iso_code', 'country', or 'id'."
    
    # Check 3: Data Quality
    empty_cols = df.columns[df.isnull().all()].tolist()
    assert not empty_cols, f"{file_path.name} contains completely empty columns: {empty_cols}"

if __name__ == "__main__":
    # If run directly, just check the directory exists
    print(f"Target Directory: {DATA_DIR}")
    print(f"Found {len(get_group_datasets())} datasets.")
