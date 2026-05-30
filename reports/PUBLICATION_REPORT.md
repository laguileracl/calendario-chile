# PUBLICATION_REPORT

> **Actualización (2026-05-30):** el proyecto fue promovido a la versión final **`v0.1.0`** (release no-prerelease). Este documento describe la publicación del **release candidate** `v0.1.0-rc1.2`, que se mantiene como prerelease. Ver `reports/FINAL_RELEASE_REPORT.md`.

Reporte de la publicación controlada de `calendario-chile` como **release candidate público** (no versión final).

## Datos de publicación

- **Fecha:** 2026-05-30 (UTC).
- **Repositorio:** https://github.com/laguileracl/calendario-chile
- **Visibilidad:** público.
- **Remoto:** `origin` → `https://github.com/laguileracl/calendario-chile.git` (HTTPS).
- **Cuenta GitHub:** `laguileracl` (gh CLI autenticado).
- **Rama publicada:** `main`.
- **Tag publicado:** `v0.1.0-rc1.2` → commit `298d1a3` (anotado).

## Release

- **URL:** https://github.com/laguileracl/calendario-chile/releases/tag/v0.1.0-rc1.2
- **Tipo:** **prerelease** (no es release final; `isPrerelease=true`, `isDraft=false`).
- **Título:** `v0.1.0-rc1.2 — Public release candidate`.

### Artefactos adjuntos (8)

| Archivo | Tamaño |
|---|--:|
| `calendario-chile-api-v0.1.0.zip` | 11.003.128 B |
| `calendario-chile-json-v0.1.0.zip` | 1.384.585 B |
| `calendario-chile-sqlite-v0.1.0.zip` | 795.396 B |
| `calendario-chile-parquet-v0.1.0.zip` | 483.468 B |
| `calendario-chile-ics-v0.1.0.zip` | 460.983 B |
| `calendario-chile-csv-v0.1.0.zip` | 437.139 B |
| `SHA256SUMS.txt` | 596 B |
| `ARTIFACT_MANIFEST.md` | 1.723 B |

Hashes verificados localmente antes de subir: **6/6 OK** (`shasum -c SHA256SUMS.txt`).

## GitHub Pages

- **Estado:** activo (Deploy from branch `main`, carpeta `/`).
- **URL base:** https://laguileracl.github.io/calendario-chile/

### URLs públicas validadas (todas HTTP 200)

```
/                                       200
/data/api/v1/metadata.json              200   (license=MIT, total_events=33746, 1981–2100)
/data/api/v1/index.json                 200
/data/api/v1/hoy.json                   200
/data/api/v1/proximos.json              200
/data/api/v1/years/2020.json            200
/data/api/v1/years/2022.json            200
/data/api/v1/years/2025.json            200
/data/api/v1/years/2026.json            200
/data/public/ics/feriados-chile.ics     200
```

> La API completa de los 120 años **no** se publicó en el repo/Pages; queda disponible como artefacto ZIP en la Release (`calendario-chile-api-v0.1.0.zip`).

## CI (GitHub Actions)

- Workflow `validate.yml`: **success** (≈23 s) sobre el commit publicado en `main`.
- `pages build and deployment`: completado (sitio live).
- `Dependency Graph`: success.

## Licencia

- `LICENSE` (MIT, titular Luis Aguilera 2026) presente en el repo y servido en Pages.
- `metadata.json` declara `license: MIT`.
- La **detección automática de licencia** de GitHub (`licenseInfo`) puede tardar en propagar; al cierre de este reporte aún no estaba reflejada en la API de repo. No bloquea: el archivo `LICENSE` es MIT canónico.

## Problemas encontrados y resueltos

- En preflight, `make clean-check` detectó **1 ruta absoluta local** (de tipo `/<usuario>/…`) introducida en `NEXT_STEPS_GITHUB.md`. Se corrigió **antes** del primer push (commit `298d1a3`) y se re-apuntó el tag al snapshot limpio **estando aún sin publicar**. Tras ello, clean-check quedó limpio.

## Integridad del tag

- El tag `v0.1.0-rc1.2` apunta a `298d1a3` y **no se movió después de publicar**. El reporte de publicación se registra en un **commit posterior** al tag (el tag permanece en el snapshot del release candidate).

## Próximos pasos para promover a `v0.1.0` final

1. Revisar documentación, API y artefactos publicados; recoger feedback del release candidate.
2. (Opcional) abordar por lotes los 665 `low-confidence` y los 29 feriados escolares restringidos.
3. Confirmar detección de licencia MIT en GitHub.
4. Cuando esté validado: crear tag `v0.1.0`, Release final (no prerelease) y, si se desea, publicar la API completa de 120 años en Pages o como artefacto estable.
