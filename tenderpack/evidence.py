"""Evidence items: what a requirement needs submitted or done (the A1 'Evidence needed' column, A5 input).

Vocabulary files: curation/evidence_items/*.yaml, each {items: {EV-ID: {name, envelope, issuer, per, ...}}}.
An id defined in two files is an error. Every evidence id a row uses must be in the vocabulary, and every
item a row in force needs must have A5 activities or a justified exception (schedule.py, C44).
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from .util import load_yaml


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    envelope: Literal["A", "B", "A+B", "none"]          # where it is submitted ('none': an action, not a document)
    issuer: str
    per: Literal["proposal", "member", "signatory", "reference", "lead_member", "epc_contractor", "om_operator"] = "proposal"
    source: str                                        # unit(s) that require it, e.g. "VOL-I:9.1(g); VOL-I:6.3"
    counted: bool = True                               # counted in the copies of VOL-I 6.5 (1 original + 3 copies + USB)
    note: str | None = None


def load_evidence_items(directory: Path) -> tuple[dict[str, EvidenceItem], list[str]]:
    items: dict[str, EvidenceItem] = {}
    problems = []
    for f in sorted(Path(directory).glob("*.yaml")):
        for k, v in ((load_yaml(f) or {}).get("items") or {}).items():
            if k in items:
                problems.append(f"evidence item {k} defined twice (again in {f.name})")
            items[k] = EvidenceItem.model_validate(v)
    return items, problems
