import zipfile
import os
from pathlib import Path
from datetime import datetime
import sys

def zip_task_folder(unit: int, task_type: str, author: str = "ERIK_CONDOY"):
    """
    Empaqueta la carpeta de una tarea específica (ACD, AA, APE) en un ZIP listo para el EVA.
    
    Args:
        unit: Número de unidad (1, 2, 3)
        task_type: Tipo de tarea ('ACD', 'AA', 'APE')
        author: Nombre del estudiante
    """
    PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
    TASK_DIR = PROJECT_ROOT / "docs" / f"unidad{unit}" / task_type.upper()
    EXPORTS_DIR = PROJECT_ROOT / "data" / "exports"
    
    if not TASK_DIR.exists():
        print(f"❌ Error: La carpeta {TASK_DIR} no existe.")
        return

    # Nombre del archivo final
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    zip_name = f"{author}_U{unit}_{task_type.upper()}_{timestamp}.zip"
    
    DELIVERIES_DIR = PROJECT_ROOT / "deliveries"
    DELIVERIES_DIR.mkdir(exist_ok=True)
    
    output_path = DELIVERIES_DIR / zip_name
    
    print(f"📦 Creando paquete de entrega: {zip_name}...")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 1. Incluir todos los archivos de la carpeta de la tarea (Word, Excel, .do)
        for root, _, files in os.walk(TASK_DIR):
            for file in files:
                file_path = Path(root) / file
                # No incluir el propio zip si existiera
                if file.endswith('.zip'): continue
                arcname = Path(task_type.upper()) / file_path.relative_to(TASK_DIR)
                zipf.write(file_path, arcname)
                print(f"  + Añadiendo documento: {file}")

        # 2. Incluir la Base de Datos Maestra desde data/raw/excel (si existe)
        master_excel = PROJECT_ROOT / "data" / "raw" / "excel" / "APE1_Modelos_Dinamicos.xlsx"
        if master_excel.exists():
            zipf.write(master_excel, Path("DATA") / "APE1_Auditoria_Forense_MASTER.xlsx")
            print(f"  + Añadiendo Base de Datos: {master_excel.name}")
        
        # 3. Incluir el Manifiesto de Trazabilidad (Forensics)
        manifest = PROJECT_ROOT / "data" / "raw" / "manifest_fuentes_raw.csv"
        if manifest.exists():
            zipf.write(manifest, Path("DATA") / "trazabilidad_fuentes.csv")
            print("  + Añadiendo Evidencia de Trazabilidad (Forensics)")

        # 4. Incluir Scripts de Stata desde el Laboratorio (/stata)
        STATA_DIR = PROJECT_ROOT / "stata" / f"unidad{unit}"
        if STATA_DIR.exists():
            for file in os.listdir(STATA_DIR):
                if file.endswith(".do") and task_type.lower() in file.lower():
                    zipf.write(STATA_DIR / file, Path("CODIGO_STATA") / file)
                    print(f"  + Añadiendo Script Stata: {file}")

    print(f"\n✅ ÉXITO: Entregable generado en:\n{output_path}")

if __name__ == "__main__":
    # Por defecto empaqueta la Unidad 1 - ACD (donde está trabajando el usuario)
    unit_val = 1
    type_val = "ACD"
    
    if len(sys.argv) > 2:
        unit_val = int(sys.argv[1])
        type_val = sys.argv[2]
        
    zip_task_folder(unit_val, type_val)
