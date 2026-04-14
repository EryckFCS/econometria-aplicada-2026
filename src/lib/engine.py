import pandas as pd
import numpy as np
import logging
from itertools import product
from typing import Any, Dict, List, Mapping, Tuple

from core.pipeline_config import PipelineProfile, load_pipeline_profile
from core.source_backends import SourceBackendRegistry

logger = logging.getLogger(__name__)


def _as_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return tuple()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def _unique(sequence: List[str]) -> list[str]:
    unique_items: list[str] = []
    for item in sequence:
        if item and item not in unique_items:
            unique_items.append(item)
    return unique_items

class WECPanelEngine:
    """
    Motor unificado para la descarga de datos del World Bank y construcción de paneles balanceados.
    Diseñado bajo principios de simplicidad radical (KISS).
    """
    def __init__(self, countries: List[str], start_year: int, end_year: int, countries_dict: Dict[str, str] = None):
        self.countries = countries
        self.countries_str = ";".join(countries)
        self.start_year = start_year
        self.end_year = end_year
        self.countries_dict = countries_dict or {c: c for c in countries}

    def _resolve_profile(self, profile: PipelineProfile | str | None) -> PipelineProfile:
        if profile is None:
            return PipelineProfile(
                name="runtime",
                scope="global",
                countries=tuple(self.countries),
                start_year=self.start_year,
                end_year=self.end_year,
                allowed_scopes=tuple(),
                default_source="world_bank",
                source_priority=("world_bank",),
                allow_partial=True,
                description="Perfil temporal de ejecución sin archivo de configuración.",
                metadata={},
            )

        if isinstance(profile, str):
            return load_pipeline_profile(profile)

        return profile

    def _variable_scope(self, variable: Mapping[str, Any]) -> tuple[str, ...]:
        raw_scope = variable.get("scope") or variable.get("scopes") or variable.get("scope_tags")
        return _as_tuple(raw_scope)

    def _backend_chain(self, variable: Mapping[str, Any], profile: PipelineProfile) -> list[str]:
        chain = [
            str(variable.get("source_kind") or "").strip(),
            str(variable.get("source") or "").strip(),
            profile.default_source,
        ]

        chain.extend(_as_tuple(variable.get("fallback_source_kinds")))
        chain.extend(profile.source_priority)

        return _unique([candidate for candidate in chain if candidate])

    def _variable_window(
        self,
        variable: Mapping[str, Any],
        profile: PipelineProfile,
    ) -> tuple[int, int]:
        variable_start = variable.get("start_year", variable.get("min_year", profile.start_year))
        variable_end = variable.get("end_year", variable.get("max_year", profile.end_year))
        effective_start = max(profile.start_year, int(variable_start))
        effective_end = min(profile.end_year, int(variable_end))
        return effective_start, effective_end

    def build_panel(
        self,
        series_catalog: List[Dict],
        profile: PipelineProfile | str | None = None,
    ) -> Tuple[pd.DataFrame, List[Dict]]:
        """Construye un panel balanceado con múltiples variables descargadas de fuentes configurables."""

        resolved_profile = self._resolve_profile(profile)
        countries = list(resolved_profile.countries or self.countries)
        countries_dict = self.countries_dict or {c: c for c in countries}
        countries_str = ";".join(countries)

        print(
            f"🏗️ Construyendo panel para {len(countries)} países ({resolved_profile.start_year}-{resolved_profile.end_year})"
        )
        
        # 1. Crear esqueleto balanceado
        years = range(resolved_profile.start_year, resolved_profile.end_year + 1)
        base = pd.DataFrame(
            list(product(countries, years)),
            columns=["iso2", "year"]
        )
        base["pais"] = base["iso2"].map(countries_dict)
        base = base[["iso2", "pais", "year"]]

        manifest = []
        
        # 2. Descargar e inyectar cada variable
        for series in series_catalog:
            variable = dict(series)
            name = variable["nombre_raw"]
            variable_scope = self._variable_scope(variable)

            if resolved_profile.allowed_scopes and variable_scope:
                if not set(variable_scope).intersection(set(resolved_profile.allowed_scopes)):
                    logger.info("Omitiendo %s por alcance %s", name, ",".join(variable_scope))
                    base[name] = np.nan
                    manifest.append(
                        {
                            "variable_local": name,
                            "status": "skipped_scope",
                            "profile_name": resolved_profile.name,
                            "profile_scope": resolved_profile.scope,
                            "variable_scope": list(variable_scope),
                            "requested_start_year": resolved_profile.start_year,
                            "requested_end_year": resolved_profile.end_year,
                            "effective_start_year": None,
                            "effective_end_year": None,
                            "source_candidates": [],
                        }
                    )
                    continue

            effective_start, effective_end = self._variable_window(variable, resolved_profile)
            if effective_start > effective_end:
                logger.warning("⚠️ Ventana vacía para %s", name)
                base[name] = np.nan
                manifest.append(
                    {
                        "variable_local": name,
                        "status": "empty_window",
                        "profile_name": resolved_profile.name,
                        "profile_scope": resolved_profile.scope,
                        "variable_scope": list(variable_scope),
                        "requested_start_year": resolved_profile.start_year,
                        "requested_end_year": resolved_profile.end_year,
                        "effective_start_year": effective_start,
                        "effective_end_year": effective_end,
                        "source_candidates": [],
                    }
                )
                continue

            source_candidates = self._backend_chain(variable, resolved_profile)
            print(f"  📥 Descargando: {name} ({effective_start}-{effective_end})")

            df_s = pd.DataFrame()
            selected_meta: dict[str, Any] = {}
            selected_source_kind = ""
            attempts: list[dict[str, Any]] = []

            for source_kind in source_candidates:
                try:
                    df_candidate, meta = SourceBackendRegistry.fetch(
                        source_kind,
                        variable,
                        countries_str,
                        effective_start,
                        effective_end,
                    )
                except KeyError as error:
                    attempts.append({"source_kind": source_kind, "status": "unregistered", "message": str(error)})
                    continue
                except Exception as error:
                    attempts.append({"source_kind": source_kind, "status": "error", "message": str(error)})
                    continue

                valid_rows = int(df_candidate["value"].notna().sum()) if not df_candidate.empty else 0
                attempts.append(
                    {
                        "source_kind": source_kind,
                        "status": "empty" if valid_rows == 0 else "loaded",
                        "rows": int(len(df_candidate)),
                        "valid_rows": valid_rows,
                    }
                )

                if df_candidate.empty or valid_rows == 0:
                    continue

                df_s = df_candidate
                selected_meta = dict(meta)
                selected_source_kind = source_kind
                break

            if df_s.empty:
                logger.warning("⚠️ Sin datos para %s", name)
                base[name] = np.nan
                manifest.append(
                    {
                        "variable_local": name,
                        "status": "unresolved",
                        "profile_name": resolved_profile.name,
                        "profile_scope": resolved_profile.scope,
                        "variable_scope": list(variable_scope),
                        "requested_start_year": resolved_profile.start_year,
                        "requested_end_year": resolved_profile.end_year,
                        "effective_start_year": effective_start,
                        "effective_end_year": effective_end,
                        "source_candidates": source_candidates,
                        "source_attempts": attempts,
                        "institucion": variable.get("institucion", variable.get("fuente", "WB")),
                    }
                )
                continue

            df_s = df_s.rename(columns={"value": name})
            df_s["year"] = df_s["year"].astype(int)
            base = base.merge(df_s[["iso2", "year", name]], on=["iso2", "year"], how="left")

            selected_meta.update(
                {
                    "variable_local": name,
                    "status": "loaded",
                    "profile_name": resolved_profile.name,
                    "profile_scope": resolved_profile.scope,
                    "variable_scope": list(variable_scope),
                    "requested_start_year": resolved_profile.start_year,
                    "requested_end_year": resolved_profile.end_year,
                    "effective_start_year": effective_start,
                    "effective_end_year": effective_end,
                    "source_kind": selected_source_kind,
                    "source_candidates": source_candidates,
                    "source_attempts": attempts,
                    "institucion": variable.get("institucion", variable.get("fuente", "WB")),
                }
            )
            manifest.append(selected_meta)
                
        return base, manifest
