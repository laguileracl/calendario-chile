"""Enums, vocabularios controlados y mapas de referencia."""

# --- Vocabulario de tipos y categorías ---
TYPE_ENUM = {"public", "bank", "commemorative", "local", "school",
             "restricted", "other"}
CATEGORY_ENUM = {"civic", "religious", "legal", "cultural", "educational",
                 "labor", "environmental", "health", "financial", "other"}

WEEKDAYS_EN = ["monday", "tuesday", "wednesday", "thursday", "friday",
               "saturday", "sunday"]

ORDINALS = {"primera": 1, "segunda": 2, "tercera": 3, "cuarta": 4, "quinta": 5}

# --- Agrupaciones de calendarios de origen ---
FERIADO_GROUPS = {"feriados ámbito normal", "feriados ámbito restringido",
                  "feriados locales ámbito normal"}
COMM_GROUPS = {"días nacionales", "días nacionales no oficiales",
               "semanas/meses/años nacionales", "días locales"}
LOCAL_GROUPS = {"feriados locales ámbito normal", "días locales"}

# Mapeo de archivo de calendario de origen -> (grupo, tipo por defecto)
ICS_MAP = {
    "feriados-ambito-normal.ics":        ("feriados ámbito normal", "public"),
    "feriados-bancarios.ics":            ("feriados bancarios", "bank"),
    "feriados-ambito-restringido.ics":   ("feriados ámbito restringido", "restricted"),
    "feriados-locales-ambito-normal.ics": ("feriados locales ámbito normal", "local"),
    "dias-locales.ics":                  ("días locales", "local"),
    "dias-nacionales.ics":               ("días nacionales", "commemorative"),
    "dias-nacionales-no-oficiales.ics":  ("días nacionales no oficiales", "commemorative"),
    "semanas-meses-anios-nacionales.ics": ("semanas/meses/años nacionales", "commemorative"),
}

# --- ISO 3166-2 de las regiones de Chile ---
ISO_REGIONS = {
    "arica y parinacota": "CL-AP",
    "tarapaca": "CL-TA",
    "antofagasta": "CL-AN",
    "atacama": "CL-AT",
    "coquimbo": "CL-CO",
    "valparaiso": "CL-VS",
    "metropolitana de santiago": "CL-RM",
    "metropolitana": "CL-RM",
    "libertador general bernardo o'higgins": "CL-LI",
    "libertador general bernardo ohiggins": "CL-LI",
    "o'higgins": "CL-LI",
    "ohiggins": "CL-LI",
    "maule": "CL-ML",
    "nuble": "CL-NB",
    "biobio": "CL-BI",
    "la araucania": "CL-AR",
    "araucania": "CL-AR",
    "los rios": "CL-LR",
    "los lagos": "CL-LL",
    "aysen": "CL-AI",
    "aysen del general carlos ibanez del campo": "CL-AI",
    "magallanes y de la antartica chilena": "CL-MA",
    "magallanes": "CL-MA",
}
VALID_ISO = set(ISO_REGIONS.values())

ISO_REGION_NAMES = {
    "CL-AP": "Arica y Parinacota", "CL-TA": "Tarapacá", "CL-AN": "Antofagasta",
    "CL-AT": "Atacama", "CL-CO": "Coquimbo", "CL-VS": "Valparaíso",
    "CL-RM": "Metropolitana de Santiago", "CL-LI": "O'Higgins", "CL-ML": "Maule",
    "CL-NB": "Ñuble", "CL-BI": "Biobío", "CL-AR": "La Araucanía",
    "CL-LR": "Los Ríos", "CL-LL": "Los Lagos", "CL-AI": "Aysén",
    "CL-MA": "Magallanes y de la Antártica Chilena",
}
