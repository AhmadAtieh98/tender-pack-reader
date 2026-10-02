"""Checks on right-to-left text and numerals that look at rendered output, not stored characters.

Why this exists: Unicode stores Arabic in logical (reading) order, and the bidi algorithm
decides what appears on the page. A digit run broken by a hyphen inside Arabic text is
re-ordered: the logical string "٤-٢" is displayed, left to right, as "٢-٤". A transcription
can therefore contain exactly the right characters in the wrong order, and a character-level
comparison would never notice. These checks render the stored text with a bundled Arabic font
(PyMuPDF ships Noto Naskh Arabic, so the result does not depend on system fonts) and read the
glyph order back from the rendering.

Latin expressions inside Arabic text ("45 dB(A)", "NUPA/ISTP/2026/014") are laid out as
left-to-right islands, as a correctly typeset Arabic document shows them. Plain UAX #9 without
directional markup would display "45 dB(A)" in a right-to-left paragraph as "(dB(A 45". The
transcription is never changed: the island is marked only in the text handed to the renderer
(`display_form`, LRE…PDF embedding; MuPDF lays out embeddings correctly but not isolates).

Result of a rendered-order check: "pass" when the whole declared token is found in the rendered
glyph order; "partial" when only its digits/Latin/punctuation could be verified because the
token contains Arabic letters that the renderer's text extraction garbles; "fail" otherwise.

Digit identity (is a glyph ٢ or ٣?) is checked separately and only *advisorily*, by comparing
the shape of each glyph cropped from the source against reference renders of the ten
Arabic-Indic digits (chamfer distance). A low margin between the best and second-best digit
is reported as an uncertainty for the human reviewer; it never overrides a reading.
"""
from __future__ import annotations

import re
import unicodedata

import numpy as np
import pymupdf

PRESENTATION_FORMS = [(0xFB50, 0xFDFF), (0xFE70, 0xFEFF)]
BIDI_CONTROLS = set("‎‏‪‫‬‭‮⁦⁧⁨⁩")
NUMERAL_CHARS = set("0123456789٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹-./,:٫٬")


def storage_problems(text: str) -> list[str]:
    """Arabic must be stored as logical Unicode letters, not as visual presentation-form glyphs."""
    out = []
    pf = [ch for ch in text if any(a <= ord(ch) <= b for a, b in PRESENTATION_FORMS)]
    if pf:
        out.append(f"{len(pf)} presentation-form glyph(s) (e.g. U+{ord(pf[0]):04X}); store logical letters")
    bc = [ch for ch in text if ch in BIDI_CONTROLS]
    if bc:
        out.append(f"{len(bc)} bidi control character(s) present; they change rendering and must be declared")
    return out


LRE, PDF = "\u202a", "\u202c"
_LATIN_EXPR = re.compile(r"\(?[A-Za-z0-9][A-Za-z0-9 .,:;/()%+\-]*")
_ARABIC_LETTER = re.compile("[\u0600-\u065f\u066e-\u06d3\u06d5-\u06ff\u0750-\u077f\ufb50-\ufdff\ufe70-\ufeff]")


def display_form(text: str) -> str:
    """Text as handed to the renderer: each Latin expression (a run of Latin letters, European digits,
    spaces and ASCII punctuation containing at least one Latin letter) is embedded left to right.
    For display only; never stored."""
    def wrap(m):
        expr = m.group(0).rstrip(" .,:;")
        if not re.search(r"[A-Za-z]", expr):
            return m.group(0)
        return LRE + expr + PDF + m.group(0)[len(expr):]
    return _LATIN_EXPR.sub(wrap, text)


def render_rtl(text: str, width: float = 1400, size: float = 22) -> tuple[pymupdf.Document, pymupdf.Page]:
    doc = pymupdf.open()
    page = doc.new_page(width=width, height=size * 3.5)
    safe = display_form(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    page.insert_htmlbox(pymupdf.Rect(6, 6, width - 6, size * 3.4),
                        f'<p dir="rtl" style="font-size:{size}px; margin:0">{safe}</p>')
    return doc, page


def visual_order(text: str) -> str:
    """Glyph order, left to right, of `text` rendered as an RTL paragraph."""
    _, page = render_rtl(text)
    chars = []
    for block in page.get_text("rawdict")["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                for ch in span["chars"]:
                    chars.append((ch["bbox"][0], ch["c"]))
    chars.sort()
    vis = "".join(c for _, c in chars if c not in BIDI_CONTROLS)
    return re.sub(r"\s+", " ", vis).strip()


def visual_numeral_runs(text: str) -> list[str]:
    """Runs of digits and separators as they appear left to right when `text` is rendered RTL."""
    vis = visual_order(text)
    runs, cur = [], ""
    for ch in vis:
        if ch in NUMERAL_CHARS and (ch.isdigit() or cur):
            cur += ch
        else:
            if any(c.isdigit() for c in cur):
                runs.append(cur.strip("-./,:٫٬"))
            cur = ""
    if any(c.isdigit() for c in cur):
        runs.append(cur.strip("-./,:٫٬"))
    return runs


# ------------------------------------------------------------- digit glyph advisory

def _gray(pix: pymupdf.Pixmap) -> np.ndarray:
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    return a[..., :3].mean(axis=2) if pix.n >= 3 else a[..., 0].astype(float)


def _points(ink: np.ndarray, n: int = 400) -> np.ndarray:
    r = np.where(ink.any(axis=1))[0]
    c = np.where(ink.any(axis=0))[0]
    g = ink[r.min():r.max() + 1, c.min():c.max() + 1]
    y, x = np.nonzero(g)
    pts = np.stack([x / g.shape[0], y / g.shape[0]], 1)
    if len(pts) > n:
        pts = pts[np.linspace(0, len(pts) - 1, n).astype(int)]
    return pts


def _chamfer(a: np.ndarray, b: np.ndarray) -> float:
    d = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(-1))
    return float((d.min(1).mean() + d.min(0).mean()) / 2)


_REFS: dict[str, np.ndarray] = {}


def _references() -> dict[str, np.ndarray]:
    if not _REFS:
        for d in "٠١٢٣٤٥٦٧٨٩":
            doc = pymupdf.open()
            pg = doc.new_page(width=80, height=80)
            pg.insert_htmlbox(pymupdf.Rect(5, 5, 75, 75), f'<p style="font-size:36px">{d}</p>')
            _REFS[d] = _points(_gray(pg.get_pixmap(dpi=400)) < 128)
    return _REFS


def glyph_segments(gray: np.ndarray, thr: int = 130) -> list[tuple[int, int]]:
    ink = gray < thr
    cols = ink.any(axis=0)
    segs, x = [], 0
    while x < len(cols):
        if cols[x]:
            s = x
            while x < len(cols) and cols[x]:
                x += 1
            segs.append((s, x))
        else:
            x += 1
    return segs


def digit_advisory(page: pymupdf.Page, bbox_pt: list[float], dpi: int = 800) -> dict:
    """Classify each glyph in a numeral crop; returns visual LTR guess with margins."""
    pix = page.get_pixmap(clip=pymupdf.Rect(bbox_pt), dpi=dpi)
    gray = _gray(pix)
    refs = _references()
    glyphs = []
    for s, e in glyph_segments(gray):
        ink = gray[:, s:e] < 130
        rows = np.where(ink.any(axis=1))[0]
        h, w = rows.max() - rows.min() + 1, e - s
        if h < 0.45 * w or h < 6:                       # flat stroke: a hyphen or similar
            glyphs.append({"glyph": "-", "kind": "separator", "px": [int(s), int(e)]})
            continue
        if w < 2:
            continue
        pts = _points(ink)
        scores = sorted((_chamfer(pts, r), d) for d, r in refs.items())
        best, second = scores[0], scores[1]
        margin = (second[0] - best[0]) / max(second[0], 1e-9)
        glyphs.append({"glyph": best[1], "kind": "digit", "px": [int(s), int(e)],
                       "best": [best[1], round(best[0], 4)], "second": [second[1], round(second[0], 4)],
                       "margin": round(margin, 3), "low_confidence": margin < 0.25})
    return {"visual_ltr_guess": "".join(g["glyph"] for g in glyphs), "glyphs": glyphs,
            "method": "chamfer distance to Noto Naskh Arabic digit renders; advisory only"}


def digits_of(s: str) -> list[int]:
    return [unicodedata.digit(c) for c in s if unicodedata.category(c) == "Nd"]


def _reliable(t: str) -> str:
    """The characters whose rendered order can be read back reliably: everything but Arabic letters."""
    return re.sub(r"\s+", " ", _ARABIC_LETTER.sub(" ", t)).strip()


def visual_check(source: str, expected_visual: str) -> tuple[str, str]:
    """Does rendering `source` right to left put the glyphs of a token in the order seen in the crop?

    Returns ("pass" | "partial" | "fail", detail). The whole token is compared first (after NFKC,
    which folds Arabic presentation forms back to letters). If that fails and the token contains
    Arabic letters, whose extraction can be garbled, only the digits, Latin letters and punctuation
    are compared, in order: a match there is PARTIAL (the Arabic letters' order is not verified).
    A token with no Arabic letters must match in full.
    """
    vis = unicodedata.normalize("NFKC", visual_order(source))
    exp = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", expected_visual)).strip()
    if exp in vis:
        return "pass", f"'{exp}' found in rendered glyph order '{vis}'"
    exp_r, vis_r = _reliable(exp), _reliable(vis)
    if _ARABIC_LETTER.search(exp) and exp_r and any(c.isdigit() for c in exp_r) and exp_r in vis_r:
        return "partial", (f"PARTIAL: only digits/Latin/punctuation verified ('{exp_r}' in '{vis_r}'); "
                           "the order of the Arabic letters could not be read back")
    return "fail", f"rendered glyph order '{vis}'; expected '{exp}'"
