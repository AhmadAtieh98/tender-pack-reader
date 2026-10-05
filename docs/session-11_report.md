# Session 11 report: the workflow finished, the AI phases under one set of controls, blind rehearsal 05, and the audit of the real package through ADD-02

For the owner. The full record is `worklog/2026-10-04_session-11_workflow-and-audit.md`; your message is kept verbatim in
`worklog/2026-10-04_session-11_prompt.md`. **Nothing was committed during the session** (your instruction); the work was committed afterwards as `6053493`
(08:20 UTC, 5 Oct) on your authorisation and pushed. Nothing was approved, accepted, rejected or sent. Cost and pricing stay provisional.

## 1. What you asked, what was done

| Part | Asked | Done | Where |
|---|---|---|---|
| 1 | Finish the downstream workflow: explicit, evidenced requirement introduction; ID-based row updates; honest completion; bindings over every curated input and revalidation before promotion; a consecutive-addenda test; a host-driven run to a usable candidate build with interventions recorded | Done (D1, failing tests first against the committed code): `Row.introduced` and the applicability rule (NOT IN FORCE / NEW), checked against the printed words; downstream validation at every stage; rows found and updated by id; `completeness` / `execution` / `approval` records; identity over register, relationships, issues, dispositions, evidence items, clarifications, ledger, scenarios, triggers, formulas; revalidation before promotion; the four-addenda test; a recorded end-to-end run; blind-04 as the host-driven run (see §3) | `tenderpack/register.py`, `ai/downstream.py`, `ai/workflow.py`, `ai/tools.py`, `ai/contract.py`; `tests/test_session11_downstream.py`, `tests/test_session11_stages.py` |
| 2 | The same controls for every AI phase; failure classes; bounded backoff; resumable checkpoints; less repeated context; the critic inside the workflow; routes kept, tested vs unverified stated | Done (D2): `tenderpack/ai/requests.py` (one path for readings, analysis, downstream, critic; schemas; capability checks; complete sizing; split or escalate, never truncate; bounded repair; visible notices); `config/ai.yaml` failure classes; `resume` re-asks deferred batches only; `concurrency.batches: 1`; the critic after each analysis batch and after downstream validation; `ai propose` and `host-session` on the same layer | `tenderpack/ai/requests.py`, `hostsession.py`, `batching.py`, `critic.py`, `providers/*`, `config/ai.yaml`, `docs/AI_ROUTES.md` §§12–16; `tests/test_session11_requests.py` |
| 3 | Deterministic calculation tools; relationship discovery and propagation; cycle-safe traversal with completeness; blockers through chains; conditional and effective-dated amendments incl. amendments of amendments; confirming vs changing answers; the critic on cover wording | Done (D3): `tenderpack/calc.py` + `config/formulas.yaml`; `relationships.trace` cycle-safe with completeness and a budget; blockers propagated; `relationships discover`; `effective_from` and `condition` on ops; triggers only from a person's record; `classify_answer`; direction claims checked against the numbers (C28) | `tenderpack/calc.py`, `relationships.py`, `amend.py`, `register.py`, `schedule.py`, `summary.py`, `cli.py`, `ai/tools.py`; `tests/test_session11_calc.py`, `_relationships.py`, `_conditional.py` |
| 4 | Labelled candidate A3/A5 for partial addenda; crops, Arabic, translations kept; the maxima ambiguity unresolved; the Permit visible; blind-04 as regression; a new sealed rehearsal timed against 30 min; an interrupted or rate-limited run resumed | Done (D4, the coordinator): `tenderpack/partial.py` (candidate A3 and A5 beside the validated ones); blind-04 regression to a published candidate build with a crash and a rate limit survived; blind-05 sealed run: blind-05 sealed run scored 21 hit / 16 partial / 1 missed of 38 (1 false positive, fixed post-key) in 72 min 27 s against 30, no interruption, no manual intervention | `tenderpack/partial.py`, `render.py`, `programme.py`, `live.py`; `rehearsals/blind-04/REGRESSION-S11.md`, `rehearsals/blind-05/` |
| 5 | An independent audit of BASE → ADD-02 and the emails across A1–A5 and the rendered files; stale statements; a brief-requirement matrix; fixes and rechecks; regressions, the suite, a fresh rebuild, the strict check | Six independent reviewers (A1, A2, A3, A4, A5, R), expectations first; 1 blocking (the owner's decision), 27 major and 26 minor findings; fixes by three fixers and the coordinator: three fixer agents (F1 A1/A2: 21 findings, 20 failing-first tests; F2 A3/R: 14 findings, 13 tests; F3 A5: 9 findings, 13 tests) in a separate worktree, merged after blind-05; the coordinator fixed the A4 record items and the rechecks' leftovers; rechecks: the five original reviewers rechecked the rebuilt outputs against their own expectation notes: 41 of 46 findings fixed outright, the rest fixed afterwards or the owner's (§4, §6); verification: final tree, 5 Oct 07:33–07:54 UTC: `ingest` 524 units STRUCTURE OK (04:08); `outputs` exit 0, structural checks ok (C13 17 items; C43 one page at 7.72 pt; C46, C48, C52 ok; C28 report-only findings on both covers); `outputs --strict` exit 3 with exactly the two human-approval blockers (205 of 205 rows and 37 of 37 ops proposed) and no defect blocker; the full suite **776 passed, 0 failed** in 20 min 46 s (the session added 118 tests across 13 new files, each regression written failing first; 4 existing expectations changed with a comment); the real pack's `out/` and `build/` regenerated from the finished code | §4–§6 below |

## 2. Models that actually ran

- The coordinator: Fable 5.1 (this session's configured model, as the session reports it).
- Subagents (launched with the Opus option; each reported Opus 5.5 by its own instructions, which the launching session
  cannot verify): four implementers D1–D4, the blind-05 author, six audit reviewers, three audit fixers.
- The headless host sessions of the rehearsal runs: `claude -p --model opus`; the CLI reported `claude-opus-5-5` in
  every session (`staging/ai/runs/*/ai/*/session.json`).
- No API-key call was made (no key in the container); the Anthropic, OpenRouter and Ollama routes are tested with
  recorded responses only and stay unverified live.

## 3. The rehearsals

**Blind-04 as regression** (`rehearsals/blind-04/REGRESSION-S11.md`): the same Addendum No. 3 through the fixed
workflow on the host route, 22:22 → 02:54 UTC with a container restart and the plan's rate limit in between. Steps:
63 min of work; the candidate build published (101 files with the banner); completeness partial with its reasons
(1 provision unresolved; 34 of 51 downstream tasks answered by promotable items, 17 only by unpromotable ones, 0
unanswered; 12 check-register findings naming the obligations no promoted row holds). No manual intervention; three
`ai resume` calls by the coordinator and one code fix between them (E135, below).

**Blind-05, sealed** (`rehearsals/blind-05/`): frozen before the run (`FROZEN.md`), the first outputs frozen by hash (`FROZEN-OUTPUTS.md`, 327 files) before the key was opened, the key then unsealed and verified; **21 hit / 16 partial / 1 missed of 38** expected findings (provisions 6/9/0 of 15; answers 7/0/0; cover errors 2/1/0; Arabic 3/0/0; secondary effects 3/6/1); 1 false positive (a plural clause list the citation parser did not read; fixed after the key with a failing-first test, labelled in `COMPARISON.md`) and 6 false signals (a decoy and a confirming answer marked as changes); 23 provisions unresolved with honest reasons; no manual intervention (15 automatic host sessions); review effort about 4 hours (an untested estimate); **72 min 27 s** from the PDF to the candidate outputs and the review packet, no interruption, against the brief's 30 minutes. The partials are mostly detected changes escalated or held instead of applied, and dates computed but not planned; the candidate build was published.

**What the interrupted runs showed:** a crash (the container restart, E134) and a rate limit (E136) were both survived
by `resume` without re-asking any done batch; the crash exposed E135 (a dead process's staging lock refused every later
session and the refusals were recorded as done batches), fixed with seven failing-first tests
(`tests/test_session11_locks.py`).

## 4. The audit: findings by deliverable

The reviewers derived their expectations from the brief, the email and the six PDFs before opening any output; their
reports and expectation notes are kept outside the repository (the coordinator's scratchpad) and summarised in the work
log. Severity: blocking (would mislead the assessors or a bid team), major (wrong but recoverable with the page in hand),
minor (presentation).

| Deliverable | Right about the documents | Defects (before fixes) | Status after fixes |
|---|---|---|---|
| A1 | All 205 rows' verbatim text at the cited page; the 20 image-read rows against the crops; dates; CSV/JSON/xlsx agree; nothing invented; the 70/30 trap not registered | 4 major (addendum effects invisible in the status column; VOL-I 9.1 not amended by ADD-02 7.1; the concession-term wording contradicts itself; an assumption shown as pack-stated), 7 minor | 9 of 11 fixed on the recheck, 2 minor points fixed by the coordinator afterwards (the Q12 chain link; the pass_fail reasoning); all 205 rows' text re-checked by the reviewer, nothing regressed; the relabels right against the sources |
| A2 | All 76 provisions accounted for; every moved date recomputed and right; before/after wording right; no requirement invented | 4 major (appended words shown as "None" and a reinstatement cut short; VOL-I 9.1; a wrong page label; op issues absent from the page), 6 minor | 9 of 10 fixed on the recheck, A2-6 completed afterwards (the op's effect) and one new minor wording fixed (A2-11); `a2_provisions` byte-identical, dates and wording unchanged |
| A3 | All 16 bid-out triggers present and correctly categorised; nothing that should be absent; the 18 items equal A1's | 6 major (no reasons on the page; INFEASIBLE without its basis; the gate heading's claims; the stale translation label; overlaps unfolded; footnote 12 paraphrased wider), 3 minor | all 9 fixed; all 16 triggers still present and categorised; one page at 7.7 pt; three minor leftovers fixed afterwards (a check-only INFEASIBLE flag, a cut-off reason, the † legend) |
| A4 | Error notes exist for every sampled fix; the clarification register grounded, draft, not sent; model attributions honest | 1 blocking (the undisclosed rewrite of four commits on 2 Oct, the owner's decision), 6 major (no entry point; subagent briefs absent; "nothing is committed" inside commits; "no live call"; the cost note; stale README lines), 4 minor | Fixed by the coordinator except the owner's decision (§6) |
| A5 | Every date computed backwards from the right deadline; all 43 activities' float recomputed with no difference; the Gantt matches the data; lead times labelled assumptions; the LCC infeasibility reported, not hidden | 4 major (decision gates after the clarification cut-off; a non-responsiveness row carried by no activity; a missing dependency; the change list calls confirmations changes), 4 minor | 7 of 8 fully fixed, the consortium check's timing fixed afterwards (before the clarification route); every date and float of the 44 activities recomputed by the reviewer with 0 mismatches; the Gantt matches |
| Rendering | A1 xlsx = CSV; A3 one page with every link resolving; the Gantt one page matching 43 activities and 22 milestones; banners present; nothing §4 forbids | 3 major (the translation label described three ways; the committed README stale; A3 reasons), 6 minor | 7 of 9 fixed in the outputs; R-10 (two confidence reasons) fixed afterwards; R-2 and the reading YAML headers wait on the owner (§6); the cross-document pass agrees |

## 5. The brief-requirement-to-artifact matrix

Each reviewer derived the rows of the brief for its deliverable (`A1-1` … `R-4`, `G-n` for the general rules) and judged them before the fixes; the same reviewer rechecked the rebuilt outputs afterwards (A4's rows were rechecked by the coordinator's record work, the history item excepted). After the fixes: 53 PASS, 1 FAIL, 2 PENDING of 56 rows. The FAIL is the undisclosed history rewrite (the owner's decision); the PENDING rows wait on the owner's commit of the rebuilt outputs and on the reading YAML headers the approvals pin by hash.

| Row | Requirement (from the brief or the owner's asks) | Reviewer | Before the fixes | After the fixes and rechecks | Note |
|---|---|---|---|---|---|
| A1-1 | "One row per requirement." | A1 | PASS | PASS (unchanged) | 70/30 minutes statement correctly not a row |
| A1-2 | "A requirement identifier" | A1 | PASS | PASS (unchanged) |  |
| A1-3 | "the verbatim source text" | A1 | PASS | PASS (unchanged) | Effective text is labelled "ASSEMBLED … not a printed text" |
| A1-4 | "the document, clause and page it came from" | A1 | PASS | PASS (unchanged) | A1-5 (one wrong page label in a chain) |
| A1-5 | "whether it is pass/fail or scored" | A1 | PASS (with note) | PASS (note: ADD-02-5.2-01 kept pass_fail, reasoned) | A1-10: two undefined extra values, uneven use |
| A1-6 | "the discipline that owns it" | A1 | PASS | PASS (unchanged) |  |
| A1-7 | "the evidence needed to prove compliance" | A1 | PASS (with note) | PASS | A1-7: codes undefined inside A1 |
| A1-8 | "its status after each addendum" | A1 | FAIL | PASS | A1-1, A1-2, A1-8 |
| A1-9 | "and your confidence" | A1 | PASS (with note) | PASS | A1-3: inverted on concession |
| A1-10 | "Machine-readable — CSV or JSON — plus whatever interface" | A1 | PASS | PASS (unchanged) | Visual render not verified (§6) |
| A1-11 | Owner's audit asks: completeness; source support; stage statuses; original vs amended; dates; assumptions; interpreta… | A1 | FAIL | PASS |  |
| A2-1 | "What each addendum changed, added and deleted." | A2 | FAIL | PASS | Only because of A2-1: the ADD-01 5.1 appended words show as "None", and the 9.1 reinstated text is cut before 35% and the consequence |
| A2-2 | "Which register rows move as a result." | A2 | FAIL | PASS | A2-2: VOL-I-9.1-01 shown as unchanged after ADD-02 7.1. A2-6: T1-1 A/C/E/F shown as AMENDED although unchanged |
| A2-3 | "Which earlier answers are now wrong." | A2 | PASS | PASS (unchanged) | The dedicated list is narrower than its title (A2-10) |
| A2-4 | "We must be able to trace any row back through the chain to the original document." | A2 | FAIL | PASS | A2-3: ADD-02-7.2-01 link says "VOL-I p3". A2-7: date-moved and Q-answer rows lack the addendum link |
| A2-5 | Every provision, note, table, form and image covered; the full chain, including superseded answers and indirect effects | A2 | PASS | PASS (unchanged) | Blocker propagation and the CSV are incomplete (A2-5 minor) |
| A3-1 | "One page" | A3 | PASS | PASS (unchanged) | It fits on one page only by removing the unresolved reasons (finding A3-1). Body text is 8.1 pt (PyMuPDF spans). |
| A3-1 | "One page" | R | PASS | PASS (unchanged) | The unresolved list fits only by dropping the "why" (R-3). |
| A3-2 | "Every requirement whose breach would put a bid out — the ones the documents themselves say cause rejection, disquali… | A3 | PASS | PASS (unchanged) | All 16 triggers are present and their categories match the wording. 11.3 and the Arabic "exclusion" are labelled separately. Obligations … |
| A3-3 | "with your confidence in each" | A3 | PASS | PASS (unchanged) | The medium ratings (6.2-02, F4C-04, F4C-N1) are explained only off the page. |
| A3-4 | "And, explicitly, the list of things your system could not resolve, and why." | A3 | FAIL | PASS | The "why" is not on the page (A3-1). INFEASIBLE flags lack their assumption basis (A3-2). |
| A3-5 | Owner asks: categories supported and distinguished; unresolved readable with reason on the page; condensed issue ids;… | A3 | FAIL | PASS | Categories: pass. Reasons on the page: fail. Ids understandable alone: fail. Deduplication: fail (A3-5, A3-6). |
| A4-1 | "The repository with its real commit history." | A4 | FAIL | FAIL (the owner's decision: disclose or stop calling the history real) | Rewritten on 2 Oct with dates preserved and no disclosure (A4-1). Sessions 09/10 are single commits; session 11 is uncommitted (A4-10). |
| A4-2 | "The prompts and model calls you used." | A4 | FAIL | PASS (briefs exported; "no live call" corrected) | Two owner prompts edited without a note and two messages left out (A4-1). Subagent briefs absent (A4-2). "No live call" stale (A4-5). Mod… |
| A4-3 | "a short written note of every place your system was wrong while you were building it, and how you caught it." | A4 | PASS (content) | PASS (unchanged) | Not short, no index, ids collide, 09/10 tables lack "how caught" (A4-3, A4-9). |
| A4-4 | "A work log that records no errors tells us you were not checking." | A4 | PASS | PASS (unchanged) | Includes errors where the model misled (E8 premature glyph claim; E20 reply reconstructed from memory). |
| A4-5 | Owner's asks: actual history, prompts, model/tool calls, errors, corrections, development; the clarification register… | A4 | FAIL | PASS (A4 index; the history item is the owner's) | out/a4 is honestly labelled "supporting record", but there is no A4 entry point (A4-3) and the history is undisclosed (A4-1). |
| A5-1 | "Generated by your system from A1 — not drawn by hand." | A5 | PASS | PASS (unchanged) |  |
| A5-2 | "the activities needed to get a compliant bid out of the door, with durations, dependencies, owners by discipline, an… | A5 | PASS | PASS (unchanged) | One dependency missing (A5-3) |
| A5-3 | "Every activity must carry the requirement ID or IDs from A1 that it discharges" | A5 | FAIL | PASS | A5-2 |
| A5-4 | "every date must be computed backwards from the deadline, not typed in." | A5 | PASS | PASS (unchanged) | The gate decide-by dates ignore the cut-off (A5-1) |
| A5-5 | "the marshalling plan ... every physical and documentary item the pack requires, who issues it, how long that takes, … | A5 | PASS | PASS (unchanged) |  |
| A5-6 | "Output the plan as data, CSV or JSON ... the chart is not the deliverable." | A5 | PASS | PASS (unchanged) |  |
| A5-6 | "Output the plan as data, CSV or JSON… the chart is not the deliverable" | R | PASS | PASS (unchanged) |  |
| A5-7 | "does it survive the lead times the documents actually impose" | A5 | FAIL | PASS | The four gated issues get decide-by dates after the 12 Nov cut-off that the pack imposes on raising them (A5-1) |
| A5-8 | owner's audit asks (coverage, backward planning, calendars, fixed vs relative, durations, dependencies, resources, ma… | A5 | FAIL | PASS | Coverage (A5-2), dependency (A5-3), Gantt omits flags and dependencies (A5-6) |
| G-2 | "Use whatever models, tools and assistance you like … log it, and … defend every number" (A4 part only) | A4 | FAIL | PASS (subagent briefs and model-call logs in the repository; cost note corrected, money still not stated) | Logging is incomplete (subagent briefs). Cost/effort figures cannot be defended as stated (A4-6). |
| G-3 | "If your system cannot determine something, say so" | A1 | PASS | PASS (unchanged) |  |
| G-3 | "If your system cannot determine something, say so" | A2 | FAIL | PASS | A2-4. A1 and A3 do show I-CONCESSION, I-F4A-FIELDS and I-PERMIT |
| G-3 | "If your system cannot determine something, say so" | A3 | PASS | PASS | It says so and is honest ("Unknown answers stay unknown"). The reasons are only in the detail (A3-4 FAIL). |
| G-4 | No requirement "with no source and no flag" | A1 | PASS | PASS (unchanged) | A1-4 is an assumption mislabelled as pack-stated (not a register row) |
| G-4 | "Asserting a requirement that is not in the pack ... with no source and no flag" | A2 | PASS | PASS (unchanged) | ADD-01-Q4-01 is over-classified as a new obligation (A2-6), but it is sourced |
| G-5 | Show "the clause and the page … inside a minute" | A1 | PASS | PASS (unchanged) | A1-5 minor |
| G-6 | Surface to a human the questions a person has to own | A1 | PASS (decisions PENDING) | PASS (unchanged) | A1-3: the concession wording says "settled" in one place and "unresolved" in others |
| G-6 | "Letting the tool decide a commercial or legal question that a person has to own … Surfacing those to a human is the … | A3 | PASS | PASS (unchanged) | Nothing is decided by the tool: "exclusion" is not equated with the three categories, the stale Form 4-A date is not corrected, and the E… |
| G-7 | §4: no chat, no departments, no dashboard/logo/product name/roadmap/pricing, no "could be extended to" | R | PASS | PASS (unchanged) | The A3 footer "tenderpack: evidence build…" is the package name in a provenance line, not branding. |
| G-9 | "The bid programme in A5 must be generated by your system from your register, not drawn by hand." | A5 | PASS | PASS (unchanged) |  |
| R-1 | Rendered Excel (A1 xlsx) readable: columns, statuses, Arabic cells, no truncation | R | PASS | PASS (unchanged) | Not checked visually: LibreOffice Calc is not installed. The R-1 stale text is counted under R-4. |
| R-2 | Rendered PDF readable: Arabic, tables, page count | A3 | PASS | PASS (unchanged) | The two image-read units are shown in English on the PDF, labelled "(Arabic only)". Arabic text in the HTML is in correct logical order. … |
| R-2 | Rendered PDF (A5 Gantt) readable | A5 | PASS | PASS (unchanged) |  |
| R-2 | Rendered PDF (A3 one page; A5 Gantt) readable: Arabic rendering, tables, page count | R | PASS | PASS (unchanged) | Minor: R-6 (hyphen breaks) and R-9 (truncated status). |
| R-3 | Same row reads the same in A1 and A3 | A3 | PASS | PASS (unchanged) | 8.6-01 REINSTATED-AMENDED, ADD-02-7.2-01 NEW and 6.1-01 ACTIVE (as amended) carry matching page flags. Both files share the stale "not re… |
| R-3 | Same row/op/date reads the same across A1, A2, A3, A5 | A5 | FAIL | PASS | A5-4; the permit flag is only in the A5 data (A5-6) |
| R-3 | Same row/op/date reads the same in A1, A2, A3, A5 and the review pages | R | FAIL | PASS (R-10 fixed by the coordinator after the recheck) | Translation status (R-1); counts 17 vs 18 and 38 vs 46 (R-4); committed README vs committed A1/A3 (R-2). |
| R-4 | No stale statements | A4 | FAIL | PENDING (the committed `out/` waits on the owner's commit) | out/README is fixed in the session-11 working tree but not regenerated or committed. |
| R-4 | No stale statements (readings "pending" when approved; counts that disagree with the data) | R | FAIL | PENDING (the committed `out/README.md` and the reading YAML headers wait on the owner; the rebuilt outputs are correct) | R-1, R-2, R-8. |

## 6. Decisions that need you

1. **The commit.** Done after the session: you authorised it ("commit", 08:13 UTC, 5 Oct) and everything of session 11 is committed as `6053493` and pushed. The committed `out/README.md` now names the approved readings and the committed outputs carry every fix above (audit R-2).
2. **The history of 2 Oct 2026** (audit A4-1, blocking in the reviewer's rating). Four commits were rewritten at your instruction with their dates kept and force-pushed; the record still calls the history real and two prompts verbatim. Either an erratum is added to the session-03 and session-04 logs and the A4 index (time, the four old → new hashes, what changed and why, without the wording you asked to be removed), or the record stops calling the bundle "the real history" and those prompts "verbatim". I have made neither change.
3. **The reading YAML headers.** `curation/readings/VOL-II-p3-r1.yaml` and `VOL-IV-p6-r1.yaml` still begin "PROPOSED READING — PENDING HUMAN REVIEW. Not approved." (written before your approval). Your approval entries pin each file's sha256, so even a comment change alters a recorded hash; only you should change them (and re-record with `approve`, which shows the differences).
4. **The proposed content changes of the audit fixes**, all still `review: proposed`, each with the source words quoted in the YAML: the concession-term wording (I-CONCESSION, VOL-I-12.1-01 medium confidence, VOL-V-3.1-01/3.2-01/42.2-01); VOL-I-4.2-01 and VOL-I-11.5-01 as pass_fail; ADD-02-5.2-01's pass_fail reasoned; VOL-V-12.1-01's 18.4 cap and the VOL-V:18.4 disposition; VOL-I-8.5-01 in footnote 12's words; VOL-IV-F4C-N1 corroborating VOL-I-9.4-01; ADD-01-Q4-01 and the ADD-01/Q4 op as `interprets` restating VOL-I 5.5; VOL-II-4.2-01's note aligned with I-FLOWS; the two Form 4-C confidence reasons; I-READING-F4C on the detail page only; the A5 templates (Form 4-F after the model audit opinion, Form 4-B after the completion certificates, the consortium check before the clarifications, VOL-I-6.2-02 and VOL-I-8.1-01 carried, VOL-I-4.2-01 and VOL-I-11.5-01 excepted) and the two new provisional assumptions (`submission.delivery_buffer_wd: 0`, `lead_times.consortium_confirmation: 1 WD`). Accept, reject or amend them with `tenderpack accept|reject`; nothing is applied as accepted.
5. **The genuine approval blockers**, unchanged and separate from defects: 205 of 205 rows and 37 of 37 ops proposed; the questions kept for people (the concession term and Form 4-E, the reissued Form 4-A, the Form 4-C "exclusion" category, the dry-weather flow, the chlorine/pH ranges under the "maxima" qualifier, the Environmental Permit, Envelope B contents, contract value in Envelope A, the Bid Bond vs the Financial Close long-stop, the Local Content Certificate issuer and lead time, the bidder facts); the 21 draft clarification questions, not sent (cut-off 12 Nov 2026).
6. **Blind-05's candidate** (synthetic): 23 provisions unresolved and 23 downstream tasks answered only by unpromotable items are listed first in its review packet; nothing of it touches the real curation.
7. **The live routes.** No API key in the container, OpenRouter blocked, no Mac: the Anthropic, OpenRouter and Ollama routes remain unverified live. If you want them tested, a key and a USD cap through secure configuration (never in chat or files), the OpenRouter host in the network policy, and the Mac for Ollama.
8. **The 30-minute target.** Blind-05 took 72 min from the PDF to the candidate outputs on the host route with batches one at a time (your instruction not to rely on concurrency); blind-04's steps took 63 min. The time is model latency (15 sequential host sessions). Options that do not weaken validation: fewer, larger batches where the request fits (the request layer now sizes them), the critic only on consequential items (already selective), or a faster host model for the reading and downstream phases; each is your call, and each is a trade against detection quality that the next sealed rehearsal would measure.

## 7. Verification

final tree, 5 Oct 07:33–07:54 UTC: `ingest` 524 units STRUCTURE OK (04:08); `outputs` exit 0, structural checks ok (C13 17 items; C43 one page at 7.72 pt; C46, C48, C52 ok; C28 report-only findings on both covers); `outputs --strict` exit 3 with exactly the two human-approval blockers (205 of 205 rows and 37 of 37 ops proposed) and no defect blocker; the full suite **776 passed, 0 failed** in 20 min 46 s (the session added 118 tests across 13 new files, each regression written failing first; 4 existing expectations changed with a comment); the real pack's `out/` and `build/` regenerated from the finished code.

What the suite does not cover: the Anthropic, OpenRouter and Ollama routes live (recorded responses only); the xlsx in a spreadsheet application and the HTML in a browser (neither is installed here; checked with openpyxl and as text); the Mac. The draft archive was not rebuilt (it is built from a commit).

## 8. Runnable commands

```
make setup                                   # once, needs network
.venv/bin/python -m tenderpack ingest        # the evidence build
.venv/bin/python -m tenderpack outputs --evidence build --out out            # A1–A5 working draft
.venv/bin/python -m tenderpack outputs --evidence build --out out --strict   # the release check (exit 3 while anything is unapproved)
.venv/bin/python -m tenderpack check-register
.venv/bin/python -m tenderpack ai run ADD-03 --pdf PATH --route host --host-model-alias opus   # an unseen addendum
.venv/bin/python -m tenderpack ai resume RUN_ID [--from STEP]                                   # after an interruption or a code change
.venv/bin/python -m tenderpack ai run-status RUN_ID
.venv/bin/python -m tenderpack relationships discover --to FILE
.venv/bin/python -m pytest -q -p no:cacheprovider                              # the full suite
```
