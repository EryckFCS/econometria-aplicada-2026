# Uso del script `parse_stata_log.py`

- Objetivo: parsear `logs/stata_master_table.log` y generar:
  - `reports/unit_root_tests.xlsx`
  - `reports/unit_root_tests.docx`

- Requisitos: instalar las dependencias indicadas en `requirements.txt` del mismo directorio.

Instalación (entorno virtual recomendado):

```bash
python3 -m pip install -r scripts/requirements.txt
```

Ejecución:

```bash
python3 scripts/parse_stata_log.py
```

Salida:

- `docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/analysis_erick_condoy/reports/unit_root_tests.xlsx`
- `docs/vaults/u1-aa-01-applied-econometrics/ape2-crisis-iess/analysis_erick_condoy/reports/unit_root_tests.docx`
