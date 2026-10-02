"""Stage 1 accounting and reports.

C01  sources match the manifest (sha256, page count)            -> sources.py raises before anything runs
C02  every page accounted for (content spans, exclusions, regions)
C03  every content span is assigned to exactly one unit
C04  every exclusion matched a declared furniture rule; rules with an expected count matched it on every page
C05  every region has a reading and every reading has a region; readings pass their checks;
     pending review is shown, never hidden (pending is not a failure)
C06  every superscript is classified (unit exponent or footnote marker) and every footnote is paired
C07  unit ids are unique across the pack (text-layer and reading units); nothing was renamed
C08  every content span appears exactly once in exactly one unit's anchors, and every anchored
     span exists on its page
C09  segmentation reported no problems
C10  full evidence: every text-layer unit is compared with spans re-extracted from the PDF.
     Flow units: the whole printed text (label excluded) and the whole matching text must equal
     the spans' text, character for character apart from whitespace. Tables, rows and form
     fields: the characters of the title, headers and cells must be exactly the characters of
     their spans (same multiset), and each cell must appear in the row text.

Any failing check is a structural failure: `ingest` exits non-zero and keeps the previous build.
Pending human review is a separate status, not a failure.
"""
from __future__ import annotations

import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import pymupdf

from .extract import extract_page
from .textnorm import normalize_latin
from .util import write_text


def _chars(text: str) -> str:
    """Characters for evidence comparison: NFKC (a superscript ³ compares as 3), whitespace removed."""
    return "".join(unicodedata.normalize("NFKC", text).split())


def full_evidence(d, rules) -> dict:
    """C10: re-extract every page of the document and compare each text-layer unit in full."""
    pdf = pymupdf.open(d.doc.path)
    fresh = {}
    for i in range(pdf.page_count):
        for s in extract_page(d.doc.doc_id, pdf[i], rules).content:
            fresh[s.span_id] = s
    checked, failures = 0, []

    def fail(u, why):
        failures.append({"unit": u.unit_id, "kind": u.kind, "why": why})

    for u in d.units.values():
        sids = [sid for a in u.anchors for sid in a["spans"]]
        if u.kind == "region":
            continue
        checked += 1
        missing = [sid for sid in sids if sid not in fresh]
        if missing:
            fail(u, f"anchored spans not found when the PDF is re-extracted: {missing[:3]}")
            continue
        spans = [fresh[sid] for sid in sids]
        if not spans:
            if u.text.strip():
                fail(u, "text with no source spans")
            continue
        if u.kind == "table":
            t = u.table or {}
            header = "".join(t.get("columns") or [])
            want = Counter(_chars((t.get("title") or "") + header + header * len(t.get("repeated_headers", []))))
            if Counter(_chars("".join(s.text for s in spans))) != want:
                fail(u, "title and header characters differ from the caption and header spans")
            elif u.text != (t["title"] + " — " if t.get("title") else "") + " | ".join(t.get("columns") or []):
                fail(u, "table text is not its title and header")
            continue
        if u.kind in ("table_row", "form_field"):
            cells = list((u.cells or {}).values())
            if Counter(_chars("".join(s.text for s in spans))) != Counter(_chars("".join(cells))):
                fail(u, "cell characters differ from the row's spans")
            elif not all(c in u.text for c in cells):
                fail(u, "a cell value is missing from the row text")
            continue
        body = [s for s in spans if s.span_id != u.label_span]
        markers = {m["span_id"] for m in u.footnote_markers}
        printed = _chars("".join(s.text for s in body))
        match = _chars(normalize_latin("".join(s.text for s in body if s.span_id not in markers)))
        if _chars(u.text) != printed:
            fail(u, "printed text differs from its spans")
        elif _chars(u.normalized) != match:
            fail(u, "matching text differs from its spans")
    return {"units_checked": checked, "failures": failures}


def coverage_report(pack, packets: dict[str, dict], reading_units: dict[str, list[dict]],
                    orphan_readings: list[str] | None = None) -> dict:
    checks = []
    pages = []
    exclusions = []
    superscripts = []
    footnotes = []
    split_tables = []
    small_print = []
    rotated_content = []
    problems = []
    notices = []
    anchor_twice, anchor_none, anchor_unknown, duplicates = [], [], [], []
    evidence = {"units_checked": 0, "failures": []}
    for d in pack.docs:
        doc_id = d.doc.doc_id
        assigned = Counter(d.span_unit.values())
        unit_pages = defaultdict(set)
        for u in d.units.values():
            for pg in u.pages:
                unit_pages[pg].add(u.unit_id)
        for p in d.pages:
            excl = Counter(e.rule for e in p.exclusions)
            content_ids = [s.span_id for s in p.content]
            unassigned = [sid for sid in content_ids if sid not in d.span_unit]
            regs = [g for g in d.regions if g.page == p.page]
            pages.append({
                "doc": doc_id, "page": p.page, "printed_page": p.printed_page,
                "content_spans": len(content_ids), "assigned": len(content_ids) - len(unassigned),
                "unassigned": unassigned, "excluded": dict(sorted(excl.items())), "blank_spans": p.blank_spans,
                "invisible_spans": p.invisible_spans, "units": len(unit_pages[p.page]),
                "regions": [{"id": g.region_id, "kind": g.kind,
                             "reading": packets.get(g.region_id, {}).get("status", "unread")} for g in regs],
            })
            for e in p.exclusions:
                exclusions.append(e.__dict__)
            for s in p.content:
                if s.angle != 0 and not s.invisible:
                    rotated_content.append({"span": s.span_id, "text": s.text, "angle": s.angle,
                                            "unit": d.span_unit.get(s.span_id)})
                if s.superscript:
                    u = d.units.get(d.span_unit.get(s.span_id, ""))
                    kind = ("unit exponent" if u and s.span_id in u.unit_exponents else
                            "footnote marker" if u and any(m["span_id"] == s.span_id for m in u.footnote_markers) else
                            "unclassified")
                    paired = None
                    if u and kind == "footnote marker":
                        paired = next((m.get("footnote") for m in u.footnote_markers if m["span_id"] == s.span_id), None)
                    superscripts.append({"span": s.span_id, "text": s.text, "size": s.size, "unit": d.span_unit.get(s.span_id),
                                         "class": kind, "footnote": paired})
        for u in d.units.values():
            if u.kind == "footnote":
                footnotes.append({"unit": u.unit_id, "label": u.label, "host": u.parent, "page": u.pages,
                                  "text": u.text})
            if u.kind == "table" and len(u.pages) > 1:
                split_tables.append({"unit": u.unit_id, "pages": u.pages, "title": u.table.get("title"),
                                     "rows": len(u.children),
                                     "repeated_headers": u.table.get("repeated_headers", []),
                                     "row_pages": {c: d.units[c].pages for c in u.children}})
            if u.style.get("small_print"):
                small_print.append({"unit": u.unit_id, "kind": u.kind, "max_size": u.style.get("max_size"),
                                    "text": u.text[:160]})
        problems += [f"{doc_id}: {x}" for x in d.problems]
        notices += [f"{doc_id}: {x}" for x in getattr(d, "notices", [])]
        anchored = Counter(sid for u in d.units.values() for a in u.anchors for sid in a["spans"])
        content = {s.span_id for p in d.pages for s in p.content}
        anchor_twice += [sid for sid, n in anchored.items() if n > 1]
        anchor_none += [sid for sid in content if sid not in anchored]
        anchor_unknown += [sid for sid in anchored if sid not in content]
        duplicates += list(getattr(d, "duplicates", []))
        ev = full_evidence(d, pack.rules)
        evidence["units_checked"] += ev["units_checked"]
        evidence["failures"] += ev["failures"]

    total_content = sum(p["content_spans"] for p in pages)
    total_assigned = sum(p["assigned"] for p in pages)
    checks.append({"id": "C01", "ok": True, "detail": f"{len(pack.docs)} documents match sources/manifest.json (sha256, pages)"})
    checks.append({"id": "C02", "ok": len(pages) == sum(d.doc.pages for d in pack.docs),
                   "detail": f"{len(pages)} pages accounted for out of {sum(d.doc.pages for d in pack.docs)}"})
    checks.append({"id": "C03", "ok": total_content == total_assigned and not any("assigned twice" in x for x in problems),
                   "detail": f"{total_assigned} of {total_content} content spans assigned to exactly one unit"})
    excl_counts = Counter(e["rule"] for e in exclusions)
    checks.append({"id": "C04", "ok": not pack.furniture_problems,
                   "detail": f"{len(exclusions)} spans excluded, all by declared rules: {dict(sorted(excl_counts.items()))}; "
                             f"expected-count problems: {pack.furniture_problems or 'none'}"})
    regions = [g for d in pack.docs for g in d.regions]
    unread = [g.region_id for g in regions if g.region_id not in packets or packets[g.region_id]["status"] == "unread"]
    failing = [rid for rid, pk in packets.items() if any(not c["ok"] for c in pk.get("checks", []))]
    pending = [rid for rid, pk in packets.items() if pk.get("status") == "pending"]
    orphan = sorted(orphan_readings or [])
    checks.append({"id": "C05", "ok": not unread and not failing and not orphan,
                   "detail": f"{len(regions)} regions; unread {unread or 'none'}; readings failing checks {failing or 'none'}; "
                             f"readings with no detected region {orphan or 'none'}; "
                             f"PENDING HUMAN REVIEW: {pending or 'none'}"})
    unclassified = [s for s in superscripts if s["class"] == "unclassified"]
    unpaired = [s for s in superscripts if s["class"] == "footnote marker" and not s["footnote"]]
    checks.append({"id": "C06", "ok": not unclassified and not unpaired and not any("footnote" in x for x in problems),
                   "detail": f"{len(superscripts)} superscripts: "
                             f"{sum(1 for s in superscripts if s['class'] == 'unit exponent')} unit exponents, "
                             f"{sum(1 for s in superscripts if s['class'] == 'footnote marker')} footnote markers "
                             f"(all paired: {not unpaired}); unclassified {len(unclassified)}"})
    ids = [u.unit_id for d in pack.docs for u in d.units.values()] + \
          [u["unit_id"] for us in reading_units.values() for u in us]
    id_dups = sorted({i for i, n in Counter(ids).items() if n > 1} | set(duplicates))
    checks.append({"id": "C07", "ok": not id_dups,
                   "detail": f"{len(ids)} unit ids; produced more than once: {id_dups or 'none'}"})
    checks.append({"id": "C08", "ok": not (anchor_twice or anchor_none or anchor_unknown),
                   "detail": f"{total_content} content spans; in more than one anchor: {sorted(anchor_twice)[:5] or 'none'}; "
                             f"in no anchor: {sorted(anchor_none)[:5] or 'none'}; anchored but not on the page: "
                             f"{sorted(anchor_unknown)[:5] or 'none'}"})
    checks.append({"id": "C09", "ok": not problems,
                   "detail": f"segmentation problems: {len(problems)}" + (f" (see Problems): {problems[:3]}" if problems else "")})
    checks.append({"id": "C10", "ok": not evidence["failures"],
                   "detail": f"{evidence['units_checked']} text-layer units compared in full with spans re-extracted from "
                             f"the PDF; mismatches: {[f['unit'] for f in evidence['failures']][:5] or 'none'}"})
    status = "ok" if all(c["ok"] for c in checks) else "structural_failure"
    return {"status": status, "checks": checks, "evidence": evidence, "notices": notices, "pages": pages, "exclusions": exclusions, "superscripts": superscripts,
            "footnotes": footnotes, "split_tables": split_tables, "small_print": small_print,
            "rotated_content": rotated_content, "problems": problems,
            "regions": [{"id": g.region_id, "doc": g.doc, "page": g.page, "kind": g.kind, "bbox": g.bbox,
                         "detection": g.detection, "notes": g.notes,
                         "reading_status": packets.get(g.region_id, {}).get("status", "unread"),
                         "reading_units": len(reading_units.get(g.region_id, []))} for g in regions],
            "pending_review": pending}


def coverage_markdown(cov: dict, title: str) -> str:
    L = [f"# Coverage report — {title}", "",
         "Generated by `python -m tenderpack ingest`. Deterministic: no timestamps. "
         "Accounting is not correctness: a span assigned to a unit says the text was captured, "
         "not that its meaning has been interpreted.", ""]
    if cov["status"] != "ok":
        L += [f"> **STRUCTURAL FAILURE:** checks {', '.join(c['id'] for c in cov['checks'] if not c['ok'])} failed. "
              "This build is not usable; the previous build (if any) was kept.", ""]
    if cov["pending_review"]:
        L += [f"> **PENDING HUMAN REVIEW:** {', '.join(cov['pending_review'])}. Units derived from these readings are "
              "marked `reading.status = pending`.", ""]
    L += ["## Checks", "", "| Check | Result | Detail |", "|---|---|---|"]
    for c in cov["checks"]:
        L.append(f"| {c['id']} | {'pass' if c['ok'] else 'FAIL'} | {c['detail']} |")
    L += ["", "## Pages", "", "| Doc | PDF p | Printed | Content spans | Assigned | Excluded (rule: n) | Units | Regions (reading) |",
          "|---|---|---|---|---|---|---|---|"]
    for p in cov["pages"]:
        ex = ", ".join(f"{k}: {v}" for k, v in p["excluded"].items())
        rg = ", ".join(f"{r['id']} {r['kind']} ({r['reading']})" for r in p["regions"]) or "—"
        L.append(f"| {p['doc']} | {p['page']} | {p['printed_page']} | {p['content_spans']} | {p['assigned']} | {ex} | "
                 f"{p['units']} | {rg} |")
    L += ["", "## Regions (content outside the text layer)", "", "| Region | Kind | BBox (pt) | Detection | Reading | Units from reading |",
          "|---|---|---|---|---|---|"]
    for r in cov["regions"]:
        L.append(f"| {r['id']} | {r['kind']} | {r['bbox']} | {r['detection']} | **{r['reading_status']}** | {r['reading_units']} |")
    L += ["", "## Superscripts", "", "| Span | Text | Size | Class | Unit | Footnote |", "|---|---|---|---|---|---|"]
    for s in cov["superscripts"]:
        L.append(f"| {s['span']} | {s['text']} | {s['size']} | {s['class']} | {s['unit']} | {s['footnote'] or ''} |")
    L += ["", "## Footnotes", ""]
    for f in cov["footnotes"]:
        L.append(f"- `{f['unit']}` (label {f['label']}, host `{f['host']}`, p{f['page']}): {f['text']}")
    L += ["", "## Tables split across pages", ""]
    for t in cov["split_tables"]:
        L.append(f"- `{t['unit']}` pages {t['pages']}, {t['rows']} rows; title: {t['title'] or '—'}; "
                 f"repeated header rows recognised and kept with the table: "
                 f"{[(h['page'], len(h['spans'])) for h in t['repeated_headers']]}; row pages: "
                 + ", ".join(f"{k.split('/')[-1] if '/' in k else k}: {v}" for k, v in t["row_pages"].items()))
    L += ["", "## Small print (largest font < 85% of the document's body size)", ""]
    for s in cov["small_print"]:
        L.append(f"- `{s['unit']}` ({s['kind']}, {s['max_size']} pt): {s['text']}")
    L += ["", "## Rotated text kept as content", ""]
    L += [f"- `{r['span']}` angle {r['angle']}: {r['text']} -> `{r['unit']}`" for r in cov["rotated_content"]] or \
         ["None in this pack: every rotated span matched the WATERMARK rule (see exclusions)."]
    L += ["", "## Full evidence check (C10) mismatches", ""] + (
        [f"- `{f['unit']}` ({f['kind']}): {f['why']}" for f in cov["evidence"]["failures"]] or
        [f"None: {cov['evidence']['units_checked']} units compared in full."])
    L += ["", "## Problems", ""] + ([f"- {p}" for p in cov["problems"]] or ["None."])
    L += ["", "## Notices (reported, not failures)", ""] + ([f"- {p}" for p in cov["notices"]] or ["None."])
    return "\n".join(L) + "\n"


def exclusions_markdown(cov: dict, rules: list[dict], title: str) -> str:
    L = [f"# Excluded text — {title}", "",
         "Every span below was excluded from content because it matched a declared rule in "
         "`config/furniture.yaml` on all of the rule's attributes. Nothing else is excluded; in particular, "
         "rotated text that does not match the WATERMARK rule stays content.", "", "## Rules", ""]
    for r in rules:
        attrs = {k: v for k, v in r.items() if not k.startswith("_") and k not in ("id", "reason")}
        L.append(f"- **{r['id']}**: {r['reason']}. Attributes: `{attrs}`")
    L += ["", f"## All exclusions ({len(cov['exclusions'])} spans)", "",
          "| Span | Rule | Text | Angle | Colour | Size | BBox |", "|---|---|---|---|---|---|---|"]
    for e in cov["exclusions"]:
        L.append(f"| {e['span_id']} | {e['rule']} | {e['text']} | {e['angle']} | {e['color']} | {e['size']} | {e['bbox']} |")
    return "\n".join(L) + "\n"


def units_markdown(ordered_units: list[dict], title: str) -> str:
    L = [f"# Source units — {title}", "",
         "One line per unit, in reading order. `text` is as printed (superscripts shown as ¹²/³); "
         "matching text is in units.json (`normalized`). Units from image readings show their review status.", ""]
    doc = None
    for u in ordered_units:
        if u["doc"] != doc:
            doc = u["doc"]
            L += ["", f"## {doc}", "", "| Unit | Kind | Pages | Flags | Text |", "|---|---|---|---|---|"]
        flags = []
        st = u.get("style", {})
        if st.get("small_print"):
            flags.append(f"small print {st.get('max_size')}pt")
        if u.get("origin") == "image_reading":
            flags.append(f"image reading: **{u['reading']['status'].upper()}**")
        if u.get("angle"):
            flags.append(f"rotated {u['angle']}°")
        if u.get("footnote_markers"):
            flags.append("footnote " + ",".join(m["number"] for m in u["footnote_markers"]))
        if u.get("unit_exponents"):
            flags.append(f"{len(u['unit_exponents'])} unit exponent(s)")
        if u.get("uncertain"):
            flags.append(f"{len(u['uncertain'])} uncertainty(ies)")
        if u.get("table", {}) and u["table"].get("repeated_headers"):
            flags.append(f"split table, repeated headers on p{[h['page'] for h in u['table']['repeated_headers']]}")
        text = u.get("text", "").replace("|", "/")
        if u.get("translation"):
            text += f" — *translation:* {u['translation']}"
        L.append(f"| `{u['unit_id']}` | {u['kind']} | {','.join(map(str, u.get('pages', [])))} | {'; '.join(flags)} | {text} |")
    return "\n".join(L) + "\n"


def write_reports(out: Path, cov: dict, ordered_units: list[dict], rules: list[dict], title: str) -> None:
    write_text(out / "coverage.md", coverage_markdown(cov, title))
    write_text(out / "exclusions.md", exclusions_markdown(cov, rules, title))
    write_text(out / "units.md", units_markdown(ordered_units, title))
