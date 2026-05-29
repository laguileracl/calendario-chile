"""Construye el dataset COMPLETO (todos los tipos) en data/internal/intermediate
con trazabilidad interna, más los esquemas y el datapackage. Material interno.
"""
import _bootstrap  # noqa
import json

from calendario_chile import build_events, event_schema, holiday_schema, datapackage
from calendario_chile.config import INTERMEDIATE, AUDIT, SCHEMA, ensure_dirs
from calendario_chile.export import (flat_row, write_json, write_csv,
                                     write_parquet, write_sqlite)


def main():
    ensure_dirs()
    events, ctx = build_events()
    norms = ctx["norms"]

    # Dataset completo interno (con bloque source)
    write_json(events, INTERMEDIATE / "calendar_chile_events.full.json", indent=0)
    rows = [flat_row(e, internal=True) for e in events]
    cols = write_csv(rows, INTERMEDIATE / "calendar_chile_events.full.csv")
    write_parquet(rows, INTERMEDIATE / "calendar_chile_events.full.parquet")
    write_sqlite(rows, INTERMEDIATE / "calendar_chile_events.full.sqlite",
                 norms=norms, events=events)

    # Catálogo de normas (auditoría legal interna)
    nr = [{"anchor": a, **{k: n[k] for k in ("type", "number", "year", "title",
                                             "url", "name", "raw")}}
          for a, n in norms.items()]
    write_json(nr, AUDIT / "legal_basis_catalog.json")

    # Esquemas + datapackage (contrato de datos, publicable)
    write_json(event_schema(), SCHEMA / "calendar_chile_event.schema.json")
    write_json(holiday_schema(), SCHEMA / "calendar_chile_holiday.schema.json")
    # columnas públicas (sin trazabilidad interna) para el datapackage
    pub_cols = [c for c in cols if c not in (
        "definition_anchor", "source_file", "source_calendar", "source_url",
        "source_anchor", "extraction_method", "notes")]
    write_json(datapackage(pub_cols), SCHEMA / "datapackage.json")

    print(f"[build_dataset] {len(events)} eventos -> {INTERMEDIATE}")
    print(f"  norms: {len(nr)} | schema + datapackage -> {SCHEMA}")


if __name__ == "__main__":
    main()
