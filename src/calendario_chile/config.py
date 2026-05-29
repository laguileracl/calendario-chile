"""Rutas y configuración central del proyecto calendario-chile."""
from pathlib import Path

# Raíz del proyecto (…/calendario-chile-next)
ROOT = Path(__file__).resolve().parents[2]

# Fuentes propias (material interno, no publicable sin revisión)
RAW = ROOT / "data" / "internal" / "raw"
RAW_HTML = RAW / "html"
RAW_ICS = RAW / "ics"

# Datos derivados
INTERNAL = ROOT / "data" / "internal"
INTERMEDIATE = INTERNAL / "intermediate"     # dataset completo y pesado
AUDIT = INTERNAL / "audit"                    # trazabilidad / revisión
SOURCE_INV = INTERNAL / "source_inventory"

PUBLIC = ROOT / "data" / "public"             # release liviano (MVP)
PUB_JSON = PUBLIC / "json"
PUB_CSV = PUBLIC / "csv"
PUB_ICS = PUBLIC / "ics"
PUB_SQLITE = PUBLIC / "sqlite"
PUB_PARQUET = PUBLIC / "parquet"

API = ROOT / "data" / "api" / "v1"
API_YEARS = API / "years"

SCHEMA = ROOT / "schema"
REPORTS = ROOT / "reports"

YEAR_MIN = 1981
YEAR_MAX = 2100

# Referencia temporal fija (el entorno no permite Date.now en el pipeline;
# se usa para la API estática "hoy/próximos"). Ajustable por script.
TODAY = "2026-05-29"


def ensure_dirs():
    for p in [INTERMEDIATE, AUDIT, SOURCE_INV, PUB_JSON, PUB_CSV, PUB_ICS,
              PUB_SQLITE, PUB_PARQUET, API, API_YEARS, SCHEMA, REPORTS]:
        p.mkdir(parents=True, exist_ok=True)
