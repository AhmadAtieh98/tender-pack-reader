"""Session 14 (F1): the fixes for the independent recheck's findings on A1 and A2 (R1-1 .. R1-8; R2 m6).

R1-1  the value column sees a row deleted at one stage and reinstated at a later one as CHANGED at the reinstating
      stage (value and consequence); an annotation of a provision a later addendum revokes is named as revoked.
R1-5  the value state comes from the row's OWN quote and cells: a row whose status says 'the row's words unchanged'
      never reads 'changed at <stage>'; an amended list or form says what was amended.
R1-6  a re-reading op reads '<op> (<kind>; proposed, not accepted; not counted as a confirmation)'; the A1 notice
      defines the three state columns; every A2 CONFIRMED line resting on something proposed says it awaits a person.
R1-2  one rule for an open issue's reach through a relationship (relationships.inherited_issue_links): A1's Issues
      cell, A2's relationship-impact table and A2's rows-moved table agree on the rows a document-not-supplied issue
      (the Environmental Permit) reaches through a limit_applies link, within the link's scope.
R1-3  the Form 4-E checks' judgments are mirrored by PROPOSED issues (I-FORM-4E-COMMERCIAL-QUALIFICATION,
      I-FORM-4E-CROSS-CHECK); a judgment without a mirror is a check-register finding.
R1-7  a relationship narrowed by scope_words carries a change only from inside its scope (VOL-II 2.5's continuous
      monitoring is not moved by the TN limit).
R1-8  A1's Relationships sheet shows each relationship's scope words; the scope-limited lines say the scope is
      PROPOSED and that the owner may keep the issue on the row.
R2 m6 an issue whose curated subject lies in a relationship's `from` travels along it within its scope (the 'at all
      times' and compliance-point issues reach VOL-V-31.1-02 and VOL-II-7.2-01)."""
from __future__ import annotations

import pytest

from tenderpack import human_owned as H
from tenderpack import programme, relationships, signals, stage2
from tenderpack.util import ROOT


@pytest.fixture(scope="module")
def real():
    return stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)


@pytest.fixture(scope="module")
def states(real):
    return stage2.row_states(real)


@pytest.fixture(scope="module")
def a1(real):
    return stage2.a1_table(real, stage2.collect_issues(real, None))


@pytest.fixture(scope="module")
def a2(real):
    return stage2.a2(real)


# ------------------------------------------------------------------------------------------------- R1-1
def test_r1_1_deleted_then_reinstated_reads_changed_at_the_reinstating_stage(real, states):
    order = real["order"]
    seen = 0
    for e in real["evals"]:
        stg = e["stages"]
        act = [stg[s]["active"] for s in order]
        gaps = [i for i in range(1, len(order)) if act[i] and not act[i - 1] and any(act[:i - 1] + act[i - 1:i] or [False])
                and any(act[:i])]
        if not gaps:
            continue
        seen += 1
        v = states[e["row"].id]["value"]
        assert not v.startswith("unchanged"), (e["row"].id, v)
        for i in gaps:
            assert f"at {order[i]}" in v and ("changed at" in v or "reinstated at" in v), (e["row"].id, v)
            gone = next(order[k] for k in range(i - 1, -1, -1) if act[k] and not act[k + 1])
            assert f"at {order[order.index(gone) + 1]}" in v, (e["row"].id, v)
    assert seen, "the real pack has a deleted-then-reinstated row"
    v = states["VOL-I-8.6-01"]["value"]
    assert "changed at ADD-02 by ADD-02/9.1" in v and "deleted at ADD-01 by ADD-01/4.1" in v, v
    assert "consequence" in v, v
    # an annotation of a provision a later addendum revokes is never listed as a live re-reading
    assert "ADD-01/4.2" not in v.split("re-read by")[-1] or "revoked" in v, v


# ------------------------------------------------------------------------------------------------- R1-5
def test_r1_5_value_state_follows_the_rows_own_words(real, states):
    order = real["order"]
    for e in real["evals"]:
        v = states[e["row"].id]["value"]
        for s in order[1:]:
            st = e["stages"][s]["status"]
            if "the row's words unchanged" in st or "reissued by" in st and "unchanged" in st:
                assert f"changed at {s}" not in v.replace("unchanged at", ""), (e["row"].id, s, st, v)
            if st.startswith("AMENDED"):
                assert f"amended at {s}" in v or f"changed at {s}" in v, (e["row"].id, s, st, v)
    v = states["VOL-I-9.1-01"]["value"]
    assert "amended at ADD-02 by ADD-02/7.1" in v and "quoted words unchanged" in v, v
    assert "amended at ADD-01 by ADD-01/AppA/para1" in states["VOL-IV-F4A-02"]["value"]
    for rid in ("VOL-II-4.4-02", "VOL-II-5.3-02"):
        v = states[rid]["value"]
        assert v.startswith("unchanged since BASE") and "the row's words unchanged" in v, (rid, v)


# ------------------------------------------------------------------------------------------------- R1-6
def test_r1_6_reread_wording_and_the_notice(states, a1, a2):
    for rid, s in states.items():
        assert "(an annotation; not a confirmation)" not in s["value"], (rid, s["value"])
        if "re-read by" in s["value"]:
            assert "not counted as a confirmation" in s["value"] or "no longer in force" in s["value"], (rid, s["value"])
            assert "(confirms; ADD-02) (an annotation" not in s["value"]
    assert "(confirms; proposed, not accepted; not counted as a confirmation)" in states["VOL-II-T2-4-BOD5"]["value"]
    n = a1["notice"]
    for w in ("'Value at the validated stage'", "'Interpretation'", "'Approval'"):
        assert w in n, w
    for m in a2["rows_moved"]:
        if m["change"] == signals.CONFIRMED:
            assert signals.AWAITING in " ".join(m["why"]), m


# ------------------------------------------------------------------------------------------------- R1-2
def test_r1_2_one_rule_for_an_issue_reached_through_a_blocked_limit(real, a1, a2):
    by_row = stage2.row_issues(real)
    ents = {e["id"]: e for e in real["relationships"] if isinstance(e, dict) and e.get("id")}
    rows = {e["row"].id for e in real["evals"]}
    for st, d in (real.get("relationship_impact") or {}).items():
        for rec in d.get("records") or []:
            if rec["target"] not in rows or rec["kind"] == "missing_document":
                continue
            for b in rec.get("blockers") or []:
                for i in ents[b["entry_id"]].get("issues") or []:
                    assert i in by_row[rec["target"]], (st, rec["target"], b["entry_id"], i)
    for rid in ("VOL-V-29.3-01", "VOL-II-2.5-01", "VOL-II-4.3-02"):
        assert "I-PERMIT" in by_row[rid], rid
    row = next(x for x in a1["rows"] if x["id"] == "VOL-V-29.3-01")
    assert "I-PERMIT" in " ".join(row["issues"]) and H.HUMAN_DECISION_PENDING in row["interpretation_state"]
    assert "I-PERMIT" in row["interpretation_state"]
    sheet = {x["id"]: x for x in a1["sheets"]["Issues"]["rows"]}
    assert any(x.startswith("VOL-V-29.3-01") for x in sheet["I-PERMIT"]["rows"])
    for m in a2["rows_moved"]:
        if m["row"] == "VOL-V-29.3-01":
            assert m["change"] != signals.CONFIRMED, m


def test_r1_2_inherited_issue_links_synthetic():
    units = {"V:T1": {"text": "t"}, "V:T1/A": {"text": "A | 30-day rolling average"},
             "V:T1/B": {"text": "B | Continuous at outlet"}}
    gap = {"id": "REL-GAP", "from": ["V:2"], "to": ["ROW-A", "ROW-B"], "kind": "missing_document",
           "status": "confirmed", "issues": ["I-DOC"], "document": "d", "origin": "curator"}
    nar = {"id": "REL-N", "from": ["V:T1"], "to": ["ROW-N"], "kind": "limit_applies", "status": "confirmed",
           "scope_words": "rolling average", "origin": "curator"}
    off = dict(nar, id="REL-OFF", to=["ROW-OFF"], scope_words="Continuous")
    other = dict(nar, id="REL-DEP", kind="depends_on", to=["ROW-DEP"], scope_words=None)
    row_units = {"ROW-A": ["V:T1/A"], "ROW-B": ["V:T1/A"]}
    links = relationships.issue_links([gap, nar, off, other], {"ROW-A", "ROW-B", "ROW-N", "ROW-OFF", "ROW-DEP"},
                                      issues={"I-DOC": {"text": "x"}}, units=units, row_units=row_units)
    assert [(x["issue"], x["via"]) for x in links["ROW-N"]] == [("I-DOC", "REL-GAP > REL-N")]
    assert "ROW-OFF" not in links                       # the blocked members are outside the link's scope
    assert "ROW-DEP" not in links                       # only a limit applied from the blocked source inherits
    assert [x["issue"] for x in links["ROW-A"]] == ["I-DOC"]


# ------------------------------------------------------------------------------------------------- R2 m6
def test_r2_m6_subject_issues_travel_along_the_whole_table_links(real):
    by_row = stage2.row_issues(real)
    for i in ("I-VOL-II-AT-ALL-TIMES", "I-VOL-II-COMPLIANCE-POINT"):
        for rid in ("VOL-V-31.1-02", "VOL-II-7.2-01"):
            assert i in by_row[rid], (i, rid)


def test_r2_m6_subject_rule_synthetic():
    units = {"V:T1": {"text": "t"}, "V:T1/A": {"text": "A | rolling average"}, "V:T1/B": {"text": "B | Continuous"}}
    whole = {"id": "REL-W", "from": ["V:T1"], "to": ["ROW-W"], "kind": "limit_applies", "status": "confirmed",
             "origin": "curator"}
    nar = dict(whole, id="REL-N", to=["ROW-N"], scope_words="rolling average")
    issues = {"I-B": {"text": "b", "subject": ["V:T1/B"]}, "I-ALL": {"text": "all", "subject": ["V:T1"]},
              "I-ELSE": {"text": "else", "subject": ["V:9"]}}
    links = relationships.issue_links([whole, nar], {"ROW-W", "ROW-N"}, issues=issues, units=units)
    assert sorted(x["issue"] for x in links["ROW-W"]) == ["I-ALL", "I-B"]
    assert [x["issue"] for x in links["ROW-N"]] == ["I-ALL"]


# ------------------------------------------------------------------------------------------------- R1-3
F4E_ROWS = ("VOL-I-9.6-01", "VOL-I-10.5-01", "VOL-I-6.2-02", "VOL-IV-F4F-02")


def test_r1_3_form_4e_judgments_are_issues(real, a1):
    iss = real["curated_issues"]
    com, cc = iss["I-FORM-4E-COMMERCIAL-QUALIFICATION"], iss["I-FORM-4E-CROSS-CHECK"]
    assert com["owner"].startswith("Legal") and "Commercial" in com["text"]
    assert cc["owner"] == "Bid manager"
    assert "while containing a qualification elsewhere in the Proposal shall be treated as non-responsive" in com["text"]
    links = H.pending_links(real.get("clarifications"))
    for iid, it in (("I-FORM-4E-COMMERCIAL-QUALIFICATION", com), ("I-FORM-4E-CROSS-CHECK", cc)):
        assert H.issue_label(iid, it, [], links.get(iid)).startswith(H.HUMAN_DECISION_PENDING), iid
        assert not it.get(H.MARKER), iid                     # curated (PROPOSED), not the AI workflow's
        assert "Form 4-E check" in it["text"], iid
    by_row = stage2.row_issues(real)
    for rid in F4E_ROWS:
        assert "I-FORM-4E-COMMERCIAL-QUALIFICATION" in by_row[rid], rid
        row = next(x for x in a1["rows"] if x["id"] == rid)
        assert "I-FORM-4E-COMMERCIAL-QUALIFICATION" in row["interpretation_state"], rid
    sheet = {x["id"]: x for x in a1["sheets"]["Issues"]["rows"]}
    assert sheet["I-FORM-4E-COMMERCIAL-QUALIFICATION"]["rows"]
    # the one pending set (A1's Issues sheet, the A3 detail, A4) carries both as HUMAN DECISION PENDING
    lab = {x["id"]: x.get("human_decision") for x in stage2.collect_issues(real, None)}
    assert all(lab[i] == H.HUMAN_DECISION_PENDING for i in ("I-FORM-4E-COMMERCIAL-QUALIFICATION",
                                                            "I-FORM-4E-CROSS-CHECK")), lab


def test_r1_3_the_check_names_its_issue_and_an_unmirrored_judgment_is_a_finding(real):
    prog = stage2.a5_all(real)[real["validated"].stage]
    res = programme.form_4e_checks_for(real, prog)
    said = " ".join(res["findings"])
    assert "I-FORM-4E-COMMERCIAL-QUALIFICATION" in said and "I-FORM-4E-CROSS-CHECK" in said, said
    assert programme.form_4e_mirror_findings(real["curated_issues"]) == []
    less = {k: v for k, v in real["curated_issues"].items() if k != "I-FORM-4E-CROSS-CHECK"}
    f = programme.form_4e_mirror_findings(less)
    assert f and "cross-check" in f[0], f
    assert not [x for x in stage2.register_findings(real) if "form-4e" in x["detail"].lower()]


# ------------------------------------------------------------------------------------------------- R1-7
def test_r1_7_a_scoped_link_carries_only_changes_inside_its_scope(real, a2):
    imp = (real.get("relationship_impact") or {}).get("ADD-02") or {}
    assert not [x for x in imp.get("records") or [] if x["target"] == "VOL-II-2.5-01"]
    for m in a2["rows_moved"]:
        if m["row"] == "VOL-II-2.5-01" and m["stage"] == "ADD-02":
            assert "T2-4/TN" not in " ".join(m["why"]), m
    assert "I-VOL-II-T24-TENSIONS" in stage2.row_issues(real)["VOL-II-2.5-01"]
    assert not stage2.relationship_findings(real)


def test_r1_7_trace_respects_scope_synthetic():
    nar = {"id": "REL-N", "from": ["V:T1"], "to": ["ROW-N"], "kind": "limit_applies", "status": "confirmed",
           "scope_words": "Continuous", "origin": "curator"}
    scopes = {"REL-N": {"V:T1/B"}}
    assert not relationships.trace([nar], {"V:T1", "V:T1/A"}, scopes=scopes)
    assert [x["target"] for x in relationships.trace([nar], {"V:T1", "V:T1/B"}, scopes=scopes)] == ["ROW-N"]
    assert [x["target"] for x in relationships.trace([nar], {"V:T1"}, scopes=scopes, whole={"V:T1"})] == ["ROW-N"]


# ------------------------------------------------------------------------------------------------- R1-8
def test_r1_8_scope_shown_and_labelled_proposed(a1, a2):
    sheet = {x["id"]: x for x in a1["sheets"]["Relationships"]["rows"]}
    assert sheet["REL-T24-RAMP-UP-DEDUCTIONS"]["scope"].startswith("rolling average")
    assert "scope" in [c["key"] for c in a1["sheets"]["Relationships"]["columns"]]
    row = next(x for x in a1["rows"] if x["id"] == "VOL-V-29.3-01")
    line = next(x for x in row["relationships"] if "not carried" in x)
    assert "(scope PROPOSED, not reviewed; the owner may keep the issue on the row)" in line, line
    md = [ln for ln in a2["markdown"].splitlines() if ln.startswith("- VOL-V-29.3-01 ")]
    assert md and all("(scope PROPOSED, not reviewed; the owner may keep the issue on the row)" in ln for ln in md), md


# ------------------------------------------------------------------------------------------------- R1-4
# Session 14 (F1; R1-4, R2-M4, R3): an issue whose point the document's own amended words settle is re-presented by
# W4's applied-rule mechanism (`applied_rule`, `confirm`: PROPOSED BASIS, a person confirms the application), never
# closed or deleted: its owner is kept, its rows stay NOT SETTLED until a person accepts it, and no pending decision of
# the clarification register keeps it an open-ended HUMAN DECISION PENDING escalation. Checked on every curated issue
# that carries an applied rule (none is named in code); the page-limit issue is the real pack's one.
def test_r1_4_an_applied_rule_issue_is_a_proposed_basis_everywhere(real, a1, a2):
    from tenderpack.register import effective
    iss = real["curated_issues"]
    applied = {i: it for i, it in iss.items() if H.applied_basis(it)}
    assert "I-VOL-I-PAGE-LIMIT-Q2" in applied, sorted(applied)
    links = H.pending_links(real.get("clarifications"))
    val = real["validated"].stage
    state = {s.stage: s for s in real["stages"]}[val].state
    by_row = stage2.row_issues(real)
    states = stage2.row_states(real)
    sheet = {x["id"]: x for x in a1["sheets"]["Issues"]["rows"]}
    for iid, it in applied.items():
        assert it.get("owner") and it.get("status") in (None, "", "open") and not it.get("resolution"), iid
        assert iid not in links, (iid, links.get(iid))             # no pending decision keeps it an escalation
        assert H.issue_label(iid, it, real.get("decisions"), links.get(iid)) == H.PROPOSED_BASIS, iid
        assert H.pending_reasons(iid, it, real.get("decisions"), links.get(iid)) == [], iid
        assert iid in (real.get("awaiting_issues") or {}), iid
        # the applied clause is quoted verbatim from the clause's words in force at the validated stage
        for line in it["applied_rule"]:
            doc, clause = line.split(" ")[:2]                        # "<DOC> <clause> [as amended ...] provides: '...'"
            words = line.split(" provides: '", 1)[1].rsplit("'", 1)[0]
            u = effective(state, f"{doc}:{clause}", True)
            assert u is not None and words in " ".join(u.text.split()), (iid, line)
        assert all(c.startswith("applied rule: ") and c.endswith("a person confirms the application")
                   for c in it["confirm"]), it["confirm"]
        assert sheet[iid]["text"].startswith(H.PROPOSED_BASIS) and sheet[iid]["owner"] == it["owner"], sheet[iid]
        assert H.HUMAN_DECISION_PENDING not in sheet[iid]["text"], sheet[iid]
        rows = [rid for rid, ids in by_row.items() if iid in ids]
        assert rows, iid
        for rid in rows:
            assert signals.AWAITING_RULE in states[rid]["interpretation"], (rid, states[rid]["interpretation"])
            assert f"{H.HUMAN_DECISION_PENDING}: {iid}" not in states[rid]["interpretation"], rid
            for m in a2["rows_moved"]:
                if m["row"] == rid and m["stage"] == val:
                    assert m["change"] != signals.CONFIRMED and signals.awaiting_note(iid) in " ".join(m["why"]), m
    # the page-limit issue keeps its owner, and its rows stay not settled at the stage that raises it
    assert iss["I-VOL-I-PAGE-LIMIT-Q2"]["owner"] == "Bid manager"
