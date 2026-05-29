# ADR-0004 — API estática

- **Estado:** aceptado
- **Contexto:** se busca exponer los datos a desarrolladores sin operar infraestructura.

## Decisión

Generar una **API estática** (archivos JSON) servible desde GitHub Pages o cualquier CDN:

- `v1/years/{YYYY}.json` — partición por año (consumo eficiente).
- `v1/index.json` — metadatos y descubrimiento de endpoints.
- `v1/hoy.json`, `v1/proximos.json` — vistas de conveniencia respecto de una fecha de referencia.

Versionado bajo prefijo `v1/` para permitir evolución sin romper consumidores.

## Alternativas consideradas

- API dinámica con servidor (descartada: costo y mantenimiento; innecesaria para datos que cambian poco).

## Consecuencias

- Costo de hosting cero; alta disponibilidad y cacheabilidad.
- `hoy`/`próximos` dependen de la regeneración periódica (CI).
