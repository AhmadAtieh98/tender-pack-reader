"""Session 09: an obligation whose words are deleted from a clause that stays in force (blind rehearsal 02, ADD-03 4.1:
the model audit opinion struck out of VOL-I 10.3). The register had no status for it: VOL-I-10.3-02 showed
"AMENDED (ADD-03/4.1)", stayed in force, and A5 kept planning the model-auditor activities for it.

An interpretation may now carry `removed: {by: <op id>, note}`. The row is then "REMOVED (<op id>)" and out of force
from that stage (A3, A5 and the general gate leave it out; A1 shows it). Its quote is checked against the unit as it
stood before the op, and the op must exist, be applied at or before that stage and have changed one of the row's units.
A row still in force whose quote vanished because an op deleted words is reported (deleted_words) so a person either
re-makes the reading or marks it removed.
"""
from __future__ import annotations

import pytest

from tenderpack import review, stage2, trace
from tenderpack.amend import Engine, OpFile
from tenderpack.dates import Calendar
from tenderpack.register import Register, RowFile
from tenderpack.schedule import in_force
from tenderpack.util import ROOT

OPINION = ", and shall be accompanied by an opinion from an independent model auditor"


def _units():
    u = lambda uid, doc, kind, text: {"unit_id": uid, "doc": doc, "kind": kind, "text": text, "pages": [1]}  # noqa: E731
    return [u("VOL-I:10.3", "VOL-I", "clause", f"The Financial Model shall be submitted in Excel{OPINION}."),
            u("VOL-I:10.4", "VOL-I", "clause", "All prices shall be stated in Saudi Riyals."),
            u("ADD-01:cover/para1", "ADD-01", "paragraph", "Issued 3 November 2026"),
            u("ADD-01:4.1", "ADD-01", "clause", f"In Volume I Clause 10.3, the words '{OPINION}' are deleted."),
            u("ADD-01:4.2", "ADD-01", "clause", "In Volume I Clause 10.4, 'Saudi Riyals' is deleted and 'SAR' is substituted.")]


def _stages():
    f = OpFile.model_validate({"addendum": "ADD-01", "issued_from": "ADD-01:cover/para1", "prepared_by": "test", "method": "test",
                               "ops": [{"id": "ADD-01/4.1", "provision": "ADD-01:4.1", "type": "replace_text",
                                        "target": "VOL-I:10.3", "old": OPINION, "new": ""},
                                       {"id": "ADD-01/4.2", "provision": "ADD-01:4.2", "type": "replace_text",
                                        "target": "VOL-I:10.4", "old": "Saudi Riyals", "new": "SAR"}],
                               "dispositions": [{"provision": "ADD-01:cover/para1", "disposition": "no_effect",
                                                 "reason": "issue date"}]})
    stages = Engine(_units(), [f]).run()
    assert stages[-1].status == "APPLIED"
    return stages


def _register(stages, later: dict | None):
    interps = [{"stage": "BASE", "quote": "shall be accompanied by an opinion from an independent model auditor"}]
    if later is not None:
        interps.append({"stage": "ADD-01", **later})
    rf = RowFile.model_validate({"prepared_by": "test", "method": "test", "anchors": {}, "rows": [
        {"id": "VOL-I-10.3-02", "group": "VOL-I:10.3", "scope": ["model_audit"], "requirement": "model audit opinion",
         "units": ["VOL-I:10.3"], "discipline": "Finance", "assessment": "pass_fail", "evidence": ["EV-MODEL-AUDIT"],
         "interpretations": interps, "confidence": "high", "confidence_reason": "test"}]})
    return Register(rf, stages, Calendar()), rf.rows[0]


QUOTE = "shall be accompanied by an opinion from an independent model auditor"


def test_a_row_marked_removed_is_out_of_force_and_its_removal_is_checked():
    stages = _stages()
    reg, row = _register(stages, {"quote": QUOTE, "removed": {"by": "ADD-01/4.1", "note": "struck out"}})
    base, add = reg.evaluate(row, stages[0]), reg.evaluate(row, stages[1])
    assert base["status"] == "ACTIVE" and base["active"]
    assert add["status"] == "REMOVED (ADD-01/4.1)" and not add["active"] and add["problems"] == [] and add["stale"] == []
    for force in (in_force, trace._in_force, review._in_force):        # every shared in-force reading agrees
        assert not force(add["status"]) and force(base["status"])
    assert add["interpretation"]["removed"] == {"by": "ADD-01/4.1", "note": "struck out"}
    # an interpretation without `removed` dumps exactly as before the field existed (decision bindings unchanged)
    assert "removed" not in row.interpretations[0].model_dump() and "removed" in row.interpretations[1].model_dump()


@pytest.mark.parametrize("removed, why", [
    ({"by": "ADD-01/9.9"}, "no op of the amendment path"),
    ({"by": "ADD-01/4.2"}, "changed none of the row's units"),
])
def test_a_removal_that_the_amendment_path_does_not_support_is_a_problem(removed, why):
    stages = _stages()
    reg, row = _register(stages, {"quote": QUOTE, "removed": removed})
    ev = reg.evaluate(row, stages[1])
    assert ev["status"].startswith("REMOVED") and any(why in p for p in ev["problems"]), ev["problems"]


def test_the_removed_quote_must_be_in_the_unit_before_the_op():
    stages = _stages()
    reg, row = _register(stages, {"quote": "shall be certified by the Authority", "removed": {"by": "ADD-01/4.1"}})
    assert any("as it stood before the op" in p for p in reg.evaluate(row, stages[1])["problems"])
    reg, row = _register(stages, {"quote": "The Financial Model shall be submitted", "removed": {"by": "ADD-01/4.1"}})
    assert reg.evaluate(row, stages[1])["problems"] == []            # what remained is also in the clause before the op


def test_a_quote_lost_to_a_deletion_of_words_is_reported_until_a_person_decides():
    stages = _stages()
    reg, row = _register(stages, None)                               # no reading made at ADD-01
    r = {"register": reg, "stages": stages, "evals": reg.all()}
    found = stage2.deleted_words(r)
    assert [f["kind"] for f in found] == ["deleted_words"] and found[0]["where"] == "VOL-I-10.3-02"
    assert "ADD-01/4.1" in found[0]["detail"] and "removed: {by: ADD-01/4.1}" in found[0]["detail"]
    reg, row = _register(stages, {"quote": QUOTE, "removed": {"by": "ADD-01/4.1"}})
    assert stage2.deleted_words({"register": reg, "stages": stages, "evals": reg.all()}) == []
    reg, row = _register(stages, {"quote": "The Financial Model shall be submitted in Excel."})   # re-made reading
    assert stage2.deleted_words({"register": reg, "stages": stages, "evals": reg.all()}) == []


# ------------------------------------------------------------------------------------------------ blind rehearsal 02

@pytest.fixture(scope="module")
def blind02():
    b = ROOT / "rehearsals/blind-02"
    r = stage2.run(b / "build", b / "work/pack.yaml", ROOT)
    return {"r": r, "a5": stage2.a5_all(r)}


def ev(r, rid, stage):
    return next(e for e in r["evals"] if e["row"].id == rid)["stages"][stage]


def test_blind02_model_audit_opinion_row_is_removed_at_add03(blind02):
    r = blind02["r"]
    assert ev(r, "VOL-I-10.3-02", "ADD-02")["status"] == "ACTIVE" and in_force(ev(r, "VOL-I-10.3-02", "ADD-02")["status"])
    a = ev(r, "VOL-I-10.3-02", "ADD-03")
    assert a["status"] == "REMOVED (ADD-03/4.1)" and not in_force(a["status"]) and a["problems"] == []
    assert ev(r, "VOL-I-10.3-01", "ADD-03")["status"].startswith("AMENDED")     # the rest of 10.3 stays a requirement
    assert not [f for f in stage2.register_findings(r) if f["kind"] == "deleted_words"]
    assert r["validated"].stage == "ADD-03"
    a1 = stage2.a1_table(r, [])
    assert next(x for x in a1["rows"] if x["id"] == "VOL-I-10.3-02")["status:ADD-03"] == "REMOVED (ADD-03/4.1)"


def test_blind02_a5_and_a3_drop_the_removed_row_and_keep_the_post_award_one(blind02):
    r, progs = blind02["r"], blind02["a5"]
    cites = lambda st, rid: [a["id"] for a in progs[st]["activities"] if rid in a["req_ids"]]  # noqa: E731
    assert cites("ADD-02", "VOL-I-10.3-02")                     # planned while it was a Proposal requirement
    assert cites("ADD-03", "VOL-I-10.3-02") == []               # no A5 activity at ADD-03 cites the removed row
    post = cites("ADD-03", "ADD-03-12.5-01")
    assert {"model-auditor-appoint", "model-audit-review", "model-audit-opinion"} <= set(post)
    assert all("Preferred Bidder" in (a.get("condition") or "") for a in progs["ADD-03"]["activities"] if a["id"] in post)
    a3 = stage2.a3(r, stage2.collect_issues(r, progs["ADD-03"]), progs["ADD-03"])
    assert "VOL-I-10.3-02" not in a3["none_stated_ids"] + a3["explicit_ids"]
    assert not [t for t in r["trace"] if "VOL-I-10.3-02" in t.get("rows", [])]
