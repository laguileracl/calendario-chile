# Estrategia de distribución

Evaluación de opciones para distribuir `calendario-chile` manteniendo el repo manejable, los datos accesibles y la trazabilidad interna privada. **Nada está publicado aún.**

## Restricción de fondo

El dataset completo pesa cientos de MB y los derivados públicos ~85 MB; la API por año ~83 MB. Versionar todo el bulk en git infla el repositorio y degrada `clone`/`fetch`. La estrategia debe separar **pipeline + muestra** (en repo) de **datos completos** (distribución específica).

## A. Repo liviano

- **Contenido:** código, docs, schema, reports, `SAMPLE.json`, índices API y API de **años recientes** (p. ej. 2024–2027).
- **Ventajas:** clon rápido; foco en código y contrato; navegable.
- **Desventajas:** los datos completos no están en el repo (hay que ir a Release/Pages).
- **Veredicto:** **base recomendada.**

## B. Repo liviano + GitHub Releases

- **Contenido extra:** datasets completos comprimidos (`.zip`/`.tar.gz`) adjuntos a cada tag (`v0.1.0`).
- **Ventajas:** versionado inmutable por release; sin inflar git; ideal para descargas puntuales.
- **Desventajas:** no apto para consumo programático "en vivo" (hay que descargar y descomprimir).
- **Veredicto:** **recomendado** para los datasets completos (JSON/CSV/SQLite/Parquet).

## C. Repo + Git LFS

- **Ventajas:** archivos grandes versionados con punteros; transparente para el usuario.
- **Desventajas:** cuotas de almacenamiento/ancho de banda de LFS (costo); fricción en forks; `clone` sigue descargando objetos LFS.
- **Veredicto:** **no recomendado** para Fase 1. Datos regenerables + Releases cubren el caso sin costo de LFS. Reconsiderar sólo si se exige historial versionado de los datos dentro del repo.

## D. GitHub Pages

- **Contenido:** API estática (`data/api/v1/`): `index.json`, `metadata.json`, `years/{YYYY}.json`, `hoy.json`, `proximos.json`, y `.ics` para suscripción.
- **Ventajas:** consumo programático directo por URL; costo cero; cacheable por CDN.
- **Límites prácticos:** sitio recomendado < 1 GB y archivos individuales razonables; nuestra API (~83 MB) está holgadamente dentro. Construir y desplegar Pages desde CI.
- **Veredicto:** **recomendado** para la API estática y los `.ics`.

## E. Repositorio de datos externo (Zenodo / Hugging Face Datasets / data registry)

- **Zenodo:** DOI citable, ideal para *snapshots* académicos/versionados; bueno para reproducibilidad.
- **Hugging Face Datasets:** excelente DX para data science (carga directa, *viewer*, Parquet).
- **data.gov-like / registries:** mayor descubribilidad institucional.
- **Veredicto (conceptual):** **valioso a futuro** (Fase 3), no requerido para Fase 1. Un DOI de Zenodo por release aporta citabilidad con bajo esfuerzo.

## Recomendación para Fase 1

**Combinar A + B + D:**

1. **Repo liviano (A):** pipeline, docs, schema, reports, `SAMPLE.json`, índices API y años recientes.
2. **GitHub Pages (D):** desplegar la API estática completa (`data/api/v1/`) y los `.ics` desde CI.
3. **GitHub Releases (B):** adjuntar los datasets completos comprimidos al tag de versión.

Mantener **todo `data/internal/` privado**. Evaluar **Zenodo (E)** para un DOI citable cuando se publique `v0.1.0` estable.

### Implicancias operativas

- `.gitignore` ya excluye el bulk regenerable; el repo queda liviano por defecto.
- El workflow `build.yml` puede generar artefactos y, en una iteración futura, desplegar Pages y crear el Release.
- `hoy.json`/`proximos.json` requieren regeneración periódica (fecha de referencia) vía CI.
