# Blind rehearsal 01: results against the sealed answer key

## How the rehearsal ran

- **The addendum:** an independent subagent wrote it from the sources and the brief only (`FROZEN.md`).
- **The freeze:** the answer key was frozen by hash in commit `53ad76f` (pushed 01:05:50 UTC).
- **Blind curation:** the orchestrator ran the normal workflow and recorded its results before opening the key. It opened `SEALED/` at 01:29:49 UTC, after the curated outputs and `diff` were written. Every hash matched (`sha256sum -c SEALED/SHA256SUMS`).
- **Limits of the blindness:** the author's brief named the kinds of change the addendum had to contain (a date chain, a Working-Day period, a text-table cell, an image-only value, a deletion, an insertion with a consequence, a scope trap, a substantive and a restating answer, one ambiguity, and two change types not used in ADD-01/02, chosen from an example list that included renumbering). The curator therefore knew the categories, but not the provisions or values. Before the rehearsal the orchestrator learned only the hashes, the page count, the issue date and the author's elapsed time (checked against the session transcript). The curator was the assistant, which also wrote the code.
- **What was scored:** the outputs scored here are the ones made blind: `out-drafted/`, `out-curated/` and `diff-ADD-02-to-ADD-03.md`, all as published at 01:28 UTC. Fixes made after the comparison are listed at the end and are not counted as hits.

## Timeline (UTC, from `clock.txt`; wall clock including the curator's reading and writing)

| Step | Start | End | Elapsed |
|---|---|---|---|
| Set up the pack (received PDF + copies of the curation) | 01:17:17 | 01:17:22 | 0:05 |
| Ingest, Stage 1 (7 documents, 569 units): C01–C10 pass first time | 01:17:22 | 01:17:35 | 0:13 |
| Draft (6 ops; 23 provisions unresolved) and read every ADD-03 unit | 01:17:40 | 01:19:17 | 1:37 |
| **Live fix 1:** drafter phrasings (qualified citations, "further amended", footnote target, "new Clause … inserted in"); tests | 01:19:17 | 01:19:53 | 0:36 |
| Re-draft (10 ops; 19 for a person). Drafted working draft published (PARTIAL; validated state stays ADD-02) | 01:19:53 | 01:20:11 | 0:18 |
| Reading the engine's handling of chained amendments (no clock entry) | 01:20:11 | 01:21:40 | 1:29 |
| **Live fix 2:** text-cell `set_value`; `replace_text` in a table row updates the cell; tests | 01:21:40 | 01:23:01 | 1:21 |
| Checking the re-drafted state (no clock entry) | 01:23:01 | 01:24:00 | 0:59 |
| Curation of the op file (28 ops, 4 dispositions) | 01:24:00 | 01:24:44 | 0:44 |
| **Live fix 3:** citation forms (Appendix A to Addendum No. 1; clarification request 13 in Addendum No. 2; "the fifth numbered declaration"; "in row 2-6.2"); tests | 01:24:44 | 01:24:54 | 0:10 |
| Rows: 4 new, 11 interpretations re-made, 1 row extended, 4 issues; replanning (hard copies 3 → 0) | 01:24:54 | 01:25:56 | 1:02 |
| Pin the new interpretations; record new row ids | 01:26:03 | 01:26:08 | 0:05 |
| Curated outputs, first attempt: **refused** (C43: A3 over one page, because of the extra issue line from a C30 finding on the corrected Form 4-A date) | 01:26:08 | 01:26:10 | 0:02 |
| **Live fix 4:** C30 counts a form field printing the current anchor date as covered; A3 condensation ladder | 01:26:10 | 01:28:09 | 1:59 |
| Curated outputs published: ADD-03 APPLIED, structural checks pass, C46/C30 clean | 01:28:09 | 01:28:21 | 0:12 |
| Live fix 4's tests; the condensation test corrected | 01:28:21 | 01:29:25 | 1:04 |
| `diff`, `check-register` (0 findings), `show ADD-03-8.1-01` | 01:29:25 | 01:29:30 | 0:05 |
| **Total, receipt to replanned outputs and `diff`** | **01:17:17** | **01:29:30** | **12:13** |

The curator was the assistant, so the time a person needs to review the result is NOT included. Every row and op remains PROPOSED.

## Scored against the key

Legend: **hit** (what the key requires), **partial**, **miss**. The sealed key's own wording is in `SEALED/expected_findings.yaml`.

### Dates (planning date 5 Nov 2026)

| Item | Key | System (blind) | Result |
|---|---|---|---|
| Proposal Due Date | 10 Dec 2026 14:00 | 10 Dec 2026 (via VOL-I 6.1 → ADD-01 2.1 → ADD-03 2.1, with the chain claimed and verified) | hit |
| Clarification cut-off | Thu 19 Nov 2026 14:00 (15 WD back, stated date not counted) | 2026-11-19; the 14:00 wording from 3.2 is in the row | hit |
| Bid Bond validity | 8 Jun 2027 (alt. 7 Jun) | 2027-06-08 (both readings shown) | hit |
| Proposal validity | 9 May 2027 (alt. 8 May) | 2027-05-09 (both readings shown) | hit |
| Reference-plant look-back | COD on/after 10 Dec 2016 | Both readings computed; planning uses the conservative one, 11 Dec 2016 (boundary excluded) | partial: the convention differs and is stated |
| ISO current at | 10 Dec 2026 | 2026-12-10 | hit |
| Financial Close long-stop | PBN + 300 days, no calendar date | 300 days; no date computed (PBN external) | hit |
| Scope trap: 10 WD in VOL-I 12.3 and VOL-V 29.4 unchanged | must not change | confirmed by an `expect` op; both unchanged | hit |

### Provisions

| Provision | Key | System (blind) | Result |
|---|---|---|---|
| Cover | summary not exhaustive; acknowledgement extended to ADD-03 | change list taken from the body (C20 covers all 29 provisions); acknowledgement row extended. The summary's omissions are not reported (C28 not built) | partial |
| 1.1, 1.2 | no effect | no effect, with reasons | hit |
| 2.1 | chain amendment | `replace_text` with an ADD-01 2.1 claim, verified | hit |
| 2.2 | ADD-01 2.2 re-anchoring applies | interprets ADD-01 2.2; every PDD-anchored date recomputed; dependent rows STALE | hit |
| 2.3 | correct the ADD-01 App A date to 10 Dec | `replace_text` (after live fix 3); the C31 conflict cleared | hit |
| 3.1 / 3.2 | 5.2 only; 14:00 added | both; scope confirmed | hit |
| 4.1 | SAR 6m; **no consequence added** | amended; no consequence; not on A3 | hit |
| 5.1 | only the hard copies go | whole first sentence replaced with the quoted text; physical copies A 108 → 27, B 16 → 4 | hit |
| 6.1 | fn12 60,000; rest unchanged | amended (after live fix 1); the unchanged parts confirmed; VOL-I 8.8 untouched | hit |
| 7.1 | 30%; consequence kept | amended; consequence kept; A3 line shows 30% | hit |
| 8.1 | new rejection row on A3 | new row ADD-03-8.1-01 (rejection) on A3 | hit |
| 8.2 | renumbering; lineage kept; A3 cites 10.6; ADD-02 Q14 re-pointed | lineage kept (annotation; ids unchanged). A3 still cites "VOL-I 10.5"; Q14 not flagged | **miss** (outputs) |
| 9.1 / 9.2 | 300 days; ADD-02 Q13 superseded | both (Q13 revoked, after live fix 3) | hit |
| 10.1 | TSS 15 mg/l; single-sample basis; old values from the image; ramp-up relief lost (VOL-V 29.3) | both cells set (after live fix 2); old values from the image; flagged as an image-read value change; VOL-V-29.3-01 STALE for a person (not interpreted) | partial |
| 11.1 / 11.2 | 9,000 in row 2-6.2; Section 5 main also depends | row and cell (after live fix 2); new row for 11.2; VOL-II-5.2-01 (the main) STALE through the table dependency | hit |
| 12.1 / 12.2 | new non-responsive requirement; on A3 AND on the "could not resolve" list (English vs Arabic) | new row VOL-IV-F4C-06 (non-responsive via VOL-I 9.4) on A3; I-BLIND-F4C-LANG on A3's unresolved list | hit |
| Q15, Q18, Q19, Q20 | restate | confirms annotations | hit |
| Q16 | changes VOL-II 6.1 (inside an answer); 8.3 unchanged | `replace_text` on VOL-II 6.1; 8.3 untouched | hit |
| Q17 | new restriction; fn12 line gains it | new row (lesser consequence: disregarded), with a note linking it to the fn12 rejection; the A3 fn12 line does not show it | partial |

### A3 ("what puts the bid out")

| Key | System (blind) | Result |
|---|---|---|
| Add: VOL-I 10.5 cap → rejected | added | hit |
| Amend fn12: 60,000 / COD window / own projects | quote shows 60,000. **The row's summary still reads "80,000"** (defect). COD date and Q17 not on the line | **miss** |
| Amend 8.6: 30% | shown | hit |
| Amend 6.1/6.6: 10 Dec 14:00 | shown | hit |
| Form 4-C sixth declaration, also unresolved | both | hit |
| Renumber: conditional price now 10.6 | still "VOL-I 10.5" | miss |
| Must NOT add: bond, hard copies, TSS/Table 2-6/control room, late clarifications | none added | hit |

### Programme

| Key | System (blind) | Result |
|---|---|---|
| Clarifications by 19 Nov 14:00 | clarifications activity moved (latest start 18 Nov) | hit |
| No specific activity for the Form 4-C clarification | issue on A3 only | partial |
| Bond SAR 6m, validity ≥ 8 Jun 2027; references; LCC; Form 4-C re-execution; price ceiling; TSS; hydraulics; control room staffing; Form 4-A; marshalling (no hard copies); ISO | REWORK / MOVED on the bond, references, completion certificates, Form 4-B/4-C/4-F, Form 4-A, Technical Proposal, copies and delivery; marshalling 108 → 27 copies | hit |

### Earlier answers

- **Hits:** ADD-02 Q13 superseded; Q8 and Q11 listed for review (Q11 quotes the replaced 7,500).
- **Miss:** ADD-02 Q14 (renumbered clause) not flagged.

### Pre-existing issues (credit, no penalty)

- **Flagged:** Form 4-A omissions, Form 4-G lettering, storm flow vs peak flow, concession start, Volume III.
- **Not flagged as a live conflict:** VOL-IV's own Form 4-A date. It is superseded by ADD-01 App A, which is correct.

## Summary

- **Of the 21 numbered provisions and 6 answers:** 22 hits, 4 partials and 1 miss (8.2 renumbering).
- **On A3:** the footnote-12 line is the significant miss. The row's stage-neutral summary kept a figure the addendum changed, so the page showed "80,000" next to the quoted "60,000". The A3 page itself was otherwise correct, with nothing added that must not be.
- **Live fixes:** four, each with tests, all generic: no outcome of this addendum is hardcoded.
- **The refusal** (A3 over one page, caused by the issue line of a C30 finding) is the checks working: nothing was published until it was resolved. Once C30 was fixed the page fitted with no condensation (7.69 pt, scale 0.904, just above the 0.9 floor); the condensation ladder added in the same fix is a guard.
- **Left for a person:** 28 rows STALE at ADD-03, most of them PDD-anchored rows whose dependency moved. The curator re-made 11 interpretations; the rest are the main human cost of a live addendum.

## Fixes made after the comparison (not counted above)

See the session 06 work log, §6, for the code. Each fix has a test.

1. A requirement summary that states a figure the effective text no longer contains is flagged (A1, A3, `check-register`, release blocker). It is not silently rewritten.
2. Renumbering is an op effect (`renumbers`). Outputs cite the current number, with the issued one in brackets; answers citing a renumbered clause are listed for review.
3. A3 lines show clarifications that add to or narrow a row's units (e.g. Q17 on footnote 12).
4. **Session 07, C28 (cover summary vs provisions):** the summary's omissions are now reported: 2.3, 3.2, 8.2, 9.2, the change inside the answer to Q16 and the restriction in Q17, which are the key's six. The scored "Cover: partial" stays as it was. C28 was written after the key was opened, so this is a regression, not a blind result (`tests/test_session07_summary.py`).
