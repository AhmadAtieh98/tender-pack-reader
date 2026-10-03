"""Compare a rebuilt out/ folder with the deliverables in an unpacked draft archive.

Usage: python scripts/compare_outputs.py OUT_DIR ARCHIVE_ROOT
Exit 0 when every archived A1/A2/A3/A5/REVIEW file is byte-identical to its rebuilt counterpart.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

MAP = {"A1_compliance_register": "a1", "A2_addendum_reconciliation": "a2", "A3_disqualification_sheet": "a3",
       "A5_programme": "a5", "REVIEW": "review"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(out: Path, root: Path) -> int:
    diff, n = [], 0
    for arch, sub in MAP.items():
        for f in sorted((root / arch).rglob("*")):
            if not f.is_file():
                continue
            n += 1
            g = out / sub / f.relative_to(root / arch)
            if not g.exists():
                diff.append(f"missing in the rebuild: {sub}/{f.relative_to(root / arch)}")
            elif sha(f) != sha(g):
                diff.append(f"differs: {sub}/{f.relative_to(root / arch)}")
    if diff:
        print("\n".join(diff))
        print(f"{len(diff)} of {n} files differ")
        return 1
    print(f"outputs identical to the archive ({n} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
