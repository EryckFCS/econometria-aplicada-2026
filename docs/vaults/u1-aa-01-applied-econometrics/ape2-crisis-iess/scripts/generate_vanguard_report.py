import pandas as pd
import pickle
from statsmodels.iolib.summary2 import summary_col

# Load models
with open("logs/models_comparison.pkl", "rb") as f:
    data = pickle.load(f)
    m1 = data["model_1"]
    m2 = data["model_2"]

# Rename variables for presentation
rename_map = {
    "const": "Constante",
    "trend": "Tendencia (t)",
    "ln_afiliacion.L1": "Ln(Afiliación)_{t-1}",
    "ln_dependencia.L0": "Ln(Dependencia)_{t}",
    "ln_dependencia.L1": "Ln(Dependencia)_{t-1}",
    "ln_subempleo.L0": "Ln(Subempleo)_{t}",
    "ln_wti.L0": "Ln(Precio WTI)_{t}",
    "ln_wti.L1": "Ln(Precio WTI)_{t-1}",
    "ln_embi.L0": "Ln(EMBI Ecuador)_{t}",
    "ln_embi.L1": "Ln(EMBI Ecuador)_{t-1}",
    "ln_remesas.L0": "Ln(Remesas/PIB)_{t}",
    "ln_remesas.L1": "Ln(Remesas/PIB)_{t-1}",
    "ln_matricula.L0": "Ln(Matrícula Superior)_{t}",
    "ln_brecha.L0": "Ln(Brecha Género)_{t}",
}

# Create combined table
# Using summary_col for LaTeX/Text style alignment
df_results = summary_col(
    [m1, m2],
    stars=True,
    model_names=["Modelo 1 (Base)", "Modelo 2 (Vanguardia)"],
    float_format="%0.4f",
    info_dict={
        "N": lambda x: "{0:d}".format(int(x.nobs)),
        "R2": lambda x: "{:.4f}".format(x.rsquared),
        "BIC": lambda x: "{:.2f}".format(x.bic),
    },
)

# Export to Markdown/HTML for Quarto
table_md = df_results.as_text()
with open("assets/ardl_comparison.txt", "w") as f:
    f.write(table_md)


# Generate a "Premium" Styled HTML table using Pandas Styler
# This will be used in the QMD via a specialized block
def generate_premium_html(m1, m2):
    # Extract coefficients and p-values manually for more control
    def get_df(m, name):
        df = pd.DataFrame({"Coef": m.params, "P": m.pvalues})
        df.index = [rename_map.get(i, i) for i in df.index]
        return df.add_prefix(f"{name}_")

    df1 = get_df(m1, "M1")
    df2 = get_df(m2, "M2")
    res = pd.concat([df1, df2], axis=1).fillna("-")

    # Custom HTML output
    return res.to_html(classes="premium-table table-hover", border=0)


html_table = generate_premium_html(m1, m2)
with open("assets/premium_table.html", "w") as f:
    f.write(html_table)

print("Comparison table generated in assets/")
