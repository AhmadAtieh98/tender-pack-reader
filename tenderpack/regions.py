"""Non-text-layer content: detection, evidence crops and raster structure.

A page can carry content that the text layer does not: embedded raster images, vector
drawings that are not table rules, invisible text over a scan, or ink produced by
something we did not model at all. "The page has text" is not evidence that the page
was read, so every such region becomes a Region that needs a reading.

Detection methods (all deterministic):
  image            every embedded raster image (get_image_info), any size
  vector_graphic   drawing paths that are not structure. Structure is only: axis-aligned straight rules;
                   rectangles that are stroked only, lightly filled, or thinner than 2.5 pt (a rule
                   drawn as a filled bar); and dark-filled rectangles with
                   text printed on them (e.g. a table header band). Diagonal or free-form straight
                   lines (a triangle, an arrow), curves, and dark fills with no text on them (which
                   could hide content, e.g. a redaction box) are uncertain drawings and stay visible
                   as regions for a person to review.
  invisible_text   text with render mode 3 / opacity 0 (e.g. an OCR layer); never trusted as content
  unexplained_ink  dark pixels in a page render that no text span, image or drawing accounts for

Evidence for each region: the native image bytes as embedded (if any), a rendered crop of
the region at a fixed dpi, and a page context image with the region outlined; all hashed.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import pymupdf

from .extract import PageText
from .util import bbox_r, r1, relpath, sha256_bytes, sha256_file

CROP_DPI = 200
CONTEXT_DPI = 60
INK_DPI = 50
INK_THRESHOLD = 160          # grey level below which a pixel counts as ink
INK_CELL_PT = 12.0           # grid cell size for unexplained-ink clustering
INK_MIN_PIXELS = 6           # unexplained dark pixels needed for a cell to count


@dataclass
class Region:
    region_id: str
    doc: str
    page: int
    kind: str                 # image | vector_graphic | invisible_text | unexplained_ink
    bbox: list[float]
    detection: str
    xref: int | None = None
    native: dict | None = None        # {path, sha256, width, height, ext}
    crop: dict | None = None          # {path, sha256, dpi}
    context: dict | None = None       # {path, sha256, dpi}
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


LIGHT_FILL = 0.8               # fill luminance at or above which a rectangle is background shading
RULE_PT = 2.5                  # a filled rectangle thinner than this is a rule (a border drawn as a box)


def _axis_aligned(p, q, tol: float = 0.5) -> bool:
    return abs(p.x - q.x) <= tol or abs(p.y - q.y) <= tol


def _is_structural(path: dict, text_points: list[pymupdf.Point]) -> bool:
    """Rules, borders and shading are structure; anything else drawn is content to be reviewed."""
    items = path.get("items", [])
    if not items:
        return True
    kinds = {it[0] for it in items}
    r = pymupdf.Rect(path["rect"])
    if kinds <= {"l"}:
        return all(_axis_aligned(it[1], it[2]) for it in items)      # rules; a diagonal is a drawing
    if kinds <= {"re", "qu"}:
        if any(it[0] == "qu" and not it[1].is_rectangular for it in items):
            return False
        if all(min(pymupdf.Rect(it[1].rect if it[0] == "qu" else it[1]).width,
                   pymupdf.Rect(it[1].rect if it[0] == "qu" else it[1]).height) < RULE_PT for it in items):
            return True                                              # thin filled bars: rules drawn as boxes
        fill = path.get("fill")
        if fill is None or (0.299 * fill[0] + 0.587 * fill[1] + 0.114 * fill[2]) >= LIGHT_FILL:
            return True                                              # borders, light cell shading
        return any(r.contains(pt) for pt in text_points)             # dark band carrying text (header)
    return False                                                     # curves, mixed paths: a drawing


def _merge_rects(rects: list[pymupdf.Rect], gap: float = 6.0) -> list[pymupdf.Rect]:
    rects = [pymupdf.Rect(r) for r in rects]
    changed = True
    while changed:
        changed = False
        out: list[pymupdf.Rect] = []
        for r in rects:
            for i, o in enumerate(out):
                if (o + (-gap, -gap, gap, gap)).intersects(r):
                    out[i] = o | r
                    changed = True
                    break
            else:
                out.append(r)
        rects = out
    return sorted(rects, key=lambda r: (r.y0, r.x0))


def _gray(pix: pymupdf.Pixmap) -> np.ndarray:
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    if pix.n >= 3:
        return a[..., :3].mean(axis=2)
    return a[..., 0].astype(float)


def unexplained_ink(page: pymupdf.Page, explained: list[pymupdf.Rect]) -> list[pymupdf.Rect]:
    """Cells of the page render that contain dark pixels no known object accounts for."""
    pix = page.get_pixmap(dpi=INK_DPI, colorspace=pymupdf.csGRAY)
    g = _gray(pix)
    ink = g < INK_THRESHOLD
    scale = INK_DPI / 72.0
    mask = np.zeros_like(ink)
    for r in explained:
        x0 = max(int((r.x0 - 1.5) * scale), 0)
        y0 = max(int((r.y0 - 1.5) * scale), 0)
        x1 = min(int((r.x1 + 1.5) * scale) + 1, ink.shape[1])
        y1 = min(int((r.y1 + 1.5) * scale) + 1, ink.shape[0])
        mask[y0:y1, x0:x1] = True
    left = ink & ~mask
    cell = max(int(INK_CELL_PT * scale), 1)
    found = []
    for y in range(0, left.shape[0], cell):
        for x in range(0, left.shape[1], cell):
            if left[y:y + cell, x:x + cell].sum() >= INK_MIN_PIXELS:
                found.append(pymupdf.Rect(x / scale, y / scale, (x + cell) / scale, (y + cell) / scale))
    return _merge_rects(found, gap=1.0)


def detect_regions(doc_id: str, page: pymupdf.Page, text: PageText) -> list[Region]:
    pno = page.number + 1
    regions: list[Region] = []
    explained: list[pymupdf.Rect] = []

    # text spans explain their own ink (rotated spans by character boxes)
    for s in text.content:
        if s.char_bboxes:
            explained.extend(pymupdf.Rect(b) for b in s.char_bboxes)
        else:
            explained.append(pymupdf.Rect(s.bbox))
    raw = page.get_text("rawdict")
    for block in raw["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for sp in line["spans"]:
                for ch in sp["chars"]:
                    explained.append(pymupdf.Rect(ch["bbox"]))   # covers excluded furniture too

    # 1. embedded raster images
    for info in sorted(page.get_image_info(xrefs=True), key=lambda i: (i["bbox"][1], i["bbox"][0])):
        rect = pymupdf.Rect(info["bbox"]) & page.rect
        if rect.is_empty:
            continue
        explained.append(rect)
        regions.append(Region("", doc_id, pno, "image", bbox_r(rect),
                              "embedded raster image (get_image_info)", xref=info.get("xref") or None))

    # 2. vector drawings that are not table structure
    text_points = [pymupdf.Point(s.cx, s.cy) for s in text.content if s.text.strip()]
    graphic = []
    for path in page.get_drawings():
        r = pymupdf.Rect(path["rect"])
        explained.append(r)
        if not _is_structural(path, text_points):
            graphic.append(r)
    for r in _merge_rects(graphic):
        regions.append(Region("", doc_id, pno, "vector_graphic", bbox_r(r),
                              "uncertain drawing (diagonal or free-form lines, curves, or a dark fill with no "
                              "text on it); needs a reading"))

    # 3. invisible text (never trusted as content; flags the area for reading)
    inv = [pymupdf.Rect(tr["bbox"]) for tr in page.get_texttrace()
           if tr.get("type") == 3 or tr.get("opacity", 1) == 0]
    for r in _merge_rects(inv):
        hosts = [g for g in regions if g.kind == "image" and pymupdf.Rect(g.bbox).intersects(r)]
        if hosts:
            hosts[0].notes.append("invisible text layer overlaps this image; it is not used as content")
        else:
            regions.append(Region("", doc_id, pno, "invisible_text", bbox_r(r),
                                  "text with render mode 3 or zero opacity"))

    # 4. ink nobody explains
    for r in unexplained_ink(page, explained):
        regions.append(Region("", doc_id, pno, "unexplained_ink", bbox_r(r),
                              f"page render at {INK_DPI} dpi: dark pixels outside every text, image and drawing box"))

    regions.sort(key=lambda g: (g.bbox[1], g.bbox[0], g.kind))
    for i, g in enumerate(regions, 1):
        g.region_id = f"{doc_id}-p{pno}-r{i}"
    return regions


def save_region_evidence(doc: pymupdf.Document, region: Region, out_dir: Path, base: Path) -> None:
    """Native image bytes (as embedded), a rendered crop and an outlined page context.

    Paths are recorded relative to `base` (the build directory) so outputs do not depend on
    where the build was made."""
    page = doc[region.page - 1]
    rdir = out_dir / region.region_id
    rdir.mkdir(parents=True, exist_ok=True)
    rect = pymupdf.Rect(region.bbox)
    if region.xref:
        img = doc.extract_image(region.xref)
        npath = rdir / f"native.{img['ext']}"
        npath.write_bytes(img["image"])
        region.native = {"path": relpath(npath, base), "sha256": sha256_bytes(img["image"]),
                         "width": img["width"], "height": img["height"], "ext": img["ext"]}
    pix = page.get_pixmap(clip=rect, dpi=CROP_DPI)
    cpath = rdir / "crop.png"
    pix.save(cpath)
    region.crop = {"path": relpath(cpath, base), "sha256": sha256_file(cpath), "dpi": CROP_DPI}
    ctx_doc = pymupdf.open()
    ctx = ctx_doc.new_page(width=page.rect.width, height=page.rect.height)
    ctx.show_pdf_page(ctx.rect, doc, page.number)
    ctx.draw_rect(rect, color=(0.85, 0.1, 0.1), width=2)
    ctx.insert_text((rect.x0, max(rect.y0 - 4, 10)), region.region_id, fontsize=8, color=(0.85, 0.1, 0.1))
    xpath = rdir / "context.png"
    ctx.get_pixmap(dpi=CONTEXT_DPI).save(xpath)
    region.context = {"path": relpath(xpath, base), "sha256": sha256_file(xpath),
                      "dpi": CONTEXT_DPI}


# ---------------------------------------------------------------- raster structure

def image_array(doc: pymupdf.Document, region: Region) -> np.ndarray:
    """Greyscale pixels of the native image if embedded, else of a rendered crop."""
    if region.xref:
        pix = pymupdf.Pixmap(doc.extract_image(region.xref)["image"])
    else:
        pix = doc[region.page - 1].get_pixmap(clip=pymupdf.Rect(region.bbox), dpi=CROP_DPI)
    return _gray(pix)


def estimate_skew(ink: np.ndarray, span_deg: float = 2.0, step: float = 0.02) -> float:
    """Angle (degrees) that maximises the sharpness of the horizontal projection profile."""
    ys, xs = np.nonzero(ink)
    best = (-1.0, 0.0)
    for th in np.arange(-span_deg, span_deg + 1e-9, step):
        t = np.tan(np.radians(th))
        idx = np.round(ys - xs * t).astype(int)
        prof = np.bincount(idx - idx.min()).astype(float)
        score = float(np.square(prof).sum())
        if score > best[0]:
            best = (score, float(th))
    return round(best[1], 2)


def _lines(ink: np.ndarray, skew: float, axis: str, frac: float) -> list[float]:
    ys, xs = np.nonzero(ink)
    t = np.tan(np.radians(skew))
    idx = np.round(ys - xs * t).astype(int) if axis == "h" else np.round(xs + ys * t).astype(int)
    off = idx.min()
    prof = np.bincount(idx - off)
    span = ink.shape[1] if axis == "h" else ink.shape[0]
    cand = np.nonzero(prof > frac * span)[0]
    groups: list[list[int]] = []
    for c in cand:
        if groups and c - groups[-1][-1] <= 3:
            groups[-1].append(int(c))
        else:
            groups.append([int(c)])
    return [float(np.mean(g) + off) for g in groups]


@dataclass
class Grid:
    skew_deg: float
    h_lines: list[float]          # positions in the image (pixels), measured along the skew
    v_lines: list[float]
    width: int
    height: int

    @property
    def rows(self) -> int:
        return max(len(self.h_lines) - 1, 0)

    @property
    def cols(self) -> int:
        return max(len(self.v_lines) - 1, 0)

    def cell_box(self, r: int, c: int, pad: int = 3) -> tuple[int, int, int, int]:
        """Axis-aligned pixel box enclosing cell (r, c) of the skewed grid."""
        t = np.tan(np.radians(self.skew_deg))
        x0, x1 = self.v_lines[c], self.v_lines[c + 1]
        y0, y1 = self.h_lines[r], self.h_lines[r + 1]
        # line y = y_line + x * t ; line x = x_line - y * t
        ys = [y0 + x0 * t, y0 + x1 * t, y1 + x0 * t, y1 + x1 * t]
        xs = [x0 - y0 * t, x1 - y0 * t, x0 - y1 * t, x1 - y1 * t]
        return (max(int(min(xs)) - pad, 0), max(int(min(ys)) - pad, 0),
                min(int(max(xs)) + pad, self.width), min(int(max(ys)) + pad, self.height))


def _bounded_by_rules(ink: np.ndarray, skew: float, h: list[float], min_rules: int = 2, cover: float = 0.8,
                      margin: int = 5) -> list[float]:
    """Session 13 (E160): the horizontal rules that belong to ONE table: a band between two consecutive rules is a
    table band when at least `min_rules` vertical rules cross it (ink over >= `cover` of the band's height at one
    column, measured along the skew); the table is the longest run of consecutive table bands and its rules are
    returned. A rule nothing connects to the next one (a letterhead separator above the table, a footer line below
    it) is dropped: blind-07's page 3 counted the letterhead rule as an 8th horizontal rule and refused a correct
    reading. When no band qualifies the rules are returned unchanged (no table is claimed; the columns decide)."""
    if len(h) < 2:
        return h
    ys, xs = np.nonzero(ink)
    t = np.tan(np.radians(skew))
    yl = ys - xs * t                                    # the row of each ink pixel, along the skew
    xl = xs + ys * t                                    # its column, along the skew
    flags = []
    for y0, y1 in zip(h[:-1], h[1:]):
        a, b = y0 + margin, y1 - margin
        if b - a < 2 * margin:
            flags.append(False)
            continue
        sel = (yl >= a) & (yl <= b)
        if not sel.any():
            flags.append(False)
            continue
        col = np.round(xl[sel]).astype(int)
        prof = np.bincount(col - col.min())
        cand = np.nonzero(prof >= cover * (b - a))[0]
        groups = 0
        last = None
        for c in cand:
            if last is None or c - last > 3:
                groups += 1
            last = c
        flags.append(groups >= min_rules)
    best = (0, 0, 0)                                    # (length, start, end) of the longest run of table bands
    i = 0
    while i < len(flags):
        if flags[i]:
            j = i
            while j + 1 < len(flags) and flags[j + 1]:
                j += 1
            if j - i + 1 > best[0]:
                best = (j - i + 1, i, j)
            i = j + 1
        else:
            i += 1
    if best[0] == 0:
        return h
    return h[best[1]:best[2] + 2]


def detect_grid(gray: np.ndarray, frac: float = 0.5) -> Grid:
    ink = gray < 140
    skew = estimate_skew(ink)
    h = _lines(ink, skew, "h", frac)                      # rules spanning > frac of the width
    h = _bounded_by_rules(ink, skew, h)                   # session 13 (E160): only the rules vertical rules connect
    table_h = (h[-1] - h[0]) if len(h) > 1 else ink.shape[0]
    v = _lines(ink, skew, "v", 0.6 * table_h / ink.shape[0])  # rules spanning > 60% of the table height
    return Grid(skew, [r1(x) for x in h], [r1(x) for x in v], ink.shape[1], ink.shape[0])


def despeckle(ink: np.ndarray, min_neighbours: int = 2) -> np.ndarray:
    """Drop isolated dark pixels (scan speckle): keep ink with >= min_neighbours dark neighbours."""
    n = np.zeros(ink.shape, dtype=np.int16)
    p = np.pad(ink, 1)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy or dx:
                n += p[1 + dy:1 + dy + ink.shape[0], 1 + dx:1 + dx + ink.shape[1]]
    return ink & (n >= min_neighbours)


def _erase_long_runs(ink: np.ndarray, axis: int, min_len: int) -> tuple[np.ndarray, int]:
    """Remove straight ink runs longer than min_len along rows (axis=1) or columns (axis=0)."""
    out = ink.copy()
    a = out if axis == 1 else out.T
    removed = 0
    for i in range(a.shape[0]):
        row = a[i]
        if row.sum() < min_len:
            continue
        edges = np.flatnonzero(np.diff(np.concatenate(([0], row.astype(np.int8), [0]))))
        for s0, e0 in zip(edges[::2], edges[1::2]):
            if e0 - s0 >= min_len:
                row[s0:e0] = False
                removed += 1
    return out, removed


def ink_mask(gray: np.ndarray, delta: float = 80.0) -> np.ndarray:
    """Ink relative to the image's own background (median), despeckled. Catches faint grey text."""
    bg = float(np.median(gray))
    return despeckle(gray < bg - delta)


def text_bands(gray: np.ndarray, min_gap: int = 6, min_height: int = 8) -> list[dict]:
    """Text lines of an image region, after removing ruling lines (box borders, table grid).

    Each band: index, y0, y1 (pixels), x0, x1, and split_x when the band holds two separate
    blocks side by side (e.g. an English label on the left and its Arabic counterpart on the
    right): the largest internal gap, if it exceeds max(40 px, 2.5% of width) and each side
    holds at least 10% of the band's ink.
    """
    ink = ink_mask(gray)
    H, W = ink.shape
    ink, _ = _erase_long_runs(ink, axis=1, min_len=max(int(0.3 * W), 60))
    ink, _ = _erase_long_runs(ink, axis=0, min_len=max(int(0.04 * H), 80))
    rows = ink.sum(axis=1) > 0.003 * W
    bands = []
    y = 0
    while y < H:
        if rows[y]:
            s0 = y
            while y < H and (rows[y] or rows[y:y + min_gap].any()):
                y += 1
            if y - s0 >= min_height:
                bands.append((s0, y))
        else:
            y += 1
    out = []
    for i, (a, b) in enumerate(bands):
        colsum = ink[a:b].sum(axis=0)
        xs = np.flatnonzero(colsum >= 2)
        if len(xs) == 0:
            xs = np.flatnonzero(colsum > 0)
        split = None
        if len(xs) > 1:
            gaps = np.diff(xs)
            j = int(np.argmax(gaps))
            if gaps[j] > max(40, 0.025 * W):
                left, right = colsum[:xs[j] + 1].sum(), colsum[xs[j + 1]:].sum()
                tot = left + right
                if left >= 0.1 * tot and right >= 0.1 * tot:
                    split = int((xs[j] + xs[j + 1]) // 2)
        # rule residue (a skewed or broken ruling line): thin, long and almost gap-free.
        # Text has gaps between glyphs and taller ink columns.
        span_w = int(xs.max()) + 1 - int(xs.min())
        inked = colsum[xs.min():xs.max() + 1] > 0
        frac = float(inked.mean()) if span_w else 0.0
        med = float(np.median(colsum[xs.min():xs.max() + 1][inked])) if inked.any() else 0.0
        kind = "rule" if (b - a) <= 24 and span_w >= 0.3 * W and frac >= 0.8 and med <= 5 else "text"
        out.append({"index": i, "y0": int(a), "y1": int(b), "x0": int(xs.min()), "x1": int(xs.max()) + 1,
                    "split_x": split if kind == "text" else None, "kind": kind})
    return out
