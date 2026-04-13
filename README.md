# Econometria Aplicada 2026

Repositorio de trabajo para la asignatura Econometria Aplicada. Aqui se concentran los materiales del curso, los scripts de construccion de datos, los notebooks de analisis y el flujo de auditoria forense APE1 para construir paneles econometricos con trazabilidad completa.

El proyecto trabaja principalmente con datos de America Latina y, en la parte local, integra fuentes del Banco Central del Ecuador (BCE) y del INEC. La capa `raw` no aplica interpolacion, imputacion ni transformaciones analiticas silenciosas.

## Que contiene

- Material de la asignatura por unidades en `docs/`.
- Scripts de construccion y auditoria en `src/`.
- Notebooks exploratorios en `notebooks/`.
- Entregables y salidas reproducibles en `data/`.
- Scripts Stata en `stata/`.
- Pruebas automatizadas en `tests/`.

## Estructura principal

| Ruta | Proposito |
| --- | --- |
| `data/raw/` | Insumos crudos, manifests y panel base. |
| `data/processed/` | Diccionario de variables, auditorias y propuestas de modelo. |
| `data/exports/` | Productos finales, incluido el Excel maestro. |
| `docs/` | Syllabus, bibliografia y entregables por unidad. |
| `notebooks/` | Cuadernos de analisis y apoyo a la reproduccion. |
| `src/core/` | Utilidades comunes y configuracion de rutas. |
| `src/processing/` | Construccion del panel raw y artefactos de auditoria. |
| `src/orchestration/` | Flujo maestro para reconstruir el producto final. |
| `src/scrapers/` | Scrapers para BCE, INEC, World Bank y otras fuentes. |
| `src/tools/` | Utilidades auxiliares, como busqueda de indicadores. |
| `stata/` | Scripts `.do` para analisis en Stata. |
| `tests/` | Pruebas unitarias y de integracion ligera. |

## Requisitos

- Python 3.12 o superior.
- `uv` para una instalacion reproducible.
- `PYTHONPATH=src` al ejecutar los scripts, porque el repositorio usa un layout `src/` con imports directos.
- `PYTHONPATH=src/core:src` al ejecutar las pruebas, porque `tests/test_fetch.py` usa el shim legado `ape1_utils`.

Si quieres una guia corta para migracion a `uv`, revisa [docs/syllabus/README_UV.md](docs/syllabus/README_UV.md).

## Instalacion

Instalacion recomendada para desarrollo:

```bash
uv sync --extra dev
export PYTHONPATH=src
```

Si prefieres una instalacion minima, puedes usar el archivo `requirements.txt`, pero esa ruta puede no incluir todo el entorno de desarrollo.

## Ejecucion rapida

Generar el panel raw:

```bash
PYTHONPATH=src uv run python src/processing/ape1_auditoria_raw.py
```

Generar los artefactos de auditoria:

```bash
PYTHONPATH=src uv run python src/processing/ape1_auditoria_artefactos.py
```

Recrear el producto final completo:

```bash
PYTHONPATH=src uv run python src/orchestration/ape1_master_build.py
```

Empaquetar una entrega por unidad:

```bash
PYTHONPATH=src uv run python src/orchestration/zip_task.py 1 ACD
```

## Productos generados

El flujo APE1 produce, entre otros, estos archivos:

- `data/raw/panel_raw.csv`
- `data/raw/manifest_fuentes_raw.csv`
- `data/raw/series_catalog.pkl`
- `data/processed/diccionario_variables.csv`
- `data/processed/matriz_cumplimiento_consigna.csv`
- `data/processed/auditoria_redundancia.csv`
- `data/processed/auditoria_integridad.csv`
- `data/processed/propuesta_panel_modelo.csv`
- `data/exports/APE1_Auditoria_Forense_MASTER.xlsx`
- `docs/README_AUDITORIA.md`
- `docs/variables_no_resueltas.md`

## Calidad y pruebas

Ejecutar pruebas:

```bash
PYTHONPATH=src/core:src uv run python -m pytest -q
```

Ejecutar lint:

```bash
PYTHONPATH=src uv run ruff check .
```

La integridad del proyecto tambien se valida en CI con Python 3.12.

## Notas metodologicas

- El panel raw no usa fillna, forward-fill ni interpolacion propia.
- Las variables redundantes se documentan en lugar de eliminarse de forma opaca.
- Las variables sin serie publica directa se marcan como proxies o como no resueltas.
- Los manifests registran la trazabilidad de descarga y ayudan a reproducir los artefactos.

## Material adicional

- [notebooks/README.md](notebooks/README.md)
- `docs/unidad1/`, `docs/unidad2/` y `docs/unidad3/` contienen entregables y apoyos por unidad.
- `src/processing/legacy/` conserva versiones anteriores del flujo para referencia.

## Estado del proyecto

La Unidad 1 concentra el flujo mas completo y el resto del repositorio sirve como base para las siguientes unidades y para la reproducibilidad de los entregables.
