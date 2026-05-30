---
name: investment-project-analysis
description: Evaluación financiera avanzada de proyectos de inversión públicos y privados, simulación estocástica Monte Carlo de flujos de caja, y análisis de sensibilidad sobre VAN y TIR.
version: 1.0.0
---

# SKILL: Análisis de Proyectos de Inversión y Modelado Monte Carlo

Esta habilidad dota al agente del criterio y las herramientas de código en Python necesarias para evaluar financieramente proyectos de inversión privados y de desarrollo social, calculando métricas de rentabilidad determinísticas y modelando la incertidumbre de flujos futuros a través de simulaciones estocásticas Monte Carlo.

---

## 1. Métricas Financieras Fundamentales

### A. Valor Actual Neto (VAN / NPV)
El valor presente de los flujos de efectivo netos (beneficios menos costos) descontados a una tasa de descuento de oportunidad ($r$):
$$VAN = -I_0 + \sum_{t=1}^{n} \frac{FC_t}{(1 + r)^t}$$

Donde:
- $I_0$: Inversión inicial requerida.
- $FC_t$: Flujo de caja en el período $t$.
- $r$: Tasa de Descuento de Oportunidad (WACC o tasa social de descuento).

### B. Tasa Interna de Retorno (TIR / IRR)
La tasa de descuento que hace que el VAN sea exactamente igual a cero:
$$0 = -I_0 + \sum_{t=1}^{n} \frac{FC_t}{(1 + TIR)^t}$$

---

## 2. Simulación Estocástica Monte Carlo de Flujos de Caja

En proyectos del mundo real (e.g. evaluación del proyecto de inversión en Bambú `eco_bambu`), variables clave como el precio del producto, el costo de los insumos y la demanda no son estáticos, sino que siguen distribuciones probabilísticas (Normal, Triangular, Lognormal). 

A continuación se presenta un algoritmo completo en Python para modelar flujos de caja estocásticos y derivar la distribución del VAN y la probabilidad de pérdida.

```python
import numpy as np
import numpy_financial as npf
import pandas as pd
from loguru import logger

def simulate_project_monte_carlo(
    initial_investment: float,
    years: int,
    wacc: float,
    iterations: int = 10000
) -> pd.DataFrame:
    """
    Simula estocásticamente el VAN de un proyecto modelando incertidumbre
    en precios (Normal) y costos operativos (Triangular).
    """
    logger.info(f"Iniciando simulación Monte Carlo con {iterations} iteraciones...")
    
    results = []
    
    for i in range(iterations):
        # 1. Modelar variables estocásticas
        # El precio promedio es $40 con desviación de $5 (dist. normal)
        simulated_prices = np.random.normal(loc=40.0, scale=5.0, size=years)
        
        # El volumen de ventas anual tiene dist. triangular
        simulated_volume = np.random.triangular(left=8000, mode=10000, right=13000, size=years)
        
        # Costo operativo porcentual (entre 45% y 55% de los ingresos)
        op_cost_pct = np.random.uniform(low=0.45, high=0.55, size=years)
        
        # 2. Reconstruir flujos de caja anuales
        revenues = simulated_prices * simulated_volume
        costs = revenues * op_cost_pct
        cash_flows = revenues - costs
        
        # Insertar inversión inicial en el período 0
        all_cash_flows = np.insert(cash_flows, 0, -initial_investment)
        
        # 3. Calcular VAN e TIR
        # npf.npv espera una lista de flujos descontada desde el periodo 1 en adelante y suma el periodo 0 aparte
        npv = npf.npv(wacc, all_cash_flows)
        
        try:
            irr = npf.irr(all_cash_flows)
        except Exception:
            irr = np.nan
            
        results.append({
            "iteration": i,
            "npv": npv,
            "irr": irr
        })
        
    df_results = pd.DataFrame(results)
    
    # 4. Calcular métricas de decisión cuantitativas
    prob_negative_npv = (df_results["npv"] < 0).mean() * 100
    mean_npv = df_results["npv"].mean()
    
    logger.success(
        f"Simulación completa -> VAN Promedio: ${mean_npv:,.2f} | "
        f"Probabilidad de Pérdida (VAN < 0): {prob_negative_npv:.2f}%"
    )
    return df_results
```

---

## 3. Análisis de Sensibilidad (Tornado Plot)

El agente debe poder aislar y medir el impacto individual de cada parámetro en el VAN del proyecto. Esto se realiza modificando un único parámetro clave a la vez en rangos específicos (e.g., $-20\%$ a $+20\%$) mientras se mantienen los demás en sus valores base.
- Si el VAN es extremadamente sensible al costo de la materia prima, la recomendación de inversión estratégica debe centrarse en mitigar este riesgo específico mediante contratos de cobertura de precio fijo.
- Si el VAN se mantiene positivo bajo estrés severo (TIR $>$ costo de capital en todos los escenarios), el proyecto se califica como **altamente robusto**.
EOF
