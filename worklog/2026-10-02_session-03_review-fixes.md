# Session 03: owner's Stage 1 review, reproduction and fixes

- **Date:** 1 Oct 2026, 22:59 UTC, to 2 Oct 2026, about 01:10 UTC (01:59–04:10 Riyadh, 2 Oct).
- **Who:**
  - The owner reviewed the Stage 1 work and tests.
  - The findings below are the owner's.
  - Reproduction, fixes, tests and this log were done by the coding assistant (Claude Code, in the cloud container).
- **Scope:**
  - Reproduce the six gaps, fix what was confirmed, and show the evidence.
  - Make the plan consistent and report back.
  - Stop before Stage 2.
  - Approve nothing on the owner's behalf.

## 1. The exchanges (verbatim)

**Owner, 22:59 UTC.** Message text as received:

~~~~text
good progress , but not ready to accept stage 1 yet. i went through the work and tests, and i found these potential gaps need another look.
reproduce them first, then fix what’s confirmed. if you think i’m wrong, tell me why and show the evidence.

1. vol-i §3.3 gets split after “under section”, turning “5. a bidder...” into a separate item. unrelated tables also get merged across pages just because their columns match, despite intervening text and headings. fix the boundary logic without hardcoding these examples, and keep genuine numbering and table continuations working.
2. duplicate clause ids and span anchors can still leave the checks passing and ingestion returning success. structural errors should fail clearly, with a nonzero exit. pending human review is a different status. alsoo ,checking the first few letters of a unit isn’t enough to verify its full source evidence.
3. changing a source image and updating its hash can leave the old approval valid. adding an uncertainty can too. approval needs to cover the evidence, location, reading and uncertainties, with a reviewer identified. changed evidence must trigger review again even if the transcription stays the same. don’t approve anything on my behalf.
4. removing the tn row’s unit and assessment basis still passes validation. check required cells, unique keys and explicitly recorded blanks. `parse_limit` also assumes every single number is a maximum. keep the numerical reading separate from what the actual headings and notes mean.
5. a triangle made of straight lines disappears from image detection because those lines are treated as structural. uncertain drawings should remain visible for review. also test an arabic image table through transcription, validation and actual rendering, including mixed numerals and right to left layout. an unread bilingual fixture doesn’t prove that works.
6. reject output paths that could overwrite the repo or inputs. build in a temporary location and replace previous results only after success. test this in disposable directories.

add failing regression tests first, then show the fixes passing alongside the existing suite. keep this focused , no new framework or more glyph research.
my arabic and table approval is still pending. show the crops beside the readings, with a short list of decisions you need from me. be clear about what the checks prove and what still needs my review.
make the current plan consistent. keep a1 excel, configurable bidder assumptions and the later claude code app / openrouter / ollama options. integrations and model selection can wait.
keep the work log accurate. preserve the exchanges and record actual failures, fixes and test results. passing tests don’t equal correct interpretation or human approval.
send back a short before/after report and updated review packets. stop there , before stage 2.
~~~~

**Other exchanges in this session, in order:**

| UTC | From | Text |
|---|---|---|
| 22:59 | assistant | "I'll start by checking what changed on disk since my last commit, since several files were modified outside this session." |
| 22:59 | assistant | "The working tree is clean and matches the remote, so the "changed on disk" notices are from the container being restored, not content changes. I'll check that the environment survived." |
| 23:02 | assistant | "Nothing has changed since `79ef49c` and the environment is intact. I'll reproduce each of your six points before changing anything, starting with the §3.3 split and the cross-page table merging." |
| 23:02 | system | "You've hit your session limit · resets 12:30am (UTC)" |
| 23:27 | owner | "Continue from where you left off." |
| 23:27 | system | "You've hit your session limit · resets 12:30am (UTC)" |
| 00:31 | owner | "I hit my usage limit while you were working, but it has reset now. Please continue from where you left off." and "Continue from where you left off." |
| 00:36 | assistant | "The fixture is reworked. Next I'm writing the regression tests against the behaviour you described, before any fix, so they must fail on the current code." |
| 00:39 | system | The conversation reached its context limit and was summarised automatically; work continued from the summary. The pre-summary transcript is the source for this section. |
| 00:40–01:10 | assistant | Short progress notes only (status lines while working); the final reply is preserved verbatim in `2026-10-02_session-03_reply.md`. |

## 2. Reproduction on commit 79ef49c (before any fix)

- **How it was run:**
  - Everything ran in disposable directories under the session scratchpad. Nothing was written to the repository.
  - The final "before" run used a detached `git worktree` of `79ef49c`, also in the scratchpad.
- **1a (§3.3 split):** reproduced from the committed `build/units.json`.
  - `VOL-I:3.3` ended "…shall raise it as a request for clarification under Section".
  - `VOL-I:S3/item5` held "5. A Bidder that resolves such a conflict unilaterally…".
  - Measured from the PDF: the line "…under Section" ends at x = 532.6 pt, the right edge of the text column. The line "5. A Bidder…" follows at normal line spacing.
- **Other findings:** reproduced with `repro_before.py` (scratchpad), output verbatim:

~~~~text
== 1b unrelated tables merged across pages
  table T-01:cover/T1 pages [1, 2] rows ['1', '2', '7', '8']
== 2a duplicate clause ids -> checks / exit status
  unit ids: ['T-01:1.1', 'T-01:1.1~2']
  checks all ok: True | problems: ['T-01: duplicate unit id T-01:1.1; renamed T-01:1.1~2']
  ingest exit code would be: 0
== 2b span listed in two units' anchors
  checks all ok: True | problems: ["T-01: spans listed in more than one unit: ['T-01/p1/s001']"]
== 2c trace check only looks at the first word
  first-word check on corrupted text passes: True
== 3 approval survives evidence / uncertainty changes; no reviewer required
  approved with reviewer=None: approved
  after changing native image hash: approved
  after adding an uncertainty: approved
  after moving the bbox: approved
== 4 table cells: missing unit/basis, duplicate keys; parse_limit semantics
  TN without unit/basis + duplicate row key -> failing checks: []
  parse_limit('10') = {'max': 10.0, 'rule': "single value read as a maximum (table header: 'all values are maxima')"}
== 5 triangle of straight lines
  regions detected: []
  black box with no text (possible redaction): []
== 6 output path safety (disposable fake repo)
  out == repo root: FileNotFoundError [Errno 2] No such file or directory: '<scratch>' | precious exists: False
  previous results present before failed rebuild: True | after failed rebuild: False
~~~~

**Verdict:** all six confirmed. I found nothing to dispute. Each is a defect in my session 02 work:

- **1a.** Any line starting "N. " in plain type opened a numbered paragraph.
- **1b.** Table continuation never asked whether anything came between the two parts.
- **2.** Renamed duplicate IDs and doubly anchored spans were only "problems", not failures. My session 02 trace test checked four letters of the first word.
- **3.** The approval hash covered only content: no evidence, no uncertainties, no reviewer requirement.
- **4.** No cell validation, and `parse_limit` attached "maximum" to every single number.
- **5.** Every path made only of straight lines, and every rectangle, counted as structure.
- **6.** `ingest` called `rmtree(out)` before doing anything. A mistaken `--out` could delete the repository; in the disposable copy it did.

A first version of the script recorded **2b** and **6** wrongly (error E27). The output above is from the corrected script.

## 3. Regression tests written first: the failing run

- **Test file:** `tests/test_review_regressions.py`, 34 tests (with parameters), written at 00:37 before any fix.
- **Run:** 00:40 UTC, against the 79ef49c code. The fixture was reworked as described in §4.5.
- **Result:** `28 failed, 4 passed, 2 errors in 19.97s`.
- **The 2 errors:** the reworked fixture's readings use new schema fields (table `direction`, no table `title`), which the old models rejected.
- **The 4 passes:**
  - `test_genuine_numbered_paragraphs_still_split` and `test_genuine_split_table_still_joins` are guards that must keep passing.
  - `test_nothing_is_approved_on_the_owners_behalf` is the "no approvals file" guard.
  - `test_approve_command_refuses_placeholder_reviewer` passed **for the wrong reason** (error E30): argparse rejected the unknown option `--approvals`. The old `approve` would have accepted "<name>" and written to `curation/approvals.yaml`. I did not run it against the repository.

## 4. Fixes (none keyed to the reported examples)

### 4.1 Boundaries (`segment.py`)

- **Numbered paragraphs.** A line beginning "N. " opens a numbered paragraph only if both hold:
  - **N is in sequence:** it is 1, or one more than the previous numbered paragraph in the section.
  - **It does not carry on an unfinished sentence.** The sentence counts as unfinished when all three hold:
    - the open text does not end in `. : ; ? !`;
    - the line is close enough to continue it;
    - the previous line **wrapped**: the new line's first word would not have fitted in the room left at its end. This is the standard reflow test.
  - The wrap test was needed. Form 4-A's "To: The Northern Utilities Procurement Authority" ends without punctuation at normal spacing, yet item 1 must still start after it. That line ends at x = 254.9 pt in a 532.6 pt column.
- **List items.** A list item starts only after open text ending ":", ";", ",", " and" or " or", or "." for a previous list item.
- **Table continuation.** All of the following are required:
  - nothing (text, heading, caption, region or rotated text) came after the earlier part;
  - the table is the first item on the next page;
  - it has the same column count and column edges (within 2 pt);
  - any header row repeats the earlier header.
- **Effect on the real pack.** The only unit change was `VOL-I:3.3`, whole again, and `VOL-I:S3/item5` removed: 525 → 524 units.
  - A field-by-field diff against `79ef49c:build/units.json` found no other change to text, matching text, pages, kind or text-layer anchors.
  - The other differences are the new fields only:
    - `label_span`;
    - table `col_edges` and `direction`;
    - `subject_sha256` in reading status;
    - `cell_bbox_pt` in Table 2-4 row anchors;
    - `numeric` and `context` replacing `parsed`.

### 4.2 Structural failures (`coverage.py`, `pipeline.py`, `cli.py`)

- **New checks:**
  - C07: unique unit IDs, including reading units.
  - C08: each content span in exactly one anchor, and every anchored span exists.
  - C09: no segmentation problems.
  - C10: full evidence. Every page is re-extracted, and every text-layer unit is compared in full.
    - Flow units: the printed and matching texts must equal their spans' text character for character, apart from whitespace and excluding the label.
    - Tables, rows and form fields: the same characters as their spans, and each cell must appear in the row text.
- **C05** now also fails on readings with no detected region.
- **Printed-page mismatches** became notices; they are not failures.
- **Exit codes and output:**
  - **0:** structure OK, with "PENDING HUMAN REVIEW" printed.
  - **2:** STRUCTURAL FAILURE. The failing IDs are printed, the previous build is kept, and this build goes to `<out>.failed`.
  - **3:** pending review, when `--require-approved` is given.

### 4.3 Approvals (`readings.py`, `cli.py`)

- **Review subject.** `review_subject(reading, region, doc_sha256)` hashes two things:
  - the whole reading: content, every uncertainty, source claims, preparer and method;
  - the evidence: source PDF sha256, region doc, page, bbox and kind, and native image sha256.
- **Status.** `review_status` approves only on a matching subject with a valid reviewer. Placeholders (`<…>`, "name", "tbd", blank, none) are refused.
- **`approve`:**
  - refuses placeholders before any input or output;
  - verifies source hashes and re-detects the region from the PDF;
  - refuses readings that fail checks;
  - writes the subject, what it covers, the evidence and the reviewer;
  - `--approvals PATH` lets tests write to a disposable file.
- **Content hash.** The old `content_sha256` is removed. Old-format approval entries can no longer approve anything.
- **Unknown fields** in readings are now rejected.

### 4.4 Table readings (`readings.py`)

- **RD8:**
  - column keys, headings and row keys must be unique;
  - every row has every column, with no unknown keys;
  - an empty cell must be written as `""` and listed in `blank`, and a listed blank must be empty;
  - `blank` and numerals may name only real columns.
- **`parse_limit` replaced by `numeric_reading`.** It records `{form: single|range, values, text}` and reads Arabic-Indic digits and ٫ as numbers. Units carry `numeric`, plus `context` holding the title, headings, qualifier and notes, with `interpretation: null`.
- **New reading fields:** table `direction` (rtl maps logical column i to grid column n−1−i for crops and positions), column `lang`, per-cell `numerals`, and an optional title.
- **RD6** now covers Arabic and mixed table cells: each cell is rendered right to left.
- **Numeral separators** now include ":", ٫ and ٬.

### 4.5 Drawings and the Arabic image table (`regions.py`, fixture)

- **What counts as structure.** Only these:
  - axis-aligned straight rules;
  - rectangles that are stroked only, lightly filled (luminance ≥ 0.8), or thinner than 2.5 pt;
  - dark-filled rectangles with text on them.
- **Uncertain drawings** (diagonals, curves, dark boxes with no text) become regions. A `graphic` reading needs a description (RD9).
- **Fixture page 4** now holds three things:
  - a raster **right-to-left Arabic table**: Arabic headings; "45 dB(A)"; the time range ٢٢:٠٠-٠٦:٠٠; the decimal range ٦٫٠ - ٩٫٠; ١٢; and a declared blank cell;
  - a straight-line triangle;
  - a curve.
- **Fixture page 5** adds a dark box.
- **Readings.** The builder writes readings for all five regions from its own ground truth. They stay **pending**. One test approves one of them, but only in a disposable copy.
- **Independent oracle.** The builder also records, from the vector page it rasterised, two things:
  - where each cell was drawn, which verifies the RTL column mapping;
  - the left-to-right order of each cell's digit and Latin glyphs.
- **Oracle results.** The declared visual orders matched what was actually drawn: "(dB(A 45", "٠٦:٠٠-٢٢:٠٠", "٩٫٠ - ٦٫٠" and "١٢".

### 4.6 Output safety (`cli.py`)

- **`check_output_dir` refuses:**
  - `/`, home, or anything containing it;
  - the repository or any parent of it;
  - protected folders: `sources`, `config`, `curation`, `tenderpack`, `tests`, `docs`, `worklog`, `.git`, `.venv`;
  - anything that contains or lies inside an input;
  - an existing non-empty folder that is not a previous build, checked for both `out` and `<out>.failed`.
- **Build flow:**
  - build into `.<name>.building-<pid>`;
  - on success, swap it in, remove the old build and remove a stale `<out>.failed`;
  - on structural failure, move it to `<out>.failed` and leave `out` untouched;
  - on an exception, remove the temporary folder and re-raise.
- **Testing:** in pytest temporary directories and a fake repository only.

### 4.7 Review packets (`packets.py`)

- **Content added:**
  - "What the checks prove, and what they do not";
  - "Points recorded for your decision";
  - heading crops for tables;
  - every cell crop beside its value, in RTL order where the table is RTL;
  - numeral render checks for table cells.
- **`packet.html`:** a self-contained page with every crop embedded beside its reading, checked by rendering it in headless Chromium.

## 5. Results after the fixes

The same scenarios, run with `repro_after.py` (verbatim):

~~~~text
== 1b unrelated tables merged across pages
  table T-01:cover/T1 pages [1] rows ['1', '2']
  table T-01:S2/T1 pages [2] rows ['7', '8']
== 2a duplicate clause ids -> checks / exit status
  unit ids: ['T-01:1.1', 'T-01:1.1~2']
  failing checks: ['C07', 'C09'] | status: structural_failure | exit code: 2
== 2b span listed in two units' anchors
  failing checks: ['C08', 'C10'] | status: structural_failure
== 2c trace check only looks at the first word
  (old first-word oracle still passes: True ) -> now replaced by C10:
  corrupted unit text: failing checks ['C10'] [{'unit': 'T-01:1.1', 'kind': 'clause', 'why': 'printed text differs from its spans'}]
== 3 approval survives evidence / uncertainty changes; no reviewer required
  (test-only approval, in memory) named reviewer: approved
  reviewer=None: pending - approval entry does not identify a reviewer
  reviewer='': pending - approval entry does not identify a reviewer
  reviewer='<name>': pending - approval entry does not identify a reviewer
  image replaced and reading hash updated to match: pending
  after adding an uncertainty: pending
  after moving the bbox: pending
== 4 table cells: missing unit/basis, duplicate keys; parse_limit semantics
  TN without unit/basis + duplicate row key -> failing checks: [('RD8', '4 columns x 10 rows; 0 declared blank cells; duplicate row key(s) ['BOD5']; row TN: missing cells ['unit', 'basis'] (write every cell; an empty one as "" and li')]
  numeric_reading('10') = {'form': 'single', 'values': [10.0], 'text': '10'}
== 5 triangle of straight lines
  regions detected: [('vector_graphic', [50.0, 60.0, 250.0, 250.0])]
  black box with no text (possible redaction): [('vector_graphic', [60.0, 100.0, 240.0, 140.0])]
== 6 output path safety (disposable fake repo)
  out == repo root: UnsafeOutputError refusing to write the build to <scratch> | precious exists: True
  previous results present before failed rebuild: True | after failed rebuild: True | temporary dirs left: []
~~~~

### Tests

- **Full suite:** `79 passed in 40.08s` (`make verify`), made up of:
  - the 39 existing tests, 3 of them adjusted to the new APIs:
    - `test_synthetic_regions` now expects 5 regions, C05 passing, all readings pending;
    - TN's `parsed` became `numeric`;
    - `test_approval_is_pinned_to_content` uses the review subject;
  - the trace test is kept, with a docstring marking it a weak locality check;
  - 40 regression tests: 34 written first, and 6 added while fixing and marked as such:
    - 2 more parameters of the altered-text test;
    - the altered-table-cell test;
    - the drawn-cell RTL oracle;
    - thin border bars;
    - `approve` end to end on a disposable fixture copy.
- **Rebuild:** `make verify` rebuilt twice into disposable directories; outputs **identical**.
- **Real pack (`make evidence`):**
  - C01–C10 pass;
  - 1,240 of 1,240 spans in exactly one unit;
  - 160 exclusions;
  - **2 regions**, both readings **PENDING**;
  - C10 compared 482 text-layer units in full with no mismatches;
  - 524 units.
- **Synthetic fixture:** C01–C10 pass, 5 regions, 5 readings, all pending.

### Deliberate mutations

Each fix was broken in turn and the relevant tests run:

~~~~text
M1 table continuation ignores intervening content: CAUGHT
M2 numbered paragraph needs no sequence/sentence test: CAUGHT
M3 every line counts as wrapped: CAUGHT
M4 C10 skips flow-unit text comparison: SURVIVED  (see E29)
M5 approval subject omits evidence: CAUGHT
M6 diagonal lines treated as rules: CAUGHT
M7 RTL column mapping removed: CAUGHT
M8 RD8 cell checks disabled: CAUGHT
M9 thin filled bars not rules: CAUGHT
M10 placeholder reviewer accepted: CAUGHT
M11 failed build replaces previous: CAUGHT
after tightening: M4a printed-text comparison off: CAUGHT; M4b matching-text comparison off: CAUGHT;
                  M4c row cell comparison off: CAUGHT
~~~~

## 6. Errors in this session (continuing from E21)

| # | What was wrong | How it was caught | Correction |
|---|---|---|---|
| E22 | The six gaps above, all mine from session 02 (§2). | The owner's review | Fixed (§4); tested (§5) |
| E23 | I expected "45 dB(A)" to display unchanged in a right-to-left cell. Under UAX #9 the number and Latin run are embedded and the trailing ")" takes the paragraph direction and is mirrored, so it displays "(dB(A 45". | Running the bundled engine before writing the fixture's expectations (00:35) | The fixture declares "(dB(A 45". Later confirmed by the drawn-page oracle (§4.5). |
| E24 | The first RTL table raster had its columns left to right: MuPDF's HTML engine ignores `dir="rtl"` on `<table>` for column order. | Viewing the render (00:35) | Cells written in reverse order. The builder asserts that each cell's digits landed in the predicted column. |
| E25 | My new structure rule first turned **thin filled bars** (table borders drawn as filled boxes, common in generated PDFs) into regions. The real pack still gave exactly 2 regions, so the pack tests could not catch it. | Seeing the HTML table's borders as thin black filled rectangles while building the oracle | `RULE_PT = 2.5`, plus `test_thin_filled_border_rects_are_structure` |
| E26 | The packet's "Decisions needed from you" listed every recorded uncertainty, some of which are notes, not decisions. | Reading the regenerated packet | Retitled "Points recorded for your decision". The short decision list is in the report. |
| E27 | My reproduction script's 2b scenario injected nothing: the mini pack had one clause, so the first "before" output ("checks all ok") was vacuous. Scenario 6 reused a pack that now fails structurally. | Reading the "after" output, which showed 2b passing | Both scenarios corrected and re-run on a disposable worktree of 79ef49c (§2). The failing-first test for 2b used two clauses and was valid all along. |
| E28 | Editing the script, I placed a comment that swallowed `marker = …` (NameError). | The run | Fixed |
| E29 | Mutation M4 survived: the test altered both the printed and the matching text, so either comparison alone caught it. The first cell test then survived M4c twice: first because no test altered a cell; then because a secondary check caught an inconsistent edit. | Mutation runs | The test now alters each field on its own. The cell test alters the cell and row text consistently, so only the comparison with the page catches it. |
| E30 | In the failing-first run, the placeholder-reviewer test passed for the wrong reason (unknown CLI option). | Reading why it passed | Recorded. After the fix it passes because the name is refused (M10 confirms). |

## 7. What this does and does not establish

- **Shown by checks and tests:**
  - every span is accounted for once;
  - each text-layer unit's text equals its source spans;
  - readings point at the right image;
  - tables have every cell, with blanks declared;
  - every text band is read;
  - Arabic is stored in logical order;
  - declared numerals render right to left in the order the crop shows;
  - structural errors stop the build;
  - approvals cover the reading, its uncertainties and its evidence.
- **Not shown:**
  - that any word, mark, digit or value in the two readings is right;
  - that a translation is right;
  - what Table 2-4's ranges mean;
  - whether Form 4-C's declaration 5 cites §4.2 or §4.3.

  **Passing tests are not correct interpretation, and they are not human approval.**
- **Not approved:** nothing. `curation/approvals.yaml` does not exist. The only approvals made in this session were in tests: in memory, or in a disposable copy of the synthetic fixture, under the test name "Fixture Test Reviewer".
- **Plan:** rewritten as one consistent revision 3, keeping:
  - A1 in Excel;
  - configurable bidder assumptions (three members by default);
  - the later Claude Code / OpenRouter / Ollama routes, with integrations and model selection deferred.
- **Stopped before Stage 2.**
