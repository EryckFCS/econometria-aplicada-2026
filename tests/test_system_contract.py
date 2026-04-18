from collections import Counter
from unittest.mock import Mock, patch

from core.utils import fetch_wb
from lib.catalog import SERIES_APE1
from core.source_backends import SourceBackendRegistry


def _make_mock_response(sample_json):
    mock_resp = Mock()
    mock_resp.json.return_value = sample_json
    mock_resp.raise_for_status.return_value = None
    return mock_resp


def test_catalog_entries_are_unique_and_backend_compatible():
    required_keys = ["nombre_raw", "codigo_api", "unidad_api", "rol", "concepto"]
    available_backends = set(SourceBackendRegistry.available())

    names = [entry["nombre_raw"] for entry in SERIES_APE1]
    codes = [entry["codigo_api"] for entry in SERIES_APE1]

    assert not [name for name, count in Counter(names).items() if count > 1]
    assert not [code for code, count in Counter(codes).items() if count > 1]

    for entry in SERIES_APE1:
        for key in required_keys:
            assert key in entry, f"Error: '{entry.get('nombre_raw', 'SIN_NOMBRE')}' carece de '{key}'."
            assert entry[key] is not None, f"Error: '{key}' vacío en '{entry['nombre_raw']}'."
            assert isinstance(entry[key], str), f"Error: '{key}' en '{entry['nombre_raw']}' debe ser string."

        source_kind = entry.get("source_kind", "world_bank")
        assert source_kind in available_backends, (
            f"Backend '{source_kind}' de '{entry['nombre_raw']}' no está registrado."
        )


def test_fetch_wb_single_page():
    sample_json = [
        {"page": 1, "pages": 1, "per_page": "1000", "total": 2},
        [
            {"country": {"id": "ARG"}, "countryiso3code": "ARG", "date": "2000", "value": 10},
            {"country": {"id": "BRA"}, "countryiso3code": "BRA", "date": "2001", "value": 20},
        ],
    ]

    mock_resp = _make_mock_response(sample_json)
    with patch("requests.Session.get", return_value=mock_resp):
        df, meta = fetch_wb("TEST", "AR;BR", 2000, 2001)

    assert not df.empty
    assert meta["total_registros_validos"] == 2
    assert set(df["iso2"]) == {"AR", "BR"}
    assert df["value"].tolist() == [10.0, 20.0]


def test_fetch_wb_paginates_and_deduplicates():
    first_page = [
        {"page": 1, "pages": 2, "per_page": "1000", "total": 4},
        [
            {"country": {"id": "ARG"}, "countryiso3code": "ARG", "date": "2000", "value": 10},
            {"country": {"id": "BRA"}, "countryiso3code": "BRA", "date": "2001", "value": 20},
        ],
    ]
    second_page = [
        {"page": 2, "pages": 2, "per_page": "1000", "total": 4},
        [
            {"country": {"id": "BRA"}, "countryiso3code": "BRA", "date": "2001", "value": 20}, # Duplicado perfecto (permitido)
            {"country": {"id": "CHL"}, "countryiso3code": "CHL", "date": "2002", "value": 30},
        ],
    ]

    responses = [_make_mock_response(first_page), _make_mock_response(second_page)]
    with patch("requests.Session.get", side_effect=responses) as mocked_get:
        df, meta = fetch_wb("TEST", "AR;BR;CL", 2000, 2002)

    assert mocked_get.call_count == 2
    assert meta["total_registros_descargados"] == 4
    assert meta["total_registros_validos"] == 3
    assert set(df["iso2"]) == {"AR", "BR", "CL"}
    assert set(tuple(row) for row in df[["iso2", "year", "value"]].to_numpy()) == {
        ("AR", 2000, 10.0),
        ("BR", 2001, 20.0),
        ("CL", 2002, 30.0),
    }

def test_fetch_wb_raises_on_contradiction():
    from core.exceptions import DataIntegrityError
    import pytest
    
    contradictory_data = [
        {"page": 1, "pages": 1, "per_page": "1000", "total": 2},
        [
            {"countryiso3code": "ECU", "date": "2020", "value": 1.0},
            {"countryiso3code": "ECU", "date": "2020", "value": 9.9}, # CONTRADICCIÓN
        ],
    ]

    mock_resp = _make_mock_response(contradictory_data)
    with patch("requests.Session.get", return_value=mock_resp):
        with pytest.raises(DataIntegrityError, match="Contradicción"):
            fetch_wb("TEST", "EC", 2020, 2020)