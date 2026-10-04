# Session 09: implementation report (AI integration)

For the owner. The full record is `worklog/2026-10-04_session-09_ai-integration.md`; your message is kept verbatim in `worklog/2026-10-04_session-09_prompt.md`. **Nothing is committed** (you asked for that; the next commit title starts with `AI IMPLEMENTATION START` when you authorise it). **Nothing was sent to anyone, no clarification question was sent, and no row, op, reading or proposal was accepted, approved or rejected** by the program or the assistant.

**What ran.** The coordinator ran as Fable 5.1 (your switch). The implementation, review, authoring, proposing and curating subagents ran as Opus 5.5 (probed). No application API call was made: there is no key in this environment. Every live-looking result below is **recorded** (hand-written cassettes) or **host** (the coding assistant's own model through the tools); nothing is live or local.

## 1. Before and after

| Area | Before (session 08) | After (session 09) |
|---|---|---|
| PDD time in A5 | 14:00 typed in labels, names, an assumption and the A3 subtitle; blind-02's A5 said 14:00 after ADD-03 moved it to 11:00 | Date, time, timezone and effective source flow from the register into the programme, the milestones, the marshalling labels and A3; a typed time is a C45 problem; the delivery address comes from the Appendix 3 row's words |
| `clarify.check` | No owner required, empty sources accepted, "answered" accepted without evidence, cut-off never checked | Owner and sources required; three states only, "answered by addendum" needs a verbatim answer on an addendum page; the cut-off date and the time in its note are checked against the computed VOL-I 5.2 cut-off, in `check-register` and the gate |
| Decision bindings | Content only: a moved `VOL-I:T1-1/B` box left the ADD-02/3.1 decision valid | Every binding carries the document sha256, pages, anchor boxes, spans and reading evidence (readings' pins stay content-only, by design) |
| `diff` | Missed rows whose secondary units changed | Compares every unit a row cites |
| Deleted obligations | Shown AMENDED and still planned | REMOVED (out of force): off A1's active rows, A3 and A5 |
| Index entries in prose | Annotated only | `insert_row` op, every cell checked against the provision (C47) |
| C28 | Missed "X is unchanged", inverted the validity match, merged compound claims | Tests "unchanged" claims against the ops, matches validity through the date rules, splits claims, reads re-letter/re-number/re-issue and deletions |
| Consequence classes | Refusals and criterion zeros forced into `lesser` / `score_elimination` | `document_refusal` (stays in the VOL-I 11.1(i) gate; "Document refused" on A3) and `criterion_zero` (apart from the threshold); never a disqualification |
| Gantt | Non-ASCII became "?" | Unicode kept (SVG/HTML); the PDF draws it with /ActualText and an Arabic fallback font |
| AI | None | `tenderpack/ai/`: one typed contract, 13 narrow tools, a controller that assigns every status and writes to `staging/ai/` only, budgets, locks, a redacting run log, four routes and an MCP server |
| Unseen addendum | Blind rehearsal 02 (24 hit / 6 partial / 0 missed) | Blind rehearsal 03 with the AI layer in the loop: §3 |

## 2. The AI workflow, in one paragraph

A model gets a task packet (the addendum's provisions, candidate targets, the pattern drafter's output marked unverified, and the schema). It reads through read-only tools (`search_evidence`, `get_unit`, `get_group`, `get_crop`, `compare_state`, `calculate`), checks with `simulate_amendment`, `simulate_programme` and `validate_proposal`, and submits a proposal set. Deterministic code then verifies every quotation against the state before the addendum (verbatim, on the stated page), the state identity and the engine dry run; it assigns the status (`invalid` > `conflicting` > `escalated` > `insufficient_evidence` > `interpretation_pending` > `evidence_verified`), overwrites any status the model wrote and logs the overwrite, computes the impact (STALE rows, voided decisions, C46, A3, programme) and writes `staging/ai/<run_id>/{proposals.yaml,review_request.md,log.jsonl}`. Facts, assumptions and interpretations are kept apart. A named person reads the review request; `tenderpack ai promote RUN_ID --by "Your Name"` copies verified items into curation as PROPOSED drafts, and the accept/reject workflow of session 08 still follows. The model never approves, never edits evidence, never changes policy, never runs code and never publishes; `staging/` is never applied.

## 3. Measured results

### 3.1 Recorded route (offline; hand-written cassettes, not a model)

`tests/test_session09_ai_{contract,tools,propose,mcp}.py`: malformed output, fabricated citations, wrong numbers, prompt injection, stale evidence, rejected ops, provider failure, budget exhaustion, missing capabilities, the lock, the MCP handshake over a subprocess — all pass. The demonstration run on blind-02 (`staging/ai/ADD-03-recorded-20261004T101121Z-1df6/`) ends `partial`: 5 of 42 provisions accounted for (3 `evidence_verified`, 1 `insufficient_evidence`, 1 `escalated`), as the cassette intends.

### 3.2 Host route on blind rehearsal 03 (a Claude Code subagent, Opus 5.5 declared; no application call)

Run `staging/ai/ADD-03-host-20261004T102718Z-97c1/`, 10:14–10:27 UTC (13 minutes), status `complete`, 35 of 35 provisions accounted for: 16 `evidence_verified`, 5 `interpretation_pending`, 5 `conflicting`, 1 `insufficient_evidence`, 13 `escalated`. The proposer declared one assumption (forward counting of "within five Working Days of the date of this Addendum") and three interpretations (the notified closure day, the Q17/3.2 date conflict, the Arabic "working days" against the English "days"); each is marked "needs a person". Its five escalations about Form 4-G and its calendar escalation pointed at tool gaps, fixed before the curation (§3.4).

### 3.3 Blind rehearsal 03 through the normal path

Receipt 10:11 → ingest (573 units) → draft (6 ops, 29 provisions left) → the proposer (above, 12:39) → five live fixes (3:12) → the curator, an Opus 5.5 subagent acting as the live-session curator: every AI item used, corrected or rejected against the evidence (`rehearsals/blind-03/ai-proposals-used.md`), 27 ops, 12 rows, 32 re-made readings, 7 issues, 7 activities, the clarification cut-off recomputed, 2 draft questions (not sent) → `pin`, `check-register` (0 findings), `outputs` (ADD-03 APPLIED, STALE none, exit 0), `diff` → scored output at 11:01:55 (**50 min 31 s** from receipt; the curation 25:52) → key opened at 11:05 after the hashes were checked.

**Score (pre-key outputs only; `rehearsals/blind-03/COMPARISON.md`):** 34 provisions, answers, cover errors, secondary effects and A3 changes: **31 hits, 3 partial, 0 missed**. Every derived date right (the 3.3 notice by the stated alternative the key accepts); all 17 "must not report" traps avoided; the deliberate ambiguity (3.2 vs Q17) escalated with both sources and planned to the earlier date, labelled. The planted cover omission (E2) was found by C28; the planted false statement (E1, "the closure does not affect any deadline") was found by the curator from the recomputed cut-off but not by C28 (fixed after the key). The three partials: the Schedule 11 gap, the membership knock-ons (8.2, 8.4, the new member's own Form 4-C) and the effluent-limit knock-ons (the reliability run, VOL-V 31.1(b)). One marshalling item partial: no activity depends on the VOL-V 29.3 row, so the 85 % Ramp-Up change did not mark the Financial Model for rework.

**What the model did and did not do:** 16 of its items were used exactly as proposed (verified verbatim by the controller); 5 interpretations used; 5 "conflicting" statuses corrected by the curator (two declared conflicts were not conflicts; one was the old approval policy; one date ignored the closure; the real conflict kept open); 13 escalations resolved by the curator, 10 of them tool gaps fixed live. It wrote no register row, reading, issue or activity: the contract carries ops, dispositions and statements, and a person still decided every item. **Human review time** for what the rehearsal produced, estimated and untested: about 2–2½ hours for one reviewer (the 40-item review request against its evidence, 27 ops, 12 rows and 32 readings, 7 issues and 2 questions), before any legal or commercial call.

### 3.4 Live fixes during the rehearsal (before the key was opened; each with a regression)

A form inserted by an addendum is citable (`ADD-02:F4-G`); Arabic words match without diacritic or alef-form differences for `replace_text` on image readings; a notified non-working day is an `annotate` op (`effect: non_working_day`) that the date rules and the programme count from that stage; a whole cell value is evidence however short; an amendment to an owner-approved reading is recorded, not a conflict. The host-route run above was kept as made, before these fixes.

### 3.5 Verification

- **Regressions:** every one of the six findings, the six live fixes and the three post-key fixes has a test that failed before the fix and passes now (`tests/test_session09_*.py`).
- **Full suite:** **516 passed, 0 failed** (38 min 15 s, 12:19–12:57 UTC, every fix in place; session 08 ended at 390). Two earlier runs this session found three stale or crashing tests (an expectation written before a later change; `Register` built without a calendar), each corrected (session log §5).
- **Fresh build:** the real pack rebuilt with the final code is byte-identical to `out/` (every file, the review packets included). A1–A5 differ from session 08 only as intended: the A3 subtitle carries the timezone, the delivery activity carries the Appendix 3 row's full address, and the typed-time assumption row is gone.
- **Strict mode:** `outputs --strict` exits 3 and refuses the release; the only blockers are the 205 rows and 37 ops without a named decision (unchanged since session 08). There is no reading, STALE, coverage or clarification blocker.
- **`make verify`:** passes (two clean rebuilds in disposable folders, byte-identical to each other).
- **The rehearsal folders:** blind-01 and blind-02 regenerated (only the engine's `cited` lists changed); blind-03's scored build untouched, its after-fixes build rebuilt.
- **Logs:** every run log, staging log and cassette scanned for key-like strings: none. No key was ever present in this environment.
- **Not done:** the offline archive was not rebuilt (it is built from a commit, and nothing is committed); the Mac, native viewers and every live route are unchecked.

## 4. Runnable commands per route

Paths are from the repository root; `.venv` is `make setup`'s environment. Nothing below needs a key except the two paid routes.

**Claude Code (MCP, the host's own model; free of application cost):**

```
claude mcp add tenderpack -- $PWD/.venv/bin/python -m tenderpack ai serve-mcp
# in the session: get_task_packet {"addendum":"ADD-03","claim":true,"host_model":"<model>"} → read → simulate/validate → submit_proposals
```

**Codex (MCP):** `~/.codex/config.toml` → `[mcp_servers.tenderpack] command = ".../.venv/bin/python", args = ["-m","tenderpack","ai","serve-mcp"]`, then the same steps.

**Any host through the CLI (what the blind-03 run used):**

```
.venv/bin/python -m tenderpack ai task ADD-03 --claim --host-model "<model>" > /tmp/task.json
.venv/bin/python -m tenderpack ai tool get_unit --json '{"unit_id":"VOL-I:6.1","stage":"ADD-02"}'
.venv/bin/python -m tenderpack ai tool simulate_amendment --json '{"addendum":"ADD-03","ops":[...]}'
.venv/bin/python -m tenderpack ai submit /tmp/ADD-03.proposals.json --route host --host-model "<model>"
```

**Anthropic Messages API (paid; refuses to start without limits):**

```
read -rs ANTHROPIC_API_KEY && export ANTHROPIC_API_KEY
.venv/bin/python -m tenderpack ai capabilities --route anthropic --model claude-opus-5-5     # no paid call
.venv/bin/python -m tenderpack ai propose ADD-03 --route anthropic --model claude-opus-5-5 \
    --max-calls 20 --max-input-tokens 600000 --max-output-tokens 60000 --max-usd <your cap>
```

**OpenRouter (paid):** `read -rs OPENROUTER_API_KEY && export OPENROUTER_API_KEY`, then the same two commands with `--route openrouter --model anthropic/claude-opus-5.5`. Refused from this cloud environment: its network policy blocks `openrouter.ai`.

**Ollama on your Mac (local; never reachable from the cloud):**

```
ollama pull qwen3-vl:32b && ollama serve
.venv/bin/python -m tenderpack ai capabilities --route ollama --model qwen3-vl:32b
.venv/bin/python -m tenderpack ai propose ADD-03 --route ollama --model qwen3-vl:32b
```

**Recorded (tests only):** `.venv/bin/python -m tenderpack ai propose ADD-03 --route recorded --cassette tests/fixtures/ai_cassettes/add03_propose.yaml --evidence rehearsals/blind-02/build --pack rehearsals/blind-02/work/pack.yaml --out /tmp/tp-staging --worklog /tmp/tp-worklog`.

**After any run:** read `staging/ai/<run_id>/review_request.md`; `tenderpack ai promote <run_id> --by "Your Name"`; then `pin`, `check-register --update-ids`, `outputs`, `diff`, and your decisions.

## 5. Remaining defects and limits

1. **No live call has been made.** The Anthropic adapter is written against the API reference and tested with cassettes only; OpenRouter's listing is blocked from this environment; Ollama is unreachable from the cloud and its candidates are unmeasured; a Claude Code session registered with `claude mcp add` (or a Codex session) has not been run: the host route was exercised through the CLI tools by a subagent, and the MCP server by hand over stdio.
2. **A host's model is declared, not verified**, and its usage is invisible to the tool. The USD cap works only on the application routes, from the usage the endpoint reports, against list prices you still have to confirm.
3. **The model's contract carries ops, dispositions and statements, not register rows.** Rows, readings, issues, activities and clarification entries are still written by a person (or the assistant as curator).
4. **A5 does not rework activities for contract-stage rows** (the 85 % Ramp-Up change reached A1 but no activity depends on the VOL-V 29.3 row), and **knock-on rows are not linked** (membership → 8.2, 8.4, the new member's Form 4-C; an effluent limit → the reliability run, VOL-V 31.1(b)): `diff` reports only rows that cite the changed unit.
5. **A referenced but unsupplied document** (Schedule 11) is not raised as an issue on the row whose provision cites it.
6. **A substitution printed across two provisions** needs `old_resolved: matched_in_target` under the provision that prints the new words, or two ops; `new_text_from` exists for `insert_unit` only.
7. **C28 is a report, never a gate.** Its new test covers "does not affect any deadline | the <anchor>" sentences; other phrasings of a derived-date claim are not parsed.
8. **Interpretation pins stay content-only by design**: a moved box with the same words voids decisions, not readings.
9. **Tool friction** reported by the proposer (session log §4.6): the `{"proposal": …}` wrapper, `calculate`'s fixed purpose and unit lists, `simulate_amendment` counting escalations as unaccounted, `get_unit` on a group, a declared conflict outranking `escalated`.
10. **The human review time figures are estimates**, untested against a real reviewer; the blind rehearsals' curators were the assistant, which also wrote the tool.
11. **Blind-01's committed outputs** carry 29 STALE rows from its historical state and its 33 post-award findings; left as history.
12. **Checked on Linux x86_64 only.** The Mac, native Excel and PDF viewers are not checked.

## 6. Inputs needed from you

1. **A key**, set in the environment's credentials (`ANTHROPIC_API_KEY`), never in chat, a file or Git. Until then no application route has made a live call.
2. **A spending cap in USD** for the paid routes (`--max-usd`, or `routes.anthropic.caps.max_usd` in `config/ai.yaml`), and a word on the list prices entered there (Opus 5.5 at 4.0 / 20.0 and Haiku 4.5 at 1.0 / 5.0 USD per million input / output tokens; from the API reference, to confirm against your console).
3. **`openrouter.ai` in the network policy**, if you want that route exercised from the cloud.
4. **Your Mac** for the Ollama route: the measurement protocol is `docs/AI_ROUTES.md` §6; no performance is claimed until it runs.
5. **Your decisions** on the 205 rows and 37 ops of the real pack (unchanged since session 08), and on the blind-03 escalations if you want them as examples of the review step.
6. Whether `staging/` and `worklog/model_calls/` are to be committed (they hold the tender's words and the run logs).
