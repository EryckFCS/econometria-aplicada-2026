# Changelog - APE1 Auditoría Forense

## [Unreleased]
### Added
- Nuevo sistema de orquestación maestro (`src/orchestration/ape1_master_build.py`).
- Integración de scrapers locales de alta fidelidad (`src/scrapers/`):
    - `bce_scraper.py`: Datos del Banco Central del Ecuador.
    - `inec_scraper.py`: Datos del Instituto Nacional de Estadística y Censos.
- Generación de producto final unificado en Excel (`data/exports/APE1_Auditoria_Forense_MASTER.xlsx`).
- Manejo de dependencias profesional con `uv`.

### Changed
- Reorganización total del repositorio en capas (`src`, `data`, `docs`, `logs`).
- Migración de scripts monolíticos a una arquitectura de orquestación.
- Corrección de rutas hardcodeadas para permitir ejecución en cualquier entorno.

### Fixed
- Error de importación de `Path` en `src/processing/ape1_auditoria_artefactos.py`.
- Errores de persistencia de datos donde los archivos intermedios no se guardaban antes de la auditoría.
- Dependencia faltante `tenacity` instalada para resiliencia en red.

## [0.1.0] - 2026-04-12
### Added
- Scripts base de scraping para el Banco Mundial.
- Lógica de generación de 8 artefactos de auditoría.
- Estructura inicial de utilidades en `core/`.

## [PLANIFICACIÓN SEMESTRAL]
### Unidad 1: Fundamentos y Auditoría Forense (En curso)
- [x] Reorganización de repositorio.
- [x] Automatización de Panel Forense APE1.
- [ ] Validación de cumplimiento normativo.

### Unidad 2: Modelado Avanzado y Heterocedasticidad (Próximamente)
- [ ] Implementación de modelos lineales avanzados.
- [ ] Pruebas de robustez.

### Unidad 3: Series de Tiempo y Datos de Panel (Próximamente)
- [ ] Análisis dinámico.
- [ ] Artefacto de predicción econométrica.
