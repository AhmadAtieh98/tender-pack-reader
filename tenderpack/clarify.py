"""The tender clarification register (session 08): discrepancies, ambiguities and missing information in the tender
volumes and addenda, with DRAFT questions. Nothing here is ever sent: the program only checks and publishes the
register, and a person decides what to raise through the Portal (VOL-I 5.1) before the VOL-I 5.2 cut-off.

    curation/clarifications/register.yaml   (curated data; `clarifications` in config/pack.yaml overrides the path)
      clarifications:        one entry per genuine unresolved matter: volume, clause, page, units, verbatim sources,
                             gap, what is already settled, practical impact, proposed question, interim handling,
                             decision owner, response status, linked issues, theme (the A3 group)
      checked_no_question:   topics checked that need no question because the pack's own words settle them (quoted)
      pending_decision:      proposed readings that rest on a judgment (precedence, an interpretation, an engineering
                             reading, whether an earlier answer survives): no question drafted, a decision owner named,
                             shown as HUMAN DECISION PENDING (session 12, F1; audit R-1, A4-2)
      unavailable_material:  referenced material not in the pack, its impact and handling (never a prerequisite)
    -> out/a4/clarification_register.{md,csv,json}; the A3 groups list the question ids; A1's Issues sheet links them

Checks (check-register, release gate as coverage): every quotation is verbatim in its unit's text on the stated page,
and names a unit, a page and non-blank words (session 10: an empty or whitespace quotation is found in any text, so it
is refused, never checked); every entry has the fields the owner asked for, each non-blank after stripping, including
a decision owner (whitespace is not an owner) and at least one verbatim source; the
response status is exactly one of RESPONSE_STATES (anything else, e.g. "answered", "sent" or "pending", is an unknown
state); "answered by addendum" needs `answer: {unit, page, words}` quoting a unit of an addendum (ADD-) verbatim on
that page: an answer is evidence-backed only this way, and unknown answers stay unknown; linked issues exist.
Session 12: `recorded_answer: {unit, page, words}` is an addendum response the AI workflow RECORDED against a question
(checked like an answer: an Addendum unit, verbatim on that page) without changing its status; whether it resolves the
question is a human decision. A closing status ("answered by addendum", "withdrawn (not sent)") is presented as settled
only with a person's recorded decision bound to the entry (tenderpack.human_owned; `tenderpack accept CQ-...`): every
output shows the status through human_owned.clarification_status, and A5 keeps the question open until then.
The cut-off (session 09): `cut_off.date` must be the planning value of the date rule `cut_off.rule_id` (default
CLARIFICATION-CUTOFF) on the row that defines it at the validated stage, and `cut_off.note` must state the effective
time of that rule's anchor (the Proposal Due Date) and no other time. stage2 passes this as `cutoff`
(effective_cutoff), so check-register and the release gate both use the effective values.

The window (session 12): `window(r, stage)` compares an addendum's issue date with the cut-off computed at its own stage
(effective_cutoff(r, stage): the pack's date rule, never a typed date). When the addendum issues after the cut-off, the
route is closed for every question that addendum raises, and every place that would suggest a clarification says so in
one wording, CLOSED_WINDOW ('the clarification window closed on <date> (VOL-I 5.2): this question cannot be submitted as
a clarification; it is a bid-decision for a person'): the escalations and the downstream clarification proposals of the
AI workflow, the candidate A3's unresolved list, the candidate A5's clarification activity, the diff and the review
packet. A proposed entry is still written as a DRAFT ('draft, not sent') with the note beside it (`with_window`; field
`clarification_window`). When the addendum issues on or before the cut-off, nothing changes.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from . import human_owned
from .register import found
from .render import write_csv_json
from .review import _in_force
from .util import load_yaml, write_text

DEFAULT_PATH = "curation/clarifications/register.yaml"
REQUIRED = ("id", "kind", "volume", "clause", "page", "gap", "practical_impact", "proposed_question", "interim_handling",
            "decision_owner", "response_status", "theme")
RESPONSE_STATES = ("draft, not sent", "withdrawn (not sent)", "answered by addendum")
CUTOFF_RULE = "CLARIFICATION-CUTOFF"
_TIME = re.compile(r"(?<![\d:.])([01]?\d|2[0-3]):([0-5]\d)(?![\d:])")
_ZONE = re.compile(r"\b[A-Z][a-z]+ time\b")


def _hhmm(t) -> str | None:
    m = _TIME.search(str(t or ""))
    return f"{int(m.group(1)):02d}:{m.group(2)}" if m else None


def load(cfg: dict, root: Path) -> dict:
    p = Path(cfg.get("clarifications", DEFAULT_PATH))
    p = p if p.is_absolute() else root / p
    return (load_yaml(p) or {}) if p.exists() else {}


CLOSED_WINDOW = ("the clarification window closed on {date} ({rule}): this question cannot be submitted as a "
                 "clarification; it is a bid-decision for a person")


def effective_cutoff(r: dict, stage: str | None = None) -> dict | None:
    """The clarification cut-off as the evaluated register computes it, for clarify.check(cutoff=...):
    {"rule": "VOL-I 5.2", "rule_id", "row", "stage", "date": "<iso planning value>" | None, "anchor": "PDD",
     "pdd": {"date", "time", "tz", "unit", "source"}, "conflicts": [...]}.
    The date is the planning value of the date rule named by the register's `cut_off.rule_id` (default
    CLARIFICATION-CUTOFF) on the row that defines it, at the validated stage; the anchor's date, time and timezone come
    from r["anchor_details"] when stage2 computed it, else from the effective text of the anchor's defining unit.
    None when the register is empty or the evaluation is missing; a rule no row defines gives date None. `stage`
    (session 12): the stage to evaluate at (default the validated stage), e.g. a PARTIAL addendum's own stage."""
    reg = r.get("clarifications") or {}
    if not reg or "evals" not in r or "validated" not in r:
        return None
    rule_id = (reg.get("cut_off") or {}).get("rule_id") or CUTOFF_RULE
    stage = stage or r["validated"].stage
    hits = []
    for e in r["evals"]:
        rd = next((x for x in e["row"].date_rules if x.rule_id == rule_id), None)
        ev = e["stages"].get(stage) or {}
        d = next((x for x in ev.get("dates") or [] if x["rule_id"] == rule_id), None)
        if rd is not None:
            hits.append((_in_force(str(ev.get("status", ""))), e["row"].id, rd, (d or {}).get("planning", {}).get("value")))
    out = {"rule_id": rule_id, "stage": stage, "row": None, "rule": None, "date": None, "anchor": None, "pdd": {},
           "conflicts": []}
    if not hits:
        return out
    hits.sort(key=lambda h: not h[0])                       # rows in force first
    _, row_id, rd, value = hits[0]
    doc, _, local = rd.source_unit.partition(":")
    out.update(row=row_id, rule=f"{doc} {local}", date=value, anchor=rd.anchor)
    out["conflicts"] = [f"{h[1]} gives {h[3]}" for h in hits[1:] if h[0] and h[3] != value]
    ad = ((r.get("anchor_details") or {}).get(stage) or {}).get(rd.anchor)
    if ad is None and rd.anchor in r["rowfile"].anchors:    # derived here when stage2 does not provide it
        from .dates import parse_date
        from .register import effective
        uid = r["rowfile"].anchors[rd.anchor]["defined_in"]
        st = next((s for s in r.get("stages") or [] if s.stage == stage), r["validated"])
        u = effective(st.state, uid, True)
        text = u.text if u is not None and u.status == "active" else ""
        p = parse_date(text) if text else None
        z = _ZONE.search(text[text.find(p[1]):] if p and p[1] and p[1] in text else text)
        ad = {"date": p[0] if p else None, "time": p[1] if p else None, "tz": z.group(0) if z else None, "unit": uid}
    if ad:
        d = ad.get("date")
        out["pdd"] = {"date": d.isoformat() if isinstance(d, date) else d, "time": _hhmm(ad.get("time")),
                      "tz": ad.get("tz"), "unit": ad.get("unit"), "source": ad.get("source")}
    return out


def window(r: dict, stage: str) -> dict | None:
    """The clarification route for questions an addendum raises (session 12): {stage, issued, date (the cut-off computed
    at that stage), rule ('VOL-I 5.2', from the date rule's source unit), closed (issued after the cut-off), note
    (CLOSED_WINDOW filled in when closed, else '')}. None when the stage, its issue date or the cut-off is unknown."""
    s = next((x for x in r.get("stages") or [] if x.stage == stage), None)
    if s is None or not s.issued:
        return None
    eff = effective_cutoff(r if r.get("clarifications") else dict(r, clarifications={"cut_off": {}}), stage)
    if not eff or not eff.get("date"):
        return None
    rule = eff.get("rule") or "VOL-I 5.2"
    closed = str(s.issued) > str(eff["date"])
    return {"stage": stage, "issued": str(s.issued), "date": str(eff["date"]), "rule": rule, "row": eff.get("row"),
            "closed": closed, "note": CLOSED_WINDOW.format(date=eff["date"], rule=rule) if closed else ""}


def route_lines(win: dict | None) -> list[str]:
    """Markdown lines for a review packet or a diff: the closed route, once; [] when the window is open or unknown."""
    if not win or not win.get("closed"):
        return []
    return [f"- **Clarification route:** {win['note']} ({win.get('stage')} issued {win.get('issued')}; the cut-off is "
            f"computed from {win.get('row') or 'the date rule'} at that stage). No question about it is suggested as "
            "sendable; a proposed entry stays a DRAFT, not sent."]


def with_window(entry: dict, win: dict | None) -> dict:
    """A proposed clarification entry as written into the candidate: unchanged when the window is open; when it is
    closed, a copy that stays a DRAFT ('draft, not sent' unless it already says it was withdrawn or answered) with the
    note in `clarification_window`."""
    if not win or not win.get("closed"):
        return entry
    out = dict(entry, clarification_window=win["note"])
    if not str(out.get("response_status") or "").startswith(("withdrawn", "answered")):
        out["response_status"] = "draft, not sent"
    return out


def check(reg: dict, units: list[dict], issue_ids: set[str], cutoff: dict | None = None) -> list[str]:
    """Findings (strings, 'where: what'). `cutoff` (effective_cutoff) adds the cut-off checks."""
    by_id = {u["unit_id"]: u for u in units}
    out = []

    def blank(v) -> bool:
        return v is None or (isinstance(v, str) and not v.strip())

    def quotes(where: str, items) -> None:
        for q in items or []:
            if not isinstance(q, dict) or any(blank(q.get(k)) for k in ("unit", "page")):
                out.append(f"{where}: a quotation needs a unit, a page and the words; got {q!r}")
                continue
            if blank(q.get("words")):
                out.append(f"{where}: empty quotation from {q.get('unit')} p{q.get('page')}: the words are required "
                           "(an empty or whitespace quotation would be found in any text)")
                continue
            u = by_id.get(q.get("unit"))
            if u is None:
                out.append(f"{where}: unit {q.get('unit')} does not exist")
            elif not found(q.get("words", ""), u.get("text", "")):
                out.append(f"{where}: not verbatim in {q.get('unit')}: '{str(q.get('words'))[:80]}'")
            elif q.get("page") not in u.get("pages", []):
                out.append(f"{where}: {q.get('unit')} is on page(s) {u.get('pages')}, not p{q.get('page')}")

    evidenced = ("an answer is evidence-backed only by `answer: {unit, page, words}` quoting the answering Addendum "
                 "unit verbatim on that page; unknown answers stay unknown")
    seen = set()
    for c in reg.get("clarifications") or []:
        cid = c.get("id", "?")
        if cid in seen:
            out.append(f"{cid}: duplicate id")
        seen.add(cid)
        missing = [k for k in REQUIRED if blank(c.get(k))]
        if missing:
            out.append(f"{cid}: missing {missing}" + (" (blank: whitespace only)" if any(
                isinstance(c.get(k), str) and c.get(k) for k in missing) else ""))
        if not isinstance(c.get("sources"), list) or not c.get("sources"):
            out.append(f"{cid}: no sources: every question needs at least one verbatim source (unit, page, words)")
        status = c.get("response_status")
        if status not in RESPONSE_STATES:
            out.append(f"{cid}: unknown response state {status!r}: it must be exactly one of {list(RESPONSE_STATES)}"
                       + ("; the program never records a question as sent"
                          if "sent" in str(status).lower() and "not sent" not in str(status).lower() else "")
                       + ("; " + evidenced if "answer" in str(status).lower() else ""))
        ans = c.get("answer")
        if status == "answered by addendum":
            if not isinstance(ans, dict) or any(blank(ans.get(k)) for k in ("unit", "page", "words")):
                out.append(f"{cid}: response_status 'answered by addendum' without answer evidence: {evidenced}")
            elif ans.get("unit") in by_id and not str(by_id[ans["unit"]].get("doc", "")).startswith("ADD-"):
                out.append(f"{cid}: answer unit {ans.get('unit')} is not a unit of an Addendum (ADD-): {evidenced}")
            else:
                quotes(f"{cid} answer", [ans])
        elif ans:
            out.append(f"{cid}: an answer is recorded but response_status is {status!r}, not 'answered by addendum'")
        rec = c.get("recorded_answer")
        if rec is not None:                     # session 12: an addendum response recorded, the status unchanged
            if not isinstance(rec, dict) or any(blank(rec.get(k)) for k in ("unit", "page", "words")):
                out.append(f"{cid}: recorded_answer needs a unit, a page and the words; got {rec!r}")
            elif rec.get("unit") in by_id and not str(by_id[rec["unit"]].get("doc", "")).startswith("ADD-"):
                out.append(f"{cid}: recorded answer unit {rec.get('unit')} is not a unit of an Addendum (ADD-)")
            else:
                quotes(f"{cid} recorded_answer", [rec])
        bad = [i for i in c.get("linked_issues") or [] if i not in issue_ids]
        if bad:
            out.append(f"{cid}: linked issues that do not exist: {bad}")
        quotes(cid, c.get("sources"))
    for i, c in enumerate(reg.get("checked_no_question") or []):
        quotes(f"checked_no_question[{c.get('topic', i)}]", c.get("sources"))
    for i, c in enumerate(reg.get("pending_decision") or []):
        name = f"pending_decision[{c.get('topic', i)}]"
        for k in ("topic", "finding", "decision_owner"):
            if blank(c.get(k)):
                out.append(f"{name}: missing or blank {k}")
        bad = [x for x in c.get("linked_issues") or [] if x not in issue_ids]
        if bad:
            out.append(f"{name}: linked issues that do not exist: {bad}")
        if not c.get("sources"):
            out.append(f"{name}: no verbatim source")
        quotes(name, c.get("sources"))
    for i, c in enumerate(reg.get("unavailable_material") or []):
        quotes(f"unavailable_material[{c.get('item', i)}]", c.get("referenced_in"))
    if cutoff is not None and reg:
        out += _check_cutoff(reg.get("cut_off") or {}, cutoff)
    return out


def judgment_findings(reg: dict) -> list[str]:
    """Session 12 (F1; audit R-1, A4-2): `checked_no_question` entries whose own words (quotations aside) carry a closure
    or topic word of human_owned.TRIGGERS. No decision can be recorded on these entries, so none may assert one: such an
    entry belongs in `pending_decision` with the person who decides it, or must quote the pack's words that settle it.
    A regression for the curated register (tests/test_session12_content_wording.py); not a release gate, because the
    sealed rehearsal registers were written before the rule."""
    out = []
    for i, c in enumerate(reg.get("checked_no_question") or []):
        said = human_owned.triggers(human_owned.own_words(f"{c.get('topic', '')} {c.get('finding', '')}"))
        if said:
            out.append(f"checked_no_question[{c.get('topic', i)}]: its own words assert a judgment ({'; '.join(said)}): "
                       "list it under pending_decision with the person who decides it, or quote the pack's words that "
                       "settle it")
    return out


def _check_cutoff(cut: dict, eff: dict) -> list[str]:
    """The register's cut-off against the effective one (date, and the anchor's time in the note)."""
    out = []
    rid, anchor, pdd = eff.get("rule_id"), eff.get("anchor") or "anchor", eff.get("pdd") or {}
    basis = (f"{rid} on {eff.get('row')} at {eff.get('stage')}, counted from the {anchor} "
             + " ".join(str(x) for x in (pdd.get("date"), pdd.get("time"), pdd.get("tz")) if x)
             + (f" ({pdd['source']})" if pdd.get("source") else f" ({pdd['unit']})" if pdd.get("unit") else ""))
    if not cut:
        return [f"cut_off: missing; the effective cut-off is {eff.get('date')} ({basis})"]
    if eff.get("row") is None:
        return [f"cut_off: no row defines the date rule {rid}; the register's cut-off {cut.get('date')} cannot be verified"]
    if eff.get("conflicts"):
        out.append(f"cut_off: rows define {rid} with different values at {eff.get('stage')}: {eff.get('row')} gives "
                   f"{eff.get('date')}; " + "; ".join(eff["conflicts"]))
    if eff.get("date") is None:
        out.append(f"cut_off: the effective cut-off ({basis}) is not computed; the register's date {cut.get('date')} "
                   "cannot be verified")
    elif str(cut.get("date")) != eff["date"]:
        out.append(f"cut_off: date {cut.get('date')} is not the effective cut-off {eff['date']} ({basis})")
    t = pdd.get("time")
    if t:
        said = {f"{int(h):02d}:{m}" for h, m in _TIME.findall(str(cut.get("note") or ""))}
        if t not in said:
            out.append(f"cut_off: the note does not state the effective {anchor} time {t} ({basis})")
        if said - {t}:
            out.append(f"cut_off: the note states {sorted(said - {t})}, not the effective {anchor} time {t} ({basis})")
    return out


PENDING_LABEL = f"{human_owned.HUMAN_DECISION_PENDING}: no decision recorded"


def _src(items) -> str:
    return "; ".join(f"{q.get('unit')} p{q.get('page')}: “{q.get('words')}”" for q in items or [])


def write(reg: dict, out_dir: Path, decisions: list[dict] | None = None,
          pending_issues: list[dict] | None = None) -> list[Path]:
    """a4/clarification_register.{md,csv,json}: the questions, the topics closed without one, and the unavailable
    material. Deterministic. The response status is shown through human_owned.clarification_status (session 12): never
    answered or withdrawn without a person's decision bound to the entry (`decisions`, the pack's decisions file).
    `pending_issues` (session 12, F5; audit R-a): the open issues that are a person's decision not yet recorded
    (human_owned.pending_reasons), each {id, owner, text, reasons}; those no pending decision links are listed under the
    pending readings, so A4 names the same pending set as A1, A3 and a3_detail.html."""
    out_dir = Path(out_dir)
    qs = [dict(c, response_status=human_owned.clarification_status(c, decisions)) for c in reg.get("clarifications") or []]
    cut = reg.get("cut_off") or {}
    cols = [("id", "Id", 22), ("theme", "Group", 12), ("kind", "Kind", 14), ("volume", "Volume", 16),
            ("clause", "Clause", 12), ("page", "Page", 6), ("gap", "Discrepancy or gap", 60),
            ("already_settled", "Already settled (not re-asked)", 50), ("practical_impact", "Practical impact", 50),
            ("proposed_question", "Proposed question (draft)", 70), ("interim_handling", "Interim handling", 50),
            ("decision_owner", "Decision owner", 14), ("response_status", "Response status", 14),
            ("linked_issues", "Linked issues", 20), ("sources", "Sources (verbatim)", 70)]
    rows = [{**{k: c.get(k, "") for k, _, _ in cols}, "linked_issues": c.get("linked_issues") or [],
             "sources": _src(c.get("sources"))} for c in qs]
    table = {"title": "Tender clarification register — DRAFT questions, NOT SENT",
             "notice": "Draft questions only; nothing has been sent to the Authority, the hiring team or anyone else. "
                       f"Cut-off: {cut.get('rule', 'VOL-I 5.2')} = {cut.get('date', '?')}. Unknown answers stay unknown.",
             "columns": [{"key": k, "header": h, "width": w} for k, h, w in cols], "rows": rows,
             "checked_no_question": reg.get("checked_no_question") or [],
             "pending_decision": [dict(c, status=PENDING_LABEL) for c in reg.get("pending_decision") or []],
             "pending_issues": _pending_issues(reg, pending_issues),
             "unavailable_material": reg.get("unavailable_material") or []}
    if any(c.get("clarification_window") for c in qs):        # session 12: only when an entry carries it
        table["columns"].insert(-1, {"key": "clarification_window", "header": "Clarification route", "width": 50})
        for row, c in zip(rows, qs):
            row["clarification_window"] = c.get("clarification_window") or ""
    paths = write_csv_json(table, out_dir, "clarification_register")
    path = out_dir / "clarification_register.md"
    write_text(path, markdown({**reg, "clarifications": qs, "pending_issues": _pending_issues(reg, pending_issues)}))
    return paths + [path]


def _pending_issues(reg: dict, pending: list[dict] | None) -> list[dict]:
    """The pending issues no pending decision of the register links (those are listed with their topic)."""
    linked = {i for c in reg.get("pending_decision") or [] for i in c.get("linked_issues") or []}
    return [dict(x, status=PENDING_LABEL) for x in pending or [] if x.get("id") not in linked]


def markdown(reg: dict) -> str:
    """The register as markdown (a4/clarification_register.md)."""
    qs = reg.get("clarifications") or []
    cut = reg.get("cut_off") or {}
    table = {"checked_no_question": reg.get("checked_no_question") or [],
             "pending_decision": reg.get("pending_decision") or [],
             "unavailable_material": reg.get("unavailable_material") or []}
    md = ["# Tender clarification register (A4 supporting record)", "",
          "**DRAFT questions, NOT SENT.** Nothing has been sent to the Authority, the hiring team or anyone else. A person "
          "decides what to raise through the Portal, citing Volume, Clause and page (VOL-I 5.1). Only Addenda bind the "
          "Authority (VOL-I 5.3). Unknown answers stay unknown: the interim handling never assumes a response.", "",
          f"- Cut-off: {cut.get('rule', 'VOL-I 5.2')}: **{cut.get('date', '?')}**. {cut.get('note', '')}",
          f"- {len(qs)} questions drafted; {len(table['checked_no_question'])} topics checked and closed without a "
          f"question (the pack's own words settle them); {len(table['pending_decision'])} proposed readings pending a "
          f"person's decision (no question drafted); {len(table['unavailable_material'])} referenced items not in the "
          "pack.", "",
          "## Questions (most important first)", ""]
    for c in qs:
        md += [f"### {c['id']} — {c.get('volume')} {c.get('clause')}, page {c.get('page')}", "",
               f"- **Kind / group / owner:** {c.get('kind')} / {c.get('theme')} / {c.get('decision_owner', '')}",
               f"- **Discrepancy or gap:** {c.get('gap')}",
               f"- **Already settled (not re-asked):** {c.get('already_settled') or 'nothing'}",
               f"- **Practical impact:** {c.get('practical_impact')}",
               f"- **Proposed question (draft):** {c.get('proposed_question')}",
               f"- **Interim handling:** {c.get('interim_handling')}",
               f"- **Response status:** {c.get('response_status')}",
               f"- **Linked issues:** {', '.join(c.get('linked_issues') or []) or 'none'}",
               f"- **Sources:** {_src(c.get('sources'))}"]
        if c.get("clarification_window"):
            md.append(f"- **Clarification route:** {c['clarification_window']}")
        md.append("")
    md += ["## Checked, no question (the pack's own words settle the point; quoted in the sources)", ""]
    md += [f"- **{c.get('topic')}:** {c.get('finding')} Sources: {_src(c.get('sources'))}"
           for c in table["checked_no_question"]]
    md += ["", f"## Proposed readings, {PENDING_LABEL} (no question drafted; proposed by the assistant, not reviewed "
               "by a person)", ""]
    md += [f"- **{c.get('topic')}** ({human_owned.HUMAN_DECISION_PENDING}; decides: {c.get('decision_owner')}"
           + (f"; {', '.join(c.get('linked_issues') or [])}" if c.get("linked_issues") else "") + f"): {c.get('finding')} "
           f"Sources: {_src(c.get('sources'))}" for c in table["pending_decision"]] or ["None."]
    if reg.get("pending_issues"):                  # session 12 (F5; audit R-a): the same pending set as A1 and A3
        md += ["", f"Also {human_owned.HUMAN_DECISION_PENDING} (open issues a person decides; no decision recorded; the "
                   "same set A1's Issues sheet labels and the A3 page marks ⚑):", ""]
        md += [f"- **{x['id']}** (decides: {x.get('owner')}; {'; '.join(x.get('reasons') or [])}): {x.get('text')}"
               for x in reg["pending_issues"]]
    md += ["", "## Referenced but not in the pack (impact; not a prerequisite for completing the bid)", ""]
    md += [f"- **{c.get('item')}:** {c.get('impact')} Handling: {c.get('handling')}" for c in table["unavailable_material"]]
    return "\n".join(md) + "\n"
