# NEXT_STEPS_GITHUB

Instrucciones para publicar `calendario-chile` **cuando el titular lo decida**. Nada de esto se ha ejecutado todavía: el repositorio sólo tiene commits **locales**, sin remoto ni push.

## 1. Conectar el remoto y hacer push

```bash
git remote add origin git@github.com:<usuario-o-org>/calendario-chile.git
git branch -M main
git push -u origin main
git push origin v0.1.0-rc1.2
```

> Reemplazar `<usuario-o-org>` por el usuario u organización de GitHub elegido.

## 2. Crear la GitHub Release `v0.1.0`

Los artefactos completos están en `release_artifacts/v0.1.0/` (carpeta hermana del proyecto, fuera de este repo). Reemplaza `<ruta-artefactos>` por su ubicación local.

```bash
cd <ruta-artefactos>/release_artifacts/v0.1.0

# verificar integridad antes de subir
shasum -c SHA256SUMS.txt

# crear la release y adjuntar los ZIPs + checksums
gh release create v0.1.0 \
  calendario-chile-json-v0.1.0.zip \
  calendario-chile-csv-v0.1.0.zip \
  calendario-chile-sqlite-v0.1.0.zip \
  calendario-chile-parquet-v0.1.0.zip \
  calendario-chile-api-v0.1.0.zip \
  calendario-chile-ics-v0.1.0.zip \
  SHA256SUMS.txt \
  --title "calendario-chile v0.1.0" \
  --notes-file ../../public_repo_ready/calendario-chile/CHANGELOG.md
```

## 3. Activar GitHub Pages (API estática + .ics)

Opciones:

- **Pages desde rama:** publicar el contenido de `data/api/v1/` y `data/public/ics/` en una rama/carpeta servida por Pages (p. ej. `gh-pages` o `/docs`).
- **Pages vía workflow:** crear un workflow de despliegue que suba esos directorios a Pages.

Apuntar Pages a la carpeta/branch que se defina y confirmar el dominio resultante (p. ej. `https://<usuario>.github.io/calendario-chile/`).

## 4. Validar URLs públicas

```bash
curl -s https://<host>/v1/index.json | jq .
curl -s https://<host>/v1/metadata.json | jq '.license'      # debe decir "MIT"
curl -s https://<host>/v1/years/2025.json | jq '.[0].name.es'
# .ics suscribible:
#   https://<host>/ics/feriados-chile.ics
```

## 5. Checklists

Antes de publicar, revisar `docs/publishing_plan.md` (checklist de primer commit y de primer release) y `reports/PUBLIC_REPO_READINESS.md`.

## Recordatorio

- La licencia es **MIT** (`LICENSE`).
- No publicar `data/internal/` ni fuentes brutas (no están en este repo).
- No usar Git LFS.
