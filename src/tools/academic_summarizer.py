"""
Academic Summarizer for Applied Econometrics 2026.
Converts technical regression results into formal academic draft summaries.
"""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

try:
    from ecs_quantitative.nlp.rag.router import AgenticRouter
    from ecs_quantitative.core.logger import get_logger
except ImportError:
    print("Error: capital-workstation-libs not found. Please install shared libs.")
    sys.exit(1)

try:
    from lib.bibliography_rag import BibliographyRAG
except ImportError:
    BibliographyRAG = None

logger = get_logger("AcademicSummarizer")


class AcademicSummarizer:
    def __init__(self):
        # We use the router to determine if the summary should be causal, factual or structural
        self.router = AgenticRouter(domain="Academic Econometrics (Ecuador)")

    def summarize_results(
        self, model_df: pd.DataFrame, title: str = "Linear Regression Model"
    ):
        """
        Takes a statsmodels-like dataframe (coefficients, p-values) and
        returns an 'AI-driven' summary interpretation.
        """
        summary_text = f"Draft Interpretation for: {title}\n"
        summary_text += "-" * 40 + "\n"

        for index, row in model_df.iterrows():
            coeff = row.get("coef", 0)
            p_val = row.get("P>|t|", 1.0)
            significance = (
                "***"
                if p_val < 0.01
                else "**"
                if p_val < 0.05
                else "*"
                if p_val < 0.1
                else "N/S"
            )

            direction = "positivo" if coeff > 0 else "negativo"

            summary_text += f"\nVariable [{index}]: Tiene un impacto {direction} y es {significance}."

            # Use Router-like logic for qualitative addition
            decision = self.router.route_query(
                f"¿Por qué {index} impacta en el modelo?"
            )
            if decision["strategy"] == "GRAPH":
                summary_text += f" [Sugerencia: Revisar vínculos causales en {index}]"

        return summary_text

    def bibliography_context(self, query_text: str, n_results: int = 3) -> str:
        """Optional bibliography context block for future summaries."""
        if BibliographyRAG is None:
            return ""

        try:
            rag = BibliographyRAG()
            results = rag.query(query_text, n_results=n_results)
            return rag.format_results(results)
        except Exception as exc:
            logger.warning(f"Bibliography context unavailable: {exc}")
            return ""


if __name__ == "__main__":
    # Example usage with mock data
    mock_data = pd.DataFrame(
        {"coef": [0.45, -1.2, 0.01], "P>|t|": [0.005, 0.08, 0.5]},
        index=["Educacion", "Pobreza", "Edad"],
    )

    summarizer = AcademicSummarizer()
    print(summarizer.summarize_results(mock_data))
