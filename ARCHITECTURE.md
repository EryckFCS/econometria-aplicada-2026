# Arquitectura del Ecosistema de Econometría Aplicada

Este documento define la estructura técnica del repositorio, diseñada para soportar tanto tareas académicas (ACD, AA, APE) como proyectos de investigación de largo plazo (Tesis de Titulación).

## 🏛️ Capas del Sistema

### 1. Librerías de Lógica (`src/lib/`)
Contiene el código reusable que NO debe cambiar entre tareas. Estas son las piezas del motor:
- **`loaders/`**: Ingesta de datos vía API o Scrapers (ej. `WorldBankLoader`).
- **`processors/`**: Transformación de datos crudos a estructuras econométricas (`PanelBuilder`, `TimeSeriesBuilder`).
- **`exporters/`**: Formateo de salidas profesionales (`AcademicExcelExporter`).
- **`catalog.py`**: El "Diccionario de Datos Maestro" con validación automática (CI).
- **`bibliography.py`**: Motor de gobernanza bibliográfica (Citas APA).

### 2. Tareas de Orquestación (`src/tasks/`)
Scripts livianos que usan las librerías para ejecutar un flujo específico. Se organizan por unidad académica o por proyecto de investigación:
- **Nomenclatura**: `Task_[Tema]_[Unidad].py` (Ej. `Task_Panel_Ambiental_Latam.py`).
- **Regla Oro**: Un orquestador NO debe contener lógica de limpieza o descarga; solo llama a `lib`.

### 3. Evidencias y Metadatos (`data/` y `docs/manuals/`)
Estructura de almacenamiento segregada:
- `/data/raw/csv/`: Para consumo de Stata.
- `/data/raw/excel/`: Para revisión humana/docente.
- `/docs/manuals/`: Repositorio de manuales metodológicos (Auditoría Forense).

## 🚀 Convergencia con Proyecto de Titulación

El sistema no solo resuelve tareas de clase; es el **motor de tu tesis**:
1. **Pipeline de Datos**: La descarga y limpieza de datos de informalidad (ENEMDU) está automatizada en los Loaders.
2. **Registro de Variables**: Al usar el `catalog.py`, aseguras que tu tesis use siempre la misma definición técnica que los manuales del INEC.
3. **Generación Documental**: El objetivo final es el **Paper Engine**, que tomará tus resultados de Stata y los llevará directamente a un borrador de investigación digno de publicación.

---
*Mantenimiento: El sistema se valida con `pytest tests/test_catalog.py`.*
