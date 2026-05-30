# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/) y versionado semántico.

## [0.1.0] - 2026-05-29

### Added
- First stable public release of `calendario-chile`.
- MIT-licensed open dataset for Chilean public holidays, bank holidays, local events and legal calendar data.
- Static API metadata and selected year endpoints.
- iCalendar files.
- Downloadable release artifacts in JSON, CSV, SQLite, Parquet, ICS and full static API ZIP formats.
- JSON Schema and Frictionless Data Package metadata.

### Validation
- Public validation passed.
- Public tests passed.
- Public clean-check passed.
- GitHub Actions green.
- Release artifacts verified with SHA-256.

### Notes
- This release promotes `v0.1.0-rc1.2` to `v0.1.0`.
- The 665 low-confidence records and 29 restricted school-related events remain documented limitations for future review.

## [0.1.0-rc1.2] - 2026-05-29

### Fixed
- Added official legal basis for the 2020 and 2022 national plebiscite holidays.
- Fundamento: Ley 18.700 (feriado del día de plebiscito, art. 169/180) y Ley 19.973 (irrenunciabilidad de segunda categoría), con fichas oficiales BCN/LeyChile.
- Ambos eventos: `is_irrenunciable = true`, `irrenunciability_category = 2`, `confidence = high`.
- Mecanismo reproducible vía `src/calendario_chile/overrides.py` (curación por id exacto); sólo afecta a esos 2 eventos.

### Validation
- `make validate`: 10/10. Tests: 19/19. `make clean-check`: 0 coincidencias.
- Total de eventos sin cambio (33.746); fechas y nombres sin cambio.
- Feriados/bancarios sin fundamento legal: 31 → **29** (los 29 restantes son la conmemoración escolar restringida, `requires_manual_review`).
- Eventos irrenunciables: 518 → **520**.

### Added
- `reports/PLEBISCITES_LEGAL_BASIS_PATCH.md`.

## [0.1.0-rc1.1] - 2026-05-29

### Changed
- **Licencia definitiva: MIT** (titular: Luis Aguilera, 2026) para toda la superficie pública. Se eliminó el estado de "licencia pendiente".
- `LICENSE` (MIT) creado en la raíz; `LICENSE_DRAFT.md` movido a `data/internal/audit/OBSOLETE_LICENSE_DRAFT.md`.
- `pyproject.toml`, `schema/datapackage.json`, `data/api/v1/metadata.json` y reportes actualizados a MIT.
- ADR-0003 marcado como **aceptado** (MIT).
- Release candidato `v0.1.0-rc1` regenerado con la licencia aplicada.

### Added
- `reports/LICENSE_DECISION_REPORT.md`.

## [0.1.0-rc1] - 2026-05-29

Primer **release candidato interno** congelado para revisión humana. No publicado, sin commits, sin subir a GitHub.

### Added
- `release_candidates/v0.1.0-rc1/` — vista limpia y revisable (código, docs, schema, reports, datos públicos, API recientes, muestra) con `MANIFEST.md`.
- `reports/PUBLICATION_MATRIX.md` — clasificación archivo a archivo (repo / release / privado / regenerable / riesgo).
- `docs/distribution_strategy.md` — evaluación A–E y recomendación Fase 1 (repo liviano + Pages + Releases).
- `reports/LEGAL_LICENSE_REVIEW_CHECKLIST.md` — revisión de licencias y sensibilidad de contenido.
- `reports/MISSING_LEGAL_BASIS_REVIEW.md` — análisis de los 31 feriados del MVP sin fundamento legal.
- `reports/LOW_CONFIDENCE_SUMMARY.md` — agrupación de los 665 registros `low-confidence` (sin corregir aún).
- `reports/PUBLIC_SURFACE_CLEAN_CHECK.md` — verificación anti-referencias externas de la superficie pública.
- `data/api/v1/metadata.json` — metadatos de la API.

### Changed
- API por año (`data/api/v1/years/`) serializada en JSON compacto.

### Validation
- 10/10 validaciones del dataset; 19/19 tests; cobertura 1981–2100 completa; 0 duplicados exactos.
- `clean-check`: 0 coincidencias de terceros en la superficie pública.

### Known Issues
- 31 feriados del MVP sin fundamento legal mapeado (2 plebiscitos públicos + 29 conmemoración escolar restringida).
- 665 registros `low-confidence` (634 conmemorativos fuera del MVP) pendientes de revisión por lotes.
- Estrategia de distribución/peso del repo por confirmar.

## [Unreleased]

### Added
- Estructura profesional del proyecto (`src/`, `scripts/`, `docs/`, `schema/`, `tests/`, `reports/`).
- Paquete `calendario_chile` con módulos: `config`, `constants`, `normalize`, `territorial`, `legal`, `ics`, `models`, `validate`, `export`, `api`.
- Pipeline reproducible (`make all`) y suite de validación.
- Dataset completo interno (1981–2100), release público MVP de feriados, API estática por año e iCalendar.
- Esquemas JSON Schema y Frictionless datapackage.
- Reportes de calidad, inventario de fuentes, mapeo legal, readiness, checklist de publicación y limpieza de atribución.

### Pending
- Promoción de la capa conmemorativa al release público (Fase 2).

## [0.1.0-internal] — pre-release

- Primera versión interna del dataset y del pipeline. No publicada.
