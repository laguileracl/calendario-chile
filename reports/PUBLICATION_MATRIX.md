# PUBLICATION_MATRIX — Qué publicar, cómo y dónde

Clasificación de cada grupo de archivos para la publicación Fase 1. Tamaños aproximados (medición local). "Regenerable" = se reconstruye con el pipeline desde las fuentes internas.

| Ruta / patrón | Descripción | Tamaño aprox. | ¿Repo? | ¿Release? | ¿Privado? | ¿Regenerable? | Riesgo legal/licencia | Recomendación |
|---|---|--:|:--:|:--:|:--:|:--:|---|---|
| `src/` | Código del pipeline (paquete) | 156 KB | ✅ | — | — | no | Bajo (código propio) | **Publicar** bajo **MIT**. |
| `scripts/` | Scripts ejecutables | 48 KB | ✅ | — | — | no | Bajo | **Publicar.** |
| `tests/` | Suite de tests | 52 KB | ✅ | — | — | no | Bajo | **Publicar.** |
| `docs/` | Documentación | 56 KB | ✅ | — | — | no | Bajo (sin terceros) | **Publicar** bajo **MIT**. |
| `schema/` | JSON Schema + datapackage | 16 KB | ✅ | — | — | sí | Bajo | **Publicar** (contrato de datos). |
| `reports/` | Reportes de calidad/legal/release | 24 KB | ✅ | — | — | sí | Bajo | **Publicar** (transparencia); excluye material interno. |
| `data/public/json/` | MVP feriados (JSON) | 48 MB | ⚠️ | ✅ | — | sí | Bajo (MIT) | **Release** (pesado); en repo sólo `SAMPLE.json`. |
| `data/public/csv/` | MVP feriados (CSV) | 14 MB | ⚠️ | ✅ | — | sí | Bajo (MIT) | **Release**. |
| `data/public/ics/` | iCalendar publicable | 6.9 MB | ⚠️ | ✅ | — | sí | Bajo (MIT) | **Release** (o Pages para suscripción). |
| `data/public/sqlite/` | MVP en SQLite | 16 MB | ❌ | ✅ | — | sí | Bajo (MIT) | **Release** opcional; no en repo. |
| `data/public/parquet/` | MVP en Parquet | 588 KB | ⚠️ | ✅ | — | sí | Bajo (MIT) | **Release** (liviano; podría ir en repo). |
| `data/public/SAMPLE.json` | Muestra 2025 (público) | 400 KB | ✅ | — | — | sí | Bajo (MIT) | **Publicar en repo** (ejemplo navegable). |
| `data/api/v1/index.json`, `metadata.json`, `hoy.json`, `proximos.json` | Índices API livianos | ~170 KB | ✅ | — | — | sí | Bajo (MIT) | **Publicar** (Pages/repo). |
| `data/api/v1/years/` | API por año (120 archivos) | 83 MB | ⚠️ | ✅ | — | sí | Bajo (MIT) | **GitHub Pages** (ideal) o Release; no commit directo del bulk. |
| `data/internal/raw/` | Fuentes brutas (HTML + `.ics`) | 24 MB | ❌ | ❌ | ✅ | n/a | **Alto** (revisión previa) | **Mantener privado** hasta revisión legal. |
| `data/internal/intermediate/` | Dataset completo con trazabilidad | 238 MB | ❌ | ❌ | ✅ | sí | Medio (procedencia interna) | **Mantener privado**; regenerable. |
| `data/internal/audit/` | Catálogo legal + revisión de referencias | 416 KB | ❌ | — | ✅ | sí | Medio | **Privado**; insumo de auditoría. |
| `notebooks/` | Análisis exploratorio | 4 KB | ✅ | — | — | no | Bajo | **Publicar** (es liviano; sin outputs guardados). |
| `.github/workflows/` | CI (validate/build) | 8 KB | ✅ | — | — | no | Bajo | **Publicar.** |

## Convenciones

- ✅ repo: se versiona en el repositorio.
- ⚠️ repo: sólo muestra/índice liviano; el bulk va a Release/Pages.
- ❌ repo: no se versiona.

## Síntesis

- **Repo liviano:** código + docs + schema + reports + `SAMPLE.json` + índices API + notebooks + CI (~360 KB de contenido versionado, fuera de datos pesados).
- **GitHub Pages:** API estática (`data/api/v1/`) — ideal para `years/` y suscripción `.ics`.
- **GitHub Releases:** datasets completos (`data/public/*`) comprimidos.
- **Privado:** todo `data/internal/`.
