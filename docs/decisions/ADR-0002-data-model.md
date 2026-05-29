# ADR-0002 — Modelo de datos

- **Estado:** aceptado
- **Contexto:** se necesita un modelo interoperable que además capture particularidades chilenas.

## Decisión

Adoptar un registro por **(fecha, evento)** con:

- Vocabulario alineado a estándares: **ISO 3166-2** para subdivisiones, **RFC 5545** para fechas/iCalendar, `weekday` en inglés, **JSON Schema** y **Frictionless** como contrato.
- Extensiones propias de Chile: `is_irrenunciable` + `irrenunciability_category` (1–5), `is_bank_holiday`, y `legal_basis` con trazabilidad a la norma.
- **Texto original preservado** en campos `*_raw`.
- Separación entre **vista pública** (hechos) y **bloque interno `source`** (procedencia, `confidence`, `notes`).

## Alternativas consideradas

- Modelo "sólo feriados" (descartado: pierde la capa conmemorativa y la legal).
- Calcular feriados por reglas en vez de materializar fechas (descartado: el objetivo es un dataset histórico verificable, no sólo lógica).

## Consecuencias

- Interoperable y a la vez específico para Chile.
- El `id` `cl-{fecha}-{slug}` es estable y legible.
