# Migración a `uv` — guía rápida

Este repositorio contiene una migración inicial de `pip` (`requirements.txt`) al gestor `uv`.

Archivos añadidos:

- `uv.toml` — manifiesto de dependencias (semver/>= como en `requirements.txt`).
- `uv.lock` — lock con versiones fijadas extraídas del `.venv` actual.
- `scripts/uv_bootstrap.sh` — script auxiliar para crear `.venv` e intentar sincronizar con `uv`.

Pasos recomendados para usar `uv` (adaptar según la documentación de tu instalador `uv`):

1. Crear/activar el virtualenv (este repo usa `.venv`):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

1. Instalar la herramienta `uv` (consulta la doc oficial de `uv`). Si está disponible vía `pip`:

```bash
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install uv
```

1. Instalar dependencias con `uv` (comando ejemplo — adapta según `uv`):

```bash
uv sync --lock uv.lock   # o `uv install` según la CLI de uv
```

1. Fallback con pip (si no hay `uv` disponible todavía):

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Notas:

- El `uv.lock` contiene solo las dependencias listadas en `uv.toml` con versiones fijas; si `uv` gestiona resolución transitiva y hashes, se recomienda regenerar el lock con la CLI de `uv` una vez instalada.
- No se ha modificado código para depender de `uv`; este cambio es estrictamente de gestión de dependencias. Actualizar CI y scripts si quieres que CI use `uv` en lugar de `pip`.
