"""Normalización de alcance territorial: regiones, comunas e ISO 3166-2."""
import re

from .constants import ISO_REGIONS
from .normalize import clean, norm


def territory(location_raw):
    """Normaliza el alcance territorial.

    Devuelve (nationwide, scope_text, regions, communes, iso_codes).
    Conserva el texto original en scope_text; sólo asigna ISO cuando el mapeo
    es confiable (coincidencia exacta de nombre de región).
    """
    if not location_raw:
        return None, None, [], [], []
    low = norm(location_raw)
    if low in ("chile", "todo el territorio nacional", "nacional"):
        return True, None, [], [], []
    regions, iso = [], []
    for name_key, code in ISO_REGIONS.items():
        if re.search(r"\b" + re.escape(name_key) + r"\b", low):
            if code not in iso:
                iso.append(code)
                regions.append(name_key)
    communes = []
    for m in re.finditer(r"comunas?\s+de\s+([^,;]+?)(?:,|;|$)", location_raw, re.I):
        for c in re.split(r"\s+y\s+", m.group(1)):
            c = clean(c).strip()
            if c and c.lower() != "chile":
                communes.append(c)
    return False, clean(location_raw), regions, communes, iso
