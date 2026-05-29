# ADR-0001 — Alcance del proyecto

- **Estado:** aceptado
- **Contexto:** se requiere un dataset de referencia del calendario chileno, completo y reutilizable, que supere a las soluciones parciales existentes.

## Decisión

Cubrir **1981–2100** e incluir cinco familias de eventos: feriados públicos, feriados bancarios, eventos locales, feriados de ámbito restringido y eventos conmemorativos (días/semanas/meses/años nacionales).

El **MVP público** se limita a los feriados (`public`, `bank`, `local`, `restricted`); la capa conmemorativa se entrega vía API estática y se promueve al release público en la Fase 2.

## Consecuencias

- Amplio valor histórico y prospectivo.
- Se distingue lo que tiene efectos legales (feriados) de lo conmemorativo.
- Mayor volumen de datos → se gestiona con separación público/interno y formatos livianos.
