# APE 1: Auditoría Forense y Construcción de Paneles

Este documento detalla la implementación técnica del primer hito del curso (APE1). El objetivo es la construcción de una base raw trazable para el análisis de determinantes de la violencia en América Latina y Ecuador.

## Flujo de Trabajo

El pipeline unificado integra:

1. **Ingesta Inteligente**: Descarga coordinada del Banco Mundial (API) y fuentes locales (BCE/INEC).
2. **Curación Proactiva**: Aplicación de curas documentadas a través del motor `DataDoctor`.
3. **Auditoría Académica**: Generación de matrices de cumplimiento y diccionario de variables.

## Productos Generados (Artefactos APE1)

El flujo de ejecución maestra vigente genera los siguientes archivos en la estructura de datos:

| Archivo | Proposito |
| --- | --- |
| `data/raw/csv/Base_Raw_Ecuador_Homicidios_Long.csv` | Salida principal en CSV para análisis estadístico y compatibilidad con Stata. |
| `data/raw/excel/Base_Raw_Ecuador_Homicidios_Long.xlsx` | Salida principal en Excel con la pestaña `Diccionario`. |
| `data/curation/ecuador_homicidios_manifest.json` | Manifiesto de curación aplicado por `DataDoctor`. |
| `logs/curation_audit.log` | Registro de auditoría de curaciones generado durante la ejecución. |

> Nota: las referencias históricas a `panel_raw.csv` quedaron como compatibilidad legacy en utilidades auxiliares; el flujo Python vigente exporta `Base_Raw_Ecuador_Homicidios_Long.csv/.xlsx`.

## Ejecución del Módulo

Para regenerar los resultados específicos de APE1:

```bash
PYTHONPATH=src .venv/bin/python src/orchestration/M01-U1-APE-Master_Build.py
```

---
*Referencia: Sílabo Unidad 1 - Econometría Aplicada 2026.*
