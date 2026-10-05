"""Session 11: statements the outputs print about the readings' review status must come from the build, not from a
fixed sentence. The real pack's `out/README.md` said "image readings are PENDING the owner's review" after both
readings had been approved (curation/approvals.yaml, 3 Oct 2026)."""
from tenderpack import stage2


def _cov(statuses):
    return {"pending_review": [i for i, s in statuses.items() if s != "approved"],
            "regions": [{"id": i, "kind": "image", "reading_status": s, "reading_units": 3} for i, s in statuses.items()]}


def test_readme_sentence_reports_approved_readings_as_approved():
    s = stage2.readings_status_sentence(_cov({"VOL-II-p3-r1": "approved", "VOL-IV-p6-r1": "approved"}))
    assert "approved" in s and "PENDING" not in s
    assert "VOL-II-p3-r1" in s and "VOL-IV-p6-r1" in s


def test_readme_sentence_reports_pending_readings_as_pending():
    s = stage2.readings_status_sentence(_cov({"VOL-II-p3-r1": "approved", "VOL-IV-p6-r1": "pending"}))
    assert "PENDING" in s and "VOL-IV-p6-r1" in s
    assert "approved" in s and "VOL-II-p3-r1" in s


def test_readme_sentence_without_image_readings():
    s = stage2.readings_status_sentence({"pending_review": [], "regions": []})
    assert "no image readings" in s


# --- stage2 must hand the recorded trigger facts to the engine (session 11, D3's note: without this a recorded
# trigger is never read and a conditional op can never be applied through a build)

def test_stage2_engine_reads_recorded_triggers(tmp_path):
    (tmp_path / "curation").mkdir()
    (tmp_path / "curation" / "triggers.yaml").write_text(
        "triggers:\n  - condition: ADD-03/S7\n    occurred: true\n    date: 2026-11-10\n    recorded_by: Fixture Test Reviewer\n"
        "    evidence: [{unit: 'ADD-03:7.1', words: 'notice'}]\n", encoding="utf-8")
    eng = stage2.engine_for({"units": [], "opfiles": [], "decisions": [], "cfg": {}, "root": tmp_path})
    assert "ADD-03/S7" in eng.triggers and eng.triggers["ADD-03/S7"]["occurred"] is True


def test_stage2_engine_without_a_triggers_file_has_no_triggers(tmp_path):
    eng = stage2.engine_for({"units": [], "opfiles": [], "decisions": [], "cfg": {}, "root": tmp_path})
    assert eng.triggers == {}


# --- a candidate workspace must copy the recorded trigger facts (D1's note: candidate.PACK_PATHS lacked `triggers`, so
# a candidate read the real curation/triggers.yaml instead of its own copy)

def test_candidate_copies_the_triggers_file():
    from tenderpack.ai import candidate
    assert candidate.PACK_PATHS.get("triggers") == ("file", "curation/triggers.yaml")
    real = candidate.real_inputs({}) if hasattr(candidate, "real_inputs") else None
    if real is not None:
        assert any(str(p).endswith("curation/triggers.yaml") for p in real)
