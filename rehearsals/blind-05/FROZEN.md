# Blind rehearsal 05: frozen before the run

**Synthetic, not tender content.** An independent author (a separate subagent session, started cold from a brief)
wrote an unseen-style Addendum No. 3 on the base pack (Volumes I, II, IV, V as amended by Addenda 1 and 2), from the
pack's PDFs, the brief and the correspondence only. It was told to read the blind-01 to blind-04 addenda solely to avoid
overlapping their subjects and the earlier builder scripts and author notes as a technique example, and not to read the
tool's code, tests, curation, config, outputs, docs, work logs, staging, or any rehearsal's work, outputs, comparison or
answer key. Its answer key, notes and builder script were written outside the repository (the coordinator's scratchpad)
and are sealed by the hash below. The coordinator and the processing agents have not read them; the coordinator listed
the sealed folder's file names and sizes and hashed its `SHA256SUMS` without opening any of the files.

Recorded 4 Oct 2026, 2026-10-04 19:20:22 UTC, before the addendum was ingested. The coordinator ran `pdfinfo` for the page count and looked at the first lines of the cover page (title, tender number, issue date) to confirm the printed date; nothing else of the PDF was read before the run. The hashes were computed by the
coordinator with `sha256sum` and equal the ones the author reported (the author's final message carried only the
hashes, the page count, the printed issue date, its elapsed time, about 47 minutes, and its model, Opus 5.5 by its own
report).

| File | sha256 |
|---|---|
| `input/ADD-03_Addendum_No_3.pdf` (5 pages; prints "Issued 15 November 2026") | `9c5e22d59a80d48f82f07cbb0cfb7649f14a8618fb8fc4503a576f4a0293eae3` |
| sealed `SHA256SUMS` (over `build_addendum.py`, `expected_findings.yaml`, `author_notes.md` and the PDF) | `0ed6f3ab23bf4fedf4283b19e6da61ebc5e085b6f3eb545be13cfa11e4a879c7` |

The sealed files are added to `SEALED/` unchanged after the first outputs are frozen, so `sha256sum -c SEALED/SHA256SUMS`
(the three files from inside `SEALED/`, the PDF line from the repository root) and the hash of `SEALED/SHA256SUMS`
above can be checked.

**What this rehearsal is for (session 11):** the first unseen addendum processed by the workflow after the session-11
changes (explicit requirement introduction and applicability, ID-based downstream updates, completion that reflects
downstream coverage, state bindings over every curated input, one request path with failure classes, bounded backoff and
resumable checkpoints, the selective critic inside the workflow, calculation tools, cycle-safe relationship traversal,
conditional and effective-dated amendments, candidate A3/A5 for partial states). It runs on the host route (a headless
host session that has only the MCP tools, so it cannot reach the sealed key), measured from receiving the PDF to a
working update against the brief's 30-minute segment. The first candidate outputs are frozen before the key is opened;
anything changed afterwards is labelled and not scored. Detection results, missed effects, unresolved decisions, manual
interventions and review effort are reported separately in `COMPARISON.md`.
