# LEGAL_LICENSE_REVIEW_CHECKLIST

Revisión legal/licencia. **Licencia decidida: MIT** (titular: Luis Aguilera, 2026) para toda la superficie pública. Ver `LICENSE` y `reports/LICENSE_DECISION_REPORT.md`.

## 1. Licencia por componente — ✅ DECIDIDA

| Componente | Archivos | Licencia |
|---|---|---|
| **Código** | `src/`, `scripts/`, `tests/` | **MIT** |
| **Datos** | `data/public/`, `data/api/` | **MIT** |
| **Documentación** | `docs/`, `README.md` | **MIT** |
| **Schemas y derivados publicables** | `schema/`, `.ics`, CSV/JSON/SQLite/Parquet públicos | **MIT** |

Una **única licencia MIT** cubre toda la superficie pública (decisión del titular), salvo que un archivo indique expresamente otra cosa.

- [x] Combinación aprobada: **MIT** para todo lo público.
- [x] `LICENSE_DRAFT.md` reemplazado por `LICENSE`; el borrador quedó en `data/internal/audit/OBSOLETE_LICENSE_DRAFT.md`.
- [x] `pyproject.toml`, `schema/datapackage.json` y `data/api/v1/metadata.json` actualizados a MIT.

## 2. Inventario de contenido por sensibilidad

| Categoría | Archivos | Acción |
|---|---|---|
| **Datos propios procesados** | `data/public/*`, `data/api/*` | Publicables bajo **MIT**. |
| **Fuentes internas no publicables** | `data/internal/raw/*` (HTML, `.ics`) | **No publicar** sin revisión. |
| **Trazabilidad interna** | `data/internal/intermediate/*`, `data/internal/audit/*` | **Privado.** |
| **Referencias normativas públicas** | `legal_basis` en datos; catálogo en `data/internal/audit/legal_basis_catalog.json` | Identificadores de normas y enlaces oficiales = hechos; publicables. |

## 3. Verificaciones de contenido

- [x] **¿Texto de terceros copiado literalmente?** No: la vista pública contiene sólo datos estructurados (fechas, nombres breves, identificadores, enlaces oficiales). No se reproduce prosa extensa.
- [x] **¿URLs externas / anclas internas en el dataset público?** Excluidas: `to_public()` elimina el bloque `source` (anclas/host internos). Los únicos enlaces son a **fuentes oficiales** en `legal_basis[].url`.
- [x] **¿La documentación pública evita atribuciones indebidas?** Sí: describe el origen como *fuentes internas del proyecto procesadas*; `make clean-check` lo verifica.
- [x] **¿Declaración de "no asesoría legal"?** Presente en `README.md`, `docs/legal_notes.md` y reportes.
- [ ] **Confirmar** que ningún archivo a publicar proviene de `data/internal/raw/`.

## 4. Riesgos y mitigaciones

| Riesgo | Nivel | Mitigación |
|---|---|---|
| Licencia sin decidir | ~~Bloqueante~~ **Resuelto** | Licencia MIT fijada (sección 1). |
| Publicar fuentes brutas internas | Alto | Mantener `data/internal/` privado. |
| Confusión de origen | Medio | Documentación uniforme + `clean-check` en CI. |
| Norma sin fuente | Bajo | No inventar; marcar para revisión (ver `MISSING_LEGAL_BASIS_REVIEW.md`). |

## 5. Veredicto

- **Licencia:** **MIT** decidida y aplicada a toda la superficie pública.
- **Código, documentación y datos públicos:** licenciados (MIT) y limpios de terceros.
- **Material interno:** debe permanecer privado en Fase 1.
