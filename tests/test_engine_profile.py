from unittest.mock import patch

import pandas as pd

from core.pipeline_config import load_pipeline_profile
from lib.engine import WECPanelEngine


def test_engine_uses_profile_window_and_skips_local_scope_variables():
    profile = load_pipeline_profile("ape1_latam", countries=("EC", "AR"), start_year=2000, end_year=2001)
    engine = WECPanelEngine(
        countries=list(profile.countries),
        start_year=profile.start_year,
        end_year=profile.end_year,
        countries_dict={"EC": "Ecuador", "AR": "Argentina"},
    )

    sample_frame = pd.DataFrame(
        {
            "iso2": ["EC"],
            "year": [2000],
            "value": [10.0],
        }
    )

    with patch("lib.engine.SourceBackendRegistry.fetch", return_value=(sample_frame, {"source_kind": "world_bank"})) as mocked_fetch:
        panel, manifest = engine.build_panel(
            [
                {
                    "nombre_raw": "global_indicator",
                    "codigo_api": "TEST",
                    "unidad_api": "u",
                    "rol": "test",
                    "concepto": "Indicador global",
                    "scope": "latam_panel",
                    "source_kind": "world_bank",
                },
                {
                    "nombre_raw": "ecuador_local_only",
                    "codigo_api": "LOCAL_ENEMDU_INF",
                    "unidad_api": "%",
                    "rol": "objetivo",
                    "concepto": "Indicador local",
                    "scope": "ecuador_local",
                    "source_kind": "local_file",
                },
            ],
            profile=profile,
        )

    assert mocked_fetch.call_count == 1
    assert "global_indicator" in panel.columns
    assert "ecuador_local_only" in panel.columns

    local_entry = next(item for item in manifest if item["variable_local"] == "ecuador_local_only")
    assert local_entry["status"] == "skipped_scope"

    global_entry = next(item for item in manifest if item["variable_local"] == "global_indicator")
    assert global_entry["status"] == "loaded"
    assert global_entry["profile_name"] == profile.name
    assert global_entry["effective_start_year"] == 2000
    assert global_entry["effective_end_year"] == 2001