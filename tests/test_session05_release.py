"""Session 05: working drafts vs strict release, A3 readability, full-register coverage.

Structurally checked does not mean approved: a strict release is refused while coverage is incomplete,
interpretations are stale or approvals are pending, and the program never approves anything itself.
"""
from __future__ import annotations

import json

import pymupdf
import pytest

from tenderpack import stage2
from tenderpack.dispositions import effective_disposition
from tenderpack.util import ROOT

EVIDENCE, PACK = ROOT / "build", ROOT / "config/pack.yaml"


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


def test_strict_release_is_refused_and_keeps_the_previous_outputs(tmp_path):
    out = tmp_path / "out"
    first = stage2.build(EVIDENCE, out, PACK, ROOT, quiet=True)
    assert first["exit_code"] == 0 and first["release"].startswith("WORKING DRAFT")
    before = (out / "a1/a1.json").read_bytes()
    res = stage2.build(EVIDENCE, out, PACK, ROOT, quiet=True, strict=True)
    assert res["exit_code"] == 3 and res["status"] == "release_refused"
    assert (out / "a1/a1.json").read_bytes() == before                       # previous outputs untouched
    reason = (tmp_path / "out.rejected/RELEASE_REJECTED.md").read_text(encoding="utf-8")
    assert "stale" in reason and "approval" in reason and "image readings pending" in reason
    assert not (ROOT / "curation/approvals.yaml").exists()


def test_release_blockers_name_each_kind(real):
    kinds = {b["kind"] for b in stage2.release_blockers(real)}
    assert {"stale", "approval"} <= kinds
    details = " ".join(b["detail"] for b in stage2.release_blockers(real))
    assert "not accepted by a person" in details and "VOL-I-8.3-01" in details


def test_the_gate_opens_only_when_everything_is_reviewed(real):
    """In memory only: the gate's own logic, with every review simulated. Nothing is written."""
    import copy
    from tenderpack import review
    r = copy.deepcopy(real)
    assert stage2.release_blockers(r)
    for e in r["evals"]:
        for ev in e["stages"].values():
            ev["stale"] = []
    # session 06: acceptance is a named decision bound to each item's current fingerprint (flags do not count)
    decisions = [{"kind": k, "item": i, "decision": "accept", "reviewer": "Fixture Test Reviewer", "fingerprint": v["fingerprint"]}
                 for (k, i), v in r["reviews"].items()]
    r["reviews"] = review.compute(r, decisions)
    assert {b["kind"] for b in stage2.release_blockers(r)} == {"approval"}       # the readings are still pending
    for u in r["units"]:
        if (u.get("reading") or {}).get("status") == "pending":
            u["reading"]["status"] = "approved"
    assert stage2.release_blockers(r) == []


def test_incomplete_coverage_blocks_a_release(real):
    import copy
    r = copy.deepcopy(real)
    gone = next(k for k, d in r["dispositions"].items() if d.disposition == "informational")
    del r["dispositions"][gone]
    from tenderpack.dispositions import check_dispositions
    r["disposition_problems"] = check_dispositions(r["units"], r["dispositions"], r["rowfile"].rows)
    assert any(b["kind"] == "coverage" and "disposition" in b["detail"] for b in stage2.release_blockers(r))


def test_every_volume_unit_has_a_disposition_and_every_row_an_owner(real):
    vol = [u for u in real["units"] if not u["doc"].startswith("ADD-")]
    assert all(effective_disposition(u, real["dispositions"]) is not None for u in vol)
    assert real["disposition_problems"] == []
    assert all(e["row"].owner_role for e in real["evals"])
    assert stage2.register_findings(real) == []
    c14, c15 = real["sweeps"]
    assert c15 == []                                                  # every consequence word is linked


def test_consequence_sweeps_catch_an_unlinked_consequence_in_english_and_arabic(real):
    """C15 is an omission sweep: a consequence word that no row quotes and no disposition explains is a finding
    (and blocks a release), in either language. C14 lists obligation words in non-requirement units for a person."""
    import copy
    from tenderpack.dispositions import UnitDisposition, check_sweeps
    units = real["units"] + [
        {"unit_id": "VOL-I:SYN-EN", "doc": "VOL-I", "kind": "clause", "text": "A late notice shall be disregarded."},
        {"unit_id": "VOL-IV:SYN-AR", "doc": "VOL-IV", "kind": "paragraph", "text": "أي نقص في المستندات يؤدي إلى رفض العرض."},
    ]
    disp = {**real["dispositions"], "VOL-I:SYN-EN": UnitDisposition(disposition="informational", reason="synthetic"),
            "VOL-IV:SYN-AR": UnitDisposition(disposition="informational", reason="synthetic")}
    c14, c15 = check_sweeps(units, disp, real["rowfile"].rows)
    assert {(h["unit"], h["lang"]) for h in c15} == {("VOL-I:SYN-EN", "en"), ("VOL-IV:SYN-AR", "ar")}
    assert any(h["unit"] == "VOL-I:SYN-EN" and h["word"] == "shall" for h in c14)
    # the pack's own Arabic consequence (Form 4-C declaration 4, image) is caught once no row quotes it
    decl4 = "VOL-IV:F4-C/image/decl4"
    rows = [r for r in real["rowfile"].rows
            if not any(getattr(it.consequence, "unit", None) == decl4 for it in r.interpretations)]
    assert len(rows) < len(real["rowfile"].rows)
    _, c15_real = check_sweeps(real["units"], real["dispositions"], rows)
    assert (decl4, "ar") in {(h["unit"], h["lang"]) for h in c15_real}
    r = copy.deepcopy(real)
    r["sweeps"] = (c14, c15)
    assert any(b["kind"] == "coverage" and "C15" in b["detail"] for b in stage2.release_blockers(r))


def test_no_addendum_provision_is_left_outside_the_slice(real):
    for s in real["stages"][1:]:
        assert {c["disposition"] for c in s.coverage} <= {"op", "no_effect"}
    import yaml
    for a in ("ADD-01", "ADD-02"):
        assert "outside_slice" not in (ROOT / f"curation/amendments/{a}.yaml").read_text(encoding="utf-8")


def test_a3_is_readable_with_linked_detail(tmp_path, real):
    res = stage2.write(real, tmp_path / "out")
    assert res["a3_fit"]["min_text_pt"] >= 7.5
    doc = pymupdf.open(tmp_path / "out/a3/a3.pdf")
    assert len(doc) == 1
    raw = " ".join(doc.xref_object(l["xref"]) for l in doc[0].get_links())
    links = [m for m in __import__("re").findall(r"/URI \(([^)]*)\)", raw)]          # /URI actions, not /Launch
    assert "/Launch" not in raw
    detail = (tmp_path / "out/a3/a3_detail.html").read_text(encoding="utf-8")
    a3 = json.loads((tmp_path / "out/a3/a3.json").read_text(encoding="utf-8"))
    for x in a3["explicit"]:
        assert f"a3_detail.html#{x['id']}" in links and f'id="{x["id"]}"' in detail
        assert x["consequence"].replace("&", "&amp;")[:30] in detail or x["consequence"][:30] in detail
    assert a3["missing"]["items"] and any(i["id"] == "I-VOL-III" for i in a3["missing"]["items"])
