"""Session 12, fixer F4: the rendering findings of the session-12 audit (reviewer R: R-2, R-3, R-5, R-6) on the real
pack (the committed evidence build, as tests/test_stage2.py reads it). Each test reproduces the finding and states the
general rule the fix makes.

  R-2  what an owner's approval of an image reading covers is said one way everywhere, from the approval record
       (curation/approvals.yaml: the reading as pinned, its translations included where it displays them; the
       entry's own `does_not_cover` list), never "transcription only" when the reading displays translations;
  R-3  the batch-04 header states the proposals' actual states, counted from the data;
  R-5  the A1 xlsx banner (the register's notice) is wrapped and readable in the sheet;
  R-6  wherever relationships are listed, a one-line legend says that a link's "confirmed" means stated in the
       documents, not confirmed by a person.

Nothing here approves, accepts or applies anything; the approvals file is only read."""
from __future__ import annotations

import csv
import math
import re

import pytest
import yaml
from openpyxl import load_workbook

from tenderpack import live, render, stage2
from tenderpack.util import ROOT

EVIDENCE = ROOT / "build"
PACK = ROOT / "config/pack.yaml"
LEGEND_WORDS = "confirmed = stated in the documents"


@pytest.fixture(scope="module")
def real():
    return stage2.run(EVIDENCE, PACK, ROOT)


@pytest.fixture(scope="module")
def issues(real):
    return stage2.collect_issues(real, None)


@pytest.fixture(scope="module")
def batches(real, tmp_path_factory):
    from tenderpack.batches import write_batches
    out = tmp_path_factory.mktemp("review")
    write_batches(real, out, EVIDENCE)
    return out


def _approvals() -> list[dict]:
    return yaml.safe_load((ROOT / "curation/approvals.yaml").read_text(encoding="utf-8"))["approvals"]


def _translated(real, region: str) -> bool:
    return any(u.get("translation") for u in real["units"]
               if (u.get("reading") or {}).get("region") == region and u["kind"] != "region")


def _text(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


# ------------------------------------------------------------------------------------------------------------ R-2

def test_r2_the_approval_scope_reads_the_same_in_the_packets_the_a3_banner_a1_and_the_readme(real, issues, batches):
    apps = _approvals()
    assert apps, "the real pack's approvals are the subject of this test"
    b1 = _text((batches / "batch-01-image-readings.html").read_text(encoding="utf-8"))
    a3 = stage2.a3(real, issues, None)["banner"]
    a1 = stage2.a1_table(real, issues)["notice"]
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for doc, name in ((b1, "batch-01"), (a3, "A3 banner"), (a1, "A1 notice"), (readme, "README")):
        assert not re.search(r"transcriptions? only", doc, re.I), f"{name} narrows the approval to the transcription"
    any_translated = False
    for a in apps:
        rg = a["region_id"]
        tr = _translated(real, rg)
        # the approval record itself says it confirms the displayed translations exactly when the reading has some
        assert tr == ("translation" in str(a.get("notes", "")).lower()), rg
        any_translated |= tr
        what = "the transcription and the displayed translations" if tr else "the transcription"
        sec = b1[b1.index(f"{rg}:"):]
        sec = sec[:sec.index("Points the reading itself records")]
        assert f"The approval covers {what}" in sec, (rg, sec[:600])
        for item in a.get("does_not_cover") or []:                 # the entry's own list, each item's head
            head = re.split(r":| \(", str(item))[0].strip()
            assert head in sec, (rg, head)
        assert f"{rg} ({what.replace('the ', '')})" in a1, (rg, a1)
    if any_translated:
        assert "transcriptions and displayed translations confirmed by the owner" in a3, a3
        assert "transcriptions and displayed translations" in readme


# ------------------------------------------------------------------------------------------------------------ R-3

def test_r3_the_batch04_header_states_the_proposals_states_counted_from_the_data(batches):
    items = [x for x in csv.DictReader(open(batches / "items.csv", encoding="utf-8")) if x["batch"] == "4"]
    counts = {s: sum(1 for x in items if x["status"] == s) for s in ("applied", "superseded", "not applied")}
    assert sum(counts.values()) == len(items) > 0
    page = (batches / "batch-04-stale-proposals.html").read_text(encoding="utf-8")
    intro = _text(page[:page.index('<div class="item"')])
    assert "Prepared, not applied and not accepted" not in intro or counts["applied"] == 0, intro
    assert f"{counts['applied']} applied" in intro, intro
    assert f"{counts['superseded']} superseded" in intro, intro
    assert f"{counts['not applied']} not applied" in intro, intro


def test_r3_the_batch04_intro_is_computed_not_fixed():
    from tenderpack.batches import batch4_intro
    assert "0 applied" in batch4_intro(["not applied", "not applied"], 0)
    assert "2 not applied" in batch4_intro(["not applied", "not applied"], 0)
    t = batch4_intro(["applied", "superseded", "applied"], 1)
    assert "2 applied" in t and "1 superseded" in t and "0 not applied" in t and "1 accepted" in t


# ------------------------------------------------------------------------------------------------------------ R-5

def test_r5_the_a1_xlsx_banner_is_wrapped_merged_and_tall_enough_to_read(real, issues, tmp_path):
    a1 = stage2.a1_table(real, issues)
    render.write_a1(a1, tmp_path)
    wb = load_workbook(tmp_path / "a1.xlsx")
    ws = wb[render.A1_SHEET]
    cell = ws["A2"]
    assert cell.value == a1["notice"] and len(cell.value) > 500
    assert cell.alignment.wrap_text, "the banner is one unwrapped line"
    merged = [m for m in ws.merged_cells.ranges if m.min_row <= 2 <= m.max_row]
    assert len(merged) == 1 and merged[0].min_col == 1 and merged[0].min_row == merged[0].max_row == 2, merged
    ncols = len(a1["columns"])
    assert 2 <= merged[0].max_col <= ncols
    width = sum(c["width"] for c in a1["columns"][:merged[0].max_col])
    lines = math.ceil(len(cell.value) / width)
    assert ws.row_dimensions[2].height and ws.row_dimensions[2].height >= 15 * lines, ws.row_dimensions[2].height
    # every other cell as it was: one merged range only, the title and the header row unchanged
    assert [str(m) for m in ws.merged_cells.ranges] == [str(merged[0])]
    assert ws["A1"].value == a1["title"]
    assert [ws.cell(render.A1_HEADER_ROW, i + 1).value for i in range(ncols)] == [c["header"] for c in a1["columns"]]


# ------------------------------------------------------------------------------------------------------------ R-6

def test_r6_a_legend_says_what_a_links_confirmed_means_wherever_relationships_are_listed(real, issues, tmp_path):
    assert real.get("relationships"), "the real pack has curated relationships"
    a1 = stage2.a1_table(real, issues)
    assert LEGEND_WORDS in a1["notice"], "A1 notice"
    render.write_a1(a1, tmp_path)
    ws = load_workbook(tmp_path / "a1.xlsx")["Relationships"]
    assert LEGEND_WORDS in str(ws["A1"].value), "A1 Relationships sheet"
    hdr = [c.value for c in ws[2]]
    assert hdr[:3] == ["Id", "Kind", "Status"], hdr
    md = stage2.a2(real)["markdown"]
    for sec in md.split("### Reached through relationships")[1:]:
        assert LEGEND_WORDS in sec.split("\n### ")[0][:1500], "A2"
    a3d = stage2.a3(real, issues, None)
    html = stage2.a3_detail_html(a3d)
    assert "Reached through relationships" in html and LEGEND_WORDS in html, "a3_detail"
    text, _ = live.diff(real, "ADD-01", "ADD-02")
    sec = text[text.index("## Reached through relationships"):]
    assert LEGEND_WORDS in sec[:1500], "diff"


# ------------------------------------------------------------------------------------------------------------ R-7

def test_r7_the_readme_ai_paragraph_says_what_ai_routes_and_mac_setup_say():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    para = next(x for x in readme.splitlines() if x.startswith("- **AI layer"))
    assert "automated Codex execution unverified" in (ROOT / "docs/AI_ROUTES.md").read_text(encoding="utf-8")
    assert "automated Codex execution is unverified" in para
    assert "PENDING ON THE MAC" in (ROOT / "docs/MAC_SETUP.md").read_text(encoding="utf-8")
    assert "`docs/MAC_SETUP.md`" in para and "fake local server" in para
    assert "the Claude Code host route has run for real" in para
