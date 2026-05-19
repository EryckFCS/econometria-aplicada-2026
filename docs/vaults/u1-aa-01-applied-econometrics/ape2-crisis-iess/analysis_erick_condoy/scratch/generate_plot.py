import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
data_path = '/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/analysis_erick_condoy/data/base_analisis.csv'
df = pd.read_csv(data_path)

# Variables
# Independent: gasto_militar_pib (GM) - Hypothesis: Crowding out effect
# Control: fuerza_laboral (FL) - Scale of economy
x = df['gasto_militar_pib']
y = df['fuerza_laboral'] / 1e6 # Millions
years = df['anio']

# Setup Style: Dark & Premium
plt.rcParams['font.family'] = 'sans-serif'
fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
fig.patch.set_facecolor('#0b0f19')
ax.set_facecolor('#0b0f19')

# Create a custom color gradient for the timeline
norm = plt.Normalize(years.min(), years.max())
cmap = plt.get_cmap('magma') # 'magma' gives a premium purple-orange-yellow look

# Plot lines connecting years (Story path)
for i in range(len(years) - 1):
    ax.plot(x[i:i+2], y[i:i+2], color=cmap(norm(years[i])), alpha=0.6, lw=2.5, solid_capstyle='round', zorder=1)

# Scatter points with color gradient
sc = ax.scatter(x, y, c=years, cmap='magma', s=120, edgecolors='#ffffff', linewidth=0.8, alpha=0.9, zorder=2)

# Annotations for key historical moments
# 1. 1995: War of Cenepa (High Military Spending)
# 2. 2000: Dollarization
# 3. 2014: High Oil Prices period
# 4. 2020: Pandemic
key_points = {
    1995: ("Guerra del Cenepa\n(Pico de Gasto Militar)", -0.1, 0.2),
    2000: ("Dolarización\n(Inestabilidad Económica)", 0.2, 0.1),
    2014: ("Bonanza Petrolera", -0.1, 0.1),
    2023: ("Crisis de Seguridad", 0.1, -0.1)
}

for yr, (label, dx, dy) in key_points.items():
    if yr in years.values:
        idx = df[df['anio'] == yr].index[0]
        ax.annotate(f"{yr}: {label}", 
                    xy=(x[idx], y[idx]), 
                    xytext=(x[idx] + dx, y[idx] + dy),
                    color='#e2e8f0', fontsize=10, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color='#fbbf24', lw=1.5, connectionstyle="arc3,rad=.2"),
                    bbox=dict(boxstyle='round,pad=0.3', fc='#1e293b', alpha=0.8, ec='#fbbf24', lw=0.5))

# Axes Labels & Aesthetic Polish
ax.set_xlabel('Gasto Militar (% del PIB)', fontsize=13, color='#94a3b8', labelpad=15, fontweight='500')
ax.set_ylabel('Fuerza Laboral (Millones de Personas)', fontsize=13, color='#94a3b8', labelpad=15, fontweight='500')

# Grid
ax.grid(color='#1e293b', linestyle='--', alpha=0.4, zorder=0)

# Remove spines
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#334155')
ax.spines['bottom'].set_color('#334155')
ax.tick_params(colors='#64748b', which='both', labelsize=11)

# Title & Description (The "Story")
plt.text(0.01, 1.08, 'Evolución de la Fuerza Laboral vs. Presión del Gasto Militar (1990-2024)', 
         transform=ax.transAxes, fontsize=20, color='#ffffff', fontweight='bold')
plt.text(0.01, 1.03, 'El gráfico muestra la trayectoria histórica de la economía ecuatoriana: cómo el mercado laboral se expande mientras\nla asignación presupuestaria militar fluctúa ante conflictos, crisis y bonanzas.', 
         transform=ax.transAxes, fontsize=12, color='#94a3b8', linespacing=1.5)

# Colorbar for year
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = fig.colorbar(sc, cax=cbar_ax)
cbar.set_label('Año', color='#94a3b8', size=11, labelpad=10)
cbar.ax.tick_params(colors='#94a3b8')
cbar.outline.set_edgecolor('#334155')

# Save result
output_path = '/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/analysis_erick_condoy/assets/correlation_story_militar_laboral.png'
plt.savefig(output_path, facecolor='#0b0f19', bbox_inches='tight')
print(f"Graph saved at: {output_path}")
