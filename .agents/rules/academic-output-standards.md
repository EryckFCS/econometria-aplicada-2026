# RULE: Estándares de Entregables Académicos (UNL)

- **Activación**: `model-decision`
- **Ámbito**: Jupyter Notebooks (`glob: "**/*.ipynb"`), reportes y repositorios académicos/UNL
- **Versión**: 1.0.0

---

## 1. Declaración de Política

Todos los entregables académicos, análisis econométricos y notebooks destinados a proyectos de la Universidad Nacional de Loja (UNL) deben cumplir con los máximos estándares de rigor científico, estructuración metodológica y reproducibilidad. Los notebooks no son meros borradores de código: son documentos científicos integrados donde la prosa markdown académica justifica, detalla e interpreta rigurosamente los bloques de código y sus resultados empíricos.

---

## 2. Restricciones Específicas y Accionables

1. **Orden Secuencial Estricto**: Todo notebook debe ser ejecutable de principio a fin sin dependencias de ejecución cruzadas o celdas fuera de orden (ejecutar `Kernel -> Restart & Run All` debe funcionar al 100% sin excepciones).
2. **Cero Salidas de Debug Sucias**: Queda vetada la entrega de notebooks con trazas de error masivas no resueltas, prints de variables internas temporales, o tablas crudas de miles de líneas sin formatear.
3. **Estructura Metodológica Formal**: Todo notebook de investigación debe comenzar con un encabezado formal que incluya: Título Científico, Autor (Erick Condoy), Resumen, y seguir la estructura estándar:
   - *1. Introducción y Marco Teórico*
   - *2. Metodología Econométrica y Datos*
   - *3. Análisis Exploratorio y Tratamiento (Dollar Bars / Vectorial)*
   - *4. Estimación y Resultados Empíricos*
   - *5. Conclusiones y Referencias Bibliográficas*
4. **Visualizaciones Profesionales**: Todos los gráficos generados (Matplotlib, Seaborn o Plotly) deben poseer etiquetas de ejes claras, títulos descriptivos, leyendas de unidades, y utilizar una paleta de colores sobria y consistente (vetados colores primarios crudos).
5. **Citación Formal**: Todo modelo o suposición no trivial incorporada debe citar su paper o documento oficial de referencia.

---

## 3. Ejemplo de Estructura de Celda Académica

❌ **INCORRECTO (Desordenado, sin explicaciones ni formato)**
```python
# Celda 1 (sin contexto)
import pandas as pd
data = pd.read_csv('raw_enemdu.csv')

# Celda 2 (código de scraping/limpieza y visualización mezclada)
data['ingreso'] = data['ingreso'].apply(lambda x: x if x > 0 else None)
print(data.describe())
import matplotlib.pyplot as plt
plt.plot(data['ingreso'])
```

   **CORRECTO (Estructurado y justificado científicamente)**

*Celda Markdown:*
> ### 3.1. Tratamiento e Imputación de Ingresos Laborales
> Siguiendo los lineamientos metodológicos del INEC para la ENEMDU, se realiza un proceso de limpieza de ingresos declarados nulos o negativos para evitar distorsiones en la estimación del coeficiente de informalidad. Los ingresos menores o iguales a cero son tratados como datos faltantes (`NaN`) y el análisis se restringe a la población ocupada con ingresos positivos.

*Celda Código:*
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from loguru import logger

def process_academic_dataset(file_path: str) -> pd.DataFrame:
    """Prepara el dataset de empleo ENEMDU bajo estándares académicos rigurosos."""
    logger.info("Iniciando depuración de ingresos de empleo...")
    df = pd.read_csv(file_path)
    
    # Tratamiento inmutable de ingresos ausentes/nulos
    df["ingreso_procesado"] = df["ingreso_mensual"].apply(
        lambda x: x if x > 0 else np.nan
    )
    
    # Mostrar resumen formateado para el paper
    summary_stats = df["ingreso_procesado"].describe().to_frame()
    logger.success("Depuración finalizada con éxito.")
    return df
```
