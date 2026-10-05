# Subagent brief 3: Build A1/A3 deterministic renderers

Launched 2026-10-02 07:51:02 UTC; model option requested: `(default)`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

Implement deterministic output writers for a tender-pack reader. Repository: /home/user/tender-pack-reader (Python 3.11; `.venv/bin/python`; tests: `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_render.py`). Available libraries: PyMuPDF (`import pymupdf`, 1.28.2), openpyxl 3.1.5, standard library. You may create/edit ONLY `tenderpack/render.py` and `tests/test_render.py`. Do not edit other files, do not commit or push. Match the repo's style (module docstring, type hints, short comments). Read tenderpack/util.py for `dump_json` (deterministic JSON) and use it for JSON outputs.

Byte-for-byte determinism is a hard requirement: writing the same input twice (in different directories, at different times) must produce identical bytes for every file. openpyxl stamps created/modified times in docProps/core.xml and zip entry timestamps; fix both (set workbook properties created/modified/lastModifiedBy to fixed values, and after saving, rewrite the zip with every ZipInfo.date_time = (1980,1,1,0,0,0), entries in a fixed order, same compression). For PDF use PyMuPDF and save with `garbage=3, deflate=True, no_new_id=True` and fixed metadata (creationDate/modDate "D:20261001000000Z", producer "tenderpack").

API to implement (keep names/signatures):

1. `write_a1(a1: dict, out_dir: Path) -> list[Path]` writes `a1.json`, `a1.csv`, `a1.xlsx` into out_dir and returns the paths. Input contract:
```
a1 = {
  "title": str, "notice": str,                      # notice: e.g. "DRAFT - interpretations proposed by the assistant, not reviewed; image readings pending"
  "stages": ["BASE", "ADD-01", "ADD-02"],           # ordered
  "validated_stage": "ADD-02", "working_stage": None or "ADD-03",
  "columns": [ {"key": str, "header": str, "width": int} , ... ],   # ordered; keys may include per-stage ones like "status:ADD-01"
  "rows": [ {key: value, ...}, ... ],               # values are str, int, float, bool, None, or list[str] (join lists with "; " in CSV/XLSX)
  "sheets": { "Dates": {"columns": [...same shape...], "rows": [...]}, "Issues": {...}, "Stages": {...}, "Assumptions": {...} }  # optional extra sheets, any number, ordered by key insertion
}
```
- a1.json: `dump_json(a1, path)`.
- a1.csv: the main rows only, header row = column headers, UTF-8 with BOM (so Excel opens Arabic correctly), `\r\n` line endings via csv module, values as text (None -> "", bool -> "TRUE"/"FALSE", lists joined with "; ").
- a1.xlsx: first sheet "A1 register" with a 2-line banner above the table (row 1 = title in bold, row 2 = notice in italic), header row 4 frozen, autofilter over the table, column widths from `width`, wrap text, top-aligned; cells whose header starts with "status:" get a fill by value: values beginning "DELETED" grey (#D9D9D9), "STALE" or containing "STALE" orange (#FCE4D6), "NEW" or "REINSTATED" green (#E2EFDA), "AMENDED" yellow (#FFF2CC), "NOT ISSUED" light grey (#F2F2F2); cells containing the text "pending" (case-insensitive) in any column whose key contains "status" get italic font. Then one sheet per entry of `sheets` (header row 1 bold, frozen, autofilter, widths). Right-to-left text (Arabic) must be preserved as given (no reordering).

2. `write_csv_json(table: dict, out_dir: Path, stem: str) -> list[Path]` generic: table = {"columns": [...], "rows": [...]} -> stem.csv (same CSV conventions) and stem.json (dump_json of the dict). Used for A2 and A5 tables.

3. `write_a3_pdf(a3: dict, path: Path) -> dict` renders ONE A4 portrait page and returns {"pages": 1, "scale": float, "spare_pt": float}. If the content cannot fit on one page at a scale >= 0.62, raise `A3OverflowError` (define it) — never silently drop content and never produce a second page. Input contract:
```
a3 = {
  "title": str, "subtitle": str,                           # subtitle: state line, e.g. "Validated state: ADD-02 ... DRAFT"
  "banner": str,                                           # one-line warning shown in a shaded box at the top
  "sections": [ {"heading": str, "note": str or "", "items": [ {"id": str, "text": str, "consequence": str, "source": str, "confidence": str, "flags": [str]} ] } ],
  "unresolved": {"heading": str, "items": [ {"id": str, "text": str, "owner": str} ]},
  "footer": str
}
```
Layout: compact, legible, sober (no logos, no colour except a light grey banner box and small red text for flags). Use `page.insert_htmlbox(rect, html, css=..., scale_low=0.62)` and interpret its return value (spare height, scale; spare < 0 means it did not fit) — check PyMuPDF docs/behaviour by experiment. Escape HTML. Arabic text inside items must render right-to-left correctly: wrap any item text containing Arabic letters (U+0600–U+06FF) in `<span dir="rtl">…</span>`; check visually by rendering a test page to PNG (you can view PNGs) that Arabic shapes and reads correctly. Each item renders as one compact line or two: bold id, text, consequence in quotes, source, confidence, flags in red.

Tests (tests/test_render.py): build small synthetic inputs (include one Arabic string like "يؤدي إلى استبعاد العرض" and a list value); check files exist, CSV header/rows, xlsx opens with openpyxl and has the expected sheets/frozen panes/fills, JSON round-trips, two writes into two temp dirs are byte-identical for all files (xlsx, csv, json, pdf), the A3 PDF has exactly 1 page and contains key texts (page.get_text()), and an oversized A3 input (e.g. 300 items) raises A3OverflowError. Make all tests pass.

Final message: report the API as implemented (any deviation and why), how determinism was achieved, the pytest result line, and a path to one rendered sample A3 PNG you produced under /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/render-agent/ (put any scratch files there).
