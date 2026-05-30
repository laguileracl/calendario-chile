# FINAL_RELEASE_REPORT

Promoción de `calendario-chile` a versión **final `v0.1.0`** (release no-prerelease), a partir del release candidate `v0.1.0-rc1.2`.

- **Fecha:** 2026-05-30 (UTC).
- **Versión final:** `v0.1.0`.
- **Relación con el RC:** promueve `v0.1.0-rc1.2` a `v0.1.0`. El tag `v0.1.0-rc1.2` **no se mueve ni se modifica**; permanece en `298d1a3` como prerelease.

## URLs

- Repo: https://github.com/laguileracl/calendario-chile
- Release final: https://github.com/laguileracl/calendario-chile/releases/tag/v0.1.0
- Release candidate (se mantiene): https://github.com/laguileracl/calendario-chile/releases/tag/v0.1.0-rc1.2
- Pages: https://laguileracl.github.io/calendario-chile/

## Commit y tags

- **Commit del release final:** `9ade4ed (9ade4ed46251aef3668599669d63ead06a077c34)` (commit "Prepare final v0.1.0 release").
- **Tag `v0.1.0`** → apunta al commit final.
- **Tag `v0.1.0-rc1.2`** → `298d1a3` (intacto, sin mover).

## Validación (preflight)

- `make validate`: OK.
- `make test`: 7/7 OK.
- `make clean-check`: limpio (terceros 0, pendiente-activo 0, rutas absolutas 0).
- CI `validate.yml` en `main`: verde.

## Artefactos finales

Preparados en `release_artifacts/v0.1.0-final/`, contenido idéntico al RC (mismos hashes), nombres definitivos:

| Archivo |
|---|
| `calendario-chile-api-v0.1.0.zip` (API completa 1981–2100) |
| `calendario-chile-json-v0.1.0.zip` |
| `calendario-chile-csv-v0.1.0.zip` |
| `calendario-chile-sqlite-v0.1.0.zip` |
| `calendario-chile-parquet-v0.1.0.zip` |
| `calendario-chile-ics-v0.1.0.zip` |
| `SHA256SUMS.txt` |
| `ARTIFACT_MANIFEST.md` |

- **Hashes:** `shasum -a 256 -c SHA256SUMS.txt` → 6/6 OK (local).
- **Verificación post-subida (descarga desde GitHub):** `6/6 OK (descargados desde GitHub Release v0.1.0)`.

## Pages

- Activa; API estática parcial (índices + años 2020/2022/2025/2026) e `.ics` accesibles por HTTPS.
- La API completa 1981–2100 se distribuye como artefacto de release (`calendario-chile-api-v0.1.0.zip`), **no** comprometida íntegra al repo (decisión mantenida).

## Limitaciones conocidas

- 665 registros `low-confidence` documentados para revisión futura.
- 29 eventos escolares de ámbito restringido marcados `requires_manual_review`.

## Confirmaciones

- ✅ Licencia **MIT** (detectada por GitHub vía endpoint `/license`).
- ✅ **No se movió** el tag `v0.1.0-rc1.2`.
- ✅ **No se alteraron datos sustantivos** (artefactos idénticos en contenido/hashes al RC).
- ✅ Sin `data/internal` ni fuentes raw en repo/artefactos.
- ✅ Sin Git LFS.

## Estado del release final (se completa tras crear tag y release)

- Release `v0.1.0` visible y **no-prerelease:** `visible, prerelease=false, latest del repo`.
- Assets adjuntos: `8 (6 ZIP + SHA256SUMS.txt + ARTIFACT_MANIFEST.md)`.
