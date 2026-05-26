"""Consolidated integration, database schema, and RAG/Lake contract tests."""

from __future__ import annotations

from pathlib import Path
from collections import Counter
from unittest.mock import Mock, patch
import pandas as pd
import pytest

from ecs_quantitative.core.lake import LakeManager
from ecs_quantitative.core import fetch_wb
from ecs_quantitative.ingestion import SourceBackendRegistry
from lib.catalog import SERIES_APE1

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data" / "curation" / "group_work" / "standardized"
REQUIRED_COLUMNS = {"iso2", "year"}
METADATA_COLUMNS = {"iso2", "pais", "country", "year"}


# --- Lake Manifest & Library Integration Contracts ---

def _make_mock_response(sample_json):
    mock_resp = Mock()
    mock_resp.json.return_value = sample_json
    mock_resp.raise_for_status.return_value = None
    return mock_resp


def test_bibliography_manifest_is_built_from_the_central_lake(tmp_path: Path) -> None:
    from src.core.lake import build_bibliography_manifest
    
    source_file = tmp_path / "sample_bibliography.pdf"
    source_file.write_bytes(b"%PDF-1.4\n% sample bibliography\n")

    lake = LakeManager(lake_base=tmp_path / "lake")
    registered_path = lake.register_bibliography(
        source_file, "sample_source", tags=["test"]
    )

    manifest = build_bibliography_manifest(lake_base=lake.base)

    assert manifest["library"]
    entry = manifest["library"][0]
    assert entry["id"] == "sample_source"
    assert entry["path"] == str(registered_path)
    assert entry["source_type"] == "book"
    assert entry["tags"] == ["test"]


def test_bibliography_manifest_can_be_written_to_disk(tmp_path: Path) -> None:
    from src.core.lake import write_bibliography_manifest
    
    source_file = tmp_path / "sample_bibliography.pdf"
    source_file.write_bytes(b"%PDF-1.4\n% sample bibliography\n")

    lake = LakeManager(lake_base=tmp_path / "lake")
    lake.register_bibliography(source_file, "sample_source", tags=["test"])

    output_path = write_bibliography_manifest(
        output_path=tmp_path / "generated_manifest.json", lake_base=lake.base
    )

    assert output_path.is_file()
    assert "sample_source" in output_path.read_text(encoding="utf-8")


# --- System & Catalog Contracts ---

def test_catalog_entries_are_unique_and_backend_compatible():
    """Valida que el catálogo local sea único y compatible con los backends centralizados."""
    required_keys = ["nombre_raw", "codigo_api", "unidad_api", "rol", "concepto"]
    available_backends = set(SourceBackendRegistry.available())

    names = [entry["nombre_raw"] for entry in SERIES_APE1]
    codes = [entry["codigo_api"] for entry in SERIES_APE1]

    # Validar unicidad
    assert not [name for name, count in Counter(names).items() if count > 1], (
        "Nombres duplicados en catálogo"
    )
    assert not [code for code, count in Counter(codes).items() if count > 1], (
        "Códigos duplicados en catálogo"
    )

    for entry in SERIES_APE1:
        # Validar llaves requeridas
        for key in required_keys:
            assert key in entry, (
                f"Error: '{entry.get('nombre_raw', 'SIN_NOMBRE')}' carece de '{key}'."
            )
            assert entry[key] is not None, (
                f"Error: '{key}' vacío en '{entry['nombre_raw']}'."
            )
            assert isinstance(entry[key], str), (
                f"Error: '{key}' en '{entry['nombre_raw']}' debe ser string."
            )

        # Validar compatibilidad de backends
        source_kind = entry.get("source_kind", "world_bank")
        assert source_kind in available_backends, (
            f"Backend '{source_kind}' de '{entry['nombre_raw']}' no está registrado en ecs_quantitative."
        )


def test_library_integration_fetch_wb():
    """Verifica que la integración con fetch_wb de ecs_quantitative funcione desde el nodo."""
    sample_json = [
        {"page": 1, "pages": 1, "per_page": "1000", "total": 1},
        [
            {
                "country": {"id": "EC"},
                "countryiso3code": "ECU",
                "date": "2023",
                "value": 100,
            },
        ],
    ]

    mock_resp = _make_mock_response(sample_json)
    with patch("requests.Session.get", return_value=mock_resp):
        df, meta = fetch_wb("TEST_IND", "EC", 2023, 2023)

    assert not df.empty
    assert df.iloc[0]["iso2"] == "EC"
    assert df.iloc[0]["value"] == 100.0


# --- Downstream Data contracts ---

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
