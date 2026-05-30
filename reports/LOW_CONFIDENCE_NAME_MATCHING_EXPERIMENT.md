# LOW_CONFIDENCE_NAME_MATCHING_EXPERIMENT

Experimento de recuperación de eventos `low-confidence` por **nombre normalizado** (issue #4). **Solo análisis — no se modificó ningún dato.**

- **Fecha:** 2026-05-30
- **Input (local, no publicado):** `calendar_chile_events.full.json` (dataset canónico/intermedio interno; ruta local fuera del repo público)
- **Parámetros:** min_score=0.88, auto_score=0.95, max_candidates=5
- **Referencias (high/medium):** 33,083 eventos / 281 nombres normalizados distintos

## Universo analizado

- **low-confidence analizados:** 663
- de ellos **sin ancla en `.ics`:** 511

## Resultados por clasificación (mejor candidato por evento)

| Clasificación | Eventos | % |
|---|--:|--:|
| auto_safe_candidate | 112 | 16.9% |
| review_candidate | 88 | 13.3% |
| conflict | 0 | 0.0% |
| no_candidate | 463 | 69.8% |

## Resultados por tipo de evento

| type | auto_safe | review | conflict | no_candidate |
|---|--:|--:|--:|--:|
| commemorative | 83 | 88 | 0 | 463 |
| restricted | 29 | 0 | 0 | 0 |
| public | 0 | 0 | 0 | 0 |
| bank | 0 | 0 | 0 | 0 |
| local | 0 | 0 | 0 | 0 |

## Top auto_safe_candidate (top 30 de 112)

| score | low → candidato | tipo | calendario |
|--:|---|---|---|
| 1.0 | Día Nacional del Niño (de facto) → Día Nacional del Niño (de facto) | commemorative→commemorative | días nacionales no oficiales |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |
| 1.0 | Nacimiento del Prócer de la Independenci → Nacimiento del Prócer de la Independenci | restricted→local | feriados ámbito restringido |

## Top review_candidate (top 30 de 88)

| score | low → candidato | tipo | calendario |
|--:|---|---|---|
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |
| 0.8989 | Día Mundial de los Océanos (inconstituci → Día Mundial de los Refugiados (inconstit | commemorative→commemorative | días nacionales |

## Conflicts (todos: 0)

| score | low → candidato | conflicto |
|--:|---|---|

## Estimación de recuperación

- **Recuperación segura estimada (auto_safe):** 112 eventos (16.9% de los low-confidence) — subirían a `confidence: medium` tras revisión ligera.
  - de ellos **29 afectan datos públicos** (type restringido/feriado) → tratar con cautela vía issue #3 (revisión manual), no auto-aplicar.
  - **83 son capas futuras** (conmemorativos) → candidatos a la línea B de v0.2.0.
- **Candidatos a revisión humana (review):** 88.
- **Sin candidato confiable:** 463.
- **Conflictos (no recuperables automáticamente):** 0.

## Recomendación de siguiente paso

1. Validar manualmente una muestra de `auto_safe_candidate` (p. ej. 30) para confirmar precisión antes de cualquier aplicación.
2. Si la precisión es alta, diseñar una aplicación **conservadora** (en una rama aparte, con tests de no regresión) que solo suba a `confidence: medium` y registre la procedencia; **nunca** tocar feriados públicos estables sin test.
3. Tratar `review_candidate` por lotes con revisión humana; `conflict` y `no_candidate` quedan para análisis caso a caso.

> **Advertencia:** este experimento **no modificó ningún dato**. No se aplicaron overrides, no se cambió el `confidence` de ningún evento, no se alteraron datasets públicos ni canónicos.

## Manual audit sample

A representative audit sample was generated in:
- `reports/name_matching_manual_audit_sample.csv`
- `reports/NAME_MATCHING_MANUAL_AUDIT.md`

No dataset changes were applied.

Hallazgo de la auditoría: los 112 `auto_safe` se concentran en muy pocos nombres distintos (≈2 conmemorativos + 1 restringido), y no existen casos con score en [0.95, 0.97] (el matching es bimodal: exacto 1.0 o por debajo de 0.90). Esto hace que la revisión humana cubra casi todo el universo con pocas decisiones.
