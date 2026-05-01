# Arquitectura Tecnica - Applied Econometrics 2026

Este documento describe la estructura real del nodo despues de la
reestructuracion controlada a Nivel 5.

## 1. Bootstrap local

- `src/core/config.py`: resuelve la raiz del proyecto y las rutas canonicas.
- `src/core/brain.py`: expone el estado basal de memoria con
  `global_knowledge` como coleccion declarativa y `memory=None`.
- `main.py`: publica la identidad del nodo sin ejecutar ingesta.

## 2. Capa analitica

- `src/lib/catalog.py`: carga los catalogos TOML del trabajo de grupo.
- `src/tasks/`: contiene `T01-U1-APE-Homicidios_Ecuador.py`,
  `T02-U1-ACD-Consolidado_Equipo.py`, `T03-U1-AA-Panel_Ambiental_Latam.py`,
  `T04-U1-ACD-SEM_Homicidios.py` y `T05-Report_Engine.py`.
- `src/orchestration/M01-U1-APE-Master_Build.py`: imprime un plan declarativo
  y no dispara procesos de datos.

## 3. Data mart real

- `data/curation/group_work/standardized/`: CSV estandarizados con esquema
  `iso2`, `year` y columnas de variables.
- `tests/governance/test_data_contracts.py`: verifica ese contrato minimo.

## 4. Vaults documentales

- `docs/evidence/U1-Applied-Econometrics/`: evidencia por unidad.
- `docs/readings/`: placeholder vacio reservado para lecturas futuras.
- `docs/syllabus/`: syllabus institucional.
- `docs/manuals/`: guias operativas cortas.
- `docs/bibliography/`: indice bibliografico local y estado RAG legado.
- `writing/`: salida Quarto y reportes.

## 5. QA y gatekeepers

- `tests/test_main.py`: valida la identidad publica del nodo.
- `tests/test_system_contract.py`: valida el catalogo local y la integracion
  con la libreria central.
- `tests/governance/test_data_contracts.py`: valida el data mart estandarizado.
- `tests/test_vault_architecture.py`: valida la estructura de bovedas.

No se ejecuta ingesta ni reindexacion RAG en esta fase.
