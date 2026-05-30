#!/usr/bin/env python3
"""
Genera una **muestra curada para revisión humana** de los candidatos de matching
por nombre (issue #4), a partir del CSV del experimento. SOLO produce reportes;
no modifica datasets, no cambia `confidence`, no aplica overrides.

Uso:
  python3 scripts/audit_name_matching_sample.py \
    --input reports/low_confidence_name_matching_candidates.csv \
    --output reports/name_matching_manual_audit_sample.csv \
    --markdown reports/NAME_MATCHING_MANUAL_AUDIT.md \
    --sample-size 30 --seed 20260530
"""
import argparse
import csv
import random
import sys
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AUDIT_COLS = ["audit_id", "classification", "low_id", "low_name", "low_type",
              "low_calendar_group", "low_date", "candidate_id", "candidate_name",
              "candidate_type", "candidate_calendar_group", "candidate_date",
              "score", "proposed_decision", "reviewer_decision", "reviewer_notes"]


def fscore(r):
    try:
        return float(r["score"])
    except (TypeError, ValueError):
        return 0.0


def proposed(r):
    cls, t = r["classification"], r["low_type"]
    if t == "restricted":
        return "defer_to_issue_3"
    if cls == "auto_safe_candidate" and fscore(r) >= 0.999 and t == r["candidate_type"]:
        return "accept_candidate"
    if cls in ("auto_safe_candidate", "review_candidate"):
        return "review_manually"
    return "reject_candidate"


def diverse_by_name(rows, n, rng):
    """Selecciona hasta n filas maximizando diversidad de nombre y de año."""
    by_name = defaultdict(list)
    for r in rows:
        by_name[r["low_name"]].append(r)
    for nm in by_name:
        # ordenar por año, repartido (no solo consecutivos)
        by_name[nm].sort(key=lambda r: r["low_date"])
    names = sorted(by_name)
    rng.shuffle(names)
    out, idx = [], {nm: 0 for nm in names}
    # round-robin por nombre
    while len(out) < n and any(idx[nm] < len(by_name[nm]) for nm in names):
        for nm in names:
            if len(out) >= n:
                break
            lst = by_name[nm]
            if idx[nm] < len(lst):
                # repartir años: tomar índices espaciados
                step = max(1, len(lst) // max(1, (n // max(1, len(names))) + 1))
                out.append(lst[(idx[nm] * step) % len(lst)])
                idx[nm] += 1
    return out[:n]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", default="reports/low_confidence_name_matching_candidates.csv")
    ap.add_argument("--output", default="reports/name_matching_manual_audit_sample.csv")
    ap.add_argument("--markdown", default="reports/NAME_MATCHING_MANUAL_AUDIT.md")
    ap.add_argument("--sample-size", type=int, default=30)
    ap.add_argument("--seed", type=int, default=20260530)
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"[aviso] No existe el CSV de candidatos: {in_path}\n"
              "Ejecuta primero scripts/analyze_low_confidence_name_matching.py. "
              "No se generó muestra.", file=sys.stderr)
        return 0

    rows = list(csv.DictReader(open(in_path, encoding="utf-8")))
    rng = random.Random(args.seed)

    auto_comm = [r for r in rows if r["classification"] == "auto_safe_candidate"
                 and r["low_type"] == "commemorative"]
    auto_restr = [r for r in rows if r["classification"] == "auto_safe_candidate"
                  and r["low_type"] == "restricted"]
    review = [r for r in rows if r["classification"] == "review_candidate"]
    near = [r for r in rows if 0.95 <= fscore(r) <= 0.97]

    n = args.sample_size
    n_comm = round(n * 20 / 30)
    n_restr = round(n * 5 / 30)
    n_review = n - n_comm - n_restr

    notes = []
    sel_comm = diverse_by_name(auto_comm, n_comm, rng)
    if len(sel_comm) < n_comm:
        notes.append(f"auto_safe commemorative disponibles ({len(auto_comm)}, "
                     f"{len(set(r['low_name'] for r in auto_comm))} nombres distintos) "
                     f"menores a lo pedido; se incluyeron {len(sel_comm)}.")
    sel_restr = diverse_by_name(auto_restr, n_restr, rng)
    if len(sel_restr) < n_restr:
        notes.append(f"auto_safe restricted disponibles ({len(auto_restr)}) "
                     f"limitados; se incluyeron {len(sel_restr)}.")
    review.sort(key=lambda r: -fscore(r))
    sel_review = diverse_by_name(review[:max(n_review * 4, n_review)], n_review, rng) \
        if review else []
    if len(sel_review) < n_review:
        notes.append(f"review_candidate disponibles ({len(review)}) limitados; "
                     f"se incluyeron {len(sel_review)}.")

    # near-threshold: incluir TODOS los que existan (no duplicar)
    chosen_ids = {r["low_id"] for r in sel_comm + sel_restr + sel_review}
    sel_near = [r for r in near if r["low_id"] not in chosen_ids]
    if not near:
        notes.append("No existen candidatos con score en [0.95, 0.97]: los auto_safe "
                     "son coincidencias exactas (score 1.0) y los review caen por "
                     "debajo de 0.90. No hay casos limítrofes que auditar.")

    sample = sel_comm + sel_restr + sel_review + sel_near
    # dedup por low_id preservando orden
    seen, deduped = set(), []
    for r in sample:
        if r["low_id"] not in seen:
            seen.add(r["low_id"]); deduped.append(r)

    audit_rows = []
    for i, r in enumerate(deduped, 1):
        audit_rows.append({
            "audit_id": f"AU-{i:03d}", "classification": r["classification"],
            "low_id": r["low_id"], "low_name": r["low_name"], "low_type": r["low_type"],
            "low_calendar_group": r["low_calendar_group"], "low_date": r["low_date"],
            "candidate_id": r["candidate_id"], "candidate_name": r["candidate_name"],
            "candidate_type": r["candidate_type"],
            "candidate_calendar_group": r["candidate_calendar_group"],
            "candidate_date": r["candidate_date"], "score": r["score"],
            "proposed_decision": proposed(r),
            "reviewer_decision": "", "reviewer_notes": "",
        })

    # CSV de auditoría
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=AUDIT_COLS)
        w.writeheader()
        w.writerows(audit_rows)

    write_markdown(Path(args.markdown), args, in_path, audit_rows, notes,
                   auto_comm, auto_restr, review, near)
    print(f"[ok] muestra: {len(audit_rows)} casos -> {args.output}\n"
          f"     reporte -> {args.markdown}", file=sys.stderr)
    return 0


def write_markdown(path, args, in_path, audit_rows, notes, auto_comm, auto_restr,
                   review, near):
    by_cls = Counter(r["classification"] for r in audit_rows)
    by_type = Counter(r["low_type"] for r in audit_rows)
    by_dec = Counter(r["proposed_decision"] for r in audit_rows)
    L = ["# NAME_MATCHING_MANUAL_AUDIT\n",
         "Muestra curada para **revisión humana** de los candidatos de matching por "
         "nombre normalizado (issue #4), para estimar la **precisión real** antes de "
         "diseñar cualquier aplicación automática. **No se modificó ningún dato.**\n",
         "- **Fecha:** 2026-05-30",
         f"- **Fuente:** `{in_path.name}` (CSV del experimento)",
         f"- **Parámetros:** sample_size={args.sample_size}, seed={args.seed}\n",
         "## Metodología de muestreo\n",
         "Muestreo determinista (seed fija) con diversidad por nombre y por año:",
         "- ~20 `auto_safe_candidate` de tipo `commemorative`;",
         "- ~5 `auto_safe_candidate` de tipo `restricted` (marcados **solo issue #3, no "
         "auto-aplicar**);",
         "- ~5 `review_candidate` de mayor score;",
         "- **todos** los casos con score en [0.95, 0.97], si existieran.\n",
         "### Observación estructural (importante)\n",
         f"- Los **{len(auto_comm)} auto_safe commemorative** se reducen a "
         f"**{len(set(r['low_name'] for r in auto_comm))} nombres distintos** (sobre todo "
         "*semanas/meses/años nacionales* recurrentes cuyas ocurrencias en algunos años "
         "no traían ancla).",
         f"- Los **{len(auto_restr)} auto_safe restricted** son **"
         f"{len(set(r['low_name'] for r in auto_restr))} nombre** repetido por año "
         "(conmemoración escolar; pertenece a issue #3).",
         f"- **No hay casos con score en [0.95, 0.97]** ({len(near)}): los auto_safe son "
         "coincidencias **exactas** (score 1.0); los review caen por debajo de 0.90. El "
         "matching es **bimodal**, sin zona gris cercana al umbral.",
         "- Conclusión: auditar **pocas decisiones distintas de nombre** cubre casi todo "
         "el universo auto_safe.\n"]
    if notes:
        L.append("### Notas de redistribución\n")
        for nt in notes:
            L.append(f"- {nt}")
        L.append("")
    L += ["## Resumen de la muestra\n",
          f"- **Total de casos:** {len(audit_rows)}",
          f"- Por clasificación: {dict(by_cls)}",
          f"- Por tipo: {dict(by_type)}",
          f"- Por decisión propuesta (preliminar): {dict(by_dec)}\n",
          "## Casos seleccionados\n",
          "| audit_id | clasif. | low (nombre / fecha) | candidato | tipo | score | decisión propuesta |",
          "|---|---|---|---|---|--:|---|"]
    for r in audit_rows:
        L.append(f"| {r['audit_id']} | {r['classification'][:11]} | "
                 f"{r['low_name'][:34]} / {r['low_date']} | {r['candidate_name'][:30]} "
                 f"| {r['low_type']}→{r['candidate_type']} | {r['score']} | "
                 f"{r['proposed_decision']} |")
    L += ["\n## Cómo revisar\n",
          "1. Abrir `reports/name_matching_manual_audit_sample.csv`.",
          "2. Para cada fila, comparar `low_name` vs `candidate_name` y el contexto "
          "(tipo, calendario, fecha).",
          "3. Completar `reviewer_decision` (accept / reject / review / defer) y "
          "`reviewer_notes`. Dejar `proposed_decision` como referencia.\n",
          "## Criterio recomendado de decisión\n",
          "- **Aceptar** sólo si el nombre coincide **sustantivamente** (mismo evento).",
          "- **No aceptar** si cambia **tipo, alcance o sentido** del evento.",
          "- **No aceptar** casos `restricted`/escolares sin revisión jurídica separada "
          "(→ issue #3).",
          "- Si se acepta, la aplicación futura debe subir como **máximo a `medium`**, "
          "salvo fuente legal/definición firme.",
          "- Dejar **trazabilidad** del candidato usado (`candidate_id`).\n",
          "## Estimación de precisión\n",
          "Se completará tras la revisión humana (campo `reviewer_decision`). Dado que "
          "los auto_safe son coincidencias **exactas de nombre** y mismo tipo "
          "(conmemorativo↔conmemorativo), se espera **precisión alta**, pero debe "
          "confirmarse manualmente sobre la muestra antes de cualquier aplicación.\n",
          "> **Advertencia:** este documento es solo una muestra para revisión. **No se "
          "modificó ningún dato, ni `confidence`, ni se aplicaron overrides.**\n"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
