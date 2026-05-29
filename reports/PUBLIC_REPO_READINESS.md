# PUBLIC_REPO_READINESS

Evaluación del repositorio público preparado en `public_repo_ready/calendario-chile/`. **Nada publicado.**

## Respuestas rápidas

| Pregunta | Respuesta |
|---|---|
| ¿Lista para **revisión humana**? | **Sí.** |
| ¿Lista para **primer commit**? | **Sí** (ver checklist en `docs/publishing_plan.md`). |
| ¿Lista para **publicación** (push a GitHub)? | **Sí, técnicamente**; queda la decisión humana de publicar y configurar Pages/Release. |

## Métricas

- **Tamaño total:**  11M.
- **Archivos:** 82 (código .py: 24).
- **Datos incluidos:**  10M (muestra + 4 .ics + API parcial).
- **Años de API incluidos:** 2020.json 2022.json 2025.json 2026.json 

## Qué contiene

- Raíz: README, LICENSE (MIT), CHANGELOG, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, pyproject.toml, Makefile, .gitignore, .gitattributes, .editorconfig.
- `src/` (paquete), `scripts/` (validate_public, public_clean_check, build_*), `tests/` (datos incluidos), `.github/workflows/validate.yml`.
- `schema/`, `docs/` (incl. downloads.md, publishing_plan.md), `reports/` (públicos).
- `data/public/SAMPLE.json`, `data/public/ics/*.ics`.
- `data/api/v1/{index,metadata,hoy,proximos}.json` + `years/{2020,2022,2025,2026}.json`.

## Qué excluye

- `data/internal/` (fuentes brutas, intermedios, auditoría) — **no presente**.
- Datasets completos pesados (JSON/CSV/SQLite/Parquet) y API de 120 años — vía Release/Pages.
- `OBSOLETE_LICENSE_DRAFT.md`, `LICENSE_DRAFT.md`, notebooks, caches — **no presentes**.
- `reports/SOURCE_INVENTORY.md` (hashes de fuentes internas) — excluido.

## Validaciones

- `make validate` (validate_public): **OK** (fechas, enums, ISO, multiday, ids, sin bloque source, sin tokens externos).
- Tests sobre datos incluidos: **7/7**.
- `make clean-check`: **limpio** (terceros 0, pendiente-activo 0, rutas absolutas 0; 3 menciones históricas no bloqueantes).

## Riesgos pendientes

- Decisión humana de **publicar** y de **configurar Pages/Release**.
- 29 feriados escolares restringidos sin ley (`requires_manual_review`) y 665 `low-confidence`: documentados como limitaciones; no bloquean el MVP.

## Recomendación final

**Listo para revisión humana y para primer commit.** Publicar tras: (1) confirmar los datasets completos como GitHub Release usando `release_artifacts/v0.1.0/`, y (2) configurar GitHub Pages para la API estática. No publicar automáticamente sin esa decisión.
