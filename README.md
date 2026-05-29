# calendario-chile

> Dataset abierto del calendario chileno: feriados públicos, feriados bancarios, eventos locales y calendario legal, 1981–2100.

**Estado:** `v0.1.0-rc1.2` — release candidato (preparación para primera publicación). **Licencia: [MIT](LICENSE).**

## Descripción

`calendario-chile` es un dataset estructurado y reproducible del calendario chileno: feriados públicos, feriados bancarios, eventos locales/regionales, feriados de ámbito restringido y días conmemorativos, con cobertura **1981–2100**, **fundamento legal** por evento, **alcance territorial** (ISO 3166-2) e **irrenunciabilidad** laboral con su categoría. Aspira a ser una fuente de referencia abierta e interoperable para el calendario de Chile.

## Qué incluye este repositorio

- **Pipeline** (`src/`, `scripts/`): código que genera y valida el dataset.
- **Esquema** (`schema/`): JSON Schema + Frictionless datapackage.
- **Documentación** (`docs/`) y **reportes** (`reports/`).
- **Muestra** (`data/public/SAMPLE.json`): feriados públicos y bancarios de 2025.
- **iCalendar** (`data/public/ics/`): calendarios `.ics` suscribibles.
- **API estática (parcial)** (`data/api/v1/`): índices + años 2020, 2022, 2025 y 2026.

## Qué NO incluye todavía

- Los **datasets completos** (JSON/CSV/SQLite/Parquet de los ~33.700 eventos) y la **API de los 120 años** no se versionan aquí por peso. Se publican como **GitHub Release** o se regeneran con el pipeline. Ver [`docs/downloads.md`](docs/downloads.md).
- Las **fuentes internas** del proyecto no forman parte de la distribución pública.

## Formatos disponibles

| Formato | Dónde |
|---|---|
| JSON (muestra) | `data/public/SAMPLE.json` |
| iCalendar `.ics` | `data/public/ics/` |
| API estática JSON | `data/api/v1/` (años 2020/2022/2025/2026 incluidos) |
| JSON/CSV/SQLite/Parquet completos | GitHub Release / regenerables (ver `docs/downloads.md`) |

## Ejemplo (un evento)

```json
{
  "id": "cl-2025-09-18-dia-de-la-independencia-nacional-irrenunciable",
  "date": "2025-09-18",
  "year": 2025,
  "weekday": "thursday",
  "name": { "es": "Día de la Independencia Nacional (irrenunciable)", "en": null },
  "type": "public",
  "category": "civic",
  "nationwide": true,
  "is_irrenunciable": true,
  "irrenunciability_category": 5,
  "legal_basis": [
    { "type": "ley", "number": "2.977", "role": "Recopilación y cambio de identidad", "url": null }
  ]
}
```

## Uso rápido

```bash
# feriados de la muestra (2025)
jq '.[] | select(.type=="public") | .name.es' data/public/SAMPLE.json

# eventos de un año desde la API estática
jq '.[].name.es' data/api/v1/years/2025.json

# suscribir un calendario .ics en tu agenda:
#   data/public/ics/feriados-chile.ics
```

## Validación

```bash
make validate     # valida los datos incluidos (muestra + API)
make test         # tests (pytest) sobre los datos incluidos
make clean-check  # verifica que el repo no exponga material interno
```

## Regeneración del dataset completo

El dataset completo se reconstruye con el pipeline (`src/calendario_chile`) a partir de los insumos del proyecto, **no incluidos** en este repositorio público. Con esos insumos disponibles:

```bash
make build   # imprime instrucciones; requiere los insumos
```

Alternativamente, descarga los artefactos de la **GitHub Release v0.1.0** (ver [`docs/downloads.md`](docs/downloads.md)).

## API estática

Pensada para servirse vía GitHub Pages o CDN. Endpoints: `v1/index.json`, `v1/metadata.json`, `v1/years/{YYYY}.json`, `v1/hoy.json`, `v1/proximos.json`. Detalle en [`docs/api_static.md`](docs/api_static.md).

## Limitaciones conocidas

- 29 feriados escolares de ámbito restringido sin fundamento legal mapeado (`requires_manual_review`).
- 665 registros con `confidence: low` (mayoría conmemorativos) pendientes de revisión por lotes.
- `data/api/v1/` incluye sólo años seleccionados; la API completa va por Release/Pages.

## Roadmap

- **Fase 1:** MVP de feriados públicos + bancarios (este release).
- **Fase 2:** conmemorativos, locales y fundamento legal ampliado.
- **Fase 3:** API estática completa, visor web y paquetes (PyPI/npm).
- **Fase 4:** contribuciones externas y automatización.

Ver [`docs/roadmap.md`](docs/roadmap.md).

## Licencia

Este proyecto se publica bajo licencia **MIT**. Cubre código, documentación, schemas, datasets públicos y archivos derivados de la superficie pública, salvo que un archivo indique expresamente otra cosa. Ver [`LICENSE`](LICENSE).

## Aviso

Este proyecto **no constituye asesoría legal**. Las fechas e identificadores normativos se entregan como datos de referencia; para efectos legales o laborales, verificar contra las fuentes oficiales vigentes.
