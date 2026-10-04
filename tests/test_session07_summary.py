"""Session 07: C28, each addendum's cover summary checked against its actual provisions (report only).

The summary ("This Addendum amends ..., deletes ..., and responds to ...") is the Authority's description of the
addendum, not an operative provision. It must never decide what is applied: ops come only from the provisions.
C28 compares the two and reports omissions and contradictions for a person.

The expectations for the real pack were written from the printed addenda (build/units.md), before C28 existed:

ADD-01 summary: amends the Proposal Due Date (2.1), deletes one qualification requirement (4.1, VOL-I 8.6),
  amends Volume II Clause 5.3 (5.1), publishes the minutes (Appendix B), responds to requests 1 to 6.
  Not in it: Appendix A reissues Form 4-A (VOL-IV F4-A replaced); 3.1 adds a duty to report a wrongly recorded
  attendance within five Working Days ("publishes the minutes" does not announce a duty). The answer to request 4
  adds a duty ("Bidders shall satisfy themselves as to ground conditions") under "responds to".
ADD-02 summary: page limit (2.1), technical evaluation table (3.1), VOL-II 4.4 and Table 2-4 (4.1, 5.1), Form 4-G
  (7.1), VOL-V 36.2 (8.1), reinstates VOL-I 8.6 (9.1), requests 7 to 14.
  Not in it: note (2) to the reissued table amends VOL-I 11.2 (weighting 60/40 -> 65/35); 9.2 ends ADD-01
  Section 4.2; 5.2 adds a process-design duty. 9.1 reinstates 8.6 "in the following amended form" (35% instead
  of 30%, and a new non-responsive consequence) while the summary says only "reinstates"; 7.2 makes a missing
  Form 4-G non-responsive, which "adds Form 4-G" does not say.
"""
from __future__ import annotations

import copy
import json
import sys

import pytest

from tenderpack import stage2
from tenderpack.amend import Engine
from tenderpack.cli import ingest
from tenderpack.draft import draft
from tenderpack.util import ROOT

sys.path.insert(0, str(ROOT / "tests/fixtures"))
import make_drill  # noqa: E402


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


def by_add(r):
    return {x["addendum"]: x for x in r["summary_check"]}


def kinds(sc):
    return {(f["kind"], f.get("op") or f.get("provision")) for f in sc["findings"]}


def test_real_add01_summary_claims_are_found_and_its_omissions_reported(real):
    sc = by_add(real)["ADD-01"]
    assert sc["cover"] == "ADD-01:cover/para3"
    assert [c["text"] for c in sc["claims"]] == [
        "amends the Proposal Due Date", "deletes one qualification requirement", "amends Volume II Clause 5.3",
        "publishes the minutes of the Pre-Bid Conference", "responds to clarification requests 1 to 6"]
    assert {c["status"] for c in sc["claims"]} == {"supported"}
    assert "ADD-01/4.1" in sc["claims"][1]["matched"] and "ADD-01/2.1" in sc["claims"][0]["matched"]
    assert kinds(sc) == {("omitted", "ADD-01/AppA/para1"), ("omitted", "ADD-01/3.1"), ("understated", "ADD-01/Q4")}
    omitted = next(f for f in sc["findings"] if f.get("op") == "ADD-01/AppA/para1")
    assert "VOL-IV:F4-A" in omitted["detail"]


def test_real_add02_hidden_changes_in_a_table_note_and_a_revocation_are_reported(real):
    sc = by_add(real)["ADD-02"]
    assert len(sc["claims"]) == 7 and {c["status"] for c in sc["claims"]} == {"supported"}
    assert kinds(sc) == {("omitted", "ADD-02/T1-1-rev/note(2)"), ("omitted", "ADD-02/9.2"), ("omitted", "ADD-02/5.2"),
                         ("understated", "ADD-02/9.1"), ("consequence not mentioned", "ADD-02/9.1"),
                         ("consequence not mentioned", "ADD-02/7.2")}
    f = {(x["kind"], x.get("op")): x["detail"] for x in sc["findings"]}
    assert "VOL-I:11.2" in f[("omitted", "ADD-02/T1-1-rev/note(2)")]
    assert "amended form" in f[("understated", "ADD-02/9.1")]
    assert "non-responsive" in f[("consequence not mentioned", "ADD-02/7.2")]


def test_c28_is_reported_never_structural_and_reaches_a2_and_the_issues(real, tmp_path):
    rep = [c for c in stage2.reported_checks(real) if c["id"] == "C28"]
    assert [c["stage"] for c in rep] == ["ADD-01", "ADD-02"] and not any(c["ok"] for c in rep)
    out = stage2.write(real, tmp_path / "out")
    assert out["status"] == "ok"
    checks = json.loads((tmp_path / "out/checks.json").read_text(encoding="utf-8"))
    assert "C28" not in {c["id"] for c in checks["structural"]}
    assert not any("C28" in b["detail"] for b in checks["release"]["blockers"])          # report only
    a2 = (tmp_path / "out/a2/a2.md").read_text(encoding="utf-8")
    assert "Cover summary vs provisions (C28)" in a2 and "never applied" in a2
    assert "ADD-02/T1-1-rev/note(2)" in a2.split("Cover summary vs provisions (C28)")[2]
    issues = json.loads((tmp_path / "out/a1/a1.json").read_text(encoding="utf-8"))["sheets"]["Issues"]
    assert "I-AUTO-SUMMARY-ADD-02" in json.dumps(issues)


def test_a_misleading_summary_changes_nothing_that_is_applied(real):
    """Same provisions, a summary that lies: every unit's effective text and status is identical at every stage."""
    units = copy.deepcopy(real["units"])
    cover = next(u for u in units if u["unit_id"] == "ADD-02:cover/para3")
    cover["text"] = ("This Addendum deletes Volume I Clause 8.6, amends Volume I Clause 6.1 and Volume II Clause 5.3, "
                     "and responds to clarification requests 7 to 20. Bidders shall acknowledge receipt in Form 4-A.")
    a = Engine(real["units"], real["opfiles"]).run()
    b = Engine(units, real["opfiles"]).run()
    for sa, sb in zip(a, b):
        assert sa.status == sb.status and [x.op.id for x in sa.ops] == [x.op.id for x in sb.ops]
        for k, ua in sa.state.items():
            if k == "ADD-02:cover/para3":
                continue
            assert (ua.text, ua.status) == (sb.state[k].text, sb.state[k].status), k
    from tenderpack.summary import summary_check
    sc = {x["addendum"]: x for x in summary_check(b, units)}["ADD-02"]
    ks = kinds(sc)
    assert ("contradicted", "ADD-02/9.1") in ks                    # says deletes 8.6; the body reinstates it
    assert any(k == "not found" for k, _ in ks)                    # VOL-I 6.1 and VOL-II 5.3: no ADD-02 provision
    assert any(k == "contradicted" and "20" in f["detail"] for f in sc["findings"] for k in [f["kind"]])
    assert ("omitted", "ADD-02/8.1") in ks and ("omitted", "ADD-02/2.1") in ks


def test_the_drafter_never_drafts_a_change_from_cover_text(real):
    units = copy.deepcopy(real["units"])
    cover = next(u for u in units if u["unit_id"] == "ADD-02:cover/para3")
    cover["text"] = ("This Addendum deletes Volume I Clause 10.5. Volume I Clause 10.6 is deleted in its entirety. "
                     "Bidders shall acknowledge receipt in Form 4-A.")
    f = draft(units, "ADD-02")
    from_cover = [o for o in f.ops if o.provision == "ADD-02:cover/para3"]
    assert all(o.type == "annotate" and o.effect == "adds_obligation" for o in from_cover)
    assert not any(o.target in ("VOL-I:10.5", "VOL-I:10.6") for o in f.ops)
    d = [x for x in f.dispositions if x.provision == "ADD-02:cover/para3"]
    assert d and d[0].disposition == "unresolved" and "10.6" in d[0].reason


MISLEADING = ("This Addendum amends the Proposal Due Date and Volume II Clause 4.4, reinstates Volume I Clause 8.6, "
              "deletes Volume V Clause 31.3, adds Form 4-H, and responds to clarification requests 15 to 18.")


@pytest.fixture(scope="module")
def drills(tmp_path_factory):
    out = {}
    for name, front in (("truthful", None), ("misleading", [MISLEADING] + make_drill.FRONT[1:])):
        base = tmp_path_factory.mktemp(f"drill-{name}")
        make_drill.build(base / "src", front=front)
        res = ingest(base / "src/pack.yaml", base / "evidence", ROOT, quiet=True)
        assert res["exit_code"] == 0
        r = stage2.run(base / "evidence", base / "src/pack.yaml", ROOT)
        out[name] = {"r": r, "base": base, "out": stage2.write(r, base / "out")}
    return out


def test_synthetic_misleading_summary_end_to_end(drills):
    t, m = drills["truthful"]["r"], drills["misleading"]["r"]
    # the summary never decides what is applied: the same ops are drafted and the same state results
    ops = lambda r: [(x.op.id, x.op.type, x.op.target, x.op.old, x.op.new, x.valid) for x in r["stages"][-1].ops]  # noqa: E731
    assert ops(t) == ops(m)
    for st_t, st_m in zip(t["stages"], m["stages"]):
        assert st_t.status == st_m.status
        for k, u in st_t.state.items():
            if k != "ADD-03:cover/para3":
                assert (u.text, u.status) == (st_m.state[k].text, st_m.state[k].status), k
    # truthful summary: nothing omitted or contradicted; what cannot be checked is said so
    st_ = by_add(t)["ADD-03"]
    assert {f["kind"] for f in st_["findings"]} == {"claimed, not applied", "unchecked"}
    assert ("claimed, not applied", "ADD-03/7.1") in kinds(st_)
    # misleading summary: every planted error is reported
    sm = by_add(m)["ADD-03"]
    ks = kinds(sm)
    assert ("contradicted", "ADD-03/4.1") in ks                    # "reinstates 8.6"; the body deletes it
    assert ("contradicted", "ADD-03/3.1") in ks                    # "deletes 31.3"; the body amends it
    assert ("omitted", "ADD-03/5.1") in ks                         # Table 2-4 TP change not mentioned
    assert ("claimed, not applied", "ADD-03/7.1") in ks            # claimed VOL-II 4.4; its op is invalid
    nf = [f for f in sm["findings"] if f["kind"] == "not found"]
    assert len(nf) == 1 and "Form 4-H" in nf[0]["detail"]
    rng = [f for f in sm["findings"] if f["kind"] == "contradicted" and "clarification" in f["detail"]]
    assert len(rng) == 1 and "15 to 18" in rng[0]["detail"] and "15, 16" in rng[0]["detail"]
    assert {p for k, p in ks if k == "unchecked"} == {"ADD-03:6.1", "ADD-03:Q15", "ADD-03:Q16"}
    a2 = (drills["misleading"]["base"] / "out/a2/a2.md").read_text(encoding="utf-8")
    assert "Form 4-H" in a2 and "never applied" in a2


def test_blind_addendum_summary_omissions_match_the_sealed_key(blind01_run):
    """Regression on rehearsal 01 (NOT blind evidence: C28 was written after the key was unsealed). The key's trap for
    the cover (SEALED/expected_findings.yaml, cover_text.traps) lists what the summary omits: 2.3, 3.2, 8.2, 9.2, the
    change inside the answer to Q16 and the new restriction in Q17. Each must be reported."""
    import yaml
    b = ROOT / "rehearsals/blind-01"
    key = yaml.safe_load((b / "SEALED/expected_findings.yaml").read_text(encoding="utf-8"))
    trap = key["cover_text"]["traps"][0]["correct"]
    for n in ("2.3", "3.2", "8.2", "9.2", "Q16", "Q17"):
        assert n in trap
    r = blind01_run                    # a fresh, disposable ingest of b/work/pack.yaml (its exit code 0 is asserted there)
    sc = by_add(r)["ADD-03"]
    flagged = {f.get("op") for f in sc["findings"] if f["kind"] in ("omitted", "understated")}
    assert {"ADD-03/2.3", "ADD-03/3.2", "ADD-03/8.2", "ADD-03/9.2", "ADD-03/Q16", "ADD-03/Q17"} <= flagged
    assert {c["status"] for c in sc["claims"]} == {"supported"}       # every claim in that summary is true
    assert not any(f["kind"] in ("contradicted", "not found") for f in sc["findings"])


def test_review_folder_carries_the_full_reading_packets_with_crops(real, tmp_path):
    """The owner reviews from out/review alone (or the archive's REVIEW/): the Stage 1 packets of both image readings
    (Table 2-4 cells; the Arabic Form 4-C bands and numerals) are copied there, self-contained, and linked."""
    from tenderpack.batches import write_batches
    out = tmp_path / "review"
    write_batches(real, out, ROOT / "build")
    for rg in ("VOL-II-p3-r1", "VOL-IV-p6-r1"):
        page = (out / "packets" / f"{rg}.html").read_text(encoding="utf-8")
        assert "APPROVED by Ahmad" in page and "Does not cover" in page                 # the owner's confirmations
        assert "data:image/png;base64," in page and 'src="http' not in page
        assert f'href="packets/{rg}.html"' in (out / "batch-01-image-readings.html").read_text(encoding="utf-8")
        assert f'href="packets/{rg}.html"' in (out / "index.html").read_text(encoding="utf-8")
    assert 'dir="rtl"' in (out / "packets/VOL-IV-p6-r1.html").read_text(encoding="utf-8")
