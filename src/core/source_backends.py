"""Registro de backends de datos para pipelines configurables."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import pandas as pd

from .config import PROJECT_ROOT
from .utils import ISO3_TO_ISO2, fetch_wb

BackendFn = Callable[[Mapping[str, Any], str, int, int], tuple[pd.DataFrame, dict[str, Any]]]


class SourceBackendRegistry:
    """Registro simple de backends de ingesta."""

    _backends: dict[str, BackendFn] = {}

    @classmethod
    def register(cls, name: str, *aliases: str) -> Callable[[BackendFn], BackendFn]:
        def decorator(func: BackendFn) -> BackendFn:
            cls._backends[name] = func
            for alias in aliases:
                cls._backends[alias] = func
            return func

        return decorator

    @classmethod
    def available(cls) -> tuple[str, ...]:
        return tuple(sorted(set(cls._backends)))

    @classmethod
    def fetch(
        cls,
        source_kind: str,
        variable: Mapping[str, Any],
        countries_str: str,
        start_year: int,
        end_year: int,
    ) -> tuple[pd.DataFrame, dict[str, Any]]:
        backend = cls._backends.get(source_kind)
        if backend is None:
            raise KeyError(
                f"Backend '{source_kind}' no registrado. Disponibles: {', '.join(cls.available()) or 'ninguno'}"
            )

        return backend(variable, countries_str, start_year, end_year)


def _split_countries(countries_str: str) -> set[str]:
    return {item.strip().upper() for item in countries_str.split(";") if item.strip()}


def _resolve_source_path(source_ref: str | Path) -> Path:
    source_path = Path(source_ref)
    if not source_path.is_absolute():
        source_path = PROJECT_ROOT / source_path
    return source_path


def _standardize_long_frame(frame: pd.DataFrame, variable: Mapping[str, Any]) -> pd.DataFrame:
    country_column = variable.get("country_column")
    year_column = variable.get("year_column", "year")
    value_column = variable.get("value_column") or variable.get("target_column") or variable.get("nombre_raw")

    if country_column is None:
        if "iso2" in frame.columns:
            country_column = "iso2"
        elif "iso3" in frame.columns:
            country_column = "iso3"
        elif "country_code" in frame.columns:
            country_column = "country_code"
        elif "pais" in frame.columns:
            country_column = "pais"
        else:
            raise KeyError("No se encontró columna de país en la fuente local")

    if year_column not in frame.columns:
        raise KeyError(f"No se encontró la columna de año '{year_column}' en la fuente local")

    if value_column in frame.columns:
        selected_value_column = value_column
    elif "value" in frame.columns:
        selected_value_column = "value"
    else:
        candidate_columns = []
        for column in frame.columns:
            if column in {country_column, year_column, "iso2", "iso3", "pais"}:
                continue
            if pd.api.types.is_numeric_dtype(frame[column]):
                candidate_columns.append(column)

        if len(candidate_columns) != 1:
            raise KeyError(
                "No se pudo inferir la columna de valores en la fuente local; especifica 'value_column' o 'target_column'"
            )

        selected_value_column = candidate_columns[0]

    normalized = frame[[country_column, year_column, selected_value_column]].copy()
    normalized = normalized.rename(
        columns={country_column: "country_raw", year_column: "year", selected_value_column: "value"}
    )

    if country_column == "iso3":
        normalized["iso2"] = normalized["country_raw"].astype(str).str.upper().map(
            lambda code: ISO3_TO_ISO2.get(code, code[:2])
        )
    elif country_column == "pais":
        normalized["iso2"] = normalized["country_raw"].astype(str).str.upper().str.slice(0, 2)
    else:
        normalized["iso2"] = normalized["country_raw"].astype(str).str.upper()

    normalized["year"] = pd.to_numeric(normalized["year"], errors="coerce")
    normalized = normalized.dropna(subset=["iso2", "year"])
    normalized["year"] = normalized["year"].astype(int)
    normalized["iso2"] = normalized["iso2"].astype(str).str.upper()
    return normalized[["iso2", "year", "value"]]


@SourceBackendRegistry.register("world_bank", "wb", "worldbank")
def fetch_world_bank(
    variable: Mapping[str, Any],
    countries_str: str,
    start_year: int,
    end_year: int,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    code = variable["codigo_api"]
    frame, meta = fetch_wb(code, countries_str, start_year, end_year)
    meta = dict(meta)
    meta["source_kind"] = "world_bank"
    meta["source_ref"] = code
    return frame, meta


@SourceBackendRegistry.register("local_csv", "csv")
def fetch_local_csv(
    variable: Mapping[str, Any],
    countries_str: str,
    start_year: int,
    end_year: int,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    source_ref = variable.get("source_ref") or variable.get("source_path")
    if not source_ref:
        raise ValueError(
            f"La variable '{variable.get('nombre_raw', 'SIN_NOMBRE')}' requiere 'source_ref' para usar el backend local_csv"
        )

    source_path = _resolve_source_path(source_ref)
    if not source_path.exists():
        raise FileNotFoundError(f"No existe la fuente local: {source_path}")

    frame = pd.read_csv(source_path)
    normalized = _standardize_long_frame(frame, variable)
    allowed_countries = _split_countries(countries_str)
    filtered = normalized[
        normalized["iso2"].isin(allowed_countries)
        & normalized["year"].between(start_year, end_year)
    ].copy()

    meta = {
        "source_kind": "local_csv",
        "source_ref": str(source_path),
        "records_loaded": int(len(normalized)),
        "records_kept": int(len(filtered)),
    }
    return filtered, meta


@SourceBackendRegistry.register("local_parquet", "parquet")
def fetch_local_parquet(
    variable: Mapping[str, Any],
    countries_str: str,
    start_year: int,
    end_year: int,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    source_ref = variable.get("source_ref") or variable.get("source_path")
    if not source_ref:
        raise ValueError(
            f"La variable '{variable.get('nombre_raw', 'SIN_NOMBRE')}' requiere 'source_ref' para usar el backend local_parquet"
        )

    source_path = _resolve_source_path(source_ref)
    if not source_path.exists():
        raise FileNotFoundError(f"No existe la fuente local: {source_path}")

    frame = pd.read_parquet(source_path)
    normalized = _standardize_long_frame(frame, variable)
    allowed_countries = _split_countries(countries_str)
    filtered = normalized[
        normalized["iso2"].isin(allowed_countries)
        & normalized["year"].between(start_year, end_year)
    ].copy()

    meta = {
        "source_kind": "local_parquet",
        "source_ref": str(source_path),
        "records_loaded": int(len(normalized)),
        "records_kept": int(len(filtered)),
    }
    return filtered, meta


@SourceBackendRegistry.register("local_excel", "xlsx", "excel")
def fetch_local_excel(
    variable: Mapping[str, Any],
    countries_str: str,
    start_year: int,
    end_year: int,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    source_ref = variable.get("source_ref") or variable.get("source_path")
    if not source_ref:
        raise ValueError(
            f"La variable '{variable.get('nombre_raw', 'SIN_NOMBRE')}' requiere 'source_ref' para usar el backend local_excel"
        )

    source_path = _resolve_source_path(source_ref)
    if not source_path.exists():
        raise FileNotFoundError(f"No existe la fuente local: {source_path}")

    sheet_name = variable.get("sheet_name", 0)
    frame = pd.read_excel(source_path, sheet_name=sheet_name)
    if isinstance(frame, dict):
        # Si el archivo devuelve múltiples hojas, por defecto tomamos la primera.
        frame = next(iter(frame.values()))

    normalized = _standardize_long_frame(frame, variable)
    allowed_countries = _split_countries(countries_str)
    filtered = normalized[
        normalized["iso2"].isin(allowed_countries)
        & normalized["year"].between(start_year, end_year)
    ].copy()

    meta = {
        "source_kind": "local_excel",
        "source_ref": str(source_path),
        "sheet_name": sheet_name,
        "records_loaded": int(len(normalized)),
        "records_kept": int(len(filtered)),
    }
    return filtered, meta