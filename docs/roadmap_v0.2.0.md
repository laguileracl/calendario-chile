# Roadmap v0.2.0

Plan de trabajo para la próxima versión menor de `calendario-chile`, partiendo de la versión estable `v0.1.0`. **Este documento no modifica datos.**

## Objetivo de la versión

Mejorar la **completitud y confianza** del dataset y abrir la **capa conmemorativa** al release público, sin regresiones en los feriados públicos ya estables.

## Líneas de trabajo

### A — Calidad y confianza (núcleo de v0.2.0)
- Revisar por lotes los **665 registros `low-confidence`**, distinguiendo los que afectan datos públicos actuales (MVP feriados) de los que solo afectan capas futuras (conmemorativos).
- Revisar los **29 eventos escolares de ámbito restringido** marcados `requires_manual_review`.
- Mejorar el **matching de anclas** mediante nombre normalizado (causa raíz de la mayoría de `low-confidence`: eventos `.ics` sin ancla).

### B — Cobertura y enriquecimiento
- Enriquecer **categorías temáticas** de los conmemorativos (hoy mayormente `other`).
- Preparar la **publicación gradual de la capa conmemorativa** en el release público.
- Mejorar los **reportes de calidad por tipo de evento**.
- Agregar **fixtures** adicionales para años históricos relevantes (p. ej. 1988/1989, 2019, 2023).

### C — Distribución y ecosistema (evaluación)
- Evaluar publicar la **API completa (1981–2100) en GitHub Pages**.
- Evaluar un **visor web** de consulta por año/región/tipo.
- Evaluar paquetes **PyPI** y **npm**.
- Evaluar **DOI en Zenodo** para citabilidad.

## Orden de trabajo sugerido

1. **Lote A** (confianza) — mayor retorno y prerrequisito de B.
2. **Lote B** (cobertura) — apoyado en el matching mejorado de A.
3. **Lote C** (distribución) — evaluaciones; se materializan según decisión.

## Ramas de trabajo

- `dev/v0.2.0-low-confidence` — línea A.
- `dev/v0.2.0-commemoratives` — línea B.
- `dev/v0.2.0-api-pages` — línea C.

## Criterios de salida (Definition of Done para v0.2.0)

- `make validate`, `make test`, `make clean-check` en verde.
- Sin regresiones en feriados públicos (cobertura 1981–2100, conteos estables salvo correcciones justificadas y testeadas).
- `low-confidence` reducido y documentado; pendientes claramente marcados.
- Licencia MIT intacta; sin `data/internal` ni fuentes raw en lo público; tags `v0.1.0` y `v0.1.0-rc1.2` sin mover.

## No-objetivos de v0.2.0

- No alterar feriados públicos sin un test que lo justifique.
- No publicar fuentes internas.
- No comprometer datasets pesados completos al repo (se mantienen como artefactos de release / Pages).
