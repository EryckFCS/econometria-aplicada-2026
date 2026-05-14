# Scripts de Análisis - Sostenibilidad IESS

Este directorio contiene la lógica de procesamiento de datos y análisis econométrico para el artículo.

## Pipeline de Análisis (Stata)

- **`master_analysis.do`**: Script maestro unificado. Ejecuta la secuencia completa:
  1. Selección de rezagos (VAR).
  2. Pruebas de causalidad de Granger.
  3. Cointegración de Johansen.
  4. Pruebas de raíz unitaria con quiebre estructural (Zandrews-Andrews).
  5. Estimación ARDL (Relación de largo plazo y mecanismo de ajuste).
  6. Diagnósticos de robustez (Normalidad, Autocorrelación, Heterocedasticidad, Especificación).
  7. Generación de gráficos de estabilidad (CUSUM).

## Procesamiento de Datos (Python)

- **`prepare_data.py`**: Realiza la limpieza e imputación lineal de la tasa de homicidios y prepara el archivo `data/base_analisis.csv`.
- **`parse_stata_log.py`**: Automatiza la extracción de resultados del log de Stata hacia formatos Word/Excel para las tablas del paper.

## Uso

1. Preparar datos:
   ```bash
   python3 scripts/prepare_data.py
   ```
2. Ejecutar análisis en Stata:
   Abrir Stata y ejecutar `do scripts/master_analysis.do`.
3. Generar tablas de reporte:
   ```bash
   python3 scripts/parse_stata_log.py
   ```

## Requisitos

Instalar dependencias de Python:
```bash
python3 -m pip install -r scripts/requirements.txt
```
