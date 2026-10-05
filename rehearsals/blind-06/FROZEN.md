# Blind rehearsal 06: frozen before the run

**Synthetic, not tender content.** An independent author (a separate subagent session, started cold from a brief)
wrote an unseen-style Addendum No. 3 on the base pack (Volumes I, II, IV, V as amended by Addenda 1 and 2) and a short
Addendum No. 4 that stacks on its own Addendum No. 3 (for the consecutive-addenda check), from the pack's PDFs, the
brief and the correspondence only. It was told to read the blind-01 to blind-05 addenda solely to avoid overlapping
their subjects, and blind-05's builder script and author notes as a technique example, and not to read the tool's
code, tests, curation, config, outputs, docs, work logs, staging, or any rehearsal's work, outputs, comparison or answer
key. Its answer key, notes and builder script were written outside the repository (the coordinator's scratchpad,
`s12/blind06-sealed/`) and are sealed by the hash below. The coordinator and the processing agents have not read them;
the coordinator listed the sealed folder's file names and sizes and hashed its `SHA256SUMS` without opening any of
the files, and checked the two PDFs against the author's reported hashes with `sha256sum -c --ignore-missing`.

Recorded 5 Oct 2026, 09:53:37 UTC, before either addendum was ingested. The coordinator ran `pdfinfo` for the page
counts only (it did not read the PDFs). The author's final message carried only the hashes, the page counts, the
printed issue dates, its elapsed time (about 29 minutes 26 seconds, 09:23:48 to 09:53:13 UTC) and its model (Opus 5.5
by its own report).

| File | sha256 |
|---|---|
| `input/ADD-03_Addendum_No_3.pdf` (5 pages; the author reports "Issued 10 November 2026") | `9b96c1f627af3c50e15fd8527159d6d012e98827d3479ba10d473fcc8d209341` |
| `input/ADD-04_Addendum_No_4.pdf` (2 pages; the author reports "Issued 16 November 2026") | `bb1d2a8b7da2fa5674a4fc06faf02af19c5d36994445942b810d78c89b16027e` |
| sealed `SHA256SUMS` (over `build_addendum.py`, `expected_findings.yaml`, `author_notes.md` and the two PDFs) | `b57023adcfb0d984e339005d9cf0dbab2a5e26dff293f23efc0d6ba9b84b68a3` |

The sealed files are added to `SEALED/` unchanged after the first outputs are frozen, so `sha256sum -c SEALED/SHA256SUMS`
(the three files from inside `SEALED/`, the PDF lines from the repository root) and the hash of `SEALED/SHA256SUMS`
above can be checked.

The run happens after this session's core fixes are merged (the point of the rehearsal is the workflow as it will be
handed over); the time from the PDF to the frozen candidate outputs is measured against the brief's 30 minutes and
reported in `COMPARISON.md` with detection, usable updates, missed effects, pending decisions and interventions
counted separately.
