import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

# 1. Configuración de Estética
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["font.family"] = "sans-serif"

# 2. Carga de Datos
data_path = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/data/raw/csv/Base_Raw_Ecuador_Homicidios_Long.csv"
df = pd.read_csv(data_path)

# Asegurar que los datos están ordenados
df = df.sort_values("year")

# 3. Preparación para series de tiempo interrumpidas (ITS)
# Punto de intervención 1: 2011 (Prohibición de armas)
# Punto de intervención 2: 2019 (Aumento crimen organizado)
int1 = 2011
int2 = 2019

# Crear variables para el modelo
df["time"] = np.arange(len(df))
# Break 1
df["policy1"] = (df["year"] >= int1).astype(int)
df["trend_after_p1"] = (df["year"] - int1).clip(lower=0) * df["policy1"]
# Break 2
df["policy2"] = (df["year"] >= int2).astype(int)
df["trend_after_p2"] = (df["year"] - int2).clip(lower=0) * df["policy2"]

# 4. Modelado Econométrico (OLS con errores robustos Newey-West)
# Corregimos autocorrelación encontrada (DW~0.58)
X = df[["time", "policy1", "trend_after_p1", "policy2", "trend_after_p2"]]
X = sm.add_constant(X)
y = df["homicidios_100k"]

# Usamos Covariance Type 'HAC' (Newey-West) con 1 lag (anual)
model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 1})
print(model.summary())

# Rutas de salida (absolutas para evitar errores)
output_dir = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/acd0-evaluacion-diagnostica/

# guardar resultados para el reporte quarto
results_path = os.path.join(output_dir, "src/model_results.txt")
with open(results_path, "w") as f:
    f.write(model.summary().as_text())

# 5. Visualización de Impacto
plt.figure(figsize=(12, 7))

# Datos observados
sns.scatterplot(
    data=df,
    x="year",
    y="homicidios_100k",
    color="black",
    alpha=0.6,
    label="Homicidios Observados (ENEMDU/INEC)",
)

# Línea de predicción (Modelo Completo)
df["y_pred"] = model.predict(X)
sns.lineplot(
    data=df,
    x="year",
    y="y_pred",
    color="#2563eb",
    linewidth=2.5,
    label="Modelo ITS Doble Quiebre (2011, 2019)",
)

# Línea de contrafactual 1 (Sin política 2011)
X_cf1 = X.copy()
X_cf1[["policy1", "trend_after_p1", "policy2", "trend_after_p2"]] = 0
df["y_cf1"] = model.predict(X_cf1)
sns.lineplot(
    data=df[df["year"] >= int1],
    x="year",
    y="y_cf1",
    color="#dc2626",
    linestyle=":",
    alpha=0.5,
    label="Contrafactual (Sin 2011)",
)

# Línea de contrafactual 2 (Sin quiebre 2019 - Proyección política 2011)
X_cf2 = X.copy()
X_cf2[["policy2", "trend_after_p2"]] = 0
df["y_cf2"] = model.predict(X_cf2)
sns.lineplot(
    data=df[df["year"] >= int2],
    x="year",
    y="y_cf2",
    color="#16a34a",
    linestyle="--",
    alpha=0.6,
    label="Contrafactual (Proyección tendencia 2011)",
)

# Marcadores de intervención
plt.axvline(x=int1, color="#475569", linestyle=":", label="Prohibición Armas (2011)")
plt.axvline(
    x=int2, color="#b45309", linestyle=":", label="Inflexión Inseguridad (2019)"
)

# Estética adicional
plt.title(
    "Impacto en Seguridad Pública: De la Prohibición de Armas a la Crisis Actual",
    fontsize=15,
    fontweight="bold",
    pad=20,
)
plt.xlabel("Año", fontsize=12)
plt.ylabel("Homicidios por cada 100k hab.", fontsize=12)
plt.legend(frameon=True, facecolor="white", framealpha=0.9, loc="upper left")
plt.tight_layout()

# Guardar gráfica
plot_path = os.path.join(output_dir, "graph/impact_homicidios_its.png")
plt.savefig(plot_path, dpi=300)
print(f"✅ Gráfica guardada en: {plot_path}")

# 6. Guardar coeficientes en JSON para Quarto
output_json = {
    "intervention_year": int(int1),
    "crisis_year": int(int2),
    "r_squared": float(model.rsquared),
    "beta_policy1": float(model.params["policy1"]),
    "beta_policy2": float(model.params["policy2"]),
    "p_values": {k: float(v) for k, v in model.pvalues.items()},
}

stats_path = os.path.join(output_dir, "src/stats.json")
with open(stats_path, "w") as f:
    json.dump(output_json, f, indent=4)
