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
from .utils import create_session, fetch_wb, normalize_iso2
from .exceptions import RegistryOverwriteDataError

BackendFn = Callable[[Mapping[str, Any], str, int, int], tuple[pd.DataFrame, dict[str, Any]]]


class SourceBackendRegistry:
    """
    Registro unificado de backends del CIE.
    
    Administra los '3 Pilares Canónicos' (world_bank, http_api, local_file)
    y gestiona alias para retrocompatibilidad.
    """

    _backends: dict[str, BackendFn] = {}
    _canonical_names: set[str] = set()

    @classmethod
    def register(cls, name: str, *aliases: str) -> Callable[[BackendFn], BackendFn]:
        def decorator(func: BackendFn) -> BackendFn:
            if name in cls._backends:
                raise RegistryOverwriteDataError(f"El backend '{name}' ya está registrado.")
            cls._backends[name] = func
            cls._canonical_names.add(name)
            for alias in aliases:
                if alias in cls._backends:
                    raise RegistryOverwriteDataError(f"El alias '{alias}' ya está registrado.")
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

        if source_kind not in cls._canonical_names:
            import logging
            # Buscar el nombre canónico correspondiente (el que apunta a la misma función)
            canonical = "desconocido"
            for name, func in cls._backends.items():
                if func == backend and name in cls._canonical_names:
                    canonical = name
                    break
            
            logging.getLogger(__name__).warning(
                "⚠️ Backend deprecado: '%s' es un alias. Usa el nombre canónico '%s' en tus configuraciones.",
                source_kind, canonical
            )

        return backend(variable, countries_str, start_year, end_year)


def _split_countries(countries_str: str) -> set[str]:
    return {item.strip().upper() for item in countries_str.split(";") if item.strip()}


def _resolve_source_path(source_ref: str | Path) -> Path:
    source_path = Path(source_ref)
    if source_path.is_absolute():
        return source_path
        
    candidates = [
        PROJECT_ROOT / source_path,
        PROJECT_ROOT / "data" / "curation" / "group_work" / "standardized" / source_path,
        PROJECT_ROOT / "data" / "raw" / "csv" / source_path,
    ]
    found_candidates = []
    for candidate in candidates:
        if candidate.exists():
            found_candidates.append(candidate)
    
    if len(found_candidates) > 1:
        import logging
        logging.getLogger(__name__).warning(
            "⚠️ Ambigüedad en ruta: se encontraron %d archivos para '%s'. Usando: %s",
            len(found_candidates), source_ref, found_candidates[0]
        )
    
    if found_candidates:
        return found_candidates[0]
            
    return PROJECT_ROOT / source_path


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

    # Uso del motor de normalización centralizado
    normalized["iso2"] = normalized["country_raw"].apply(normalize_iso2)

    normalized["year"] = pd.to_numeric(normalized["year"], errors="coerce")
    normalized = normalized.dropna(subset=["iso2", "year"])
    normalized["year"] = normalized["year"].astype(int)
    normalized["iso2"] = normalized["iso2"].astype(str).str.upper()
    return normalized[["iso2", "year", "value"]]


@SourceBackendRegistry.register("world_bank")
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


@SourceBackendRegistry.register("http_api")
def fetch_http_api(
    variable: Mapping[str, Any],
    countries_str: str,
    start_year: int,
    end_year: int,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    source_ref = variable.get("url") or variable.get("endpoint") or variable.get("source_ref")
    if not source_ref:
        raise ValueError(
            f"La variable '{variable.get('nombre_raw', 'SIN_NOMBRE')}' requiere 'url' o 'endpoint' para usar el backend http_api"
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
        "http_api",
        str(response.url),
        extra_meta={
            "http_method": method,
            "http_status_code": int(response.status_code),
            "http_content_type": str(response.headers.get("content-type", "")),
        },
    )
    return filtered, meta


def _smart_load_dataframe(source_path: Path, variable: Mapping[str, Any]) -> pd.DataFrame:
    """Implementa una escalera de detección inteligente por contenido y extensión."""
    import logging
    logger = logging.getLogger(__name__)
    
    # 1. Intentar por extensión (Vía rápida)
    ext = source_path.suffix.lower()
    try:
        if ext == ".csv":
            logger.info("Detección rápida: cargando '%s' como CSV", source_path.name)
            return pd.read_csv(source_path, compression="infer")
        if ext in {".xlsx", ".xls", ".xlsm"}:
            logger.info("Detección rápida: cargando '%s' como Excel", source_path.name)
            return pd.read_excel(source_path, sheet_name=variable.get("sheet_name", 0))
        if ext == ".parquet":
            logger.info("Detección rápida: cargando '%s' como Parquet", source_path.name)
            return pd.read_parquet(source_path)
    except Exception as e:
        logger.warning("Fallo en detección rápida para '%s': %s. Iniciando modo Inteligente...", source_path.name, e)

    # 2. Escalera de Inferencia (Modo Inteligente)
    # 2.a. ¿Es Parquet? (Detección por buffer)
    try:
        df = pd.read_parquet(source_path)
        logger.info("🎯 Inteligencia: '%s' detectado como Parquet por contenido", source_path.name)
        return df
    except Exception:
        pass

    # 2.b. ¿Es Excel?
    try:
        df = pd.read_excel(source_path, sheet_name=variable.get("sheet_name", 0))
        logger.info("🎯 Inteligencia: '%s' detectado como Excel por contenido", source_path.name)
        return df
    except Exception:
        pass

    # 2.c. ¿Es CSV/Text? (Probando delimitadores comunes)
    for sep in [",", ";", "\t", "|"]:
        try:
            # Cargamos solo 5 líneas para validar estructura base
            df_test = pd.read_csv(source_path, sep=sep, nrows=5, compression="infer")
            # Si tiene más de una columna, asumimos que el separador es correcto
            if len(df_test.columns) > 1:
                df = pd.read_csv(source_path, sep=sep, compression="infer")
                logger.info("🎯 Inteligencia: '%s' detectado como CSV (separador='%s')", source_path.name, sep)
                return df
        except Exception:
            continue

    # 3. Último recurso: CSV plano
    try:
        logger.info("🚀 Último recurso: cargando '%s' como CSV plano", source_path.name)
        return pd.read_csv(source_path, compression="infer")
    except Exception as e:
        raise ValueError(f"Fallo total en la carga inteligente del archivo '{source_path.name}': {e}")


@SourceBackendRegistry.register("local_file")
def fetch_local_file(
    variable: Mapping[str, Any],
    countries_str: str,
    start_year: int,
    end_year: int,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Cargador unificado de archivos locales con Súper-Inteligencia (Smart Loading).
    
    Infiere automáticamente el formato (Parquet > Excel > CSV/TSV) y 
    resuelve rutas relativas mediante el Smart Pathing Cascade.
    """
    source_ref = variable.get("source_ref") or variable.get("source_path")
    if not source_ref:
        raise ValueError(
            f"La variable '{variable.get('nombre_raw', 'SIN_NOMBRE')}' requiere 'source_ref' para cargador local"
        )

    source_path = _resolve_source_path(source_ref)
    if not source_path.exists():
        raise FileNotFoundError(f"No existe la fuente local: {source_path}")

    frame = _smart_load_dataframe(source_path, variable)
    
    if isinstance(frame, dict):
        frame = next(iter(frame.values()))

    return _finalize_frame(frame, variable, countries_str, start_year, end_year, "local_file", str(source_path))


# --- REGISTRO DE SCRAPERS ESPECIALIZADOS (Ecuador) ---
try:
    from scrapers import bce_scraper, inec_scraper  # noqa: F401
except ImportError:
    # Soporte para imports relativos según el contexto de ejecución
    try:
        from ..scrapers import bce_scraper, inec_scraper  # noqa: F401
    except ImportError:
        pass