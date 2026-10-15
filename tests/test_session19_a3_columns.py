"""Session 19: the main A3 tries the two-column issue layout at level 2 before it drops reasons (level 3).

The timed ADD03 run on the Claude Code route (11 Oct 2026): the candidate's A3 at the validated ADD-02 state listed the
run's new open issues (60 open, 29 listed) and fell to level 3, dropping every issue's reason, while the same content
fits one page at level 2 in two issue columns with each reason cut to ten words (smallest text 7.58 pt). Until now only
the candidate one-page briefing (partial.write_candidate_one_page) tried two columns. The fixture is that run's
a3.json (the synthetic drill ADD03 on the interview demo's ADD-02 baseline)."""
from __future__ import annotations

import json
from pathlib import Path

from tenderpack import stage2
from tenderpack.render import A3_SCALE_LOW

FIXTURE = Path(__file__).resolve().parent / "fixtures/session19_a3_add03_candidate_state.json"


def test_a3_pages_offers_two_columns_at_level_two_before_dropping_reasons():
    a3d = json.loads(FIXTURE.read_text(encoding="utf-8"))
    seen = [(level, words, page.get("issue_columns", 1)) for level, words, page in stage2.a3_pages(a3d)]
    first_level3 = next(i for i, (level, _, _) in enumerate(seen) if level == 3)
    level2 = [(w, c) for level, w, c in seen[:first_level3] if level == 2]
    assert level2 == [(None, 1), (None, 2), (16, 1), (16, 2), (10, 1), (10, 2)]


def test_the_crowded_a3_keeps_its_reasons_on_one_page(tmp_path):
    a3d = json.loads(FIXTURE.read_text(encoding="utf-8"))
    fit = stage2.fit_a3(a3d, tmp_path / "a3.pdf")
    assert fit["pages"] == 1 and fit["condensed"] == 2 and fit["issue_columns"] == 2, fit
    assert fit["scale"] >= A3_SCALE_LOW and fit["min_text_pt"] >= 7.5, fit
    assert a3d["condensed"] == 2 and a3d["issue_columns"] == 2


def test_an_a3_that_fits_one_column_keeps_one_column(tmp_path):
    a3d = json.loads((Path(__file__).resolve().parents[1] / "out/a3/a3.json").read_text(encoding="utf-8"))
    fit = stage2.fit_a3(a3d, tmp_path / "a3.pdf")
    assert fit["condensed"] == 2 and fit["issue_columns"] == 1 and "reason_words" not in fit, fit
