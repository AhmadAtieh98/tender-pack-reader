"""Prepared proposals for register rows (session 06), e.g. re-made interpretations for STALE rows.

A proposal is prepared by the assistant and applied only when a person runs
    tenderpack apply-proposal PROPOSAL_ID --by NAME
which inserts the interpretation into the row's YAML (comments and layout kept), pins that interpretation alone,
and leaves the row PROPOSED: it still needs `tenderpack accept`. A proposal may also carry `replace_requirement:
{old, new}` (a corrected requirement summary, applied only if the row still has the old one). A proposal marked
`status: superseded` keeps its text and the reason (`superseded_by`, `superseded_because`) and cannot be applied. Applying changes the row's content, so any
earlier decision on it no longer counts.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import yaml

from .readings import valid_reviewer
from .util import load_yaml


def load_proposals(directory: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for f in sorted(Path(directory).glob("*.yaml")) if Path(directory).is_dir() else []:
        for p in (load_yaml(f) or {}).get("proposals") or []:
            out[p["id"]] = {**p, "_file": f}
    return out


def is_applied(p: dict, rows: dict) -> bool:
    row = rows.get(p["row"])
    ai = p.get("add_interpretation") or {}
    note = (ai.get("note") or "").strip()
    return bool(row) and any(it.stage == ai.get("stage") and it.quote == ai.get("quote") and (it.note or "").startswith(note)
                             for it in row.interpretations)


def _row_file(root: Path, rows_path: Path, row_id: str) -> Path | None:
    for f in [rows_path, *sorted((rows_path.parent / "rows").glob("*.yaml"))]:
        if f"- id: {row_id}\n" in f.read_text(encoding="utf-8"):
            return f
    return None


def insert_interpretation(path: Path, row_id: str, interp: dict) -> None:
    """Append an interpretation to a row's `interpretations:` list, keeping the file's comments and layout."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    start = next(i for i, l in enumerate(lines) if l.rstrip("\n") == f"  - id: {row_id}")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("  - id: ") or lines[i].startswith("  # ")),
               len(lines))
    ii = next(i for i in range(start, end) if lines[i].rstrip("\n") == "    interpretations:")
    j = ii + 1
    while j < end and (lines[j].startswith("      ") or not lines[j].strip()):
        j += 1
    block = yaml.safe_dump([interp], allow_unicode=True, sort_keys=False, width=110)
    new = ["      " + l + "\n" for l in block.rstrip("\n").split("\n")]
    path.write_text("".join(lines[:j] + new + lines[j:]), encoding="utf-8")


def apply_proposal(pid: str, by: str, evidence: Path, pack_path: Path, directory: Path, root: Path) -> int:
    from .cli import pin_cmd
    from .register import load_rows
    if not valid_reviewer(by):
        print(f"refused: --by must name the person applying the proposal ({by!r}). Nothing written.")
        return 2
    props = load_proposals(directory)
    if pid not in props:
        print(f"refused: no proposal {pid} in {directory}")
        return 1
    p = props[pid]
    cfg = load_yaml(pack_path)
    rows_path = root / cfg.get("register", "curation/register/rows.yaml")
    rows = {r.id: r for r in load_rows(rows_path).rows}
    if is_applied(p, rows):
        print(f"{pid} is already applied to {p['row']}")
        return 0
    f = _row_file(root, rows_path, p["row"])
    if f is None:
        print(f"refused: row {p['row']} not found")
        return 1
    if p.get("status") == "superseded":
        print(f"refused: {pid} is superseded ({p.get('superseded_by')}). Nothing written.")
        return 1
    interp = dict(p["add_interpretation"])
    interp["note"] = (interp.get("note") or "").strip() + f" [Applied from proposal {pid} by {by.strip()} on {dt.date.today().isoformat()}.]"
    rr = p.get("replace_requirement")
    if rr:                                                   # a corrected requirement summary, written with the interpretation
        text = f.read_text(encoding="utf-8")
        old_line = f'    requirement: "{rr["old"]}"\n'
        if text.count(old_line) != 1:
            print(f"refused: the requirement of {p['row']} is not the one the proposal corrects ({rr['old'][:60]}...). Nothing written.")
            return 1
        f.write_text(text.replace(old_line, f'    requirement: "{rr["new"]}"\n'), encoding="utf-8")
    insert_interpretation(f, p["row"], interp)
    load_rows(rows_path)                                      # the register must still load
    print(f"wrote the {interp['stage']} interpretation of {p['row']} into {f}")
    code = pin_cmd(evidence, pack_path, refresh=False, only=f"{p['row']}@{interp['stage']}")
    print(f"next: the row is PROPOSED; its owner decides: python -m tenderpack accept {p['row']} --reviewer \"Your Name\"  "
          "(or reject with --note)")
    return code
