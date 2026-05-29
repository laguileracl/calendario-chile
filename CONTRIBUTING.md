# Contributing

¡Gracias por tu interés en contribuir a **calendario-chile**!

> Estado: pre-release. La estructura puede cambiar antes de la Fase 1.

## Entorno

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Flujo

1. Crea una rama desde `main`.
2. Haz tus cambios con commits claros (estilo *Conventional Commits*: `feat:`, `fix:`, `docs:`…).
3. Asegura que pasa todo:
   ```bash
   make validate
   make test
   make clean-check
   ```
4. Si tu cambio afecta los datos, regenera y revisa el reporte:
   ```bash
   make all
   ```
5. Abre un Pull Request describiendo el cambio y su impacto en el dataset/esquema.

## Reglas de datos

- **No inventar:** lo ausente en la fuente queda `null` o lista vacía.
- **Preservar el texto original** (`*_raw`) además del valor normalizado.
- **No introducir** referencias a fuentes o terceros externos en artefactos públicos (`make clean-check` lo verifica).
- Cambios incompatibles de esquema → actualizar versión y `CHANGELOG.md`.

## Estilo de código

- Python ≥ 3.10, líneas ≤ 100 columnas.
- Módulos pequeños y con responsabilidad única (ver `src/calendario_chile/`).

## Reporte de problemas

Usa *issues* con: descripción, datos esperados vs obtenidos, año/tipo afectado y, si aplica, el `id` del evento.
