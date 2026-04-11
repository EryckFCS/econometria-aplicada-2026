from unittest.mock import patch, Mock

from ape1_utils import fetch_wb


def _make_mock_response(sample_json):
    mock_resp = Mock()
    mock_resp.json.return_value = sample_json
    mock_resp.raise_for_status.return_value = None
    return mock_resp


def test_fetch_wb_single_page():
    sample_json = [
        {"page": 1, "pages": 1, "per_page": "1000", "total": 2},
        [
            {"country": {"id": "ARG"}, "countryiso3code": "ARG", "date": "2000", "value": 10},
            {"country": {"id": "BRA"}, "countryiso3code": "BRA", "date": "2001", "value": 20},
        ],
    ]

    mock_resp = _make_mock_response(sample_json)
    with patch('requests.Session.get', return_value=mock_resp):
        df, meta = fetch_wb("TEST", "AR;BR", 2000, 2001)
        assert not df.empty
        assert meta["total_registros_validos"] == 2
        assert set(df["iso2"]) == {"AR", "BR"}
        assert df["value"].tolist() == [10.0, 20.0]
