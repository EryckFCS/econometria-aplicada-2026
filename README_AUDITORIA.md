# README — Auditoría Forense APE1

**Versión:** 2.0 (RAW forense)  
**Fecha:** 2026-04-11T19:32:42Z  
**Protocolo:** CERO interpolación | CERO imputación | CERO proxies no aprobados en panel_raw

---

## Qué ES raw en este panel

El archivo `panel_raw.csv` contiene **exclusivamente** series descargadas directamente desde APIs públicas del World Bank (WDI, WGI, Global Findex), sin ninguna transformación analítica:

- No hay interpolación (ni lineal ni polinomial).
- No hay forward-fill ni backward-fill.
- No hay imputación de medias, medianas ni modelos.
- No hay escala, normalización ni estandarización.
- Los NaN representan datos genuinamente no disponibles en la fuente.
- Los valores negativos en `ghg_total_incl_lulucf_mt_co2e` son VÁLIDOS: reflejan países con sumidero forestal neto (Panamá, Venezuela).

---

## Qué NO está resuelto

Las siguientes variables de la consigna **no tienen representación directa** en el panel_raw:

| Variable | Razón |
|---|---|
| Factor de capacidad de carga | Sin API pública estándar; requiere GFN manual |
| Incertidumbre política climática | Sin datos para todos los 20 países |
| Incertidumbre relacionada con energía | Sin serie estandarizada |
| Índice de riesgo climático | Requiere CRI o ND-GAIN, descarga manual |

---

## Variables mal rotuladas o ambiguas (versión anterior)

### 1. `capacidad_renovable_gw` → NOMBRE INCORRECTO
**Indicador real:** `EG.ELC.RNEW.ZS` = *Renewable electricity output (% of total electricity output)*  
**Unidad real:** porcentaje (%), NO gigavatios (GW)  
**Nombre correcto en RAW:** `renewable_electricity_output_pct`  
**Acción:** Dato conservado sin modificación. Rename propuesto en panel_modelo.

### 2. `pib_per_capita_ppa` — AÑO BASE DESACTUALIZADO
**La v1 documentaba año base 2017. La API devuelve base 2021** (ICP 2021).  
**Nombre correcto en RAW:** `gdp_per_capita_ppp_const2021_intl`  
**Acción:** Dato conservado. Rename propuesto en panel_modelo.

### 3. `empleo_informal_pct` → CONCEPTO IMPRECISO
**Indicador real:** `SL.EMP.VULN.ZS` = *Vulnerable employment* (empleo vulnerable)  
**Empleo vulnerable ≠ informalidad** en sentido estricto de la OIT.  
**Nombre correcto en RAW:** `vulnerable_employment_pct_total`  
**Acción:** Dato conservado. Rename y nota metodológica en panel_modelo.

---

## Redundancias diagnosticadas

### Bloque forestal
`forest_area_km2` y `forest_area_pct_land` son la misma variable FAO en dos unidades. Para un modelo: usar `forest_area_pct_land` (normalizada, cobertura 100%).

### Bloque GEI/CO2
`ghg_total_incl_lulucf_mt_co2e` contiene a `co2_excl_lulucf_mt_co2e` como subconjunto. No usar ambas como variables dependientes simultáneas.

### Bloque PIB
`gdp_per_capita_const2015_usd` y `gdp_per_capita_ppp_const2021_intl` miden lo mismo en deflactores distintos. Elegir una según marco teórico.

### Bloque tecnología
`internet_users_pct_pop` y `mobile_subscriptions_per100` son proxies del mismo concepto.

### Bloque renovables
`renewable_energy_pct_final_energy` y `renewable_electricity_output_pct` miden participación renovable con denominadores distintos.

### Bloque WGI (6 dimensiones)
Todas las dimensiones WGI provienen del mismo índice compuesto. Correlación intragrupo ~0.7-0.9. Incluir más de 2 en un modelo genera multicolinealidad grave.

---

## Transformaciones pendientes para Fase 2 (panel_modelo)

Estas transformaciones están **explícitamente PENDIENTES** y requieren aprobación:

1. **Interpolación Global Findex** (`account_ownership_pct_adults`): los años sin encuesta quedan NaN. Propuesta: interpolación lineal acotada a ventana 3 años — requiere aprobación.

2. **Renombrar columnas inconsistentes** (listadas arriba): rename sin alterar datos.

3. **Parsimonia en bloque WGI**: elegir 1-2 dimensiones o construir índice PCA.

4. **Incorporar variables no resueltas** (GFN, CRI, EPS): requieren descarga manual y aprobación.

5. **Logaritmización de PIB y población**: transformación común en modelos EKC — pendiente aprobación.

6. **Rezagos temporales**: variables potencialmente endógenas (GEI, CO2, PIB) pueden requerir rezagos — pendiente definición del modelo.

---

## Patrón de interpolación en datos FAO (información, no alerta de error)

La serie `forest_area_km2` del WB muestra diferencias anuales **constantes dentro de períodos quinquenales** (patrón lineal), lo cual confirma que el WB aplica interpolación de los datos FAO (quinquenales) para producir una serie anual. Esta interpolación es **realizada por la fuente (FAO/WB), no por este equipo**. Se documenta por transparencia pero NO es un error de este panel.

---

## Reproducibilidad

Todos los datos descargados vía World Bank API v2:
```
https://api.worldbank.org/v2/country/[ISO2]/indicator/[CÓDIGO]?format=json&per_page=1000&date=2000:2023
```
WGI vía source=3 del WB (código: `GOV_WGI_*`).  
Fecha de descarga registrada en `manifest_fuentes.csv`.  
Hash SHA-256 parcial de cada columna disponible en manifest para verificación.

---

## Archivos generados

| Archivo | Descripción |
|---|---|
| `panel_raw.csv` | Base principal cruda — 480 filas × 31 cols |
| `diccionario_variables.csv` | Trazabilidad completa por columna |
| `matriz_cumplimiento_consigna.csv` | Mapa consigna → disponibilidad |
| `manifest_fuentes.csv` | Log de descarga por serie |
| `auditoria_redundancia.csv` | Diagnóstico de redundancias sin borrado |
| `auditoria_integridad.csv` | Cobertura, patrones temporales, alertas |
| `variables_no_resueltas.md` | Variables sin solución directa |
| `README_AUDITORIA.md` | Este documento |
