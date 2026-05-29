"""Genera archivos iCalendar (.ics) publicables a partir del dataset:
uno combinado de feriados y uno por tipo. Salida: data/public/ics/."""
import _bootstrap  # noqa

from calendario_chile import build_events, to_public
from calendario_chile.ics import write_ics
from calendario_chile.config import PUB_ICS, ensure_dirs

CALS = {
    "feriados-publicos": ("public", "Feriados públicos de Chile"),
    "feriados-bancarios": ("bank", "Feriados bancarios de Chile"),
    "feriados-locales": ("local", "Feriados/días locales de Chile"),
}


def main():
    ensure_dirs()
    events, _ = build_events()
    pub = [to_public(e) for e in events]

    feriados = [e for e in pub if e["type"] in ("public", "bank", "local", "restricted")]
    n = write_ics(feriados, PUB_ICS / "feriados-chile.ics", "Feriados de Chile")
    print(f"[build_ics] feriados-chile.ics: {n} eventos")
    for fname, (typ, title) in CALS.items():
        subset = [e for e in pub if e["type"] == typ]
        if subset:
            write_ics(subset, PUB_ICS / f"{fname}.ics", title)
            print(f"  {fname}.ics: {len(subset)} eventos")


if __name__ == "__main__":
    main()
