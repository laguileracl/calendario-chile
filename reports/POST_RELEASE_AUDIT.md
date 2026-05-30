# POST_RELEASE_AUDIT

Auditoría pública post-release de `calendario-chile`, previa a decidir la promoción a `v0.1.0` final. **No se crea `v0.1.0`, no se mueve el tag `v0.1.0-rc1.2`, no se cambia la licencia.**

- **Fecha:** 2026-05-30 (UTC).
- **Auditor:** revisión externa de publicación.

## URLs auditadas

- Repo: https://github.com/laguileracl/calendario-chile
- Release (prerelease): https://github.com/laguileracl/calendario-chile/releases/tag/v0.1.0-rc1.2
- Pages: https://laguileracl.github.io/calendario-chile/

## 1. Repositorio público

| Check | Resultado |
|---|---|
| Visibilidad | público ✅ |
| Descripción | clara ✅ |
| LICENSE detectada por GitHub | **MIT** ✅ (endpoint `/license` → `MIT`; el campo `licenseInfo` de la API de repo iba rezagado) |
| Branch por defecto | `main` ✅ |
| Topics | aplicados (12) ✅ |
| Homepage | apunta a Pages ✅ |
| Archivos prohibidos en el árbol remoto | **0** ✅ (sin `data/internal`, `/raw/`, `.html`, `LICENSE_DRAFT`, `OBSOLETE`, `release_artifacts`) |
| `.ics` remotos | sólo en `data/public/ics/` (4) ✅ |
| Años de API en repo | sólo 2020/2022/2025/2026 ✅ |
| Rutas locales absolutas | 0 en superficie pública ✅ (ver hallazgo M-1) |

## 2. GitHub Pages

10/10 URLs **HTTP 200** con content-type correcto:

| Recurso | HTTP | Content-Type |
|---|--:|---|
| `/` | 200 | text/html |
| `data/api/v1/metadata.json` | 200 | application/json |
| `data/api/v1/index.json` | 200 | application/json |
| `data/api/v1/hoy.json` | 200 | application/json |
| `data/api/v1/proximos.json` | 200 | application/json |
| `data/api/v1/years/{2020,2022,2025,2026}.json` | 200 | application/json |
| `data/public/ics/feriados-chile.ics` | 200 | text/calendar |

- JSON válido; años coherentes (cada archivo contiene sólo su año).
- **Sin** bloque interno `source`; **sin** rutas locales; **sin** referencias externas.
- `metadata.json`: `license = MIT`, `total_events = 33746`, cobertura 1981–2100. ✅

## 3. Release y artefactos (descargados desde GitHub)

- Tipo: **prerelease** ✅ (no final). 8 assets.
- **Hashes:** `shasum -c SHA256SUMS.txt` → **6/6 OK** ✅ (verificado sobre las descargas, no sobre los locales).
- **Integridad ZIP:** los 6 descomprimen sin error ✅.
- **Contenido:** ningún ZIP contiene `data/internal`, fuentes raw, `.html` ni archivos obsoletos de licencia ✅.
- **API completa:** `calendario-chile-api-v0.1.0.zip` cubre **1981–2100 (120 años)** ✅.
- **Schema:** `calendario-chile-json-v0.1.0.zip` → 15.354 eventos (MVP feriados), claves esperadas, con `legal_basis`, **sin** `source` ✅.
- `ARTIFACT_MANIFEST.md` consistente con los 6 artefactos publicados ✅.

## 4. Documentación

- README, `docs/downloads.md`, `docs/publishing_plan.md`, `docs/api_static.md`, `docs/legal_notes.md`, `reports/PUBLICATION_REPORT.md`, `reports/PUBLIC_REPO_READINESS.md`: revisados.
- Disclaimer "no constituye asesoría legal" presente en README y `legal_notes.md` ✅.
- Sin lenguaje exagerado/absoluto; sin declarar "release final" indebidamente ✅.
- URLs apuntan correctamente a `laguileracl` ✅.
- **Hallazgo menor (M-2):** los artefactos se nombran `-v0.1.0.zip` mientras el tag/release es `v0.1.0-rc1.2`. Es intencional (los artefactos llevan el contenido del eventual `0.1.0`), pero puede confundir a un usuario externo.

## 5. CI

- `validate.yml` en el commit del tag (`298d1a3`): **success** ✅.
- `pages-build-deployment`: **success** (sitio `built`) ✅.
- `validate.yml` en el commit del reporte de publicación (`eefd889`): **failure** → ver hallazgo M-1 (corregido en esta auditoría).

## Hallazgos

| ID | Severidad | Descripción | Acción |
|---|---|---|---|
| **M-1** | minor | El paso `clean-check` falló en `main` porque `reports/PUBLICATION_REPORT.md` contenía un literal de ruta absoluta (escrito como ejemplo al documentar el arreglo previo), que el escáner detecta. | **Corregido**: reemplazado por un placeholder `/<usuario>/…`. Commit separado; el tag no se movió. |
| **M-2** | minor | Nombres de artefactos `-v0.1.0.zip` vs tag `v0.1.0-rc1.2`. | Documentado; resolver al promover a `v0.1.0` (renombrar artefactos o alinear naming). No bloquea. |
| C-1 | cosmetic | `licenseInfo` de la API de repo iba rezagado (el endpoint `/license` ya devuelve MIT). | Sin acción; se resuelve solo. |

- **Blockers:** 0. **Majors:** 0. **Minors:** 2 (1 corregido). **Cosmetic:** 1.

## Recomendación final

**Mantener como release candidate (`v0.1.0-rc1.2`) y corregir los menores antes de promover.** El repo, Pages, Release y artefactos están **sanos e íntegros**; el único fallo real (CI por autorreferencia de ruta) quedó corregido en esta pasada. Antes de promover a `v0.1.0` final se recomienda:

1. Confirmar **CI verde en `main`** tras el fix M-1.
2. Resolver el naming de artefactos (M-2).
3. (Opcional) abordar por lotes los 665 `low-confidence` y los 29 feriados escolares restringidos.

No se identificaron motivos para retirar o despublicar el release candidate.
