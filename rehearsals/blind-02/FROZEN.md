# Blind rehearsal 02: frozen before the run

**Synthetic, not tender content.** An independent author (a separate subagent session) wrote an unseen-style
Addendum No. 3 from the pack's PDFs and the brief only. It did not read the tool's code, tests, curation or outputs.
Its answer key, notes and builder script were written outside the repository and are sealed by the hash below. The
engineer running the rehearsal has not read them.

Recorded 3 Oct 2026, 20:25 UTC, before the addendum was opened or ingested.

| File | sha256 |
|---|---|
| `input/ADD-03_Addendum_No_3.pdf` (4 pages; prints "Issued 3 November 2026") | `0655d5e07967a2572390d60573cfe4c81680513472841a7e3827c04e59be3a81` |
| sealed `SHA256SUMS` (over `build_addendum.py`, `expected_findings.yaml`, `author_notes.md` and the PDF) | `a9277b0a21deaa721fe1fdec496909107f3fa47d6fe496162023fb505f2757bf` |

The sealed files are added to `SEALED/` unchanged after the rehearsal, so `sha256sum -c SEALED/SHA256SUMS` and the hash
of `SEALED/SHA256SUMS` above can be checked.
