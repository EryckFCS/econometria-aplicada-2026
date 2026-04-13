import pandas as pd
from pathlib import Path
from typing import List, Dict

class AcademicExcelExporter:
    def __init__(self, output_path: Path):
        self.output_path = output_path

    def export(self, df_panel: pd.DataFrame, catalog: List[Dict]):
        """Genera el Excel Maestro con Diccionario y pestañas temáticas."""
        
        # 1. Preparar Diccionario
        diccionario_data = []
        for s in catalog:
            diccionario_data.append({
                "Variables": s.get("nombre_raw", ""),
                "Unidad de medida": s.get("unidad_api", "N/A"),
                "Definición": s.get("concepto", "N/A"),
                "Fuente": s.get("institucion", "N/A"),
                "Link": s.get("url_indicador", "N/A")
            })
        df_dic = pd.DataFrame(diccionario_data)

        with pd.ExcelWriter(self.output_path, engine='xlsxwriter') as writer:
            # Hoja 1: Diccionario
            df_dic.to_excel(writer, sheet_name="Diccionario", index=False)
            
            # Hoja 2: Panel de datos (Petición expresa del usuario)
            df_panel.to_excel(writer, sheet_name="Panel de datos", index=False)

            # Hoja 3+: Divisiones temáticas (Facilidad humana)
            self._add_thematic_sheets(writer, df_panel, catalog)

            # Formateo
            workbook = writer.book
            for worksheet in writer.sheets.values():
                worksheet.set_column('A:Z', 22)

    def _add_thematic_sheets(self, writer, df, catalog):
        ejes = {
            "Economia": ["económica", "apertura", "inversión"],
            "Ambiental": ["ambiental", "tecnología verde"],
            "Institucional": ["gobernanza", "financiero"]
        }
        for title, kw_list in ejes.items():
            cols = [s['nombre_raw'] for s in catalog if any(kw in s.get('rol', '').lower() for kw in kw_list)]
            valid = ['iso2', 'pais', 'year'] + [c for c in cols if c in df.columns]
            if len(valid) > 3:
                df[valid].to_excel(writer, sheet_name=f"Eje_{title}", index=False)
