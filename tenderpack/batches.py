"""Review batches for the owner (session 06): what to look at, what exactly to decide, and the command to record it.

  out/review/index.html                       the batches, their counts and review status, how decisions work
  out/review/batch-01-image-readings.html     the two image readings: crops beside each read row/band, the points
                                              for decision, `tenderpack approve` (or correct the reading)
  out/review/packets/<region>.html            the full Stage 1 packet of each reading (every band, cell and numeral
                                              at native resolution, Arabic right to left), copied from the evidence
                                              build so the folder is complete on its own (session 07)
  out/review/batch-02-disqualifiers.html      every A3 row: crops of its source units beside the quote and the
                                              consequence, the decision, `tenderpack accept | reject`
  out/review/batch-03-amendments.html         every amendment op: the provision's crop beside the target's, the
                                              change, its checks, the decision
  out/review/batch-04-stale-proposals.html    the prepared proposals for STALE rows: what changed, the proposal,
                                              `tenderpack apply-proposal` then `accept`
  out/review/batch-05..                       the remaining rows, by document, ~40 per batch (text only)
  out/review/items.csv / items.json           every item: batch, kind, id, status, fingerprint, decision, command
Nothing here decides anything. Each item shows its current review status and the fingerprint a decision binds to.
"""
from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

from . import review
from .live import crop_unit
from .proposals import is_applied, load_proposals
from .packets import _tagged
from .register import Consequence, consequence_gloss

CSS = ("body{font-family:system-ui,sans-serif;margin:16px;max-width:1200px;color:#111;background:#fff}"
       "h1{font-size:22px}h2{font-size:17px;margin-top:26px;border-bottom:1px solid #ccc}"
       ".item{border:1px solid #ccc;border-radius:6px;padding:10px 12px;margin:14px 0}"
       ".grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px}"
       "@media (max-width:760px){.grid{grid-template-columns:1fr}}"
       "img{max-width:100%;border:1px solid #bbb}figure{margin:6px 0}figcaption{font-size:12px;color:#444}"
       "code,pre{background:#f4f4f4;padding:2px 4px;border-radius:3px;white-space:pre-wrap;word-break:break-word}"
       ".decide{background:#fff7d6;padding:6px 8px;border-left:3px solid #c90}"
       ".st{font-size:12px;padding:1px 6px;border-radius:9px;background:#eee}.st.accepted{background:#d7f5d7}"
       ".st.changed,.st.rejected{background:#fde0e0}td,th{border:1px solid #ccc;padding:3px 6px;font-size:13px;"
       "vertical-align:top;text-align:left}table{border-collapse:collapse}[dir=rtl]{font-size:16px}")


def _e(t) -> str:
    return html.escape(str(t if t is not None else ""), quote=False)


def _page(title: str, intro: str, body: list[str]) -> str:
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" "
            f"content=\"width=device-width, initial-scale=1\"><title>{_e(title)}</title><style>{CSS}</style></head><body>"
            f"<p><a href=\"index.html\">All batches</a></p><h1>{_e(title)}</h1><p>{intro}</p>" + "".join(body) + "</body></html>\n")


def _fig(c: dict, caption: str) -> str:
    return f'<figure><img src="{_e(c["file"])}" alt="{_e(caption)}" loading="lazy"><figcaption>{_e(caption)}</figcaption></figure>'


def _status(st: dict) -> str:
    return f'<span class="st {st["status"]}">{_e(review.label(st))}</span> <small>fingerprint {st["fingerprint"][:16]}</small>'


def _cmd_row(rid: str) -> str:
    return (f'<pre>python -m tenderpack accept {rid} --reviewer "Your Name" [--note "..."]\n'
            f'python -m tenderpack reject {rid} --reviewer "Your Name" --note "what is wrong"</pre>')


def _packet_link(build_dir: Path, out: Path, rg: str) -> str:
    """The Stage 1 review packet of a reading (every band, cell and numeral at native resolution, Arabic right to
    left; self-contained HTML) copied next to the batches so the review folder is complete on its own (session 07)."""
    src = Path(build_dir) / "review" / rg / "packet.html"
    if not src.exists():
        return f"<p>Full packet: not found in the evidence build ({_e(str(src))}); run <code>make evidence</code>.</p>"
    (out / "packets").mkdir(exist_ok=True)
    shutil.copyfile(src, out / "packets" / f"{rg}.html")
    return (f'<p><a href="packets/{_e(rg)}.html">Full packet for {_e(rg)}</a>: every band, cell and numeral at native '
            "resolution beside its reading (Arabic shown right to left); the crops below are the same regions, one per "
            "unit. Scroll sideways in the packet: crops are kept at native size so diacritics and decimal points stay "
            "visible.</p>")


def _confidence_reason(r: dict, row) -> str:
    """The confidence reason as A1 prints it (one wording for one approval; stage2.confidence_reason)."""
    from .stage2 import confidence_reason
    return confidence_reason(r, row)


def batch4_intro(statuses: list[str], accepted: int) -> str:
    """The batch-04 header, counted from the proposals' states (session 12, audit R-3: a fixed "Prepared, not applied
    and not accepted" stood above cards that said "Applied."). `statuses`: one per proposal ("applied", "superseded",
    "not applied"); `accepted`: how many of their rows a person has accepted (a recorded decision)."""
    n = {s: statuses.count(s) for s in ("applied", "superseded", "not applied")}
    return (f"{len(statuses)} proposal(s): {n['applied']} applied, {n['superseded']} superseded (never applied, kept for "
            f"the record only), {n['not applied']} not applied; their rows: {accepted} accepted by a person. Applying a "
            "proposal writes the interpretation and pins it; the row is then PROPOSED and needs your decision. Applied is "
            "not accepted.")


def write_batches(r: dict, out: Path, build_dir: Path) -> dict:
    out = Path(out)
    if out.exists():
        shutil.rmtree(out)
    img = out / "img"
    img.mkdir(parents=True)
    units = {u["unit_id"]: u for u in r["units"]}
    val = r["validated"].stage
    rv = r["reviews"]
    items: list[dict] = []
    crops_cache: dict[str, list[dict]] = {}

    def crops(uid: str) -> list[dict]:
        if uid not in crops_cache:
            crops_cache[uid] = crop_unit(r, uid, img, build_dir)
        return crops_cache[uid]

    # ------------------------------------------------------------------ batch 1: image readings
    body = []
    regions = sorted({u["reading"]["region"] for u in r["units"] if (u.get("reading") or {}).get("region")})
    for rg in regions:
        packet = json.loads((build_dir / "review" / rg / "packet.json").read_text(encoding="utf-8")) \
            if (build_dir / "review" / rg / "packet.json").exists() else {}
        rus = [u for u in r["units"] if (u.get("reading") or {}).get("region") == rg and u["kind"] != "region"]
        status = rus[0]["reading"]["status"] if rus else "?"
        appr = packet.get("approval") if status == "approved" else None
        tr_label = (f"confirmed as displayed by {appr.get('reviewer')}, {appr.get('date')}" if appr
                    else "proposed, not reviewed")
        rows = []
        for u in rus:
            cs = crops(u["unit_id"])
            cells = u.get("cells")
            if cells:                                   # the table's printed column order, not the stored key order
                order = (u.get("context") or {}).get("column_headings") or list(cells)
                cells = {k: cells[k] for k in [*order, *[c for c in cells if c not in order]] if k in cells}
            read = ("<table>" + "".join(f"<tr><th>{_e(k)}</th><td>{_e(v)}</td></tr>" for k, v in cells.items()) + "</table>") \
                if cells else (f'<p dir="{"rtl" if u.get("lang") == "ar" else "ltr"}">{_e(u.get("text"))}</p>'
                               + (f"<p><i>translation ({tr_label}):</i> {_e(u['translation'])}</p>" if u.get("translation") else ""))
            unc = "".join(f"<li>{_e(_tagged(x, appr))}</li>" for x in (u.get("uncertain") or []))   # R-8: settled points
            rows.append(f'<div class="item"><b>{_e(u["unit_id"])}</b><div class="grid"><div>'
                        + "".join(_fig(c, f"{u['unit_id']} (page {c['page']})") for c in cs)
                        + f"</div><div>{read}" + (f"<ul>{unc}</ul>" if unc else "") + "</div></div></div>")
        decisions = "".join(f"<li>{_e(_tagged(d, appr))}</li>" for d in packet.get("decisions") or [])
        if appr:
            from .packets import approval_scope_html
            from .readings import approval_scope_line
            box = (f'<div class="decide"><b>Approved by {_e(appr.get("reviewer"))} on {_e(appr.get("date"))}</b> for '
                   f"review subject <code>{_e(packet.get('subject_sha256', '')[:16])}</code> (this reading and its evidence, "
                   "exactly as shown here). No decision is needed unless the reading changes: any change makes it pending "
                   "again, and <code>tenderpack approve</code> then shows the differences before an approval can be "
                   "extended. " + _e(approval_scope_line(appr, any(u.get("translation") for u in rus)))   # session 12 (R-2)
                   + approval_scope_html({"status": "approved", **appr})
                   + "<p>Points the reading itself records as uncertain (kept as recorded):</p>"
                   f"<ul>{decisions}</ul></div>")
        else:
            box = (f'<div class="decide"><b>Decision needed:</b> does each crop show exactly what is read beside it '
                   f"(every word, digit and cell)? Then approve the reading, or correct "
                   f"<code>curation/readings/{_e(rg)}.yaml</code> and re-run <code>make evidence</code>. Points to check:"
                   f"<ul>{decisions}</ul><pre>python -m tenderpack approve {_e(rg)} --reviewer \"Your Name\" "
                   f"[--notes \"...\"]</pre></div>")
        body.append(f"<h2>{_e(rg)}: {_e(packet.get('doc', ''))} page {_e(packet.get('page', ''))} — reading {_e(status)}</h2>"
                    + box + _packet_link(build_dir, out, rg) + "".join(rows))
        items.append({"batch": 1, "kind": "reading", "id": rg, "status": status, "fingerprint": packet.get("subject_sha256", ""),
                      "decision": (f"approved by {appr.get('reviewer')} ({appr.get('date')}); none unless it changes" if appr
                                   else "approve the reading (or correct it)"),
                      "command": "" if appr else f'python -m tenderpack approve {rg} --reviewer "Your Name"'})
    (out / "batch-01-image-readings.html").write_text(_page(
        "Batch 1 — the two image readings", "A reading is a transcription, with any translation displayed beside it; what a "
        "value means is decided in the rows. "
        "An approval pins the reading and its evidence; any later change makes it pending again.", body), encoding="utf-8")

    # ------------------------------------------------------------------ batch 2: disqualifiers (A3 rows)
    body, done, classes = [], set(), {}
    for e in r["evals"]:
        row, ev = e["row"], e["stages"][val]
        it = r["register"].interp_at(row, val)
        c = getattr(it, "consequence", None)
        if not (isinstance(c, Consequence) and ev["status"]
                and not ev["status"].startswith(("NOT ISSUED", "NOT IN FORCE", "DELETED", "REVOKED", "REMOVED"))
                and c.cls in ("rejection", "disqualification", "non_responsive", "exclusion", "score_elimination",
                              "document_refusal", "criterion_zero")):          # every class A3 lists (session 09)
            continue
        done.add(row.id)
        classes[c.cls] = classes.get(c.cls, 0) + 1
        st = rv[("row", row.id)]
        chain = [r["register"]._op_by_id(h) for h in (ev.get("ops") or [])]
        provs = [x.op.provision for x in chain if x is not None]           # the amending provisions, beside the original
        cs = [x for u in list(dict.fromkeys([*row.units[:3], c.unit, *provs]))[:7] for x in crops(u)]
        failing = {"document_refusal": "a refusal of the document (what then follows for the Proposal is not stated: "
                                       "the row stays in the VOL-I 11.1(i) pass or fail check)",
                   "criterion_zero": "zero marks under one scoring criterion (scored, not a disqualification)"}
        decide = (f"Accept that <b>{_e(row.requirement)}</b> is required as quoted, and that failing it is "
                  f"<b>{_e(failing.get(c.cls, c.cls.replace('_', '-')))}</b> under the words “{_e(c.quote)}” "
                  f"({_e((ev.get('consequence_source') or {}).get('latest', c.unit))}). Otherwise reject it with what is wrong.")
        extra = []
        if ev["stale"]:
            extra.append("STALE: " + "; ".join(ev["stale"]))
        if ev["transcription"] == "pending":
            extra.append("relies on an image reading pending your review (batch 1)")
        if row.issues:
            extra.append("issues: " + ", ".join(row.issues))
        body.append(f'<div class="item" id="{_e(row.id)}"><b>{_e(row.id)}</b> {_status(st)}<div class="grid"><div>'
                    + "".join(_fig(x, f"{x['unit']} (page {x['page']})") for x in cs)
                    + f"</div><div><p>{_e(row.requirement)}</p><p>Quote at {val}: “{_e(it.quote if it else '')}”</p>"
                    f"<p>Consequence: <i>{_e(c.cls)}</i> “{_e(c.quote)}”"            # gloss label: the approval state
                    + (f" ({_e(consequence_gloss(r, row, c))}: ‘{_e(c.gloss)}’)" if c.gloss else "")
                    + f"</p><p>Latest source: {_e((ev.get('source') or {}).get('latest', ''))}; confidence {_e(row.confidence)}: "
                    f"{_e(_confidence_reason(r, row))}</p>" + "".join(f"<p><small>{_e(x)}</small></p>" for x in extra)
                    + f'<div class="decide"><b>Decision needed:</b> {decide}</div>{_cmd_row(row.id)}</div></div></div>')
        items.append({"batch": 2, "kind": "row", "id": row.id, "status": st["status"], "fingerprint": st["fingerprint"],
                      "decision": f"accept {row.id} as quoted with consequence {c.cls}, or reject",
                      "command": f'python -m tenderpack accept {row.id} --reviewer "Your Name"'})
    (out / "batch-02-disqualifiers.html").write_text(_page(
        "Batch 2 — what puts the bid out (A3 rows)", f"{len(done)} rows with an explicit consequence at {val} ("
        + ", ".join(f"{n} {k.replace('_', '-')}" for k, n in sorted(classes.items())) + "). "
        "A decision binds to the row, its evidence items and its dependencies; any later change voids it.", body), encoding="utf-8")

    # ------------------------------------------------------------------ batch 3: amendment ops
    body = []
    for s in r["stages"][1:]:
        body.append(f"<h2>{_e(s.stage)} — {_e(s.status)} ({len(s.ops)} ops)</h2>")
        for x in s.ops:
            o, st = x.op, rv[("op", x.op.id)]
            tgt = o.target or o.anchor or ", ".join(o.targets or [])
            change = {"replace_text": f"‘{o.old}’ → ‘{o.new}’", "set_value": f"{o.column} → ‘{o.new}’",
                      "set_status": f"{o.status}", "replace_unit": f"replaced by {o.replacement}",
                      "insert_unit": f"insert {o.new_group or ''} {('after ' + o.anchor) if o.anchor else ''}",
                      "insert_row": f"insert a row {'after ' + o.after if o.after else 'at the end'}: "
                                    + "; ".join(f"{k}: {v}" for k, v in (o.cells or {}).items()),
                      "append_text": f"append ‘{o.new}’", "annotate": f"{o.effect}: {o.note or ''}"}.get(o.type, o.type)
            cs = crops(o.provision) + [y for t in ([o.target] if o.target else []) for y in crops(t)]
            bad = [f"{c['id']}: {c['detail']}" for c in x.checks if not c["ok"]]
            body.append(f'<div class="item" id="{_e(o.id)}"><b>{_e(o.id)}</b> {_status(st)}<div class="grid"><div>'
                        + "".join(_fig(c, f"{c['unit']} (page {c['page']})") for c in cs)
                        + f"</div><div><p><b>{_e(o.type)}</b> on {_e(tgt)}: {_e(change)}</p>"
                        + (f"<p>Issue: {_e(o.issue)}</p>" if o.issue else "")
                        + f"<p>Checks: {'all pass' if x.valid else 'INVALID: ' + _e('; '.join(bad))}"
                        + (" — WITHHELD: rejected by a person, not applied" if x.withdrawn else "") + "</p>"
                        f'<div class="decide"><b>Decision needed:</b> accept that {_e(o.provision)} makes exactly this change '
                        f"to {_e(tgt)} (and nothing else), or reject it with what is wrong.</div>"
                        f'<pre>python -m tenderpack accept {_e(o.id)} --reviewer "Your Name"\n'
                        f'python -m tenderpack reject {_e(o.id)} --reviewer "Your Name" --note "what is wrong"</pre></div></div></div>')
            items.append({"batch": 3, "kind": "op", "id": o.id, "status": st["status"], "fingerprint": st["fingerprint"],
                          "decision": f"accept {o.id} ({o.type} on {tgt}) or reject",
                          "command": f'python -m tenderpack accept {o.id} --reviewer "Your Name"'})
    (out / "batch-03-amendments.html").write_text(_page(
        "Batch 3 — amendment operations", "Each op as the engine applied it. A rejected op is withdrawn and its addendum "
        "becomes PARTIAL until the provision is treated again.", body), encoding="utf-8")

    # ------------------------------------------------------------------ batch 4: proposals for STALE rows
    body = []
    rows = {x.id: x for x in r["rowfile"].rows}
    props = load_proposals(r["root"] / "curation/register/proposals")
    shown = [k for k, v in props.items() if any(x["row"].id == v["row"] for x in r["evals"])]
    for pid, p in props.items():
        e = next((x for x in r["evals"] if x["row"].id == p["row"]), None)
        if e is None:
            continue
        # session 12 (F5; audit R-c): where the replacement stands on this page, from the order the cards are printed in
        rep = p.get("superseded_by")
        where = (" (above)" if shown.index(rep) < shown.index(pid) else " (below)") if rep in shown else ""
        st = rv[("row", p["row"])]
        applied = is_applied(p, rows)
        superseded = p.get("status") == "superseded"
        ai = p.get("add_interpretation") or {}
        body.append(f'<div class="item" id="{_e(pid)}"><b>{_e(pid)}</b> for {_e(p["row"])} {_status(st)}'
                    f"<p>Why it is STALE: {_e('; '.join(e['stages'][val]['stale']) or 'not stale now')}</p>"
                    f"<p>Changed: {_e(p.get('changed_dependency'))}</p><p>Proposed {_e(ai.get('stage'))} interpretation: "
                    f"“{_e(ai.get('quote'))}”</p><p>{_e(ai.get('note'))}</p><p>Effect: {_e(p.get('effect'))}</p>"
                    + (f"<p><b>Owner's direction:</b> {_e(p['direction'])}</p>" if p.get("direction") else "")
                    + ("<p><b>Source evidence:</b></p><ul>" + "".join(
                        f"<li>{_e(x.get('unit'))}" + (f" p{x['page']}" if x.get("page") else "") + f": “{_e(x.get('words'))}”</li>"
                        for x in p["evidence"]) + "</ul>" if p.get("evidence") else "")
                    + (f"<p><b>Requirement corrected:</b> “{_e(p['replace_requirement']['old'])}” → "
                       f"“{_e(p['replace_requirement']['new'])}”</p>" if p.get("replace_requirement") else "")
                    + (f"<p><b>Supersedes</b> {_e(p['supersedes'])}.</p>" if p.get("supersedes") else "")
                    + ("<p><b>Why it was superseded (exact conflict with the owner's direction):</b></p><ul>"
                       + "".join(f"<li>{_e(x)}</li>" for x in p["superseded_because"]) + "</ul>"
                       if p.get("superseded_because") else "")
                    + (f'<div class="decide"><b>Superseded, never applied:</b> replaced by {_e(rep)}{where}. '
                       f'Kept for the record; it cannot be applied.</div></div>'
                       if superseded else
                       f'<div class="decide"><b>Decision needed:</b> {_e(p.get("decision_needed"))}</div>'
                       f"<p>{'Applied.' if applied else 'Not applied.'}</p>"
                       # an applied proposal needs no apply command (it is done); the row's accept stays a person's
                       + ("<pre>" if applied else f'<pre>python -m tenderpack apply-proposal {_e(pid)} --by "Your Name"\n')
                       + f'python -m tenderpack accept {_e(p["row"])} --reviewer "Your Name"</pre></div>'))
        items.append({"batch": 4, "kind": "proposal", "id": pid,
                      "status": "superseded" if superseded else "applied" if applied else "not applied",
                      "fingerprint": st["fingerprint"],
                      "decision": f"none: superseded by {p.get('superseded_by')}" if superseded
                      else p.get("decision_needed", ""),
                      "command": "" if superseded or applied else f'python -m tenderpack apply-proposal {pid} --by "Your Name"'})
    b4 = [x for x in items if x["batch"] == 4]
    accepted = sum(1 for p in props.values() if p.get("row") in rows and rv.get(("row", p["row"]), {}).get("status") == "accepted")
    (out / "batch-04-stale-proposals.html").write_text(_page(
        "Batch 4 — proposals for the STALE rows", batch4_intro([x["status"] for x in b4], accepted), body), encoding="utf-8")

    # ------------------------------------------------------------------ batches 5+: the remaining rows
    rest = [e for e in r["evals"] if e["row"].id not in done]
    rest.sort(key=lambda e: (e["row"].id.split("-")[0] + "-" + e["row"].id.split("-")[1], e["row"].id))
    n = 5
    for i in range(0, len(rest), 40):
        chunk, body = rest[i:i + 40], []
        for e in chunk:
            row, ev = e["row"], e["stages"][val]
            it = r["register"].interp_at(row, val)
            st = rv[("row", row.id)]
            c = getattr(it, "consequence", None)
            body.append(f'<div class="item" id="{_e(row.id)}"><b>{_e(row.id)}</b> {_status(st)} <small>{_e(ev["status"])}'
                        f"{' — STALE' if ev['stale'] else ''}</small><p>{_e(row.requirement)}</p>"
                        f"<p>Quote: “{_e(it.quote if it else '')}” — {_e((ev.get('source') or {}).get('latest', ''))}</p>"
                        + (f"<p>Consequence: <i>{_e(c.cls)}</i> “{_e(c.quote)}”</p>" if isinstance(c, Consequence) else "")
                        + f"<p><small>{_e(row.assessment)}; owner {_e(row.owner_role)}; evidence {_e(', '.join(row.evidence) or row.no_deliverable)}"
                        f"; confidence {_e(row.confidence)}</small></p>{_cmd_row(row.id)}</div>")
            items.append({"batch": n, "kind": "row", "id": row.id, "status": st["status"], "fingerprint": st["fingerprint"],
                          "decision": f"accept {row.id} as quoted, or reject",
                          "command": f'python -m tenderpack accept {row.id} --reviewer "Your Name"'})
        first, last = chunk[0]["row"].id, chunk[-1]["row"].id
        (out / f"batch-{n:02d}-rows.html").write_text(_page(
            f"Batch {n} — rows {first} … {last}", "Text only; `python -m tenderpack show ROW-ID` gives pages, crops and the "
            "amendment chain for any row.", body), encoding="utf-8")
        n += 1

    # ------------------------------------------------------------------ index and item list
    counts: dict[int, dict] = {}
    for x in items:
        c = counts.setdefault(x["batch"], {})
        c[x["status"]] = c.get(x["status"], 0) + 1
    names = {1: "batch-01-image-readings.html", 2: "batch-02-disqualifiers.html", 3: "batch-03-amendments.html",
             4: "batch-04-stale-proposals.html"}
    lines = []
    for b in sorted(counts):
        f = names.get(b, f"batch-{b:02d}-rows.html")
        lines.append(f'<tr><td><a href="{f}">{_e(f)}</a></td><td>{sum(counts[b].values())}</td>'
                     f"<td>{_e(', '.join(f'{k} {v}' for k, v in sorted(counts[b].items())))}</td></tr>")
    idx = _page("Review batches — pending your decisions",
                "Work through the batches in order: the readings first (rows depend on them), then what puts the bid out, "
                "then the amendment ops, then the STALE-row proposals, then the remaining rows. Nothing has been approved or "
                "accepted for you. A decision is recorded only by the commands shown, with your name, and binds to the item's "
                "current content: if the item, its evidence or a dependency changes later, it needs review again. "
                "The <code>review:</code> flags in the YAML files are drafting flags and never count.",
                ["<table><tr><th>Batch</th><th>Items</th><th>Status</th></tr>" + "".join(lines) + "</table>"]
                + ([f"<p>Full review packets of the image readings (native crops beside every band and cell): "
                    + ", ".join(f'<a href="packets/{_e(q.name)}">{_e(q.stem)}</a>' for q in sorted((out / "packets").glob("*.html")))
                    + "</p>"] if (out / "packets").exists() else []))
    (out / "index.html").write_text(idx, encoding="utf-8")
    (out / "items.json").write_text(json.dumps({"items": items}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    import csv
    with open(out / "items.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["batch", "kind", "id", "status", "fingerprint", "decision", "command"])
        w.writeheader()
        w.writerows(items)
    return {"items": len(items), "batches": len(counts), "images": len(list(img.glob("*.png")))}
