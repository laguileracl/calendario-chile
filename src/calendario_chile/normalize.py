"""Normalización de texto, slugs, fechas y clasificación por ocurrencia."""
import re
import html
import unicodedata

from .config import RAW_HTML
from .constants import ORDINALS


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", " ", s)


def clean(s: str) -> str:
    s = html.unescape(s)
    s = strip_tags(s)
    s = s.replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip()


def norm(s: str) -> str:
    """Forma canónica para comparar: sin tildes, minúsculas, sin punto final."""
    s = clean(s).lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s)
                if unicodedata.category(c) != "Mn")
    return s.strip().rstrip(".").strip()


def slugify(s: str) -> str:
    s = norm(s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def ics_unfold(text: str) -> str:
    """RFC 5545: las líneas continuadas comienzan con espacio o tab."""
    return re.sub(r"\r?\n[ \t]", "", text)


def ics_unescape(v: str) -> str:
    return (v.replace("\\,", ",").replace("\\;", ";")
             .replace("\\n", "\n").replace("\\N", "\n").replace("\\\\", "\\")).strip()


def parse_occurrence_classification():
    """Clasificación por (fecha, ancla) desde las páginas de feriados por año.

    Devuelve dict[(date_iso, anchor)] -> flags (recurrente/singular,
    irrenunciable + categoría, religioso, local, escolar, fin de semana).
    """
    cls = {}
    for f in sorted(RAW_HTML.glob("[12][0-9][0-9][0-9]-[12][0-9][0-9][0-9].html")):
        txt = f.read_text(encoding="utf-8", errors="replace")
        for seg in re.split(r"<br\s*/?>", txt):
            md = re.search(r"(\d{2})/(\d{2})/(\d{4})", seg)
            ma = re.search(r'<a\s+class="(es\w+)"\s+href="(?:index\.html)?#([^"]+)"', seg)
            if not (md and ma):
                continue
            d, mth, y = md.groups()
            date_iso = f"{y}-{mth}-{d}"
            low = seg.lower()
            cat = None
            mc = re.search(r"irrenunciable de\s*(?:<[^>]+>)?\s*"
                           r"(primera|segunda|tercera|cuarta|quinta)\s+categor", low)
            if mc:
                cat = ORDINALS[mc.group(1)]
            cls[(date_iso, ma.group(2))] = {
                "recurrent": ma.group(1) == "esRecurrente",
                "singular": ma.group(1) == "esSingular",
                "is_irrenunciable": "esirrenunciable" in low,
                "irren_category": cat,
                "is_religious": "esreligioso" in low,
                "is_local": "eslocal" in low,
                "is_school": "esescolar" in low,
                "weekend": "findesemana" in low,
                "source_file": f.name,
            }
    return cls
