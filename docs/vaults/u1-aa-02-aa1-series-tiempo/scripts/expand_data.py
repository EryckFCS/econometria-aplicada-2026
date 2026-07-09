import pandas as pd

# Load original data
df_orig = pd.read_excel('docs/vaults/u1-aa-02-aa1-series-tiempo/data/aa1_import_function.xlsx', sheet_name='data')

# Load QOG data for controls
df_qog = pd.read_csv('docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/data/raw/external/qog_ecuador.csv')

# Select relevant controls
# wdi_fdiin: FDI net inflows (% of GDP)
# wdi_oilrent: Oil rents (% of GDP)
# wdi_inflation: Inflation, consumer prices (annual %)
controls_cols = ['year', 'wdi_fdiin', 'wdi_oilrent', 'wdi_inflation']
df_controls = df_qog[controls_cols].copy()

# Rename for clarity
df_controls.columns = ['year', 'fdi', 'oil_rent', 'inflation']

# Merge
df_merged = pd.merge(df_orig, df_controls, on='year', how='inner')

# Drop missing values to have a balanced panel/time series
df_final = df_merged.dropna().copy()

# Save as expanded dataset
output_path = 'docs/vaults/u1-aa-02-aa1-series-tiempo/data/aa1_expanded_data.xlsx'
with pd.ExcelWriter(output_path) as writer:
    df_final.to_excel(writer, sheet_name='data', index=False)
    
    # Create dictionary sheet
    dict_data = {
        'Variable': ['year', 'gdp', 'imports', 'fdi', 'oil_rent', 'inflation'],
        'Description': [
            'Año de la observación',
            'Producto Interno Bruto Real (USD constantes)',
            'Importaciones de bienes y servicios (USD constantes)',
            'Inversión Extranjera Directa (% del PIB)',
            'Rentas del Petróleo (% del PIB)',
            'Inflación, precios al consumidor (% anual)'
        ],
        'Source': ['Banco Mundial', 'Banco Mundial', 'Banco Mundial', 'WDI (QOG)', 'WDI (QOG)', 'WDI (QOG)']
    }
    pd.DataFrame(dict_data).to_excel(writer, sheet_name='dictionary', index=False)

print(f"Expanded dataset created at {output_path} with {len(df_final)} observations.")
print(f"Sample range: {int(df_final['year'].min())} - {int(df_final['year'].max())}")
