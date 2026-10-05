"""Session 12 (W3a): blind rehearsal 05's candidate as regression material, built once per test session.

The candidate workspace the workflow produced in blind-05 is committed under
staging/ai/runs/ADD-03-run-host-blind05-20261005T025444Z/candidate/ (its pack, its curation and the addendum PDF; its
evidence build is not). It is ingested afresh into a disposable folder (about 17 s) and stage2.run is computed once;
nothing is written under staging/, rehearsals/, curation/ or out/. Synthetic material: used to reproduce how the
outputs signal changes, never as the truth about the tender. Treat the run as read-only (deep-copy before changing)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = "ADD-03-run-host-blind05-20261005T025444Z"
PACK = ROOT / "staging" / "ai" / "runs" / RUN / "candidate" / "pack.yaml"
_CACHE: dict = {}


def build(tmp_path_factory) -> Path:
    if "build" not in _CACHE:
        from tenderpack.cli import ingest
        out = tmp_path_factory.mktemp("s12-blind05") / "build"
        res = ingest(PACK, out, ROOT, quiet=True)
        assert res["exit_code"] == 0, res.get("status")
        _CACHE["build"] = out
    return _CACHE["build"]


def run(tmp_path_factory) -> dict:
    """{"r": stage2.run of the candidate, "build": its evidence build, "pack": its pack.yaml}."""
    if "r" not in _CACHE:
        from tenderpack import stage2
        b = build(tmp_path_factory)
        _CACHE["r"] = stage2.run(b, PACK, ROOT)
    return {"r": _CACHE["r"], "build": _CACHE["build"], "pack": PACK}
