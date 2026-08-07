#!/usr/bin/env python3
"""
Agrupa los candidatos de matching por nombre (issue #4) en **familias revisables**
(por nombre normalizado + tipo + calendario + clasificación), para que la revisión
humana se haga por familia y no evento por evento.

SOLO genera reportes; no modifica datasets, ni `confidence`, ni aplica overrides.

Uso:
  python3 scripts/group_name_matching_families.py \
    --input reports/low_confidence_name_matching_candidates.csv \
    --csv reports/name_matching_families.csv \
    --markdown reports/NAME_MATCHING_FAMILY_REVIEW.md
"""
import argparse
import csv
import re
import sys
import unicodedata
from collections import defaultdict, Counter
from pathlib import Path


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "")
                   if unicodedata.category(c) != "Mn")


def norm(s):
    s = strip_accents((s or "").lower())
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def year(d):
    return d[:4] if d and len(d) >= 4 else ""


FAMILY_COLS = ["family_id", "classification", "low_type", "candidate_type",
               "low_name_normalized", "candidate_name_normalized",
               "representative_low_name", "representative_candidate_name",
               "low_calendar_group", "candidate_calendar_group",
               "score_min", "score_max", "event_count", "first_year", "last_year",
               "sample_low_ids", "sample_candidate_ids",
               "proposed_family_decision", "reviewer_family_decision",
               "reviewer_notes"]


def proposed_decision(classification, low_type, candidate_type, score_min):
    # Escolares / restricted SIEMPRE se difieren a issue #3.
    if low_type == "restricted" or candidate_type == "restricted":
        return "defer_to_issue_3"
    if classification == "auto_safe_candidate":
        # exacto + tipo conmemorativo compatible -> familia aceptable (preliminar)
        if score_min >= 0.999 and low_type == candidate_type:
            return "accept_family"
        return "review_family"
    if classification == "review_candidate":
        return "review_family"
    return "reject_family"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", default="reports/low_confidence_name_matching_candidates.csv")
    ap.add_argument("--csv", default="reports/name_matching_families.csv")
    ap.add_argument("--markdown", default="reports/NAME_MATCHING_FAMILY_REVIEW.md")
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"[aviso] No existe el CSV de candidatos: {in_path}\n"
              "Ejecuta primero scripts/analyze_low_confidence_name_matching.py. "
              "No se generaron familias.", file=sys.stderr)
        return 0

    rows = list(csv.DictReader(open(in_path, encoding="utf-8")))
    # Solo agrupamos candidatos con candidato real (auto_safe / review).
    cand = [r for r in rows if r["classification"] in
            ("auto_safe_candidate", "review_candidate") and r["candidate_id"]]

    groups = defaultdict(list)
    for r in cand:
        key = (r["classification"], r["low_type"], r["candidate_type"],
               norm(r["low_name"]), norm(r["candidate_name"]),
               r["low_calendar_group"], r["candidate_calendar_group"])
        groups[key].append(r)

    families = []
    for i, (key, items) in enumerate(sorted(groups.items(),
                                            key=lambda kv: (-len(kv[1]), kv[0])), 1):
        cls, lt, ct, lnn, cnn, lcg, ccg = key
        scores = [float(x["score"]) for x in items if x["score"]]
        years = sorted(y for y in (year(x["low_date"]) for x in items) if y)
        low_ids = [x["low_id"] for x in items]
        cand_ids = sorted(set(x["candidate_id"] for x in items))
        smin = round(min(scores), 4) if scores else ""
        families.append({
            "family_id": f"FAM-{i:03d}", "classification": cls,
            "low_type": lt, "candidate_type": ct,
            "low_name_normalized": lnn, "candidate_name_normalized": cnn,
            "representative_low_name": items[0]["low_name"],
            "representative_candidate_name": items[0]["candidate_name"],
            "low_calendar_group": lcg, "candidate_calendar_group": ccg,
            "score_min": smin, "score_max": round(max(scores), 4) if scores else "",
            "event_count": len(items),
            "first_year": years[0] if years else "",
            "last_year": years[-1] if years else "",
            "sample_low_ids": " ".join(low_ids[:5]),
            "sample_candidate_ids": " ".join(cand_ids[:5]),
            "proposed_family_decision": proposed_decision(cls, lt, ct,
                                                          float(smin) if smin != "" else 0.0),
            "reviewer_family_decision": "", "reviewer_notes": "",
        })

    Path(args.csv).parent.mkdir(parents=True, exist_ok=True)
    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FAMILY_COLS)
        w.writeheader(); w.writerows(families)

    write_markdown(Path(args.markdown), in_path, families, cand)
    print(f"[ok] {len(families)} familias (de {len(cand)} candidatos) -> {args.csv}\n"
          f"     reporte -> {args.markdown}", file=sys.stderr)
    return 0


def write_markdown(path, in_path, families, cand):
    by_dec = Counter(f["proposed_family_decision"] for f in families)
    auto = [f for f in families if f["classification"] == "auto_safe_candidate"
            and f["proposed_family_decision"] == "accept_family"]
    deferred = [f for f in families if f["proposed_family_decision"] == "defer_to_issue_3"]
    review = [f for f in families if f["classification"] == "review_candidate"]
    auto_review = [f for f in families if f["classification"] == "auto_safe_candidate"
                   and f["proposed_family_decision"] == "review_family"]

    def fam_table(fams):
        out = ["| family_id | familia (low → candidato) | tipo | nº ev. | años | score | decisión propuesta |",
               "|---|---|---|--:|---|--:|---|"]
        for f in fams:
            yr = f"{f['first_year']}–{f['last_year']}" if f["first_year"] else "—"
            sc = f["score_min"] if f["score_min"] == f["score_max"] else f"{f['score_min']}–{f['score_max']}"
            out.append(f"| {f['family_id']} | {f['representative_low_name'][:34]} → "
                       f"{f['representative_candidate_name'][:30]} | "
                       f"{f['low_type']}→{f['candidate_type']} | {f['event_count']} | "
                       f"{yr} | {sc} | {f['proposed_family_decision']} |")
        return out

    L = ["# NAME_MATCHING_FAMILY_REVIEW\n",
         "Revisión **por familia de nombre** (no evento por evento) de los candidatos "
         "de matching por nombre normalizado (issue #4), para decidir si los `auto_safe` "
         "conmemorativos pueden aplicarse en una fase posterior. **No se modificó ningún "
         "dato.**\n",
         "- **Fecha:** 2026-05-30",
         f"- **Insumo:** `{in_path.name}` (CSV de candidatos del experimento)",
         f"- **Candidatos agrupados:** {len(cand)} → **{len(families)} familias**\n",
         "## Resumen\n",
         f"- **Total de familias:** {len(families)}",
         f"- `accept_family` (auto_safe conmemorativas): **{len(auto)}**",
         f"- `review_family` (auto_safe a revisar + review_candidate): "
         f"**{len(auto_review) + len(review)}**",
         f"- `defer_to_issue_3` (escolares/restricted): **{len(deferred)}**",
         f"- Decisiones propuestas: {dict(by_dec)}\n",
         "## Familias auto_safe conmemorativas (candidatas a aceptación)\n"]
    L += fam_table(auto) if auto else ["_(ninguna)_"]
    L += ["\n## Familias auto_safe a revisar\n"]
    L += fam_table(auto_review) if auto_review else ["_(ninguna)_"]
    L += ["\n## Familias review_candidate\n"]
    L += fam_table(review) if review else ["_(ninguna)_"]
    L += ["\n## Familias escolares / restricted (diferidas a issue #3)\n",
          "> **No se aplican ni se resuelven aquí.** Requieren revisión jurídica "
          "separada (issue #3).\n"]
    L += fam_table(deferred) if deferred else ["_(ninguna)_"]

    L += ["\n## Recomendación por familia\n",
          "- **`accept_family`** (auto_safe conmemorativas, coincidencia exacta de "
          "nombre, mismo tipo): aprobables por el humano; la aplicación futura subiría "
          "como máximo a `confidence: medium`, registrando el `candidate_id`.",
          "- **`review_family`**: revisar el nombre/sentido caso por caso.",
          "- **`defer_to_issue_3`**: no tocar aquí (escolares/restricted).",
          "- **`reject_family`**: descartar.\n",
          "## Criterios de aceptación\n",
          "1. El nombre normalizado de la familia coincide **sustantivamente** (mismo "
          "evento), no solo por palabras genéricas.",
          "2. **No** cambia tipo, alcance ni sentido (conmemorativo↔conmemorativo).",
          "3. La familia es **recurrente y coherente** entre años (la diferencia es solo "
          "el ancla faltante en algunas ocurrencias).",
          "4. Escolares/restricted **excluidos** (→ issue #3).",
          "5. La aplicación se hará **en rama aparte, con tests de no regresión**, sin "
          "tocar feriados públicos estables.\n",
          "## Decisión humana\n",
          "Completar en `reports/name_matching_families.csv` los campos "
          "`reviewer_family_decision` (accept_family / review_family / defer_to_issue_3 / "
          "reject_family) y `reviewer_notes`. **Una decisión por familia** cubre todas sus "
          "ocurrencias.\n",
          "> **Advertencia:** este documento es preparación para decisión humana. **No se "
          "modificó ningún dato, ni `confidence`, ni se aplicaron overrides.**\n"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
