import pandas as pd
from pathlib import Path
from typing import List, Dict

# Catálogo Maestro de Referencias Bibliográficas
# Este módulo centraliza la inteligencia documental para el generador de papers.

BIBLIOGRAPHY_DB = [
    {
        "id": "INEC_ENEMDU_MET",
        "title": "Metodología de la Encuesta Nacional de Empleo, Desempleo y Subempleo (ENEMDU)",
        "author": "INEC",
        "year": 2021,
        "type": "Manual Metodológico",
        "url": "docs/manuals/ecuador/Metodologia_ENEMDU_General.pdf",
        "citation_apa": "INEC. (2021). Metodología de la Encuesta Nacional de Empleo, Desempleo y Subempleo (ENEMDU). Quito, Ecuador.",
        "key_concepts": ["fuerza de trabajo", "sector informal", "subempleo"]
    },
    {
        "id": "WORLD_BANK_WDI",
        "title": "World Development Indicators Database",
        "author": "World Bank",
        "year": 2023,
        "type": "Data Source",
        "url": "https://data.worldbank.org/",
        "citation_apa": "World Bank. (2023). World Development Indicators. Washington, DC.",
        "key_concepts": ["macroeconomic data", "development indicators"]
    }
]

class BibliographyGovernance:
    def __init__(self, db: List[Dict] = BIBLIOGRAPHY_DB):
        self.db = db

    def get_citation(self, bib_id: str) -> str:
        """Retorna la cita APA por ID."""
        for entry in self.db:
            if entry["id"] == bib_id:
                return entry["citation_apa"]
        return "Cita no encontrada."

    def export_bib_table(self, output_path: Path):
        """Exporta la bibliografía a un CSV o Excel para auditoría."""
        df = pd.DataFrame(self.db)
        df.to_csv(output_path, index=False)
