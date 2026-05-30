---
# WORKFLOW: Pipeline Econométrico de Alta Fidelidad
- **Descripción**: Pipeline riguroso para la estimación de modelos de series de tiempo (SARIMA, ARCH/GARCH) y microeconométricos (Probit Bivariado) utilizando datos unificados extraídos soberanamente mediante servidores MCP e integrados en los repositorios de la UNL.
- **Versión**: 2.0.0

---

## 1. Cuándo Invocar este Workflow

Debe activarse al desarrollar nuevos análisis empíricos para los repositorios académicos de la UNL (e.g., `applied_econometrics_2026`, `double-informality-determinants-ecuador`) o cuando se requiera modelar el comportamiento estructural de variables macrofinancieras de Ecuador.

---

## 2. Prerrequisitos

- Servidores MCP `capital-inec` y `capital-bce` activos.
- Dependencias de modelado estadístico (`statsmodels`, `scikit-learn`, `scipy`, `pandas`, `pyarrow`) instaladas mediante `uv sync`.
- Entorno configurado para guardar los datos procesados en `data/processed/` dentro del repositorio del proyecto.

---

## 3. Pasos del Proceso y Herramientas Activas

### Paso 1: Extracción Automatizada y Soberana de Datos
Antes de cualquier estimación, extraer las series de tiempo macroeconómicas o microdatos requeridos directamente desde fuentes oficiales utilizando los servidores MCP dedicados.

#### A. Para Series de Tiempo (Inflación, Tasas de Interés, Morosidad)
- **Herramientas**: `capital-bce:bce_get_macro_series`, `capital-bce:bce_get_interest_rates`, `capital-bce:sbs_get_morosity`
- **Uso**: Extraer series oficiales de inflación, tasas activas/pasivas y morosidad de la SBS de forma directa para depositarlas en `data/raw/` o cargarlas en memoria.

#### B. Para Microdatos e Indicadores de Empleo (ENEMDU)
- **Herramientas**: `capital-inec:inec_query`, `capital-inec:inec_describe_variable`, `capital-inec:inec_get_indicator`
- **Uso**: Consultar estructuras de variables de empleo, informalidad y pobreza, y extraer microdatos estructurados directo al ecosistema local.

---

### Paso 2: Pruebas de Estacionariedad y Raíz Unitaria (Series de Tiempo)
Antes de estimar cualquier modelo dinámico (como SARIMA o VAR), validar la estacionariedad de las series obtenidas mediante pruebas de Dickey-Fuller Aumentada (ADF) y KPSS.
```bash
# Correr script de diagnóstico estadístico de series de tiempo
uv run python scripts/ops/check_stationarity.py --input data/processed/bce_inflation.parquet
```

---

### Paso 3: Estimación del Modelo Econométrico
Ejecutar el script de estimación formal según el tipo de hipótesis (ej. regresión Probit para decisiones de informalidad laboral o SARIMA/GARCH para volatilidad macrofinanciera).
```bash
uv run python scripts/estimate_probit.py --data data/processed/enemdu_clean.parquet --target informality
```

---

### Paso 4: Validación de Supuestos e Inferencia Rigurosa
Validar autocorrelación de residuos (Ljung-Box para series de tiempo, heterocedasticidad y especificación para Probit) y exportar tablas de coeficientes, errores estándar y p-valores en formatos listos para LaTeX.
```bash
uv run python scripts/validate_residuals.py --model outputs/models/probit_v1.pkl
```

---

## 4. Manejo de Errores y Excepciones

- **No Estacionariedad**: Si la serie no es estacionaria, aplicar diferenciación de primer orden o estacional ($d$ o $D$) y volver a ejecutar la prueba ADF.
- **No Convergencia del Optimizador**: Si la estimación de máxima verosimilitud (ML) del Probit o GARCH no converge, cambiar el algoritmo de optimización (e.g., de 'newton' a 'bfgs' en `statsmodels`) o verificar la colinealidad de los regresores.
- **Errores de Conexión de APIs en MCP**: El servidor MCP `capital-inec` o `capital-bce` puede experimentar límites de tasa (rate limits). Utilizar caching local e implementar reintentos exponenciales en los scripts de ingesta.

---

## 5. Outputs Esperados

- Tabla formal de resultados econométricos exportada en LaTeX/Markdown dentro de `docs/reports/table_results.md`.
- Gráficos de diagnóstico de residuos (FAC/FACP) en `docs/figures/residuals_acf.png`.
- Series de datos crudas y procesadas integradas en la estructura de datos local en `data/processed/`.
