# Session 08: audit fixes, the owner's source confirmations, interpretations, A1–A3, A5 and Gantt, clarifications

- **Date:** 3 Oct 2026 from 19:29:58 UTC to 20:27 UTC; paused at a usage limit; resumed 4 Oct 2026 at 05:17:22 UTC.
- **Who:**
  - **The owner (Ahmad)** gave the instructions, reviewed and confirmed the two image readings, directed three interpretations, and steered the work in a follow-up message.
  - **The assistant** (Claude Code, in the cloud container) did the work, as orchestrator, with four subagents (§4.8).
- **Records of the exchange:** `worklog/2026-10-03_session-08_prompt.md` holds the owner's three messages verbatim (the main message, the follow-up, the resume message), with their received times from the session transcript.
- **What the owner decided in this session (and only this):** the confirmations of the two readings (§4.2) and the direction of the 8.3, 3.4 and 6.7 interpretations (§4.3). Rows and ops are still PROPOSED: no `accept` or `reject` decision has been recorded (`curation/reviews/decisions.yaml` does not exist).
- **Nothing was sent** to the hiring team or anyone else. The clarification questions are drafts.
- **Deferred, as directed:** the Claude Code app, OpenRouter and Ollama integrations, model selection, model-cost calculations and the cost-per-bid follow-up (§4.9).

## 1. The exchange

The owner's main message (received 19:29:58 UTC) asked for seven things: (1) reproduce and fix four engineering findings, with failing regressions first, and fix the decision workflow before recording anything; (2) record the owner's confirmations of the Form 4-C and Table 2-4 readings, with their limits; (3) apply three interpretations (VOL-I 8.3, 3.4, 6.7); (4) complete A1–A3; (5) improve A5 and generate a Gantt; (6) keep a tender clarification register; (7) verify, log and return the work, and stop before final submission.

The follow-up (19:58:25 UTC, sent twice) interrupted the work just after the assistant had written the three interpretations straight into the register rows: show the existing proposal, its exact conflict with the direction and the source evidence for the replacement; each interpretation must be supported by the tender clauses and amendments; preserve the originals and the reasons for superseding them; do not bypass the review workflow; keep clear that the Permit confirmation covers only where the precedence language is; use subagents effectively.

The verbatim texts are in the prompt file. The owner's steering in them is followed in §4; where the assistant departed from it or could not follow it, §5 and §7 say so.

## 2. Timeline

All times UTC, from the session transcript's timestamps.

| UTC | Step |
|---|---|
| 3 Oct 19:29:58 | Owner's message. |
| 19:30–19:31 | Read the decision, engine, trace and schedule code. Message preserved verbatim (19:31:40). |
| 19:31–19:34 | Read the evidence for the four findings. Wrote `tests/test_session08_audit.py` (9 tests). |
| 19:34 | **Failing regressions:** all four findings fail. Finding 1 reproduced end to end (§3.1); finding 2 shown on the real binding (19:34:59). |
| 19:35–19:38 | Fixes: engine subject and withheld state, single-pass evaluation, consumers, C46 needs, Working-Day windows. One self-inflicted error (E88). |
| 19:39–19:48 | Full suite: 355 passed, 1 failed (a session 06 test asserting the conflation the owner asked to remove; updated). |
| 19:48–19:49 | Outputs compared with `out/`: one wrong flag found and fixed (E89); otherwise only fingerprints and the new applied/withheld fields differ; A3 and A5 unchanged. |
| 19:49–19:53 | `approve` extended (record, versions, snapshot, differences shown before an approval is extended; tested on disposable copies). **The owner's two confirmations recorded** (19:52:14); approved subjects checked against the packets the owner reviewed (19:52:23). Packets and batch 1 show the scope. |
| 19:53–19:56 | Register and issues updated for the confirmations (Form 4-C declaration 5 → VOL-I 4.2; "exclusion" kept apart; TN 5 vs 3; qualifier; Permit precedence location corrected to the p3 preamble; VOL-V 29.3). |
| 19:55–19:57 | The three interpretations written **directly into the rows** and pinned (E90). |
| 19:57–19:58 | A1/A3 inspection: Form 4-G, multi-unit rows, blank post-award evidence confirmed. |
| 19:58:25 | **Owner's follow-up.** |
| 20:00–20:03 | Direct writes reverted; originals kept and marked superseded with the exact conflicts; evidence-backed `P-S08-*` proposals written and every quotation checked; applied through `apply-proposal` on the owner's instruction; decisions and approvals under an assistant's name refused (E91); Permit scope split into confirmed / not confirmed. |
| 20:03–20:05 | Full suite started in the background. **Three subagents launched** (clarification register; post-award evidence; sealed unseen Addendum No. 3). |
| 20:06–20:12 | Form 4-G split into one row per undertaking; Form 4-A consequence moved off blank fields; A3 restructured (explicit, the 11.1(i) gate, grouped unresolved matters); A1 exports every unit of multi-unit rows. |
| 20:13 | **A5 and Gantt subagent launched.** |
| 20:13–20:25 | Suite result: 18 failures, all from the new state (approved readings, no STALE rows, superseded proposals) or from a run that collided with an edit (E99). Tests reworked with disposable fixtures (a no-approval build; the register before session 08) so they keep testing the same behaviour. Post-award evidence integrated (33 rows) and checked. |
| 20:24:55 | **Blind addendum frozen** (`rehearsals/blind-02/FROZEN.md`) before it was opened. |
| 20:26–20:27 | Clarification register reviewed and stored as curated data. |
| 20:27 – 4 Oct 05:17 | **Paused at a usage limit.** The A5 subagent had stopped on the same limit before writing anything. |
| 4 Oct 05:17:22 | Owner: continue. |
| 05:17–05:25 | Key test files run (2 failures from the fuller chain and the new headings; updated). **Checkpoint `2d5dda4` pushed.** A5 subagent resumed. |
| 05:25–05:31 | ADD-02 Q7/Q11 notes and settled-point issues corrected (E97); `tenderpack/clarify.py` and its outputs; `tests/test_session08_outputs.py`; blind-02 setup; plan revision 8 started; attribution note in the session 05 log (§4.10); prompt-file times corrected from the transcript (E101); operating guide. |
| 05:31–05:49 | The A5 subagent's work in progress committed (`5676441`, `38fe62f`: forward pass, float, effort vs waiting, gates, conditional items, Gantt); evidence rebuilt with the owner's approvals. A transient failure while its scenarios named an assumption not yet added (E103). |
| 05:49–06:20 | A1 per-stage source columns; tests follow the full chain in addendum order (E102) (`0565b2d`). The A5 subagent finished at 06:10:31; its work reviewed and integrated, outputs regenerated (`2708261`, 06:20). Full suite started on the committed state. |
| 06:20:31 | **Blind rehearsal 02 starts** (§4.7): set-up, ingest, draft, drafted outputs (06:21:57). |
| 06:22–06:33 | The assistant's working context was summarised; no work in this interval. |
| 06:33–06:52 | Curation of ADD-03: 31 ops; four live fixes with regressions; 8 new rows, 42 re-made readings, 6 issues; A5 templates; clarification register; curated outputs published (06:52:41); `diff`. |
| 06:50 | Full suite on `2708261`: **386 passed** (29 min 37 s). |
| 06:52:58 | **Key unsealed**; hashes verified. Pre-key state committed and pushed (`ec8085b`, 06:54). |
| 06:53–07:03 | Comparison written; post-key fixes (marked, not scored) rebuilt into `out-after-fixes/` (07:00). Real outputs rebuilt with the live fixes: byte-identical to `out/` (07:00). Final full suite started and `outputs --strict` run (exit 3; §6) at 07:01. Pushed (`c6bcbdb`, 07:03). |
| 07:03–07:30 | A date claim in the comparison corrected on re-check (E111, 07:03). Work log, PLAN §14, operating guide, cost and effort, before/after report (`e63b277`). |

## 3. The four findings, reproduced before any fix

### 3.1 A rejected op applied again after reject → rebuild → reject

Disposable decisions file; real pack; "Fixture Test Reviewer" (19:34:28):

```
build 0 | T1-1/B at ADD-02: superseded | ADD-02 APPLIED | review: proposed (not reviewed)
rejected op ADD-02/3.1 by Fixture Test Reviewer; bound to fingerprint 99e2e3baced961bb
build 1 | T1-1/B at ADD-02: active     | ADD-02 PARTIAL | review: rejected ... but CHANGED since: review again
rejected op ADD-02/3.1 by Fixture Test Reviewer; bound to fingerprint 1b224a73ddc1dab7
build 2 | T1-1/B at ADD-02: superseded | ADD-02 APPLIED | review: rejected ... but CHANGED since: review again
```

**Cause.** An op decision was bound to the content the op brought in, which existed only when the op applied: withholding a rejected op changed its own fingerprint. The first rejection then looked "changed", a "changed" rejection no longer withheld the op, and the second rejection (bound to the withheld state) made the next build apply it again. The loop in `stage2.run` re-ran the engine until the rejections were stable, which hid the dependency.

### 3.2 A changed old member row did not void a decision on the table's replacement

On the real binding (19:34:59): `before keys: ['VOL-I:T1-1']`; changing VOL-I:T1-1/B from 20 to 21 marks left the fingerprint unchanged. **Cause:** only the table container was pinned; its member rows were not.

### 3.3 An inserted obligation was covered by the anchor's existing row

With the rows citing the inserted Form 4-G item removed from a copy of the register, C46 still found no gap for ADD-02/7.1. **Cause:** the trace accepted any row citing the insertion anchor (VOL-I 9.1(e)), whose rows predate the insertion.

### 3.4 A one-Working-Day task with a Friday or holiday deadline

The backward pass put a 1-WD task on the Friday itself (`lf` not a Working Day); with a Thursday holiday the window was the holiday. **Cause:** the latest finish was the legal deadline, whatever the day.

## 4. Changes

### 4.1 The decision workflow (fixed before the confirmations were recorded)

- **Subject captured before each op** (`amend.Engine.subject`): the op's provision (text, pages, evidence anchors), its section heading, and the pin of every unit it reads or changes, including every member of a replaced table or form and of its replacement, inserted groups, annotated groups, covered provisions and claims, as they stand immediately before the op. A decision on an op binds to the op and this subject, whether or not the op then applies.
- **Three separate states on every op result:** `valid` (structural checks), `withdrawn` (a person's latest decision is a rejection; still checked, never applied) and `applied`. A provision whose ops are all withheld is `rejected` in the coverage; one whose ops are invalid is `unresolved`. Both keep the addendum PARTIAL. Consumers (trace, C28, A2, `diff`, batches, answers to review) were switched to `applied` where they meant it.
- **A rejection never lapses into applying.** `review.withdrawn_ops` withholds every op whose latest named decision is a rejection, whatever its fingerprint; a rejection made against a different subject is shown "CHANGED since: review again; the op is still withheld until a person decides again". The engine now runs once (`stage2.evaluate`).
- **Row decisions** also bind to where each of the row's units is printed (page, box, spans, reading subject).
- **C46:** an insertion needs a row holding the inserted item (or its provision) and a row holding the new group's content; the anchor's rows never count.
- **Working-Day windows:** a deadline on a weekend day or a declared holiday keeps its legal date; the work finishes on the last Working Day before it, flagged DEADLINE ON A NON-WORKING DAY; NO WORKING WINDOW when that day has passed but the deadline has not (an explicit conflict for a person).
- **Assistant names refused:** `accept`, `reject` and `approve` refuse a name that identifies the assistant or the program (E91).
- **Tests:** `tests/test_session08_audit.py` (11 tests, written failing first for the four findings; plus the changed-rejection and approval-record tests).

### 4.2 The owner's source-reading confirmations

- **Recorded** with `tenderpack approve` (19:52:14), reviewer "Ahmad", dated 2026-10-03 (the day of the confirmation; nothing backdated), confirmation record = the owner's message (prompt file §2).
- **Same versions as reviewed:** the reading files are unchanged since commit `1997ef8`; the approved review subjects (`6bc65059…` Table 2-4, `f433c2ca…` Form 4-C) equal those in the session 07 archive's packets (`9fdfd96`), which the owner reviewed.
- **Each entry records:** the subject sha256 and evidence, the reading file's sha256, last commit and a snapshot, what the owner confirmed, what he settled, what stays open, and what the approval does not cover (changed or unseen content, the register's interpretations, amendment operations, bidder compliance).
  - Form 4-C: declaration 5 refers to VOL-I 4.2 (the owner settles the uncertain digit; the alternative 4.3 is set aside). Open: diacritic placement; "exclusion" is not treated as equivalent to the other consequence categories.
  - Table 2-4: the qualifier and the limits as read (including 2.2). TN = 5 mg/l is the original reading; 3 mg/l is ADD-02 5.1's separate amended value. Open: the qualifier's interaction with the chlorine and pH ranges; each parameter's own basis; anything outside the visible image; VOL-V 29.3's Ramp-Up exception kept as a payment exception only.
  - **Permit (after the follow-up):** the confirmation covers only the location of the precedence language (the VOL-II p3 reproduction preamble, text layer, outside the image); the Permit's contents and Permit compliance are recorded as **not confirmed**. The entry says it was amended for this, by whom and when.
- **Differences before extending an approval:** `approve` now prints every meaningful difference from the approved snapshot and writes nothing unless run again with `--confirm-changes` (tested on disposable copies).
- **Register follow-through:** Form 4-C declaration 5 → VOL-I 4.2; the "exclusion" category kept apart (new issue I-F4C-EXCLUSION); Table 2-4 rows' "pending" wording replaced; the Permit precedence cited at the p3 preamble (it had said VOL-II 2.4); VOL-V 29.3 stated as a payment exception, not an exemption from technical compliance or commissioning.

### 4.3 The interpretations of VOL-I 8.3, 3.4 and 6.7 (after the follow-up)

The three rows are the three STALE rows of session 06, which had prepared proposals (`P-STALE-*`) the owner had said not to apply. The owner's direction differs from each:

| Row | Existing proposal said | Exact conflict with the direction | Source evidence for the replacement (verbatim, checked) |
|---|---|---|---|
| VOL-I-8.3-01 (ISO) | "...must be current on 26 November 2026 ... No consequence is stated (I-NO-CONSEQUENCE)" | Said there is no consequence and did not cite the 11.1(i) gate; kept only "current as at the Proposal Due Date", dropping the accredited issuer and the Envelope A copy; gave the date without the time | VOL-I 8.3 p4 (certificate, current as at the PDD, accredited body, copy with Envelope A); 2.6 p2 (the PDD is "the date and time ... as ... amended"); 6.1 p3 and ADD-01 2.1 p1 (26 Nov 2026, 14:00 unchanged); 11.1 p5 ("(i) a responsiveness and mandatory compliance check on a pass or fail basis; (ii) ... those Proposals that pass stage (i)"); no ADD-02 op touches 6.1 or 8.3; no clause allows or excludes a cure |
| VOL-I-3.4-01 (omission claims) | "no omission claim is entertained after 26 November 2026. In practice the known gaps ... must be raised ... before the VOL-I 5.2 cut-off" | Date without the time; tied the omission cut-off to the clarification deadline, which 3.4 does not mention | VOL-I 3.4 p3; 2.6 p2; ADD-01 2.1 p1; 5.2 p3 (ten Working Days before the PDD); ADD-01 2.2 p1; 3.3 p2 |
| VOL-I-6.7-01 (withdraw/modify) | "a withdrawal or modification must be notified ... before then; none is accepted afterwards"; requirement "only before" | "none" and "only" extend the late prohibition to withdrawals; 6.7 says "No modification will be accepted thereafter" | VOL-I 6.7 p3; 2.6 p2; ADD-01 2.1 p1; no addendum amends 6.7 |

- **First attempt (E90):** at 19:57 the assistant wrote the three interpretations straight into the rows and pinned them. The follow-up stopped this; it was reverted at 20:01 (the rows and pins returned to their committed state).
- **Through the workflow:** `curation/register/proposals/2026-10-03_session-08_owner-directed.yaml` holds `P-S08-VOL-I-8.3-01`, `-3.4-01`, `-6.7-01`, each with the owner's direction (quoted), the source evidence (14 quotations, all checked against the evidence build; the three non-quotation statements checked by test), a corrected requirement summary and the interpretation. The originals stay in `2026-10-03_stale-rows.yaml`, unchanged, marked `superseded` with `superseded_by` and `superseded_because` (the conflicts above); `apply-proposal` refuses them.
- **Applied** with `apply-proposal ... --by "Claude Code (assistant), on Ahmad's written instruction of 3 Oct 2026 (session 08 §3)"`, because the owner's message said "Apply these interpretations". Each row is now not STALE and is **PROPOSED**: the owner still accepts or rejects it. The assistant's name cannot be used for that decision.
- **The wording respects the limits given:** 8.3 cites the 11.1(i) gate, keeps the issuer and the Envelope A copy, and states that the pack gives no ISO-specific label and says nothing on cure (neither implied); 3.4 keeps 14:00 and a separate cut-off from 5.2; 6.7 keeps the late prohibition to modifications. I-NO-CONSEQUENCE was reworded the same way ("no clause-specific consequence; the 11.1(i) gate applies").

### 4.4 A1–A3

- **Form 4-G:** six rows, one per undertaking, each with its own quote (24-hour incident notification, annual independent penetration test and report, MFA and logging, the security officer, segregation, the ISMS), plus the signature and submission rows.
- **Multi-unit rows:** A1's "Text as issued" and "Effective text" list every unit with its reference; a new column lists every cited unit with the ops that amended it; each "Status after ADD-0N" carries its source when amended; the evidence chain covers every unit (it now shows ADD-02/9.2 ending ADD-01 4.2 in the LCC row, which the first-unit chain hid).
- **Post-award "evidence needed":** a subagent drafted the 33 blank entries from the clauses (24 proposed requirements, 3 not applicable, 6 unresolved because Schedules 7/11, the Direct Agreement or a definition are missing); the assistant reviewed and integrated them (`post_award_evidence` on the row model). check-register verifies every quotation and refuses a blank post-award field. None says the bidder holds anything.
- **Form 4-A:** VOL-IV-F4A-02 no longer carries VOL-I 9.3's consequence: a blank field is not "unsigned or improperly executed". The execution consequence stays on VOL-I-9.3-01.
- **A3:** explicit consequences by category (rejection, disqualification, non-responsive, exclusion kept apart, Envelope B returned unopened), each citing the amendment beside the consequence (the late-submission line: VOL-I 6.6 with VOL-I 6.1 as amended by ADD-01 2.1); the general mandatory-compliance gate (VOL-I 11.1(i)) as its own list; every open issue grouped by theme, with the clarification question ids, each linked to its detail. One page.

### 4.5 The tender clarification register

- A subagent drafted it from the pack (21 questions, 20 topics closed without a question, 8 unavailable items; 142 quotations checked). The assistant reviewed every entry against the clauses, kept it as curated data (`curation/clarifications/register.yaml`, with a theme per question) and wrote `tenderpack/clarify.py`: check-register verifies every quotation and page, the fields the owner listed and that no status says "sent"; `out/a4/clarification_register.{md,csv,json}` (archive: `A4_work_log/clarification_register/`); A3 lists the ids by group; A1's Issues sheet links them.
- Settled points are kept as settled: ADD-02 Q7 (precedence), Q11 (design to the Volume II figures), Q13 (12.2 periods unchanged); copy quantities per Proposal; Excel required; Form 4-G's obligations valid; average and peak flows not contradictory. Follow-ups ask only what those answers leave open. The interim approaches for Form 4-A, Envelope B and Form 4-B are the owner's.
- The existing texts that misstated those answers were corrected (E97).

### 4.6 A5 and the Gantt

A subagent did the A5 work from a written brief, working only on its own files: `tenderpack/schedule.py`, `tenderpack/programme.py`, the new `tenderpack/gantt.py`, the A5 templates and assumptions, and `tests/test_session08_a5.py`. The assistant reviewed the diff, ran the tests, integrated it, and checked that the A5 README matches the outputs.

- **Planning basis.**
  - The planning date is the latest addendum's issue date: 22 Oct 2026 for the real pack.
  - The consortium is editable in `config/assumptions.yaml`: three members, one of them foreign (scenarios with no foreign member and with two).
  - Every duration and effort figure is labelled PROVISIONAL ASSUMPTION, with its basis.
  - Shared data comes from A1: every activity carries the A1 requirement ids it supports.
- **Scheduling.**
  - A forward pass (ES/EF) from the planning date and a backward pass (LS/LF) from the pack deadlines, in Working Days.
  - Total float; negative float is shown as `INFEASIBLE by n WD` and never compressed. `drivers.csv` says what would make it feasible.
  - Elapsed duration is kept apart from staff effort (`effort_wd`), and `waiting_on` names the external party.
- **Three separate statuses on every activity.**
  - timing: OK / INFEASIBLE / DEADLINE PASSED / NO WORKING WINDOW / CONDITIONAL;
  - decision: READY, or GATED by an open issue, with the date the decision is needed;
  - resource: OK or OVERLOAD.
  - Only finalisation is gated; preparation continues.
  - The real pack has four gates: Form 4-A (I-F4A-FIELDS), Form 4-B (I-VOL-I-ENV-A-PRICES), Envelope B (I-VOL-I-ENV-B), copies (I-VOL-I-COPIES).
- **Resources and conditions.**
  - Disciplines and resources are listed; 5 overload runs are reported and not resolved. No levelling is claimed.
- **Dates and conditions.**
  - Fixed pack dates are milestones at their legal dates.
  - Conditional obligations are shown as conditional. The ADD-01 3.1 attendance notice reads "CONDITIONAL — window elapsed 2026-10-14; whether the condition arose is not known": an elapsed window, not a missed duty.
- **Marshalling plan.** 26 items: each deliverable with its count, issuer, envelope and A1 ids.
- **Findings on the real pack.**
  - 43 activities. The Local Content Certificate chain and the delivery chain are INFEASIBLE by 12 WD on the provisional durations.
  - That is a finding for the owner, not a plan: the durations are assumptions to replace with real ones.
- **Gantt.** `a5/gantt.{svg,html,pdf}`, in Working Days, with float, gates, conditional items and milestones.

### 4.7 Blind rehearsal 02

Full record: `rehearsals/blind-02/COMPARISON.md`, `README.md` and `clock.txt`.

- **Through the normal pipeline**, as a live session would: `ingest` → `draft` → drafted outputs → curation of the op file, the register, the issues, the A5 templates and the clarification register → `pin` → `check-register` (0 findings) → `outputs` → `diff`. Then the key was unsealed. From receipt to the scored output took 32 minutes, including about 10 minutes when the assistant's context was being summarised.
- **Result against the sealed key:** 30 provisions, answers and notes; 24 hits, 6 partial, none missed.
  - Every expected date is reproduced; the look-back start by its alternative reading, one day apart by stated convention.
  - Every "must not report" trap was avoided: the PDD date is not changed, the revocation gives 72 h, the re-lettered "(i)" means the Powers of Attorney, and Q17/Q19/Q21 have no effect.
- **What failed.**
  - The cover-summary check missed both planted cover errors: "The Proposal Due Date is unchanged" was not extracted as a claim, and the Bid Bond validity omission was inverted.
  - The curator's `lesser` class on the Q15 and Q16 refusals took two existing rows off the A3 gate.
  - Note (3) was mis-classed.
  - The model-auditor steps stayed in the pre-submission programme.
  - `diff` does not flag multi-unit rows whose secondary units changed.
  - The register has no status for deleted words in a clause that stays in force.
- **Four live fixes, all general and each with a regression** (`tests/test_blind02_live_fixes.py`): Volume appendix citations; quoted row names; letter ranges in a re-lettering; C47 alignment around punctuation. The fixes leave the real pack's outputs byte-identical.
- **Post-key fixes** (marked, not scored) are in `out-after-fixes/`. The tool follow-ups go to PLAN §14.

### 4.8 Subagents

Each started cold from a written brief, worked on its own files or outside the repository, and reported back; the assistant reviewed every result before using it.

| Subagent | Brief | Result |
|---|---|---|
| Clarification register | Research the topics the owner listed, apply precedence and existing answers, draft questions per VOL-I 3.3 and 5, verify every quotation, send nothing | 21 questions, 20 closed without a question, 8 unavailable items; 142 quotations verified; adopted after review (§4.5). Reported 276,780 tokens; finished 20:25 |
| Post-award evidence | One entry per blank post-award row: proposed requirement, not applicable or unresolved; never imply evidence is held | 33 entries, 60 basis quotations verified; integrated (§4.4). Reported 169,540 tokens; finished 20:14 |
| Blind addendum author | Write an unseen-style Addendum No. 3 from the PDFs and the brief only; seal the key outside the repository; reply with hashes only | 4-page PDF, issued 3 Nov 2026; hashes frozen before it was opened (§4.7). Reported 254,315 tokens; finished 20:20 |
| A5 and Gantt | Forward/backward pass, float, effort vs waiting, overloads, gates, conditional items, marshalling completeness, Gantt; only its own files | Stopped by the usage limit before writing anything (20:27); resumed 05:25; finished 06:10; reviewed and integrated by 06:20 (§4.6) |

### 4.9 The plan

Revision 8 (`docs/PLAN.md`): status, a revision row, §4.6 restating that every route (the Claude Code app, OpenRouter, Ollama, a person) produces PROPOSED records that pass the same checks and need a person's decision, and that integrations, model selection, model-cost calculations and the cost-per-bid / eight-concurrent-bids follow-up wait until the owner has set up the API and local-model routes; §14 for this session. The reviewed build runs with no model.

### 4.10 Attribution

- **Corrected:** the session 05 log presents the owner's message verbatim, but the owner's own words naming a model had been replaced by "[model name omitted in the repository]" (commit `33f1f81`). A note now says so on the line itself: the words were the owner's, removed because no model identifier may be written into the repository's files, and the message as first recorded is unchanged in commit `6a5d6cb`. The redaction stays: this environment's rules forbid model identifiers in repository files, which overrides restoring them; the history (including `6a5d6cb`) is kept as the owner asked, nothing rewritten.
- **Checked, accurate:** "the owner's email of 1 Oct" (the assumptions) is Ahmad's email to the hiring team (`sources/correspondence/2026-10-01_questions_to_hiring.md`), and the hiring team's reply confirms the basis.
- **Times:** the prompt file first gave approximate received times; they were replaced by the transcript's (E101).

## 5. Errors and corrections

| # | Error | Found | Fix |
|---|---|---|---|
| E84 | A rejected op applied again after reject → rebuild → reject (§3.1) | Owner's review; reproduced 19:34 | Subject before the op; rejection always withholds; single pass |
| E85 | A decision on a table replacement ignored its member rows (§3.2) | Owner's review; reproduced 19:35 | Every member of the replaced and replacing groups pinned |
| E86 | C46 accepted the insertion anchor's row (§3.3) | Owner's review; reproduced 19:34 | Each inserted part needs its own row |
| E87 | A 1-WD task on a Friday/holiday deadline had a non-working window (§3.4) | Owner's review; reproduced 19:34 | Last Working Day before the legal deadline; explicit flags |
| E88 | The assistant's own edit inserted `window_flags` inside `backward_pass` (TypeError) | 19:38, by the tests | Moved |
| E89 | The first NO WORKING WINDOW also flagged an activity whose window was set by its successors (lcc-ratio) | 19:48, by comparing outputs | Only when the deadline itself sets the window |
| E90 | The owner-directed interpretations were written straight into the rows, bypassing the proposal step | Owner's follow-up, 19:58 | Reverted; evidence-backed proposals; originals kept with reasons; applied through the workflow |
| E91 | `apply-proposal` suggested `accept` with the applier's name, which was the assistant's | 20:02, on reading its output | Message fixed; assistant names refused for decisions and approvals |
| E92 | Register texts said "pending" statically, and cited the Permit's precedence at VOL-II 2.4 | 19:54, after the confirmations | Wording made accurate; citation moved to the p3 preamble |
| E93 | Form 4-A's completion row carried "unsigned or improperly executed → non-responsive", as if every blank field were fatal | 20:07, A3 inspection | Consequence only on the execution row |
| E94 | Form 4-G undertakings 3–6 were one row behind one quotation | 19:57, A1 inspection | Six rows |
| E95 | A1 exported only the first unit of a multi-unit row (Table 2-2 values and citations lost) | 19:57, A1 inspection | Every unit exported; full chain |
| E96 | 33 post-award rows had a blank "evidence needed" | 19:57, A1 inspection | Filled and checked (§4.4) |
| E97 | Issue and op texts misstated ADD-02 Q7 ("declines to amend"; "not answered") and Q11 ("did not answer"), and treated settled points (copies per Proposal, Excel) as open | 20:27–05:25, reviewing the clarification register | Reworded: settled vs follow-up |
| E98 | Edit slips: a YAML closing quote lost (05:25); a quote-escaped search string missed (20:01); a test asserted "curable" for "can be cured" (05:29) | At once | Fixed |
| E99 | A suite run collided with a model change and produced transient load errors (20:14) | Reading the failures | Re-run after the edit |
| E100 | The A5 subagent stopped on the usage limit before writing anything | 4 Oct 05:17 | Resumed with its context |
| E101 | The prompt file gave approximate received times | 05:31, against the transcript | Exact times |
| E102 | `test_drill` assumed the evidence chain in the order units were cited; the full chain lists ops in addendum order | 06:10, by the test | The chain sorted by stage; the test follows it |
| E103 | A rebuild failed while the A5 scenarios named `bidder.foreign_members` before the assumption existed | 05:27, by the build (it refused) | Integrated together; rebuilt |
| E104 | Blind-02 curation: two `annotate` targets that the provisions do not cite (Q16 at the issued item (h), Q21 at VOL-I 6.1) | 06:36, by C22 | Q16 on the cited list VOL-I 9.1 with the mapping in the note; Q21 on ADD-03 2.1 |
| E105 | Blind-02 curation: the first 7.2 note said Volume IV has no Index of Forms (it is the cover table) | 06:41, on reading the cover units | Corrected before the build |
| E106 | Blind-02 curation: two issue themes outside the A3 vocabulary | 06:43, on writing them | Mapped to existing themes |
| E107 | The first C47 fix also stripped punctuation from the words it checks, breaking two true matches | 06:48, by the build (C47 failed on them) | Align without punctuation; check the words as printed; regression |
| E108 | A post-key edit broke the YAML quoting of a note, and one note replacement silently matched nothing (wrapped text) | 06:58, by check-register and a count | Edited through the YAML structure |
| E109 | Blind-02 curation: `lesser` for refusals of a submitted document (Q15, Q16) took two rows off the A3 gate; `score_elimination` for a zero on one criterion | After unsealing, by the key | Post-key fix (not scored); curator guidance in PLAN §14 |
| E110 | Blind-02 curation: the model-auditor appointment and review stayed in the pre-submission programme | After unsealing, by the key | Post-key fix (not scored) |
| E111 | The comparison first said every expected date was reproduced; the look-back start is the alternative reading (one day apart, by stated convention) | 07:03, on re-checking the dates | `COMPARISON.md` corrected; the `c6bcbdb` commit message keeps the first wording (history not rewritten) |
| E112 | The archive check reported 5 of 537 A3 links as broken: their targets contain parentheses (`note(2)`), which PDF escapes, and its regular expression stopped at the escaped `)`. The links were valid (the ids exist; viewers decode the escape) | 07:33, first verification of the `091dbe9` archive | The verifier reads the target as a PDF literal string; test `tests/test_archive_scripts.py`; archive rebuilt and re-verified |

## 6. Verification results

All runs on the cloud container: Linux x86_64, CPython 3.11.15, PyMuPDF 1.28.2, openpyxl 3.1.5. No Mac, native Excel or native PDF viewer was used.

| Check | Result |
|---|---|
| The four findings' regressions (`tests/test_session08_audit.py`) | Failed before the fixes (19:34, §3) and pass now |
| Session 08 tests (`test_session08_outputs.py`, `test_session08_a5.py`, `test_blind02_live_fixes.py`) | Pass |
| Full suite on `2708261` (before the blind-02 live fixes) | **386 passed** in 29 min 37 s (06:20–06:50) |
| Full suite with the four live fixes (the code as committed in `c6bcbdb`; later commits change documents only) | **390 passed** in 29 min 59 s (07:01–07:31) |
| Fresh build of the real pack with today's code | `outputs` into a new folder: exit 0. **Every file byte-identical to `out/`**, the review packets included (07:00) |
| Strict mode (`outputs --strict`) | **Exit 3: release refused**; the previous outputs kept. Blockers: 205 of 205 rows and 37 of 37 ops without a named decision. No reading blocker (both readings carry the owner's confirmations), no STALE row, no structural failure |
| Unseen-style rehearsal | `rehearsals/blind-02/COMPARISON.md`: 24 hit, 6 partial, 0 missed, out of 30; C28 missed both planted cover errors; four live fixes; post-key fixes kept apart |
| Archive | `LAMAR-PPP-R2-DRAFT_eb32b13`: every check passes, including the offline rebuild and 391 tests offline (§6.1). This result is recorded after the archive, which cannot contain its own verification |

**Content and rendering are reported apart** (`scripts/compare_outputs.py`). Content identity covers the text deliverables (CSV, JSON, Markdown, HTML, YAML, SVG): byte-identical, or the content differs. For the rendered files (PDF, PNG, XLSX), the bytes are compared first; if they differ, the content is compared: every PDF page's text and link targets, a PNG's size, every cell of every sheet. Bytes that differ with identical content are a platform rendering difference (fonts, image encoding, zip compression), reported but not a failure. Only the Linux container was checked. On a Mac, the PDF and XLSX bytes may differ while their content matches (`docs/VERIFY_ON_MAC.md`).

### 6.1 The archive from `eb32b13`, checked in a fresh folder

The check is `scripts/verify_archive.py` (Linux x86_64, CPython 3.11). It ran from 07:34:05 to 08:15:46, 2,501 s in total. The first archive, from `091dbe9`, stopped at the A3 link check (E112, a verifier bug); the fix is in `eb32b13`, which this archive holds.

| Step | Result |
|---|---|
| Extraction | 252 entries |
| `SHA256SUMS` | 251 files match; no unlisted file |
| A3 | One page; 537 `/URI` links (111 targets), each to an id in `a3_detail.html` |
| Review pages | 13 pages, 240 `src`/`href`, all resolved inside the archive |
| Bundle | Clones to HEAD `eb32b13`, 33 commits, tree clean. The full history is kept, including `6a5d6cb` |
| Network | None inside `unshare -n` |
| Offline install | Linux wheelhouse, 12 s |
| Offline regeneration | `make evidence` 14 s; `outputs` 66 s; `drill` 84 s; `rehearsal` 213 s; blind-01 re-ingest and rebuild 71 s; blind-02 re-ingest and rebuild 149 s |
| Clean tree | Every regenerated file is byte-identical to the committed one (`build/`, `out/`, both drills, both blind rehearsals' `out-after-fixes`) |
| Archive comparison | Content identical: 181 files, all byte-identical; no rendering-only differences on this platform |
| Tests | **391 passed** offline in 31 min 30 s (the 390 plus `test_archive_scripts.py`) |

**The Mac setup files.**

- **Byte-identical to session 07.** The wheels and `requirements.txt` for both architectures are byte-identical to the ones delivered in session 07 (`uv.lock` is unchanged), so they were not sent again.
- **Parts.** Joined with `cat`, each part set matches its `.sha256` and unzips: arm64 in 5 parts, x86_64 in 4.
- **Offline resolution.** With uv and no network, every requirement resolves for Python 3.11, 3.12 and 3.13 on Apple silicon, and on Intel with a macOS 14 target. Against macOS 13 on Intel it fails, because numpy needs macOS 14 (documented in `docs/VERIFY_ON_MAC.md`).
- **Not done:** installing or importing on a Mac.

## 7. What this establishes, and what it does not

**Establishes:**

- **The four findings.** The four reviewed findings are reproduced by tests that failed first, and pass now: a rejection can never flip back into force; a changed member row voids a decision on its table's replacement; an insertion needs its own row; a Working-Day window never falls on a non-working day, and the legal deadline never moves.
- **The confirmations.** The owner's two confirmations are recorded against the same versions he reviewed. Their limits are kept: Permit location only; diacritics and "exclusion" open; qualifier interaction open.
- **The three interpretations.** They went through the proposal workflow with verbatim, checked evidence. The originals and the reasons for superseding them are kept, and the rows remain PROPOSED.
- **The unseen addendum.** It went through the normal pipeline in about 20 minutes of work, with every date and trap right. Its gaps were found by a sealed key, not by the curator.

**Does not establish:**

- **Correctness.** That any row, op, interpretation or clarification question is right. None is accepted; passing tests are not approval.
- **Releasability.** That the outputs are releasable: strict mode refuses them (205 rows and 37 ops await a person's decision).
- **The A5 durations.** They are provisional assumptions. The INFEASIBLE chains are findings to check with real lead times.
- **Other environments.** Only the Linux x86_64 container was checked (Python 3.11.15, PyMuPDF 1.28.2, openpyxl 3.1.5). The Mac, native Excel and native PDF viewers were not.
- **The cover-summary check.** That it catches misleading cover summaries: rehearsal 02 shows it does not yet.
- **Blindness.** Full blindness: the curator also wrote the tool and knew the addendum would be "unseen-style".
