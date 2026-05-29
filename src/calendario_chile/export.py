"""Escritores de salida: JSON, CSV, Parquet, SQLite y derivados."""
import json
import csv as csvmod
import sqlite3

import pandas as pd

PIPE = "|"


def flat_row(e, internal=False):
    """Aplana un evento a fila tabular. internal=True conserva trazabilidad."""
    lb = e["legal_basis"]
    row = {
        "id": e["id"], "date": e["date"], "start_date": e["start_date"],
        "end_date": e["end_date"], "year": e["year"], "weekday": e["weekday"],
        "name_es": e["name"]["es"], "name_en": e["name"]["en"], "slug": e["slug"],
        "summary_original": e["summary_original"], "type": e["type"],
        "category": e["category"], "calendar_group": e["calendar_group"],
        "nationwide": e["nationwide"],
        "subdivisions": PIPE.join(e["subdivisions"]),
        "regions": PIPE.join(e["regions"]), "communes": PIPE.join(e["communes"]),
        "location_raw": e["location_raw"], "scope_text": e["scope_text"],
        "is_public_holiday": e["is_public_holiday"],
        "is_bank_holiday": e["is_bank_holiday"],
        "is_commemorative": e["is_commemorative"], "is_local": e["is_local"],
        "is_school": e["is_school"], "is_religious": e["is_religious"],
        "is_civic": e["is_civic"], "is_irrenunciable": e["is_irrenunciable"],
        "irrenunciability_category": e["irrenunciability_category"],
        "irrenunciability_category_label": e["irrenunciability_category_label"],
        "recurring": e["recurring"], "singular": e["singular"],
        "movable": e["movable"], "is_multiday": e["is_multiday"],
        "duration_days": e["duration_days"], "legal_basis_count": len(lb),
        "legal_basis_summary": " ; ".join(filter(None, (l["raw"] if "raw" in l
                                          else (l.get("title") or "") for l in lb))),
        "confidence": e.get("confidence", e.get("source", {}).get("confidence")),
    }
    if internal:
        s = e["source"]
        row.update({
            "definition_anchor": e["definition"]["anchor"],
            "source_file": s["source_file"], "source_calendar": s["source_calendar"],
            "source_url": s["source_url"], "source_anchor": s["source_anchor"],
            "extraction_method": PIPE.join(s["extraction_method"]),
            "notes": " ; ".join(s["notes"]),
        })
    return row


def write_json(events, path, indent=2):
    path.write_text(json.dumps(events, ensure_ascii=False, indent=indent),
                    encoding="utf-8")


def write_csv(rows, path):
    cols = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csvmod.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)
    return cols


def write_parquet(rows, path):
    pd.DataFrame(rows).to_parquet(path, index=False)


def write_sqlite(rows, path, norms=None, events=None):
    if path.exists():
        path.unlink()
    con = sqlite3.connect(path)
    pd.DataFrame(rows).to_sql("events", con, index=False)
    if norms is not None:
        nr = [{"anchor": a, "type": n["type"], "number": n["number"],
               "year": n["year"], "title": n["title"], "url": n["url"],
               "name": n["name"]} for a, n in norms.items()]
        pd.DataFrame(nr).to_sql("norms", con, index=False)
    if events is not None:
        elb = [{"event_id": e["id"], "norma_anchor": l.get("norma_anchor"),
                "role": l["role"], "type": l["type"], "number": l["number"],
                "year": l["year"], "title": l["title"], "url": l["url"],
                "articulo": l["articulo"]}
               for e in events for l in e["legal_basis"]]
        if elb:
            pd.DataFrame(elb).to_sql("event_legal_basis", con, index=False)
            con.execute("CREATE INDEX idx_elb ON event_legal_basis(event_id)")
    con.execute("CREATE INDEX idx_date ON events(date)")
    con.execute("CREATE INDEX idx_year ON events(year)")
    con.execute("CREATE INDEX idx_type ON events(type)")
    con.commit(); con.close()
