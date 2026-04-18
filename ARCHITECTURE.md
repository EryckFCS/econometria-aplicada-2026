# Arquitectura Técnica: CIE - Centro de Investigación Econométrica

Este documento define la infraestructura técnica del repositorio, diseñada bajo estándares de ingeniería de software aplicados a la econometría de alto nivel.

## 🏛️ Capas del Sistema

### 1. Núcleo e Ingesta Inteligente (`src/core/`)

Constituye el corazón del sistema y la Única Fuente de la Verdad:

- **`constants.py`**: Centraliza todos los mapeos geográficos (ISO3, ISO2) y la definición de la región de estudio (LATAM-20). Prohibida su duplicación en otras capas.
- **`source_backends.py`**: Registro de los "3 Pilares" (`world_bank`, `http_api`, `local_file`). Implementa **Smart Loading**, que infiere el formato de archivos locales (Parquet > Excel > CSV/TSV) automáticamente.
- **`utils.py`**: Utilidades robustas de normalización (`normalize_iso2`) y gestión de sesiones con reintentos inteligentes.
- **`config.py`**: Resolución dinámica de rutas del proyecto y directorios de datos.

### 2. Motor de Paneles (`src/lib/`)

Lógica estable y agnóstica al tema de investigación:

- **`engine.py`**: Construcción de paneles econométricos con filtrado por perfil y fallback de fuentes.
- **`data_doctor.py`**: Guardian de la integridad científica. Valida metadatos (ISO2, años) y reporta inconsistencias antes de la fase de estimación.
- **`catalog.py`**: Desacopla la lógica de las variables mediante catálogos TOML.

### 3. Landing Zone de Datos (`data/raw/`)

Organización segregada para garantizar la auditoría forense:

- **`partners/`**: El punto de entrada para contribuciones de socios investigadores (Erick, Abel, Marvin, etc.).
- **`externos/`**: Almacén para fuentes globales como PWT (Penn World Table) o Maddison Project.
- **`standardized/`**: Salida de los scripts de normalización unificada (`_std.csv`).

### 4. Tareas y Orquestación (`src/tasks/`)

Scripts de ejecución siguiendo la nomenclatura institucional `[Tarea]-[Unidad]-[Tipo]-[Tema].py`:

- **`T02-U1-ACD-Consolidado_Equipo.py`**: Proceso canónico de unión de datos de socios con trazabilidad de origen.

---

## 🚀 Verificación de la Calidad (QA)

El sistema garantiza su integridad mediante una suite de pruebas jerárquica:

1. **Contracts**: Validación de cargadores externos (`tests/test_system_contract.py`).
2. **Backends**: Validación de la inteligencia del cargador local (`tests/test_source_backends.py`).
3. **Pipeline**: Validación del flujo completo de configuración (`tests/test_pipeline_config.py`).

*Comando de validación: `PYTHONPATH=src .venv/bin/python -m pytest`.*
