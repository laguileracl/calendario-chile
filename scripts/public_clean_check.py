"""
Verificación anti-contaminación del repo PÚBLICO.

Confirma que el repositorio no contiene material interno ni referencias a
fuentes/terceros externos, que la licencia MIT está declarada y que no quedan
rutas absolutas locales. Escribe `reports/PUBLIC_REPO_CLEAN_CHECK.md`.
No escribe en `data/internal/` (no existe en el repo público).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Patrones de terceros / fuentes externas que NO deben aparecer.
FORBIDDEN = ["farah", "feriadoschilenos"]
# Afirmaciones de licencia pendiente. Sólo se consideran BLOQUEANTES en los
# archivos de declaración autoritativa de licencia (abajo). En documentación
# histórica (CHANGELOG, reports, ADR) pueden aparecer como referencia al estado
# ya superado ("se eliminó el estado de 'licencia pendiente'") y son informativas.
PENDING = ["licencia pendiente", "licencia por definir", "pending license",
           "LicenseRef-PENDING", "no license selected", "licencia definitiva pendiente"]
# Archivos donde la licencia se declara de forma autoritativa.
AUTHORITATIVE = {
    "README.md", "pyproject.toml", "LICENSE", "datapackage.json",
    "metadata.json", "index.json", "legal_notes.md",
}
ABS_PATH = "/Users/"
TOKEN_RE = re.compile("|".join(re.escape(t) for t in FORBIDDEN), re.I)
PENDING_RE = re.compile("|".join(re.escape(t) for t in PENDING), re.I)

# Archivos que nombran patrones por diseño (escáneres/tests/este reporte).
SKIP = {"public_clean_check.py", "validate_public.py", "test_public_data.py",
        "PUBLIC_REPO_CLEAN_CHECK.md"}
SKIP_SUFFIX = (".sqlite", ".parquet", ".pyc", ".ics")


def scan():
    third, pending_active, pending_hist, abspath = [], [], [], []
    for f in ROOT.rglob("*"):
        if not f.is_file() or f.suffix in SKIP_SUFFIX or f.name in SKIP:
            continue
        if "__pycache__" in f.parts:
            continue
        rel = f.relative_to(ROOT)
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if TOKEN_RE.search(txt):
            third.append(rel)
        if PENDING_RE.search(txt):
            (pending_active if f.name in AUTHORITATIVE else pending_hist).append(rel)
        if ABS_PATH in txt:
            abspath.append(rel)
    return third, pending_active, pending_hist, abspath


def structural_checks():
    checks = []
    checks.append(("No existe data/internal/", not (ROOT / "data" / "internal").exists()))
    checks.append(("No existe LICENSE_DRAFT.md", not (ROOT / "LICENSE_DRAFT.md").exists()))
    checks.append(("No existe OBSOLETE_LICENSE_DRAFT.md",
                   not list(ROOT.rglob("OBSOLETE_LICENSE_DRAFT.md"))))
    checks.append(("No hay fuentes raw (.html de fuente / carpeta raw)",
                   not list(ROOT.rglob("data/internal/raw/*")) and not (ROOT / "data" / "raw").exists()))
    checks.append(("LICENSE (MIT) presente", (ROOT / "LICENSE").exists()
                   and "MIT License" in (ROOT / "LICENSE").read_text(encoding="utf-8")))
    pj = ROOT / "pyproject.toml"
    checks.append(("pyproject declara MIT", pj.exists()
                   and 'text = "MIT"' in pj.read_text(encoding="utf-8")))
    return checks


def main():
    third, pending_active, pending_hist, abspath = scan()
    checks = structural_checks()
    ok = (not third and not pending_active and not abspath
          and all(v for _, v in checks))
    L = ["# PUBLIC_REPO_CLEAN_CHECK\n",
         "Verificación anti-contaminación del repositorio público "
         "(`public_repo_ready/calendario-chile/`).\n",
         "## Chequeos estructurales\n", "| Chequeo | Resultado |\n|---|:--:|"]
    for name, v in checks:
        L.append(f"| {name} | {'✅' if v else '❌'} |")
    L += ["\n## Búsqueda de patrones\n", "| Patrón | Coincidencias | Bloqueante |\n|---|--:|:--:|",
          f"| Terceros / fuentes externas | {len(third)} | sí |",
          f"| Licencia pendiente en archivo autoritativo | {len(pending_active)} | sí |",
          f"| Mención histórica de licencia (CHANGELOG/reports/ADR) | {len(pending_hist)} | no |",
          f"| Rutas absolutas locales (`/Users/...`) | {len(abspath)} | sí |"]
    if third:
        L.append("\n**Terceros:** " + ", ".join(f"`{p}`" for p in third))
    if pending_active:
        L.append("\n**Pendiente (autoritativo):** " + ", ".join(f"`{p}`" for p in pending_active))
    if abspath:
        L.append("\n**Rutas absolutas:** " + ", ".join(f"`{p}`" for p in abspath))
    if pending_hist:
        L.append("\n_Menciones históricas no bloqueantes (documentan que el estado "
                 "pendiente fue superado por MIT):_ "
                 + ", ".join(f"`{p}`" for p in pending_hist))
    L += ["\n> Nota: `public_clean_check.py`, `validate_public.py` y "
          "`test_public_data.py` nombran patrones por diseño y se excluyen; los `.ics` "
          "se omiten (binarios de calendario). La licencia se valida en los archivos "
          "de declaración autoritativa (README, pyproject, LICENSE, datapackage, "
          "metadata, legal_notes).\n",
          f"## Conclusión\n\n{'✅ Repo público limpio para revisión humana.' if ok else '❌ Hay observaciones bloqueantes que corregir.'}\n"]
    (ROOT / "reports" / "PUBLIC_REPO_CLEAN_CHECK.md").write_text("\n".join(L), encoding="utf-8")
    print(f"[public_clean_check] terceros={len(third)} pendiente_activo={len(pending_active)} "
          f"hist={len(pending_hist)} abs_path={len(abspath)} | "
          f"estructural={'OK' if all(v for _,v in checks) else 'FALLA'}")
    print("  " + ("✅ limpio" if ok else "❌ revisar reports/PUBLIC_REPO_CLEAN_CHECK.md"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
