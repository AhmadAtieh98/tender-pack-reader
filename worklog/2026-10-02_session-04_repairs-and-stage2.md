# Session 04: second review repairs, and Stage 2 (thin end-to-end slice)

- **Date:** 2 Oct 2026, from 07:32 UTC (10:32 Riyadh).
- **Who:**
  - The owner reviewed the repaired Stage 1 work; the three findings below are the owner's.
  - Reproduction, fixes, Stage 2, tests and this log were done by the coding assistant (Claude Code, in the cloud container).
  - Subagents (launched by the assistant, each with a written brief; their results were checked by the assistant before use):
    - an **adversarial reviewer** of the round-1 repairs (attacks only; it changed no program file);
    - a **dates** agent (`tenderpack/dates.py`, `tests/test_dates.py`);
    - a **render** agent (`tenderpack/render.py`, `tests/test_render.py`);
    - an **independent oracle** (`tests/golden/stage2_expectations.yaml`), written from the PDFs and the two pending readings only, without reading or running the program;
    - a **drill fixture** agent (`tests/fixtures/make_drill.py`). The first launch stopped with an error before writing any file; the relaunch wrote the builder but stopped before verifying it; the assistant verified and completed the drill itself (§7, E31).
- **Scope:** reproduce and fix three gaps with failing tests first; then Stage 2 as a representative slice; stop before Stage 3. Approve nothing on the owner's behalf; no model integrations.

## 1. The exchanges (verbatim)

**Owner, 07:32 UTC.** Message text as received:

~~~~text
good progress 

let’s close the remaining gaps and do more in stage 2
first reproduce and fix thse,with failing tests before the changes. if you disagree, show me why.

1. the evidence checks accept `120,000` becoming `210,000`, changes to normalized table text, and incorrect page/crop references with unchanged span ids. check ordered text per cell and column, normalized values, and the actual page and geometry of each anchor.
2. the arabic fixture accepts scrambled `45 dB(A)` output, while the validator can pass just because the digits match. handle the english expression correctly inside the arabic layout, keep the raw transcription unchanged, and test against a correctly rendered source. digits-only verification must be labelled partial.
3. `--require-approved` replaces previous results before rejecting pending readings. apply that gate before publishing; keep rejected candidates separate and preserve the previous build.

once these pass, contnue into stage 2. i want a working end-to-end version covering the difficult cases, with outputs i can inspect.
include the lcc deletion, reinstatement and revocation chain; deadline changes and their dependencies, including the footnote; repeated-wording traps; the weighting change; image-based tn; form 4-g; the arabic form 4-c consequences; and the conflicting form 4-a. use the same amendment path for both existing addenda and future ones, without hardcoded outcomes.
generate the first connected versions of:

* a1 in excel, csv and json, with status at each stage.
* a2 showing changes, affected rows and the evidence chain.
* a3 as a one-page draft with explicit consequences and unresolved issues.
* a5 generated from those a1 rows, with dependencies, labelled lead-time assumptions and infeasibility flags.

keep this to a representative set of rows; don’t expand into the full register yet. account for the remaining addendum provisions as outside the slice or unresolved, so partial coverage is obvious.
for d3, use independently testable obligations with clause grouping and scope tags. for d4, show plausible counting interpretations and an explicit configurable planning assumption. for d7, keep review evidence committed for now.
prove wrong-target rejection, dependency staleness and pending image status carrying through. partial changes must preserve the last validated state. run one synthetic addendum drill through the same path.
also , non-binding minutes and questions quoting old values aren’t automatically revoked answers. keep transcription approval separate from interpretation; my image approvals remain pending.
keep the work log accurate, including errors and actual test results. leave model integrations for later.
return the repair evidence, generated outputs and a short list of decisions needed from me. stop before stage 3.

Use subagents effectively
~~~~

**Other owner messages in this session, in order:**

| From | Text |
|---|---|
| owner | "Try again" (after the first drill-fixture agent stopped before writing anything; it was relaunched) |
| owner | "test agent stopped because of lost connection, continue , additionally , they replied to my email , record that", with the hiring team's reply attached as an `.eml` file |

**The hiring team's reply** (received Thu 1 Oct 2026 17:51 PDT = Fri 2 Oct 03:51 Riyadh; provided by the owner in this session) is recorded as received in `sources/correspondence/2026-10-02_reply_from_hiring.eml`, with its plain-text body in `2026-10-02_reply_from_hiring.md` and both files in `sources/manifest.json`. It confirms all six points of the owner's 1 Oct email: tools (including in the live session, if documented); the pack is complete as provided, with Volume III and Drawing 03-C-114 to be treated as referenced but not supplied and the gaps and impact flagged; Addendum 3 will be a PDF in the same format, shared at the start of the live session; no written clarifications to other candidates; the A5 basis; the archive and formats. Delivery "by 17:00 Monday 5 October at the latest". Recorded in `docs/PLAN.md` §0, §1.4, F13, D1, D6, and as Issue `I-VOL-III` (on A3).

The assistant's progress notes while working were short status lines; the final reply is preserved verbatim in `2026-10-02_session-04_reply.md`.

## 2. Repairs: reproduction before any fix

All three findings were reproduced on the code as it stood at the start of the session (commit `574f4b3`). **None is disputed.** Round 1 of the fixes is commit `0c8abb2`, round 2 `25c78fd`.

| # | Reproduced |
|---|---|
| 1 | In a disposable copy of the evidence: `120,000` changed to `210,000` in a table cell (same characters, reordered), text moved between columns, a changed `normalized` value of a table row, and anchors pointing at the wrong page or box with the same span ids — C10 passed every one. |
| 2 | The synthetic Arabic fixture drew `45 dB(A)` in a scrambled order and the reading still passed RD6, because RD6 compared digits only. |
| 3 | `ingest --require-approved` swapped the new build into place, then exited 3 because readings were pending: the previous build was already gone. |

### 2.1 Failing-first, round 1

`tests/test_session04_repairs.py` was written before any change. First run: **14 failed, 1 passed** (the passing one is `test_gate_passes_when_everything_is_approved`, a guard that must keep passing). Two tests were added while fixing, after deliberate mutations survived (marked in the file): R1a (per-cell order) and R1b (column placement) first survived because the original tests changed several fields at once, so a neighbouring check caught them first.

### 2.2 Fixes, round 1

- **C10, per cell and per anchor** (`segment.py`, `coverage.py`): every table cell keeps its spans in reading order (`cell_spans`); C10 re-extracts each cell's text from those spans and compares it in order; rebuilds the row and table text and the `normalized` value; checks every anchor's page and box against the span's real page and box; checks span order across anchors. Image-reading units are checked against the crops they cite (`reading_evidence`).
- **Arabic layout of Latin expressions** (`arabic.py`, `readings.py`, `packets.py`, fixture): the raw transcription stays in logical order, unchanged; for display only, a Latin expression inside Arabic is wrapped in LRE…PDF (`display_form`; MuPDF ignores `dir` on a mixed span and misplaces isolates). The fixture now draws `45 dB(A)` correctly and the test checks the reading against what was drawn. `visual_check` is tri-state: **pass**, **partial** (digits verified, Arabic letters inside the token not verifiable by position) and **fail**; packets and C05 show PARTIAL.
- **Approval gate before publishing** (`cli.py`): the gate is applied to the candidate build; a rejected candidate goes to `<out>.rejected` with `REJECTED.md`, and the previous build is untouched. First build with pending readings publishes nothing.

Round-1 mutations (each check switched off in turn; `s04/mutations.txt` in the session scratchpad): R1a and R1b survived until the isolated tests were added, then caught; R1c–R1g, R2a, R2b, R3a caught.

### 2.3 Adversarial review of the repairs (round 2)

An adversarial subagent attacked the round-1 checks with its own scripts and found **about 30 ways through**. Examples: relabelling a footnote as a clause, moving a label span, changing a unit's `kind`, giving an invisible text layer a paragraph kind, mutating a reading-derived unit consistently with its anchors, naming another run of the same line as the declared visual order, an empty expected order, an input inside the `.failed` sibling, a symlinked sibling. Its reproductions were ported into `tests/test_session04_adversary.py` first: **34 failed, 15 passed** (the 15 are controls that must keep passing), then a second batch of **14 failed**. Fixes:

- C10 compares every field of every text-layer unit with an **independent re-segmentation of a fresh extraction** (cached by file hash and furniture rules), and checks table cells and headers against grids re-detected from the page (column, row membership, one table per grid). Labels, label spans (first span of the first line), kinds, region units with no text and order across anchors are checked too.
- Units from image readings are **re-derived from their reading** and compared; every anchor must cite a crop: blocks the crop and box of the band they were read from (the band is tied in the anchor), rows their grid row, cells their column (right-to-left aware).
- RD6: a declared visual order must hold exactly the token's characters and match a whole rendered run; several numerals on one line are checked in their left-to-right order. The Latin island covers unit signs, super/subscripts, the hyphen family and Arabic-Indic digits inside a Latin reference, and leaves an enclosing bracket outside. Extended Arabic-Indic digits are no longer treated as letters.
- `.failed` / `.rejected` siblings get the same safety checks as the output folder; symlinks are refused; the temporary build is removed if setting it aside fails.

Round-2 mutations (`s04/mutations_round2.txt`): A1, A3, A5, A7, A8 caught at once. **A2 (fresh-grid checks off), A4 (band tie off) and A6 (token character check off) survived.** Three tests were added that simulate a bug shared by the segmenter and its re-check (merging two grid rows; a reading-derivation bug; another run of the same line); two of my first mutation forms were wrong (one made every test fail, one routed to a different branch) and were corrected. After that all three are caught.

## 3. Stage 2: what was built

`docs/PLAN.md` §10 lists the modules and checks. In short:

- **One amendment path.** `outputs` applies the op file of every addendum in number order; an addendum without a curated op file is drafted by `draft` (patterns over the addendum's own wording; anything it cannot type is `unresolved`) and goes through the same engine. No outcome is written into the code: the engine knows op types and checks, not tender facts.
- **Op files for ADD-01 and ADD-02** (`curation/amendments/`): started from the drafter's output, completed by the assistant. ADD-01: 11 ops, 17 dispositions; ADD-02: 14 ops, 12 dispositions; 0 unresolved. Every op is **proposed**.
- **Register slice** (`curation/register/rows.yaml`): 26 rows (D3: independently testable obligations, `group` = source clause, `scope` tags). Interpretations are pinned (`pin` → `pins.yaml`) to the hashes of their dependencies; a later change makes the row STALE.
- **Dates** (D4): every plausible counting reading is computed and shown; planning uses `planning.counting_policy: conservative` in `config/assumptions.yaml`.
- **A5**: activities from the evidence items of rows in force (`curation/activity_templates.yaml`), durations from labelled assumptions (value, basis, owner), backward pass in Working Days, INFEASIBLE / DEADLINE PASSED flags, stage-to-stage deltas.
- **Outputs** (`out/`, D7: committed): A1 xlsx/csv/json with a status column per stage and Dates, Issues, Stages, Assumptions sheets; A2 markdown with changes, rows that move (and why), answers to review, non-binding statements, provision coverage and evidence chains; A3 one-page PDF; A5 programme, marshalling, replan deltas, per-stage JSON.

### 3.1 What the outputs show on the real pack (all proposals; nothing reviewed)

- **PDD** 12 Nov → 26 Nov 2026 (ADD-01 2.1). Clarification cut-off 29 Oct → 12 Nov; bond validity, proposal validity and the footnote 12 look-back move with it, each with two readings shown. VOL-I 8.3 (ISO current at the PDD) is **STALE** after ADD-01: its interpretation was made at BASE and no addendum text addresses it again.
- **LCC**: active (30%, no consequence) → deleted (ADD-01 4.1) → reinstated at 35% with "non-responsive" (ADD-02 9.1); ADD-01 4.2 (disregard any LCC reference) in effect at ADD-01, revoked by ADD-02 9.2. In A5 at ADD-02, with the 30-WD lead-time **assumption**, the certificate is **INFEASIBLE by 7 WD** and the ratio calculation by 12 WD.
- **Repeated wording**: ADD-02 4.1 changes "seventy-two (72) hours" in VOL-II 4.4 only; VOL-V 31.3 has the same words and is recorded as "also in, not targeted". 60/40 in VOL-V 29.2 is untouched by the 11.2 weighting change.
- **Weighting** 60/40 → 65/35, made only inside note (2) to the reissued Table 1-1 (old words located by shape, flagged for a person). Table 1-1 B 20→15, D 15→20.
- **TN** 5 → 3 mg/l; the old value comes from the image reading, **pending**; flagged on the row, in A3 and on the A5 activities.
- **Form 4-G** inserted after VOL-I 9.1(e) (re-lettering not stated: an issue); "non-responsive" if not submitted.
- **Form 4-C**: the Arabic consequences are quoted in Arabic with a proposed translation labelled as not reviewed; "exclusion" vs the pack's English categories is for a person. Readings pending.
- **Form 4-A**: the reissued form (ADD-01 App A) still prints 12 November 2026; raised as an issue (C31), never corrected.
- **Answers**: ADD-01 Q2 (120-page limit) is listed for review at ADD-02, which changed VOL-I 9.2; it stays in force. The minutes (ADD-01 App B) are non-binding context, never answers.
- **ADD-01 3.1** attendance notice: OK at ADD-01; at ADD-02 its deadline (14 Oct, conservative reading) is before the status date: DEADLINE PASSED, "record whether it was done".

## 4. Stage 2 tests

`tests/test_stage2.py` compares the engine with the independent oracle (PDD and dependants, every counting reading, LCC chain, repeated wording incl. negative controls, weighting and Table 1-1 marks per stage, TN, Form 4-G, Form 4-C, Form 4-A, provision coverage of every oracle provision, answers incl. the oracle's negative controls) and proves, in disposable copies of the curated inputs:

- **wrong-target rejection**: ADD-02 4.1 retargeted to VOL-V 31.3 fails C22; neither clause changes; ADD-02 becomes PARTIAL and the validated state stays ADD-01. A second case arose by accident (E29): an op attaching ADD-02 Q8 to VOL-I 6.3 is rejected because Q8 does not cite 6.3;
- **dependency staleness**: a further answer about VOL-I 6.4 makes both 6.4 rows STALE, and the flag reaches A5 and the issues; VOL-I 8.3 is STALE after the PDD moves;
- **pending image status** carried through A1, A3 and A5;
- **partial preserves the validated state**: an unaccounted provision makes ADD-02 PARTIAL; A1 marks its column WORKING, A3 and the main A5 come from ADD-01, the working A5 goes to `a5/working/`;
- a missing quote is a **structural failure**: nothing published, previous outputs kept, candidate in `out.failed`; output paths inside the repository are refused;
- **transcription approval is separate from interpretation**: in a disposable copy, "Fixture Test Reviewer" approves the Table 2-4 reading; TN's transcription becomes approved, its interpretation stays proposed, Form 4-C stays pending. The real `curation/approvals.yaml` is never created;
- two builds are **byte-identical**.


## 7. Errors in this session (continuing from E22)

| # | Error | Caught by | Fix |
|---|---|---|---|
| E23 | The three gaps above (§2), all mine from session 03. | The owner's review | Fixed (§2.2) |
| E24 | About 30 bypasses of my round-1 repairs (§2.3). | The adversarial subagent | Fixed (§2.3) |
| E25 | My first "partial" test used a Latin-letter mismatch, which must fail, not be partial. | Re-reading the test against the definition | Changed to an Arabic-letter case |
| E26 | Mutations R1a/R1b (round 1) and A2/A4/A6 (round 2) survived: tests changed several fields at once, or the check and the re-check shared the bug. | Deliberate mutations | Isolated and shared-bug tests added (§2.2, §2.3) |
| E27 | Round-2 false positive: the label-span check sorted spans by a rounded centre, so a superscript could come first. Also a name collision in a page-table cache (`TypeError` on `len(Table)`) and a 5-second re-segmentation per check. | Running the suite | Same-line test (`_same_line`); one fresh-extraction cache keyed by file hash and rules |
| E28 | Plan §2.5 said "24 Working Days" from ADD-02 to the PDD without saying which days count; `working_days_between(22 Oct, 26 Nov)` = 25 (after 22 Oct up to and including 26 Nov). | The dates agent's tests | Plan corrected (both counts stated) |
| E29 | Drafter: `_shape` built an invalid regular expression; the citation resolver missed "footnote 12 to Clause 8.5" (ADD-01 PARTIAL); `set_value` reordered a row's text (cells sorted); "also in" listed addendum units. | First engine runs on the real pack | Token wildcards; pattern added; only the changed cell replaced; volumes only |
| E30 | First Stage 2 outputs: A2 listed ADD-01 Q5 and ADD-02 Q11/Q14 as answers to review because a bare "5", "12" or "120" matched (the question number, footnote 12, 120,000 m³/day); A3 doubled quotation marks and showed "active by addendum"; "WINDOW CLOSED" mixed a passed pack deadline with an infeasible chain; dates shown for rows not yet issued; duplicate "accounted by" entries. My own synthetic staleness op (Q8 → VOL-I 6.3) was rejected by C22 because Q8 does not cite 6.3. | Reading the outputs; the oracle's negative controls; the test | Figures matched with their unit ("120 pages", "12 November", "5 mg/l"), question numbers excluded; class and quote rendered separately, with the translation; DEADLINE PASSED vs INFEASIBLE; dates only for rows in force; deduplicated; the rejected op kept as a second wrong-target test and the staleness test retargeted to 6.4 |
| E31 | The drill-fixture subagent stopped twice: first with an error before writing any file; then after writing the builder but before verifying it. | Its completion notices; the owner | Relaunched once; the second time the assistant ran the brief's verification itself (§8) |
| E32 | Design gap found by the drill test: when a later addendum changes the words an interpretation quoted (ADD-03 moves the PDD that VOL-I-6.1-01 quotes), C16 would have called the whole build a structural failure. The intended behaviour is STALE. | Writing `test_drill.py` before running it | A missing quote is structural only for a current interpretation; for a row already STALE it is added to the staleness ("expected: the interpretation predates the change"); a row that was never pinned is not excused. C16's report names such rows |
| E33 | C01 always printed "sources/manifest.json", also for the fixture and the drill, which use their own manifests. | Reading the drill's coverage report | C01 names the pack's own manifest (`build/fixture/coverage.*` changes accordingly) |
| E34 | A2 listed rows as "moving" in the next addendum when only the label changed ("AMENDED (x)" → "ACTIVE (as amended by x)"). | Reading the drill's A2 | "status" is reported only when this addendum's ops touched the row or it came into or out of force |

## 8. The ADD-03 drill

`tests/fixtures/make_drill.py` builds a synthetic "Addendum No. 3" (not tender content) laid out like the received addenda (same fonts, furniture with the WinAnsi em dash, ruled Q&A table) and a seven-document pack around it. Verification, run by the assistant: two builds byte-identical (PDF sha256 `0c1a4917…c694`); `ingest` exit 0 with C01–C10 passing (547 units, 34 pages, 170 furniture spans by the unchanged rules); all 524 real units identical to the real build; the 23 ADD-03 units match the builder's own record (`expected.yaml`) exactly.

There is no curated op file for ADD-03, so `outputs` drafts one with the same drafter and applies it with the same engine (`make drill`: `build/drill-src/`, `build/drill/`, `out-drill/`):

| Provision | Drafted | Engine |
|---|---|---|
| 2.1 PDD 26 Nov → 10 Dec | replace_text VOL-I:6.1 | valid; dates recomputed (cut-off 26 Nov, bond 8 Jun 2027, proposal 9 May 2027, look-back 11 Dec 2016); six rows STALE |
| 3.1 VOL-V 31.3 72 h → 48 h | replace_text VOL-V:31.3 | valid; VOL-II 4.4 untouched; VOL-V-31.3-01 STALE |
| 4.1 delete VOL-I 8.6 | set_status deleted | valid; LCC chain active → deleted → reinstated → deleted (working state only) |
| 5.1 TP → 0.5 mg/l | set_value VOL-II:T2-4/TP | valid; old value 1 from the pending image reading, flagged |
| 6.1 "bid security period extended by thirty days" | unresolved | PARTIAL until a person decides |
| 7.1 VOL-II 4.4 72 h → 60 h | replace_text VOL-II:4.4 | **invalid (C23)**: the old words are no longer there (ADD-02 made them 96 h); not retargeted |
| Q15 (cites VOL-I 9.2) | unresolved | not listed for review (negative control) |
| Q16 (quotes "26 November 2026") | unresolved | listed "REVIEW (not automatically revoked)" |

ADD-03 is **PARTIAL**: the validated state stays ADD-02. A1 shows an ADD-03 column marked WORKING; A3 and the main A5 come from ADD-02 (PDD 26 Nov); the working A5 (`out-drill/a5/working/ADD-03.json`, status date 5 Nov) plans to 10 Dec with no LCC activity; A2 lists the drafted ops, the invalid op and the unresolved provisions. The drafted op file is written to `out-drill/drafted/ADD-03.yaml`, never into `curation/`.

## 9. Results

**Tests:** `make test`: **237 passed** in 143 s.

| File | Tests | |
|---|---|---|
| `test_session04_repairs.py` | 17 | repairs (15 written first; 2 added after surviving mutations) |
| `test_session04_adversary.py` | 66 | the adversarial reviewer's attacks, controls and shared-bug cases |
| `test_stage2.py` | 35 | oracle comparisons and scenarios (§4) |
| `test_drill.py` | 10 | the ADD-03 drill (§8) |
| `test_dates.py` | 20 | calendar and counting readings |
| `test_render.py` | 10 | A1 workbook and A3 page determinism, one-page limit, right-to-left text |
| earlier sessions | 79 | unchanged |

**Rebuilds:** Stage 1 `make evidence` leaves `build/` unchanged except the corrected C01 wording in `build/fixture/`; two Stage 2 builds are byte-identical and identical to the committed `out/`.

**Checks on the real pack:** E01, C16, C25, C13, C40, C43 pass (A3 at scale 0.968); C20 and C21–C27: ADD-01 36 provisions and 11 ops, ADD-02 40 provisions and 14 ops, nothing unresolved or invalid; C11 reports VOL-I-8.3-01 STALE at ADD-01 and ADD-02.

## 10. What this does and does not establish

The tests show that the engine reproduces the independent oracle on the slice, that wrong targets and stale old words are rejected, that staleness and pending reading status travel to every output, that a partial addendum never replaces the validated state, and that the same path takes an unseen addendum. They do **not** show that any interpretation, consequence class, translation, lead time or counting choice is right, and nothing has been reviewed or approved by a person: every op and row is a proposal, and both image readings remain pending the owner's review. Passing tests are not correct interpretation, and they are not approval.
