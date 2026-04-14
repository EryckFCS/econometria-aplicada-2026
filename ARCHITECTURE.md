# Arquitectura del Ecosistema de Econometría Aplicada

Este documento define la estructura técnica del repositorio, diseñada para soportar tanto tareas académicas (ACD, AA, APE) como proyectos de investigación de largo plazo (Tesis de Titulación).

## 🏛️ Capas del Sistema

### 1. Configuración y Backends (`src/core/`)

Contiene la configuración transversal y los adaptadores de entrada:

- **`config.py`**: rutas base y directorios de trabajo.
- **`pipeline_config.py`**: perfiles declarativos, rango temporal, alcance y prioridades de fuente.
- **`source_backends.py`**: registro de fuentes intercambiables (`world_bank`, `http`, `local_csv`, `local_parquet`, `local_excel`).
- **`utils.py`**: utilidades compartidas de descarga y parseo.

### 2. Motor Común (`src/lib/`)

Contiene la lógica reusable que sí debe ser estable entre tareas:

- **`engine.py`**: construcción de paneles con filtrado por perfil y fallback de fuentes.
- **`catalog.py`**: diccionario de variables y países por tarea.
- **`exporters.py`**: salida a CSV/Excel con diccionario de variables.
- **`data_doctor.py`**: curación puntual y trazable sobre el dataset final.

### 3. Tareas de Orquestación (`src/tasks/`)

Scripts livianos que usan el motor común para ejecutar un flujo específico. Se organizan por unidad académica o por proyecto de investigación:

- **Nomenclatura**: `Task_[Tema]_[Unidad].py` (Ej. `Task_Panel_Ambiental_Latam.py`).
- **Regla Oro**: Un orquestador no debe contener lógica de backend, filtrado de rango ni selección de fuente; solo resuelve el perfil y llama al motor.

### 4. Perfiles Declarativos (`config/`)

Los perfiles de ejecución se describen en `config/pipeline_profiles.toml` y se pueden ajustar por variables de entorno para cambiar:

- **Rango**: año inicial y final.
- **Alcance**: país, región o dominio local.
- **Fuentes**: prioridad entre World Bank, HTTP genérico y archivos locales.

### 5. Evidencias y Metadatos (`data/` y `docs/manuals/`)

Estructura de almacenamiento segregada:

- `/data/raw/csv/`: Para consumo de Stata.
- `/data/raw/excel/`: Para revisión humana/docente.
- `/docs/manuals/`: Repositorio de manuales metodológicos (Auditoría Forense).

## 🚀 Convergencia con Proyecto de Titulación

El sistema no solo resuelve tareas de clase; también sirve como motor para la tesis:

1. **Pipeline de Datos**: La descarga y limpieza de datos se resuelven desde perfiles y backends, sin acoplar la lógica a una sola API.
2. **Registro de Variables**: El catálogo y el perfil de ejecución mantienen consistencia técnica entre tareas y ventanas temporales.
3. **Generación Documental**: La salida del motor se conserva trazable para llevar resultados a Stata, Excel y documentación metodológica.

---
*Mantenimiento: el sistema se valida con `PYTHONPATH=src uv run pytest -q`.*
