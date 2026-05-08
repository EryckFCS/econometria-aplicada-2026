# 📊 Guía de Estudio: Modelos ARMA, ARCH y GARCH

Esta guía proporciona los fundamentos teóricos y prácticos para el modelado de series de tiempo financieras y macroeconómicas, alineada con los contenidos de la **Unidad 1 de Econometría Aplicada**.

---

## 1. Modelo ARMA (AutoRegressive Moving Average)

### Definición
El modelo ARMA combina dos procesos: uno autorregresivo (AR) y uno de medias móviles (MA). Se utiliza para modelar series de tiempo estacionarias donde el valor actual depende de sus valores pasados y de los errores de pronóstico pasados.

### Ecuación Base (ARMA(p, q))
$$ Y_t = c + \sum_{i=1}^{p} \phi_i Y_{t-i} + \varepsilon_t + \sum_{j=1}^{q} \theta_j \varepsilon_{t-j} $$
Donde:
- $\phi_i$: Coeficientes autorregresivos.
- $\theta_j$: Coeficientes de medias móviles.
- $\varepsilon_t$: Ruido blanco.

### Aplicación
- Predicción de variables macroeconómicas estables (PIB trimestral, Inflación subyacente).
- Modelado de series con persistencia temporal.

### Ejemplo Real
**Pronóstico de la Inflación en Ecuador:** Se puede modelar la tasa de inflación mensual como un ARMA(1,1), donde el dato de este mes depende fuertemente del mes anterior (AR) y de un ajuste por choques inesperados recientes (MA).

---

## 2. Modelo ARCH (Autoregressive Conditional Heteroskedasticity)

### Definición
Introducido por Robert Engle (1982), el modelo ARCH permite que la varianza del error no sea constante en el tiempo (heterocedasticidad), sino que dependa del cuadrado de los errores pasados. Se enfoca en el "clustering de volatilidad".

### Ecuación Base (ARCH(q))
Ecuación de la media: $Y_t = \mu + \varepsilon_t$  
Ecuación de la varianza:
$$ \sigma_t^2 = \alpha_0 + \sum_{i=1}^{q} \alpha_i \varepsilon_{t-i}^2 $$
Donde:
- $\sigma_t^2$: Varianza condicional.
- $\alpha_i > 0$: Peso de los choques pasados en la volatilidad actual.

### Aplicación
- Análisis de riesgo financiero.
- Modelado de periodos de alta turbulencia seguidos de calma.

### Ejemplo Real
**Crisis de Precios del Petróleo (WTI):** Durante choques geopolíticos, los residuos al cuadrado de los precios del petróleo aumentan drásticamente, lo que eleva la varianza condicional para el día siguiente, capturando la incertidumbre del mercado.

---

## 3. Modelo GARCH (Generalized ARCH)

### Definición
Desarrollado por Tim Bollerslev (1986), el GARCH es una extensión del ARCH que incluye términos autorregresivos de la propia varianza. Es más parsimonioso (usa menos parámetros) que un ARCH de orden alto.

### Ecuación Base (GARCH(p, q))
$$ \sigma_t^2 = \omega + \sum_{i=1}^{q} \alpha_i \varepsilon_{t-i}^2 + \sum_{j=1}^{p} \beta_j \sigma_{t-j}^2 $$
Donde:
- $\beta_j$: Coeficiente de persistencia de la volatilidad (memoria de largo plazo).

### Aplicación
- Modelado de retornos de activos financieros (Acciones, Criptomonedas).
- Estimación del Valor en Riesgo (VaR).

### Ejemplo Real
**Volatilidad del S&P 500:** Un modelo GARCH(1,1) es el estándar para capturar cómo la volatilidad de ayer y el choque de ayer determinan el riesgo de hoy. Si $\alpha + \beta \approx 1$, la volatilidad es extremadamente persistente.

---

## 🧪 ¿Podemos modelarlos actualmente?

**Sí.** Nuestra infraestructura v8.1.5 cuenta con los componentes necesarios:

1.  **Datos**: Tenemos acceso a `yfinance` para descargar series históricas de mercados (Brent, WTI, Oro) y el `Master Macro Lake` para series de inflación y PIB.
2.  **Software**: Las librerías `statsmodels` (para ARMA/ARIMA) y `arch` (para ARCH/GARCH) están integradas en nuestro entorno `uv`.
3.  **Capacidad Analítica**: Podemos usar el **Master Orchestrator** para automatizar la estimación y generar el reporte de volatilidad directamente en Quarto.

---
**Elaborado por:** Antigravity (AI Operador Técnico)  
**Fecha:** 2026-05-04  
**Contexto:** Unidad 1 - Técnicas y Modelos de Series de Tiempo.
