import pandas as pd
from pathlib import Path
from typing import List, Dict

class AcademicExporter:
    """
    Exportador unificado para CSV y Excel con estándares académicos.
    """
    def __init__(self, output_base: Path):
        self.output_base = output_base

    def to_stata_csv(self, df: pd.DataFrame, filename: str = "Base_Final.csv"):
        """Exporta a CSV optimizado para Stata (utf-8-sig)."""
        path = self.output_base / "csv" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"📊 CSV (Stata) generado: {path}")
        return path

    def to_academic_excel(self, df: pd.DataFrame, catalog: List[Dict], filename: str = "Base_Revision.xlsx"):
        """Exporta a Excel con diccionario de variables y pestañas temáticas."""
        path = self.output_base / "excel" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Preparar Diccionario
        df_dic = pd.DataFrame([{
            "Variables": s.get("nombre_raw", ""),
            "Unidad": s.get("unidad_api", "N/A"),
            "Definición": s.get("concepto", "N/A"),
            "Fuente": s.get("institucion", "N/A"),
            "Backend": s.get("source_kind", "world_bank"),
            "Alcance": s.get("scope", "global"),
            "Link": s.get("url_indicador", "N/A")
        } for s in catalog])

        with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
            df_dic.to_excel(writer, sheet_name="Diccionario", index=False)
            df.to_excel(writer, sheet_name="Panel_Datos", index=False)
            
            # Formatos
            workbook = writer.book
            for ws in writer.sheets.values():
                ws.set_column('A:Z', 22)

        print(f"📗 Excel (Revisión) generado: {path}")
        return path
