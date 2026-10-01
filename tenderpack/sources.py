"""Source integrity (check C01): every source file must match the recorded hash and page count."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pymupdf

from .util import ROOT, sha256_file
import json


class SourceIntegrityError(Exception):
    pass


@dataclass(frozen=True)
class Document:
    doc_id: str
    kind: str
    path: Path
    number: int | None
    sha256: str
    pages: int


def load_documents(pack_cfg: dict, root: Path = ROOT, verify: bool = True) -> list[Document]:
    manifest_path = root / pack_cfg["manifest"]
    manifest = {f["path"]: f for f in json.loads(manifest_path.read_text(encoding="utf-8"))["files"]}
    docs: list[Document] = []
    problems: list[str] = []
    for d in pack_cfg["documents"]:
        path = root / d["path"]
        entry = manifest.get(d["path"])
        if entry is None:
            problems.append(f"{d['doc_id']}: {d['path']} is not in {pack_cfg['manifest']}")
            continue
        actual = sha256_file(path)
        pages = pymupdf.open(path).page_count
        if verify and actual != entry["sha256"]:
            problems.append(f"{d['doc_id']}: sha256 {actual} != manifest {entry['sha256']}")
        if verify and pages != entry.get("pages"):
            problems.append(f"{d['doc_id']}: {pages} pages != manifest {entry.get('pages')}")
        docs.append(Document(d["doc_id"], d["kind"], path, d.get("number"), actual, pages))
    if problems:
        raise SourceIntegrityError("C01 source integrity failed:\n  " + "\n  ".join(problems))
    return docs
