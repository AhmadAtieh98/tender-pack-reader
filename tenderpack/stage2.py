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
validated state, and the working A5 is written to out/a5/working/. Beside them (session 11, partial.py), the
candidate A3 and A5 of the working stage, labelled NOT VALIDATED: out/a3/a3_candidate.{pdf,md,html,json} and
out/a5/candidate/ (what would enter, leave or move, with the source ops, the blockers and the conditional scenarios).

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
  C52 no output calls the translation of an approved image reading 'not reviewed' (session 11, audit A3-4/R-1)
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
from .register import (BID_OUT, GLOSS_NOT_REVIEWED, Consequence, Register, consequence_gloss, found, load_rows,
                       printed_date_conflicts)
from .readings import approval_covers
from .render import A3OverflowError, write_a1, write_a3_pdf, write_csv_json
from . import programme
from .schedule import a3_rows, deltas, in_force, plan
from .trace import obligation_trace
from .summary import date_changes_by_stage, rule_index, summary_check
from .datecover import counting_conventions, date_coverage
from . import clarify, derived, human_owned, relationships, review, signals
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
    rel_path = relationships.default_path(cfg, root)               # session 10: curated indirect links
    try:
        rels, rel_problems = relationships.load(rel_path), []
    except Exception as e:                                   # noqa: BLE001
        if not lenient:
            raise
        rels, rel_problems = [], [f"{rel_path.name}: skipped, does not load: {str(e)[:300]}"]
    r = {"cfg": cfg, "root": root, "units": units, "problems": problems, "assumptions": assumptions, "cal": cal, "policy": policy,
         "templates": templates, "curated_issues": curated_issues, "rowfile": rowfile, "opfiles": opfiles,
         "drafted": drafted, "dispositions": dispositions,
         "disposition_problems": dproblems + check_dispositions(units, dispositions, rowfile.rows),
         "evidence_items": evidence_items, "evidence_problems": eproblems,
         "load_problems": load_problems + issue_problems + rel_problems,
         "sweeps": check_sweeps(units, dispositions, rowfile.rows), "decisions_file": decisions_file, "decisions": decisions,
         "evidence_dir": Path(evidence_dir), "clarifications": clarify.load(cfg, root),
         "relationships": rels, "relationships_path": rel_path}
    return evaluate(r)


def engine_for(r: dict):
    """The amendment engine over the inputs held in `r`: the units, the op files, the ops a person rejected (withheld)
    and, session 11, the trigger facts a person recorded for conditional ops (amend.load_triggers; the file named by
    the pack config's `triggers:` or curation/triggers.yaml; none when it does not exist). Nothing assumes a trigger."""
    from .amend import load_triggers, triggers_path
    triggers = load_triggers(triggers_path(r["cfg"], r["root"]))
    return Engine(r["units"], r["opfiles"], review.withdrawn_ops(r["decisions"]), triggers=triggers)


def evaluate(r: dict) -> dict:
    """The amendment path, register, review statuses and reported analyses from the inputs held in `r` (units, op
    files, rows, decisions, calendar). One pass: every op whose latest named decision is a rejection is withheld
    (review.withdrawn_ops), and each decision is bound to a subject captured before its op runs, so withholding an
    op never changes what its rejection is bound to (no rebuild can flip a rejected op back into force)."""
    units, cfg, root = r["units"], r["cfg"], r["root"]
    r.pop("_unit_evidence", None)                        # recomputed from the units by review.row_binding
    stages = engine_for(r).run()
    val = validated_stage(stages)
    reg = Register(r["rowfile"], stages, r["cal"], r["policy"])
    r["non_working_days"] = {s.stage: list(s.non_working_days) for s in stages}   # days notified under VOL-I 2.4
    r.update({"stages": stages, "validated": val, "working": stages[-1] if stages[-1].stage != val.stage else None,
              "register": reg, "evals": reg.all(), "order": [s.stage for s in stages]})
    from .register import anchor_details      # date, time, timezone and source of each anchor, from its effective text
    r["anchor_details"] = {s.stage: anchor_details(s.state, r["rowfile"].anchors, reg.issued, reg.op_stage,
                                                   reg.op_provision) for s in stages}
    from .signals import attach_dependencies  # session 12 (F2): what each row depends on, for the one change predicate
    attach_dependencies(r)
    from .signals import attach_pending       # session 12 (F5): a row under an undecided human-owned issue: NOT SETTLED
    r["issue_stages"] = issue_stages(r)        # session 13 (F4; audit R1-7, R1-9): A1's set, from its stage
    attach_pending(r, row_issues(r), r["issue_stages"])
    r["reviews"] = review.compute(r, r["decisions"])
    r["trace"] = obligation_trace(r)
    r["summary_check"] = summary_check(r["stages"], units, r["rowfile"].anchors,    # C28: report only, never applied
                                       rule_index(r["rowfile"].rows),
                                       date_changes=date_changes_by_stage(r["evals"], r["order"]))
    r["date_coverage"] = date_coverage(r)
    r["c32"] = counting_conventions(r)
    # session 10: what each addendum reaches through the curated relationships (labelled classes, never merged with the
    # direct-citation changes); A2, A3, A5 and `diff` read it
    r["relationship_impact"] = relationships.impact(r)
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
    n13 = (a3_fit or {}).get("count_words") or f"{len(a3_ids)} A3 items"   # session 13 (F2; audit R2-9): one count
    checks.append({"id": "C13", "ok": not bad13, "detail": f"{n13}, each row with an explicit quoted consequence"
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


STALE_GLOSS_WORDS = ("not reviewed", "proposed translation", "translation proposed")


def gloss_currency_check(r: dict, out: Path) -> dict:
    """C52 (session 11, audit A3-4/R-1): every consequence gloss that the approval state labels as a confirmed
    translation (register.consequence_gloss) must not be called 'not reviewed' or a 'proposed translation' in any written
    output: A1 (csv, json), A2, A3 (json, html, md, pdf text), the review batches. Each occurrence of the gloss is checked
    against the 80 characters before it."""
    import html as _h
    glosses = sorted({it.consequence.gloss for e in r["evals"] for it in e["row"].interpretations
                      if isinstance(it.consequence, Consequence) and it.consequence.gloss
                      and consequence_gloss(r, e["row"], it.consequence) != GLOSS_NOT_REVIEWED})
    files = [p for p in sorted(Path(out).rglob("*")) if p.is_file() and p.suffix in (".csv", ".json", ".md", ".html", ".pdf")
             and p.name not in ("checks.json",)]
    bad = []
    for p in files:
        try:
            if p.suffix == ".pdf":
                import pymupdf
                with pymupdf.open(p) as doc:
                    text = " ".join(" ".join(pg.get_text().split()) for pg in doc)
            else:
                text = _h.unescape(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:                                # noqa: BLE001  an unreadable file is not this check's subject
            continue
        low = " ".join(text.split()).lower()
        for g in glosses:
            for m in re.finditer(re.escape(g.lower()), low):
                if any(w in low[max(0, m.start() - 80):m.start()] for w in STALE_GLOSS_WORDS):
                    bad.append(f"{p.relative_to(out)}: '{g}'")
                    break
    return {"id": "C52", "ok": not bad,
            "detail": (f"{len(glosses)} confirmed translation(s) of approved readings; none called 'not reviewed' in "
                       "the outputs") if not bad else
                      "translation of an approved reading called 'not reviewed' or 'proposed': " + "; ".join(sorted(set(bad))[:6])}


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

def gate_rows(r: dict, stage: str | None = None) -> list[str]:
    """The rows of A3's general gate at `stage` (default: the validated stage): in force, pass_fail, and no consequence
    stated (or a stated document refusal, whose Proposal fate is the gate's). The same test as a3() applies."""
    v = stage or r["validated"].stage
    out = []
    for e in r["evals"]:
        row, ev = e["row"], e["stages"][v]
        if not in_force(ev["status"]) or row.assessment != "pass_fail":
            continue
        it = r["register"].interp_at(row, v)
        cons = it.consequence if it else "none_stated"
        if not isinstance(cons, Consequence) or cons.cls == "document_refusal":
            out.append(row.id)
    return out


def collect_issues(r: dict, a5: dict | None) -> list[dict]:
    val = r["validated"]
    rows_by_issue: dict[str, list[str]] = {}
    for e in r["evals"]:
        for i in e["row"].issues:
            rows_by_issue.setdefault(i, []).append(e["row"].id)
    # session 12 (F5; audit A3-6): the issue of the general gate (theme 'gate') lists the gate's rows as A3 derives them
    # at render time, so a row the gate drops (ADD-02-5.2-01, now scored) or gains is never out of step with it
    gate = gate_rows(r)
    for iid, it in r["curated_issues"].items():
        if it.get("theme") == "gate":
            rows_by_issue[iid] = list(gate)
    # session 13 (audit R1-2, R1-6): the rows an issue reaches through a curated relationship or a reissued form, with
    # why ('VOL-II-3.1-01 (via REL-T24-PROCESS-DESIGN (confirmed))'), listed after the rows that list it themselves
    linked_rows: dict[str, dict[str, list[str]]] = {}
    for rid, xs in row_issue_links(r).items():
        for x in xs:
            if rid not in rows_by_issue.get(x["issue"], []):
                linked_rows.setdefault(x["issue"], {}).setdefault(rid, []).append(_link_words(x))
    out = []
    links = human_owned.pending_links(r.get("clarifications"))   # session 12 (F5, audit R1-1): a pending decision's issues
    for iid, it in r["curated_issues"].items():
        # session 12: an issue the AI workflow proposed, or one carrying a status or resolution, reads HUMAN DECISION
        # PENDING until a person's decision is bound to it (tenderpack.human_owned.issue_label); open curated issues
        # are open by construction and read as before. F5 (audit A3-5, R-a, R1-1): so does one a pending decision of the
        # clarification register links, or one owned by Legal or Commercial (human_owned.pending_reasons)
        lab = human_owned.issue_label(iid, it, r.get("decisions"), links.get(iid))
        pre = (lambda t: f"{lab}: {t}" if t else t) if lab else (lambda t: t)  # noqa: E731
        out.append({"id": iid, "text": pre(it["text"]), "owner": it["owner"], "source": "curated (proposed wording)",
                    "rows": rows_by_issue.get(iid, []),
                    "rows_linked": [f"{k} ({'; '.join(dict.fromkeys(w))})" for k, w in (linked_rows.get(iid) or {}).items()],
                    "show_in_a3": bool(it.get("show_in_a3")), "a3": pre(it.get("a3")),
                    "theme": it.get("theme"), "short": pre(it.get("short")), "folds": list(it.get("folds") or [])}
                   | ({"human_decision": lab} if lab else {}))
    out += missing_document_issues(r)                           # session 10: documents referenced but not supplied
    # session 14 (W4; part 3 (b)): a class table without a rule for an item in more than one class is a genuine
    # ambiguity (blind-07 DA1), raised as a generated issue, HUMAN DECISION PENDING; nothing is chosen
    out += signals.class_scope_issues(r.get("units") or [], {e["row"].id: list(e["row"].units) for e in r["evals"]})
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
    src = {}
    for e in r["evals"]:
        for d in e["stages"][val.stage]["dates"]:
            if d["readings_differ"]:
                src.setdefault(d["rule_id"], d.get("source_unit") or "")
    differ = sorted(src)
    if differ:
        # session 12 (F5; audit A3 recheck): the page names the clause each rule comes from (the date rule's source
        # unit), not the internal rule id; A1 keeps both
        out.append({"id": "I-AUTO-COUNTING", "text": "Counting conventions not stated in the pack for "
                    + ", ".join(f"{k} ({clause_names([src[k]])})" if src[k] else k for k in differ) + ": every "
                    f"reading is shown (A1 Dates); planning uses the {r['policy']} reading (config/assumptions.yaml)",
                    "owner": "Bid manager", "source": "D4 (automatic)", "rows": [], "show_in_a3": True,
                    "a3": f"day count not stated ({clause_names(list(src.values()))}); A1 Dates: both readings; "
                          f"A5: {r['policy']}"})
    pend = sorted({e["row"].id for e in r["evals"] if e["stages"][val.stage]["transcription"] == "pending"})
    if pend:
        out.append({"id": "I-AUTO-PENDING-READINGS", "text": f"{len(pend)} row(s) rely on image readings (Table 2-4, "
                    f"Form 4-C) still pending the owner's review. Rows: {', '.join(pend)}", "owner": "Owner",
                    "source": "readings (automatic)", "rows": pend, "show_in_a3": True,
                    "a3": f"{len(pend)} row(s) rely on the image readings (Table 2-4, Form 4-C) pending the owner's review"})
    if a5:
        bad = [a for a in a5["activities"] if a["status"] != "OK"]
        for a in bad:
            # session 12 (audit A3-2, A3-4): a conditional activity's line names its condition, and the window end shows
            # every reading of its rule (the ambiguous count is never chosen: config/formulas.yaml), as A1 and A3 do
            when = next((d for e in r["evals"] for d in e["stages"][val.stage]["dates"]
                         if a.get("deadline_rule") and d["rule_id"] == a["deadline_rule"]), None)
            st = a["status"]
            if when is not None and when["planning"]["value"]:
                st = st.replace(str(when["planning"]["value"]), _when(when), 1)
            if a.get("condition") and "whether the condition arose" in st:     # the condition named where it is asked
                a3_ = st.replace("whether the condition arose", f"whether {a['condition']}", 1)
            else:
                a3_ = st + (f"; needed only if {a['condition']}" if a.get("condition") else "")
            a3_ = a3_ if a["status"].startswith("CONDITIONAL") else None
            out.append({"id": f"I-A5-{a['id']}", "text": f"A5 {a['id']}: {a['flags'][0]} ({', '.join(a['req_ids'])}; "
                        f"duration {a['duration_wd']} WD is an ASSUMPTION: {a['duration_assumption']})",
                        "owner": a["owner"], "source": "A5 (automatic)", "rows": a["req_ids"], "show_in_a3": False,
                        **({"a3": a3_} if a3_ else {})})
        late = [a for a in bad if a["status"].startswith(("INFEASIBLE", "DEADLINE PASSED"))]
        if late:
            out.append({"id": "I-A5-FEASIBILITY", "text": "A5 at the status date: " + "; ".join(
                f"{a['id']} {a['flags'][0].split(' (')[0]}" for a in late) + ". Lead times are PROVISIONAL assumptions "
                "(A5 drivers)", "owner": "Bid manager", "source": "A5 (automatic)",
                "rows": sorted({x for a in late for x in a["req_ids"]}), "show_in_a3": True,
                "a3": "A5 at the status date: " + _ids([f"{a['id']} {a['flags'][0].split(' (')[0]}" for a in sorted(
                    late, key=lambda a: (-int((re.search(r"by (\d+)", a["status"]) or [0, 0])[1]), a["id"]))], 5) + " (lead times PROVISIONAL)"})
    return out


_APPROVAL_WORDS = re.compile(r"\btranscription(?: and (?:the )?displayed translations?)?(?= confirmed by the owner)")


def confidence_reason(r: dict, row) -> str:
    """The row's curated confidence reason, with one wording for one approval (session 12, F5; audit R-b): where it says
    what the owner confirmed of an image reading the row rests on, the words are readings.approval_covers' for that
    reading ('transcription and displayed translations' when the reading displays translations, else 'transcription'),
    so rows with the same evidence read the same in A1 and batch 2."""
    from .readings import approval_covers
    regions = {}
    for u in r.get("units") or []:
        g = (u.get("reading") or {}).get("region")
        if g and (u.get("reading") or {}).get("status") == "approved":
            regions.setdefault(g, {"units": set(), "translated": False})
            regions[g]["units"].add(u["unit_id"])
            regions[g]["translated"] |= bool(u.get("translation"))
    mine = [g for g, v in regions.items() if v["units"] & set(row.units)]
    text = str(row.confidence_reason or "")
    if len(mine) != 1:
        return text
    words = approval_covers(regions[mine[0]]["translated"]).replace("the ", "")
    return _APPROVAL_WORDS.sub(words, text)


def clause_names(units: list[str]) -> str:
    """'ADD-01 3.1; VOL-I 6.3, 7.1, 8.5; Form 4-A' for source units ('VOL-I:8.5#fn12' -> VOL-I 8.5; a form's unit ->
    'Form 4-A'), each once, grouped by document in the order given."""
    by: dict[str, list[str]] = {}
    for u in units:
        if not u or ":" not in u:
            continue
        doc, local = u.split(":", 1)
        local = re.split(r"[#/]", local)[0]
        if re.fullmatch(r"F\d-[A-Z]", local):
            by.setdefault(f"Form {local[1:]}", [])
            continue
        if local not in by.setdefault(doc, []):
            by[doc].append(local)
    return "; ".join(k + (" " + ", ".join(sorted(v, key=lambda x: [int(n) if n.isdigit() else n for n in re.split(r"(\d+)", x)]))
                          if v else "") for k, v in sorted(by.items(), key=lambda kv: (kv[0].startswith("Form"), kv[0])))


def missing_document_issues(r: dict) -> list[dict]:
    """One open issue per document the relationships file records as referenced but not supplied (kind
    missing_document; session 10): where the pack refers to it, and, against each row or unit whose conclusion it
    blocks, what cannot be established, with the link's status. Theme 'missing' (A3's 'Referenced but not supplied'
    group); the curated issues it relates to are named, never resolved."""
    out = []
    curated = r.get("curated_issues") or {}
    for did, d in relationships.missing_documents(r.get("relationships") or []).items():
        refs = ", ".join(f.replace(":", " ", 1) for f in d["sources"])
        linked = sorted({i for e in d["entries"] for i in e.get("issues") or []})
        owner = next((curated[i]["owner"] for i in linked if i in curated and curated[i].get("owner")), "Bid manager")
        blocks = "; ".join(f"{', '.join(relationships.ends(e, 'to'))} ({e['id']}, link {e.get('status')}): "
                           f"{e.get('blocks')}" + (f" [{relationships.context_text(e)}]" if e.get("context") else "")
                           for e in d["entries"])                   # session 13 (audit R1-4): the context travels
        rows = sorted({t for e in d["entries"] for t in relationships.ends(e, "to") if ":" not in t})
        targets = list(d["targets"])
        out.append({"id": f"I-AUTO-NOT-SUPPLIED-{did}", "owner": owner, "source": "relationships (automatic)",
                    "text": f"{d['document']} is referenced but not supplied (referenced in {refs}). Without it these "
                            f"conclusions cannot be established: {blocks}"
                            + (f". Linked open issues: {', '.join(linked)}" if linked else "")
                            + ". Not a prerequisite for completing the bid; a person decides whether to raise a "
                              "clarification or reserve the position",
                    "rows": rows, "show_in_a3": True, "theme": "missing",
                    "a3": f"{d['document']} not supplied ({refs}): blocks conclusions on {_ids(targets, 4)}",
                    "short": f"{d['document']} not supplied: blocks {_ids(targets, 3)}", "folds": [],
                    "linked": linked})                    # session 11: A3 folds it into a linked 'missing' issue
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


_GAP_MARK = re.compile(r"(?:^|[.;:]\s+)(?:still open|open|unresolved|not resolved)\s*:\s*", re.I)
_DRAFT_REF = re.compile(r"\s*\((?:draft question|draft questions|follow-up|clarification register)\b[^()]*\)", re.I)


def gap_clause(text) -> str:
    """The clause of an issue's text that states the gap (session 12, audit A3-2): the words after the text's own
    open-point marker ('Still open:', 'Open:', 'Unresolved:'), to the end of that clause (the first ';' or sentence end
    outside brackets, or before a relative clause (', which', ', on which', ', so') that starts after 50 characters),
    without the bracketed draft-question ids (they are on the A4 register). '' when the text has no marker: such a text
    states its gap first, and its short line is that statement."""
    t = " ".join(str(text or "").split())
    m = _GAP_MARK.search(t)
    if not m:
        return ""
    rest, depth, end = t[m.end():], 0, None
    for j, ch in enumerate(rest):
        depth += (ch == "(") - (ch == ")")
        if depth <= 0 and (ch == ";" or (ch == "." and (j + 1 == len(rest) or rest[j + 1] == " "))):
            end = j
            break
    c = _DRAFT_REF.sub("", rest[:end]).strip(" ;,.")
    m2 = re.compile(r", (?:on which|which|so that|so) ").search(c, 50)   # the first clause: what follows is on the detail
    return c[:m2.start()] if m2 else c


_STOP = {"the", "and", "for", "with", "from", "that", "this", "its", "not", "are", "was", "how", "any", "all", "which",
         "whether", "under", "into", "per", "vs"}


def _content(t: str) -> set[str]:
    return {w for w in re.findall(r"[\w./-]+", re.sub(r"'s\b", "", t.lower())) if len(w) >= 3 and w not in _STOP}


def _parts(t: str) -> list[str]:
    """A short line split at its '; ' separators outside brackets."""
    out, depth, cur = [], 0, ""
    for j, ch in enumerate(t):
        depth += (ch == "(") - (ch == ")")
        if depth <= 0 and t.startswith("; ", j):
            out.append(cur)
            cur = ""
            continue
        if cur == "" and ch == " " and out and t[j - 1] == ";":
            continue
        cur += ch
    return [x.strip() for x in out + [cur] if x.strip()]


def with_reason(short: str, gap: str) -> str:
    """The short line with the reason clause of its issue (gap_clause), never longer than it must be: unchanged when it
    already says the clause; else each '; ' part of the short that the clause restates (most of its words are in the
    clause) gives way to the clause, in its place, after the part's subject (the words before a ':' or ' vs ': 'Table
    2-4: anything outside the visible image (e.g. whether a further note was cut off below Note 1)'); else the short,
    its bracketed 'settled' note giving way to the open clause, and the clause."""
    norm = lambda x: " ".join(re.sub(r"[^\w./-]+", " ", x.lower()).split())  # noqa: E731
    if not gap or norm(gap) in norm(short):
        return short
    out, placed = [], False
    for part in _parts(short):
        bare = re.sub(r"\s*\([^()]*\)", "", part).strip()
        subj = re.split(r": | vs ", bare, maxsplit=1)[0] if re.search(r": | vs ", bare) else ""
        sw = _content(bare) - _content(subj)
        if sw and len(sw & _content(gap)) >= 0.6 * len(sw):          # restated by the clause
            if not placed:
                out.append((subj + ": " if subj and not _content(subj) <= _content(gap) else "") + gap)
                placed = True
            continue
        out.append(part)
    if placed:
        return "; ".join(out)
    base = re.sub(r"\s*\([^()]*\bsettled\b[^()]*\)", "", short).strip()
    gw = gap.split()
    for k in range(len(gw) - 1, 2, -1):                  # the short ends with the clause's first words: continue it
        if norm(base).endswith(norm(" ".join(gw[:k]))):
            gap = " ".join(gw[k:])
            break
    return base + (" " if gap.startswith("(") else " — ") + gap


# a label an output puts before an issue's words (human_owned.issue_label): kept apart from the reason it prefixes
_LABEL = re.compile(r"^((?:" + re.escape(human_owned.HUMAN_DECISION_PENDING) + r"|[A-Z]{4,}(?: [A-Z]+)*)"
                    r"(?: \([^()]*\))?): ")


def folded_pending(folds: list[str], issues: list[dict], parent_owner: str | None = None) -> list[str]:
    """Session 13 (F4; audit R2-11): the issues folded under a line on the A3 page that are a person's decision not yet
    recorded (label HUMAN DECISION PENDING: human_owned.issue_label), so the parent line names them with the mark instead
    of hiding them in '+n': 'I-X, I-Y' per owner, with '(Owner)' when it is not the parent line's own owner (shown
    on the line already)."""
    by = {i["id"]: i for i in issues}
    groups: dict[str, list[str]] = {}
    for f in folds or []:
        if f in by and str(by[f].get("human_decision") or "").startswith(human_owned.HUMAN_DECISION_PENDING):
            groups.setdefault(str(by[f].get("owner") or "owner not named"), []).append(f)
    return [", ".join(ids) + (f" ({o})" if o != parent_owner else "") for o, ids in groups.items()]


def question_subject(q: dict) -> str:
    """Session 13 (F4; audit R2-12): the A3 page's label for a drafted question, from the entry's own subject words:
    the subject its topic states in brackets ('permit/table interpretation (ranges under ...)' -> 'ranges under ...';
    after a 'kind: ' prefix, the words after it), else the words of its id without the 'CQ' prefix and the reference
    codes (tokens with a digit: F4D, T24): 'CQ-F4D-GUARANTEE-SCOPE' -> 'guarantee scope'. A topic without brackets is
    a category (e.g. 'guarantee wording'), never a subject."""
    t = str(q.get("topic") or "")
    m = re.match(r"^[^()]*\((.+)\)$", t)
    if m:
        return m.group(1).split(": ")[-1]
    words = [w for w in str(q.get("id") or "").split("-")[1:] if w and not re.search(r"\d", w)]
    return " ".join(words).lower() or t or str(q.get("id"))


def issue_short(i: dict) -> str:
    """The reason of an open issue on its A3 line: the curated `a3` wording when the issue has one (session 13, F2;
    audit R2-3: the curator's page wording before any generated summary); else the curated `short` (or one made from
    the generated text), always with the clause of the issue text that states the gap (gap_clause; session 12, audit
    A3-2): never an id alone. An automatic issue's `a3` is itself generated and keeps the rule below."""
    if i.get("a3") and not str(i.get("source") or "").endswith("(automatic)"):
        return str(i["a3"])
    short, text = _issue_short(i), str(i.get("text") or "")
    m = _LABEL.match(short)
    if m and text.startswith(m.group(0)):               # the label prefixes both: the reason is read without it
        return m.group(0) + with_reason(short[m.end():], gap_clause(text[m.end():]))
    return with_reason(short, gap_clause(text))


def _issue_short(i: dict) -> str:
    if i.get("short"):
        return i["short"]
    iid = i["id"]
    if iid.startswith("I-AUTO-SUMMARY-"):
        return f"{iid.rsplit('-', 2)[-2]}-{iid.rsplit('-', 1)[-1]} cover summary vs provisions: findings in A2 (C28)"
    if iid == "I-AUTO-COUNTING":                          # session 12 (A3-2): which rules, and the reading planned
        return i.get("a3") or "counting conventions not stated for some date rules: every reading in A1 Dates"
    if iid.startswith("I-A5-") and i.get("a3"):          # session 12 (A3-2, A3-4): the condition and both readings
        return i["a3"]
    if iid == "I-AUTO-STALE":
        return "rows STALE: their reading needs a person (A1)"
    if iid.startswith("I-PARTIAL-"):
        return f"{iid[len('I-PARTIAL-'):]} PARTIAL: provisions not yet applied (A2)"
    t = (i.get("a3") or i["text"]).split(". ")[0]
    if i["id"].startswith("I-OP-") and ": " in t:                       # 'ADD-02/Q7: ...' -> the text after the op id
        t = t.split(": ", 1)[1]
    if i["id"].startswith("I-A5-") and ": " in t:                       # the id already names the activity; keep the
        t = t.split(": ", 1)[1].split(" (")[0]                           # finding itself, not its bracketed detail
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


# ---------------------------------------------------------------------------------------------- linked issues (s13)

def _form_units(state: dict, form: str) -> list[str]:
    """The units that make up `form` (a form or table id) in `state` as in force: the form and its members, each followed
    to the unit that supersedes it (a reissue), with that unit's members."""
    out: list[str] = []
    for k in [k for k in state if k == form or k.startswith(form + "/")]:
        kk, seen = k, set()
        while state[kk].status == "superseded" and state[kk].superseded_by in state and kk not in seen:
            seen.add(kk)
            kk = state[kk].superseded_by
        for m in [kk] + [x for x in state if x.startswith(kk + "/")]:
            if m not in out:
                out.append(m)
    return out


def _form_text(state: dict, form: str) -> list[tuple[str, str]]:
    return [(k, state[k].text or "") for k in _form_units(state, form) if state[k].status == "active"]


def reissued_form_gaps(rows, stages, quote_at) -> dict[str, list[dict]]:
    """Session 13 (audit R1-6): row id -> [{stage, evidence, form, unit, form_row, flag, issues}] for a row whose evidence
    item is a form (or table) that a stage reissues or changes, when the words the row relies on (its quote at the
    earlier stage, `quote_at(row, stage)`) were printed in the form as it stood and are not in the form in force at the
    stage. An evidence item's forms are the parts (the unit id before '/') of the rows that list it and cite a member;
    those rows are the form's own rows and are not checked against themselves. `issues`: the open issues of the form row
    that printed the words which the row does not already list. `stages`: [(stage, state)] in order. Flags only; nothing
    is decided or rewritten."""
    forms: dict[str, dict[str, list]] = {}
    for row in rows:
        for u in row.units:
            if "/" in u:
                for ev in row.evidence:
                    lst = forms.setdefault(ev, {}).setdefault(u.split("/", 1)[0], [])
                    if row not in lst:
                        lst.append(row)
    out: dict[str, list[dict]] = {}
    texts: dict[tuple[int, str], list[tuple[str, str]]] = {}
    # session 14: a form's text at a stage is scanned once per call, not once per row that cites it; the function stays
    # pure (the states live in `stages` for the whole call, so id() is a stable key here and nowhere else)

    def form_text(state: dict, f: str) -> list[tuple[str, str]]:
        key = (id(state), f)
        if key not in texts:
            texts[key] = _form_text(state, f)
        return texts[key]

    for row in rows:
        for ev in dict.fromkeys(row.evidence):
            for f, frows in (forms.get(ev) or {}).items():
                if any(u == f or u.startswith(f + "/") for u in row.units):
                    continue
                for (ps, pst), (s, st) in zip(stages, stages[1:]):
                    before, after = form_text(pst, f), form_text(st, f)
                    if before == after:
                        continue
                    q = quote_at(row, ps)
                    hit = next((k for k, t in before if q and found(q, t)), None)
                    if hit is None or any(found(q, t) for _, t in after):
                        continue
                    frow = next((x for x in frows if hit in x.units), None)
                    rid = frow.id if frow is not None else hit
                    out.setdefault(row.id, []).append({
                        "stage": s, "evidence": ev, "form": f, "unit": hit, "form_row": rid,
                        "flag": f"evidence field not on the reissued form ({rid})",
                        "issues": [i for i in (frow.issues if frow is not None else []) if i not in row.issues]})
    return out


def row_issue_links(r: dict) -> dict[str, list[dict]]:
    """Session 13 (audit R1-2, R1-6): row id -> the issues linked to the row besides its own `issues`, each with why:
    {issue, via, status} for a curated relationship naming the row in `to` (relationships.issue_links), {issue, why} for
    an evidence field the reissued form no longer prints (reissued_form_gaps). One rule for every issue; nothing is
    resolved."""
    rows = [e["row"] for e in r.get("evals") or []]
    # session 14 (W4): an issue travels along a relationship only within its scope (relationships.issue_reaches)
    out = relationships.issue_links(r.get("relationships") or [], {x.id for x in rows}, *issue_scope_args(r))
    reg = r.get("register")
    quote_at = lambda row, st: getattr(reg.interp_at(row, st), "quote", None) if reg is not None else None  # noqa: E731
    gaps = reissued_form_gaps(rows, [(s.stage, s.state) for s in r.get("stages") or []], quote_at)
    for rid, gs in gaps.items():
        for g in gs:
            for i in g["issues"]:
                x = {"issue": i, "why": g["flag"]}
                if x not in out.setdefault(rid, []):
                    out[rid].append(x)
    return out


def issue_scope_args(r: dict) -> tuple[dict, dict]:
    """Session 14 (W4): (issues, units) for relationships.issue_reaches: the curated issues by id and the units by id
    (the evidence build's units and every unit an op made at the last stage)."""
    units = {u["unit_id"]: u for u in r.get("units") or []}
    for s in (r.get("stages") or [])[-1:]:
        for uid, u in s.state.items():
            units.setdefault(uid, {"unit_id": uid, "text": getattr(u, "text", "") or ""})
    return dict(r.get("curated_issues") or {}), units


def row_issues(r: dict) -> dict[str, list[str]]:
    """Session 13 (F4; audit R1-7): row id -> the issues that bear on the row, ONE set for A1 (the Issues cell,
    linked_issue_cells) and A2/A5 (signals.attach_pending): its own `issues`, then those the curated relationships that
    reach it carry and those of a reissued form's dropped field (row_issue_links). An issue an op's note names is context
    for the op, never a link to the op's targets."""
    links = row_issue_links(r)
    return {e["row"].id: signals.issue_ids_of(e["row"].issues, links.get(e["row"].id)) for e in r.get("evals") or []}


def issue_stages(r: dict) -> dict[str, str]:
    """Session 13 (F4; audit R1-9): issue id -> the stage from which it bears on its rows (signals.issue_since: its
    `since`, else the latest first-issue stage of the `units` it cites, else the first stage), for every curated issue."""
    order = list(r.get("order") or [s.stage for s in r.get("stages") or []])
    first: dict[str, str] = {}
    for s in r.get("stages") or []:
        for uid, u in s.state.items():
            if uid not in first and getattr(u, "status", "active") != "not_issued":
                first[uid] = s.stage
    return {iid: signals.issue_since(it, order, first.get) for iid, it in (r.get("curated_issues") or {}).items()}


def _link_words(x: dict) -> str:
    return f"via {x['via']} ({x['status']})" if x.get("via") else str(x.get("why") or "")


def linked_issue_cells(own: list[str], links: list[dict]) -> list[str]:
    """A1's Issues cell (session 13, audit R1-2): the row's own issues, then each issue linked only through `links`
    (row_issue_links) with why: 'I-X (via REL-A (confirmed); via REL-B (proposed))'. An issue the row lists itself is
    listed once, as it is."""
    out, by = list(own), {}
    for x in links or []:
        if x["issue"] not in own:
            by.setdefault(x["issue"], []).append(_link_words(x))
    return out + [f"{i} ({'; '.join(dict.fromkeys(w))})" for i, w in by.items()]


# ---------------------------------------------------------------------------------------------- value / interpretation / approval
# Session 14 (W4; the owner's part 4: "Separate unchanged table values from unresolved interpretation and approval
# status"): a row's VALUE can be unchanged while its INTERPRETATION is pending and no APPROVAL is given. row_states gives
# the three apart, at the validated stage, for A1's columns and the review cards:
#   value           what the row's words and cells did across the stages: 'unchanged since <stage>' (with the ops that
#                   re-read it, named, never as a confirmation), 'changed at <stage> by <ops>', 'new at <stage>', or
#                   'not in force at <stage>'; and the value as read (the quote)
#   interpretation  the issues that bear on the reading (row_issues, the set A1's Issues cell shows): those that are a
#                   person's decision not yet recorded (HUMAN DECISION PENDING), then the other open ones
#   approval        what a person has recorded: the image transcription (an approval of the transcription and the
#                   displayed translation only, never of the interpretation), the row's own review, and the review of
#                   every op on its units (amending ops and annotations), 'proposed (not reviewed)' until accepted
STATE_COLS = (("value_state", "Value at the validated stage (the value only: unchanged/changed/new; not a confirmation)", 36),
              ("interpretation_state", "Interpretation (open judgments on the reading; HUMAN DECISION PENDING where a "
                                       "person decides)", 36),
              ("approval_state", "Approval (what a person has recorded; an image transcription approval is not an "
                                 "approval of the interpretation)", 36))
TRANSCRIPTION_ONLY = ("image transcription approved by the owner (the transcription and its displayed translation only; "
                      "not an approval of the interpretation)")


def row_states(r: dict) -> dict[str, dict]:
    """Row id -> {value, interpretation, approval} at the validated stage (see above). Pure; nothing is decided."""
    val = r["validated"].stage
    order = list(r["order"])
    order = order[: order.index(val) + 1] if val in order else order
    by_row = row_issues(r)
    pend = r.get("pending_issues") or {}
    since = r.get("issue_stages") or issue_stages(r)
    decided = {i for i, it in (r.get("curated_issues") or {}).items()
               if human_owned.decision(r.get("decisions"), "issue", i, it) is not None}
    rv = r.get("reviews") or {}
    ann = {s: programme.answers_by_row(r, s) for s in order[1:]}
    out: dict[str, dict] = {}
    for e in r["evals"]:
        row, stg = e["row"], e["stages"]
        v = stg[val]
        it = r["register"].interp_at(row, val)
        quote = getattr(it, "quote", "") or ""
        first = next((s for s in order if stg[s]["active"]), None)
        changed, reread = [], []
        for i in range(1, len(order)):
            a, b = stg[order[i - 1]], stg[order[i]]
            new_ops = [h for h in b.get("ops") or [] if h not in (a.get("ops") or [])]
            if a["active"] and b["active"] and (a.get("text") != b.get("text") or a.get("cells") != b.get("cells")):
                changed.append(f"changed at {order[i]}" + (f" by {', '.join(new_ops)}" if new_ops else ""))
            elif a["active"] and b["active"]:
                # a unit it cites or depends on changed: the row's own words did not, but its value is not 'unchanged'
                dw = [w for w in signals.requirement_delta(a, b, ann[order[i]].get(row.id))["what"]
                      if w not in ("text", "cells", "status", "dates")]
                if dw:
                    changed.append(f"own words unchanged at {order[i]}, but what it depends on changed ({', '.join(dw)}; "
                                   "see A2)")
            for c in ann[order[i]].get(row.id) or []:
                reread.append(f"{c['op']} ({c.get('effect') or c.get('class') or 'annotation'}; {order[i]})")
        if not v["active"]:
            value = f"not in force at {val} ({v['status']})"
        elif changed:
            value = "; ".join(changed)
        elif first and first != order[0]:
            value = f"new at {first}"
        else:
            value = f"unchanged since {first or order[0]}"
        if v["active"] and reread:
            value += "; re-read by " + ", ".join(dict.fromkeys(reread)) + " (an annotation; not a confirmation)"
        if v["active"] and quote:
            value += f"; value as read: '{_short(quote, 120)}'"
        pos = lambda st: order.index(st) if st in order else 0  # noqa: E731
        ids = [i for i in by_row.get(row.id) or [] if pos(since.get(i, order[0])) <= pos(val) or since.get(i) not in order]
        pending = [i for i in ids if i in pend]
        waiting = [i for i in ids if i in (r.get("awaiting_issues") or {}) and i not in pend]
        other = [i for i in ids if i not in pend and i not in decided and i not in waiting]
        done = [i for i in ids if i in decided]
        owner = lambda i: str(((r.get("curated_issues") or {}).get(i) or {}).get("decision_owner")  # noqa: E731
                              or ((r.get("curated_issues") or {}).get(i) or {}).get("owner") or "")
        parts = []
        if pending:
            parts.append(f"{human_owned.HUMAN_DECISION_PENDING}: " + ", ".join(
                f"{i} ({owner(i)})" if owner(i) else i for i in pending))
        if waiting:
            parts.append(f"{signals.AWAITING_RULE}: " + ", ".join(waiting))
        if other:
            parts.append("open: " + ", ".join(other))
        if done:
            parts.append("decided (recorded): " + ", ".join(done))
        interp = "; ".join(parts) or "no open issue on the reading"
        appr = []
        if v.get("transcription") == "approved":
            appr.append(TRANSCRIPTION_ONLY)
        elif v.get("transcription") == "pending":
            appr.append("image transcription PENDING (not approved)")
        appr.append("row: " + review.label(rv[("row", row.id)]) if ("row", row.id) in rv else "row: not reviewed")
        ops = list(dict.fromkeys(list(v.get("ops") or []) + [c["op"] for s in order[1:]
                                                             for c in ann[s].get(row.id) or []]))
        appr += [f"{h}: {review.label(rv[('op', h)])}" for h in ops if ("op", h) in rv]
        if appr and appr[0] == TRANSCRIPTION_ONLY:
            appr = appr[1:] + appr[:1]                 # the row's own review first
        out[row.id] = {"value": value, "interpretation": interp, "approval": "; ".join(appr)}
    return out


def table_title(unit: dict | None) -> str:
    """The printed title of the table a table-row unit was read from ('' when none): the reading's `table_title`, its
    whitespace collapsed (session 13, F2; audit R2-8: 'at the Point of Discharge' is on the Table 2-4 image)."""
    if not unit or unit.get("kind") != "table_row":
        return ""
    return " ".join(str((unit.get("context") or {}).get("table_title") or "").split())


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
    # session 11 audit (A1-1): what each addendum did to the row without (or besides) a change of status
    cols += [(f"change:{s}", f"Change at {s} (reading re-made with its note, dates moved, the ops; not a status)", 40)
             for s in order[1:]]
    cols += [(f"source:{s}", f"Source after {s} (latest reference for the quoted words)", 26) for s in order]
    cols += [("consequence", "Stated consequence (quoted)", 40), ("consequence_source", "Consequence source", 18),
             ("dates", "Dates (planning reading; all readings in Dates sheet)", 30), ("confidence", "Confidence", 30),
             ("note", "Interpretation note (the reading at the validated state)", 40),
             *STATE_COLS,                              # session 14 (W4): value / interpretation / approval apart
             ("transcription", "Image reading status", 14), ("interpretation", "Interpretation review", 14),
             ("ops_review", "Amendment ops review", 14), ("chain", "Evidence chain (original -> ops)", 50),
             ("issues", "Issues", 20)]
    if r.get("relationships"):                   # session 10; a pack without a relationships file keeps its A1 as it was
        cols.append(("relationships", "Relationships (curated links, their status; reached at the validated stage; "
                                      "documents not supplied)", 50))
    rows = []
    units_by_id = {u["unit_id"]: u for u in r.get("units") or []}
    summary_stale = summary_currency(r)
    row_rel = relationship_lines(r)
    links = row_issue_links(r)                    # session 13 (audit R1-2, R1-6)
    gaps = reissued_form_gaps([e["row"] for e in r["evals"]], [(s.stage, s.state) for s in r["stages"]],
                              lambda row, st: getattr(r["register"].interp_at(row, st), "quote", None))
    computed_by = {s: derived.computed_deadlines(r, s) for s in order[1:]}    # session 12 (W3b): calc deadlines
    computed = computed_by.get(val) or []
    states = row_states(r)                        # session 14 (W4)
    for e in r["evals"]:
        row, stg = e["row"], e["stages"]
        v = stg[val]
        last = v if v["active"] else next((stg[s] for s in reversed(order) if stg[s]["active"]), v)
        it = r["register"].interp_at(row, val) or (row.interpretations[-1] if row.interpretations else None)
        cons = it.consequence if it else "none_stated"
        src = last.get("source") or {}
        ud = last.get("units_detail") or []
        multi = len(ud) > 1
        # session 12 (F1; audit A1-5): one rule for 'Text as issued': the text as the issuing document printed it; a unit
        # first issued by an addendum is labelled with its reference and the addendum (single- and multi-unit rows alike)
        orig = ("\n".join(f"[{d['ref']}" + (f"; issued by {d['issued_by']}" if d["issued_by"] else "") + f"] "
                          + (d["original_text"] or "(not in the volumes as issued)") for d in ud)
                if multi else (f"[{ud[0]['ref']}; issued by {ud[0]['issued_by']}] " if ud and ud[0]["issued_by"] else "")
                + (last.get("original_text", "") or (ud[0]["original_text"] if ud else "")))
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
        for i, s in enumerate(order):
            ev = stg[s]
            rec[f"status:{s}"] = ev["status"] + (" — STALE" if ev["stale"] else "")
            if i:
                rec[f"change:{s}"] = stage_change(stg[order[i - 1]], ev, s)
                sw = [f for f in ev.get("flags") or [] if derived.is_switch_flag(f)]      # session 12 (W3b)
                if sw:
                    rec[f"change:{s}"] = "; ".join([x for x in [rec[f"change:{s}"]] if x] + sw)
                fg = [f"{g['evidence']}: {g['flag']}" + (f" ({', '.join(g['issues'])})" if g["issues"] else "")
                      for g in gaps.get(row.id, []) if g["stage"] == s]     # session 13 (audit R1-6)
                if fg:
                    rec[f"change:{s}"] = "; ".join([x for x in [rec[f"change:{s}"]] if x] + fg)
            rec[f"source:{s}"] = ("" if ev["status"] == "NOT ISSUED" or ev["status"].startswith("NOT IN FORCE")
                                  else (ev.get("source") or {}).get("latest", ""))
        rec["consequence"] = ((f"{CLASS_WORDS[cons.cls]}: \"{cons.quote}\""      # gloss label from the approval state
                               + (f" ({consequence_gloss(r, row, cons)}: '{cons.gloss}')" if cons.gloss else ""))
                              if isinstance(cons, Consequence) else "none stated in the documents")
        csrc = last.get("consequence_source") or {}
        rec["consequence_source"] = (csrc.get("latest") or cons.unit) if isinstance(cons, Consequence) else ""
        rec["dates"] = [f"{d['rule_id']}: {d['planning']['value']} ({d['planning']['key']})"
                        + derived.date_derivation(computed, d) for d in v["dates"]] \
            if v["active"] else []                    # session 11 audit (A1-9): no dates where the row is not in force
        rec["confidence"] = f"{row.confidence}: {confidence_reason(r, row)}"
        rec["note"] = (it.note or "") if it else ""
        titles = list(dict.fromkeys(t for t in (table_title(units_by_id.get(u)) for u in row.units) if t))
        if titles:                   # session 13 (F2; audit R2-8): the printed title of the table the row was read from
            rec["note"] = (rec["note"] + " " if rec["note"] else "") + "; ".join(
                f"Printed table title: '{t}'." for t in titles if t not in rec["note"])
        rec["value_state"] = states[row.id]["value"]                    # session 14 (W4)
        rec["interpretation_state"] = states[row.id]["interpretation"]
        rec["approval_state"] = states[row.id]["approval"]
        rec["transcription"] = v["transcription"]
        rec["interpretation"] = review.label(r["reviews"][("row", row.id)])
        rec["ops_review"] = "; ".join(f"{h}: {r['reviews'][('op', h)]['status']}" for h in v["ops"]
                                      if ("op", h) in r["reviews"]) or "n/a"
        rec["chain"] = stg[order[-1]]["chain"]                 # every unit and every op, through the last stage
        rec["issues"] = (linked_issue_cells(row.issues, links.get(row.id))      # session 13 (audit R1-2, R1-6)
                         + [f"SUMMARY OUT OF DATE: '{x['figure']}'" for x in summary_stale if x["row"] == row.id])
        if r.get("relationships"):
            rec["relationships"] = row_rel.get(row.id, [])
        rows.append(rec)
    dates_rows = []
    for e in r["evals"]:
        for s in order:
            if not e["stages"][s]["active"]:          # session 11 audit (A1-9): not issued, not in force, deleted
                continue
            for d in e["stages"][s]["dates"]:
                dates_rows.append({"row": e["row"].id, "stage": s, "rule": d["rule_id"], "text": d["text"],
                                   "anchor": f"{d['anchor']} = {d['anchor_value']}" if d["anchor"] else "",
                                   "readings": [f"{i['key']}: {i['value']} ({i['basis']})" for i in d["interpretations"]],
                                   "planning": f"{d['planning']['value']} ({d['planning']['key']}, policy {d['planning']['policy']})"
                                   + derived.date_derivation(computed_by.get(s) or [], d),
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
    notes = config_comments(r["root"] / r["cfg"].get("assumptions", "config/assumptions.yaml"), "submission")
    assumption_rows += [{"key": f"submission.{k}", "value": str(v), **_submission_basis(notes.get(k, ""))}
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
    approved = {}                    # session 12 (R-2): region -> whether the approved reading displays translations
    for u in r["units"]:
        rd = u.get("reading") or {}
        if rd.get("status") == "approved" and rd.get("region") and u["kind"] != "region":
            approved[rd["region"]] = approved.get(rd["region"], False) or bool(u.get("translation"))
    used = sorted({x["row"].assessment for x in r["evals"]})
    evid = {k: {"name": v.name, "issuer": v.issuer, "envelope": v.envelope, "per": v.per, "source": v.source}
            for k, v in sorted((r.get("evidence_items") or {}).items())}
    return {
        "title": "A1 Obligations and compliance register — WORKING DRAFT",
        "notice": (f"WORKING DRAFT, full register: {len(rows)} rows (review status: "
                   + ", ".join(f"{k} {n}" for k, n in sorted(rc.items())) + "; amendment ops: "
                   + ", ".join(f"{k} {n}" for k, n in sorted(oc.items())) + "). Rows and ops count as accepted only with a "
                   "named person's decision bound to their current content. Image readings pending the owner's review: "
                   + (", ".join(pending) or "none")
                   + ("; approved by the owner: " + ", ".join(f"{g} ({approval_covers(tr).replace('the ', '')})"
                                                             for g, tr in sorted(approved.items()))
                      + "; their interpretations stay proposed" if approved else "")
                   + f". Validated state: {val}"
                   + (f"; working state {working} is PARTIAL" if working else "") + ". Pass/fail or scored: "
                   + "; ".join(f"{k} = {ASSESSMENT_WORDS.get(k, k)}" for k in used)
                   + ". 'Change at <stage>' says what that addendum did to the row besides its status (the reading "
                   "re-made, with its note; dates moved; the ops and annotations, with provision and page); a row "
                   "whose unit an op reissued or amended elsewhere with the row's own words unchanged reads 'ACTIVE "
                   "(reissued by <op>, unchanged)'. In 'Text as issued', a segment marked '[<document> <clause> "
                   "p<n>; issued by ADD-0x]' is that addendum's own text, not text of the volumes as issued. "
                   "Evidence codes are defined in the Evidence sheet."
                   + (" " + relationships.STATUS_LEGEND if r.get("relationships") else "")),
        "stages": order, "validated_stage": val, "working_stage": working, "evidence_items": evid,
        "columns": [{"key": k, "header": h, "width": w} for k, h, w in cols], "rows": rows,
        "sheets": {
            "Dates": sheet(dates_rows, [("row", 16), ("stage", 9), ("rule", 22), ("text", 40), ("anchor", 22),
                                        ("readings", 60), ("planning", 34), ("readings_differ", 10)]),
            "Issues": sheet([{**{k: i[k] for k in ("id", "text", "owner", "source")},
                              "rows": list(i["rows"]) + list(i.get("rows_linked") or []),   # session 13 (R1-2)
                              "clarification": [q["id"] for q in (r.get("clarifications") or {}).get("clarifications", [])
                                                if i["id"] in (q.get("linked_issues") or [])]} for i in issues],
                            [("id", 26), ("text", 90), ("owner", 16), ("source", 22), ("rows", 30),
                             ("clarification", 24)]),
            "Stages": sheet(stages_rows, [("stage", 9), ("addendum", 9), ("issued", 11), ("status", 10), ("ops", 6),
                                          ("invalid_ops", 9), ("ops_review", 24), ("provisions", 10),
                                          ("unresolved", 10), ("validated", 9)]),
            "Assumptions": sheet(assumption_rows, [("key", 30), ("value", 14), ("basis", 90), ("owner", 16)]),
            "Evidence": sheet([{"code": k, **v} for k, v in evid.items()],         # session 11 audit (A1-7)
                              [("code", 24), ("name", 70), ("issuer", 36), ("envelope", 10), ("per", 14), ("source", 40)]),
            "Date coverage": sheet([{k: x[k] for k in ("unit", "phrase", "treatment", "by", "sentence")}
                                    for x in r.get("date_coverage", [])],
                                   [("unit", 22), ("phrase", 26), ("treatment", 14), ("by", 60), ("sentence", 80)]),
            **({"Relationships": dict(notice=relationships.STATUS_LEGEND, **sheet(relationship_sheet(r), [
                ("id", 30), ("kind", 16), ("status", 11), ("class", 20), ("from", 30), ("to", 34), ("evidence", 70),
                ("basis", 60), ("note", 50), ("document", 30), ("blocks", 60), ("issues", 20), ("origin", 12),
                ("review", 10), ("reached", 30)]))} if r.get("relationships") else {}),
        },
    }


ASSESSMENT_WORDS = {   # session 11 audit (A1-10): the A1 'Pass/fail or scored' values, defined in the notice
    "pass_fail": "a gate checked as met or not met at bid stage (a stated rejection, disqualification, non-responsiveness "
                 "or exclusion, or a document the VOL-I 11.1 checks require)",
    "scored": "marked under the evaluation criteria (Table 1-1 or the financial evaluation); a shortfall loses marks",
    "procedural": "a step of the tender process with no stated effect on whether the Proposal stays in",
    "contractual_post_award": "an obligation under the Project Agreement after award; not assessed at bid stage",
    "informational": "context only; nothing to do"}


def config_comments(path: Path, section: str) -> dict[str, str]:
    """{key: its comment} for the direct keys of a top-level `section` of a YAML config file: the comment on the key's
    line and the comment-only lines indented under it (session 11 audit, A1-4: the config's own words for its basis)."""
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError:
        return {}
    out: dict[str, str] = {}
    inside, key = False, None
    for ln in lines:
        if re.match(r"^\S", ln):
            inside, key = ln.split("#")[0].strip() == f"{section}:", None
            continue
        if not inside:
            continue
        m = re.match(r"^  (\w+):[^#]*(?:#\s*(.*))?$", ln)
        if m:
            key = m.group(1)
            out[key] = (m.group(2) or "").strip()
        elif key and re.match(r"^\s+#", ln):
            out[key] = (out[key] + " " + ln.strip().lstrip("#").strip()).strip()
    return out


def _submission_basis(comment: str) -> dict:
    """Basis and owner of a `submission` value: a key the config marks as an ASSUMPTION carries the config's own words
    (never 'stated in the pack'); any other is stated in VOL-I 6.5."""
    if "ASSUMPTION" in comment.upper():
        m = re.search(r"\bowner ([A-Z][\w ]+?)\s*(?:;|$)", comment)
        return {"basis": comment if comment.upper().startswith("PROVISIONAL ASSUMPTION")
                else f"PROVISIONAL ASSUMPTION (config/assumptions.yaml): {comment}",
                "owner": m.group(1) if m else "Bid manager"}
    return {"basis": "stated in VOL-I 6.5", "owner": "Bid manager"}


def stage_change(a: dict, b: dict, stage: str) -> str:
    """Session 11 audit (A1-1): what one addendum did to a row besides its status, for A1's 'Change at <stage>': the
    reading re-made at the stage with its note, the dates that moved, a status change, and the ops and annotations of
    the stage in the row's evidence chain (provision and page). Empty when the stage did nothing to the row."""
    parts = []
    if a["status"] != b["status"]:
        parts.append(f"status {a['status']} -> {b['status']}")
    if b["interpretation_stage"] == stage and a["interpretation"] != b["interpretation"]:
        note = (b["interpretation"] or {}).get("note")
        parts.append(f"reading re-made at {stage}" + (f": {note}" if note else ""))
    if a["active"] and b["active"]:
        pa = {d["rule_id"]: d["planning"]["value"] for d in a["dates"]}
        moved = [f"{d['rule_id']} {pa[d['rule_id']]} -> {d['planning']['value']}" for d in b["dates"]
                 if d["rule_id"] in pa and pa[d["rule_id"]] != d["planning"]["value"]]
        if moved:
            parts.append("dates moved: " + "; ".join(moved))
    ops = [ln for ln in b.get("chain") or [] if re.match(r"\S+ \[" + re.escape(stage) + ";", ln)]
    if parts and ops:
        parts.append("by " + "; ".join(ops))
    return ". ".join(p.rstrip(". ") for p in parts)


def relationship_lines(r: dict) -> dict[str, list[str]]:
    """Per row id, the A1 'Relationships' lines (session 10): each curated link naming the row (status, kind, the other
    end), each document not supplied that blocks a conclusion of the row (what cannot be established), and what reached
    the row at the validated stage (class, source, path). Rows without any have none."""
    ents = r.get("relationships") or []
    out: dict[str, list[str]] = {}
    rows = {e["row"].id for e in r["evals"]}
    for e in ents:
        if not isinstance(e, dict) or not e.get("id"):
            continue
        tag = f"{e['id']} [{e.get('status')} {e.get('kind')}]"
        for t in relationships.ends(e, "to"):
            if t not in rows:
                continue
            if e.get("kind") == "missing_document":
                out.setdefault(t, []).append(f"NOT SUPPLIED: {e.get('document')} ({e['id']}, link {e.get('status')}): "
                                             f"cannot be established: {e.get('blocks')}")
            else:
                out.setdefault(t, []).append(f"<- {tag} from {', '.join(relationships.ends(e, 'from'))}")
        for f in relationships.ends(e, "from"):
            if f in rows and e.get("kind") != "missing_document":
                out.setdefault(f, []).append(f"-> {tag} to {', '.join(relationships.ends(e, 'to'))}")
    # session 14 (W4): an issue a relationship names that does not reach the row (outside its scope) is said, with why
    for t, xs in relationships.out_of_scope_links(ents, rows, *issue_scope_args(r)).items():
        out.setdefault(t, []).extend(f"issue {x['why']}" for x in xs)
    val = r["validated"].stage
    for rec in ((r.get("relationship_impact") or {}).get(val) or {}).get("records", []):
        if rec["target"] in rows and rec["kind"] != "missing_document":
            out.setdefault(rec["target"], []).append(
                f"REACHED at {val} ({rec['class']}): from {', '.join(rec['sources'])} via {' > '.join(rec['path'])}")
    return out


def relationship_sheet(r: dict) -> list[dict]:
    """A1 'Relationships' sheet: every curated entry with its evidence or basis, and the stages at which it reached
    something (relationships.impact)."""
    used: dict[str, list[str]] = {}
    for st, d in (r.get("relationship_impact") or {}).items():
        for rec in d.get("records", []):
            for eid in rec["path"]:
                if st not in used.setdefault(eid, []):
                    used[eid].append(st)
    out = []
    for e in r.get("relationships") or []:
        if not isinstance(e, dict):
            continue
        out.append({"id": e.get("id"), "kind": e.get("kind"), "status": e.get("status"),
                    "class": relationships.CLASSES.get(e.get("status"), ""),
                    "from": relationships.ends(e, "from"), "to": relationships.ends(e, "to"),
                    "evidence": relationships.evidence_text(e), "basis": e.get("basis") or "",
                    "note": "; ".join(x for x in (e.get("note") or "", relationships.context_text(e)) if x),  # s13 R1-4
                    "document": e.get("document") or "", "blocks": e.get("blocks") or "", "issues": e.get("issues") or [],
                    "origin": e.get("origin") or "", "review": e.get("review") or "proposed",
                    "reached": [s for s in r["order"] if s in used.get(e.get("id"), [])]})
    return out


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


REREAD = "to be re-read against the new text"



def changed_units_for_reread(ops, switched: dict | None = None) -> dict:
    """{unit: the applied op result that changed it}: what an earlier answer may have relied on that this addendum
    changes (answers_to_review). Replaced, set, deleted or renumbered units; appended words and inserted rows; units an
    annotation (not a confirming or interpreting one) targets; a clause whose condition an op switched (W3b); and,
    session 12 (blind-06 follow-up 11), an INSERTED unit together with its anchor and new group: a new 31.1(d) event
    changes what an answer on 29.x relied on when a relationship joins them, which the trace from these units finds."""
    from .signals import CONFIRMING_EFFECTS
    changed, extra = {}, {}
    for x in ops:
        if not x.applied:
            continue
        o = x.op
        if o.type in ("replace_text", "set_value", "set_status", "replace_unit"):
            changed[o.target] = x
        if o.effect == "renumbers":                    # an answer citing a renumbered clause reads differently now
            for k in o.renumber:
                changed[k] = x
        if o.type in ("append_text", "insert_row"):                     # session 12
            extra.setdefault(o.target, x)
        if o.type in ("relocate_unit", "adjust_value"):                 # session 14 (W3): moved or recomputed
            for k in [o.target, *(getattr(x, "changed", None) or [])]:
                changed.setdefault(k, x)
        if o.type == "insert_table" and o.new_group:                    # session 14 (W3): a table made part of a volume
            extra.setdefault(o.new_group, x)
        if o.type == "insert_unit":                                      # session 12 (follow-up 11)
            for k in [*(getattr(x, "changed", None) or []), o.anchor, o.new_group]:
                if k:
                    extra.setdefault(k, x)
        if o.type == "annotate" and o.effect not in CONFIRMING_EFFECTS + ("renumbers",):
            for k in o.targets:
                extra.setdefault(k, x)
    for k, x in (switched or {}).items():            # session 12 (W3b): a clause whose condition an op switched
        extra.setdefault(k, x)
    return {**extra, **changed}                      # the session-08 ops keep their precedence over the session-12 ones


def answers_to_review(r: dict, s: StageResult) -> list[dict]:
    """Clarification answers that cite a unit this addendum changed, or quote a figure it replaced. They are
    listed for a person to review; an answer is never marked revoked automatically. Non-binding minutes are
    not answers and are listed separately.
    Session 12 (W3a; blind-05 S5/IE3, follow-up 8): an answer also relies on the units its own annotation op targets
    (ADD-01/Q1 annotates VOL-II 3.1), and on what those govern through a curated relationship (relationships.trace from
    the changed units: a path that reaches a unit or a row the answer relies on); 'changed' also counts appended words,
    an inserted table row and an annotation that adds an obligation (never a confirming or interpreting one:
    signals.CONFIRMING_EFFECTS). Each answer carries `reread`: 'to be re-read against the new text of <units> (<ops>)'.
    Session 12 (F1; audit A2-4): a changed table or form row also stands for its table in that trace, for an answer whose
    own words name the table (ADD-01 Q1 'Any process capable of meeting Table 2-4', after ADD-02 5.1 sets the TN row).
    Nothing decides the outcome: the status stays REVIEW (not automatically revoked)."""
    changed = changed_units_for_reread(s.ops, derived.switched_units(r, s))
    reg = r["register"]
    relied_by_op: dict[str, list[tuple[str, str]]] = {}          # answer unit -> [(target, its annotation op)]
    for h, prov in reg.op_provision.items():
        o = reg._op_by_id(h)
        if o is not None and o.op.type == "annotate" and reg.order.index(reg.op_stage.get(h, BASE)) <= \
                reg.order.index(s.stage):
            relied_by_op.setdefault(prov, []).extend((t, h) for t in o.op.targets)
    # what the changed units reach through the curated relationships (a unit, or a row and the units it cites)
    rows_units = {e["row"].id: set(e["row"].units) for e in r["evals"]}
    via: dict[str, list[tuple[str, list[str], str]]] = {}        # reached unit -> [(changed source, path, op id)]
    # session 12 (F1; audit A2-4): a changed table or form row stands for its table too, as in
    # relationships.impact_between (a relationship from VOL-II:T2-4 is reached when ADD-02 5.1 sets its TN row), for an
    # answer whose own words name that table ('Any process capable of meeting Table 2-4'); an answer that only relies on
    # a clause the table's relationships reach, without naming the table, is not listed through the table
    parent_of, parent_name = {}, {}
    for t in changed:
        p = getattr(s.state.get(t), "parent", None)
        pu = s.state.get(p) if p else None
        if p and p not in changed and pu is not None and pu.kind in ("table", "form"):
            parent_of.setdefault(p, t)
            m = re.match(r"((?:Table|Form)\s+[\w.-]+)", pu.label or "")
            if m:
                parent_name[p] = re.compile(r"\b" + re.escape(m.group(1)).replace(r"\ ", r"\s+") + r"(?![\w-])", re.I)
    if r.get("relationships") and changed:
        for rec in relationships.trace(r["relationships"], set(changed) | set(parent_of)):
            if rec.get("kind") == "missing_document":
                continue
            src = next((x for x in rec.get("sources") or [] if x in changed), None)
            named = None
            if src is None:
                named = next((x for x in rec.get("sources") or [] if x in parent_of), None)
                src = parent_of.get(named) if named else None
            if src is None:
                continue
            for u in ({rec["target"]} | rows_units.get(rec["target"], set())):
                via.setdefault(u, []).append((src, list(rec.get("path") or []), changed[src].op.id, named))
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
        under = lambda t, c: t == c or t.startswith(c + "/") or t.startswith(c + "#")  # noqa: E731
        hit = [(t, x) for t, x in changed.items() if any(under(t, c) for c in cited)]
        mine = relied_by_op.get(k, []) if u.issued_by != s.stage else []
        tgt = [(t, h, x) for t, x in changed.items() for (c, h) in mine
               if under(t, c) and not any(t == y for y, _ in hit)]
        num = [(lab, x) for (lab, rx), x in figures.items() if re.search(rx, text, re.I)]
        relied = set(cited) | {c for c, _ in mine}
        rel = [] if hit or tgt or u.issued_by == s.stage else \
            [(c, src, path, oid) for c in sorted(relied) for (src, path, oid, named) in via.get(c, [])
             if named is None or (named in parent_name and parent_name[named].search(text))][:3]
        if hit or num or tgt or rel:
            why = [f"cites {t}, changed by {x.op.id}" for t, x in hit] + \
                  [f"its annotation {h} targets {t}, changed by {x.op.id}" for t, h, x in tgt] + \
                  [f"relies on {c}, which {src} (changed by {oid}) governs through {' > '.join(path)}"
                   for c, src, path, oid in rel] + \
                  [f"quotes '{lab}', a figure {x.op.id} replaced" for lab, x in num if not any(x is y for _, y in hit)]
            units = list(dict.fromkeys([t for t, _ in hit] + [t for t, _, _ in tgt] + [src for _, src, _, _ in rel]
                                       + [x.op.target for _, x in num if x.op.target]))
            ops = list(dict.fromkeys([x.op.id for _, x in hit] + [x.op.id for _, _, x in tgt] + [o for *_, o in rel]
                                     + [x.op.id for _, x in num]))
            out.append({"answer": k, "issued_by": u.issued_by, "text": _short(u.text, 220), "why": "; ".join(why),
                        "status": "REVIEW (not automatically revoked)",
                        "reread": f"{REREAD} of {', '.join(units)} ({', '.join(ops)}); a person decides whether the "
                                  "answer still holds"})
    return out


def reversed_ops(r: dict, s: StageResult, prev: StageResult) -> list[dict]:
    """Session 11 audit (A2-10): ops of an earlier stage that an op of this stage reverses or revokes, listed with the
    earlier answers to review: a set_status that reinstates, deletes or revokes a unit an earlier op changed (ADD-02 9.1
    reinstates VOL-I 8.6, which ADD-01/4.1 deleted), or that revokes the provision of an earlier op (ADD-02 9.2 revokes
    ADD-01 4.2, the provision of ADD-01/4.2); and a replace_unit of a unit an earlier op changed. Never revoked
    automatically. Session 12 (F1; audit A2-4): where a set_status op applies the addendum's own words (reinstated,
    deleted, revoked), the line says so plainly ('REVERSED by ADD-02 9.1', 'REVOKED by ADD-02 9.2', quoting the
    provision) instead of 'a person decides': the pack decided it; the op stays proposed. A replacement keeps REVIEW."""
    reg = r["register"]
    out = []
    for x in s.ops:
        o = x.op
        if not x.applied or o.type not in ("set_status", "replace_unit") or not o.target:
            continue
        verb = {"reinstated": "reversed (reinstated)", "deleted": "reversed (deleted)", "revoked": "revoked"}.get(
            o.status or "", "superseded (replaced)")
        # session 12 (F1; audit A2-4): a set_status op applies the addendum's own words ('is reinstated', 'ceases to have
        # effect'): the pack itself reverses or revokes the earlier op, so the line says so plainly; 'a person decides'
        # stays only where the pack is silent (a replacement, whose new text a person compares)
        express = o.type == "set_status" and o.status in ("reinstated", "deleted", "revoked")
        pv = s.state.get(o.provision)
        tgt = prev.state.get(o.target)
        hits = [(h, f"{o.target} was changed by {h}") for h in (tgt.history if tgt is not None else [])
                if reg.op_stage.get(h) and reg.order.index(reg.op_stage[h]) < reg.order.index(s.stage)]
        hits += [(h, f"{o.target} is the provision of {h}") for h, p in reg.op_provision.items()
                 if p == o.target and reg.op_stage.get(h) and reg.order.index(reg.op_stage[h]) < reg.order.index(s.stage)]
        for h, how in hits:
            if any(y["answer"] == h for y in out):
                continue
            pu = prev.state.get(reg.op_provision.get(h))
            if express:
                status = (f"{'REVOKED' if o.status == 'revoked' else 'REVERSED'} by {_doc_clause(o.provision)} "
                          f"(op {o.id}, proposed)")
                reread = (f"the addendum says so in its own words ({_doc_clause(o.provision)}: "
                          f"'{_short(pv.text if pv else '', 160)}'); no longer in force as written")
            else:
                status = "REVIEW (not automatically revoked)"
                reread = f"{REREAD} of {o.target} ({o.id}); a person decides whether it still holds"
            out.append({"answer": h, "issued_by": reg.op_stage[h], "text": _short(pu.text if pu else "", 220),
                        "why": f"{verb} by {o.id} ({o.provision}): {how}", "status": status, "reread": reread})
    return out


def _date_readings(d: dict) -> str:
    """'ATTENDANCE-NOTICE 2026-10-14 (2026-10-15 if the ADD-01 issue day is excluded)': the planning value and, when the
    counting convention is not stated and the readings differ, every other reading in the words A5 uses
    (schedule.other_readings), never chosen (config/formulas.yaml). Session 12 (F1; audit A2-5)."""
    from .schedule import other_readings
    alt = other_readings({"planning": d.get("planning"), "readings": d.get("interpretations") or [],
                          "readings_differ": d.get("readings_differ"), "anchor": d.get("anchor")})
    return (f"{d['rule_id']} {d['planning']['value']}"
            + (" (" + "; ".join(f"{x['value']} {x['words']}" for x in alt) + ")" if alt else ""))


def _doc_clause(uid: str) -> str:
    """'ADD-02:9.1' -> 'ADD-02 9.1'."""
    return str(uid or "").replace(":", " ", 1)


def _word_diff(old: str, new: str) -> str:
    """The words that differ between two texts: 'a' -> 'b'; + 'added'; - 'removed' (A2-1)."""
    import difflib
    a, b = (old or "").split(), (new or "").split()
    groups: list[list[int]] = []                  # [i1, i2, j1, j2]: changes up to two equal words apart are one phrase
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if groups and i1 - groups[-1][1] <= 2 and j1 - groups[-1][3] <= 2:
            groups[-1][1], groups[-1][3] = i2, j2
        else:
            groups.append([i1, i2, j1, j2])
    out = []
    for i1, i2, j1, j2 in groups:
        o, n = " ".join(a[i1:i2]), " ".join(b[j1:j2])
        out.append(f"'{o}' -> '{n}'" if o and n else f"+ '{n}'" if n else f"- '{o}'")
    return "; ".join(out)


def op_change(x, prev: StageResult, s: StageResult, note_limit: int | None = None) -> str:
    """What an op does, with the words the addendum adds or removes in full (session 11 audit, A2-1), for every op
    type: replace_text 'old' -> 'new'; append_text + 'new'; set_status with the words deleted, revoked or reinstated
    (a reinstatement in an amended form also gives the words that differ); insert_unit with the inserted text.
    Session 13 (audit R1-5): an annotation's note is written in full (a2_changes.json/.csv); only the markdown table
    passes `note_limit`, and a note cut there ends with a pointer to the csv."""
    o = x.op
    from .amend import describe_op                  # session 14 (W3): relocate_unit, insert_table, adjust_value, disapplies
    if (said := describe_op(x)) is not None:
        return said
    if o.type == "replace_text":
        return f"'{o.old}' -> '{o.new}'" if (o.new or "").strip() else f"- '{o.old}'"
    if o.type == "append_text":
        return f"+ '{o.new}'"
    if o.type == "set_value":
        return f"{o.column}: {x.details.get('old_value')} -> {o.new}" + (" (old value from an image reading PENDING review)"
                                                                         if x.details.get("reading_status") == "pending" else "")
    if o.type == "set_status":
        before = x.details.get("before") or (prev.state[o.target].text if o.target in prev.state else "")
        if o.status == "reinstated":
            diff = _word_diff(before, o.new_text or "")
            return f"REINSTATED: '{o.new_text}'" + (f" (as it stood before: {diff})" if diff and before else "")
        return o.status.upper() + (f": - '{before}'" if before else "")
    if o.type == "replace_unit":
        return f"replaced by {o.replacement} ({len(x.details.get('content', []))} units)"
    if o.type == "insert_unit":
        new = f"{o.anchor}+{s.stage}" if o.anchor else None
        text = s.state[new].text if new in s.state else (o.new_text or "")
        return (f"inserted {o.new_group or ''} {('after ' + o.anchor) if o.anchor else ''}".strip()
                + (f": '{text}'" if text else ""))
    if o.type == "insert_row":                      # session 09: a table row described in prose
        return (f"row {x.details.get('inserted') or '(not inserted)'} after {x.details.get('after') or o.after}: "
                + "; ".join(f"{k}: {v}" for k, v in (o.cells or {}).items()))
    ac = x.details.get("answer_class") or {}
    return (f"{o.effect}" + (", with open question" if o.issue else "")
            + (f"; mentions of '{o.subject}': {x.details.get('mentions')}" if o.subject else "")
            + (f" — {_note_cut(o.note, note_limit)}" if o.note else "")
            + (f" [answer read against {', '.join(ac.get('restates') or []) or 'its targets'}: {ac['class']}; "
               + "; ".join(f"'{y['text']}' {y['kind']}" for y in ac.get("sentences") or []) + "]" if ac else ""))


FULL_CHANGE_POINTER = "(full text in a2_changes.csv)"


def _note_cut(note: str, limit: int | None) -> str:
    """The note in full (one line), or cut at `limit` characters with the pointer to the full text."""
    t = " ".join(str(note or "").split())
    return t if limit is None or len(t) <= limit else f"{_short(t, limit)} {FULL_CHANGE_POINTER}"


def op_issue_ids(r: dict, o) -> list[str]:
    """The issue and clarification ids an op's open question is linked to (A2-4): ids named in its `issue`, curated
    issues that fold the op's own issue (I-OP-<op>), and clarifications citing the op's provision or those issues."""
    ids = re.findall(r"\b(?:I|CQ)-[A-Z0-9][A-Z0-9-]*[A-Z0-9]\b", o.issue or "")
    ids += [k for k, v in (r.get("curated_issues") or {}).items() if f"I-OP-{o.id}" in (v.get("folds") or [])]
    ids += [q["id"] for q in (r.get("clarifications") or {}).get("clarifications", [])
            if o.provision in (q.get("units") or []) or set(q.get("linked_issues") or []) & set(ids)]
    return sorted(dict.fromkeys(ids), key=lambda i: (not i.startswith("I-"), i))


def _held(r: dict, x) -> str:
    """Why a valid op is not applied (session 11): a conditional op is held until a person records its trigger
    (partial.conditional_label: CONDITIONAL, the decision date, both states); any other is withheld by a rejection."""
    if getattr(x, "conditional_pending", False):
        from .partial import conditional_label
        return conditional_label(r, x).replace("|", "/")
    return "WITHHELD (rejected by a person)"


def a2(r: dict) -> dict:
    val = r["validated"].stage
    stages = r["stages"]
    md = ["# A2 Addendum reconciliation — WORKING DRAFT", "",
          f"**DRAFT.** Ops are PROPOSED (not reviewed by a person). Validated state: **{val}**"
          + (f"; working state **{r['working'].stage}** is PARTIAL and does not replace it." if r["working"] else "."),
          "Every provision of every addendum is accounted for below: by an op, as content of an op, as no effect "
          "(with the reason), or as UNRESOLVED (a person must decide it). An op that leaves a question open says so in "
          "its Issue column (OPEN QUESTION, with the issue and clarification ids; an answer that confirms reads "
          "'confirms, with open question'): its effect is applied, the question stays for a person.", ""]
    changes, provs, moved, answers, summary_rows, rel_rows = [], [], [], [], [], []
    for i, s in enumerate(stages[1:], 1):
        prev = stages[i - 1]
        md += [f"## {s.stage} (issued {s.issued}) — {s.status}", "",
               f"Op file: {'drafted by tenderpack.draft for this build (out/drafted/)' if s.stage in r['drafted'] else 'curation/amendments/' + s.stage + '.yaml'}. "
               f"Prepared by: {s.prepared_by}", ""]
        counts = {}
        for c in s.coverage:
            counts[c["disposition"]] = counts.get(c["disposition"], 0) + 1
        md += [f"Provisions: {len(s.coverage)} — " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())), ""]
        md += ["### What it changed, added and deleted", "",
               "| Op | Type | Target | Change | Provision | Valid | Review | Issue |", "|---|---|---|---|---|---|---|---|"]
        op_missing = []                               # session 11 audit (A2-5): documents an op says are not supplied
        for x in s.ops:
            o = x.op
            tgt = o.target or o.new_group or ", ".join(o.targets)
            ch = op_change(x, prev, s)                 # session 11 audit (A2-1): the words in full, every op type
            ch_md = op_change(x, prev, s, note_limit=90)   # session 13 (audit R1-5): only the markdown table is cut
            ids = op_issue_ids(r, o) if o.issue else []
            iss = f"OPEN QUESTION ({'; '.join(ids) or 'no id'}): {o.issue}" if o.issue else ""
            if o.issue and any(w in o.issue for w in MISSING_DOC_WORDS):
                op_missing.append(x)
            if x.details.get("also_in"):
                ch += f" [same words also in {', '.join(x.details['also_in'])}: not targeted]"
                ch_md += f" [same words also in {', '.join(x.details['also_in'])}: not targeted]"
            pu = s.state.get(o.provision)
            bad = "; ".join(c["id"] + ": " + c["detail"] for c in x.checks if not c["ok"])
            md.append(f"| {o.id} | {o.type} | {tgt} | {ch_md.replace('|', '/')} | {o.provision} p{pu.pages[0] if pu and pu.pages else '?'} | "
                      f"{('yes' if x.applied else 'no: ' + _held(r, x)) if x.valid else 'NO — ' + bad.replace('|', '/')} | "
                      f"{review.label(r['reviews'][('op', o.id)])} ({o.origin}) | {iss.replace('|', '/')} |")
            changes.append({"stage": s.stage, "op": o.id, "type": o.type, "target": tgt, "change": ch, "provision": o.provision,
                            "valid": x.valid, "withdrawn": x.withdrawn, "applied": x.applied, "failed_checks": bad, "review": review.label(r["reviews"][("op", o.id)]), "origin": o.origin,
                            "issue": o.issue or "", "issue_ids": ids})
        md += ["", "### Register rows that move", "", "| Row | Before | After | Why |", "|---|---|---|---|"]
        # session 12 (W3a): one predicate with A5, the diff and the candidate (signals.requirement_delta): a row that a
        # confirming op or a re-made reading with the same words, values, parameters, dates and consequence touches is
        # CONFIRMED (unchanged), listed apart with the op and provision it rests on, never as a row that moves
        from .signals import (CONFIRMED, acknowledgement_rows, cause_relationships, in_force_pending,
                              relationship_issue_notes, row_label)
        causes = programme.answers_by_row(r, s.stage)
        # session 13 (F4; audit R1-9): an issue's notes on this stage's lines only from the stage its evidence exists
        pend_here = in_force_pending(r.get("pending_issues"), r.get("issue_stages") or issue_stages(r), r["order"],
                                     s.stage)
        unsettled = {}
        if r.get("working") is not None and s.stage in {x.stage for x in r["stages"]
                                                        if r["order"].index(x.stage) > r["order"].index(r["validated"].stage)}:
            from .partial import unresolved_rows
            unsettled = unresolved_rows(r)                # a row a pending stage does not settle is never CONFIRMED
        ack_rows = acknowledgement_rows(r.get("templates"))   # session 12 (F5, audit R-f): Form 4-A names the Addenda
        confirmed_md, open_md = [], []
        for e in r["evals"]:
            a, b = e["stages"][prev.stage], e["stages"][s.stage]
            pa = [d["planning"] for d in a["dates"]] if a["active"] else []
            pb = [d["planning"] for d in b["dates"]] if b["active"] else []
            why = []
            here = [h for h in b["ops"] if r["register"].op_stage.get(h) == s.stage]
            if here or a["active"] != b["active"] or (a["status"] == "NOT ISSUED") != (b["status"] == "NOT ISSUED"):
                why.append("status")                 # not a relabel such as AMENDED -> ACTIVE (as amended by ...)
            if b["interpretation_stage"] == s.stage and a["interpretation"] != b["interpretation"]:
                why.append(f"interpretation re-made at {s.stage}" + (f" ({' '.join(b['interpretation']['note'].split())})"
                                                                    if (b["interpretation"] or {}).get("note") else ""))
            if pa != pb and a["active"] and b["active"]:
                why.append("dates moved")
            if bool(a["stale"]) != bool(b["stale"]):
                why.append("became STALE" if b["stale"] else "no longer STALE")
            # session 12 (F2, audit A2-2/A2-3): the one predicate for every row in force at both stages; a row whose
            # dependencies (relationships, its consequence unit, a printed anchor date) or cited units changed is listed
            # and CHANGED with the cause named, whatever confirmation touched it. F5 (audit R-f): the label is the one
            # A5's replan deltas give the row (signals.row_label): a row naming the Addenda issued is CHANGED at every
            # later stage; a row the stage leaves unsettled (a printed date conflict, an undecided human-owned issue) is
            # NOT SETTLED, listed even when nothing else moved
            dl = row_label(a, b, causes.get(e["row"].id), unsettled.get(e["row"].id),
                           acknowledge=(s.stage, prev.stage) if e["row"].id in ack_rows else None) \
                if a["active"] and b["active"] else None
            label = (dl or {}).get("label")
            if label == "CHANGED" and dl.get("causes"):
                why.append("changed through: " + "; ".join(x["text"] for x in dl["causes"]))
                # session 13 (audit R1-1): the open issues of the relationships the change came through, one note
                # per issue (signals.issue_note: "open: I-X, human decision pending" for a pending one)
                why += relationship_issue_notes(r.get("relationships"), cause_relationships(dl["causes"],
                                                r.get("relationships")), pend_here, *issue_scope_args(r))
            if label == "CHANGED":
                # session 13 (F4; audit R1-7, R1-9): a changed row also names the open decisions that bear on it at this
                # stage (its pending list, the set A1's Issues cell shows), once each
                said = " ".join(why)
                why += [n for n in b.get("pending") or [] if n.split(",")[0] + "," not in said]
            if why or label:
                da = "; ".join(_date_readings(d) for d in a["dates"]) if a["active"] else ""
                db = "; ".join(_date_readings(d) for d in b["dates"]) if b["active"] else ""
                before = a["status"] + (f" [{da}]" if da else "")
                after = b["status"] + (f" [{db}]" if db else "") + (" — STALE: " + "; ".join(b["stale"]) if b["stale"] else "")
                if label == "NOT SETTLED":
                    why = [x for x in why if x != "status"] + [dl["detail"]]
                    open_md.append(f"| {e['row'].id} | {before} | {after.replace('|', '/')} | "
                                   f"{'; '.join(why).replace('|', '/')} |")
                    moved.append({"stage": s.stage, "row": e["row"].id, "change": "NOT SETTLED", "before": before,
                                  "after": after, "why": why, "chain": b["chain"]})
                    continue
                if label == CONFIRMED:
                    why = [f"{CONFIRMED}: {dl['detail']}"]
                    confirmed_md.append(f"| {e['row'].id} | {before} | {after.replace('|', '/')} | "
                                        f"{dl['detail'].replace('|', '/')} |")
                    moved.append({"stage": s.stage, "row": e["row"].id, "change": CONFIRMED, "before": before,
                                  "after": after, "why": why, "chain": b["chain"]})
                    continue
                md.append(f"| {e['row'].id} | {before} | {after.replace('|', '/')} | {'; '.join(why).replace('|', '/')} |")
                moved.append({"stage": s.stage, "row": e["row"].id, "change": "CHANGED", "before": before, "after": after,
                              "why": why, "chain": b["chain"]})
        if open_md:
            md += ["", "### Rows not settled at this stage (NOT SETTLED)", "",
                   "Nothing in the row changed, but it is not confirmed either: a printed date conflicts with its amended "
                   "anchor, a provision of the stage is unresolved, or an issue linked to the row is a person's decision "
                   "not yet recorded (HUMAN DECISION PENDING). A person decides; the same label as A5's replan deltas.",
                   "", "| Row | Before | After | Why not settled |", "|---|---|---|---|"] + open_md
        if confirmed_md:
            md += ["", f"### Rows confirmed or re-read, unchanged ({CONFIRMED})", "",
                   "A confirming op (an annotation labelled confirms or interprets, or an answer that only confirms) or a "
                   "reading re-made with the same words, values, parameters, dates and consequence: not a change. The op "
                   "and provision it rests on are named; labels are proposals a person checks.", "",
                   "| Row | Before | After | Confirmed by |", "|---|---|---|---|"] + confirmed_md
        if r.get("relationships"):                  # session 10: indirect effects, kept apart from the rows above
            recs = ((r.get("relationship_impact") or {}).get(s.stage) or {}).get("records", [])
            md += ["", "### Reached through relationships (indirect: for review, not direct citations)", "",
                   "Curated links (relationships file) followed from what this addendum changed. The rows above cite a "
                   "changed unit; these are reached through another provision. A5 marks the activities that serve them "
                   "REVIEW with their dates unchanged.", "", relationships.STATUS_LEGEND, ""]
            # session 13 (audit R1-1): each record carries the open issues of the relationships on its path and of
            # the documents not supplied that block it (signals.relationship_issue_notes; the same note for every issue)
            scope_args = issue_scope_args(r)              # session 14 (W4): the same scope rule on the records
            notes = lambda x: relationship_issue_notes(r["relationships"], list(x["path"]) + [  # noqa: E731
                b["entry_id"] for b in x.get("blockers") or []], pend_here, *scope_args)
            # session 13 (F4; audit R1 nit): the non-binding context of the entries on the path, as a2.md words it
            ctx = lambda x: "; ".join(dict.fromkeys(  # noqa: E731
                relationships.context_text(e)[len("context (not binding): "):] for e in r["relationships"]
                if isinstance(e, dict) and e.get("id") in set(x["path"]) | {b["entry_id"] for b in x.get("blockers") or []}
                and e.get("context")))
            with_notes = lambda line, x: line + "".join(f"; {n}" for n in notes(x))  # noqa: E731
            for cls, items in relationships.by_class(recs):
                md.append(f"**{cls[0].upper() + cls[1:]}** ({len(items)})")
                md += [with_notes(f"- {relationships.label(x)}", x).replace("|", "/") for x in items] or ["- none"]
                md.append("")
            gp = relationships.gaps(recs)
            md.append(f"**Referenced but not supplied: conclusions in play that cannot be established** "
                      f"({len(gp) + len(op_missing)})")
            md += ([with_notes(f"- {relationships.label(x, r['relationships'])}", x).replace("|", "/") for x in gp]
                   + [f"- {x.op.id} ({x.op.provision} p{(s.state[x.op.provision].pages or ['?'])[0] if x.op.provision in s.state else '?'}; "
                      f"op issue): {x.op.issue}".replace("|", "/") for x in op_missing]) or ["- none"]
            rel_rows += [{"stage": s.stage, "class": "not supplied" if x["kind"] == "missing_document" else x["class"],
                          "target": x["target"], "target_type": x.get("target_type", ""),
                          "target_status": x.get("target_status", ""), "kind": x["kind"], "link_status": x["status"],
                          "path": x["path"], "sources": x["sources"], "lexical": x["lexical"],
                          "via_target": x["via_target"], "direct": x.get("direct", False),
                          "blocked_by": [f"{b['entry_id']}: {b['document']}" for b in x.get("blockers") or []],
                          "open_issues": notes(x), "context (not binding)": ctx(x)}
                         for x in recs]
            rel_rows += [{"stage": s.stage, "class": "not supplied", "target": x.op.target or ", ".join(x.op.targets),
                          "target_type": "op", "target_status": "", "kind": "missing_document (op issue)",
                          "link_status": "", "path": [x.op.id], "sources": [x.op.provision], "lexical": False,
                          "via_target": False, "direct": True, "blocked_by": [x.op.issue], "open_issues": [],
                          "context (not binding)": ""}
                         for x in op_missing]
        ans = answers_to_review(r, s) + reversed_ops(r, s, prev)     # session 11 audit (A2-10): ops reversed too
        md += ["", "### Earlier answers to review (never revoked automatically)", ""]
        md += [f"- `{x['answer']}` ({x['issued_by']}): {x['why']}. {x['status']}"
               + (f": {x['reread']}." if x.get("reread") else ".") for x in ans] or ["None found."]
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
    md += ["## Evidence chains (rows changed by an addendum)", "",
           "Rows whose status or dates an addendum changed (session 11 audit, A2-7): every unit the row cites, then each "
           "op that changed it and each annotation or anchor change that re-made it or moved its dates, newest first.", ""]
    changed_rows = {m["row"] for m in moved if any(w == "status" or w == "dates moved" for w in m["why"])}
    for e in r["evals"]:
        ch = e["stages"][r["order"][-1]]["chain"]
        if e["row"].id in changed_rows:
            md.append(f"- **{e['row'].id}**: " + " ← ".join(reversed(ch)))
    return {"markdown": "\n".join(md) + "\n", "changes": changes, "provisions": provs, "rows_moved": moved, "answers": answers,
            "summary": summary_rows, "relationships": rel_rows}


# ---------------------------------------------------------------------------------------------- A3

MISSING_DOC_WORDS = ("not supplied", "not in the pack", "referenced but", "not provided")
A3_CLASS_ORDER = (("rejection", "Rejection"), ("disqualification", "Disqualification"),
                  ("non_responsive", "Non-responsive"),
                  ("exclusion", "Exclusion (Arabic text only; not equated with the other categories; I-F4C-EXCLUSION)"))


def _infeasibility_basis(r: dict, a5: dict | None) -> dict[str, dict]:
    """Activity id -> what its INFEASIBLE status rests on (session 11, audit A3-2), from the A5 drivers
    (programme.drivers): the PROVISIONAL lead times whose shortening alone would make it feasible, each with its value,
    what it is for and whether the pack states it, and the activity's total float. Generated, never typed."""
    if not a5:
        return {}
    try:
        drv = programme.drivers(a5, r["assumptions"], r["register"].cal_by_stage.get(a5.get("stage"), r["cal"]))
    except Exception:                                    # noqa: BLE001  a label only: A5 states its drivers itself
        return {}
    lead = (r.get("assumptions") or {}).get("lead_times") or {}
    acts = {a["id"]: a for a in a5["activities"]}
    by_key: dict[str, dict] = {}
    for a in a5["activities"]:
        by_key.setdefault(a.get("duration_assumption"), a)
    out = {}
    for d in drv:
        keys = list(dict.fromkeys(m[1] for o in d["would_make_feasible"] for m in [re.match(r"(\w+) <= \d+ WD \(now", o)] if m))
        lts = []
        for k in keys:
            a = by_key.get(k) or {}
            basis = str((lead.get(k) or {}).get("basis", ""))
            lts.append(f"{a.get('item') or a.get('name') or k} {(lead.get(k) or {}).get('value', a.get('duration_wd'))} WD"
                       + (", not stated in the pack" if re.search(r"not stated|no lead time stated", basis) else ""))
        out[d["activity"]] = {"keys": keys, "lead_times": lts, "float_wd": (acts.get(d["activity"]) or {}).get("float_wd"),
                              "status": d["status"]}
    return out


def _infeasible_flag(acts: list[str], basis: dict[str, dict]) -> str:
    lts = list(dict.fromkeys(x for a in acts for x in (basis.get(a) or {}).get("lead_times", [])))
    fl = sorted({basis[a]["float_wd"] for a in acts if a in basis and basis[a].get("float_wd") is not None})
    return ("INFEASIBLE on PROVISIONAL assumed lead times: " + ("; ".join(lts) or "see A5 drivers")
            + (f"; float {fl[0]} WD" if fl else "") + "; I-A5-FEASIBILITY")


def _cite_listed(f: str, folded: dict[str, str]) -> str:
    """A flag with each folded issue id replaced by the id it is listed under on the page (once)."""
    for i in signals.issue_refs(f):
        if i in folded:
            root = folded[i]
            f = re.sub(r"(?<![\w./-])" + re.escape(i) + r"(?![\w-])", "" if root in f else root, f)
            f = re.sub(r"(?:;\s*){2,}", "; ", f).strip(" ;")
    return f


def _when(d: dict) -> str:
    """A computed date with every other reading of the rule beside it (D4: readings that differ are all shown)."""
    p = str(d["planning"]["value"])
    return p + "".join(f" ({i['value']} if {i['key'].replace('_', ' ')})" for i in d.get("interpretations") or []
                       if str(i["value"]) != p)


def _date_facts(r: dict, row, ev: dict, v: str, status_date: str | None) -> list[str]:
    """Computed date facts an A3 line states (session 11, audit A3-7/A3-9), from the register's date rules: where a
    window the row depends on starts; an event of the row already past at the A5 status date (compliance is then a fact
    to confirm, with the row's programme issues); and a deadline on another row in force that shares an evidence item
    with this one and has closed by the status date (e.g. a correction window). Never typed."""
    out, rules = [], {x.rule_id: x for x in row.date_rules}
    cur = r.get("curated_issues") or {}
    anchors = r["rowfile"].anchors
    for d in ev["dates"]:
        val_ = str(d["planning"]["value"] or "")
        rd = rules.get(d["rule_id"])
        if not val_ or rd is None:
            continue
        if d["purpose"] == "window_start" and rd.kind == "relative":     # a window that moves with its anchor
            out.append(f"window starts {_when(d)}" + (
                f": {rd.offset} {rd.unit.replace('_', ' ')}{'s' if rd.offset != 1 else ''} {rd.direction} the "
                f"{rd.anchor} {d['anchor_value']}" if d.get("anchor_value") else ""))
        elif d["purpose"] == "event" and status_date and val_ < status_date:
            own = [i for i in row.issues if (cur.get(i) or {}).get("theme") == "programme"]
            out.append(f"held {_when(d)} (before the status date): compliance is a bidder fact to confirm"
                       + (f" ({', '.join(own)})" if own else ""))
    if status_date and row.evidence:
        for e2 in r["evals"]:
            if e2["row"].id == row.id or not set(e2["row"].evidence) & set(row.evidence) \
                    or not in_force(e2["stages"][v]["status"]):
                continue
            for d in e2["stages"][v]["dates"]:
                if d["purpose"] == "deadline" and d["planning"]["value"] and str(d["planning"]["value"]) < status_date:
                    u = next((s.state for s in r["stages"] if s.stage == v), r["validated"].state).get(d["source_unit"])
                    ref = _doc_ref(d["source_unit"], [], u.number if u else None)
                    out.append(f"{ref} window closed {_when(d)}")
    return out


def _corroborations(r: dict, v: str, explicit: list[dict]) -> dict[str, dict]:
    """Row id -> its verified corroboration (session 11, audit A3-6): the row's consequence restates another explicit
    row's, of the same class, and every quotation it gives is found in its unit's effective text at `v`. A claim that
    fails is returned with `problem` (the row then stays on its own line, flagged)."""
    state = next((s.state for s in r["stages"] if s.stage == v), r["validated"].state)
    by_id = {x["id"]: x for x in explicit}
    out = {}
    for x in explicit:
        row = next((e["row"] for e in r["evals"] if e["row"].id == x["id"]), None)
        c = getattr(row, "corroborates", None)
        if c is None:
            continue
        bad = [f"{q.unit}: '{q.words[:60]}' not found" for q in [*c.also, *c.adds_evidence]
               if q.unit not in state or not found(q.words, state[q.unit].text or "")]
        tgt = by_id.get(c.row)
        if tgt is None or tgt.get("cls") != x.get("cls"):
            bad.append(f"{c.row} is not an explicit {x.get('class')} row at {v}")
        refs = []
        for q in c.also:
            u = state.get(q.unit)
            refs.append(_doc_ref(q.unit, [q.page], u.number if u else None))
        out[x["id"]] = {"row": c.row, "also": refs, "adds": c.adds, "problem": "; ".join(bad),
                        "adds_evidence": [f"{q.unit} p{q.page}: “{q.words}”" for q in c.adds_evidence]}
    return out


def fold_issues(r: dict, issues: list[dict], a5: dict | None, basis: dict[str, dict] | None = None) -> dict:
    """How the open issues go on the one page (session 11, audit A3-1/A3-5/R-3/R-5): overlapping issues are folded into
    the issue they restate BEFORE anything is shrunk, and pipeline/A2 matters stay on a3_detail.html. Rules, applied to
    any pack: (1) the curated `folds`; (2) an A5 per-activity issue of an INFEASIBLE or DEADLINE PASSED activity folds into
    I-A5-FEASIBILITY, which folds into the one curated 'programme' issue carried by the rows of the activity whose lead
    time alone would make it feasible (the A5 drivers); (3) a document referenced but not supplied folds into the first
    curated 'missing' issue its relationship entries link; (4) amendment-op issues (I-OP-*) and cover-summary findings
    (C28, A2) and curated issues marked `page: detail` are listed on a3_detail.html only. Returns {root: [folded ids,
    transitively]}, {folded id: root}, the detail-only ids and the A5 summary of a root that folds I-A5-FEASIBILITY."""
    by_id = {i["id"]: i for i in issues}
    cur = r.get("curated_issues") or {}
    direct = {i["id"]: [f for f in i.get("folds") or [] if f in by_id] for i in issues}
    late = [a for a in (a5 or {}).get("activities", []) if a["status"].startswith(("INFEASIBLE", "DEADLINE PASSED"))]
    if "I-A5-FEASIBILITY" in by_id:
        direct["I-A5-FEASIBILITY"] += [f"I-A5-{a['id']}" for a in late if f"I-A5-{a['id']}" in by_id]
        keys = {k for b in (basis or {}).values() for k in b.get("keys", [])}
        rows = {rid for a in (a5 or {}).get("activities", []) if a.get("duration_assumption") in keys for rid in a["req_ids"]}
        roots = sorted({i for e in r["evals"] if e["row"].id in rows for i in e["row"].issues
                        if (cur.get(i) or {}).get("theme") == "programme" and i in by_id})
        if len(roots) == 1:
            direct[roots[0]].append("I-A5-FEASIBILITY")
    for i in issues:
        root = next((x for x in i.get("linked") or [] if (cur.get(x) or {}).get("theme") == "missing" and x in by_id), None)
        if root and root != i["id"]:
            direct[root].append(i["id"])
    parent = {f: k for k, fs in direct.items() for f in fs if f != k}

    def top(i: str) -> str:
        seen = set()
        while i in parent and i not in seen:
            seen.add(i)
            i = parent[i]
        return i
    folded = {f: top(f) for f in parent}
    roots: dict[str, list[str]] = {}
    for f, k in folded.items():
        roots.setdefault(k, []).append(f)
    detail = sorted(i["id"] for i in issues if i["id"] not in folded and (
        i.get("source") in ("amendment op", "C28 (automatic)") or (cur.get(i["id"]) or {}).get("page") == "detail"))
    a5_note = {}
    if late and "I-A5-FEASIBILITY" in folded:
        lts = list(dict.fromkeys(x for a in late for x in ((basis or {}).get(a["id"]) or {}).get("lead_times", [])))
        by = sorted({m[1] for a in late for m in [re.search(r"by (\d+) WD", a["status"])] if m}, key=int)
        a5_note[folded["I-A5-FEASIBILITY"]] = (f"A5: {len(late)} INFEASIBLE" + (f" by {by[-1]} WD" if by else "")
                                               + (f" (PROVISIONAL {'; '.join(x.split(', not stated')[0] for x in lts)})"
                                                  if lts else ""))
    return {"roots": {k: sorted(v) for k, v in roots.items()}, "folded": folded, "detail": detail, "a5_note": a5_note}


# session 13 (F2; audit R2-6): the brief's A4 is the work log; the register is a supporting record
REGISTER_LABEL = "clarification register (supporting record, out/a4/clarification_register.*)"


def trigger_count(explicit: list[dict]) -> str:
    """The count of the explicit bid-out triggers as every output prints it (session 13, F2; audit R2-9): the distinct
    triggers, and each row listed on another's line (it restates that row's consequence) named beside the count:
    '16 (+ VOL-IV-F4C-N1, which restates VOL-I-9.4-01)'."""
    n = sum(1 for x in explicit if not x.get("corroborates"))
    extra = [f"+ {x['id']}, which restates {x['corroborates']}" for x in explicit if x.get("corroborates")]
    return f"{n}" + (f" ({'; '.join(extra)})" if extra else "")


def a3_count_words(explicit: list[dict], score: list[dict], members: dict | list) -> str:
    """The A3 set in one phrase, from the one set (schedule.a3_rows, F3) and the page's lines (session 13, F2; audit
    R2-9, R3-5): '16 (+ VOL-IV-F4C-N1, which restates VOL-I-9.4-01) explicit bid-out triggers + 1 below the score
    threshold = 18 A3 rows'. The page, a3_detail.html, review batch 2 and checks.json C13 print it."""
    return (f"{trigger_count(explicit)} explicit bid-out triggers + {len(score)} below the score threshold = "
            f"{len(members)} A3 rows")


def answer_row_index(r: dict) -> dict[str, tuple[list[str], list[str]]]:
    """Row id -> (its units and effective units at the validated stage, its issues), for clarify.question_rows."""
    v = r["validated"].stage
    out = {}
    for e in r.get("evals") or []:
        ud = (e["stages"].get(v) or {}).get("units_detail") or []
        out[e["row"].id] = (list(e["row"].units) + [d.get("effective_unit") for d in ud if d.get("effective_unit")],
                            list(e["row"].issues or []))
    return out


def a3(r: dict, issues: list[dict], a5: dict | None) -> dict:
    """A3: one readable page. One line per requirement, grouped by the consequence the documents state; the
    quotations, sources and flags of every line are in a3_detail.html (linked by row id)."""
    val = r["validated"]
    v = val.stage
    infeasible = {}
    row_checks = ((a5 or {}).get("a3_coverage") or {}).get("row_checks") or {}   # row -> the activities that only CHECK it
    for a in (a5 or {}).get("activities", []):
        if a["status"].startswith("INFEASIBLE"):
            for rid in a["req_ids"]:
                if isinstance(row_checks.get(rid), list) and a["id"] in row_checks[rid]:
                    continue      # session 11 recheck: a check carried by an infeasible activity is not itself infeasible
                infeasible.setdefault(rid, []).append(a["id"])
    basis = _infeasibility_basis(r, a5)       # session 11 (A3-2): what each INFEASIBLE status rests on (A5 drivers)
    status_date = (a5 or {}).get("status_date") or val.issued
    explicit, score, none_stated = [], [], []
    refused, zero, gate = [], [], []          # session 09: document_refusal and criterion_zero; the gate's row ids
    summary_currency_cache = summary_currency(r)
    rel_recs = ((r.get("relationship_impact") or {}).get(v) or {}).get("records", []) if r.get("relationships") else []
    members = a3_rows(r["evals"], v)          # session 13 (R3-5): the A3 rows, one set (and one function) with A5's
    rel_flags: dict[str, list[str]] = {}      # session 10: shown on a3_detail.html only (the one page keeps its fit)
    for x in rel_recs:
        if x["kind"] != "missing_document":
            rel_flags.setdefault(x["target"], []).append(f"REVIEW ({x['class']}): reached at {v} from "
                                                         f"{', '.join(x['sources'])} via {' > '.join(x['path'])}")
    for e in r.get("relationships") or []:
        if isinstance(e, dict) and e.get("kind") == "missing_document":
            for t in relationships.ends(e, "to"):
                rel_flags.setdefault(t, []).append(f"NOT SUPPLIED: {e.get('document')} ({e.get('id')}, link "
                                                   f"{e.get('status')}): cannot be established: {e.get('blocks')}")
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
        flags += [f for f in ev.get("flags") or [] if derived.is_switch_flag(f)]   # session 12 (W3b): re-read
        if getattr(row, "derived_consequence", None) is not None:                   # session 12 (W3b)
            dc = row.derived_consequence
            flags.append(f"DERIVED CONSEQUENCE from {dc.rule} (PROPOSED; " + (
                "deterministic: the rule's words name the value)" if dc.owner == "deterministic" else
                f"{human_owned.HUMAN_DECISION_PENDING}: whether {dc.unit} covers it)"))
        if row.id in infeasible:
            flags.append(_infeasible_flag(infeasible[row.id], basis))
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
                "flags": flags, "row_source": rsrc.get("latest", ""),
                **({"rel_flags": rel_flags[row.id]} if row.id in rel_flags else {})}
        facts = _date_facts(r, row, ev, v, status_date)          # session 11 (A3-7, A3-9): computed, never typed
        if facts:
            base["facts"] = facts
        if csrc and rsrc.get("latest") and (rsrc.get("from_amendment") or " as amended by " in rsrc["latest"]) \
                and rsrc["latest"] != csrc:
            csrc = f"{csrc}; the requirement as amended: {rsrc['latest']}"   # e.g. the deadline amendment beside 6.6
        cls = (members.get(row.id) or {}).get("class")
        if cls in BID_OUT and isinstance(cons, Consequence):
            cu = val.state.get(cons.unit)
            explicit.append({**base, "cls": cons.cls, "class": CLASS_WORDS[cons.cls], "consequence": cons.quote,
                             "gloss": cons.gloss, **({"gloss_label": consequence_gloss(r, row, cons)} if cons.gloss else {}),
                             "source": csrc or _doc_ref(cons.unit, cu.pages if cu else [], cu.number if cu else None)})
        elif cls == "score_elimination" and isinstance(cons, Consequence):
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
    # session 11 (A3-6): a row whose consequence restates another explicit row's is listed once, on that row
    corr = _corroborations(r, v, explicit)
    for x in explicit:
        c = corr.get(x["id"])
        if c and not c["problem"]:
            x["corroborates"] = c["row"]
            tgt = next(y for y in explicit if y["id"] == c["row"])
            tgt.setdefault("corroborated_by", []).append(
                {"id": x["id"], "source": x["source"], "consequence": x["consequence"], "confidence": x["confidence"],
                 "also": c["also"], "adds": c["adds"], "adds_evidence": c["adds_evidence"],
                 **({"gloss": x["gloss"], "gloss_label": x.get("gloss_label", "")} if x.get("gloss") else {})})
        elif c:
            x["flags"].append(f"CORROBORATION NOT VERIFIED ({c['problem']})")
    shown = [i for i in issues if i["show_in_a3"]]
    missing = [i for i in shown if any(w in i["text"].lower() for w in MISSING_DOC_WORDS)]
    unresolved = [i for i in shown if i not in missing]
    # every open issue, grouped by theme; session 11 (A3-1, A3-5, R-3, R-5): overlapping issues are folded into the issue
    # they restate first, pipeline and A2 matters stay on a3_detail.html, and each issue on the page keeps its reason
    # (`short`) and owner; an issue a person must decide before submission (show_in_a3: the 'unresolved' and 'missing'
    # lists below) is marked `decide` on the line it is listed on
    fo = fold_issues(r, issues, a5, basis)
    folded, detail_only = fo["folded"], set(fo["detail"])
    listed_as = lambda i: folded.get(i, i)  # noqa: E731
    # session 12 (audit A3-3, A3-4): a flag cites an issue as it is listed on the page (a folded id by the issue it is
    # folded into), and a confidence below high points to the row's issues listed on the page (its reason)
    on_page = {i["id"] for i in issues if i["id"] not in folded and i["id"] not in detail_only}
    rows_by_id = {e["row"].id: e["row"] for e in r["evals"]}
    for x in [*explicit, *score, *none_stated, *refused, *zero]:
        x["flags"] = [_cite_listed(f, folded) for f in x.get("flags") or []]
        if x.get("confidence") and x["confidence"] != "high":
            see = list(dict.fromkeys(listed_as(i) for i in rows_by_id[x["id"]].issues if listed_as(i) in on_page
                                     and listed_as(i) not in dict(A3_CLASS_ORDER).get(x.get("cls"), "")))
            if see:
                x["confidence"] = f"{x['confidence']} (see {', '.join(see[:2])})"
    decide = {listed_as(i["id"]) for i in shown}
    clar = r.get("clarifications") or {}
    # session 13 (F2; audit R2-4/R2-5/R2-7): the questions as A4 shows them (owner, interim label, rows), one function
    shown_qs = clarify.presented(clar, r.get("decisions"), r.get("pending_issues"), r.get("curated_issues"),
                                 answer_row_index(r))
    # session 13 (F2; audit R2-7): a drafted question tied to no issue listed on the page is named, with its subject, on
    # its group's line, and whether its answer changes a bid-out row (an explicit trigger or the score threshold) is said
    bid_out = {x["id"] for x in explicit} | {x["id"] for x in score}

    subject = question_subject                  # session 13 (F4; audit R2-12): the entry's own subject words
    unlisted: dict[str, list[str]] = {}
    for q in shown_qs:
        if {listed_as(i) for i in q.get("linked_issues") or []} & on_page:
            continue
        hit = sorted(set(q.get("answer_rows") or []) & bid_out)
        unlisted.setdefault(str(q.get("theme")), []).append(
            f"{q['id']} ({subject(q)}" + (f"; changes bid-out row {', '.join(hit)})" if hit else ")"))
    unlisted_words = {k: "on no listed issue: " + "; ".join(v) + (
        "; no bid-out row" if not any("bid-out row" in x for x in v) else "") for k, v in unlisted.items()}
    groups = []
    for key, title in ISSUE_THEMES:
        members = [i for i in issues if issue_theme(i) == key and i["id"] not in folded and i["id"] not in detail_only]
        qs = sorted({q["id"] for q in clar.get("clarifications", []) if q.get("theme") == key})
        if not members and not qs:
            continue
        groups.append({"key": key, "title": title, "items": [
            {"id": i["id"], "short": issue_short(i) + (f"; {fo['a5_note'][i['id']]}" if i["id"] in fo["a5_note"] else ""),
             "owner": i["owner"], "folds": fo["roots"].get(i["id"], []), "decide": i["id"] in decide,
             # session 13 (F4; audit R2-11): a folded issue that is a person's decision not yet recorded is named on
             # its parent's line with the mark ('+1: ⚑ I-X (Owner)'), never hidden in the count
             "folds_pending": folded_pending(fo["roots"].get(i["id"], []), issues, i["owner"])} for i in members],
            "questions": qs, **({"unlisted": unlisted_words[key]} if key in unlisted_words else {})})
    n_listed = sum(len(g["items"]) for g in groups)
    gate_issues = sorted(i["id"] for i in issues if issue_theme(i) not in dict(ISSUE_THEMES))
    # session 12 (audit A3-2/A3-3): the same counts in fewer words, so the reasons on the lines keep the page's size
    # session 13 (F4; audit R2-11): a fold is not always a restatement (PAGE-LIMIT-Q2 under APPENDICES); the count says
    # 'folded (+n)' only, and a folded issue that is a person's decision not yet recorded is named on its line with ⚑
    issue_counts = (f"{len(issues)} open issues: {n_listed} listed, {len(folded)} folded (+n), "
                    f"{len(detail_only)} on a3_detail.html only"
                    + (f", {', '.join(gate_issues)} in the gate note" if gate_issues else "") + ".")
    n_marked = sum(1 for g in groups for it in g["items"] if it.get("decide"))
    # session 12 (F5; audit A3-5): † and ⚑ are defined once, in the legend at the top (A3_MARKS); the note counts
    decide_note = (f"† {len(unresolved)} unresolved, {len(missing)} not supplied"
                   + (f" ({n_marked} marked, the rest folded)" if n_marked < len(unresolved) + len(missing) else ""))
    pdd = next((d["anchor_value"] for e in r["evals"] for d in e["stages"][v]["dates"] if d["anchor"] == "PDD"), None)
    working = r["working"]
    compact = lambda x: {**x, "compact": True}  # noqa: E731  (the consequence quote is on a3_detail.html; nothing cut)
    sections = []
    for cls, title in A3_CLASS_ORDER:
        items = [compact(x) for x in explicit if x["cls"] == cls]
        if items:                          # a corroborating row is shown on the line of the row it restates (A3-6)
            sections.append({"heading": f"Explicit — {title}: {sum(1 for x in items if not x.get('corroborates'))}",
                             "note": "", "items": items})
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
    # session 11 (A3-3): what the pack says, no more: the pack names a general pass or fail check (VOL-I 11.1(i)) but not
    # which clause is checked at which stage; Envelope B rows (VOL-I 11.3) and rows with a lesser consequence are counted
    ev_items = r.get("evidence_items") or {}
    env_b = [x for x in gate if (lambda row: row.evidence and all(getattr(ev_items.get(k), "envelope", "") == "B"
                                                                  for k in row.evidence))(
        next(e["row"] for e in r["evals"] if e["row"].id == x))]
    sections.append({"heading": f"General gate — mandatory, pass or fail; no bid-out consequence stated (VOL-I 11.1(i)): {len(gate)}",
                     "note": "Mandatory; no bid-out consequence stated. VOL-I 11.1(i) is a general pass/fail check; the pack "
                             "does not say which clause is checked at which stage"
                             + (f" ({len(env_b)} are Envelope B items, VOL-I 11.3)" if env_b else "")
                             + ". No clause-specific label or curability is implied (I-NO-CONSEQUENCE)."
                             + (" It also holds the rows whose document is refused (above)." if len(gate) > len(none_stated)
                                else ""),
                     "items": [], "ids": gate, "envelope_b_ids": env_b})
    n_rows = len(r["evals"])
    n_distinct = sum(1 for x in explicit if not x.get("corroborates"))
    rc = _count(r["reviews"][("row", e["row"].id)]["status"] for e in r["evals"])
    readings = sorted({(u["reading"]["region"], u["reading"]["status"]) for u in r["units"]
                       if (u.get("reading") or {}).get("region") and u["kind"] != "region"})
    pend = [g for g, st in readings if st == "pending"]
    # session 12 (audit A3-2): the footer already says every id links to its quotes, sources and flags (a3_detail.html)
    banner = ("WORKING DRAFT — every register row and amendment op is PROPOSED: "
              + (f"{rc['proposed']} rows. " if set(rc) == {"proposed"} else
                 ", ".join(f"{k} {n}" for k, n in sorted(rc.items())) + " rows. ")
              + (f"Image readings pending the owner's review: {', '.join(pend)}. " if pend else
                 f"Image readings: {approval_covers(any(u.get('translation') for u in r['units'] if (u.get('reading') or {}).get('status') == 'approved'), plural=True)} "   # session 12 (R-2)
                 "confirmed by the owner (approval file); their interpretations are proposed. ")
              + "Explicit wording only.")
    page = {
        "title": "A3 — What would put this bid out (working draft)",
        "subtitle": f"State after {v} (issued {val.issued}); Proposal Due Date (PDD) "  # from the anchor's effective text
                    + (" ".join(str(x) for x in map((r["anchor_details"][v].get("PDD") or {}).get, ("date", "time", "tz")) if x)
                       or "not stated in the effective text")
                    + (f". Working state {working.stage} is PARTIAL and NOT used here" if working else "")
                    + f". {a3_count_words(explicit, score, a3_rows(r['evals'], v))}.",   # (A3-3: a row restating another is shown on that
                                                                           # row's line; R2-9: and named in the count)
        "banner": banner,
        "sections": sections,
        "groups": {"heading": f"Unresolved matters, grouped — {n_listed} open issues"
                              + (f", {len(clar.get('clarifications', []))} clarification questions drafted (not sent)"
                                 if clar.get("clarifications") else ""),
                   "note": issue_counts + f" Line: id, reason (owner); {decide_note}. Unknown answers stay unknown."
                           + (f" Questions: {REGISTER_LABEL}." if clar.get("clarifications") else ""),
                   "counts": {"all": len(issues), "listed": n_listed, "folded": len(folded), "detail_only": len(detail_only),
                              "gate_note": gate_issues, "decide": len(shown)},
                   "groups": groups},
        # session 11 (A3-8, R-4): the same issues as in `groups` (merged there and marked †), with where each is listed
        "missing": {"heading": f"Referenced but not supplied — impact: {len(missing)} (marked † in the grouped list)",
                    "items": [{"id": i["id"], "text": i.get("a3") or i["text"], "owner": i["owner"],
                               "listed_as": listed_as(i["id"])} for i in missing]},
        "unresolved": {"heading": f"Could not resolve — kept with people: {len(unresolved)} (marked † in the grouped list)",
                       "items": [{"id": i["id"], "text": i.get("a3") or i["text"], "owner": i["owner"],
                                  "listed_as": listed_as(i["id"])} for i in unresolved]},
        "footer": "tenderpack: evidence build + curation + config/assumptions.yaml. Each id links to a3_detail.html "
                  "(quotes, sources, flags) and traces to A1 and A2.",
        "explicit": explicit, "score": score, "none_stated": none_stated,
        "none_stated_ids": [x["id"] for x in none_stated],
        "explicit_ids": [x["id"] for x in explicit],
        "trigger_count": trigger_count(explicit),          # session 13 (F2; audit R2-9): one count, everywhere
        "a3_count_words": a3_count_words(explicit, score, a3_rows(r["evals"], v)),
        **({"refused": refused, "gate_ids": gate} if refused else {}), **({"criterion_zero": zero} if zero else {}),
        "issues_detail": [{"id": i["id"], "text": i["text"], "owner": i["owner"], "rows": i["rows"],
                           "theme": dict(ISSUE_THEMES).get(issue_theme(i), ""), "folded_into": folded.get(i["id"], ""),
                           "detail_only": i["id"] in detail_only, "decide": i["show_in_a3"],
                           "pending": bool(str(i.get("human_decision") or "").startswith(
                               human_owned.HUMAN_DECISION_PENDING))}
                          for i in issues],
        "issue_counts": issue_counts,
        # session 12: the status as presented (never answered/withdrawn without a person's recorded decision)
        "clarifications": shown_qs,
        **({"relationships": {
            "stage": v, "from": ((r.get("relationship_impact") or {}).get(v) or {}).get("from"),
            "note": "Rows, activities and calculations reached through the curated relationships from what the addendum "
                    "of this stage changed (not direct citations; for review). Documents referenced but not supplied are "
                    "listed with the conclusions they block.",
            "items": [{"class": "not supplied" if x["kind"] == "missing_document" else x["class"], "target": x["target"],
                       "target_type": x.get("target_type", ""), "target_status": x.get("target_status", ""),
                       "kind": x["kind"], "link_status": x["status"], "sources": x["sources"], "path": x["path"],
                       "direct": x.get("direct", False)} for x in rel_recs]}} if r.get("relationships") else {}),
    }
    fp = any(it.get("folds_pending") for g in groups for it in g["items"])  # session 13 (F4; R2-11): ⚑ on a fold
    page["legend"] = a3_legend(page, (A3_MARKS[:1] if n_marked else ()) + (A3_MARKS[1:] if fp else ()))   # session 12 (A3-3, F5): abbreviations, †
    if page["legend"]:
        page["subtitle"] += " " + page["legend"]
    return page


A3_LEVELS = 5
# session 12 (the coordinator, C43 on the blind-02 rehearsal after the session's additions): level 5 keeps every
# explicit trigger's quoted consequence, source and owner and drops the requirement's own words (in A1 and on
# a3_detail.html) before the page is declared not to fit
A3_REASON_WORDS = (16, 10)     # level 2, if it still does not fit: each issue's reason to its first N words, then fewer


def a3_pages(a3d: dict):
    """(level, reason words, page) in the order stage2.write tries them for the one page: levels 0, 1 and 2; then level 2
    with each issue's reason abbreviated to its first N words and '…' (A3_REASON_WORDS; never dropped; in full on
    a3_detail.html); then level 3 (reasons dropped: the last resort) and level 4."""
    for level in range(A3_LEVELS + 1):
        yield level, None, condense_a3(a3d, level)
        if level == 2:
            for n in A3_REASON_WORDS:
                yield level, n, condense_a3(a3d, level, reason_words=n)


def pending_mark(t: str) -> str:
    """A short line as the condensed page shows it (level 2): a leading HUMAN DECISION PENDING label (and its bracketed
    qualifier) written as the marker A3_PENDING_MARK, which the page's legend defines; the full label stays on
    a3_detail.html and in A1."""
    return re.sub(r"^" + re.escape(human_owned.HUMAN_DECISION_PENDING) + r"(?: \(([^()]*)\))?: ",
                  lambda m: A3_PENDING_MARK + (f" ({m.group(1)})" if m.group(1) else "") + " ", t or "")


def _first_words(t: str, n: int) -> str:
    w = str(t or "").split()
    return t if len(w) <= n else " ".join(w[:n]).rstrip(",;:—") + " …"

A3_PENDING_MARK = "\u2691"                          # ⚑: HUMAN DECISION PENDING on the condensed page (defined in its legend)
# session 12 (F5; audit A3-5): the two marks and what each means, in the legend of the page (and a3_detail.html): † an
# issue to decide before submission (the issue's show_in_a3), ⚑ an issue that is a person's judgment with no decision
# recorded (human_owned.pending_reasons: owner Legal or Commercial, own words asserting a judgment, a pending decision
# of the clarification register, an AI proposal); an item can carry both
A3_MARKS = (("\u2020", "decide before submission (no decision recorded)"),
            (A3_PENDING_MARK, "a legal, commercial or technical judgment no one has recorded"))
# session 12 (audit A3-3): every abbreviation the page uses, written out (definitions as the pack gives them); the page
# shows those its text uses (condense_a3 keeps them; a3_legend picks them)
A3_LEGEND = (("WD", "Working Day"), ("PDD", "Proposal Due Date"),
             ("PBN", "Preferred Bidder Notification"), ("LCC", "Local Content Certificate"),
             ("PCOD", "Project Commercial Operation Date"))


def a3_legend(page: dict, marks: tuple = ()) -> str:
    """'WD = Working Day; PDD = ...' for the abbreviations the page's text uses (and the `marks` it uses: (mark,
    meaning)), else ''."""
    import json as _json
    text = _json.dumps({k: v for k, v in page.items() if k not in ("issues_detail", "clarifications", "legend",
                                                                   "relationships", "none_stated", "explicit", "score",
                                                                   "missing", "unresolved")}, ensure_ascii=False)
    used = [(k, v) for k, v in A3_LEGEND if re.search(r"(?<![\w-])" + k + r"(?![\w-])", text)
            and f"{v} ({k})" not in text] + list(marks)     # one written out at its first use needs no entry
    return ("; ".join(f"{k}: {v}" for k, v in used) + ".") if used else ""


def condense_a3(a3d: dict, level: int, reason_words: int | None = None) -> dict:
    """What goes on the one page when the full content does not fit at a readable size (C43), in this order (session
    11, audit A3-1/R-3: the gate's id list goes before any issue's reason). Level 1: the gate's row ids become their
    count (listed on a3_detail.html). Level 2: each group's drafted question ids become their count (A4 register).
    Level 3: each open issue's reason is dropped (its linked id and owner stay). Level 4: each group of open issues
    becomes its count. Level 5 (session 12): each explicit trigger keeps its quoted consequence, source and owner but
    loses the requirement's own words (A1; a3_detail.html). The explicit consequences themselves are never condensed.
    Each step is stated on the page; the full text is on a3_detail.html. Without groups (an older a3 dict) the unresolved and missing lists become ids from level 3.
    Session 12 (F2): level 2 also writes the human-decision label as a marker defined in the legend, and with
    `reason_words` (a3_pages, only when level 2 does not fit otherwise) cuts each reason to its first N words with '…'."""
    if level == 0:
        return a3d
    page = {**a3d, "sections": [dict(s) for s in a3d["sections"]]}
    for sec in page["sections"]:
        if sec.get("ids"):
            sec["note"] = (sec.get("note") or "") + " Rows: a3_detail.html."
            sec["ids"] = []
    g = a3d.get("groups")
    if g and level >= 2:
        # session 12 (F2 follow-up): the same words, fewer of them, before any reason is dropped: the human-decision
        # label becomes a marker defined once in the legend (the full label stays on a3_detail.html and in A1)
        page["groups"] = {**g, "groups": [{**x, "questions": [], "n_questions": len(x.get("questions") or []),
                                           "items": [{**i, "short": pending_mark(i.get("short"))} for i in x["items"]]}
                                          for x in g["groups"]]}
        used = any(i["short"].startswith(A3_PENDING_MARK) or i.get("folds_pending")
                   for x in page["groups"]["groups"] for i in x["items"])
        dag = any(i.get("decide") for x in page["groups"]["groups"] for i in x["items"])
        legend = a3_legend(a3d, (A3_MARKS[:1] if dag else ()) + (A3_MARKS[1:] if used else ()))
        if a3d.get("legend") and legend:
            page["subtitle"] = a3d["subtitle"].replace(" " + a3d["legend"], "") + " " + legend
        if reason_words and level == 2:
            page["groups"] = {**page["groups"], "note": page["groups"]["note"] + " Reasons abbreviated (…) to fit one "
                              "page; in full on a3_detail.html.",
                              "groups": [{**x, "items": [{**i, "short": _first_words(i["short"], reason_words)}
                                                         for i in x["items"]]} for x in page["groups"]["groups"]]}
    if g and level >= 3:
        page["groups"] = {**page["groups"], "note": page["groups"]["note"] + " Condensed to fit one page: each "
                          "issue's reason is on a3_detail.html.",
                          "groups": [{**x, "items": [{**i, "short": ""} for i in x["items"]]} for x in page["groups"]["groups"]]}
    if g and level >= 4:
        page["groups"] = {**page["groups"], "note": g["note"] + " Condensed to fit one page: the count of "
                          "each group is shown; its issue ids, text and owners are on a3_detail.html.",
                          "groups": [{**x, "items": [], "questions": [], "count": len(x["items"]),
                                      "n_questions": len(x.get("questions") or [])} for x in g["groups"]]}
    if level >= 5:                                   # session 12: the triggers' requirement words go, their quotes stay
        for sec in page["sections"]:
            if sec.get("items"):
                sec["items"] = [{**i, "text": "", "flags": []} for i in sec["items"]]
                sec["note"] = (sec.get("note") or "") + " Condensed to fit one page: each trigger's requirement words are on a3_detail.html; its quoted consequence stays here."
    if not g and level >= 3:
        note = "condensed to fit one page: the text of each item is on a3_detail.html"
        for key in ("missing", "unresolved"):
            sec = a3d[key]
            page[key] = {"heading": sec["heading"], "note": note,
                         "ids": [i["id"] for i in sec["items"]], "owners": {i["id"]: i.get("owner") for i in sec["items"]}}
    page.setdefault("subtitle", a3d["subtitle"])
    page["banner"] = a3d["banner"] + " Shortened to fit one page."     # on the banner line, which has room
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
    counts = {"Explicit consequences": a3d.get("trigger_count")}          # session 13 (F2; audit R2-9)
    if a3d.get("criterion_zero"):                                     # session 09: only when there are such rows
        tables.append(("Criterion-level zero marks (scored; not a disqualification)", a3d["criterion_zero"]))
    if a3d.get("refused"):
        tables.append(("Document refused (the Proposal's fate is not stated; in the VOL-I 11.1(i) gate)", a3d["refused"]))
    tables.append(("Pass/fail with no bid-out consequence stated (VOL-I 11.1(i) general check; the pack does not say "
                   "which clause is checked at which stage)", a3d["none_stated"]))
    for title, items in tables:
        rows.append(f"<h2>{esc(title)} ({esc(counts.get(title) or str(len(items)))})</h2><table><tr><th>Row</th><th>Requirement</th><th>Consequence "
                    "(quoted)</th><th>Latest source</th><th>Confidence</th><th>Flags</th></tr>")
        for x in items:
            q = (f"<i>{esc(x.get('class', ''))}</i>: “{quote(x['consequence'])}”" if x.get("consequence") else "none stated")
            if x.get("gloss"):                    # session 11 (A3-4, R-1): the label follows the approval state
                q += f"<br><small>{esc(x.get('gloss_label') or GLOSS_NOT_REVIEWED)}: ‘{esc(x['gloss'])}’</small>"
            for c in x.get("corroborated_by") or []:                     # session 11 (A3-6)
                q += (f"<br><small>also stated in <a href=\"#{esc(c['id'])}\">{esc(c['id'])}</a> ({esc(c['source'])}: "
                      f"“{quote(c['consequence'])}”)" + (f" and {esc(', '.join(c['also']))}" if c.get("also") else "")
                      + (f"; {esc(c['adds'])} ({esc('; '.join(c.get('adds_evidence') or []))})" if c.get("adds") else "")
                      + "</small>")
            if x.get("corroborates"):
                q += f"<br><small>restates the consequence of <a href=\"#{esc(x['corroborates'])}\">{esc(x['corroborates'])}</a>: listed once on A3</small>"
            text = esc(x["text"]) + (f"<br><small>{esc('; '.join(x['facts']))}</small>" if x.get("facts") else "")
            rows.append(f'<tr id="{esc(x["id"])}"><td><b>{esc(x["id"])}</b></td><td>{text}</td><td>{q}</td>'
                        f'<td>{esc(x["source"])}<br><small>row: {esc(x.get("row_source", ""))}</small></td>'
                        f'<td>{esc(x["confidence"])}</td><td>{esc("; ".join(x["flags"] + x.get("rel_flags", [])))}</td></tr>')
        rows.append("</table>")
    rel = a3d.get("relationships")
    if rel:                                                       # session 10
        rows.append(f"<h2>Reached through relationships at {esc(rel['stage'])} ({len(rel['items'])})</h2>"
                    f"<p>{esc(rel['note'])}</p><p><i>{esc(relationships.STATUS_LEGEND)}</i></p>"   # session 12 (R-6)
                    "<table><tr><th>Class</th><th>Target</th><th>Status at the stage</th>"
                    "<th>Reached from</th><th>Via (relationships)</th><th>Kind; link status</th></tr>")
        rows += [f"<tr><td>{esc(x['class'])}</td><td><b>{esc(x['target'])}</b> <small>{esc(x['target_type'])}</small></td>"
                 f"<td>{esc(x['target_status'])}</td><td>{esc(', '.join(x['sources']))}</td>"
                 f"<td>{esc(' > '.join(x['path']))}</td><td>{esc(x['kind'])}; {esc(x['link_status'])}"
                 + ("; also changed directly" if x["direct"] else "") + "</td></tr>" for x in rel["items"]]
        rows.append("</table>")
    rows.append(f"<h2>Open issues ({len(a3d['issues_detail'])}), by group</h2>"
                + (f"<p>{esc(a3d['issue_counts'])} " + "; ".join(f"{k}: {v}" for k, v in A3_MARKS)   # F5 (A3-5, R-a)
                   + ".</p>" if a3d.get("issue_counts") else ""))
    for key in ("unresolved", "missing"):                         # session 11 (A3-8, R-4): the same lists as a3.json
        sec = a3d.get(key) or {}
        if sec.get("items"):
            rows.append(f"<p><b>{esc(sec['heading'])}:</b> " + "; ".join(
                f'<a href="#{esc(i["id"])}">{esc(i["id"])}</a>'
                + (f" (listed with {esc(i['listed_as'])})" if i.get("listed_as", i["id"]) != i["id"] else "")
                for i in sec["items"]) + "</p>")
    rows.append("<table><tr><th>Issue</th><th>Group</th><th>Text</th><th>Owner</th><th>Rows</th></tr>")
    rows += [f'<tr id="{esc(i["id"])}"><td><b>{esc(i["id"])}</b>{" †" if i.get("decide") else ""}'
             f'{" " + A3_PENDING_MARK if i.get("pending") else ""}</td><td>{esc(i.get("theme", ""))}'
             + (f'<br><small>listed with {esc(i["folded_into"])}</small>' if i.get("folded_into") else "")
             + ('<br><small>on this page only (pipeline, A2 or reading-precision matter)</small>' if i.get("detail_only") else "")
             + f'</td><td>{esc(i["text"])}</td><td>{esc(i["owner"])}</td><td>{esc(", ".join(i["rows"]))}</td></tr>'
             for i in sorted(a3d["issues_detail"], key=lambda i: (i.get("theme", ""), i["id"]))]
    rows.append("</table>")
    if a3d.get("clarifications"):
        rows.append(f"<h2>Clarification questions drafted, not sent ({len(a3d['clarifications'])})</h2><p>Full register "
                    + "(sources, impact, interim handling, the rows each answer would change): " + esc(REGISTER_LABEL) + ".</p><table><tr><th>Id</th><th>Clause</th>"
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
    questions = programme.gate_questions(r)          # session 11 audit (A5-1, F3): ask_by / finalise_by per gate
    for s in r["stages"][1:]:
        if not s.issued:
            continue
        pdd = next((d["anchor_value"] for e in r["evals"] for d in e["stages"][s.stage]["dates"] if d["anchor"] == "PDD"), None)
        anchors_by_stage[s.stage] = {"PDD": pdd}
        progs[s.stage] = plan(s.stage, r["evals"], r["templates"], r["assumptions"], r["register"].cal_by_stage[s.stage], date.fromisoformat(s.issued),
                              anchors_by_stage[s.stage], evidence_items=r["evidence_items"],
                              anchor_details=r["anchor_details"][s.stage], notified_days=r["non_working_days"].get(s.stage),
                              reached=((r.get("relationship_impact") or {}).get(s.stage) or {}).get("records"),
                              questions=questions, question_units=programme.question_units(r))   # F5 (A5 N2)
        programme.attach_open_decisions(progs[s.stage], r)       # session 13 (F2; audit R2-2, R3-1)
    return progs


# ---------------------------------------------------------------------------------------------- write

def write(r: dict, out: Path, candidate: bool = True, op_status: dict | None = None) -> dict:
    """Every output under `out`. With a working stage (a PARTIAL addendum) and `candidate`, also the candidate A3 and A5
    (tenderpack.partial: a3/a3_candidate.*, a5/candidate/), labelled NOT VALIDATED; the validated outputs are the same
    bytes with or without them. `op_status` (op id -> the controller's status) is shown beside each candidate op."""
    progs = a5_all(r)
    val = r["validated"].stage
    main = progs.get(val)
    issues = collect_issues(r, main)
    a3d = a3(r, issues, main)
    a3_fit: dict = {}
    for level, words, page in a3_pages(a3d):        # session 12 (F2): level 2 abbreviates reasons before level 3
        try:
            fit = write_a3_pdf(page, out / "a3" / "a3.pdf")
            a3_fit = dict(fit, explicit_ids=a3d["explicit_ids"], condensed=level, count_words=a3d.get("a3_count_words"),
                          **({"reason_words": words} if words else {}))
            a3d["condensed"] = level
            break
        except A3OverflowError as e:
            a3_fit = {"pages": 0, "error": str(e), "explicit_ids": a3d["explicit_ids"], "condensed": level}
    dump_json(a3d, out / "a3" / "a3.json")
    r["a3_count_words"] = a3d.get("a3_count_words")      # session 13 (F2; audit R2-9): batch 2 prints the same count
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
    if r.get("relationships"):                                    # session 10: indirect effects per addendum
        write_csv_json(tbl(a2d["relationships"]), out / "a2", "a2_relationship_impact")
    if r.get("clarifications"):
        clarify.write(r["clarifications"], out / "a4", r.get("decisions"),   # the detailed register sits with A4
                      [{"id": k, "owner": (r["curated_issues"].get(k) or {}).get("owner"),
                        "text": (r["curated_issues"].get(k) or {}).get("text"), "reasons": v}
                       for k, v in (r.get("pending_issues") or {}).items()],
                      r.get("curated_issues"), answer_row_index(r))   # session 13 (F2; audit R2-4/R2-5/R2-7)
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
            dl += [dict(x, from_stage=a, to_stage=b)                 # answers: session 11 audit (A5-4, F3)
                   for x in deltas(progs[a], progs[b], ea, eb, answers=programme.answers_by_row(r, b))]
        write_csv_json(tbl(dl), out / "a5", "replan_deltas")
        for st, p in progs.items():
            dump_json(p, out / "a5" / "stages" / f"{st}.json")
    prog_w = None
    if r["working"] and r["working"].stage in progs:
        prog_w = programme.stage_planner(r, r["working"].stage)(r["assumptions"])
        dump_json(prog_w, out / "a5" / "working" / f"{r['working'].stage}.json")
    cand_files, cand_error = [], None
    if candidate and r["working"]:                  # session 11: the PARTIAL addendum's candidate A3 and A5 (partial.py)
        from . import partial
        try:
            cand_files = partial.write(r, out, a3d, prog_ext if main else None, prog_w, op_status)
        except Exception as e:                      # noqa: BLE001  a candidate view never blocks the validated outputs;
            cand_error = f"{type(e).__name__}: {e}"  # its failure is written down and listed in README.md
            write_text(out / "a3" / "a3_candidate_FAILED.md", f"# A3/A5 candidate NOT produced\n\n{cand_error}\n")
    from .batches import write_batches
    write_batches(r, out / "review", r["evidence_dir"], issues,       # session 13 (R3-2): the cards read the issues
                  {x["id"]: x.get("issues") for x in a1d["rows"]},      # as A1 renders them
                  states=row_states(r),                                # session 14 (W4): value/interpretation/approval
                  readiness=programme.readiness_by_row(main))          # session 14 (W4): preparation vs finalisation
    for a, f in r["drafted"].items():
        write_text(out / "drafted" / f"{a}.yaml",
                   f"# DRAFTED by tenderpack.draft for this build; every op PROPOSED; not curated.\n"
                   + yaml.safe_dump(f.model_dump(exclude_none=True), allow_unicode=True, sort_keys=False, width=110))
    dump_json([{"stage": s.stage, "status": s.status, "issued": s.issued, "problems": s.problems, "scope_leak": s.scope_leak,
                "ops": [x.to_dict() for x in s.ops], "coverage": s.coverage} for s in r["stages"]], out / "stages.json")
    checks = structural_checks(r, a3_fit, {st: p for st, p in progs.items() if st == val})
    checks.append(gloss_currency_check(r, out))             # session 11 (C52): stale 'not reviewed' glosses
    rep = reported_checks(r)
    if (progs.get(val) or {}).get("a3_coverage") is not None:   # session 11 audit (A5-2, F3): rows the programme carries
        rep.append(programme.coverage_check(progs[val]))         # session 12 (audit A5-4): every A1 row in force
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
              "PROPOSED; " + readings_status_sentence(json.loads((r["evidence_dir"] / "coverage.json")
                                                                 .read_text(encoding="utf-8"))), "",
              "## What blocks a release (`outputs --strict`)", ""]
    readme += [f"- **{b['kind']}**: {b['detail']}" for b in blockers] or ["- nothing"]
    readme += ["",
              "| Output | Files |", "|---|---|",
              "| A1 compliance register (every row), status at each stage, review decisions | a1/a1.xlsx, a1/a1.csv, a1/a1.json |",
              "| A2 reconciliation: changes, rows that move, answers to review, provision coverage, evidence chains | a2/a2.md, a2/*.csv, a2/*.json |",
              "| A3 one-page disqualification sheet, with linked detail | a3/a3.pdf, a3/a3_detail.html, a3/a3.json |",
              "| A5 programme, marshalling plan, documents, resources, infeasibility drivers, scenarios, replan deltas, Gantt | a5/*.csv, a5/*.json, a5/gantt.*, a5/scenarios/, a5/stages/ |",
              # session 13 (audit R3-4): A4 is the work log (the brief's A4), kept in the repository's worklog/; the
              # clarification register is a supporting record under a4/
              a4_work_log_row(r["root"]),
              "| Supporting record: tender clarification register (DRAFT questions, NOT SENT; not the A4 work log) | "
              "a4/clarification_register.md, .csv, .json |",
              "| Engine results per stage | stages.json |", "| Checks | checks.json |", ""]
    if cand_files:                                  # session 11: only when a PARTIAL addendum gives a candidate
        readme[-1:-1] = [f"| A3 and A5 CANDIDATE: {r['working'].stage} as proposed, NOT VALIDATED (the rows and dates it "
                         "would move, blockers, conditional scenarios; the validated A3 and A5 above are unchanged) | "
                         "a3/a3_candidate.pdf, .md, .html, .json; a5/candidate/ |"]
    elif cand_error:
        readme[-1:-1] = [f"| A3 and A5 CANDIDATE: NOT PRODUCED ({cand_error.replace('|', '/')[:200]}) | "
                         "a3/a3_candidate_FAILED.md |"]
    readme += ["## Checks", "", "| Check | Result | Detail |", "|---|---|---|"]
    readme += [f"| {c['id']} | {'pass' if c['ok'] else 'FAIL'} | {c['detail'].replace('|', '/')} |" for c in checks]
    readme += [f"| {c['id']}{(' ' + c['stage']) if c.get('stage') else ''} | {'ok' if c['ok'] else 'REPORTED'} | "
               f"{c['detail'].replace('|', '/')} |" for c in rep]
    write_text(out / "README.md", "\n".join(readme) + "\n")
    return {"status": status, "checks": checks, "reported": rep, "a3_fit": a3_fit, "issues": issues, "a1": a1d, "a2": a2d,
            "a3": a3d, "a5": progs, "release": release, "blockers": blockers,
            "candidate": [p.relative_to(out).as_posix() for p in cand_files], "candidate_error": cand_error}


def a4_work_log_row(root: Path) -> str:
    """The outputs index's A4 row (session 13, audit R3-4): A4 is the work log in the repository's worklog/ (the
    session logs, the error index, the model calls, the subagent briefs) and the commit history; each part is named as
    it is found under `root`, and one that is absent is said to be absent (never implied)."""
    wl = Path(root) / "worklog"
    parts = [("the session logs (worklog/<date>_session-NN_*.md)", any(wl.glob("*_session-*.md"))),
             ("the work log index (worklog/README.md)", (wl / "README.md").is_file()),
             ("the note of every place the system was wrong (worklog/ERROR_INDEX.md)", (wl / "ERROR_INDEX.md").is_file()),
             ("the prompts and model calls (worklog/model_calls/)", (wl / "model_calls").is_dir()),
             ("the subagent briefs (worklog/subagent_briefs/)", (wl / "subagent_briefs").is_dir())]
    have = [k for k, ok in parts if ok]
    gone = [k for k, ok in parts if not ok]
    return ("| A4 work log: " + "; ".join(have or ["no worklog/ folder in this repository"])
            + (f"; not present: {'; '.join(gone)}" if have and gone else "")
            + "; and the commit history (`git log`) | worklog/ at the repository root (not under out/); `git log` |")


def readings_status_sentence(cov: dict) -> str:
    """What the outputs say about the image readings' review status, taken from the evidence build's coverage
    (`reading_status` per region comes from curation/approvals.yaml at ingest time), never from a fixed sentence."""
    regs = [r for r in cov.get("regions", []) if r.get("kind") == "image" and r.get("reading_status")]
    if not regs:
        return "There are no image readings in this pack."
    approved = [r["id"] for r in regs if r.get("reading_status") == "approved"]
    pending = [r["id"] for r in regs if r.get("reading_status") != "approved"]
    parts = []
    if approved:
        parts.append(f"image readings approved by a named reviewer: {', '.join(approved)} (see build/coverage.md)")
    if pending:
        parts.append(f"image readings PENDING HUMAN REVIEW: {', '.join(pending)}")
    return "; ".join(parts) + "."


def build(evidence_dir: Path, out: Path, pack_path: Path, root: Path, quiet: bool = False, strict: bool = False,
          op_status: dict | None = None) -> dict:
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
                                           ("activity_templates", "curation/activity_templates.yaml"))] + \
        [relationships.default_path(cfg, root)]
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
        res = write(r, tmp, op_status=op_status)          # op_status: shown beside the candidate's ops (session 11)
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
    without a deliverable, unlinked consequence words (C15), quotes lost to a deletion of words from a unit that
    stays in force (deleted_words: re-make the reading or mark it `removed`) and the relationships file (session 10:
    quotes, targets, statuses). Used by check-register (exit 1) and by the release gate (each kind other than quotes,
    which C16 already checks structurally, is a coverage blocker)."""
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
        out_cls = sorted({i.consequence.cls for i in row.interpretations if isinstance(i.consequence, Consequence)
                          and i.consequence.cls in BID_OUT})
        if out_cls and row.assessment not in ("pass_fail", "scored"):   # session 11 audit (A1-10)
            out.append({"kind": "assessment", "where": row.id,
                        "detail": f"assessment '{row.assessment}', but a breach puts the Proposal out "
                                  f"({', '.join(out_cls)}): pass_fail (ASSESSMENT_WORDS)"})
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
                if not basis_found(b, units, r["stages"][-1].state):
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
                           cutoff=clarify.effective_cutoff(r),            # the effective cut-off (session 09)
                           state=(r["stages"][-1].state if r.get("stages") else None),   # session 12: amended words
                           row_ids={e["row"].id for e in r["evals"]}):    # session 13 (F2; R2-7): curated rows exist
        out.append({"kind": "clarification", "where": p.split(":")[0], "detail": p})
    for p in relationship_findings(r):                                    # session 10: every quote, target and status
        out.append({"kind": "relationship", "where": p.split(":")[0], "detail": p})
    from .signals import issue_ref_findings                               # session 12: issue ids must exist
    out += issue_ref_findings(r["rowfile"].rows, r.get("templates") or {}, r.get("clarifications") or {},
                              set(r["curated_issues"]), r.get("opfiles") or [])
    out += pending_wording_findings(r)                                     # session 13 (audit R1-3)
    return out


def relationship_findings(r: dict) -> list[str]:
    """relationships.validate over the pack's relationships file, against its units (and the units ops made), rows,
    activity templates, evidence items and issues."""
    if not r.get("relationships"):
        return []
    return relationships.validate(r["relationships"], r["units"], r["rowfile"].rows, r.get("templates") or {},
                                  evidence_items=r.get("evidence_items") or {}, issues=set(r["curated_issues"]),
                                  known_units=set(r["stages"][-1].state))


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


def basis_found(b: dict, units: dict, state: dict) -> bool:
    """A quoted basis {unit, page, words} is found: the words in the unit's text, on one of its pages. A unit an addendum
    inserted (VOL-II:5.5+ADD-03) is not in the evidence build; it is printed in the addendum, so its text and pages are
    the inserted unit's in the state, i.e. the inserting provision's pages (session 12, blind-05 follow-up 13)."""
    u = units.get(b.get("unit"))
    if u is not None:
        text, pages = u.get("text", ""), u.get("pages", [])
    else:
        su = state.get(b.get("unit"))
        if su is None or su.origin != "addendum_op":
            return False
        text, pages = su.text or "", list(su.pages or [])
    return found(b.get("words", ""), text) and b.get("page") in pages


def pending_wording_findings(r: dict) -> list[dict]:
    """Session 13 (audit R1-3): an issue labelled HUMAN DECISION PENDING (signals.pending_issues) whose own words settle
    one of its limbs (human_owned.settled_wording: 'is not treated as', 'is read as', 'means', 'therefore', ...) is
    reported for a person (check-register, kind `pending_settled`). Report only: the wording is a person's to change."""
    out = []
    pend = r.get("pending_issues")
    if pend is None:
        pend = signals.pending_issues(r)
    for iid, it in (r.get("curated_issues") or {}).items():
        if iid not in pend:
            continue
        hit = human_owned.settled_wording(it)
        if hit:
            out.append({"kind": "pending_settled", "where": iid,
                        "detail": f"labelled {human_owned.HUMAN_DECISION_PENDING}, yet its own words settle a limb of it "
                                  f"({', '.join(hit)}): reword it as open (the proposed reading, 'not decided', and who "
                                  "decides) or record a person's decision"})
    return out


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
    intro = [e["stages"][r["order"][0]].get("introduction") or {} for e in rows]       # session 11 (register.py)
    print(f"row introduction: {sum(1 for x in intro if x.get('explicit'))} explicit (`introduced`, supported), "
          f"{sum(1 for x in intro if not x.get('explicit'))} derived from the row's primary unit")
    c14 = [h for h in r["sweeps"][0] if not doc or mine(h["unit"])]
    if c14:
        print(f"C14 (for a person to confirm; not a failure): {len(c14)} obligation words in non-requirement units")
    for f in found:
        print(f"  [{f['kind']}] {f['where']}: {f['detail']}")
    return 1 if found else 0
