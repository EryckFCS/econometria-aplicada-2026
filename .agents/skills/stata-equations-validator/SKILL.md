# Validation of Econometric Equations and Stata 18 Alignment

Habilidad especializada para el diseño, formulación matemática, validación estructural y referenciación académica de ecuaciones econométricas alineadas con las especificaciones de StataCorp y la literatura empírica original.

## 1. Directrices de Redacción Científica y Referenciación

Para evitar imprecisiones retóricas o expresiones débiles (como *"según el manual de Stata"*), la incorporación de ecuaciones en los reportes de investigación debe fundamentarse exclusivamente en dos pilares:
1. **Los Autores Originales / Proponentes del Modelo:** Citados bajo norma APA 7 (p. ej., Johansen, 1988) para justificar la derivación teórica.
2. **La Especificación Computacional Exacta (StataCorp):** Referenciada mediante su sección técnica correspondiente e hipervinculada directamente al documento PDF oficial del manual de Stata 18 para posibilitar la replicabilidad.

### Reglas de Estilo para la Redacción de Ecuaciones
- **Voz y Tono:** Se utilizará la tercera persona del singular o la voz pasiva refleja. Se omitirá cualquier mención al software en el cuerpo de la ecuación (la vinculación metodológica al comando y opciones de Stata se relegará a notas metodológicas a pie de página o especificaciones en el anexo técnico).
- **Consistencia Matemática:** Todas las variables en las expresiones de diferencias ($\Delta y_t$) o niveles ($y_t$) deben definirse explícitamente en el párrafo inmediato anterior o posterior a la ecuación.
- **El Término de Ruido Blanco:** Toda ecuación dinámica debe incluir explícitamente el término de perturbación estocástica y declarar sus supuestos (ej. $u_t \sim i.i.d.(0, \sigma^2)$).

---

## 2. Estructura de Citas y Atribución Histórica

Cada modelo o contraste estimado debe seguir la siguiente plantilla estructural de documentación dentro de las notas de desarrollo o borradores científicos:

```markdown
### [Nombre Formal del Modelo / Contraste]

- **Especificación Matemática:** 
  [Fórmula en formato LaTeX]

- **Formulación del Contraste de Hipótesis (si aplica):**
  - $H_0: \text{[Condición sobre el parámetro]} \quad \text{([Significado económico])}$
  - $H_1: \text{[Condición sobre el parámetro]} \quad \text{([Significado económico])}$

- **Atribución Teórica Primaria:** [Autor/es original/es (Año)] en su artículo fundacional.
- **Referencia Técnica del Manual:** [StataCorp (2023)](https://www.stata.com/manuals/[nombre_pdf].pdf) `[Código_Manual] Comando`.
- **Correspondencia Empírica:** Comando exacto con opciones clave `comando varlist, opciones`.
```

---

## 3. Catálogo de Modelos y Referencias Técnicas Oficiales de Stata 18

### A. Prueba de Raíz Unitaria Dickey-Fuller Aumentada (ADF)
La dinámica de la prueba se basa en el trabajo seminal de **Dickey y Fuller (1979)** y su extensión para procesos de orden superior desarrollada por **Said y Dickey (1984)**.

*   **Especificación con tendencia determinista y constante:**
    $$\Delta y_t = \alpha + \beta y_{t-1} + \delta t + \sum_{j=1}^{k} \zeta_j \Delta y_{t-j} + \epsilon_t$$
    Donde $\epsilon_t \sim i.i.d.(0, \sigma^2)$.

*   **Contraste de Hipótesis:**
    *   $H_0: \beta = 0$ (La serie posee raíz unitaria, indicando no estacionariedad).
    *   $H_1: \beta < 0$ (La serie es estacionaria en torno a una tendencia temporal determinista).

*   **Referencia Técnica:** [StataCorp (2023)](https://www.stata.com/manuals/tsdfuller.pdf) `[TS] dfuller`.
*   **Correspondencia Empírica:** `dfuller varname, trend lags(k)`

### B. Prueba de Estacionariedad KPSS
Desarrollada por **Kwiatkowski, Phillips, Schmidt y Shin (1992)** para evaluar la estacionariedad como hipótesis nula.

*   **Especificación matemática:**
    $$y_t = \xi t + r_t + \eta_t, \quad r_t = r_{t-1} + u_t$$
    Donde $\eta_t$ es un error estacionario y $u_t \sim i.i.d.(0, \sigma_u^2)$ es el componente de paseo aleatorio.

*   **Contraste de Hipótesis:**
    *   $H_0: \sigma_u^2 = 0$ (La varianza del paseo aleatorio es nula; la serie es estacionaria).
    *   $H_1: \sigma_u^2 > 0$ (La varianza es positiva; la serie posee un paseo aleatorio y es no estacionaria).

*   **Referencia Técnica:** [StataCorp (2023)](https://www.stata.com/manuals/tskpss.pdf) `[TS] kpss` (módulo provisto por la comunidad y estandarizado en la documentación científica).
*   **Correspondencia Empírica:** `kpss varname, trend`

### C. Cointegración Multivariada (Johansen)
El análisis de cointegración multivariado se fundamenta en la metodología de máxima verosimilitud de **Johansen (1988, 1991, 1995)**.

*   **Modelo de Corrección de Error Vectorial (VECM):**
    $$\Delta \mathbf{y}_t = \mathbf{\alpha}\mathbf{\beta}' \mathbf{y}_{t-1} + \sum_{i=1}^{p-1} \mathbf{\Gamma}_i \Delta \mathbf{y}_{t-i} + \mathbf{\delta}_0 + \mathbf{\delta}_1 t + \mathbf{\varepsilon}_t$$
    Donde $\mathbf{\beta}' \mathbf{y}_{t-1}$ representa las relaciones de equilibrio a largo plazo ($ECT_{t-1}$), y $\mathbf{\alpha}$ la velocidad de ajuste dinámico.

*   **Referencia Técnica:** 
    *   Para la determinación del rango: [StataCorp (2023)](https://www.stata.com/manuals/tsvecrank.pdf) `[TS] vecrank`.
    *   Para la estimación del VECM: [StataCorp (2023)](https://www.stata.com/manuals/tsvec.pdf) `[TS] vec`.
*   **Correspondencia Empírica:** `vecrank varlist, trend(trend)` / `vec varlist, trend(trend) rank(r)`

### D. Modelo de Rezagos Distribuidos Autorregresivos (ARDL) y F-Bounds Test
La técnica del test de límites (*bounds test*) para cointegración bajo órdenes de integración mixtos $I(0)$ e $I(1)$ fue propuesta por **Pesaran, Shin y Smith (2001)**.

*   **Especificación condicional en diferencias (ARDL-ECM):**
    $$\Delta y_t = c_0 + \theta_y y_{t-1} + \sum_{i=1}^{k} \theta_{x_i} x_{i, t-1} + \sum_{j=1}^{p-1} \psi_j \Delta y_{t-j} + \sum_{i=1}^{k} \sum_{j=0}^{q_i-1} \varphi_{i,j} \Delta x_{i, t-j} + u_t$$
    Donde los coeficientes en niveles ($\theta_y, \theta_{x_i}$) definen la relación de largo plazo.

*   **Contraste de Hipótesis:**
    *   $H_0: \theta_y = \theta_{x_1} = \dots = \theta_{x_k} = 0$ (Inexistencia de relación a largo plazo).
    *   $H_1: \text{Al menos un } \theta \neq 0$ (Existencia de relación a largo plazo).

*   **Referencia Técnica:** [StataCorp (2023)](https://www.stata.com/manuals/tsardl.pdf) `[TS] ardl` (desarrollado formalmente en el ecosistema Stata por Kripfganz y Wright, 2018).
*   **Correspondencia Empírica:** `ardl y x1 x2 x3, ec` seguido del test de cotas `estat ectest`.

---

## 4. Protocolo de Auditoría de Ecuaciones
El Agente de IA debe contrastar de manera obligatoria cada borrador matemático con este checklist antes de declararlo listo:
1. [ ] **Eliminación de Locuciones Informales:** ¿Se ha evitado el uso de la frase "según el manual de Stata" o similares en el cuerpo del texto?
2. [ ] **Atribución Primaria:** ¿Se cita al autor/es que plantearon el modelo originalmente junto con el año de publicación original del artículo científico?
3. [ ] **Referencia Técnica Inequívoca:** ¿Se proporciona la referencia a [StataCorp (2023)](https://www.stata.com/manuals/) en formato hipervínculo apuntando al PDF técnico correspondiente de la función analizada?
4. [ ] **Definición de Variables:** ¿Se han declarado formalmente todas las variables y operadores del modelo (p. ej., $\Delta$, $t$, términos de rezago)?
5. [ ] **Especificación de Perturbación:** ¿Está explícito el supuesto estadístico de la perturbación aleatoria ($\epsilon_t$ o $\mathbf{\varepsilon}_t$)?
