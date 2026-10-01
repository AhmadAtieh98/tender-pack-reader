"""Text-layer extraction with explicit, audited exclusion of page furniture.

Every non-blank text span on every page ends up in exactly one of two places:
  * content spans (later assigned to units by segment.py), or
  * exclusions, each carrying the id of the furniture rule that matched it.

Rotated text is NOT discarded as a class. A rotated span is excluded only if it matches
a declared rule in full (e.g. the WATERMARK rule: exact text, colour, size range and
angle range). Any other rotated span is content and keeps its angle.
"""
from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pymupdf

from .util import bbox_r, hex_color, load_yaml, r1


@dataclass
class Span:
    span_id: str
    doc: str
    page: int
    text: str
    font: str
    size: float
    color: str
    bold: bool
    superscript: bool
    bbox: list[float]
    origin: list[float]
    angle: float
    invisible: bool = False
    char_bboxes: list[list[float]] = field(default_factory=list)  # only kept for rotated spans

    @property
    def x0(self): return self.bbox[0]

    @property
    def y0(self): return self.bbox[1]

    @property
    def x1(self): return self.bbox[2]

    @property
    def y1(self): return self.bbox[3]

    @property
    def cy(self): return (self.bbox[1] + self.bbox[3]) / 2

    @property
    def cx(self): return (self.bbox[0] + self.bbox[2]) / 2

    def to_dict(self) -> dict:
        d = asdict(self)
        if not self.char_bboxes:
            d.pop("char_bboxes")
        return d


@dataclass
class Exclusion:
    span_id: str
    doc: str
    page: int
    rule: str
    reason: str
    text: str
    bbox: list[float]
    angle: float
    color: str
    size: float
    font: str


@dataclass
class PageText:
    doc: str
    page: int
    width: float
    height: float
    printed_page: str | None
    content: list[Span]
    exclusions: list[Exclusion]
    blank_spans: int
    invisible_spans: int


class FurnitureRules:
    def __init__(self, cfg: dict):
        self.rules = cfg["rules"]
        for r in self.rules:
            if "pattern" in r:
                r["_re"] = re.compile(r["pattern"])

    @classmethod
    def from_file(cls, path: Path) -> "FurnitureRules":
        return cls(load_yaml(path))

    def match(self, span: Span) -> tuple[dict, re.Match | None] | None:
        for r in self.rules:
            m = None
            if "text" in r and span.text.strip() != r["text"]:
                continue
            if "_re" in r:
                m = r["_re"].match(span.text.strip())
                if not m:
                    continue
            if "color" in r and span.color.lower() != r["color"].lower():
                continue
            if "size" in r and not (r["size"][0] <= span.size <= r["size"][1]):
                continue
            if "angle" in r and not (r["angle"][0] <= span.angle <= r["angle"][1]):
                continue
            if "angle" not in r and abs(span.angle) > 0.5:
                continue  # rules without an angle only apply to horizontal text
            if "max_y1" in r and span.y1 > r["max_y1"]:
                continue
            if "min_y0" in r and span.y0 < r["min_y0"]:
                continue
            return r, m
        return None


def _line_angle(direction) -> float:
    a = math.degrees(math.atan2(-direction[1], direction[0]))
    a = round(a, 1)
    return 0.0 if a == 0 else a  # normalise -0.0


def _invisible_boxes(page: pymupdf.Page) -> list[pymupdf.Rect]:
    boxes = []
    for tr in page.get_texttrace():
        if tr.get("type") == 3 or tr.get("opacity", 1) == 0:
            boxes.append(pymupdf.Rect(tr["bbox"]))
    return boxes


def extract_page(doc_id: str, page: pymupdf.Page, rules: FurnitureRules) -> PageText:
    pno = page.number + 1
    invisible = _invisible_boxes(page)
    raw = page.get_text("rawdict", flags=pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_PRESERVE_LIGATURES)
    content: list[Span] = []
    exclusions: list[Exclusion] = []
    blank = 0
    n_invisible = 0
    printed_page = None
    idx = 0
    for block in raw["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            angle = _line_angle(line["dir"])
            for s in line["spans"]:
                text = "".join(ch["c"] for ch in s["chars"])
                idx += 1
                sid = f"{doc_id}/p{pno}/s{idx:03d}"
                if not text.strip():
                    blank += 1
                    continue
                rect = pymupdf.Rect(s["bbox"])
                is_invisible = any(
                    (rect & b).get_area() > 0.5 * max(rect.get_area(), 1e-6) for b in invisible
                )
                n_invisible += int(is_invisible)
                span = Span(
                    span_id=sid,
                    doc=doc_id,
                    page=pno,
                    text=text,
                    font=s["font"],
                    size=r1(s["size"]),
                    color=hex_color(s["color"]),
                    bold=bool(s["flags"] & 16) or "Bold" in s["font"],
                    superscript=bool(s["flags"] & 1),
                    bbox=bbox_r(s["bbox"]),
                    origin=[r1(s["origin"][0]), r1(s["origin"][1])],
                    angle=angle,
                    invisible=is_invisible,
                    char_bboxes=[bbox_r(ch["bbox"]) for ch in s["chars"]] if angle != 0 else [],
                )
                hit = rules.match(span)
                if hit:
                    rule, m = hit
                    if m is not None and "printed_page" in (m.groupdict() or {}):
                        printed_page = m.group("printed_page")
                    exclusions.append(
                        Exclusion(sid, doc_id, pno, rule["id"], rule["reason"], text, span.bbox,
                                  angle, span.color, span.size, span.font)
                    )
                else:
                    content.append(span)
    return PageText(doc_id, pno, r1(page.rect.width), r1(page.rect.height), printed_page,
                    content, exclusions, blank, n_invisible)


def check_expected_counts(pages: list[PageText], rules: FurnitureRules) -> list[str]:
    """Rules that declare expect_per_page must match exactly that many spans on every page."""
    problems = []
    for r in rules.rules:
        n = r.get("expect_per_page")
        if n is None:
            continue
        for p in pages:
            got = sum(1 for e in p.exclusions if e.rule == r["id"])
            if got != n:
                problems.append(f"{p.doc} p{p.page}: rule {r['id']} matched {got} spans, expected {n}")
    return problems
