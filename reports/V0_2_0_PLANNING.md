# V0_2_0_PLANNING

Reporte técnico de planificación de `v0.2.0`. **No modifica datos**; cuantifica el trabajo y propone milestone, issues, ramas y criterios de no regresión.

- **Fecha:** 2026-05-30.
- **Base:** versión estable `v0.1.0`.

## Estado de partida (medido)

| Métrica | Valor |
|---|--:|
| Eventos totales | 33.746 |
| `low-confidence` actuales | **663** |
| ↳ que afectan **datos públicos** (MVP, `type` restricted) | **29** |
| ↳ que afectan **capas futuras** (conmemorativos) | **634** |
| Feriados/bancarios sin fundamento legal | 29 (los mismos escolares restringidos) |

> Nota de reconciliación: en `v0.1.0` se documentaron **665** `low-confidence`; tras el patch de plebiscitos (`rc1.2`) que llevó 2 eventos a `high`, el conteo actual es **663**.

### Desglose de `low-confidence` por calendario de origen

| Calendario | Eventos |
|---|--:|
| días nacionales | 414 |
| días nacionales no oficiales | 130 |
| semanas/meses/años nacionales | 90 |
| feriados ámbito restringido (escolar) | 29 |

### Causa raíz

- **511** de los 663 provienen de eventos `.ics` **sin ancla** → no se resuelve su definición ni su normativa. La mejora de mayor retorno es el **matching por nombre normalizado** (issue A4).
- **152** restantes: ancla presente pero no encontrada en definiciones (revisión por nombre/alias).

## Milestone propuesto

`v0.2.0` — "Confianza, cobertura y capa conmemorativa".

## Issues propuestos (por prioridad)

### Prioridad A — Calidad y confianza
- **A1.** Revisar los 663 `low-confidence` por lotes (empezar por *días nacionales* sin ancla).
- **A2.** Clasificar `low-confidence`: separar los 29 que afectan datos públicos de los 634 de capas futuras; reportar.
- **A3.** Revisar los 29 eventos escolares restringidos `requires_manual_review` (fundamento legal/clasificación; sin inventar normas).
- **A4.** Mejorar matching de anclas por **nombre normalizado** (recupera ~511 sin ancla).

### Prioridad B — Cobertura y enriquecimiento
- **B1.** Enriquecer categorías temáticas de conmemorativos (hoy mayormente `other`).
- **B2.** Preparar publicación gradual de la **capa conmemorativa** en el release público.
- **B3.** Mejorar reportes de calidad **por tipo de evento**.
- **B4.** Agregar **fixtures** adicionales para años históricos relevantes (1988/1989, 2019, 2023).

### Prioridad C — Distribución y ecosistema (evaluación)
- **C1.** Evaluar API completa (1981–2100) en **GitHub Pages**.
- **C2.** Evaluar **visor web**.
- **C3.** Evaluar paquete **PyPI**.
- **C4.** Evaluar paquete **npm**.
- **C5.** Evaluar **DOI en Zenodo**.

## Ramas propuestas

| Rama | Línea | Issues |
|---|---|---|
| `dev/v0.2.0-low-confidence` | A | A1, A2, A3, A4 |
| `dev/v0.2.0-commemoratives` | B | B1, B2, B3, B4 |
| `dev/v0.2.0-api-pages` | C | C1, C2, C3, C4, C5 |

Cada rama se mergea a `main` vía PR con CI verde. Esta planificación vive en `dev/v0.2.0-planning`.

## Orden de trabajo

1. **A4** (matching por nombre) → habilita resolver gran parte de A1/A2.
2. **A1 + A2** (revisión y clasificación de `low-confidence`).
3. **A3** (escolares restringidos).
4. **B1–B4** (cobertura conmemorativa) sobre el matching mejorado.
5. **C** (evaluaciones de distribución), según decisión.

## Checklist de no regresión

- [ ] No romper la licencia **MIT**.
- [ ] No subir `data/internal`.
- [ ] No subir fuentes raw.
- [ ] No mover los tags `v0.1.0` ni `v0.1.0-rc1.2`.
- [ ] No alterar eventos de **feriados públicos** sin un test que lo justifique.
- [ ] Mantener `make validate`, `make test`, `make clean-check` en verde.
- [ ] Mantener cobertura 1981–2100 y total de eventos estable (salvo correcciones justificadas + testeadas).

## Riesgos

| Riesgo | Mitigación |
|---|---|
| El matching por nombre genera falsos positivos | Umbral conservador + revisión manual de los re-emparejados; marcar `confidence: medium`. |
| Promover conmemorativos infla el release y altera conteos públicos | Publicación **gradual** y por tipo; tests de no regresión sobre feriados. |
| "Corregir" sin fuente oficial | Mantener la regla: no inventar normativa; usar `overrides.py` solo con fuente verificada. |
| Cambios rompen consumidores de la API/schema | Versionado de esquema; cambios incompatibles → bump y CHANGELOG. |

## Primer lote recomendado

**Lote A — empezar por A4 (matching por nombre) + A2 (clasificación de `low-confidence`).** Es el de mayor retorno (recupera ~511 eventos sin ancla), no toca feriados públicos estables y es prerrequisito de la línea B. Entregable: reporte de cuántos `low-confidence` suben de confianza y cuáles quedan para revisión manual, sin alterar aún datos publicados.
