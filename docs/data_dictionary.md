# Data Dictionary

Diccionario de campos del evento canónico. La **vista pública** incluye todos los campos salvo el bloque interno `source` y las anclas internas de `definition`.

## Identificación

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | string | Identificador único: `cl-{fecha}-{slug}` (sufijo numérico si colisiona). |
| `slug` | string | Nombre normalizado sin tildes ni símbolos. |
| `name.es` | string | Nombre en español. |
| `name.en` | string\|null | Nombre en inglés. `null` si no está disponible (no se traduce automáticamente). |
| `summary_original` | string | Texto original del evento, sin alterar. |

## Fechas

| Campo | Tipo | Descripción |
|---|---|---|
| `date` | date | Fecha de inicio (= `start_date`). |
| `start_date` | date | Primer día (inclusive), ISO 8601. |
| `end_date` | date | Último día (inclusive). Para 1 día, igual a `start_date`. |
| `year` | int | Año de `start_date`. |
| `weekday` | enum | Día de la semana en inglés (`monday`…`sunday`). |
| `is_multiday` | bool | `true` si abarca más de un día. |
| `duration_days` | int | Número de días (≥1). Ver tratamiento de `DTEND` en [methodology](methodology.md). |
| `recurring` | bool\|null | Se repite cada año. |
| `singular` | bool\|null | Ocurrencia única. |
| `movable` | bool | Fecha móvil (p. ej. dependiente de Pascua). |

## Tipo y clasificación

| Campo | Tipo | Valores |
|---|---|---|
| `type` | enum | `public`, `bank`, `commemorative`, `local`, `school`, `restricted`, `other`. |
| `category` | enum | `civic`, `religious`, `legal`, `cultural`, `educational`, `labor`, `environmental`, `health`, `financial`, `other`. |
| `calendar_group` | string | Grupo de origen (p. ej. *feriados ámbito normal*, *días nacionales*). |
| `is_public_holiday` | bool | Es feriado de ámbito normal/restringido/local. |
| `is_bank_holiday` | bool | Es feriado bancario. |
| `is_commemorative` | bool | Es día/semana/mes/año conmemorativo. |
| `is_local` | bool | Tiene alcance subnacional. |
| `is_school` | bool | Marca escolar. |
| `is_religious` / `is_civic` | bool | Carácter. |
| `is_irrenunciable` | bool | Feriado irrenunciable (no se puede renunciar al descanso). |
| `irrenunciability_category` | int\|null | Categoría 1–5. |
| `irrenunciability_category_label` | string\|null | Etiqueta textual de la categoría. |

> **Nota sobre `category`:** muchos eventos conmemorativos no traen una clasificación temática en la fuente; en esos casos `category` es `other` (no se infieren categorías no sustentadas).

## Alcance territorial

| Campo | Tipo | Descripción |
|---|---|---|
| `nationwide` | bool | Aplica a todo el país. |
| `subdivisions` | string[] | Códigos ISO 3166-2 de regiones (`CL-AP`, `CL-RM`, …). |
| `regions` | string[] | Nombres de regiones detectadas. |
| `communes` | string[] | Nombres de comunas detectadas. |
| `location_raw` | string\|null | Texto territorial original. |
| `scope_text` | string\|null | Texto territorial preservado (cuando no es nacional). |

## Fundamento legal

`legal_basis` es una lista; cada elemento:

| Campo | Tipo | Descripción |
|---|---|---|
| `type` | string\|null | `ley`, `decreto ley`, `DFL`, `decreto`, `constitución`, `resolución`, … |
| `number` | string\|null | Número de la norma. |
| `year` | string\|null | Año. |
| `title` | string\|null | Título/descripción. |
| `url` | string\|null | Enlace a la ficha oficial, si existe. |
| `role` | string\|null | Rol respecto del evento (Creación, Renombramiento, Irrenunciabilidad, …). |
| `articulo` | string\|null | Artículo citado. |
| `raw` | string | Texto original consolidado (sólo en dataset interno). |

## Definición (vista pública)

`definition` conserva descriptores factuales: `fecha_raw`, `vigencia_raw`, `ambito`, `valido_en_raw`, `caracter_raw`, `irren_text_raw`.

## Procedencia (sólo interna)

El bloque `source` (archivo, ancla, `uid`, `extraction_method`, `confidence`, `notes`, `dtstart_raw`/`dtend_raw`) existe **sólo** en el dataset interno para reproducibilidad y auditoría. `confidence` se expone también en la vista pública como campo simple.
