# NAME_MATCHING_FAMILY_REVIEW

Revisión **por familia de nombre** (no evento por evento) de los candidatos de matching por nombre normalizado (issue #4), para decidir si los `auto_safe` conmemorativos pueden aplicarse en una fase posterior. **No se modificó ningún dato.**

- **Fecha:** 2026-05-30
- **Insumo:** `low_confidence_name_matching_candidates.csv` (CSV de candidatos del experimento)
- **Candidatos agrupados:** 200 → **5 familias**

## Resumen

- **Total de familias:** 5
- `accept_family` (auto_safe conmemorativas): **2**
- `review_family` (auto_safe a revisar + review_candidate): **2**
- `defer_to_issue_3` (escolares/restricted): **1**
- Decisiones propuestas: {'review_family': 2, 'accept_family': 2, 'defer_to_issue_3': 1}

## Familias auto_safe conmemorativas (candidatas a aceptación)

| family_id | familia (low → candidato) | tipo | nº ev. | años | score | decisión propuesta |
|---|---|---|--:|---|--:|---|
| FAM-002 | Mes Nacional de la Ciberseguridad  → Mes Nacional de la Ciberseguri | commemorative→commemorative | 82 | 2019–2100 | 1.0 | accept_family |
| FAM-005 | Día Nacional del Niño (de facto) → Día Nacional del Niño (de fact | commemorative→commemorative | 1 | 2020–2020 | 1.0 | accept_family |

## Familias auto_safe a revisar

_(ninguna)_

## Familias review_candidate

| family_id | familia (low → candidato) | tipo | nº ev. | años | score | decisión propuesta |
|---|---|---|--:|---|--:|---|
| FAM-001 | Día Mundial de los Océanos (incons → Día Mundial de los Refugiados  | commemorative→commemorative | 83 | 2018–2100 | 0.8989 | review_family |
| FAM-004 | Semana de las Empresas de Menor Ta → Semana de las Empresas de Meno | commemorative→commemorative | 5 | 2020–2021 | 0.8872 | review_family |

## Familias escolares / restricted (diferidas a issue #3)

> **No se aplican ni se resuelven aquí.** Requieren revisión jurídica separada (issue #3).

| family_id | familia (low → candidato) | tipo | nº ev. | años | score | decisión propuesta |
|---|---|---|--:|---|--:|---|
| FAM-003 | Nacimiento del Prócer de la Indepe → Nacimiento del Prócer de la In | restricted→local | 29 | 1981–2013 | 1.0 | defer_to_issue_3 |

## Recomendación por familia

- **`accept_family`** (auto_safe conmemorativas, coincidencia exacta de nombre, mismo tipo): aprobables por el humano; la aplicación futura subiría como máximo a `confidence: medium`, registrando el `candidate_id`.
- **`review_family`**: revisar el nombre/sentido caso por caso.
- **`defer_to_issue_3`**: no tocar aquí (escolares/restricted).
- **`reject_family`**: descartar.

## Criterios de aceptación

1. El nombre normalizado de la familia coincide **sustantivamente** (mismo evento), no solo por palabras genéricas.
2. **No** cambia tipo, alcance ni sentido (conmemorativo↔conmemorativo).
3. La familia es **recurrente y coherente** entre años (la diferencia es solo el ancla faltante en algunas ocurrencias).
4. Escolares/restricted **excluidos** (→ issue #3).
5. La aplicación se hará **en rama aparte, con tests de no regresión**, sin tocar feriados públicos estables.

## Decisión humana

Completar en `reports/name_matching_families.csv` los campos `reviewer_family_decision` (accept_family / review_family / defer_to_issue_3 / reject_family) y `reviewer_notes`. **Una decisión por familia** cubre todas sus ocurrencias.

> **Advertencia:** este documento es preparación para decisión humana. **No se modificó ningún dato, ni `confidence`, ni se aplicaron overrides.**
