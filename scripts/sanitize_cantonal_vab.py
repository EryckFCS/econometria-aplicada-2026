#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para sanitizar y estructurar en formato de panel de datos largo (long format)
el VAB cantonal del Ecuador para el periodo 2007-2024.
"""

import pathlib
import pandas as pd
import numpy as np

# Rutas de archivos
BASE_DIR = pathlib.Path("/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026")
INPUT_FILE = BASE_DIR / "docs/vaults/u3-acd-01-datos-de-panel-entregable/data/raw/Boletin_retropolacion_regionales_2007_2024p_val.xlsx"
OUTPUT_DIR = BASE_DIR / "docs/vaults/u3-acd-01-datos-de-panel-entregable/data/processed"
OUTPUT_FILE = OUTPUT_DIR / "panel_vab_cantonal.csv"

def main():
    print("Iniciando sanitización del VAB Cantonal...")
    
    # 1. Asegurar directorio de salida
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"No se encontró el archivo de entrada en: {INPUT_FILE}")
    
    # 2. Cargar datos especificando la fila 8 como cabecera (header=8)
    print(f"Cargando archivo: {INPUT_FILE.name}")
    df = pd.read_excel(INPUT_FILE, sheet_name="VAB cantonal", header=8)
    
    # 3. Limpiar y filtrar filas no deseadas
    # Descartamos las filas vacías y las filas de totales/notas que no tienen código cantonal
    df = df.dropna(subset=["CÓDIGO CANTÓN"])
    
    # 4. Formatear códigos de provincia y cantón
    # Asegurar ceros a la izquierda (2 dígitos para provincia, 4 para cantón)
    df["CÓDIGO PROVINCIA"] = df["CÓDIGO PROVINCIA"].astype(float).astype(int).astype(str).str.zfill(2)
    df["CÓDIGO CANTÓN"] = df["CÓDIGO CANTÓN"].astype(float).astype(int).astype(str).str.zfill(4)
    
    # Limpiar nombres de cantón y provincia
    df["PROVINCIA"] = df["PROVINCIA"].astype(str).str.strip()
    df["CANTÓN"] = df["CANTÓN"].astype(str).str.strip()
    
    # 5. Normalizar nombres de columnas iniciales
    df = df.rename(columns={
        "CÓDIGO PROVINCIA": "codigo_provincia",
        "PROVINCIA": "provincia",
        "CÓDIGO CANTÓN": "codigo_canton",
        "CANTÓN": "canton"
    })
    
    # 6. Transformación a formato largo (melt)
    id_vars = ["codigo_provincia", "provincia", "codigo_canton", "canton"]
    value_vars = [col for col in df.columns if col not in id_vars]
    
    df_long = df.melt(
        id_vars=id_vars,
        value_vars=value_vars,
        var_name="anio_raw",
        value_name="vab"
    )
    
    # 7. Limpiar la columna de año
    # Ejemplos: 2007.0 -> 2007, '2024 (p)' -> 2024
    df_long["anio"] = df_long["anio_raw"].astype(str).str.extract(r"(\d{4})").astype(int)
    df_long = df_long.drop(columns=["anio_raw"])
    
    # 8. [imputation] Tratamiento de ceros en cantones de reciente creación
    # Reemplazar 0.0 por NaN para indicar que el cantón no existía o no reportaba de forma independiente
    # esto previene distorsiones y sesgos en el cálculo de elasticidades o crecimiento.
    df_long["vab"] = df_long["vab"].replace(0.0, np.nan)
    
    # 9. Calcular participación del cantón en el VAB de su provincia por año (%)
    # Se calcula sobre los datos limpios (si el VAB es NaN, la participación también será NaN)
    df_long["vab_provincial_total"] = df_long.groupby(["codigo_provincia", "anio"])["vab"].transform("sum")
    df_long["participacion_provincial"] = (df_long["vab"] / df_long["vab_provincial_total"]) * 100
    df_long = df_long.drop(columns=["vab_provincial_total"])
    
    # Reordenar columnas para presentación canónica de panel
    df_panel = df_long[[
        "codigo_provincia",
        "provincia",
        "codigo_canton",
        "canton",
        "anio",
        "vab",
        "participacion_provincial"
    ]].sort_values(by=["codigo_canton", "anio"]).reset_index(drop=True)
    
    # 10. Guardar dataset de VAB sanitizado completo (2007-2024)
    df_panel.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"Dataset de panel de VAB sanitizado y guardado en: {OUTPUT_FILE}")
    
    # 11. Integrar con el panel de empleo y empresas (2015-2024)
    PANEL_EXT_FILE = BASE_DIR / "docs/vaults/u3-acd-01-datos-de-panel/data/datos_de_panel_sanitized.xlsx"
    CONSOLIDATED_FILE = OUTPUT_DIR / "panel_cantonal_consolidado.csv"
    
    if PANEL_EXT_FILE.exists():
        print(f"Cargando panel de empleo y empresas: {PANEL_EXT_FILE.name}")
        df_ext = pd.read_excel(PANEL_EXT_FILE)
        
        # Formatear llaves de cruce
        df_ext["canton_id"] = df_ext["canton_id"].astype(float).astype(int).astype(str).str.zfill(4)
        df_ext = df_ext.rename(columns={"year": "anio", "canton_id": "codigo_canton"})
        
        # Filtrar columnas de metadatos repetidas antes del merge
        df_ext_clean = df_ext[["codigo_canton", "anio", "vab_group", "num_emp", "ventas_totales", "empleo_prom", "plazas"]]
        
        # Hacer merge (cruce)
        # Usamos inner ya que limitamos el panel al periodo común 2015-2024
        df_consolidated = pd.merge(
            df_panel,
            df_ext_clean,
            on=["codigo_canton", "anio"],
            how="inner"
        )
        
        # Ordenar el panel de forma consistente
        df_consolidated = df_consolidated.sort_values(by=["codigo_canton", "anio"]).reset_index(drop=True)
        
        # Guardar base final
        df_consolidated.to_csv(CONSOLIDATED_FILE, index=False, encoding="utf-8")
        print(f"Dataset consolidado final (2015-2024) guardado en: {CONSOLIDATED_FILE}")
        
        # Validación final
        print("Validación del panel consolidado final:")
        print(f"  - Cantones únicos: {df_consolidated['codigo_canton'].nunique()}")
        print(f"  - Años cubiertos: {df_consolidated['anio'].min()} a {df_consolidated['anio'].max()}")
        print(f"  - Columnas en base final: {df_consolidated.columns.tolist()}")
        print(f"  - Total de registros: {len(df_consolidated)}")
    else:
        print(f"ADVERTENCIA: No se encontró el archivo de empleo y empresas en: {PANEL_EXT_FILE}")

if __name__ == "__main__":
    main()
