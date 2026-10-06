# Session 12 report (5 Oct 2026): ready to run, with the decisions that remain yours

For the owner. The full record is `worklog/2026-10-05_session-12_ready-to-run.md`; your message is kept verbatim in
`worklog/2026-10-05_session-12_prompt.md`. **A progress commit `cfaac79` was made and pushed at 13:38 UTC on your
authorisation ("commit progress now and continue the work fully and commit once done"); the closing commit is
the head of branch `claude/hopeful-curie-7oki9q` at the end of the session, made after this text was written, so its hash is not in it (`git log -1`).** Nothing was sent to anyone, no clarification question was sent, and no row, op, reading,
relationship, issue, clarification entry or proposal was accepted, approved or rejected by the program or the
assistant. Your confirmed readings, recorded decisions, labelled assumptions and unresolved questions are preserved.
Cost and pricing stay provisional (`docs/COST_AND_EFFORT.md`).

## 1. What you asked, what was done

| # | You asked | Done | Where |
|---|---|---|---|
| 1 | Close the legal/commercial review gap: failing regressions, then fixes across proposals, issues, clarifications and rendered outputs; valid evidence never validates a conclusion; human-owned questions settled only by a recorded decision | `tenderpack/human_owned.py` classifies human-owned items (closure and topic words, by item type, on the model's own wording); such an item is never `evidence_verified`; an existing CQ entry's status and an issue's resolution change only through `accept`/`reject` on CQ-/I- items bound to content (the workflow never calls them); HUMAN DECISION PENDING on the register, A3, A5, the candidate outputs and the review packet; the analysis phase holds confirms/interprets ops on such questions. 15 failing-first tests. The audit then found the same gap in the real outputs (the concession term) and it was fixed as a pending Legal decision everywhere | §4 (A1-1), `tests/test_session12_human_owned.py`, `tests/test_session12_content_wording.py` |
| 2 | Finish the unseen-addendum workflow from blind-05's comparison; time against 30 min without weakening checks; blind-05 as a labelled regression; a new sealed addendum; consecutive addenda; interrupted-run recovery | Clause lists and ranges resolved against the document structure (INCOMPLETE SCOPE flagged); one replacement across a clause and its items; same-addendum targets; precedence between renderings; cover discrepancies retained as cover findings while the operative change proceeds; one change predicate following dependencies and printed anchor dates (confirmations never hide a change); "not reached" counts unresolved citations; issue references checked; the closed clarification window said everywhere; superseded answers listed for re-reading; image-table readings as rows conditional on approval; computed deadlines into A5 with their derivation; switched conditions and changed definitions to their rows; derived consequences only from an existing rule, held for a person. Bounded concurrency with a run-scoped lock and a shared rate gate; prompts 14 % smaller. The rehearsals: §3 | §3, §4 |
| 3 | A genuinely offline Mac version: explicit offline mode for every phase, local critic or a visible gap, capability checks, no automatic downloads, setup and launcher, Mac checks pending | `tenderpack/ai/offline.py` (`--offline`, `offline: true`, `TENDERPACK_OFFLINE=1`): hosted routes refused before any process or call; the critic local or recorded "did not run"; Ollama capability, context and memory checks, never a pull; `tenderpack ai routes`; the same validation on every route; Codex wording corrected; `scripts/mac/setup.sh`, `launch.command`, `checks.sh`, `docs/MAC_SETUP.md` with the ten Mac-only checks marked PENDING ON THE MAC | `docs/MAC_SETUP.md`, `docs/AI_ROUTES.md` §17–18 |
| 4 | An independent audit of the real submission through ADD-02, rendered files included; fixes and rechecks; the matrix; decisions in groups; the A4 history correction drafted | Six reviewers (A1, A2, A3, A4, A5, R) deriving expectations first: 1 blocking (found by three of them), 11 major, 22 minor; four fixers and the coordinator; rechecks by the same reviewers: done: 46 matrix rows after the rechecks (41 PASS, 3 FAIL all fixed by F5, 2 PENDING for you), the decision groups in §6, the A4 erratum as a draft for you. The erratum drafted and corrected on seven points for your review (`docs/drafts/ERRATUM_A4_history-disclosure_DRAFT.md`), not applied | §4, §5, §6 |
| 5 | The local control panel on real jobs, after the core corrections and the audit | built and merged (`tenderpack panel`, standard library only, 127.0.0.1 with a token per start); a usability pass on your words of 18:34: the deliverables first with open/download, a new addendum in one form, a self-refreshing run page with the review packet first, Runs and Jobs saying what each needs; 19 tests pass here (loopback, token, traversal, uploads, output parity, upload-to-results on the recorded route, resume after SIGKILL, candidate isolation, the decisions form); the browser, `--open`, launcher item 7 and a real run from the panel are PENDING ON THE MAC | `docs/PANEL.md` |
| 6 | The handover: regressions, the suite, a fresh rebuild, strict and offline checks; a labelled snapshot; the archive's rehearsal list; report, guide, log; nothing committed | `scripts/make_snapshot.py` (base revision, uncommitted-change disclosure, diff, manifest; the archive's clean-commit refusal kept); the archive takes every rehearsal with a comparison and every session report; verification: §7 | §7, §8 |

## 2. Models that actually ran

- The coordinator: Fable 5.1 (this session's configured model, as the session reports it).
- Subagents (launched with the Opus option; each reported Opus 5.5 by its own instructions, which the launching
  session cannot verify): five implementers W1–W5, the blind-06 author, six audit reviewers, their rechecks, six
  fixers F1–F6 (F2 twice), the panel agent P and its usability follow-up, and the blind-06 scorer S. Every brief and follow-up message is exported verbatim to `worklog/subagent_briefs/` (45 on).
- The headless host sessions of the rehearsal runs: `claude -p --model opus`; the CLI reported `claude-opus-5-5`
  (`staging/ai/runs/*/ai/*/session.json`).
- No API-key call was made; the Ollama route ran only against a fake local server in tests (pending on the Mac).
- The host plan's session limit stopped the work twice (11:49–12:30 and 13:57–17:30 UTC); the pauses are in the log.

## 3. The rehearsals

Every rehearsal is an Addendum No. 3 one; the stacked Addendum No. 4 was dropped on your instruction of 18:34 UTC (its
run was stopped at 18:35:19 in its analysis step and is not scored; the consecutive-addenda code, tests and guide stay).
Counts are reported separately, never merged into one number.

**Blind-06, sealed, timed (the live exercise).** An independent author (a separate agent, started cold) wrote a 5-page
Addendum No. 3 on the base pack with a sealed key (`rehearsals/blind-06/FROZEN.md`, 09:53 UTC, before anything was
ingested); the run happened on the frozen tree with every core correction of the session merged and two host sessions
in flight (`max_parallel_sessions: 2`): `ADD-03-run-host-blind06-20261005T173226Z`, 17:32:26 to 18:28:15 UTC.
The first outputs were frozen by hash (367 files) before the key was copied into the folder and opened; the scorer (an
agent that had seen neither the run nor the key before) wrote `rehearsals/blind-06/COMPARISON.md` (507 lines, every
row citing a frozen file and line) and verified every hash itself.

| Measure | Result |
|---|---|
| Detection, N = 35 (13 provisions, 6 answers, 3 planted cover errors, 3 Arabic items, 10 secondary effects) | **20 hit, 14 partial, 1 missed** (provisions 6/7/0; answers 4/2/0; cover errors 3/0/0; Arabic 3/0/0, 30 of 31 strings verbatim; secondary effects 4/5/1, the miss: an ADD-01 answer whose basis the addendum overturned) |
| Other key tables | indirect effects 1 hit / 5 partial / 2 missed; missing evidence 2 / 0 / 1; the no-correct-answer ambiguity partial, the inconsistency and both judgment items hit; dates 5 right / 1 partial / 2 missed; marshalling 4 / 1 / 0; 23 of 23 "must not report" traps avoided (2 borderline); 3 false positives, 5 false signals |
| Usable updates, of 34 detected effects | **17 applied as is, 5 applied in part, 12 detection only, 0 applied with wrong content**; one promoted group would mislead if accepted as is (two `no_effect` dispositions settle table notes whose obligations reached no row because a check rejected the rows) |
| Missed effects | 1 of 35 (above), each miss in the other tables with its reason in `COMPARISON.md` §3 (a row type the validator refused, a batch boundary, a quote against the printed rather than the amended text) |
| Pending decisions | no judgment the key reserves for a person was made by the system; several points the documents settle were handed to a person instead (over-escalation, listed by name) |
| Manual interventions | **none** (15 automatic host sessions, each recorded "not a person"; every batch ran once) |
| Time, PDF to candidate outputs and review packet | **55 min 49 s** wall clock (the steps add up to 3,345.6 s: analysis 2,170.6 s in ten batches, downstream 838.9 s, the one image reading 211.4 s) against the brief's 30 minutes: missed by 25 min 49 s; 16 min 38 s faster than blind-05 (72 min 27 s, one session in flight, 54 provisions against 70 here). The second session bought about 31 minutes of overlap; what did not speed up: the lone image reading, each session's own latency (3–8 min), in-order collection with the critic inside it (the second slot idle about 8.7 min), downstream waiting for all of analysis. The scorer's estimate: about three sessions in flight on average to reach 30 minutes. |

The scorer's 14 general workflow defects (`COMPARISON.md`, "Follow-ups"): the coordinator itself fixed eleven of the fourteen points (or parts of them) during the plan pause, failing tests first in `tests/test_session12_blind06_coord.py` (a provision with an escalated sibling stays unresolved and in the packet's first section; a clarification quotation matching the words as amended is verbatim; a typed `replace_requirement` with a validator message naming the field; an image region whose blocks are provisions as a cited unit; opposite treatments of one unit across batches make both items conflicting, and a `no_effect` on an obligation no row carries is a person's decision; an "adds/introduces" cover claim done by an amendment that only adds words; a cover annotation's words kept out of C46; an exclusion the clause already makes confirms; the re-read trace started from inserted units; free-standing provisions given their row path in the packet's instructions); the rest (the computed-date path, the downstream-reversal check, the staleness pin on a confirming annotation, over-escalation, out-of-order collection) were F6's: F6 (relaunched 21:12 after the owner's limit reset, 56 min; 14 failing-first tests in `tests/test_session12_blind06_fixes.py`) did the rest: a confirming annotation no longer changes a unit's pin (pin format 3, the real pack re-pinned, packs pinned under format 2 read right without re-pinning), the computed-date task carries a date rule the register accepts and the programme's milestone shares its fingerprint (forward periods with no counting rule say so instead of being silent), a point a clause settles is re-presented as the clause's own words applied rather than a decision for Legal, a downstream item that reverses an analysis conclusion is marked conflicting, and the next batch is asked before a batch's critic runs; collecting results out of order is left as the owner's decision (the documented sequential-result invariant) (its open points: §6 items 38–42).

**Blind-05 as a labelled post-key regression, with the interrupted-run demonstration.** Three attempts, all labelled post-key (the first at 11:48
exposed the run-scoped lock defect E139, fixed; the second at 13:03 ran the readings and nine analysis batches with two
sessions in flight in 25.5 minutes before the workspace-staleness guard stopped it because the tree had been changed
under it, the coordinator's error E145; the third started 18:35:35 on the frozen tree, was interrupted by SIGTERM after
its third analysis batch at 18:48:25, its status recorded, and resumed at 18:48:31 with the dead process's lock taken over.) The third attempt is the regression of record: it started 18:35:35 on the frozen tree, was interrupted by SIGTERM at 18:48:25 after its third analysis batch (exit 143), its status recorded (`run-status`: analysis running, batches 1–3 done), resumed at 18:48:31 with the dead process's lock taken over and continued from batch 4 without re-asking a done batch, deferred as designed at 18:55:14 when the host plan's limit hit (exit 5), resumed a second time at 21:11:05 after the owner's reset (two sessions in flight throughout: a resumed run keeps the concurrency its checkpoint records, 2, whatever `config/ai.yaml` says at the time; E155) and ended at 22:10:34 with exit 0: status partial, 17 provisions unresolved against the session-11 sealed run's 23, 27 downstream tasks answered only by unpromotable items; the steps add up to 4,171.2 s (analysis 2,529.0 s against the baseline's 2,676 s, downstream 1,315.8 s against 1,260 s), a figure the interruption and the deferral make incomparable with the baseline's 72 min 27 s of wall clock (one session in flight in session 11, two here). Scored against the opened key by S (`rehearsals/blind-05/REGRESSION-S12.md`): **26 hit, 12 partial, 0 missed of the key's 38 items** (the session-11 sealed run: 21, 16, 1); the indirect effects 1 hit, 5 partial, 2 missed of 8 (0, 5, 3); the dates 7 right, 3 partial, 0 missed of 10 (5, 4, 1); the 19 traps avoided as before; 1 false positive, the session-11 defect in a smaller form (the modification cut-off planned on the PDD as if 2.1 had not moved it). **Usable updates:** 19 ops, 21 dispositions, 1 new row, 19 readings, 3 issues and 4 activities promoted, all PROPOSED (session 11: 12 ops, 19 dispositions, 2 rows); of the 38 items 22 applied so that a person could accept them as they are, 9 applied in part, 7 detection only, the one wrong application inside 2.1 (that cut-off date). **Missed effects:** none of the 38 without a trace (session 11's two misses now have one); IE5, IE8, D3 and ME2 missed outside the 38; the detected-but-not-applied items have recorded reasons: analysis `row_new` items are never promoted and the printed reason is empty, the register refused the date-rule kind "deadline" (F6's item 5 landed after this run), two clarification drafts failed the verbatim check, one row held on a bidder fact, one held by the new consistency check. **Pending decisions:** 17 unresolved provisions, each ending with the closed-route sentence; 0 analysis escalations (session 11: 8); 14 downstream items escalated and 9 conflicting; HUMAN DECISION PENDING on 17 analysis and 13 downstream items; D1 (both horns, Commercial) and D2 handled as the key wants, D1 better than session 11; three points the key settles were still handed to a person (the Arabic precedence called a legal question downstream, the cover against 6.6, VOL-II 3.2's applicability), the kind F6's item 12 re-presents as applied rules (merged after this run); **no system judgment the key reserves for a person.** **Interventions:** the planned SIGTERM and the two resumes, by the coordinator's scripts; no content edited between the PDF and the outputs; 18 automatic host-session interventions recorded; analysis-004 asked three times and 005 twice (the SIGTERM-killed and the 429-ended starts), about 12 minutes of two sessions' work discarded at the deferral (four staged proposal sets unused); downstream-001 repaired once. **Time:** steps 4,171.2 s (analysis 2,529.0 s of which 401.9 s discarded, downstream 1,315.8 s, readings 186.8 s, critic 67.8 s); wall clock 3 h 34 min 59 s including the 2 h 15 min 51 s deferral; the three running segments 79 min 2 s (12:50, 6:43, 59:29) against the baseline's 72 min 27 s, not comparable (the interruption lost the first segment's analysis time; two sessions in flight here against one in session 11). **Ten general defects** recorded by S for the next session (`REGRESSION-S12.md`, "Defects seen in this run"): the step timer loses a running step's time on SIGTERM; a session that submitted proposals and then ended with a 429 is discarded whole; analysis `row_new` items cannot be promoted and the reason is empty; an anchor rule with a working-day offset is planned on the anchor itself and a deleted row keeps its planning date; the "deadline" kind refused; "invalid" shown for a promoted row whose second proposal was invalid; a `replace_text` and an `annotate` on one unit treated as conflicting; one row promoted twice; the HUMAN DECISION PENDING words firing on statements of fact and settled precedence; and **the code changed between the run's segments** (the tree merged during the deferral; the checkpoint records no code version per segment), so no per-fix attribution is possible from the run's files: E154. S found no item where the key is wrong.

## 4. The audit: findings by deliverable, and what was done with them

Six reviewers derived their expectations from the brief, the email and the six source PDFs before opening any output,
then compared, inspected the rendered files (Chromium renderings, 150-dpi PDF pages, openpyxl) and judged human
ownership (brief §6). Severity: blocking (would mislead the assessors or a bid team), major (wrong but recoverable with
the page in hand), minor (presentation).

| Deliverable | Checked | Findings | Done |
|---|---|---|---|
| A1 | All 205 rows verbatim on the cited page (scripted); the 20 image-read rows against the crops; all 37 consequences; the status at every stage for all 205 rows, the amended text by hand for 40+; dates; xlsx = csv = json | 1 blocking (A1-1: the concession term decided by the tool), 5 minor | All fixed as proposals with the pack's words quoted; recheck recheck: every A1 row PASS (A1-11 with a note), the leftovers (the Q7 quote and chain link on VOL-V-42.2-01, the pending labels of I-FLOWS/I-F4G-NO, I-F4D-WORDING, the Assumptions-sheet id) fixed by F5 |
| A2 | All 37 ops verbatim (scripted); all 76 provisions; the 8.6 chain; every moved date recomputed; the Permit blocker; C28 on ADD-02's cover | 1 blocking (A2-1, the same), 3 major (CONFIRMED labels hiding the TN change and the Form 4-A printed date; the earlier-answers list), 3 minor | The predicate follows dependencies and printed anchors; the three labels now CHANGED with their cause; ADD-01 Q1 listed, 4.1/4.2 "REVERSED/REVOKED"; both readings of the ambiguous dates; three proposed relationships; recheck recheck: A2-1, A2-3, A2-4, A2-5, G-3, G-4 PASS; A2-2 FAIL on the two Q7 labels only, fixed by F5 (NOT SETTLED, Q7 read as `interprets`); A2-8 and the nits fixed by F5 |
| A3 | 16 triggers derived first, all on the page under the right category; A1 = A3 on 18 items; readability measured (7.72 pt, about 8,000 characters) | 1 blocking (A3-1, the same), 1 major (five unresolved lines without a reason on the page), 2 minor | Every unresolved line carries its reason; the legend; flags cite listed ids; both readings of the attendance date; after the merge the page fell to level 3 and was brought back to level 2 at 7.70 pt with every reason (E146); recheck recheck: all PASS (the concession line ⚑ with its legend, every unresolved line with a reason and owner, the legend, both attendance readings); the ⚑ rule, the gate count, the rule ids and ESIA fixed by F5; 25 lines at 7.7 pt, level 2 |
| A4 | Prompts against the transcript; model attributions; the error index; the records; the erratum draft; the commit records | 4 major (the register treating the concession term as settled; "(in the row)" for 110 index entries; a wrong row in this session's log; stale record lines), 1 minor | The index filled from the logs (90 cells), the log rows corrected (E141, E142), the erratum corrected on seven points; recheck recheck: A4-2..A4-5 and G-2 PASS, A4-1 PENDING (your decision on the erratum), the three one-line slips fixed; E148–E151 added since |
| A5 | The reviewer's own forward/backward pass over all 44 activities (no differences); four scenarios; resources; marshalling; lead times; the LCC infeasibility; the Gantt against the data (44/44, 12/12 milestones) | 4 major (the LCC lines unlinked to their question; VOL-V 36.2's change not reaching Form 4-E; a missing Form 4-E dependency; 41 in-force rows carried by no activity without a reason), 6 minor | All fixed: C48 now covers every in-force row (190 carried, 10 excepted with a reason, none uncarried); `ask_by` 11 Nov on the LCC question; the VOL-V volume check; form-4e after technical-proposal (floats 3 → 1 and 11 → 1); recheck recheck: all ten findings PASS, A5-7 PENDING (your lead times); N1 (the Q7 CONFIRMED), N2 (the question reach) and N3 (the coverage split) fixed by F5 |
| Rendering | All 14 HTML views rendered in Chromium; 257 links checked (0 missing); the Arabic in the browser and the xlsx; cross-document dates, statuses and classes | 1 major (R-1: three judgments presented as settled in the register's "checked, no question"), 6 minor | The register's six judgment entries moved to "Proposed readings, HUMAN DECISION PENDING" with an owner; one wording of the approval scope; batch headers from the data; the xlsx banner wrapped; a relationships legend; README caveats; recheck recheck: R-1, R-2, R-4, G-7, A3-1, A5-6 PASS, R-3 FAIL minor (the A2/A5 label pairs, ⚑ coverage, the confidence wordings) fixed by F5 with one label function and a regression over every A5 row; the Gantt cells and legend, the batch-04 cards fixed by F5 |

## 5. The brief-requirement-to-artifact matrix

After the fixers F1–F4 the six reviewers rechecked the rebuilt outputs (17:33–17:44 UTC): **46 matrix rows: 41 PASS, 3 FAIL (all minor or the single Q7 label residue), 2 PENDING (both yours)**. Every FAIL and every minor residue was then fixed by F5 (19:00) and merged; the last column says how. F5's fixes were not rechecked by the reviewers (the plan limit stopped the host models at 18:53); they rest on F5's 21 failing-first tests, the files it changed passing on the main tree, and the coordinator's render of the real pack (47 output files differ, as F5 reported). Before the fixes the six reports had about 40 PASS, 14 FAIL and 2 PENDING rows (`MATRIX_BEFORE` in the coordinator's scratchpad).

| Row | Reviewer(s) | After the rechecks | Evidence or note | After F5 |
|---|---|---|---|---|
| A1-1 every expectation a row | A1 | PASS | 205 rows; every expectation a row, a consequence or a disposition |  |
| A1-2 unique ids, one order | A1 | PASS | 205 unique ids, the same order in xlsx, csv, json |  |
| A1-3 verbatim text | A1 | PASS | 205 rows verbatim by script; 20 image rows against the crops; the four addendum quotes verbatim |  |
| A1-4 sources and pages | A1 | PASS | amended rows cite the amending provision and page |  |
| A1-5 the ADD-02 5.2 row | A1 | PASS | ADD-02-5.2-01 scored, with its reason |  |
| A1-6 discipline and owner | A1 | PASS | filled for all rows; one internal audit id left in the Assumptions sheet | the id moved to a YAML comment (F5) |
| A1-7 evidence vocabulary | A1 | PASS | 26 codes |  |
| A1-8 status at every stage | A1 | PASS | 205 statuses as expected; none changed by the fixes |  |
| A1-9 confidence | A1 | PASS | the concession rows equal (medium) with the pending decision stated |  |
| A1-10 xlsx = csv = json | A1 | PASS | 0 mismatches; the rendered spreadsheet not viewed (no LibreOffice here) |  |
| A1-11 interpretation boundaries | A1 | PASS (note) | held; minor: the pending labels of I-FLOWS/I-F4G-NO (R1-1) | the Issues sheet labels every issue a pending decision links; I-F4D-WORDING added (F5) |
| G-3 unresolved points given with reasons | A1, A2, A3 | PASS |  |  |
| G-4 no invented requirement | A1, A2 | PASS | no row without source or chain; the new relationships cite the documents or say inferred |  |
| G-5 every quoted word on its page | A1 | PASS | 2 superscript artefacts verified by eye |  |
| G-6 the tool decides no legal or commercial question | A1, A3 | PASS (decisions pending) | the concession precedence pending Legal, no decision recorded; I-PERMIT and T24 labelled; ⚑ coverage inconsistent (minor) | one pending rule everywhere; ⚑ on 12 lines (F5) |
| A2-1 ops verbatim | A2 | PASS | 37 ops, quoted words verbatim (script); deletion, reinstatement and revocation shown |  |
| A2-2 row labels right | A2 | FAIL | only VOL-I-12.1-01 and VOL-V-3.1-01 still "CONFIRMED by ADD-02/Q7"; the TN rows and Form 4-A CHANGED with their cause | NOT SETTLED "open: I-CONCESSION, human decision pending"; Q7 read as `interprets` (F5) |
| A2-3 ADD-01 Q1 | A2 | PASS | 4.1 REVERSED and 4.2 REVOKED in the addendum's words |  |
| A2-4 chains | A2 | PASS | correct; relationship causes printed |  |
| A2-5 every provision, dates, indirect effects | A2 | PASS | 76 of 76; LCC to 9.1(i), Form 4-E, Change in Law; the Permit blocker; both date readings |  |
| A3-1 one page | A3, R | PASS | 1 A4 page at 7.70 pt, readable with effort | 25 lines, 7.7 pt, level 2 after F5 |
| A3-2 bid-out requirements only | A3 | PASS | 16 of 16 triggers in the right category; the gate of 36 holds only pass/fail rows | I-NO-CONSEQUENCE's rows = the gate rows (F5) |
| A3-3 confidence | A3 | PASS | the same level as A1 for all 18; 6.2-02 points to its reason |  |
| A3-4 could not resolve, and why | A3 | PASS | all 24 lines carry a reason clause |  |
| A3-5 the owner's asks | A3 | PASS | reasons, abbreviations and folds fixed; minor: ⚑ rule, the gate count, ESIA, rule ids | the legend defines † and ⚑; clause names; ESIA written out (F5) |
| A4-1 the real commit history | A4 | PENDING | facts verified; the erratum draft accurate, complete and neutral; applying it is the owner's decision; the pre-rewrite commits may still be served by hash | unchanged: the owner's decision (§6 item 1) |
| A4-2 prompts and model calls | A4 | PASS | the session-12 briefs exported at the end of the session | exported (§7) |
| A4-3 every error and how it was caught | A4 | PASS | 90 of 90 cells verbatim for sessions 04–08; the 09/10 rule applied; E138–E147 indexed | E148–E150 added |
| A4-4 the log records errors | A4 | PASS | 156 indexed entries at the recheck | 159 at the end |
| A4-5 out/a4 a supporting record | A4 | PASS | the settled judgments of out/a4 fixed |  |
| G-2 defend every number (A4 part) | A4 | PASS | the cost note's title and total fixed |  |
| R-4 no stale statements (A4 part) | A4 | FAIL (minor) | three one-line slips (the 11:50 row, "151 entries", 13:36) | fixed at 17:41 |
| A5-1 every activity cites a row in force | A5 | PASS | 44 of 44; the reviewer's recompute reproduces everything |  |
| A5-2 dependencies and disciplines | A5 | PASS |  |  |
| A5-3 the four wrong lines | A5 | PASS | assemble-envelope-b, FORMS-01, 4.1 and 5.5 fixed |  |
| A5-4 scenarios | A5 | PASS | the baseline and all 7 scenarios reproduce |  |
| A5-5 marshalling | A5 | PASS | 26 lines; the LCC line carries CQ-LCC-ISSUER |  |
| A5-6 chart = data | A5, R | PASS | SVG, PDF and HTML equal the data; 44 of 44 rows, 12 of 12 milestones |  |
| A5-7 lead times | A5 | PENDING | the owner's lead times; LCC infeasible by 12 WD, not compressed; ask by 11 Nov shown | unchanged: the owner (§6 item 16) |
| A5-8 coverage | A5 | PASS | 200 = 190 + 10 (a labelling point, N3) | 160 discharged, 30 reviewed, 10 excepted (F5) |
| G-9 generated from the register | A5 | PASS |  |  |
| R-1 the spreadsheet readable | R | PASS | 8 sheets, nothing hidden, the banner merged and wrapped, 23 Arabic cells clean; not viewed in Excel or Calc |  |
| R-2 the PDFs readable | R, A3, A5 | PASS (minor) | a3.pdf 1 page, legible at 150 dpi, 42 of 42 links; gantt.pdf 1 A3 page, two status cells cut | the cells no longer cut, the legend printed (F5) |
| R-3 cross-document consistency | R, A5 | FAIL (minor) | ADD-01-AppA-01 CONFIRMED in A2 but REWORK in A5; VOL-IV-F4A-01/-02 NOT SETTLED in A5 only; ⚑ coverage; two confidence wordings | one label function for A2 and A5, a regression over every A5 row (F5) |
| R-4 no stale statements (rendered files) | R | PASS (minor) | the batch-04 header, the README caveats, the approval scope fixed; the apply command and "(below)" on batch-04 cards | fixed (F5) |
| G-7 §4 forbidden content | R | PASS | grep clean; the Gantt a plain chart |  |

## 6. Decisions that need you, in groups

Each entry: the source, what the outputs propose, the practical effect, and what is pending now. Nothing below is
decided; the outputs present every one of them as pending.

### Group A: contract and precedence (Legal)

1. **The concession term.** VOL-I 12.1 p6: "twenty-five (25) years commencing on the Project Commercial Operation
   Date"; VOL-V 3.1 p2: "twenty-five (25) years from the Effective Date". ADD-02 Q7 p2: "The Authority notes the
   question. The order of precedence at Volume I Clause 3.2 applies. The Authority does not consider further amendment
   necessary at this stage." VOL-I 3.2 ranks the Addenda, then Volume I, then Volume V; VOL-I 3.3: a Bidder resolving
   a conflict on its own does so "at its own risk"; the VOL-V Note: a deviation not listed in Form 4-E is "taken as
   accepted". *Proposed now:* both readings shown, no choice; the rows VOL-I-12.1-01, VOL-V-3.1-01, VOL-V-3.2-01 and
   VOL-V-42.2-01 at medium confidence; I-CONCESSION, the A3 line (⚑) and CQ-CONCESSION-TERM pending Legal.
   *Effect:* the operating years priced in the Financial Model (from the Effective Date about 36 months of
   construction come out of the 25 years), whether VOL-V 3.1 is listed in Form 4-E, the year-20 handback reserve.
   *Pending:* your decision, recorded with `tenderpack accept` on the rows and the entry, or the drafted question sent
   before 12 Nov 2026 (CQ-CONCESSION-TERM still assumes the PCOD reading in its question text).
2. **The 2 Oct history disclosure (A4-1).** Brief p4: "The repository with its real commit history." *Proposed:* the
   erratum draft `docs/drafts/ERRATUM_A4_history-disclosure_DRAFT.md`, corrected on seven points by the A4 audit,
   options 1–3 (full erratum; short erratum; no disclosure and the words "real" and "verbatim" removed from the 2 Oct
   material). *Effect:* options 1 and 2 make A4-1 pass and leave nothing an assessor can find unexplained; option 3
   leaves the index and the session-11 report, which already state the rewrite, as the only disclosure. One point
   inside it: whether the two instruction times stay in the text (the A4 recheck: optional; "on the owner's
   instructions of 2 Oct 2026" suffices). *Pending:* the option and the wording; nothing applied. **Before any
   change of the repository's visibility:** GitHub may still serve the four pre-rewrite commits by their full hash
   after the force-push (not verified from here; no outbound call was made); if it does, a public repository exposes
   the removed wording whatever the erratum says. A read-only check of each full hash against the GitHub API settles
   it; the full hashes are in the transcript, not in the repository.

### Group B: forms (Legal, Technical)

3. **The reissued Form 4-A.** ADD-01 App A p3 prints "12 November 2026" and drops paragraphs 1–6 (the offer wording,
   the 150-day validity, the bid bond, no other proposal, pre-bid attendance) while ADD-01 2.1 moves the date to
   26 Nov and VOL-IV p2 says the form is "reproduced without alteration". *Proposed:* App A as the baseline, no
   correction method adopted; the A2 row now CHANGED with the printed-date conflict and NOT SETTLED afterwards; A5
   `form-4a` gated "decide whether to ask by 11 Nov, finalise by 23 Nov". *Effect:* what is printed and signed in
   Envelope A (an improperly executed Form 4-A is non-responsive, VOL-I 9.3). *Pending:* CQ-F4A-REISSUE, draft.
4. **Form 4-C declaration 4 "exclusion".** VOL-IV p6 (Arabic, governing): "يؤدي إلى استبعاد العرض". *Proposed:* its
   own A3 category, not equated with the others. *Effect:* if equated with non-responsiveness, the A3 line moves;
   A5 unchanged. *Pending:* Legal (CQ-F4C-EXCLUSION, draft; the approval record keeps it open).
5. **Form 4-G "No" answers and undertakings 3–6.** ADD-02 7.2 p3. *Proposed:* no longer "No question"; pending
   Technical in the register's new "Proposed readings" section. *Effect:* if Technical cannot confirm all six, a
   question must be drafted before 12 Nov. *Pending:* Technical (I-F4G-NO).
6. **What Form 4-E is checked against.** VOL-I 9.6. *Proposed:* form-4e after technical-proposal (float 11 → 1).
   *Effect:* if the cross-check also covers Form 4-F and the financing schedule, the Envelope B chain becomes about
   2 WD infeasible. *Pending:* the scope of the check.

### Group C: envelopes and copies (Bid manager)

7. **Envelope B "only".** VOL-I 10.1 against 10.3 (the model auditor's opinion) and 10.6 (the financing schedule).
8. **Form 4-B's contract values in Envelope A.** VOL-I 6.2 makes commercial information in Envelope A non-responsive.
9. **The electronic copy.** VOL-I 6.5 "one (1) searchable electronic copy" against two sealed envelopes.
   *Proposed for 7–9:* prepare everything, gate only the finalisation (ask by 11 Nov, finalise 23–25 Nov); the
   assembly activities now carry only their own envelope's rules. *Effect:* what goes where; a wrong placement is
   non-responsive. *Pending:* I-VOL-I-ENV-B, I-VOL-I-ENV-A-PRICES, I-VOL-I-COPIES (drafts).
10. **Re-lettering of the VOL-I 9.1 list after Form 4-G** (I-F4G-LETTERING): the Envelope A dividers.
11. **ADD-01 Q2 after ADD-02 2.1** (the Form Sheets outside the 150-page limit): A2 says REVIEW, the register now
    says pending, no longer "its substance stands".

### Group D: technical basis (Process engineer, Technical)

12. **TN 3 mg/l against the missing Environmental Permit.** VOL-II p3 "the Environmental Permit shall prevail";
    ADD-02 5.1 amends only the reproduction. *Proposed:* "Permit compliance is not claimed"; I-PERMIT labelled pending
    (its own wording uses "precedence"/"prevails"). *Effect:* the process design basis, the deduction exposure
    (VOL-V 31.1(b)), the reliability run. *Pending:* whether to raise it or reserve the position.
13. **Design flows and "dry weather flow".** Table 2-6 rows 2-6.2 and 2-6.4; Q11. *Proposed now:* Q11 settled the
    question asked (design to the Volume II figures); "not contradictory" (the 1.5 peaking factor) labelled an
    engineering reading; dry weather flow open (CQ-DWF-STORM-FLOW, draft).
14. **The chlorine and pH ranges under the "maxima" qualifier** against UV-only disinfection (I-VOL-II-T24-TENSIONS,
    pending, labelled). Preserved unresolved as you asked.
15. **The scoring method** (ADD-02 note (3) "multiplied by the weight shown" where the table shows marks;
    CQ-SCORING-METHOD): how the 70-mark threshold is reached.

### Group E: commercial and programme (Commercial, Bid management)

16. **The Local Content Certificate.** ADD-02 9.1 (35 %, non-responsive if missing); ADD-01 App B item 4 records the
    difficulty. *Proposed:* 30 WD PROVISIONAL, which gives INFEASIBLE by 12 WD on A3 lines 6.1-01 and 8.6-01; feasible
    at 18 WD or less; A5 now links CQ-LCC-ISSUER with `ask_by` 11 Nov. *Pending:* the issuer, the real lead time,
    whether to ask (by 11 Nov, submit by 12 Nov).
17. **Bid Bond validity against the Financial Close long-stop** (I-VOL-I-BOND-LONGSTOP): the extension cost.
18. **Counting conventions and the calendar.** VOL-I 2.4 (the backward rule for Working Days only); "N days before X"
    computed as X − N by analogy (labelled in `config/formulas.yaml`; removable, then every such date is ambiguous
    and escalated); holidays none declared; the delivery buffer 0 WD (one buffer day makes the whole submission chain
    one WD tighter); the two ambiguous dates (attendance notice 14 or 15 Oct; look-back 26 or 27 Nov 2016) shown with
    both readings everywhere.
19. **The assumed bidder** (3 members, 1 foreign, 2 reference plants, 1 signatory per member; attendance at the
    Pre-Bid Conference NOT assumed): confirmation.

### Group F: the tool's own rules that you may want to narrow or widen

20. The human-owned classifier is deliberately broad (topic words such as "means", "governs"); curated issues are
    labelled only where their own words assert a judgment (now I-CONCESSION, I-PERMIT, I-VOL-II-T24-TENSIONS);
    closure words in curated issues ("settled" in I-VOL-I-COPIES, I-VOL-I-FILE-NAMES, I-VOL-I-BOND-LONGSTOP) are not
    labelled; four readings are still listed as closed without trigger words (Ramp-Up, SCADA "not a conflict", the
    Financial Model format, copy quantities); `clarify.judgment_findings` is a regression, not a release gate.
21. The change predicate trusts an op's own label (`interprets`) unless the answer reads as a change; a re-made
    reading that records an added obligation only in its note counts as CONFIRMED (VOL-II-3.1-01 at ADD-02 in A5,
    CHANGED in the diff); an added obligation alone is not made a change (it re-created a blind-05 false signal).
22. The A5 question rule gives `ask_by` to 24 activities (CQ-F4A-REISSUE on every Form step): keep, or link a
    question only where its units meet the activity's rows. The VOL-V rows' relationship flags now also sit on
    deviations-review and form-4e.
23. The cover-discrepancy rule reads the model's free-text conflict for unit ids; a structured `conflicts:` field in
    the contract would be firmer. Ranges are still read as one id by three modules (`summary._subject_units`, the
    answer-cites check, `draft._target`). A replaced list the addendum does not re-letter keeps two items with the
    same letter, recorded, never corrected. The PROPOSED cover issues name "Bid manager" as owner.
24. Offline: the installed Ollama model names for `routes.ollama.models.{text,vision,critic}` (the shipped ids are
    candidates); whether an `ollama` run outside offline mode should default to a local critic (now: host, with a
    notice); grouping critic requests across batches; `max_parallel_sessions` 2 on the host route (it halved the
    analysis phase in the regression attempt; shipped at 1).
25. Exit code 6 is new for a run that stops because it cannot go on by itself; wrapper scripts that treated 0 as
    "finished" need to check for it.

### Group G: approvals (unchanged, not defects)

26. 205 of 205 rows and 37 of 37 ops are PROPOSED; every assumption needs its owner's confirmation; the two image
    readings are approved by you and shown so; 21 clarification questions are drafts, not sent (cut-off 12 Nov 2026).
27. The reading YAML headers still begin "PROPOSED READING — PENDING HUMAN REVIEW" (your approvals pin their hashes).

### Group H: the local panel (`tenderpack panel`; the panel agent's open points)

28. **What the panel calls A4.** The home page labels the clarification register "A4 clarification register" (as the
    panel brief said) and links the work log index beside it (`worklog/README.md`, the A4 proper): keep both, or one.
29. **Stopping the panel does not stop its jobs.** A run started from the panel keeps going in its own process group
    when the panel is closed (so closing a browser tab cannot kill an AI run); the next panel start shows it. The
    alternative, stop every job when the panel exits, is one line if you prefer it.
30. **Decision state on the Decisions page** is the latest record in the decisions file; whether that record still
    binds to the current content is the engine's computation and is shown in the outputs, not recomputed by the panel.
31. **Decision commands** shown by the panel carry explicit `--evidence`/`--pack` (longer than the `command` field of
    `items.json`, but exact). The Anthropic and OpenRouter routes are not offered in the form (terminal only).

### Group I: the unseen-addendum workflow after blind-06 (the scorer's points that are judgments)

32. **Over-escalation.** The candidate hands to Legal points the documents settle (the operative text over the cover;
    an addendum's own precedence clause; "is amended accordingly" read as an amendment). The fixer F6 was told to
    present such points as "settled by <clause>: <words>" and keep only genuine judgments pending: confirm that this is
    the behaviour you want, or keep every precedence question pending for Legal.
33. **Working-day counting on an addendum's own dates.** The key and the candidate agree on the number (12 WD left)
    by different conventions (the key counts the issue date inclusive and the PDD exclusive; the tool's packet says
    "the issue date not counted, the PDD counted; Working Days per VOL-I 2.4", `rehearsals/blind-06/review/index.md`
    l.170): confirm the tool's convention or change it (the counting rules live in `config/formulas.yaml`).
34. **How wide the pending rule reaches (F5).** One pending set now drives ⚑ on A3, the NOT SETTLED row label in
    A2 and A5, A1's Issues sheet and A4: every issue owned by Legal or Commercial, every issue whose words assert a
    judgment, and every issue linked from a pending decision. Three rows the A2 reviewer had accepted as CONFIRMED
    are therefore NOT SETTLED now: VOL-I-12.2-02 (I-VOL-I-BOND-LONGSTOP), VOL-II-4.2-01 (I-FLOWS) and VOL-II-3.1-01
    at ADD-01 (I-PERMIT). Keep one set everywhere (as built), or narrow the row rule to the asserted-judgment and
    pending-decision reasons (VOL-I-12.2-02 would return to CONFIRMED; the other two stay NOT SETTLED).
35. **I-VOL-I-ENV-A-PRICES** (owner Bid manager) carries † but no ⚑ although the A3 reviewer called it a person's
    decision: set its `decision_owner` to Legal or Commercial to mark it, or leave it.
36. **A question's reach into the programme (A5 N2)** now runs through the deliverables shared by the activities that
    carry the question's rows (CQ-F4A-REISSUE on the Form 4-A steps and the clarifications step; CQ-ENV-B-CONTENTS still
    on the nine Envelope B steps): a heuristic, stated as such.
37. **The ⚑ legend** now reads "a legal, commercial or technical judgment no one has recorded", because the pending set
    holds engineering readings too (I-FLOWS, I-F4G-NO); and I-F4D-WORDING adds a line to the A3 page, which stays at
    level 2 with a scale margin of 0.006 after I-AUTO-COUNTING was shortened.
38. **The decision binding and the re-pin (F6, item 9).** A confirming annotation no longer changes a unit's pin
    (pin format 3; the real pack re-pinned: 25 pin values on the units carrying the ADD-01 3.2 and ADD-02 Q8–Q14 and
    Table 1-1 confirmations), so no row goes STALE for a confirmation. The review binding of a row still includes its
    pins, so 19 rows' review fingerprints changed; no decision is bound today (every row is proposed), so nothing is
    invalidated. Accept this, or drop the pins from the decision binding.
39. **A confirming provision stays a dependency** (a row read before the confirmation is STALE as "new dependency …
    which confirms …"), because the confirmation is itself a proposed op and could be wrong (blind-06's Q16): keep, or
    drop confirming provisions from the dependencies.
40. **Settled points (F6, items 12 and 6 b).** An issue or escalation that turns on a point a clause settles ("X
    governs", "X prevails over Y", the addendum's own cover rule, "is amended accordingly" in the provision) is
    re-presented as "<clause> provides: '<words>' (applied, not decided)", its owner becoming the Bid manager on
    promotion (the original owner and text are kept beside it); a downstream item that hands such a point back to a
    person is marked a reversal. Confirm the rule's scope, or keep Legal as the owner of those issues.
41. **Forward periods (F6, item 5).** "Within N Working Days of <event>" needs a forward counting rule in
    `config/formulas.yaml` and, for an event anchor, the event's date; until you add them the computed deadline says
    "not computed: no rule" with both readings (blind-06's Mon 23 Nov and Sun 22 Nov).
42. **Collecting results as they arrive (F6, item 14)** would change the documented sequential-result invariant (answers
    taken in plan order, each packet re-checked); F6 only asks the next batch before a batch's critic runs. Keep the
    invariant, or allow out-of-order collection for speed.

## 7. Verification

On the final tree (every merge of the session, `max_parallel_sessions: 1`, nothing running), at 22:11–23:55 UTC:

| Check | Result |
|---|---|
| Full suite (22:11–22:50) | **1,045 passed, 0 failed** in 38 min 47 s on the final tree. The earlier run at 19:18–19:55 (1,010 passed, 6 failed: five test expectations updated for "Proposal Due Date (PDD)" at first use, with a comment each; one regression, E152, the blind-02 rehearsal's A3 page no longer fitting one page, fixed with a general condensation level 5) preceded the blind-06 fixes and F6 |
| Fresh rebuild (23:53–23:55) | `ingest` 524 units STRUCTURE OK (every unit checked in full against the PDF, no mismatch); the synthetic fixture 31 units; `outputs` exit 0 (C43 7.7 pt at level 2; the two approval blockers only); the drill 547 units, `out-drill/` PARTIAL with its expected blockers; `out/` and `build/` regenerated from this code; against the last progress commit `2cff460` the outputs change in exactly the 9 files F6 explains (one A1 planning note on a forward period with no counting rule; 19 rows' review fingerprints after the re-pin, in the packet's items and five batch pages) |
| Strict release check | `outputs --strict` exit 3 with exactly the two human-approval blockers (205 of 205 rows, 37 of 37 ops proposed), no defect blocker |
| Register | `check-register` exit 0, 0 findings (C14: 16 obligation words in non-requirement units, for a person) |
| Offline checks (`scripts/mac/checks.sh --no-ai`) | 7 PASS, 4 PENDING (the looks in Numbers/Excel and a browser, the two Ollama checks: yours on the Mac), 0 FAIL |
| Panel | 19 tests pass (loopback, token, traversal, uploads, output parity, upload to results, resume after SIGKILL, candidate isolation, the decisions form, the deliverables strip, the packet link); pages checked in Chromium screenshots |
| Rehearsals | blind-06 scored before the key was opened (§3); the blind-05 regression interrupted, resumed, deferred, resumed and finished (exit 0, 17 unresolved) and scored (§3; `rehearsals/blind-05/REGRESSION-S12.md`); ADD-04 dropped on your instruction |
| Records | the work log with E138–E155, the error index (164 entries), the briefs 45–85 exported verbatim, PLAN revision 12, README, PANEL.md, MAC_SETUP.md, OPERATING_GUIDE.md §3b/§9, COST_AND_EFFORT.md row 12; the labelled working-tree snapshot built from the closing tree: `LAMAR-PPP-R2-SNAPSHOT_2cff460+wt_20261006T0003Z.zip` (115.6 MB, 5,875 files, 5875 manifest lines; base `2cff460` with 178 paths differing; sha256 `7644a12bff382719a9f058cdd436362e6fcff272282fbe474276eb16ad10821e`), built at 00:03–00:04 UTC into the session's scratchpad; too large for the repository and the container is ephemeral, so it is recorded here by name and hash and `scripts/make_snapshot.py` rebuilds the same tree from the closing commit |

## 8. Runnable commands

```
make setup                                   # once, needs network (or scripts/mac/setup.sh on the Mac)
.venv/bin/python -m tenderpack ingest        # the evidence build
.venv/bin/python -m tenderpack outputs --evidence build --out out            # A1–A5 working draft
.venv/bin/python -m tenderpack outputs --evidence build --out out --strict   # the release check (exit 3 while anything is unapproved)
.venv/bin/python -m tenderpack check-register
.venv/bin/python -m tenderpack ai routes [--offline]                         # what each route can do here, and what is pending on the Mac
.venv/bin/python -m tenderpack ai run ADD-03 --pdf PATH --route host --host-model-alias opus   # an unseen addendum (connected host)
.venv/bin/python -m tenderpack ai run ADD-03 --pdf PATH --offline                              # the same, local Ollama only
.venv/bin/python -m tenderpack ai run ADD-04 --pdf PATH --base-run RUN_ID3 …                   # a consecutive addendum on a run's candidate (built and tested on synthetic addenda; not run live, on your instruction)
.venv/bin/python -m tenderpack ai resume RUN_ID [--from STEP]                                  # after an interruption or a code change
.venv/bin/python -m tenderpack ai run-status RUN_ID
.venv/bin/python -m tenderpack panel                                                           # the local control panel (127.0.0.1, a token per start; browser pending on the Mac)
.venv/bin/python scripts/make_snapshot.py DEST --label "review"                                # the labelled working-tree snapshot
.venv/bin/python -m pytest -q -p no:cacheprovider                                              # the full suite
```
