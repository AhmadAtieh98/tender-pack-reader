"""Session 13, fixer F3: three findings of reviewer R3 (the review cards, the A3-row set of A5 and A3, the outputs'
index), on the real pack (the committed evidence build, as tests/test_stage2.py reads it) and on synthetic cases.

  R3-2  the review row cards (batch-02, batch-04, batch-05..), where a person accepts or rejects a row, show the
        row's open issues beside the decision block, as the register (A1's Issues cell) gives them: each id with its
        one-line text, its owner, and HUMAN DECISION PENDING where the issue is a person's decision not yet recorded
        (the rule of A3's detail); the "Decision needed" sentence and items.json's decision say "with these open
        issues: ..."; accepting the row records nothing about them;
  R3-5  A5's A3 rows and the A3 page's rows are one set, from one function (schedule.a3_rows), and the C48 line prints
        its members;
  R3-4  out/README.md names A4 as the work log (worklog/) and the clarification register as a supporting record.

Nothing here approves, accepts or decides anything; the decisions and approvals files are only read."""
from __future__ import annotations

import copy
import json
import re

import pytest

from tenderpack import human_owned, schedule, stage2
from tenderpack.util import ROOT

EVIDENCE = ROOT / "build"
PACK = ROOT / "config/pack.yaml"
HDP = human_owned.HUMAN_DECISION_PENDING


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


@pytest.fixture(scope="module")
def issues(real):
    return stage2.collect_issues(real, None)


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp("f3-out") / "out"
    res = stage2.build(EVIDENCE, out, PACK, ROOT, quiet=True)
    assert res["status"] == "ok", res.get("status")
    return out


def _text(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).replace("&amp;", "&")


def _cards(review_dir) -> dict[str, tuple[str, str]]:
    """Row id -> (batch file, the card's text) for every card that asks for a decision on a row (batch 2, 4, 5..)."""
    out = {}
    for f in sorted(review_dir.glob("batch-*.html")):
        if f.name.startswith(("batch-01", "batch-03")):
            continue
        html = f.read_text(encoding="utf-8")
        for m in re.finditer(r'<div class="item" id="([^"]+)">(.*?)(?=<div class="item" id=|</body>)', html, re.S):
            out[m.group(1)] = (f.name, _text(m.group(2)))
    return out


def _a1_cells(built) -> dict[str, list]:
    return {x["id"]: x["issues"] for x in json.loads((built / "a1/a1.json").read_text(encoding="utf-8"))["rows"]}


# ------------------------------------------------------------------------------------------------------------ R3-2

@pytest.mark.parametrize("row, ids", [("VOL-V-3.1-01", ["I-CONCESSION"]),
                                      ("VOL-II-T2-4-ResidualChlorine", ["I-VOL-II-T24-TENSIONS", "I-READING-T24"]),
                                      ("VOL-II-T2-4-pH", ["I-VOL-II-T24-TENSIONS", "I-READING-T24"])])
def test_r3_2_the_row_card_prints_the_rows_open_issues_beside_the_decision(built, issues, row, ids):
    cards = _cards(built / "review")
    assert row in cards, f"{row} has no review card"
    f, card = cards[row]
    by = {i["id"]: i for i in issues}
    for iid in ids:
        assert iid in card, f"{f} {row}: issue {iid} not shown on the card"
        i = by[iid]
        short = stage2.issue_short(i)
        assert _text(short) in card, f"{f} {row}: the one-line text of {iid} is not shown: {short!r}"
        assert f"owner {i['owner']}" in card, f"{f} {row}: the owner of {iid} is not shown"
    assert re.search(r"Decision needed:.*with these open issues: [^.]*" + re.escape(ids[0]), card), card[:600]
    # the human-owned ones (Legal's concession term; the Process engineer's maxima/range question) are labelled
    for iid in ids:
        if str(by[iid].get("human_decision") or "").startswith(HDP):
            assert re.search(re.escape(iid) + r"\W+" + HDP, card), f"{f} {row}: {iid} not labelled {HDP}"
    assert "records nothing about" in card


def test_r3_2_every_card_of_a_row_with_issues_prints_them_and_items_json_says_so(built, issues):
    """Every row card (batch 2, the proposals of batch 4, batches 5..) of a row whose A1 Issues cell names an issue
    prints each id with its owner; items.json's decision names the open ones. The rule reads A1's cell, so an issue the
    register attaches to a row by any route (a relationship's, once propagated) reaches the card the same way."""
    cells = _a1_cells(built)
    by = {i["id"]: i for i in issues}
    cards = _cards(built / "review")
    items = json.loads((built / "review/items.json").read_text(encoding="utf-8"))["items"]
    rows_with = {k for k, v in cells.items() if any(re.search(r"\bI-[A-Z]", str(x)) for x in v)}
    assert len(rows_with) > 50                                   # the real pack: 115 rows carry an issue
    seen = 0
    for rid, (f, card) in cards.items():
        row = rid if rid in cells else next((x["id"] for x in items if x["id"] == rid and x["kind"] == "row"), None)
        if row is None:                                          # a batch-04 card: its id is the proposal's
            row = next(k for k in cells if f"for {k} " in card)
        for entry in cells.get(row) or []:
            for iid in re.findall(r"(?<![\w./-])I-[A-Z][A-Za-z0-9]*(?:[-./][A-Za-z0-9]+)*", str(entry)):
                seen += 1
                assert iid in card, f"{f} {rid}: {iid} (A1 Issues of {row}) not on the card"
                if iid in by:
                    assert f"owner {by[iid]['owner']}" in card, f"{f} {rid}: owner of {iid} missing"
    assert seen > 100
    for x in items:
        if x["kind"] != "row":
            continue
        open_ids = [i for e in cells.get(x["id"]) or [] for i in re.findall(r"(?<![\w./-])I-[A-Z][\w.-]*", str(e))]
        if open_ids:
            assert "with these open issues: " in x["decision"] and all(i in x["decision"] for i in open_ids), x
        else:
            assert "open issues" not in x["decision"], x


def test_r3_2_issue_entries_read_the_a1_cell_as_given_synthetic():
    """The card's rule on a synthetic cell: ids are read from each entry of A1's Issues cell (a relationship-propagated
    entry keeps its route as a note), each with its one-line text and owner; a pending human-owned issue is labelled;
    a decided one is not counted open; an id the issues list does not hold is said to be so, never dropped."""
    from tenderpack.batches import issue_entries, issues_block_html, with_open_issues
    by = {"I-SYN-LEGAL": {"id": "I-SYN-LEGAL", "text": f"{HDP}: which clause governs the term", "owner": "Legal",
                          "short": f"{HDP}: term start, clause A or clause B?", "human_decision": HDP},
          "I-SYN-OPEN": {"id": "I-SYN-OPEN", "text": "Unresolved: whether a note was cut off", "owner": "Owner",
                         "short": "Table X: anything outside the image"},
          "I-SYN-DONE": {"id": "I-SYN-DONE", "text": "DECIDED (decision recorded: A. Person, 2026-10-01): x",
                         "owner": "Legal", "short": "DECIDED (decision recorded: A. Person, 2026-10-01): x",
                         "human_decision": "DECIDED (decision recorded: A. Person, 2026-10-01)"}}
    cell = ["I-SYN-OPEN", "I-SYN-LEGAL (via REL-SYN-1 (confirmed))", "I-SYN-DONE", "I-SYN-GONE",
            "SUMMARY OUT OF DATE: '80,000'"]
    es = issue_entries(cell, by)
    assert [e["id"] for e in es["issues"]] == ["I-SYN-OPEN", "I-SYN-LEGAL", "I-SYN-DONE", "I-SYN-GONE"]
    assert es["flags"] == ["SUMMARY OUT OF DATE: '80,000'"]
    legal = es["issues"][1]
    assert legal["pending"] and legal["owner"] == "Legal" and legal["notes"] == ["via REL-SYN-1 (confirmed)"]
    assert not es["issues"][0]["pending"] and es["issues"][0]["open"]
    assert not es["issues"][2]["open"]                       # a person's recorded decision: listed, not open
    assert es["issues"][3]["open"] and "not in the issues list" in es["issues"][3]["short"]
    html = _text(issues_block_html(es))
    assert f"I-SYN-LEGAL — {HDP}: term start, clause A or clause B? (owner Legal; via REL-SYN-1 (confirmed))" in html
    assert "I-SYN-OPEN — Table X: anything outside the image" in html and "owner Owner" in html
    assert "records nothing about" in html and "SUMMARY OUT OF DATE" in html
    assert with_open_issues(es) == ", with these open issues: I-SYN-OPEN, I-SYN-LEGAL, I-SYN-GONE"
    assert with_open_issues(issue_entries([], by)) == "" and issues_block_html(issue_entries([], by)) == ""
    # the same id twice (directly and through a relationship) is one entry with both routes
    twice = issue_entries(["I-SYN-LEGAL", "I-SYN-LEGAL via REL-SYN-2 (not confirmed)"], by)["issues"]
    assert len(twice) == 1 and twice[0]["notes"] == ["via REL-SYN-2 (not confirmed)"]


def test_r3_2_a_synthetic_row_with_an_issue_in_a_batch_fixture(real, tmp_path):
    """A row of the remaining-rows batches that carries no issue is given a synthetic one owned by Commercial (a
    person's judgment: human_owned.owner_judgment); its card then prints it, labelled, beside the decision, and
    items.json names it; a row without issues keeps the plain sentence."""
    from tenderpack.batches import write_batches
    r = copy.deepcopy(real)
    r["curated_issues"]["I-SYN-PRICE-BASIS"] = {"text": "The price basis the form asks for is not stated",
                                                "owner": "Commercial", "short": "price basis of the form"}
    val = r["validated"].stage
    b2 = ("rejection", "disqualification", "non_responsive", "exclusion", "score_elimination", "document_refusal",
          "criterion_zero")                                  # batch 2's classes: those rows are not in batches 5..
    plain = [e["row"].id for e in r["evals"] if not e["row"].issues
             and getattr(getattr(r["register"].interp_at(e["row"], val), "consequence", None), "cls", None) not in b2]
    target, other = plain[-1], plain[-2]                     # rows with no issue (batches 5..)
    row = next(e["row"] for e in r["evals"] if e["row"].id == target)
    row.issues = ["I-SYN-PRICE-BASIS"]
    out = tmp_path / "review"
    write_batches(r, out, EVIDENCE)
    cards = _cards(out)
    f, card = cards[target]
    assert f.endswith("-rows.html")
    assert f"I-SYN-PRICE-BASIS — {HDP}: price basis of the form" in card and "owner Commercial" in card, card[:900]
    assert "with these open issues: I-SYN-PRICE-BASIS" in card
    assert "open issues" not in cards[other][1]
    items = {x["id"]: x for x in json.loads((out / "items.json").read_text(encoding="utf-8"))["items"]}
    assert "with these open issues: I-SYN-PRICE-BASIS" in items[target]["decision"]
    assert "open issues" not in items[other]["decision"]


# ------------------------------------------------------------------------------------------------------------ R3-5

def test_r3_5_a5_and_the_a3_page_count_one_set_of_a3_rows(real, issues, built):
    val = real["validated"].stage
    one = schedule.a3_rows(real["evals"], val)
    page = stage2.a3(real, issues, None)
    on_page = [*page["explicit_ids"], *(x["id"] for x in page["score"])]
    assert sorted(on_page) == sorted(one), (sorted(set(on_page) ^ set(one)))
    prog = json.loads((built / "a5/stages" / f"{val}.json").read_text(encoding="utf-8"))
    assert sorted(prog["a3_coverage"]["rows"]) == sorted(one)
    # the members as R3 found them: the restating row (shown on the line of the row it restates) and the score row
    assert {"VOL-IV-F4C-N1", "VOL-I-11.3-01"} <= set(one)
    # where the count is printed, the members are printed: C48's line (checks.json and README) and A5's README
    c48 = next(c for c in json.loads((built / "checks.json").read_text(encoding="utf-8"))["reported"] if c["id"] == "C48")
    assert f"{len(one)} A3 " in c48["detail"] and all(k in c48["detail"] for k in one), c48["detail"]
    a5 = (built / "a5/README.md").read_text(encoding="utf-8")
    sec = a5.split("## A3 rows carried by the programme", 1)[1].split("\n## ", 1)[0]
    assert f"({len(one)} A3" in sec and all(f"`{k}`" in sec for k in one)


def test_r3_5_a3_rows_synthetic():
    """In force, with a stated consequence that puts the bid out or returns Envelope B unopened; not a lesser
    consequence, not a refused document, not a row out of force."""
    def ev(rid, status, cls):
        return {"row": type("R", (), {"id": rid})(), "stages": {"S": {"status": status, "interpretation": (
            {"consequence": {"class": cls, "unit": "D:1", "quote": "q"}} if cls else {"consequence": "none_stated"})}}}
    evals = [ev("A", "ACTIVE", "disqualification"), ev("B", "ACTIVE", "score_elimination"),
             ev("C", "ACTIVE", "lesser"), ev("D", "DELETED by ADD-01", "rejection"), ev("E", "ACTIVE", None),
             ev("F", "AMENDED by ADD-02", "non_responsive"), ev("G", "ACTIVE", "document_refusal")]
    assert list(schedule.a3_rows(evals, "S")) == ["A", "B", "F"]
    assert schedule.a3_rows(evals, "S")["B"]["class"] == "score_elimination"


# ------------------------------------------------------------------------------------------------------------ R3-4

def test_r3_4_out_readme_names_a4_as_the_work_log(built):
    md = (built / "README.md").read_text(encoding="utf-8")
    rows = [ln for ln in md.splitlines() if ln.startswith("| A4")]
    assert len(rows) == 1, rows
    a4 = rows[0]
    for w in ("work log", "worklog/", "ERROR_INDEX.md", "model_calls/", "subagent_briefs/", "commit history"):
        assert w in a4, f"A4 row lacks {w!r}: {a4}"
    assert "clarification register" not in a4.lower()
    reg = [ln for ln in md.splitlines() if "clarification register" in ln.lower() and ln.startswith("|")]
    assert len(reg) == 1 and "supporting record" in reg[0].lower() and "a4/clarification_register" in reg[0]
    assert not reg[0].startswith("| A4")


def test_r3_4_the_a4_row_names_what_the_worklog_holds_synthetic(tmp_path):
    """The row names each part of the work log found under the root and says which are absent (never implied)."""
    (tmp_path / "worklog/model_calls").mkdir(parents=True)
    (tmp_path / "worklog/2026-01-01_session-01_x.md").write_text("x", encoding="utf-8")
    row = stage2.a4_work_log_row(tmp_path)
    assert row.startswith("| A4 work log: ") and "worklog/model_calls/" in row and "session logs" in row
    assert "not present: " in row and "ERROR_INDEX.md" in row.split("not present: ", 1)[1]
    assert "subagent_briefs/" in row.split("not present: ", 1)[1] and "`git log`" in row
    assert "no worklog/ folder" in stage2.a4_work_log_row(tmp_path / "none")
