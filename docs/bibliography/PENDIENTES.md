# PENDIENTES — Bibliografía Econometría Aplicada


---

## Cómo añadir bibliografía

1. Coloca los PDFs en: `docs/bibliography/`
2. Registra la entrada en: `docs/bibliography/bibliography_index.json`
3. Ejecuta: `uv run python scratch/sync_rag_econometria.py` *(crear si no existe, basado en el patrón Gold Standard)*

---


| Archivo | Motivo |
|:---|:---|
| `docs/bibliography/Econometric Analysis of Cross Section and Panel Data 2nd (Wooldridge 2010).pdf` | **Ya existe en el nodo** — solo falta ejecutar la ingesta |

```bash
uv run python -c "
from ecs_quantitative.ingestion.rag import BibliographyRAG, CorpusEntry
rag = BibliographyRAG(collection_name='bibliography', ocr_enabled=False, formula_enabled=False)
entry = CorpusEntry(
    id='wooldridge_panel_2010',
    name='Econometric Analysis of Cross Section and Panel Data (2nd ed.)',
    path='docs/bibliography/Econometric Analysis of Cross Section and Panel Data, 2nd -- Jeffrey M_ Wooldridge -- 2, 2010 -- MIT press -- bbc8445e912c872f90.pdf'
)
stats = rag.index_entry(entry, include_text=True, include_formulas=False)
print(stats)
"
```

---

## Lista de Pendientes

### 🟡 ALTA PRIORIDAD

| Título | Autores | Año | Estado |
|:---|:---|:---:|:---|
| Econometric Analysis of Cross Section and Panel Data (2ª ed.) | Wooldridge, J.M. | 2010 | ⚡ PDF disponible — pendiente ingesta |
| Introductory Econometrics: A Modern Approach | Wooldridge, J.M. | 2020 | Obtener PDF |
| Material adicional del docente (Alvarado Lopez) | Alvarado Lopez, J.R. | 2026 | Solicitar al docente |

---

> Actualiza `docs/bibliography/bibliography_index.json` después de cada ingesta.
> Última revisión: 2026-04-21
