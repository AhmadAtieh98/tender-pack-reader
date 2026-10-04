"""The tender clarification register (session 08): discrepancies, ambiguities and missing information in the tender
volumes and addenda, with DRAFT questions. Nothing here is ever sent: the program only checks and publishes the
register, and a person decides what to raise through the Portal (VOL-I 5.1) before the VOL-I 5.2 cut-off.

    curation/clarifications/register.yaml   (curated data; `clarifications` in config/pack.yaml overrides the path)
      clarifications:        one entry per genuine unresolved matter: volume, clause, page, units, verbatim sources,
                             gap, what is already settled, practical impact, proposed question, interim handling,
                             decision owner, response status, linked issues, theme (the A3 group)
      checked_no_question:   topics checked against the clauses, precedence and earlier answers that need no question
      unavailable_material:  referenced material not in the pack, its impact and handling (never a prerequisite)
    -> out/a4/clarification_register.{md,csv,json}; the A3 groups list the question ids; A1's Issues sheet links them

Checks (check-register, release gate as coverage): every quotation is verbatim in its unit's text on the stated page;
every entry has the fields the owner asked for; no status says the question was sent or answered unless an addendum
unit is named as the answer; linked issues exist.
"""
from __future__ import annotations

from pathlib import Path

from .register import found
from .render import write_csv_json
from .util import load_yaml, write_text

DEFAULT_PATH = "curation/clarifications/register.yaml"
REQUIRED = ("id", "kind", "volume", "clause", "page", "gap", "practical_impact", "proposed_question", "interim_handling",
            "response_status", "theme")


def load(cfg: dict, root: Path) -> dict:
    p = Path(cfg.get("clarifications", DEFAULT_PATH))
    p = p if p.is_absolute() else root / p
    return (load_yaml(p) or {}) if p.exists() else {}


def check(reg: dict, units: list[dict], issue_ids: set[str]) -> list[str]:
    by_id = {u["unit_id"]: u for u in units}
    out = []

    def quotes(where: str, items) -> None:
        for q in items or []:
            u = by_id.get(q.get("unit"))
            if u is None:
                out.append(f"{where}: unit {q.get('unit')} does not exist")
            elif not found(q.get("words", ""), u.get("text", "")):
                out.append(f"{where}: not verbatim in {q.get('unit')}: '{str(q.get('words'))[:80]}'")
            elif q.get("page") not in u.get("pages", []):
                out.append(f"{where}: {q.get('unit')} is on page(s) {u.get('pages')}, not p{q.get('page')}")

    seen = set()
    for c in reg.get("clarifications") or []:
        cid = c.get("id", "?")
        if cid in seen:
            out.append(f"{cid}: duplicate id")
        seen.add(cid)
        missing = [k for k in REQUIRED if c.get(k) in (None, "")]
        if missing:
            out.append(f"{cid}: missing {missing}")
        status = str(c.get("response_status", "")).lower()
        if "sent" in status and "not sent" not in status:
            out.append(f"{cid}: response_status says it was sent; the program never records a question as sent")
        bad = [i for i in c.get("linked_issues") or [] if i not in issue_ids]
        if bad:
            out.append(f"{cid}: linked issues that do not exist: {bad}")
        quotes(cid, c.get("sources"))
    for i, c in enumerate(reg.get("checked_no_question") or []):
        quotes(f"checked_no_question[{c.get('topic', i)}]", c.get("sources"))
    for i, c in enumerate(reg.get("unavailable_material") or []):
        quotes(f"unavailable_material[{c.get('item', i)}]", c.get("referenced_in"))
    return out


def _src(items) -> str:
    return "; ".join(f"{q.get('unit')} p{q.get('page')}: “{q.get('words')}”" for q in items or [])


def write(reg: dict, out_dir: Path) -> list[Path]:
    """a4/clarification_register.{md,csv,json}: the questions, the topics closed without one, and the unavailable
    material. Deterministic."""
    out_dir = Path(out_dir)
    qs = reg.get("clarifications") or []
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
             "unavailable_material": reg.get("unavailable_material") or []}
    paths = write_csv_json(table, out_dir, "clarification_register")
    md = ["# Tender clarification register (A4 supporting record)", "",
          "**DRAFT questions, NOT SENT.** Nothing has been sent to the Authority, the hiring team or anyone else. A person "
          "decides what to raise through the Portal, citing Volume, Clause and page (VOL-I 5.1). Only Addenda bind the "
          "Authority (VOL-I 5.3). Unknown answers stay unknown: the interim handling never assumes a response.", "",
          f"- Cut-off: {cut.get('rule', 'VOL-I 5.2')}: **{cut.get('date', '?')}**. {cut.get('note', '')}",
          f"- {len(qs)} questions drafted; {len(table['checked_no_question'])} topics checked and closed without a "
          f"question; {len(table['unavailable_material'])} referenced items not in the pack.", "",
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
               f"- **Sources:** {_src(c.get('sources'))}", ""]
    md += ["## Checked, no question (settled by the clauses, precedence or an earlier answer)", ""]
    md += [f"- **{c.get('topic')}:** {c.get('finding')}" for c in table["checked_no_question"]]
    md += ["", "## Referenced but not in the pack (impact; not a prerequisite for completing the bid)", ""]
    md += [f"- **{c.get('item')}:** {c.get('impact')} Handling: {c.get('handling')}" for c in table["unavailable_material"]]
    path = out_dir / "clarification_register.md"
    write_text(path, "\n".join(md) + "\n")
    return paths + [path]
