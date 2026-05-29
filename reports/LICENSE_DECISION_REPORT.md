# LICENSE_DECISION_REPORT

Registro del cambio de estado de licencia del proyecto `calendario-chile`.

## Decisión

- **Licencia:** **MIT**.
- **Titular del copyright:** Luis Aguilera.
- **Año:** 2026.
- **Fecha de la decisión:** 2026-05-29.

## Alcance

La licencia **MIT** aplica a **toda la superficie pública** del proyecto, salvo que un archivo indique expresamente otra cosa:

- Código (`src/`, `scripts/`, `tests/`).
- Documentación (`docs/`, `README.md`).
- Schemas y contrato de datos (`schema/`).
- Datasets públicos (`data/public/`: JSON, CSV, ICS, SQLite, Parquet).
- API estática (`data/api/`).
- Reportes públicos (`reports/`).

**No** se aplican licencias adicionales (se descartaron las opciones CC BY / CC0 / ODC-BY que figuraban en el borrador). Una única licencia MIT cubre código y datos.

## Archivos creados

- `LICENSE` — texto MIT con `Copyright (c) 2026 Luis Aguilera`.
- `reports/LICENSE_DECISION_REPORT.md` — este documento.

## Archivos actualizados (estado "pendiente/DRAFT" → MIT)

| Archivo | Cambio |
|---|---|
| `pyproject.toml` | `license = "MIT"` (antes `LicenseRef-PENDING`). |
| `README.md` | Estado a "Licencia: MIT"; nueva sección **## Licencia**; aviso sin "aprobarse antes de publicar". |
| `docs/legal_notes.md` | Sección licencia reescrita a MIT. |
| `docs/index.md` | "licencia pendiente" → "Licencia: MIT". |
| `docs/roadmap.md` | Ítem Fase 1 de licencia marcado como definido (MIT). |
| `docs/decisions/ADR-0003-legal-and-licensing.md` | Estado **aceptado**; decisión = MIT. |
| `schema/datapackage.json` | `licenses: [{MIT}]` (regenerado). |
| `data/api/v1/metadata.json` | `license: "MIT"`, `license_url` (regenerado). |
| `data/api/v1/index.json` | `license: "MIT"` (regenerado). |
| `reports/RELEASE_READINESS.md` | Licencia deja de ser bloqueo; ítems marcados. |
| `reports/PUBLICATION_CHECKLIST.md` | Sección 1 = ✅ MIT. |
| `reports/LEGAL_LICENSE_REVIEW_CHECKLIST.md` | Licencia decidida (MIT); riesgo "sin decidir" = resuelto. |
| `reports/PUBLICATION_MATRIX.md` | Riesgo de datos → "Bajo (MIT)"; recomendaciones a MIT. |
| `reports/PUBLIC_SURFACE_CLEAN_CHECK.md` | Referencia raíz `LICENSE_DRAFT.md` → `LICENSE`. |
| `CHANGELOG.md` | Entrada `0.1.0-rc1.1`; quitado el bloqueo de licencia. |
| Generadores: `src/calendario_chile/models.py`, `src/calendario_chile/api.py` | Emiten MIT en datapackage/metadata/index. |

## Archivos donde se eliminó "licencia pendiente"

`README.md`, `docs/index.md`, `docs/legal_notes.md`, `docs/roadmap.md`, `docs/decisions/ADR-0003-legal-and-licensing.md`, `reports/RELEASE_READINESS.md`, `reports/PUBLICATION_CHECKLIST.md`, `reports/LEGAL_LICENSE_REVIEW_CHECKLIST.md`, `reports/PUBLICATION_MATRIX.md`, `CHANGELOG.md`, `pyproject.toml`, `schema/datapackage.json`, `data/api/v1/metadata.json`, y sus copias en `release_candidates/v0.1.0-rc1/`.

## Borrador obsoleto

`LICENSE_DRAFT.md` fue **eliminado de la raíz** y conservado, sólo por trazabilidad interna, en `data/internal/audit/OBSOLETE_LICENSE_DRAFT.md` con encabezado de obsolescencia (reemplazado por MIT).

## Material interno excluido de la distribución pública

`data/internal/raw/`, `data/internal/intermediate/`, `data/internal/audit/` — no forman parte de la superficie pública ni de la licencia de distribución (salvo decisión expresa posterior).

## Verificaciones

- `make validate`: 10/10.
- `make test`: 19/19.
- `make clean-check`: 0 coincidencias de terceros en superficie pública.
- `grep` de "licencia pendiente / LICENSE_DRAFT / pending license": sin coincidencias en superficie pública (sólo material interno obsoleto, marcado).

## Advertencia

**No se publicó nada, no se hizo commit y no se subió a GitHub.** Sólo se actualizaron archivos locales. No se alteró titularidad ni datos sustantivos; no se inventó fundamento legal.

## Próximos pasos recomendados

1. Revisar los **2 plebiscitos** públicos irrenunciables sin fundamento legal enlazado (`MISSING_LEGAL_BASIS_REVIEW.md`).
2. Definir la **estrategia de distribución/peso** (repo liviano + Pages + Releases).
3. (Opcional) Revisar los **665 low-confidence** por lotes.
4. Cuando se decida publicar: crear repo, aplicar `.gitignore`, y publicar datos pesados vía Releases/Pages.
