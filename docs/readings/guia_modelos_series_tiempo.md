# 📊 Guía de Estudio: Modelos ARMA, ARCH y GARCH

Esta guía proporciona los fundamentos teóricos y prácticos para el modelado de series de tiempo financieras y macroeconómicas, alineada con los contenidos de la **Unidad 1 de Econometría Aplicada**.

---

## 📑 Resumen Ejecutivo de Modelos

| Modelo | Enfoque Principal | Requisito Clave | Uso Típico |
|:---|:---|:---|:---|
| **ARMA** | Nivel de la serie (Media) | Estacionariedad | Pronóstico univariante. |
| **Dinam. Gral (ADL)** | Relación dinámica multivariante | Exogeneidad y Cointegración | Impacto de X sobre Y en el tiempo. |
| **ARCH** | Variabilidad (Varianza) | Clustering de volatilidad | Medición de riesgo. |
| **GARCH** | Variabilidad + Persistencia | Estabilidad ($\alpha + \beta < 1$) | Mercados financieros. |

---

## 1. Modelo ARMA (AutoRegressive Moving Average)

### Intuición Económica
El modelo ARMA asume que el valor actual de una variable es una función de su propia historia (**AR**) y de la acumulación de shocks o errores pasados (**MA**). Es el "estándar de oro" para series que muestran inercia pero que eventualmente regresan a su media (estacionarias).

### Componentes Técnicos (ARMA(p, q))
$$ Y_t = c + \sum_{i=1}^{p} \phi_i Y_{t-i} + \varepsilon_t + \sum_{j=1}^{q} \theta_j \varepsilon_{t-j} $$

> [!TIP]
> **Identificación:** Se utiliza la Función de Autocorrelación (ACF) para identificar el componente **MA** y la Función de Autocorrelación Parcial (PACF) para el componente **AR**.

### Fortalezas y Debilidades
*   **Fortaleza:** Excelente capacidad de pronóstico a corto plazo para variables como el PIB o la inflación.
*   **Debilidad:** Falla catastróficamente si la serie no es estacionaria (requiere diferenciación previa, convirtiéndose en ARIMA).

---

## 2. Modelo Dinámico General (ADL - Autoregressive Distributed Lag)

### Intuición Económica
A diferencia de los modelos univariantes, el **Modelo Dinámico General** permite modelar la relación entre varias variables considerando que los efectos no son instantáneos. Captura cómo los cambios en una variable independiente ($X$) afectan a la dependiente ($Y$) a lo largo de varios periodos.

### Ecuación Base (ADL(p, q))
$$ Y_t = c + \sum_{i=1}^{p} \phi_i Y_{t-i} + \sum_{j=0}^{q} \beta_j X_{t-j} + \varepsilon_t $$

> [!TIP]
> **Multiplicadores:** Este modelo permite calcular el **multiplicador de impacto** ($\beta_0$) y el **multiplicador de largo plazo** ($\frac{\sum \beta_j}{1 - \sum \phi_i}$), esenciales para el diseño de política económica.

### Aplicación Práctica
*   **Política Monetaria:** ¿Cómo afecta un cambio en la tasa de interés hoy al consumo privado en los próximos 6 meses?
*   **Comercio Exterior:** Relación entre el tipo de cambio real y la balanza comercial.

---

## 3. Modelo ARCH (Autoregressive Conditional Heteroskedasticity)

### El Fenómeno del "Volatility Clustering"
En finanzas, "los errores grandes tienden a ser seguidos por errores grandes". El ARCH captura este fenómeno permitiendo que la varianza de hoy dependa del tamaño de los shocks de ayer.

### Estructura del Modelo (ARCH(q))
1. **Ecuación de la Media:** $Y_t = \mu + \varepsilon_t$ (donde $\varepsilon_t$ es el shock).
2. **Ecuación de la Varianza:**
$$ \sigma_t^2 = \alpha_0 + \alpha_1 \varepsilon_{t-1}^2 + \dots + \alpha_q \varepsilon_{t-q}^2 $$

> [!IMPORTANT]
> Los coeficientes $\alpha_i$ deben ser positivos para garantizar que la varianza sea siempre positiva. Si $\alpha_1$ es alto, los shocks pasados impactan fuertemente en la incertidumbre actual.

### Aplicación Práctica
Fundamental en el análisis de **commodities** (Petróleo, Oro). Permite entender por qué tras un evento geopolítico la incertidumbre no desaparece inmediatamente, sino que se disipa gradualmente.

---

## 4. Modelo GARCH (Generalized ARCH)

### Parsimonia y Persistencia
Mientras que un modelo ARCH podría necesitar muchos rezagos ($q$) para capturar la volatilidad, el GARCH añade la varianza pasada como regresor. Esto lo hace más eficiente (parsimonioso) y permite medir la **memoria de la volatilidad**.

### Ecuación Base (GARCH(p, q))
$$ \sigma_t^2 = \omega + \sum_{i=1}^{q} \alpha_i \varepsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_j \sigma_{t-j}^2 $$

> [!CAUTION]
> **La Condición de Estabilidad:** La suma $\sum \alpha_i + \sum \beta_j$ debe ser menor a 1. 
> - Si $\alpha + \beta \approx 1$, la volatilidad es extremadamente persistente (un shock hoy afecta el riesgo por mucho tiempo).
> - Si $\alpha + \beta > 1$, el proceso es explosivo y el riesgo no tiene límite superior.

---

## 🛠️ Metodología de Implementación (Pipeline v8.1.5)

Para una estimación robusta, seguimos este flujo de trabajo:

1.  **Detección de Estacionariedad:** Test de Dickey-Fuller Aumentado (ADF).
2.  **Identificación:** Análisis de correlogramas (ACF/PACF).
3.  **Estimación:** Máxima Verosimilitud (MLE) usando `statsmodels`.
4.  **Diagnóstico de Residuos:** Test de Ljung-Box para asegurar que no queda información en los errores (Ruido Blanco).
5.  **Detección de Efectos ARCH:** Test de Engle para justificar el uso de modelos de volatilidad.

---

## 🧪 Capacidades Operativas

Nuestra infraestructura permite:
*   **Ingesta:** Conexión directa a Bloomberg/Yahoo Finance vía `ecs_quantitative`.
*   **Automatización:** Scripts en `src/tasks/` para recalibrar modelos diariamente.
*   **Reporteo:** Renderizado automático en PDF/HTML con Quarto para presentaciones ejecutivas.

---
**Elaborado por:** Antigravity (AI Operador Técnico)  
**Fecha:** 2026-05-11  
**Contexto:** Unidad 1 - Técnicas Avanzadas de Modelado Econométrico.
