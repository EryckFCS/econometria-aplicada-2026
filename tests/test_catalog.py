import pytest
from lib.catalog import SERIES_APE1

def test_catalog_structure():
    """Valida que cada entrada en el catálogo tenga los campos mínimos requeridos."""
    required_keys = ["nombre_raw", "codigo_api", "unidad_api", "rol", "concepto"]
    
    for entry in SERIES_APE1:
        for key in required_keys:
            assert key in entry, f"Error: Al indicador '{entry.get('nombre_raw', 'SIN_NOMBRE')}' le falta el campo '{key}'."
            assert entry[key] is not None, f"Error: El campo '{key}' en '{entry['nombre_raw']}' está vacío."
            assert isinstance(entry[key], str), f"Error: El campo '{key}' en '{entry['nombre_raw']}' debe ser string."

def test_no_duplicate_names():
    """Valida que no existan nombres raw duplicados en el catálogo."""
    names = [e["nombre_raw"] for e in SERIES_APE1]
    duplicates = [n for n in names if names.count(n) > 1]
    assert not duplicates, f"Error: Nombres duplicados en catálogo: {set(duplicates)}"

def test_no_duplicate_api_codes():
    """Valida que no existan códigos API duplicados."""
    codes = [e["codigo_api"] for e in SERIES_APE1]
    duplicates = [c for c in codes if codes.count(c) > 1]
    assert not duplicates, f"Error: Códigos API duplicados: {set(duplicates)}"
