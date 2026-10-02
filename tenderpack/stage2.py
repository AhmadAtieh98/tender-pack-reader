"""Stage 2: the first connected versions of A1, A2, A3 and A5, from a published Stage 1 evidence build.

    build/ (Stage 1, structure OK)                    units with their evidence
    curation/amendments/ADD-0N.yaml (or drafted)       ops for every addendum in the pack (amend.py)
    curation/register/rows.yaml, issues.yaml          the A1 slice and the open issues (register.py)
    config/assumptions.yaml, curation/activity_templates.yaml   planning assumptions (schedule.py)
      -> out/a1 (xlsx, csv, json)  out/a2 (md, csv, json)  out/a3 (one-page pdf, json)  out/a5 (csv, json)
         out/checks.json, out/stages.json, out/README.md

An addendum with no op file in curation/amendments is drafted by draft.py (every op proposed) and the
draft is written to out/drafted/ — the same path as for the existing addenda. A PARTIAL addendum never
replaces the validated state: A1 shows its column labelled WORKING, A3 and the main A5 come from the
validated state, and the working A5 is written to out/a5/working/.

Structural checks (any failure: nothing is published; exit 2):
  E01 the evidence build is structurally OK and was built from the current inputs
  C16 every interpretation's quote, and every consequence quote, is found in the effective text at
      every stage where the row is in force (evidence vs effective text, PLAN §4.3)
  C25 no addendum changed a unit no op targeted (scope)
  C13 A3's explicit-consequence list holds only rows with an explicit, quoted consequence in force
  C40 every A5 activity cites at least one A1 row in force at that stage
  C43 A3 fits on one page
Reported, not structural: C20 provision coverage and C21-C24/C27 op validity (they make an addendum
PARTIAL), C11 STALE rows, C31 printed dates that disagree with the effective anchor.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path

import yaml

from .amend import BASE, Engine, StageResult, load_opfile, validated_stage
from .citations import citations
from .dates import calendar_from_config
from .draft import draft
from .register import BID_OUT, Consequence, Register, load_rows, printed_date_conflicts
from .render import A3OverflowError, write_a1, write_a3_pdf, write_csv_json
from .schedule import deltas, in_force, plan
from .util import dump_json, load_yaml, sha256_file, write_text

CLASS_WORDS = {"rejection": "rejection", "disqualification": "disqualification", "non_responsive": "non-responsive",
               "exclusion": "exclusion", "score_elimination": "Envelope B returned unopened", "lesser": "lesser consequence"}


def _doc_ref(unit_id: str, pages) -> str:
    doc, _, local = unit_id.partition(":")
    return f"{doc} {local} p{','.join(map(str, pages))}" if pages else f"{doc} {local}"


def _short(t: str, n: int = 150) -> str:
    t = " ".join((t or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


def load_evidence(evidence_dir: Path, root: Path) -> tuple[list[dict], list[str]]:
    problems = []
    cov = json.loads((evidence_dir / "coverage.json").read_text(encoding="utf-8"))
    if cov.get("status") != "ok":
        problems.append(f"evidence build {evidence_dir} is not structurally OK")
    man = json.loads((evidence_dir / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))
    for p, sha in man.get("inputs", {}).items():
        f = Path(p) if Path(p).is_absolute() else root / p
        if not f.exists() or sha256_file(f) != sha:
            problems.append(f"evidence build is stale: input {p} changed since it was built (re-run ingest)")
    units = json.loads((evidence_dir / "units.json").read_text(encoding="utf-8"))["units"]
    return units, problems


def run(evidence_dir: Path, pack_path: Path, root: Path) -> dict:
    """Everything Stage 2 computes, as plain data. Writes nothing."""
    cfg = load_yaml(pack_path)
    units, problems = load_evidence(evidence_dir, root)
    assumptions = load_yaml(root / cfg.get("assumptions", "config/assumptions.yaml"))
    cal = calendar_from_config(assumptions.get("calendar"))
    policy = assumptions["planning"].get("counting_policy", "conservative")
    templates = load_yaml(root / cfg.get("activity_templates", "curation/activity_templates.yaml"))
    curated_issues = load_yaml(root / cfg.get("issues", "curation/register/issues.yaml"))["issues"]
    rowfile = load_rows(root / cfg.get("register", "curation/register/rows.yaml"))
    amend_dir = root / cfg.get("amendments_dir", "curation/amendments")
    addenda = sorted({u["doc"] for u in units if u["doc"].startswith("ADD-")}, key=lambda d: int(d.split("-")[1]))
    opfiles, drafted = [], {}
    for a in addenda:
        p = amend_dir / f"{a}.yaml"
        if p.exists():
            opfiles.append(load_opfile(p))
        else:
            f = draft(units, a)
            drafted[a] = f
            opfiles.append(f)
    stages = Engine(units, opfiles).run()
    val = validated_stage(stages)
    reg = Register(rowfile, stages, cal, policy)
    evals = reg.all()
    order = [s.stage for s in stages]
    working = stages[-1] if stages[-1].stage != val.stage else None
    return {"cfg": cfg, "units": units, "problems": problems, "assumptions": assumptions, "cal": cal, "policy": policy,
            "templates": templates, "curated_issues": curated_issues, "rowfile": rowfile, "opfiles": opfiles,
            "drafted": drafted, "stages": stages, "validated": val, "working": working, "register": reg,
            "evals": evals, "order": order}


# ---------------------------------------------------------------------------------------------- checks

def structural_checks(r: dict, a3_fit: dict | None, a5_by_stage: dict) -> list[dict]:
    checks = [{"id": "E01", "ok": not r["problems"], "detail": "; ".join(r["problems"]) or
               "evidence build structurally OK and built from the current inputs"}]
    bad = [f"{e['row'].id}@{st}: {p}" for e in r["evals"] for st, ev in e["stages"].items() for p in ev["problems"]]
    checks.append({"id": "C16", "ok": not bad, "detail": f"{len(r['evals'])} rows x {len(r['order'])} stages; "
                   + (f"quotes not found: {bad[:4]}" if bad else "every quote and consequence quote found in the effective text")})
    leaks = [f"{s.stage}: {x}" for s in r["stages"] for x in s.scope_leak]
    checks.append({"id": "C25", "ok": not leaks, "detail": "; ".join(leaks[:4]) or "no unit changed without an op targeting it"})
    val = r["validated"].stage
    a3_ids = (a3_fit or {}).get("explicit_ids", [])
    bad13 = [i for i in a3_ids if not any(e["row"].id == i and isinstance(r["register"].interp_at(e["row"], val).consequence, Consequence)
                                          and e["row"].id for e in r["evals"])]
    checks.append({"id": "C13", "ok": not bad13, "detail": f"{len(a3_ids)} A3 items, each with an explicit quoted consequence"
                   + (f"; without: {bad13}" if bad13 else "")})
    bad40 = []
    for st, prog in a5_by_stage.items():
        force = {e["row"].id for e in r["evals"] if in_force(e["stages"][st]["status"])}
        bad40 += [f"{st}:{a['id']}" for a in prog["activities"] if not set(a["req_ids"]) & force]
    checks.append({"id": "C40", "ok": not bad40, "detail": f"every A5 activity cites an A1 row in force" if not bad40 else f"orphans: {bad40[:5]}"})
    checks.append({"id": "C43", "ok": bool(a3_fit and a3_fit.get("pages") == 1),
                   "detail": f"A3 fits one page at scale {a3_fit.get('scale')}" if a3_fit and a3_fit.get("pages") == 1
                   else f"A3 does not fit one page: {(a3_fit or {}).get('error')}"})
    return checks


def reported_checks(r: dict) -> list[dict]:
    out = []
    for s in r["stages"][1:]:
        unacc = [c["provision"] for c in s.coverage if c["disposition"] in ("UNACCOUNTED", "unresolved")]
        out.append({"id": "C20", "stage": s.stage, "ok": not unacc,
                    "detail": f"{len(s.coverage)} provisions; unresolved or unaccounted: {unacc or 'none'}"})
        inv = [f"{x.op.id} ({next(c['id'] + ': ' + c['detail'] for c in x.checks if not c['ok'])})" for x in s.ops if not x.valid]
        out.append({"id": "C21-C27", "stage": s.stage, "ok": not inv, "detail": f"{len(s.ops)} ops; invalid: {inv or 'none'}"})
    stale = [f"{e['row'].id}@{st}" for e in r["evals"] for st, ev in e["stages"].items() if ev["stale"]]
    out.append({"id": "C11", "ok": not stale, "detail": f"STALE rows: {stale or 'none'}"})
    return out


# ---------------------------------------------------------------------------------------------- issues

def collect_issues(r: dict, a5: dict | None) -> list[dict]:
    val = r["validated"]
    rows_by_issue: dict[str, list[str]] = {}
    for e in r["evals"]:
        for i in e["row"].issues:
            rows_by_issue.setdefault(i, []).append(e["row"].id)
    out = []
    for iid, it in r["curated_issues"].items():
        out.append({"id": iid, "text": it["text"], "owner": it["owner"], "source": "curated (proposed wording)",
                    "rows": rows_by_issue.get(iid, []), "show_in_a3": bool(it.get("show_in_a3"))})
    for c in printed_date_conflicts(val, r["rowfile"].anchors):
        out.append({"id": f"I-AUTO-PRINTED-{c['unit'].split(':', 1)[1].replace('/', '-')}",
                    "text": f"{c['unit']} prints the {r['rowfile'].anchors[c['anchor']]['name']} as {c['printed']}; "
                            f"the effective date ({c['defined_in']}) is {c['effective']}. Not corrected: a person decides "
                            "what to print and sign, and whether to seek clarification",
                    "owner": "Legal", "source": "C31 (automatic)", "rows": [], "show_in_a3": True})
    for s in r["stages"][1:]:
        for x in s.ops:
            if x.op.issue:
                out.append({"id": f"I-OP-{x.op.id}", "text": f"{x.op.id}: {x.op.issue}", "owner": "Bid manager",
                            "source": "amendment op", "rows": [], "show_in_a3": False})
        unres = [c["provision"] for c in s.coverage if c["disposition"] in ("UNACCOUNTED", "unresolved")]
        inv = [x.op.id for x in s.ops if not x.valid]
        if unres or inv or s.status == "PARTIAL":
            out.append({"id": f"I-PARTIAL-{s.stage}", "text": f"{s.stage} is PARTIAL: unresolved provisions {unres or 'none'}; "
                        f"invalid ops {inv or 'none'}. The validated state stays at {val.stage}",
                        "owner": "Bid manager", "source": "C20/C21-C27 (automatic)", "rows": [], "show_in_a3": True})
        outside = sum(1 for c in s.coverage if c["disposition"] == "outside_slice")
        if outside:
            out.append({"id": f"I-SLICE-{s.stage}", "text": f"{s.stage}: {outside} of {len(s.coverage)} provisions are outside "
                        "this register slice (listed in A2); their effect on rows not in the slice is not modelled",
                        "owner": "Bid manager", "source": "C20 (automatic)", "rows": [], "show_in_a3": False})
    stale = [e["row"].id for e in r["evals"] if e["stages"][val.stage]["stale"]]
    if stale:
        out.append({"id": "I-AUTO-STALE", "text": f"STALE at {val.stage} (a dependency changed after the interpretation was "
                    f"made; dates recomputed, reading needs a person): {', '.join(stale)}", "owner": "Bid manager",
                    "source": "C11 (automatic)", "rows": stale, "show_in_a3": True})
    differ = sorted({d["rule_id"] for e in r["evals"] for d in e["stages"][val.stage]["dates"] if d["readings_differ"]})
    if differ:
        out.append({"id": "I-AUTO-COUNTING", "text": f"Counting conventions not stated in the pack for {', '.join(differ)}: every "
                    f"reading is shown (A1 Dates); planning uses the {r['policy']} reading (config/assumptions.yaml)",
                    "owner": "Bid manager", "source": "D4 (automatic)", "rows": [], "show_in_a3": True})
    pend = sorted({e["row"].id for e in r["evals"] if e["stages"][val.stage]["transcription"] == "pending"})
    if pend:
        out.append({"id": "I-AUTO-PENDING-READINGS", "text": "Rows relying on image readings still pending the owner's review: "
                    + ", ".join(pend), "owner": "Owner", "source": "readings (automatic)", "rows": pend, "show_in_a3": True})
    if a5:
        bad = [a for a in a5["activities"] if a["status"] != "OK"]
        for a in bad:
            out.append({"id": f"I-A5-{a['id']}", "text": f"A5 {a['id']}: {a['flags'][0]} ({', '.join(a['req_ids'])}; "
                        f"duration {a['duration_wd']} WD is an ASSUMPTION: {a['duration_assumption']})",
                        "owner": a["owner"], "source": "A5 (automatic)", "rows": a["req_ids"],
                        "show_in_a3": a["status"].startswith(("INFEASIBLE", "DEADLINE PASSED"))})
    return out


# ---------------------------------------------------------------------------------------------- A1

def a1_table(r: dict, issues: list[dict]) -> dict:
    val, order = r["validated"].stage, r["order"]
    working = r["working"].stage if r["working"] else None
    cols = [("id", "Requirement ID", 16), ("group", "Clause group", 13), ("scope", "Scope tags", 18),
            ("requirement", "Requirement (summary)", 40), ("verbatim", "Verbatim source text (effective, validated state)", 60),
            ("source", "Document / clause / page", 20), ("assessment", "Pass/fail or scored", 13),
            ("discipline", "Discipline", 13), ("evidence", "Evidence needed", 16)]
    cols += [(f"status:{s}", f"Status after {s}" + (" (WORKING, not validated)" if s == working else ""), 22) for s in order]
    cols += [("consequence", "Stated consequence (quoted)", 40), ("consequence_source", "Consequence source", 18),
             ("dates", "Dates (planning reading; all readings in Dates sheet)", 30), ("confidence", "Confidence", 30),
             ("transcription", "Image reading status", 14), ("interpretation", "Interpretation review", 14),
             ("ops_review", "Amendment ops review", 14), ("chain", "Evidence chain (original -> ops)", 50),
             ("issues", "Issues", 20)]
    rows = []
    for e in r["evals"]:
        row, stg = e["row"], e["stages"]
        v = stg[val]
        last = v if v["active"] else next((stg[s] for s in reversed(order) if stg[s]["active"]), v)
        it = r["register"].interp_at(row, val) or (row.interpretations[-1] if row.interpretations else None)
        cons = it.consequence if it else "none_stated"
        rec = {"id": row.id, "group": row.group, "scope": row.scope, "requirement": row.requirement,
               "verbatim": last["text"], "source": _doc_ref(last["effective_unit"] or row.units[0], last["pages"]),
               "assessment": row.assessment, "discipline": row.discipline, "evidence": row.evidence}
        for s in order:
            ev = stg[s]
            rec[f"status:{s}"] = ev["status"] + (" — STALE" if ev["stale"] else "")
        rec["consequence"] = ((f"{CLASS_WORDS[cons.cls]}: \"{cons.quote}\""
                               + (f" (proposed translation, not reviewed: '{cons.gloss}')" if cons.gloss else ""))
                              if isinstance(cons, Consequence) else "none stated in the documents")
        rec["consequence_source"] = cons.unit if isinstance(cons, Consequence) else ""
        rec["dates"] = [f"{d['rule_id']}: {d['planning']['value']} ({d['planning']['key']})" for d in v["dates"]]
        rec["confidence"] = f"{row.confidence}: {row.confidence_reason}"
        rec["transcription"] = v["transcription"]
        rec["interpretation"] = row.review + (f" by {row.reviewer}" if row.reviewer else " (not reviewed)")
        rec["ops_review"] = ", ".join(v["ops_review"]) or "n/a"
        rec["chain"] = v["chain"]
        rec["issues"] = row.issues
        rows.append(rec)
    dates_rows = []
    for e in r["evals"]:
        for s in order:
            for d in e["stages"][s]["dates"]:
                dates_rows.append({"row": e["row"].id, "stage": s, "rule": d["rule_id"], "text": d["text"],
                                   "anchor": f"{d['anchor']} = {d['anchor_value']}" if d["anchor"] else "",
                                   "readings": [f"{i['key']}: {i['value']} ({i['basis']})" for i in d["interpretations"]],
                                   "planning": f"{d['planning']['value']} ({d['planning']['key']}, policy {d['planning']['policy']})",
                                   "readings_differ": d["readings_differ"]})
    stages_rows = [{"stage": s.stage, "addendum": s.addendum or "", "issued": s.issued or "", "status": s.status,
                    "ops": len(s.ops), "invalid_ops": sum(1 for x in s.ops if not x.valid),
                    "ops_review": ", ".join(sorted({x.op.review for x in s.ops})) or "",
                    "provisions": len(s.coverage),
                    "outside_slice": sum(1 for c in s.coverage if c["disposition"] == "outside_slice"),
                    "unresolved": sum(1 for c in s.coverage if c["disposition"] in ("unresolved", "UNACCOUNTED")),
                    "validated": s.stage == val or r["order"].index(s.stage) < r["order"].index(val)} for s in r["stages"]]
    asm = r["assumptions"]
    assumption_rows = [{"key": f"lead_times.{k}", "value": f"{v['value']} WD", "basis": v["basis"], "owner": v["owner"]}
                       for k, v in asm["lead_times"].items()]
    assumption_rows += [{"key": f"bidder.{k}", "value": str(v), "basis": "configurable assumption (owner's email of 1 Oct)",
                         "owner": "Bid manager"} for k, v in asm["bidder"].items()]
    assumption_rows += [{"key": f"planning.{k}", "value": str(v), "basis": "configurable planning choice", "owner": "Bid manager"}
                        for k, v in asm["planning"].items()]
    assumption_rows += [{"key": "calendar.holidays", "value": str(asm["calendar"].get("holidays") or "none"),
                         "basis": "the pack declares none (VOL-I 2.4 excludes declared public holidays)", "owner": "Bid manager"}]
    sheet = lambda rows, keys: {"columns": [{"key": k, "header": k.replace("_", " ").capitalize(), "width": w} for k, w in keys],  # noqa: E731
                                "rows": rows}
    return {
        "title": "A1 Obligations and compliance register — SLICE (Stage 2 first connected version)",
        "notice": (f"DRAFT. {len(rows)} representative rows, not the full register. Interpretations and amendment ops are "
                   "PROPOSED by the assistant and not reviewed by a person; image readings are PENDING the owner's review. "
                   f"Validated state: {val}" + (f"; working state {working} is PARTIAL" if working else "") + "."),
        "stages": order, "validated_stage": val, "working_stage": working,
        "columns": [{"key": k, "header": h, "width": w} for k, h, w in cols], "rows": rows,
        "sheets": {
            "Dates": sheet(dates_rows, [("row", 16), ("stage", 9), ("rule", 22), ("text", 40), ("anchor", 22),
                                        ("readings", 60), ("planning", 34), ("readings_differ", 10)]),
            "Issues": sheet([{k: i[k] for k in ("id", "text", "owner", "source", "rows")} for i in issues],
                            [("id", 26), ("text", 90), ("owner", 16), ("source", 22), ("rows", 30)]),
            "Stages": sheet(stages_rows, [("stage", 9), ("addendum", 9), ("issued", 11), ("status", 10), ("ops", 6),
                                          ("invalid_ops", 9), ("ops_review", 12), ("provisions", 10), ("outside_slice", 10),
                                          ("unresolved", 10), ("validated", 9)]),
            "Assumptions": sheet(assumption_rows, [("key", 30), ("value", 14), ("basis", 90), ("owner", 16)]),
        },
    }


# ---------------------------------------------------------------------------------------------- A2

_NUM = r"\d[\d,]*(?:\.\d+)?"


def replaced_figures(x, state) -> list[tuple[str, str]]:
    """Figures an op replaced, each with the word or unit that follows it ('120 pages', '12 November',
    '72 hours', '5 mg/l'), so a bare number elsewhere (a question number, a footnote number) is not a match.
    Numbers of five or more characters ('5,000,000') are distinctive enough on their own."""
    out = []
    old = " ".join(filter(None, [x.op.old, x.details.get("old_value")]))
    if x.op.type == "set_value" and x.details.get("old_value") and x.op.target in state:
        unit = next((v for c, v in (state[x.op.target].cells or {}).items() if c.lower() == "unit"), "")
        if unit and unit != "-":
            old = f"{x.details['old_value']} {unit}"
    words = re.sub(r"\((" + _NUM + r")\)", r"\1", old)          # 'one hundred and twenty (120) pages' -> '... 120 pages'
    words = re.sub(r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|[a-z]+teen|[a-z]+ty)(?:[- ][a-z]+)*\s+(?=\d)",
                   "", words, flags=re.I)
    for m in re.finditer(r"(" + _NUM + r")\s*(?:-\s*)?([A-Za-z%/][\w/%³]*)?", words):
        num, unit = m.group(1), m.group(2)
        if unit:
            stem = re.escape(unit.rstrip("s")) if len(unit) > 3 else re.escape(unit)
            out.append((f"{num} {unit}", r"(?<![\d,.])" + re.escape(num) + r"\s*(?:-\s*)?" + stem))
        elif len(num) >= 5:
            out.append((num, r"(?<![\d,.])" + re.escape(num) + r"(?![\d,])"))
    return out


def answers_to_review(r: dict, s: StageResult) -> list[dict]:
    """Clarification answers that cite a unit this addendum changed, or quote a figure it replaced. They are
    listed for a person to review; an answer is never marked revoked automatically. Non-binding minutes are
    not answers and are listed separately."""
    changed = {}
    for x in s.ops:
        if x.valid and x.op.type in ("replace_text", "set_value", "set_status", "replace_unit"):
            changed[x.op.target] = x
    figures = {}                                   # (label, regex) -> op: a replaced figure WITH its unit
    for t, x in changed.items():
        for label, rx in replaced_figures(x, s.state):
            figures.setdefault((label, rx), x)
    out = []
    for k, u in s.state.items():
        if u.kind != "table_row" or not u.doc.startswith("ADD-") or u.status != "active" or "Authority response" not in (u.cells or {}):
            continue
        text = " ".join(v for c, v in u.cells.items() if c not in ("No", "No.", "Q"))   # never the question number
        cited = [c.target for c in citations(text)]
        hit = [(t, x) for t, x in changed.items() if t in cited or any(t.startswith(c + "/") or t.startswith(c + "#") for c in cited)]
        num = [(lab, x) for (lab, rx), x in figures.items() if re.search(rx, text, re.I)]
        if hit or num:
            why = [f"cites {t}, changed by {x.op.id}" for t, x in hit] + \
                  [f"quotes '{lab}', a figure {x.op.id} replaced" for lab, x in num if not any(x is y for _, y in hit)]
            out.append({"answer": k, "issued_by": u.issued_by, "text": _short(u.text, 220), "why": "; ".join(why),
                        "status": "REVIEW (not automatically revoked)"})
    return out


def a2(r: dict) -> dict:
    val = r["validated"].stage
    stages = r["stages"]
    md = ["# A2 Addendum reconciliation — Stage 2 first connected version", "",
          f"**DRAFT.** Ops are PROPOSED (not reviewed by a person). Validated state: **{val}**"
          + (f"; working state **{r['working'].stage}** is PARTIAL and does not replace it." if r["working"] else "."),
          "Every provision of every addendum is accounted for below: by an op, as content of an op, as no effect "
          "(with the reason), as OUTSIDE THE SLICE, or as UNRESOLVED.", ""]
    changes, provs, moved, answers = [], [], [], []
    for i, s in enumerate(stages[1:], 1):
        prev = stages[i - 1]
        md += [f"## {s.stage} (issued {s.issued}) — {s.status}", "",
               f"Op file: {'drafted by tenderpack.draft for this build (out/drafted/)' if s.stage in r['drafted'] else 'curation/amendments/' + s.stage + '.yaml'}. "
               f"Prepared by: {s.prepared_by}", ""]
        counts = {}
        for c in s.coverage:
            counts[c["disposition"]] = counts.get(c["disposition"], 0) + 1
        md += [f"Provisions: {len(s.coverage)} — " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())), ""]
        md += ["### What it changed, added and deleted", "", "| Op | Type | Target | Change | Provision | Valid | Review |",
               "|---|---|---|---|---|---|---|"]
        for x in s.ops:
            o = x.op
            tgt = o.target or o.new_group or ", ".join(o.targets)
            if o.type == "replace_text":
                ch = f"'{_short(o.old, 60)}' -> '{_short(o.new, 60)}'"
            elif o.type == "set_value":
                ch = f"{o.column}: {x.details.get('old_value')} -> {o.new}" + (" (old value from an image reading PENDING review)"
                                                                            if x.details.get("reading_status") == "pending" else "")
            elif o.type == "set_status":
                ch = o.status.upper() + (f": '{_short(o.new_text, 80)}'" if o.new_text else "")
            elif o.type == "replace_unit":
                ch = f"replaced by {o.replacement} ({len(x.details.get('content', []))} units)"
            elif o.type == "insert_unit":
                ch = f"inserted {o.new_group or ''} {('after ' + o.anchor) if o.anchor else ''}".strip()
            else:
                ch = f"{o.effect}" + (f"; mentions of '{o.subject}': {x.details.get('mentions')}" if o.subject else "") + \
                     (f" — {_short(o.note, 90)}" if o.note else "")
            if x.details.get("also_in"):
                ch += f" [same words also in {', '.join(x.details['also_in'])}: not targeted]"
            pu = s.state.get(o.provision)
            bad = "; ".join(c["id"] + ": " + c["detail"] for c in x.checks if not c["ok"])
            md.append(f"| {o.id} | {o.type} | {tgt} | {ch.replace('|', '/')} | {o.provision} p{pu.pages[0] if pu and pu.pages else '?'} | "
                      f"{'yes' if x.valid else 'NO — ' + bad.replace('|', '/')} | {o.review} ({o.origin}) |")
            changes.append({"stage": s.stage, "op": o.id, "type": o.type, "target": tgt, "change": ch, "provision": o.provision,
                            "valid": x.valid, "failed_checks": bad, "review": o.review, "origin": o.origin,
                            "issue": o.issue or ""})
        md += ["", "### Register rows that move", "", "| Row | Before | After | Why |", "|---|---|---|---|"]
        for e in r["evals"]:
            a, b = e["stages"][prev.stage], e["stages"][s.stage]
            pa = [d["planning"] for d in a["dates"]] if a["active"] else []
            pb = [d["planning"] for d in b["dates"]] if b["active"] else []
            why = []
            if a["status"] != b["status"]:
                why.append("status")
            if b["interpretation_stage"] == s.stage and a["interpretation"] != b["interpretation"]:
                why.append(f"interpretation re-made at {s.stage}" + (f" ({_short(b['interpretation'].get('note') or '', 90)})"
                                                                    if (b["interpretation"] or {}).get("note") else ""))
            if pa != pb and a["active"] and b["active"]:
                why.append("dates moved")
            if bool(a["stale"]) != bool(b["stale"]):
                why.append("became STALE" if b["stale"] else "no longer STALE")
            if why:
                da = "; ".join(f"{d['rule_id']} {d['planning']['value']}" for d in a["dates"]) if a["active"] else ""
                db = "; ".join(f"{d['rule_id']} {d['planning']['value']}" for d in b["dates"]) if b["active"] else ""
                before = a["status"] + (f" [{da}]" if da else "")
                after = b["status"] + (f" [{db}]" if db else "") + (" — STALE: " + "; ".join(b["stale"]) if b["stale"] else "")
                md.append(f"| {e['row'].id} | {before} | {after.replace('|', '/')} | {'; '.join(why).replace('|', '/')} |")
                moved.append({"stage": s.stage, "row": e["row"].id, "before": before, "after": after, "why": why,
                              "chain": b["chain"]})
        ans = answers_to_review(r, s)
        md += ["", "### Earlier answers to review (never revoked automatically)", ""]
        md += [f"- `{x['answer']}` ({x['issued_by']}): {x['why']}. {x['status']}." for x in ans] or ["None found."]
        answers += [dict(x, stage=s.stage) for x in ans]
        nb = [c for c in s.coverage if c["disposition"] == "no_effect" and "non-binding" in c["reason"]]
        if nb:
            md += ["", "### Non-binding statements (context only; not answers, not revoked, not applied)", ""]
            md += [f"- `{c['provision']}`: {_short(c['text'], 160)}" for c in nb]
        md += ["", "### Provision coverage", "", "| Provision | Page | Disposition | Accounted by | Reason |", "|---|---|---|---|---|"]
        for c in s.coverage:
            disp = c["disposition"].upper() if c["disposition"] in ("outside_slice", "unresolved", "UNACCOUNTED") else c["disposition"]
            md.append(f"| {c['provision']} | {c['page']} | {disp} | {', '.join(c['accounted_by'])} | {c['reason'].replace('|', '/')} |")
            provs.append({"stage": s.stage, **{k: c[k] for k in ("provision", "page", "disposition", "reason")},
                          "accounted_by": c["accounted_by"], "text": c["text"]})
        md.append("")
    md += ["## Evidence chains (rows changed by an addendum)", ""]
    for e in r["evals"]:
        ch = e["stages"][r["order"][-1]]["chain"]
        if len(ch) > 1:
            md.append(f"- **{e['row'].id}**: " + " ← ".join(reversed(ch)))
    return {"markdown": "\n".join(md) + "\n", "changes": changes, "provisions": provs, "rows_moved": moved, "answers": answers}


# ---------------------------------------------------------------------------------------------- A3

def a3(r: dict, issues: list[dict], a5: dict | None) -> dict:
    val = r["validated"]
    v = val.stage
    infeasible = {}
    for a in (a5 or {}).get("activities", []):
        if a["status"].startswith("INFEASIBLE"):
            for rid in a["req_ids"]:
                infeasible.setdefault(rid, []).append(a["id"])
    explicit, score, none_stated = [], [], []
    for e in r["evals"]:
        row, ev = e["row"], e["stages"][v]
        if not in_force(ev["status"]):
            continue
        it = r["register"].interp_at(row, v)
        cons = it.consequence if it else "none_stated"
        flags = []
        if ev["transcription"] == "pending":
            flags.append("image reading pending")
        if ev["stale"]:
            flags.append("STALE")
        if row.id in infeasible:
            flags.append("INFEASIBLE: " + ", ".join(infeasible[row.id]))
        if ev["status"].startswith("NEW"):
            flags.append("new by addendum")
        elif ev["status"].startswith("REINSTATED"):
            flags.append("reinstated in amended form by addendum")
        elif ev["status"].startswith("AMENDED") or "as amended" in ev["status"]:
            flags.append("amended by addendum")
        if isinstance(cons, Consequence) and cons.cls in BID_OUT:
            cu = val.state.get(cons.unit)
            explicit.append({"id": row.id, "text": row.requirement, "class": CLASS_WORDS[cons.cls], "consequence": cons.quote,
                             "gloss": cons.gloss, "source": _doc_ref(cons.unit, cu.pages if cu else []),
                             "confidence": row.confidence, "flags": flags})
        elif isinstance(cons, Consequence) and cons.cls == "score_elimination":
            score.append({"id": row.id, "text": row.requirement, "class": CLASS_WORDS[cons.cls], "consequence": cons.quote,
                          "source": _doc_ref(cons.unit, val.state[cons.unit].pages), "confidence": row.confidence, "flags": flags})
        elif not isinstance(cons, Consequence) and row.assessment == "pass_fail":
            none_stated.append({"id": row.id, "text": row.requirement, "consequence": "", "source": row.group,
                                "confidence": row.confidence, "flags": flags})
    unresolved = [{"id": i["id"], "text": _short(i["text"], 210), "owner": i["owner"]} for i in issues if i["show_in_a3"]]
    pdd = next((d["anchor_value"] for e in r["evals"] for d in e["stages"][v]["dates"] if d["anchor"] == "PDD"), None)
    working = r["working"]
    return {
        "title": "A3 — What would put this bid out (draft)",
        "subtitle": f"Validated state {v} (issued {val.issued}); Proposal Due Date {pdd} 14:00" +
                    (f". Working state {working.stage} is PARTIAL and NOT used here" if working else "") +
                    f". Slice of {len(r['evals'])} rows, not the full register.",
        "banner": "DRAFT — interpretations and amendment ops proposed by the assistant, not reviewed by a person; "
                  "image readings pending the owner's review. Explicit wording only; confidence is on the reading of the text.",
        "sections": [
            {"heading": "Explicit consequences stated in the documents (rejection, disqualification, non-responsiveness, exclusion)",
             "note": "", "items": explicit},
            {"heading": "Score-based elimination", "note": "", "items": score},
            {"heading": "Pass/fail requirements with no consequence stated — a person decides",
             "note": "Not in the list above because the documents do not say what failure causes.", "items": none_stated},
        ],
        "unresolved": {"heading": "Could not resolve — kept with people", "items": unresolved},
        "footer": "Generated by tenderpack from the Stage 1 evidence build, curation/amendments, curation/register and "
                  "config/assumptions.yaml. Every item traces to A1 (row id) and A2 (evidence chain).",
        "explicit_ids": [x["id"] for x in explicit],
    }


# ---------------------------------------------------------------------------------------------- A5

def a5_all(r: dict) -> dict:
    anchors_by_stage = {}
    progs = {}
    for s in r["stages"][1:]:
        if not s.issued:
            continue
        pdd = next((d["anchor_value"] for e in r["evals"] for d in e["stages"][s.stage]["dates"] if d["anchor"] == "PDD"), None)
        anchors_by_stage[s.stage] = {"PDD": pdd}
        progs[s.stage] = plan(s.stage, r["evals"], r["templates"], r["assumptions"], r["cal"], date.fromisoformat(s.issued),
                              anchors_by_stage[s.stage])
    return progs


# ---------------------------------------------------------------------------------------------- write

def write(r: dict, out: Path) -> dict:
    progs = a5_all(r)
    val = r["validated"].stage
    main = progs.get(val)
    issues = collect_issues(r, main)
    a3d = a3(r, issues, main)
    a3_fit: dict
    try:
        fit = write_a3_pdf({k: v for k, v in a3d.items() if k != "explicit_ids"}, out / "a3" / "a3.pdf")
        a3_fit = dict(fit, explicit_ids=a3d["explicit_ids"])
    except A3OverflowError as e:
        a3_fit = {"pages": 0, "error": str(e), "explicit_ids": a3d["explicit_ids"]}
    dump_json(a3d, out / "a3" / "a3.json")
    a1d = a1_table(r, issues)
    write_a1(a1d, out / "a1")
    a2d = a2(r)
    write_text(out / "a2" / "a2.md", a2d["markdown"])
    tbl = lambda rows: {"columns": [{"key": k, "header": k, "width": 20} for k in (rows[0].keys() if rows else ["none"])], "rows": rows}  # noqa: E731
    write_csv_json(tbl(a2d["changes"]), out / "a2", "a2_changes")
    write_csv_json(tbl(a2d["provisions"]), out / "a2", "a2_provisions")
    write_csv_json(tbl(a2d["rows_moved"]), out / "a2", "a2_rows_moved")
    write_csv_json(tbl(a2d["answers"]), out / "a2", "a2_answers_to_review")
    if main:
        prog_rows = [{k: a[k] for k in ("id", "name", "req_ids", "owner", "issuer", "duration_wd", "duration_assumption",
                                        "duration_basis", "multiplicity", "predecessors", "latest_start", "latest_finish",
                                        "deadline", "status", "flags")} for a in main["activities"]]
        write_csv_json(tbl(prog_rows), out / "a5", "programme")
        write_csv_json(tbl(main["marshalling"]), out / "a5", "marshalling")
        dl = []
        ordered = [s for s in r["order"] if s in progs]
        for a, b in zip(ordered, ordered[1:]):
            ea = {e["row"].id: e["stages"][a] for e in r["evals"]}
            eb = {e["row"].id: e["stages"][b] for e in r["evals"]}
            dl += [dict(x, from_stage=a, to_stage=b) for x in deltas(progs[a], progs[b], ea, eb)]
        write_csv_json(tbl(dl), out / "a5", "replan_deltas")
        for st, p in progs.items():
            dump_json(p, out / "a5" / "stages" / f"{st}.json")
    if r["working"] and r["working"].stage in progs:
        dump_json(progs[r["working"].stage], out / "a5" / "working" / f"{r['working'].stage}.json")
    for a, f in r["drafted"].items():
        write_text(out / "drafted" / f"{a}.yaml",
                   f"# DRAFTED by tenderpack.draft for this build; every op PROPOSED; not curated.\n"
                   + yaml.safe_dump(f.model_dump(exclude_none=True), allow_unicode=True, sort_keys=False, width=110))
    dump_json([{"stage": s.stage, "status": s.status, "issued": s.issued, "problems": s.problems, "scope_leak": s.scope_leak,
                "ops": [x.to_dict() for x in s.ops], "coverage": s.coverage} for s in r["stages"]], out / "stages.json")
    checks = structural_checks(r, a3_fit, {st: p for st, p in progs.items() if st == val})
    rep = reported_checks(r)
    status = "ok" if all(c["ok"] for c in checks) else "structural_failure"
    dump_json({"status": status, "structural": checks, "reported": rep, "validated_stage": val,
               "working_stage": r["working"].stage if r["working"] else None}, out / "checks.json")
    readme = ["# Stage 2 outputs (first connected version, DRAFT)", "",
              f"Status: **{status}**. Validated state: **{val}**" + (f"; working state **{r['working'].stage}** (PARTIAL)." if r["working"] else "."),
              "Interpretations and ops are PROPOSED (not reviewed); image readings are PENDING the owner's review.", "",
              "| Output | Files |", "|---|---|",
              "| A1 register slice, status at each stage | a1/a1.xlsx, a1/a1.csv, a1/a1.json |",
              "| A2 reconciliation: changes, rows that move, answers to review, provision coverage, evidence chains | a2/a2.md, a2/*.csv, a2/*.json |",
              "| A3 one-page draft | a3/a3.pdf, a3/a3.json |",
              "| A5 programme, marshalling plan, replan deltas | a5/programme.*, a5/marshalling.*, a5/replan_deltas.*, a5/stages/*.json |",
              "| Engine results per stage | stages.json |", "| Checks | checks.json |", "",
              "## Checks", "", "| Check | Result | Detail |", "|---|---|---|"]
    readme += [f"| {c['id']} | {'pass' if c['ok'] else 'FAIL'} | {c['detail'].replace('|', '/')} |" for c in checks]
    readme += [f"| {c['id']}{(' ' + c['stage']) if c.get('stage') else ''} | {'ok' if c['ok'] else 'REPORTED'} | "
               f"{c['detail'].replace('|', '/')} |" for c in rep]
    write_text(out / "README.md", "\n".join(readme) + "\n")
    return {"status": status, "checks": checks, "reported": rep, "a3_fit": a3_fit, "issues": issues, "a1": a1d, "a2": a2d,
            "a3": a3d, "a5": progs}


def build(evidence_dir: Path, out: Path, pack_path: Path, root: Path, quiet: bool = False) -> dict:
    """Compute and publish Stage 2 outputs with the same output safety as ingest: written to a temporary
    sibling and swapped in only if every structural check passes; otherwise set aside as <out>.failed."""
    import os
    from .cli import MARKER, _failed_dir, _inputs, check_output_dir
    evidence_dir, pack_path, root = Path(evidence_dir).resolve(), Path(pack_path).resolve(), Path(root).resolve()
    out = Path(out).absolute()
    cfg = load_yaml(pack_path)
    inputs = _inputs(pack_path, cfg, root) + [evidence_dir] + \
        [root / cfg.get(k, d) for k, d in (("amendments_dir", "curation/amendments"),
                                           ("register", "curation/register/rows.yaml"),
                                           ("issues", "curation/register/issues.yaml"),
                                           ("assumptions", "config/assumptions.yaml"),
                                           ("activity_templates", "curation/activity_templates.yaml"))]
    check_output_dir(out, root, inputs)
    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.parent / f".{out.name}.building-{os.getpid()}"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    try:
        (tmp / MARKER).write_text("tenderpack build directory (safe for tenderpack to replace)\n", encoding="utf-8")
        r = run(evidence_dir, pack_path, root)
        res = write(r, tmp)
        if res["status"] == "ok":
            old = None
            if out.exists():
                old = out.parent / f".{out.name}.old-{os.getpid()}"
                out.rename(old)
            tmp.rename(out)
            if old is not None:
                shutil.rmtree(old)
            res["out"] = out
        else:
            if _failed_dir(out).exists():
                shutil.rmtree(_failed_dir(out))
            tmp.rename(_failed_dir(out))
            res["out"] = _failed_dir(out)
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    res["run"] = r
    res["exit_code"] = 0 if res["status"] == "ok" else 2
    if not quiet:
        for c in res["checks"]:
            print(f"{c['id']} {'pass' if c['ok'] else 'FAIL'}  {c['detail']}")
        for c in res["reported"]:
            print(f"{c['id']}{(' ' + c['stage']) if c.get('stage') else ''} {'ok' if c['ok'] else 'REPORTED'}  {c['detail']}")
        print(("OUTPUTS PUBLISHED: " if res["status"] == "ok" else "STRUCTURAL FAILURE, not published: ") + str(res["out"]))
    return res
