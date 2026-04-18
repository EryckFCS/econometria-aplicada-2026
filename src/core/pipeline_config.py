"""Configuración declarativa para perfiles de pipeline econométrico."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 no aplica aquí.
    tomllib = None

from .config import PIPELINE_CONFIG_FILE

DEFAULT_PROFILE_NAME = "ape1_latam"
LATAM_COUNTRIES = (
    "AR",
    "BO",
    "BR",
    "CL",
    "CO",
    "CR",
    "CU",
    "EC",
    "SV",
    "GT",
    "HT",
    "HN",
    "MX",
    "NI",
    "PA",
    "PY",
    "PE",
    "DO",
    "UY",
    "VE",
)


def _to_tuple(value: Any, fallback: Sequence[str] = ()) -> tuple[str, ...]:
    if value is None:
        return tuple(fallback)

    if isinstance(value, str):
        return (value,)

    return tuple(str(item) for item in value)


def _to_int(value: Any, fallback: int) -> int:
    if value is None:
        return fallback

    return int(value)


def _to_bool(value: Any, fallback: bool) -> bool:
    if value is None:
        return fallback

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}

    return bool(value)


@dataclass(frozen=True, slots=True)
class PipelineProfile:
    """Define un contexto de ejecución para una tarea de datos."""

    name: str
    scope: str
    countries: tuple[str, ...]
    start_year: int
    end_year: int
    allowed_scopes: tuple[str, ...] = ("global",)
    default_source: str = "world_bank"
    source_priority: tuple[str, ...] = ("world_bank",)
    allow_partial: bool = True
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def countries_str(self) -> str:
        return ";".join(self.countries)

    @property
    def years(self) -> range:
        return range(self.start_year, self.end_year + 1)


def _built_in_profiles() -> dict[str, PipelineProfile]:
    return {
        "ape1_latam": PipelineProfile(
            name="ape1_latam",
            scope="latam_panel",
            countries=LATAM_COUNTRIES,
            start_year=2000,
            end_year=2023,
            allowed_scopes=("global", "latam_panel"),
            default_source="world_bank",
            source_priority=("world_bank", "http_api", "local_file"),
            allow_partial=True,
            description="Panel LATAM APE1 con 20 países y rango estándar.",
            metadata={"task": "APE1", "mode": "panel"},
        ),
        "homicidios_ecuador": PipelineProfile(
            name="homicidios_ecuador",
            scope="ecuador_local",
            countries=("EC",),
            start_year=1990,
            end_year=2023,
            allowed_scopes=("global", "ecuador_local"),
            default_source="world_bank",
            source_priority=("world_bank", "http_api", "local_file"),
            allow_partial=True,
            description="Base raw para homicidios Ecuador con ventana amplia.",
            metadata={"task": "homicidios", "mode": "panel"},
        ),
    }


def _profile_from_mapping(name: str, raw_profile: Mapping[str, Any], fallback: PipelineProfile | None = None) -> PipelineProfile:
    fallback = fallback or PipelineProfile(
        name=name,
        scope="global",
        countries=tuple(),
        start_year=0,
        end_year=0,
    )

    metadata = dict(fallback.metadata)
    raw_metadata = raw_profile.get("metadata") if isinstance(raw_profile, Mapping) else None
    if isinstance(raw_metadata, Mapping):
        metadata.update(raw_metadata)

    profile = PipelineProfile(
        name=name,
        scope=str(raw_profile.get("scope", fallback.scope)),
        countries=_to_tuple(raw_profile.get("countries"), fallback.countries),
        start_year=_to_int(raw_profile.get("start_year"), fallback.start_year),
        end_year=_to_int(raw_profile.get("end_year"), fallback.end_year),
        allowed_scopes=_to_tuple(raw_profile.get("allowed_scopes"), fallback.allowed_scopes),
        default_source=str(raw_profile.get("default_source", fallback.default_source)),
        source_priority=_to_tuple(raw_profile.get("source_priority"), fallback.source_priority),
        allow_partial=_to_bool(raw_profile.get("allow_partial"), fallback.allow_partial),
        description=str(raw_profile.get("description", fallback.description)),
        metadata=metadata,
    )

    if not profile.countries:
        raise ValueError(f"El perfil '{name}' no define países")

    if profile.start_year > profile.end_year:
        raise ValueError(f"El perfil '{name}' tiene un rango temporal inválido")

    return profile


def _merge_profile(base: PipelineProfile, overrides: Mapping[str, Any]) -> PipelineProfile:
    updates: dict[str, Any] = {}

    for key, value in overrides.items():
        if value is None:
            continue
        if key == "countries":
            updates[key] = _to_tuple(value, base.countries)
        elif key in {"allowed_scopes", "source_priority"}:
            updates[key] = _to_tuple(value, getattr(base, key))
        elif key in {"start_year", "end_year"}:
            updates[key] = int(value)
        elif key == "allow_partial":
            updates[key] = _to_bool(value, base.allow_partial)
        elif key == "metadata":
            merged_metadata = dict(base.metadata)
            if isinstance(value, Mapping):
                merged_metadata.update(value)
            updates[key] = merged_metadata
        else:
            updates[key] = value

    merged = replace(base, **updates)
    if not merged.countries:
        raise ValueError(f"El perfil '{merged.name}' quedó sin países luego de aplicar overrides")
    if merged.start_year > merged.end_year:
        raise ValueError(f"El perfil '{merged.name}' quedó con rango temporal inválido luego de aplicar overrides")
    return merged


def _load_config_file(config_path: Path) -> Mapping[str, Any]:
    if tomllib is None or not config_path.exists():
        return {}

    with config_path.open("rb") as handle:
        raw = tomllib.load(handle)

    if isinstance(raw, Mapping):
        return raw

    return {}


def load_pipeline_profile(
    profile_name: str | None = None,
    *,
    config_path: str | Path | None = None,
    **overrides: Any,
) -> PipelineProfile:
    """Carga un perfil declarativo desde TOML o desde perfiles integrados."""

    resolved_name = profile_name or os.getenv("PIPELINE_PROFILE", DEFAULT_PROFILE_NAME)
    resolved_config_path = Path(config_path) if config_path else PIPELINE_CONFIG_FILE

    builtins = _built_in_profiles()
    config_data = _load_config_file(resolved_config_path)
    profiles_data = config_data.get("profiles", {}) if isinstance(config_data, Mapping) else {}

    if resolved_name in profiles_data:
        base_profile = _profile_from_mapping(
            resolved_name,
            profiles_data[resolved_name],
            fallback=builtins.get(resolved_name),
        )
    elif resolved_name in builtins:
        base_profile = builtins[resolved_name]
    else:
        raise KeyError(
            f"Perfil '{resolved_name}' no encontrado en {resolved_config_path} ni en los perfiles integrados"
        )

    if overrides:
        base_profile = _merge_profile(base_profile, overrides)

    return base_profile


def load_pipeline_profile_from_env(
    profile_name: str | None = None,
    *,
    config_path: str | Path | None = None,
) -> PipelineProfile:
    """Carga un perfil y aplica overrides desde variables de entorno."""

    env_overrides: dict[str, Any] = {}

    if "PIPELINE_START_YEAR" in os.environ:
        env_overrides["start_year"] = int(os.environ["PIPELINE_START_YEAR"])
    if "PIPELINE_END_YEAR" in os.environ:
        env_overrides["end_year"] = int(os.environ["PIPELINE_END_YEAR"])
    if "PIPELINE_COUNTRIES" in os.environ:
        env_overrides["countries"] = tuple(
            item.strip().upper()
            for item in os.environ["PIPELINE_COUNTRIES"].split(",")
            if item.strip()
        )
    if "PIPELINE_SCOPE" in os.environ:
        env_overrides["scope"] = os.environ["PIPELINE_SCOPE"].strip()
    if "PIPELINE_ALLOWED_SCOPES" in os.environ:
        env_overrides["allowed_scopes"] = tuple(
            item.strip()
            for item in os.environ["PIPELINE_ALLOWED_SCOPES"].split(",")
            if item.strip()
        )
    if "PIPELINE_DEFAULT_SOURCE" in os.environ:
        env_overrides["default_source"] = os.environ["PIPELINE_DEFAULT_SOURCE"].strip()
    if "PIPELINE_SOURCE_PRIORITY" in os.environ:
        env_overrides["source_priority"] = tuple(
            item.strip()
            for item in os.environ["PIPELINE_SOURCE_PRIORITY"].split(",")
            if item.strip()
        )
    if "PIPELINE_ALLOW_PARTIAL" in os.environ:
        env_overrides["allow_partial"] = _to_bool(os.environ["PIPELINE_ALLOW_PARTIAL"], True)

    return load_pipeline_profile(
        profile_name=profile_name,
        config_path=config_path,
        **env_overrides,
    )