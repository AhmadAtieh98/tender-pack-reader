"""Session 09: a table entry an addendum describes in prose (blind rehearsal 02, ADD-03 7.2: "The Index of Forms in Volume
IV is amended by adding, after the entry for Form 4-F, an entry for Form 4-G with the title 'Cybersecurity Compliance
Undertaking', Envelope 'A' and Status 'Mandatory'."). The curator could only annotate it; the index table never had the row.

The op type `insert_row` (target table, `after` row, `cells`) inserts `<table>/<key>+<addendum>`. C22: the provision cites
the table ("the Index of Forms in Volume IV" is the volume's one table whose first column is "Form" and which has a
"Title" column), names the row it follows, every column is in the header and the key is new. C21: every cell is printed
after its column's name. C47 accepts the new row because each cell value is printed by the addendum.
"""
from __future__ import annotations

import pytest

from tenderpack import stage2
from tenderpack.amend import Engine, OpFile, UState, unevidenced_additions
from tenderpack.citations import after_row, citations, is_index_table, row_names
from tenderpack.util import ROOT

PROSE = ("The Index of Forms in Volume IV is amended by adding, after the entry for Form 4-F, an entry for Form 4-G with "
         "the title ‘Cybersecurity Compliance Undertaking’, Envelope ‘A’ and Status ‘Mandatory’.")
CELLS = {"Form": "4-G", "Title": "Cybersecurity Compliance Undertaking", "Envelope": "A", "Status": "Mandatory"}
NEW = "VOL-IV:cover/T1/4-G+ADD-01"


def test_the_index_citation_and_the_row_to_follow_are_read_from_the_prose():
    c = [x for x in citations(PROSE) if x.kind == "index"]
    assert [(x.text, x.target) for x in c] == [("Index of Forms in Volume IV", "VOL-IV:index")]
    assert after_row(PROSE) == "4-F" and "4-F" in row_names(PROSE)
    assert after_row("an entry for Form 4-G is added") is None
    assert after_row("after the row 'TN', a row for ammonia") == "TN"
    assert is_index_table(["Form", "Title", "Envelope", "Status"]) and not is_index_table(["Parameter", "Unit", "Average"])


def _units(prose=PROSE, second_index=False):
    def u(uid, kind, text, doc="VOL-IV", **kw):
        return {"unit_id": uid, "doc": doc, "kind": kind, "text": text, "pages": [1], **kw}
    out = [u("VOL-IV:H:cover-2", "heading", "INDEX OF FORMS"),
           u("VOL-IV:cover/T1", "table", "Form | Title | Envelope | Status")]
    for key, title, env in (("4-A", "Proposal Submission Letter", "A"), ("4-F", "Financial Proposal Schedule", "B")):
        cells = {"Form": key, "Title": title, "Envelope": env, "Status": "Mandatory"}
        out.append(u(f"VOL-IV:cover/T1/{key}", "table_row", " | ".join(f"{k}: {v}" for k, v in cells.items()),
                     parent="VOL-IV:cover/T1", label=key, cells=cells))
    out.append(u("VOL-IV:cover/para5", "paragraph", "Forms shall be reproduced without alteration."))
    if second_index:
        out.append(u("VOL-IV:annex/T9", "table", "Form | Title | Volume"))
    out += [u("ADD-01:cover/para1", "paragraph", "Issued 3 November 2026", doc="ADD-01"),
            u("ADD-01:7.2", "clause", prose, doc="ADD-01")]
    return out


def _run(units, **op):
    f = OpFile.model_validate({"addendum": "ADD-01", "issued_from": "ADD-01:cover/para1", "prepared_by": "test", "method": "test",
                               "ops": [{"id": "ADD-01/7.2", "provision": "ADD-01:7.2", "type": "insert_row",
                                        "target": "VOL-IV:cover/T1", "after": "VOL-IV:cover/T1/4-F", "cells": CELLS, **op}],
                               "dispositions": [{"provision": "ADD-01:cover/para1", "disposition": "no_effect",
                                                 "reason": "issue date"}]})
    eng = Engine(units, [f])
    return eng, eng.run()


def test_an_index_entry_in_prose_becomes_a_row_of_the_index_table():
    eng, stages = _run(_units())
    s = stages[-1]
    x = s.ops[0]
    assert x.valid and x.applied and s.status == "APPLIED" and x.changed == [NEW] and not s.scope_leak
    u = s.state[NEW]
    assert (u.kind, u.parent, u.status, u.origin, u.label, u.history, u.issued_by) == (
        "table_row", "VOL-IV:cover/T1", "active", "addendum_op", "4-G", ["ADD-01/7.2"], "ADD-01")
    assert u.cells == CELLS and u.text == "Form: 4-G | Title: Cybersecurity Compliance Undertaking | Envelope: A | Status: Mandatory"
    assert u.text == u.row_text()                                       # the siblings' text form
    i = eng.order.index(NEW)
    assert eng.order[i - 1] == "VOL-IV:cover/T1/4-F" and eng.order[i + 1] == "VOL-IV:cover/para5"
    assert unevidenced_additions(stages[0].state, s.state, "ADD-01") == []          # C47: every cell is printed
    assert [c["disposition"] for c in s.coverage if c["provision"] == "ADD-01:7.2"] == ["op"]          # C20


def test_without_after_the_row_is_appended_after_the_last_row():
    eng, stages = _run(_units(PROSE.replace("after the entry for Form 4-F, ", "")), after=None)
    assert stages[-1].ops[0].valid
    i = eng.order.index(NEW)
    assert eng.order[i - 1] == "VOL-IV:cover/T1/4-F"


@pytest.mark.parametrize("units_kw, op, check, why", [
    ({}, {"cells": {**CELLS, "Title": "Cyber Undertaking"}}, "C21", "not printed in the provision"),
    ({}, {"cells": {**CELLS, "Pages": "2"}}, "C22", "not those of"),
    ({}, {"cells": {k: v for k, v in CELLS.items() if k != "Form"}}, "C22", "key column 'Form'"),
    ({}, {"after": "VOL-IV:cover/T1/4-A"}, "C22", "names as the one to follow"),
    ({}, {"cells": {**CELLS, "Form": "4-F"}}, "C22", "already has a row keyed '4-F'"),
    ({"prose": PROSE.replace("The Index of Forms in Volume IV", "The list of forms")}, {}, "C22", "cites no"),
    ({"second_index": True}, {}, "C22", "the index tables of VOL-IV are"),
])
def test_an_insert_row_the_provision_does_not_support_changes_nothing(units_kw, op, check, why):
    eng, stages = _run(_units(**units_kw), **op)
    x = stages[-1].ops[0]
    failed = [c for c in x.checks if not c["ok"]]
    assert not x.valid and failed[0]["id"] == check and why in failed[0]["detail"], failed
    assert not [k for k in stages[-1].state if k.endswith("+ADD-01")] and not any(k.endswith("+ADD-01") for k in eng.order)
    assert stages[-1].status == "PARTIAL"


def test_c47_still_flags_a_new_row_whose_cell_the_addendum_does_not_print():
    prev = {u["unit_id"]: UState(u["unit_id"], u["doc"], u["kind"], "active", u["text"], u.get("cells"), [1], "text_layer",
                                 None, parent=u.get("parent"), label=u.get("label")) for u in _units()}
    cur = dict(prev)
    cur["VOL-IV:cover/T1/4-H+ADD-01"] = UState("VOL-IV:cover/T1/4-H+ADD-01", "VOL-IV", "table_row", "active",
                                               "Form: 4-H | Title: Escrow Letter", {"Form": "4-H", "Title": "Escrow Letter"},
                                               [1], "addendum_op", None, parent="VOL-IV:cover/T1", label="4-H")
    assert unevidenced_additions(prev, cur, "ADD-01") == ["VOL-IV:cover/T1/4-H+ADD-01: '4-H'",
                                                         "VOL-IV:cover/T1/4-H+ADD-01: 'Escrow Letter'"]


# ------------------------------------------------------------------------------------------------ blind rehearsal 02

@pytest.fixture(scope="module")
def blind02():
    b = ROOT / "rehearsals/blind-02"
    return stage2.run(b / "build", b / "work/pack.yaml", ROOT)


def test_blind02_add03_7_2_inserts_form_4g_in_the_index_and_the_row_quotes_it(blind02):
    r = blind02
    s = next(st for st in r["stages"] if st.stage == "ADD-03")
    x = next(x for x in s.ops if x.op.id == "ADD-03/7.2")
    new = "VOL-IV:cover/T1/4-G+ADD-03"
    assert x.op.type == "insert_row" and x.applied and x.changed == [new] and s.status == "APPLIED"
    assert s.state[new].cells == {"Form": "4-G", "Title": "Cybersecurity Compliance Undertaking", "Envelope": "A",
                                  "Status": "Mandatory"} and s.state[new].parent == "VOL-IV:cover/T1"
    assert new not in next(st for st in r["stages"] if st.stage == "ADD-02").state
    ev = next(e for e in r["evals"] if e["row"].id == "ADD-03-7.2-01")["stages"]
    assert ev["ADD-03"]["effective_unit"] == new and ev["ADD-03"]["status"] == "NEW" and ev["ADD-03"]["problems"] == []
    assert ev["ADD-03"]["interpretation"]["quote"] in s.state[new].text
    assert ev["ADD-02"]["status"] == "NOT ISSUED"
    rep = {(c["id"], c.get("stage")): c for c in stage2.reported_checks(r)}
    assert rep[("C20", "ADD-03")]["ok"] and rep[("C21-C27", "ADD-03")]["ok"]
    st = {c["id"]: c for c in stage2.structural_checks(r, {"pages": 1, "explicit_ids": []}, {})}
    assert st["C47"]["ok"] and st["C25"]["ok"] and st["C16"]["ok"]
    assert not [t for t in r["trace"] if t["op"] == "ADD-03/7.2"]                   # C46: a row holds the new entry
    a2 = stage2.a2(r)
    ch = next(c for c in a2["changes"] if c["op"] == "ADD-03/7.2")
    assert new in ch["change"] and "Cybersecurity Compliance Undertaking" in ch["change"]


def test_the_drafter_proposes_the_same_insert_row_from_the_prose(blind02):
    from tenderpack.draft import draft
    f = draft(blind02["units"], "ADD-03")
    op = next(o for o in f.ops if o.provision == "ADD-03:7.2")
    assert (op.type, op.target, op.after, op.origin, op.review) == (
        "insert_row", "VOL-IV:cover/T1", "VOL-IV:cover/T1/4-F", "pattern", "proposed")
    assert op.cells == {"Form": "4-G", "Title": "Cybersecurity Compliance Undertaking", "Envelope": "A", "Status": "Mandatory"}
    assert not [d for d in f.dispositions if d.provision == "ADD-03:7.2"]
