"""Modelo de datos: construcción de eventos canónicos, vista pública y esquemas."""
from collections import Counter, defaultdict

from .constants import (TYPE_ENUM, CATEGORY_ENUM, ORDINALS,
                        FERIADO_GROUPS, COMM_GROUPS, LOCAL_GROUPS)
from .normalize import norm, slugify, parse_occurrence_classification
from .territorial import territory
from .legal import parse_norms, parse_definitions, resolve_legal
from .ics import parse_ics_events
from .overrides import apply_override
from bisect import bisect_left


def _anchor_resolver(defs):
    keys = sorted(defs.keys())

    def resolve(anchor, name):
        if not anchor:
            return None, "name", "low"
        if anchor in defs:
            return anchor, "exact", "high"
        i = bisect_left(keys, anchor)
        cands = []
        while i < len(keys) and keys[i].startswith(anchor):
            cands.append(keys[i]); i += 1
        if len(cands) == 1:
            return cands[0], "prefix1", "high"
        if len(cands) > 1:
            target = norm(name)
            for c in cands:
                if target and any(norm(n) == target for n in defs[c].get("names", [])):
                    return c, "prefixN_name", "medium"
            return cands[0], "prefixN_first", "low"
        return None, "name", "low"
    return resolve


def build_events():
    """Construye la lista de eventos canónicos + contexto (normas, defs, cls)."""
    norms = parse_norms()
    defs, name_index = parse_definitions()
    cls = parse_occurrence_classification()
    resolve = _anchor_resolver(defs)
    base = parse_ics_events()

    years_by_key = defaultdict(set)
    for e in base:
        years_by_key[(e["calendar_group"], e["source_anchor"])].add(e["year"])

    out, id_counts = [], Counter()
    for e in base:
        notes, methods, conf = [], ["ics"], "high"
        cg = e["calendar_group"]

        def_anchor, dmethod, dconf = resolve(e["source_anchor"], e["name_es"])
        if def_anchor is None:
            k = norm(e["name_es"])
            if k in name_index:
                def_anchor, dmethod, dconf = name_index[k], "name", "medium"
        d = defs.get(def_anchor) if def_anchor else None
        if d:
            methods.append("html_definition")
        if def_anchor and def_anchor != e["source_anchor"]:
            notes.append(f"ancla '{e['source_anchor']}' resuelta a '{def_anchor}' ({dmethod})")
        if def_anchor is None and e["source_anchor"]:
            notes.append(f"ancla '{e['source_anchor']}' sin definición encontrada")

        is_bank = cg == "feriados bancarios"
        is_pub = cg in FERIADO_GROUPS
        is_comm = cg in COMM_GROUPS
        is_local = cg in LOCAL_GROUPS

        date_iso = e["start_date"].isoformat()
        c = cls.get((date_iso, def_anchor)) if def_anchor else None
        if c is None and e["source_anchor"]:
            c = cls.get((date_iso, e["source_anchor"]))
        if c:
            methods.append("html_classification")

        is_religious = bool((d and d["is_religious"]) or (c and c["is_religious"])
                            or "religios" in norm(e["name_es"]))
        is_civic = bool(d and d["is_civic"])
        if d and d.get("caracter"):
            category = "religious" if is_religious else ("civic" if is_civic else "other")
        elif is_religious:
            category = "religious"
        elif is_pub or is_bank:
            category, is_civic = "civic", True
        else:
            category = "other"
            notes.append("categoría no clasificada en la fuente; asignada 'other'")

        is_irren, irren_cat, irren_label = False, None, None
        if is_pub or is_bank or (is_local and cg == "feriados locales ámbito normal"):
            if c is not None:
                is_irren = c["is_irrenunciable"]
                irren_cat = c["irren_category"]
                if irren_cat:
                    irren_label = [k for k, v in ORDINALS.items() if v == irren_cat][0] + " categoría"
            elif d and d["irren_tramos"]:
                for tr in d["irren_tramos"]:
                    if tr.get("irren") is False:
                        is_irren = False; break
                    if (tr["y_from"] or 0) <= e["year"] <= (tr["y_to"] or 9999):
                        is_irren, irren_cat, irren_label = True, tr["cat"], tr["label"]
                        notes.append(f"irrenunciabilidad inferida del rango de la definición ({tr['raw']})")
                        if conf == "high":
                            conf = "medium"
                        break

        nationwide, scope_text, regions, communes, iso = territory(e["location_raw"])
        if nationwide is None:
            nationwide = (d["nationwide"] if d else (not is_local))
        if is_local:
            nationwide = False
            if not (regions or communes or scope_text):
                notes.append("evento local sin alcance territorial detallado en la fuente")

        if c is not None:
            recurring, singular = c["recurrent"], c["singular"]
        else:
            n_years = len(years_by_key[(cg, e["source_anchor"])])
            recurring, singular = n_years > 1, n_years <= 1
            notes.append("recurrencia inferida por repetición anual en la fuente")

        legal = resolve_legal(d["legal_refs"], norms) if d else []
        if legal:
            methods.append("legal_mapping")
        if (is_pub or is_bank) and not legal:
            notes.append("feriado sin fundamento legal mapeado")

        if def_anchor is None:
            conf = "low"
        elif dconf == "low" and conf != "low":
            conf = "low"
        elif dconf == "medium" and conf == "high":
            conf = "medium"

        slug = slugify(e["name_es"]) or "evento"
        base_id = f"cl-{date_iso}-{slug}"
        id_counts[base_id] += 1
        ev_id = base_id if id_counts[base_id] == 1 else f"{base_id}-{id_counts[base_id]}"

        rec = {
            "id": ev_id, "date": date_iso, "start_date": date_iso,
            "end_date": e["end_date"].isoformat(), "year": e["year"],
            "weekday": e["weekday"], "name": {"es": e["name_es"], "en": None},
            "slug": slug, "summary_original": e["summary_original"],
            "type": e["default_type"], "category": category, "calendar_group": cg,
            "nationwide": bool(nationwide), "subdivisions": iso,
            "regions": regions, "communes": communes,
            "location_raw": e["location_raw"], "scope_text": scope_text,
            "is_public_holiday": is_pub, "is_bank_holiday": is_bank,
            "is_commemorative": is_comm, "is_local": is_local,
            "is_school": bool(c and c["is_school"]), "is_religious": is_religious,
            "is_civic": is_civic, "is_irrenunciable": is_irren,
            "irrenunciability_category": irren_cat,
            "irrenunciability_category_label": irren_label,
            "recurring": recurring, "singular": singular,
            "movable": bool(d and d["movable"]),
            "is_multiday": e["is_multiday"], "duration_days": e["duration_days"],
            "legal_basis": [
                {"type": l["type"], "number": l["number"], "year": l["year"],
                 "title": l["title"], "url": l["url"], "raw": l["raw"],
                 "role": l["role"], "articulo": l["articulo"],
                 "norma_anchor": l["norma_anchor"]} for l in legal],
            "definition": {
                "anchor": def_anchor,
                "fecha_raw": d["fecha_raw"] if d else None,
                "vigencia_raw": d["vigencia_raw"] if d else None,
                "ambito": d["ambito"] if d else None,
                "valido_en_raw": d["valido_en_raw"] if d else None,
                "caracter_raw": d["caracter"] if d else None,
                "irren_text_raw": d["irren_text"] if d else None,
                "source_file": d["source_file"] if d else None,
            },
            "source": {
                "source_file": e["source_file"], "source_calendar": e["source_calendar"],
                "source_url": e["source_url"], "source_anchor": e["source_anchor"],
                "definition_anchor": def_anchor, "uid": e["uid"],
                "last_modified": e["last_modified"], "dtstart_raw": e["dtstart_raw"],
                "dtend_raw": e["dtend_raw"], "extraction_method": methods,
                "confidence": conf, "notes": notes,
            },
        }
        # Curación manual verificada (fundamento legal de eventos sin ancla).
        apply_override(rec, norms, resolve_legal)
        out.append(rec)
    return out, {"norms": norms, "defs": defs, "cls": cls}


# --------------------------------------------------------------------------
# Vista pública: elimina procedencia interna y referencias internas de origen.
# Conserva todos los HECHOS (fechas, nombres, tipos, territorio, irrenunciabilidad,
# fundamento legal con URLs oficiales). NO conserva el bloque `source` ni anclas
# internas (que apuntan a archivos/host de las fuentes internas del proyecto).
# --------------------------------------------------------------------------
PUBLIC_DEFINITION_KEYS = ("fecha_raw", "vigencia_raw", "ambito", "valido_en_raw",
                          "caracter_raw", "irren_text_raw")


def to_public(e):
    pub = {k: v for k, v in e.items() if k not in ("source", "definition")}
    pub["legal_basis"] = [
        {"type": l["type"], "number": l["number"], "year": l["year"],
         "title": l["title"], "url": l["url"], "role": l["role"],
         "articulo": l["articulo"]}
        for l in e["legal_basis"]
    ]
    pub["definition"] = {k: e["definition"].get(k) for k in PUBLIC_DEFINITION_KEYS}
    pub["confidence"] = e["source"]["confidence"]
    return pub


# --------------------------------------------------------------------------
# Esquemas
# --------------------------------------------------------------------------
def event_schema():
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "https://calendario-chile/schema/calendar_chile_event.schema.json",
        "title": "Calendario Chile — Evento (vista pública)",
        "type": "object",
        "required": ["id", "date", "year", "name", "type", "calendar_group"],
        "properties": {
            "id": {"type": "string"},
            "date": {"type": "string", "format": "date"},
            "start_date": {"type": "string", "format": "date"},
            "end_date": {"type": "string", "format": "date"},
            "year": {"type": "integer", "minimum": 1981, "maximum": 2100},
            "weekday": {"type": "string", "enum": [
                "monday", "tuesday", "wednesday", "thursday", "friday",
                "saturday", "sunday"]},
            "name": {"type": "object", "properties": {
                "es": {"type": "string"}, "en": {"type": ["string", "null"]}}},
            "slug": {"type": "string"},
            "summary_original": {"type": "string"},
            "type": {"type": "string", "enum": sorted(TYPE_ENUM)},
            "category": {"type": "string", "enum": sorted(CATEGORY_ENUM)},
            "calendar_group": {"type": "string"},
            "nationwide": {"type": "boolean"},
            "subdivisions": {"type": "array", "items": {
                "type": "string", "pattern": "^CL-[A-Z]{2}$"}},
            "regions": {"type": "array", "items": {"type": "string"}},
            "communes": {"type": "array", "items": {"type": "string"}},
            "location_raw": {"type": ["string", "null"]},
            "scope_text": {"type": ["string", "null"]},
            "is_public_holiday": {"type": "boolean"},
            "is_bank_holiday": {"type": "boolean"},
            "is_commemorative": {"type": "boolean"},
            "is_local": {"type": "boolean"},
            "is_school": {"type": "boolean"},
            "is_religious": {"type": "boolean"},
            "is_civic": {"type": "boolean"},
            "is_irrenunciable": {"type": "boolean"},
            "irrenunciability_category": {"type": ["integer", "null"],
                                          "minimum": 1, "maximum": 5},
            "irrenunciability_category_label": {"type": ["string", "null"]},
            "recurring": {"type": ["boolean", "null"]},
            "singular": {"type": ["boolean", "null"]},
            "movable": {"type": "boolean"},
            "is_multiday": {"type": "boolean"},
            "duration_days": {"type": "integer", "minimum": 1},
            "legal_basis": {"type": "array", "items": {"type": "object"}},
            "definition": {"type": "object"},
            "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        },
    }


def holiday_schema():
    s = event_schema()
    s["$id"] = "https://calendario-chile/schema/calendar_chile_holiday.schema.json"
    s["title"] = "Calendario Chile — Feriado (público/bancario)"
    s["properties"]["type"] = {"type": "string",
                               "enum": ["public", "bank", "local", "restricted"]}
    return s


def datapackage(csv_cols):
    return {
        "name": "calendario-chile",
        "title": "Calendario de Chile — Feriados, días bancarios, locales y conmemorativos (1981–2100)",
        "description": ("Dataset estructurado del calendario chileno generado a partir "
                        "de fuentes internas del proyecto. Cobertura 1981–2100."),
        "licenses": [{"name": "MIT", "title": "MIT License",
                      "path": "https://opensource.org/license/mit"}],
        "version": "0.1.0-internal",
        "sources": [{"title": "Fuentes internas del proyecto (procesadas)"}],
        "resources": [
            {"name": "holidays", "path": "data/public/csv/calendar_chile_holidays.csv",
             "format": "csv", "mediatype": "text/csv", "encoding": "utf-8",
             "schema": {"fields": [{"name": c, "type": "string"} for c in csv_cols]}},
            {"name": "holidays-json",
             "path": "data/public/json/calendar_chile_holidays.json", "format": "json"},
        ],
    }
