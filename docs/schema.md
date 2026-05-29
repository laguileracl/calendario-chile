# Schema

El contrato de datos se publica como **JSON Schema (draft-07)** y como **Frictionless Data Package**.

## Archivos

| Archivo | Uso |
|---|---|
| `schema/calendar_chile_event.schema.json` | Esquema del evento (todos los tipos). |
| `schema/calendar_chile_holiday.schema.json` | Variante restringida a feriados (`public`/`bank`/`local`/`restricted`). |
| `schema/datapackage.json` | Descriptor Frictinless con recursos y campos. |

## Validación

```bash
# con check-jsonschema (ejemplo)
pip install check-jsonschema
check-jsonschema --schemafile schema/calendar_chile_event.schema.json \
  data/api/v1/years/2025.json
```

## Reglas destacadas

- `year` ∈ [1981, 2100].
- `type` y `category` restringidos a sus enums.
- `subdivisions[]` cumple el patrón `^CL-[A-Z]{2}$` (ISO 3166-2 de Chile).
- `weekday` en inglés (`monday`…`sunday`).
- `duration_days` ≥ 1; `irrenunciability_category` ∈ [1,5] o `null`.

## Estabilidad

El esquema sigue versionado semántico a partir de la Fase 1. Cambios incompatibles incrementarán la versión mayor y se registrarán en [`CHANGELOG.md`](../CHANGELOG.md).
