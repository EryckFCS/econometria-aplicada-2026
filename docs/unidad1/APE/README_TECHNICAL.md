# APE 1: Auditoría Forense y Construcción de Paneles

Este documento detalla la implementación técnica del primer hito del curso (APE1). El objetivo es la construcción de una base raw trazable para el análisis de determinantes de la violencia en América Latina y Ecuador.

## Flujo de Trabajo

El pipeline unificado integra:
1. **Ingesta Inteligente**: Descarga coordinada del Banco Mundial (API) y fuentes locales (BCE/INEC).
2. **Curación Proactiva**: Aplicación de curas documentadas a través del motor `DataDoctor`.
3. **Auditoría Académica**: Generación de matrices de cumplimiento y diccionario de variables.

## Productos Generados (Artefactos APE1)

El flujo de ejecución maestra genera los siguientes archivos en la estructura de datos:

| Archivo | Proposito |
| --- | --- |
| `data/raw/panel_raw.csv` | Panel balanceado listo para procesamiento. |
| `data/raw/manifest_fuentes_raw.csv` | Registro de trazabilidad (URL/Hash) de cada serie. |
| `data/processed/diccionario_variables.csv` | Definiciones, unidades y fuentes de cada variable. |
| `data/exports/APE1_Auditoria_Forense_MASTER.xlsx` | Reporte maestro con formato institucional para revisión. |
| `docs/variables_no_resueltas.md` | Registro de gaps de información para proxies futuras. |

## Ejecución del Módulo

Para regenerar los resultados específicos de APE1:

```bash
PYTHONPATH=src .venv/bin/python src/orchestration/M01-U1-APE-Master_Build.py
```

---
*Referencia: Sílabo Unidad 1 - Econometría Aplicada 2026.*
