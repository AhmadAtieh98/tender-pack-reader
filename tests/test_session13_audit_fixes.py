"""Session 13, fixer F1: reviewer R1's findings on A1 and A2 (R1-1 .. R1-6), with R2-1/R2-2 where they fall inside them.

R1-1  a relationship's open issues are shown in A2 wherever the relationship carries a change (a2_relationship_impact and
      the rows-moved "why"), by one function for every issue; ADD-02 5.1's "All other parameters in Table 2-4 are
      unchanged." is a PROPOSED confirming annotation on the other nine Table 2-4 rows, with the open question carried.
R1-2  a relationship's issues reach its target rows' Issues cells and the Issues sheet's rows list, marked with the
      relationship id and its status.
R1-3  a pending issue whose own words settle one of its limbs is reported by check-register for a person.
R1-4  ADD-01 App B item 5 (the permit under review) is context on REL-MISSING-ENVIRONMENTAL-PERMIT and in I-PERMIT.
R1-5  A2's change text is written in full in json and csv; only the markdown table shortens it, with a pointer.
R1-6  an evidence item whose form is reissued is checked against the reissued form's units; words gone -> a flag and the
      form row's issue link in A1.
Real pack (the committed build) and synthetic cases; nothing is written under the repository and nothing is approved."""
from __future__ import annotations

import pytest

from tenderpack import human_owned, relationships, signals, stage2
from tenderpack.util import ROOT, load_yaml

PENDING = "human decision pending"
T24 = "I-VOL-II-T24-TENSIONS"
NINE = ["BOD5", "COD", "TSS", "TP", "Turbidity", "FaecalColiforms", "ResidualChlorine", "pH", "OilGrease"]


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


@pytest.fixture(scope="module")
def a2d(real):
    return stage2.a2(real)


@pytest.fixture(scope="module")
def issues(real):
    return stage2.collect_issues(real, None)


@pytest.fixture(scope="module")
def a1(real, issues):
    return stage2.a1_table(real, issues)


def _rows(a1):
    return {x["id"]: x for x in a1["rows"]}


# ---------------------------------------------------------------------------------------------- R1-1

def test_r1_1_one_note_for_every_issue_synthetic():
    pend = {"I-A": ["its own words ..."]}
    assert signals.issue_note("I-A", pend) == "open: I-A, human decision pending"
    assert signals.issue_note("I-B", pend) == "open: I-B"
    entries = [{"id": "REL-1", "issues": ["I-A", "I-B"], "status": "confirmed"},
               {"id": "REL-2", "issues": ["I-A"], "status": "proposed"}, {"id": "REL-3", "status": "confirmed"}]
    notes = signals.relationship_issue_notes(entries, ["REL-1", "REL-2", "REL-3"], pend)
    assert notes == ["open: I-A, human decision pending (via REL-1, REL-2)", "open: I-B (via REL-1)"], notes


def test_r1_1_relationship_impact_carries_the_relationships_issues(a2d, real):
    by_id = {e["id"]: e for e in real["relationships"]}
    pend = real["pending_issues"]
    assert T24 in pend, "I-VOL-II-T24-TENSIONS is a person's decision not yet recorded"
    seen = set()
    scope = stage2.issue_scope_args(real)
    for x in a2d["relationships"]:
        # session 14 (W4; report section 9 A4): an issue travels along a relationship only within its scope
        # (relationships.issue_reaches); this test expected every issue of every entry on the path before the rule, so
        # the maxima/range issue was noted on VOL-V-29.3-01 through the rolling-average ramp-up link
        want = [i for rid in x["path"] for i in (by_id.get(rid) or {}).get("issues") or []
                if relationships.issue_reaches(by_id.get(rid) or {}, i, *scope)[0]]
        for i in want:
            assert any(n.startswith(signals.issue_note(i, pend)) for n in x["open_issues"]), (x["target"], i, x)
        if x["stage"] == "ADD-02" and T24 in want:
            seen.add(x["target"])
    # R2-2: the rows the reviewer names, all REL-T24-* targets. Session 14 (F1; R1-7): VOL-II-2.5-01 monitors only the
    # parameters assessed on a continuous basis (REL-T24-CONTINUOUS-MONITORING, scope_words PROPOSED), so the ADD-02
    # change to the rolling-average TN limit no longer reaches it
    assert {"VOL-V-31.1-02", "VOL-II-7.2-01", "VOL-II-3.1-01"} <= seen, seen
    assert "VOL-II-2.5-01" not in seen, seen
    md = a2d["markdown"]
    for row in ("VOL-V-31.1-02", "VOL-II-7.2-01", "VOL-II-3.1-01"):
        line = next(ln for ln in md.splitlines() if ln.startswith(f"- {row} (row;") and "REL-T24" in ln)
        assert f"open: {T24}, {PENDING}" in line, line


def test_r1_1_rows_moved_why_carries_the_issue_where_the_relationship_carries_the_change(a2d):
    hit = 0
    for m in a2d["rows_moved"]:
        if m["change"] == "CHANGED" and any("depends on it: REL-T24" in w for w in m["why"]):
            assert any(w.startswith(f"open: {T24}, {PENDING}") for w in m["why"]), m
            hit += 1
    assert hit >= 5, hit          # session 14 (F1; R1-7): VOL-II-2.5-01 is outside the TN change's scope


def test_r1_1_add02_5_1_second_sentence_confirms_the_other_nine_rows(real, a2d):
    ops = load_yaml(ROOT / "curation/amendments/ADD-02.yaml")["ops"]
    op = next((o for o in ops if o["provision"] == "ADD-02:5.1" and o["type"] == "annotate"), None)
    assert op is not None, "no annotate op records 'All other parameters in Table 2-4 are unchanged.'"
    assert op["effect"] == "confirms" and op["origin"] == "assistant" and op["review"] == "proposed"
    assert sorted(op["targets"]) == sorted(f"VOL-II:T2-4/{p}" for p in NINE)
    assert {"unit": "ADD-02:5.1", "contains": "All other parameters in Table 2-4 are unchanged."} in op["expect"]
    assert "p1" in op["note"] and T24 in op["note"] and human_owned.HUMAN_DECISION_PENDING in op["note"]
    x = next(y for s in real["stages"] for y in s.ops if y.op.id == op["id"])
    assert x.valid and x.applied, [c for c in x.checks if not c["ok"]]
    moved = {m["row"]: m for m in a2d["rows_moved"] if m["stage"] == "ADD-02"}
    for p in NINE:
        m = moved.get(f"VOL-II-T2-4-{p}")
        assert m is not None and m["change"] != "CHANGED", (p, m)
        why = " ".join(m["why"])
        assert op["id"] in why, (p, why)                      # the confirmation is named beside the open issue
        if p in ("ResidualChlorine", "pH"):
            assert f"open: {T24}, {PENDING}" in why, (p, why)
    assert moved["VOL-II-T2-4-TN"]["change"] == "CHANGED"


# ---------------------------------------------------------------------------------------------- R1-2

def test_r1_2_issue_links_synthetic():
    entries = [{"id": "REL-A", "to": ["R-1", "U:1"], "status": "confirmed", "issues": ["I-X"]},
               {"id": "REL-B", "to": "R-1", "status": "proposed", "issues": ["I-X", "I-Y"]},
               {"id": "REL-C", "to": ["R-2"], "status": "confirmed"}]
    got = relationships.issue_links(entries, {"R-1", "R-2"})
    assert got == {"R-1": [{"issue": "I-X", "via": "REL-A", "status": "confirmed"},
                           {"issue": "I-X", "via": "REL-B", "status": "proposed"},
                           {"issue": "I-Y", "via": "REL-B", "status": "proposed"}]}, got
    assert stage2.linked_issue_cells(["I-Y"], got["R-1"]) == ["I-Y", "I-X (via REL-A (confirmed); via REL-B (proposed))"]


def test_r1_2_every_target_row_of_a_relationship_lists_its_issues(real, a1):
    rows = _rows(a1)
    sheet = {i["id"]: i for i in a1["sheets"]["Issues"]["rows"]}
    n = 0
    scope = stage2.issue_scope_args(real)
    for e in real["relationships"]:
        for t in relationships.ends(e, "to"):
            if t not in rows:
                continue
            for i in e.get("issues") or []:
                cell = rows[t]["issues"]
                # session 14 (W4; report section 9 A4, R1's weak ramp-up link): an issue reaches a row through a
                # relationship only when the relationship's scope includes the issue's subject
                # (relationships.issue_reaches); a link outside the scope is said on the row's Relationships cell
                # instead of listing the issue (this test asserted every link before the rule)
                if not relationships.issue_reaches(e, i, *scope)[0]:
                    assert any(f"issue {i} not carried by {e['id']}" in x for x in rows[t]["relationships"]), t
                    continue
                assert i in cell or any(c.startswith(f"{i} (via ") and e["id"] in c and f"({e['status']})" in c
                                        for c in cell), (t, i, cell)
                assert any(str(x).split(" ")[0] == t for x in sheet[i]["rows"]), (i, t, sheet[i]["rows"])
                n += 1
    assert n > 20
    for t in ("VOL-V-31.1-02", "VOL-II-2.5-01", "VOL-II-7.2-01", "VOL-II-3.1-01"):      # R2-2
        assert any(c.startswith(f"{T24} (via REL-T24-") and "(confirmed)" in c for c in rows[t]["issues"]), rows[t]["issues"]


# ---------------------------------------------------------------------------------------------- R1-3

def test_r1_3_settling_words_in_a_pending_issue_synthetic():
    bad = {"text": "Each keeps its basis; read together this means continuous compliance, which is not treated as a "
                   "conflict", "owner": "Process engineer"}
    got = human_owned.settled_wording(bad)
    assert any("is not treated as" in g for g in got) and any("means" in g for g in got), got
    ok = {"text": "Unresolved: how 'at all times' combines with each basis ('the basis means X' quoted). Proposed "
                  "reading, not decided (Process engineer): no decision recorded", "owner": "Process engineer"}
    assert human_owned.settled_wording({"text": "the Authority's words: 'which is not treated as a conflict'"}) == []
    assert human_owned.settled_wording({"text": "A by means of B; therefore C"}) == ["'therefore'"]
    assert human_owned.settled_wording(ok) == [], human_owned.settled_wording(ok)
    r = {"curated_issues": {"I-BAD": bad, "I-OK": ok, "I-NOT-PENDING": {"text": "x is read as y", "owner": "Bid"}},
         "pending_issues": {"I-BAD": ["linked"], "I-OK": ["linked"]}}
    f = stage2.pending_wording_findings(r)
    assert [x["where"] for x in f] == ["I-BAD"] and f[0]["kind"] == "pending_settled", f


def test_r1_3_the_t24_issue_is_worded_as_pending_and_the_real_register_has_no_finding(real):
    t = real["curated_issues"][T24]["text"]
    assert "is not treated as" not in t and " means " not in t
    # session 13 (F4; audit R1 recheck nit, deliberate): the 'at all times' limb lives in I-VOL-II-AT-ALL-TIMES only,
    # worded as a proposed reading for the Process engineer; T24's text cross-refers to it
    assert "the 'at all times' reading is I-VOL-II-AT-ALL-TIMES" in t, t
    at = real["curated_issues"]["I-VOL-II-AT-ALL-TIMES"]["text"]
    assert "Proposed reading (not decided)" in at and "for the Process engineer; no decision recorded" in at, at
    assert stage2.pending_wording_findings(real) == []
    assert T24 in real["pending_issues"]


# ---------------------------------------------------------------------------------------------- R1-4

ITEM5 = "the permit was under review by the regulator and that any change would be issued by Addendum."


def test_r1_4_context_is_checked_verbatim_synthetic():
    units = [{"unit_id": "D:1", "pages": [2], "text": "The thing was under review."},
             {"unit_id": "D:2", "pages": [3], "text": "Doc X prevails."}]
    base = {"id": "REL-M", "from": "D:2", "to": "D:2", "kind": "missing_document", "status": "confirmed",
            "document": "Doc X", "document_id": "X", "blocks": "y", "origin": "curator",
            "evidence": [{"unit": "D:2", "page": 3, "words": "Doc X prevails."}]}
    good = dict(base, context=[{"unit": "D:1", "page": 2, "words": "was under review", "note": "non-binding"}])
    assert relationships.validate([good], units, [], []) == []
    bad = dict(base, context=[{"unit": "D:1", "page": 2, "words": "was final"}])
    assert any("context not verbatim" in f for f in relationships.validate([bad], units, [], [])), \
        relationships.validate([bad], units, [], [])
    line = relationships.label({"target": "D:2", "entry_id": "REL-M", "kind": "missing_document", "status": "confirmed",
                                "path": ["REL-M"], "source": "D:2"}, [good])
    assert "context (not binding): D:1 p2 'was under review' (non-binding)" in line, line


def test_r1_4_the_minutes_item_is_context_on_the_permit_link_and_in_i_permit(real, a1, a2d):
    e = next(x for x in real["relationships"] if x["id"] == "REL-MISSING-ENVIRONMENTAL-PERMIT")
    ctx = e.get("context") or []
    assert any(c["unit"] == "ADD-01:AppB/item-5-effluent-standards" and c["page"] == 4 and c["words"] == ITEM5
               for c in ctx), ctx
    assert stage2.relationship_findings(real) == []
    assert ITEM5 in real["curated_issues"]["I-PERMIT"]["text"] and "ADD-01 3.2" in real["curated_issues"]["I-PERMIT"]["text"]
    sheet = {i["id"]: i for i in a1["sheets"]["Issues"]["rows"]}
    assert ITEM5 in sheet["I-PERMIT"]["text"] and ITEM5 in sheet["I-AUTO-NOT-SUPPLIED-ENVIRONMENTAL-PERMIT"]["text"]
    gap = [ln for ln in a2d["markdown"].splitlines() if "NOT SUPPLIED: the Environmental Permit" in ln]
    assert gap and all(ITEM5 in ln for ln in gap), gap


# ---------------------------------------------------------------------------------------------- R1-5

def test_r1_5_change_text_is_full_in_json_and_csv(real, a2d):
    notes = {y.op.id: y.op.note for s in real["stages"] for y in s.ops if y.op.note}
    longer = 0
    for c in a2d["changes"]:
        assert not c["change"].endswith("…"), c
        n = notes.get(c["op"])
        if n and len(n) > 90 and c["type"] == "annotate":
            assert " ".join(n.split()) in c["change"], (c["op"], c["change"])
            longer += 1
    assert longer >= 10
    table = [ln for ln in a2d["markdown"].splitlines() if ln.startswith("| ADD-01/4.2 |")]
    assert table and "full text in a2_changes.csv" in table[0], table


# ---------------------------------------------------------------------------------------------- R1-6

def test_r1_6_reissued_form_evidence_synthetic():
    from types import SimpleNamespace as NS
    u = lambda t, st="active", by=None: NS(text=t, status=st, superseded_by=by)   # noqa: E731
    base = {"F:A": u("Form A"), "F:A/1": u("We confirm validity of 150 days."), "F:A/2": u("Name:")}
    new = {"F:A": u("Form A", "superseded", "G:A"), "F:A/1": u("We confirm validity of 150 days.", "superseded", "G:A"),
           "F:A/2": u("Name:", "superseded", "G:A"), "G:A": u("Form A (reissued)"), "G:A/1": u("Name:")}
    row = lambda i, units, ev, quote, issues=(): NS(id=i, units=units, evidence=ev, issues=list(issues), quote=quote)  # noqa: E731
    rows = [row("R-REQ", ["V:7"], ["EV-A"], "validity of 150 days"),
            row("R-F1", ["F:A/1"], ["EV-A"], "validity of 150 days", ["I-FORM", "I-NO"]),
            row("R-F2", ["F:A/2"], ["EV-A"], "Name:"),
            row("R-OTHER", ["V:8"], ["EV-A"], "Name:", ["I-NO"])]
    got = stage2.reissued_form_gaps(rows, [("BASE", base), ("ADD-9", new)], lambda rw, st: rw.quote)
    assert got == {"R-REQ": [{"stage": "ADD-9", "evidence": "EV-A", "form": "F:A", "unit": "F:A/1", "form_row": "R-F1",
                              "flag": "evidence field not on the reissued form (R-F1)", "issues": ["I-FORM", "I-NO"]}]}, got


def test_r1_6_vol_i_7_1_01_is_flagged_with_the_form_issue(real, a1):
    row = _rows(a1)["VOL-I-7.1-01"]
    cell = " ".join(row["issues"])
    assert "I-F4A-FIELDS (evidence field not on the reissued form (VOL-IV-F4A-04))" in row["issues"], row["issues"]
    assert "evidence field not on the reissued form (VOL-IV-F4A-04)" in row["change:ADD-01"], row["change:ADD-01"]
    assert "I-NO-CONSEQUENCE" in cell
    sheet = {i["id"]: i for i in a1["sheets"]["Issues"]["rows"]}
    assert any(str(x).startswith("VOL-I-7.1-01 ") for x in sheet["I-F4A-FIELDS"]["rows"]), sheet["I-F4A-FIELDS"]["rows"]


# ---------------------------------------------------------------------------------------------- found while fixing R1-1

def test_a_row_made_stale_only_by_a_confirming_op_is_recognised_synthetic():
    # register.evaluate writes the provision's confirming ops after the provision; the suffix was not matched (session
    # 12's pattern ended at the provision), so such a row read as CHANGED ("stale") instead of confirmed
    why = ["new dependency P:1 (the provision of OP-1, which confirms a unit of the row unchanged)"]
    assert signals.stale_from_confirmations(why, [{"op": "OP-1", "provision": "P:1"}])
    assert not signals.stale_from_confirmations(why, [{"op": "OP-2", "provision": "P:2"}])
    assert not signals.stale_from_confirmations(["never pinned"], [{"op": "OP-1", "provision": "P:1"}])


def test_words_that_quantify_over_a_cited_tables_rows_cite_them_synthetic():
    from tenderpack.citations import quantified_row
    ids = {"VOL-II:T2-4", "VOL-II:T2-4/TN", "VOL-II:T2-4/BOD5", "VOL-II:T2-6/peak"}
    t = ("In Volume II Table 2-4, the limit for Total Nitrogen (TN) is amended to 3 mg/l. All other parameters in "
         "Table 2-4 are unchanged.")
    assert quantified_row("VOL-II:T2-4/BOD5", t, ids)[0]
    assert not quantified_row("VOL-II:T2-4/TN", t, ids)[0]          # the row the provision names is not 'other'
    assert not quantified_row("VOL-II:T2-6/peak", t, ids)[0]        # another table
    assert not quantified_row("VOL-II:T2-4/BOD5", "In Volume II Table 2-4, the limit for TN is amended.", ids)[0]


def test_the_nine_rows_are_re_read_at_add02_not_stale(real):
    # the readings are re-made at ADD-02 (PROPOSED) with the same words and values, so the confirmation leaves them
    # unchanged and not STALE (a STALE row would add I-AUTO-STALE to A3 and REVIEW flags to A5)
    for p in NINE:
        e = next(x for x in real["evals"] if x["row"].id == f"VOL-II-T2-4-{p}")
        b = e["stages"]["ADD-02"]
        assert not b["stale"] and b["interpretation_stage"] == "ADD-02", (p, b["stale"])
        assert "ADD-02/5.1/unchanged" in (b["interpretation"] or {}).get("note", "")
