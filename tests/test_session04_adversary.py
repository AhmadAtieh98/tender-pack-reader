"""Mutations from the independent adversarial review of the session 04 repairs (a separate reviewer agent,
scripts kept in the session log). Each mutation changes what a unit says or where it points; the full coverage
report (C01-C10) must fail. Written from the reviewer's reproductions BEFORE the second round of fixes.
Applied to deep copies in memory; nothing is written to the repository.
"""
from __future__ import annotations

import copy

import pytest

from tenderpack.coverage import coverage_report
from tenderpack.textnorm import normalize_latin

ATTACKS, CONTROLS, RATTACKS, RCONTROLS = [], [], [], []


def attack(name, doc_id, units):
    def deco(fn):
        ATTACKS.append(pytest.param(doc_id, fn, id=name.split(" ")[0]))
        return fn
    return deco


def control(name, doc_id, units):
    def deco(fn):
        CONTROLS.append(pytest.param(doc_id, fn, id=name.split(" ")[0]))
        return fn
    return deco


def rattack(name):
    def deco(fn):
        RATTACKS.append(pytest.param(fn, id=name.split(" ")[0]))
        return fn
    return deco


def rcontrol(name):
    def deco(fn):
        RCONTROLS.append(pytest.param(fn, id=name.split(" ")[0]))
        return fn
    return deco


def spans_of(d):
    return {s.span_id: s for p in d.pages for s in p.content}


def rebox(d, a):
    sp = spans_of(d)
    ss = [sp[x] for x in a["spans"]]
    a["bbox"] = [min(s.x0 for s in ss), min(s.y0 for s in ss), max(s.x1 for s in ss), max(s.y1 for s in ss)]


def row_text(u, cols):
    return " | ".join(f"{c}: {u.cells[c]}" for c in cols if c in u.cells and u.cells[c])


def _reading_units(pack):
    ru = {}
    for u in pack["units"]:
        if u.get("origin") == "image_reading":
            ru.setdefault(u["region"], []).append(copy.deepcopy(u))
    return ru


def _failing(pack, doc_id=None, mutate=None, rmutate=None) -> list[str]:
    p = copy.deepcopy(pack["pack"])
    if mutate:
        mutate(next(d for d in p.docs if d.doc.doc_id == doc_id))
    ru = _reading_units(pack)
    if rmutate:
        rmutate(ru)
    cov = coverage_report(p, pack["packets"], ru, [], pack["evidence"], pack.get("reading_sources"))
    return [c["id"] for c in cov["checks"] if not c["ok"]]


def by_id(ru, uid):
    return next(u for us in ru.values() for u in us if u["unit_id"] == uid)



# ============================================================== text-layer attacks (reviewer's)
# ---------------------------------------------------------------- tables: header / columns
@attack("T1 header names permuted (Criterion<->Value) and every row re-keyed by position", "VOL-II",
        ["VOL-II:T2-6"] + [f"VOL-II:T2-6/2-6.{i}" for i in range(1, 7)])
def _(d):
    t = d.units["VOL-II:T2-6"]
    cols = ["Ref", "Value", "Criterion", "Unit"]
    t.table["columns"] = cols
    t.text = t.table["title"] + " — " + " | ".join(cols)
    t.normalized = normalize_latin(t.text)
    for uid in t.children:
        u = d.units[uid]
        ren = {"Criterion": "Value", "Value": "Criterion"}
        u.cells = {ren.get(k, k): v for k, v in u.cells.items()}
        u.cell_spans = {ren.get(k, k): v for k, v in u.cell_spans.items()}
        u.text = row_text(u, cols)
        u.normalized = u.normalized  # rebuilt below
        u.normalized = normalize_latin(" | ".join(f"{c}: {u.cells[c].replace('³', '3')}" for c in cols if c in u.cells))


@attack("T2 values swapped between two rows of the same column (row membership)", "VOL-II",
        ["VOL-II:T2-6/2-6.1", "VOL-II:T2-6/2-6.2"])
def _(d):
    a, b = d.units["VOL-II:T2-6/2-6.1"], d.units["VOL-II:T2-6/2-6.2"]
    a.cells["Value"], b.cells["Value"] = b.cells["Value"], a.cells["Value"]
    sa, sb = a.cell_spans["Value"], b.cell_spans["Value"]
    a.cell_spans["Value"], b.cell_spans["Value"] = sb, sa
    for u, old, new in ((a, sa, sb), (b, sb, sa)):
        an = u.anchors[0]
        an["spans"] = [new[0] if x == old[0] else x for x in an["spans"]]
        rebox(d, an)
        u.text = row_text(u, ["Ref", "Criterion", "Value", "Unit"])
        u.normalized = u.text.replace("³", "3")


@attack("T3 form-field values swapped between rows (Tender reference <-> Proposal Due Date)", "VOL-IV",
        ["VOL-IV:F4-A/tender-reference", "VOL-IV:F4-A/proposal-due-date"])
def _(d):
    a, b = d.units["VOL-IV:F4-A/tender-reference"], d.units["VOL-IV:F4-A/proposal-due-date"]
    a.cells["col2"], b.cells["col2"] = b.cells["col2"], a.cells["col2"]
    sa, sb = a.cell_spans["col2"], b.cell_spans["col2"]
    a.cell_spans["col2"], b.cell_spans["col2"] = sb, sa
    for u, old, new in ((a, sa, sb), (b, sb, sa)):
        an = u.anchors[0]
        an["spans"] = [new[0] if x == old[0] else x for x in an["spans"]]
        rebox(d, an)
        u.text = f"{u.cells['col1']}: {u.cells['col2']}"
        u.normalized = u.text


@attack("T4 form field detached from its table (parent=None), label and value swapped", "VOL-IV",
        ["VOL-IV:F4-A/tender-reference"])
def _(d):
    u = d.units["VOL-IV:F4-A/tender-reference"]
    u.parent = None
    u.cells = {"col1": u.cells["col2"], "col2": u.cells["col1"]}
    u.cell_spans = {"col1": u.cell_spans["col2"], "col2": u.cell_spans["col1"]}
    u.text = f"{u.cells['col1']}: {u.cells['col2']}"
    u.normalized = u.text


@attack("T5 table row detached from its table (parent=None) with text and matching text emptied", "VOL-II",
        ["VOL-II:T2-6/2-6.1"])
def _(d):
    u = d.units["VOL-II:T2-6/2-6.1"]
    u.parent = None
    u.text = ""
    u.normalized = ""


@attack("T6 table column edges edited so '120,000' becomes part of the Unit cell (Value cell gone)", "VOL-II",
        ["VOL-II:T2-6", "VOL-II:T2-6/2-6.1"])
def _(d):
    t = d.units["VOL-II:T2-6"]
    g3 = next(g for g in t.table["grid"] if g["page"] == 3)
    g3["col_edges"] = [70.9, 127.6, 354.3, 370.0, 524.4]       # 120,000 cx=371.65; 7,500 cx=367.55
    u = d.units["VOL-II:T2-6/2-6.1"]
    u.cells = {"Ref": "2-6.1", "Criterion": "Average daily flow", "Unit": "120,000 m³/day"}
    u.cell_spans = {"Ref": u.cell_spans["Ref"], "Criterion": u.cell_spans["Criterion"],
                    "Unit": u.cell_spans["Value"] + u.cell_spans["Unit"]}
    u.text = row_text(u, t.table["columns"])
    u.normalized = u.text.replace("³", "3")


@attack("T7 table matching text (normalized) replaced", "VOL-II", ["VOL-II:T2-6"])
def _(d):
    d.units["VOL-II:T2-6"].normalized = "Table 9-9 - Unrelated - Ref | Criterion | Value | Unit"


@attack("T8 table with no spans (form grid) given arbitrary text and title", "VOL-IV", ["VOL-IV:F4-A/T1"])
def _(d):
    t = d.units["VOL-IV:F4-A/T1"]
    t.text = "Bid security: USD 0 (waived)"
    t.normalized = t.text
    t.label = "Table 9-9 — Waiver"


@attack("T9 table grid anchor moved to another ruled table on the same page", "VOL-IV", ["VOL-IV:F4-A/T1"])
def _(d):
    d.units["VOL-IV:F4-A/T1"].anchors[0]["bbox"] = list(d.units["VOL-IV:F4-A/T2"].anchors[0]["bbox"])


@attack("T10 captions (titles + caption spans) swapped between Table 2-2 (p2) and Table 2-6 (p3)", "VOL-II",
        ["VOL-II:T2-2", "VOL-II:T2-6"])
def _(d):
    a, b = d.units["VOL-II:T2-2"], d.units["VOL-II:T2-6"]
    ca, cb = a.table["caption_spans"], b.table["caption_spans"]
    a.table["caption_spans"], b.table["caption_spans"] = cb, ca
    a.table["title"], b.table["title"] = b.table["title"], a.table["title"]
    a.label, b.label = b.label, a.label
    for u, old, new in ((a, ca, cb), (b, cb, ca)):
        newpg = spans_of(d)[new[0]].page
        for an in u.anchors:                       # remove the old caption span
            an["spans"] = [x for x in an["spans"] if x not in old]
        an = next((x for x in u.anchors if x["page"] == newpg and x["spans"]), None)
        if an is None:
            an = {"page": newpg, "bbox": None, "spans": []}
            u.anchors.append(an)
            if newpg not in u.pages:
                u.pages.append(newpg)
        an["spans"] = new + an["spans"]
        for x in u.anchors:
            if x["spans"]:
                rebox(d, x)
        u.anchors = [x for x in u.anchors if x["spans"] or x["bbox"] is not None]
        u.text = u.table["title"] + " — " + " | ".join(u.table["columns"])
        u.normalized = normalize_latin(u.text)


# ---------------------------------------------------------------- flow units
@attack("F1 clause label changed (8.5 -> 8.6), footnote label changed (12 -> 13)", "VOL-I", ["VOL-I:8.5", "VOL-I:8.5#fn12"])
def _(d):
    d.units["VOL-I:8.5"].label = "8.6"
    d.units["VOL-I:8.5#fn12"].label = "13"


@attack("F2 label_span pointed at the '120,000 m' span; capacity dropped from text and matching text", "VOL-II", ["VOL-II:2.1"])
def _(d):
    u = d.units["VOL-II:2.1"]
    u.label_span = "VOL-II/p2/s024"                   # '120,000 m'
    u.text = "2.1 The Facility shall be designed for a nominal treatment capacity of ³/day average daily flow, " \
             "measured at the inlet works, at the design year influent characteristics stated in Table 2-2."
    u.normalized = normalize_latin(u.text)


@attack("F3 ordinary body line listed as a 'footnote marker'; dropped from matching text only", "VOL-II", ["VOL-II:2.2"])
def _(d):
    u = d.units["VOL-II:2.2"]
    u.footnote_markers.append({"number": "1", "span_id": "VOL-II/p2/s030", "footnote": "VOL-I:8.5#fn12"})
    u.normalized = normalize_latin("electrical equipment shall be not less than twenty (20) years or the manufacturer's "
                                   "rated life, whichever is the shorter, with lifecycle replacement provided for in the "
                                   "Project Company's lifecycle plan.")


@attack("F4 unit exponent reclassified as a footnote marker in a clause (m3/day -> m/day in matching text)", "VOL-II", ["VOL-II:2.1"])
def _(d):
    u = d.units["VOL-II:2.1"]
    u.unit_exponents.remove("VOL-II/p2/s025")
    u.footnote_markers.append({"number": "3", "span_id": "VOL-II/p2/s025", "footnote": "VOL-II:no-such-footnote"})
    u.normalized = u.normalized.replace("m3/day", "m/day")


@attack("F5 footnote marker reclassified as a unit exponent (matching text 'Form 4-B.12')", "VOL-I", ["VOL-I:8.5"])
def _(d):
    u = d.units["VOL-I:8.5"]
    u.footnote_markers = []
    u.unit_exponents.append("VOL-I/p4/s033")
    u.normalized = u.normalized + "12"


@attack("F6 table-row exponent reclassified as footnote marker (Unit 'm3/day' -> 'm/day' in matching text)", "VOL-II",
        ["VOL-II:T2-6/2-6.1"])
def _(d):
    u = d.units["VOL-II:T2-6/2-6.1"]
    u.unit_exponents.remove("VOL-II/p3/s040")
    u.footnote_markers.append({"number": "3", "span_id": "VOL-II/p3/s040", "footnote": "anything"})
    u.normalized = u.normalized.replace("m3/day", "m/day")


@attack("F7 one anchor split in two on the same page, listed in reverse; text reordered (line 2 before line 1)", "VOL-II", ["VOL-II:2.1"])
def _(d):
    u = d.units["VOL-II:2.1"]
    a = u.anchors[0]
    first = {"page": a["page"], "spans": [s for s in a["spans"] if s != "VOL-II/p2/s028"]}
    second = {"page": a["page"], "spans": ["VOL-II/p2/s028"]}
    rebox(d, first), rebox(d, second)
    u.anchors = [second, first]
    u.text = ("the inlet works, at the design year influent characteristics stated in Table 2-2. "
              "The Facility shall be designed for a nominal treatment capacity of 120,000 m³/day average daily flow, measured at")
    u.normalized = u.text.replace("³", "3")


@attack("F8 last line of clause 2.1 moved to the end of clause 2.2 (spans and texts moved consistently)", "VOL-II",
        ["VOL-II:2.1", "VOL-II:2.2"])
def _(d):
    a, b = d.units["VOL-II:2.1"], d.units["VOL-II:2.2"]
    a.anchors[0]["spans"].remove("VOL-II/p2/s028")
    rebox(d, a.anchors[0])
    b.anchors.append({"page": 2, "spans": ["VOL-II/p2/s028"]})
    rebox(d, b.anchors[-1])
    line = "the inlet works, at the design year influent characteristics stated in Table 2-2."
    a.text = a.text.replace(" " + line, "")
    a.normalized = a.normalized.replace(" " + line, "")
    b.text += " " + line
    b.normalized += " " + line


@attack("F9 printed text: footnote marker '¹²' written as ordinary digits 'Form 4-B.12' (NFKC fold)", "VOL-I", ["VOL-I:8.5"])
def _(d):
    u = d.units["VOL-I:8.5"]
    u.text = u.text.replace("4-B.¹²", "4-B.12")


@attack("F10 whitespace moved inside a form value: '12 November 2026' -> '1 2 November 20 26'", "VOL-IV",
        ["VOL-IV:F4-A/proposal-due-date"])
def _(d):
    u = d.units["VOL-IV:F4-A/proposal-due-date"]
    u.cells["col2"] = "1 2 November 20 26, 14:00 Riyadh time"
    u.text = f"{u.cells['col1']}: {u.cells['col2']}"
    u.normalized = u.text


@attack("F11 region placeholder unit given text", "VOL-II", [None])
def _(d):
    u = next(x for x in d.units.values() if x.kind == "region")
    u.text = "Effluent BOD5 limit: 500 mg/l"
    u.normalized = u.text


@attack("F12 footnote re-parented to another clause and host marker pointed at a non-existent unit", "VOL-I",
        ["VOL-I:8.5#fn12", "VOL-I:8.5"])
def _(d):
    d.units["VOL-I:8.5#fn12"].parent = "VOL-I:8.8"
    d.units["VOL-I:8.5"].footnote_markers[0]["footnote"] = "VOL-I:does-not-exist"


# ---------------------------------------------------------------- controls (should be caught)
@control("CTRL1 digits reordered in a flow clause (120,000 -> 210,000) in text and normalized", "VOL-II", ["VOL-II:2.1"])
def _(d):
    u = d.units["VOL-II:2.1"]
    u.text = u.text.replace("120,000", "210,000"); u.normalized = u.normalized.replace("120,000", "210,000")


@control("CTRL2 header text changed (Value -> Limit) with header_cell_spans re-keyed", "VOL-II", ["VOL-II:T2-6"])
def _(d):
    t = d.units["VOL-II:T2-6"]
    t.table["columns"] = ["Ref", "Criterion", "Limit", "Unit"]
    t.table["header_cell_spans"]["Limit"] = t.table["header_cell_spans"].pop("Value")
    t.text = t.table["title"] + " — Ref | Criterion | Limit | Unit"


@control("CTRL3 caption title edited (Table 2-6 -> Table 2-7)", "VOL-II", ["VOL-II:T2-6"])
def _(d):
    t = d.units["VOL-II:T2-6"]
    t.table["title"] = t.table["title"].replace("2-6", "2-7")
    t.text = t.text.replace("2-6", "2-7")


@control("CTRL4 spans permuted within a cell (m ³ /day -> /day m ³)", "VOL-II", ["VOL-II:T2-6/2-6.1"])
def _(d):
    u = d.units["VOL-II:T2-6/2-6.1"]
    u.cell_spans["Unit"] = ["VOL-II/p3/s041", "VOL-II/p3/s039", "VOL-II/p3/s040"]
    u.cells["Unit"] = "/daym³"
    u.text = row_text(u, ["Ref", "Criterion", "Value", "Unit"]); u.normalized = u.text.replace("³", "3")


@control("CTRL5 footnote marker dropped from printed text", "VOL-I", ["VOL-I:8.5"])
def _(d):
    u = d.units["VOL-I:8.5"]
    u.text = u.text.replace("¹²", "")


@control("CTRL6 anchor bbox shifted but spans unchanged", "VOL-IV", ["VOL-IV:F4-A/tender-reference"])
def _(d):
    a = d.units["VOL-IV:F4-A/tender-reference"].anchors[0]
    a["bbox"] = [a["bbox"][0], a["bbox"][1] + 23, a["bbox"][2], a["bbox"][3] + 23]


@control("CTRL7 label/value swapped in a form field that keeps its parent", "VOL-IV", ["VOL-IV:F4-A/tender-reference"])
def _(d):
    u = d.units["VOL-IV:F4-A/tender-reference"]
    u.cells = {"col1": u.cells["col2"], "col2": u.cells["col1"]}
    u.cell_spans = {"col1": u.cell_spans["col2"], "col2": u.cell_spans["col1"]}
    u.text = f"{u.cells['col1']}: {u.cells['col2']}"; u.normalized = u.text


@control("CTRL8 span from another clause appended out of reading order (2.2 line before 2.1 line inside one anchor)", "VOL-II", ["VOL-II:2.2"])
def _(d):
    b = d.units["VOL-II:2.2"]
    b.anchors[0]["spans"].insert(1, "VOL-II/p2/s032")
    b.anchors[0]["spans"].pop()                     # move last line to second position
    rebox(d, b.anchors[0])
    b.text = ("shorter, with lifecycle replacement provided for in the Project Company's lifecycle plan. The design life of all "
              "civil structures shall be not less than fifty (50) years. The design life of mechanical and electrical equipment "
              "shall be not less than twenty (20) years or the manufacturer's rated life, whichever is the")
    b.normalized = b.text



# ============================================================== reading-unit attacks (reviewer's)
@rattack("R1 anchors (crop + bbox) swapped between English header block and Arabic header block")
def _(ru):
    a, b = by_id(ru, "VOL-IV:F4-C/image/hdr-en"), by_id(ru, "VOL-IV:F4-C/image/hdr-ar")
    a["anchors"], b["anchors"] = b["anchors"], a["anchors"]


@rattack("R2 declaration 5 ('البند ٤-٢') anchored to declaration 1's band crop and bbox")
def _(ru):
    by_id(ru, "VOL-IV:F4-C/image/decl5")["anchors"] = copy.deepcopy(by_id(ru, "VOL-IV:F4-C/image/decl1")["anchors"][:1])


@rattack("R3 cell crops AND cell bboxes swapped between columns Limit and Unit of row BOD5")
def _(ru):
    a = by_id(ru, "VOL-II:T2-4/BOD5")["anchors"][0]
    for k in ("cell_crops", "cell_bbox_pt"):
        a[k]["Limit"], a[k]["Unit"] = a[k]["Unit"], a[k]["Limit"]


@rattack("R4 row anchors swapped between BOD5 and COD with grid_row removed")
def _(ru):
    a, b = by_id(ru, "VOL-II:T2-4/BOD5"), by_id(ru, "VOL-II:T2-4/COD")
    a["anchors"], b["anchors"] = b["anchors"], a["anchors"]
    for u in (a, b):
        u["anchors"][0].pop("grid_row")


@rattack("R5 row cells/text changed (BOD5 limit 10 -> 100); anchors untouched")
def _(ru):
    u = by_id(ru, "VOL-II:T2-4/BOD5")
    u["cells"]["Limit"] = "100"
    u["text"] = u["text"].replace("Limit: 10 ", "Limit: 100 ")
    u["normalized"] = u["text"]
    u["numeric"]["Limit"] = {"form": "single", "values": [100.0], "text": "100"}


@rattack("R6 row units' order permuted together with their texts (COD text at grid row 1, BOD5 at grid row 2)")
def _(ru):
    us = ru["VOL-II-p3-r1"]
    i, j = next(k for k, u in enumerate(us) if u["unit_id"] == "VOL-II:T2-4/BOD5"), \
        next(k for k, u in enumerate(us) if u["unit_id"] == "VOL-II:T2-4/COD")
    for key in ("unit_id", "label", "cells", "text", "normalized", "numeric"):
        us[i][key], us[j][key] = us[j][key], us[i][key]


@rattack("R7 unit with no anchors at all")
def _(ru):
    by_id(ru, "VOL-IV:F4-C/image/decl3")["anchors"] = []


@rattack("R8 block crop removed (None) and bbox moved to another place inside the region")
def _(ru):
    a = by_id(ru, "VOL-IV:F4-C/image/decl5")["anchors"][0]
    a["crop"] = None
    a["bbox"] = [100.0, 650.0, 300.0, 700.0]


@rattack("R9 block cites the whole-region crop with an arbitrary bbox")
def _(ru):
    a = by_id(ru, "VOL-IV:F4-C/image/decl5")["anchors"][0]
    a["crop"] = REGIONS["VOL-IV-p6-r1"].crop["path"]
    a["bbox"] = [100.0, 650.0, 300.0, 700.0]


@rattack("R10 cell crops dropped (None) / missing for some headings")
def _(ru):
    a = by_id(ru, "VOL-II:T2-4/BOD5")["anchors"][0]
    a["cell_crops"]["Limit"] = None
    del a["cell_crops"]["Unit"]


@rattack("R4b row anchors swapped between BOD5 and COD, grid_row removed from every row unit")
def _(ru):
    a, b = by_id(ru, "VOL-II:T2-4/BOD5"), by_id(ru, "VOL-II:T2-4/COD")
    a["anchors"], b["anchors"] = b["anchors"], a["anchors"]
    for u in ru["VOL-II-p3-r1"]:
        for an in u["anchors"]:
            an.pop("grid_row", None)


# controls -------------------------------------------------------------------------
@rcontrol("CTRL1 row crop swapped between two rows (grid_row kept)")
def _(ru):
    a, b = by_id(ru, "VOL-II:T2-4/BOD5")["anchors"][0], by_id(ru, "VOL-II:T2-4/COD")["anchors"][0]
    a["crop"], b["crop"] = b["crop"], a["crop"]


@rcontrol("CTRL2 block crop swapped without its bbox")
def _(ru):
    a, b = by_id(ru, "VOL-IV:F4-C/image/hdr-en")["anchors"][0], by_id(ru, "VOL-IV:F4-C/image/hdr-ar")["anchors"][0]
    a["crop"], b["crop"] = b["crop"], a["crop"]


@rcontrol("CTRL3 whole row anchors swapped (grid_row kept)")
def _(ru):
    a, b = by_id(ru, "VOL-II:T2-4/BOD5"), by_id(ru, "VOL-II:T2-4/COD")
    a["anchors"], b["anchors"] = b["anchors"], a["anchors"]


@rcontrol("CTRL4 cell crop swapped without its cell bbox")
def _(ru):
    a = by_id(ru, "VOL-II:T2-4/BOD5")["anchors"][0]
    a["cell_crops"]["Limit"], a["cell_crops"]["Unit"] = a["cell_crops"]["Unit"], a["cell_crops"]["Limit"]


@rcontrol("CTRL5 anchor bbox outside the region")
def _(ru):
    by_id(ru, "VOL-IV:F4-C/image/decl5")["anchors"][0]["bbox"] = [10.0, 10.0, 50.0, 50.0]




@pytest.fixture(scope="module")
def regions(pack):
    return {g.region_id: g for d in pack["pack"].docs for g in d.regions}


REGIONS = {}


@pytest.mark.parametrize("doc_id,mutate", ATTACKS)
def test_text_layer_mutation_is_caught(pack, doc_id, mutate):
    assert _failing(pack, doc_id, mutate)


@pytest.mark.parametrize("doc_id,mutate", CONTROLS)
def test_text_layer_control_is_caught(pack, doc_id, mutate):
    assert _failing(pack, doc_id, mutate)


@pytest.mark.parametrize("mutate", RATTACKS)
def test_reading_unit_mutation_is_caught(pack, regions, mutate):
    REGIONS.update(regions)
    assert _failing(pack, rmutate=mutate)


@pytest.mark.parametrize("mutate", RCONTROLS)
def test_reading_unit_control_is_caught(pack, regions, mutate):
    REGIONS.update(regions)
    assert _failing(pack, rmutate=mutate)


def test_unmutated_pack_passes(pack):
    assert _failing(pack) == []


def test_footnote_relabelled_as_clause_is_caught(pack):
    def m(d):
        u = d.units["VOL-I:8.5#fn12"]
        u.kind, u.parent = "clause", None
    assert _failing(pack, "VOL-I", m)


def test_invisible_layer_relabelled_as_paragraph_is_caught(synthetic):
    p = copy.deepcopy(synthetic["pack"])
    u = next(x for x in p.docs[0].units.values() if x.kind == "invisible_text")
    u.kind, u.notes = "paragraph", []
    cov = coverage_report(p, synthetic["packets"], _reading_units(synthetic), [], synthetic["evidence"],
                          synthetic.get("reading_sources"))
    assert any(not c["ok"] for c in cov["checks"])


# ============================================================== render check and output paths (reviewer's)

ARABIC_LINE = "خامساً: نلتزم بقواعد الاتصال المنصوص عليها في البند ٤-٢ من المجلد الأول."


@pytest.mark.parametrize("expected", ["", "-", "٢"])
def test_empty_or_partial_expected_visual_order_fails(expected):
    from tenderpack.arabic import visual_check
    assert visual_check(ARABIC_LINE, expected)[0] == "fail"


def test_empty_expected_visual_order_fails_rd6_on_the_real_reading(pack):
    import pymupdf
    from conftest import ROOT
    from tenderpack.readings import check_reading, load_readings
    reading, _ = load_readings(ROOT / "curation/readings")["VOL-IV-p6-r1"]
    region = next(g for d in pack["pack"].docs for g in d.regions if g.region_id == "VOL-IV-p6-r1")
    r = reading.model_copy(deep=True)
    next(b for b in r.blocks if b.key == "decl5").lines[0].numerals[0].visual_ltr_expected = ""
    pdf = pymupdf.open(ROOT / "sources/candidate_pack/VOL-IV_Form_Sheets.pdf")
    assert any(c["check"] == "RD6" and not c["ok"] for c in check_reading(r, region, pdf))


def test_two_numerals_are_checked_in_their_left_to_right_order():
    """Numerals of one line are declared in the order the crop shows them, left to right; a transcription with the
    from/to times typed the wrong way round must fail even though each token is found."""
    from tenderpack.arabic import order_check
    correct = "يبدأ العمل من 10:00 إلى 12:00 يومياً"       # printed: from 10:00 to 12:00
    wrong = "يبدأ العمل من 12:00 إلى 10:00 يومياً"
    crop_ltr = ["12:00", "10:00"]                          # an RTL line shows 'to' on the left
    assert order_check(correct, crop_ltr)[0] and not order_check(wrong, crop_ltr)[0]


@pytest.mark.parametrize("source,token", [
    ("الطاقة 120,000 m³/day تقريباً", "120,000 m³/day"),
    ("درجة الحرارة 25 °C كحد أقصى", "25 °C"),
    ("التركيز 0.5 µg/l كحد أقصى", "0.5 µg/l"),
    ("النموذج Form 4‑B مطلوب", "Form 4‑B"),
    ("المرجع NUPA/ISTP/٢٠٢٦/014 للمناقصة", "NUPA/ISTP/٢٠٢٦/014"),
])
def test_latin_expressions_render_as_printed(source, token):
    from tenderpack.arabic import visual_check
    assert visual_check(source, token)[0] == "pass"


def test_bracket_of_an_arabic_parenthetical_stays_outside_the_latin_island():
    from tenderpack.arabic import display_form, LRE, PDF
    assert display_form("(انظر Form 4-B)") == f"(انظر {LRE}Form 4-B{PDF})"


def test_extended_arabic_indic_digits_are_not_letters():
    from tenderpack.arabic import visual_check
    assert visual_check("رقم ۱۲/45 فقط", "۲۱/45")[0] == "fail"


def test_inputs_inside_a_candidate_sibling_are_refused(tmp_path):
    import make_fixture
    from conftest import ROOT
    from tenderpack.cli import UnsafeOutputError, ingest
    rej = tmp_path / "build.rejected"
    rej.mkdir()
    (rej / ".tenderpack-build").write_text("marker\n")
    make_fixture.build(rej / "pack")
    with pytest.raises(UnsafeOutputError):
        ingest(rej / "pack/pack.yaml", tmp_path / "build", ROOT, quiet=True, require_approved=True)
    assert (rej / "pack/pack.yaml").exists()


def test_symlinked_candidate_sibling_is_refused(tmp_path):
    import make_fixture
    from conftest import ROOT
    from tenderpack.cli import UnsafeOutputError, ingest
    make_fixture.build(tmp_path / "src")
    (tmp_path / "other").mkdir()
    (tmp_path / "build.rejected").symlink_to(tmp_path / "other")
    with pytest.raises(UnsafeOutputError):
        ingest(tmp_path / "src/pack.yaml", tmp_path / "build", ROOT, quiet=True, require_approved=True)
    assert not [p for p in tmp_path.iterdir() if ".building-" in p.name]


# ============================================================== added after mutations A2, A4, A6 survived
# The reviewer's mutations alter units after they were made, so re-derivation catches them first. These three
# reproduce what only the independent checks can see: a defect inside the derivation itself.

def test_segmenter_bug_shared_by_the_recheck_is_caught_by_fresh_geometry(tmp_path, monkeypatch):
    """A segmenter that merges two grid rows into one row unit produces the same wrong unit when C10 re-runs it
    (cell text and columns stay consistent); only the independently re-detected grid shows the row spans two rows."""
    import make_fixture as mf
    import pymupdf
    from conftest import ROOT
    from test_review_regressions import mini_pack
    from tenderpack.cli import ingest
    import tenderpack.segment as seg
    orig = seg.Segmenter._tables

    def swapped(self, pno, content):
        found, cell_of = orig(self, pno, content)
        return found, {sid: (ti, 1 if ri == 2 else ri, ci) for sid, (ti, ri, ci) in cell_of.items()}
    monkeypatch.setattr(seg.Segmenter, "_tables", swapped)

    def pages(doc):
        mf.ruled_table(doc.new_page(width=595, height=842), 71, 100, [80, 220, 80],
                       [["1", "Alpha", "10"], ["2", "Beta", "20"]], header=["Ref", "Item", "Value"])
    res = ingest(mini_pack(tmp_path / "t", pages), tmp_path / "out", ROOT, quiet=True)
    assert "C10" in {c["id"] for c in res["coverage"]["checks"] if not c["ok"]}


def test_reading_derivation_bug_shared_by_the_recheck_is_caught_by_the_band_tie(pack, monkeypatch):
    """A derivation that gives a block another block's crop and box is repeated by the re-derivation; only the
    band each anchor declares shows the crop belongs to a different band."""
    import tenderpack.readings as rd
    orig = rd.reading_units

    def buggy(reading, region, status, ev):
        units = orig(reading, region, status, ev)
        blocks = [u for u in units if u["kind"] == "reading_block"]
        if len(blocks) >= 2:
            a, b = blocks[0]["anchors"][0], blocks[1]["anchors"][0]
            for k in ("crop", "bbox"):
                a[k], b[k] = b[k], a[k]
        return units
    monkeypatch.setattr(rd, "reading_units", buggy)
    ru = {rid: buggy(r, next(g for d in pack["pack"].docs for g in d.regions if g.region_id == rid), st, pack["evidence"][rid])
          for rid, (r, st) in pack["reading_sources"].items()}
    cov = coverage_report(copy.deepcopy(pack["pack"]), pack["packets"], ru, [], pack["evidence"], pack["reading_sources"])
    assert any(not c["ok"] for c in cov["checks"])


def test_declared_visual_naming_another_run_of_the_line_fails():
    """'NUPA' is a whole run in the rendered line, but it is not the token '2026/014'."""
    from tenderpack.arabic import visual_check
    line = "مناقصة رقم: NUPA/ISTP/2026/014"
    assert visual_check(line, "2026/014", "2026/014")[0] == "pass"
    assert visual_check(line, "NUPA", "2026/014")[0] == "fail"
