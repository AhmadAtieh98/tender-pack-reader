"""Guards shared by the tests: what may exist in the repository's own review records.

Until session 08 no approval existed. On 3 Oct 2026 the owner confirmed the two image readings in writing
(worklog/2026-10-03_session-08_prompt.md §2) and they were recorded with `tenderpack approve`. The repository may hold
exactly those two approvals, by "Ahmad", dated 2026-10-03, each pinned to the reviewed subject; no review decision on
a row or an op exists (curation/reviews/decisions.yaml is never created by the program or the tests).
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OWNER_APPROVALS = {"VOL-II-p3-r1": "6bc6505956429dc7fef21c829905f5e0177568e81a74481593d324460101f012",
                   "VOL-IV-p6-r1": "f433c2ca4e56267920ad7819090469185ae2b28ac9dc5d52ee04390fec934247"}


def only_owner_approvals() -> bool:
    assert not (ROOT / "curation/reviews/decisions.yaml").exists()
    path = ROOT / "curation/approvals.yaml"
    entries = yaml.safe_load(path.read_text(encoding="utf-8"))["approvals"] if path.exists() else []
    assert {e["region_id"]: e["subject_sha256"] for e in entries} == OWNER_APPROVALS and len(entries) == 2, entries
    for e in entries:
        assert e["reviewer"] == "Ahmad" and e["date"] == "2026-10-03"
        assert "worklog/2026-10-03_session-08_prompt.md" in e["confirmation_record"]
        assert e["does_not_cover"]
    return True


def pack_without_session08_interpretations(tmp: Path, extra: dict | None = None) -> Path:
    """A disposable pack whose register is the real one minus the three interpretations applied on 3 Oct 2026 from the
    owner-directed proposals (P-S08-VOL-I-8.3-01, -3.4-01, -6.7-01): those rows are then STALE at ADD-01 and ADD-02, as
    they were before session 08. Used to keep testing how a STALE row behaves; the repository is untouched."""
    import shutil
    reg = tmp / "register"
    shutil.copytree(ROOT / "curation/register", reg)
    for f in [reg / "rows.yaml", *sorted((reg / "rows").glob("*.yaml"))]:
        lines = f.read_text(encoding="utf-8").split("\n")
        out, i = [], 0
        while i < len(lines):
            if lines[i].startswith("      - stage: "):
                j = i + 1
                while j < len(lines) and lines[j].startswith("        "):
                    j += 1
                if "[Applied from proposal P-S08-" in " ".join(x.strip() for x in lines[i:j]):
                    i = j
                    continue
            out.append(lines[i])
            i += 1
        text = "\n".join(out)
        for prop in (yaml.safe_load((reg / "proposals/2026-10-03_session-08_owner-directed.yaml").read_text(encoding="utf-8"))
                     ["proposals"]):
            rr = prop.get("replace_requirement")
            if rr:                                             # the requirement summary as it was before the proposal
                text = text.replace(f'    requirement: "{rr["new"]}"\n', f'    requirement: "{rr["old"]}"\n')
        f.write_text(text, encoding="utf-8")
    cfg = yaml.safe_load((ROOT / "config/pack.yaml").read_text(encoding="utf-8"))
    cfg.update({"register": str(reg / "rows.yaml"), "issues": str(reg / "issues.yaml"),
                "dispositions_dir": str(reg / "dispositions"), "row_ids": str(reg / "ids.yaml")}, **(extra or {}))
    p = tmp / "pack.yaml"
    p.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    return p
