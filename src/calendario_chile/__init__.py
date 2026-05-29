"""calendario-chile — dataset estructurado del calendario chileno.

Generado a partir de fuentes internas del proyecto. Cobertura 1981–2100.
"""
__version__ = "0.1.0-internal"

from .models import build_events, to_public, event_schema, holiday_schema, datapackage

__all__ = ["build_events", "to_public", "event_schema", "holiday_schema",
           "datapackage", "__version__"]
