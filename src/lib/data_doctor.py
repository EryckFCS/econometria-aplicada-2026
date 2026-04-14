import json
import pandas as pd
from pathlib import Path
from loguru import logger

class DataDoctor:
    """
    Clase encargada de la curación y saneamiento de datos econométricos.
    Permite inyectar parches validados desde manifiestos JSON con trazabilidad.
    """
    def __init__(self, manifest_path: str = None):
        self.manifest_path = Path(manifest_path) if manifest_path else None
        self.curations = []
        if self.manifest_path and self.manifest_path.exists():
            self._load_manifest()

    def _load_manifest(self):
        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.curations = data.get("curations", [])
            logger.info(f"🩺 Manifiesto cargado: {self.manifest_path} ({len(self.curations)} curaciones)")
        except Exception as e:
            logger.error(f"❌ Error cargando manifiesto: {e}")

    def apply_cures(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica las curaciones definidas en el manifiesto al DataFrame."""
        if not self.curations:
            logger.warning("⚠️ No hay curaciones definidas para aplicar.")
            return df

        audit_log = []
        applied_count = 0

        for cure in self.curations:
            iso2 = cure["target_iso2"]
            col = cure["target_column"]
            year = cure["year"]
            new_val = cure["value"]
            source = cure["source"]

            if col not in df.columns:
                continue

            mask = (df["iso2"] == iso2) & (df["year"] == year)
            
            # Verificar si existe el registro y si es NaN
            subset = df.loc[mask]
            if not subset.empty:
                old_val = subset[col].values[0]
                if pd.isna(old_val) or old_val == 0: # Curar si es NaN o 0 (si aplica)
                    df.loc[mask, col] = new_val
                    applied_count += 1
                    msg = f"🩹 [CURE] {iso2} {year} {col}: {old_val} -> {new_val} (Fuente: {source})"
                    logger.success(msg)
                    audit_log.append(msg)

        if applied_count > 0:
            self._write_audit_log(audit_log)
        
        return df

    def _write_audit_log(self, logs: list):
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        audit_file = log_dir / "curation_audit.log"
        
        with open(audit_file, "a", encoding="utf-8") as f:
            f.write(f"\n--- Sesión de Curación: {pd.Timestamp.now()} ---\n")
            for line in logs:
                f.write(line + "\n")
        logger.info(f"📝 Auditoría guardada en {audit_file}")
