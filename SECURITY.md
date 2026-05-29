# Política de Seguridad

## Alcance

Este proyecto distribuye **datos** y **scripts** de procesamiento. Los riesgos relevantes son principalmente de **integridad/calidad de datos** y de la cadena de build, más que de seguridad de aplicaciones en ejecución.

## Reportar una vulnerabilidad o un problema de integridad

- Para problemas sensibles, usa un canal **privado** (no abras un issue público con detalles explotables).
- Incluye: descripción, impacto, pasos para reproducir y, si aplica, el archivo/`id` afectado.
- Tiempo de respuesta objetivo: acuse dentro de **7 días**.

## Buenas prácticas para consumidores

- Verifica los archivos contra los esquemas en `schema/` antes de integrarlos.
- Fija una versión/etiqueta del dataset para builds reproducibles.
- No uses estos datos como única fuente para decisiones legales o financieras sin verificación oficial.

## Dependencias

El pipeline usa dependencias mínimas (ver `pyproject.toml`). Las actualizaciones de seguridad se gestionan vía PRs.
