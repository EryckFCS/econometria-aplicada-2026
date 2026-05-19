# Radiografía de la Sostenibilidad del IESS en el Ecuador (1990-2024)
## Interacción Dinámica de Canales Fiscales, Demográficos e Institucionales

La sostenibilidad del sistema previsional de reparto administrado por el Instituto Ecuatoriano de Seguridad Social (IESS) colisiona con perturbaciones macroeconómicas, fiscales e institucionales que exceden los determinantes paramétricos tradicionales. La figura multipanel [`fig-radiografia-problema.png`](file:///home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/analysis_erick_condoy/assets/fig-radiografia-problema.png) mapea de manera empírica la interacción dinámica entre la cobertura del seguro general y sus tres canales de transmisión causal: la violencia civil, la competencia fiscal por defensa y el flujo migratorio neto.

---

## 1. Contribución Científica y Brecha en la Literatura

La literatura previsional tradicional incurre en un sesgo de determinismo demográfico. Los estudios clásicos basados en el Modelo de Generaciones Traslapadas (OLG) de Diamond (1965) o en la taxonomía de modelos de protección social Bismarckianos y Beveridgeanos (Murillo, 2025) asumen que la masa de afiliados al seguro social está determinada únicamente por la estructura etaria, la productividad del mercado de trabajo y el diseño paramétrico de aportes. Esta visión ignora la endogeneidad institucional del mercado laboral en economías en desarrollo y dolarizadas.

Este análisis cierra tres brechas críticas en la literatura económica aplicada:

1.  **Integración Previsional de la Economía del Crimen (Becker, 1968)**: Supera el enfoque clásico de la informalidad como mera evasión tributaria o baja productividad laboral. Al incorporar la tasa de homicidios, el modelo formaliza teóricamente la "informalidad defensiva" —donde los agentes optan por la economía informal para camuflar sus ingresos y reducir su exposición a la delincuencia y extorsión— como un determinante directo del encogimiento del fondo de pensiones.
2.  **Transmisión Fiscal del Crowding-out en Dolarización**: La literatura empírica local suele tratar el gasto social y la contribución estatal del 40% al IESS como variables aisladas de la defensa nacional. Este análisis demuestra que el financiamiento estatal es un juego de suma cero. Bajo restricciones monetarias estrictas, la seguridad nacional militarizada compite directamente y desplaza las transferencias previsionales obligatorias.
3.  **Endogenización del Drenaje Demográfico**: Conecta las dinámicas migratorias netas directamente con la tasa de cobertura. El flujo de salida físico de trabajadores jóvenes altera el ratio de soporte activo/pasivo del esquema de reparto, aportando evidencia empírica en un contexto donde el censo previsional nacional no capta en tiempo real la fuga de capital humano.

---

## 2. Variable de Anclaje: Tasa de Cobertura Previsional ($COB_t$)

La viabilidad del esquema de reparto se evalúa a través de la **Tasa de Cobertura Previsional ($COB_t$)**, la cual cuantifica la proporción de la fuerza laboral nacional que cotiza activamente en el seguro obligatorio:

$$
COB_t = \left( \frac{\text{Afiliados Activos IESS}_t}{\text{Fuerza Laboral Total}_t} \right) \times 100
$$

La serie temporal (1990-2024) revela una trayectoria no lineal con tres fases nítidamente delimitadas:
*   **Fase de Estancamiento Estructural (1990-2000)**: La cobertura fluctuó en un piso histórico del **22.9% al 24.8%**. La volatilidad monetaria y la inestabilidad de fin de siglo asfixiaron el crecimiento del empleo formal.
*   **Fase de Expansión Formal (2001-2015)**: La cobertura experimentó un crecimiento secular sin precedentes hasta alcanzar su **pico histórico del 46.3% en 2015**. Este ascenso responde a la liquidez de la dolarización, el auge de los commodities y reformas institucionales de alta coercitividad (penalización de la no-afiliación laboral post-2008).
*   **Fase de Repliegue y Crisis (2016-2024)**: Se registra una persistente contracción que se acelera tras el COVID-19 y la subsiguiente crisis de violencia civil, provocando un retroceso de la cobertura al **42.9% en 2024**.

---

## 3. Análisis Técnico por Canales Estructurales (Paneles A, B, C y D)

### Panel A: Canal de Inestabilidad Social (Homicidios vs. Cobertura)
El **Panel A** contrasta la Tasa de Cobertura (eje Y1, línea azul) con la **Tasa de Homicidios por cada 100,000 habitantes** (eje Y2, línea discontinua roja) en escala temporal.

*   **Descripción del Gráfico**: Se presenta un eje dual sincronizado a nivel anual (1990-2024). Muestra la estabilidad de la tasa de homicidios en niveles inferiores a 18 casos por cada 100k hab. hasta 2019, año a partir del cual se desata un crecimiento exponencial hacia los **45.72** homicidios. En paralelo, la cobertura previsional rompe su tendencia de estabilización y entra en una pendiente negativa pronunciada.
*   **Explicación y Mecanismo**: La inestabilidad social actúa como un impuesto al sector formal. El auge del crimen organizado y la extorsión generalizada incrementan los costos operativos de las micro y pequeñas empresas. Los trabajadores independientes eligen la informalidad voluntaria y el autoempleo como escudos de camuflaje operativo, evitando la visibilidad de los registros de afiliación obligatorios. La violencia destruye el incentivo de planeación previsional de largo plazo y reduce la masa de cotizantes.

### Panel B: Canal de Prioridad Fiscal (Gasto Militar vs. Cobertura)
El **Panel B** mapea la interacción entre la Cobertura (eje Y1, línea azul) y el **Gasto Militar expresado como porcentaje del PIB** (eje Y2, línea discontinua dorada).

*   **Descripción del Gráfico**: Se observan picos pronunciados de gasto militar que rompen la tendencia secular de la serie. Destacan el conflicto armado del Cenepa en 1995 (gasto militar militar se eleva a **1.99% del PIB**) y el periodo de rearme estatal 2008-2011 (con picos que rozan el **3.24% del PIB**). En ambos hitos temporales de prioridad fiscal en defensa, la tasa de cobertura previsional experimenta desaceleraciones notables.
*   **Explicación y Mecanismo**: En una economía dolarizada bajo estricta restricción de liquidez, la reasignación de ingresos del Estado es un juego de suma cero. El gasto en seguridad y defensa actúa como un rubro fiscal rígido que desplaza de forma directa el cumplimiento de la transferencia estatal del 40% al IESS. La postergación de la deuda del Estado con el fondo previsional debilita los saldos de reserva e incrementa el déficit de reparto, minando la liquidez del instituto para cubrir las jubilaciones actuales.

### Panel C: Canal de Drenaje Demográfico (Migración)
El **Panel C** muestra la Tasa de Cobertura (eje Y1, línea azul) frente a la **Migración Neta en miles de personas** (eje Y2, barras verdes).

*   **Descripción del Gráfico**: Se visualiza la cobertura en contraste con barras que reflejan el flujo migratorio neto anual. Los saldos migratorios netos negativos de fines de los noventa superan las **40,000 personas anuales** en migración de salida, coincidiendo con el colapso pre-dolarización. De igual manera, el flujo de salida post-2020 registra saldos marcadamente negativos, limitando la recuperación de la masa de afiliados cotizantes.
*   **Explicación y Mecanismo**: La emigración masiva constituye una fuga directa de capital humano en edad productiva. Al expulsar físicamente a trabajadores jóvenes que constituyen la base de la pirámide de reparto previsional, el mercado de trabajo ecuatoriano pierde de manera irreversible a cotizantes potenciales. El ratio de soporte del sistema de reparto se degrada severamente, acelerando el agotamiento actuarial de las reservas.

### Panel D: Trayectoria de Informalización Beckeriana (La Radiografía del Colapso)
El **Panel D** es un *connected scatter plot* dinámico que grafica la **Tasa de Homicidios** (eje X) frente a la **Tasa de Cobertura Previsional** (eje Y).

*   **Descripción del Gráfico**: Supera la correlación lineal y traza la secuencia cronológica conjunta. Las etiquetas de hitos históricos específicos (**1990, 1995, 2000, 2008, 2015, 2020, 2024**) demuestran visualmente los cambios de régimen. La trayectoria dibuja un patrón en forma de **"L" invertida**. 
*   **Explicación y Mecanismo**: El tramo vertical ascendente (2001-2015) refleja un régimen de estabilidad institucional y crecimiento de la cobertura a tasas de delincuencia controladas. El tramo horizontal hacia la derecha (2020-2024) demuestra empíricamente la existencia de un **umbral crítico de inestabilidad**: una vez que la tasa de homicidios supera la barrera de los 20 casos por cada 100k hab., la masa de cotizantes del IESS se deprime de manera sistemática. La violencia delictiva extrema bloquea físicamente los incentivos tradicionales a la formalización laboral, revelando la no-linealidad de la precarización previsional.

---

## 4. Evidencia Econométrica e Implicaciones de Política

La estimación de los modelos dinámicos registrados en `logs/Figure_problem.log` confirma matemáticamente la consistencia causal de estos canales:
*   Existe una correlación negativa severa y estadísticamente significativa de **-0.67** entre homicidios y cobertura.
*   La regresión de referencia confirma que la inestabilidad social y la prioridad fiscal en defensa son regresores robustos e individualmente significativos que deprimen la tasa de cobertura previsional a largo plazo.

**Implicación de Política**: Las reformas paramétricas clásicas (modificación de la edad de jubilación o incremento en el porcentaje de cotización) resultan estériles si el Estado no estabiliza de manera prioritaria el entorno institucional de seguridad. El control de la violencia extrema y la reducción del riesgo país son precondiciones obligatorias para permitir la formalización del empleo y restablecer el equilibrio financiero del seguro social de reparto.

---

## 5. Bibliografía

*   **Becker, G. S.** (1968). Crime and punishment: An economic approach. *Journal of Political Economy*, 76(2), 169–217. https://doi.org/10.1086/259394
*   **Diamond, P. A.** (1965). National debt in a neoclassical growth model. *The American Economic Review*, 55(5), 1126–1150. https://www.aeaweb.org/articles?id=10.2307/1816733
*   **Murillo, A., Guerrero, W., & Cuaical, D.** (2025). Factors influencing the probability of affiliation to the social security system among informal sector workers in Ecuador. *Cuestiones Económicas*, 35(1), 107–139.
*   **Samuelson, P. A.** (1958). An exact consumption-loan model of interest with or without the social contrivance of money. *Journal of Political Economy*, 66(6), 467–482. https://doi.org/10.1086/258100
