# QUALITY_REPORT — calendario-chile

Validación del dataset generado a partir de fuentes internas del proyecto.

- **Total de eventos:** 33,746
- **Rango de fechas:** 1981-01-01 → 2100-12-31
- **Años cubiertos:** 1981–2100 (120)

## Por calendario de origen

| Grupo | Eventos |
|---|--:|
| días nacionales | 15,266 |
| feriados ámbito normal | 8,233 |
| feriados bancarios | 6,011 |
| días nacionales no oficiales | 2,678 |
| días locales | 869 |
| semanas/meses/años nacionales | 448 |
| feriados locales ámbito normal | 211 |
| feriados ámbito restringido | 30 |

## Por tipo

| type | Eventos |
|---|--:|
| commemorative | 18,392 |
| public | 8,233 |
| bank | 6,011 |
| local | 1,080 |
| restricted | 30 |

## Por categoría

| category | Eventos |
|---|--:|
| other | 19,159 |
| religious | 7,430 |
| civic | 7,157 |

## Confianza

| confidence | Eventos |
|---|--:|
| high | 31,708 |
| medium | 1,375 |
| low | 663 |

## Por década

| Década | Eventos |
|---|--:|
| 1980s | 1,482 |
| 1990s | 1,842 |
| 2000s | 2,094 |
| 2010s | 2,506 |
| 2020s | 3,120 |
| 2030s | 3,195 |
| 2040s | 3,199 |
| 2050s | 3,198 |
| 2060s | 3,199 |
| 2070s | 3,198 |
| 2080s | 3,196 |
| 2090s | 3,198 |
| 2100s | 319 |

## Indicadores de calidad

| Indicador | Valor |
|---|--:|
| Duplicados exactos | 0 |
| Posibles duplicados semánticos | 0 |
| Eventos sin fecha | 0 |
| Eventos sin nombre | 0 |
| Tipo no válido | 0 |
| Categoría no válida | 0 |
| Locales sin alcance territorial | 0 |
| Feriados/bancarios sin fundamento legal | 29 |
| DTEND problemático | 0 |
| Eventos multi-día | 641 |
| Recurrentes | 33,649 |
| Singulares | 97 |
| Irrenunciables | 520 |
| Con subdivisión ISO | 402 |

## Tests automáticos

| Test | Resultado | Detalle |
|---|:--:|---|
| Todas las fechas son válidas ISO | ✅ | 0 inválidas |
| start_date <= end_date | ✅ |  |
| year coincide con start_date | ✅ |  |
| type dentro del enum | ✅ |  |
| category dentro del enum | ✅ |  |
| subdivisions con ISO 3166-2 válido | ✅ |  |
| eventos multi-día con duración > 1 | ✅ |  |
| IDs únicos | ✅ |  |
| categoría de irrenunciabilidad en 1..5 | ✅ |  |
| cobertura 1981–2100 completa | ✅ | faltan 0 |

**10/10 tests aprobados.**
