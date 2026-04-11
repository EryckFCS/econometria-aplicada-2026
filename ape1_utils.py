"""Compat shim: re-exportar utilidades desde `core.utils`.

Mantener `from ape1_utils import fetch_wb` compatible con scripts y tests existentes.
"""

from core.utils import create_session, fetch_wb

__all__ = ["create_session", "fetch_wb"]
