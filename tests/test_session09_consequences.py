"""Session 09: the consequence vocabulary separates three things it had conflated (blind rehearsal 02).

  document_refusal  a stated refusal of a submitted document ("will not be accepted", "treated as not submitted") whose
                    effect on the Proposal is not stated: A3 lists it under "Document refused" with the refusal's words,
                    and the row keeps its place in the VOL-I 11.1(i) general gate; never shown as a disqualification
  criterion_zero    zero marks under one scoring criterion: scored, listed apart from "Envelope B returned unopened"
                    (the VOL-I 11.3 threshold, score_elimination) and never as a disqualification
  BID_OUT           unchanged

In the scored blind output the curator had to choose between `lesser` (which took Q15 and Q16 off A3) and
`score_elimination` (which labelled note (3) "Envelope B returned unopened"). The real pack has no such rows, so its
A3 is unchanged (checked by a build of the real pack against out/a3; see the session report).
"""
from __future__ import annotations

import json

import pytest
import yaml

from tenderpack import stage2, trace
from tenderpack.register import BID_OUT, CONSEQUENCE_CLASSES, Consequence
from tenderpack.util import ROOT

B = ROOT / "rehearsals/blind-02"
REFUSED = {"VOL-I-6.4-02", "VOL-I-9.1h-01", "ADD-03-Q16-01"}


def test_the_two_classes_exist_and_are_not_bid_out():
    for cls in ("document_refusal", "criterion_zero"):
        assert cls in CONSEQUENCE_CLASSES and cls not in BID_OUT and cls in stage2.CLASS_WORDS
        Consequence.model_validate({"class": cls, "unit": "ADD-03:Q15", "quote": "will not be accepted"})
    assert "disqualif" not in stage2.CLASS_WORDS["document_refusal"].replace("not a disqualification", "")
    assert "not a disqualification" in stage2.CLASS_WORDS["criterion_zero"]
    assert BID_OUT == ("rejection", "disqualification", "non_responsive", "exclusion")


def test_refusal_and_zero_marks_words_are_consequence_words_for_c46():
    assert trace._consequence_words("A Power of Attorney that does not comply will be treated as not submitted.") == {
        "treated as not submitted"}
    assert "will not be accepted" in trace._consequence_words("A Bid Bond issued by a branch will not be accepted.")
    assert trace._consequence_words("The Technical Proposal will be awarded no marks under criterion A.") == {
        "awarded no marks"}
    assert trace._consequence_words("Proposals scoring at least seventy (70) marks proceed.") == set()


@pytest.fixture(scope="module")
def blind02(tmp_path_factory):
    r = stage2.run(B / "build", B / "work/pack.yaml", ROOT)
    out = tmp_path_factory.mktemp("b02") / "out"
    return {"r": r, "res": stage2.write(r, out), "out": out}


def section(a3, start):
    return next((s for s in a3["sections"] if s["heading"].startswith(start)), None)


def test_blind02_document_refusals_are_listed_with_their_words_and_stay_in_the_gate(blind02):
    a3 = blind02["res"]["a3"]
    sec = section(a3, "Document refused (stated; the Proposal's fate is not stated: VOL-I 11.1(i) gate applies): 3")
    assert sec is not None and {i["id"] for i in sec["items"]} == REFUSED
    words = {i["id"]: i["text"] for i in sec["items"]}
    assert "will not be accepted" in words["VOL-I-6.4-02"] and "ADD-03 Q15" in next(
        i["source"] for i in sec["items"] if i["id"] == "VOL-I-6.4-02")
    assert all("treated as not submitted" in words[k] for k in ("VOL-I-9.1h-01", "ADD-03-Q16-01"))
    gate = section(a3, "General gate")
    assert REFUSED <= set(gate["ids"]) and gate["heading"].endswith(f": {len(gate['ids'])}")
    assert REFUSED <= set(a3["gate_ids"]) and not REFUSED & set(a3["none_stated_ids"])
    assert not REFUSED & set(a3["explicit_ids"])                      # never a disqualification
    for s in a3["sections"]:
        if s["heading"].startswith("Explicit"):
            assert not REFUSED & {i["id"] for i in s["items"]}


def test_blind02_zero_marks_on_one_criterion_is_not_the_threshold(blind02):
    a3 = blind02["res"]["a3"]
    zero = section(a3, "Criterion-level zero marks (scored; not a disqualification): 1")
    assert [i["id"] for i in zero["items"]] == ["ADD-03-T22n3-01"]
    assert "awarded no marks under criterion A" in zero["items"][0]["consequence"]
    threshold = section(a3, "Explicit — Envelope B returned unopened")
    assert "ADD-03-T22n3-01" not in {i["id"] for i in threshold["items"]} and "ADD-03-T22n3-01" not in a3["explicit_ids"]
    assert "ADD-03-T22n3-01" not in section(a3, "General gate")["ids"]


def test_blind02_checks_pass_and_the_outputs_say_it(blind02):
    res, out = blind02["res"], blind02["out"]
    st = {c["id"]: c for c in res["checks"]}
    assert res["status"] == "ok" and st["C13"]["ok"] and st["C43"]["ok"] and st["C16"]["ok"]
    assert {c["id"]: c for c in res["reported"]}["C46"]["ok"]
    assert not [t for t in blind02["r"]["trace"] if t["output"] == "A3"]
    # the refusal words of Q15 are carried by the document_refusal consequence, not by a disposition note any more
    assert not (blind02["r"]["dispositions"]["VOL-I:6.4"].consequence_note or "").strip()
    pdf_text = __import__("pymupdf").open(out / "a3/a3.pdf")[0].get_text()
    assert "Document refused" in pdf_text and "Criterion-level zero marks" in pdf_text
    detail = (out / "a3/a3_detail.html").read_text(encoding="utf-8")
    assert "Document refused (the Proposal&#x27;s fate" in detail or "Document refused (the Proposal's fate" in detail
    a1 = json.loads((out / "a1/a1.json").read_text(encoding="utf-8"))
    row = next(x for x in a1["rows"] if x["id"] == "VOL-I-6.4-02")
    assert row["consequence"].startswith("document refused (the Proposal's fate is not stated")


def test_blind02_the_sealed_keys_a3_delta_is_met_for_q15_q16_and_note_3(blind02):
    key = yaml.safe_load((B / "SEALED/expected_findings.yaml").read_text(encoding="utf-8"))["a3_delta"]
    assert any(x.startswith("Q15:") for x in key["add_or_update"]) and any(x.startswith("Q16:") for x in key["add_or_update"])
    assert any(x.startswith("Note (3):") for x in key["not_disqualifying_but_flag"])
    a3 = blind02["res"]["a3"]
    refused = {i["id"]: i for i in section(a3, "Document refused")["items"]}
    assert "ADD-03 Q15" in refused["VOL-I-6.4-02"]["source"]                          # Q15: on A3 (inferential link)
    assert "ADD-03 Q16" in refused["ADD-03-Q16-01"]["source"]                         # Q16: on A3
    assert {"VOL-I-6.4-02", "VOL-I-9.1h-01"} <= set(section(a3, "General gate")["ids"])   # both back in the gate
    note3 = section(a3, "Criterion-level zero marks")["items"][0]                       # note (3): flagged, not a
    assert note3["id"] == "ADD-03-T22n3-01"                                              # disqualification
    ev = next(e for e in blind02["r"]["evals"] if e["row"].id == "ADD-03-T22n3-01")["stages"]["ADD-03"]
    assert "threshold" in ev["interpretation"]["note"] and "75" in ev["interpretation"]["note"]
