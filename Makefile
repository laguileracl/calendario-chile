.PHONY: install validate test clean-check build api ics help

PY ?= python3
S := scripts

help:
	@echo "calendario-chile — targets:"
	@echo "  make install      Instala el paquete (editable)"
	@echo "  make validate     Valida los datos incluidos (muestra + API)"
	@echo "  make test         Tests (pytest) sobre los datos incluidos"
	@echo "  make clean-check  Verifica que el repo no exponga material interno/terceros"
	@echo "  make build        (requiere fuentes internas o artefactos de release)"

install:
	$(PY) -m pip install -e ".[dev]"

validate:      ## Valida la superficie pública incluida (no requiere fuentes)
	$(PY) $(S)/validate_public.py

test:          ## Tests sobre los datos incluidos
	$(PY) -m pytest -q tests/

clean-check:   ## Verificación anti-contaminación del repo público
	$(PY) $(S)/public_clean_check.py

build:         ## Regenera el dataset COMPLETO (requiere insumos no incluidos)
	@echo "El dataset completo se regenera desde las fuentes internas del proyecto,"
	@echo "que NO se incluyen en este repositorio público (ver docs/downloads.md)."
	@echo "Con esos insumos: $(PY) $(S)/build_dataset.py  (y build_mvp/build_api/build_ics)."
	@echo "Alternativa: descargar los artefactos de la GitHub Release v0.1.0."

api:           ## (requiere dataset completo) regenera la API estática
	$(PY) $(S)/build_api.py

ics:           ## (requiere dataset completo) regenera los .ics
	$(PY) $(S)/build_ics.py
