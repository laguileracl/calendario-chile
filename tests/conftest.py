"""Fixtures para los tests del repo público: cargan los datos INCLUIDOS
(muestra + API estática), sin requerir las fuentes internas."""
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pytest


def _load():
    recs = []
    sample = ROOT / "data" / "public" / "SAMPLE.json"
    if sample.exists():
        recs += json.loads(sample.read_text(encoding="utf-8"))
    for f in sorted((ROOT / "data" / "api" / "v1" / "years").glob("*.json")):
        recs += json.loads(f.read_text(encoding="utf-8"))
    return recs


@pytest.fixture(scope="session")
def records():
    return _load()
