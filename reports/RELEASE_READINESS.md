# RELEASE_READINESS — calendario-chile

Evaluación del estado del proyecto para revisión humana y, eventualmente, publicación. **Nada está publicado.**

## Resumen

| Pregunta | Respuesta |
|---|---|
| ¿Lista para **revisión humana**? | **Sí.** Estructura, pipeline, datos, validación y documentación completos. |
| ¿Lista para **repo público**? | **Casi.** Licencia resuelta (MIT). Bloqueo restante: definir estrategia de peso/distribución y revisar 2 plebiscitos sin ley. |
| ¿Datos validados? | **Sí** — 10/10 tests; cobertura 1981–2100; 0 duplicados exactos. |
| ¿Documentación sin terceros? | **Sí** — 0 coincidencias en zonas públicas (`clean_public_release`). |

## Qué bloquea la publicación

1. ~~Licencia definitiva~~ — **RESUELTO: MIT** (ver `LICENSE` y `reports/LICENSE_DECISION_REPORT.md`).
2. ~~Revisión de los 2 plebiscitos públicos irrenunciables~~ — **RESUELTO** con fuente oficial (ver `reports/PLEBISCITES_LEGAL_BASIS_PATCH.md`).
3. **Peso del repositorio / estrategia de distribución** sin decidir (ver abajo).
4. **Revisión de calidad fina (opcional):** 665 eventos `low-confidence` por lotes; 29 feriados escolares restringidos sin ley (`requires_manual_review`).
5. **Decisión sobre fuentes brutas** (`data/internal/raw/`): publicar o mantener privadas.

## Qué es publicable

- `src/`, `scripts/`, `tests/`, `Makefile`, `pyproject.toml` (pipeline).
- `docs/`, `schema/`, `reports/` (documentación y contrato).
- Vista pública de datos (`to_public`): **sin** procedencia interna ni fuentes externas.
- `data/public/SAMPLE.json` y los índices livianos de `data/api/v1/`.

## Qué debe quedar privado (por ahora)

- `data/internal/raw/` — fuentes brutas (24 MB).
- `data/internal/intermediate/` — dataset completo con trazabilidad (237 MB).
- `data/internal/audit/REVIEW_THIRD_PARTY_REFERENCES.md` — referencias internas a revisar.

## Pesos (orientativo)

| Zona | Tamaño | Nota |
|---|--:|---|
| `data/internal/intermediate` | ~237 MB | interno; no versionar. |
| `data/api/v1` | ~83 MB | regenerable; distribuir vía Pages/release, no commit directo. |
| `data/public/json+csv+ics` | ~70 MB | regenerable; idem. |
| `data/internal/raw` | ~24 MB | interno; decisión pendiente. |

Por defecto, `.gitignore` excluye el bulk regenerable y versiona sólo pipeline, docs, esquema, reportes, una **muestra** (`SAMPLE.json`) e índices API livianos.

## Faltante para Fase 1 (MVP)

- [x] Resolver licencia → **MIT**.
- [ ] Revisar 665 `low-confidence` y 31 feriados sin ley.
- [ ] Definir distribución (Pages / GitHub Releases / LFS).
- [x] `LICENSE` (MIT) creado + `pyproject.toml` y `datapackage.json` actualizados.

## Faltante para versión completa

- [ ] Promover capa conmemorativa al release público (Fase 2).
- [ ] Curar `category` temática de conmemorativos.
- [ ] Visor web y paquetes (PyPI/npm) (Fase 3).
- [ ] Automatización CI de regeneración (Fase 4).
