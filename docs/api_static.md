# API estática

Una **API sin servidor**: archivos JSON servibles directamente (p. ej. GitHub Pages o cualquier CDN). No requiere backend.

## Endpoints

| Ruta | Contenido |
|---|---|
| `data/api/v1/index.json` | Metadatos: cobertura, total, endpoints. |
| `data/api/v1/years/{YYYY}.json` | Todos los eventos del año `YYYY`. |
| `data/api/v1/hoy.json` | Eventos vigentes en la fecha de referencia. |
| `data/api/v1/proximos.json` | Próximos 50 eventos desde la fecha de referencia. |

## Ejemplo de consumo

```bash
# Eventos de 2025
curl -s https://<host>/v1/years/2025.json | jq '.[].name.es'

# ¿Qué se conmemora/feria hoy?
curl -s https://<host>/v1/hoy.json | jq '.events[].name.es'
```

```js
const res = await fetch("https://<host>/v1/years/2025.json");
const eventos = await res.json();
const feriados = eventos.filter(e => e.type === "public");
```

## Notas

- `hoy.json` y `proximos.json` se calculan respecto de una **fecha de referencia** fija al generar (configurable en `src/calendario_chile/config.py`, `TODAY`). En automatización (CI) se regeneran periódicamente.
- Los archivos por año contienen la **vista pública** (sin procedencia interna).
