"""Live-session commands (session 06): `show ROW-ID` and `diff`.

  show ROW-ID   the row's requirement, owner, evidence and review decision; its status, quote, consequence and dates
                at every stage; its source pages (latest reference) with highlighted crops; the amendment chain
                (each op, its provision's words, page and validity); the A5 activities that plan it. Writes
                <to>/<ROW-ID>/index.html with the crops beside the text (default: show/, outside every build).
  diff          what one addendum changed, from one stage to the next (default: the last two): the addendum's
                status and unresolved provisions; requirements that are new, gone or changed (and why: every unit
                a row cites is compared, not only its first, so a row whose secondary unit was replaced, amended,
                deleted, issued or annotated is listed with that unit and the op that changed it); rows that
                became STALE, review decisions it voided and image-read values it changed; obligations that do
                not reach the outputs (C46); what the change reaches through the curated relationships (session 10:
                confirmed dependency / proposed relationship / possible impact, and documents not supplied whose
                blocked conclusions are in play; never merged with the direct changes); disqualifiers that enter or
                leave A3; and the programme impact (new / removed / moved / rework activities, REVIEW through a
                relationship, feasibility changes, document counts). When the addendum is PARTIAL (session 11), it
                also points to the validated and the candidate A3/A5 and says in one paragraph what may be changing
                (partial.diff_lines).
Both read a published evidence build and the curated inputs; neither writes into a build, the outputs or curation.
"""
from __future__ import annotations

import html
import shutil
from pathlib import Path

import pymupdf

from . import programme, relationships, review
from .register import BID_OUT, Consequence
from .schedule import deltas

DPI = 110


def _in_force(status: str) -> bool:
    from .schedule import in_force          # one rule for every consumer (REMOVED rows are out of force; session 09)
    return in_force(status)


def _docs(r: dict) -> dict[str, Path]:
    return {d["doc_id"]: (r["root"] / d["path"]) for d in r["cfg"]["documents"]}


def crop_unit(r: dict, uid: str, dest: Path, build_dir: Path) -> list[dict]:
    """PNG crop(s) of one unit: the reading's own crops for image units, else the page region with the unit's
    anchors outlined in red. Returns [{'unit', 'page', 'file'}] (file relative to dest's parent)."""
    u = next((x for x in r["units"] if x["unit_id"] == uid), None)
    if u is None or not u.get("anchors"):
        return []
    dest.mkdir(parents=True, exist_ok=True)
    safe = uid.replace(":", "_").replace("/", "_").replace("#", "_").replace("+", "_")
    out = []
    crops = [a["crop"] for a in u["anchors"] if a.get("crop")]
    if crops:
        for i, c in enumerate(crops):
            src = build_dir / c
            if src.exists():
                f = dest / f"{safe}-{i}.png"
                shutil.copyfile(src, f)
                out.append({"unit": uid, "page": u["anchors"][0]["page"], "file": f"{dest.name}/{f.name}"})
        return out
    pdf_path = _docs(r).get(u["doc"])
    if pdf_path is None or not pdf_path.exists():
        return []
    pdf = pymupdf.open(pdf_path)
    for page_no in sorted({a["page"] for a in u["anchors"]}):
        page = pdf[page_no - 1]
        rects = [pymupdf.Rect(a["bbox"]) for a in u["anchors"] if a["page"] == page_no]
        box = rects[0]
        for x in rects[1:]:
            box |= x
        doc = pymupdf.open()
        pg = doc.new_page(width=page.rect.width, height=page.rect.height)
        pg.show_pdf_page(pg.rect, pdf, page_no - 1)
        for x in rects:
            pg.draw_rect(x + (-2, -2, 2, 2), color=(0.85, 0.1, 0.1), width=1.2)
        clip = pymupdf.Rect(20, max(box.y0 - 36, 0), page.rect.width - 20, min(box.y1 + 36, page.rect.height))
        f = dest / f"{safe}-p{page_no}.png"
        pg.get_pixmap(dpi=DPI, clip=clip).save(f)
        out.append({"unit": uid, "page": page_no, "file": f"{dest.name}/{f.name}"})
    return out


def _ops_by_id(r: dict) -> dict:
    return {x.op.id: (s, x) for s in r["stages"] for x in s.ops}


def _ref(r: dict, uid: str) -> str:
    u = next((x for x in r["units"] if x["unit_id"] == uid), None)
    if not u:
        return uid
    doc, _, local = uid.partition(":")
    return f"{doc} {local} p{','.join(str(p) for p in u.get('pages') or [])}"


def show_row(r: dict, row_id: str, to: Path, build_dir: Path) -> tuple[str, Path]:
    e = next(x for x in r["evals"] if x["row"].id == row_id)
    row, order, val = e["row"], r["order"], r["validated"].stage
    rv = r["reviews"][("row", row_id)]
    ops = _ops_by_id(r)
    last = e["stages"][order[-1]]
    lines = [f"{row.id}  {row.requirement}",
             f"  owner {row.owner_role} | {row.assessment} | scope {', '.join(row.scope)} | confidence {row.confidence}",
             f"  evidence: " + (", ".join(f"{k} ({r['evidence_items'][k].envelope}, issuer {r['evidence_items'][k].issuer})"
                                         if k in r["evidence_items"] else k for k in row.evidence)
                                or f"none: {row.no_deliverable}"),
             f"  review: {review.label(rv)} (fingerprint {rv['fingerprint'][:16]})",
             f"  issues: {', '.join(row.issues) or 'none'}"]
    if r.get("relationships"):                                   # session 10: curated links naming this row
        from .stage2 import relationship_lines
        rel = relationship_lines(r).get(row_id, [])
        lines += ["  relationships:"] + [f"    {x}" for x in rel] if rel else []
    lines += ["", "  stage      status / quote / consequence / dates"]
    for st in order:
        ev = e["stages"][st]
        it = r["register"].interp_at(row, st)
        cons = it.consequence if it else None
        lines.append(f"  {st:<9}  {ev['status']}" + ("  STALE: " + "; ".join(ev["stale"]) if ev["stale"] else ""))
        if _in_force(ev["status"]) and it:
            lines.append(f"             quote: “{it.quote}”")
            if isinstance(cons, Consequence):
                lines.append(f"             consequence ({cons.cls}): “{cons.quote}” [{cons.unit}]")
            for d in ev["dates"]:
                lines.append(f"             date {d['rule_id']}: {d['planning']['value']} ({d['planning']['key']})"
                             + (f"  [{d['reread']}]" if d.get("reread") else ""))
    src = last.get("source") or {}
    lines += ["", f"  latest reference: {src.get('latest', '')}", "  source units:"]
    dest = to / row_id
    if dest.exists():
        shutil.rmtree(dest)
    crops: list[dict] = []
    cu = [it.consequence.unit for it in row.interpretations if isinstance(it.consequence, Consequence)]
    for uid in dict.fromkeys([*row.units, *cu]):
        c = crop_unit(r, uid, dest / "img", build_dir)
        crops += c
        lines.append(f"    {_ref(r, uid)}" + (f"  crop: {dest / c[0]['file']}" if c else "  (no page anchor: created by an op)"))
    lines += ["", "  amendment chain:"]
    chain = list(dict.fromkeys(last.get("ops") or []))
    if not chain:
        lines.append("    none (as issued)")
    def _held(x):                                        # session 11: conditional (held), or withheld by a rejection
        if getattr(x, "conditional_pending", False):
            from .partial import conditional_label
            return conditional_label(r, x)
        return "WITHHELD (rejected)"
    for oid in chain:
        s, x = ops[oid]
        o = x.op
        what = {"replace_text": lambda: f"'{o.old}' -> '{o.new}'", "set_value": lambda: f"{o.column}: -> {o.new}",
                "set_status": lambda: o.status, "replace_unit": lambda: f"replaced by {o.replacement}",
                "insert_unit": lambda: f"inserted {o.new_group or ''} after {o.anchor or ''}".strip(),
                "insert_row": lambda: f"row {o.cells} inserted in {o.target} after {o.after or 'the last row'}",
                "append_text": lambda: f"+ '{o.new}'", "annotate": lambda: f"{o.effect}: {o.note or ''}"}[o.type]()
        lines.append(f"    {oid} [{s.stage}] {o.type}: {what}  ({_ref(r, o.provision)}; "
                     f"{('applied' if x.applied else _held(x)) if x.valid else 'INVALID'}; "
                     f"{r['reviews'][('op', oid)]['status']})")
        crops += crop_unit(r, o.provision, dest / "img", build_dir)
    final = r["stages"][-1].state
    notes = list(dict.fromkeys(a for uid in row.units if uid in final for a in final[uid].annotations))
    if notes:
        lines += ["  clarifications and rules annotating its units:"]
        for oid in notes:
            s, x = ops[oid]
            lines.append(f"    {oid} [{s.stage}] {x.op.effect}: {(x.op.note or '')[:160]} ({_ref(r, x.op.provision)}; "
                         f"{r['reviews'][('op', oid)]['status']})")
    prog = programme.stage_planner(r, val)(r["assumptions"])
    acts = [a for a in prog["activities"] if row_id in a["req_ids"]]
    lines += ["", f"  A5 at {val} (status date {prog['status_date']}):"]
    lines += [f"    {a['id']}: {a['status']}; latest start {a['latest_start']}, finish {a['latest_finish']}; "
              f"{a['duration_wd']} WD ({a['duration_assumption']})" for a in acts] or ["    no activity (see evidence / no_deliverable)"]
    text = "\n".join(lines)
    page = ["<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,"
            " initial-scale=1\"><title>" + html.escape(row_id) + "</title><style>body{font-family:system-ui,sans-serif;margin:16px;"
            "background:#fff;color:#111}pre{white-space:pre-wrap;font-size:13px}figure{margin:10px 0}img{max-width:100%;"
            "border:1px solid #ccc}figcaption{font-size:12px;color:#444}</style></head><body>",
            f"<h1>{html.escape(row_id)}</h1><pre>{html.escape(text)}</pre><h2>Source crops</h2>"]
    for c in crops:
        page.append(f"<figure><img src=\"{html.escape(c['file'])}\" alt=\"{html.escape(c['unit'])}\">"
                    f"<figcaption>{html.escape(_ref(r, c['unit']))}</figcaption></figure>")
    page.append("</body></html>\n")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.html").write_text("".join(page), encoding="utf-8")
    return text, dest / "index.html"


def _unit_changes(sa: dict, sb: dict, uid: str) -> list[dict]:
    """How one unit a row cites changed between two stage states, as [{"unit", "change", "ops", "now", "detail"}].
    Compared: whether it is issued, its status, text and cells, its effective replacement (followed through superseded
    units, so a replacement amended or replaced again is seen) and the annotations on it and on its replacement."""
    from .register import effective
    ua, ub = sa.get(uid), sb.get(uid)
    if ub is None or ub.status == "not_issued":
        return [{"unit": uid, "change": "no longer exists", "ops": []}] if ua is not None and ub is None else []
    new_ops = lambda a, b: [h for h in (b.history if b else []) if h not in (a.history if a else [])]  # noqa: E731
    if ua is None or ua.status == "not_issued":
        return [{"unit": uid, "change": "issued", "ops": new_ops(ua, ub)}]
    out, ops = [], new_ops(ua, ub)
    if ua.status != ub.status:
        change = {"superseded": "replaced", "active": "reinstated"}.get(ub.status, ub.status)
        out.append({"unit": uid, "change": change, "ops": ops,
                    "now": ub.superseded_by if ub.status == "superseded" else None})
    elif (ua.text, ua.cells) != (ub.text, ub.cells):
        cells = [f"{k}: {(ua.cells or {}).get(k)} -> {v}" for k, v in (ub.cells or {}).items() if (ua.cells or {}).get(k) != v]
        out.append({"unit": uid, "change": "amended", "ops": ops, "detail": "; ".join(cells) or "wording"})
    ea, eb = effective(sa, uid, True), effective(sb, uid, True)
    pairs = [(ua, ub)]
    if ua.status == ub.status == "superseded" and eb is not None and eb.unit_id != uid:
        if ea is None or ea.unit_id != eb.unit_id:
            out.append({"unit": uid, "change": f"replaced earlier; now in force as {eb.unit_id} (was "
                        f"{ea.unit_id if ea is not None else 'none'})", "ops": new_ops(ea, eb)})
        else:
            pairs.append((ea, eb))
            if (ea.status, ea.text, ea.cells) != (eb.status, eb.text, eb.cells):
                out.append({"unit": uid, "change": f"replaced earlier; its replacement {eb.unit_id} "
                            + ("amended" if ea.status == eb.status else eb.status), "ops": new_ops(ea, eb)})
    for a_u, b_u in pairs:
        notes = [h for h in b_u.annotations if h not in a_u.annotations]
        if notes:
            out.append({"unit": uid, "change": "annotated" if b_u is ub else
                        f"replaced earlier; its replacement {b_u.unit_id} annotated", "ops": notes})
    return out


def _secondary(row, sa: dict, sb: dict) -> tuple[list[str], list[str]]:
    """Reasons and op ids for the secondary units of a row (every unit it cites after the first), grouped by change and
    op: 'secondary units VOL-II:T2-2/bod5, VOL-II:T2-2/cod replaced by ADD-03/6.1 (now ADD-03:T2-2-rev/bod5, ...)'."""
    groups: dict[tuple, list[dict]] = {}
    for uid in dict.fromkeys(row.units[1:]):
        for c in _unit_changes(sa, sb, uid):
            groups.setdefault((c["change"], tuple(c["ops"]), c.get("detail")), []).append(c)
    reasons, ops = [], []
    for (change, oids, detail), cs in groups.items():
        units = [c["unit"] for c in cs]
        now = list(dict.fromkeys(c["now"] for c in cs if c.get("now")))
        reasons.append(f"secondary unit{'s' if len(units) > 1 else ''} {', '.join(units)} {change}"
                       + (f" by {', '.join(oids)}" if oids else "") + (f" (now {', '.join(now)})" if now else "")
                       + (f" ({detail})" if detail else ""))
        ops += [o for o in oids if o not in ops]
    return reasons, ops


def diff(r: dict, frm: str | None = None, to: str | None = None) -> tuple[str, dict]:
    order = r["order"]
    to = to or order[-1]
    frm = frm or order[order.index(to) - 1]
    sto = next(s for s in r["stages"] if s.stage == to)
    sfrm = next(s for s in r["stages"] if s.stage == frm)
    md = [f"# What changed from {frm} to {to}", ""]
    data: dict = {"from": frm, "to": to}
    if sto.addendum:
        unres = [c for c in sto.coverage if c["disposition"] in ("unresolved", "UNACCOUNTED")]
        inv = [x for x in sto.ops if not x.valid]
        md += [f"## {to}: {sto.status}" + (f" (issued {sto.issued})" if sto.issued else ""), "",
               f"- ops: {len(sto.ops)} ({len(inv)} invalid); provisions: {len(sto.coverage)} ({len(unres)} unresolved)",
               f"- validated state: {r['validated'].stage}" + (" — this addendum does NOT replace it until every provision "
                                                                 "is treated and every op is valid" if sto.status != "APPLIED" else "")]
        md += [f"- UNRESOLVED {c['provision']}: {c.get('text', '')[:200]}" for c in unres]
        md += [f"- INVALID {x.op.id}: " + "; ".join(c["id"] + " " + c["detail"] for c in x.checks if not c["ok"]) for x in inv]
        md += [f"- WITHHELD {x.op.id}: rejected by a person; not applied" for x in sto.ops if x.valid and x.withdrawn]
        from .partial import conditional_label           # session 11: a held conditional op is not a rejected one
        md += [f"- CONDITIONAL {x.op.id}: {conditional_label(r, x)}" for x in sto.ops
               if getattr(x, "conditional_pending", False)]
        sc = next((x for x in r.get("summary_check", []) if x["stage"] == to), None)
        if sc is not None:                     # C28 (session 07): the cover summary is never applied, only compared
            found = [f for f in sc["findings"] if f["kind"] != "unchecked"]
            md.append(f"- cover summary vs provisions (C28, report only): "
                      + (f"{len(found)} finding(s)" if found else "no omission or contradiction found"))
            md += [f"  - {f['kind']}: {f['detail']}" for f in found]
            data["summary_check"] = sc["findings"]
        md.append("")
        from .partial import diff_lines                  # session 11: a PARTIAL `to`: validated vs candidate, and why
        cand_md, cand = diff_lines(r, to)
        md += cand_md
        if cand:
            data["candidate"] = cand
    # ---- requirements
    new, gone, changed, secondary = [], [], [], {}
    for e in r["evals"]:
        a, b = e["stages"][frm], e["stages"][to]
        fa, fb = _in_force(a["status"]), _in_force(b["status"])
        rid = e["row"].id
        why = [h for h in (b.get("ops") or []) if h not in (a.get("ops") or [])]
        if fb and not fa:
            new.append((rid, b["status"], why))
        elif fa and not fb:
            gone.append((rid, b["status"], why))
        elif fa and fb:
            what = []
            if a["text"] != b["text"]:
                what.append("wording")
            if (a.get("interpretation") or {}).get("quote") != (b.get("interpretation") or {}).get("quote"):
                what.append("quoted words")
            da = {d["rule_id"]: d["planning"]["value"] for d in a["dates"]}
            db = {d["rule_id"]: d["planning"]["value"] for d in b["dates"]}
            what += [f"{k} {da.get(k)} -> {v}" for k, v in db.items() if da.get(k) != v]
            sec, sec_ops = _secondary(e["row"], sfrm.state, sto.state)     # every other unit the row cites
            what += sec
            why += [h for h in sec_ops if h not in why]
            if sec:
                secondary[rid] = sec
            if what or why:
                changed.append((rid, b["status"], why, what))
    md += ["## Requirements", "", f"- new: {len(new)}; out of force: {len(gone)}; changed: {len(changed)}", ""]
    md += [f"- NEW {rid}: {st}" + (f" (by {', '.join(w)})" if w else "") for rid, st, w in new]
    md += [f"- OUT {rid}: {st}" for rid, st, _ in gone]
    md += [f"- CHANGED {rid}: {'; '.join(w) or 'amended'}" + (f" (by {', '.join(o)})" if o else "") for rid, st, o, w in changed]
    data["requirements"] = {"new": [x[0] for x in new], "out": [x[0] for x in gone], "changed": [x[0] for x in changed],
                            "secondary": secondary}
    # ---- stale interpretations, voided decisions, image-read values changed
    stale = [(e["row"].id, e["stages"][to]["stale"]) for e in r["evals"] if e["stages"][to]["stale"]]
    carried = {e["row"].id for e in r["evals"] if e["stages"][frm]["stale"]}
    md += ["", "## Stale readings and decisions", ""]
    md += [f"- STALE {rid}" + (" (already stale before)" if rid in carried else "") + f": {'; '.join(why)[:220]}"
           for rid, why in stale] or ["- no row is STALE"]
    voided = [k[1] for k, v in r["reviews"].items() if v["status"] == "changed"]
    md += [f"- DECISION VOID (content changed since review): {', '.join(voided)}"] if voided else []
    img = []
    for x in sto.ops:
        if x.applied and x.op.type == "set_value" and x.details.get("reading_status"):
            img.append(f"{x.op.target} {x.op.column}: image shows {x.details.get('old_value')}, {to} makes it {x.op.new} "
                       f"(reading {x.details['reading_status']}; the image itself is unchanged)")
    md += [f"- IMAGE-READ VALUE CHANGED: {t}" for t in img]
    data["stale"] = [x[0] for x in stale]
    # ---- obligations through the outputs (C46)
    tr = [t for t in r.get("trace", []) if t["stage"] == to]
    md += ["", "## Obligations not reaching the outputs (C46)", ""]
    md += [f"- {t['op']} [{t['output']}]: {t['detail'][:240]}" for t in tr] or ["- none"]
    # ---- relationships (session 10): what the change reaches through other provisions; never merged with the above
    if r.get("relationships"):
        consecutive = order.index(to) - order.index(frm) == 1
        imp = (r.get("relationship_impact") or {}).get(to) if consecutive else None
        imp = imp if imp is not None else relationships.impact_between(r, frm, to)
        recs = imp["records"]
        md += ["", "## Reached through relationships (indirect: for review, not direct citations)", "",
               "Curated links (relationships file) followed from what changed. The requirements above cite a changed "
               "unit; these are reached through another provision, in three classes that are never merged. A5 marks the "
               "activities that serve them REVIEW with their dates unchanged.", ""]
        data["relationships"] = {}
        for cls, items in relationships.by_class(recs):
            md.append(f"### {cls[0].upper() + cls[1:]} ({len(items)})")
            md += [f"- {relationships.label(x)}" for x in items] or ["- none"]
            md.append("")
            data["relationships"][cls] = sorted({x["target"] for x in items})
        gp = relationships.gaps(recs)
        md.append(f"### Referenced but not supplied: conclusions in play that cannot be established ({len(gp)})")
        md += [f"- {relationships.label(x, r['relationships'])}" for x in gp] or ["- none"]
        data["relationships"]["not supplied"] = sorted({x["target"] for x in gp})
    # ---- A3
    def a3set(st):
        out = {}
        for e in r["evals"]:
            if not _in_force(e["stages"][st]["status"]):
                continue
            it = r["register"].interp_at(e["row"], st)
            c = it.consequence if it else None
            if isinstance(c, Consequence) and c.cls in BID_OUT:
                out[e["row"].id] = (c.cls, c.quote)
        return out
    xa, xb = a3set(frm), a3set(to)
    md += ["", "## Disqualifiers (A3)", ""]
    md += [f"- ENTERS {k}: {v[0]} “{v[1]}”" for k, v in xb.items() if k not in xa]
    md += [f"- LEAVES {k}" for k in xa if k not in xb]
    md += [f"- CHANGES {k}: {xa[k][0]} -> {v[0]} “{v[1]}”" for k, v in xb.items() if k in xa and xa[k] != v]
    if md[-1] == "":
        md.append("- no change")
    data["a3"] = {"enters": [k for k in xb if k not in xa], "leaves": [k for k in xa if k not in xb]}
    # ---- programme
    try:
        pa = programme.stage_planner(r, frm)(r["assumptions"])
        pb = programme.stage_planner(r, to)(r["assumptions"])
    except Exception as err:                                   # noqa: BLE001  (e.g. a stage before any planning date)
        md += ["", "## Programme impact", "", f"- not planned at both stages: {err}"]
        return "\n".join(md) + "\n", data
    ea = {e["row"].id: e["stages"][frm] for e in r["evals"]}
    eb = {e["row"].id: e["stages"][to] for e in r["evals"]}
    dl = deltas(pa, pb, ea, eb)
    sa = {a["id"]: a["status"] for a in pa["activities"]}
    md += ["", f"## Programme impact (status date {pa['status_date']} -> {pb['status_date']})", ""]
    md += [f"- {d['change']} {d['activity']}: {d['detail']}" for d in dl] or ["- no activity changes"]
    md += [f"- FEASIBILITY {a['id']}: {sa.get(a['id'], 'absent')} -> {a['status']}" for a in pb["activities"]
           if sa.get(a["id"]) != a["status"] and a["status"] != "OK" or (sa.get(a["id"], "OK") != "OK" and a["status"] == "OK")]
    ta = {t["envelope"]: t for t in pa["documents"]["totals"]}
    for t in pb["documents"]["totals"]:
        o = ta.get(t["envelope"], {})
        if (o.get("items"), o.get("physical_count")) != (t["items"], t["physical_count"]):
            md.append(f"- ENVELOPE {t['envelope']}: items {o.get('items')} -> {t['items']}, physical copies "
                      f"{o.get('physical_count')} -> {t['physical_count']}")
    data["programme"] = dl
    return "\n".join(md) + "\n", data
