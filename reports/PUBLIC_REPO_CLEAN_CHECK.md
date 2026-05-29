# PUBLIC_REPO_CLEAN_CHECK

Verificación anti-contaminación del repositorio público (`public_repo_ready/calendario-chile/`).

## Chequeos estructurales

| Chequeo | Resultado |
|---|:--:|
| No existe data/internal/ | ✅ |
| No existe LICENSE_DRAFT.md | ✅ |
| No existe OBSOLETE_LICENSE_DRAFT.md | ✅ |
| No hay fuentes raw (.html de fuente / carpeta raw) | ✅ |
| LICENSE (MIT) presente | ✅ |
| pyproject declara MIT | ✅ |

## Búsqueda de patrones

| Patrón | Coincidencias | Bloqueante |
|---|--:|:--:|
| Terceros / fuentes externas | 0 | sí |
| Licencia pendiente en archivo autoritativo | 0 | sí |
| Mención histórica de licencia (CHANGELOG/reports/ADR) | 3 | no |
| Rutas absolutas locales (`/Users/...`) | 0 | sí |

_Menciones históricas no bloqueantes (documentan que el estado pendiente fue superado por MIT):_ `CHANGELOG.md`, `docs/publishing_plan.md`, `reports/LICENSE_DECISION_REPORT.md`

> Nota: `public_clean_check.py`, `validate_public.py` y `test_public_data.py` nombran patrones por diseño y se excluyen; los `.ics` se omiten (binarios de calendario). La licencia se valida en los archivos de declaración autoritativa (README, pyproject, LICENSE, datapackage, metadata, legal_notes).

## Conclusión

✅ Repo público limpio para revisión humana.
