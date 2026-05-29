# Descargas y datasets completos

Este repositorio público es **liviano**: incluye el pipeline, la documentación, el esquema, una **muestra** y una **API estática parcial** (años 2020, 2022, 2025, 2026). Los **datasets completos** (todos los eventos / todos los años) no se versionan aquí por peso.

## Cómo obtener los datasets completos

### Opción A — Regenerar con el pipeline

El dataset completo se reconstruye con el código de `src/calendario_chile` a partir de los insumos del proyecto (no incluidos en el repo público). Con esos insumos disponibles, los scripts de `scripts/` generan todos los formatos.

### Opción B — GitHub Release

Los datasets completos se publican como **artefactos comprimidos** en la GitHub Release correspondiente a la versión. Nombres de artefactos esperados para `v0.1.0`:

| Artefacto | Contenido |
|---|---|
| `calendario-chile-json-v0.1.0.zip` | Dataset público completo en JSON |
| `calendario-chile-csv-v0.1.0.zip` | Dataset público completo en CSV |
| `calendario-chile-sqlite-v0.1.0.zip` | Base SQLite (events + tablas) |
| `calendario-chile-parquet-v0.1.0.zip` | Dataset en Parquet |
| `calendario-chile-api-v0.1.0.zip` | API estática completa (1981–2100) |
| `calendario-chile-ics-v0.1.0.zip` | Calendarios iCalendar |

> Estos nombres son la convención prevista. La Release y los artefactos **aún no están publicados**.

### Opción C — GitHub Pages

La **API estática completa** (todos los años) y los `.ics` están pensados para servirse vía GitHub Pages/CDN, de modo que se puedan consumir por URL sin descargar el repositorio.

## Integridad

Cada Release incluirá un archivo `SHA256SUMS.txt` con los hashes de los artefactos para verificación.

## Qué SÍ está en el repo

- `data/public/SAMPLE.json` — muestra (feriados 2025).
- `data/public/ics/*.ics` — calendarios suscribibles.
- `data/api/v1/{index,metadata,hoy,proximos}.json` — índices.
- `data/api/v1/years/{2020,2022,2025,2026}.json` — años seleccionados.
