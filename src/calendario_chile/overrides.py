"""
Curación manual de fundamento legal, verificada contra fuente oficial.

Sólo se aplica a eventos específicos (por `id` exacto) en los que la fuente
interna no traía ancla y, por tanto, el pipeline no pudo mapear su normativa,
pero cuyo fundamento legal está claramente establecido por normas generales ya
presentes en el catálogo (con URL oficial de BCN/LeyChile).

NO inventa normas: reutiliza entradas del catálogo de normas del propio
proyecto (mismas URLs oficiales que el pipeline usa para plebiscitos análogos,
p. ej. el plebiscito nacional de 2023 y los plebiscitos comunales irrenunciables).

Fundamento aplicado a los plebiscitos nacionales 2020 y 2022:
  - Feriado legal del día de plebiscito  -> Ley 18.700 (LOC sobre Votaciones
    Populares y Escrutinios), art. 169 (hoy art. 180).
  - Irrenunciabilidad de SEGUNDA categoría -> Ley 19.973 (2004), que convierte
    los feriados por elecciones o plebiscitos en irrenunciables de 2.ª categoría.
Verificado: Dirección del Trabajo y catálogo interno (BCN/LeyChile). El
plebiscito del 4-09-2022 fue feriado irrenunciable de segunda categoría a nivel
nacional. Ver reports/PLEBISCITES_LEGAL_BASIS_PATCH.md.
"""

# Roles de las normas generales aplicables a un feriado por plebiscito nacional.
_PLEBISCITE_REFS = [
    {"norma_anchor": "ley_18700",
     "role": "Feriado legal del día de plebiscito (art. 169, hoy art. 180)",
     "articulo": "[art. 169]"},
    {"norma_anchor": "ley_19973",
     "role": "Irrenunciabilidad de segunda categoría",
     "articulo": None},
]

_NOTE = ("fundamento legal curado manualmente y verificado contra fuente oficial "
         "(BCN/LeyChile; Dirección del Trabajo). Mismas normas generales que el "
         "pipeline aplica a plebiscitos nacionales análogos. Ver "
         "reports/PLEBISCITES_LEGAL_BASIS_PATCH.md")

# Clave = id exacto del evento. Valor = parámetros de irrenunciabilidad.
OVERRIDES = {
    "cl-2020-10-25-plebiscito-nacional-aprobacion-o-rechazo-de-la-elaboracion-"
    "de-una-nueva-constitucion-y-eleccion-del-tipo-de-organo-a-cargo-de-ello-"
    "irrenunciable": {
        "legal_refs": _PLEBISCITE_REFS,
        "is_irrenunciable": True,
        "irrenunciability_category": 2,
    },
    "cl-2022-09-04-plebiscito-nacional-aprobacion-o-rechazo-de-la-constitucion-"
    "propuesta-por-la-convencion-constituyente-irrenunciable": {
        "legal_refs": _PLEBISCITE_REFS,
        "is_irrenunciable": True,
        "irrenunciability_category": 2,
    },
}


def apply_override(rec, norms, resolve_legal):
    """Aplica curación al registro `rec` (mutándolo) si su id está en OVERRIDES.

    Devuelve True si se aplicó. `resolve_legal(refs, norms)` se inyecta para
    construir los objetos de `legal_basis` reutilizando el catálogo de normas.
    """
    ov = OVERRIDES.get(rec["id"])
    if not ov:
        return False
    legal = resolve_legal(ov["legal_refs"], norms)
    rec["legal_basis"] = [
        {"type": l["type"], "number": l["number"], "year": l["year"],
         "title": l["title"], "url": l["url"], "raw": l["raw"],
         "role": l["role"], "articulo": l["articulo"],
         "norma_anchor": l["norma_anchor"]} for l in legal
    ]
    rec["is_irrenunciable"] = ov["is_irrenunciable"]
    rec["irrenunciability_category"] = ov["irrenunciability_category"]
    if ov["irrenunciability_category"]:
        labels = {1: "primera", 2: "segunda", 3: "tercera", 4: "cuarta", 5: "quinta"}
        rec["irrenunciability_category_label"] = (
            labels[ov["irrenunciability_category"]] + " categoría")
    src = rec["source"]
    if "legal_mapping" not in src["extraction_method"]:
        src["extraction_method"].append("legal_mapping")
    src["extraction_method"].append("manual_curation")
    src["confidence"] = "high"
    src["notes"].append(_NOTE)
    return True
