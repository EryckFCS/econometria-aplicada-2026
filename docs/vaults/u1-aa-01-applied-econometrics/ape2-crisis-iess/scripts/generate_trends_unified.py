import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar estilo visual premium
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16,
    'legend.fontsize': 10,
    'figure.dpi': 300
})

# 1. Cargar datos
base_path = "data/base_analisis.csv"
df = pd.read_csv(base_path)

# 2. Indexación a Base 100 en 1990 (para homogeneizar escalas de evolución)
# Para la migración neta, al tener valores negativos y fluctuar en torno a cero,
# aplicamos una normalización Min-Max [0, 100] para representar su evolución
# en el mismo rango visual.
df_indexed = pd.DataFrame()
df_indexed['Año'] = df['anio']

# Afiliados y Fuerza Laboral (Base 100 = 1990)
df_indexed['Afiliados IESS (Ind. 1990=100)'] = (df['afiliados_iess'] / df['afiliados_iess'].iloc[0]) * 100
df_indexed['Fuerza Laboral (Ind. 1990=100)'] = (df['fuerza_laboral'] / df['fuerza_laboral'].iloc[0]) * 100

# Gasto Militar e Homicidios (Base 100 = 1990)
df_indexed['Gasto Militar % PIB (Ind. 1990=100)'] = (df['gasto_militar_pib'] / df['gasto_militar_pib'].iloc[0]) * 100
df_indexed['Tasa de Homicidios (Ind. 1990=100)'] = (df['tasa_homicidios'] / df['tasa_homicidios'].iloc[0]) * 100

# Migración Neta (Min-Max 0-100 para evitar divisiones por valores negativos en la base 100)
min_mig = df['migracion_neta'].min()
max_mig = df['migracion_neta'].max()
df_indexed['Migración Neta (Escala Min-Max 0-100)'] = ((df['migracion_neta'] - min_mig) / (max_mig - min_mig)) * 100

# 3. Graficar en una sola panel
fig, ax = plt.subplots(figsize=(12, 7))

# Definir colores de alta gama (curados y premium)
colors = {
    'Afiliados IESS (Ind. 1990=100)': '#0d47a1',          # Azul oscuro institucional
    'Fuerza Laboral (Ind. 1990=100)': '#4a148c',          # Púrpura profundo
    'Gasto Militar % PIB (Ind. 1990=100)': '#ef6c00',     # Naranja cobrizo
    'Tasa de Homicidios (Ind. 1990=100)': '#b71c1c',      # Rojo carmesí
    'Migración Neta (Escala Min-Max 0-100)': '#00695c'    # Verde esmeralda oscuro
}

# Estilos de línea para diferenciar
linestyles = {
    'Afiliados IESS (Ind. 1990=100)': '-',
    'Fuerza Laboral (Ind. 1990=100)': '--',
    'Gasto Militar % PIB (Ind. 1990=100)': '-.',
    'Tasa de Homicidios (Ind. 1990=100)': '-',
    'Migración Neta (Escala Min-Max 0-100)': ':'
}

# Trazar cada serie
for col in df_indexed.columns:
    if col == 'Año':
        continue
    ax.plot(
        df_indexed['Año'], 
        df_indexed[col], 
        label=col, 
        color=colors[col], 
        linestyle=linestyles[col],
        linewidth=2.5 if col in ['Afiliados IESS (Ind. 1990=100)', 'Tasa de Homicidios (Ind. 1990=100)'] else 1.8
    )

# 4. Anotaciones de Hitos de Cambios Estructurales y Polémicas Históricas
# Feriado Bancario y Dolarización (2000)
ax.axvline(x=2000, color='gray', linestyle=':', alpha=0.7)
ax.text(2000.3, 150, '2000: Feriado Bancario\ny Dolarización', fontsize=9, color='#424242', weight='bold')

# Constitución de Montecristi (2008)
ax.axvline(x=2008, color='gray', linestyle=':', alpha=0.7)
ax.text(2008.3, 220, '2008: Reforma\nConstitucional', fontsize=9, color='#424242', weight='bold')

# Penalización del IESS (COIP 2014) y Retiro del 40% (2015)
ax.axvline(x=2014, color='gray', linestyle=':', alpha=0.7)
ax.text(2011.5, 310, '2014: Penalización No Afiliación\n2015: Retiro del aporte 40%', fontsize=9, color='#424242', weight='bold')

# Ola de Violencia Extrema (2020-2024)
ax.axvline(x=2020, color='gray', linestyle=':', alpha=0.7)
ax.text(2020.3, 50, '2020: Pandemia y\nEstallido Criminal', fontsize=9, color='#b71c1c', weight='bold')

# Configuración de ejes y etiquetas
ax.set_title('Trayectoria Longitudinal Homogénea de las Series de Investigación (1990-2024)', pad=20, weight='bold')
ax.set_xlabel('Año', labelpad=10)
ax.set_ylabel('Índice de Evolución Relativa (Base 100 = 1990)', labelpad=10)
ax.set_xlim(1990, 2024)
ax.set_xticks(range(1990, 2025, 5))

# Añadir una línea de referencia base 100
ax.axhline(y=100, color='black', linestyle='-', linewidth=0.8, alpha=0.5)

# Colocar la leyenda de forma premium en la parte superior izquierda
ax.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='none', shadow=True)

# Guardar figura de alta definición
plt.tight_layout()
output_path = "assets/fig-evolucion-unica.png"
plt.savefig(output_path, dpi=300)
print(f"Gráfica premium guardada en: {output_path}")
