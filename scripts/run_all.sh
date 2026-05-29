#!/usr/bin/env bash
# Pipeline completo de calendario-chile. Regenera datos internos, release público,
# API estática, ICS, validación y reportes. No publica nada.
set -euo pipefail
cd "$(dirname "$0")"

echo "==> 1/8  Dataset completo interno + esquemas (build_dataset.py)"
python3 build_dataset.py
echo "==> 2/8  Release público MVP (build_mvp.py)"
python3 build_mvp.py
echo "==> 3/8  API estática (build_api.py)"
python3 build_api.py
echo "==> 4/8  iCalendar (build_ics.py)"
python3 build_ics.py
echo "==> 5/8  Validación (validate_dataset.py)"
python3 validate_dataset.py
echo "==> 6/8  Reporte de calidad (quality_report.py)"
python3 quality_report.py
echo "==> 7/8  Inventario de fuentes (source_inventory.py)"
python3 source_inventory.py
echo "==> 8/8  Verificación de release público (clean_public_release.py)"
python3 clean_public_release.py

echo "==> Listo."
