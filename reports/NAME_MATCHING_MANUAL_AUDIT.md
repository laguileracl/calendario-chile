# NAME_MATCHING_MANUAL_AUDIT

Muestra curada para **revisión humana** de los candidatos de matching por nombre normalizado (issue #4), para estimar la **precisión real** antes de diseñar cualquier aplicación automática. **No se modificó ningún dato.**

- **Fecha:** 2026-05-30
- **Fuente:** `low_confidence_name_matching_candidates.csv` (CSV del experimento)
- **Parámetros:** sample_size=30, seed=20260530

## Metodología de muestreo

Muestreo determinista (seed fija) con diversidad por nombre y por año:
- ~20 `auto_safe_candidate` de tipo `commemorative`;
- ~5 `auto_safe_candidate` de tipo `restricted` (marcados **solo issue #3, no auto-aplicar**);
- ~5 `review_candidate` de mayor score;
- **todos** los casos con score en [0.95, 0.97], si existieran.

### Observación estructural (importante)

- Los **83 auto_safe commemorative** se reducen a **2 nombres distintos** (sobre todo *semanas/meses/años nacionales* recurrentes cuyas ocurrencias en algunos años no traían ancla).
- Los **29 auto_safe restricted** son **1 nombre** repetido por año (conmemoración escolar; pertenece a issue #3).
- **No hay casos con score en [0.95, 0.97]** (0): los auto_safe son coincidencias **exactas** (score 1.0); los review caen por debajo de 0.90. El matching es **bimodal**, sin zona gris cercana al umbral.
- Conclusión: auditar **pocas decisiones distintas de nombre** cubre casi todo el universo auto_safe.

### Notas de redistribución

- No existen candidatos con score en [0.95, 0.97]: los auto_safe son coincidencias exactas (score 1.0) y los review caen por debajo de 0.90. No hay casos limítrofes que auditar.

## Resumen de la muestra

- **Total de casos:** 30
- Por clasificación: {'auto_safe_candidate': 25, 'review_candidate': 5}
- Por tipo: {'commemorative': 25, 'restricted': 5}
- Por decisión propuesta (preliminar): {'accept_candidate': 20, 'defer_to_issue_3': 5, 'review_manually': 5}

## Casos seleccionados

| audit_id | clasif. | low (nombre / fecha) | candidato | tipo | score | decisión propuesta |
|---|---|---|---|---|--:|---|
| AU-001 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2019-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-002 | auto_safe_c | Día Nacional del Niño (de facto) / 2020-08-16 | Día Nacional del Niño (de fact | commemorative→commemorative | 1.0 | accept_candidate |
| AU-003 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2026-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-004 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2033-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-005 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2040-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-006 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2047-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-007 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2054-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-008 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2061-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-009 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2068-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-010 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2075-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-011 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2082-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-012 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2089-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-013 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2096-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-014 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2021-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-015 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2028-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-016 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2035-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-017 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2042-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-018 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2049-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-019 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2056-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-020 | auto_safe_c | Mes Nacional de la Ciberseguridad  / 2063-10-01 | Mes Nacional de la Ciberseguri | commemorative→commemorative | 1.0 | accept_candidate |
| AU-021 | auto_safe_c | Nacimiento del Prócer de la Indepe / 1981-08-20 | Nacimiento del Prócer de la In | restricted→local | 1.0 | defer_to_issue_3 |
| AU-022 | auto_safe_c | Nacimiento del Prócer de la Indepe / 1985-08-20 | Nacimiento del Prócer de la In | restricted→local | 1.0 | defer_to_issue_3 |
| AU-023 | auto_safe_c | Nacimiento del Prócer de la Indepe / 1990-08-20 | Nacimiento del Prócer de la In | restricted→local | 1.0 | defer_to_issue_3 |
| AU-024 | auto_safe_c | Nacimiento del Prócer de la Indepe / 1994-08-20 | Nacimiento del Prócer de la In | restricted→local | 1.0 | defer_to_issue_3 |
| AU-025 | auto_safe_c | Nacimiento del Prócer de la Indepe / 1999-08-20 | Nacimiento del Prócer de la In | restricted→local | 1.0 | defer_to_issue_3 |
| AU-026 | review_cand | Día Mundial de los Océanos (incons / 2019-06-08 | Día Mundial de los Refugiados  | commemorative→commemorative | 0.8989 | review_manually |
| AU-027 | review_cand | Día Mundial de los Océanos (incons / 2034-06-08 | Día Mundial de los Refugiados  | commemorative→commemorative | 0.8989 | review_manually |
| AU-028 | review_cand | Día Mundial de los Océanos (incons / 2044-06-08 | Día Mundial de los Refugiados  | commemorative→commemorative | 0.8989 | review_manually |
| AU-029 | review_cand | Día Mundial de los Océanos (incons / 2063-06-08 | Día Mundial de los Refugiados  | commemorative→commemorative | 0.8989 | review_manually |
| AU-030 | review_cand | Día Mundial de los Océanos (incons / 2073-06-08 | Día Mundial de los Refugiados  | commemorative→commemorative | 0.8989 | review_manually |

## Cómo revisar

1. Abrir `reports/name_matching_manual_audit_sample.csv`.
2. Para cada fila, comparar `low_name` vs `candidate_name` y el contexto (tipo, calendario, fecha).
3. Completar `reviewer_decision` (accept / reject / review / defer) y `reviewer_notes`. Dejar `proposed_decision` como referencia.

## Criterio recomendado de decisión

- **Aceptar** sólo si el nombre coincide **sustantivamente** (mismo evento).
- **No aceptar** si cambia **tipo, alcance o sentido** del evento.
- **No aceptar** casos `restricted`/escolares sin revisión jurídica separada (→ issue #3).
- Si se acepta, la aplicación futura debe subir como **máximo a `medium`**, salvo fuente legal/definición firme.
- Dejar **trazabilidad** del candidato usado (`candidate_id`).

## Estimación de precisión

Se completará tras la revisión humana (campo `reviewer_decision`). Dado que los auto_safe son coincidencias **exactas de nombre** y mismo tipo (conmemorativo↔conmemorativo), se espera **precisión alta**, pero debe confirmarse manualmente sobre la muestra antes de cualquier aplicación.

> **Advertencia:** este documento es solo una muestra para revisión. **No se modificó ningún dato, ni `confidence`, ni se aplicaron overrides.**
