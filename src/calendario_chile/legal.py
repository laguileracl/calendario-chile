"""Fundamento legal: parsing del catálogo de normas, de las definiciones de
eventos (con su normativa relevante) y resolución de referencias legales."""
import re

from .config import RAW_HTML
from .constants import ORDINALS
from .normalize import clean, norm

FIELD_LABELS = ["Fecha:", "Vigencia:", "Válido en:", "Ámbito:", "Carácter:",
                "Carácter :", "Normativa relevante:", "Notas:", "Notas :"]


# --------------------------------------------------------------------------
# Catálogo de normas
# --------------------------------------------------------------------------
def _type_number_year(name, anchor, pub_dates):
    t = name.lower()
    if "d.f.l" in t or t.startswith("dfl") or "decreto con fuerza de ley" in t:
        typ = "DFL"
    elif "decreto ley" in t:
        typ = "decreto ley"
    elif t.startswith("decreto") or "decreto supremo" in t:
        typ = "decreto"
    elif t.startswith("ley"):
        typ = "ley"
    elif "constituci" in t:
        typ = "constitución"
    elif "reglamento" in t:
        typ = "reglamento"
    elif "resoluci" in t:
        typ = "resolución"
    elif "circular" in t:
        typ = "circular"
    elif "acuerdo" in t:
        typ = "acuerdo"
    else:
        typ = "otro"
    num = None
    pats = {"ley": r"ley\s+([\d.]+)", "decreto ley": r"decreto ley\s+([\d.]+)",
            "DFL": r"d\.?\s*f\.?\s*l\.?\s*(\d+)",
            "decreto": r"decreto(?:\s+supremo)?\s+(\d+)"}
    if typ in pats:
        m = re.search(pats[typ], t)
        if m:
            num = m.group(1)
    m = re.search(r"_(\d{4})(?:_|$)", anchor) or re.search(r"\bde\s+(\d{4})\b", name)
    yr = m.group(1) if m else (pub_dates[-1].split("/")[-1] if pub_dates else None)
    return typ, num, yr


def parse_norms():
    txt = (RAW_HTML / "normas.html").read_text(encoding="utf-8", errors="replace")
    anchors = [(m.group(1), m.start())
               for m in re.finditer(r'<[^>]*\bid="([^"]+)"[^>]*>', txt)]
    norms = {}
    for i, (anc, pos) in enumerate(anchors):
        end = anchors[i + 1][1] if i + 1 < len(anchors) else len(txt)
        flat = clean(txt[pos:end])
        mdate = re.search(r"\d{2}/\d{2}/\d{4}", flat)
        name = (flat[:mdate.start()] if mdate else flat[:80]).strip().rstrip(".").strip()
        dates = re.findall(r"\d{2}/\d{2}/\d{4}", flat)
        title = None
        if dates:
            after = flat.split(dates[-1], 1)[-1].strip()
            title = (after.split(".")[0].strip() or None)
            if title:
                title = title[:300]
        mu = re.search(r'href="(https?://[^"]*bcn\.cl[^"]*)"', txt[pos:end])
        url = mu.group(1).replace("&amp;", "&") if mu else None
        typ, num, yr = _type_number_year(name, anc, dates[:2])
        norms[anc] = {"anchor": anc, "type": typ, "number": num, "year": yr,
                      "title": title, "url": url, "name": name,
                      "raw": name + ((" — " + title) if title else ""),
                      "pub_dates": dates[:2]}
    return norms


# --------------------------------------------------------------------------
# Definiciones de eventos
# --------------------------------------------------------------------------
def _field(flat, label, nexts):
    i = flat.find(label)
    if i < 0:
        return None
    start = i + len(label)
    end = len(flat)
    for nl in nexts:
        j = flat.find(nl, start)
        if 0 <= j < end:
            end = j
    return flat[start:end].strip().strip(".").strip() or None


def parse_irren_ranges(text):
    if not text:
        return []
    low = text.lower()
    if "no es irrenunciable" in low and "categor" not in low:
        return [{"cat": None, "label": None, "y_from": None, "y_to": None,
                 "raw": "No es irrenunciable", "irren": False}]
    out = []
    for m in re.finditer(
            r"(primera|segunda|tercera|cuarta|quinta)\s+categor[íi]a"
            r"\s*(entre\s+(\d{4})\s+y\s+(\d{4})|desde\s+(?:el\s+)?(\d{4})|"
            r"hasta\s+(?:el\s+)?(\d{4}))?", low):
        yf = yt = None
        if m.group(3):
            yf, yt = int(m.group(3)), int(m.group(4))
        elif m.group(5):
            yf = int(m.group(5))
        elif m.group(6):
            yt = int(m.group(6))
        out.append({"cat": ORDINALS[m.group(1)], "label": m.group(1) + " categoría",
                    "y_from": yf, "y_to": yt, "raw": m.group(0), "irren": True})
    return out


def _legal_refs(block):
    i = block.find("Normativa relevante")
    seg = block[i:] if i >= 0 else block
    refs = []
    for li in re.split(r"<li>", seg)[1:]:
        m = re.search(r'href="normas\.html#([^"]+)"', li)
        if not m:
            continue
        role = clean(li.split("<a")[0]).rstrip(":").strip() or None
        art = re.search(r'class="articulo">\s*(\[[^<]+\])', li)
        refs.append({"role": role, "norma_anchor": m.group(1),
                     "articulo": clean(art.group(1)) if art else None})
    return refs


def _caracter(flat):
    c = _field(flat, "Carácter:", FIELD_LABELS) or _field(flat, "Carácter :", FIELD_LABELS)
    is_rel = is_civ = False
    if c:
        cl = c.lower()
        is_rel = "religios" in cl
        is_civ = ("civil" in cl) or ("civic" in cl) or ("cívic" in cl)
    if not c and "feriado religioso" in flat.lower():
        is_rel = True
    return c, is_rel, is_civ


def parse_definitions():
    defs, name_index = {}, {}
    for fname in ["index.html", "DiasNacionales.html"]:
        txt = (RAW_HTML / fname).read_text(encoding="utf-8", errors="replace")
        heads = [m.start() for m in re.finditer(r'<h[1-6]\b', txt)]
        for i, pos in enumerate(heads):
            end = heads[i + 1] if i + 1 < len(heads) else len(txt)
            block = txt[pos:end]
            head_tag = re.match(r'<h[1-6]\b[^>]*>', block)
            mid = re.search(r'\bid="([^"]+)"', head_tag.group(0) if head_tag else "")
            if not mid:
                continue
            anc = mid.group(1)
            alias = re.findall(r'\bid="([^"]+)"', block)
            mh = re.search(r"<h[1-6][^>]*>(.*?)</h[1-6]>", block, re.S)
            head_text = mh.group(1) if mh else ""
            old_names = re.findall(r'class="feriadoRenombrado"[^>]*>(.*?)</span>',
                                   head_text, re.S)
            primary = clean(re.sub(r'<span class="feriadoRenombrado".*?</span>', " ",
                                   head_text, flags=re.S)).rstrip(".").strip() or None
            names = ([primary] if primary else []) + \
                    [clean(o).rstrip(".").strip() for o in old_names if clean(o)]
            flat = clean(block)
            ambito = _field(flat, "Ámbito:", FIELD_LABELS)
            if ambito:
                w = re.split(r"[.\s]", ambito.strip(), 1)[0].lower()
                ambito = w if w in ("normal", "restringido") else None
            mi = re.search(r"((?:Es|No es) irrenunciable[^.]*\.)", flat)
            irren_txt = mi.group(1) if mi else None
            fecha = _field(flat, "Fecha:", FIELD_LABELS)
            vigencia = _field(flat, "Vigencia:", FIELD_LABELS)
            valido = _field(flat, "Válido en:", FIELD_LABELS)
            caracter, is_rel, is_civ = _caracter(flat)
            d = {"anchor": anc, "source_file": fname, "names": names, "name": primary,
                 "fecha_raw": fecha, "movable": bool(fecha and "móvil" in fecha.lower()),
                 "vigencia_raw": vigencia, "valido_en_raw": valido,
                 "nationwide": bool(valido and "todo el territorio" in valido.lower()),
                 "ambito": ambito, "irren_text": irren_txt,
                 "irren_tramos": parse_irren_ranges(irren_txt),
                 "caracter": caracter, "is_religious": is_rel, "is_civic": is_civ,
                 "legal_refs": _legal_refs(block),
                 "is_definition": bool(fecha or vigencia or irren_txt)}
            for a in dict.fromkeys([anc] + alias):
                defs.setdefault(a, d)
            for nm in names:
                k = norm(nm)
                if k and k not in name_index:
                    name_index[k] = anc
    return defs, name_index


def resolve_legal(legal_refs, norms):
    out = []
    for ref in legal_refs:
        n = norms.get(ref["norma_anchor"])
        if not n:
            out.append({"type": None, "number": None, "year": None, "title": None,
                        "url": None, "raw": ref.get("norma_anchor"),
                        "role": ref.get("role"), "articulo": ref.get("articulo"),
                        "norma_anchor": ref["norma_anchor"]})
            continue
        out.append({"type": n["type"], "number": n["number"], "year": n["year"],
                    "title": n["title"], "url": n["url"],
                    "raw": n["raw"] + (" " + ref["articulo"] if ref.get("articulo") else ""),
                    "role": ref.get("role"), "articulo": ref.get("articulo"),
                    "norma_anchor": ref["norma_anchor"]})
    return out
