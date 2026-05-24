from docx import Document
from docx.shared import Cm
import os


def heal_template(source_path, target_path):
    if not os.path.exists(source_path):
        print(f"Error: No se encontró la plantilla en {source_path}")
        return

    print(f"Saneando plantilla: {source_path}")
    doc = Document(source_path)

    # Aplicar márgenes APA 7 (2.54 cm / 1 pulgada) en todas las secciones
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)
        # Asegurar tamaño A4
        section.page_height = Cm(29.7)
        section.page_width = Cm(21.0)

    doc.save(target_path)
    print(f"Plantilla sanada y guardada en: {target_path}")


if __name__ == "__main__":
    SOURCE = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/writing/templates/template.docx"
    TARGET = "/home/erick-fcs/Documentos/universidad/07_Ciclo/septimo_ciclo/applied_econometrics_2026/writing/templates/template_fixed.docx"
    heal_template(SOURCE, TARGET)
