# Changelog - APE1 Auditoría Forense

## [0.4.0] - 2026-04-17
### Added
- **Desacoplamiento de Catálogos**: Transición total de metadatos de variables de `src/lib/catalog.py` a archivos declarativos `config/catalog_*.toml`.
- **Carga Dinámica**: Función `load_catalog(name)` para inyectar diccionarios de variables en tiempo de ejecución.
- **Smart Pathing**: Resolución de rutas en cascada en `source_backends.py` que simplifica la declaración de fuentes locales (solo requiere el nombre del archivo).
- **Catálogo APE1**: Migración del catálogo base de América Latina a TOML.

### Changed
- Refactorización de `Task_Final_Consolidado_Equipo.py` para usar el nuevo sistema dinámico.
- Simplificación de `catalog_equipo.toml` eliminando rutas relativas complejas.

## [0.5.0] - 2026-04-18
### Added
- **Orquestación Maestra**: Implementación de `src/orchestration/ape1_master_build.py` para ejecución unificada de fases.
- **Backends Especializados (Ecuador)**: Integración de scrapers para BCE e INEC en `src/scrapers/`.
- **Generalización de DataDoctor**: Soporte para cualquier identificador de entidad (censo, cantón, parroquia) mediante la propiedad `entity_column`.
- **Registro Dinámico**: Los nuevos scrapers se registran automáticamente en el `SourceBackendRegistry`.
- **Estandarización de Nomenclatura**: Migración de todos los orquestadores de tareas al formato estándar `[Tarea]-[Unidad]-[Tipo]-[Tema].py`.
- **Master Build Dinámico**: Implementación de `importlib` en el orquestador maestro para soportar nombres de archivos con guiones.
- Manejo de dependencias profesional con `uv`.

### Changed
- Reorganización total del repositorio en capas (`src`, `data`, `docs`, `logs`).
- Migración de scripts monolíticos a una arquitectura de orquestación.
- Corrección de rutas hardcodeadas para permitir ejecución en cualquier entorno.
- Actualización de los perfiles de pipeline para soportar la nueva estructura de ingesta.

### Fixed
- **Ghost Components**: Restauración de archivos y directorios reportados pero no existentes en disco.
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
