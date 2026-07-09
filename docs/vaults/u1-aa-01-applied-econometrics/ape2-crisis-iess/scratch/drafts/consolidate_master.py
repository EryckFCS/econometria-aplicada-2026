import os
import pandas as pd

# Definir rutas
data_dir = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/data"
path_base = os.path.join(data_dir, "base_analisis.csv")
path_evo = "/home/erick-fcs/.capital/lake/evolucion_asegurados_iess.csv"
path_masa = "/home/erick-fcs/.capital/lake/raw_data/evolucion_masa_salarial.parquet"

# 1. Cargar bases de datos curadas y oficiales
try:
    df_base = pd.read_csv(path_base)
    df_evo = pd.read_csv(path_evo)
    df_masa = pd.read_parquet(path_masa)
    print("Bases de datos oficiales cargadas con éxito.")
except Exception as e:
    print("Error cargando bases:", e)
    exit(1)

# Estandarizar nombre de columna de tiempo
df_evo.rename(columns={'Año': 'anio'}, inplace=True)
df_masa.rename(columns={'Año': 'anio'}, inplace=True)

# 2. Fusión maquetada
# Realizamos un LEFT JOIN sobre df_base (1990-2024) para mantener la completitud de la muestra de 35 años
# Seleccionamos todas las columnas de evolucion_asegurados_iess.csv excepto 'Total_Afiliados' para evitar redundancias
cols_evo = [col for col in df_evo.columns if col != 'Total_Afiliados']
df_merged = pd.merge(df_base, df_evo[cols_evo], on='anio', how='left')

# Fusionamos la Masa Salarial
df_merged = pd.merge(df_merged, df_masa[['anio', 'Masa_Salarial_Dolares']], on='anio', how='left')

# Convertir tipos
df_merged['Total_Pensionistas'] = df_merged['Total_Pensionistas'].astype(float)
df_merged['Masa_Salarial_Dolares'] = df_merged['Masa_Salarial_Dolares'].astype(float)

# 3. Generar Cobertura de Caja previsional
df_merged['Cobertura_Caja'] = df_merged['Masa_Salarial_Dolares'] / df_merged['Total_Pensionistas']

# Reordenar columnas para una estructura impecable
cols_order = [
    'anio', 'afiliados_iess', 'fuerza_laboral', 'migracion_neta', 
    'gasto_militar_pib', 'rentas_recursos_naturales_pib', 'tasa_homicidios', 'tasa_dependencia_vejez',
    'Masa_Salarial_Dolares', 'Total_Pensionistas', 'Cobertura_Caja',
    'SSC_Jefe_Familia', 'SGO_TNRH', 'SGO_Dependencia', 'SGO_Voluntario',
    'Pensionistas_SSC', 'Pensionistas_IVM', 'Pensionistas_Riesgos',
    'Total_Afiliados_Pensionistas', 'SSC_Dependientes', 'Cobertura_Salud_Ext', 'Total_Asegurados'
]

# Asegurar que todas las columnas existan antes de reordenar
cols_to_use = [col for col in cols_order if col in df_merged.columns]
df_master = df_merged[cols_to_use]

# 4. Guardar la Base Maestra única
parquet_output = os.path.join(data_dir, "master_previsional_ecuador.parquet")
excel_output = os.path.join(data_dir, "master_previsional_ecuador.xlsx")

try:
    df_master.to_parquet(parquet_output, index=False)
    df_master.to_excel(excel_output, index=False, sheet_name="Master_Previsional_Ecuador")
    print("\n✅ Base maestra consolidada y guardada con éxito en la bóveda:")
    print(f"   - Parquet: {parquet_output}")
    print(f"   - Excel:   {excel_output}")
    print(f"   - Cantidad de observaciones: {len(df_master)} (1990-2024)")
    print(f"   - Cantidad de variables:     {df_master.shape[1]}")
except Exception as e:
    print("Error guardando archivos:", e)

# 5. Limpieza de archivos temporales/repetidos de la bóveda
print("\n🧹 Iniciando limpieza de bases de datos duplicadas y transitorias...")
# Eliminar erick.condoy.csv
dup_csv = os.path.join(data_dir, "erick.condoy.csv")
if os.path.exists(dup_csv):
    try:
        os.remove(dup_csv)
        print(f"   - Eliminada duplicación transitoria: {dup_csv}")
    except Exception as e:
        print("Error eliminando erick.condoy.csv:", e)

# Eliminar carpeta processed/ y su contenido redundante
processed_dir = os.path.join(data_dir, "processed")
if os.path.exists(processed_dir):
    try:
        import shutil
        shutil.rmtree(processed_dir)
        print(f"   - Eliminada carpeta de procesamiento temporal: {processed_dir}")
    except Exception as e:
        print("Error eliminando processed dir:", e)

# Eliminar carpeta raw/ y su contenido redundante
raw_dir = os.path.join(data_dir, "raw")
if os.path.exists(raw_dir):
    try:
        import shutil
        shutil.rmtree(raw_dir)
        print(f"   - Eliminada carpeta de datos crudos temporales: {raw_dir}")
    except Exception as e:
        print("Error eliminando raw dir:", e)

# Eliminar carpeta metadata/ si existe y no es crítica
meta_dir = os.path.join(data_dir, "metadata")
if os.path.exists(meta_dir):
    try:
        import shutil
        shutil.rmtree(meta_dir)
        print(f"   - Eliminada carpeta de metadatos temporales: {meta_dir}")
    except Exception as e:
        print("Error eliminando metadata dir:", e)

print("\n✨ Limpieza de la bóveda de datos completada con éxito.")
