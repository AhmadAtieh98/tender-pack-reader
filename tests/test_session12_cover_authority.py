"""Session 12 (blind-05 follow-ups 3 and 4, the owner's part 2): the cover never holds an operative change.

VOL-I 3.2 orders the documents (the Addenda first, a later Addendum prevailing over an earlier one); an addendum's cover
paragraph ("This Addendum amends ...") is the addendum's summary of itself, never an operative provision. In blind-05
the proposer declared the cover's wrong clause number (3.5 for the odour clause 3.4) as a conflict on the operative
op 5.1, and the controller made the op `conflicting`, so a clear change was not promoted. Now a declared conflict that
is only a discrepancy between the cover and an operative provision does not hold the op: it is retained as a cover
finding (a validation record, the controller's report, and a PROPOSED issue in the candidate naming both texts). A
genuine conflict (two operative provisions contradicting each other) still makes the item `conflicting`, as before.

C28 (report only) finds the cover sentence for any verb: "This Addendum consolidates ..." (blind-05) and "relaxes"
(blind-04) are summaries, an unknown verb is a finding ("unknown verb"), never "no summary"; the incorporation
sentence "This Addendum forms part of the RFP Documents and takes precedence ..." is not a summary."""
from __future__ import annotations

from types import SimpleNamespace

from tenderpack.ai.controller import cover_issues, split_cover_conflicts
from tenderpack.summary import parse_claims, summary_sentences

PROVS = ["ADD-03:cover/para3", "ADD-03:2.1", "ADD-03:3.1", "ADD-03:3.3", "ADD-03:3.3(b)", "ADD-03:5.1", "ADD-03:Q19"]


def test_a_conflict_with_the_cover_on_an_operative_op_is_a_cover_discrepancy():
    c = ("ADD-03:cover/para3 names Volume II Clause 3.5 for the odour criterion; the operative provision 5.1 names "
         "Clause 3.4 and quotes words found only in 3.4 (3.5 is the noise clause)")
    cover, genuine = split_cover_conflicts([c], "ADD-03", "ADD-03:5.1", PROVS)
    assert cover == [c] and genuine == []
    c2 = "Cover ADD-03:cover/para3 says 'without change of substance'; the new text moves the modification cut-off"
    assert split_cover_conflicts([c2], "ADD-03", "ADD-03:2.1", PROVS) == ([c2], [])


def test_on_the_cover_item_a_conflict_with_one_operative_provision_is_a_cover_discrepancy():
    c = ("The cover says the 6.6/6.7 consolidation is 'without change of substance', but ADD-03:2.1 shortens the "
         "modification window to two Working Days before the Proposal Due Date (S-I1).")
    assert split_cover_conflicts([c], "ADD-03", "ADD-03:cover/para3", PROVS) == ([c], [])


def test_two_operative_provisions_contradicting_each_other_stay_a_genuine_conflict():
    g = "ADD-03:Q19 says the year-1 figure is in year-1 prices; ADD-03:3.1 puts the Availability Payment at Base Date prices"
    assert split_cover_conflicts([g], "ADD-03", "ADD-03:Q19", PROVS) == ([], [g])
    # the cover named as well does not turn a contradiction between two operative provisions into a cover finding
    g2 = "The cover says nothing of it; ADD-03:Q19 contradicts ADD-03:3.1 on the price basis"
    assert split_cover_conflicts([g2], "ADD-03", "ADD-03:5.1", PROVS) == ([], [g2])
    # a bare answer number is an operative provision too
    g3 = "the cover summary is silent, and Q19 contradicts the Base Date basis of ADD-03:3.1"
    assert split_cover_conflicts([g3], "ADD-03", "ADD-03:5.1", PROVS) == ([], [g3])


def test_a_conflict_that_does_not_name_the_cover_is_genuine():
    g = "The op contradicts an accepted decision on VOL-II:3.4"
    assert split_cover_conflicts([g], "ADD-03", "ADD-03:5.1", PROVS) == ([], [g])


def test_the_retained_cover_discrepancy_becomes_a_proposed_issue_naming_both_texts():
    rec = SimpleNamespace(check="cover_discrepancy", ok=True, detail="x")
    it = SimpleNamespace(id="ADD-03/5.1", provision="ADD-03:5.1", validation=[rec],
                         conflicts=["ADD-03:cover/para3 names Volume II Clause 3.5; the operative provision names 3.4"])
    texts = {"ADD-03:cover/para3": "This Addendum ... replaces the odour criterion in Volume II Clause 3.5 ...",
             "ADD-03:5.1": "In Volume II Clause 3.4, 'not more than 5 OU/m3 at the site boundary' is deleted ..."}
    ps = SimpleNamespace(addendum="ADD-03", items=[it])
    iss = cover_issues(ps, texts, PROVS)
    assert len(iss) == 1
    (iid, v), = iss.items()
    assert iid.startswith("I-ADD-03-COVER-")
    assert "ADD-03:cover/para3" in v["text"] and "ADD-03:5.1" in v["text"]
    assert "Volume II Clause 3.5" in v["text"] and "Volume II Clause 3.4" in v["text"]
    assert "summary" in v["text"] and "not a conflict between operative provisions" in v["text"]
    assert v["show_in_a3"] is False and "review" not in v                     # proposed; nothing decided


# ------------------------------------------------------------------------------------------------ C28

B05 = ("This Addendum consolidates Volume I Clauses 6.6 and 6.7 without change of substance, amends the definition of "
       "Availability Payment and the indexation of the Availability Payment under Volume V Clause 29.2, adds a membrane "
       "filtration requirement to Volume II Clause 3.1, and responds to clarification requests 15 to 21. This Addendum "
       "forms part of the RFP Documents and takes precedence in accordance with Volume I Clause 3.2. Bidders shall "
       "acknowledge receipt in Form 4-A.")


def test_c28_finds_the_cover_sentence_for_any_verb_and_not_the_incorporation_sentence():
    units = [{"unit_id": "ADD-03:cover/para3", "doc": "ADD-03", "kind": "paragraph", "text": B05, "pages": [1]}]
    sents = summary_sentences(units, "ADD-03")
    assert len(sents) == 1 and sents[0][1].startswith("This Addendum consolidates")
    claims = parse_claims(sents[0][1])
    assert claims[0]["verb"] == "consolidates" and claims[0]["kind"] == "unknown"
    assert "Clauses 6.6 and 6.7" in claims[0]["object"]
    assert [c["verb"] for c in claims[1:]] == ["amends", "adds", "responds to"]
    real = ("This Addendum amends the page limit, and responds to clarification requests 7 to 14. This Addendum forms "
            "part of the RFP Documents and takes precedence in accordance with Volume I Clause 3.2.")
    units = [{"unit_id": "ADD-02:cover/para3", "doc": "ADD-02", "kind": "paragraph", "text": real, "pages": [1]}]
    assert [s for _, s in summary_sentences(units, "ADD-02")] == [
        "This Addendum amends the page limit, and responds to clarification requests 7 to 14."]


def test_c28_relaxes_is_still_a_known_verb():
    assert parse_claims("This Addendum relaxes the velocity limit.")[0]["kind"] == "change"


def test_c28_reports_an_unknown_verb_and_a_scope_word_from_a_non_governing_rendering():
    from tenderpack.amend import Engine, OpFile
    from tenderpack.summary import summary_check

    def u(uid, kind, text, doc, page=1):
        return {"unit_id": uid, "doc": doc, "kind": kind, "text": text, "pages": [page]}
    units = [u("VOL-II:5.5", "clause", "The Project Company shall keep the site secure.", "VOL-II"),
             u("ADD-03:cover/para1", "paragraph", "Issued 15 November 2026", "ADD-03"),
             u("ADD-03:cover/para3", "paragraph", "This Addendum consolidates the height rules and inserts a new "
               "Volume II Clause 5.6 limiting the height of permanent structures.", "ADD-03"),
             u("ADD-03:7.2", "clause", "Table 5-1 is issued in the Arabic language. The Arabic text governs.", "ADD-03"),
             u("ADD-03:AppA/T5-1", "table", "المنشآت الدائمة والمؤقتة", "ADD-03", 4),
             u("ADD-03:AppB/T5-1", "table", "Maximum height of permanent structures", "ADD-03", 5)]
    f = OpFile.model_validate({"addendum": "ADD-03", "issued_from": "ADD-03:cover/para1", "prepared_by": "t", "method": "t",
                               "ops": [{"id": "ADD-03/7.2", "provision": "ADD-03:7.2", "type": "annotate",
                                        "effect": "interprets", "targets": ["ADD-03:AppA/T5-1", "ADD-03:AppB/T5-1"],
                                        "precedence": {"governs": "ADD-03:AppA/T5-1", "over": ["ADD-03:AppB/T5-1"],
                                                       "words": "The Arabic text governs."}}],
                               "dispositions": []})
    stages = Engine(units, [f]).run()
    rec = summary_check(stages, units)[0]
    kinds = [x["kind"] for x in rec["findings"]]
    assert "no summary" not in kinds and "unknown verb" in kinds
    scope = [x for x in rec["findings"] if x["kind"] == "scope (governing language)"]
    assert scope and "permanent" in scope[0]["detail"] and "ADD-03:AppB/T5-1" in scope[0]["detail"]


# ------------------------------------------------------------------------------------------------ the controller

def test_validate_set_retains_a_cover_discrepancy_without_holding_the_item_and_keeps_genuine_conflicts(tmp_path):
    """Through validate_set on the real pack (a disposable copy of the curation): the same curated, verifiable item with
    a declared cover discrepancy is not `conflicting` (the record says why, the report keeps it); with a declared
    conflict between two operative provisions it is `conflicting`, as before."""
    import yaml as _yaml

    from test_session10_controls_ai import _disposition, _set, hermetic_workspace  # noqa: E402

    from tenderpack.ai import controller
    ws = hermetic_workspace(tmp_path)
    f = _yaml.safe_load((tmp_path / "curation/amendments/ADD-02.yaml").read_text(encoding="utf-8"))
    p, reason = next((d["provision"], d["reason"]) for d in f["dispositions"]
                     if d["disposition"] == "no_effect" and ":cover/" not in d["provision"])
    cover = _disposition(ws, p, reason)
    cover.conflicts = ["The cover ADD-02:cover/para3 names a different clause from the one this provision amends"]
    genuine = _disposition(ws, p, reason)
    genuine.conflicts = ["ADD-02:Q13 says the periods are unchanged; ADD-02:2.1 changes one of them"]
    ps = _set(ws, "ADD-02", [cover])
    rep = controller.validate_set(ws, ps)
    it = ps.items[0]
    assert it.verification_status != "conflicting", [v.detail for v in it.validation if not v.ok]
    rec = [v for v in it.validation if v.check == "cover_discrepancy"]
    assert rec and rec[0].ok and "never an operative provision" in rec[0].detail
    assert rep["cover_findings"][0]["provision"] == p
    assert "Cover discrepancies (retained" in controller.review_markdown(ps, rep)
    ps2 = _set(ws, "ADD-02", [genuine])
    controller.validate_set(ws, ps2)
    assert ps2.items[0].verification_status == "conflicting"
