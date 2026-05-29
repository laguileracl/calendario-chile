# LOW_CONFIDENCE_SUMMARY — Resumen de los 665 registros de baja confianza

Agrupación de los **665** eventos con `confidence = low`. **No se corrigen individualmente todavía**: este resumen sirve para priorizar por lotes.

## Por tipo

| type | Eventos | ¿En MVP? |
|---|--:|:--:|
| commemorative | 634 | no |
| restricted | 29 | sí |
| public | 2 | sí |

**En MVP:** 31 (coinciden con los feriados sin ley). **Fuera de MVP (conmemorativos):** 634.

## Por calendario de origen

| Calendario | Eventos |
|---|--:|
| días nacionales | 414 |
| días nacionales no oficiales | 130 |
| semanas/meses/años nacionales | 90 |
| feriados ámbito restringido | 29 |
| feriados ámbito normal | 2 |

## Por década

| Década | Eventos |
|---|--:|
| 1980s | 14 |
| 1990s | 36 |
| 2000s | 20 |
| 2010s | 30 |
| 2020s | 68 |
| 2030s | 70 |
| 2040s | 70 |
| 2050s | 70 |
| 2060s | 70 |
| 2070s | 70 |
| 2080s | 70 |
| 2090s | 70 |
| 2100s | 7 |

## Motivo de baja confianza

| Motivo | Eventos |
|---|--:|
| sin ancla en .ics | 513 |
| ancla no encontrada en definiciones | 152 |

## Recomendación de priorización por lotes

1. **Lote A (alta prioridad, en MVP):** 31 feriados (2 plebiscitos + 29 escolar restringido). Ver `MISSING_LEGAL_BASIS_REVIEW.md`.
2. **Lote B (días nacionales, sin ancla):** mayor volumen; revisar mapeo por nombre normalizado para recuperar definición.
3. **Lote C (semanas/meses/años + no oficiales):** menor impacto; revisar al final.
4. **Causa raíz común:** 513 eventos sin ancla en el `.ics` (la mejora de mayor retorno es el match por nombre).

> Los 665 **no bloquean** el MVP de feriados salvo los 31 ya aislados; el resto son conmemorativos fuera del release MVP.
