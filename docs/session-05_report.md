# Session 05: review fixes, Stage 3 and Stage 4 working drafts, rehearsal, decisions needed

Full record: `worklog/2026-10-02_session-05_review-stage3-stage4.md`.

Everything below is a **working draft**:

- every A1 row, amendment op, disposition, owner, evidence item, lead time and resource capacity was proposed by the assistant or its subagents and **not reviewed by a person**;
- both image readings are **still pending your review**;
- nothing has been approved or accepted, and no review status was refreshed;
- `outputs --strict` refuses a release in this state (exit 3).

Stopped before final submission.

## 1. Your five findings: all confirmed, none disputed

Reproduced on `160242f` before any change. Failing tests were written first (17 failed, 2 guards passed), then fixed.

| # | Before (reproduced) | After |
|---|---|---|
| 1 | TN set to 999, or written into the Unit column, passed. Table 1-1 could be replaced by the hydraulic Table 2-6. A failed annotation left its annotation behind. | **Values:** the provision must name the column and state the value with its unit. **Replacements:** content must come from the addendum and its title must name the target. **Failed ops:** every op is transactional, so a failed op changes no text, cell, status, history, annotation or dependency. |
| 2 | Two changes in one paragraph produced one op; the paragraph was marked covered. | One op per change (`2.1(a)`, `2.1(b)`). Any remaining text is flagged `unresolved` with the text quoted. |
| 3 | A unit's page changed to 99 in `units.json` passed. The pin ignored the image review fingerprint. | **Evidence:** every evidence file is verified against `BUILD_MANIFEST.json`, and each unit's pages against its anchors (E01 fails). **Pins:** they include the reading's review-subject fingerprint; a changed reading keeps dependants STALE after re-approval. |
| 4 | A3 cited the LCC consequence to VOL-I 8.6 p4; the wording is ADD-02's. | **Citation:** A3 now gives "ADD-02 9.1 p3 (reinstating VOL-I 8.6)". **Separate columns:** A1 keeps `original_text`, `effective_text`, `quote` and the latest `source` apart, and A2/A3 cite the consequence's own page and amendment. |
| 5 | Removing the LCC template made its activities vanish, and the build passed. | Both directions are now structural: **C40** (activity needs a row), **C44** (needed deliverable needs activities or a justified exception) and **C45** (dependencies, lead times and roles defined). |

## 2. Working outputs

| Output | Files | What to look at |
|---|---|---|
| A1 | `out/a1/a1.xlsx` (and `.csv`, `.json`) | **Rows:** 202, each with owner, evidence, status at BASE / ADD-01 / ADD-02, original vs effective text, quote and latest source. **Sheets:** Dates, Assumptions. |
| A2 | `out/a2/a2.md` (tables as CSV/JSON) | Every ADD-01 (36) and ADD-02 (40) provision treated: op, or no effect with a reason. Nothing is "outside the slice". Rows that move, with reasons; answers to review. |
| A3 | `out/a3/a3.pdf` plus `out/a3/a3_detail.html` | **Layout:** one page, smallest text 8.08 pt, grouped by consequence class. **Content:** 18 explicit consequences (rejection 5, disqualification 2, non-responsive 10, exclusion in Arabic only 1), the Envelope B threshold, 36 pass/fail rows with no stated consequence, and the missing documents with their impact (Environmental Permit, Volume III / Drawing 03-C-114, the rest of VOL-V). **Detail:** each id links to the detail page. |
| A5 | `out/a5/programme.csv`, `marshalling.csv`, `documents.csv`, `resources.csv`, `drivers.csv`, `scenario_comparison.csv` | **Coverage:** both envelopes, with issuers, multiplicities, physical counts and dependencies. **Assumptions:** resources and lead times are labelled PROVISIONAL (value, basis, owner). **Outputs:** what drives each infeasibility, and the scenarios. |

**Coverage:**

- All 421 volume units have a disposition (requirement, consequence, duplicate, definition, authority, informational, context or structural).
- The consequence sweep found 43 English and 2 Arabic hits, all linked to a row; nothing unlinked.
- The obligation sweep lists 16 obligation words in non-requirement units for you to confirm (`tenderpack check-register`).

**A5 at the 22 Oct status date:**

- **LCC certificate:** INFEASIBLE by 7 WD. It becomes feasible at a lead time of 23 WD or less, or a PDD on or after 7 Dec.
- **LCC ratio:** INFEASIBLE by 12 WD.
- **Attendance notice (14 Oct):** DEADLINE PASSED; record whether it was sent.
- **Envelopes:** A has 16 items and 108 physical copies; B has 4 items and 16 copies.
- **Resources:** 15 provisional resource-week overloads (weeks 45–48).

**Scenarios (the changes flow through):**

| Scenario | Effect |
|---|---|
| 2 members | Envelope A copies 108 → 92 |
| 4 members | Envelope A copies 108 → 124 |
| LCC in 15 WD | both LCC activities OK |
| Hypothetical holidays 15–18 Nov (labelled hypothetical; the pack declares none) | LCC short by 11 WD and four more activities infeasible |
| Combined | LCC ratio 1 WD short |

**Release state** (`out/checks.json`): the structural checks pass. The blockers are:

- **stale:** VOL-I-8.3-01, 3.4-01 and 6.7-01. ADD-01 moved the PDD their dates hang on; the dates are recomputed, but the readings need a person.
- **approval:** both readings pending; 202 rows and 37 ops not accepted.

## 3. Rehearsal: drill B (`out-drill-b/`, `make rehearsal`)

A second synthetic Addendum No. 3. It is not tender content.

**Timings:** build 0.2 s, ingest 12.8 s, drafted outputs 12.3 s, curated outputs 12.4 s.

| Provision | Drafted (no op file) | Curated |
|---|---|---|
| 2.1 two changes in one paragraph (VOL-I 5.2 10 → 7 WD; 7.1 150 → 180 days) | two ops, `2.1(a)` and `2.1(b)` | the same |
| 3.1 new obligation (certificates of good standing; non-responsive) | unresolved | new row `ADD-03-3.1-01` (on A3), evidence item, A5 activity `good-standing` |
| 4.1 Table 2-4 TSS 10 → 5 (image table) | `set_value`, old value from the pending reading | the same; TSS row STALE |
| 5.1 whole clause deleted and replaced (**not seen in ADD-01/02**) | unresolved before the live fix; `replace_text` of the whole clause after it, with "compare for anything dropped" | the same, and the issue names what was dropped (modification before the PDD) |
| 6.1 new clause inserted (**not seen in ADD-01/02**) | unresolved before the live fix; `insert_unit` after it | new row `VOL-I-4.4-01` |
| Q15 quotes the replaced period | unresolved | no effect; listed in A2 for review (not revoked) |
| Q16 negative control | unresolved | a clarification on VOL-I 6.4 (its rows go STALE); not listed as an answer to review |

**Drafted run:** PARTIAL. The validated state stays ADD-02 and the outputs are labelled WORKING DRAFT.

**Curated run:** APPLIED.

- **Affected activities:** good-standing NEW; clarifications MOVED and REWORK (cut-off 17 Nov, period re-read from the amended text and flagged); REWORK on form-4a, technical-proposal, spoc, bond-approval and bond-issue.
- **Stale:** 9 rows.
- **Earlier approved state, preserved:** shown only in the disposable test run, where "Fixture Test Reviewer" approved the Table 2-4 reading and accepted two rows. The reading's approval is kept while its row goes STALE. The accepted row ADD-03 changed keeps its acceptance, is STALE, and blocks release. The accepted row it did not touch stays accepted and current.

**Defects found and fixed during the rehearsal:**

- the cut-off did not move, because the period was typed in the row;
- REWORK was missed for text and cell changes;
- a rerun could draft against the previous run's curated file.

## 4. Remaining gaps

1. **Nothing is reviewed.** All 202 rows, the 37 real-pack ops, and every disposition, owner, lead time and capacity are proposals, and the release gate stays closed until people accept them.
2. **Both image readings are pending.** The TN, TP and TSS values and the Form 4-C consequences depend on them.
3. **Three STALE rows** (VOL-I 8.3, 3.4, 6.7) need a person to confirm the reading against the moved PDD.
4. **Checks not built:**
   - C12 (row ids never disappear between builds);
   - C28 (cover-summary cross-check);
   - C29 (apply only accepted ops; deviation kept, see D8);
   - C30 (every date phrase mapped);
   - C32 (counting convention declared);
   - C41.
5. **Dates:** a "months" offset cannot be expressed. "Twelve (12) months" is modelled as 1 year.
6. **A5 assumptions are provisional.** The overloads come from assumed capacities, and copy counting per envelope vs per Proposal is open (I-VOL-I-COPIES).
7. **Open content questions** (issues, with owners):
   - Envelope B "only" vs 10.3/10.6;
   - prices in Envelope A vs Form 4-B contract values;
   - the reissued Form 4-A drops fields and confirmations and still prints 12 Nov;
   - the bond long-stop;
   - the concession term;
   - design flows;
   - Table 2-4 tensions;
   - VOL-V is an extract (contractual rows cover only what is supplied);
   - the ESIA and geotechnical report are not in the pack.
8. **Not done:**
   - a blind addendum written by someone else (Stage 5);
   - packaging and the offline Mac verification (Stage 6);
   - model integrations (deferred, as you asked).

## 5. Decisions needed from you (in priority order)

1. **Image readings:** approve or correct Table 2-4 and Form 4-C yourself (`build/review/*/packet.html`, then `tenderpack approve REGION --reviewer "Your Name"`).
2. **LCC certificate:** the lead time and issuer. It decides the main infeasibility: feasible at 23 WD or less; the ratio chain needs 18 WD or less.
3. **How to accept rows and ops (D8):** edit `review: accepted` per row and op, or a `tenderpack accept` command that records a named reviewer (recommended). Then review, starting with the 18 A3 rows and the 37 ops.
4. **The three STALE rows:** confirm the readings against the 26 Nov PDD, so they can be re-pinned with `pin --rows ROW@ADD-02,...` after your review.
5. **Legal calls** before the 12 Nov clarification cut-off:
   - the Form 4-C "exclusion" category;
   - what to print on Form 4-A, and whether to seek clarification;
   - Envelope B contents;
   - prices in Envelope A;
   - the concession term;
   - the Volume III / Drawing 03-C-114 gap.
6. **A5 assumptions (D9):** the consortium size (3 by default), the copy-counting convention, lead times and team capacities.
7. **Next stage:** accept Stage 3 and Stage 4 as the basis for packaging, or say what to change. Final submission has not been started.
