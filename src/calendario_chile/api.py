"""Generación de la API estática (JSON sin servidor) para GitHub Pages."""
import json
from collections import defaultdict

from .config import API, API_YEARS, TODAY


def _w(path, data, compact=False):
    if compact:
        txt = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    else:
        txt = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(txt, encoding="utf-8")


def build_static(public_events, today=TODAY):
    """Genera data/api/v1/: index.json, years/{YYYY}.json, hoy.json, proximos.json."""
    API_YEARS.mkdir(parents=True, exist_ok=True)
    by_year = defaultdict(list)
    for e in public_events:
        by_year[e["year"]].append(e)

    years = sorted(by_year)
    for y in years:
        _w(API_YEARS / f"{y}.json", by_year[y], compact=True)  # API: compacto

    from collections import Counter
    by_type = dict(Counter(e["type"] for e in public_events))

    _w(API / "index.json", {
        "name": "calendario-chile API (estática)",
        "version": "v1",
        "coverage": {"year_min": years[0], "year_max": years[-1]},
        "total_events": len(public_events),
        "generated_for": today,
        "license": "MIT",
        "license_url": "https://opensource.org/license/mit",
        "endpoints": {
            "index": "v1/index.json",
            "metadata": "v1/metadata.json",
            "year": "v1/years/{YYYY}.json",
            "today": "v1/hoy.json",
            "upcoming": "v1/proximos.json",
        },
    })

    _w(API / "metadata.json", {
        "name": "calendario-chile",
        "api_version": "v1",
        "dataset_version": "0.1.0-rc1",
        "generated_for": today,
        "coverage": {"year_min": years[0], "year_max": years[-1],
                     "years": len(years)},
        "total_events": len(public_events),
        "by_type": by_type,
        "license": "MIT",
        "license_url": "https://opensource.org/license/mit",
        "endpoints": {
            "index": "v1/index.json", "metadata": "v1/metadata.json",
            "year": "v1/years/{YYYY}.json", "today": "v1/hoy.json",
            "upcoming": "v1/proximos.json",
        },
        "notes": ("Dataset generado a partir de fuentes internas del proyecto. "
                  "No constituye asesoría legal."),
    })

    today_evs = [e for e in public_events
                 if e["start_date"] <= today <= e["end_date"]]
    _w(API / "hoy.json", {"date": today, "events": today_evs})

    upcoming = sorted((e for e in public_events if e["start_date"] >= today),
                      key=lambda e: e["start_date"])[:50]
    _w(API / "proximos.json", {"from": today, "count": len(upcoming),
                               "events": upcoming})
    return {"years": len(years), "today": len(today_evs), "upcoming": len(upcoming)}
