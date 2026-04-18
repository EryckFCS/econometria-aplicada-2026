"""
Constants for the Econometric Research Center (CIE).
This module serves as the Single Source of Truth for geographic mappings and scientific parameters.
"""

# Mapeo de códigos ISO3 a ISO2 para consistencia en la ingesta
ISO3_TO_ISO2 = {
    "ARG": "AR", "BOL": "BO", "BRA": "BR", "CHL": "CL", "COL": "CO", "CRI": "CR", "CUB": "CU",
    "ECU": "EC", "SLV": "SV", "GTM": "GT", "HTI": "HT", "HND": "HN", "MEX": "MX", "NIC": "NI",
    "PAN": "PA", "PRY": "PY", "PER": "PE", "DOM": "DO", "URY": "UY", "VEN": "VE",
}

# Mapeo de nombres comunes a códigos ISO2
NAME_TO_ISO2 = {
    "Argentina": "AR", "Bolivia": "BO", "Brasil": "BR", "Brazil": "BR", "Chile": "CL", "Colombia": "CO",
    "Costa Rica": "CR", "Cuba": "CU", "Ecuador": "EC", "El Salvador": "SV", "Guatemala": "GT",
    "Haití": "HT", "Haiti": "HT", "Honduras": "HN", "México": "MX", "Mexico": "MX",
    "Nicaragua": "NI", "Panamá": "PA", "Panama": "PA", "Paraguay": "PY", "Perú": "PE", "Peru": "PE",
    "República Dominicana": "DO", "Dominican Republic": "DO", "Uruguay": "UY", "Venezuela": "VE",
}

# Lista oficial de países de América Latina seleccionados para el estudio
# (LATAM-20: Basado en CEPAL/UNESCO)
PAISES_LATAM = {
    "AR": "Argentina",
    "BO": "Bolivia",
    "BR": "Brasil",
    "CL": "Chile",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "CU": "Cuba",
    "DO": "República Dominicana",
    "EC": "Ecuador",
    "GT": "Guatemala",
    "HN": "Honduras",
    "HT": "Haití",
    "MX": "México",
    "NI": "Nicaragua",
    "PA": "Panamá",
    "PE": "Perú",
    "PY": "Paraguay",
    "SV": "El Salvador",
    "UY": "Uruguay",
    "VE": "Venezuela",
}

PAISES_LATAM_ISO2 = list(PAISES_LATAM.keys())
