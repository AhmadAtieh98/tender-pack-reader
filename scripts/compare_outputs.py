"""Compare a rebuilt out/ folder with the deliverables in an unpacked draft archive.

Usage: python scripts/compare_outputs.py OUT_DIR ARCHIVE_ROOT

Every archived A1/A2/A3/A5/REVIEW file and the A4 clarification register is compared with its rebuilt counterpart.
Two kinds of identity are kept apart (session 08):
  content    text deliverables (.csv .json .md .html .yaml .txt .svg): byte-identical, or the content differs
  rendering  binary renderings (.pdf .png .xlsx): byte-identical; if not, their CONTENT is compared instead (the text
             of every PDF page and its link targets; the size of a PNG; every cell value of every sheet). A file whose
             bytes differ but whose content is the same is a platform-dependent rendering difference (fonts, image
             encoding, zip compression), reported but not a failure.
Exit 0 when no content differs (byte-identical, or only rendering differences); 1 otherwise.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

MAP = {"A1_compliance_register": "a1", "A2_addendum_reconciliation": "a2", "A3_disqualification_sheet": "a3",
       "A5_programme": "a5", "REVIEW": "review", "A4_work_log/clarification_register": "a4"}
RENDERED = (".pdf", ".png", ".xlsx")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def content_of(p: Path):
    """What a rendering says, independent of how it is encoded."""
    if p.suffix == ".pdf":
        import pymupdf
        doc = pymupdf.open(p)
        return [(page.get_text("text"), sorted(str(ln.get("uri") or ln.get("file") or "") for ln in page.get_links()))
                for page in doc]
    if p.suffix == ".png":
        import pymupdf
        pix = pymupdf.Pixmap(str(p))
        return (pix.width, pix.height)
    if p.suffix == ".xlsx":
        import openpyxl
        wb = openpyxl.load_workbook(p, read_only=True)
        return {ws.title: [list(r) for r in ws.iter_rows(values_only=True)] for ws in wb}
    return p.read_bytes()


def main(out: Path, root: Path) -> int:
    content, rendering, n, same = [], [], 0, 0
    for arch, sub in MAP.items():
        base = root / arch
        for f in sorted(base.rglob("*")) if base.is_dir() else []:
            if not f.is_file():
                continue
            n += 1
            rel = f"{sub}/{f.relative_to(base)}"
            g = out / sub / f.relative_to(base)
            if not g.exists():
                content.append(f"missing in the rebuild: {rel}")
            elif sha(f) == sha(g):
                same += 1
            elif f.suffix in RENDERED and content_of(f) == content_of(g):
                rendering.append(f"rendering only (bytes differ, content identical): {rel}")
            else:
                content.append(f"CONTENT differs: {rel}")
    for line in content + rendering:
        print(line)
    if content:
        print(f"{len(content)} of {n} files differ in content; {len(rendering)} differ in rendering only; {same} byte-identical")
        return 1
    print(f"outputs identical to the archive in content ({n} files: {same} byte-identical, "
          f"{len(rendering)} rendering-only differences)")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
