"""Genera la API estática (data/api/v1/) con la vista pública de TODOS los
eventos por año, más índices hoy/próximos."""
import _bootstrap  # noqa

from calendario_chile import build_events, to_public
from calendario_chile.api import build_static
from calendario_chile.config import ensure_dirs


def main():
    ensure_dirs()
    events, _ = build_events()
    pub = [to_public(e) for e in events]
    stats = build_static(pub)
    print(f"[build_api] {len(pub)} eventos públicos -> data/api/v1/")
    print(f"  years: {stats['years']} | hoy: {stats['today']} | próximos: {stats['upcoming']}")


if __name__ == "__main__":
    main()
