"""Session 13 (reviewers R3-3, R3-6, R3-7; R2-6 context): three panel corrections.

  * A4 is the WORK LOG (the brief: the repository with its real commit history, the prompts and model calls, the note
    of every place the system was wrong). The owner: "correct the panel's 'A4 clarification register' label—the work log
    is A4". The panel's deliverables strip and outputs listing named "A4 Clarification register and work log", register
    first; the work log was an unlabelled README.md and the error index, the model calls and the history were not
    linked. Now A4 reads "A4 Work log (...)" and links worklog/README.md, worklog/ERROR_INDEX.md, the model calls and
    subagent briefs (a worklog page) and the commit history (a read-only history page); the clarification register is
    its own "Clarification register (supporting record, drafts not sent)" entry with its md/csv/json.
  * The Stages page lists candidate stages from synthetic (rehearsal) inputs with the same label the Runs page uses.
  * The Decisions table's status and link columns do not wrap mid-word (white-space: nowrap, as Home's .nw)."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
BASE = "/t/tok/"


def _cfg(tmp: Path | None = None):
    return SimpleNamespace(out=ROOT / "out", root=ROOT, evidence=ROOT / "build", pack=ROOT / "config/pack.yaml",
                           staging=(tmp or ROOT) / "staging/ai")


def _line(html: str, label: str) -> str:
    m = re.search(r'<div class="line"><b>' + re.escape(label) + r":</b>(.*?)</div>", html)
    assert m, (label, html[:2000])
    return m.group(1)


def test_a4_is_the_work_log_and_the_register_is_a_separate_supporting_record():
    from tenderpack.panel import views as V
    strip = V.deliverables(BASE, _cfg())
    a4 = _line(strip, "A4 Work log (the repository history, prompts, model calls, errors)")
    assert f'{BASE}file/worklog/README.md"' in a4 and f'{BASE}file/worklog/ERROR_INDEX.md"' in a4
    assert f'href="{BASE}worklog"' in a4 and f'href="{BASE}history"' in a4
    assert "clarification" not in a4.lower()
    reg = _line(strip, "Clarification register (supporting record, drafts not sent)")
    for ext in ("md", "csv", "json"):
        assert f"a4/clarification_register.{ext}" in reg, ext
    assert strip.index("A4 Work log") < strip.index("Clarification register (supporting record")
    home = V.home(BASE, _cfg(), [], "<section>box</section>")
    assert "A4 Clarification register" not in home and "Clarification register and work log" not in home
    assert "A4 Work log (the repository history, prompts, model calls, errors)" in home
    full = home[home.index("Outputs in"):]
    wl = full[full.index("A4 Work log"):full.index("A5 Bid programme")]
    for href in ("file/worklog/README.md", "file/worklog/ERROR_INDEX.md", "worklog\"", "history\""):
        assert BASE + href in wl, href


def test_the_worklog_and_history_pages_list_the_record_read_only():
    from tenderpack.panel import views as V
    page = V.worklog_page(BASE, ROOT / "worklog")
    for words in ("ERROR_INDEX.md", "model_calls/", f"{BASE}file/worklog/README.md",
                  f"{BASE}history"):
        assert words in page, words
    calls = sorted((ROOT / "worklog/model_calls").glob("*.jsonl"))
    if calls:                                                           # (an interview folder starts with none)
        assert f"{BASE}file/worklog/model_calls/{calls[0].name}" in page
    h = V.history_page(BASE, ["0a63e3a 2026-10-05 Session 12 (closing): ..."], None)
    assert "0a63e3a" in h and "read-only" in h
    h2 = V.history_page(BASE, None, "no .git in this folder")
    assert "no .git in this folder" in h2 and "submitted repository" in h2


def test_the_stages_page_labels_synthetic_candidate_stages(tmp_path):
    from tenderpack.panel import views as V
    cfg = _cfg(tmp_path)
    rd = cfg.staging / "runs" / "ADD-03-x"
    (rd / "candidate/build").mkdir(parents=True)
    cp = {"addendum": "ADD-03", "status": "stopped",
          "settings": {"pdf": str(ROOT / "rehearsals/blind-02/input/ADD-03_Addendum_No_3.pdf")}}
    up = {"addendum": "ADD-03", "status": "failed", "settings": {"pdf": str(tmp_path / "staging/panel/uploads/x.pdf")}}
    (cfg.staging / "runs" / "ADD-03-y/candidate").mkdir(parents=True)
    html = V.stages_page(BASE, cfg, [("ADD-03-x", cp), ("ADD-03-y", up)], {},
                         run_jobs={"ADD-03-y": {"meta": {"synthetic": "rehearsals/blind-02/input/ADD-03.pdf"}}})
    rows = re.findall(r"<tr>(.*?)</tr>", html)
    cand = [r for r in rows if "CANDIDATE" in r]
    assert len(cand) == 2 and all("synthetic (rehearsal input)" in r for r in cand), cand
    real = {"addendum": "ADD-04", "status": "stopped", "settings": {"pdf": str(tmp_path / "ADD-04.pdf")}}
    html = V.stages_page(BASE, cfg, [("ADD-04-z", real)], {}, run_jobs={})
    assert "synthetic" not in html


def test_the_decisions_status_and_link_columns_do_not_wrap():
    from tenderpack.panel import views as V
    html = V.decisions_page(BASE, [{"kind": "row", "id": "VOL-I-6.1-01", "status": "proposed", "prompt": "p"}],
                            Counter(), {})
    row = re.findall(r"<tr>(.*?)</tr>", html)[1]
    cells = re.findall(r"<td>(.*?)</td>", row)
    assert cells[2] == '<span class="nw">proposed</span>', cells[2]
    assert 'class="nw"' in cells[-1] and "decide" in cells[-1], cells[-1]
    assert ".nw{white-space:nowrap}" in V.CSS
