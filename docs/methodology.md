# Methodology

El dataset se genera con un pipeline reproducible a partir de **fuentes internas del proyecto**: calendarios en formato iCalendar (`.ics`) y documentos de apoyo en HTML (definiciones, clasificación por ocurrencia y catálogo de normas).

## 1. Extracción desde fuentes propias

- **Calendarios `.ics`** → eventos base: fecha(s), nombre, ancla de definición, alcance territorial y metadatos.
- **Documentos HTML** → tres capas complementarias:
  - *Definiciones*: fecha, vigencia, ámbito, irrenunciabilidad (con tramos por año), carácter y normativa relevante.
  - *Clasificación por ocurrencia*: por cada (fecha, ancla), las marcas de irrenunciabilidad y su categoría, carácter religioso, recurrencia, etc.
  - *Catálogo de normas*: tipo, número, año, título y enlace a la ficha oficial.

## 2. Parsing de iCalendar (RFC 5545)

Cada `VEVENT` se desdobla (líneas continuadas) y se leen `DTSTART`, `DTEND`, `SUMMARY`, `URL`, `LOCATION`, `UID` y `LAST-MODIFIED`.

### Tratamiento de `DTEND` exclusivo

En eventos de día completo (`VALUE=DATE`), **`DTEND` es exclusivo**: corresponde al día siguiente al último día del evento. Por lo tanto:

```
duration_days = DTEND − DTSTART        (en días)
end_date      = DTEND − 1 día          (último día inclusivo)
```

Un evento de un día tiene `DTEND = DTSTART + 1`, `duration_days = 1` y `end_date = start_date`. Los eventos multi-día (semanas, meses, años) se modelan con su rango real e inclusivo.

## 3. Resolución de definiciones

El ancla del evento se cruza con el catálogo de definiciones:

1. **Exacto** → match directo.
2. **Prefijo** → las anclas en `.ics` pueden venir truncadas (~22 caracteres); se resuelven por prefijo único.
3. **Nombre** → si hay ambigüedad o no hay ancla, se compara el nombre normalizado.

La cobertura confiable (exacto + prefijo único) ronda el 89%; el resto se conserva con `confidence` `medium`/`low`. **Ningún evento se descarta.**

## 4. Normalización

- **Nombres y slugs:** limpieza de entidades/etiquetas, normalización de espacios; `slug` sin tildes.
- **Fechas:** ISO 8601; `weekday` derivado.
- **Tipos y categorías:** vocabularios controlados (ver [data_dictionary](data_dictionary.md)).
- **Irrenunciabilidad:** se prioriza el dato por ocurrencia (año concreto); si falta, se infiere del tramo declarado en la definición y se marca como inferencia.
- **Recurrencia:** del dato por ocurrencia; si falta, se infiere por repetición anual.

## 5. Mapeo territorial (ISO 3166-2)

El alcance territorial en texto libre se normaliza:

- `nationwide` cuando aplica a todo el país.
- `subdivisions`: códigos **ISO 3166-2** (`CL-AP`, `CL-RM`, …) sólo cuando el mapeo de la región es confiable.
- `regions` / `communes`: nombres detectados.
- `scope_text`: **texto original** siempre preservado.

## 6. Fundamento legal

De la "normativa relevante" de cada definición se extraen referencias (rol + norma + artículo), que se resuelven contra el catálogo de normas para obtener tipo, número, año, título y enlace oficial. El texto original se conserva en `raw`.

## 7. Validaciones y derivados

Se ejecuta una suite de validación (fechas, enums, ISO, multi-día, IDs únicos, cobertura 1981–2100) y se generan los derivados (MVP público, API estática por año, iCalendar) y los reportes de calidad.

## Trazabilidad

Cada evento conserva, en material **interno**, su procedencia (`source`: archivo, ancla, método de extracción, `confidence`, `notes`). La **vista pública** omite esa procedencia y mantiene sólo los hechos.
