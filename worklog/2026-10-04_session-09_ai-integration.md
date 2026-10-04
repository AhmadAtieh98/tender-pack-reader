# Session 09: controls tightened, the AI layer around the engine, four routes, blind rehearsal 03

- **Date:** 4 Oct 2026 from 08:42:11 UTC.
- **Who:**
  - **The owner (Ahmad)** gave the instructions (`worklog/2026-10-04_session-09_prompt.md`, verbatim) and switched the session's model before sending them.
  - **The coordinator:** the assistant in the cloud container, running as Fable 5.1 (the owner's switch; the session was configured for Opus 5.5 before it). It read the state, wrote the sequence, briefed the subagents, integrated their work, ran the suite and wrote the records.
  - **The implementation and review subagents:** launched with the `opus` model option; each one reports its model as Opus 5.5 when asked (checked at 08:44 with a one-line probe before any work was briefed).
- **What this environment can and cannot do (checked at 08:42, `get_session`, `env`, `curl`):**
  - no Anthropic or OpenRouter API key is configured (no `ANTHROPIC_API_KEY`, no `OPENROUTER_API_KEY`);
  - `api.anthropic.com` is reachable through the container's proxy; `openrouter.ai` is denied by the environment's network policy; no Ollama runs here and the owner's Mac is not reachable from the cloud;
  - the `claude` CLI is installed; `codex` is not.
  - The owner was asked at 08:50 for a key (set in the environment's API credentials, never in chat), a spending cap in USD, and, for OpenRouter, the host to be allowed. Until then every run uses the recorded or host routes, reported as such.
- **One commit, at the end, on the owner's authorisation.** The owner asked that no commit, push or history rewrite happen until authorised and that the next commit title start with `AI IMPLEMENTATION START`; the stop hook's six requests to commit were refused. The owner authorised the commit at about 12:55 ("if all good please commit"), after the final suite had passed; the session's work is one commit on `claude/hopeful-curie-7oki9q`.
- **Nothing was sent** to the hiring team or anyone else. No clarification question was sent. No row, op, reading or proposal was accepted, approved or rejected by the program or the assistant.

## 1. The exchange

The owner's message asked for five things: (1) six control findings reproduced with regressions and fixed; (2) an AI layer around the existing engine with one typed contract, narrow tools, controller-assigned verification and staging-only writes; (3) the same application usable through four routes (Claude Code and Codex through a CLI/service and MCP interface; OpenRouter; local Ollama), with capability checks, bounded retries, timeouts, concurrency and spending controls, a recorded adapter for offline tests, and secure credentials; (4) unfamiliar addenda as the end-to-end demonstration; (5) tests of malformed responses, fabricated citations, numerical changes, prompt injection, stale evidence, rejected operations, provider failure and budget exhaustion, the suite, a new sealed blind rehearsal, and a compact report with runnable commands per route, measured results, remaining defects and the inputs needed from the owner.

## 2. Timeline

All times UTC, from the session transcript.

| UTC | Step |
|---|---|
| 08:42:11 | Owner's message (model switched to Fable 5.1 just before). |
| 08:42–08:44 | Session facts checked (model, credentials, network); the message preserved verbatim. |
| 08:44 | Subagent model probe: `opus` → Opus 5.5. |
| 08:44–08:50 | Evidence for the six findings located in the code and the blind-02 outputs (§3). |
| 08:50 | Sequence and the two open inputs (credentials, spend cap, OpenRouter host) sent to the owner. |
| 08:51 | Five subagents briefed and launched: W1 (PDD time flow, Gantt Unicode), W2 (clarify checks, decision bindings, diff), W3 (C28, removed obligations, index rows in prose, consequence classes), W4 (AI contract, tools, controller, providers, MCP, CLI, adversarial tests), W5 (independent author of the sealed blind-03 addendum). |
| 08:55–08:57 | The coordinator wrote this record's skeleton and `rehearsals/blind-03/setup_pack.py` (nothing a subagent owns). |
| 09:21 | **W5 (blind-03 author) finished**: 4 pages, "Issued 1 November 2026", about 25 minutes. The coordinator computed the hashes itself (equal to the author's) and wrote `rehearsals/blind-03/FROZEN.md` at 09:22:15, before anyone opened the addendum. The key stays sealed outside the repository. |
| 09:23 | **W2 finished**: `clarify.check` strict states and the effective cut-off; decision bindings carry each unit's source identity (document sha256), location (pages, anchor boxes, spans) and reading evidence; `diff` compares every unit a row cites. 32 new tests; 117 passed across its seven files. |
| 09:30 | **W1 finished**: `register.anchor_details`, placeholders for the PDD time/timezone/date/source and `{ROW:<id>:<parameter>}` in activity names and milestone labels, `delivery_cutoff_time` refused as an assumption, Gantt Unicode (SVG/HTML) and an `insert_htmlbox` path with /ActualText for the PDF. 14 new tests (13 failed before the fix); the real pack's A5 is byte-identical. |
| 09:31–09:40 | The coordinator: fixed milestones take their time from the rule's own quoted words (the Pre-Bid Conference label no longer types 10:00; test added); the `delivery` assumption's basis no longer types the time; the delivery address comes from the Appendix 3 row's own words (`{ROW:VOL-I-App3-01:address}`; the row re-pinned); blind-01 got its own clarification register copy with the cut-off its ADD-03 produces (19 Nov 2026, computed by the build), labelled as a later fix. A YAML slip in that copy was caught by `check-register` and redone through the YAML structure. |
| 09:51 | **W4 finished**: `tenderpack/ai/` (contract, config, run log, budget, tools, controller, CLI, providers: recorded, anthropic, openrouter, ollama, host), `tenderpack/mcp_server.py`, `config/ai.yaml`, `docs/AI_ROUTES.md`, 34 offline tests with six cassettes. No live call was made (no key); the OpenRouter listing is blocked here; Ollama is unreachable from the cloud. |
| 09:52–10:00 | The coordinator re-ran W4's tests (34 passed), checked the Anthropic adapter against the API reference (request shape, Models endpoint fields, retries: consistent; no forced tool choice; no silent fallback), and entered the first-party list prices for the two configured models into `config/ai.yaml` so a USD cap can be enforced (marked as list prices to confirm). |
| 10:03 | **W3 finished**: C28 "unchanged" claims, validity matching through the date rules, "re-letters" and deletions as verbs; `removed` interpretations and the REMOVED status; the `insert_row` op; `document_refusal` and `criterion_zero` classes with their A3 sections and a third condensation level. 32 new tests (30 failed before the fix). |
| 10:04–10:08 | The coordinator: `live.py` uses the one in-force rule and labels `insert_row`; the blind-02 delivery address from the Appendix 3 row's words; re-pins; the operating guide's C28 caveat and the blind-02 comparison's follow-up list updated. 107 session-09 tests run together: 106 pass; the one failure was W2's blind-01 test expecting the old, wrong cut-off to be reported (rewritten for the corrected register). |
| 10:08–10:13 | Real pack, blind-02 and blind-01 rebuilt into scratch and compared: the real pack differs from `out/` only as intended (A3 subtitle timezone; the A1 assumptions row removed; the delivery activity's full address and reworded basis; review fingerprints); blind-01's 29 STALE rows are its committed, historical state. The three committed output folders regenerated in place. The recorded demonstration run written to `staging/ai/ADD-03-recorded-20261004T101121Z-1df6/`. Full suite started. |
| 10:11–10:13 | **Blind-03 opened**: set-up, ingest (573 units, C10 pass), draft (6 pattern ops, 29 provisions left), drafted outputs published (ADD-03 PARTIAL). |
| 10:16 | **Proposer P launched**: an Opus 5.5 subagent as the coding host's model, host route through the CLI tools only, blind to the key. |
| 10:19–10:22 | The coordinator: the recorded run's log checked (expected events, no secret-like strings); the MCP server hand-driven over stdio (initialize → tools/list → get_unit). |
| 10:30 | **P finished** (13 min): run `ADD-03-host-20261004T102718Z-97c1`, status complete, 35/35 provisions accounted for; 16 evidence_verified, 5 interpretation_pending, 5 conflicting, 1 insufficient_evidence, 13 escalated. It reported tool gaps (§4.7). |
| 10:31–10:35 | **Live fixes before the curation** (logged in blind-03's clock; the host-route run is kept as made): a form an addendum inserted is citable (`ADD-02:F4-G`); Arabic words matched without diacritics or alef-form differences for `replace_text` on image readings; a notified non-working day as an `annotate` op (`effect: non_working_day`, `date`) that the date rules and the programme count from that stage; a whole cell value is evidence however short; an amendment to an owner-approved reading is recorded, not a conflict (ADD-02 5.1 is one). Six regressions; W4's approval test rewritten to the policy. |
| 10:36 | **Curator C launched** for blind-03: the AI proposals as input, the normal path to curated outputs, blind to the key. |
| 10:40–10:51 | The real pack rebuilt into scratch with the live fixes and compared with `out/`: every deliverable byte-identical; only `stages.json` differs, where ADD-02/7.1 (the op that adds Form 4-G to the VOL-I 9.1 list) now also cites `ADD-02:F4-G` (live fix 1; the op stays valid, no check changes). The same for blind-02 (ADD-02/7.1 and its ADD-03 op 22). `out/` regenerated in place; the rehearsal folders after their rebuilds. |
| 10:45 | The full suite started at 10:11 (before the live fixes) finished: 503 passed, 1 failed (34 min 30 s). The failure was W1's `test_real_pack_reads_exactly_as_before`, written before the delivery address was taken from the Appendix 3 row's words (09:35); its expected string now carries the row's full address. Re-run of the file: 10 passed. |
| 10:53–10:55 | `rehearsals/blind-02/out-after-fixes/` and `rehearsals/blind-01/out-after-fixes/` regenerated in place (the same `cited` difference only); each byte-identical to its scratch rebuild afterwards. A second full suite started at 10:55 (the curator still running in its own folders). |
| 11:02 | **Curator C finished** (26 min from 10:36): 27 ops and 4 dispositions (0 unresolved), 12 new rows, 32 re-made readings, 7 issues, 4 evidence items, 7 new activities, the clarification cut-off recomputed (11 Nov) and 2 draft questions; `outputs` exit 0 with ADD-03 APPLIED, STALE none, `check-register` 0 findings; the diff written. It reported that `pin --rows` crashed (worked around from a scratch script; `pins.yaml` checked) and that the Form 4-C substitution could not be one `replace_text` (§4.5). Nothing accepted, sent or unsealed. |
| 11:04 | **Live fix 6** (pre-key): `pin --rows` built the register without a calendar after live fix 3; it now builds the pack's own; regression added (6 pass). |
| 11:05 | **Unsealed.** The four sealed files copied to `rehearsals/blind-03/SEALED/`; `sha256sum -c` passed for the three files, the PDF line passed from the root, and the hash of `SHA256SUMS` equals `FROZEN.md`'s. |
| 11:05–11:17 | **Scored** against the key: 34 items, 31 hits, 3 partial, 0 missed; every date; all 17 traps avoided; the deliberate ambiguity escalated with both sources (`rehearsals/blind-03/COMPARISON.md`, `README.md`). |
| 11:08–11:18 | **Post-key fixes** (not scored; each general; `tests/test_session09_blind03_postkey_fixes.py`, 6 failed before and pass after): C28 judges a "does not affect any deadline" claim by the computed date changes (the planted E1, which C28 had missed and the curator had found by hand); an insert + delete at one anchor is a substitution (the three C28 artefacts gone); a heading names a form whatever its case. `out-after-fixes/` rebuilt: C28 on ADD-03 reads contradicted 1 (E1), omitted 6, understated 3. |
| 11:25–11:35 | The real pack and the three rehearsals rebuilt and compared: only `cited` lists differed, a form named in both a body and its heading now listed twice; `citations.resolve` deduplicates. The 10:55 suite finished at 11:30: 507 passed, 2 failed, both `AttributeError: 'NoneType' … with_days` from `Register(…, None)` (one through the old `pin --rows`, one a session-06 test that builds the register without a calendar): `Register` now defaults to `Calendar()`; the two tests and the live-fix file pass. `blind-01/out-after-fixes` regenerated (its older `cited` duplicates gone); `blind-03/out-after-fixes` regenerated. |
| 11:36–12:19 | `outputs --strict`: exit 3, the 205 rows and 37 ops only. `make verify`: exit 0, the two clean rebuilds identical. The run logs, staging logs and cassettes scanned for key-like strings: none. The records written: `rehearsals/blind-03/COMPARISON.md` and `README.md`, this log §4–§7, PLAN §15 and revision 9, `docs/session-09_report.md`, the cost file, the operating guide, the routes document; model identifier strings removed from prose (kept only as configuration values in commands and tests). |
| 12:19–12:57 | **Final full suite: 516 passed, 0 failed** (38 min 15 s). |
| 12:5x | The owner asked whether the run was stuck and authorised the commit "if all good". Committed and pushed with the title the owner asked for (`AI IMPLEMENTATION START …`), with `staging/` and `worklog/model_calls/` included as the session's record (the owner can remove them from history only by rewriting it, which was not asked). |

## 3. The six findings: evidence before any fix

| # | Finding | Evidence (before the fix) |
|---|---|---|
| 1 | A5 says 14:00 after ADD-03 moved the time to 11:00 | `rehearsals/blind-02/out-after-fixes/a5/milestones.csv` row PDD: time `14:00`, short `PDD 14:00`; `a5/README.md` "**2026-11-26 14:00** Proposal Due Date, 14:00 Riyadh time (VOL-I 6.1 as amended by ADD-01 2.1 …)"; A3 subtitle "Proposal Due Date 2026-11-26 14:00". Causes: typed `_milestones.labels.PDD` (`curation/activity_templates.yaml:36`), `planning.delivery_cutoff_time: "14:00"` (`config/assumptions.yaml:10`, read by `schedule.milestones` and `programme.py:605`), typed activity names (`deliver`, `seal-and-mark`), and `stage2.py:872` `f"… Proposal Due Date {pdd} 14:00"`. A1 is right because it reads the effective text. **Confirmed.** |
| 2 | `clarify.check()` too lenient | `clarify.py`: `REQUIRED` lacks `decision_owner` and does not require a non-empty `sources`; `response_status` is only tested for the word "sent"; `cut_off.date` is never compared with the computed cut-off. **Confirmed.** |
| 3 | Decision bindings ignore the source's identity and location | `amend.unit_pin` hashes status/text/cells, annotations and the image-reading subject only; `Engine.subject` pins "before" with it; `review.row_binding` adds anchors for the row's own units but not for an op's members, and neither carries the document's sha256. Moving `VOL-I:T1-1/B`'s box with the same text leaves the ADD-02/3.1 subject unchanged. **Confirmed.** |
| 4 | Blind-02 follow-ups | `COMPARISON.md`: `diff` misses rows whose secondary units changed; `VOL-I-10.3-02` shows AMENDED after its words were deleted and A5 still plans the auditor; C28 missed "The Proposal Due Date is unchanged" (not a claim) and inverted the validity match (6.3 vs 7.1), and merged a compound claim; the Index of Forms entry could only be annotated. **Confirmed.** |
| 5 | Consequence classes conflated | `register.CONSEQUENCE_CLASSES` has no class for a refused document ("will not be accepted") or a criterion-level zero; the curator used `lesser` and `score_elimination`, which took rows off the gate and mislabelled a scored risk. **Confirmed.** |
| 6 | Gantt non-ASCII | `gantt.py:50` `_t()` maps every character outside 32–126 to "?" (SVG, HTML and PDF). **Confirmed.** A PyMuPDF Story probe here rendered Arabic with the bundled "Noto Naskh Arabic" fallback (checked at 08:49), so a PDF path exists. |

## 4. What changed

Every change is in the working tree, uncommitted. Nothing in `curation/approvals.yaml`, `curation/readings/`, `curation/reading-snapshots/` or any decision file was touched.

### 4.1 Controls (the six findings of §3)

| # | Fix | Where | Regression (failed before the fix) |
|---|---|---|---|
| 1 | The PDD's date, time, timezone and effective source flow from the register (`register.anchor_details`: date, time, tz, unit, as-amended-by, source) into the programme, the milestones, the marshalling labels and the A3 subtitle. Activity names, milestone labels and bases take placeholders (`{PDD_TIME}`, `{PDD_TZ}`, `{PDD_DATE}`, `{PDD_SOURCE}`, `{ROW:<row>:<parameter>}`, `{time}/{tz}/{date}/{source}`) that `schedule.fill` resolves; a typed time in a label is a C45 problem; `delivery_cutoff_time` is refused as an assumption; a fixed milestone's time comes from the rule's own words (`schedule.stated_time`). The delivery address comes from the Appendix 3 row's words (`{ROW:VOL-I-App3-01:address}`). | `tenderpack/register.py`, `schedule.py`, `programme.py`, `stage2.py`, `curation/activity_templates.yaml` (+ the rehearsal copies), `config/assumptions.yaml` (+ copies), the Appendix 3 rows | `tests/test_session09_pdd_flow.py` (blind-02's A5 now reads 11:00 from ADD-03 2.1; the real pack 14:00 from VOL-I 6.1 as amended by ADD-01 2.1; a typed time fails C45) |
| 2 | `clarify.check`: `decision_owner` and a non-empty `sources` required; three response states only (`draft, not sent`, `withdrawn (not sent)`, `answered by addendum` with verbatim `answer` evidence on an addendum unit and page); the `cut_off` date and the time in its note compared with `clarify.effective_cutoff(r)` (the in-force VOL-I 5.2 rule, computed by the register); `check-register` and the release gate pass the effective cut-off. | `tenderpack/clarify.py`, `stage2.py` | `tests/test_session09_clarify.py` |
| 3 | Decision bindings carry source identity: `amend.unit_pin(state, uid, evidence)` hashes the document's sha256, the pages, the anchor boxes and spans and the reading evidence of every unit; `Engine.subject` (an op's "before") and `review.row_binding` use it. Moving `VOL-I:T1-1/B`'s box with the same text now changes the ADD-02/3.1 subject (fixture `row_shift_pt`, built through the normal evidence-build validation). Interpretation pins stay content-only by design: a moved box does not void a reading of the words. | `tenderpack/amend.py`, `review.py`, `tests/fixtures/make_fixture.py` | `tests/test_session09_binding.py` |
| 4 | Blind-02 follow-ups: `diff` compares every unit a row cites (`live.py`); an interpretation with `removed: true` is REMOVED (out of force; A1 status `REMOVED (op)`, A3 and A5 drop it); the `insert_row` op (index tables, `after_row`, each cell checked against the provision; C47); C28 tests "X is unchanged" sentences against the ops on X, matches validity claims through the register's date rules (6.3 bond vs 7.1 proposal), splits compound claims, and reads "re-letters/re-numbers/re-issues" and deletions as verbs. | `tenderpack/live.py`, `register.py`, `amend.py`, `citations.py`, `draft.py`, `summary.py`, `trace.py`, `render.py`, `batches.py`, `stage2.py` | `tests/test_session09_diff.py`, `_removed.py`, `_insert_row.py`, `_summary.py` |
| 5 | Two consequence classes: `document_refusal` (a stated refusal of a submitted document; the row keeps its place in the VOL-I 11.1(i) gate and A3 lists it under "Document refused", never as a disqualification) and `criterion_zero` (zero marks under one criterion; listed apart from the VOL-I 11.3 threshold). A third A3 condensation level. The operating guide says how to choose. Blind-02's two rows re-classed and marked as a post-key fix. | `tenderpack/register.py`, `stage2.py`, `render.py`, `docs/OPERATING_GUIDE.md`, `rehearsals/blind-02/work/register/rows/*.yaml` | `tests/test_session09_consequences.py` |
| 6 | `gantt.py` keeps Unicode in the SVG and HTML; the PDF draws non-ASCII labels with `insert_htmlbox` (/ActualText, Noto Naskh Arabic fallback), checked visually on an Arabic label rendered here. | `tenderpack/gantt.py` | `tests/test_session09_gantt_unicode.py` |

### 4.2 The AI layer (`tenderpack/ai/`)

- **Contract** (`contract.py`): `StateIdentity` (pack, evidence build hash, validated and working stage, decisions hash), `EvidenceRef` (doc, unit, page, kind: span/cell/crop/unit, exact words, cell, bbox), `Statement` (fact / assumption / interpretation, kept apart), `ChangeProposal` (type: amendment_op / disposition / row_reading / clarification_item / escalation; provision; target; previous and proposed values; dependencies; declared conflicts; missing information; `validation` and `verification_status` written by the controller only), `ProposalSet` (status complete / partial / malformed / provider_failed / budget_exhausted / stale). `CONTROLLER_VERSION = "s09-ai-1"`.
- **Tools** (`tools.py`): `search_evidence`, `get_unit`, `get_group`, `get_crop`, `compare_state`, `calculate` (the register's calendar, per stage, with notified days), `simulate_amendment`, `simulate_programme`, `validate_proposal`, `get_state`, `get_task_packet`, `request_review`, `submit_proposals`. All read-only except the last two, which write to `staging/ai/` only.
- **Controller** (`controller.py`): checks every reference (verbatim words in the named unit at the state before the addendum, on the stated page; a whole cell value is evidence however short; a bare short span is not), the state identity, the engine dry run (C21–C27, C47), dependencies, declared conflicts, missing information, rejections and accepted decisions, and records an amendment to an approved reading; assigns the status (`invalid` > `conflicting` > `escalated` > `insufficient_evidence` > `interpretation_pending` > `evidence_verified`); overwrites any model-supplied status and logs the overwrite; computes the impact (dry run: addendum status, units and rows changed, STALE rows, voided decisions, C46, clarification entries, A3 enters/leaves, programme changes); writes `proposals.yaml`, `review_request.md` and `log.jsonl`; `promote RUN_ID --by` copies verified items into curation as PROPOSED drafts, never overwriting.
- **Budget** (`budget.py`): caps (calls, input and output tokens, USD, time, turns, concurrency), the spend meter `staging/ai/spend.jsonl`, the per-addendum lock `staging/ai/.lock-<ADD>` (stale reported, broken only by a named person, logged).
- **Run log** (`runlog.py`): every prompt, tool call, raw response, usage, error, overwrite and validation, with keys redacted before writing; `worklog/model_calls/<run_id>.jsonl`.
- **Providers** (`providers/`): `recorded` (cassettes; offline; not a live integration), `anthropic` (Messages API over `urllib`; capabilities from `GET /v1/models/{id}`; retries on 408/409/429/5xx/529 with `retry-after`; no fallback), `openrouter` (capabilities from the model listing; refused when unreachable), `ollama` (`/api/show` capabilities; `num_ctx` bound; the context bound stops the run before it is outgrown), `host` (no application call; the host's model declared, not verified).
- **MCP server** (`tenderpack/mcp_server.py`): JSON-RPC 2.0 over stdio, 13 tools, the same functions.
- **CLI** (`tenderpack ai …`): `propose`, `validate`, `submit`, `task`, `tool`, `serve-mcp`, `capabilities`, `promote`, `locks`.
- **Configuration** (`config/ai.yaml`): routes, model ids as values, caps, list prices (to confirm), lock staleness. No credential anywhere but the environment.
- **Tests:** `tests/test_session09_ai_{contract,tools,propose,mcp}.py` with six cassettes: malformed output, fabricated citations, wrong numbers, prompt injection, stale evidence, rejected ops, provider failure, budget exhaustion, missing capabilities, the lock, the MCP handshake over a subprocess.

### 4.3 Live fixes during blind rehearsal 03 (before the curation; each with a regression in `tests/test_session09_blind03_live_fixes.py`)

1. A form an addendum inserted is citable: "Form 4-G" resolves to `ADD-02:F4-G` (and to `ADD-03:F4-G` once the reissue exists); a Volume IV form stays itself (`citations.resolve`).
2. Arabic words are matched without diacritics or alef-form differences for `replace_text` on image readings (`amend._contains`, `_quoted_in`, `_replace_once`, `_arabic_span`, over `normalize_arabic`).
3. A notified non-working day is an op: `annotate` with `effect: non_working_day` and `date`; C21 requires the provision to print that date; `StageResult.non_working_days`; the register keeps a calendar per stage (`Register.cal_by_stage`, `Calendar.with_days`), the date rules and the programme count it from that stage, and the planning basis names it ("notified by an addendum under VOL-I 2.4").
4. A whole cell value is evidence however short (the controller's short-quote rule applies to spans, not cells).
5. An amendment to an owner-approved reading is recorded (`approvals` record, ok), not a conflict: the approval covers the transcription of the issued page, not the words of a later addendum.
6. `pin --rows` built the register without a calendar and crashed after fix 3 (found by the curator); `cli.pin_cmd` now builds the pack's own calendar, and `Register` defaults to `Calendar()` for a caller that needs no dates (two session-06 tests built it that way).

**After the key (11:08–11:18; not scored; `tests/test_session09_blind03_postkey_fixes.py`):**

1. C28 "no date affected" claims (`summary.no_date_effect_claims`, `_check_no_date_effect`, `date_changes_by_stage`): a cover sentence "<X> does not affect any deadline | the Proposal Due Date | …" is judged by the register's computed dates, contradicted when a date rule in force at both stages has a different planning date; a scope naming one anchor or rule is judged by that one. `stage2` feeds the changes from `Register.all()`.
2. An `insert_unit` whose anchor a `set_status deleted` removes at the same stage is a substitution for C28 (class "replace").
3. `citations()` reads "Form N-X" whatever its case (a heading prints "FORM 4-C"), and `resolve` lists a target named twice once.

### 4.4 Status documents reconciled (history kept)

- `docs/OPERATING_GUIDE.md`: the C28 caveat, the consequence-class guidance, §6 "The AI layer".
- `docs/PLAN.md`: the status line, §4.6 (model use and routes: designed there, implemented in §15), §14's follow-ups marked as done in session 09, §15 added.
- `README.md`: the tested bullet (three rehearsals, the blind-03 score) and the AI-layer bullet.
- `docs/AI_ROUTES.md`: what is recorded, mocked, live or local, as observed on 4 Oct 2026 (the host route run once for real on blind-03; the approved-reading policy of §10).
- `docs/COST_AND_EFFORT.md`: the session 09 row, the seven subagents with their reported tokens, the sizes, the model-call line.
- `docs/OPERATING_GUIDE.md` §3: the blind-03 time (50 minutes with the AI layer; the estimated review time).
- `scripts/make_draft_archive.py`, `scripts/verify_archive.py`: blind-03 carried and rebuilt like the other two.
- `docs/session-09_report.md`: the compact implementation report (before/after, the workflow, measured results per route, runnable commands, remaining defects, inputs needed).
- `rehearsals/blind-02/COMPARISON.md`: the follow-ups note (done, with the test files) and a look-back date corrected.
- Session 08's log and report are unchanged.

### 4.5 Blind rehearsal 03

Full record: `rehearsals/blind-03/COMPARISON.md` (timeline, results item by item, the AI layer's measured contribution, the human review time, what the engine could not express, the live and post-key fixes, the follow-ups) and `README.md`.

- **Path:** set-up and ingest (573 units, 10:11) → draft (6 ops, 29 provisions left) → drafted outputs (PARTIAL) → the proposer on the host route (12:39; 35 of 35 provisions accounted for; `staging/ai/ADD-03-host-20261004T102718Z-97c1/`) → five live fixes → the curator (26 min; every AI item used, corrected or rejected against the evidence, `ai-proposals-used.md`; 27 ops, 12 rows, 32 readings, 7 issues, 7 activities, 2 draft questions) → `pin`, `check-register` (0), `outputs` (APPLIED, STALE none), `diff` → live fix 6 → unseal (11:05).
- **Score (pre-key outputs only):** 34 provisions, answers, cover errors, secondary effects and A3 changes: 31 hits, 3 partial (the Schedule 11 gap under 6.2; the membership knock-ons 8.2/8.4 and the new member's own Form 4-C; the TP knock-ons in the reliability run and VOL-V 31.1(b)), 0 missed. Every derived date right (the 3.3 notice by the stated alternative). All 17 traps avoided. The deliberate ambiguity (3.2 vs Q17) escalated with both sources and planned to the earlier date, labelled. The planted cover errors: E2 found by C28; E1 found by the curator but not by C28 (post-key fix 1). Marshalling M8 partial: no activity depends on the VOL-V 29.3 row. Not raised: Schedule 11 (U5), the single-entity case (U6), whether the amended definition governs Volume V's own periods (A3 of the key).
- **The AI layer's contribution:** the proposer's 16 evidence-verified items were used as proposed (14 identical to the final ops); 5 interpretation-pending used; 5 conflicting corrected (two declared conflicts were not conflicts; one was the old approval policy; one date ignored the closure; the Q17 conflict real and kept open); 13 escalations resolved by the curator, 10 of them tool gaps fixed live. A person still decided every item and wrote the rows, readings, issues, activities and clarification entries. Estimated human review time for what the rehearsal produced: about 2–2½ hours for one reviewer (untested).
- **Receipt to scored output:** 50 min 31 s, of which the proposal run 12:39 and the live-fix pause 8:43; the curation 25:52 (blind-02: 32 min with a 10-minute interruption, no AI layer).

### 4.6 Tool friction reported by the proposer (host route, blind-03)

The proposer subagent reported these after its run; none stopped it, and each is a candidate improvement, not a defect in the outputs:

1. `validate_proposal` expects `{"proposal": {...}}`; a bare proposal object is refused with a schema message.
2. `calculate` takes a fixed list of purposes and units; a period phrased differently must be restated in the list's terms.
3. `simulate_amendment` counts escalations as unaccounted provisions until the set is submitted (the submit path counts them).
4. `get_unit` on a group id fails; `get_group` must be used for a table or form.
5. A declared conflict outranks `escalated`, so an escalation that also declares a conflict shows `conflicting`.

Fixed before the curation (§4.3): the form target an earlier addendum added (item 7.1 of the run was escalated for "a target the engine accepts for a form added by an earlier addendum"), and the notified-closure calendar entry (item 2.2 was escalated for "the calendar entry for the notified closure in the pack's assumptions").

## 5. Errors and corrections (numbering continues from the session 08 log)

| # | What went wrong | Correction |
|---|---|---|
| E113 | W1 typed the Pre-Bid Conference time (10:00) into a milestone label and the delivery address into an activity name, the same class of defect as finding 1. | `schedule.stated_time` takes a fixed milestone's time from the rule's own quoted words; `{ROW:<row>:<parameter>}` takes the address from the Appendix 3 row; a typed time is a C45 problem (test added). |
| E114 | The blind-01 clarification register copy was made by text replacement and came out as invalid YAML (`linked_issues: []` form). | Caught by `check-register`; redone through the YAML structure (`safe_load` / `safe_dump`). |
| E115 | `tenderpack draft` was called with `--pack` (not a flag of that command). | Re-run as `draft ADD-03 --evidence … --to …`. |
| E116 | A multi-hunk edit script asserted on the `amend.py` docstring line (two spaces, not one) and stopped before its last hunks. | The remaining hunks applied in a second script; the docstring applied separately; the file re-read. |
| E117 | W2's blind-01 test expected the real register's wrong cut-off to be reported against blind-01; after the pack got its own register copy that expectation was wrong. | Rewritten: the pack's copy is clean, and the real register's 12 November is reported when checked against blind-01. |
| E118 | W4's approvals test expected `conflicting` for an amendment to an approved reading. | Rewritten to the policy adopted in the live fixes (recorded, not a conflict; `AI_ROUTES.md` §10 says so and why). |
| E119 | The coordinator's live-fix test called `ws.r()`; `Workspace.r` is a property. | `ws.r`. |
| E120 | W1's `test_real_pack_reads_exactly_as_before` carried the delivery name with the typed short address; it failed in the full suite after E113's correction. | The expected string now carries the Appendix 3 row's full address, with a comment saying where it comes from. |
| E121 | Two timeline rows were written with guessed times (10:31–10:48, 10:49) instead of the clock's (10:35, 10:36). | Corrected from `rehearsals/blind-03/clock.txt`. |
| E122 | `scripts/compare_outputs.py` was run on two output folders; it compares an archive's outputs and reported "0 files". | `diff -rq` on the folders, then the JSON difference walked field by field. |
| E123 | Live fix 3 changed `Register`'s construction (a calendar per stage) and `cli.pin_cmd` still passed `None`: `pin --rows` crashed for the curator (10:56). | `pin_cmd` builds the pack's calendar (live fix 6, pre-key, with a regression); the curator's workaround was checked (`pins.yaml` diff = the three re-pins). |
| E124 | The same crash in two session-06 tests that build `Register(…, None)` (the 10:55 suite: 2 failures). | `Register` defaults to `Calendar()` when no calendar is given. |
| E125 | After the case-insensitive form pattern, an op's `cited` list named a form twice (body and heading). | `citations.resolve` deduplicates, order kept; the real pack's `stages.json` then matches the committed one. |
| E126 | The clock line for live fix 6 said the test file had 7 tests; it has 6. | Corrected before the unsealing. |
| — | The stop hook asked five times to commit and push. | Refused each time: the owner asked that nothing be committed until authorised. |

## 6. Verification (actual results)

| Check | Result |
|---|---|
| Regressions before fixes | Finding 1: 13 of W1's 14 tests failed before its fix; finding 2: W2's clarify tests failed on the lenient `check`; finding 3: the moved-box fixture left the ADD-02/3.1 subject unchanged before the binding fix; finding 4–5: 30 of W3's 32 tests failed before; finding 6: the Gantt test failed on "?"; the six blind-03 live fixes and the three post-key fixes each had a test that failed before (the post-key file: 6 failed, then 6 pass). |
| AI layer tests | `tests/test_session09_ai_{contract,tools,propose,mcp}.py`: malformed output, fabricated citations, wrong numbers, prompt injection, stale evidence, rejected ops, provider failure, budget exhaustion, missing capabilities, the lock, the MCP handshake over a subprocess: all pass (34 at 09:52; the approvals test rewritten at 10:35 to the recorded-not-conflict policy). |
| Full suite, run 1 | 10:11–10:45 (before the live fixes): 503 passed, 1 failed (a stale expectation, E120; corrected). |
| Full suite, run 2 | 10:55–11:30 (before the post-key fixes): 507 passed, 2 failed (`Register` without a calendar, E123/E124; corrected; the two tests pass). |
| Full suite, final | 12:19–12:57, every fix in place (the post-key fixes, the dedupe, the `Register` default): **516 passed, 0 failed** (38 min 15 s). Session 08 ended at 390. |
| Fresh build of the real pack | Rebuilt into scratch after every fix and compared with `out/` (10:40, 11:25, 11:34): byte-identical. `out/` itself was regenerated in place at 10:13 (the intended session-09 changes: A3 subtitle timezone, the assumptions row, the delivery name and basis, review fingerprints) and at 10:51 (`stages.json`: ADD-02/7.1 also cites `ADD-02:F4-G`). A1–A5 are unchanged since 10:13. |
| Strict mode | `outputs --strict` into scratch (11:36): exit 3, release refused; the only blockers are the 205 rows and 37 ops without a named decision, as in session 08. No reading, STALE, coverage or clarification blocker. |
| `make verify` | 11:37–12:19: exit 0; the two clean rebuilds (Stage 1 and the outputs) are byte-identical to each other ("stage 2 outputs identical"). |
| Rehearsal folders | `blind-01/out-after-fixes` and `blind-02/out-after-fixes` regenerated in place (`cited` lists only) and byte-identical to their scratch rebuilds; `blind-03/out-curated` is the scored build (11:01:55, untouched); `blind-03/out-after-fixes` rebuilt with the post-key fixes (11:36) and byte-identical to its scratch rebuild. |
| Blind-03 key | Four hashes checked against `FROZEN.md` at 11:05, after the scored outputs and the diff. |
| Run logs | `worklog/model_calls/*.jsonl`, `staging/ai/*/log.jsonl` and the cassettes scanned for key-like strings (`sk-ant-`, `sk-or-`, `Bearer …`, `x-api-key`): none (12:19). |
| Offline archive | Not rebuilt this session: the session 08 archive (`LAMAR-PPP-R2-DRAFT_eb32b13`) stands; `scripts/make_draft_archive.py` and `verify_archive.py` were extended to carry and rebuild blind-03, and will be run when the owner authorises the commit (the archive is built from a commit). |
| Environment | Linux x86_64 only (Python 3.11.15, PyMuPDF 1.28.2). The Mac, native Excel and PDF viewers, a live API, OpenRouter and Ollama were not exercised. |

## 7. What this session establishes, and what it does not

**Establishes.**

- The six control findings were real, are reproduced by tests that failed first, and are fixed in general code; the real pack's A1–A5 change only where the fixes intend (the A3 subtitle's timezone, the delivery name from the Appendix 3 row, the removed typed-time assumption).
- The AI layer works end to end offline and on the host route: a model proposes through narrow tools; the deterministic controller verifies every quotation, state and dry run, assigns every status, overwrites the model's, simulates the impact and writes to staging only; a person decides. On an unseen addendum it accounted for 35 of 35 provisions, and the curated outputs scored 31 hits, 3 partial, 0 missed with every date right and every trap avoided.
- The adversarial cases (malformed output, fabricated citations, wrong numbers, prompt injection, stale evidence, rejected ops, provider failure, budget exhaustion, missing capabilities, the lock) are handled and tested with recorded cassettes.
- The four routes exist as code with the same contract and validation; their credentials live in the environment only and are redacted from every log.

**Does not establish.**

- Anything about live model behaviour, quality or cost on the Anthropic, OpenRouter or Ollama routes: no live call was made (no key; a blocked host; no Mac). The cassettes are hand-written, and the host route's model is declared, not verified.
- The Mac's performance with the Ollama candidates, or the per-bid cost of PLAN §1.3.
- How blind the rehearsal was: the proposer and the curator were subagents of the session that wrote the tool, and the author of the addendum was another; none saw the key, but they share the tool's vocabulary.
- The human review time (estimated, untested) and any decision: every row, op, reading and proposal is still PROPOSED; nothing was sent.
