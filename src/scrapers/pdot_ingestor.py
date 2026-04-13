"""
PDOT Ingestor (Plan de Desarrollo y Ordenamiento Territorial)
V2.0 - Agnostic & Autonomous
Descarga, extrae y limpia el texto de documentos PDF masivos de planificación cantonal.
Utiliza Google Dorking para evadir la navegación de portales y el ResilientClient para descargas blindadas.
"""
import asyncio
import io
import re
from pathlib import Path
from typing import Optional, Dict, List
import PyPDF2
from googlesearch import search
from loguru import logger
from concurrent.futures import ThreadPoolExecutor

from ecs_quantitative.ingestion.resilient_client import ResilientClient

class PdotIngestor:
    """Ingestor especializado en extraer texto estructural de PDFs vía Búsqueda Dorking Autónoma."""
    
    def __init__(self, base_data_dir: Path):
        self.base_dir = Path(base_data_dir)
        self.pdot_dir = self.base_dir / "01_Raw" / "pdot_texts"
        self.pdot_dir.mkdir(parents=True, exist_ok=True)
        
        # Regex estricto de LOTAIP/PDOT
        self.pdot_regex = re.compile(r'(?i)pdot.*\.pdf')
        self.pugs_regex = re.compile(r'(?i)pugs.*\.pdf') # For Plan de Uso y Gestion de Suelo (future proofing)
        
        # Core Library Resilient Client (Timeout extendido para PDFs grandes)
        self.client = ResilientClient(timeout=60.0, max_retries=5)
        
        logger.info(f"📂 Repositorio PDOT inicializado en: {self.pdot_dir}")

    def find_pdot_url(self, canton: str) -> Optional[str]:
        """
        Heurística LOTAIP usando Google Dorking:
        site:gob.ec filetype:pdf "PDOT" "{canton}"
        """
        query = f'site:gob.ec filetype:pdf "PDOT" "{canton}"'
        logger.info(f"🔍 Dorking Inyectado: {query}")
        
        try:
            # We search the top 5 results to find the exact PDF match
            results = list(search(query, num_results=5, lang="es"))
            
            for url in results:
                # Fallback Regex Validation
                if url.endswith('.pdf'):
                    # Verify it's actually a PDOT and not some random municipal PDF
                    if self.pdot_regex.search(url) or "ordenamiento-territorial" in url.lower() or "desarrollo" in url.lower():
                        logger.success(f"🎯 URL de PDOT interceptada para {canton}: {url}")
                        return url
            
            logger.warning(f"⚠️ No se encontró URL directa y verificable para {canton}.")
            return None
            
        except Exception as e:
            logger.error(f"Fallo en Dorking para {canton}: {e}")
            return None

    async def download_pdf_async(self, url: str) -> bytes:
        """Descarga un PDF usando el cliente resiliente agnóstico de grado militar."""
        logger.info(f"⬇️ Iniciando descarga blindada: {url}")
        
        try:
            response = await self.client.get(url)
            
            if '%PDF' not in response.content[:5].decode('utf-8', errors='ignore'):
                 logger.warning(f"El archivo descargado de {url} no parece ser un PDF válido (Posible PDF falso 404).")
                 return b""
                 
            return response.content
        except Exception as e:
            logger.error(f"❌ Error descargando PDF de {url}: {e}")
            return b""

    def extract_text(self, pdf_bytes: bytes) -> str:
        """Usa PyPDF2 para extraer el texto de las páginas del documento."""
        if not pdf_bytes: return ""
        
        logger.info("📄 Extrayendo texto y metadatos con PyPDF2...")
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PyPDF2.PdfReader(pdf_file)
            total_pages = len(reader.pages)
            
            text_blocks = []
            for i in range(total_pages):
                page = reader.pages[i]
                text = page.extract_text()
                if text:
                    clean_text = " ".join(text.split())
                    text_blocks.append(clean_text)
                    
            logger.success(f"✅ Extracción completa: {total_pages} páginas procesadas.")
            return "\n\n".join(text_blocks)
        except Exception as e:
            logger.error(f"❌ Error extrayendo texto del PDF: {e}")
            return ""

    async def ingest_canton_async(self, canton: str, exact_url: Optional[str] = None) -> Optional[Path]:
        """Flujo completo asíncrono: Dorking (Opcional) -> Download -> Extract -> Save"""
        if not exact_url:
            url = self.find_pdot_url(canton)
        else:
            url = exact_url
            logger.info(f"🔗 Usando URL estricta inyectada por el usuario para {canton}: {url}")
            
        if not url: return None
        
        pdf_bytes = await self.download_pdf_async(url)
        if not pdf_bytes: return None
        
        full_text = self.extract_text(pdf_bytes)
        if not full_text: return None
        
        filename = f"{canton.lower().replace(' ', '_')}_pdot.txt"
        filepath = self.pdot_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_text)
            logger.info(f"💾 Guardado exitoso: {filepath} ({len(full_text)} caracteres)")
            return filepath
        except Exception as e:
            logger.error(f"❌ Error guardando el archivo de texto: {e}")
            return None

    async def cleanup(self):
        """Cierra de forma segura el pool de conexiones del ResilientClient."""
        await self.client.close()

async def run_autonomous_ingestion(cantons: List[str], manual_urls: Dict[str, str] = None):
    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / "data"
    ingestor = PdotIngestor(base_data_dir=data_dir)
    
    tasks = []
    
    # Process Manual URLs if provided (for strict testing like Loja)
    if manual_urls:
        for canton, url in manual_urls.items():
            tasks.append(ingestor.ingest_canton_async(canton, exact_url=url))
            
    # Process Autonomous Cantons
    for canton in cantons:
        if not manual_urls or canton not in manual_urls:
            tasks.append(ingestor.ingest_canton_async(canton))
            
    # Ejecución paralela pura usando Asyncio y ResilientClient
    await asyncio.gather(*tasks)
    await ingestor.cleanup()

if __name__ == "__main__":
    logger.info("--- PRUEBA DE INGESTA DE PDOT V2 (DORKING + RESILIENT CLIENT) ---")
    
    # 1. Cantones a buscar de forma 100% autónoma
    cantones_autonomos = ["Saraguro", "Catamayo"]
    
    # 2. Inyección estricta (Por ejemplo, las URLs directas que el usuario proporcionó para validación)
    urls_strictas = {
        "Loja": "https://www.loja.gob.ec/files/image/LOTAIP/pdot-2023-2027.pdf"
    }
    
    # Disparar pipeline asíncrono masivo
    # NOTA: Comentamos esto para pruebas de CI, descomentar en el entorno del usuario
    # asyncio.run(run_autonomous_ingestion(cantons=cantones_autonomos, manual_urls=urls_strictas))
    print("Script V2 SOTA preparado. Para lanzar, ejecuta asyncio.run() al final.")
