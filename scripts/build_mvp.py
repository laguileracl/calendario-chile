"""Construye el RELEASE PÚBLICO (MVP): feriados públicos, bancarios, locales y de
ámbito restringido — vista pública sin trazabilidad interna. Liviano.
Salida: data/public/{json,csv,sqlite,parquet}.
"""
import _bootstrap  # noqa

from calendario_chile import build_events, to_public
from calendario_chile.config import (PUB_JSON, PUB_CSV, PUB_SQLITE, PUB_PARQUET,
                                     ensure_dirs)
from calendario_chile.export import (flat_row, write_json, write_csv,
                                     write_parquet, write_sqlite)

MVP_TYPES = {"public", "bank", "local", "restricted"}


def main():
    ensure_dirs()
    events, _ = build_events()
    feriados = [e for e in events if e["type"] in MVP_TYPES]
    pub = [to_public(e) for e in feriados]

    write_json(pub, PUB_JSON / "calendar_chile_holidays.json")
    rows = [flat_row(e) for e in pub]
    write_csv(rows, PUB_CSV / "calendar_chile_holidays.csv")
    write_parquet(rows, PUB_PARQUET / "calendar_chile_holidays.parquet")
    write_sqlite(rows, PUB_SQLITE / "calendar_chile_holidays.sqlite")

    print(f"[build_mvp] MVP público: {len(pub)} feriados -> data/public/")
    from collections import Counter
    print("  por tipo:", dict(Counter(e["type"] for e in pub)))


if __name__ == "__main__":
    main()
