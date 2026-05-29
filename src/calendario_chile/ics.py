"""Lectura y generación de iCalendar (RFC 5545)."""
import re
from datetime import date, timedelta

from .config import RAW_ICS
from .constants import ICS_MAP, WEEKDAYS_EN
from .normalize import clean, ics_unfold, ics_unescape


def parse_ics_events():
    """Lee los calendarios de origen -> eventos base con trazabilidad RFC 5545.

    DTEND en eventos VALUE=DATE es EXCLUSIVO: end_date = DTEND - 1 día.
    """
    events = []
    for path in sorted(RAW_ICS.glob("*.ics")):
        cal_group, default_type = ICS_MAP[path.name]
        raw = ics_unfold(path.read_text(encoding="utf-8", errors="replace"))
        mcn = re.search(r"X-WR-CALNAME:(.+)", raw)
        calname = ics_unescape(mcn.group(1)) if mcn else None
        for block in re.findall(r"BEGIN:VEVENT(.*?)END:VEVENT", raw, re.S):
            def prop(name):
                m = re.search(rf"^{name}[^:\r\n]*:(.+)$", block, re.M)
                return m.group(1).strip() if m else None
            dtstart_raw, dtend_raw = prop("DTSTART"), prop("DTEND")
            ms = re.search(r"(\d{8})", dtstart_raw or "")
            if not ms:
                continue
            g = ms.group(1)
            sd = date(int(g[:4]), int(g[4:6]), int(g[6:]))
            if dtend_raw and re.search(r"(\d{8})", dtend_raw):
                de = re.search(r"(\d{8})", dtend_raw).group(1)
                ed_excl = date(int(de[:4]), int(de[4:6]), int(de[6:]))
                duration = (ed_excl - sd).days
                end_incl = ed_excl - timedelta(days=1)
            else:
                duration, end_incl = 1, sd
            if duration < 1:
                duration, end_incl = 1, sd
            summary = ics_unescape(prop("SUMMARY") or "")
            url = prop("URL")
            anchor = url.split("#", 1)[1].strip() if (url and "#" in url) else None
            location = prop("LOCATION")
            events.append({
                "summary_original": summary,
                "name_es": clean(summary).rstrip(".").strip(),
                "start_date": sd, "end_date": end_incl,
                "duration_days": duration, "is_multiday": duration > 1,
                "year": sd.year, "weekday": WEEKDAYS_EN[sd.weekday()],
                "source_anchor": anchor,
                "source_url": (url.split("#")[0] + "#" + anchor) if anchor else url,
                "location_raw": ics_unescape(location) if location else None,
                "calendar_group": cal_group, "source_calendar": calname,
                "source_file": f"data/internal/raw/ics/{path.name}",
                "default_type": default_type,
                "dtstart_raw": dtstart_raw, "dtend_raw": dtend_raw,
                "uid": prop("UID"), "last_modified": prop("LAST-MODIFIED"),
            })
    return events


# --------------------------------------------------------------------------
# Generación de iCalendar a partir del dataset canónico
# --------------------------------------------------------------------------
def _esc(s):
    return (s or "").replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")


def _fold(line):
    out, b = [], line.encode("utf-8")
    while len(b) > 73:
        out.append(b[:73].decode("utf-8", "ignore"))
        b = b" " + b[73:]
    out.append(b.decode("utf-8", "ignore"))
    return "\r\n".join(out)


def write_ics(events, path, calname, dtstamp="20260529T000000Z"):
    """Genera un archivo .ics a partir de registros canónicos."""
    L = ["BEGIN:VCALENDAR", "VERSION:2.0",
         "PRODID:-//calendario-chile//ES", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
         _fold(f"X-WR-CALNAME:{_esc(calname)}"), "X-WR-TIMEZONE:America/Santiago"]
    for e in events:
        sd = e["start_date"].replace("-", "")
        ed = (date.fromisoformat(e["end_date"]) + timedelta(days=1)).strftime("%Y%m%d")
        L += ["BEGIN:VEVENT",
              f"UID:{e['id']}@calendario-chile",
              f"DTSTAMP:{dtstamp}",
              f"DTSTART;VALUE=DATE:{sd}",
              f"DTEND;VALUE=DATE:{ed}",
              _fold(f"SUMMARY:{_esc(e['name']['es'])}"),
              "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT"]
    L.append("END:VCALENDAR")
    path.write_text("\r\n".join(L) + "\r\n", encoding="utf-8")
    return len(events)
