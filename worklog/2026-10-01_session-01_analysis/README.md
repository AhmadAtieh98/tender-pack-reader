# Session 01 analysis scripts (throwaway; NOT application code)

These are the temporary analysis scripts run during the planning exchange of session 01, kept
so that the findings in `docs/PLAN.md` §2 can be reproduced. They are not part of the system,
they are not tested, and they will not be imported by it.

They were run from the session scratchpad against the unzipped upload, hence the relative path
`src/lamarholdingpppaipartnerround2assignment/candidate_pack`. To re-run them against this
repository, change `P` to `sources/candidate_pack`. They need PyMuPDF (installed in a scratch venv
during the session; it is not yet a project dependency).

| Script | What it established |
|---|---|
| `fonts.py` | First span scan (filter too broad, see work log error E2); image blocks; metadata |
| `fonts2.py` | Corrected scan: small print (ADD-02 notes 7.2 pt), superscripts, rotated watermark text |
| `misc.py` | No annotations, links, widgets, embedded files; no white text outside dark fills; image bboxes |
| `strike.py` | No strike-throughs (all hits were watermark-bbox false positives, see E3) |
| `grep.py` | Repeated wording, PDD references, consequence phrases, referenced-but-missing documents, day periods |
| `draw.py` | Vector drawings are greyscale table rules/fills plus two separator rules only |
| `superscript_count.py` | 12 superscript spans = 11 m³ exponents + 1 footnote marker (see E4) |
| `dates_check.py` | Weekdays and PDD-relative dates in docs/PLAN.md §2.5 |

Shell one-liners also used: `unzip`, `sha256sum`, `pdfinfo`, `pdftotext` (raw and `-layout`),
`pdfimages -list` / `-png`, `pdftoppm -r 100`.
