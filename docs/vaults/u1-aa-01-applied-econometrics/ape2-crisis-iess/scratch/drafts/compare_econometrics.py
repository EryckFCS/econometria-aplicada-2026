import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col

# 1. Cargar bases
path_base = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/analysis_erick_condoy/data/base_analisis.csv"
path_evo = "/home/erick-fcs/.capital/lake/evolucion_asegurados_iess.csv"
path_masa = "/home/erick-fcs/.capital/lake/raw_data/evolucion_masa_salarial.parquet"

df_base = pd.read_csv(path_base)
df_evo = pd.read_csv(path_evo)
df_masa = pd.read_parquet(path_masa)

# Estandarizar columnas de año
df_base.rename(columns={'anio': 'anio'}, inplace=True)
df_evo.rename(columns={'Año': 'anio'}, inplace=True)
df_masa.rename(columns={'Año': 'anio'}, inplace=True)

# 2. Fusiones
df = pd.merge(df_base, df_evo[['anio', 'Total_Pensionistas']], on='anio', how='inner')
df = pd.merge(df, df_masa[['anio', 'Masa_Salarial_Dolares']], on='anio', how='inner')

# Convertir tipos
df['Total_Pensionistas'] = df['Total_Pensionistas'].astype(float)
df['Masa_Salarial_Dolares'] = df['Masa_Salarial_Dolares'].astype(float)

# 3. Generación de Variables
df['AF'] = np.log(df['afiliados_iess'])
df['GM'] = df['gasto_militar_pib']
df['RR'] = df['rentas_recursos_naturales_pib']
df['MI'] = df['migracion_neta'] / 1000 # Escalar a miles para coeficientes legibles
df['HO'] = np.log(df['tasa_homicidios'])
df['FL'] = np.log(df['fuerza_laboral'])

# Previsionales
df['MS'] = np.log(df['Masa_Salarial_Dolares'])
df['PE'] = np.log(df['Total_Pensionistas'])
df['COV'] = df['Masa_Salarial_Dolares'] / df['Total_Pensionistas']
df['ln_COV'] = np.log(df['COV'])

print(f"Data merged successfully. Sample size: {len(df)} observations (years {df['anio'].min()} to {df['anio'].max()}).\n")

# 4. Regresiones
# Variable Dependiente: Log Afiliados (AF)
X_base_gm = sm.add_constant(df[['GM', 'MI', 'HO', 'FL']])
X_base_rr = sm.add_constant(df[['RR', 'MI', 'HO', 'FL']])

m1 = sm.OLS(df['AF'], X_base_gm).fit()
m2 = sm.OLS(df['AF'], X_base_rr).fit()

# Variable Dependiente: Cobertura de Caja (COV)
m3 = sm.OLS(df['COV'], X_base_gm).fit()
m4 = sm.OLS(df['COV'], X_base_rr).fit()

# Variable Dependiente: Log Cobertura de Caja (ln_COV)
m5 = sm.OLS(df['ln_COV'], X_base_gm).fit()
m6 = sm.OLS(df['ln_COV'], X_base_rr).fit()

# Variable Dependiente: Log Masa Salarial (MS)
m7 = sm.OLS(df['MS'], X_base_gm).fit()
m8 = sm.OLS(df['MS'], X_base_rr).fit()

# 5. Comparaciones
print("==========================================================================")
print("COMPARE 1: DEPENDIENTE = Log Afiliados (AF) (M1: con GM vs M2: con RR)")
print("==========================================================================")
print(summary_col([m1, m2], stars=True, model_names=['AF (GM)', 'AF (RR)'], info_dict={'R2': lambda x: f"{x.rsquared:.4f}", 'Adj R2': lambda x: f"{x.rsquared_adj:.4f}", 'AIC': lambda x: f"{x.aic:.2f}"}))

print("\n==========================================================================")
print("COMPARE 2: DEPENDIENTE = Cobertura de Caja (COV) (M3: con GM vs M4: con RR)")
print("==========================================================================")
print(summary_col([m3, m4], stars=True, model_names=['COV (GM)', 'COV (RR)'], info_dict={'R2': lambda x: f"{x.rsquared:.4f}", 'Adj R2': lambda x: f"{x.rsquared_adj:.4f}", 'AIC': lambda x: f"{x.aic:.2f}"}))

print("\n==========================================================================")
print("COMPARE 3: DEPENDIENTE = Log Cobertura de Caja (ln_COV) (M5: con GM vs M6: con RR)")
print("==========================================================================")
print(summary_col([m5, m6], stars=True, model_names=['ln_COV (GM)', 'ln_COV (RR)'], info_dict={'R2': lambda x: f"{x.rsquared:.4f}", 'Adj R2': lambda x: f"{x.rsquared_adj:.4f}", 'AIC': lambda x: f"{x.aic:.2f}"}))

print("\n==========================================================================")
print("COMPARE 4: DEPENDIENTE = Log Masa Salarial (MS) (M7: con GM vs M8: con RR)")
print("==========================================================================")
print(summary_col([m7, m8], stars=True, model_names=['MS (GM)', 'MS (RR)'], info_dict={'R2': lambda x: f"{x.rsquared:.4f}", 'Adj R2': lambda x: f"{x.rsquared_adj:.4f}", 'AIC': lambda x: f"{x.aic:.2f}"}))

print("\n==========================================================================")
print("CORRELATION BETWEEN VARIABLES:")
print("==========================================================================")
print(df[['AF', 'MS', 'PE', 'COV', 'ln_COV', 'GM', 'RR', 'MI', 'HO', 'FL']].corr())
