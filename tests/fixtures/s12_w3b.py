"""Session 12 (W3b): helpers over blind rehearsal 05's candidate (tests/fixtures/s12_blind05.py) for the downstream phase.

  workspace(tmp_path_factory)   a Workspace on the candidate's pack and its evidence build (ingested into tmp once)
  promoted(ws)                  the candidate's own ADD-03 ops and dispositions dry-run as the promoted set (tools.simulate)
  dset(ws, items)               a DownstreamSet of hand-written items (this test's data, no model)
  copy_candidate(tmp, rows=..)  a disposable copy of the candidate's curation and config (pack.yaml rewritten to it), with
                                extra rows in a test row file; the PDFs and the evidence build stay the run's (read-only)

Synthetic regression material: never the truth about the tender. Nothing is written under staging/, rehearsals/,
curation/ or out/."""
from __future__ import annotations

import shutil
from pathlib import Path
from types import SimpleNamespace

import yaml

import s12_blind05 as F

CAND = F.PACK.parent
PREFIX = f"staging/ai/runs/{F.RUN}/candidate/"
_C: dict = {}


def workspace(tmp_path_factory):
    from tenderpack.ai.tools import Workspace
    if "ws" not in _C:
        _C["ws"] = Workspace(evidence=F.build(tmp_path_factory), pack=F.PACK, root=F.ROOT)
    return _C["ws"]


def promoted(ws, addendum: str = "ADD-03") -> dict:
    from tenderpack.ai.tools import simulate
    r = ws.require_ok()
    of = next(x for x in r["opfiles"] if x.addendum == addendum)
    sim, r2 = simulate(ws, addendum, [o.model_dump(exclude_none=True) for o in of.ops],
                       [d.model_dump() for d in of.dispositions])
    return {"ops": {o.id: o for o in of.ops}, "dispositions": {}, "dropped": {}, "sim": sim, "r2": r2}


def tasks(ws, prom, addendum: str = "ADD-03"):
    from tenderpack.ai import downstream as DS
    return DS.tasks(ws, SimpleNamespace(addendum=addendum, items=[]), prom, {})


def dset(ws, items, addendum: str = "ADD-03"):
    from tenderpack.ai.contract import DownstreamItem, DownstreamSet
    st = ws.identity()
    return DownstreamSet(run_id="s12-w3b", created="2026-10-05T00:00:00Z", route="recorded", provider="test",
                         model_requested="test", addendum=addendum, state=st,
                         items=[DownstreamItem(state=st, **it) for it in items])


def copy_candidate(tmp: Path, rows: list[dict] | None = None, readings: dict[str, str] | None = None,
                   templates: dict[str, list[dict]] | None = None) -> Path:
    """A copy of the candidate's curation/ and config/ under `tmp` and its pack.yaml pointing there (documents and the
    input PDF stay where they are). `rows`: extra rows written to curation/register/rows/S12-TEST.yaml (this test's data,
    labelled). `readings`: {file name: text appended} to change a reading file in the copy."""
    tmp = Path(tmp)
    for d in ("curation", "config"):
        shutil.copytree(CAND / d, tmp / d, dirs_exist_ok=True)
    text = (CAND / "pack.yaml").read_text(encoding="utf-8")
    for d in ("curation/", "config/"):
        text = text.replace(PREFIX + d, str(tmp / d) + "/")
    pack = tmp / "pack.yaml"
    pack.write_text(text, encoding="utf-8")
    if rows:
        (tmp / "curation/register/rows/S12-TEST.yaml").write_text(yaml.safe_dump(
            {"doc": "ADD-03", "prepared_by": "session 12 test data (not the pack's, not a proposal)",
             "method": "hand-written regression rows", "rows": rows}, allow_unicode=True, sort_keys=False), encoding="utf-8")
    if templates:                                     # extra activities (this test's data) under evidence items
        p = tmp / "curation/activity_templates.yaml"
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        for ev, acts in templates.items():
            data.setdefault(ev, []).extend(acts)
        p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    for name, extra in (readings or {}).items():
        p = tmp / "curation/readings" / name
        p.write_text(p.read_text(encoding="utf-8") + extra, encoding="utf-8")
    return pack
