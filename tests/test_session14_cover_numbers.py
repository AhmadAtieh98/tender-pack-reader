"""Session 14 (W2; the blind-07 scorer's defect 12, rehearsals/blind-07/COMPARISON.md §8 item 12; report §9 L28).

The cover check (C28, tenderpack/summary.py) split the summary at every comma, inside "SAR 4,000,000" too, and did not
know the verbs "relocates", "invites" or "provides for", so blind-07's cover became three mixed segments reported "not
found", and no figure, count or modality was compared with the operative provisions: none of the three planted cover
errors (E1 a stale-base figure, E2 "invites" against "shall demonstrate", E3 "four asset classes" against a five-row
table) was named. The cover sentence and the provision texts below are the frozen run's own words
(rehearsals/blind-07/out-candidate/a1/a1.csv L40, a2/a2_provisions.json); the stages around them are this test's data
(synthetic: VOL-V 36.2's figures are the ones the run's files state, 5,000,000 as issued and 2,500,000 after ADD-02)."""
from __future__ import annotations

from types import SimpleNamespace as NS

from tenderpack import summary as S

COVER = ("This Addendum reduces the threshold in Volume V Clause 36.2 for compensation for a General Change in Law to SAR "
         "4,000,000, relocates the handback condition survey from Volume II to Volume V, replaces the remaining design "
         "life required at handback with minimum residual service lives for four asset classes set out in Table 42-1 "
         "(issued in Arabic), invites Bidders to describe in their Technical Proposals how their lifecycle plans address "
         "Table 42-1, inserts a new Volume V Clause 12.5 on adverse ground conditions and requires Bidders to state the "
         "ground conditions assumed for the design of foundations, provides for the inspection of borehole cores and "
         "laboratory records with a limited exception to Volume I Clause 4.2, and responds to clarification requests 15 "
         "to 19.")
PROV = {
    "ADD-03:2.1": "The amount stated in Volume V Clause 36.2 is reduced by SAR 1,000,000.",
    "ADD-03:3.1": "Volume II Clause 8.5 is relocated to Volume V, in which it becomes Clause 42.3. Its text is unchanged "
                  "and reads as follows: ‘42.3  A handback condition survey shall be carried out in the final two (2) "
                  "years of the concession’",
    "ADD-03:3.4": "In Volume V Clause 42.1, ‘with a remaining design life of not less than five (5) years for all major "
                  "assets’ is deleted and ‘with a residual service life, for each asset class, of not less than that "
                  "stated in Table 42-1’ is substituted.",
    "ADD-03:3.6": "The Bidder shall demonstrate in the Technical Proposal how its lifecycle plan achieves the residual "
                  "service lives in Table 42-1.",
}
VOLV_362 = "The Authority shall compensate the Project Company where the cost of a General Change in Law exceeds {}."


def _u(uid, text, kind="clause", doc=None):
    return NS(unit_id=uid, doc=doc or uid.split(":")[0], kind=kind, status="active", text=text, cells=None, label=None)


def _stages():
    base = {"VOL-V:36.2": _u("VOL-V:36.2", VOLV_362.format("SAR 5,000,000"))}
    add2 = {"VOL-V:36.2": _u("VOL-V:36.2", VOLV_362.format("SAR 2,500,000"))}
    add3 = dict(add2)
    add3["ADD-03:cover/para3"] = _u("ADD-03:cover/para3", COVER, "paragraph")
    for k, t in PROV.items():
        add3[k] = _u(k, t)
    for n in range(1, 6):                                  # the English table and the Arabic image table: five rows each
        add3[f"ADD-03:T42-1/{n}"] = _u(f"ADD-03:T42-1/{n}", f"No: {n}", "table_row")
        add3[f"ADD-03:T42-1/image/r{n}"] = _u(f"ADD-03:T42-1/image/r{n}", f"م: {n}", "table_row")
    cov = [{"provision": k, "disposition": "unresolved", "text": t, "reason": "test data"} for k, t in PROV.items()]
    return [NS(stage="BASE", addendum=None, state=base, ops=[], coverage=[]),
            NS(stage="ADD-02", addendum="ADD-02", state=add2, ops=[], coverage=[]),
            NS(stage="ADD-03", addendum="ADD-03", state=add3, ops=[], coverage=cov)]


UNITS = [{"unit_id": "ADD-03:cover/para3", "doc": "ADD-03", "kind": "paragraph", "text": COVER, "pages": [1]}] + \
        [{"unit_id": k, "doc": "ADD-03", "kind": "clause", "text": t, "pages": [1]} for k, t in PROV.items()]


def _rec():
    return next(x for x in S.summary_check(_stages(), UNITS, {}) if x["addendum"] == "ADD-03")


def test_numbers_are_read_whole_and_mid_sentence_verbs_start_a_claim():
    claims = S.parse_claims(COVER)
    assert [c["verb"] for c in claims] == ["reduces", "relocates", "replaces", "invites", "inserts", "requires",
                                           "provides for", "responds to"], [c["text"] for c in claims]
    assert claims[0]["text"].endswith("to SAR 4,000,000"), claims[0]
    assert S.figures("SAR 4,000,000")[0]["value"] == 4_000_000


def test_no_claim_of_the_frozen_cover_is_reported_not_found_as_a_mixed_segment():
    rec = _rec()
    nf = [f for f in rec["findings"] if f["kind"] == "not found"]
    assert not any("relocates" in f["detail"] and "reduces" in f["detail"] for f in nf), nf
    assert not any("000, 000" in f["detail"] for f in rec["findings"]), rec["findings"]


def test_e1_the_figure_is_compared_with_the_operative_provision_and_the_base_it_amends():
    rec = _rec()
    f = [x for x in rec["findings"] if x["kind"] == "figure differs"]
    assert len(f) == 1 and f[0]["claim"] == 1, rec["findings"]
    d = f[0]["detail"]
    assert "SAR 4,000,000" in d and "reduced by SAR 1,000,000" in d          # both texts quoted
    assert "SAR 1,500,000" in d and "arithmetic for a person to check" in d  # the computed value, labelled as such
    assert "SAR 5,000,000" in d and "superseded base" in d                   # the mechanism of the error
    assert next(c for c in rec["claims"] if c["n"] == 1)["status"] == "contradicted"


def test_e2_the_modal_word_is_compared():
    rec = _rec()
    f = [x for x in rec["findings"] if x["kind"] == "modality differs"]
    assert any(x["claim"] == 4 and "ADD-03:3.6" in x["detail"] and "shall demonstrate" in x["detail"]
               and "invites Bidders to describe" in x["detail"] for x in f), rec["findings"]


def test_e3_the_count_is_compared_with_the_rows_of_the_table():
    rec = _rec()
    f = [x for x in rec["findings"] if x["kind"] == "count differs"]
    assert any(x["claim"] == 3 and "four asset classes" in x["detail"] and "5 row(s)" in x["detail"] for x in f), \
        rec["findings"]


def test_an_accurate_claim_is_not_reported():
    stages = _stages()
    stages[2].state["ADD-03:cover/para3"].text = COVER.replace("4,000,000", "1,500,000").replace("four asset", "five asset") \
        .replace("invites Bidders to describe", "requires Bidders to demonstrate")
    units = [dict(UNITS[0], text=stages[2].state["ADD-03:cover/para3"].text)] + UNITS[1:]
    rec = next(x for x in S.summary_check(stages, units, {}) if x["addendum"] == "ADD-03")
    assert not [x for x in rec["findings"] if x["kind"] in S.OPERATIVE_KINDS], rec["findings"]
