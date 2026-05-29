# Roadmap

## Fase 0 — Extracción privada y validación ✅
- Pipeline reproducible desde fuentes internas.
- Dataset canónico completo (1981–2100), validado (cobertura y consistencia).
- Separación datos públicos / internos / pipeline.

## Fase 1 — MVP: feriados públicos + bancarios
- Release liviano de feriados (`public`, `bank`, `local`, `restricted`) en JSON/CSV/ICS.
- Esquema estable y documentado; datapackage.
- Revisión de registros `low-confidence` y feriados sin fundamento legal.
- Licencia definida: **MIT** (código, documentación, datasets públicos y derivados). ✅

## Fase 2 — Conmemorativos, locales y fundamento legal ampliado
- Incorporar la capa conmemorativa al release público.
- Enriquecer alcance territorial (comunas → identificadores) y `category` temática curada.
- Ampliar y verificar el fundamento legal.

## Fase 3 — API estática, visor web y paquetes
- Publicar API estática por año (índices `hoy`/`próximos`).
- Visor web (consulta por año/región/tipo).
- Paquetes para desarrolladores (PyPI / npm).

## Fase 4 — Contribuciones externas y automatización
- Guía de contribución y *issues* curados.
- CI que regenera y valida periódicamente, abriendo PRs ante cambios.
- Versionado semántico del dataset y del esquema.
