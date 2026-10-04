"""Blind rehearsal 02: set up the pack as a live session would, with the received Addendum No. 3 added.

The six received documents (unchanged, from sources/candidate_pack) plus input/ADD-03_Addendum_No_3.pdf (an unseen-style
addendum by an independent author; key sealed, FROZEN.md). The owner's reading approvals (curation/approvals.yaml) are
used read-only, as a live session would; nothing is approved or decided here. The rest of the curation is COPIED into work/ (op files for ADD-01/ADD-02, register, evidence items, A5 templates, assumptions),
so everything the rehearsal curates stays inside this folder; curation/ and config/ are not touched.
Usage: python rehearsals/blind-01/setup_pack.py      (refuses to overwrite an existing work/)
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pymupdf
import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
from tenderpack.util import sha256_file  # noqa: E402

work = HERE / "work"
if work.exists():
    sys.exit(f"refused: {work} exists")
work.mkdir()
rel = lambda p: Path(p).resolve().relative_to(REPO).as_posix()  # noqa: E731
cfg = yaml.safe_load((REPO / "config/pack.yaml").read_text(encoding="utf-8"))
cfg["documents"].append({"doc_id": "ADD-03", "kind": "addendum", "number": 3, "path": rel(HERE / "input/ADD-03_Addendum_No_3.pdf")})
files = []
for d in cfg["documents"]:
    p = REPO / d["path"]
    doc = pymupdf.open(p)
    files.append({"path": d["path"], "bytes": p.stat().st_size, "sha256": sha256_file(p), "pages": len(doc),
                  "producer": doc.metadata.get("producer"), "creation_date": doc.metadata.get("creationDate")})
(work / "manifest.json").write_text(json.dumps({"files": files}, indent=1), encoding="utf-8")
(work / "amendments").mkdir()
for a in ("ADD-01", "ADD-02"):
    shutil.copy(REPO / f"curation/amendments/{a}.yaml", work / "amendments" / f"{a}.yaml")
shutil.copytree(REPO / "curation/register", work / "register")
shutil.copytree(REPO / "curation/evidence_items", work / "evidence_items")
shutil.copy(REPO / "curation/activity_templates.yaml", work / "activity_templates.yaml")
shutil.copy(REPO / "config/assumptions.yaml", work / "assumptions.yaml")
shutil.copy(REPO / "config/scenarios.yaml", work / "scenarios.yaml")
shutil.copytree(REPO / "curation/clarifications", work / "clarifications")
cfg.update({"pack_id": "NUPA-ISTP-2026-014-BLIND-02", "manifest": rel(work / "manifest.json"),
            # the owner's real reading approvals are used read-only, as in a live session (nothing is approved here)
            "approvals": "curation/approvals.yaml", "decisions": rel(work / "decisions.yaml"),
            "clarifications": rel(work / "clarifications/register.yaml"),
            "amendments_dir": rel(work / "amendments"), "register": rel(work / "register/rows.yaml"),
            "issues": rel(work / "register/issues.yaml"), "dispositions_dir": rel(work / "register/dispositions"),
            "row_ids": rel(work / "register/ids.yaml"), "evidence_items_dir": rel(work / "evidence_items"),
            "activity_templates": rel(work / "activity_templates.yaml"), "assumptions": rel(work / "assumptions.yaml"),
            "scenarios": rel(work / "scenarios.yaml")})
(work / "pack.yaml").write_text("# Blind rehearsal 02 pack: the received pack plus the blind Addendum No. 3 (not tender content).\n"
                                + yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False), encoding="utf-8")
print(f"pack: {rel(work / 'pack.yaml')}")
