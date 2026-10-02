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
from .dispositions import check_dispositions, check_sweeps, load_dispositions
from .evidence import load_evidence_items
from .draft import draft
from .register import BID_OUT, Consequence, Register, load_rows, printed_date_conflicts
from .render import A3OverflowError, write_a1, write_a3_pdf, write_csv_json
from . import programme
from .schedule import deltas, in_force, plan
from .util import dump_json, load_yaml, sha256_file, write_text

CLASS_WORDS = {"rejection": "rejection", "disqualification": "disqualification", "non_responsive": "non-responsive",
               "exclusion": "exclusion", "score_elimination": "Envelope B returned unopened", "lesser": "lesser consequence",
               "contractual": "contractual remedy (post-award)"}


def _doc_ref(unit_id: str, pages) -> str:
    doc, _, local = unit_id.partition(":")
    return f"{doc} {local} p{','.join(map(str, pages))}" if pages else f"{doc} {local}"


def _short(t: str, n: int = 150) -> str:
    t = " ".join((t or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


def load_evidence(evidence_dir: Path, root: Path) -> tuple[list[dict], list[str]]:
    """Units from a published evidence build, after checking that nothing was edited since it was built (E01):
      - the build is structurally OK and its inputs are unchanged;
      - every file the build wrote still has the hash its BUILD_MANIFEST recorded (units.json, coverage, crops);
      - each unit is internally consistent: its pages are the pages of its anchors, and every anchored span
        id names that page (so an edit that also rewrites the manifest is still caught)."""
    problems = []
    man = json.loads((evidence_dir / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))
    if man.get("status") != "ok":
        problems.append(f"evidence build {evidence_dir} is not structurally OK")
    for p, sha in man.get("inputs", {}).items():
        f = Path(p) if Path(p).is_absolute() else root / p
        if not f.exists() or sha256_file(f) != sha:
            problems.append(f"evidence build is stale: input {p} changed since it was built (re-run ingest)")
    for p, sha in sorted(man.get("outputs", {}).items()):
        f = evidence_dir / p
        if not f.is_file():
            problems.append(f"evidence file {p} listed in BUILD_MANIFEST.json is missing")
        elif sha256_file(f) != sha:
            problems.append(f"evidence file {p} differs from BUILD_MANIFEST.json (edited after the build)")
    if "units.json" not in man.get("outputs", {}):
        problems.append("BUILD_MANIFEST.json does not cover units.json")
    cov = json.loads((evidence_dir / "coverage.json").read_text(encoding="utf-8"))
    if cov.get("status") != "ok":
        problems.append(f"evidence build {evidence_dir} is not structurally OK (coverage.json)")
    units = json.loads((evidence_dir / "units.json").read_text(encoding="utf-8"))["units"]
    for u in units:
        anchor_pages = sorted({a.get("page") for a in u.get("anchors", [])})
        if anchor_pages and sorted(set(u.get("pages", []))) != anchor_pages:
            problems.append(f"{u['unit_id']}: pages {u.get('pages')} disagree with its anchors' pages {anchor_pages}")
        for a in u.get("anchors", []):
            bad = [sid for sid in a.get("spans", []) if f"/p{a.get('page')}/" not in sid]
            if bad:
                problems.append(f"{u['unit_id']}: anchored spans {bad[:2]} are not on page {a.get('page')}")
    return units, problems


def run(evidence_dir: Path, pack_path: Path, root: Path, lenient: bool = False) -> dict:
    """Everything Stages 2-4 compute, as plain data. Writes nothing. `lenient` (check-register only) skips
    curated files that do not load and reports them instead of failing."""
    cfg = load_yaml(pack_path)
    units, problems = load_evidence(evidence_dir, root)
    assumptions = load_yaml(root / cfg.get("assumptions", "config/assumptions.yaml"))
    cal = calendar_from_config(assumptions.get("calendar"))
    policy = assumptions["planning"].get("counting_policy", "conservative")
    templates = load_yaml(root / cfg.get("activity_templates", "curation/activity_templates.yaml"))
    issues_path = root / cfg.get("issues", "curation/register/issues.yaml")
    curated_issues = dict(load_yaml(issues_path)["issues"])
    issue_problems = []
    for f in sorted((issues_path.parent / "issues").glob("*.yaml")):       # per-document issue files (Stage 3)
        try:
            for k, v in ((load_yaml(f) or {}).get("issues") or {}).items():
                if k in curated_issues:
                    issue_problems.append(f"issue {k} defined twice (again in {f.name})")
                curated_issues[k] = v
        except Exception as e:                               # noqa: BLE001
            if not lenient:
                raise
            issue_problems.append(f"{f.name}: skipped, does not load: {str(e)[:300]}")
    load_problems: list[str] = []
    rowfile = load_rows(root / cfg.get("register", "curation/register/rows.yaml"), load_problems if lenient else None)
    disp_dir = root / cfg.get("dispositions_dir", "curation/register/dispositions")
    try:
        dispositions, dproblems = load_dispositions(disp_dir)
    except Exception as e:                                   # noqa: BLE001
        if not lenient:
            raise
        dispositions, dproblems = {}, [f"dispositions do not load: {str(e)[:400]}"]
    evidence_items, eproblems = load_evidence_items(root / cfg.get("evidence_items_dir", "curation/evidence_items"))
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
    return {"cfg": cfg, "root": root, "units": units, "problems": problems, "assumptions": assumptions, "cal": cal, "policy": policy,
            "templates": templates, "curated_issues": curated_issues, "rowfile": rowfile, "opfiles": opfiles,
            "drafted": drafted, "stages": stages, "validated": val, "working": working, "register": reg,
            "evals": evals, "order": order, "dispositions": dispositions,
            "disposition_problems": dproblems + check_dispositions(units, dispositions, rowfile.rows),
            "evidence_items": evidence_items, "evidence_problems": eproblems, "load_problems": load_problems + issue_problems,
            "sweeps": check_sweeps(units, dispositions, rowfile.rows)}


# ---------------------------------------------------------------------------------------------- checks

def structural_checks(r: dict, a3_fit: dict | None, a5_by_stage: dict) -> list[dict]:
    checks = [{"id": "E01", "ok": not r["problems"], "detail": "; ".join(r["problems"]) or
               "evidence build structurally OK and built from the current inputs"}]
    bad = [f"{e['row'].id}@{st}: {p}" for e in r["evals"] for st, ev in e["stages"].items() for p in ev["problems"]]
    moved = sorted({f"{e['row'].id}@{st}" for e in r["evals"] for st, ev in e["stages"].items()
                    if any("quote not found" in x for x in ev["stale"])})
    checks.append({"id": "C16", "ok": not bad, "detail": f"{len(r['evals'])} rows x {len(r['order'])} stages; "
                   + (f"quotes not found: {bad[:4]}" if bad else "every quote and consequence quote of a current "
                      "interpretation found in the effective text")
                   + (f"; quoted text changed under STALE rows (reported as C11): {moved}" if moved else "")})
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
    bad44 = [f"{st}: {p}" for st, prog in a5_by_stage.items() for p in prog.get("problems", []) if p.startswith("C44")]
    missing = sorted({re.search(r"C44: (\S+)", b).group(1) for b in bad44})
    checks.append({"id": "C44", "ok": not bad44, "detail": "every deliverable needed by a row in force has activities or a "
                   "justified exception" if not bad44 else f"{len(missing)} deliverable(s) needed by rows in force have no "
                   f"activities and no justified exception: {', '.join(missing)}"})
    bad45 = [f"{st}: {p}" for st, prog in a5_by_stage.items() for p in prog.get("problems", []) if p.startswith("C45")]
    checks.append({"id": "C45", "ok": not bad45, "detail": "every dependency and lead time is defined" if not bad45
                   else "; ".join(sorted(set(bad45))[:4])})
    fits = bool(a3_fit and a3_fit.get("pages") == 1)
    checks.append({"id": "C43", "ok": fits,
                   "detail": f"A3 fits one page; smallest text {a3_fit.get('min_text_pt')} pt (scale {a3_fit.get('scale')})"
                   if fits else f"A3 does not fit one page at a readable size: {(a3_fit or {}).get('error')}"})
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
        out.append({"id": "I-AUTO-STALE", "text": f"{len(stale)} row(s) STALE at {val.stage}: a dependency changed after the "
                    f"interpretation was made (dates recomputed; the reading needs a person). Rows: {', '.join(stale)}",
                    "owner": "Bid manager", "source": "C11 (automatic)", "rows": stale, "show_in_a3": True})
    differ = sorted({d["rule_id"] for e in r["evals"] for d in e["stages"][val.stage]["dates"] if d["readings_differ"]})
    if differ:
        out.append({"id": "I-AUTO-COUNTING", "text": f"Counting conventions not stated in the pack for {', '.join(differ)}: every "
                    f"reading is shown (A1 Dates); planning uses the {r['policy']} reading (config/assumptions.yaml)",
                    "owner": "Bid manager", "source": "D4 (automatic)", "rows": [], "show_in_a3": True})
    pend = sorted({e["row"].id for e in r["evals"] if e["stages"][val.stage]["transcription"] == "pending"})
    if pend:
        out.append({"id": "I-AUTO-PENDING-READINGS", "text": f"{len(pend)} row(s) rely on image readings (Table 2-4, "
                    f"Form 4-C) still pending the owner's review. Rows: {', '.join(pend)}", "owner": "Owner",
                    "source": "readings (automatic)", "rows": pend, "show_in_a3": True})
    if a5:
        bad = [a for a in a5["activities"] if a["status"] != "OK"]
        for a in bad:
            out.append({"id": f"I-A5-{a['id']}", "text": f"A5 {a['id']}: {a['flags'][0]} ({', '.join(a['req_ids'])}; "
                        f"duration {a['duration_wd']} WD is an ASSUMPTION: {a['duration_assumption']})",
                        "owner": a["owner"], "source": "A5 (automatic)", "rows": a["req_ids"], "show_in_a3": False})
        late = [a for a in bad if a["status"].startswith(("INFEASIBLE", "DEADLINE PASSED"))]
        if late:
            out.append({"id": "I-A5-FEASIBILITY", "text": "A5 at the status date: " + "; ".join(
                f"{a['id']} {a['flags'][0].split(' (')[0]}" for a in late) + ". Lead times are PROVISIONAL assumptions "
                "(A5 drivers)", "owner": "Bid manager", "source": "A5 (automatic)",
                "rows": sorted({x for a in late for x in a["req_ids"]}), "show_in_a3": True})
    return out


# ---------------------------------------------------------------------------------------------- A1

def a1_table(r: dict, issues: list[dict]) -> dict:
    val, order = r["validated"].stage, r["order"]
    working = r["working"].stage if r["working"] else None
    cols = [("id", "Requirement ID", 16), ("group", "Clause group", 13), ("scope", "Scope tags", 18),
            ("requirement", "Requirement (summary)", 40),
            ("original_text", "Text as issued (original document; never assembled)", 50),
            ("effective_text", "Effective text at the validated state (ASSEMBLED by applying the addenda; not a printed text)", 50),
            ("quote", "Quoted words relied on", 40),
            ("source", "Latest reference for the quoted words (document clause page; amending provision)", 26),
            ("assessment", "Pass/fail or scored", 13),
            ("discipline", "Discipline", 13), ("owner", "Owner (role)", 14), ("evidence", "Evidence needed", 16)]
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
        src = last.get("source") or {}
        rec = {"id": row.id, "group": row.group, "scope": row.scope, "requirement": row.requirement,
               "original_text": last.get("original_text", ""), "effective_text": last["text"],
               "quote": (it.quote if it else ""),
               "source": src.get("latest") or _doc_ref(last["effective_unit"] or row.units[0], last["pages"]),
               "assessment": row.assessment, "discipline": row.discipline, "owner": row.owner_role,
               "evidence": row.evidence or ([f"none: {row.no_deliverable}"] if row.no_deliverable else [])}
        for s in order:
            ev = stg[s]
            rec[f"status:{s}"] = ev["status"] + (" — STALE" if ev["stale"] else "")
        rec["consequence"] = ((f"{CLASS_WORDS[cons.cls]}: \"{cons.quote}\""
                               + (f" (proposed translation, not reviewed: '{cons.gloss}')" if cons.gloss else ""))
                              if isinstance(cons, Consequence) else "none stated in the documents")
        csrc = last.get("consequence_source") or {}
        rec["consequence_source"] = (csrc.get("latest") or cons.unit) if isinstance(cons, Consequence) else ""
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
    bb = asm.get("bidder_basis") or {}
    default = {"basis": "configurable assumption (owner's email of 1 Oct; confirmed by the hiring team's reply of 2 Oct)",
               "owner": "Bid manager"}
    assumption_rows += [{"key": f"bidder.{k}", "value": str(v), "basis": (bb.get(k) or default).get("basis", ""),
                         "owner": (bb.get(k) or default).get("owner", "")} for k, v in asm["bidder"].items()]
    assumption_rows += [{"key": f"resources.{k}", "value": f"capacity {v.get('capacity')}", "basis": v.get("basis", ""),
                         "owner": v.get("owner", "")} for k, v in (asm.get("resources") or {}).items()]
    assumption_rows += [{"key": f"submission.{k}", "value": str(v), "basis": "stated in VOL-I 6.5", "owner": "Bid manager"}
                        for k, v in (asm.get("submission") or {}).items() if not isinstance(v, dict)]
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
        text = re.sub(r"\((" + _NUM + r")\)", r"\1", text)                           # 'ten (10) Working Days' -> '... 10 Working Days'
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
            here = [h for h in b["ops"] if r["register"].op_stage.get(h) == s.stage]
            if here or a["active"] != b["active"] or (a["status"] == "NOT ISSUED") != (b["status"] == "NOT ISSUED"):
                why.append("status")                 # not a relabel such as AMENDED -> ACTIVE (as amended by ...)
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

MISSING_DOC_WORDS = ("not supplied", "not in the pack", "referenced but", "not provided")
A3_CLASS_ORDER = (("rejection", "Rejection"), ("disqualification", "Disqualification"),
                  ("non_responsive", "Non-responsive"), ("exclusion", "Exclusion (Arabic text only; category for a person)"))


def a3(r: dict, issues: list[dict], a5: dict | None) -> dict:
    """A3: one readable page. One line per requirement, grouped by the consequence the documents state; the
    quotations, sources and flags of every line are in a3_detail.html (linked by row id)."""
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
            flags.append("reinstated by addendum")
        elif ev["status"].startswith("AMENDED") or "as amended" in ev["status"]:
            flags.append("amended by addendum")
        csrc = (ev.get("consequence_source") or {}).get("latest")
        base = {"id": row.id, "text": row.requirement, "short": _short(row.requirement, 92), "confidence": row.confidence,
                "flags": flags, "row_source": (ev.get("source") or {}).get("latest", "")}
        if isinstance(cons, Consequence) and cons.cls in BID_OUT:
            cu = val.state.get(cons.unit)
            explicit.append({**base, "cls": cons.cls, "class": CLASS_WORDS[cons.cls], "consequence": cons.quote,
                             "gloss": cons.gloss, "source": csrc or _doc_ref(cons.unit, cu.pages if cu else [])})
        elif isinstance(cons, Consequence) and cons.cls == "score_elimination":
            score.append({**base, "cls": cons.cls, "class": CLASS_WORDS[cons.cls], "consequence": cons.quote,
                          "source": csrc or _doc_ref(cons.unit, val.state[cons.unit].pages)})
        elif not isinstance(cons, Consequence) and row.assessment == "pass_fail":
            none_stated.append({**base, "consequence": "", "source": base["row_source"]})
    shown = [i for i in issues if i["show_in_a3"]]
    missing = [i for i in shown if any(w in i["text"].lower() for w in MISSING_DOC_WORDS)]
    unresolved = [i for i in shown if i not in missing]
    pdd = next((d["anchor_value"] for e in r["evals"] for d in e["stages"][v]["dates"] if d["anchor"] == "PDD"), None)
    working = r["working"]
    compact = lambda x: {**x, "text": x["short"], "compact": True}  # noqa: E731
    sections = []
    for cls, title in A3_CLASS_ORDER:
        items = [compact(x) for x in explicit if x["cls"] == cls]
        if items:
            sections.append({"heading": f"{title}: {len(items)}", "note": "", "items": items})
    sections.append({"heading": f"Envelope B returned unopened (technical score below the threshold): {len(score)}",
                     "note": "", "items": [compact(x) for x in score]})
    sections.append({"heading": f"Pass/fail with no stated consequence — a person decides: {len(none_stated)}",
                     "note": "", "items": [], "ids": [x["id"] for x in none_stated]})
    n_rows = len(r["evals"])
    return {
        "title": "A3 — What would put this bid out (working draft)",
        "subtitle": f"Validated state {v} (issued {val.issued}); Proposal Due Date {pdd} 14:00"
                    + (f". Working state {working.stage} is PARTIAL and NOT used here" if working else "")
                    + f". {n_rows} register rows; {len(explicit)} with an explicit consequence.",
        "banner": "WORKING DRAFT — proposed by the assistant, not reviewed by a person; image readings pending the owner's "
                  "review. Explicit wording only. Quotations, sources and flags for every line: a3_detail.html.",
        "sections": sections,
        "missing": {"heading": f"Referenced but not supplied — impact: {len(missing)}",
                    "items": [{"id": i["id"], "text": _short(i["text"], 205), "owner": i["owner"]} for i in missing]},
        "unresolved": {"heading": f"Could not resolve — kept with people: {len(unresolved)}",
                       "items": [{"id": i["id"], "text": _short(i["text"], 160), "owner": i["owner"]} for i in unresolved]},
        "footer": "tenderpack: evidence build + curation + config/assumptions.yaml. Each id links to a3_detail.html "
                  "(quotes, sources, flags) and traces to A1 and A2.",
        "explicit": explicit, "score": score, "none_stated": none_stated,
        "none_stated_ids": [x["id"] for x in none_stated],
        "explicit_ids": [x["id"] for x in explicit],
        "issues_detail": [{"id": i["id"], "text": i["text"], "owner": i["owner"], "rows": i["rows"]} for i in shown],
    }


def a3_detail_html(a3d: dict) -> str:
    """The supporting detail for A3: every line with its full quotation, latest source, flags and confidence."""
    import html as _h
    esc = lambda t: _h.escape(t or "", quote=False)  # noqa: E731

    def quote(t):
        rtl = any("\u0600" <= c <= "\u06ff" for c in t or "")
        return f'<span dir="rtl" lang="ar">{esc(t)}</span>' if rtl else esc(t)
    rows = []
    for title, items in (("Explicit consequences", a3d["explicit"]), ("Envelope B returned unopened", a3d["score"]),
                         ("Pass/fail with no stated consequence", a3d["none_stated"])):
        rows.append(f"<h2>{esc(title)} ({len(items)})</h2><table><tr><th>Row</th><th>Requirement</th><th>Consequence "
                    "(quoted)</th><th>Latest source</th><th>Confidence</th><th>Flags</th></tr>")
        for x in items:
            q = (f"<i>{esc(x.get('class', ''))}</i>: “{quote(x['consequence'])}”" if x.get("consequence") else "none stated")
            if x.get("gloss"):
                q += f"<br><small>proposed translation, not reviewed: ‘{esc(x['gloss'])}’</small>"
            rows.append(f'<tr id="{esc(x["id"])}"><td><b>{esc(x["id"])}</b></td><td>{esc(x["text"])}</td><td>{q}</td>'
                        f'<td>{esc(x["source"])}<br><small>row: {esc(x.get("row_source", ""))}</small></td>'
                        f'<td>{esc(x["confidence"])}</td><td>{esc("; ".join(x["flags"]))}</td></tr>')
        rows.append("</table>")
    rows.append(f"<h2>Issues shown on A3 ({len(a3d['issues_detail'])})</h2><table><tr><th>Issue</th><th>Text</th>"
                "<th>Owner</th><th>Rows</th></tr>")
    rows += [f'<tr id="{esc(i["id"])}"><td><b>{esc(i["id"])}</b></td><td>{esc(i["text"])}</td><td>{esc(i["owner"])}</td>'
             f'<td>{esc(", ".join(i["rows"]))}</td></tr>' for i in a3d["issues_detail"]]
    rows.append("</table>")
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" "
            "content=\"width=device-width, initial-scale=1\"><title>A3 detail</title><style>"
            "body{font-family:system-ui,sans-serif;margin:16px;color:#111;background:#fff}"
            "table{border-collapse:collapse;width:100%;margin-bottom:18px}td,th{border:1px solid #ccc;padding:4px 6px;"
            "vertical-align:top;font-size:13px;text-align:left}th{background:#eee}tr:target{background:#fff7d6}"
            "[dir=rtl]{font-size:15px}small{color:#555}</style></head><body>"
            f"<h1>{esc(a3d['title'])} — supporting detail</h1><p>{esc(a3d['subtitle'])}</p><p><b>{esc(a3d['banner'])}</b></p>"
            + "".join(rows) + "</body></html>\n")


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
                              anchors_by_stage[s.stage], evidence_items=r["evidence_items"])
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
        fit = write_a3_pdf(a3d, out / "a3" / "a3.pdf")
        a3_fit = dict(fit, explicit_ids=a3d["explicit_ids"])
    except A3OverflowError as e:
        a3_fit = {"pages": 0, "error": str(e), "explicit_ids": a3d["explicit_ids"]}
    dump_json(a3d, out / "a3" / "a3.json")
    write_text(out / "a3" / "a3_detail.html", a3_detail_html(a3d))
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
        # A5 at the validated stage: programme, marshalling with document counts, resources, infeasibility drivers,
        # and the scenarios (consortium size, lead times, working calendar) run through the same planner
        mk = programme.stage_planner(r)
        prog_ext = mk(r["assumptions"])
        scen_path = r["root"] / r["cfg"].get("scenarios", "config/scenarios.yaml")
        scen = programme.run_scenarios(mk, r["assumptions"], load_yaml(scen_path), r["evidence_items"]) \
            if scen_path.exists() else None
        programme.write(prog_ext, scen, out)
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
        dump_json(programme.stage_planner(r, r["working"].stage)(r["assumptions"]),
                  out / "a5" / "working" / f"{r['working'].stage}.json")
    for a, f in r["drafted"].items():
        write_text(out / "drafted" / f"{a}.yaml",
                   f"# DRAFTED by tenderpack.draft for this build; every op PROPOSED; not curated.\n"
                   + yaml.safe_dump(f.model_dump(exclude_none=True), allow_unicode=True, sort_keys=False, width=110))
    dump_json([{"stage": s.stage, "status": s.status, "issued": s.issued, "problems": s.problems, "scope_leak": s.scope_leak,
                "ops": [x.to_dict() for x in s.ops], "coverage": s.coverage} for s in r["stages"]], out / "stages.json")
    checks = structural_checks(r, a3_fit, {st: p for st, p in progs.items() if st == val})
    rep = reported_checks(r)
    status = "ok" if all(c["ok"] for c in checks) else "structural_failure"
    blockers = release_blockers(r)
    release = "RELEASABLE" if not blockers else "WORKING DRAFT (not releasable)"
    dump_json({"status": status, "structural": checks, "reported": rep, "validated_stage": val,
               "working_stage": r["working"].stage if r["working"] else None,
               "release": {"status": release, "blockers": blockers,
                           "note": "structurally checked does not mean reviewed or approved by a person"}},
              out / "checks.json")
    readme = ["# A1-A5 outputs (WORKING DRAFT)", "",
              f"Structural checks: **{status}**. Release: **{release}**. Validated state: **{val}**"
              + (f"; working state **{r['working'].stage}** (PARTIAL)." if r["working"] else "."),
              "Structurally checked does not mean reviewed or approved by a person. Interpretations and ops are "
              "PROPOSED; image readings are PENDING the owner's review.", "",
              "## What blocks a release (`outputs --strict`)", ""]
    readme += [f"- **{b['kind']}**: {b['detail']}" for b in blockers] or ["- nothing"]
    readme += ["",
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
            "a3": a3d, "a5": progs, "release": release, "blockers": blockers}


def build(evidence_dir: Path, out: Path, pack_path: Path, root: Path, quiet: bool = False, strict: bool = False) -> dict:
    """Compute and publish the outputs with the same output safety as ingest: written to a temporary sibling
    and swapped in only if every structural check passes; otherwise set aside as <out>.failed (exit 2).
    With `strict` (a release), any release blocker refuses publication: the previous outputs are kept and the
    candidate goes to <out>.rejected with RELEASE_REJECTED.md (exit 3). Without it, a working draft is
    published and labelled as such, with its blockers listed."""
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
                                           ("scenarios", "config/scenarios.yaml"),
                                           ("dispositions_dir", "curation/register/dispositions"),
                                           ("evidence_items_dir", "curation/evidence_items"),
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
        if res["status"] == "ok" and strict and res["blockers"]:
            from .cli import _rejected_dir
            (tmp / "RELEASE_REJECTED.md").write_text(
                "# Release refused (outputs --strict)\n\nStructurally checked, but not releasable. Nothing was "
                "approved or accepted by the program. Blockers:\n\n" + "\n".join(f"- {b['kind']}: {b['detail']}"
                                                                                 for b in res["blockers"]) + "\n",
                encoding="utf-8")
            if _rejected_dir(out).exists():
                shutil.rmtree(_rejected_dir(out))
            tmp.rename(_rejected_dir(out))
            res["out"], res["status"] = _rejected_dir(out), "release_refused"
        elif res["status"] == "ok":
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
    res["exit_code"] = {"ok": 0, "release_refused": 3}.get(res["status"], 2)
    if not quiet:
        for c in res["checks"]:
            print(f"{c['id']} {'pass' if c['ok'] else 'FAIL'}  {c['detail']}")
        for c in res["reported"]:
            print(f"{c['id']}{(' ' + c['stage']) if c.get('stage') else ''} {'ok' if c['ok'] else 'REPORTED'}  {c['detail']}")
        for b in res.get("blockers", []):
            print(f"RELEASE BLOCKER [{b['kind']}] {b['detail']}")
        print({"ok": f"OUTPUTS PUBLISHED ({res.get('release')}): ",
               "release_refused": "RELEASE REFUSED (--strict); previous outputs kept; candidate in: "}.get(
            res["status"], "STRUCTURAL FAILURE, not published: ") + str(res["out"]))
    return res


# ---------------------------------------------------------------------------------------------- release gate

def release_blockers(r: dict) -> list[dict]:
    """Everything that stops a RELEASE (outputs --strict). Structural checks passing means the outputs are
    internally consistent; it does not mean anything was reviewed or approved by a person. A working draft
    is published with these listed; a strict release is refused while any remains:
      coverage   an addendum PARTIAL or with unresolved provisions; a unit without a disposition or a broken
                 disposition-row link; an unlinked consequence word (C15); a bid-stage row with no deliverable
                 and no reason; register files that do not load
      stale      a row whose interpretation predates a change to its dependencies, at the latest stage
      approval   an image reading pending its review; an interpretation or an amendment op not accepted by a
                 named person (the program never accepts or approves anything itself)"""
    out = []
    for s in r["stages"][1:]:
        unres = [c["provision"] for c in s.coverage if c["disposition"] in ("unresolved", "UNACCOUNTED")]
        if s.status != "APPLIED" or unres:
            out.append({"kind": "coverage", "detail": f"{s.stage} is {s.status}; unresolved provisions: {unres or 'none'}"})
    found = register_findings(r)
    groups: dict[str, list[str]] = {}
    for f in found:
        if f["kind"] != "quote":
            groups.setdefault(f["kind"], []).append(f["where"] or f["detail"][:60])
    for k, v in sorted(groups.items()):
        out.append({"kind": "coverage", "detail": f"{len(v)} {k} finding(s): {', '.join(sorted(set(v))[:12])}"
                    + (" ..." if len(set(v)) > 12 else "")})
    last = r["order"][-1]
    stale = [e["row"].id for e in r["evals"] if e["stages"][last]["stale"]]
    if stale:
        out.append({"kind": "stale", "detail": f"{len(stale)} row(s) STALE at {last}: {', '.join(stale[:12])}"
                    + (" ..." if len(stale) > 12 else "")})
    pending = sorted({u["reading"]["region"] if "region" in (u.get("reading") or {}) else u.get("region", u["unit_id"])
                      for u in r["units"] if (u.get("reading") or {}).get("status") == "pending"})
    if pending:
        out.append({"kind": "approval", "detail": f"image readings pending the owner's review: {', '.join(pending)}"})
    proposed_rows = [e["row"].id for e in r["evals"] if e["row"].review != "accepted"]
    if proposed_rows:
        out.append({"kind": "approval", "detail": f"{len(proposed_rows)} of {len(r['evals'])} register rows not accepted by a person"})
    proposed_ops = [x.op.id for s in r["stages"][1:] for x in s.ops if x.op.review != "accepted"]
    if proposed_ops:
        out.append({"kind": "approval", "detail": f"{len(proposed_ops)} amendment op(s) not accepted by a person"})
    return out


# ---------------------------------------------------------------------------------------------- check-register

BID_STAGE = ("pass_fail", "scored", "procedural")


def register_findings(r: dict) -> list[dict]:
    """Everything a register drafter must clear, as {kind, where, detail}. Used by check-register and by
    the build's structural checks (C12, C15, C16, C44, D01)."""
    out = []
    for p in r["load_problems"]:
        out.append({"kind": "load", "where": p.split(":")[0], "detail": p})
    for p in r["disposition_problems"]:
        out.append({"kind": "disposition", "where": p.split(":")[0].split(" ")[-1], "detail": p})
    for p in r["evidence_problems"]:
        out.append({"kind": "evidence_vocabulary", "where": "", "detail": p})
    for e in r["evals"]:
        row = e["row"]
        for st, ev in e["stages"].items():
            for p in ev["problems"]:
                out.append({"kind": "quote", "where": row.id, "detail": f"{st}: {p}"})
        unknown = [x for x in row.evidence if x not in r["evidence_items"]]
        if unknown:
            out.append({"kind": "evidence_vocabulary", "where": row.id, "detail": f"unknown evidence items {unknown}"})
        missing_units = [u for u in row.units if u not in r["stages"][-1].state]
        if missing_units:
            out.append({"kind": "unit", "where": row.id, "detail": f"units that do not exist: {missing_units}"})
        if row.assessment in BID_STAGE and not row.evidence and not (row.no_deliverable or "").strip():
            out.append({"kind": "deliverable", "where": row.id,
                        "detail": "bid-stage row with no evidence item and no no_deliverable reason"})
    c14, c15 = r["sweeps"]
    for h in c15:
        out.append({"kind": "C15", "where": h["unit"], "detail": f"consequence word '{h['word']}' ({h['lang']}) not linked "
                    f"to a row's consequence or a consequence_note: {h['sentence'][:140]}"})
    return out


def check_register(evidence_dir: Path, pack_path: Path, root: Path, doc: str | None = None) -> int:
    r = run(Path(evidence_dir), Path(pack_path), Path(root), lenient=True)
    found = register_findings(r)
    def mine(w: str) -> bool:                                   # 'VOL-I' must not match 'VOL-II' or 'VOL-IV'
        return w == doc or w.startswith(doc + ":") or w.startswith(doc + "-")
    if doc:
        found = [f for f in found if mine(f["where"]) or mine(f["detail"].split(": ")[0].split(" ")[-1])
                 or f["kind"] in ("load", "evidence_vocabulary") and doc in f["detail"]]
    units = [u for u in r["units"] if not doc or u["doc"] == doc]
    disp = r["dispositions"]
    from .dispositions import effective_disposition
    have = sum(1 for u in units if effective_disposition(u, disp) is not None)
    rows = [e for e in r["evals"] if not doc or mine(e["row"].id) or any(x.startswith(doc + ":") for x in e["row"].units)]
    print(f"units: {len(units)} ({have} with a disposition); rows: {len(rows)}; findings: {len(found)}")
    c14 = [h for h in r["sweeps"][0] if not doc or mine(h["unit"])]
    if c14:
        print(f"C14 (for a person to confirm; not a failure): {len(c14)} obligation words in non-requirement units")
    for f in found:
        print(f"  [{f['kind']}] {f['where']}: {f['detail']}")
    return 1 if found else 0
