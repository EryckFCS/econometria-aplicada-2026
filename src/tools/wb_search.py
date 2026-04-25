import sys
import httpx
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Configuración de rutas
SRC_DIR = Path(__file__).parent.parent.resolve()
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

console = Console()


def search_indicators(query: str, language: str = "es"):
    """
    Busca indicadores en la API del Banco Mundial por palabras clave.
    """
    url = "https://api.worldbank.org/v2/es/indicator"
    params = {"format": "json", "search": query, "per_page": 50}

    console.print(f"[bold blue]🔍 Buscando indicadores para:[/bold blue] '{query}'...")

    try:
        with httpx.Client(timeout=20.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if len(data) < 2 or not data[1]:
                console.print(
                    "[bold red]❌ No se encontraron indicadores para esa búsqueda.[/bold red]"
                )
                return

            indicators = data[1]

            table = Table(title=f"Resultados para: {query}")
            table.add_column("ID (Código API)", style="cyan", no_wrap=True)
            table.add_column("Nombre del Indicador", style="green")
            table.add_column("Fuente", style="magenta")

            for ind in indicators:
                table.add_row(ind["id"], ind["name"], ind["source"]["value"])

            console.print(table)
            console.print(
                "\n[italic]Sugerencia: Usa el ID en tu lista de SERIES_RAW para descargar la data automáticamente.[/italic]"
            )

    except Exception as e:
        console.print(f"[bold red]Error en la conexión:[/bold red] {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[yellow]Uso: python wb_search.py 'palabra clave'[/yellow]")
        # Búsqueda por defecto para probar
        search_indicators("pobreza")
    else:
        search_indicators(" ".join(sys.argv[1:]))
