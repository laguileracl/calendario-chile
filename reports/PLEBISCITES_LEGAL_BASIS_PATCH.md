# PLEBISCITES_LEGAL_BASIS_PATCH

Corrección del fundamento legal de los **2 plebiscitos nacionales** del MVP que
figuraban como `public` / irrenunciables **sin `legal_basis`**. Patch `v0.1.0-rc1.2` (2026-05-29).

## Eventos revisados

| id | fecha | nombre |
|---|---|---|
| `cl-2020-10-25-plebiscito-nacional-aprobacion-o-rechazo-de-la-elaboracion-de-una-nueva-constitucion-y-eleccion-del-tipo-de-organo-a-cargo-de-ello-irrenunciable` | 2020-10-25 | Plebiscito nacional (aprobación o rechazo de la elaboración de una nueva constitución…) (irrenunciable) |
| `cl-2022-09-04-plebiscito-nacional-aprobacion-o-rechazo-de-la-constitucion-propuesta-por-la-convencion-constituyente-irrenunciable` | 2022-09-04 | Plebiscito nacional (aprobación o rechazo de la constitución propuesta por la Convención Constituyente) (irrenunciable) |

## Estado anterior

- `legal_basis`: `[]` (vacío).
- `is_irrenunciable`: `false`; `irrenunciability_category`: `null`.
- `confidence`: `low` (evento sin ancla → sin definición → sin mapeo legal).

## Fuente oficial usada

- **Ley 18.700** — Ley Orgánica Constitucional sobre Votaciones Populares y Escrutinios. El día de elecciones y plebiscitos es **feriado legal** (art. 169, hoy art. 180). Ficha oficial BCN/LeyChile: `https://www.bcn.cl/leychile/navegar?idNorma=30082`.
- **Ley 19.973** (2004) — convierte los feriados por elecciones o plebiscitos en **irrenunciables de segunda categoría**. Ficha oficial BCN/LeyChile: `https://www.bcn.cl/leychile/navegar?idNorma=230132`.

Verificación de apoyo: Dirección del Trabajo (dt.gob.cl) confirma que el 04-09-2022 fue feriado **obligatorio e irrenunciable de segunda categoría**, válido en todo el territorio nacional, en virtud de la LOC 18.700.

> Estas son las **mismas normas generales** que el pipeline ya aplica —desde las mismas fichas oficiales— a plebiscitos nacionales análogos (p. ej. el plebiscito nacional del 17-12-2023) y a los plebiscitos comunales irrenunciables (2009, 2011, 2019). **No se inventó normativa**; se aplicó el marco general vigente, ya verificado y catalogado.

## Fundamento legal agregado

Para **ambos** eventos, distinguiendo feriado e irrenunciabilidad:

| Norma | Rol | URL oficial |
|---|---|---|
| Ley 18.700 | Feriado legal del día de plebiscito (art. 169, hoy art. 180) | https://www.bcn.cl/leychile/navegar?idNorma=30082&idVersion=1988-05-06 |
| Ley 19.973 | Irrenunciabilidad de segunda categoría | https://www.bcn.cl/leychile/navegar?idNorma=230132&idVersion=2004-09-10 |

- `is_irrenunciable`: `true`; `irrenunciability_category`: `2` ("segunda categoría").
- `confidence`: `high`.
- `source.extraction_method`: añade `legal_mapping` + `manual_curation`.
- `source.notes`: nota de curación verificada.

## Mecanismo (reproducible)

La corrección se aplica vía `src/calendario_chile/overrides.py` (curación por `id` exacto), no editando archivos generados a mano. Así sobrevive a `make all`. Sólo afecta a los 2 ids listados.

## Archivos modificados

- **Código:** `src/calendario_chile/overrides.py` (nuevo), `src/calendario_chile/models.py` (aplica override).
- **Datos regenerados:** `data/internal/intermediate/*`, `data/public/{json,csv,ics,sqlite,parquet}`, `data/api/v1/{index,metadata}.json`, `data/api/v1/years/2020.json`, `data/api/v1/years/2022.json`.
- **Reportes:** este archivo, `MISSING_LEGAL_BASIS_REVIEW.md`, `QUALITY_REPORT.md`, `LEGAL_MAPPING_REPORT.md`, `RELEASE_READINESS.md`, `CHANGELOG.md`.
- **RC:** `release_candidates/v0.1.0-rc1/` regenerado (incluye años 2020 y 2022 en su API).

## Validaciones ejecutadas

- `make validate`: 10/10.
- tests: 19/19.
- `make clean-check`: 0 coincidencias en superficie pública.

## Impacto en métricas

| Métrica | Antes | Después |
|---|--:|--:|
| Total de eventos | 33.746 | 33.746 (sin cambio) |
| Feriados/bancarios sin fundamento legal | 31 | **29** |
| Eventos irrenunciables | 518 | **520** |
| Eventos con ≥1 fundamento legal | 31.410 | **31.412** |
| Fechas / nombres modificados | — | **ninguno** |

## Asuntos pendientes

- Quedan **29** feriados sin ley = conmemoración escolar de ámbito restringido (`type=restricted`), marcados `requires_manual_review`; **no** se modificaron en este ciclo.
- No se revisaron los 665 `low-confidence` (fuera de alcance de este patch).
