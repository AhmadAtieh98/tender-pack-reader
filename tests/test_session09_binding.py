"""Session 09, finding B: a decision must be bound to where its units are printed, not only to their words.

Before the fix, amend.unit_pin hashed a unit's status, text, cells, annotations and image-reading subject only, so an
op's subject (Engine.subject "before" pins) and a row's dependency pins did not change when a unit's SOURCE moved:
Table 1-1 row B printed somewhere else with the same words left a decision on ADD-02/3.1 (which replaces Table 1-1)
standing, and a row decision did not notice a dependency (e.g. the Proposal Due Date clause) printed elsewhere.

The genuine test builds two synthetic packs that differ only in where ONE table row is drawn (make_fixture
row_shift_pt), ingests both through the normal pipeline and loads them with stage2's loader (E01 must pass for both:
units.json is never edited). The real-pack tests below it are labelled unit tests of the pin function and of the
bindings, made by moving a box in an in-memory copy. Decisions are written only to disposable files by
"Fixture Test Reviewer"; nothing in the repository is accepted, rejected or approved.
"""
from __future__ import annotations

import copy
import hashlib
import json

import pytest
import yaml

import make_fixture
from tenderpack import review, stage2
from tenderpack.amend import Engine, Op, unit_evidence, unit_pin
from tenderpack.cli import ingest
from tenderpack.dates import Calendar
from tenderpack.register import Interp, Register, Row, RowFile, pin_value
from tenderpack.util import ROOT, load_yaml

MOVED, KEPT = "SYN-01:T9-1/9-1.5", "SYN-01:T9-1/9-1.1"
WHO = "Fixture Test Reviewer"


# ---------------------------------------------------------------------------------------------- two synthetic builds

def _pdf(src):
    return (src / "SYN-01_Synthetic_Test_Volume.pdf").read_bytes()


@pytest.fixture(scope="module")
def builds(tmp_path_factory):
    """'a' and 'a2': the unchanged fixture ingested twice; 'b': the same fixture with row 9-1.5 drawn 15 pt lower."""
    t = tmp_path_factory.mktemp("s09-binding")
    srcs = {"a": t / "src-a", "b": t / "src-b", "zero": t / "src-zero"}
    make_fixture.build(srcs["a"])
    make_fixture.build(srcs["b"], row_shift_pt=15.0)
    make_fixture.build(srcs["zero"], row_shift_pt=0.0)
    out = {"srcs": srcs}
    for name, src in (("a", srcs["a"]), ("a2", srcs["a"]), ("b", srcs["b"])):
        ev = t / f"build-{name}"
        assert ingest(src / "pack.yaml", ev, ROOT, quiet=True)["exit_code"] == 0
        units, problems = stage2.load_evidence(ev, ROOT)              # E01: built from these inputs, nothing edited
        assert problems == [], (name, problems)
        out[name] = _bind_ctx(units, ev, load_yaml(src / "pack.yaml"))
    return out


def _bind_ctx(units, evidence_dir, cfg) -> dict:
    """What review.row_binding / op_binding read, for a synthetic row citing the row that moves."""
    row = Row(id="SYN-01-T9-1-01", group="SYN-01:T9-1", scope=["bid"], requirement="Synthetic: velocity value applies",
              units=[MOVED], discipline="technical", assessment="pass_fail", no_deliverable="synthetic test row",
              interpretations=[Interp(stage="BASE", quote="Velocity")], confidence="high", confidence_reason="synthetic")
    eng = Engine(units, [], set())
    stages = eng.run()
    reg = Register(RowFile(prepared_by="test", method="test", anchors={}, rows=[row]), stages, Calendar())
    r = {"units": units, "cfg": cfg, "root": ROOT, "evidence_dir": evidence_dir, "evidence_items": {}, "register": reg,
         "stages": stages, "order": [s.stage for s in stages]}
    r["evals"] = reg.all()
    return {"r": r, "engine": eng, "state": stages[0].state, "units": {u["unit_id"]: u for u in units}}


def test_the_fixture_parameter_defaults_to_the_same_bytes(builds):
    s = builds["srcs"]
    assert hashlib.sha256(_pdf(s["a"])).hexdigest() == hashlib.sha256(_pdf(s["zero"])).hexdigest()
    assert (s["a"] / "expected.yaml").read_bytes() == (s["zero"] / "expected.yaml").read_bytes()
    assert _pdf(s["a"]) != _pdf(s["b"])


def test_only_the_moved_rows_source_differs_its_words_do_not(builds):
    a, b = builds["a"]["units"], builds["b"]["units"]
    assert sorted(a) == sorted(b)
    assert [k for k in a if (a[k].get("text"), a[k].get("cells")) != (b[k].get("text"), b[k].get("cells"))] == []
    assert [k for k in a if a[k].get("anchors") != b[k].get("anchors")] == [MOVED]
    assert a[MOVED]["anchors"][0]["bbox"][1] + 15 == pytest.approx(b[MOVED]["anchors"][0]["bbox"][1], abs=0.11)


def test_the_moved_rows_pin_changes_and_only_its_pin(builds):
    a, b = builds["a"], builds["b"]
    assert unit_pin(a["state"], MOVED, a["engine"].evidence) != unit_pin(b["state"], MOVED, b["engine"].evidence)
    assert unit_pin(a["state"], KEPT, a["engine"].evidence) == unit_pin(b["state"], KEPT, b["engine"].evidence)
    # the content-only pin (what an interpretation is pinned to for STALE) is unchanged: the words did not change
    assert unit_pin(a["state"], MOVED) == unit_pin(b["state"], MOVED) == pin_value(b["state"], MOVED)


@pytest.mark.parametrize("op", [
    Op(id="SYN-TEST/1", provision="SYN-01:3.1", type="replace_unit", target="SYN-01:T9-1"),
    Op(id="SYN-TEST/2", provision="SYN-01:3.1", type="set_value", target=MOVED, column="Value", new="1.3"),
])
def test_an_ops_subject_changes_when_a_member_row_is_printed_elsewhere(builds, op):
    a, b = builds["a"], builds["b"]
    sa, sb = a["engine"].subject(op, a["state"]), b["engine"].subject(op, b["state"])
    assert MOVED in sa["before"] and sa["before"][MOVED] != sb["before"][MOVED]
    assert {k: v for k, v in sa["before"].items() if k != MOVED} == {k: v for k, v in sb["before"].items() if k != MOVED}
    assert sa != sb


def test_a_row_citing_the_moved_unit_gets_a_new_binding(builds):
    a, b = builds["a"], builds["b"]
    ba, bb = (review.row_binding(x["r"], x["r"]["evals"][0]) for x in (a, b))
    assert ba["row"] == bb["row"]                                        # the row as written is the same
    assert ba["source"][MOVED]["anchors"] != bb["source"][MOVED]["anchors"]
    assert ba["states"][0]["dependencies"][MOVED] != bb["states"][0]["dependencies"][MOVED]
    assert review.fingerprint(ba) != review.fingerprint(bb)
    # the document is identified by the sha256 the build manifest recorded for it (a different PDF here)
    for x, src in ((a, builds["srcs"]["a"]), (b, builds["srcs"]["b"])):
        assert review.documents(x["r"]) == {"SYN-01": hashlib.sha256(_pdf(src)).hexdigest()}


def test_two_ingests_of_the_same_pdf_give_the_same_pins_and_bindings(builds):
    a, a2 = builds["a"], builds["a2"]
    assert {k: unit_pin(a["state"], k, a["engine"].evidence) for k in a["units"]} == \
        {k: unit_pin(a2["state"], k, a2["engine"].evidence) for k in a2["units"]}
    assert a["engine"].evidence == a2["engine"].evidence
    op = Op(id="SYN-TEST/1", provision="SYN-01:3.1", type="replace_unit", target="SYN-01:T9-1")
    assert a["engine"].subject(op, a["state"]) == a2["engine"].subject(op, a2["state"])
    ba, ba2 = (review.row_binding(x["r"], x["r"]["evals"][0]) for x in (a, a2))
    assert review.fingerprint(ba) == review.fingerprint(ba2)


# ---------------------------------------------------------------------------------------------- the real pack

EVIDENCE, PACK = ROOT / "build", ROOT / "config/pack.yaml"


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


def _stage(r, name):
    return next(s for s in r["stages"] if s.stage == name)


def test_unit_test_of_the_pin_function_vol_i_table_1_1_row_b(real):
    """UNIT TEST of amend.unit_pin (not a rebuild): the pin of VOL-I:T1-1/B carries its document, page, box and
    spans, so the same words with a shifted box, another page, other spans or another document version pin
    differently. The two-build test above is the genuine one."""
    ev = review._evidence(real)
    st = _stage(real, "ADD-01").state                                    # immediately before ADD-02/3.1
    uid = "VOL-I:T1-1/B"
    assert ev[uid]["doc"] == "VOL-I" and ev[uid]["pages"] == [6] and ev[uid]["anchors"][0]["page"] == 6
    pin = unit_pin(st, uid, ev)
    assert pin == unit_pin(st, uid, copy.deepcopy(ev))
    for change in ("bbox", "page", "spans", "doc_sha256"):
        moved = copy.deepcopy(ev)
        a = moved[uid]["anchors"][0]
        if change == "bbox":
            a["bbox"][1] = f"{float(a['bbox'][1]) + 15:.1f}"
        elif change == "page":
            a["page"], moved[uid]["pages"] = 7, [7]
        elif change == "spans":
            a["spans"] = a["spans"][:-1]
        else:
            moved[uid]["doc_sha256"] = "0" * 64
        assert unit_pin(st, uid, moved) != pin, change
    assert unit_pin(st, uid) == pin_value(st, uid)                        # interpretation pins stay content-only
    manifest = json.loads((EVIDENCE / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))["inputs"]
    assert ev[uid]["doc_sha256"] == manifest["sources/candidate_pack/VOL-I_Instructions_to_Bidders.pdf"]


def test_unit_test_the_add_02_3_1_binding_names_its_documents(real):
    b = real["reviews"][("op", "ADD-02/3.1")]["binding"]
    assert "VOL-I:T1-1/B" in b["before"] and "ADD-02:T1-1-rev/B" in b["before"]
    manifest = json.loads((EVIDENCE / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))["inputs"]
    assert b["documents"] == {"ADD-02": manifest["sources/candidate_pack/ADD-02_Addendum_No_2.pdf"],
                              "VOL-I": manifest["sources/candidate_pack/VOL-I_Instructions_to_Bidders.pdf"]}


def _moved(r, uid, dy=15.0):
    r2 = copy.deepcopy(r)
    a = next(u for u in r2["units"] if u["unit_id"] == uid)["anchors"][0]
    a["bbox"] = [a["bbox"][0], a["bbox"][1] + dy, a["bbox"][2], a["bbox"][3] + dy]
    stage2.evaluate(r2)
    return r2


def test_unit_test_a_moved_source_voids_the_decisions_bound_to_it(real, tmp_path):
    """In-memory copies of the real pack with one box moved (labelled: not a rebuild). Disposable decisions only."""
    dec = tmp_path / "decisions.yaml"
    cfg = yaml.safe_load(PACK.read_text(encoding="utf-8"))
    cfg["decisions"] = str(dec)
    (tmp_path / "pack.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    r = stage2.run(EVIDENCE, tmp_path / "pack.yaml", ROOT)
    code, msgs = review.decide(r, ["ADD-02/3.1", "VOL-I-5.2-01"], "accept", WHO, "fixture: source binding", dec)
    assert code == 0, msgs
    r["decisions"] = review.load_decisions(dec)
    same = copy.deepcopy(r)
    stage2.evaluate(same)
    assert same["reviews"][("op", "ADD-02/3.1")]["status"] == "accepted"
    assert same["reviews"][("row", "VOL-I-5.2-01")]["status"] == "accepted"
    # Table 1-1 row B printed elsewhere with the same words: the decision on its replacement is void
    t11 = _moved(r, "VOL-I:T1-1/B")
    assert t11["reviews"][("op", "ADD-02/3.1")]["status"] == "changed"
    assert t11["reviews"][("row", "VOL-I-5.2-01")]["status"] == "accepted"          # not a dependency of that row
    assert _stage(t11, "ADD-02").state["VOL-I:T1-1/B"].status == "superseded"      # the op still applies
    # the Proposal Due Date clause printed elsewhere: a dependency (not one of the row's own units) of VOL-I-5.2-01
    pdd = _moved(r, "VOL-I:6.1")
    assert "VOL-I:6.1" not in pdd["reviews"][("row", "VOL-I-5.2-01")]["binding"]["source"]
    assert pdd["reviews"][("row", "VOL-I-5.2-01")]["status"] == "changed"
    assert pdd["reviews"][("op", "ADD-02/3.1")]["status"] == "accepted"
    assert not any(e["stages"][st]["stale"] for e in pdd["evals"] for st in pdd["order"]
                   if e["row"].id == "VOL-I-5.2-01")                              # same words: no new reading needed
