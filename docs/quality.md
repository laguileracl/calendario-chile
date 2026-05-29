# Quality

La calidad se controla con una **suite de validación** (apta para CI) y un **reporte** regenerable.

## Cómo ejecutar

```bash
make validate   # tests de integridad; falla si hay errores
make report     # genera reports/QUALITY_REPORT.md
make test       # tests unitarios (pytest)
```

## Qué se valida

- Todas las fechas son ISO válidas; `start_date ≤ end_date`; `year` coincide con la fecha.
- `type` y `category` dentro de sus enums.
- `subdivisions` con códigos ISO 3166-2 válidos para Chile.
- Eventos multi-día con `duration_days > 1`; consistencia duración/fechas.
- IDs únicos; sin duplicados exactos.
- Cobertura **1981–2100 completa**.

## Indicadores reportados

Conteos por calendario de origen, por tipo, por categoría, por confianza y por década; además: duplicados exactos y semánticos, eventos sin fecha/nombre/tipo, locales sin alcance territorial, feriados sin fundamento legal, multi-día, recurrentes vs singulares, irrenunciables y eventos con subdivisión ISO.

## Niveles de confianza

| `confidence` | Significado |
|---|---|
| `high` | Definición resuelta por ancla exacta o prefijo único. |
| `medium` | Resuelto por nombre o con irrenunciabilidad inferida de un rango. |
| `low` | Sin definición resuelta (el evento se conserva igualmente). |

El detalle vigente está en [`reports/QUALITY_REPORT.md`](../reports/QUALITY_REPORT.md).
