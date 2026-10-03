"""The named accept workflow (session 06): decisions bound to content, evidence and dependencies.

Every decision here is written to a disposable decisions file by "Fixture Test Reviewer"; proposals are applied
only to a disposable copy of the register. Nothing is accepted, rejected, applied or refreshed in the repository.
"""
from __future__ import annotations

import copy
import shutil
from pathlib import Path

import pytest
import yaml

from tenderpack import review, stage2
from tenderpack.proposals import apply_proposal, load_proposals
from tenderpack.util import ROOT

EVIDENCE, PACK = ROOT / "build", ROOT / "config/pack.yaml"
WHO = "Fixture Test Reviewer"


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


def _rerun(r, path):
    r = copy.deepcopy(r)
    r["decisions"] = review.load_decisions(path)
    r["reviews"] = review.compute(r, r["decisions"])
    return r


def test_a_bound_decision_is_the_only_acceptance(real, tmp_path):
    path = tmp_path / "decisions.yaml"
    code, msgs = review.decide(real, ["VOL-I-9.3-01", "ADD-02/9.1"], "accept", WHO, "checked against p5", path)
    assert code == 0, msgs
    r = _rerun(real, path)
    assert r["reviews"][("row", "VOL-I-9.3-01")]["status"] == "accepted"
    assert r["reviews"][("op", "ADD-02/9.1")]["status"] == "accepted"
    assert review.label(r["reviews"][("row", "VOL-I-9.3-01")]).startswith(f"accepted by {WHO}")
    approval = " ".join(b["detail"] for b in stage2.release_blockers(r) if b["kind"] == "approval")
    assert f"{len(r['evals']) - 1} of {len(r['evals'])} register rows not accepted" in approval
    entry = yaml.safe_load(path.read_text())["decisions"][0]
    assert entry["fingerprint"] and "VOL-I:9.3" in entry["bound_to"]["dependencies"]
    assert not (ROOT / "curation/reviews/decisions.yaml").exists()


def test_changed_row_content_needs_review_again(real, tmp_path):
    path = tmp_path / "decisions.yaml"
    assert review.decide(real, ["VOL-I-9.3-01"], "accept", WHO, None, path)[0] == 0
    r = copy.deepcopy(real)
    row = next(e["row"] for e in r["evals"] if e["row"].id == "VOL-I-9.3-01")
    row.requirement += " (edited)"
    r = _rerun(r, path)
    st = r["reviews"][("row", "VOL-I-9.3-01")]
    assert st["status"] == "changed" and "CHANGED since: review again" in review.label(st)


def test_a_changed_dependency_needs_review_again(real, tmp_path):
    path = tmp_path / "decisions.yaml"
    assert review.decide(real, ["VOL-I-9.3-01"], "accept", WHO, None, path)[0] == 0
    r = copy.deepcopy(real)
    for s in r["stages"][1:]:
        s.state["VOL-I:9.3"].text += " Amended."
    assert _rerun(r, path)["reviews"][("row", "VOL-I-9.3-01")]["status"] == "changed"


def test_a_changed_evidence_item_needs_review_again(real, tmp_path):
    path = tmp_path / "decisions.yaml"
    assert review.decide(real, ["VOL-I-9.3-01"], "accept", WHO, None, path)[0] == 0
    r = copy.deepcopy(real)
    ev = next(e["row"] for e in r["evals"] if e["row"].id == "VOL-I-9.3-01").evidence[0]
    r["evidence_items"][ev].issuer = "someone else"
    assert _rerun(r, path)["reviews"][("row", "VOL-I-9.3-01")]["status"] == "changed"


def test_refusals_write_nothing(real, tmp_path):
    path = tmp_path / "decisions.yaml"
    assert review.decide(real, ["VOL-I-9.3-01"], "accept", "<name>", None, path)[0] == 2
    assert review.decide(real, ["VOL-I-9.3-01"], "reject", WHO, None, path)[0] == 2           # a rejection needs a note
    assert review.decide(real, ["VOL-I-8.3-01"], "accept", WHO, None, path)[0] == 1           # STALE
    assert review.decide(real, ["VOL-I-9.3-01", "NO-SUCH-ROW"], "accept", WHO, None, path)[0] == 1
    assert not path.exists()


def test_a_rejected_op_is_withdrawn_and_its_addendum_is_partial(tmp_path):
    path = tmp_path / "decisions.yaml"
    r = stage2.run(EVIDENCE, PACK, ROOT)
    assert review.decide(r, ["ADD-02/8.1"], "reject", WHO, "wrong clause", path)[0] == 0
    cfg = yaml.safe_load(PACK.read_text())
    cfg["decisions"] = str(path)
    (tmp_path / "pack.yaml").write_text(yaml.safe_dump(cfg))
    r2 = stage2.run(EVIDENCE, tmp_path / "pack.yaml", ROOT)
    s = next(s for s in r2["stages"] if s.stage == "ADD-02")
    x = next(x for x in s.ops if x.op.id == "ADD-02/8.1")
    assert not x.valid and s.status == "PARTIAL" and r2["validated"].stage == "ADD-01"
    assert "SAR 5,000,000" in s.state["VOL-V:36.2"].text                                    # not applied
    assert r2["reviews"][("op", "ADD-02/8.1")]["status"] == "rejected"
    assert any("rejected: ADD-02/8.1" in b["detail"] for b in stage2.release_blockers(r2))


def test_a_stale_row_proposal_can_be_applied_then_reviewed(tmp_path):
    """In a disposable copy of the register only: apply the prepared proposal, the row is no longer STALE and is
    PROPOSED (not accepted); a named decision then accepts it."""
    reg = tmp_path / "register"
    shutil.copytree(ROOT / "curation/register", reg)
    cfg = yaml.safe_load(PACK.read_text())
    cfg.update({"register": str(reg / "rows.yaml"), "issues": str(reg / "issues.yaml"),
                "dispositions_dir": str(reg / "dispositions"), "decisions": str(tmp_path / "decisions.yaml")})
    (tmp_path / "pack.yaml").write_text(yaml.safe_dump(cfg))
    assert set(load_proposals(ROOT / "curation/register/proposals")) >= {"P-STALE-VOL-I-8.3-01", "P-STALE-VOL-I-3.4-01",
                                                                         "P-STALE-VOL-I-6.7-01"}
    assert apply_proposal("P-STALE-VOL-I-8.3-01", WHO, EVIDENCE, tmp_path / "pack.yaml", reg / "proposals", ROOT) == 0
    r = stage2.run(EVIDENCE, tmp_path / "pack.yaml", ROOT)
    ev = next(e for e in r["evals"] if e["row"].id == "VOL-I-8.3-01")
    assert not ev["stages"]["ADD-02"]["stale"] and r["reviews"][("row", "VOL-I-8.3-01")]["status"] == "proposed"
    assert review.decide(r, ["VOL-I-8.3-01"], "accept", WHO, None, tmp_path / "decisions.yaml")[0] == 0
    assert _rerun(r, tmp_path / "decisions.yaml")["reviews"][("row", "VOL-I-8.3-01")]["status"] == "accepted"
    # the repository's own register is untouched
    assert "P-STALE" not in (ROOT / "curation/register/rows.yaml").read_text()


def test_review_batches_cover_every_item_with_its_crops_and_command(real, tmp_path):
    import csv
    import re as _re
    from tenderpack.batches import write_batches
    res = write_batches(real, tmp_path / "review", EVIDENCE)
    items = list(csv.DictReader(open(tmp_path / "review/items.csv", encoding="utf-8")))
    ids = {(x["kind"], x["id"]) for x in items}
    assert {("reading", "VOL-II-p3-r1"), ("reading", "VOL-IV-p6-r1")} <= ids
    assert all(("row", e["row"].id) in ids for e in real["evals"])
    assert all(("op", x.op.id) in ids for s in real["stages"][1:] for x in s.ops)
    assert {x["id"] for x in items if x["kind"] == "proposal"} >= {"P-STALE-VOL-I-8.3-01", "P-STALE-VOL-I-3.4-01", "P-STALE-VOL-I-6.7-01"}
    b1 = (tmp_path / "review/batch-01-image-readings.html").read_text(encoding="utf-8")
    assert 'approve VOL-II-p3-r1 --reviewer "Your Name"' in b1 and "decimal point in 2.2" in b1
    b2 = (tmp_path / "review/batch-02-disqualifiers.html").read_text(encoding="utf-8")
    a3 = stage2.a3(real, stage2.collect_issues(real, None), None)
    for x in a3["explicit"] + a3["score"]:
        assert f'id="{x["id"]}"' in b2 and f'accept {x["id"]} --reviewer' in b2
    for src in _re.findall(r'src="(img/[^"]+)"', b1 + b2):
        assert (tmp_path / "review" / src).exists(), src
    assert all(x["status"] in ("proposed", "pending", "not applied") for x in items)        # nothing decided for the owner
    assert res["images"] > 50
