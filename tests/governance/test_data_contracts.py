"""Governance tests for the standardized group datasets."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "curation" / "group_work" / "standardized"
REQUIRED_COLUMNS = {"iso2", "year"}
METADATA_COLUMNS = {"iso2", "pais", "country", "year"}


def get_group_datasets() -> list[Path]:
    """Devuelve los CSV estandarizados disponibles."""
    if not DATA_DIR.exists():
        return []
    return sorted(DATA_DIR.glob("*_std.csv"))


@pytest.mark.parametrize("file_path", get_group_datasets())
def test_group_data_contract(file_path: Path) -> None:
    """Valida el esquema minimo del data mart estandarizado."""
    df = pd.read_csv(file_path)
    lower_columns = {column.lower() for column in df.columns}
    data_columns = [
        column for column in df.columns if column.lower() not in METADATA_COLUMNS
    ]

    assert REQUIRED_COLUMNS.issubset(lower_columns), (
        f"{file_path.name} debe incluir al menos 'iso2' y 'year'."
    )

    assert data_columns, f"{file_path.name} no contiene columnas de datos."
    assert df[data_columns].notna().any().any(), (
        f"{file_path.name} no tiene ninguna serie con valores activos."
    )

    assert df["iso2"].dropna().astype(str).str.fullmatch(r"[A-Z]{2}").all(), (
        f"{file_path.name} tiene valores iso2 invalidos."
    )

    non_empty_years = df["year"].dropna()
    assert not non_empty_years.empty, f"{file_path.name} no contiene years validos."
    assert pd.to_numeric(non_empty_years, errors="coerce").notna().all(), (
        f"{file_path.name} tiene valores year no numericos en filas activas."
    )


if __name__ == "__main__":
    print(f"Target Directory: {DATA_DIR}")
    print(f"Found {len(get_group_datasets())} datasets.")
