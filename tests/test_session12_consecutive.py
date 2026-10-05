"""Session 12 (W5): consecutive addenda through the AI workflow (`tenderpack ai run ADD-04 --pdf ... --base-run RUN`).

Before this, `ai run ADD-04` ran on the real curation, where ADD-03 is unknown: ADD-04's references to units ADD-03
introduced could not resolve, and the session-11 consecutive test (test_session11_downstream.py, test_b_... two-stage
promote) covered only the promote step inside one candidate. Here, failing first:

  chain      a recorded ADD-03 run (synthetic Addendum No. 3: inserts Volume I Clause 6.8, amends Clause 7.1), then an
             ADD-04 run with --base-run on it (synthetic Addendum No. 4: amends the Clause 6.8 ADD-03 inserted, reverses
             ADD-03's change to Clause 7.1, amends base Clause 6.1). The ADD-04 candidate starts from the ADD-03
             candidate (its op file, rows, pack with ADD-03's PDF and its evidence build; ADD-03 is ws.prev_stage), the
             candidate build's A2 shows ADD-03 -> ADD-04, the register carries the ADD-03 row at both stages with the
             ADD-04 change, the unresolved list is honest, the diff and out-before compare with the ADD-03 state.
  isolation  the base run's folder is byte-identical after the ADD-04 run; the real curation is untouched.
  names      run-status, the checkpoint settings, the review packet and the candidate README name the base run.
  gap        without --base-run, the ADD-04 provision citing ADD-03's clause is unresolved with the reason
             "ADD-03 is not in this state; run it first or pass --base-run".
  refusals   a base that has not reached promotion, a base being driven (live run lock), --pack with --base-run.
  stale      a base changed after the ADD-04 sets were validated: the sets are STALE (base_candidate_sha256) and
             promotion refuses; the out-before cache key follows the base.
  resume     `resume --base-run` with the recorded base continues; another base is refused.

The addenda are SYNTHETIC (tests/fixtures/s12_consecutive.py, built like make_drill.py's; not tender content), the
cassettes are hand-written recorded fixtures written here (no live call is made and none is implied). Everything is
written into pytest's disposable folders; nothing under the repository."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path

import pytest
import yaml

import s12_consecutive as F
from ai_fixture import ROOT
from tenderpack.ai import budget as B
from tenderpack.ai import candidate as CAND
from tenderpack.ai import workflow as W

quiet = lambda *a, **k: None  # noqa: E731
CAPS = {"name": "s12-consecutive", "model": "recorded-fixture-model",
        "capabilities": {"images": False, "tools": True, "structured_output": False, "context_tokens": 400000,
                         "retention": "recorded fixture: nothing leaves the process",
                         "source": "cassette (recorded fixture)"}}
ST = "${state}"


def _ev(doc, unit, words, page=1):
    return {"doc": doc, "unit_id": unit, "page": page, "kind": "span", "words": words}


def _no_effect(add, prov, reason, words):
    return {"id": f"{add}/{prov}", "state": ST, "statement_type": "disposition", "provision": f"{add}:{prov}",
            "payload": {"provision": f"{add}:{prov}", "disposition": "no_effect", "reason": reason},
            "evidence": [_ev(add, f"{add}:{prov}", words)]}


def _op(add, prov, target, old, new, words, prev, val):
    return {"id": f"{add}/{prov}", "state": ST, "statement_type": "amendment_op", "provision": f"{add}:{prov}",
            "target": target, "payload": {"id": f"{add}/{prov}", "provision": f"{add}:{prov}", "type": "replace_text",
                                          "target": target, "old": old, "new": new},
            "previous_value": prev, "proposed_value": val, "evidence": [_ev(add, f"{add}:{prov}", words)]}


def _covers(add, front_words, issued):
    return [_no_effect(add, "cover/para1", "the addendum's issue date line (the stage date)", issued),
            _no_effect(add, "cover/para2", "the tender reference on the cover", "Tender NUPA/ISTP/2026/014"),
            _no_effect(add, "cover/para3", "the cover summary of the sections below; the sections themselves make the "
                                           "changes", front_words)]


ROW_68 = {"id": "ADD-03-6.8-01", "group": "ADD-03:1.1", "scope": ["bid_submission", "delivery", "new_in_addendum"],
          "requirement": "Register through the Portal the names of up to two representatives who will deliver the Proposal",
          "units": ["VOL-I:6.7+ADD-03", "ADD-03:1.1"], "discipline": "Bid management", "owner": "Bid manager",
          "assessment": "pass_fail", "evidence": ["EV-DELIVERY"],
          "interpretations": [{"stage": "ADD-03", "parameters": {"representatives_max": 2},
                               "quote": "register through the Portal the names of not more than two (2) representatives "
                                        "who will deliver its Proposal"}],
          "introduced": {"stage": "ADD-03", "by": "ADD-03/1.1",
                         "evidence": {"unit": "ADD-03:1.1", "page": 1,
                                      "words": "The following new Clause 6.8 is inserted in Volume I after Clause 6.7"}},
          "confidence": "high", "confidence_reason": "verbatim inserted clause", "issues": ["I-NO-CONSEQUENCE"]}


def _session(phase, when, add, items, contains):
    body = json.dumps({"addendum": add, "state": "STATE", "statements": [], "items": items}, ensure_ascii=False)
    body = body.replace('"STATE"', ST).replace('"${state}"', ST)
    return {"phase": phase, "when": when,
            "turns": [{"match": {"last_role": "user", "contains": ["TASK PACKET"] + contains},
                       "response": {"usage": {"input_tokens": 9000, "output_tokens": 900}, "text": body}}]}


def cassette_03() -> dict:
    items = _covers("ADD-03", "This Addendum inserts a new Clause 6.8 in Volume I", "Issued 5 November 2026") + [
        {"id": "ADD-03/1.1", "state": ST, "statement_type": "amendment_op", "provision": "ADD-03:1.1", "target": "VOL-I:6.7",
         "payload": {"id": "ADD-03/1.1", "provision": "ADD-03:1.1", "type": "insert_unit", "anchor": "VOL-I:6.7",
                     "new_text": F.NEW_68, "note": "new Clause 6.8 inserted after Clause 6.7"},
         "evidence": [_ev("ADD-03", "ADD-03:1.1", "The following new Clause 6.8 is inserted in Volume I after Clause 6.7")]},
        _op("ADD-03", "2.1", "VOL-I:7.1", "one hundred and fifty (150) days", "one hundred and eighty (180) days",
            "‘one hundred and fifty (150) days’ is deleted", "150", "180")]
    down = [{"id": "D1", "state": ST, "statement_type": "row_new", "task": "c46:ADD-03/1.1", "provision": "ADD-03:1.1",
             "target": "VOL-I:6.7+ADD-03", "payload": {"row": ROW_68},
             "evidence": [_ev("VOL-I", "VOL-I:6.7+ADD-03", "register through the Portal the names of not more than two "
                                                         "(2) representatives who will deliver its Proposal")]}]
    return dict(CAPS, sessions=[_session("analysis", {"provisions_include": ["ADD-03:1.1", "ADD-03:2.1"]}, "ADD-03",
                                         items, ["ADD-03:1.1"]),
                                _session("downstream", {"tasks_include": ["c46:ADD-03/1.1"]}, "ADD-03", down,
                                         ["propose_downstream"])])


def cassette_04() -> dict:
    """The same answer whether or not the state holds ADD-03 (what a model reading ADD-04 alone would propose): 1.1
    names the clause ADD-03 inserted."""
    items = _covers("ADD-04", "This Addendum amends Volume I Clause 6.8 as inserted by Addendum No. 3",
                    "Issued 19 November 2026") + [
        _op("ADD-04", "1.1", "VOL-I:6.7+ADD-03", "two (2) representatives", "three (3) representatives",
            "‘two (2) representatives’ is deleted", "2", "3"),
        _op("ADD-04", "2.1", "VOL-I:7.1", "one hundred and eighty (180) days", "one hundred and fifty (150) days",
            "‘one hundred and eighty (180) days’ is deleted", "180", "150"),
        _op("ADD-04", "3.1", "VOL-I:6.1", "14:00 hours Riyadh time", "11:00 hours Riyadh time",
            "‘14:00 hours Riyadh time’ is deleted", "14:00", "11:00")]
    down = [{"id": "D1", "state": ST, "statement_type": "row_reading", "task": "row:ADD-03-6.8-01", "provision": "ADD-04:1.1",
             "target": "ADD-03-6.8-01",
             "payload": {"row": "ADD-03-6.8-01",
                         "interpretation": {"stage": "ADD-04", "parameters": {"representatives_max": 3},
                                            "quote": "register through the Portal the names of not more than three (3) "
                                                     "representatives who will deliver its Proposal",
                                            "note": "ADD-04 1.1 amends the Clause 6.8 that ADD-03 1.1 inserted"},
                         "replace_requirement": {"old": ROW_68["requirement"],
                                                 "new": "Register through the Portal the names of up to three "
                                                        "representatives who will deliver the Proposal"}},
             "evidence": [_ev("VOL-I", "VOL-I:6.7+ADD-03", "register through the Portal the names of not more than three "
                                                         "(3) representatives who will deliver its Proposal"),
                          _ev("ADD-04", "ADD-04:1.1", "‘three (3) representatives’ is substituted")]}]
    return dict(CAPS, sessions=[_session("analysis", {"provisions_include": ["ADD-04:1.1", "ADD-04:3.1"]}, "ADD-04",
                                         items, ["ADD-04:1.1"]),
                                _session("downstream", {"tasks_include": ["row:ADD-03-6.8-01"]}, "ADD-04", down,
                                         ["propose_downstream"])])


# ---------------------------------------------------------------------------------------------- fixtures

@pytest.fixture(scope="module")
def prev_build(tmp_path_factory):
    """The preceding state's evidence build (the real pack as received), ingested into a disposable folder."""
    from tenderpack.cli import ingest
    out = tmp_path_factory.mktemp("s12c-prev") / "build"
    assert ingest(ROOT / "config/pack.yaml", out, ROOT, quiet=True)["exit_code"] == 0
    return out


@pytest.fixture(scope="module")
def area(tmp_path_factory):
    d = tmp_path_factory.mktemp("s12c")
    pdfs = d / "pdfs"
    pdfs.mkdir()
    out = {"staging": d / "staging", "worklog": d / "worklog", "pdf03": F.make("ADD-03", pdfs),
           "pdf04": F.make("ADD-04", pdfs)}
    for name, fn in (("c03", cassette_03), ("c04", cassette_04)):
        out[name] = d / f"{name}.yaml"
        out[name].write_text(yaml.safe_dump(fn(), allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    return out


KW = dict(route="recorded", batch_size=8, downstream_batch_size=60, background_before=False, echo=quiet,
          sleep=lambda s: None, caps={"max_tokens_per_call": 120000})


def run03(prev_build, area, run_id, **kw):
    return W.start("ADD-03", area["pdf03"], pack=ROOT / "config/pack.yaml", evidence=prev_build, staging=area["staging"],
                   worklog=area["worklog"], run_id=run_id, cassette=area["c03"], **KW, **kw)


def run04(area, run_id, **kw):
    return W.start("ADD-04", area["pdf04"], staging=area["staging"], worklog=area["worklog"], run_id=run_id,
                   cassette=area["c04"], **KW, **kw)


def tree_hash(d: Path) -> dict[str, str]:
    return {f.relative_to(d).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in sorted(Path(d).rglob("*")) if f.is_file()}


def _yaml(p):
    return yaml.safe_load(Path(p).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def chain(prev_build, area):
    r3 = run03(prev_build, area, "c03")
    base_dir = Path(r3["run_dir"])
    before = tree_hash(base_dir)
    real_before = CAND.fingerprint(ROOT / "config/pack.yaml")
    r4 = run04(area, "c04", base_run="c03")
    return {"r3": r3, "r4": r4, "base_dir": base_dir, "before": before, "after": tree_hash(base_dir),
            "real_before": real_before, "dir": Path(r4["run_dir"]),
            "cp": W.load("c04", area["staging"]).data, "cp3": W.load("c03", area["staging"]).data}


# ---------------------------------------------------------------------------------------------- the chain

def test_the_base_run_reaches_its_candidate_build(chain):
    cp3 = chain["cp3"]
    assert cp3["steps"]["promotion"]["status"] == "done" and cp3["steps"]["outputs"]["exit_code"] == 0, cp3["status_reason"]
    assert "ADD-03-6.8-01" in cp3["steps"]["promotion"]["rows_new"]


def test_the_add04_candidate_starts_from_the_base_candidate(chain, area):
    cp, d = chain["cp"], chain["dir"]
    b = cp["settings"]["base_run"]
    assert b["run_id"] == "c03" and b["addendum"] == "ADD-03" and b["chain"] == ["ADD-03"]
    pack = _yaml(d / "candidate/pack.yaml")
    docs = {x["doc_id"]: x for x in pack["documents"]}
    assert list(docs)[-2:] == ["ADD-03", "ADD-04"]
    # the base addendum's PDF is a copy in THIS run's candidate (same bytes), never read from the base run in place
    p03 = CAND.resolve(docs["ADD-03"]["path"])
    assert p03.is_relative_to(d / "candidate/input")
    assert p03.read_bytes() == Path(area["pdf03"]).read_bytes()
    assert pack["base_run"]["run_id"] == "c03"
    # the base candidate's curation as promoted: ADD-03's op file and the AI row file
    assert (Path(pack["amendments_dir"]) / "ADD-03.yaml").is_file()
    assert (Path(pack["register"]).parent / "rows/ADD-03-ai.yaml").is_file()
    ctx = W.Ctx(W.load("c04", area["staging"]), quiet)
    assert ctx.ws.prev_stage("ADD-04") == "ADD-03"
    st = ctx.ws.identity()
    assert st.base_run == "c03" and st.base_candidate_sha256 == b["fingerprint"]
    assert cp["out_before"]["status"] == "done"
    assert Path(cp["settings"]["evidence"]) == chain["base_dir"] / "candidate/build"


def test_the_ops_of_add04_resolve_against_add03(chain):
    prom = chain["cp"]["steps"]["promotion"]
    assert set(prom["ops"]) >= {"ADD-04/1.1", "ADD-04/2.1", "ADD-04/3.1"}, prom
    assert prom["unresolved"] == [], prom["unresolved"]
    assert prom["readings"] == ["ADD-03-6.8-01"], prom


def test_the_candidate_build_shows_the_chain_and_the_row_at_both_stages(chain):
    cp, d = chain["cp"], chain["dir"]
    assert cp["steps"]["outputs"]["exit_code"] == 0 and not cp["steps"]["outputs"]["refused"], cp["steps"]["outputs"]
    out = d / "candidate/out"
    a2 = (out / "a2/a2.md").read_text(encoding="utf-8")
    heads = [x for x in a2.splitlines() if x.startswith("## ADD-")]
    assert [h.split()[1] for h in heads] == ["ADD-01", "ADD-02", "ADD-03", "ADD-04"], heads
    assert heads[2].endswith("APPLIED") and heads[3].endswith("APPLIED"), heads
    # the ADD-03 row moves at both stages: NEW at ADD-03 (in the ADD-03 section), AMENDED by ADD-04/1.1 at ADD-04
    sec03, sec04 = a2[a2.index(heads[2]):a2.index(heads[3])], a2[a2.index(heads[3]):]
    assert "| ADD-03-6.8-01 | NOT IN FORCE (introduced at ADD-03 by ADD-03/1.1) | NEW (introduced by ADD-03/1.1) |" in sec03
    assert "| ADD-03-6.8-01 | NEW (introduced by ADD-03/1.1) | AMENDED (ADD-04/1.1) |" in sec04
    chain_line = next(x for x in a2.splitlines() if x.startswith("- **ADD-03-6.8-01**:"))
    assert chain_line.index("ADD-04/1.1") < chain_line.index("ADD-03/1.1") < chain_line.index("VOL-I:6.7+ADD-03")
    a1 = json.loads((out / "a1/a1.json").read_text(encoding="utf-8"))
    row = {r["id"]: r for r in a1["rows"]}["ADD-03-6.8-01"]
    assert row["status:ADD-03"] == "NEW (introduced by ADD-03/1.1)", row["status:ADD-03"]
    assert row["status:ADD-04"] == "AMENDED (ADD-04/1.1)", row["status:ADD-04"]
    assert row["requirement"].startswith("Register through the Portal the names of up to three"), row["requirement"]
    assert row["status:BASE"].startswith("NOT IN FORCE")
    # the diff compares ADD-03 -> ADD-04 and out-before is the ADD-03 candidate state (the row is not new there)
    assert cp["steps"]["diff"]["stage"] == "ADD-03 -> ADD-04" and cp["steps"]["diff"]["base_run"] == "c03"
    cmp_ = json.loads((d / "review/outputs-before-after.json").read_text(encoding="utf-8"))
    assert "ADD-03-6.8-01" not in cmp_["a1"]["new"], cmp_["a1"]
    before = json.loads((d / "candidate/out-before/a1/a1.json").read_text(encoding="utf-8"))
    assert "ADD-03-6.8-01" in {r["id"] for r in before["rows"]}


def test_the_unresolved_list_is_honest(chain):
    cp = chain["cp"]
    comp = cp["completeness"]
    # every provision is answered; what is not complete is listed with its reason (downstream tasks left unanswered)
    assert chain["r4"]["status"] in ("partial", "complete")
    if chain["r4"]["status"] == "partial":
        assert comp["reasons"], comp
        assert not any("provision(s) unresolved" in x for x in comp["reasons"]), comp["reasons"]
    assert cp["approval"]["status"] == "none"


def test_the_base_run_folder_is_byte_identical_and_the_real_curation_untouched(chain):
    assert chain["after"] == chain["before"], sorted(k for k in set(chain["after"]) | set(chain["before"])
                                                     if chain["after"].get(k) != chain["before"].get(k))[:10]
    assert CAND.fingerprint(ROOT / "config/pack.yaml") == chain["real_before"]


def test_run_status_settings_review_and_readme_name_the_base(chain, area):
    cp, d = chain["cp"], chain["dir"]
    s = W.summary(W.load("c04", area["staging"]))
    assert s["base_run"]["run_id"] == "c03" and s["base_run"]["chain"] == ["ADD-03"]
    md = (d / "review/index.md").read_text(encoding="utf-8")
    assert "**Base run** `c03`" in md and "ADD-03 -> ADD-04" in md
    assert "base run c03's candidate state" in md
    for name in ("README.md", "CANDIDATE.md"):
        t = (d / "candidate/out" / name).read_text(encoding="utf-8")
        assert "**Base run** `c03`" in t, name
    assert "base run c03" in (d / "candidate/pack.yaml").read_text(encoding="utf-8").splitlines()[0]


# ---------------------------------------------------------------------------------------------- the gap

def test_without_base_run_the_citing_provision_is_unresolved_with_the_reason(prev_build, area):
    res = W.start("ADD-04", area["pdf04"], pack=ROOT / "config/pack.yaml", evidence=prev_build, staging=area["staging"],
                  worklog=area["worklog"], run_id="gap04", cassette=area["c04"], stop_after="promotion", **KW)
    cp = W.load("gap04", area["staging"]).data
    assert cp["settings"]["missing_addenda"] == ["ADD-03"] and res.get("missing_addenda") == ["ADD-03"]
    prom = cp["steps"]["promotion"]
    assert "ADD-04:1.1" in prom["unresolved"], prom
    op = _yaml(Path(cp["candidate"]["dir"]) / "curation/amendments/ADD-04.yaml")
    text = json.dumps(op, ensure_ascii=False)
    assert "ADD-03 is not in this state; run it first or pass --base-run" in text, text[:2000]
    # the base clause ADD-04 amends is not held back by the gap
    assert "ADD-04/3.1" in prom["ops"]


# ---------------------------------------------------------------------------------------------- refusals

def test_a_base_that_has_not_reached_promotion_is_refused(prev_build, area):
    run03(prev_build, area, "c03-early", stop_after="validation")
    with pytest.raises(CAND.CandidateError, match="has not reached promotion"):
        run04(area, "c04-early", base_run="c03-early")
    assert not (area["staging"] / "runs/c04-early").exists()


def test_a_running_base_and_pack_with_base_are_refused(chain, area):
    live = area["staging"] / "runs/c03-live"
    shutil.copytree(chain["base_dir"], live, ignore=shutil.ignore_patterns("candidate"))
    import socket
    (live / "run.lock").write_text(json.dumps({"pid": os.getpid(), "host": socket.gethostname(), "created": "now",
                                               "token": "x"}), encoding="utf-8")
    with pytest.raises(CAND.CandidateError, match="being driven now"):
        run04(area, "c04-live", base_run="c03-live")
    with pytest.raises(B.Refused, match="do not pass --pack or --evidence"):
        run04(area, "c04-pack", base_run="c03", pack=ROOT / "config/pack.yaml")


# ---------------------------------------------------------------------------------------------- stale, resume

def test_resume_with_the_base_and_stale_on_a_changed_base(prev_build, area):
    run03(prev_build, area, "s03", stop_after="promotion")
    r = run04(area, "s04", base_run="s03", stop_after="validation")
    assert r["status"] == "stopped", r
    # resume --base-run: the recorded base continues; another base is refused
    with pytest.raises(B.Refused, match="was started on base run s03"):
        W.resume("s04", area["staging"], base_run="c03", echo=quiet, sleep=lambda s: None)
    r = W.resume("s04", area["staging"], base_run="s03", stop_after="downstream_validation", echo=quiet,
                 sleep=lambda s: None)
    assert r["status"] == "stopped" and "stopped after downstream_validation" in r["status_reason"], r
    d = Path(r["run_dir"])
    key_before = CAND.before_key(d, Path(W.load("s04", area["staging"]).data["settings"]["evidence"]))
    # the base changes (a person edits the base candidate's AI rows) after the ADD-04 sets were validated
    base_pack = _yaml(area["staging"] / "runs/s03/candidate/pack.yaml")
    rows = Path(base_pack["register"]).parent / "rows/ADD-03-ai.yaml"
    rows.write_text(rows.read_text(encoding="utf-8").replace("up to two representatives", "up to 2 representatives"),
                    encoding="utf-8")
    assert CAND.before_key(d, Path(W.load("s04", area["staging"]).data["settings"]["evidence"])) != key_before
    r = W.resume("s04", area["staging"], stop_after="promotion", echo=quiet, sleep=lambda s: None)
    cp = W.load("s04", area["staging"]).data
    assert r["status"] == "stopped" and "promotion refused" in r["status_reason"], r["status_reason"]
    assert "STALE" in r["status_reason"] and "base_candidate_sha256" in r["status_reason"], r["status_reason"]
    assert any(e.get("event") == "base_checked" and e.get("changed_since_start") for e in cp["events"]), cp["events"][-5:]
    assert not (d / "promotion.json").exists()
