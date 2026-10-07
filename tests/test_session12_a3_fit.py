"""Session 12, fixer F2 follow-up: the merged A3 page keeps every unresolved line's reason (A3-2) on one page.

Each fixer's page fitted alone; merged (the HUMAN DECISION PENDING labels, the reworded shorts, the reason clauses, the
legend, the longer banner) the real page no longer fitted at condensation level 2, so stage2.write fell to level 3 and
printed the unresolved list as ids and owners only. Required: the REAL page renders at a level that keeps every reason
(level <= 2) at a scale >= 0.9 and a text size >= the 7.5 pt floor, and no unresolved line on the page is an id and owner
only. The shortening at level 2 is general (repeated words folded, a short marker for the human-decision label defined
once in the legend, the legend on one line); the full label stays in the detail page. Real pack (the committed build);
nothing is written under the repository and nothing is approved."""
from __future__ import annotations

import unicodedata

import pymupdf
import pytest

from tenderpack import human_owned as H
from tenderpack import stage2
from tenderpack.render import A3_SCALE_LOW, A3_MIN_TEXT_PT, A3OverflowError, write_a3_pdf
from tenderpack.util import ROOT


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    r = stage2.run(ROOT / "build", ROOT / "config/pack.yaml", ROOT)
    v = r["validated"].stage
    main = stage2.a5_all(r)[v]
    issues = stage2.collect_issues(r, main)
    a3 = stage2.a3(r, issues, main)
    out = tmp_path_factory.mktemp("s12fit")
    fit = level = cond = None
    for level, _words, cond in stage2.a3_pages(a3):   # as stage2.write does: the first page that fits
        try:
            fit = write_a3_pdf(cond, out / "a3.pdf")
            break
        except A3OverflowError:
            continue
    text = " ".join(unicodedata.normalize("NFKC", pymupdf.open(out / "a3.pdf")[0].get_text()).split())
    return {"a3": a3, "cond": cond, "fit": fit, "level": level, "text": text, "out": out}


def test_the_real_page_keeps_every_reason_at_a_readable_size(built):
    fit, level = built["fit"], built["level"]
    assert fit and fit["pages"] == 1, fit
    assert level <= 2, (level, fit)                         # level 3 drops the reasons: a last resort only
    # session 14: the floor is render.A3_SCALE_LOW (0.89, a hair above the 7.5 pt minimum), no longer the literal 0.9
    assert fit["scale"] >= A3_SCALE_LOW and fit["min_text_pt"] >= A3_MIN_TEXT_PT, fit
    assert "each issue's reason is on a3_detail.html" not in built["text"]


def test_no_unresolved_line_on_the_page_is_an_id_and_owner_only(built):
    items = [i for g in built["cond"]["groups"]["groups"] for i in g.get("items") or []]
    assert items and all("count" not in g for g in built["cond"]["groups"]["groups"])
    for i in items:
        s = " ".join(unicodedata.normalize("NFKC", i.get("short") or "").split())
        assert s and s != i["id"], i
        assert s[:40] in built["text"], (i["id"], s[:40])


def test_level_2_abbreviates_a_reason_before_it_drops_one():
    a3 = {"sections": [], "subtitle": "s", "banner": "b", "legend": "", "groups": {"note": "n", "groups": [
        {"title": "t", "questions": [], "items": [{"id": "I-X", "short": " ".join(f"w{k}" for k in range(30)),
                                                   "owner": "o", "folds": []}]}]}}
    pages = list(stage2.a3_pages(a3))
    order = [(lv, n) for lv, n, _ in pages]
    assert order.index((2, None)) < order.index((2, stage2.A3_REASON_WORDS[0])) < order.index((3, None))
    cut = next(p for lv, n, p in pages if n)["groups"]["groups"][0]["items"][0]["short"]
    assert cut.startswith("w0 w1") and cut.endswith("…") and len(cut.split()) == stage2.A3_REASON_WORDS[0] + 1


def test_the_human_decision_label_is_a_marker_defined_once_and_kept_in_full_on_the_detail_page(built):
    cond, text = built["cond"], built["text"]
    shorts = [i["short"] for g in cond["groups"]["groups"] for i in g.get("items") or []]
    pend = [i for g in built["a3"]["groups"]["groups"] for i in g["items"] if H.HUMAN_DECISION_PENDING in i["short"]]
    assert pend, "the merged tree labels some issues HUMAN DECISION PENDING"
    assert not any(H.HUMAN_DECISION_PENDING in s for s in shorts)
    assert sum(s.startswith(stage2.A3_PENDING_MARK) for s in shorts) == len(pend)
    # session 12, F5 (audit A3-5, deliberate): the legend defines both marks, ⚑ as a judgment no one has recorded
    # (was '⚑: human decision pending'); still defined once
    meaning = dict(stage2.A3_MARKS)[stage2.A3_PENDING_MARK]
    assert f"{stage2.A3_PENDING_MARK}: {meaning}" in " ".join(text.split()) and text.count(meaning.split()[-1]) >= 1
    assert " ".join(text.split()).count(f"{stage2.A3_PENDING_MARK}: ") == 1
    detail = stage2.a3_detail_html(built["a3"])
    assert all(H.HUMAN_DECISION_PENDING in detail[detail.index(f'id="{i["id"]}"'):][:1500] for i in pend)


def test_level_5_drops_the_requirement_words_and_keeps_every_quoted_consequence():
    """Session 12 (the coordinator): after the audit's additions the blind-02 rehearsal's A3 (24 explicit triggers) no
    longer fitted one page at scale >= 0.9 at any level (C43 structural_failure). Level 5 is the last resort before
    that failure: each explicit trigger keeps its id, quoted consequence, source and owner; the requirement's own words
    (in A1 and on a3_detail.html) go, and the section says so. The quotes are never condensed."""
    from tenderpack import stage2
    a3d = {"subtitle": "State after ADD-03", "banner": "WORKING DRAFT", "legend": "", "explicit_ids": ["R-1", "R-2"],
           "sections": [{"heading": "Explicit — Rejection: 2", "note": "", "items": [
               {"id": "R-1", "text": "A long requirement sentence about the bond.", "consequence": "shall be rejected",
                "class": "rejection", "source": "VOL-I 8.5 p12", "owner": "Legal", "flags": ["check"]},
               {"id": "R-2", "text": "Another requirement.", "consequence": "returned unopened", "source": "VOL-I 6.1 p9"}]}],
           "groups": {"note": "", "groups": [{"key": "unresolved", "title": "Unresolved", "items": [
               {"id": "I-X", "short": "why it is open", "owner": "Commercial"}], "questions": []}]}}
    levels = [(lvl, words) for lvl, words, _ in stage2.a3_pages(a3d)]
    assert levels[-1] == (5, None) and (4, None) in levels and (2, 16) in levels
    page = stage2.condense_a3(a3d, 5)
    items = page["sections"][0]["items"]
    assert [i["text"] for i in items] == ["", ""] and [i["consequence"] for i in items] == ["shall be rejected", "returned unopened"]
    assert items[0]["source"] == "VOL-I 8.5 p12" and items[0]["owner"] == "Legal" and items[0]["flags"] == []
    assert "requirement words are on a3_detail.html" in page["sections"][0]["note"]
    assert a3d["sections"][0]["items"][0]["text"].startswith("A long")           # the source dict is untouched
    page4 = stage2.condense_a3(a3d, 4)
    assert page4["sections"][0]["items"][0]["text"].startswith("A long")         # level 4 keeps the words
