import json
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from core.source_backends import SourceBackendRegistry


def _make_http_response(payload, url):
    response = Mock()
    response.json.return_value = payload
    response.text = json.dumps(payload)
    response.content = response.text.encode("utf-8")
    response.headers = {"content-type": "application/json"}
    response.status_code = 200
    response.url = url
    response.raise_for_status.return_value = None
    return response


def test_world_bank_backend_routes_through_fetch_wb():
    sample_frame = pd.DataFrame(
        {
            "iso2": ["EC"],
            "year": [2000],
            "value": [12.5],
        }
    )

    with patch("core.source_backends.fetch_wb", return_value=(sample_frame, {"mocked": True})) as mocked_fetch:
        frame, meta = SourceBackendRegistry.fetch(
            "world_bank",
            {"codigo_api": "TEST"},
            "EC",
            2000,
            2000,
        )

    mocked_fetch.assert_called_once_with("TEST", "EC", 2000, 2000)
    assert frame.equals(sample_frame)
    assert meta["source_kind"] == "world_bank"
    assert meta["source_ref"] == "TEST"


def test_local_csv_backend_filters_and_standardizes(tmp_path):
    source_path = tmp_path / "series.csv"
    pd.DataFrame(
        {
            "iso2": ["EC", "EC", "AR"],
            "year": [1990, 1991, 1991],
            "my_value": [1.0, 2.0, 3.0],
        }
    ).to_csv(source_path, index=False)

    frame, meta = SourceBackendRegistry.fetch(
        "local_csv",
        {"source_ref": Path(source_path), "target_column": "my_value", "nombre_raw": "demo"},
        "EC;AR",
        1991,
        1991,
    )

    assert frame.shape == (2, 3)
    assert set(frame["iso2"]) == {"EC", "AR"}
    assert set(frame["year"]) == {1991}
    assert "value" in frame.columns
    assert meta["source_kind"] == "local_csv"
    assert meta["records_kept"] == 2


def test_http_backend_parses_json_records_and_templates_request():
    payload = {
        "data": {
            "records": [
                {"country_code": "EC", "year": 2001, "indicator_value": 1.2},
                {"country_code": "AR", "year": 2001, "indicator_value": 2.3},
                {"country_code": "EC", "year": 2000, "indicator_value": 9.9},
            ]
        }
    }

    response = _make_http_response(
        payload,
        "https://api.example.org/indicator?countries=EC,AR&start=2001&end=2001",
    )

    session = Mock()
    session.request.return_value = response

    with patch("core.source_backends.create_session", return_value=session):
        frame, meta = SourceBackendRegistry.fetch(
            "http",
            {
                "nombre_raw": "vdem_proxy",
                "url": "https://api.example.org/indicator?countries={countries_csv}",
                "http_method": "GET",
                "params": {"start": "{start_year}", "end": "{end_year}"},
                "response_format": "json",
                "records_path": "data.records",
                "country_column": "country_code",
                "year_column": "year",
                "value_column": "indicator_value",
            },
            "EC;AR",
            2001,
            2001,
        )

    session.request.assert_called_once_with(
        "GET",
        "https://api.example.org/indicator?countries=EC,AR",
        headers={},
        params={"start": "2001", "end": "2001"},
        timeout=30.0,
        verify=True,
    )
    assert frame.shape == (2, 3)
    assert set(frame["iso2"]) == {"EC", "AR"}
    assert meta["source_kind"] == "http"
    assert meta["http_status_code"] == 200
    assert meta["http_method"] == "GET"