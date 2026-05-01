# Applied Econometrics 2026

Nodo Level 5 controlado para econometria aplicada. Este repositorio quedo
reestructurado para arrancar con un bootstrap local minimo, contratos de datos
reales y sin lanzar ingesta ni sincronizacion del vector store.

## Estado actual

- `main.py` reporta identidad y disponibilidad basica de memoria mediante
  `src.core.config` y `src.core.brain`.
- `src/core/` contiene la configuracion canonica del nodo.
- `src/orchestration/M01-U1-APE-Master_Build.py` expone un plan declarativo
  de la Unidad 1 sin ejecutar datos.
- `src/tasks/` contiene las tareas T01 a T05 del flujo local.
- `tests/test_vault_architecture.py` valida la estructura de bovedas.
- `data/curation/group_work/standardized/` contiene el data mart real del
  equipo.

## Vaults

- `docs/vaults/U1-Applied-Econometrics/` evidencia por unidad.
- `docs/readings/` reservado como placeholder y mantenido vacio por diseno.
- `docs/syllabus/` syllabus institucional.
- `docs/manuals/` guias operativas.
- `docs/bibliography/` indice bibliografico local y estado RAG legado.
- `writing/` capa de reporteo Quarto.

## QA local

```bash
uv sync
uv run pytest tests/test_main.py tests/test_system_contract.py tests/governance/test_data_contracts.py tests/test_vault_architecture.py
uv run python main.py
uv run python src/orchestration/M01-U1-APE-Master_Build.py
```

No se ejecuta ingesta ni se toca el vector store en esta fase.
