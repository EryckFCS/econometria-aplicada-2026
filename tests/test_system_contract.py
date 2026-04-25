from collections import Counter
from unittest.mock import Mock, patch

from ecs_quantitative.core import fetch_wb
from ecs_quantitative.ingestion import SourceBackendRegistry
from lib.catalog import SERIES_APE1


def _make_mock_response(sample_json):
    mock_resp = Mock()
    mock_resp.json.return_value = sample_json
    mock_resp.raise_for_status.return_value = None
    return mock_resp


def test_catalog_entries_are_unique_and_backend_compatible():
    """
    Valida que el catálogo local sea único y compatible con los backends
    registrados en la librería central.
    """
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
