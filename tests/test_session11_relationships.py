"""Session 11, owner's section 3: relationships beyond the curated examples, traversed without a silent stop.

1. trace() stopped after four links without saying so (MAX_DEPTH = 4): an indirect chain looked complete when it was
   not. The traversal is now cycle-safe (a visited set per path) and every record says whether its path is complete,
   truncated by the configured bound (reported, never silent) or cyclic.
2. A missing-document blocker disappeared when its blocked target was reached only indirectly: the gap entry was
   reported only when its own `from` or its target changed directly. A target reached through a blocked node now
   carries the blocker ("cannot be established: <document> not supplied") along the chain.
3. discover(units) proposes `proposed` entries from the documents' own cross-references, never confirmed.

Each regression failed before its fix. Synthetic entries; the real pack's committed build is only read.
"""
from __future__ import annotations

import pytest

from tenderpack import relationships as R


def link(i: int, frm: str, to: str, **kw) -> dict:
    e = {"id": f"REL-{i}", "from": frm, "to": to, "kind": "depends_on", "status": "confirmed",
         "evidence": [{"unit": "VOL-X:1.1", "page": 1, "words": "x"}], "origin": "curator", "review": "proposed"}
    e.update(kw)
    return e


def chain(n: int) -> list[dict]:
    """N0 -> N1 -> ... -> Nn, one link each."""
    return [link(i, f"N{i - 1}", f"N{i}") for i in range(1, n + 1)]


# ---------------------------------------------------------------------------------------------- 1. completeness

def test_a_chain_of_five_links_reaches_its_target_and_says_it_is_complete():
    recs = R.trace(chain(5), {"N0"})
    by = {r["target"]: r for r in recs}
    assert "N5" in by, sorted(by)                               # session 10 stopped at N4 without a word
    assert by["N5"]["path"] == ["REL-1", "REL-2", "REL-3", "REL-4", "REL-5"]
    assert all(r["completeness"] == "complete" and r["chain_complete"] for r in recs)


def test_a_configured_bound_is_reported_never_silent():
    recs = R.trace(chain(5), {"N0"}, max_depth=3)
    by = {r["target"]: r for r in recs}
    assert set(by) == {"N1", "N2", "N3"}
    cut = by["N3"]
    assert cut["completeness"] == "truncated" and not cut["chain_complete"]
    assert cut["unfollowed"] == ["REL-4"] and cut["bound"] == 3
    assert by["N2"]["completeness"] == "complete"
    s = R.completeness(recs)
    assert s["complete"] is False and s["truncated"] == ["N3"]
    assert "CHAIN INCOMPLETE" in R.label(cut) and "REL-4" in R.label(cut)
    assert "CHAIN INCOMPLETE" not in R.label(by["N2"])


def test_a_cycle_is_followed_once_and_labelled_cyclic():
    ents = chain(3) + [link(9, "N3", "N1")]                     # N1 -> N2 -> N3 -> N1
    recs = R.trace(ents, {"N0"})
    back = [r for r in recs if r["path"][-1] == "REL-9"]
    assert len(back) == 1 and back[0]["completeness"] == "cyclic" and back[0]["chain_complete"]
    assert back[0]["cycle"] == ["N1", "N2", "N3", "N1"]
    assert len(recs) == 4                                       # nothing followed round the loop again
    assert R.completeness(recs)["cyclic"] == ["N1"]


def test_completeness_survives_into_impact_and_reach():
    recs = R.trace(chain(6), {"N0"}, max_depth=2)
    assert R.reach(chain(6), {"N0"}).keys() >= {"N6"}           # reach uses the default bound
    assert R.completeness(recs)["truncated"] == ["N2"]


# ---------------------------------------------------------------------------------------------- 2. blockers

GAP = {"id": "REL-GAP", "from": "VOL-X:9.2", "to": ["ROW-TERM"], "kind": "missing_document", "status": "confirmed",
       "document": "Schedule 4", "document_id": "SCH-4", "blocks": "which events terminate",
       "evidence": [{"unit": "VOL-X:9.2", "page": 2, "words": "listed in Schedule 4"}], "origin": "curator",
       "review": "proposed"}


def test_a_target_reached_through_a_blocked_node_carries_the_blocker():
    ents = [link(1, "VOL-X:9.1", "ROW-PRICE"), link(2, "ROW-PRICE", "ROW-TERM"), link(3, "ROW-TERM", "ROW-MODEL"), GAP]
    recs = R.trace(ents, {"VOL-X:9.1"})
    by = {r["target"]: r for r in recs}
    assert set(by) == {"ROW-PRICE", "ROW-TERM", "ROW-MODEL"}
    for t in ("ROW-TERM", "ROW-MODEL"):                        # the blocked node itself and what is reached through it
        bl = by[t].get("blockers") or []
        assert [b["document_id"] for b in bl] == ["SCH-4"], (t, by[t])
        assert bl[0]["node"] == "ROW-TERM" and bl[0]["entry_id"] == "REL-GAP"
        assert bl[0]["text"] == "cannot be established: Schedule 4 not supplied (which events terminate)"
        assert "cannot be established: Schedule 4 not supplied" in R.label(by[t])
    assert not by["ROW-PRICE"]["blockers"]
    assert {r["target"] for r in R.blocked(recs)} == {"ROW-TERM", "ROW-MODEL"}
    assert R.gaps(recs) == []                                   # the gap entry itself was not in play: not a gap record


def test_a_blocked_changed_source_blocks_what_it_reaches():
    ents = [link(1, "ROW-TERM", "ROW-MODEL"), GAP]
    recs = R.trace(ents, {"ROW-TERM"})
    model = next(r for r in recs if r["target"] == "ROW-MODEL")
    assert [b["node"] for b in model["blockers"]] == ["ROW-TERM"]
    assert [g["target"] for g in R.gaps(recs)] == ["ROW-TERM"]  # reported as before (its blocked target changed)


# ---------------------------------------------------------------------------------------------- the real pack

@pytest.fixture(scope="module")
def real():
    from tenderpack import stage2
    from tenderpack.util import ROOT
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


def test_the_real_pack_permit_blocker_now_reaches_the_row_found_only_indirectly(real):
    """ADD-02 changes Table 2-4; VOL-II-2.4-01 is reached through REL-T24-COMPLIANCE-MONITORING-STREAMS, and the
    Environmental Permit (not supplied) blocks it: session 10 dropped that blocker because the row did not change
    directly."""
    imp = real["relationship_impact"]["ADD-02"]
    assert imp["completeness"]["complete"] and imp["completeness"]["truncated"] == []
    rec = next(x for x in imp["records"] if x["target"] == "VOL-II-2.4-01" and x["kind"] != "missing_document")
    assert not rec["direct"] and rec["blocked"]
    assert [b["document_id"] for b in rec["blockers"]] == ["ENVIRONMENTAL-PERMIT"]
    assert "VOL-II-2.4-01" in imp["blocked"]
    assert "BLOCKED: cannot be established: the Environmental Permit issued for the site not supplied" in R.label(rec)
    from tenderpack import stage2
    tp = next(a for a in stage2.a5_all(real)["ADD-02"]["activities"] if a["id"] == "technical-proposal")
    assert any(f.startswith("REVIEW (confirmed dependency)") and "BLOCKED: cannot be established: the Environmental "
               "Permit" in f for f in tp["flags"])


# ---------------------------------------------------------------------------------------------- 3. discovery

SYN = [
    {"unit_id": "VOL-V:1.3", "doc": "VOL-V", "kind": "clause", "pages": [2],
     "text": "Estimated Project Cost means the aggregate capital cost of the Facility."},
    {"unit_id": "VOL-V:18.4", "doc": "VOL-V", "kind": "clause", "pages": [2],
     "text": "The aggregate liability shall not exceed ten per cent (10%) of the Estimated Project Cost."},
    {"unit_id": "VOL-V:29.1", "doc": "VOL-V", "kind": "clause", "pages": [3],
     "text": "The Authority shall pay the Availability Payment, subject to the deductions in Clause 31."},
    {"unit_id": "VOL-V:31.1", "doc": "VOL-V", "kind": "clause", "pages": [3], "text": "An Unavailability Event occurs."},
    {"unit_id": "VOL-V:39.1", "doc": "VOL-V", "kind": "clause", "pages": [4],
     "text": "The Authority may terminate for the events listed in Schedule 11."},
    {"unit_id": "VOL-V:40.1", "doc": "VOL-V", "kind": "clause", "pages": [4],
     "text": "The comparison required by this Clause shall be made."},
    {"unit_id": "VOL-I:10.2", "doc": "VOL-I", "kind": "clause", "pages": [5],
     "text": "The price shall be calculated in accordance with the payment mechanism at Volume V Clause 29."},
    {"unit_id": "ADD-03:4.1", "doc": "ADD-03", "kind": "clause", "pages": [1],
     "text": "In Volume V Clause 18.1, the rate is subject to Volume V Clause 18.4 and the Estimated Project Cost."},
]


def test_discovery_proposes_links_from_the_documents_own_words_and_never_confirms():
    res = R.discover(SYN, rows=[{"id": "VOL-V-18.4-01", "units": ["VOL-V:18.4"]}])
    got = {(tuple(e["from"]), e["to"][0]): e for e in res["entries"]}
    defn = got[(("VOL-V:1.3",), "VOL-V:18.4")]
    assert defn["kind"] == "depends_on" and defn["to"] == ["VOL-V:18.4", "VOL-V-18.4-01"]
    assert {"unit": "VOL-V:18.4", "page": 2, "words": "ten per cent (10%) of the Estimated Project Cost"} in defn["evidence"]
    calc = got[(("VOL-V:29.1",), "VOL-I:10.2")]
    assert calc["kind"] == "feeds_calculation"
    assert calc["evidence"][0]["words"] == "calculated in accordance with the payment mechanism at Volume V Clause 29"
    sub = got[(("VOL-V:31.1",), "VOL-V:29.1")]                 # a bare 'Clause 31' takes the unit's own volume
    assert sub["kind"] == "depends_on" and sub["evidence"][0]["words"] == "subject to the deductions in Clause 31"
    assert not any(e["to"][0] == "VOL-V:40.1" for e in res["entries"])          # 'required by this Clause': itself
    assert not any(e["to"][0].startswith("ADD-") for e in res["entries"])       # addenda are amendment targets
    assert res["unresolved"] == [{"unit": "VOL-V:39.1", "page": 4, "words": "listed in Schedule 11",
                                  "reference": "Schedule 11"}]
    for e in res["entries"]:
        assert e["status"] == "proposed" and e["origin"] == "discover" and e["review"] == "proposed" and e["basis"]
        assert e["id"].startswith("REL-DISC-")
    assert R.validate(res["entries"], SYN, ["VOL-V-18.4-01"], {}) == []
    again = R.discover(SYN, existing=[{"id": "REL-X", "from": "VOL-V:1.3", "to": "VOL-V:18.4", "kind": "cites"}])
    assert not any(e["to"][0] == "VOL-V:18.4" for e in again["entries"]) and len(again["already_curated"]) == 1
    capped = R.discover(SYN, max_term_uses=0)
    assert capped["skipped_terms"] == {"Estimated Project Cost": 1}


def test_discovery_on_the_real_pack_and_the_cli_writes_a_new_file_for_a_person(real, tmp_path):
    import hashlib

    from tenderpack.cli import main
    from tenderpack.util import ROOT
    res = R.discover(real["units"], real["rowfile"].rows, real["relationships"])
    assert len(res["entries"]) >= 40
    assert R.validate(res["entries"], real["units"], real["rowfile"].rows, real["templates"],
                      evidence_items=real["evidence_items"]) == []
    links = {(tuple(e["from"]), e["to"][0]) for e in res["entries"]}
    assert (("VOL-V:1.3",), "VOL-V:18.4") in links                                # IE2: the EPC definition and the cap
    assert (("VOL-V:1.3",), "VOL-IV:F4-F/estimated-project-cost-sar") in links
    assert {"Schedule 7", "Schedule 11"} <= {u["reference"] for u in res["unresolved"]}
    assert all(e["status"] == "proposed" for e in res["entries"])
    curated = ROOT / "curation/relationships.yaml"
    before = hashlib.sha256(curated.read_bytes()).hexdigest()
    out = tmp_path / "discovered.yaml"
    assert main(["relationships", "discover", "--to", str(out)]) == 0
    written = R.load(out)
    assert len(written) == len(res["entries"]) and all(e["status"] == "proposed" for e in written)
    assert main(["relationships", "discover", "--to", str(out)]) == 2               # never overwrites
    assert main(["relationships", "discover", "--to", str(curated)]) == 2           # never the curated file
    assert hashlib.sha256(curated.read_bytes()).hexdigest() == before
