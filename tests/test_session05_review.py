"""Regression tests for the owner's code review in session 05 (five findings).

Written BEFORE the fixes and run against commit 160242f to confirm each failure (see the session 05 log).
Every scenario changes in-memory copies of the curated inputs or disposable copies of the evidence;
nothing writes to the repository.
"""
from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path

import pytest
import yaml

from tenderpack import stage2
from tenderpack.amend import Engine, base_state, load_opfile
from tenderpack.draft import draft
from tenderpack.register import pin_value
from tenderpack.util import ROOT

UNITS = json.loads((ROOT / "build/units.json").read_text(encoding="utf-8"))["units"]


def opfiles():
    return [load_opfile(ROOT / "curation/amendments/ADD-01.yaml"), load_opfile(ROOT / "curation/amendments/ADD-02.yaml")]


def run_mut(mutate):
    a, b = opfiles()
    mutate(a, b)
    return Engine(copy.deepcopy(UNITS), [a, b]).run()


def op_of(f, oid):
    return next(o for o in f.ops if o.id == oid)


def result(stages, oid):
    return next(x for s in stages for x in s.ops if x.op.id == oid)


def snapshot(state):
    return {k: (u.sha(), tuple(u.history), tuple(u.annotations), u.superseded_by) for k, u in state.items()}


# ============================================================================ 1. amend.py

def test_set_value_must_be_the_value_the_amendment_states():
    def m(a, b): op_of(b, "ADD-02/5.1").new = "999"
    s = run_mut(m)
    x = result(s, "ADD-02/5.1")
    assert not x.valid and s[2].state["VOL-II:T2-4/TN"].cells["Limit"] == "5"


def test_set_value_must_change_the_column_the_amendment_names():
    def m(a, b): op_of(b, "ADD-02/5.1").column = "Unit"
    s = run_mut(m)
    assert not result(s, "ADD-02/5.1").valid
    assert s[2].state["VOL-II:T2-4/TN"].cells["Unit"] == "mg/l"


def test_replacement_content_must_come_from_the_amendment():
    def m(a, b): op_of(b, "ADD-02/3.1").replacement = "VOL-II:T2-6"
    s = run_mut(m)
    assert not result(s, "ADD-02/3.1").valid
    assert s[2].state["VOL-I:T1-1/B"].status == "active"
    assert all(not u.history for k, u in s[2].state.items() if k.startswith("VOL-II:T2-6"))


def test_replacement_must_be_the_table_the_amendment_prints_for_that_target():
    """A table from the same addendum but for another target (here: Form 4-G's table) is not Table 1-1."""
    def m(a, b): op_of(b, "ADD-02/3.1").replacement = "ADD-02:F4-G"
    s = run_mut(m)
    assert not result(s, "ADD-02/3.1").valid


def test_a_failed_annotation_changes_nothing():
    def m(a, b): op_of(b, "ADD-02/T1-1-rev/note(1)").expect = [{"unit": "VOL-I:11.3", "contains": "eighty (80) marks"}]
    s = run_mut(m)
    assert not result(s, "ADD-02/T1-1-rev/note(1)").valid
    assert "ADD-02/T1-1-rev/note(1)" not in s[2].state["VOL-I:11.3"].annotations


@pytest.mark.parametrize("oid,mutate", [
    ("ADD-02/T1-1-rev/note(1)", lambda o: setattr(o, "expect", [{"unit": "VOL-I:11.3", "contains": "eighty (80) marks"}])),
    ("ADD-02/5.1", lambda o: setattr(o, "new", "999")),
    ("ADD-02/3.1", lambda o: setattr(o, "replacement", "VOL-II:T2-6")),
    ("ADD-02/9.1", lambda o: setattr(o, "new_text", o.new_text + " Extra words not in the provision.")),
    ("ADD-02/7.1", lambda o: setattr(o, "new_group", "ADD-02:F4-G-missing")),
])
def test_a_failed_op_leaves_the_state_exactly_as_without_it(oid, mutate):
    """Text, cells, status, history, annotations (dependencies) and supersession all as if the op were absent."""
    def m(a, b): mutate(op_of(b, oid))
    failed = run_mut(m)
    assert not result(failed, oid).valid

    def drop(a, b): b.ops = [o for o in b.ops if o.id != oid]
    without = run_mut(drop)
    assert snapshot(failed[2].state) == snapshot(without[2].state)


# ============================================================================ 2. draft.py

def _synthetic(text: str) -> list[dict]:
    base = [u for u in UNITS if not u["doc"].startswith("ADD-")]
    return base + [{"unit_id": "ADD-09:cover/para1", "doc": "ADD-09", "kind": "paragraph", "text": "Issued 1 December 2026", "pages": [1]},
                   {"unit_id": "ADD-09:2.1", "doc": "ADD-09", "kind": "clause", "label": "2.1", "pages": [1], "text": text}]


def test_two_recognised_changes_in_one_paragraph_give_two_ops():
    units = _synthetic("In Volume I Clause 9.2, ‘one hundred and twenty (120) pages’ is deleted and ‘one hundred and fifty "
                       "(150) pages’ is substituted, and in Volume V Clause 36.2, ‘SAR 5,000,000’ is deleted and "
                       "‘SAR 2,500,000’ is substituted.")
    f = draft(units, "ADD-09")
    assert sorted(o.target for o in f.ops if o.provision == "ADD-09:2.1") == ["VOL-I:9.2", "VOL-V:36.2"]
    st = Engine(units, [f]).run()[-1]
    assert "2,500,000" in st.state["VOL-V:36.2"].text and "one hundred and fifty (150) pages" in st.state["VOL-I:9.2"].text
    assert next(c for c in st.coverage if c["provision"] == "ADD-09:2.1")["disposition"] == "op"


def test_unrecognised_remainder_of_a_paragraph_is_flagged_unresolved():
    units = _synthetic("In Volume I Clause 9.2, ‘one hundred and twenty (120) pages’ is deleted and ‘one hundred and fifty "
                       "(150) pages’ is substituted. The bid security period is extended by thirty days.")
    f = draft(units, "ADD-09")
    assert [o.target for o in f.ops if o.provision == "ADD-09:2.1"] == ["VOL-I:9.2"]
    d = [x for x in f.dispositions if x.provision == "ADD-09:2.1"]
    assert d and d[0].disposition == "unresolved" and "bid security period" in d[0].reason
    st = Engine(units, [f]).run()[-1]
    assert st.status == "PARTIAL"
    assert next(c for c in st.coverage if c["provision"] == "ADD-09:2.1")["disposition"] == "unresolved"


# ============================================================================ 3. evidence and pins

def _evidence_copy(tmp: Path) -> Path:
    shutil.copytree(ROOT / "build", tmp / "ev", ignore=shutil.ignore_patterns("fixture*", "drill*"))
    return tmp / "ev"


def test_an_edited_intermediate_file_is_rejected(tmp_path):
    ev = _evidence_copy(tmp_path)
    uj = json.loads((ev / "units.json").read_text(encoding="utf-8"))
    next(u for u in uj["units"] if u["unit_id"] == "VOL-I:8.6")["pages"] = [99]
    (ev / "units.json").write_text(json.dumps(uj, ensure_ascii=False), encoding="utf-8")
    _, problems = stage2.load_evidence(ev, ROOT)
    assert any("units.json" in p for p in problems)


def test_an_edited_intermediate_file_with_a_rewritten_manifest_is_still_rejected(tmp_path):
    """Re-hashing the manifest does not help: a unit's pages must agree with its anchors."""
    import hashlib
    ev = _evidence_copy(tmp_path)
    uj = json.loads((ev / "units.json").read_text(encoding="utf-8"))
    next(u for u in uj["units"] if u["unit_id"] == "VOL-I:8.6")["pages"] = [99]
    data = json.dumps(uj, ensure_ascii=False)
    (ev / "units.json").write_text(data, encoding="utf-8")
    man = json.loads((ev / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))
    for k in man["outputs"]:
        if k.endswith("units.json"):
            man["outputs"][k] = hashlib.sha256(data.encode("utf-8")).hexdigest()
    (ev / "BUILD_MANIFEST.json").write_text(json.dumps(man), encoding="utf-8")
    _, problems = stage2.load_evidence(ev, ROOT)
    assert any("VOL-I:8.6" in p for p in problems)


def test_pin_keeps_the_image_review_fingerprint():
    st0 = base_state(UNITS, ["ADD-01", "ADD-02"])
    units = copy.deepcopy(UNITS)
    tn = next(u for u in units if u["unit_id"] == "VOL-II:T2-4/TN")
    tn["reading"]["subject_sha256"] = "0" * 64           # the reading changed (e.g. an uncertainty) with the same text
    st1 = base_state(units, ["ADD-01", "ADD-02"])
    assert pin_value(st0, "VOL-II:T2-4/TN") != pin_value(st1, "VOL-II:T2-4/TN")
    tn["reading"]["status"] = "approved"                  # approving it again does not make the old pin valid
    st2 = base_state(units, ["ADD-01", "ADD-02"])
    assert pin_value(st2, "VOL-II:T2-4/TN") == pin_value(st1, "VOL-II:T2-4/TN") != pin_value(st0, "VOL-II:T2-4/TN")


# ============================================================================ 4. provenance of quotations

@pytest.fixture(scope="module")
def outputs(tmp_path_factory):
    out = tmp_path_factory.mktemp("s05") / "out"
    r = stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)
    stage2.write(r, out)
    return out


def test_a3_cites_the_amendment_that_supplies_the_quoted_consequence(outputs):
    a3 = json.loads((outputs / "a3/a3.json").read_text(encoding="utf-8"))
    item = next(i for s in a3["sections"] for i in s["items"] if i["id"] == "VOL-I-8.6-01")
    assert "ADD-02 9.1 p3" in item["source"]
    assert "VOL-I 8.6 p4" not in item["source"] or "as reinstated" in item["source"]


def test_a1_keeps_original_quotation_apart_from_assembled_text(outputs):
    a1 = json.loads((outputs / "a1/a1.json").read_text(encoding="utf-8"))
    keys = {c["key"] for c in a1["columns"]}
    assert {"original_text", "effective_text"} <= keys
    row = next(r for r in a1["rows"] if r["id"] == "VOL-I-8.6-01")
    assert "thirty per cent (30%)" in row["original_text"] and "thirty-five per cent (35%)" in row["effective_text"]
    assert "ADD-02 9.1 p3" in row["consequence_source"]
    assert "ADD-02 9.1 p3" in row["source"]                 # latest reference for the point


# ============================================================================ 5. schedule.py

def _pack_with_templates(tmp: Path, edit) -> Path:
    tpl = yaml.safe_load((ROOT / "curation/activity_templates.yaml").read_text(encoding="utf-8"))
    edit(tpl)
    (tmp / "tpl.yaml").write_text(yaml.safe_dump(tpl, allow_unicode=True), encoding="utf-8")
    cfg = yaml.safe_load((ROOT / "config/pack.yaml").read_text(encoding="utf-8"))
    cfg["activity_templates"] = str(tmp / "tpl.yaml")
    (tmp / "pack.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return tmp / "pack.yaml"


def test_a_required_deliverable_without_activities_is_a_failure(tmp_path):
    pack = _pack_with_templates(tmp_path, lambda t: t.pop("EV-LCC"))
    res = stage2.write(stage2.run(ROOT / "build", pack, ROOT), tmp_path / "out")
    assert res["status"] == "structural_failure"
    assert any(not c["ok"] and "EV-LCC" in c["detail"] for c in res["checks"])


def test_an_unknown_dependency_is_a_failure(tmp_path):
    def edit(t):
        t["EV-LCC"][1]["predecessors"] = ["lcc-ratio", "no-such-activity"]
    pack = _pack_with_templates(tmp_path, edit)
    res = stage2.write(stage2.run(ROOT / "build", pack, ROOT), tmp_path / "out")
    assert res["status"] == "structural_failure"
    assert any(not c["ok"] and "no-such-activity" in c["detail"] for c in res["checks"])
