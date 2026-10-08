# Session 14 report: the focused finalisation run (7 October 2026)

**Status of this report: in progress.** Sections marked PENDING are filled at the end of the session from the records; nothing below is claimed before it ran. The work is uncommitted on the owner's instruction ("Do not commit or push anything until I explicitly say so"); the base is commit `a918d5e` (the session-13 closing commit).

The owner's message of the morning is kept verbatim in `worklog/2026-10-07_session-14_prompt.md`; the work log is `worklog/2026-10-07_session-14_finalisation.md` (§2 the timeline, §3 the models that actually ran, §4 the runtime model for the rehearsals, §6 the errors); the decisions that need the owner are in one consolidated packet, `docs/session-14_review_packet.md` (PENDING: written last, with software failures, missing evidence and human approvals separated).

## 1. What you asked, what was done

Seven parts: (1) the scorer's 19 workflow defects and the §9 items of the session-13 report; (2) complete ADD-03 handling; (3) human ownership kept accurate; (4) independent rechecks of A1, A2, A3 and A5; (5) the preliminary AI briefing with scoped page access and the controlled handoff of your answers; (6) blind-07 as a labelled regression, then a fresh sealed ADD-03 (blind-08); (7) the interview package rebuilt and self-verified, with the Mac check and the routes corrected. Six implementers (W1–W6) and one addendum author (A8) worked in isolated worktrees; their patches were merged into the main tree with a test check after each; three reviewers (R1–R3) then rechecked the rebuilt outputs independently. Every agent and the coordinator stayed inside the standing rules: nothing approved, accepted or rejected on your behalf; `curation/approvals.yaml`, `curation/readings/` and `curation/reading-snapshots/` untouched; the two source-image approvals kept as transcription approvals only; every pending judgment still pending; clarification questions still drafts.

## 2. Before and after, part by part

The "before" is the session-13 state as the blind-07 scorer found it (`rehearsals/blind-07/COMPARISON.md`) and as the session-13 report's §9 listed it; the "after" is what the merged code does now, each item covered by tests that failed first on `a918d5e` (the test files are `tests/test_session14_*.py`; 21 files).

| Part | Before (session 13) | After (session 14) | Where |
|---|---|---|---|
| 1 Contract and repair | A payload with one invalid inner item failed whole; the schemas were not exposed; the model could not repair | The full `Row`/`Interp` schemas are in the packet and the policy; a failing payload is re-asked ONCE with its exact errors, and only the failing items are taken from the repair (valid siblings stay as first given); on the host route the MCP submit gate stages, returns a `repair` block and accepts one re-submission; still failing → `invalid` with its errors | W1: `tenderpack/ai/contract.py`, `requests.py`, `mcp_server.py`, policy 50/51 |
| 1 Same-clause edits | Two `replace_text` on one unit rejected even with separate spans; `annotate` with plural targets broken; `previous_value` checked against the wrong text | Disjoint spans accepted (overlap or read-what-the-other-writes still rejected); plural targets fixed; `previous_value` compared with the previous EFFECTIVE text of each target, never the answer's own new text | W1: `amend.py`, `contract.py` |
| 1 Dependencies and readiness | Untyped, cycles unrefused, no readiness, a failed shared statement blocked silently | Typed dependencies on any id of the set, cycles refused by name, `ready`/`blocked_by` on every item, the blast radius of a failed statement reported, promotion skips unready items with the blocker named | W1: `dependency_graph`, `readiness()` |
| 1 Stated rules | A quoted precedence rule could read as a decision | A stated rule can support a change "applied, not decided; a person confirms"; a quotation alone settles nothing; declared conflicts never settled automatically | W1: `applied_rule_review`; W4: "PROPOSED BASIS (applied rule; a person confirms the application)" |
| 1 Statuses | "Accounted for", "applied", "unresolved" and "approved" blurred across the op file, the packet and A3 | Four states (applied / no effect / unresolved / unaccounted) agreed across the op file, `promotion.json`, the packet and the candidate A3; "approved" only a person's recorded decision; A1's candidate column reads "UNRESOLVED (value in question)" | W2: `partial.unresolved_rows`, `dispositions.py` |
| 1 Issues, obligations, tasks | Analysis issues, new obligations and the tasks of unresolved provisions were dropped | Analysis issues promoted as PROPOSED issues (HUMAN DECISION PENDING); CONDITIONAL impact tasks (`impact:<section>`) for unresolved provisions, failed ops, escalations and not-ready items; `oblig:<op>` tasks for every op adding a unit or an obligation; every row-making task carries `needs`; `deliverable_gaps` reported | W2 + W3: `downstream.conditional_tasks`, `amend.conditional_impacts`, one basis vocabulary (`downstream._basis_of`) |
| 1 Records | The packet printed "0 calls, 0 tokens" for 10 host sessions; interruptions unrecorded | `host_usage` from every session record that exists; interventions record the person's stop, the sessions it cut, the reused answers and the resume, listed first. The regression showed the limits (R4-3): a session killed with its process leaves no record and so is not counted (the run then reads "unknown 0"), and only a drive that closes cleanly is kept in `concurrency_drives`; F3's item 7 adds the end record of a killed segment and its lost sessions | W2: `workflow.host_usage`, `checkpoint.py`; F3 |
| 1 Cover numbers, windows, documents | Cover-number traps missed; closed-window notes on software failures; newly referenced documents unlisted | Cover claims compared item by item with the operative provision (figure, count, modality, the arithmetic shown for a person); the closed-window note never on a software or schema failure; `partial.referenced_documents` lists titles, revisions and drawings the addendum newly names | W2 |
| 2 ADD-03 operations | Relocation, new clauses and tables, scoped exceptions and arithmetic were not op kinds; blocked ops left no investigation | `adjust_value` (computed from the previous effective value by `calc.relative_change`, the derivation recorded, refused when the words are not printed), `relocate_unit` (lineage both ways, atomic with rollback), `insert_unit` by number, `insert_table`, `annotate` with `disapplies` and a `scope`; conditional impact investigations for an invalid or held op, an unresolved disposition, an unaccounted provision and an op resting on a pending reading; no new amendment language; nothing hardcoded to blind-07 | W3: `amend.py`, `calc.py`, `derived.py`, policy 60 |
| 3 Human ownership | "unit not resolved" fired the human-owned classifier; the composite-asset ambiguity was missed; transcription approvals could read as interpretation approvals | `human_owned.negated()`; `I-AUTO-CLASS-SCOPE-<table>` for a table giving values by class with no rule for an item in more than one class (fires on blind-07's reading, on nothing in the real pack); an explicit Approval column; "at all times", programme readiness, the Permit and the maxima/ranges stay pending (tested); durations and bidder settings stay labelled assumptions | W4: `human_owned.py`, `stage2.row_states` |
| 4 A1 value / interpretation / approval | One status column | Three columns: value (unchanged/changed/new, never a confirmation), interpretation (open judgments; HUMAN DECISION PENDING where a person decides), approval (what a person recorded; a transcription approval is not an interpretation approval); a CONFIRMED line resting on an unaccepted op says so | W4: `out/a1/a1.csv/json/xlsx`, the review cards |
| 4 Form 4-E | Checked against the forms only | Checked against the whole Proposal (VOL-I §9.6): 19 documents, each citing 9.6 and the clause that puts it in the Proposal; three finish after Form 4-E starts; a strict ordering is infeasible by 14 WD on the assumed durations (reported, nothing changed); a commercial-qualification tension (9.6 against 6.2/10.5) raised for a person | W4: `out/a5/form_4e_checks.csv/json` |
| 4 Propagation and readiness | An issue travelled along every relationship whatever its scope; readiness and finalisation not distinguishable | `scope_words` on a relationship (verbatim in its own evidence): the maxima/range issue no longer reaches VOL-V-29.3-01 (the row says why) while it still reaches the rows in scope; `preparation` and `finalisation` on every activity, the Gantt's amber tick | W4: `relationships.py`, `programme.py`, `gantt.py`; two PROPOSED curation entries |
| 5 Briefing and answers | The host quick review had no page images; the owner's answers had no path into the run | One read-only tool `get_addendum_page {page[, region]}` serving only the new addendum's pre-rendered pages and crops (hashes re-checked on every call, nothing else served); the owner's answers taken at three checkpoints: a `fact` must cite `page N: words` or `UNIT: words` and is checked verbatim, a `judgment` is a PROPOSED judgment never an approval, a stale answer waits to be re-offered, an answer citing an approved reading is PENDING and never applied, a consumed answer re-runs exactly the affected batches, every consumption is a logged intervention; `curation/` and `out/` never written | W5: `tenderpack/ai/answers.py`, `quick_review.prepare_scope`, `serve-mcp --addendum-scope` |
| 7 The Mac check | An exit-zero Ollama run read as validated | Three levels from the records: connectivity, valid content, complete workflow, with a PARTIAL label; offline never reaches a hosted model (every hosted constructor and the HTTP helper refuse); `config/routes_status.yaml` (works / never_run / ready) holds the README, the docs, `ai routes` and the panel to one description; `docs/MAC_CHECKLIST.md` one page, cloud-tested vs PENDING ON THE MAC; `scripts/mac/verify_package.sh` verifies the packaged copy | W6 |

Found and fixed on the way (coordinator): the W2/W3 join overwrote the workflow's own provision records (one basis vocabulary now); session 14's code had slowed every model-free step of a run by 25–55 % through a session-13 function with no memo (E167; `reissued_form_gaps`; the recorded run 131 s from 416 s, outputs byte-identical); the package's smoke check read the run-scoped lock's empty folder as a session (fixed with a test).

## 3. The outputs rebuilt on the merged tree

The session-13 closing chain, in the same order, twice: on the merged packages (15:57 UTC: 29 files changed and 2 new against `a918d5e`, A3 and A4 unchanged in bytes; the reviewers worked on that state) and on the tree with the fixers F1 and F2 and the A3 fit (19:52 UTC; `worklog/continuation-s14/rebuild_chain_1952.log`): `ingest` 524 units with C10 no mismatch; `outputs` exit 0 (C13 18 A3 rows, C43 one page at condense level 2 with every reason, 7.62 pt, no STALE row, C48 200 rows in force, the two approval blockers only: 205 rows, 38 ops); the drill PARTIAL with its expected blockers; `outputs --strict` exit 3 with exactly the two approval blockers; `check-register` 0 findings; the Mac checks 9 PASS / 5 PENDING / 0 FAIL. Against `a918d5e`, 39 output files now differ (README, a1 3, a2 5, a3 3, a4 3, a5 14 with the two new Form 4-E check files, checks.json, review 9), the union of the packages' and the fixers' explained changes (§2 and §4). The chain runs once more on the final tree after F3 and F4.

## 4. The independent rechecks (part 4)

Three reviewers, read-only, expectations from the sources first, on the outputs rebuilt at 15:57 (`worklog/continuation-s14/reviews/r1.md`, `r2.md`, `r3.md`): R1 (A1/A2) 4 major + 4 minor, R2 (A3, the decisions, A4) 4 + 7, R3 (A5, the rendered files, the cards) 5 + 9, overlapping on five points. What held: every computed date; all 38 ops in the documents' exact words; 185 quotes and 251 segments on their pages; the 20 image rows against the images; xlsx = csv = json cell for cell; 260 links, 0 broken; the schedule recomputed by hand for all 44 activities; A3 one page; the pending judgments pending; the image approvals transcription-only. The findings and their fixes (F1 for A1/A2, F2 for A5/A3/A4, each failing test first; `tests/test_session14_f1_recheck_fixes.py` 13 tests, `tests/test_session14_f2_a5_a3_fixes.py` 21 tests):

| Finding | Fix |
|---|---|
| The Local Content row (VOL-I-8.6-01) showed its value as "unchanged since BASE" although ADD-01 deleted it and ADD-02 reinstated it at 35 % with a non-responsive consequence (all three reviewers) | `row_states` now sees a delete-then-reinstate: "changed at ADD-02 by ADD-02/9.1 (reinstated in amended form …; deleted at ADD-01 by ADD-01/4.1)"; the revoked re-read named as revoked; the same text on the cards |
| A1 and A2 disagreed on which rows the missing Permit reaches (three rows) | one rule for an issue's reach through blocked units (`document_blocks`, `inherits_block`, within scope): I-PERMIT on VOL-V-29.3-01, VOL-II-2.5-01 and VOL-II-4.3-02 as HUMAN DECISION PENDING; 29.3-01 at ADD-01 NOT SETTLED |
| The Form 4-E commercial-qualification tension and the cross-check method existed only as A5 prose, with no issue, owner or activity | two PROPOSED issues (`I-FORM-4E-COMMERCIAL-QUALIFICATION`, Legal counsel; `I-FORM-4E-CROSS-CHECK`, Bid manager) on their rows, on the A3 page (named on the Envelope A line with their marks and owners), in A4 and as open decisions on the form-4e activity in the programme, the Gantt, marshalling and the README; a judgment with no mirroring issue is a check-register finding |
| `form_4e_checks` printed "final on <date>" for gated documents | each document's state: linked / NOT CHECKABLE: GATED by …, finalise by D after Form 4-E starts / NEEDS A DECISION, with the earliest finish |
| I-CONCESSION never reached the Financial Model chain or Form 4-F in A5 | a new rule: an issue whose own words name a deliverable reaches its producers and the documents built from them (PROPOSED reading) |
| The page-limit issue (I-VOL-I-PAGE-LIMIT-Q2), read by all three reviewers as settled by VOL-I 9.2's own words as amended | re-presented as "PROPOSED BASIS (applied rule; a person confirms the application)" with the clause quoted, owner kept, its row NOT SETTLED; never closed by the tool (decision C6) |
| Minor: the value column against the row's status; "(confirms) … (not a confirmation)"; the A3 heading's two counts; the † against A5's dates; CQ-ENV-PERMIT's rows; Arabic in the cards; the Form 4-G citation; the WD figures; READY against NEEDS A DECISION; the scope words not shown; VOL-II-2.5-01 moved by the TN change | all fixed: one `decide_by` source for A3 and A5; "50 open issues (25 listed)"; `<bdi dir="rtl">` runs; the question's rows from the issue it mirrors; a PROPOSED link REL-T24-CONTINUOUS-MONITORING with `scope_words "continuous"`; the scope words in the Relationships sheet |

The extra pending issue pushed the one-page A3 to condense level 3 (reasons off the page); fixed by folding the two Form 4-E judgments under the Envelope A line and deriving the scale floor from the 7.5 pt minimum the check enforces (`render.A3_SCALE_LOW` 0.9 → 0.89): the page is at level 2 with every reason, 7.62 pt. The final independent review (R4) of the merged result: PENDING.

## 5. The rehearsals (part 6)

**Blind-07 as a labelled regression (an open key; scored after the run; `rehearsals/blind-07/regression-s14/COMPARISON-S14.md`).** The same addendum through a fresh package built from the merged tree (code identity `64dbc541896c4ac1`, the host and critic models pinned to `claude-opus-5-5`, two sessions in flight). The run suffered two unplanned interruptions (the plan's 429 at 16:24, which the workflow's own handling deferred, then two container restarts), and was resumed twice from the package's panel; the planned SIGTERM-after-submission was therefore not exercised here (it is blind-08's).

| Measure (33 key items) | Session 13 (before) | Session 14 (after) |
|---|---|---|
| Hit / partial / missed | 11 / 17 / 5 | 18 / 14 / 1 |
| Usable: as is / in part / detection only / wrong | 6 / 5 / 17 / 0 | 17 / 9 / 6 / 0 |
| False positives / false signals | 5 / 10 | 5 / 13 |
| Provisions listed unresolved | 19 | 9 |
| Pending decisions in the packet / promoted issues | 9 / 1 | 35 (about 26 over-escalated) / 23 |
| The 19 workflow defects | — | 13 fixed, 1 not exercised, 5 still present, 0 regressed |
| Active time (steps kept + destroyed) | 19.6 min | about 69 min (57.0 kept + about 12 destroyed); dead or deferred about 82 min; wall 2 h 31 min |

The 30-minute target is missed on every measure. The scorer's reasons: Opus-pinned sessions (the session-13 run's sessions ran on the CLI's default model), 44 downstream tasks against 17, 26 sessions started against 16. Fifteen valid ops were promoted (the engine-computed SAR 1,500,000, the relocation, the scoped disapplication among them); one regression against session 13 (the 4.3 request deadline lost its planned date, N1) and 12 new general defects (N1–N12) are listed in §9 of the comparison; the fixer F3 takes the ones that can be fixed before blind-08 (its brief: `worklog/continuation-s14/briefs/F3.md`), the rest go to the review packet.

**The sealed blind-08 (`rehearsals/blind-08/COMPARISON.md`; frozen by hash before the key was opened, `FROZEN.md`).** A new addendum written by an author agent whose key nobody read before the run (4 pages; 63 scored items, plus 9 decoys, 22 must-not-report items and 9 acceptable-if-raised items), run through a fresh package built from the frozen code `7c721d4` (code identity `a9ebd02ab0cbf8a7`), the host and critic pinned to `claude-opus-5-5`, two sessions, the planned stop right after an analysis submission and the panel's Resume.

| Class | Items | Hit | Partial | Missed |
|---|---|---|---|---|
| Provisions | 17 | 11 | 6 | 0 |
| Clarification responses | 5 | 3 | 2 | 0 |
| Image | 1 | 1 | 0 | 0 |
| Computed values | 4 | 1 | 3 | 0 |
| Derived dates | 9 | 5 | 0 | 4 |
| New obligations | 6 | 1 | 5 | 0 |
| Indirect effects | 8 | 1 | 5 | 2 |
| Genuine ambiguity | 1 | 1 | 0 | 0 |
| Settled points | 5 | 4 | 1 | 0 |
| Structural changes | 4 | 1 | 3 | 0 |
| Cover errors | 3 | 0 | 3 | 0 |
| **Total** | **63** | **29** | **28** | **6** |

Decoys 8 of 9 clean; must-not-report 0 of 22 asserted; nothing asserted as settled that the key reserves for a person; the image read correctly; the genuine ambiguity surfaced with both readings. **The interruption worked as designed**: the submission made just before the stop was reused after revalidation; both segments ran on the same code. Two batches were asked twice (one stopped before submitting, as designed; one dispatched on resume before the reused submission was folded in, a resume defect). The scorer's three main findings: one controller consistency rule treated two compatible changes to one clause as conflicting and left three provisions unresolved; most of the arithmetic and derived dates the key weighs (a duration, a notice period, volumes, drop-dead dates) were not produced, each recorded by the run as a software limitation; and too much escalation remains (about 49 pending markers for about 5 real decisions; a stated governing-language rule and the cover errors re-opened two to five times).

**The 30-minute verdict, honestly:** not met. 45.0 minutes from the upload to the review packet on an idle machine; analysis alone took 27.3 minutes; the interruption cost at most about 5 minutes. Twelve host sessions, two wasted. The ways to cut it are the owner's choices in the packet (C13): the sessions' model, three or four sessions in flight, splitting large structures, capping downstream work.

## 6. Verification

Merge checks 1–5 green on the merged tree (190, 94, 213 … passed per check, the work log §2); the panel file green after E167's fix; merge check 6 PENDING (every session-14 test file with the changed expectations); the final independent review of the merged result PENDING; the full suite on the final code PENDING.

## 7. The package and the Mac (part 7)

PENDING: the final package is built from the final code after the reviews and the rehearsals, verified by `scripts/mac/verify_package.sh` on the packaged copy, and sent as a zip. Cloud-tested vs pending on the Mac: `docs/MAC_CHECKLIST.md`.

## 8. Errors of this session

E166 the plan's session limit (3 h 50 min lost, no work lost); E167 the slowdown above; E168 the coordinator's rebuild under a running test file (one re-run). Full rows: the work log §6 and `worklog/ERROR_INDEX.md`.

## 9. Decisions that need you

`docs/session-14_review_packet.md` (in progress: the software failures, the missing evidence and the human approvals in three groups; the rehearsal rows are completed from the scorers' reports; the raw list the agents raised is `worklog/continuation-s14/decisions_raw.md`).

## 10. Models and settings that actually ran

Coordinator: Fable 5.1 (the harness's own line; the effort setting is not shown to it). Every implementer, author, reviewer and scorer: `claude-opus-5-5` by its own report with the runtime effort it showed (15 for A8 and W1–W6 at launch; W2 showed 40 later), recorded as reported in the work log §3. The runtime model of the rehearsal runs: `claude-opus-5-5`, pinned in the package copy's `config/ai.yaml` for the host session and the critic, chosen and recorded separately (the work log §4); the repository's own config keeps `model: null`.
