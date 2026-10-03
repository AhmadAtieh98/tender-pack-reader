# Session 06: second code review, the accept workflow, live commands, blind rehearsal, draft archive

- **Date:** 3 Oct 2026, 00:42–01:54 and from 05:41 UTC (03:42 Riyadh), with a pause at a usage limit.
- **Who:**
  - **The owner:** reviewed session 05 and set Stages 3 and 4 as the working basis. The four findings below are the owner's.
  - **The assistant** (Claude Code, in the cloud container): orchestrator. It reproduces, writes the failing tests, makes the fixes, builds the commands, runs the rehearsal and assembles the archive.
  - **An independent subagent:** writes the blind Addendum No. 3 from the sources and the brief only. It never sees the implementation, the curation, the tests or the work log, and its answer key stays sealed until the rehearsal is done (§6).
- **Approvals:** the owner's approvals are still pending. Nothing is approved, accepted or refreshed on the owner's behalf.

## 1. The exchange (verbatim)

**Owner.** Message text as received:

~~~~text
good progress , let’s use stages 3 and 4 as the working basis and push toward the live session and a complete draft handover. my approvals are still pending.


i found a few things to fix first:

* in `amend.py`, adding “all tender requirements are waived” after the legitimate form 4-g insertion still passes the full output checks. inserted content needs evidence for the whole change, not just a supported quotation somewhere inside it.
* in `draft.py`, “all other terms remain unchanged except that each bidder shall submit a certificate of good standing” gets discarded as harmless wording. the exception disappears while the addendum shows applied.
* in `dispositions.py`, removing drill b’s good-standing row leaves no coverage warning and its disqualifier disappears from a3. accounting for an amendment operation doesn’t prove its requirements reached the register. check new and amended obligations through a1, a3 where applicable, and a5.
* `stage2.release_blockers` accepts rows and operations marked accepted without a reviewer. also, a3’s compact rendering removes individual confidence and cuts off the lcc’s 35% threshold. keep both visible on the actual page, and replace the old “stage 2 slice” labels with accurate status.

reproduce these with failing regressions first, then fix the underlying rules. challenge anything you disagree with using evidence, then keep moving 

build the named `accept` workflow you recommended, with rejection and review notes. bind each decision to the actual row or operation, its evidence and dependencies; changed content must require review again. a status flag alone isn’t approval. prepare proposed updates for the three stale rows, but don’t accept or refresh anything for me. give me manageable review batches, starting with the images, disqualfiers and amendments, with crops beside readings and exact decisions needed.

finish the live commands:,`show` should take an a1 row id and show its source pages, crops and amendment chain. `diff` should explain changed requirements, stale readings and programmme impact. close the remaining stable id and date coverage gaps; unsupported periods must stay explicitly unresolved

run a genuinely blind addendum rehearsal. have an independent agent prepare it from the sources and brief, without seeing the implementation, and freeze its expected findings before you start. use the normal workflow, including curation and replaning. measure the whole exercise

prepare a draft archive organised around a1–a5, including excel, the readable one-page a3, and the repository with real history for a4. test extraction, links and rebuilding in a fresh location. verify offline operation where possible and give me exact mac commands for anything you cannot test. include a short operating guide and an honest cost/effort breakdown. keep claude code app / openrouter / ollama integrations deferred.
keep the work log accurate . 
come back with the draft package, a compact results report and the decisions you need from me. pending review should stay visible while you finish the independent work.
~~~~

## 2. Timeline

Times are UTC, taken from the timestamps of the session's own tool calls (checked against the transcript at 01:48, after the first version of this table was found to be written from memory: E72). The blind rehearsal's own clock is in `rehearsals/blind-01/clock.txt`.

| UTC | Step |
|---|---|
| 00:42 | Session start. 00:43: blind-addendum author started (background subagent, §6.1). |
| 00:43–00:46 | Read the code paths named in the four findings. |
| 00:46 | Reproduction script (`s06/repro.py`, session scratchpad) on `3c97a8d`: all four findings confirmed (§3). |
| 00:48 | Failing tests first: `tests/test_session06_review.py`, 16 tests: **12 failed, 4 passed** (the 4 are controls) (§3). |
| 00:48–00:50 | Fixes for findings 1 and 2 (`amend.py`, `draft.py`) (§4.1, §4.2). |
| 00:53 | Finding 3: obligation trace (`trace.py`, C46) (§4.3). |
| 00:55–01:00 | Finding 4: `review.py` and the release gate; A3 confidence and full text; A3 fit; "slice" labels (§4.4). |
| 01:01–01:02 | Drill B fixture: `updates-ADD-03.yaml` (re-made interpretations), `rehearse.py`, tests. |
| 01:04–01:05 | Stale-row proposals (`proposals.py`, `curation/register/proposals/`), `tests/test_session06_accept.py` (§5). |
| 01:05 | Blind author finished (22 min). Sealed files checked against their own SHA256SUMS and write-protected, not opened. The PDF and the hash commitment frozen in `53ad76f`, pushed 01:05:50. |
| 01:06–01:08 | `live.py`: `show ROW` and `diff` (§5.4). |
| 01:08–01:11 | Dates: month and week units, the `unresolved` kind, `date_notes`; `datecover.py` (C30, C32); row-id ledger (C12) (§5.5). |
| 01:11–01:16 | Suites; the session 05 gate test moved to bound decisions (E55); `tests/test_session06_live.py`. |
| **01:17:17–01:29:30** | **Blind rehearsal, receipt to replanned outputs and `diff`: 12 min 13 s** (§6). |
| 01:29:49 | Sealed key opened, after the blind results were on disk. 01:31: `COMPARISON.md`. |
| 01:31–01:35 | Post-comparison fixes (renumbering, summary currency, A3 pointers) with tests; blind `out-after-fixes/` (§6.5). |
| 01:35–01:37 | Review batches (`batches.py`); pages rendered with headless Chromium and looked at; test (§5.3). |
| 01:37–01:40 | `make outputs`; drills; the full suite started at 01:40 (339 passed, 6 min 14 s). |
| 01:40–01:45 | Wheelhouses for macOS and Linux; offline namespace check; operating guide; cost and effort; archive scripts (§7). |
| 01:47–01:54 | Full suite: 339 passed. Blind timings and information boundary checked against the transcript (§6.1); determinism (§9); drills regenerated; this log. |
| 01:54–05:41 | **Paused:** the owner's usage limit was reached; work resumed when it reset (3 h 47 min, not counted as work). |
| 05:41–05:50 | Work log, comparison timeline completed, README, plan revision 6, session report, `scripts/verify_archive.py`. |

## 3. Reproduction on commit 3c97a8d (before any fix)

`s06/repro.py` (session scratchpad) ran each finding against the committed code. Output, abridged:

```
== 1  insert_unit: 'all tender requirements are waived' added to the Form 4-G insertion (ADD-02/7.1)
   op valid: True | stage: APPLIED | build exit: 0 ok
   inserted unit: Form 4-G — Cybersecurity Compliance Undertaking; all tender requirements are waived
   structural checks failed: []
== 2  draft: 'All other terms remain unchanged except that each bidder shall submit a certificate of good standing.'
   ops: [('ADD-09/2.1', 'replace_text', 'VOL-I:9.2')] | dispositions for 2.1: []
   stage status: APPLIED | coverage of 2.1: op
   same words in a cover paragraph: [('ADD-09:cover/para2', 'no_effect', 'recital or cover text; changes nothing by itself')]
== 3  drill B: remove the good-standing row (ADD-03-3.1-01)
   with the row:   in A3 explicit: True
   without it: ADD-03 status: APPLIED | coverage of ADD-03:3.1: op
   A3 mentions good standing: False | release blockers of kind coverage: [] | check-register findings: 0
== 4a release gate: rows and ops marked accepted with no reviewer
   approval blockers after flags only: ["image readings pending the owner's review: VOL-II-p3-r1, VOL-IV-p6-r1"]
== 4b A3 page: LCC line and confidence
   '35' on the LCC line: False | 'confidence' anywhere on the page: False
== 4c 'slice' labels in the outputs
   out/README.md: '| A1 register slice, ...' ; out/a1/a1.json: "Outside slice"
```

All four findings were confirmed as stated. None was disputed. One clarification on finding 3: `dispositions.py` does what it claims, which is to account for every provision. The gap was that nothing went on from an op to the rows, A3 and A5. The fix is therefore a new trace (`trace.py`), not a change to the dispositions.

**Failing tests first** (`tests/test_session06_review.py`, 00:48): 12 failed, 4 passed. The 12:

1. `test_inserted_words_the_addendum_does_not_print_make_the_op_invalid`
2. `test_inserted_text_must_come_from_the_addendum_itself`
3. `test_full_outputs_refuse_a_change_whose_words_no_addendum_prints`
4. `test_an_exception_after_unchanged_wording_is_unresolved`
5. `test_cover_text_with_an_obligation_is_not_no_effect`
6. `test_with_its_row_the_new_obligation_is_traced`
7. `test_an_obligation_no_row_holds_is_a_visible_coverage_failure`
8. `test_an_obligation_without_a_deliverable_is_an_a5_gap`
9. `test_the_real_pack_obligations_are_all_traced`
10. `test_status_flags_alone_are_not_acceptance`
11. `test_a3_page_keeps_the_lcc_threshold_and_every_items_confidence`
12. `test_no_stage_2_slice_labels_remain`

The 4 that passed are controls: legitimate changes that must keep working.

## 4. Fixes

### 4.1 Finding 1, `amend.py`: inserted content needs evidence for the whole change

- **`insert_unit` (C21):**
  - `new_text_from` must be a unit of the addendum itself.
  - The **whole** inserted text must be printed in that addendum: in the provision, a content unit, or `new_text_from`. A supported quotation somewhere inside it is no longer enough. The op records where it found the text (`details["evidence"]`).
- **New structural check C47 (`unevidenced_additions`):** a difflib comparison of each unit before and after each stage. Every word a unit gains must be printed in that stage's addendum. This catches an unprinted addition by any op type, not only `insert_unit`. A failure stops publication (exit 2).
- **`set_value`:** a unit of measure is required only for numeric values. Text cells must quote the addendum (needed in the blind rehearsal, §6.3).

### 4.2 Finding 2, `draft.py`: an exception is never harmless wording

- `_BENIGN_WHOLE` matches a sentence only as a **whole** ("… remain unchanged", "this addendum forms part of …"). The old filler patterns matched a prefix and dropped the rest.
- `_remainder` computes what is left once the typed spans are taken out. A remainder with a qualifier ("except", "save that", "provided that", "subject to") or change words makes the provision **unresolved**, for a person.
- Cover and recital paragraphs follow the same rule: they are `no_effect` only when the whole remainder is benign.

### 4.3 Finding 3: new and amended obligations traced through A1, A3 and A5 (C46)

- **`trace.py`:** `obligation_trace` takes every op that adds or amends content and checks three things for each obligation:
  - the affected units are held by a register row in force at that stage (A1);
  - when the provision carries consequence words, that row is on A3 with the quoted consequence;
  - the row reaches an A5 activity or deliverable.
- **Where a finding shows:**
  - C46, reported per stage;
  - a release blocker of kind `coverage`;
  - an A3 issue `I-AUTO-UNTRACED-<stage>`;
  - `check-register`.
- **Drill B with the good-standing row removed:** C46 names `ADD-03:3.1`, A3 shows the untraced issue, and `outputs --strict` refuses.
- **Real pack:** C46 clean.

### 4.4 Finding 4: the release gate, A3 and the labels

- **Release gate:** acceptance now comes only from decisions recorded with `tenderpack accept`, each bound to the item's current content (§5). The `review:` flags in the YAML files are drafting flags and never count.
- **A3 page:**
  - every item shows its confidence;
  - the requirement is shown in full;
  - when the requirement's figures are not in its text, the current quote is appended. The LCC line now reads "… — 'not less than thirty-five per cent (35%) for the construction phase'";
  - to keep it on one page, the line height went to 1.16 and the margins to 26/20 pt. Issues use their own short `a3:` summaries, with the full text in `a3_detail.html`;
  - a condensation ladder applies only if needed: level 1 shows the issue ids with their owners, level 2 counts the no-consequence ids. Each level is stated on the page, and no disqualifier is ever dropped;
  - real pack: smallest text 7.91 pt (scale 0.931), no condensation.
- **Labels:**
  - every "slice" label is gone from the code and the outputs;
  - A1 is titled "A1 Obligations and compliance register — WORKING DRAFT", with a notice of its review counts;
  - A2 is titled "A2 Addendum reconciliation — WORKING DRAFT";
  - the status line reads "WORKING DRAFT (not releasable)".

## 5. Accept workflow, proposals, review batches, live commands, coverage

### 5.1 `tenderpack accept` / `reject` (`review.py`)

- **Usage:** `accept ITEM... --reviewer NAME [--note ...]` and `reject ITEM... --reviewer NAME --note ...` (a rejection needs a note).
- **Items:** register rows (`VOL-I-8.6-01`) and amendment ops (`ADD-02/9.1`).
- **The decisions file** is `curation/reviews/decisions.yaml`. It is append-only and **was not created**: only the owner creates it, by deciding.
- **What a decision is bound to:** a SHA-256 fingerprint of a canonical binding.
  - **A row:** its content (excluding the drafting flags), its evidence items' definitions, and its state at each stage (in force, the dependency pin values).
  - **An op:** the op, its provision's text and pages, the pin values before it, and its content.
- **Status of an item:** `accepted`, `rejected`, `changed` (decided, but the content has changed since), `proposed`, or `flag_only` (a YAML flag with no decision; it does not count). The latest decision per item applies.
- **What `accept` refuses** (it writes nothing unless every item passes):
  - a placeholder reviewer;
  - a rejection without a note;
  - an evidence build with problems;
  - an unknown item;
  - a STALE row, or a row with quote problems;
  - an invalid op.
- **A current rejection of an op** makes the engine rerun without it. Its addendum becomes PARTIAL and the validated state stays on the previous addendum.
- **Outputs:**
  - A1 shows each row's review status and its ops' statuses;
  - the release gate counts only `accepted`;
  - `outputs --strict` lists every other status.
- **Tests:** 7 workflow tests (`tests/test_session06_accept.py`), all in disposable fixture copies with the reviewer name "Fixture Test Reviewer". They cover:
  - a flag is not a decision;
  - a decision on changed content becomes `changed`;
  - a rejected op makes its addendum PARTIAL;
  - the refusals;
  - nothing is written on a partial failure.

### 5.2 Proposed updates for the three STALE rows (prepared, not applied)

- **File:** `curation/register/proposals/2026-10-03_stale-rows.yaml`.
- **The proposals:** P-STALE-VOL-I-8.3-01, P-STALE-VOL-I-3.4-01 and P-STALE-VOL-I-6.7-01. Each gives:
  - the new stage-specific interpretation;
  - its quote in the current text;
  - the dependency that changed;
  - why the reading is the same or different.
- **`tenderpack apply-proposal P-… --by NAME`** inserts the interpretation (marked "[Applied from proposal … by … on …]") and pins only that `ROW@STAGE`. It does **not** accept the row; that remains a separate `accept`.
- **Not applied:** none has been applied, and the three rows stay STALE (a release blocker).

### 5.3 Review batches (`out/review/`, `batches.py`)

`out/review/index.html` lists 244 items in 9 batches. Each batch shows what to look at, the crops beside the readings or quotes, and the exact command for each decision.

| Batch | Items | Content |
|---|---|---|
| 1 | 2 | The image readings: every read cell beside its crop (Table 2-4, 12 units; Form 4-C, 28 units) |
| 2 | 19 | Rows with an explicit consequence (A3), with the amending provisions' crops |
| 3 | 37 | Amendment ops: provision, target, old → new, crops |
| 4 | 3 | The STALE-row proposals |
| 5–9 | 183 | The remaining rows, 40 per batch |

- **Size:** 110 images, 4.1 MB.
- **Status file:** `items.csv`/`items.json` give the status of every item.

### 5.4 Live commands (`live.py`)

- **`show ROW [--to DIR]`:**
  - prints the row's requirement and its status at each stage;
  - its source pages and the amendment chain (each op, with provision and page);
  - annotations (clarifications that confirm or narrow);
  - its A5 activities;
  - writes `show/<ROW>/index.html` with the page crops (red boxes on the units) and the reading crops.
- **`diff [--from STAGE] [--to STAGE] [--md FILE]`:**
  - addendum status;
  - requirements that are new, no longer in force or changed (with date moves);
  - STALE rows and voided decisions;
  - image-read value changes;
  - C46;
  - what enters, leaves or changes on A3;
  - programme deltas, feasibility and envelope copy totals.

### 5.5 Stable ids and date coverage

- **C12, row-id ledger** (`curation/register/ids.yaml`, 202 ids):
  - every id ever issued must be present, or withdrawn with a reason (structural);
  - new ids are reported until recorded with `check-register --update-ids`.
- **C30, date coverage** (`datecover.py`). Every date or period phrase in force must have a treatment:
  - a row's date rule;
  - printed and checked (C31);
  - a form field printing the current anchor date;
  - the anchor's own definition;
  - a stated duration (not event-relative);
  - a disposition;
  - a `date_notes` entry (duration, post-award, not a date, **unresolved**).

  Anything else is UNCOVERED. That is a release blocker and an A3 issue (`I-AUTO-DATES`).
- **Unsupported periods stay unresolved:**
  - date rule kind `unresolved` (with the text and a note) gives the interpretation `unresolved`, with no value;
  - a `date_notes` treatment `unresolved` keeps the phrase visible;
  - neither is ever computed.
- **Months and weeks are now exact:** VOL-V ramp-up 12 months and scheduled PCOD 36 months. Before, these were years; the text says months.
- **C32:** counting conventions the pack does not state are reported. Every reading is shown in A1 Dates.
- **Real pack:** 46 date/period phrases in force; none uncovered; none explicitly not computed. 5 rules have unstated counting conventions.

## 6. Blind addendum rehearsal

### 6.1 How it was kept blind, and the limits of that

- **The author:** an independent subagent, given a written brief. It was allowed to read only:
  - the six tender-pack PDFs;
  - the assignment brief;
  - the hiring team's reply.

  It was barred from the code, curation, tests, docs, work logs, outputs and git history. It reported 302,136 tokens and 42 tool uses over 22 min (00:43–01:05).
- **What the orchestrator learned before the rehearsal:** only the file hashes, the page count (3), the printed issue date (5 November 2026) and the author's elapsed time. The transcript confirms that its final message said nothing else.
- **The freeze:** the PDF and the hashes of the sealed answer key, author notes and builder script were committed in `53ad76f` and pushed at 01:05:50. The sealed folder was write-protected and not opened until 01:29:49. By then the drafted and curated outputs and the `diff` were on disk.
- **Limits:**
  - **The brief named the kinds of change** the addendum had to contain: a date chain, a period in Working Days, a text-table cell, an image-only value, a deletion, an insertion with a consequence, a scope trap, a substantive Q&A answer and a restating one, one genuine ambiguity, and two change types not used in ADD-01/02, chosen by the author from an example list that included renumbering. So the curator knew the categories, but not which provisions or values.
  - **The curator was the assistant**, which also wrote the code. A person curating would take longer, and the timing excludes the owner's review.
  - **There was one blind addendum**, written by one author.

### 6.2 Timeline

From `rehearsals/blind-01/clock.txt`, confirmed against the transcript:

| Step | Elapsed |
|---|---|
| Set up the pack (received PDF, copies of the curation) | 0:05 |
| Ingest, Stage 1: 7 documents, 569 units; C01–C10 pass first time | 0:13 |
| Draft (6 ops; 23 provisions unresolved); read every ADD-03 unit | 1:37 |
| Live fix 1 (drafter phrasings); tests | 0:36 |
| Re-draft (10 ops; 19 for a person); drafted working draft published (PARTIAL; validated state stays ADD-02) | 0:18 |
| Reading the engine's handling of chained amendments (no clock entry) | 1:29 |
| Live fix 2 (text-cell `set_value`; `replace_text` on a table row updates the cell); tests | 1:21 |
| Checking the re-drafted state (no clock entry) | 0:59 |
| Curation of the op file: 28 ops, 4 dispositions | 0:44 |
| Live fix 3 (four citation forms); tests | 0:10 |
| Rows (4 new, 11 interpretations re-made, 1 extended), 4 issues; replanning (hard copies 3 → 0) | 1:02 |
| Pin the new interpretations; record new ids (`--update-ids`) | 0:05 |
| Curated outputs, first attempt **refused** (exit 2): C43, A3 over one page | 0:02 |
| Live fix 4: C30 treats a form field printing the current anchor date as covered; A3 condensation ladder; tests | 1:59 |
| Curated outputs published: ADD-03 APPLIED; structural checks pass; C30 and C46 clean | 0:12 |
| Live fix 4's condensation test run and corrected (E65) | 1:04 |
| `diff`, `check-register` (0 findings), `show ADD-03-8.1-01` | 0:05 |
| **Total** (the rows sum to 12:01; the other 12 s are gaps between commands) | **12:13** |

- **The refusal:** C43 refused the first curated output because A3 did not fit one page (21 items, 12 unresolved). The extra line was the `I-AUTO-DATES` issue from a C30 finding: ADD-01 App A's Proposal Due Date field, which ADD-03 2.3 corrects to the current date.
- **After live fix 4:** the C30 fix removed that line and the page fitted with no condensation (7.69 pt, scale 0.904). The ladder added in the same fix is a guard, not needed for this page.
- **Headroom:** small. The scale is 0.904 against a floor of 0.9.

### 6.3 Live fixes

All four are generic: no outcome of this addendum is hardcoded. Each has tests in `tests/test_session06_review.py`.

1. **Drafter phrasings:**
   - citations qualified by "as amended/reinstated/corrected by …";
   - "is further amended by deleting";
   - "In footnote N to Volume X Clause Y, 'Q' is deleted …";
   - "The following new Clause N is inserted in Volume X after Clause M".
2. **Tables:**
   - `set_value` on a text cell (no unit; must quote the addendum);
   - `replace_text` on a table row also updates the one cell that holds the old words.
3. **Citation forms:**
   - "Appendix A to Addendum No. 1";
   - "clarification request 13 in Addendum No. 2";
   - "the fifth numbered declaration";
   - "in row 2-6.2".
4. **Dates and A3:**
   - C30 counts a form field that prints the current anchor date as covered;
   - the A3 condensation ladder (§4.4).

### 6.4 Results

Scored against the sealed key in `rehearsals/blind-01/COMPARISON.md`:

- **Provisions and answers:** 22 hits, 4 partials, 1 miss.
  - **The miss:** 8.2 renumbering. Lineage was kept, but A3 cited "VOL-I 10.5" and ADD-02 Q14 was not flagged.
  - **The partials:**
    - the cover's non-exhaustive summary was not reported (C28 not built);
    - the reference-plant look-back convention differs from the key's, and is stated;
    - the ramp-up relief in VOL-V 29.3 was left STALE for a person rather than interpreted;
    - the Q17 restriction is on its own row, not on the footnote-12 A3 line.
- **A3:**
  - the footnote-12 line showed the row's old summary "80,000" next to the quoted "60,000". The row's stage-neutral summary kept a figure the addendum changed;
  - the renumbered clause was cited by its old number;
  - otherwise correct, and nothing was added that the key says must not be.
- **Replanning:** Envelope A physical copies 108 → 27, Envelope B 16 → 4; the clarification activity moved to the 19 Nov cut-off; two new disqualifiers on A3.
- **After curation:** 28 rows were STALE at ADD-03. Most of them are PDD-anchored rows whose dependency pin moved. The curator re-made 11 interpretations in the 12 minutes; the rest wait for a person. This is the main human cost of a live addendum.

### 6.5 Fixes after the comparison (not counted in the score)

Each fix has a test in `tests/test_session06_live.py`.

1. **Summary currency:** a requirement summary that states a figure the effective text no longer contains is flagged. The flag shows in:
   - A1 (`SUMMARY OUT OF DATE`);
   - A3;
   - `check-register`;
   - a release blocker.

   The summary is never silently rewritten. Drill B's curated output now shows one such finding (VOL-I-7.1-01: "150" days, which drill B's ADD-03 changes to 180). That row is also STALE there, deliberately left for a person.
2. **Renumbering** is an annotation effect (`renumbers`, with `renumber: {unit: number}`). C21 checks that the new numbers are printed.
   - Outputs cite the current number with the issued one in brackets: "VOL-I 10.6 (issued as 10.5)".
   - Answers that cite a renumbered clause are listed for review in A2.
3. **A3 pointers:** an A3 line shows the clarifications that add to or narrow its row's units (e.g. "see ADD-03/Q17" on footnote 12).

**Re-run:** `out-after-fixes/` is the same curated pack after these fixes. A3 cites "VOL-I 10.6 (issued as 10.5)" and the fn12 summary is flagged.

## 7. Draft archive and offline verification

(§7 is completed after the archive is built and verified; see below.)

## 8. Errors in this session (continuing from E50)

| # | Error | Found by | Fix |
|---|---|---|---|
| E51 | A3 overflowed after the full requirement text was added (scale 0.871) | Rendering | Line height, margins, `a3:` issue summaries; later the condensation ladder |
| E52 | Drill B's A3 overflowed: its copied issues had no `a3:` summaries | Drill B run | Fixed when the rehearsal fixture was regenerated |
| E53 | An f-string with nested double quotes (a Python 3.11 syntax error) in `stage2.py` | Import | Single quotes inside |
| E54 | An `ops` line duplicated in `register.py` by a `sed` edit | Reading the diff | Removed |
| E55 | The session 05 gate test simulated acceptance with YAML flags | The new gate | Test changed to bound decisions, intended |
| E56 | C30 counted "ten (10) Working Days before the PDD" as a plain duration | First C30 run | Event-relative periods excluded from the duration route |
| E57 | `parse_date` returns a tuple; C30 compared it with a date | Test | `_parse` takes the first element |
| E58 | C30 left the corrected Form 4-A date uncovered (blind) | Blind run, refusal | Live fix 4 |
| E59 | C30: a drill B rule declared on the provision, not on the inserted unit | Drill B | Rules match any unit the row holds |
| E60 | The drafter's qualifier group swallowed the comma | Live fix 1 test | Comma moved outside the group |
| E61 | A synthetic footnote test expected the unnormalised "m³" | Test | Expects "m3/day", as normalised |
| E62 | Blind curation: YAML flow mappings with commas failed to load | Loading | Values quoted |
| E63 | Blind: C22 failed on three citation forms (2.3, 9.2, 12.1) | Blind run | Live fix 3 |
| E64 | Blind: `set_value` on a text cell failed the unit check; `replace_text` on a row left its cell stale; "row 2-6.2" not recognised | Blind run | Live fix 2 |
| E65 | The condensation test failed on ids wrapped across lines | Test | Hyphen-wrap joined before comparing |
| E66 | The A2 title still said "Stage 2 first connected version" | Label sweep | Fixed |
| E67 | `source_of` used the BASE state, so renumbering was invisible | Post-comparison | The wrapper rewrites with the current number |
| E68 | Drill B's `prepare()` had no `row_ids` path: `--update-ids` could have written to the real ledger | Reading the code before running it | `row_ids` and `decisions` set in the fixture config |
| E69 | Review batch 1 listed cells alphabetically; batch 2 lacked the amending provisions' crops | Screenshots | Table column order; chain provisions added |
| E70 | `pip download` evaluated markers with the wrong interpreter; an old macOS x86 tag found nothing | Wheelhouse | `uvx --python <ver>`; `macosx_14_0_x86_64` |
| E71 | COST_AND_EFFORT guessed the reading unit counts | Checking against `units.json` | Corrected to 12 and 28 |
| E72 | The first rows of this log's timeline were written from memory (e.g. "00:52" for the failing tests, really 00:48) | Checking against the transcript | Table rebuilt from the tool-call timestamps |

## 9. Results

- **Tests:** **339 passed** in 374 s (`pytest -q`, 01:40–01:46 UTC), up from 289. The 50 new tests:

  | File | Tests |
  |---|---|
  | `test_session06_review.py` | 27: the 16 failing-first tests and controls, plus live-fix, table, citation and A3-condensation tests |
  | `test_session06_accept.py` | 8 |
  | `test_session06_live.py` | 14 |
  | `test_drill_b.py` | 1 (the obligation trace) |

- **Determinism:**
  - Stage 1 was rebuilt twice in disposable folders: identical manifests, both equal to `build/`;
  - the outputs were rebuilt twice: identical, and identical to the committed `out/` (`diff -r`).
- **Real pack:** structural checks pass. C20/C21–C27 (both addenda), C30, C32 and C46 are clean; C11 reports the 3 STALE rows.
  - A3: 18 explicit items plus 1 score elimination; 7.91 pt, no condensation.
  - Release blockers: the 3 STALE rows, the 2 readings, 202 rows and 37 ops without a decision.
- **Drills:** each is a WORKING DRAFT, with every row and op `proposed`.
  - **Drill A, drafted:** C20/C21 and C46 report what the uncurated draft leaves (expected).
  - **Drill B, curated:** ADD-03 APPLIED; 9 STALE rows; one summary finding.
  - **Blind, curated:** ADD-03 APPLIED; 28 STALE rows.
