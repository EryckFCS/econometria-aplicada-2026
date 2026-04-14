import json
from unittest.mock import Mock, patch

from core.source_backends import SourceBackendRegistry


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

    response = Mock()
    response.json.return_value = payload
    response.text = json.dumps(payload)
    response.content = response.text.encode("utf-8")
    response.headers = {"content-type": "application/json"}
    response.status_code = 200
    response.url = "https://api.example.org/indicator?countries=EC,AR&start=2001&end=2001"
    response.raise_for_status.return_value = None

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