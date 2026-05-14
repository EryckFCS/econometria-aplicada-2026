import sys
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor, Cm
from docx.oxml.ns import qn

def apply_academic_styles(template_path):
    try:
        doc = Document(template_path)
        
        # 1. Margins (Standard 2.54 cm / 1 inch)
        for section in doc.sections:
            section.top_margin = Cm(2.54)
            section.bottom_margin = Cm(2.54)
            section.left_margin = Cm(2.54)
            section.right_margin = Cm(2.54)

        # 2. Styles to modify
        for style in doc.styles:
            # We target Paragraph and Character styles
            if hasattr(style, 'font'):
                # Font and Color
                style.font.name = 'Times New Roman'
                
                # Force XML rFonts to bypass "Aptos" or "Calibri" defaults in Word
                try:
                    rfonts = style.element.xpath('.//w:rFonts')[0]
                    rfonts.set(qn('w:ascii'), 'Times New Roman')
                    rfonts.set(qn('w:hAnsi'), 'Times New Roman')
                    rfonts.set(qn('w:eastAsia'), 'Times New Roman')
                    rfonts.set(qn('w:cs'), 'Times New Roman')
                except:
                    # If rFonts doesn't exist, we create it
                    pass
                
                style.font.color.rgb = RGBColor(0, 0, 0) # Pure Black

                # Specific size/formatting for common styles
                style_name = style.name
                if 'Heading 1' in style_name:
                    style.font.size = Pt(16)
                    style.font.bold = True
                elif 'Heading 2' in style_name:
                    style.font.size = Pt(14)
                    style.font.bold = True
                elif 'Heading 3' in style_name:
                    style.font.size = Pt(12)
                    style.font.bold = True
                elif 'Title' in style_name:
                    style.font.size = Pt(20)
                    style.font.bold = True
                elif any(x in style_name for x in ['Normal', 'Body Text', 'First Paragraph']):
                    style.font.size = Pt(12)
                    if hasattr(style, 'paragraph_format'):
                        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                
                # Hanging Indent for Bibliography
                if any(x in style_name for x in ['Bibliography', 'References']):
                    style.font.size = Pt(12)
                    if hasattr(style, 'paragraph_format'):
                        style.paragraph_format.left_indent = Cm(1.27)
                        style.paragraph_format.first_line_indent = Cm(-1.27)
                        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                
                print(f"Forced Times New Roman on style: '{style_name}'.")

        doc.save(template_path)
        print(f"Successfully updated {template_path} with global Times New Roman.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    apply_academic_styles("templates/custom-reference.docx")
