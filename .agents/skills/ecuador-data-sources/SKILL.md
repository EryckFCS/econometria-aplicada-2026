---
name: ecuador-data-sources
description: Integración, consumo de APIs y extracción de microdatos desde entidades oficiales de Ecuador (BCE, INEC, SRI, SBS) para investigación cuantitativa y de riesgo.
version: 1.0.0
---

# SKILL: Integración de Fuentes de Datos de Ecuador

Esta habilidad detalla los procedimientos técnicos, endpoints y transformaciones específicas que el agente debe seguir para consultar datos económicos, financieros e impositivos oficiales de Ecuador.

---

## 1. Mapeo Metodológico de Fuentes

| Entidad | Tipología de Datos | Frecuencia | Formato Común | Casos de Uso |
|:---|:---|:---|:---|:---|
| **BCE** (Banco Central) | Tasas de Interés Referenciales, Balanza de Pagos, Cuentas Nacionales, PIB | Mensual / Trimestral | Excel (.xlsx), APIs | Modelado Macroeconómico y series temporales de tasas pasivas/activas. |
| **INEC** (Estadísticas) | ENEMDU (Empleo y Pobreza), IPC (Inflación), Directorio de Empresas | Mensual / Anual / Trimestral | Microdatos (.csv, .sav, .dta) | Modelos econométricos bivariados, Probit de informalidad laboral y elasticidad precio. |
| **SRI** (Rentas Internas) | Catastro de Contribuyentes, Coeficientes de Impuestos, Recaudación | Mensual / Anual | CSV, JSON | Enriquecimiento de scorecards de crédito y perfiles de ingresos corporativos. |
| **SBS** (Superbancos) | Boletines Financieros, Balance de Pérdidas y Ganancias, Tasa de Morosidad | Mensual | Excel / CSV | Modelado de carteras de crédito y provisiones Basilea III. |

---

## 2. Ingesta y Parseo de Microdatos ENEMDU (INEC)

Los microdatos de la ENEMDU son publicados comúnmente en formato SPSS (`.sav`) o Stata (`.dta`). Su ingesta robusta requiere de `pandas` y `pyreadstat` o `polars` para procesamiento masivo de memoria eficiente.

```python
import pathlib
import pandas as pd
from loguru import logger

def ingest_enemdu_microdata(file_path: pathlib.Path) -> pd.DataFrame:
    """
    Lee archivos de microdatos ENEMDU (.sav o .dta) preservando metadatos 
    de etiquetas de variables para interpretación del modelo.
    """
    logger.info(f"Iniciando ingesta de ENEMDU desde: {file_path}")
    
    suffix = file_path.suffix.lower()
    if suffix == ".sav":
        import pyreadstat
        # Ingesta robusta conservando metadatos
        df, meta = pyreadstat.read_sav(str(file_path))
        logger.success(f"Ingestados {len(df)} registros. Variables encontradas: {len(meta.column_names)}")
    elif suffix == ".dta":
        import pyreadstat
        df, meta = pyreadstat.read_dta(str(file_path))
        logger.success(f"Ingestados {len(df)} registros.")
    elif suffix == ".csv":
        df = pd.read_csv(file_path, low_memory=False)
        logger.warning("Ingestado como CSV plano. Sin etiquetas de metadatos de categoría.")
    else:
        raise ValueError(f"Extensión no soportada para ENEMDU: {suffix}")
        
    # Renombrar columnas clave según metodología estándar de CEPAL/INEC
    # p03: Edad, p41: Ingreso laboral, empleo: cond. de actividad
    column_mappings = {
        "p03": "edad",
        "p41": "ingreso_principal",
        "secemp": "sector_empleo",
        "empleo": "condicion_actividad"
    }
    
    # Renombrar solo las que existan en el dataset
    existing_mappings = {k: v for k, v in column_mappings.items() if k in df.columns}
    df = df.rename(columns=existing_mappings)
    
    return df
```

---

## 3. Descarga y Normalización de Tasas Referenciales del BCE

El BCE expone las Tasas de Interés Efectivas en reportes semanales y mensuales consolidados. La habilidad del agente debe incluir la automatización del parseo de estas hojas de cálculo que suelen contener celdas unidas y esquemas no estructurados.

```python
import pandas as pd
from loguru import logger

def parse_bce_interest_rates(excel_url: str) -> pd.DataFrame:
    """
    Descarga y parsea la serie histórica de tasas de interés activas y pasivas
    referenciales publicadas en los boletines de tasas del BCE.
    """
    logger.info(f"Consumiendo boletín de tasas del BCE desde: {excel_url}")
    
    # El BCE suele utilizar múltiples hojas. La de Tasas Efectivas comúnmente es 'TASAS'
    # Saltamos las primeras filas de logos y metadatos no estructurados
    df = pd.read_excel(excel_url, skiprows=7)
    
    # Normalización del DataFrame
    # 1. Eliminar filas enteramente vacías
    df = df.dropna(how="all")
    
    # 2. Renombrar columnas a snake_case
    df.columns = [
        "periodo", 
        "tasa_activa_productiva", 
        "tasa_activa_consumo",
        "tasa_pasiva_referencial"
    ] + list(df.columns[4:])
    
    # 3. Filtrar registros inválidos
    df = df[df["periodo"].astype(str).str.contains(r"\d{4}-\d{2}", regex=True)]
    
    logger.success("Serie histórica de tasas del BCE normalizada con éxito.")
    return df
```
EOF
