"""Ejecuta la suite de validación sobre el dataset completo e imprime resultados.
Código de salida != 0 si algún test falla (apto para CI)."""
import _bootstrap  # noqa
import sys

from calendario_chile import build_events
from calendario_chile.validate import run_tests


def main():
    events, _ = build_events()
    results = run_tests(events)
    print("== VALIDACIÓN ==")
    ok = 0
    for name, passed, detail in results:
        print(f"  [{'OK' if passed else 'FALLA'}] {name}"
              f"{(' — ' + detail) if detail and not passed else ''}")
        ok += passed
    print(f"\n{ok}/{len(results)} tests aprobados.")
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
