"""Session 10, owner's section 3: indirect effects through reusable, evidence-backed relationships.

Blind rehearsal 03 left four gaps that a row-cites-unit diff cannot see (COMPARISON.md: S9, S10, M8, U5): membership
knock-ons (Form 4-C from the new member, VOL-I 8.2, the 8.4 weighting), effluent-limit knock-ons (the VOL-II 7.2/7.3
reliability run, VOL-V 31.1(b)), the Ramp-Up payment change reaching no Financial Model or Form 4-F activity, and
Schedule 11 (not supplied) never shown against the persistent-breach conclusions. They are now curated, once, as
relationships (curation/relationships.yaml and the rehearsal copies) and followed by tenderpack.relationships into
`diff`, A1, A2, A3 and A5, in three labelled classes never merged with the direct changes.

Read-only: the rehearsal runs come from the session's disposable builds (tests/conftest.py); append_proposed writes
only into tmp copies. Nothing is accepted, approved or sent.
"""
from __future__ import annotations

import copy
import shutil

import pytest

from tenderpack import live, relationships as R, stage2
from tenderpack.util import ROOT, load_yaml

# ---------------------------------------------------------------------------------------------- synthetic

UNITS = [
    {"unit_id": "VOL-X:1.1", "doc": "VOL-X", "pages": [1], "text": "The price shall be calculated under Clause 9."},
    {"unit_id": "VOL-X:9.1", "doc": "VOL-X", "pages": [2], "text": "During the first year the payment is ninety per cent."},
    {"unit_id": "VOL-X:9.2", "doc": "VOL-X", "pages": [2], "text": "Termination for the events listed in Schedule 4."},
]
ROWS = ["ROW-PRICE", "ROW-MODEL", "ROW-TERM"]
ACTS = {"EV-MODEL": [{"id": "model-build"}], "_exceptions": {}}


def entry(**kw) -> dict:
    base = {"id": "REL-1", "from": "VOL-X:9.1", "to": "ROW-PRICE", "kind": "feeds_calculation", "status": "confirmed",
            "evidence": [{"unit": "VOL-X:1.1", "page": 1, "words": "calculated under Clause 9"}], "origin": "curator",
            "review": "proposed"}
    base.update(kw)
    return {k: v for k, v in base.items() if v is not None}


def check(*entries, **kw):
    return R.validate(list(entries), UNITS, ROWS, ACTS, evidence_items={"EV-MODEL"}, issues={"I-OPEN"}, **kw)


def test_a_confirmed_link_quoted_verbatim_on_its_page_is_clean():
    assert check(entry()) == []
    assert check(entry(to=["ROW-PRICE", "model-build", "EV-MODEL", "calc:price"])) == []


@pytest.mark.parametrize("change, why", [
    ({"evidence": []}, "status confirmed needs evidence"),
    ({"evidence": None}, "status confirmed needs evidence"),
    ({"evidence": [{"unit": "VOL-X:1.1", "page": 1, "words": "calculated under Clause 8"}]}, "not verbatim"),
    ({"evidence": [{"unit": "VOL-X:1.1", "page": 2, "words": "calculated under Clause 9"}]}, "not p2"),
    ({"evidence": [{"unit": "VOL-X:1.1", "page": 1, "words": "   "}]}, "non-blank words"),
    ({"evidence": [{"unit": "VOL-X:7.7", "page": 1, "words": "calculated"}]}, "does not exist"),
    ({"status": "proposed", "evidence": None}, "needs a `basis`"),
    ({"status": "possible", "basis": "  "}, "needs a `basis`"),
    ({"status": "certain"}, "unknown status"),
    ({"kind": "influences"}, "unknown kind"),
    ({"to": "ROW-NOPE"}, "no row, unit, activity"),
    ({"from": "ROW-NOPE"}, "no row or unit"),
    ({"to": "words:the price"}, "allowed in `from` only"),
    ({"from": "calc:orphan"}, "reached by no entry"),
    ({"issues": ["I-CLOSED"]}, "linked issues that do not exist"),
    ({"origin": None}, "missing ['origin']"),
    ({"reviewed": True}, "unknown field"),
    ({"review": "accepted by the program"}, "drafting flag"),
])
def test_every_malformed_or_unevidenced_entry_is_a_finding(change, why):
    found = check(entry(**change))                             # a None value drops the field
    assert any(why in f for f in found), found


def test_a_missing_document_entry_needs_the_document_and_the_blocked_conclusion_and_blocks_rows_or_units():
    gap = entry(id="REL-GAP", **{"from": "VOL-X:9.2"}, to=["ROW-TERM", "VOL-X:9.2"], kind="missing_document",
                evidence=[{"unit": "VOL-X:9.2", "page": 2, "words": "listed in Schedule 4"}])
    found = check(gap)
    assert sum("missing_document needs" in f for f in found) == 3, found
    ok = {**gap, "document": "Schedule 4", "document_id": "SCH-4", "blocks": "which events terminate"}
    assert check(ok) == []
    assert any("blocks rows or units only" in f for f in check({**ok, "to": ["model-build"]}))


def test_a_model_proposed_link_is_confirmed_only_by_a_named_person():
    ai = entry(origin="ai:run-1")
    assert any("confirmed only by a person" in f for f in check(ai))
    assert any("confirmed only by a person" in f for f in check({**ai, "confirmed_by": "Claude assistant"}))
    assert check({**ai, "confirmed_by": "Ahmad Atieh"}) == []
    assert check({**ai, "status": "proposed", "basis": "inferred"}) == []      # proposed needs no one


def test_traversal_classes_follow_the_weakest_link_and_never_mix():
    ents = [entry(id="REL-A", to="calc:price"),
            entry(id="REL-B", **{"from": "calc:price"}, to="ROW-PRICE"),
            entry(id="REL-C", **{"from": "calc:price"}, to="ROW-MODEL", status="proposed", basis="inferred"),
            entry(id="REL-D", **{"from": "ROW-MODEL"}, to="model-build"),
            entry(id="REL-E", **{"from": ["words:first year payment", "words:the payment"]}, to="ROW-TERM",
                  status="confirmed")]
    recs = R.trace(ents, {"VOL-X:9.1"}, words=["During the first year the payment is ninety per cent."])
    got = {(x["target"], x["status"]) for x in recs}
    assert ("calc:price", "confirmed") in got and ("ROW-PRICE", "confirmed") in got
    assert ("ROW-MODEL", "proposed") in got and ("model-build", "proposed") in got      # confirmed after proposed
    assert ("ROW-TERM", "possible") in got                    # a words: trigger is at most a possible impact
    by = dict(R.by_class(recs))
    assert [x["target"] for x in by["confirmed dependency"]] == ["ROW-PRICE", "calc:price"]
    assert {x["target"] for x in by["proposed relationship"]} == {"ROW-MODEL", "model-build"}
    assert [x["target"] for x in by["possible impact"]] == ["ROW-TERM"]
    assert R.reach(ents, {"VOL-X:9.1"})["model-build"] == [(ents[3], "proposed")]
    assert R.trace(ents, {"VOL-X:1.1"}) == []                 # nothing starts from an unrelated change


def test_a_cycle_ends_and_a_missing_document_is_reported_when_its_blocked_target_changes():
    ents = [entry(id="REL-A", to="ROW-PRICE"), entry(id="REL-B", **{"from": "ROW-PRICE"}, to="VOL-X:9.1"),
            entry(id="REL-GAP", **{"from": "VOL-X:9.2"}, to=["ROW-TERM"], kind="missing_document",
                  document="Schedule 4", document_id="SCH-4", blocks="which events terminate")]
    recs = R.trace(ents, {"VOL-X:9.1", "ROW-TERM"})
    assert {x["target"] for x in recs} == {"ROW-PRICE", "VOL-X:9.1", "ROW-TERM"}
    gap = R.gaps(recs)
    assert [(g["target"], g["via_target"]) for g in gap] == [("ROW-TERM", True)]
    assert all(x["kind"] != "missing_document" for _, xs in R.by_class(recs) for x in xs)


# ---------------------------------------------------------------------------------------------- the curated files

@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


def test_the_curated_files_are_clean_and_every_confirmed_link_quotes_the_documents(real, blind02_run, blind03_run):
    for r in (real, blind02_run, blind03_run):
        assert r["relationships"], r["relationships_path"]
        assert stage2.relationship_findings(r) == [], r["relationships_path"]
        assert not [f for f in stage2.register_findings(r) if f["kind"] == "relationship"]
        for e in r["relationships"]:
            assert e["review"] == "proposed" and e["origin"] == "curator"
            assert e["status"] != "confirmed" or e["evidence"], e["id"]
            assert e["status"] == "confirmed" or e.get("basis"), e["id"]
    assert real["relationships_path"] == ROOT / "curation/relationships.yaml"
    assert blind03_run["relationships_path"] == ROOT / "rehearsals/blind-03/work/relationships.yaml"
    kinds = {e["kind"] for e in real["relationships"]}
    assert {"member_scope", "limit_applies", "feeds_calculation", "depends_on", "missing_document"} <= kinds


def test_a_quote_that_is_not_in_the_documents_is_a_check_register_finding_and_a_release_blocker(real):
    r = copy.copy(real)
    r["relationships"] = copy.deepcopy(real["relationships"])
    r["relationships"][0]["evidence"][0]["words"] = "weighted by turnover"
    found = [f for f in stage2.register_findings(r) if f["kind"] == "relationship"]
    assert found and found[0]["where"] == r["relationships"][0]["id"] and "not verbatim" in found[0]["detail"]
    assert any(b["kind"] == "coverage" and "relationship finding" in b["detail"] for b in stage2.release_blockers(r))


def test_open_items_stay_open_and_assumptions_stay_assumptions(real):
    issues = {i["id"]: i for i in stage2.collect_issues(real, None)}
    for iid in ("I-VOL-II-T24-TENSIONS", "I-PERMIT", "I-VOL-V-MISSING", "I-BIDDER-FACTS"):
        assert iid in issues                                   # linked by the relationships, never resolved
    linked = {i for e in real["relationships"] for i in e.get("issues") or []}
    assert {"I-VOL-II-T24-TENSIONS", "I-PERMIT", "I-VOL-V-MISSING"} <= linked
    for e in real["relationships"]:                            # nothing curated touches durations or the bidder setup
        assert not any(str(t).startswith(("lead_times", "bidder", "resources")) for t in R.ends(e, "to"))


# ---------------------------------------------------------------------------------------------- the real pack

def test_the_real_pack_add_02_tn_change_reaches_the_reliability_run_and_the_contract_as_confirmed(real):
    recs = real["relationship_impact"]["ADD-02"]["records"]
    conf = {x["target"] for x in recs if x["status"] == "confirmed" and x["kind"] != "missing_document"}
    assert {"VOL-II-3.1-01", "VOL-II-7.2-01", "VOL-V-31.1-02", "VOL-V-29.3-01"} <= conf
    gaps = {x["target"] for x in R.gaps(recs)}
    assert "VOL-II-T2-4-TN" in gaps                            # the amended limit is still subject to the Permit
    a5 = stage2.a5_all(real)["ADD-02"]
    tp = next(a for a in a5["activities"] if a["id"] == "technical-proposal")
    assert any(f.startswith("REVIEW (confirmed dependency)") for f in tp["flags"]) and tp["status"] == "OK"
    a2 = stage2.a2(real)
    md = a2["markdown"]
    sec = md.index("### Reached through relationships", md.index("## ADD-02"))
    order = [md.index(h, sec) for h in ("**Confirmed dependency**", "**Proposed relationship**", "**Possible impact**",
                                        "**Referenced but not supplied")]
    assert order == sorted(order)
    assert {x["stage"] for x in a2["relationships"]} == {"ADD-01", "ADD-02"}


# ---------------------------------------------------------------------------------------------- blind rehearsal 03

def _without_relationships(r: dict) -> dict:
    r2 = dict(r)
    r2["relationships"] = []
    r2["relationship_impact"] = R.impact(r2)
    return r2


@pytest.fixture(scope="module")
def b3(blind03_run):
    r = blind03_run
    return {"r": r, "a5": stage2.a5_all(r), "a5_plain": stage2.a5_all(_without_relationships(r)),
            "diff": live.diff(r, "ADD-02", "ADD-03")}


def test_blind03_ramp_up_change_reaches_the_financial_model_and_form_4f_marking_them_for_review(b3):
    """M8: the 29.3 change (ADD-03/6.1) reached A1 only; no Envelope B activity depended on it."""
    recs = b3["r"]["relationship_impact"]["ADD-03"]["records"]
    from_293 = [x for x in recs if "VOL-V:29.3" in x["sources"]]
    by = {(x["target"], x["status"]) for x in from_293}
    assert ("VOL-I-10.3-01", "proposed") in by                 # the model: inferred, not stated -> proposed
    assert ("VOL-I-10.2-01", "confirmed") in by                # the quoted price: VOL-I 10.2 cites Clause 29
    assert ("VOL-IV-F4F-02", "proposed") in by
    acts = {a["id"]: a for a in b3["a5"]["ADD-03"]["activities"]}
    plain = {a["id"]: a for a in b3["a5_plain"]["ADD-03"]["activities"]}
    for aid in ("fin-model-build", "fin-model-freeze"):
        assert any(f.startswith("REVIEW (proposed relationship)") and "VOL-V:29.3" in f for f in acts[aid]["flags"]), aid
        assert not any(f.startswith("REVIEW") for f in plain[aid]["flags"])          # the gap, reproduced without them
    f4f = [f for f in acts["form-4f"]["flags"] if f.startswith("REVIEW")]
    assert any(f.startswith("REVIEW (confirmed dependency)") for f in f4f)
    assert any(f.startswith("REVIEW (proposed relationship)") for f in f4f)
    for aid in ("fin-model-build", "fin-model-freeze", "form-4f"):            # dates, durations and statuses unchanged
        for k in ("earliest_start", "latest_start", "latest_finish", "float_wd", "status", "duration_wd",
                  "duration_assumption", "count"):
            assert acts[aid][k] == plain[aid][k], (aid, k)


def test_blind03_membership_and_effluent_knock_ons_are_reached_as_confirmed_dependencies(b3):
    """S9 (membership: 8.2, the 8.4 weighting, the O&M Operator's own Form 4-C) and S10 (TP: VOL-II 3.1, the 7.2/7.3
    reliability run, VOL-V 31.1(b), 29.3's second limb)."""
    recs = b3["r"]["relationship_impact"]["ADD-03"]["records"]
    conf = {x["target"] for x in recs if x["status"] == "confirmed" and x["kind"] != "missing_document"}
    assert {"VOL-I-8.2-01", "VOL-I-8.4-01", "VOL-I-8.4-02", "VOL-I-9.4-01", "VOL-IV-F4C-N1"} <= conf
    assert {"VOL-II-3.1-01", "VOL-II-7.2-01", "VOL-V-31.1-02", "VOL-V-29.3-01"} <= conf
    om = [x for x in recs if x["target"] == "VOL-I-9.4-01" and "VOL-I:8.8" in x["sources"]]
    assert om and om[0]["path"] == ["REL-ADD03-OM-OPERATOR-MEMBER"]           # the O&M Operator's own Form 4-C
    acts = {a["id"]: a for a in b3["a5"]["ADD-03"]["activities"]}
    assert any(f.startswith("REVIEW (confirmed dependency)") for f in acts["form-4c-sign"]["flags"])
    assert any(f.startswith("REVIEW (confirmed dependency)") for f in acts["fin-standing"]["flags"])


def test_blind03_schedule_11_is_shown_against_31_4_and_39_3_with_the_conclusion_it_blocks(b3):
    """U5: 31.4 and 39.3 are deleted by ADD-03 6.2; whether persistent breach survives in Schedule 11 (not supplied)
    cannot be checked."""
    r = b3["r"]
    gaps = R.gaps(r["relationship_impact"]["ADD-03"]["records"])
    blocked = {x["target"]: x for x in gaps if x["entry_id"] == "REL-MISSING-SCHEDULE-11-PERSISTENT-BREACH"}
    assert set(blocked) == {"VOL-V-31.4-01", "VOL-V:39.3"} and all(x["status"] == "proposed" for x in blocked.values())
    issues = {i["id"]: i for i in stage2.collect_issues(r, b3["a5"]["ADD-03"])}
    sch = issues["I-AUTO-NOT-SUPPLIED-VOL-V-SCHEDULE-11"]
    assert sch["theme"] == "missing" and sch["show_in_a3"]
    for t in ("VOL-V-31.4-01", "VOL-V:39.3", "VOL-V:18.2"):
        assert t in sch["text"]
    assert "cannot be established" in sch["text"] and "persistent breach" in sch["text"]
    a3 = stage2.a3(r, list(issues.values()), b3["a5"]["ADD-03"])
    group = next(g for g in a3["groups"]["groups"] if g["key"] == "missing")
    assert "I-AUTO-NOT-SUPPLIED-VOL-V-SCHEDULE-11" in [i["id"] for i in group["items"]]
    text, data = b3["diff"]
    assert {"VOL-V-31.4-01", "VOL-V:39.3"} <= set(data["relationships"]["not supplied"])
    line = next(x for x in text.splitlines() if x.startswith("- VOL-V-31.4-01"))
    assert "NOT SUPPLIED: Volume V Schedule 11" in line and "cannot be established" in line
    a1 = stage2.a1_table(r, list(issues.values()))
    rel = next(x for x in a1["rows"] if x["id"] == "VOL-V-31.4-01")["relationships"]
    assert any(x.startswith("NOT SUPPLIED: Volume V Schedule 11") for x in rel)


def test_blind03_diff_keeps_the_three_classes_apart_from_the_direct_changes(b3):
    text, data = b3["diff"]
    lines = text.splitlines()
    i = lines.index("## Reached through relationships (indirect: for review, not direct citations)")
    heads = [x for x in lines[i:] if x.startswith("### ")][:4]
    assert [h.split(" (")[0] for h in heads] == ["### Confirmed dependency", "### Proposed relationship",
                                                 "### Possible impact", "### Referenced but not supplied: conclusions in play that cannot be established"]
    assert lines.index("## Requirements") < i < lines.index("## Disqualifiers (A3)")
    assert "VOL-I-10.3-01" in data["relationships"]["proposed relationship"]
    assert "VOL-I-10.3-01" not in data["requirements"]["changed"]       # reached, not a direct citation
    prog = text[text.index("## Programme impact"):]
    assert "- REVIEW (proposed relationship) fin-model-build:" in prog


# ---------------------------------------------------------------------------------------------- landing proposals

def test_append_proposed_lands_a_models_links_as_proposed_and_never_confirmed(tmp_path, real):
    path = tmp_path / "relationships.yaml"
    shutil.copyfile(ROOT / "curation/relationships.yaml", path)
    before = path.read_text(encoding="utf-8")
    proposals = [
        {"from": "VOL-V:29.3", "to": ["fin-model-build"], "kind": "depends_on", "status": "confirmed",
         "basis": "the model computes the Ramp-Up revenue",
         "evidence": [{"unit": "VOL-V:29.3", "page": 3, "words": "the Availability Payment shall be paid at ninety per cent (90%) of the full rate"}]},
        {"from": "VOL-I:8.1", "to": "VOL-I-9.1h-01", "kind": "member_scope", "status": "possible",
         "basis": "each new member's Form 4-C signatory needs a notarised Power of Attorney"},
    ]
    res = R.append_proposed(path, proposals, "ADD-04-host-run-1")
    assert res == {"appended": ["REL-AI-001", "REL-AI-002"], "skipped": []}
    text = path.read_text(encoding="utf-8")
    assert text.startswith(before.rstrip("\n"))                 # nothing before the new entries changed (comments kept)
    ents = R.load(path)
    new = {e["id"]: e for e in ents[-2:]}
    assert new["REL-AI-001"]["status"] == "proposed" and "said the documents state this link" in new["REL-AI-001"]["note"]
    assert new["REL-AI-002"]["status"] == "possible"
    assert all(e["origin"] == "ai:ADD-04-host-run-1" and e["review"] == "proposed" for e in new.values())
    assert R.validate(ents, real["units"], real["rowfile"].rows, real["templates"], evidence_items=real["evidence_items"],
                      issues=set(real["curated_issues"])) == []
    again = R.append_proposed(path, proposals[:1], "ADD-04-host-run-2")       # same from, to and kind: skipped
    assert again["appended"] == [] and again["skipped"]
    with pytest.raises(ValueError):
        R.append_proposed(path, [{"from": "VOL-I:8.1", "to": "VOL-I-8.4-01", "kind": "influences", "basis": "x"}], "r")
    with pytest.raises(ValueError):
        R.append_proposed(path, [{"from": "VOL-I:8.1", "to": "VOL-I-8.4-01", "kind": "member_scope"}], "r")
    assert R.load(path) == ents                                  # a refused call writes nothing
    fresh = tmp_path / "new" / "relationships.yaml"
    assert R.append_proposed(fresh, proposals[1:], "run-3")["appended"] == ["REL-AI-001"]
    assert R.load(fresh)[0]["status"] == "possible"
    # a person may later confirm a model's link only by naming themselves
    e = dict(new["REL-AI-001"], status="confirmed")
    assert any("confirmed only by a person" in f for f in R.validate([e], real["units"], real["rowfile"].rows,
                                                                       real["templates"]))
