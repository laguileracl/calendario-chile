# ADR-0003 — Aspectos legales y licenciamiento

- **Estado:** aceptado (2026-05-29)
- **Contexto:** el dataset combina hechos (fechas, normas) con metadatos derivados; debe poder publicarse de forma responsable.

## Decisión

1. Tratar fechas e identificadores normativos como **hechos**; **no** reproducir prosa extensa protegida de terceros.
2. Describir el origen como **fuentes internas del proyecto procesadas**, sin atribuir el proyecto, el dataset ni la metodología a terceros.
3. **Licencia definitiva: MIT** para toda la superficie pública (código, documentación, schemas, datasets públicos, API estática y derivados publicables). Titular: Luis Aguilera, 2026. Ver `LICENSE` y `reports/LICENSE_DECISION_REPORT.md`.
4. La **vista pública** elimina la procedencia interna; las referencias de origen quedan sólo en `data/internal/` para auditoría.

## Consecuencias

- Publicación responsable y trazable.
- La licencia deja de ser un bloqueo de publicación. El borrador previo quedó obsoleto en `data/internal/audit/OBSOLETE_LICENSE_DRAFT.md`.
