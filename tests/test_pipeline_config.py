from core.pipeline_config import load_pipeline_profile, load_pipeline_profile_from_env


def test_builtin_ape1_profile_has_expected_window():
    profile = load_pipeline_profile("ape1_latam")

    assert profile.start_year == 2000
    assert profile.end_year == 2023
    assert len(profile.countries) == 20
    assert "latam_panel" in profile.allowed_scopes


def test_profile_loader_reads_toml_and_overrides(tmp_path):
    config_path = tmp_path / "pipeline_profiles.toml"
    config_path.write_text(
        """
[profiles.demo]
description = "Perfil de prueba"
scope = "demo_scope"
countries = ["EC", "AR"]
start_year = 1995
end_year = 1999
allowed_scopes = ["global", "demo_scope"]
default_source = "local_csv"
source_priority = ["local_csv", "world_bank"]
allow_partial = false
""",
        encoding="utf-8",
    )

    profile = load_pipeline_profile("demo", config_path=config_path, end_year=2001)

    assert profile.scope == "demo_scope"
    assert profile.countries == ("EC", "AR")
    assert profile.start_year == 1995
    assert profile.end_year == 2001
    assert profile.default_source == "local_csv"
    assert profile.allow_partial is False


def test_profile_loader_applies_environment_overrides(monkeypatch):
    monkeypatch.setenv("PIPELINE_PROFILE", "ape1_latam")
    monkeypatch.setenv("PIPELINE_START_YEAR", "1990")
    monkeypatch.setenv("PIPELINE_END_YEAR", "1994")
    monkeypatch.setenv("PIPELINE_COUNTRIES", "EC,PE")
    monkeypatch.setenv("PIPELINE_SCOPE", "custom_scope")
    monkeypatch.setenv("PIPELINE_ALLOWED_SCOPES", "global,custom_scope")

    profile = load_pipeline_profile_from_env()

    assert profile.start_year == 1990
    assert profile.end_year == 1994
    assert profile.countries == ("EC", "PE")
    assert profile.scope == "custom_scope"
    assert profile.allowed_scopes == ("global", "custom_scope")