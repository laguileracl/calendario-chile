# MISSING_LEGAL_BASIS_REVIEW — Feriados del MVP sin fundamento legal

Estado tras el patch de plebiscitos (`v0.1.0-rc1.2`): quedan **29** feriados del MVP sin `legal_basis` mapeado (antes 31).

## Resueltos en este ciclo (2)

Los **2 plebiscitos nacionales** públicos irrenunciables fueron corregidos con fundamento legal oficial. Ver `PLEBISCITES_LEGAL_BASIS_PATCH.md`.

| Evento | Fecha | Estado |
|---|---|---|
| Plebiscito nacional (nueva constitución) | 2020-10-25 | ✅ resuelto — Ley 18.700 + Ley 19.973 (irrenunciable 2.ª cat.) |
| Plebiscito nacional (Convención Constituyente) | 2022-09-04 | ✅ resuelto — Ley 18.700 + Ley 19.973 (irrenunciable 2.ª cat.) |

## Pendientes (29) — Nacimiento del Prócer de la Independencia (escolar)

29 ocurrencias anuales (1981–2013), feriado **escolar de ámbito restringido** (`type = restricted`). La norma probable es de rango administrativo/escolar o municipal, **no presente** en el catálogo de normas, y el evento no trae ancla a definición.

- **Motivo de ausencia:** norma administrativa/escolar no catalogada + evento sin ancla.
- **Recomendación:** **mantener** y **marcar como histórico/restringido**; `legal_basis` vacío con nota. **`requires_manual_review`** (no inventar). **No bloquea** el MVP de feriados públicos.
- **Restricción cumplida:** estos 29 eventos escolares **no fueron modificados** en este ciclo.

| id (muestra) | fecha |
|---|---|
| `cl-1981-08-20-nacimiento-del-procer-de-la-inde…` | 1981-08-20 |
| `cl-1982-08-20-nacimiento-del-procer-de-la-inde…` | 1982-08-20 |
| `cl-1983-08-20-nacimiento-del-procer-de-la-inde…` | 1983-08-20 |
| `cl-1984-08-20-nacimiento-del-procer-de-la-inde…` | 1984-08-20 |
| `cl-1985-08-20-nacimiento-del-procer-de-la-inde…` | 1985-08-20 |
| … (+24 más) | |

## Conclusión

- 2/31 resueltos (plebiscitos públicos irrenunciables) con fuente oficial.
- 29/31 restantes = conmemoración escolar restringida → `requires_manual_review`, bajo impacto, sin tocar.
- Ningún feriado **público de ámbito normal** queda sin fundamento legal.
