"""Validaciones y métricas de calidad del dataset canónico."""
from datetime import date
from collections import Counter, defaultdict

from .constants import TYPE_ENUM, CATEGORY_ENUM, VALID_ISO
from .config import YEAR_MIN, YEAR_MAX


def _conf(e):
    return e.get("confidence") or e.get("source", {}).get("confidence")


def metrics(ev):
    m = {"total": len(ev)}
    m["by_calendar"] = Counter(e["calendar_group"] for e in ev)
    m["by_type"] = Counter(e["type"] for e in ev)
    m["by_category"] = Counter(e["category"] for e in ev)
    m["by_confidence"] = Counter(_conf(e) for e in ev)
    m["by_year"] = Counter(e["year"] for e in ev)
    dates = [e["date"] for e in ev]
    m["date_min"], m["date_max"] = min(dates), max(dates)
    seen = Counter((e["date"], e["name"]["es"], e["calendar_group"]) for e in ev)
    m["exact_dupes"] = sum(c - 1 for c in seen.values() if c > 1)
    sem = defaultdict(set)
    for e in ev:
        sem[(e["date"], e["slug"])].add(e["calendar_group"])
    m["semantic_dupes"] = sum(1 for v in sem.values() if len(v) > 1)
    m["no_date"] = sum(1 for e in ev if not e["date"])
    m["no_name"] = sum(1 for e in ev if not e["name"]["es"])
    m["bad_type"] = sum(1 for e in ev if e["type"] not in TYPE_ENUM)
    m["bad_category"] = sum(1 for e in ev if e["category"] not in CATEGORY_ENUM)
    m["local_no_territory"] = sum(1 for e in ev if e["is_local"]
                                  and not (e["subdivisions"] or e["communes"] or e["scope_text"]))
    m["feriado_no_legal"] = sum(1 for e in ev if (e["is_public_holiday"]
                                or e["is_bank_holiday"]) and not e["legal_basis"])
    m["dtend_problematic"] = sum(1 for e in ev if e["end_date"] < e["start_date"]
                                 or e["duration_days"] < 1)
    m["multiday"] = sum(1 for e in ev if e["is_multiday"])
    m["recurring"] = sum(1 for e in ev if e["recurring"])
    m["singular"] = sum(1 for e in ev if e["singular"])
    m["irrenunciables"] = sum(1 for e in ev if e["is_irrenunciable"])
    m["with_subdivisions"] = sum(1 for e in ev if e["subdivisions"])
    return m


def run_tests(ev):
    res = []

    def check(name, cond, detail=""):
        res.append((name, bool(cond), detail))

    bad = [e["id"] for e in ev if not _valid_date(e["start_date"]) or not _valid_date(e["end_date"])]
    check("Todas las fechas son válidas ISO", not bad, f"{len(bad)} inválidas")
    check("start_date <= end_date",
          not [e for e in ev if e["end_date"] < e["start_date"]])
    check("year coincide con start_date",
          not [e for e in ev if e["year"] != int(e["start_date"][:4])])
    check("type dentro del enum", not [e for e in ev if e["type"] not in TYPE_ENUM])
    check("category dentro del enum",
          not [e for e in ev if e["category"] not in CATEGORY_ENUM])
    check("subdivisions con ISO 3166-2 válido",
          not [s for e in ev for s in e["subdivisions"] if s not in VALID_ISO])
    check("eventos multi-día con duración > 1",
          not [e for e in ev if e["is_multiday"] and e["duration_days"] <= 1])
    ids = Counter(e["id"] for e in ev)
    check("IDs únicos", not [k for k, c in ids.items() if c > 1])
    check("categoría de irrenunciabilidad en 1..5",
          not [e for e in ev if e["irrenunciability_category"]
               and not (1 <= e["irrenunciability_category"] <= 5)])
    years = {e["year"] for e in ev}
    missing = [y for y in range(YEAR_MIN, YEAR_MAX + 1) if y not in years]
    check(f"cobertura {YEAR_MIN}–{YEAR_MAX} completa", not missing,
          f"faltan {len(missing)}")
    return res


def _valid_date(s):
    try:
        date.fromisoformat(s); return True
    except Exception:
        return False
