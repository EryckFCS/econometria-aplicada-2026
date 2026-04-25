import logging
from pathlib import Path
import pandas as pd
import statsmodels.api as sm
from ecs_quantitative.reporting import draw_impact_arc, draw_radar_impact

"""
ORQUESTADOR T04-U1-ACD: SEM Homicidios Ecuador
Unidad 1: Econometría Aplicada
Nomenclatura: T04-U1-ACD-SEM_Homicidios
Propósito: Modelado de sistemas de ecuaciones simultáneas para determinantes de violencia.
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("T04-U1-ACD")

# --- ESPECIFICACIÓN DEL SISTEMA SEM (Metadata) ---
# Definimos la estructura del sistema para el reporte institucional
SEM_SPECIFICATION = {
    "model_id": "SEM-01-HOMICIDIOS",
    "description": "Sistema de Ecuaciones Simultáneas: Violencia y Dinámica Socioeconómica",
    "equations": [
        {
            "target": "homicidios_100k",
            "predictors": [
                "desempleo_total_ne",
                "gasto_militar_pct_pib",
                "remesas_pct_pib",
            ],
            "label": "Ecuación de Seguridad (Violencia)",
        },
        {
            "target": "desempleo_total_ne",
            "predictors": ["remesas_pct_pib", "uso_internet_pct"],
            "label": "Ecuación Socio-Urbana (Laboral)",
        },
    ],
}


def run_task():
    print("🚀 Iniciando Auditoría y Preparación de Taller SEM (Homicidios)...")

    # 1. Rutas de Datos
    data_path = Path("data/raw/local/Base_Raw_Ecuador_Homicidios_Long.csv")
    if not data_path.exists():
        logger.error(
            f"❌ Error: La base de datos {data_path} no existe. Ejecute T01 primero."
        )
        return

    # 2. Cargar datos para validación de estructura
    df = pd.read_csv(data_path)
    logger.info(
        f"✅ Datos cargados: {len(df)} observaciones y {len(df.columns)} variables."
    )

    # 3. Preparar Repositorio de Evidencia (Bóveda)
    evidence_path = Path("docs/evidence/U1-Applied-Econometrics/ACD2-SEM-Homicidios")
    evidence_path.mkdir(parents=True, exist_ok=True)

    # 4. Generar reporte preliminar de variables para el taller
    print("\n📦 Variables identificadas para el sistema SEM:")
    for eq in SEM_SPECIFICATION["equations"]:
        print(f"  🔹 {eq['label']}:")
        print(f"     Target: {eq['target']}")
        print(f"     Predictores: {', '.join(eq['predictors'])}")

    # --- 5. Estimación Estadística (Significancia para Gráficos) ---
    print("\n📊 Estimando impactos estructurales...")
    impacts1, impacts2 = {}, {}
    try:
        df_reg = df.dropna(
            subset=[
                "homicidios_100k",
                "desempleo_total_ne",
                "gasto_militar_pct_pib",
                "remesas_pct_pib",
                "uso_internet_pct",
            ]
        )

        # Ecuación 1: Seguridad
        y1 = df_reg["homicidios_100k"]
        X1 = sm.add_constant(
            df_reg[["desempleo_total_ne", "gasto_militar_pct_pib", "remesas_pct_pib"]]
        )
        res1 = sm.OLS(y1, X1).fit()
        impacts1 = {
            var: max(0, 1 - res1.pvalues[var]) for var in X1.columns if var != "const"
        }

        # Ecuación 2: Laboral
        y2 = df_reg["desempleo_total_ne"]
        X2 = sm.add_constant(df_reg[["remesas_pct_pib", "uso_internet_pct"]])
        res2 = sm.OLS(y2, X2).fit()
        impacts2 = {
            var: max(0, 1 - res2.pvalues[var]) for var in X2.columns if var != "const"
        }
    except Exception as e:
        logger.error(f"❌ Error en estimación: {e}")

    # --- 6. Generar Gráficos de Impacto (Significancia y Proximidad) ---
    graph_path = evidence_path / "graph"
    graph_path.mkdir(exist_ok=True)

    print("\n🎨 Generando infografías de impacto (Arco SEM)...")
    try:
        # Gráfico 1: Seguridad
        draw_impact_arc(
            target_name="Homicidios (100k)",
            impacts_dict=impacts1
            if impacts1
            else {"desempleo": 0.5, "gasto_militar": 0.5, "remesas": 0.5},
            output_path=str(graph_path / "impact_homicidios.png"),
            title_prefix="SISTEMA SEM",
        )
        # Gráfico 2: Laboral
        draw_impact_arc(
            target_name="Desempleo Total",
            impacts_dict=impacts2
            if impacts2
            else {"remesas": 0.5, "uso_internet": 0.5},
            output_path=str(graph_path / "impact_laboral.png"),
            title_prefix="SISTEMA SEM",
        )
        print(f"✅ Infografías generadas en: {graph_path}")
    except Exception as e:
        logger.error(f"❌ Error generando gráficos de arco: {e}")

    # --- 7. Radar Chart (Spider Plot) based on Significance ---
    print("\n🕸️ Generando Perfil de Impacto Estructural (Radar Chart)...")
    try:
        radar_data = {"Ecuación Seguridad": impacts1, "Ecuación Laboral": impacts2}
        radar_output = graph_path / "radar_impact_sem.png"
        draw_radar_impact(radar_data, str(radar_output))
        print(f"✅ Radar Chart generado en: {radar_output}")
    except Exception as e:
        logger.warning(f"⚠️ No se pudo generar el Radar Chart: {e}")

    # 7. Exportar metadatos del modelo para consumo en Quarto
    import json

    with open(evidence_path / "model_spec.json", "w") as f:
        json.dump(SEM_SPECIFICATION, f, indent=4)

    print(f"\n✅ Metadatos de la Bóveda preparados en: {evidence_path}")
    print("Siguiente paso: Renderizar index_sem.qmd")


if __name__ == "__main__":
    run_task()
