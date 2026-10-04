"""Session 10, blind rehearsal 04: fixes made AFTER the answer key was opened (16:42 UTC), so they are not scored
(rehearsals/blind-04/COMPARISON.md). Each failed before its fix.

1. A table issued by an earlier addendum ("Table 1-1 (revised) … issued by Section 3 of Addendum No. 2") was not a
   citation target, so a replace_unit of ADD-02:T1-1-rev by the next addendum's table failed C22 (the proposer
   escalated 6.1 for that reason). The same class as the blind-03 form fix, which covered forms only.
2. C28 did not know the cover verbs "relaxes", "tightens", "divides", "splits" and "makes a conditional amendment to",
   so the whole compound cover sentence fell through as "not found" and every op was reported "omitted".

Synthetic units in the pack's style over the real pack's committed build; nothing is tender content."""
from __future__ import annotations

import copy
import json

import pytest

from tenderpack.amend import Engine, Op, OpFile, load_opfile
from tenderpack.citations import citations, resolve
from tenderpack.summary import parse_claims
from tenderpack.util import ROOT

SIX_ONE = ("Table 1-1 (revised) and the Notes to it, issued by Section 3 of Addendum No. 2, are deleted and replaced "
           "by the table and Notes below, which add criterion G (energy efficiency). The marks for criteria A to F "
           "are unchanged.")


# ---------------------------------------------------------------------------- 1. a table issued by an addendum

def test_a_table_issued_by_an_addendum_is_a_citation_target():
    cites = citations(SIX_ONE)
    assert any(c.kind == "table" and c.target == "ADD-02:T1-1" for c in cites), [(c.kind, c.target) for c in cites]
    ids = {"VOL-I:T1-1/A", "ADD-02:T1-1-rev/A", "ADD-02:T1-1-rev/note(2)", "ADD-03:T1-1/A", "ADD-02:3.1"}
    got = resolve(cites, ids)
    assert "ADD-02:T1-1-rev" in got, got                       # the issue of the table the addendum made
    assert "VOL-I:T1-1" not in got                              # not the Volume I original: the citation names ADD-02
    # a Volume table stays itself, and a bare "Table 1-1" without a document still names nothing
    assert resolve(citations("Table 1-1 of Volume I is deleted"), ids) == ["VOL-I:T1-1"]
    assert resolve(citations("the marks in Table 1-1 are unchanged"), ids) == []


@pytest.fixture(scope="module")
def units():
    base = json.load(open(ROOT / "build/units.json", encoding="utf-8"))["units"]
    rev = {u["unit_id"]: u for u in base if u["unit_id"].startswith("ADD-02:T1-1-rev")}
    add = [{"unit_id": "ADD-03:cover/para1", "doc": "ADD-03", "kind": "paragraph", "text": "Issued 9 November 2026", "pages": [1]},
           {"unit_id": "ADD-03:6.1", "doc": "ADD-03", "kind": "clause", "label": "6.1", "pages": [2], "text": SIX_ONE},
           {"unit_id": "ADD-03:T1-1", "doc": "ADD-03", "kind": "table", "label": "Table 1-1 (second revision) — Technical evaluation criteria",
            "pages": [2], "text": "Table 1-1 (second revision) — Technical evaluation criteria — Ref | Criterion | Marks"}]
    for key in ("A", "B", "C", "D", "E", "F"):
        src = rev[f"ADD-02:T1-1-rev/{key}"]
        u = copy.deepcopy(src)
        u.update({"unit_id": f"ADD-03:T1-1/{key}", "doc": "ADD-03", "pages": [2]})
        add.append(u)
    g = copy.deepcopy(rev["ADD-02:T1-1-rev/A"])
    g.update({"unit_id": "ADD-03:T1-1/G", "doc": "ADD-03", "pages": [2], "label": "G",
              "cells": {**g["cells"], "Ref": "G", "Criterion": "Energy efficiency and specific energy consumption", "Marks": "20"},
              "text": "Ref: G | Criterion: Energy efficiency and specific energy consumption | Marks: 20"})
    add.append(g)
    tot = copy.deepcopy(rev["ADD-02:T1-1-rev/total"])
    tot.update({"unit_id": "ADD-03:T1-1/total", "doc": "ADD-03", "pages": [2],
                "cells": {k: ("120" if k == "Marks" else v) for k, v in tot["cells"].items()},
                "text": tot["text"].replace("100", "120")})
    add.append(tot)
    return base + add


def test_the_next_addendum_can_replace_a_table_the_previous_one_issued(units):
    files = [load_opfile(ROOT / "curation/amendments" / f"{a}.yaml") for a in ("ADD-01", "ADD-02")]
    op = Op(id="ADD-03/6.1", provision="ADD-03:6.1", type="replace_unit", target="ADD-02:T1-1-rev", replacement="ADD-03:T1-1",
            covers=[f"ADD-03:T1-1/{k}" for k in ("A", "B", "C", "D", "E", "F", "G", "total")], origin="assistant", review="proposed")
    f = OpFile(addendum="ADD-03", issued_from="ADD-03:cover/para1", prepared_by="test", method="test", ops=[op])
    st = Engine(units, files + [f]).run()[-1]
    x = next(r for r in st.ops if r.op.id == "ADD-03/6.1")
    assert x.valid, [c for c in x.checks if not c["ok"]]
    assert "ADD-02:T1-1-rev" in x.details["cited"]
    assert x.applied and st.state["ADD-03:T1-1/G"].cells["Marks"] == "20"
    old_row = st.state["ADD-02:T1-1-rev/A"]
    assert old_row.status == "superseded" and old_row.superseded_by == "ADD-03:T1-1/A"       # the rows follow by key


# ---------------------------------------------------------------------------- 2. the cover verbs

COVER = ("This Addendum amends the definition of Estimated Project Cost, the financial capacity requirement in "
         "Volume I Clause 8.4 and the delay liquidated damages in Volume V Clause 18.1, relaxes the velocity limit for "
         "the treated effluent transmission main, amends Section 5.1 of Addendum No. 1, reissues the technical "
         "evaluation table to add a criterion for energy efficiency, divides Volume I Clause 11.3 into two Clauses, "
         "makes a conditional amendment to Volume II Clause 1.4, adds a Declaration of Beneficial Ownership (Form 4-H) "
         "which all Bidders may submit through the Portal within five Working Days after the Proposal Due Date, and "
         "responds to clarification requests 15 to 20.")


def test_every_claim_of_a_compound_cover_sentence_is_split_at_its_verb():
    verbs = [c["verb"] for c in parse_claims(COVER)]
    assert verbs == ["amends", "relaxes", "amends", "reissues", "divides", "makes a conditional amendment to", "adds",
                     "responds to"], verbs
    kinds = {c["verb"]: c["kind"] for c in parse_claims(COVER)}
    assert kinds["relaxes"] == "change" and kinds["divides"] == "change" and kinds["makes a conditional amendment to"] == "change"
    assert [c["verb"] for c in parse_claims("This Addendum tightens the noise limit and splits Clause 4.1 into two Clauses.")] == \
        ["tightens", "splits"]
