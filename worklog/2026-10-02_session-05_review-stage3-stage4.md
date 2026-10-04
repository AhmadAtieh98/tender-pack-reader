# Session 05: the owner's code review (five findings), Stage 3 (full register) and Stage 4 (A5)

- **Date:** 2 Oct 2026, from 13:31 UTC (16:31 Riyadh); work paused at a usage limit and continued from about 17:30 UTC.
- **Who:**
  - The owner reviewed the code and outputs; the five findings below are the owner's.
  - The assistant (Claude Code, in the cloud container) acted as the single orchestrator: it reproduced the findings, wrote the failing tests, made the code fixes, built the Stage 3 infrastructure, integrated the subagents' work and ran every check.
  - Subagents (each with a written brief, its own files and a validator to run; results checked by the orchestrator):
    - **register VOL-I**, **register VOL-II/VOL-V**, **register VOL-IV and addendum-created obligations**: rows, unit dispositions, evidence items and issues, each in its own files;
    - **A5 (Stage 4)**: templates for every evidence item, programme extensions (document counts, resources, infeasibility drivers), scenarios;
    - **drill B fixture**: a second synthetic Addendum No. 3 with two changes in one paragraph, a new obligation, an image-table change and two change types not seen in ADD-01/ADD-02.
  - Four of the five agents were stopped by an API usage limit; the VOL-I agent had finished its files by then, the others were resumed with their context after the reset (§8, E36).
- **Scope:** reproduce the five findings with failing tests first, fix them; complete Stage 3 and the connected Stage 4 work; labelled working drafts; a strict release gate; a second drill with rehearsal results; stop before final submission. Approve nothing and refresh no review status on the owner's behalf.

## 1. The exchanges (verbatim)

**Owner.** Message text as received:

~~~~text
while checking the code and outputs these came up. reproduce them first and tell me if i’m wrong(with evidence)

1-in amend.py, tn can become 999 instead of 3, the wrong column can change, and the evaluation table can be replaced with the hydraulic table, all passing validation. check values, columns and replacement content against the amendment itself. failed annotations also leave changes behind; failed operations must change nothing, including history and dependencis. 

2-in draft.py, a paragrph with two recognised changes produces only the first operation, but the whole paragraph is marked covered. process both or flag the remaining text as unresolved

3-checking stage2.load_evidence, changing a saved clause’s page to 99 still passes. verify intermediate files against their manifest. also, register.pin_value loses the image review fingerprint: a changed reading needs to keep dependent interpretations stale even after its transcription is approved again.

4-in the generated a3, the lcc consequence points to the original clause page, although that wording comes from add-02. cite the actual supporting page and amendment. keep original quotations separate from assembled effective text in a1–a3. Make always to reference the latest file reference for eachj point 

5-checking schedule.py, removing the lcc template makes its activities disappear while the build passes. check both directions: activities need requirements, and required deliverables need activities or a justified exception. missing templates and dependencies must be visible failure modes

add focused failing tests, fix these, then complete stage 3 and the connected stage 4 work. keep progressing where my answers aren’t needed

over all six documents, forms, footnotes, tables and addendum provisions. give every source unit a disposition and every independently testable obligation a stable row, evidence, owner and stage history.

replace “outside the slice” with actual treatment, and run english and arabic consequencce sweeps for omissions.

regenerate the full a1 excel/csv/json, a2, one-page a3 and a5 programme and marshalling plan. keep a3 readable without tiny text, with supporting detail linked. include the missing drawings and their impact

a5 should cover both envelopes, document counts, issuers, dependencies and resource assumptions. keep lead times provisional, show what drives infeasibility, and demonstrate changes to consortium size, lead times and the working calendar flowing through

proposed operations can run in labelled working drafts. structurally checked doesn’t mean human-approved. strict release must reject incomplete coverage, stale interpretations and required approvals still pending. don’t approve or refresh review status for me

run another synthetic addendum with two changes in one paragraph, a new obligation and an image/table change. show new rows, affected activities, stale dependencies and preservation of any previous approved state. (also add a couple of unseen before change cases  (in add1 or add2) 

keep the work log accurate, model integrations can wait

return the completed working outputs, remaining gaps, rehearsal results and a short prioritised decision list for me. stop before final submission

Use subagents smartly for this task with one master orchestrator [model name omitted in the repository] agent driving all processess
~~~~

*Note added in session 08 (4 Oct 2026), for accuracy: the bracketed words replace the owner's own words, which named a model. They were removed from this file in commit `33f1f81` because no model identifier may be written into the repository's files; nothing else in the message was changed. The message as first recorded, with those words, is unchanged in commit `6a5d6cb` (the history is kept as the owner asked).*

**Later owner message:** "I hit my usage limit while you were working, but it has reset now. Please continue from where you left off."

## 2. Reproduction on commit 160242f (before any fix)

A script (session scratchpad `s05/repro.py`) ran each finding against the code as committed, in memory or on disposable copies. Output, verbatim:

~~~~text
== 1a  TN set to 999 (provision says 3 mg/l)
   valid: True | stage: APPLIED | TN limit: 999
== 1b  wrong column (Unit instead of Limit)
   valid: True | stage: APPLIED | TN cells: {'Basis of assessment': '30-day rolling average', 'Limit': '5', 'Parameter': 'Total Nitrogen (TN)', 'Unit': '3'}
== 1c  Table 1-1 replaced by VOL-II Table 2-6 (hydraulic design flows)
   valid: True | stage: APPLIED | VOL-I:T1-1/B superseded_by: VOL-II:T2-6 | T2-6 rows now carry history: ['VOL-II:T2-6/2-6.1', 'VOL-II:T2-6/2-6.2', 'VOL-II:T2-6/2-6.3']
== 1d  failed annotation leaves its annotation behind
   valid: False | failed check: ['C27'] | VOL-I:11.3 annotations after the failed op: ['ADD-02/T1-1-rev/note(1)']
== 1e  failed insert leaves history on its content
   valid: False | ADD-02:F4-G/T1/1 history after the failed op: []
== 2   one paragraph, two recognised changes
   ops: [('ADD-09/2.1', 'VOL-I:9.2', 'one hundred and twenty (120) pages', 'one hundred and fifty (150) pages')]
   dispositions for ADD-09:2.1: []
   coverage of ADD-09:2.1: op | VOL-V:36.2 changed: False
== 3a  saved clause page changed to 99 in units.json
   load_evidence problems: none
   E01 check: {'id': 'E01', 'ok': True, 'detail': 'evidence build structurally OK and built from the current inputs'}
== 3b  pin ignores the image review fingerprint
   pin before: 3cd0bd71a365346a | pin after the reading changed: 3cd0bd71a365346a
   pin after it is approved again: 3cd0bd71a365346a
== 4   A3 LCC consequence source
   A3 cites: VOL-I 8.6 p4 | quote: Failure to submit the certificate shall render the Proposal non-responsive.
   in the original VOL-I 8.6 text: False | in ADD-02 9.1 (p3): True
== 5   LCC template removed
   build status: ok | lcc activities: [] | VOL-I-8.6-01 in force: REINSTATED-AMENDED (ADD-02/9.1)
~~~~

**All five findings are confirmed; none is disputed.** Two notes: 1e was my own extra probe of the insert path — that path happened not to leak (C22 rejects the anchor first), but the same "change first, check later" pattern existed there, so all ops were made transactional; in 3b, approving the reading again also leaves the pin unchanged, which is correct (the fault was that the fingerprint was not pinned at all).

## 3. Failing tests first

`tests/test_session05_review.py` (19 tests) was written before any fix. First run: **17 failed, 2 passed**. The two that passed are guards: a reinstatement whose text is not in the provision, and an insert whose group does not exist, already fail before touching the state, and must keep passing.

## 4. Fixes

### 4.1 Finding 1, `amend.py`

- **Failed ops change nothing.** Before each op, the engine snapshots the state and the unit order (`copy.deepcopy`). If any check fails, both are restored, so text, cells, status, history, annotations and the dependencies derived from them are unchanged (1d, 1e).
- **`set_value`** (C21):
  - the provision must name the column (its full heading, case-insensitive);
  - the provision must state the new value followed by the row's unit ("3 mg/l");
  - otherwise the op is invalid (1a, 1b).
- **`replace_unit`** (C22): the replacement content must be addendum content printed after the provision (headings excluded), and its group title must name the target ("Table 1-1", "Form 4-A") (1c).
- **Disposition values:** `outside_slice` is removed from the op-file model; the only values left are `no_effect | unresolved`.

### 4.2 Finding 2, `draft.py`

- Every recognised change in a provision becomes its own op, with ids `2.1(a)`, `2.1(b)`.
- Text left over once the matches and recognised boilerplate are removed ("unchanged", "all other terms", "This Addendum amends …") is quoted in an `unresolved` disposition. A paragraph is never marked covered by its first match alone.

### 4.3 Finding 3, `stage2.load_evidence` and `register.pin_value`

- **`load_evidence` checks:**
  - the build status and its inputs;
  - every output file's sha256 against `BUILD_MANIFEST.json` (an edited `units.json` is rejected);
  - each unit's pages against its anchors' pages;
  - each span id against its page.
- **`pin_value`** includes the reading's review-subject fingerprint (`UState.reading_subject`; pin format 2). A changed reading keeps dependent interpretations STALE, even after the new transcription is approved. The approval status itself is not pinned.
- **Existing pins:** `pin --migrate-format` upgraded them. It upgrades a pin only where every dependency still had its format-1 value, so nothing that had changed was refreshed by the migration. The readings had not changed since the pins were made. The pre-migration file is kept in the session scratchpad (`s05/pins_v1.yaml`).

### 4.4 Finding 4, provenance in A1–A3

- **`Register.source_of`** gives the latest reference for a quote:
  - "ADD-02 9.1 p3 (reinstating VOL-I 8.6)"; or
  - "VOL-I 6.1 p3 as amended by ADD-01 2.1 p1".
- **A1 columns are kept apart:** `original_text` (the document as printed), `effective_text` (assembled after the ops), `quote` (what the interpretation relies on) and `source` (latest reference).
- **A3 and A2** cite the consequence's own supporting page and amendment (`consequence_source`).
- **Whole-clause citations:** `citations.resolve` expands one ("Volume V Clause 29") to its sub-clauses, so annotations on a whole clause reach its rows.

### 4.5 Finding 5, `schedule.py`

Both directions are checked, and each failure is structural:

- **C40:** every activity cites a row in force.
- **C44:** every evidence item needed by a row in force has activities, or a justified exception (`_exceptions` in the templates file). The check lists every missing item.
- **C45:**
  - every dependency names a defined activity;
  - every duration names a lead-time assumption;
  - every resource is a defined role;
  - an activity listed under two items is defined identically.
- **Dependencies not needed at the current stage** are shown on the activity ("not required at this stage") and never dropped.

### 4.6 After the fixes

The same reproduction script, run again (`s05/repro_after.txt`), verbatim:

~~~~text
== 1a  TN set to 999 (provision says 3 mg/l)
   valid: False | stage: PARTIAL | TN limit: 5
== 1b  wrong column (Unit instead of Limit)
   valid: False | stage: PARTIAL | TN cells: {'Basis of assessment': '30-day rolling average', 'Limit': '5', 'Parameter': 'Total Nitrogen (TN)', 'Unit': 'mg/l'}
== 1c  Table 1-1 replaced by VOL-II Table 2-6 (hydraulic design flows)
   valid: False | stage: PARTIAL | VOL-I:T1-1/B superseded_by: None | T2-6 rows now carry history: []
== 1d  failed annotation leaves its annotation behind
   valid: False | failed check: ['C27'] | VOL-I:11.3 annotations after the failed op: []
== 1e  failed insert leaves history on its content
   valid: False | ADD-02:F4-G/T1/1 history after the failed op: []
== 2   one paragraph, two recognised changes
   ops: [('ADD-09/2.1(a)', 'VOL-I:9.2', 'one hundred and twenty (120) pages', 'one hundred and fifty (150) pages'), ('ADD-09/2.1(b)', 'VOL-V:36.2', 'SAR 5,000,000', 'SAR 2,500,000')]
   dispositions for ADD-09:2.1: []
   coverage of ADD-09:2.1: op | VOL-V:36.2 changed: True
== 3a  saved clause page changed to 99 in units.json
   load_evidence problems: ['evidence file units.json differs from BUILD_MANIFEST.json (edited after the build)', "VOL-I:8.6: pages [99] disagree with its anchors' pages [4]"]
   E01 check: {'id': 'E01', 'ok': False, 'detail': "evidence file units.json differs from BUILD_MANIFEST.json (edited after the build); VOL-I:8.6: pages [99] disagree with its anchors' pages [4]"}
== 3b  pin ignores the image review fingerprint
   pin before: eebbfdbfdc95003d | pin after the reading changed: d9d88d30362537d5
   pin after it is approved again: d9d88d30362537d5
== 4   A3 LCC consequence source
   A3 cites: ADD-02 9.1 p3 (reinstating VOL-I 8.6) | quote: Failure to submit the certificate shall render the Proposal non-responsive.
   in the original VOL-I 8.6 text: False | in ADD-02 9.1 (p3): True
== 5   LCC template removed
   build status: structural_failure | lcc activities: [] | VOL-I-8.6-01 in force: REINSTATED-AMENDED (ADD-02/9.1)
~~~~

**Tests.**

- The 19 failing-first tests pass.
- Five assertions in `tests/test_stage2.py` and the drill A expectations changed because the intended behaviour changed:
  - nothing is left "outside the slice" (session 04 left ADD-02 Table 1-1 note (3) out);
  - A3's layout moved to `explicit`, `none_stated_ids` and `issues_detail`, with items grouped by class;
  - drill A's cover paragraph 3 ("Bidders shall acknowledge receipt in Form 4-A") is now an obligation, not `no_effect`;
  - a coverage mutation test now removes `ADD-02:1.1` (Q12 now has an op).

## 5. Stage 3: the full register

### 5.1 Infrastructure (orchestrator)

- **`dispositions.py`:** every volume unit gets a disposition:
  - `requirement`, `consequence` or `duplicate`, each with rows, linked in both directions;
  - `definition`, `authority`, `informational` or `context`, each with a reason;
  - `structural`, assigned automatically for headings, table containers and image regions.
  
  Addendum provisions are covered by the op files (C20).
- **Sweeps, sentence by sentence:**
  - **C14:** obligation words in units that are not requirements, listed for a person.
  - **C15:** consequence words in English (reject, disqualif…, non-responsive, disregard, returned unopened, …) and Arabic (استبعاد, غير مستجيب, رفض, …). Each hit must link to a row that quotes its consequence from that unit, or to a `consequence_note`.
- **`evidence.py`:** a closed evidence-item vocabulary (`curation/evidence_items/`): envelope, issuer, multiplicity and whether the item is counted.
- **Register files:**
  - `RowFile.include` splits the register into files per volume;
  - each row has an `owner` (a role) and `no_deliverable` (the reason a bid-stage row needs no document);
  - issues are loaded from `issues.yaml` plus `issues/*.yaml`.
- **`tenderpack check-register [--doc VOL-I]`:** lists everything a register drafter must clear; exit 1 while anything remains.

### 5.2 Rows, dispositions and issues (subagents, checked by the orchestrator)

- **Split by volume:**
  - VOL-I: `rows/VOL-I.yaml`, 46 rows;
  - VOL-II and VOL-V: 71 and 29 rows;
  - VOL-IV and addendum-created obligations: 23 and 7 rows;
  - core rows from session 04: 26 in `rows.yaml`.
- **Each agent's files** came with dispositions and issues and were integrated only once `check-register --doc` reported no findings and the build's structural checks passed.
- **Orchestrator changes:**
  - VOL-V-29.2-01 gained an ADD-01 interpretation;
  - T1-1-B and T1-1-D now point to the Technical Proposal;
  - VOL-I-11.2-01 has a `no_deliverable` reason;
  - VOL-II-4.4-01 and VOL-II-T2-4-TN are now `scored`;
  - the 26 core rows got role owners (`Bid manager`, `Commercial lead`, `Technical lead`, `Legal counsel`) in place of the bare discipline, so all 202 rows use one vocabulary.
- **"Outside the slice" replaced by treatment.** Every ADD-01 and ADD-02 provision is now an op or a `no_effect` disposition with a reason. For example:
  - ADD-01 Q1, Q4 and Q6 annotate VOL-V 29.1–29.5;
  - ADD-02 Table 1-1 note (3), Q7 and Q10–Q14 annotate their clauses;
  - each cover paragraph that creates an obligation is an `annotate` op with `adds_obligation`.
- **Model use:** these rows were drafted by the assistant's subagents, which are model output. They are PROPOSED; none is accepted. "Model integrations" in the product (§4.6 of the plan) remain deferred.

### 5.3 Results on the real pack

- **Units:**
  - 524 units in total;
  - all 421 volume units have a disposition;
  - the 76 addendum provisions are covered by C20 (ADD-01 36, ADD-02 40), and the other 27 addendum units are structural;
  - disposition problems: 0.
- **Rows:** 202 (82 scored, 58 pass/fail, 43 contractual post-award, 19 procedural). Every row has an owner, evidence or a no-deliverable reason, and a status at BASE, ADD-01 and ADD-02.
- **Sweeps:**
  - 163 obligation hits;
  - 45 consequence hits (43 English, 2 Arabic: Form 4-C declaration 4 and its note), all linked, so C15 has no findings;
  - C14 lists 16 obligation words in non-requirement units for a person to confirm.
- **A3:**
  - 18 explicit consequences, grouped by class: rejection 5, disqualification 2, non-responsive 10, exclusion (Arabic only) 1;
  - plus the Envelope B score threshold;
  - 36 pass/fail rows with no stated consequence, listed as linked ids;
  - three documents referenced but not supplied, with their impact: the Environmental Permit, Volume III (Drawing 03-C-114), and the parts of VOL-V not supplied.
- **Release state:**
  - stale: 3 rows (VOL-I-8.3-01, 3.4-01 and 6.7-01). Their dates hang on the Proposal Due Date, which ADD-01 moved. The dates are recomputed (2026-11-26), but the readings were made before the change and need a person. They were not refreshed.
  - approval: two image readings pending, 202 rows and 37 ops not accepted.

### 5.4 Tests added late

Two tests were written after their code, so they are not failing-first tests. Each was checked against deliberate mutations and caught every one.

- **`test_consequence_sweeps_catch_an_unlinked_consequence_in_english_and_arabic`** (`tests/test_session05_release.py`). While writing the plan I found that no test showed C15 catching an omission. It caught all four mutations:
  - empty Arabic lexicon;
  - empty English lexicon;
  - C15 dropped from the release gate;
  - Arabic hits discarded.
- **`test_a_changed_period_is_re_read_or_left_unplanned_never_kept_silently`** (`tests/test_session05_review.py`). This is the fast test for E46. Before it, only the slow drill B test covered the re-read, and the "no date planned" path had no test at all. Writing it, I also simplified two duplicated branches in that code; the outputs were identical before and after. It caught all three mutations:
  - changed words never noticed;
  - a date planned when the period cannot be re-read;
  - no re-read.

## 6. Stage 4: A5 (subagent, checked by the orchestrator)

- **`programme.py`** builds on the schedule:
  - documents per envelope, with multiplicity (members, signatories, reference plants), issuer, physical count and USB;
  - resource load per ISO week against PROVISIONAL capacities;
  - infeasibility drivers, which say what would make each one feasible;
  - scenarios that apply overrides to the assumptions and compare the results.
- **Real pack at the status date of 22 Oct 2026** (ADD-02 issue):
  - 41 activities: 38 OK, 2 INFEASIBLE, 1 DEADLINE PASSED;
  - LCC certificate: INFEASIBLE by 7 WD. It becomes feasible if the lead time is at most 23 WD, or the PDD is on or after 2026-12-07;
  - LCC ratio: INFEASIBLE by 12 WD;
  - attendance notice: deadline 14 Oct, DEADLINE PASSED (whether it was done needs recording);
  - Envelope A: 16 items, 108 physical copies. Envelope B: 4 items, 16 physical copies. Envelope B holds "only" Form 4-F and the Financial Model (VOL-I 10.1) against 10.3/10.6, an open issue;
  - 15 provisional resource overloads, in weeks 45–48.
- **Scenarios** (`out/a5/scenario_comparison.*`):
  - **2 members:** 92 physical copies in Envelope A;
  - **4 members:** 124 copies;
  - **LCC in 15 WD:** both LCC activities OK;
  - **hypothetical holidays** (15–18 Nov, labelled HYPOTHETICAL; none declared in the pack): LCC short by 11 WD, and four more activities become INFEASIBLE;
  - **combined:** the LCC ratio is 1 WD short.
- **Rework detection widened (this session):** an activity is REWORK when its requirement's text, cells or staleness change, as well as its interpretation or dates. On drill A this adds "technical-proposal REWORK" for the Table 2-4 TP change, which was previously missed.

## 7. Release gate, working drafts and A3

- **`release_blockers`** has three kinds:
  - **coverage:** PARTIAL addenda, dispositions, C15, register files;
  - **stale;**
  - **approval:** pending readings, rows and ops not accepted.
- **Working drafts:**
  - `outputs` publishes a WORKING DRAFT with the blockers listed in `checks.json`, the A1 banner and the A3 subtitle;
  - `outputs --strict` refuses the release with exit 3, keeps the previous outputs, and writes the candidate to `<out>.rejected` with `RELEASE_REJECTED.md`.
- **On the real pack** (disposable directory): exit 3. The blockers were stale 3, approval (2 readings), 202 rows and 37 ops.
- **The program never approves or accepts anything:**
  - no `curation/approvals.yaml` was created;
  - no review status was refreshed;
  - test approvals happen only in disposable copies, under "Fixture Test Reviewer".
- **A3:**
  - one page;
  - body text never below 7.5 pt (render refuses below scale 0.9); the real pack renders at 8.08 pt;
  - items link to `a3_detail.html#ID`, which carries the full quote, source and flags;
  - after saving, links are rewritten from /Launch to /URI so PDF viewers follow them.

## 8. Drill B: rehearsal of a second Addendum No. 3

**Fixture** (`tests/fixtures/make_drill_b.py`, subagent; curation in `tests/fixtures/drill_b/` by the orchestrator acting as the live-session curator). Synthetic, not tender content. Provisions:

| Provision | What it drills |
|---|---|
| 2.1 | **Two changes in one paragraph:** VOL-I 5.2, clarification period 10 → 7 WD; VOL-I 7.1, validity 150 → 180 days |
| 3.1 | **A new obligation** with a consequence, amending no clause (certificates of good standing per member, non-responsive) |
| 4.1 | **An image-table change:** Table 2-4 TSS limit 10 → 5 |
| 5.1 | **Unseen in ADD-01/ADD-02:** a whole clause deleted and replaced by quoted text (VOL-I 6.7) |
| 6.1 | **Unseen in ADD-01/ADD-02:** a new clause inserted after an existing one (VOL-I 4.4 after 4.3) |
| Q15 | Quotes the period that 2.1 replaces |
| Q16 | Negative control: cites VOL-I 6.4, which ADD-03 does not change |

**Run** (`make rehearsal` → `out-drill-b/`; no review of any kind in the committed run):

1. Built and ingested: 0.16 s and 12.8 s. 545 units; C01–C10 pass.
2. **Drafted run**, with no op file. Before the live fix, the drafter left 3.1, 5.1, 6.1, Q15 and Q16 unresolved.
3. **Live fix**, as in the session. The drafter learned two patterns, with a test (`test_drafter_handles_a_whole_clause_replacement_and_a_new_clause`):
   - a whole clause "deleted and replaced by the following: '…'", which becomes `replace_text` of the whole clause plus an issue: "compare the old and new text for anything dropped";
   - "The following Clause X is added to Volume Y after Clause Z: '…'", which becomes `insert_unit`.
   
   Re-run: 2.1(a) and 2.1(b) drafted as two ops, plus cover/para3, 4.1, 5.1 and 6.1. Unresolved: 3.1, Q15 and Q16. ADD-03 is PARTIAL, so the validated state stays ADD-02 and the outputs are labelled WORKING DRAFT. Outputs took 12.3 s.
4. **Curated run.** The curator wrote:
   - 3.1, as an annotate `adds_obligation`;
   - Q15, as `no_effect` with a reason; A2 lists it for review;
   - Q16, as a clarification annotation on VOL-I 6.4;
   - rows `ADD-03-3.1-01` and `VOL-I-4.4-01`;
   - evidence item EV-GOOD-STANDING, its template and a PROVISIONAL lead time.
   
   `pin` pinned only the unpinned new interpretations. Result: ADD-03 APPLIED (8 ops), validated stage ADD-03. Outputs took 12.4 s.

**What the curated run shows:**

- **New rows:** ADD-03-3.1-01, NEW at ADD-03, non-responsive, on A3 citing "ADD-03 3.1 p…"; VOL-I-4.4-01, NEW.
- **Affected activities** (`out-drill-b/out-curated/a5/replan_deltas.*`):
  - good-standing NEW;
  - clarifications MOVED and REWORK: the cut-off is 2026-11-17, with the period re-read as 7 WD from the amended text and flagged for a person;
  - form-4a REWORK: validity now runs to 2027-05-25. The Proposal validity (180 days) now equals the Bid Bond's 180 days (VOL-I 6.3), where the bond previously outlasted it by 30 days. That is an observation for a person; drill only;
  - technical-proposal REWORK (TSS);
  - spoc REWORK (the new Clause 4.4);
  - bond-approval and bond-issue REWORK (the Q16 clarification reaches the 6.4 rows).
- **Stale dependencies:** 9 rows are STALE at ADD-03:
  - VOL-I-5.2-01 and 7.1-01 (2.1);
  - VOL-I-6.4-01 and 6.4-02 (Q16);
  - VOL-II-T2-4-TSS (4.1), and VOL-V-29.3-01, which depends on the TSS row;
  - VOL-I-6.7-01 (replaced by 5.1; already STALE since ADD-01);
  - VOL-I-8.3-01 and 3.4-01 (carried from ADD-01).
- **Preservation of an earlier approved state.** This is shown only in the disposable run of `tests/test_drill_b.py`, where "Fixture Test Reviewer" approves the Table 2-4 reading and accepts two rows before ADD-03 is applied:
  - the reading's approval is preserved, while the TSS row's interpretation turns STALE;
  - accepted VOL-I-5.2-01, which ADD-03 changed, keeps its acceptance but is STALE, and the release gate names it;
  - accepted VOL-I-9.3-01, which ADD-03 did not touch, stays accepted and current;
  - after that approval, the only pending reading is VOL-IV.
- **A defect found while making the rehearsal reproducible:** a rerun could draft against the previous run's curated `ADD-03.yaml` or fixture approval. `rehearse()` now removes both before drafting (E48). A rerun into the same directory drafted the same three unresolved provisions.

## 9. Errors in this session (continuing from E34)

| # | Error | Found by | Resolution |
|---|---|---|---|
| E35 | The five findings (§2), all in my session 04 code | The owner's review | Fixed (§4) |
| E36 | Four of the five subagents stopped at an API usage limit (the VOL-I agent had finished) | Their completion notices | Resumed with their context after the reset; their files checked as in §5.2 |
| E37 | My own ADD-01 Q6 op was rejected by C22: it cites "Volume V Clause 29", which the resolver could not map | Running the build | Whole-clause citations expand to their sub-clauses |
| E38 | My new "replacement printed after the provision" check rejected ADD-01 Appendix A, whose heading is printed before the provision | Running the build | Headings excluded from that check |
| E39 | The C44 detail was cut at four items, hiding which deliverables were missing (EV-LCC among them) | Integrating the register agents' rows: the build failed C44, as it should have, until the A5 templates caught up | Every missing item listed |
| E40 | `check-register --doc VOL-I` also matched VOL-II and VOL-IV | Reading its output | Exact document filter (`mine()`) |
| E41 | As the rows arrived, A3 shrank to scale 0.695 (about 5.9 pt text), unreadable; after the redesign the footer no longer fitted | The A3 scale in the build output, then rendering the page | Grouped by class, compact items linked to the detail page, minimum 7.5 pt enforced; footer box and wording resized |
| E42 | Relative links in the A3 PDF were written as /Launch actions, which viewers block; my first conversion left some, because it deleted links while iterating over them | Inspecting the PDF objects | Rewritten to /URI after saving, one link at a time; tested (no /Launch left) |
| E43 | `bidder_basis` entries written as dicts broke the A1 Assumptions sheet | Building A1 | Flattened to text |
| E44 | Drill B: my template named resource "Legal counsel" instead of the role key `legal_counsel` (C45 failure) | C45 | Fixed in the fixture |
| E45 | Drill B: my curation step edited the drill's `pack.yaml` after ingest (E01: inputs changed) | E01 | `prepare()` points the pack at its own copies before ingest; curation only adds files |
| E46 | Drill B: the clarification cut-off did not move when 2.1(a) changed 10 → 7 WD, because the period was typed in the row's date rule | The rehearsal's expected outcome | A date rule whose source words changed re-reads its period from the amended text and is flagged "period re-read …; needs a person" |
| E47 | Replan deltas missed REWORK when only the requirement's text, cells or staleness changed (drill A Table 2-4 TP, drill B TSS) | The rehearsal | Deltas widened; drill A now shows technical-proposal REWORK |
| E48 | A rehearsal rerun could draft against a previous run's curated op file or fixture approval | Adding the Makefile target | Both removed before drafting |
| E49 | The docstrings of `register_findings` and `dispositions.py` said C15 and the disposition checks were structural; they are release blockers and `check-register` failures | Writing the plan | Docstrings corrected; the plan says what is implemented (§4.7) |
| E50 | The 26 core rows had a discipline but no owner, so A1 showed "Technical" next to "Technical lead" | Counting owners for this log | Role owners added (§5.2) |

## 10. Results

- **Tests:** **289 passed** in 315 s (`pytest -q`, 18:19–18:25 UTC), up from 237 at the end of session 04. The 52 new tests are:
  - 21 in `test_session05_review.py`: the 19 failing-first tests, the live-fix test and the re-read test;
  - 8 in `test_session05_release.py`;
  - 18 in `test_programme.py`;
  - 5 in `test_drill_b.py`.
- **Determinism:** `build/` regenerated byte-identical to the committed evidence. `outputs` rebuilt into a disposable directory and was identical to `out/` (`diff -r`).
- **Commands:** `make evidence`, `make outputs`, `make drill` and `make rehearsal` all exit 0. Every output is a WORKING DRAFT.
- **Timings:**

  | Step | Time |
  |---|---|
  | Real-pack evidence | 13.5 s (with the fixture) |
  | Real-pack outputs | 11.4 s |
  | Drill A | 24.8 s |
  | Drill B rehearsal | about 38 s |

### What this does and does not establish

- **It establishes** that the code paths reject the five reproduced faults, that every unit and provision has a recorded treatment, and that the outputs are internally consistent and reproducible.
- **It does not establish** that any interpretation, owner, evidence item, lead time or disposition is right. Every one of them is a proposal: none is accepted, both readings are pending, and three rows are STALE. Passing tests are not a correct interpretation and not an approval.
- **Remaining gaps and the decisions for the owner:** `docs/session-05_report.md`.
