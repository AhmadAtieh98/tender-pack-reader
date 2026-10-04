# Blind rehearsal 04: frozen before the run

**Synthetic, not tender content.** An independent author (a separate subagent session, started cold from a brief) wrote
an unseen-style Addendum No. 3 on the base pack (Volumes I, II, IV, V as amended by Addenda 1 and 2), from the pack's
PDFs, the brief and the correspondence only, reading the blind-01, blind-02 and blind-03 addenda solely to avoid
overlapping their subjects and the blind-03 builder and author notes as a technique example. It did not read the tool's
code, tests, curation, config, outputs, docs, work logs, staging, or any rehearsal's work, outputs, comparison or
answer key. Its answer key, notes and builder script were written outside the repository and are sealed by the hash
below. The coordinator and the processing agents have not read them.

Recorded 4 Oct 2026, 14:12:18 UTC, before the addendum was opened or ingested. The hashes were computed by the
coordinator with `sha256sum` and equal the ones the author reported (the author's final message carried only the
hashes, the page count, the issue date, its elapsed time, about 32 minutes, and its model, Opus 5.5 by its own
report).

| File | sha256 |
|---|---|
| `input/ADD-03_Addendum_No_3.pdf` (5 pages; prints "Issued 9 November 2026") | `99728136b5653acdd75d0e7b682f990f877ae2587452ffee58be0bd85b28452e` |
| sealed `SHA256SUMS` (over `build_addendum.py`, `expected_findings.yaml`, `author_notes.md` and the PDF) | `803dfbe9b314cd1b421424a20c2c204f525ceaac65e5f898a21c188c30698aaf` |

The sealed files are added to `SEALED/` unchanged after the first outputs are frozen, so `sha256sum -c SEALED/SHA256SUMS`
(the three files from inside `SEALED/`, the PDF line from the repository root) and the hash of `SEALED/SHA256SUMS`
above can be checked.

**What this rehearsal is for (session 10):** the first unseen addendum processed by the runnable workflow
(`tenderpack ai run`): ingestion into a disposable candidate workspace → AI analysis in batches on the host route (a
headless host session that has only the MCP tools, so it cannot reach the sealed key) → sourced proposals including
the downstream rows, readings, issues, clarification items, evidence items, activities and dependencies → deterministic
validation → impact → candidate A1–A5 outputs → review packet, with checkpoints; measured against the brief's
30-minute segment. The first candidate outputs are frozen before the key is opened; anything changed afterwards is
labelled and not scored.
