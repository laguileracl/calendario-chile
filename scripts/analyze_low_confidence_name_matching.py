#!/usr/bin/env python3
"""
Experimento (SOLO ANÁLISIS) — dimensionar cuántos eventos `low-confidence`
podrían recuperarse emparejándolos por **nombre normalizado** contra los eventos
ya resueltos (high/medium confidence).

NO modifica datasets, NO aplica overrides, NO cambia `confidence`. Solo genera
reportes en `reports/`. El insumo es un dataset canónico/intermedio LOCAL (con
bloque `source`), que NO forma parte del repo público.

Uso:
  python3 scripts/analyze_low_confidence_name_matching.py \
    --input <ruta>/data/internal/intermediate/calendar_chile_events.full.json \
    --output reports/LOW_CONFIDENCE_NAME_MATCHING_EXPERIMENT.md \
    --min-score 0.88 --max-candidates 5
"""
import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# --- Normalización conservadora ------------------------------------------
_SUFFIX_PAREN = re.compile(r"\((?:irrenunciable|escolar|bancario|religioso|"
                           r"feriado religioso|feriado)\)")
_PREFIXES = [
    "semana nacional de la ", "semana nacional de los ", "semana nacional de ",
    "mes nacional de la ", "mes nacional de los ", "mes nacional de ",
    "anio nacional de la ", "anio nacional de los ", "anio nacional de ",
    "dia nacional de la ", "dia nacional de los ", "dia nacional de ",
    "dia internacional de la ", "dia internacional de los ", "dia internacional de ",
    "dia de la ", "dia de los ", "dia del ", "dia de ",
    "feriado ",
]


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def norm_name(name: str) -> str:
    """Normalización para comparar (conservadora: no quita palabras sustantivas)."""
    s = strip_accents((name or "").lower())
    s = _SUFFIX_PAREN.sub(" ", s)                 # quita sufijos entre paréntesis
    s = re.sub(r"[^a-z0-9\s]", " ", s)            # puntuación menor -> espacio
    s = re.sub(r"\s+", " ", s).strip()
    # remoción controlada de prefijos genéricos (una sola pasada)
    for p in _PREFIXES:
        if s.startswith(p):
            s = s[len(p):].strip()
            break
    return re.sub(r"\s+", " ", s).strip()


def tokens(s: str):
    return set(t for t in s.split() if len(t) > 2)


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def score(a_norm, b_norm):
    if a_norm == b_norm and a_norm:
        return 1.0
    seq = SequenceMatcher(None, a_norm, b_norm).ratio()
    jac = jaccard(tokens(a_norm), tokens(b_norm))
    return max(seq, jac)


# --- Carga de eventos -----------------------------------------------------
def confidence(e):
    return (e.get("source") or {}).get("confidence") or e.get("confidence")


def source_anchor(e):
    return (e.get("source") or {}).get("source_anchor")


def low_reason(e):
    notes = (e.get("source") or {}).get("notes") or []
    if not source_anchor(e):
        return "sin ancla en .ics"
    if any("sin definición" in n for n in notes):
        return "ancla no encontrada en definiciones"
    return "otro"


def compatible_type(t_low, t_cand):
    # feriados (público/bancario/restringido/local) entre sí son comparables;
    # conmemorativos entre sí también. Mezclar feriado<->conmemorativo = conflicto.
    feriado = {"public", "bank", "restricted", "local"}
    if t_low == t_cand:
        return True
    if t_low in feriado and t_cand in feriado:
        return True
    return False


def conflicts(low, cand):
    reasons = []
    if not compatible_type(low["type"], cand["type"]):
        reasons.append(f"tipo {low['type']}≠{cand['type']}")
    if low["nationwide"] != cand["nationwide"]:
        reasons.append("ámbito nacional/local distinto")
    if low["is_multiday"] != cand["is_multiday"]:
        reasons.append("duración (multidía) distinta")
    return reasons


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True,
                    help="dataset canónico/intermedio LOCAL (con bloque source)")
    ap.add_argument("--output", default="reports/LOW_CONFIDENCE_NAME_MATCHING_EXPERIMENT.md")
    ap.add_argument("--csv", default="reports/low_confidence_name_matching_candidates.csv")
    ap.add_argument("--min-score", type=float, default=0.88)
    ap.add_argument("--max-candidates", type=int, default=5)
    ap.add_argument("--auto-score", type=float, default=0.95)
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"[aviso] No se encontró el dataset de entrada: {in_path}\n"
              "Este análisis requiere un dataset canónico/intermedio LOCAL "
              "(con bloque `source`), que NO forma parte del repo público.\n"
              "Genera los datos con el pipeline o indica otra ruta con --input. "
              "No se produjo ningún reporte.", file=sys.stderr)
        return 0

    print(f"[1/4] Cargando {in_path} …", file=sys.stderr)
    events = json.loads(in_path.read_text(encoding="utf-8"))

    # Slim de cada evento a lo necesario
    def slim(e):
        return {
            "id": e["id"], "name": e["name"]["es"], "norm": norm_name(e["name"]["es"]),
            "type": e["type"], "calendar_group": e["calendar_group"],
            "date": e["date"], "nationwide": bool(e["nationwide"]),
            "is_multiday": bool(e["is_multiday"]),
            "anchor": (e.get("definition") or {}).get("anchor"),
            "conf": confidence(e),
        }

    low, ref = [], []
    for e in events:
        s = slim(e)
        if s["conf"] == "low":
            s["reason"] = low_reason(e)
            low.append(s)
        elif s["conf"] in ("high", "medium"):
            ref.append(s)

    # Índice de referencia por nombre normalizado (representante = el más frecuente)
    by_norm = defaultdict(list)
    for r in ref:
        if r["norm"]:
            by_norm[r["norm"]].append(r)
    # representante por norma: prioriza con anchor y tipo más común
    ref_index = {}
    for nm, rs in by_norm.items():
        types = Counter(r["type"] for r in rs)
        rep = sorted(rs, key=lambda r: (r["anchor"] is None, ))[0]
        ref_index[nm] = {"rep": rep, "count": len(rs),
                         "types": dict(types)}
    ref_norms = list(ref_index.keys())
    ref_token_sets = {nm: tokens(nm) for nm in ref_norms}

    print(f"[2/4] low={len(low)}  referencias(high/medium)={len(ref)}  "
          f"nombres_norm_referencia={len(ref_norms)}", file=sys.stderr)

    # Para cada low, generar candidatos
    rows = []
    print("[3/4] Emparejando por nombre normalizado …", file=sys.stderr)
    for i, lo in enumerate(low):
        cands = []
        if not lo["norm"]:
            rows.append({**_emptyrow(lo), "classification": "no_candidate",
                         "recommended_action": "sin nombre normalizable"})
            continue
        # 1) match exacto normalizado
        if lo["norm"] in ref_index:
            rep = ref_index[lo["norm"]]["rep"]
            cands.append((1.0, rep))
        else:
            # 2) puntaje contra referencias (filtrado por solapamiento de tokens)
            lt = tokens(lo["norm"])
            best = []
            for nm in ref_norms:
                if not (lt & ref_token_sets[nm]):
                    continue
                sc = score(lo["norm"], nm)
                if sc >= args.min_score:
                    best.append((sc, ref_index[nm]["rep"]))
            best.sort(key=lambda x: -x[0])
            cands = best[:args.max_candidates]

        if not cands:
            rows.append({**_emptyrow(lo), "classification": "no_candidate",
                         "recommended_action": "mantener; sin candidato confiable"})
            continue

        for sc, cand in cands[:args.max_candidates]:
            confl = conflicts(lo, cand)
            if confl:
                cls = "conflict"
                action = "descartar/revisión manual (conflicto)"
            elif sc >= args.auto_score and compatible_type(lo["type"], cand["type"]):
                cls = "auto_safe_candidate"
                action = ("re-emparejar (revisión ligera) → subiría a confidence "
                          "medium; NO aplicado en este experimento")
            elif sc >= args.min_score:
                cls = "review_candidate"
                action = "revisión humana"
            else:
                cls = "no_candidate"
                action = "mantener"
            rows.append({
                "low_id": lo["id"], "low_name": lo["name"], "low_type": lo["type"],
                "low_calendar_group": lo["calendar_group"], "low_date": lo["date"],
                "low_confidence_reason": lo["reason"],
                "candidate_id": cand["id"], "candidate_name": cand["name"],
                "candidate_type": cand["type"],
                "candidate_calendar_group": cand["calendar_group"],
                "candidate_date": cand["date"], "score": round(sc, 4),
                "classification": cls,
                "conflict_reason": "; ".join(confl),
                "recommended_action": action,
            })

    write_csv(Path(args.csv), rows)
    write_report(Path(args.output), args, in_path, low, ref, ref_norms, rows)
    print(f"[4/4] Reporte: {args.output}\n        CSV: {args.csv}", file=sys.stderr)
    return 0


def _emptyrow(lo):
    return {"low_id": lo["id"], "low_name": lo["name"], "low_type": lo["type"],
            "low_calendar_group": lo["calendar_group"], "low_date": lo["date"],
            "low_confidence_reason": lo.get("reason", ""), "candidate_id": "",
            "candidate_name": "", "candidate_type": "", "candidate_calendar_group": "",
            "candidate_date": "", "score": "", "conflict_reason": ""}


CSV_COLS = ["low_id", "low_name", "low_type", "low_calendar_group", "low_date",
            "low_confidence_reason", "candidate_id", "candidate_name",
            "candidate_type", "candidate_calendar_group", "candidate_date",
            "score", "classification", "conflict_reason", "recommended_action"]


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in CSV_COLS})


def _best_per_low(rows):
    """Mejor fila por low_id (mayor score, evitando conflictos para 'recuperable')."""
    best = {}
    order = {"auto_safe_candidate": 3, "review_candidate": 2, "conflict": 1,
             "no_candidate": 0}
    for r in rows:
        k = r["low_id"]
        cur = best.get(k)
        rank = (order.get(r["classification"], 0), r["score"] if isinstance(r["score"], float) else 0)
        if cur is None or rank > cur[0]:
            best[k] = (rank, r)
    return [v[1] for v in best.values()]


def write_report(path, args, in_path, low, ref, ref_norms, rows):
    best = _best_per_low(rows)
    by_class = Counter(r["classification"] for r in best)
    no_anchor = sum(1 for lo in low if lo["reason"] == "sin ancla en .ics")
    # por tipo (mejor clasificación por low)
    type_class = defaultdict(Counter)
    low_type = {lo["id"]: lo["type"] for lo in low}
    for r in best:
        type_class[low_type.get(r["low_id"], "?")][r["classification"]] += 1

    L = ["# LOW_CONFIDENCE_NAME_MATCHING_EXPERIMENT\n",
         "Experimento de recuperación de eventos `low-confidence` por **nombre "
         "normalizado** (issue #4). **Solo análisis — no se modificó ningún dato.**\n",
         "- **Fecha:** 2026-05-30",
         f"- **Input (local, no publicado):** `{in_path.name}` "
         "(dataset canónico/intermedio interno; ruta local fuera del repo público)",
         f"- **Parámetros:** min_score={args.min_score}, auto_score={args.auto_score}, "
         f"max_candidates={args.max_candidates}",
         f"- **Referencias (high/medium):** {len(ref):,} eventos / {len(ref_norms):,} "
         "nombres normalizados distintos\n",
         "## Universo analizado\n",
         f"- **low-confidence analizados:** {len(low):,}",
         f"- de ellos **sin ancla en `.ics`:** {no_anchor:,}\n",
         "## Resultados por clasificación (mejor candidato por evento)\n",
         "| Clasificación | Eventos | % |\n|---|--:|--:|"]
    for k in ["auto_safe_candidate", "review_candidate", "conflict", "no_candidate"]:
        v = by_class.get(k, 0)
        L.append(f"| {k} | {v:,} | {100*v/max(1,len(low)):.1f}% |")

    L += ["\n## Resultados por tipo de evento\n",
          "| type | auto_safe | review | conflict | no_candidate |\n|---|--:|--:|--:|--:|"]
    for t in ["commemorative", "restricted", "public", "bank", "local"]:
        c = type_class.get(t, Counter())
        L.append(f"| {t} | {c.get('auto_safe_candidate',0)} | "
                 f"{c.get('review_candidate',0)} | {c.get('conflict',0)} | "
                 f"{c.get('no_candidate',0)} |")

    def section(title, cls, n):
        items = [r for r in best if r["classification"] == cls]
        items.sort(key=lambda r: -(r["score"] if isinstance(r["score"], float) else 0))
        out = [f"\n## {title} (top {min(n,len(items))} de {len(items)})\n",
               "| score | low → candidato | tipo | calendario |\n|--:|---|---|---|"]
        for r in items[:n]:
            out.append(f"| {r['score']} | {r['low_name'][:40]} → {r['candidate_name'][:40]} "
                       f"| {r['low_type']}→{r['candidate_type']} | {r['low_calendar_group']} |")
        return out

    L += section("Top auto_safe_candidate", "auto_safe_candidate", 30)
    L += section("Top review_candidate", "review_candidate", 30)

    confl = [r for r in best if r["classification"] == "conflict"]
    L += [f"\n## Conflicts (todos: {len(confl)})\n",
          "| score | low → candidato | conflicto |\n|--:|---|---|"]
    for r in sorted(confl, key=lambda r: -(r["score"] if isinstance(r["score"], float) else 0)):
        L.append(f"| {r['score']} | {r['low_name'][:38]} → {r['candidate_name'][:38]} "
                 f"| {r['conflict_reason']} |")

    auto = by_class.get("auto_safe_candidate", 0)
    review = by_class.get("review_candidate", 0)
    mvp_types = {"public", "bank", "restricted", "local"}
    auto_public = sum(1 for r in best if r["classification"] == "auto_safe_candidate"
                      and low_type.get(r["low_id"]) in mvp_types)
    auto_future = auto - auto_public
    L += ["\n## Estimación de recuperación\n",
          f"- **Recuperación segura estimada (auto_safe):** {auto:,} eventos "
          f"({100*auto/max(1,len(low)):.1f}% de los low-confidence) — subirían a "
          "`confidence: medium` tras revisión ligera.",
          f"  - de ellos **{auto_public} afectan datos públicos** (type restringido/"
          "feriado) → tratar con cautela vía issue #3 (revisión manual), no auto-aplicar.",
          f"  - **{auto_future} son capas futuras** (conmemorativos) → candidatos a la "
          "línea B de v0.2.0.",
          f"- **Candidatos a revisión humana (review):** {review:,}.",
          f"- **Sin candidato confiable:** {by_class.get('no_candidate',0):,}.",
          f"- **Conflictos (no recuperables automáticamente):** {by_class.get('conflict',0):,}.\n",
          "## Recomendación de siguiente paso\n",
          "1. Validar manualmente una muestra de `auto_safe_candidate` (p. ej. 30) "
          "para confirmar precisión antes de cualquier aplicación.",
          "2. Si la precisión es alta, diseñar una aplicación **conservadora** (en una "
          "rama aparte, con tests de no regresión) que solo suba a `confidence: medium` "
          "y registre la procedencia; **nunca** tocar feriados públicos estables sin test.",
          "3. Tratar `review_candidate` por lotes con revisión humana; `conflict` y "
          "`no_candidate` quedan para análisis caso a caso.\n",
          "> **Advertencia:** este experimento **no modificó ningún dato**. No se "
          "aplicaron overrides, no se cambió el `confidence` de ningún evento, no se "
          "alteraron datasets públicos ni canónicos.\n"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
