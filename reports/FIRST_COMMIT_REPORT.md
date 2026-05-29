# FIRST_COMMIT_REPORT

Reporte del **primer commit local** del repositorio público `calendario-chile`. **Sin push, sin remoto, sin publicación.**

## Datos del commit

- **Fecha:** 2026-05-29
- **Commit inicial:** `35bab5a0529e9df679a08f14df0e0a081a25f26f`
- **Tag:** `v0.1.0-rc1.2` (anotado, local)
- **Rama:** `main`
- **Remoto:** ninguno (no se ejecutó `git remote add` ni `git push`)

## Contenido versionado

- **Archivos versionados (commit inicial):** 83
- **Tamaño del repo:**  12M
- Incluye: pipeline (`src/`, `scripts/`), `tests/`, `schema/`, `docs/`, `reports/`, `.github/workflows/`, raíz (README, LICENSE, CHANGELOG, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, pyproject, Makefile, .gitignore, .gitattributes, .editorconfig), muestra, `.ics` y API parcial (índices + años 2020/2022/2025/2026).

## Validaciones (antes del commit)

| Check | Resultado |
|---|---|
| `make validate` (validate_public) | OK |
| Tests sobre datos incluidos | 7/7 (vía runner; `pytest` no instalado localmente, sí en CI) |
| `make clean-check` | limpio (terceros 0, pendiente-activo 0, rutas absolutas 0) |

## Confirmaciones

- ✅ **Sin `data/internal/`** en el repo.
- ✅ **Sin fuentes raw** ni archivos `.html` de fuente.
- ✅ **Sin `LICENSE_DRAFT.md` ni `OBSOLETE_LICENSE_DRAFT.md`.**
- ✅ `.ics` sólo en `data/public/ics/` (esperado).
- ✅ **LICENSE = MIT** presente y declarada.
- ✅ Datasets completos pesados y años no seleccionados **excluidos** por `.gitignore`.
- ✅ **No se hizo push** ni se creó repositorio remoto.

## Repositorio independiente

El commit se realizó en un repositorio Git **dedicado** creado en la carpeta pública (toplevel propio), separado del repositorio contenedor del entorno de trabajo.

## Próximos pasos para publicar

Ver `NEXT_STEPS_GITHUB.md`:
1. `git remote add origin …` + `git push -u origin main` + push del tag.
2. Crear GitHub Release `v0.1.0` con los ZIPs de `release_artifacts/v0.1.0/` y verificar `SHA256SUMS.txt`.
3. Activar GitHub Pages para la API estática y los `.ics`.
4. Validar URLs públicas.
