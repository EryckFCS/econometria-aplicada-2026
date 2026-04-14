"""Registro de backends de datos para pipelines configurables."""

from __future__ import annotations

import io
import json
import os
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import pandas as pd

from .config import PROJECT_ROOT
from .utils import ISO3_TO_ISO2, create_session, fetch_wb

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


class _SafeFormatDict(dict[str, Any]):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def _format_template_value(value: Any, context: Mapping[str, Any]) -> Any:
    if isinstance(value, str):
        return value.format_map(_SafeFormatDict(context))

    if isinstance(value, Mapping):
        return {key: _format_template_value(item, context) for key, item in value.items()}

    if isinstance(value, list):
        return [_format_template_value(item, context) for item in value]

    if isinstance(value, tuple):
        return tuple(_format_template_value(item, context) for item in value)

    return value


def _build_context(
    variable: Mapping[str, Any],
    countries_str: str,
    start_year: int,
    end_year: int,
) -> dict[str, Any]:
    countries_list = [item for item in countries_str.split(";") if item]
    context: dict[str, Any] = {
        "countries_str": countries_str,
        "countries_csv": ",".join(countries_list),
        "countries_list": countries_list,
        "start_year": start_year,
        "end_year": end_year,
        "start": start_year,
        "end": end_year,
        "year_start": start_year,
        "year_end": end_year,
    }

    token_env = variable.get("auth_token_env")
    if token_env:
        token_value = os.getenv(str(token_env), "")
        if token_value:
            context["auth_token"] = token_value
            context["token"] = token_value

    return context


def _coerce_path(value: Any) -> tuple[str, ...]:
    if value is None:
        return tuple()
    if isinstance(value, str):
        return tuple(part for part in value.replace("/", ".").split(".") if part)
    if isinstance(value, (list, tuple)):
        return tuple(str(part) for part in value)
    return (str(value),)


def _walk_json_path(payload: Any, path: tuple[str, ...]) -> Any:
    current = payload
    for step in path:
        if isinstance(current, Mapping):
            current = current[step]
        elif isinstance(current, list):
            current = current[int(step)]
        else:
            raise KeyError(f"No se pudo recorrer la ruta JSON en '{step}'")
    return current


def _normalize_json_candidate(value: Any) -> Any:
    if isinstance(value, list):
        return value

    if isinstance(value, Mapping):
        for key in ("data", "records", "results", "items", "series", "dataset"):
            candidate = value.get(key)
            if candidate is not None:
                return _normalize_json_candidate(candidate)
        return value

    return value


def _json_payload_to_frame(payload: Any, variable: Mapping[str, Any]) -> pd.DataFrame:
    records_path = variable.get("records_path") or variable.get("record_path") or variable.get("json_path")
    if records_path:
        payload = _walk_json_path(payload, _coerce_path(records_path))

    payload = _normalize_json_candidate(payload)

    if isinstance(payload, pd.DataFrame):
        return payload

    if isinstance(payload, list):
        if not payload:
            return pd.DataFrame()
        if all(isinstance(item, Mapping) for item in payload):
            return pd.json_normalize(payload)
        return pd.DataFrame({"value": payload})

    if isinstance(payload, Mapping):
        return pd.json_normalize(payload)

    return pd.DataFrame({"value": [payload]})


def _infer_http_format(response: Any, variable: Mapping[str, Any]) -> str:
    explicit = str(variable.get("response_format") or variable.get("format") or "").strip().lower()
    if explicit:
        return explicit

    content_type = str(response.headers.get("content-type", "")).lower()
    if "json" in content_type:
        return "json"
    if "csv" in content_type or "text/csv" in content_type:
        return "csv"
    if "tab-separated" in content_type or "tsv" in content_type:
        return "tsv"
    if "excel" in content_type or "spreadsheet" in content_type or "sheet" in content_type:
        return "excel"

    return "json"


def _frame_from_http_response(response: Any, variable: Mapping[str, Any]) -> pd.DataFrame:
    response_format = _infer_http_format(response, variable)

    if response_format == "json":
        try:
            payload = response.json()
        except Exception:
            payload = json.loads(response.text)
        return _json_payload_to_frame(payload, variable)

    if response_format in {"csv", "tsv", "txt"}:
        separator = variable.get("separator") or variable.get("sep") or ("\t" if response_format == "tsv" else ",")
        return pd.read_csv(io.StringIO(response.text), sep=separator)

    if response_format in {"excel", "xlsx", "xls"}:
        sheet_name = variable.get("sheet_name", 0)
        frame = pd.read_excel(io.BytesIO(response.content), sheet_name=sheet_name)
        if isinstance(frame, dict):
            frame = next(iter(frame.values()))
        return frame

    if response_format == "parquet":
        return pd.read_parquet(io.BytesIO(response.content))

    raise ValueError(f"Formato HTTP no soportado: {response_format}")


def _finalize_frame(
    frame: pd.DataFrame,
    variable: Mapping[str, Any],
    countries_str: str,
    start_year: int,
    end_year: int,
    source_kind: str,
    source_ref: str,
    extra_meta: Mapping[str, Any] | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    normalized = _standardize_long_frame(frame, variable)
    allowed_countries = _split_countries(countries_str)
    filtered = normalized[
        normalized["iso2"].isin(allowed_countries)
        & normalized["year"].between(start_year, end_year)
    ].copy()

    meta: dict[str, Any] = {
        "source_kind": source_kind,
        "source_ref": str(source_ref),
        "records_loaded": int(len(normalized)),
        "records_kept": int(len(filtered)),
    }
    if extra_meta:
        meta.update(dict(extra_meta))

    return filtered, meta


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


@SourceBackendRegistry.register("http", "http_json", "api", "rest")
def fetch_http_api(
    variable: Mapping[str, Any],
    countries_str: str,
    start_year: int,
    end_year: int,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    source_ref = variable.get("url") or variable.get("endpoint") or variable.get("source_ref")
    if not source_ref:
        raise ValueError(
            f"La variable '{variable.get('nombre_raw', 'SIN_NOMBRE')}' requiere 'url' o 'endpoint' para usar el backend http"
        )

    context = _build_context(variable, countries_str, start_year, end_year)
    url = _format_template_value(source_ref, context)
    method = str(variable.get("http_method", "GET")).upper()
    headers = _format_template_value(variable.get("headers", {}), context)
    params = _format_template_value(variable.get("params") or variable.get("query_params", {}), context)
    timeout = float(variable.get("timeout", 30))
    verify = variable.get("verify", True)

    session = create_session()
    response = session.request(method, url, headers=headers, params=params, timeout=timeout, verify=verify)
    response.raise_for_status()

    frame = _frame_from_http_response(response, variable)
    filtered, meta = _finalize_frame(
        frame,
        variable,
        countries_str,
        start_year,
        end_year,
        "http",
        str(response.url),
        extra_meta={
            "http_method": method,
            "http_status_code": int(response.status_code),
            "http_content_type": str(response.headers.get("content-type", "")),
        },
    )
    return filtered, meta


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
    return _finalize_frame(frame, variable, countries_str, start_year, end_year, "local_csv", str(source_path))


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
    return _finalize_frame(frame, variable, countries_str, start_year, end_year, "local_parquet", str(source_path))


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

    return _finalize_frame(
        frame,
        variable,
        countries_str,
        start_year,
        end_year,
        "local_excel",
        str(source_path),
        extra_meta={"sheet_name": sheet_name},
    )