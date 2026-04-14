from pathlib import Path
from unittest.mock import patch

import pandas as pd

from core.source_backends import SourceBackendRegistry


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