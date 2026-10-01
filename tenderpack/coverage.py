"""Stage 1 accounting and reports.

C01  sources match the manifest (sha256, page count)            -> sources.py raises before anything runs
C02  every page accounted for (content spans, exclusions, regions)
C03  every content span is assigned to exactly one unit
C04  every exclusion matched a declared furniture rule; rules with an expected count matched it on every page
C05  every region has a reading; readings pass their checks; pending review is shown, never hidden
C06  every superscript is classified (unit exponent or footnote marker) and every footnote is paired
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from .util import write_text


def coverage_report(pack, packets: dict[str, dict], reading_units: dict[str, list[dict]]) -> dict:
    checks = []
    pages = []
    exclusions = []
    superscripts = []
    footnotes = []
    split_tables = []
    small_print = []
    rotated_content = []
    problems = []
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
        dup = [sid for sid, n in Counter(sid for u in d.units.values() for a in u.anchors for sid in a["spans"]).items() if n > 1]
        problems += [f"{doc_id}: {x}" for x in d.problems]
        if dup:
            problems.append(f"{doc_id}: spans listed in more than one unit: {dup[:5]}")

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
    checks.append({"id": "C05", "ok": not unread and not failing,
                   "detail": f"{len(regions)} regions; unread {unread or 'none'}; readings failing checks {failing or 'none'}; "
                             f"PENDING HUMAN REVIEW: {pending or 'none'}"})
    unclassified = [s for s in superscripts if s["class"] == "unclassified"]
    unpaired = [s for s in superscripts if s["class"] == "footnote marker" and not s["footnote"]]
    checks.append({"id": "C06", "ok": not unclassified and not unpaired and not any("footnote" in x for x in problems),
                   "detail": f"{len(superscripts)} superscripts: "
                             f"{sum(1 for s in superscripts if s['class'] == 'unit exponent')} unit exponents, "
                             f"{sum(1 for s in superscripts if s['class'] == 'footnote marker')} footnote markers "
                             f"(all paired: {not unpaired}); unclassified {len(unclassified)}"})
    return {"checks": checks, "pages": pages, "exclusions": exclusions, "superscripts": superscripts,
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
    L += ["", "## Problems", ""] + ([f"- {p}" for p in cov["problems"]] or ["None."])
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
