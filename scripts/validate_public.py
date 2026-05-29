"""
Validación del repo PÚBLICO: opera sobre los datos incluidos en el repositorio
(`data/public/SAMPLE.json` y `data/api/v1/years/*.json`), SIN requerir las
fuentes internas ni el dataset completo.

Para regenerar el dataset completo se necesitan las fuentes internas o los
artefactos de release (ver `docs/downloads.md`). Este validador comprueba la
integridad de la muestra y de la API estática incluida.
"""
import sys
import json
from datetime import date
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from calendario_chile.constants import TYPE_ENUM, CATEGORY_ENUM, VALID_ISO  # noqa

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = ("farah", "feriadoschilenos")


def _valid_date(s):
    try:
        date.fromisoformat(s)
        return True
    except Exception:
        return False


def bundled_files():
    files = []
    sample = ROOT / "data" / "public" / "SAMPLE.json"
    if sample.exists():
        files.append(sample)
    files += sorted((ROOT / "data" / "api" / "v1" / "years").glob("*.json"))
    return files


def check_records(records):
    errors = []

    def bad(cond, msg):
        if cond:
            errors.append(msg)

    ids = Counter(r["id"] for r in records)
    bad([k for k, c in ids.items() if c > 1], "ids duplicados")
    for r in records:
        bad(not _valid_date(r["start_date"]) or not _valid_date(r["end_date"]),
            f"fecha inválida en {r['id']}")
        bad(r["end_date"] < r["start_date"], f"start>end en {r['id']}")
        bad(r["year"] != int(r["start_date"][:4]), f"year≠fecha en {r['id']}")
        bad(r["type"] not in TYPE_ENUM, f"type inválido en {r['id']}")
        bad(r["category"] not in CATEGORY_ENUM, f"category inválida en {r['id']}")
        bad(any(s not in VALID_ISO for s in r["subdivisions"]),
            f"ISO inválido en {r['id']}")
        bad(r["is_multiday"] and r["duration_days"] <= 1,
            f"multiday<=1 en {r['id']}")
        bad(r["irrenunciability_category"] not in (None, 1, 2, 3, 4, 5),
            f"categoría irren fuera de rango en {r['id']}")
        bad("source" in r, f"contiene bloque interno 'source' en {r['id']}")
    return errors


def main():
    files = bundled_files()
    if not files:
        print("No hay datos incluidos para validar."); sys.exit(1)
    total = 0
    all_errors = []
    for f in files:
        recs = json.loads(f.read_text(encoding="utf-8"))
        total += len(recs)
        all_errors += [f"{f.name}: {e}" for e in check_records(recs)]
        blob = f.read_text(encoding="utf-8").lower()
        for tok in FORBIDDEN:
            if tok in blob:
                all_errors.append(f"{f.name}: contiene token externo '{tok}'")
    print(f"== VALIDACIÓN PÚBLICA == {len(files)} archivos, {total} registros")
    if all_errors:
        for e in all_errors[:40]:
            print("  [FALLA]", e)
        print(f"\n{len(all_errors)} problemas.")
        sys.exit(1)
    print("  [OK] fechas válidas · start<=end · year coincide")
    print("  [OK] type/category en enum · ISO 3166-2 válido")
    print("  [OK] multiday>1 · categoría irren 1..5 · ids únicos")
    print("  [OK] sin bloque interno 'source' · sin tokens externos")
    print("\nTodos los chequeos de la superficie pública aprobados.")


if __name__ == "__main__":
    main()
