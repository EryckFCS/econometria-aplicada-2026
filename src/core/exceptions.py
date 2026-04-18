"""Excepciones personalizadas para el ecosistema CIE."""

class CIEError(Exception):
    """Clase base para todas las excepciones del CIE."""
    pass

class DataIntegrityError(CIEError):
    """Se lanza cuando se detectan contradicciones en los datos (ej. duplicados incoherentes)."""
    pass

class ScraperError(CIEError):
    """Se lanza cuando falla un scraper especializado."""
    pass

class RegistryOverwriteDataError(CIEError):
    """Se lanza cuando se intenta registrar un backend que ya existe."""
    pass

class ProfileConfigurationError(CIEError):
    """Se lanza cuando hay errores en la configuración de perfiles TOML."""
    pass
