"""Stage 2: the first connected versions of A1, A2, A3 and A5, from a published Stage 1 evidence build.

    build/ (Stage 1, structure OK)                    units with their evidence
    curation/amendments/ADD-0N.yaml (or drafted)       ops for every addendum in the pack (amend.py)
    curation/register/rows.yaml, issues.yaml          the A1 register and the open issues (register.py)
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
  C44 every deliverable needed by a row in force has A5 activities, or a justified exception
  C45 every A5 dependency, lead time and resource role is defined
  C43 A3 fits on one page with no text below A3_MIN_TEXT_PT
Reported, not structural: C20 provision coverage and C21-C24/C27 op validity (they make an addendum
PARTIAL), C11 STALE rows, C31 printed dates that disagree with the effective anchor.

Release gate (release_blockers): structurally checked is not approved. A working draft is published with
its blockers listed (coverage: PARTIAL addenda, dispositions, C15; stale rows; approvals pending); with
`outputs --strict` any blocker refuses the release (exit 3, candidate in <out>.rejected).
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path

import yaml

from .amend import BASE, Engine, StageResult, load_opfile, unevidenced_additions, validated_stage
from .citations import citations
from .dates import calendar_from_config
from .dispositions import check_dispositions, check_sweeps, load_dispositions
from .evidence import load_evidence_items
from .draft import draft
from .register import BID_OUT, Consequence, Register, found, load_rows, printed_date_conflicts
from .render import A3OverflowError, write_a1, write_a3_pdf, write_csv_json
from . import programme
from .schedule import deltas, in_force, plan
from .trace import obligation_trace
from .summary import date_changes_by_stage, rule_index, summary_check
from .datecover import counting_conventions, date_coverage
from . import clarify, review
from .textnorm import normalize_latin
from .util import dump_json, load_yaml, sha256_file, write_text

CLASS_WORDS = {"rejection": "rejection", "disqualification": "disqualification", "non_responsive": "non-responsive",
               "exclusion": "exclusion", "score_elimination": "Envelope B returned unopened", "lesser": "lesser consequence",
               "contractual": "contractual remedy (post-award)",
               # session 09 (register.CONSEQUENCE_CLASSES): neither is shown as a disqualification
               "document_refusal": "document refused (the Proposal's fate is not stated: VOL-I 11.1(i) gate)",
               "criterion_zero": "zero marks under one criterion (scored; not a disqualification)"}


def _doc_ref(unit_id: str, pages, number: str | None = None) -> str:
    doc, _, local = unit_id.partition(":")
    shown = f"{number} (issued as {local})" if number else local
    return f"{doc} {shown} p{','.join(map(str, pages))}" if pages else f"{doc} {shown}"


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
    decisions_file = review.decisions_path(cfg, root)
    decisions = review.load_decisions(decisions_file)
    r = {"cfg": cfg, "root": root, "units": units, "problems": problems, "assumptions": assumptions, "cal": cal, "policy": policy,
         "templates": templates, "curated_issues": curated_issues, "rowfile": rowfile, "opfiles": opfiles,
         "drafted": drafted, "dispositions": dispositions,
         "disposition_problems": dproblems + check_dispositions(units, dispositions, rowfile.rows),
         "evidence_items": evidence_items, "evidence_problems": eproblems, "load_problems": load_problems + issue_problems,
         "sweeps": check_sweeps(units, dispositions, rowfile.rows), "decisions_file": decisions_file, "decisions": decisions,
         "evidence_dir": Path(evidence_dir), "clarifications": clarify.load(cfg, root)}
    return evaluate(r)


def evaluate(r: dict) -> dict:
    """The amendment path, register, review statuses and reported analyses from the inputs held in `r` (units, op
    files, rows, decisions, calendar). One pass: every op whose latest named decision is a rejection is withheld
    (review.withdrawn_ops), and each decision is bound to a subject captured before its op runs, so withholding an
    op never changes what its rejection is bound to (no rebuild can flip a rejected op back into force)."""
    units, cfg, root = r["units"], r["cfg"], r["root"]
    r.pop("_unit_evidence", None)                        # recomputed from the units by review.row_binding
    stages = Engine(units, r["opfiles"], review.withdrawn_ops(r["decisions"])).run()
    val = validated_stage(stages)
    reg = Register(r["rowfile"], stages, r["cal"], r["policy"])
    r["non_working_days"] = {s.stage: list(s.non_working_days) for s in stages}   # days notified under VOL-I 2.4
    r.update({"stages": stages, "validated": val, "working": stages[-1] if stages[-1].stage != val.stage else None,
              "register": reg, "evals": reg.all(), "order": [s.stage for s in stages]})
    from .register import anchor_details      # date, time, timezone and source of each anchor, from its effective text
    r["anchor_details"] = {s.stage: anchor_details(s.state, r["rowfile"].anchors, reg.issued, reg.op_stage,
                                                   reg.op_provision) for s in stages}
    r["reviews"] = review.compute(r, r["decisions"])
    r["trace"] = obligation_trace(r)
    r["summary_check"] = summary_check(r["stages"], units, r["rowfile"].anchors,    # C28: report only, never applied
                                       rule_index(r["rowfile"].rows),
                                       date_changes=date_changes_by_stage(r["evals"], r["order"]))
    r["date_coverage"] = date_coverage(r)
    r["c32"] = counting_conventions(r)
    ledger_path = root / cfg.get("row_ids", "curation/register/ids.yaml")
    ledger = (load_yaml(ledger_path) or {}) if ledger_path.exists() else {}
    known, withdrawn = set((ledger.get("ids") or {})), dict(ledger.get("withdrawn") or {})
    current = [e["row"].id for e in r["evals"]]
    r["ids"] = {"path": ledger_path, "missing": sorted(known - set(current) - set(withdrawn)),
                "new": sorted(set(current) - known), "withdrawn": withdrawn,
                "duplicates": sorted({i for i in current if current.count(i) > 1}),
                "back": sorted(set(current) & set(withdrawn))}
    return r


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
    ids = r["ids"]
    bad12 = ids["missing"] + ids["duplicates"] + ids["back"]
    checks.append({"id": "C12", "ok": not bad12, "detail": (f"row ids missing without a recorded withdrawal: {ids['missing']}; "
                   f"duplicated: {ids['duplicates']}; withdrawn ids reused: {ids['back']}") if bad12 else
                   f"every row id in the ledger is present or withdrawn with a reason ({len(ids['withdrawn'])} withdrawn)"})
    added = [f"{b.stage}: {x}" for a, b in zip(r["stages"], r["stages"][1:]) for x in unevidenced_additions(a.state, b.state, b.stage)]
    checks.append({"id": "C47", "ok": not added, "detail": "; ".join(added[:4]) if added else
                   "every word a unit gains at a stage is printed in that stage's addendum"})
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
        rej = [c["provision"] for c in s.coverage if c["disposition"] == "rejected"]
        out.append({"id": "C20", "stage": s.stage, "ok": not unacc and not rej,
                    "detail": f"{len(s.coverage)} provisions; unresolved or unaccounted: {unacc or 'none'}"
                              + (f"; not applied because a person rejected their op: {rej}" if rej else "")})
        inv = [f"{x.op.id} ({next(c['id'] + ': ' + c['detail'] for c in x.checks if not c['ok'])})" for x in s.ops if not x.valid]
        out.append({"id": "C21-C27", "stage": s.stage, "ok": not inv, "detail": f"{len(s.ops)} ops; invalid: {inv or 'none'}"})
    stale = [f"{e['row'].id}@{st}" for e in r["evals"] for st, ev in e["stages"].items() if ev["stale"]]
    out.append({"id": "C11", "ok": not stale, "detail": f"STALE rows: {stale or 'none'}"})
    dc = r.get("date_coverage", [])
    unc = [f"{x['unit']} '{x['phrase']}'" for x in dc if x["treatment"] == "UNCOVERED"]
    nc = [f"{x['unit']} '{x['phrase']}'" for x in dc if x["treatment"] == "NOT COMPUTED"]
    out.append({"id": "C30", "ok": not unc, "detail": f"{len(dc)} date/period phrases in force; uncovered: {unc or 'none'}; "
                f"explicitly not computed: {nc or 'none'}"})
    out.append({"id": "C32", "ok": True, "detail": f"{len(r.get('c32', []))} date rule(s) with unstated counting conventions: "
                "every reading shown (A1 Dates), planning uses the configured policy"})
    if r.get("ids", {}).get("new"):
        out.append({"id": "C12-new", "ok": False, "detail": f"{len(r['ids']['new'])} row id(s) not yet in the id ledger "
                    f"({r['ids']['path'].name}): {r['ids']['new'][:8]}; record them with `check-register --update-ids`"})
    for sc in r.get("summary_check", []):
        n = {}
        for f in sc["findings"]:
            n[f["kind"]] = n.get(f["kind"], 0) + 1
        out.append({"id": "C28", "stage": sc["stage"], "ok": not sc["findings"],
                    "detail": (f"cover summary ({len(sc['claims'])} claims) vs provisions: "
                               + (", ".join(f"{k} {v}" for k, v in sorted(n.items())) if n else "consistent")
                               + "; report only, the summary is never applied (A2)")})
    tr = r.get("trace", [])
    out.append({"id": "C46", "ok": not tr, "detail": "every new or amended obligation reaches A1, A3 where it carries a "
                "consequence, and A5" if not tr else f"{len(tr)} gap(s): " + "; ".join(f"{t['op']} [{t['output']}]" for t in tr[:8])})
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
                    "rows": rows_by_issue.get(iid, []), "show_in_a3": bool(it.get("show_in_a3")), "a3": it.get("a3"),
                    "theme": it.get("theme"), "short": it.get("short"), "folds": list(it.get("folds") or [])})
    for c in printed_date_conflicts(val, r["rowfile"].anchors):
        out.append({"id": f"I-AUTO-PRINTED-{c['unit'].split(':', 1)[1].replace('/', '-')}",
                    "text": f"{c['unit']} prints the {r['rowfile'].anchors[c['anchor']]['name']} as {c['printed']}; "
                            f"the effective date ({c['defined_in']}) is {c['effective']}. Not corrected: a person decides "
                            "what to print and sign, and whether to seek clarification",
                    "owner": "Legal", "source": "C31 (automatic)", "rows": [], "show_in_a3": True,
                    "a3": f"{c['unit']} prints the {r['rowfile'].anchors[c['anchor']]['name']} as {c['printed']}; effective "
                          f"{c['effective']}. Not corrected: what to print and sign is for a person"})
    for s in r["stages"][1:]:
        for x in s.ops:
            if x.op.issue:
                out.append({"id": f"I-OP-{x.op.id}", "text": f"{x.op.id}: {x.op.issue}", "owner": "Bid manager",
                            "source": "amendment op", "rows": [], "show_in_a3": False})
        unres = [c["provision"] for c in s.coverage if c["disposition"] in ("UNACCOUNTED", "unresolved")]
        inv = [x.op.id for x in s.ops if not x.valid]
        held = [x.op.id for x in s.ops if x.valid and x.withdrawn]
        if unres or inv or held or s.status == "PARTIAL":
            out.append({"id": f"I-PARTIAL-{s.stage}", "text": f"{s.stage} is PARTIAL: unresolved provisions {unres or 'none'}; "
                        f"invalid ops {inv or 'none'}; ops withheld after a person's rejection {held or 'none'}. "
                        f"The validated state stays at {val.stage}",
                        "owner": "Bid manager", "source": "C20/C21-C27 and review decisions (automatic)", "rows": [],
                        "show_in_a3": True,
                        "a3": f"{s.stage} is PARTIAL (unresolved: {_ids(unres)}; invalid: {_ids(inv)}"
                              + (f"; rejected: {_ids(held)}" if held else "") + f"): A3 and A5 stay on {val.stage}"})
        gaps: dict[str, list[str]] = {}
        for t in r.get("trace", []):
            if t["stage"] == s.stage:
                gaps.setdefault(t["op"], []).append(t["output"])
        if gaps:
            words = {t["op"]: t["detail"].split(": '", 1)[-1].rstrip("'") for t in r["trace"] if t["stage"] == s.stage}
            out.append({"id": f"I-AUTO-UNTRACED-{s.stage}", "text": f"{s.stage}: obligation(s) not carried through to the "
                        "outputs (C46): " + "; ".join(f"{op} [{', '.join(sorted(set(o)))}] '{words[op][:110]}'"
                                                      for op, o in gaps.items())
                        + ". A row, its consequence or its deliverable is missing; a person must add it",
                        "owner": "Bid manager", "source": "C46 (automatic)", "rows": [], "show_in_a3": True,
                        "a3": f"{s.stage}: obligations not carried to the outputs (C46): "
                              + "; ".join(f"{op} [{', '.join(sorted(set(o)))}]" for op, o in gaps.items())
                              + ". A row, consequence or deliverable must be added"})
    for sc in r.get("summary_check", []):
        f = [x for x in sc["findings"] if x["kind"] not in ("unchecked",)]
        if f:
            out.append({"id": f"I-AUTO-SUMMARY-{sc['stage']}", "text": f"{sc['stage']}'s cover summary does not match its "
                        f"provisions (C28): " + "; ".join(f"[{x['kind']}] {x['detail']}" for x in f)
                        + ". The summary is never applied; a person decides whether to raise a clarification",
                        "owner": "Bid manager", "source": "C28 (automatic)", "rows": [], "show_in_a3": False,
                        "a3": f"{sc['stage']} cover summary vs provisions (C28): {len(f)} finding(s); see A2"})
    dc = r.get("date_coverage", [])
    open_dates = [x for x in dc if x["treatment"] in ("UNCOVERED", "NOT COMPUTED")]
    if open_dates:
        out.append({"id": "I-AUTO-DATES", "text": "Date or period phrases not planned (C30): " + "; ".join(
            f"{x['unit']} '{x['phrase']}' {x['treatment']}" + (f" ({x['by']})" if x["treatment"] != "UNCOVERED" else "")
            for x in open_dates), "owner": "Bid manager", "source": "C30 (automatic)", "rows": [], "show_in_a3": True,
            "a3": f"{len(open_dates)} date/period phrase(s) not computed or not accounted for (C30): "
                  + _ids([f"{x['unit']} '{x['phrase']}'" for x in open_dates], 3)})
    stale = [e["row"].id for e in r["evals"] if e["stages"][val.stage]["stale"]]
    if stale:
        out.append({"id": "I-AUTO-STALE", "text": f"{len(stale)} row(s) STALE at {val.stage}: a dependency changed after the "
                    f"interpretation was made (dates recomputed; the reading needs a person). Rows: {', '.join(stale)}",
                    "owner": "Bid manager", "source": "C11 (automatic)", "rows": stale, "show_in_a3": True,
                    "a3": f"{len(stale)} row(s) STALE at {val.stage} (a dependency changed; dates recomputed, the reading "
                          f"needs a person): {_ids(stale)}"})
    differ = sorted({d["rule_id"] for e in r["evals"] for d in e["stages"][val.stage]["dates"] if d["readings_differ"]})
    if differ:
        out.append({"id": "I-AUTO-COUNTING", "text": f"Counting conventions not stated in the pack for {', '.join(differ)}: every "
                    f"reading is shown (A1 Dates); planning uses the {r['policy']} reading (config/assumptions.yaml)",
                    "owner": "Bid manager", "source": "D4 (automatic)", "rows": [], "show_in_a3": True,
                    "a3": f"Counting conventions not stated for {len(differ)} date rule(s): every reading in A1 Dates; planning "
                          f"uses the {r['policy']} one"})
    pend = sorted({e["row"].id for e in r["evals"] if e["stages"][val.stage]["transcription"] == "pending"})
    if pend:
        out.append({"id": "I-AUTO-PENDING-READINGS", "text": f"{len(pend)} row(s) rely on image readings (Table 2-4, "
                    f"Form 4-C) still pending the owner's review. Rows: {', '.join(pend)}", "owner": "Owner",
                    "source": "readings (automatic)", "rows": pend, "show_in_a3": True,
                    "a3": f"{len(pend)} row(s) rely on the image readings (Table 2-4, Form 4-C) pending the owner's review"})
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
                "rows": sorted({x for a in late for x in a["req_ids"]}), "show_in_a3": True,
                "a3": "A5 at the status date: " + _ids([f"{a['id']} {a['flags'][0].split(' (')[0]}" for a in sorted(
                    late, key=lambda a: (-int((re.search(r"by (\d+)", a["status"]) or [0, 0])[1]), a["id"]))], 5) + " (lead times PROVISIONAL)"})
    return out


# ---------------------------------------------------------------------------------------------- A1

ISSUE_THEMES = (("forms", "Forms and declarations"), ("envelopes", "Envelopes, copies and files"),
                ("technical", "Technical, permit and design basis"), ("contract", "Contract, bond and concession"),
                ("evaluation", "Evaluation and scoring"),
                ("missing", "Referenced but not supplied (impact noted; not a prerequisite for completion)"),
                ("programme", "Programme, evidence and bidder facts"), ("addenda", "Addenda and register status"))


def issue_theme(i: dict) -> str:
    """The A3 group of an open issue: its curated `theme`, or one derived from an automatic issue's id."""
    if i.get("theme"):
        return i["theme"]
    iid = i["id"]
    if iid.startswith("I-AUTO-PRINTED"):
        return "forms"
    if iid.startswith(("I-A5-", "I-AUTO-COUNTING")):
        return "programme"
    if iid.startswith("I-OP-"):
        return "evaluation" if "/T1-1-rev/" in iid else "addenda"
    return "addenda"


def issue_short(i: dict) -> str:
    if i.get("short"):
        return i["short"]
    iid = i["id"]
    if iid.startswith("I-AUTO-SUMMARY-"):
        return f"{iid.rsplit('-', 2)[-2]}-{iid.rsplit('-', 1)[-1]} cover summary vs provisions: findings in A2 (C28)"
    if iid == "I-AUTO-COUNTING":
        return "counting conventions not stated for some date rules: every reading in A1 Dates"
    if iid == "I-AUTO-STALE":
        return "rows STALE: their reading needs a person (A1)"
    if iid.startswith("I-PARTIAL-"):
        return f"{iid[len('I-PARTIAL-'):]} PARTIAL: provisions not yet applied (A2)"
    t = (i.get("a3") or i["text"]).split(". ")[0]
    if i["id"].startswith("I-OP-") and ": " in t:                       # 'ADD-02/Q7: ...' -> the text after the op id
        t = t.split(": ", 1)[1]
    return t if len(t) <= 90 else t[:89].rsplit(" ", 1)[0] + "…"


def _ids(xs: list[str], n: int = 6) -> str:
    """Ids for an A3 line: all of them when few, otherwise the first n and an explicit count of the rest."""
    xs = list(xs)
    if not xs:
        return "none"
    return ", ".join(xs[:n]) + (f" and {len(xs) - n} more (a3_detail.html)" if len(xs) > n else "")


_SUMMARY_FIG = re.compile(r"\d[\d,]*(?:\.\d+)?%?")


def summary_currency(r: dict) -> list[dict]:
    """A row's requirement summary is stage-neutral text written by a person. When it states a figure that its units
    printed as issued but no longer print at the validated stage (an addendum changed it: '80,000' -> '60,000'), the
    summary is out of date. Flagged in A1, A3 and check-register; never rewritten by the program."""
    val, base = r["validated"].state, r["stages"][0].state
    norm = lambda t: normalize_latin(t or "").replace(" ", "")  # noqa: E731
    out = []
    for e in r["evals"]:
        row = e["row"]
        if not in_force(e["stages"][r["validated"].stage]["status"]):
            continue
        now = " ".join(norm(val[k].text) + " " + " ".join(norm(v) for v in (val[k].cells or {}).values())
                       for k in row.units if k in val)
        then = " ".join(norm(base[k].text) for k in row.units if k in base and base[k].status != "not_issued")
        for fig in dict.fromkeys(_SUMMARY_FIG.findall(row.requirement)):
            f = norm(fig)
            if len(re.sub(r"\D", "", f)) >= 2 and f in then and f not in now:
                out.append({"row": row.id, "figure": fig})
    return out


def a1_table(r: dict, issues: list[dict]) -> dict:
    val, order = r["validated"].stage, r["order"]
    working = r["working"].stage if r["working"] else None
    cols = [("id", "Requirement ID", 16), ("group", "Clause group", 13), ("scope", "Scope tags", 18),
            ("requirement", "Requirement (summary)", 40),
            ("original_text", "Text as issued (original document; never assembled)", 50),
            ("effective_text", "Effective text at the validated state (ASSEMBLED by applying the addenda; not a printed text)", 50),
            ("quote", "Quoted words relied on", 40),
            ("source", "Latest reference for the quoted words (document clause page; amending provision)", 26),
            ("units", "Every unit the row cites (reference at the validated state; amending ops)", 30),
            ("assessment", "Pass/fail or scored", 13),
            ("discipline", "Discipline", 13), ("owner", "Owner (role)", 14), ("evidence", "Evidence needed", 16)]
    cols += [(f"status:{s}", f"Status after {s}" + (" (WORKING, not validated)" if s == working else ""), 22) for s in order]
    cols += [(f"source:{s}", f"Source after {s} (latest reference for the quoted words)", 26) for s in order]
    cols += [("consequence", "Stated consequence (quoted)", 40), ("consequence_source", "Consequence source", 18),
             ("dates", "Dates (planning reading; all readings in Dates sheet)", 30), ("confidence", "Confidence", 30),
             ("transcription", "Image reading status", 14), ("interpretation", "Interpretation review", 14),
             ("ops_review", "Amendment ops review", 14), ("chain", "Evidence chain (original -> ops)", 50),
             ("issues", "Issues", 20)]
    rows = []
    summary_stale = summary_currency(r)
    for e in r["evals"]:
        row, stg = e["row"], e["stages"]
        v = stg[val]
        last = v if v["active"] else next((stg[s] for s in reversed(order) if stg[s]["active"]), v)
        it = r["register"].interp_at(row, val) or (row.interpretations[-1] if row.interpretations else None)
        cons = it.consequence if it else "none_stated"
        src = last.get("source") or {}
        ud = last.get("units_detail") or []
        multi = len(ud) > 1
        orig = ("\n".join(f"[{d['ref']}" + (f"; issued by {d['issued_by']}" if d["issued_by"] else "") + f"] "
                          + (d["original_text"] or "(not in the volumes as issued)") for d in ud)
                if multi else last.get("original_text", ""))
        seen, eff_parts = set(), []
        for d in ud:
            if d["effective_unit"] in seen:
                continue
            seen.add(d["effective_unit"])
            eff_parts.append(f"[{d['effective_ref']}] " + (d["text"] if d["status"] == "active" else f"({d['status'].upper()})"))
        units_col = [f"{d['effective_ref'] or d['ref']}" + (f" (issued as {d['unit']})" if d["effective_unit"] not in (None, d["unit"]) else "")
                     + (f" <- {', '.join(d['ops'])}" if d["ops"] else "") for d in ud]
        rec = {"id": row.id, "group": row.group, "scope": row.scope, "requirement": row.requirement,
               "original_text": orig, "effective_text": "\n".join(eff_parts) if multi else last["text"],
               "quote": (it.quote if it else ""),
               "source": src.get("latest") or _doc_ref(last["effective_unit"] or row.units[0], last["pages"]),
               "units": units_col,
               "assessment": row.assessment, "discipline": row.discipline, "owner": row.owner_role,
               "evidence": row.evidence + ([row.post_award_evidence.text] if row.post_award_evidence else [])
               or ([f"none: {row.no_deliverable}"] if row.no_deliverable else [])}
        for s in order:
            ev = stg[s]
            rec[f"status:{s}"] = ev["status"] + (" — STALE" if ev["stale"] else "")
            rec[f"source:{s}"] = "" if ev["status"] == "NOT ISSUED" else (ev.get("source") or {}).get("latest", "")
        rec["consequence"] = ((f"{CLASS_WORDS[cons.cls]}: \"{cons.quote}\""
                               + (f" (proposed translation, not reviewed: '{cons.gloss}')" if cons.gloss else ""))
                              if isinstance(cons, Consequence) else "none stated in the documents")
        csrc = last.get("consequence_source") or {}
        rec["consequence_source"] = (csrc.get("latest") or cons.unit) if isinstance(cons, Consequence) else ""
        rec["dates"] = [f"{d['rule_id']}: {d['planning']['value']} ({d['planning']['key']})" for d in v["dates"]]
        rec["confidence"] = f"{row.confidence}: {row.confidence_reason}"
        rec["transcription"] = v["transcription"]
        rec["interpretation"] = review.label(r["reviews"][("row", row.id)])
        rec["ops_review"] = "; ".join(f"{h}: {r['reviews'][('op', h)]['status']}" for h in v["ops"]
                                      if ("op", h) in r["reviews"]) or "n/a"
        rec["chain"] = stg[order[-1]]["chain"]                 # every unit and every op, through the last stage
        rec["issues"] = row.issues + [f"SUMMARY OUT OF DATE: '{x['figure']}'" for x in summary_stale if x["row"] == row.id]
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
                    "withheld_ops": sum(1 for x in s.ops if x.valid and x.withdrawn),
                    "ops_review": ", ".join(f"{k} {n}" for k, n in sorted(_count(
                        r["reviews"][("op", x.op.id)]["status"] for x in s.ops).items())) or "",
                    "provisions": len(s.coverage),
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
    rc = _count(r["reviews"][("row", e["row"].id)]["status"] for e in r["evals"])
    oc = _count(v["status"] for (k, _), v in r["reviews"].items() if k == "op")
    pending = sorted({u["reading"]["region"] for u in r["units"] if (u.get("reading") or {}).get("status") == "pending"
                      and "region" in u["reading"]})
    return {
        "title": "A1 Obligations and compliance register — WORKING DRAFT",
        "notice": (f"WORKING DRAFT, full register: {len(rows)} rows (review status: "
                   + ", ".join(f"{k} {n}" for k, n in sorted(rc.items())) + "; amendment ops: "
                   + ", ".join(f"{k} {n}" for k, n in sorted(oc.items())) + "). Rows and ops count as accepted only with a "
                   "named person's decision bound to their current content. Image readings pending the owner's review: "
                   + (", ".join(pending) or "none") + f". Validated state: {val}"
                   + (f"; working state {working} is PARTIAL" if working else "") + "."),
        "stages": order, "validated_stage": val, "working_stage": working,
        "columns": [{"key": k, "header": h, "width": w} for k, h, w in cols], "rows": rows,
        "sheets": {
            "Dates": sheet(dates_rows, [("row", 16), ("stage", 9), ("rule", 22), ("text", 40), ("anchor", 22),
                                        ("readings", 60), ("planning", 34), ("readings_differ", 10)]),
            "Issues": sheet([{**{k: i[k] for k in ("id", "text", "owner", "source", "rows")},
                              "clarification": [q["id"] for q in (r.get("clarifications") or {}).get("clarifications", [])
                                                if i["id"] in (q.get("linked_issues") or [])]} for i in issues],
                            [("id", 26), ("text", 90), ("owner", 16), ("source", 22), ("rows", 30),
                             ("clarification", 24)]),
            "Stages": sheet(stages_rows, [("stage", 9), ("addendum", 9), ("issued", 11), ("status", 10), ("ops", 6),
                                          ("invalid_ops", 9), ("ops_review", 24), ("provisions", 10),
                                          ("unresolved", 10), ("validated", 9)]),
            "Assumptions": sheet(assumption_rows, [("key", 30), ("value", 14), ("basis", 90), ("owner", 16)]),
            "Date coverage": sheet([{k: x[k] for k in ("unit", "phrase", "treatment", "by", "sentence")}
                                    for x in r.get("date_coverage", [])],
                                   [("unit", 22), ("phrase", 26), ("treatment", 14), ("by", 60), ("sentence", 80)]),
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
        if x.applied and x.op.type in ("replace_text", "set_value", "set_status", "replace_unit"):
            changed[x.op.target] = x
        if x.applied and x.op.effect == "renumbers":           # an answer citing a renumbered clause reads differently now
            for k in x.op.renumber:
                changed[k] = x
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
    md = ["# A2 Addendum reconciliation — WORKING DRAFT", "",
          f"**DRAFT.** Ops are PROPOSED (not reviewed by a person). Validated state: **{val}**"
          + (f"; working state **{r['working'].stage}** is PARTIAL and does not replace it." if r["working"] else "."),
          "Every provision of every addendum is accounted for below: by an op, as content of an op, as no effect "
          "(with the reason), or as UNRESOLVED (a person must decide it).", ""]
    changes, provs, moved, answers, summary_rows = [], [], [], [], []
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
            elif o.type == "insert_row":                      # session 09: a table row described in prose
                ch = (f"row {x.details.get('inserted') or '(not inserted)'} after {x.details.get('after') or o.after}: "
                      + "; ".join(f"{k}: {v}" for k, v in (o.cells or {}).items()))
            else:
                ch = f"{o.effect}" + (f"; mentions of '{o.subject}': {x.details.get('mentions')}" if o.subject else "") + \
                     (f" — {_short(o.note, 90)}" if o.note else "")
            if x.details.get("also_in"):
                ch += f" [same words also in {', '.join(x.details['also_in'])}: not targeted]"
            pu = s.state.get(o.provision)
            bad = "; ".join(c["id"] + ": " + c["detail"] for c in x.checks if not c["ok"])
            md.append(f"| {o.id} | {o.type} | {tgt} | {ch.replace('|', '/')} | {o.provision} p{pu.pages[0] if pu and pu.pages else '?'} | "
                      f"{('yes' if x.applied else 'no: WITHHELD (rejected by a person)') if x.valid else 'NO — ' + bad.replace('|', '/')} | "
                      f"{review.label(r['reviews'][('op', o.id)])} ({o.origin}) |")
            changes.append({"stage": s.stage, "op": o.id, "type": o.type, "target": tgt, "change": ch, "provision": o.provision,
                            "valid": x.valid, "withdrawn": x.withdrawn, "applied": x.applied, "failed_checks": bad, "review": review.label(r["reviews"][("op", o.id)]), "origin": o.origin,
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
        sc = next((x for x in r.get("summary_check", []) if x["stage"] == s.stage), None)
        if sc is not None:
            md += ["", "### Cover summary vs provisions (C28)", "",
                   "The cover summary is the Authority's description of the addendum. It is never applied: only the "
                   "provisions are. Report only; a person decides whether a difference needs a clarification.", ""]
            if sc["cover"]:
                md += [f"Summary ({sc['cover']} p{sc['page']}): “{sc['sentence']}”", "",
                       "| # | Claim | Matched | Status |", "|---|---|---|---|"]
                for c in sc["claims"]:
                    extra = [q for q in c["matched_provisions"] if q.replace(":", "/", 1) not in c["matched"]]
                    shown = c["matched"] + extra[:3] + ([f"and {len(extra) - 3} more no-effect provisions"] if len(extra) > 3 else [])
                    md.append(f"| {c['n']} | {c['text']} | {', '.join(shown) or '—'} | {c['status']} |")
                md.append("")
            md += [f"- **{f['kind']}**: {f['detail']}".replace("|", "/") for f in sc["findings"]] or \
                  ["No omission or contradiction found."]
            summary_rows += [{"stage": s.stage, "kind": f["kind"], "claim": f.get("claim", ""), "op": f.get("op", ""),
                              "provision": f.get("provision", ""), "detail": f["detail"]} for f in sc["findings"]]
        nb = [c for c in s.coverage if c["disposition"] == "no_effect" and "non-binding" in c["reason"]]
        if nb:
            md += ["", "### Non-binding statements (context only; not answers, not revoked, not applied)", ""]
            md += [f"- `{c['provision']}`: {_short(c['text'], 160)}" for c in nb]
        md += ["", "### Provision coverage", "", "| Provision | Page | Disposition | Accounted by | Reason |", "|---|---|---|---|---|"]
        for c in s.coverage:
            disp = c["disposition"].upper() if c["disposition"] in ("unresolved", "UNACCOUNTED") else c["disposition"]
            md.append(f"| {c['provision']} | {c['page']} | {disp} | {', '.join(c['accounted_by'])} | {c['reason'].replace('|', '/')} |")
            provs.append({"stage": s.stage, **{k: c[k] for k in ("provision", "page", "disposition", "reason")},
                          "accounted_by": c["accounted_by"], "text": c["text"]})
        md.append("")
    md += ["## Evidence chains (rows changed by an addendum)", ""]
    for e in r["evals"]:
        ch = e["stages"][r["order"][-1]]["chain"]
        if len(ch) > 1:
            md.append(f"- **{e['row'].id}**: " + " ← ".join(reversed(ch)))
    return {"markdown": "\n".join(md) + "\n", "changes": changes, "provisions": provs, "rows_moved": moved, "answers": answers,
            "summary": summary_rows}


# ---------------------------------------------------------------------------------------------- A3

MISSING_DOC_WORDS = ("not supplied", "not in the pack", "referenced but", "not provided")
A3_CLASS_ORDER = (("rejection", "Rejection"), ("disqualification", "Disqualification"),
                  ("non_responsive", "Non-responsive"),
                  ("exclusion", "Exclusion (Arabic text only; not equated with the other categories; I-F4C-EXCLUSION)"))


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
    refused, zero, gate = [], [], []          # session 09: document_refusal and criterion_zero; the gate's row ids
    summary_currency_cache = summary_currency(r)
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
        narrowed = []                    # clarifications that add to, narrow or renumber the row's units
        for uid in row.units:
            for oid in (val.state[uid].annotations if uid in val.state else []):
                x = r["register"]._op_by_id(oid)
                if x is not None and x.op.effect in ("adds_obligation", "interprets", "renumbers") and oid not in narrowed:
                    narrowed.append(oid)
        if narrowed:
            flags.append("see " + ", ".join(narrowed))
        stale_fig = [x["figure"] for x in summary_currency_cache if x["row"] == row.id]
        if stale_fig:
            flags.append("SUMMARY OUT OF DATE: " + ", ".join(stale_fig) + " no longer in the text; the quote governs")
        if ev["status"].startswith("NEW"):
            flags.append("new by addendum")
        elif ev["status"].startswith("REINSTATED"):
            flags.append("reinstated by addendum")
        elif ev["status"].startswith("AMENDED") or "as amended" in ev["status"]:
            flags.append("amended by addendum")
        csrc = (ev.get("consequence_source") or {}).get("latest")
        rsrc = ev.get("source") or {}
        base = {"id": row.id, "text": _a3_text(row.requirement, it.quote if it else ""), "confidence": row.confidence,
                "flags": flags, "row_source": rsrc.get("latest", "")}
        if csrc and rsrc.get("latest") and (rsrc.get("from_amendment") or " as amended by " in rsrc["latest"]) \
                and rsrc["latest"] != csrc:
            csrc = f"{csrc}; the requirement as amended: {rsrc['latest']}"   # e.g. the deadline amendment beside 6.6
        if isinstance(cons, Consequence) and cons.cls in BID_OUT:
            cu = val.state.get(cons.unit)
            explicit.append({**base, "cls": cons.cls, "class": CLASS_WORDS[cons.cls], "consequence": cons.quote,
                             "gloss": cons.gloss, "source": csrc or _doc_ref(cons.unit, cu.pages if cu else [], cu.number if cu else None)})
        elif isinstance(cons, Consequence) and cons.cls == "score_elimination":
            score.append({**base, "cls": cons.cls, "class": CLASS_WORDS[cons.cls], "consequence": cons.quote,
                          "source": csrc or _doc_ref(cons.unit, val.state[cons.unit].pages, val.state[cons.unit].number)})
        elif isinstance(cons, Consequence) and cons.cls in ("document_refusal", "criterion_zero"):
            cu = val.state.get(cons.unit)
            (refused if cons.cls == "document_refusal" else zero).append(
                {**base, "cls": cons.cls, "class": CLASS_WORDS[cons.cls], "consequence": cons.quote, "gloss": cons.gloss,
                 "source": csrc or _doc_ref(cons.unit, cu.pages if cu else [], cu.number if cu else None)})
            if cons.cls == "document_refusal" and row.assessment == "pass_fail":
                gate.append(row.id)                  # the refusal is stated; the Proposal's fate is the gate's
        elif not isinstance(cons, Consequence) and row.assessment == "pass_fail":
            none_stated.append({**base, "consequence": "", "source": base["row_source"]})
            gate.append(row.id)
    shown = [i for i in issues if i["show_in_a3"]]
    missing = [i for i in shown if any(w in i["text"].lower() for w in MISSING_DOC_WORDS)]
    unresolved = [i for i in shown if i not in missing]
    # every open issue, grouped by theme (complete, concise); an issue another one folds in is listed with it
    folded = {f: i["id"] for i in issues for f in i.get("folds") or []}
    clar = r.get("clarifications") or {}
    groups = []
    for key, title in ISSUE_THEMES:
        members = [i for i in issues if issue_theme(i) == key and i["id"] not in folded]
        qs = sorted({q["id"] for q in clar.get("clarifications", []) if q.get("theme") == key})
        if not members and not qs:
            continue
        groups.append({"key": key, "title": title, "items": [
            {"id": i["id"], "short": issue_short(i), "owner": i["owner"],
             "folds": [f for f in i.get("folds") or [] if f in {x["id"] for x in issues}]} for i in members],
            "questions": qs})
    pdd = next((d["anchor_value"] for e in r["evals"] for d in e["stages"][v]["dates"] if d["anchor"] == "PDD"), None)
    working = r["working"]
    compact = lambda x: {**x, "compact": True}  # noqa: E731  (the consequence quote is on a3_detail.html; nothing cut)
    sections = []
    for cls, title in A3_CLASS_ORDER:
        items = [compact(x) for x in explicit if x["cls"] == cls]
        if items:
            sections.append({"heading": f"Explicit — {title}: {len(items)}", "note": "", "items": items})
    sections.append({"heading": f"Explicit — Envelope B returned unopened (technical score below the threshold): {len(score)}",
                     "note": "", "items": [compact(x) for x in score]})
    # session 09: shown only when the register has such rows (the real pack has none, so its A3 is unchanged)
    # one short line each (the requirement, flags and confidence are on a3_detail.html): a refused row shows the refusal's
    # own words and where they are; a zero-marks row its requirement and the words
    short_src = lambda x: x["source"].split(";")[0]  # noqa: E731
    if zero:
        sections.append({"heading": f"Criterion-level zero marks (scored; not a disqualification): {len(zero)}",
                         "note": "Scored, not a disqualification, and not the VOL-I 11.3 threshold; any threshold risk is "
                                 "stated in the row.",
                         "items": [{"id": x["id"], "text": x["text"], "consequence": x["consequence"], "class": "",
                                    "source": short_src(x)} for x in zero]})
    if refused:
        sections.append({"heading": f"Document refused (stated; the Proposal's fate is not stated: VOL-I 11.1(i) gate applies): "
                                    f"{len(refused)}",
                         "note": "The refusal is stated; the Proposal's fate is not. Not a disqualification: each pass or fail "
                                 "row stays in the gate below.",
                         "items": [{"id": x["id"], "text": f"“{x['consequence']}”", "source": short_src(x)} for x in refused]})
    sections.append({"heading": f"General gate — mandatory compliance, pass or fail (VOL-I 11.1(i)): {len(gate)}",
                     "note": "These clauses state no consequence of their own. Each is checked pass or fail at stage (i) of the "
                             "evaluation; only Proposals that pass go on to technical evaluation (11.1(ii)). No clause-specific "
                             "label, curability or incurability is implied (I-NO-CONSEQUENCE)."
                             + (" It also holds the rows whose document is refused (above)." if len(gate) > len(none_stated)
                                else ""),
                     "items": [], "ids": gate})
    n_rows = len(r["evals"])
    rc = _count(r["reviews"][("row", e["row"].id)]["status"] for e in r["evals"])
    readings = sorted({(u["reading"]["region"], u["reading"]["status"]) for u in r["units"]
                       if (u.get("reading") or {}).get("region") and u["kind"] != "region"})
    pend = [g for g, st in readings if st == "pending"]
    banner = ("WORKING DRAFT — every register row and amendment op is PROPOSED: "
              + ", ".join(f"{k} {n}" for k, n in sorted(rc.items())) + " rows. "
              + (f"Image readings pending the owner's review: {', '.join(pend)}. " if pend else
                 "Image readings: transcriptions confirmed by the owner (approval file); their interpretations are proposed. ")
              + "Explicit wording only. Quotations, sources and flags for every line: a3_detail.html.")
    return {
        "title": "A3 — What would put this bid out (working draft)",
        "subtitle": f"Validated state {v} (issued {val.issued}); Proposal Due Date "      # from the anchor's effective text
                    + (" ".join(str(x) for x in map((r["anchor_details"][v].get("PDD") or {}).get, ("date", "time", "tz")) if x)
                       or "not stated in the effective text")
                    + (f". Working state {working.stage} is PARTIAL and NOT used here" if working else "")
                    + f". {n_rows} register rows; {len(explicit)} with an explicit consequence.",
        "banner": banner,
        "sections": sections,
        "groups": {"heading": f"Unresolved matters, grouped — {sum(len(g['items']) for g in groups)} open issues"
                              + (f", {len(clar.get('clarifications', []))} clarification questions drafted (not sent)"
                                 if clar.get("clarifications") else ""),
                   "note": "Each id links to its text and owner (a3_detail.html); the questions are in the A4 clarification "
                           "register. Unknown answers stay unknown.", "groups": groups},
        "missing": {"heading": f"Referenced but not supplied — impact: {len(missing)}",
                    "items": [{"id": i["id"], "text": i.get("a3") or i["text"], "owner": i["owner"]} for i in missing]},
        "unresolved": {"heading": f"Could not resolve — kept with people: {len(unresolved)}",
                       "items": [{"id": i["id"], "text": i.get("a3") or i["text"], "owner": i["owner"]} for i in unresolved]},
        "footer": "tenderpack: evidence build + curation + config/assumptions.yaml. Each id links to a3_detail.html "
                  "(quotes, sources, flags) and traces to A1 and A2.",
        "explicit": explicit, "score": score, "none_stated": none_stated,
        "none_stated_ids": [x["id"] for x in none_stated],
        "explicit_ids": [x["id"] for x in explicit],
        **({"refused": refused, "gate_ids": gate} if refused else {}), **({"criterion_zero": zero} if zero else {}),
        "issues_detail": [{"id": i["id"], "text": i["text"], "owner": i["owner"], "rows": i["rows"],
                           "theme": dict(ISSUE_THEMES).get(issue_theme(i), ""), "folded_into": folded.get(i["id"], "")}
                          for i in issues],
        "clarifications": clar.get("clarifications", []),
    }


def condense_a3(a3d: dict, level: int) -> dict:
    """What goes on the one page when the full text does not fit at a readable size (C43). The explicit
    consequences are never condensed. Level 1: issue lines become their linked ids and owners. Level 2: the
    no-consequence list becomes a count. Level 3 (session 09): each group of open issues becomes its count. Each
    step is stated on the page; the full text is on a3_detail.html."""
    if level == 0:
        return a3d
    page = {**a3d, "sections": [dict(s) for s in a3d["sections"]]}
    note = "condensed to fit one page: the text of each item is on a3_detail.html"
    for key in ("missing", "unresolved"):
        sec = a3d[key]
        page[key] = {"heading": sec["heading"], "note": note,
                     "ids": [i["id"] for i in sec["items"]], "owners": {i["id"]: i.get("owner") for i in sec["items"]}}
    if a3d.get("groups"):
        page["groups"] = {**a3d["groups"], "note": a3d["groups"]["note"] + " " + note.capitalize() + ".",
                          "groups": [{**g, "items": [{**i, "short": ""} for i in g["items"]]} for g in a3d["groups"]["groups"]]}
    if level >= 2:
        for sec in page["sections"]:
            if sec.get("ids"):
                sec["note"], sec["ids"] = f"{len(sec['ids'])} rows, listed on a3_detail.html ({note})", []
    if level >= 3 and a3d.get("groups"):
        page["groups"] = {**page["groups"], "note": a3d["groups"]["note"] + " Condensed to fit one page: the count of "
                          "each group is shown; its issue ids, text and owners are on a3_detail.html.",
                          "groups": [{**g, "items": [], "questions": [], "count": len(g["items"]),
                                      "n_questions": len(g.get("questions") or [])} for g in a3d["groups"]["groups"]]}
    page["subtitle"] = a3d["subtitle"] + f" Condensed (level {level}) to fit one page."
    return page


_FIG = re.compile(r"\d+(?:[.,]\d+)*%?")


def _a3_text(requirement: str, quote: str) -> str:
    """The A3 line: the requirement in full and, when the requirement does not state every figure of the words the
    current interpretation relies on (a threshold, an amount, a period), those words verbatim. Never truncated."""
    missing = [f for f in _FIG.findall(quote or "") if f not in requirement]
    return requirement + (f" — “{quote}”" if missing else "")


def a3_detail_html(a3d: dict) -> str:
    """The supporting detail for A3: every line with its full quotation, latest source, flags and confidence."""
    import html as _h
    esc = lambda t: _h.escape(t or "", quote=False)  # noqa: E731

    def quote(t):
        rtl = any("\u0600" <= c <= "\u06ff" for c in t or "")
        return f'<span dir="rtl" lang="ar">{esc(t)}</span>' if rtl else esc(t)
    rows = []
    tables = [("Explicit consequences", a3d["explicit"]), ("Envelope B returned unopened", a3d["score"])]
    if a3d.get("criterion_zero"):                                     # session 09: only when there are such rows
        tables.append(("Criterion-level zero marks (scored; not a disqualification)", a3d["criterion_zero"]))
    if a3d.get("refused"):
        tables.append(("Document refused (the Proposal's fate is not stated; in the VOL-I 11.1(i) gate)", a3d["refused"]))
    tables.append(("Pass/fail with no stated consequence", a3d["none_stated"]))
    for title, items in tables:
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
    rows.append(f"<h2>Open issues ({len(a3d['issues_detail'])}), by group</h2><table><tr><th>Issue</th><th>Group</th>"
                "<th>Text</th><th>Owner</th><th>Rows</th></tr>")
    rows += [f'<tr id="{esc(i["id"])}"><td><b>{esc(i["id"])}</b></td><td>{esc(i.get("theme", ""))}'
             + (f'<br><small>listed with {esc(i["folded_into"])}</small>' if i.get("folded_into") else "")
             + f'</td><td>{esc(i["text"])}</td><td>{esc(i["owner"])}</td><td>{esc(", ".join(i["rows"]))}</td></tr>'
             for i in sorted(a3d["issues_detail"], key=lambda i: (i.get("theme", ""), i["id"]))]
    rows.append("</table>")
    if a3d.get("clarifications"):
        rows.append(f"<h2>Clarification questions drafted, not sent ({len(a3d['clarifications'])})</h2><p>Full register "
                    "(sources, impact, interim handling): A4 clarification register.</p><table><tr><th>Id</th><th>Clause</th>"
                    "<th>Gap</th><th>Proposed question</th><th>Interim handling</th><th>Status</th></tr>")
        rows += [f'<tr id="{esc(q["id"])}"><td><b>{esc(q["id"])}</b></td><td>{esc(q.get("volume", ""))} {esc(str(q.get("clause", "")))} '
                 f'p{esc(str(q.get("page", "")))}</td><td>{esc(q.get("gap", ""))}</td><td>{esc(q.get("proposed_question", ""))}</td>'
                 f'<td>{esc(q.get("interim_handling", ""))}</td><td>{esc(q.get("response_status", ""))}</td></tr>'
                 for q in a3d["clarifications"]]
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
        progs[s.stage] = plan(s.stage, r["evals"], r["templates"], r["assumptions"], r["register"].cal_by_stage[s.stage], date.fromisoformat(s.issued),
                              anchors_by_stage[s.stage], evidence_items=r["evidence_items"],
                              anchor_details=r["anchor_details"][s.stage], notified_days=r["non_working_days"].get(s.stage))
    return progs


# ---------------------------------------------------------------------------------------------- write

def write(r: dict, out: Path) -> dict:
    progs = a5_all(r)
    val = r["validated"].stage
    main = progs.get(val)
    issues = collect_issues(r, main)
    a3d = a3(r, issues, main)
    a3_fit: dict = {}
    for level in (0, 1, 2, 3):
        page = condense_a3(a3d, level)
        try:
            fit = write_a3_pdf(page, out / "a3" / "a3.pdf")
            a3_fit = dict(fit, explicit_ids=a3d["explicit_ids"], condensed=level)
            a3d["condensed"] = level
            break
        except A3OverflowError as e:
            a3_fit = {"pages": 0, "error": str(e), "explicit_ids": a3d["explicit_ids"], "condensed": level}
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
    write_csv_json(tbl(a2d["summary"]), out / "a2", "a2_cover_summary_check")
    if r.get("clarifications"):
        clarify.write(r["clarifications"], out / "a4")              # the detailed register sits with A4
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
    from .batches import write_batches
    write_batches(r, out / "review", r["evidence_dir"])
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
              "| A1 compliance register (every row), status at each stage, review decisions | a1/a1.xlsx, a1/a1.csv, a1/a1.json |",
              "| A2 reconciliation: changes, rows that move, answers to review, provision coverage, evidence chains | a2/a2.md, a2/*.csv, a2/*.json |",
              "| A3 one-page disqualification sheet, with linked detail | a3/a3.pdf, a3/a3_detail.html, a3/a3.json |",
              "| A5 programme, marshalling plan, documents, resources, infeasibility drivers, scenarios, replan deltas, Gantt | a5/*.csv, a5/*.json, a5/gantt.*, a5/scenarios/, a5/stages/ |",
              "| A4 supporting record: tender clarification register (DRAFT questions, NOT SENT) | a4/clarification_register.md, .csv, .json |",
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
    for kind, what, ids in (("row", "register rows", [e["row"].id for e in r["evals"]]),
                            ("op", "amendment op(s)", [x.op.id for s in r["stages"][1:] for x in s.ops])):
        st = [r["reviews"][(kind, i)] for i in ids]
        open_ = [i for i, s in zip(ids, st) if s["status"] != "accepted"]
        if not open_:
            continue
        c = _count(s["status"] for s in st if s["status"] != "accepted")
        flags = sum(1 for s in st if s.get("flag_only"))
        out.append({"kind": "approval", "detail": f"{len(open_)} of {len(ids)} {what} not accepted by a person (a named "
                    "decision bound to the current content): " + ", ".join(f"{k} {n}" for k, n in sorted(c.items()))
                    + (f"; {flags} carry the file flag 'accepted' with no bound decision (not counted)" if flags else "")
                    + ("; rejected: " + ", ".join(i for i, s in zip(ids, st) if s["status"] == "rejected")
                       if c.get("rejected") else "")})
    return out


def _count(values) -> dict[str, int]:
    out: dict[str, int] = {}
    for v in values:
        out[v] = out.get(v, 0) + 1
    return out


# ---------------------------------------------------------------------------------------------- check-register

BID_STAGE = ("pass_fail", "scored", "procedural")


def deleted_words(r: dict) -> list[dict]:
    """Rows still in force whose quote vanished at a stage because an op of that stage deleted words from one of their
    units (a replace_text with nothing put in the words' place) while the unit itself stays in force (session 09).
    The register cannot tell whether the obligation survives in the remaining words (re-make the reading) or went
    with the deleted ones (mark the interpretation `removed: {by: <op>}`); a person says which."""
    reg, out = r["register"], []
    for e in r["evals"]:
        row = e["row"]
        for s in r["stages"][1:]:
            ev, it = e["stages"][s.stage], reg.interp_at(row, s.stage)
            if not ev["active"] or it is None or found(it.quote, ev["text"]):
                continue
            mine = set(row.units) | {ev["effective_unit"]}
            for x in s.ops:
                o = x.op
                if x.applied and o.type == "replace_text" and not (o.new or "").strip() and o.target in mine \
                        and found(it.quote, x.details.get("before") or "") and s.state[o.target].status == "active":
                    out.append({"kind": "deleted_words", "where": row.id, "detail": (
                        f"{s.stage}: the quote '{it.quote[:80]}' is no longer in {o.target}: {o.id} deleted "
                        f"'{(o.old or '')[:80]}' and {o.target} stays in force. Re-make the reading at {s.stage} if the "
                        f"obligation survives in the remaining words, or mark the interpretation `removed: {{by: {o.id}}}` "
                        "if it went with the deleted words")})
    return out


def register_findings(r: dict) -> list[dict]:
    """Everything a register drafter must clear, as {kind, where, detail}: register files that do not load,
    unit dispositions and their links to rows, the evidence-item vocabulary, quotes, units, bid-stage rows
    without a deliverable, unlinked consequence words (C15) and quotes lost to a deletion of words from a unit that
    stays in force (deleted_words: re-make the reading or mark it `removed`). Used by check-register (exit 1) and by the
    release gate (each kind other than quotes, which C16 already checks structurally, is a coverage blocker)."""
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
        if row.assessment == "contractual_post_award" and not row.evidence and row.post_award_evidence is None \
                and not (row.no_deliverable or "").strip():
            out.append({"kind": "deliverable", "where": row.id, "detail": "post-award row with a blank 'evidence needed': "
                        "give a proposed evidence requirement, a justified not-applicable entry or an unresolved specification"})
        pa = row.post_award_evidence
        if pa is not None:
            need = {"proposed": "when", "not_applicable": "reason", "unresolved": "missing"}[pa.kind]
            if not getattr(pa, need):
                out.append({"kind": "deliverable", "where": row.id, "detail": f"post_award_evidence ({pa.kind}) has no `{need}`"})
            units = {u["unit_id"]: u for u in r["units"]}
            for b in pa.basis:
                u = units.get(b.get("unit"))
                if u is None or not found(b.get("words", ""), u.get("text", "")) or b.get("page") not in u.get("pages", []):
                    out.append({"kind": "quote", "where": row.id, "detail": f"post_award_evidence basis not found as quoted: "
                                f"{b.get('unit')} p{b.get('page')} '{str(b.get('words'))[:80]}'"})
    c14, c15 = r["sweeps"]
    for h in c15:
        out.append({"kind": "C15", "where": h["unit"], "detail": f"consequence word '{h['word']}' ({h['lang']}) not linked "
                    f"to a row's consequence or a consequence_note: {h['sentence'][:140]}"})
    for t in r.get("trace", []):
        out.append({"kind": "C46", "where": t["op"], "detail": f"[{t['output']}] {t['detail']}"})
    for x in summary_currency(r):
        out.append({"kind": "summary", "where": x["row"], "detail": f"the requirement summary states '{x['figure']}', which "
                    "the effective text no longer contains: rewrite the summary (or make it stage-neutral)"})
    out += deleted_words(r)
    for x in r.get("date_coverage", []):
        if x["treatment"] == "UNCOVERED":
            out.append({"kind": "C30", "where": x["unit"], "detail": f"date/period phrase '{x['phrase']}' accounted for by no "
                        f"rule, anchor, quote, date note or disposition: {x['sentence'][:140]}"})
    for i in r.get("ids", {}).get("new", []):
        out.append({"kind": "C12", "where": i, "detail": "row id not yet recorded in the id ledger (check-register --update-ids)"})
    for p in clarify.check(r.get("clarifications") or {}, r["units"], set(r["curated_issues"]),
                           cutoff=clarify.effective_cutoff(r)):           # the effective cut-off (session 09)
        out.append({"kind": "clarification", "where": p.split(":")[0], "detail": p})
    return out


def update_ids(r: dict) -> int:
    """C12: record every current row id in the ledger (a curation step, not a review). Ids are never removed here; a
    row taken out of the register must be entered under `withdrawn:` with a reason, by hand."""
    path = r["ids"]["path"]
    data = (load_yaml(path) or {}) if path.exists() else {}
    ids = dict(data.get("ids") or {})
    new = [e["row"].id for e in r["evals"] if e["row"].id not in ids]
    for i in new:
        ids[i] = {"first_listed": date.today().isoformat()}
    write_text(path, "# Every A1 row id ever listed (C12). Maintained by `tenderpack check-register --update-ids`; a row\n"
                     "# removed from the register must be listed under `withdrawn:` with the reason, so ids never vanish.\n"
               + yaml.safe_dump({"ids": dict(sorted(ids.items())), "withdrawn": data.get("withdrawn") or {}},
                                allow_unicode=True, sort_keys=False))
    print(f"recorded {len(new)} new row id(s) in {path}")
    return 0


def check_register(evidence_dir: Path, pack_path: Path, root: Path, doc: str | None = None, update: bool = False) -> int:
    r = run(Path(evidence_dir), Path(pack_path), Path(root), lenient=True)
    if update:
        update_ids(r)
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
