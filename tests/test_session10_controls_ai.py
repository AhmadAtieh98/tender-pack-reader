"""Session 10, two control findings from the owner's review of the AI layer, each reproduced by a regression first.

1a  A `no_effect` disposition (or another "no change" answer) on a provision whose own words amend, oblige or except
    must not verify: real amendments may not disappear through it. Coverage (every provision accounted for), evidence
    verification (quotations verbatim at the stated place), semantic resolution (the answer is consistent with what the
    provision's own words do) and approval (a named person's decision, never assigned by the controller) are reported
    apart.
1c  The state identity binds the inputs that decide a proposal and a calculation (assumptions: calendar, holidays,
    counting policy; activity templates; readings and approvals; the amendment files; the evidence build), a
    calculation carries the fingerprint of the inputs it was computed under, an evidence read verifies the file against
    the evidence build's record, a Workspace whose inputs changed since loading refuses ("workspace stale: reload"),
    and submit/promote recheck freshness.

The real pack (its committed evidence build, build/) is read where it is; everything a test changes is a disposable
copy under pytest's tmp_path (curation/, config/assumptions.yaml and, where a crop is replaced, the evidence build).
Offline: no provider is called and nothing is sent anywhere. No decision is recorded anywhere; promotion goes to
disposable folders under the reviewer name "Fixture Test Reviewer"."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
import yaml

from tenderpack.ai import controller
from tenderpack.ai.contract import ChangeProposal, EvidenceRef, ProposalSet
from tenderpack.ai.tools import ToolError, Workspace, call_tool, get_crop, get_unit
from tenderpack.util import ROOT

BUILD = ROOT / "build"
REVIEWER = "Fixture Test Reviewer"
UNITS = {u["unit_id"]: u for u in json.loads((BUILD / "units.json").read_text(encoding="utf-8"))["units"]}

# the curated inputs a pack names (defaults relative to the repository); the copy names each by absolute path
_CURATED = {"register": "curation/register/rows.yaml", "issues": "curation/register/issues.yaml",
            "row_ids": "curation/register/ids.yaml", "dispositions_dir": "curation/register/dispositions",
            "evidence_items_dir": "curation/evidence_items", "amendments_dir": "curation/amendments",
            "clarifications": "curation/clarifications/register.yaml", "approvals": "curation/approvals.yaml",
            "readings_dir": "curation/readings", "activity_templates": "curation/activity_templates.yaml",
            "decisions": "curation/reviews/decisions.yaml", "assumptions": "config/assumptions.yaml"}


def hermetic_workspace(d: Path, copy_build: bool = False) -> Workspace:
    """The real pack over disposable copies of curation/ and config/assumptions.yaml (and, with copy_build, of the
    evidence build), so a test may change an input and other work on the repository cannot change it under the test."""
    d = Path(d)
    shutil.copytree(ROOT / "curation", d / "curation", ignore=shutil.ignore_patterns("reviews"))
    (d / "config").mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "config/assumptions.yaml", d / "config/assumptions.yaml")
    cfg = yaml.safe_load((ROOT / "config/pack.yaml").read_text(encoding="utf-8"))
    for k, rel in _CURATED.items():
        cfg[k] = str(d / rel)
    (d / "pack.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    evidence = BUILD
    if copy_build:
        evidence = d / "build"
        shutil.copytree(BUILD, evidence)
    return Workspace(evidence, d / "pack.yaml", ROOT, d / "staging", d / "worklog", ROOT / "config/ai.yaml")


def _ref(p: str, words: str | None = None) -> EvidenceRef:
    u = UNITS[p]
    return EvidenceRef(doc=u["doc"], unit_id=p, page=u["pages"][0], kind="span", words=words or u["text"])


def _disposition(ws, p: str, reason: str, disposition: str = "no_effect") -> ChangeProposal:
    return ChangeProposal(id=f"{p.split(':')[0]}/{p.split(':', 1)[1]}", state=ws.identity(), statement_type="disposition",
                          provision=p, payload={"disposition": disposition, "reason": reason}, evidence=[_ref(p)])


def _set(ws, addendum: str, items: list[ChangeProposal]) -> ProposalSet:
    return ProposalSet(run_id="s10-test", created="2026-10-04T00:00:00Z", route="host", provider="host",
                       model_requested="fixture", task=controller.TASK, addendum=addendum, state=ws.identity(),
                       items=items)


def _quote(p: str, n: int = 8) -> str:
    return " ".join(UNITS[p]["text"].split()[:n])


@pytest.fixture(scope="module")
def real(tmp_path_factory):
    return hermetic_workspace(tmp_path_factory.mktemp("s10-real"))


# ---------------------------------------------------------------------------------------------- finding 1a

# the provisions of ADD-02 that print a substitution, deletion, insertion, reissue, reinstatement or revocation the
# pattern drafter (tenderpack.draft) itself drafts as an op
SUBSTITUTIONS = {"ADD-02:2.1": "replace_text", "ADD-02:3.1": "replace_unit", "ADD-02:4.1": "replace_text",
                 "ADD-02:5.1": "set_value", "ADD-02:7.1": "insert_unit", "ADD-02:8.1": "replace_text",
                 "ADD-02:9.1": "set_status", "ADD-02:9.2": "set_status"}
# provisions whose words oblige, except or amend without a drafted change op (or that are the content of a reissue)
AMENDMENT_LANGUAGE = ["ADD-02:cover/para3", "ADD-02:T1-1-rev/A", "ADD-02:T1-1-rev/note(2)", "ADD-02:5.2", "ADD-02:Q9",
                      "ADD-02:7.2", "ADD-02:F4-G/T1/1"]


def test_forty_no_effect_dispositions_on_add02_neither_verify_nor_complete(real):
    """Owner's finding 1a. Before the fix (session 09 controller) this set was `complete`, all 40 items
    `evidence_verified`, and the simulation APPLIED with no unit changed: ADD-02's amendments disappeared."""
    provs = controller._provisions(real, "ADD-02")
    assert len(provs) == 40
    ps = _set(real, "ADD-02", [_disposition(real, p, "no change") for p in provs])
    rep = controller.validate_set(real, ps)
    st = {it.provision: it.verification_status for it in ps.items}
    assert ps.status != "complete", (ps.status, st)
    assert {p for p, s in st.items() if s == "invalid"} == set(SUBSTITUTIONS)
    by = {it.provision: it for it in ps.items}
    for p, kind in SUBSTITUTIONS.items():
        sem = [v for v in by[p].validation if v.check == "semantic"]
        assert sem and not sem[0].ok and "contradicts" in sem[0].detail and kind in sem[0].detail, sem
        assert sem[0].aspect == "semantic"
        ev = [v for v in by[p].validation if v.check.startswith("evidence")]
        assert ev and all(v.ok and v.aspect == "evidence" for v in ev)       # the quotation itself is genuine
    for p in AMENDMENT_LANGUAGE:                     # unsupported "no change" on amendment language: not verified
        assert st[p] == "insufficient_evidence", (p, st[p], by[p].validation)
        assert any(v.check == "semantic" and not v.ok and "amendment language" in v.detail for v in by[p].validation)
    for it in ps.items:                              # what still verifies is what carries no amendment language
        if it.verification_status == "evidence_verified":
            assert any(v.check == "semantic" and v.ok and "no amendment language" in v.detail for v in it.validation)
    res = ps.resolution
    assert res.provisions_total == 40 and res.invalid == 8 and res.approved == 0
    assert res.resolved == sum(1 for s in st.values() if s == "evidence_verified")
    assert res.resolved + res.pending + res.invalid + res.unaccounted == 40 and res.pending >= len(AMENDMENT_LANGUAGE)
    assert set(SUBSTITUTIONS) | set(AMENDMENT_LANGUAGE) <= set(res.no_change_on_amendment_language)
    assert ps.coverage.accounted == 32 and set(ps.coverage.unaccounted) == set(SUBSTITUTIONS)
    sim = rep["simulation"]
    assert sim["clean"] is False and sim["status"] != "APPLIED"
    n = len(res.no_change_on_amendment_language)
    assert any(f"{n} provisions with amendment language carry no change" in x for x in sim["findings"]), sim["findings"]
    assert rep["impact"]["addendum_status_if_applied"] != "APPLIED" and rep["impact"]["findings"]
    md = controller.review_markdown(ps, rep)
    assert "carry no change" in md and "resolution" in md.lower() and "never assigned" in md


def test_a_reason_that_quotes_the_provision_is_pending_and_a_substitution_stays_invalid(real):
    picks = ["ADD-02:5.2", "ADD-02:7.2", "ADD-02:Q9", "ADD-02:T1-1-rev/note(2)", "ADD-02:2.1"]
    items = [_disposition(real, p, f"no change: the provision reads ‘{_quote(p)}’ and the clause it cites stands")
             for p in picks]
    ps = _set(real, "ADD-02", items)
    controller.validate_set(real, ps)
    st = {it.provision: it.verification_status for it in ps.items}
    assert st == {"ADD-02:5.2": "interpretation_pending", "ADD-02:7.2": "interpretation_pending",
                  "ADD-02:Q9": "interpretation_pending", "ADD-02:T1-1-rev/note(2)": "interpretation_pending",
                  "ADD-02:2.1": "invalid"}
    x = next(it for it in ps.items if it.provision == "ADD-02:5.2")
    assert any(v.check == "semantic" and "no_effect on amendment language: a person must confirm" in v.detail
               for v in x.validation)
    assert ps.resolution.pending == 4 and ps.resolution.invalid == 1 and ps.resolution.resolved == 0


def test_an_annotation_that_changes_nothing_cannot_stand_in_for_a_printed_substitution(real):
    """The same hole through an op: an annotate op that 'confirms' (changes nothing) as the only answer to a provision
    that prints a substitution is invalid; next to the change op itself it is left alone."""
    st = real.identity()

    def annotate(p, iid):
        return ChangeProposal(id=iid, state=st, statement_type="amendment_op", provision=p,
                              payload={"type": "annotate", "targets": ["VOL-I:9.2"], "effect": "confirms"},
                              evidence=[_ref(p)])
    alone = _set(real, "ADD-02", [annotate("ADD-02:2.1", "ADD-02/2.1(x)")])
    controller.validate_set(real, alone)
    it = alone.items[0]
    assert it.verification_status == "invalid"
    assert any(v.check == "semantic" and "leaves the provision's printed change unapplied" in v.detail
               for v in it.validation)
    op = ChangeProposal(id="ADD-02/2.1", state=st, statement_type="amendment_op", provision="ADD-02:2.1",
                        target="VOL-I:9.2", payload={"type": "replace_text", "target": "VOL-I:9.2",
                                                     "old": "one hundred and twenty (120) pages",
                                                     "new": "one hundred and fifty (150) pages"},
                        evidence=[_ref("ADD-02:2.1")])
    both = _set(real, "ADD-02", [op, annotate("ADD-02:2.1", "ADD-02/2.1(x)")])
    controller.validate_set(real, both)
    assert {i.id: i.verification_status for i in both.items} == {"ADD-02/2.1": "evidence_verified",
                                                                  "ADD-02/2.1(x)": "evidence_verified"}
    assert both.resolution.no_change_on_amendment_language == []


def test_genuine_no_effect_provisions_still_verify(real):
    """No over-correction: every provision the curated op files (curation/amendments/ADD-01.yaml, ADD-02.yaml) dispose
    as no_effect (cover date and tender lines, recitals, the notes heading, the non-binding minutes), with the curated
    reasons, still verifies; so do confirming answers ('... are unchanged', '... applies')."""
    amend_dir = Path(real.r["cfg"]["amendments_dir"])
    for add in ("ADD-01", "ADD-02"):
        f = yaml.safe_load((amend_dir / f"{add}.yaml").read_text(encoding="utf-8"))
        curated = [(d["provision"], d["reason"]) for d in f["dispositions"] if d["disposition"] == "no_effect"]
        assert len(curated) >= 4
        extra = [("ADD-02:Q13", "the answer confirms that the periods are unchanged"),
                 ("ADD-02:Q14", "the answer confirms that the clause applies")] if add == "ADD-02" else []
        ps = _set(real, add, [_disposition(real, p, reason) for p, reason in curated + extra])
        rep = controller.validate_set(real, ps)
        bad = {it.provision: [v.detail for v in it.validation if not v.ok] for it in ps.items
               if it.verification_status != "evidence_verified"}
        assert not bad, bad
        assert ps.resolution.resolved == len(ps.items) and ps.resolution.no_change_on_amendment_language == []
        assert not (rep["simulation"] or {}).get("findings")


def test_a_curated_set_with_two_obligations_answered_no_effect_reports_the_finding_not_a_clean_applied(real):
    """The curated ADD-02 op file as a proposal, except that the two obligations (5.2: 'Bidders shall reflect the amended
    limit...'; 7.2: 'Form 4-G shall be completed and submitted...') are answered no_effect: the engine accounts for
    every provision (APPLIED), and the controller reports that 2 provisions with amendment language carry no change."""
    f = yaml.safe_load((Path(real.r["cfg"]["amendments_dir"]) / "ADD-02.yaml").read_text(encoding="utf-8"))
    drop = {"ADD-02:5.2", "ADD-02:7.2"}
    st = real.identity()
    items = []
    for o in f["ops"]:
        if o["provision"] in drop:
            continue
        payload = {k: v for k, v in o.items() if k not in ("origin", "review", "reviewer")}
        items.append(ChangeProposal(id=o["id"], state=st, statement_type="amendment_op", provision=o["provision"],
                                    payload=payload, evidence=[_ref(o["provision"])]))
    for d in f["dispositions"]:
        items.append(_disposition(real, d["provision"], d["reason"], d["disposition"]))
    for p in sorted(drop):
        items.append(_disposition(real, p, f"no change: ‘{_quote(p)}’ restates what the clause already requires"))
    ps = _set(real, "ADD-02", items)
    rep = controller.validate_set(real, ps)
    assert rep["simulation"]["status"] == "APPLIED" and rep["simulation"]["unaccounted"] == []
    assert rep["simulation"]["clean"] is False
    assert any("2 provisions with amendment language carry no change" in x for x in rep["simulation"]["findings"])
    assert set(ps.resolution.no_change_on_amendment_language) == drop
    assert ps.status != "complete" and ps.coverage.unaccounted == []          # accounted, not resolved


# ---------------------------------------------------------------------------------------------- finding 1c

def _set_assumptions(ws: Workspace, change) -> None:
    p = Path(ws.r["cfg"]["assumptions"])
    a = yaml.safe_load(p.read_text(encoding="utf-8"))
    change(a)
    p.write_text(yaml.safe_dump(a, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _holiday(a):
    a["calendar"]["holidays"] = ["2026-11-24"]                      # a Tuesday inside the five Working Days


def test_calendar_assumptions_bind_the_state_identity_and_the_calculation(tmp_path):
    """Owner's finding 1c (i). Before the fix the identity was equal while the computed deadline moved."""
    ws = hermetic_workspace(tmp_path)
    args = {"kind": "add_working_days", "args": {"date": "2026-11-26", "n": -5}}
    id1 = ws.identity()
    c1 = call_tool(ws, "calculate", args, "model")
    ps = _set(ws, "ADD-02", [_disposition(ws, "ADD-02:cover/para1", "the addendum's issue date line")])
    _set_assumptions(ws, _holiday)
    c2 = call_tool(ws, "calculate", args, "model")                 # a tool call reloads the changed inputs
    id2 = ws.identity()
    assert (c1["result"], c2["result"]) == ("2026-11-19", "2026-11-18")
    assert id1 != id2, "the deadline moved but the state identity did not"
    assert id1.assumptions_sha256 != id2.assumptions_sha256
    assert c1["inputs_fingerprint"] == id1.fingerprint() and c2["inputs_fingerprint"] == id2.fingerprint()
    rep = controller.validate_set(ws, ps)
    assert ps.status == "stale" and any("assumptions_sha256" in x for x in rep["state_differences"])
    _set_assumptions(ws, lambda a: a["planning"].__setitem__("counting_policy", "day0"))   # the counting policy too
    with pytest.raises(ToolError, match="workspace stale: reload"):
        ws.identity()                                               # loaded under the old inputs: refused, not served
    rel = {"kind": "relative_date", "args": {"anchor_date": "2026-11-26", "offset": 180, "unit": "calendar_day",
                                             "purpose": "validity_end"}}
    c3 = call_tool(ws, "calculate", rel, "model")
    assert c3["planning"]["policy"] == "day0" and ws.identity() != id2
    assert c3["inputs_fingerprint"] == ws.identity().fingerprint() != c2["inputs_fingerprint"]


def test_a_replaced_crop_is_an_integrity_failure_never_served_with_the_old_transcription(tmp_path):
    """Owner's finding 1c (ii). Before the fix get_crop served the replaced file (its new sha256) and get_unit the
    transcription cached from the original."""
    ws = hermetic_workspace(tmp_path, copy_build=True)
    uid = "VOL-II:T2-4/TN"
    u1 = call_tool(ws, "get_unit", {"unit_id": uid}, "model")
    c1 = call_tool(ws, "get_crop", {"unit_id": uid}, "model")
    assert u1["cells_as_issued"]["Limit"] == "5" and c1["crops"]
    unit_crop = next(c for c in c1["crops"] if c["kind"] == "unit")
    other = next(c for c in call_tool(ws, "get_crop", {"unit_id": "VOL-II:T2-4/BOD5"}, "model")["crops"]
                 if c["kind"] == "unit")
    shutil.copy(other["path"], unit_crop["path"])                  # the crop file replaced on disk
    with pytest.raises(ToolError, match="integrity failure"):
        get_crop(ws, uid)                                          # the running workspace, no reload
    with pytest.raises(ToolError, match="workspace stale: reload"):
        get_unit(ws, uid)
    with pytest.raises(ToolError, match="integrity failure"):
        call_tool(ws, "get_crop", {"unit_id": uid}, "model")       # a reload does not make the file verify
    with pytest.raises(ToolError, match="integrity failure"):
        call_tool(ws, "get_unit", {"unit_id": uid}, "model")


def test_submit_and_promote_recheck_freshness_after_an_input_change(tmp_path):
    """Owner's finding 1c (iii): a set whose identity no longer matches the current inputs is stale and cannot be
    promoted (control: the same run promotes before the change, into disposable folders)."""
    ws = hermetic_workspace(tmp_path)
    raw = {"addendum": "ADD-02", "state": ws.identity().model_dump(), "statements": [],
           "items": [json.loads(_disposition(ws, "ADD-02:cover/para1", "the addendum's issue date line")
                                .model_dump_json(include={"id", "state", "statement_type", "provision", "payload",
                                                          "evidence"}))]}
    res = controller.submit(ws, raw, host_model="host-declared-model")
    assert res["items"][0]["status"] == "evidence_verified"
    code, msgs = controller.promote(ws, res["run_id"], REVIEWER, tmp_path / "amend0", tmp_path / "props0")
    assert code == 0, msgs                                         # control: promotable while the inputs stand
    _set_assumptions(ws, _holiday)
    code, msgs = controller.promote(ws, res["run_id"], REVIEWER, tmp_path / "amend", tmp_path / "props")
    assert code == 2 and "another state" in msgs[0] and "assumptions_sha256" in msgs[0], msgs
    assert not (tmp_path / "amend").exists() and not (tmp_path / "props").exists()
    again = controller.submit(ws, raw, host_model="host-declared-model")    # the same set submitted now: stale
    assert again["status"] == "stale" and again["items"][0]["status"] == "invalid"


def test_a_set_validated_while_the_inputs_change_is_staged_stale_not_current(tmp_path, monkeypatch):
    """submit rechecks freshness after validating and before staging: an input that changes while the set is being
    validated makes the staged set stale (every item invalid), never a current-looking verified one."""
    ws = hermetic_workspace(tmp_path)
    raw = {"addendum": "ADD-02", "state": ws.identity().model_dump(), "statements": [],
           "items": [json.loads(_disposition(ws, "ADD-02:cover/para1", "the addendum's issue date line")
                                .model_dump_json(include={"id", "state", "statement_type", "provision", "payload",
                                                          "evidence"}))]}
    real_validate = controller.validate_set

    def validate_then_change(*a, **k):
        report = real_validate(*a, **k)
        _set_assumptions(ws, _holiday)                              # the calendar changes during validation
        return report
    monkeypatch.setattr(controller, "validate_set", validate_then_change)
    res = controller.submit(ws, raw, host_model="host-declared-model")
    assert res["status"] == "stale" and res["items"][0]["status"] == "invalid"
    staged = yaml.safe_load((Path(res["staging"]) / "proposals.yaml").read_text(encoding="utf-8"))
    assert any("workspace stale: reload" in x and "assumptions.yaml" in x
               for x in staged["controller"]["state_differences"])
