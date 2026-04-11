#!/usr/bin/env bash
set -euo pipefail

# Script helper: crea .venv e intenta sincronizar dependencias con `uv`.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
PY="$VENV_DIR/bin/python"

if [ ! -x "$PY" ]; then
  echo "Creando virtualenv en $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

echo "Actualizando pip en el virtualenv..."
"$PY" -m pip install --upgrade pip setuptools wheel

echo "Intentando instalar cliente 'uv' (si está disponible vía pip)..."
"$PY" -m pip install uv || true

if command -v uv >/dev/null 2>&1; then
  echo "Ejecutando 'uv' para sincronizar dependencias usando uv.lock..."
  uv sync --lock uv.lock || echo "uv sync falló: revisa la documentación de uv o ejecuta uv install"
else
  echo "Comando 'uv' no encontrado. Usa el fallback con pip:"
  echo "  $PY -m pip install -r requirements.txt"
fi

echo "Bootstrap completo."
