"""Drill B rehearsal: a second synthetic Addendum No. 3 through the same path, as in the live session.

  1. build the drill pack (tests/fixtures/make_drill_b.py) and ingest it            -> <root>/src, <root>/build
  2. outputs with ADD-03 drafted by tenderpack.draft (no curated op file)           -> <root>/out-drafted
  3. curation: the files in this folder (op file, rows, evidence item, A5 template, lead time) are copied into
     a COPY of the register and configuration inside <root>/src (never into curation/ or config/)
  4. outputs with the curated op file                                                -> <root>/out-curated
Optionally (`fixture_review=True`, disposable runs only): before step 4, the Table 2-4 reading is approved and
two rows are accepted by "Fixture Test Reviewer" in the drill copy, to show what happens to an earlier approved
state. Nothing is ever approved in the repository; the committed rehearsal outputs are made without it.

Usage: python tests/fixtures/drill_b/rehearse.py ROOT_DIR [--fixture-review]
"""
from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE.parent))

FIXTURE_REVIEWER = "Fixture Test Reviewer"
ACCEPTED_ROWS = ("VOL-I-5.2-01", "VOL-I-9.3-01")       # one ADD-03 touches, one it does not


def _rel(p: Path) -> str:
    p = Path(p).resolve()
    return p.relative_to(REPO).as_posix() if p.is_relative_to(REPO) else p.as_posix()


def prepare(src: Path) -> None:
    """Before ingest: the drill pack points at its own copies of the register and configuration, so that the
    curation step only ADDS files (the pack file, a Stage 1 input, never changes after ingest)."""
    for name, origin in (("register", REPO / "curation/register"), ("evidence_items", REPO / "curation/evidence_items")):
        if (src / name).exists():
            shutil.rmtree(src / name)
        shutil.copytree(origin, src / name)
    shutil.copy(REPO / "curation/activity_templates.yaml", src / "activity_templates.yaml")
    shutil.copy(REPO / "config/assumptions.yaml", src / "assumptions.yaml")
    reg, ev = src / "register", src / "evidence_items"
    cfg = yaml.safe_load((src / "pack.yaml").read_text(encoding="utf-8"))
    cfg.update({"register": _rel(reg / "rows.yaml"), "issues": _rel(reg / "issues.yaml"),
                "dispositions_dir": _rel(reg / "dispositions"), "evidence_items_dir": _rel(ev),
                "activity_templates": _rel(src / "activity_templates.yaml"), "assumptions": _rel(src / "assumptions.yaml")})
    (src / "pack.yaml").write_text(yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")


def curate(src: Path, fixture_review: bool = False) -> None:
    """Step 3: add the curated ADD-03 files to the drill's copies (op file, rows, evidence item, A5 template,
    PROVISIONAL lead time). With fixture_review, two rows are marked accepted by the fixture reviewer."""
    (src / "amendments" / "ADD-03.yaml").write_bytes((HERE / "ADD-03.yaml").read_bytes())
    reg = src / "register"
    shutil.copy(HERE / "rows-ADD-03.yaml", reg / "rows" / "ADD-03.yaml")
    shutil.copy(HERE / "evidence-ADD-03.yaml", src / "evidence_items" / "ADD-03.yaml")
    tpl = yaml.safe_load((src / "activity_templates.yaml").read_text(encoding="utf-8"))
    tpl.update(yaml.safe_load((HERE / "templates-ADD-03.yaml").read_text(encoding="utf-8")))
    (src / "activity_templates.yaml").write_text(yaml.safe_dump(tpl, allow_unicode=True, sort_keys=False), encoding="utf-8")
    asm = yaml.safe_load((src / "assumptions.yaml").read_text(encoding="utf-8"))
    asm["lead_times"].update(yaml.safe_load((HERE / "lead-times-ADD-03.yaml").read_text(encoding="utf-8")))
    (src / "assumptions.yaml").write_text(yaml.safe_dump(asm, allow_unicode=True, sort_keys=False), encoding="utf-8")
    if fixture_review:
        rows = yaml.safe_load((reg / "rows.yaml").read_text(encoding="utf-8"))
        for r in rows["rows"]:
            if r["id"] in ACCEPTED_ROWS:
                r["review"], r["reviewer"] = "accepted", FIXTURE_REVIEWER
        (reg / "rows.yaml").write_text(yaml.safe_dump(rows, allow_unicode=True, sort_keys=False), encoding="utf-8")


def rehearse(root: Path, fixture_review: bool = False, quiet: bool = True) -> dict:
    import make_drill_b
    from tenderpack import stage2
    from tenderpack.cli import approve, ingest
    root = Path(root)
    src, build = root / "src", root / "build"
    t = {}
    t0 = time.perf_counter()
    expected = make_drill_b.build(src)
    for leftover in (src / "amendments" / "ADD-03.yaml", src / "approvals.yaml"):   # a rerun starts undrafted, unreviewed
        leftover.unlink(missing_ok=True)
    prepare(src)
    t["1 build drill pack"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    res = ingest(src / "pack.yaml", build, REPO, quiet=True)
    t["1 ingest (Stage 1, 7 documents)"] = time.perf_counter() - t0
    assert res["exit_code"] == 0, res["exit_code"]
    t0 = time.perf_counter()
    drafted = stage2.build(build, root / "out-drafted", src / "pack.yaml", REPO, quiet=quiet)
    t["2 outputs with ADD-03 drafted"] = time.perf_counter() - t0
    curate(src, fixture_review)
    if fixture_review:
        cfg = yaml.safe_load((src / "pack.yaml").read_text(encoding="utf-8"))
        assert approve("VOL-II-p3-r1", FIXTURE_REVIEWER, "drill B rehearsal (disposable)", REPO, src / "pack.yaml",
                       REPO / cfg["approvals"] if not Path(cfg["approvals"]).is_absolute() else Path(cfg["approvals"])) == 0
        t0 = time.perf_counter()
        assert ingest(src / "pack.yaml", build, REPO, quiet=True)["exit_code"] == 0
        t["3 re-ingest with the fixture approval"] = time.perf_counter() - t0
    # the curator pins the interpretations of the new rows (and only those: unpinned interpretations); rows whose
    # dependencies ADD-03 changed stay STALE for a person
    from tenderpack.cli import pin_cmd
    assert pin_cmd(build, src / "pack.yaml", refresh=False) == 0
    t0 = time.perf_counter()
    curated = stage2.build(build, root / "out-curated", src / "pack.yaml", REPO, quiet=quiet)
    t["4 outputs with ADD-03 curated"] = time.perf_counter() - t0
    return {"expected": expected, "drafted": drafted, "curated": curated, "timings": t, "src": src, "build": build}


if __name__ == "__main__":
    out = rehearse(Path(sys.argv[1]), fixture_review="--fixture-review" in sys.argv, quiet=False)
    print(json.dumps({k: round(v, 2) for k, v in out["timings"].items()}, indent=1))
