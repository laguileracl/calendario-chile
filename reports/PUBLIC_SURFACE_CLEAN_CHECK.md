# PUBLIC_SURFACE_CLEAN_CHECK — Verificación de superficie pública

Verificación de que la superficie pública del release candidato no contiene referencias a terceros ni a fuentes de origen externas.

## Patrones buscados

**3 patrones** correspondientes a nombres de terceros y dominios de origen externos (insensible a mayúsculas). La lista literal se mantiene sólo en el material interno de auditoría para evitar que este propio reporte la contenga.

## Archivos / zonas revisadas

- Raíz: `README.md`, `LICENSE`, `CHANGELOG.md`.
- `docs/` (incl. `decisions/`), `schema/`, `reports/`.
- `data/public/` (json, csv, ics, parquet, SAMPLE) y `data/api/` (índices y años).

## Métodos

1. **Automático:** `scripts/clean_public_release.py` (`make clean-check`).
2. **Manual:** `grep -rIil` sobre la superficie pública.

## Resultado

| Verificación | Coincidencias en zona pública | Estado |
|---|--:|:--:|
| Automática (`clean_public_release`) | 0 | ✅ |
| Manual (`grep`) | 0 | ✅ |

### Observación (no es hallazgo)

Dos archivos **de código** nombran los patrones **por diseño** y no son superficie de datos/documentación:
- `scripts/clean_public_release.py` — es el propio escáner (lista de patrones a detectar).
- `tests/test_api_outputs.py` — verifica que dichos patrones **no** aparezcan en la vista pública.

Ambos quedan fuera de las zonas públicas escaneadas y no constituyen atribución.

## Material interno (esperado, no publicable)

Las referencias de origen persisten **sólo** en `data/internal/` (45 archivos: fuentes brutas + dataset completo con trazabilidad). Es el comportamiento esperado y está documentado en `data/internal/audit/REVIEW_THIRD_PARTY_REFERENCES.md`. **No** forma parte del release candidato.

## Conclusión

✅ **El release candidato `v0.1.0-rc1` está limpio para revisión humana** en su superficie pública.
