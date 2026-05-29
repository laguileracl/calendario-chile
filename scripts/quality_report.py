"""Genera reports/QUALITY_REPORT.md a partir del dataset completo."""
import _bootstrap  # noqa
from collections import Counter

from calendario_chile import build_events
from calendario_chile.validate import metrics, run_tests
from calendario_chile.config import REPORTS, ensure_dirs


def main():
    ensure_dirs()
    ev, _ = build_events()
    m = metrics(ev)
    t = run_tests(ev)
    L = ["# QUALITY_REPORT — calendario-chile\n",
         "Validación del dataset generado a partir de fuentes internas del proyecto.\n",
         f"- **Total de eventos:** {m['total']:,}",
         f"- **Rango de fechas:** {m['date_min']} → {m['date_max']}",
         f"- **Años cubiertos:** {min(m['by_year'])}–{max(m['by_year'])} "
         f"({len(m['by_year'])})\n",
         "## Por calendario de origen\n", "| Grupo | Eventos |\n|---|--:|"]
    for k, v in m["by_calendar"].most_common():
        L.append(f"| {k} | {v:,} |")
    L += ["\n## Por tipo\n", "| type | Eventos |\n|---|--:|"]
    for k, v in m["by_type"].most_common():
        L.append(f"| {k} | {v:,} |")
    L += ["\n## Por categoría\n", "| category | Eventos |\n|---|--:|"]
    for k, v in m["by_category"].most_common():
        L.append(f"| {k} | {v:,} |")
    L += ["\n## Confianza\n", "| confidence | Eventos |\n|---|--:|"]
    for k, v in m["by_confidence"].most_common():
        L.append(f"| {k} | {v:,} |")
    L += ["\n## Por década\n", "| Década | Eventos |\n|---|--:|"]
    dec = Counter()
    for y, c in m["by_year"].items():
        dec[(y // 10) * 10] += c
    for d in sorted(dec):
        L.append(f"| {d}s | {dec[d]:,} |")
    L += ["\n## Indicadores de calidad\n", "| Indicador | Valor |\n|---|--:|"]
    for k, label in [
        ("exact_dupes", "Duplicados exactos"),
        ("semantic_dupes", "Posibles duplicados semánticos"),
        ("no_date", "Eventos sin fecha"), ("no_name", "Eventos sin nombre"),
        ("bad_type", "Tipo no válido"), ("bad_category", "Categoría no válida"),
        ("local_no_territory", "Locales sin alcance territorial"),
        ("feriado_no_legal", "Feriados/bancarios sin fundamento legal"),
        ("dtend_problematic", "DTEND problemático"),
        ("multiday", "Eventos multi-día"), ("recurring", "Recurrentes"),
        ("singular", "Singulares"), ("irrenunciables", "Irrenunciables"),
        ("with_subdivisions", "Con subdivisión ISO")]:
        L.append(f"| {label} | {m[k]:,} |")
    L += ["\n## Tests automáticos\n", "| Test | Resultado | Detalle |\n|---|:--:|---|"]
    for name, ok, detail in t:
        L.append(f"| {name} | {'✅' if ok else '❌'} | {detail} |")
    passed = sum(1 for _, ok, _ in t if ok)
    L.append(f"\n**{passed}/{len(t)} tests aprobados.**\n")
    (REPORTS / "QUALITY_REPORT.md").write_text("\n".join(L), encoding="utf-8")
    print(f"[quality_report] {passed}/{len(t)} tests -> reports/QUALITY_REPORT.md")


if __name__ == "__main__":
    main()
