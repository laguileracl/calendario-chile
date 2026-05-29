# Plan de publicación

Estrategia de distribución de `calendario-chile` para la Fase 1. **Nada está publicado aún.**

## Estructura del repo público

```
calendario-chile/
  README.md  LICENSE  CHANGELOG.md  CONTRIBUTING.md  CODE_OF_CONDUCT.md  SECURITY.md
  pyproject.toml  Makefile  .gitignore  .gitattributes  .editorconfig
  src/            # paquete calendario_chile (pipeline)
  scripts/        # ejecutables (validate_public, public_clean_check, build_*)
  tests/          # tests sobre los datos incluidos
  .github/workflows/validate.yml
  schema/         # JSON Schema + datapackage
  docs/           # documentación
  reports/        # reportes públicos
  data/public/SAMPLE.json
  data/public/ics/*.ics
  data/api/v1/{index,metadata,hoy,proximos}.json
  data/api/v1/years/{2020,2022,2025,2026}.json
```

## Qué se publica y dónde

| Destino | Contenido |
|---|---|
| **GitHub (repo)** | Código, docs, schema, tests, workflows, muestra, `.ics`, API parcial. |
| **GitHub Releases** | Datasets completos comprimidos (JSON/CSV/SQLite/Parquet/API/ICS) + `SHA256SUMS.txt`. |
| **GitHub Pages** | API estática completa (`v1/years/*.json`, índices) y `.ics` para suscripción. |
| **Privado (no se publica)** | `data/internal/` (fuentes brutas, intermedios, auditoría). |

**Git LFS:** no se usa en Fase 1 (datos regenerables + Releases cubren el caso).

## Comandos de publicación futura (referencia)

```bash
# 1) inicializar repo y primer commit (cuando se decida publicar)
git init && git add . && git commit -m "feat: calendario-chile v0.1.0"

# 2) crear el repositorio remoto y empujar
gh repo create calendario-chile --public --source=. --push

# 3) artefactos de release (generados en release_artifacts/v0.1.0/)
gh release create v0.1.0 release_artifacts/v0.1.0/*.zip \
  release_artifacts/v0.1.0/SHA256SUMS.txt --title "v0.1.0" --notes-file CHANGELOG.md

# 4) GitHub Pages: publicar data/api/v1 + ics (workflow de despliegue)
```

## Checklist antes del primer commit

- [ ] `make validate` y `make test` en verde.
- [ ] `make clean-check` sin observaciones (sin material interno ni terceros).
- [ ] `LICENSE` (MIT) presente; sin "licencia pendiente".
- [ ] Sin rutas absolutas locales en docs/reportes.
- [ ] `.gitignore` excluye `data/internal/`, `release_artifacts/`, datasets pesados.
- [ ] README revisado; disclaimer de no asesoría legal presente.

## Checklist antes del primer release

- [ ] Generar artefactos en `release_artifacts/v0.1.0/` y `SHA256SUMS.txt`.
- [ ] Verificar hashes (`shasum -c SHA256SUMS.txt`).
- [ ] Confirmar que ningún artefacto contiene `data/internal/` ni fuentes brutas.
- [ ] Redactar notas de release a partir del `CHANGELOG.md`.
- [ ] Configurar despliegue de GitHub Pages para la API estática.
