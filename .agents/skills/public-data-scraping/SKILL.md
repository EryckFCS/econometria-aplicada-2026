---
name: public-data-scraping
description: Web scraping ético y evasión de bloqueos en portales de la administración pública de Ecuador (SRI, INEC, BCE, Contraloría) para extracción estructurada de datos económicos y de mercado.
version: 1.0.0
---

# SKILL: Web Scraping Ético y Evasión de Bloqueos en Ecuador

Esta habilidad guía al agente en el desarrollo de arañas, recolectores y scrapers resilientes para descargar reportes, pdfs y boletines de los portales gubernamentales de Ecuador. Estos portales suelen tener cortafuegos rudimentarios pero agresivos que bloquean IPs ante peticiones concurrentes altas.

---

## 1. Directrices de Scraping Ético y Resiliente

1. **Cumplir con el `robots.txt`**: Validar si el portal permite o restringe el acceso automatizado a las rutas deseadas antes de iniciar el ciclo de scraping.
2. **Rotación Estratégica de User-Agents**: No realizar peticiones consecutivas con el mismo User-Agent por defecto de bibliotecas como Python requests. Se debe usar una biblioteca o una lista interna de User-Agents modernos de navegadores reales.
3. **Control de Latencia (Delays)**: Utilizar retrasos aleatorios variables (`time.sleep(uniform(min, max))`) entre cada petición para simular el comportamiento de navegación humana y evitar alertas de DDoS en los WAF de los servidores.
4. **Manejo Exponencial de Reintentos (Backoff)**: Si el servidor retorna códigos de error transitorios (`500`, `502`, `503`, `504` o `429` Too Many Requests), se debe aplicar una estrategia de reintentos exponencial antes de fallar la tarea.
5. **Guardado en Caché Inmutable**: Al descargar un archivo o JSON crudo, guardarlo de inmediato en `data/raw/` antes de parsearlo para evitar descargas duplicadas que consuman ancho de banda del portal público de forma innecesaria.

---

## 2. Implementación de un Scraper Defensivo con Reintentos

A continuación se expone un recolector HTTP genérico y altamente resiliente que puede usarse para consultar boletines e información estructurada en portales de la Superintendencia de Bancos, Contraloría o el INEC.

```python
import time
import random
import requests
from bs4 import BeautifulSoup
from loguru import logger

# Pool de User-Agents modernos para evasión de bloqueos básicos
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

def fetch_public_page_resilient(
    url: str,
    max_retries: int = 5,
    backoff_factor: float = 2.0
) -> str:
    """
    Realiza una petición HTTP GET a una página pública del gobierno de Ecuador
    con rotación de cabeceras y política estricta de reintentos exponencial.
    """
    logger.info(f"Iniciando petición resiliente a: {url}")
    
    for attempt in range(1, max_retries + 1):
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive"
        }
        
        try:
            # Añadir timeout estricto para evitar bloqueos por sockets colgados en portales lentos
            response = requests.get(url, headers=headers, timeout=20)
            
            # Si retorna rate limiting (429) o errores del lado del servidor
            if response.status_code == 429 or response.status_code >= 500:
                logger.warning(f"Intento {attempt}/{max_retries} fallido. Status: {response.status_code}.")
                raise requests.exceptions.RequestException()
                
            response.raise_for_status()
            logger.success(f"Petición exitosa en el intento {attempt}.")
            return response.text
            
        except (requests.exceptions.RequestException, Exception) as e:
            if attempt == max_retries:
                logger.critical(f"Scraping fallido permanentemente tras {max_retries} intentos. Error: {e}")
                raise e
            
            # Calcular delay exponencial con jitter aleatorio
            delay = (backoff_factor ** attempt) + random.uniform(1.0, 3.0)
            logger.warning(f"Reintentando en {delay:.2f} segundos...")
            time.sleep(delay)
            
    return ""
```

---

## 3. Manejo de Sesiones e Ingestión de Documentos PDF

Cuando se scrapean portales de la Superintendencia de Bancos o Contraloría que requieren mantener el estado de la sesión:
1. Utilizar un objeto `requests.Session()` para conservar automáticamente las cookies devueltas por el servidor durante la navegación entre páginas.
2. Si un enlace descarga un PDF, guardar el archivo temporalmente y calcular su hash MD5/SHA256 para evitar reprocesar documentos idénticos en la base de RAG.
EOF
