# Blind rehearsal 03: frozen before the run

**Synthetic, not tender content.** An independent author (a separate subagent session, started cold from a brief) wrote
an unseen-style Addendum No. 3 from the pack's PDFs, the correspondence and the brief only, reading the blind-01 and
blind-02 addenda solely to avoid overlapping their changes and the blind-02 builder as a style example. It did not read
the tool's code, tests, curation, config, outputs, docs or work logs. Its answer key, notes and builder script were
written outside the repository and are sealed by the hash below. The coordinator and the curators have not read them.

Recorded 4 Oct 2026, 09:22:15 UTC, before the addendum was opened or ingested. The hashes were computed by the
coordinator with `sha256sum` and equal the ones the author reported (the author's final message carried only hashes,
the page count, the issue date and its elapsed time: about 25 minutes).

| File | sha256 |
|---|---|
| `input/ADD-03_Addendum_No_3.pdf` (4 pages; prints "Issued 1 November 2026") | `ecdf3e24b35faca2f5d2fe8bb2b2427c6e38db5a71672e90703da5712996c6b7` |
| sealed `SHA256SUMS` (over `build_addendum.py`, `expected_findings.yaml`, `author_notes.md` and the PDF) | `46b75b145294323704406da1b006e42474f758ab3012b9dbb5845b9eb95cb42e` |

The sealed files are added to `SEALED/` unchanged after the rehearsal, so `sha256sum -c SEALED/SHA256SUMS` (the three
files from inside `SEALED/`, the PDF line from the repository root) and the hash of `SEALED/SHA256SUMS` above can be
checked.

**What this rehearsal is for (session 09):** the first unseen addendum processed with the AI layer in the loop — the
model proposes, the deterministic controller validates and simulates, a person decides — through the normal path
(`ingest` → `draft` → AI proposals to staging → curation → `pin` → `check-register` → `outputs` → `diff`), with the
pre-key results kept apart from anything changed after the key is opened. Blind-02 is regression material from now on.
