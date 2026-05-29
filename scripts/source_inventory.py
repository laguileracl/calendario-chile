"""Inventario de fuentes internas con hash SHA-256 (trazabilidad/auditoría).
Salida: reports/SOURCE_INVENTORY.md + data/internal/source_inventory/inventory.json
Describe el origen como fuentes internas del proyecto, sin terceros.
"""
import _bootstrap  # noqa
import json
import hashlib

from calendario_chile import build_events
from calendario_chile.config import RAW_ICS, RAW_HTML, SOURCE_INV, REPORTS, ensure_dirs
from calendario_chile.constants import ICS_MAP


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ensure_dirs()
    events, _ = build_events()
    from collections import Counter
    cnt = Counter(e["source"]["source_file"] for e in events)

    inv = {"ics": [], "html": []}
    L = ["# SOURCE_INVENTORY — Fuentes internas\n",
         "Inventario de los archivos fuente internos del proyecto, con tamaño y "
         "hash SHA-256 para trazabilidad y reproducibilidad. **Material interno.**\n",
         "## Calendarios de origen (.ics)\n",
         "| Archivo | Eventos | Grupo | type | Tamaño | SHA-256 (12) |\n|---|--:|---|---|--:|---|"]
    for f in sorted(RAW_ICS.glob("*.ics")):
        grp, typ = ICS_MAP[f.name]
        rel = f"data/internal/raw/ics/{f.name}"
        h = sha(f)
        L.append(f"| `{f.name}` | {cnt.get(rel,0):,} | {grp} | {typ} | "
                 f"{f.stat().st_size//1024} KB | `{h[:12]}` |")
        inv["ics"].append({"file": f.name, "events": cnt.get(rel, 0),
                           "group": grp, "type": typ,
                           "bytes": f.stat().st_size, "sha256": h})

    L += ["\n## Documentos de apoyo (HTML)\n",
          "Aportan definiciones, clasificación por ocurrencia y fundamento legal "
          "(números/identificadores de normas y enlaces a fuentes oficiales).\n",
          "| Archivo | Tamaño | SHA-256 (12) |\n|---|--:|---|"]
    roles = ["index.html", "DiasNacionales.html", "normas.html", "anexos.html"]
    for name in roles:
        p = RAW_HTML / name
        if p.exists():
            h = sha(p)
            L.append(f"| `{name}` | {p.stat().st_size//1024} KB | `{h[:12]}` |")
            inv["html"].append({"file": name, "bytes": p.stat().st_size, "sha256": h})
    pages = sorted(RAW_HTML.glob("[12][0-9][0-9][0-9]-[12][0-9][0-9][0-9].html"))
    L.append(f"\n{len(pages)} páginas anuales adicionales aportan la clasificación "
             "por ocurrencia (irrenunciabilidad por año, carácter, recurrencia).\n")
    for p in pages:
        inv["html"].append({"file": p.name, "bytes": p.stat().st_size, "sha256": sha(p)})

    (SOURCE_INV / "inventory.json").write_text(
        json.dumps(inv, ensure_ascii=False, indent=2), encoding="utf-8")
    (REPORTS / "SOURCE_INVENTORY.md").write_text("\n".join(L), encoding="utf-8")
    print(f"[source_inventory] {len(inv['ics'])} ics + {len(inv['html'])} html "
          f"-> reports/SOURCE_INVENTORY.md")


if __name__ == "__main__":
    main()
