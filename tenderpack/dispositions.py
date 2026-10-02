"""Unit dispositions (Stage 3) and the obligation / consequence sweeps (C14, C15).

Every unit of every volume gets a disposition, so nothing in the pack is silently ignored:

  requirement   the unit states (part of) an independently testable obligation; `rows` lists the A1 rows
                built on it, and each of those rows lists the unit in its `units`
  consequence   the unit states what follows from failing other requirements; `rows` lists the rows whose
                interpretation quotes their consequence from this unit
  duplicate     the unit repeats an obligation held by another row (e.g. a form note restating VOL-I 9.4);
                `rows` lists those rows; `reason` says what it repeats
  definition | authority | informational | context
                no bidder obligation: a definition, a duty or right of the Authority, information, or
                context (e.g. non-binding minutes); `reason` is required
  structural    headings, table and form containers, image regions: assigned automatically by kind

Addendum units are accounted for by the amendment op files (C20 provision coverage), not here.

Sweeps (sentence level, English and Arabic):
  C14 obligation language (shall, must, required, ...): every hit lies in a unit with a disposition, and
      hits in units dispositioned as definition / authority / informational / context are listed for a
      person to confirm (reported, not structural)
  C15 consequence language (reject, disqualif, non-responsive, disregard, returned unopened, استبعاد,
      غير مستجيب, ...): every hit is linked to a row whose consequence is quoted from that unit, or to a
      disposition whose `consequence_note` explains it (an unlinked consequence is an omission: a
      check-register finding and a release blocker)
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .util import load_yaml

KINDS = ("requirement", "consequence", "duplicate", "definition", "authority", "informational", "context", "structural")
AUTO_STRUCTURAL = {"heading", "table", "region", "image_text"}
NEEDS_ROWS = ("requirement", "consequence", "duplicate")


class UnitDisposition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    disposition: Literal["requirement", "consequence", "duplicate", "definition", "authority", "informational",
                         "context", "structural"]
    rows: list[str] = Field(default_factory=list)
    reason: str | None = None
    consequence_note: str | None = None          # C15: why a consequence word here needs no row of its own


class DispositionFile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    doc: str
    prepared_by: str
    units: dict[str, UnitDisposition]


def load_dispositions(directory: Path) -> tuple[dict[str, UnitDisposition], list[str]]:
    """All disposition files in a directory -> {unit id: disposition}; problems for duplicates."""
    out: dict[str, UnitDisposition] = {}
    problems = []
    if not Path(directory).is_dir():
        return out, problems
    for f in sorted(Path(directory).glob("*.yaml")):
        df = DispositionFile.model_validate(load_yaml(f))
        for uid, d in df.units.items():
            if uid in out:
                problems.append(f"{uid} has a disposition in more than one file ({f.name})")
            out[uid] = d
    return out, problems


def effective_disposition(unit: dict, explicit: dict[str, UnitDisposition]) -> UnitDisposition | None:
    if unit["unit_id"] in explicit:
        return explicit[unit["unit_id"]]
    if unit["kind"] in AUTO_STRUCTURAL:
        return UnitDisposition(disposition="structural", reason=f"{unit['kind']} (assigned by kind)")
    return None


def check_dispositions(units: list[dict], explicit: dict[str, UnitDisposition], rows: list) -> list[str]:
    """Every volume unit has a disposition; links between dispositions and rows hold in both directions."""
    problems = []
    by_id = {u["unit_id"]: u for u in units}
    row_by_id = {r.id: r for r in rows}
    for uid in explicit:
        if uid not in by_id:
            problems.append(f"disposition for a unit that does not exist: {uid}")
    for u in units:
        if u["doc"].startswith("ADD-"):
            continue
        d = effective_disposition(u, explicit)
        if d is None:
            problems.append(f"{u['unit_id']}: no disposition")
            continue
        if d.disposition in NEEDS_ROWS:
            if not d.rows:
                problems.append(f"{u['unit_id']}: {d.disposition} needs rows")
            for rid in d.rows:
                r = row_by_id.get(rid)
                if r is None:
                    problems.append(f"{u['unit_id']}: row {rid} does not exist")
                elif d.disposition == "requirement" and u["unit_id"] not in r.units:
                    problems.append(f"{u['unit_id']}: row {rid} does not list this unit in its units")
                elif d.disposition == "consequence" and not any(
                        getattr(it.consequence, "unit", None) == u["unit_id"] for it in r.interpretations):
                    problems.append(f"{u['unit_id']}: row {rid} does not quote its consequence from this unit")
        elif d.disposition != "structural" and not (d.reason or "").strip():
            problems.append(f"{u['unit_id']}: {d.disposition} needs a reason")
    for r in rows:
        for uid in r.units:
            u = by_id.get(uid)
            if u is None or u["doc"].startswith("ADD-"):
                continue
            d = effective_disposition(u, explicit)
            if d is None or d.disposition not in ("requirement", "duplicate") or r.id not in d.rows:
                problems.append(f"row {r.id} uses {uid}, whose disposition does not list it as a requirement")
    return problems


# ---------------------------------------------------------------------------------------------- sweeps

OBLIGATION = re.compile(r"\b(shall|must|is required|are required|required to|mandatory|failure to|no later than|"
                        r"not later than|at least|not less than|undertakes?|is to be|are to be)\b", re.I)
CONSEQUENCE_EN = re.compile(r"\b(reject\w*|disqualif\w*|non-responsive|disregard\w*|returned unopened|"
                            r"not (?:be )?(?:evaluated|considered|answered|entertained|accepted|proceed)|"
                            r"removed before evaluation|own risk|forfeit\w*|exclu(?:de|ded|sion)|"
                            r"terminat\w*|liquidated damages|deduct\w*|call(?:ed)? (?:on|upon) the|"
                            r"invalid|void)\b", re.I)
CONSEQUENCE_AR = re.compile("(استبعاد|مستبعد|غير مستجيب|رفض|يرفض|ترفض|إلغاء|يلغى|حرمان)")


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.;:!?؛。])\s+", text or "")
    return [p for p in parts if p.strip()]


def sweep(units: list[dict]) -> dict[str, list[dict]]:
    """{'obligation': [...], 'consequence': [...]} hits: {unit, sentence, word, lang}."""
    out = {"obligation": [], "consequence": []}
    for u in units:
        if u["doc"].startswith("ADD-") or u["kind"] in AUTO_STRUCTURAL:
            continue
        for s in sentences(u.get("text", "")):
            m = OBLIGATION.search(s)
            if m:
                out["obligation"].append({"unit": u["unit_id"], "sentence": s[:200], "word": m.group(0), "lang": "en"})
            for rx, lang in ((CONSEQUENCE_EN, "en"), (CONSEQUENCE_AR, "ar")):
                m = rx.search(s)
                if m:
                    out["consequence"].append({"unit": u["unit_id"], "sentence": s[:200], "word": m.group(0), "lang": lang})
    return out


def check_sweeps(units: list[dict], explicit: dict[str, UnitDisposition], rows: list) -> tuple[list[dict], list[dict]]:
    """Returns (C14 hits for a person to confirm, C15 unlinked consequence hits)."""
    hits = sweep(units)
    by_id = {u["unit_id"]: u for u in units}
    cons_units = {}
    for r in rows:
        for it in r.interpretations:
            cu = getattr(it.consequence, "unit", None)
            if cu:
                cons_units.setdefault(cu, set()).add(r.id)
    c14 = []
    for h in hits["obligation"]:
        d = effective_disposition(by_id[h["unit"]], explicit)
        if d is None or d.disposition in ("definition", "authority", "informational", "context"):
            c14.append({**h, "disposition": d.disposition if d else None, "reason": d.reason if d else None})
    c15 = []
    for h in hits["consequence"]:
        d = effective_disposition(by_id[h["unit"]], explicit)
        if h["unit"] in cons_units or (d is not None and (d.consequence_note or "").strip()):
            continue
        c15.append({**h, "disposition": d.disposition if d else None})
    return c14, c15
