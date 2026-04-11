# Variables No Resueltas — APE1

**Fecha de auditoría:** 2026-04-11T19:32:42Z

---

## 1. Factor de capacidad de carga

**Concepto teórico:** Medida de la presión sobre el sistema ecológico en relación con la biocapacidad disponible.

**Estado:** NO DISPONIBLE directamente en API pública para los 20 países, período 2000-2023.

**Mejores fuentes candidatas:**

- Global Footprint Network (GFN) — Datos de huella ecológica y biocapacidad per cápita. Disponibles previa registro en `data.footprintnetwork.org`. Licencia abierta para investigación. Cobertura: todos los países, anual desde 1961.
- UN FAO: Área agrícola disponible por habitante como proxy indirecto.
- UNDP Human Development Report — Índice de Presión Planetaria (no estandarizado como serie).

**Parte que requiere proxy:** Cualquier estimación para este panel requeriría GFN (descarga manual) o definir el ratio huella/biocapacidad.

**Parte que requiere descarga manual:** GFN no tiene API pública estándar REST. Descarga CSV desde su plataforma.

**Decisión:** AUSENTE del panel_raw. Requiere aprobación explícita del proxy a usar y descarga manual.

---

## 2. Incertidumbre de la política climática

**Estado:** NO DISPONIBLE en API pública para AL 2000-2023.

**Fuentes académicas candidatas:**

- Baker, Bloom & Davis — Economic Policy Uncertainty Index (EPU): disponible para Argentina, Brasil, Chile, Colombia, México. No cubre todos los 20 países.
- IPCC Reports — datos de escenarios, no índices de incertidumbre nacionales.

**Decisión:** AUSENTE del panel_raw. Cobertura geográfica insuficiente para los 20 países.

---

## 3. Incertidumbre relacionada con la energía

**Estado:** NO DISPONIBLE en API pública.

**Fuentes candidatas:**

- IEA World Energy Outlook — proyecciones, no series históricas de incertidumbre.
- Volatilidad de precios de commodities energéticos (proxy indirecto): disponible en World Bank Commodity Prices.

**Decisión:** AUSENTE del panel_raw. Concepto requiere definición operacional precisa antes de seleccionar proxy.

---

## 4. Índice de riesgo climático

**Estado:** NO DISPONIBLE en API pública con cobertura continua para 20 países, 2000-2023.

**Mejores fuentes candidatas:**

- Germanwatch Global Climate Risk Index (CRI) — anual, mide impacto de eventos climáticos extremos. Disponible como descarga manual PDF/XLS. Cobertura: todos los países desde 2000.
- Notre Dame Global Adaptation Index (ND-GAIN) — anual, descargar desde `gain.nd.edu`. Cobertura: 181 países desde 1995.

**Parte que requiere descarga manual:** Ambas fuentes requieren descarga manual o scraping estructurado.

**Decisión:** AUSENTE del panel_raw. Requiere aprobación del índice a usar.

---

## 5. Innovación tecnológica verde (directa)

**Estado:** NO DISPONIBLE directamente en API pública para todos los 20 países AL.

**Fuente más cercana rechazada:**

- OECD Patents on Environment Technologies: solo cubre países con patentes registradas activamente. Para AL (excepto México y Brasil), cobertura casi nula. Datos disponibles vía OECD Data Explorer pero no vía API estándar.
- IRENA Renewable Capacity Statistics: datos de capacidad instalada GW por tecnología. Descarga manual.

**Lo que SÍ está en el panel como proxy (marcado como tal):**

- `renewable_electricity_output_pct`: participación renovable en generación eléctrica (%).
- `rd_expenditure_pct_gdp`: I+D total como proxy de capacidad innovadora.

**Advertencia:** Ninguno de estos proxies mide específicamente "innovación" tecnológica verde; miden adopción y gasto genérico en I+D.

---

## 6. Protección de los derechos laborales (directa)

**Estado:** NO DISPONIBLE como índice continuo en API pública para 20 países, 2000-2023.

**Fuentes directas:**

- ITUC Global Rights Index: anual desde 2014. Solo 9 años de cobertura. Descarga manual.
- ILO ILOSTAT — `collective_bargaining_coverage_rate`: disponible pero con cobertura parcial.
- V-Dem Dataset — incluye indicadores laborales pero requiere descarga.

**Lo que está en el panel como proxy:** `child_employment_pct_7to14` (13.8% cobertura).

---

## 7. Impuestos ambientales (directos)

**Estado:** NO DISPONIBLE en API pública con cobertura continua para 20 países AL.

**Fuentes directas:**

- OECD Database on Instruments for Environmental Policy: cobertura parcial AL (México principalmente).
- CEPAL CEPALSTAT — algunos datos de impuestos ambientales, descarga manual.
- World Bank Carbon Pricing Dashboard: mecanismos de carbono, no impuestos generales.

---

## 8. Rigurosidad de la política ambiental

**Estado:** NO DISPONIBLE directamente para 20 países AL.

**Fuentes:**

- OECD Environmental Policy Stringency (EPS) Index: cubre solo países OECD.
- Yale EPI (Environmental Performance Index): bienal, 180 países, descarga manual desde `epi.yale.edu`.

---

## Resumen ejecutivo de brechas

| Variable consigna | Estado en RAW | Acción requerida |
|---|---|---|
| Factor capacidad de carga | AUSENTE | Descarga manual GFN + aprobación proxy |
| Incertidumbre política climática | AUSENTE | Definir alcance + EPU parcial |
| Incertidumbre energética | AUSENTE | Definir operacionalmente |
| Índice de riesgo climático | AUSENTE | Elegir entre CRI o ND-GAIN + descarga manual |
| Innovación tecnológica verde | PROXY parcial | Aprobación de EG.ELC.RNEW.ZS como proxy |
| Derechos laborales | PROXY débil | ITUC desde 2014 o redefinir concepto |
| Impuestos ambientales | PROXY fiscal | Aprobar GC.TAX o buscar CEPALSTAT |
| Rigurosidad política ambiental | PROXY regulatorio | Yale EPI descarga manual o WGI RQ aprobado |
