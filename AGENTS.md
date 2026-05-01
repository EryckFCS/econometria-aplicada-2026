# AGENTS.md - Federated Node: Applied Econometrics 2026

> This repository is a **Level 5 Pure Node** in the Federated Architecture v8.0.0.
> It operates under the Constitution centralized in `capital-workstation-libs`.

## Constitucion

```text
/home/erick-fcs/Capital_Workstation/capital-workstation-libs/.github/copilot-instructions.md
```

## 1. Identidad del Nodo y Gobernanza

| Campo | Valor |
| --- | --- |
| **Nodo** | Applied Econometrics 2026 |
| **Status** | Active - Master Blueprint v8.0.0 Migrated |
| **Docente** | Econ. Jose Rafael Alvarado Lopez |
| **Central Library** | `ecs_quantitative` (capital-workstation-libs) |
| **Intelligence Level** | 5 - Intelligent Ecosystem with Controlled Autonomy |
| **Architecture Standard** | Blueprint v8.0.0 (High Fidelity) |
| **Gatekeeper** | `tests/system/test_architecture.py` |
| **RAG** | `global_knowledge` como destino federado; `data/processed/vector_store/` es un artefacto legado de ejecucion y no debe convertirse en otra fuente de verdad |

## 2. Capacidades de Inteligencia (v2.0)

Este nodo esta disenado para producir econometria aplicada reproducible con trazabilidad tecnica completa.

1. Forensic Econometric Audit: valida integridad de series, metadatos, curacion y consistencia temporal antes de cualquier estimacion.
2. Agnostic Ingestion Intelligence: resuelve fuentes `world_bank`, `http_api` y `local_file` con inferencia automatica de formato y respaldo por perfiles.
3. Reproducibilidad Total: conecta limpieza, panelizacion, estimacion y reporteo bajo una sola orquestacion.
4. Quarto Delivery Layer: separa el codigo operativo de la narrativa academica y mantiene la capa de escritura en `writing/`.

## 3. Protocolos Operativos

### 3.1. Contractual QA Protocol

- Invariante: ningun cambio se considera estable si rompe los contratos del sistema o los contratos de datos.
- Accion: ejecutar `PYTHONPATH=src .venv/bin/python -m pytest tests/test_system_contract.py tests/governance/test_data_contracts.py` antes de cerrar cambios de conducta o estructura.
- Falla: si alguno falla, se corrige la causa raiz antes de continuar.

### 3.2. Research Protocol

- Deteccion: la tarea es de investigacion cuando toca ingesta, panelizacion, curacion, estimacion o reporteo.
- Ubicacion: la logica de ejecucion vive en `src/core/`, `src/lib/`, `src/tasks/` y `src/orchestration/`; la evidencia reproducible vive en `docs/evidence/`.
- Registro: cada ejecucion debe dejar logs en `logs/` o en el sub-vault correspondiente de evidencia, sin contaminar la raiz del nodo.

## 4. Arquitectura de Bovedas (Nivel 5)

### 4.1. Estructura Analitica

```text
.
|-- docs/
|   |-- evidence/            # Evidencia reproducible por unidad
|   `-- bibliography/        # Master Knowledge Vault (RAG Origin)
|       |-- manuals/         # Guías de operación y boletines técnicos
|       |-- readings/        # Lecturas críticas y teoría
|       `-- syllabus/        # Marco institucional
|-- writing/                 # Capa de presentacion y reportes Quarto
|-- src/
|   |-- core/                # Ingesta, configuracion y utilidades
|   |-- lib/                 # Motor de paneles, catalogo y data doctor
|   |-- tasks/               # Tareas institucionales de la unidad
|   `-- orchestration/       # Orquestador maestro
|-- tests/                   # Contratos, gobernanza y smoke checks
`-- main.py                  # Entrada principal del nodo
```

### 4.2. Capas Documentales

- `docs/evidence/`: Unidades de análisis con `knowledge_map.json` para trazabilidad de fuentes.
- `docs/bibliography/`: Corazón del RAG; centraliza PDFs y metadatos bibliográficos globales.
- `writing/`: Redacción académica, plantillas y salidas de reporteo.

## 5. Estrategia de Resiliencia

1. Zero Floating Doctrine: no deben flotar scripts analiticos en la raiz; la logica operativa debe quedarse en `src/` o en los sub-vaults de evidencia.
2. Path Integrity: resolver rutas con `pathlib` y la configuracion del proyecto, no con rutas codificadas a mano.
3. Data Lineage: la curacion y normalizacion deben preservar trazabilidad en los catalogos y en los logs de auditoria.
4. Quarto Hygiene: los entregables de escritura no deben mezclarse con la logica del motor ni con los datos crudos.

## 6. Entorno y Mantenimiento

```bash
uv sync
PYTHONPATH=src .venv/bin/python -m pytest tests/test_main.py tests/test_system_contract.py tests/governance/test_data_contracts.py tests/test_vault_architecture.py
uv run python main.py
```

## 7. Regla de Oro

> Si algo que se construye aqui sirve para otras materias, proponlo para la libreria central.
