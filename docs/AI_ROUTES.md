# AI routes: how a model proposes, and how each route is run

**What the AI layer does.** It reads the evidence through narrow tools and proposes changes for an addendum. Deterministic code (`tenderpack/ai/controller.py`) validates every proposal, assigns its status, computes its impact and writes it to `staging/ai/<run_id>/`. A named person then decides.

**What it never does.**

- It never writes to `curation/`, `config/`, `build/` or `out/`.
- It never approves or accepts anything, and never edits source evidence.
- It never changes validation policy, never runs generated code and never publishes outputs.
- `tenderpack ai promote RUN_ID --by "Your Name"` is a person's step. It copies verified items into curation as PROPOSED drafts and never overwrites a file.

## 1. Two kinds of route

| | Coding host (Claude Code, Codex) | Application routes (`anthropic`, `openrouter`, `ollama`) |
|---|---|---|
| Whose model | the host's own model, in its own session | the model named in `config/ai.yaml` / `--model` |
| Who pays | the host's own subscription or plan; **tenderpack makes no API call and spends nothing** | tenderpack makes the calls: paid for `anthropic` and `openrouter`, local for `ollama` |
| How it works | the host calls the tools over MCP (or the CLI) and submits a proposal file | `tenderpack ai propose` runs the turns, with caps |
| Model recorded | as **declared** by the host (`--host-model`); cannot be verified | requested, and what the endpoint reported |
| Validation | identical: the same contract, checks and statuses | identical |

**One orchestrator per addendum.** A lock file, `staging/ai/.lock-<ADDENDUM>`, stops a host and an API run working on the same addendum. It also stops two API runs doing so.

- A second run is refused while the lock is held.
- A stale lock is reported, never taken over silently. A lock is stale when its process is dead, or when it is older than `lock_stale_after_min` (120).
- Only a person removes a lock: `--break-lock --by "Your Name"`. A name that identifies the assistant or the program is refused, and every break is logged in `staging/ai/locks.jsonl`.
- `tenderpack ai locks` lists the locks.

## 2. Coding host: Claude Code (MCP)

Register the server once. The paths are absolute, and the defaults are the real pack (`build/`, `config/pack.yaml`):

```
claude mcp add tenderpack -- /path/to/tender-pack-reader/.venv/bin/python -m tenderpack ai serve-mcp
# another evidence build / pack:
claude mcp add tenderpack-blind02 -- /path/to/tender-pack-reader/.venv/bin/python -m tenderpack ai serve-mcp \
    --evidence /path/to/tender-pack-reader/rehearsals/blind-02/build --pack /path/to/tender-pack-reader/rehearsals/blind-02/work/pack.yaml
```

Then, in the Claude Code session:

1. Call `get_task_packet` with `{"addendum": "ADD-03", "claim": true, "host_model": "<the model you are running>"}`. This takes the lock and returns:
   - the provisions;
   - the candidate targets;
   - the pattern drafter's output, marked "unverified";
   - the schema.
2. Read with the read-only tools: `search_evidence`, `get_unit` (pass `stage` = the packet's `previous_stage`), `get_group`, `get_crop`, `compare_state`, `calculate`. Since session 10, `get_crop` returns the images themselves as MCP image content (base64 PNG with `mimeType`, up to 3 per call, the unit's own crops first) after the JSON with the paths and sha256, so the host's model sees the crop.
3. Check with `simulate_amendment`, `simulate_programme` and `validate_proposal`.
4. Submit the set with `submit_proposals` (`{"proposal_set": {...}, "host_model": "..."}`), or save it to a file and run:

```
.venv/bin/python -m tenderpack ai submit /tmp/ADD-03.proposals.json --route host --host-model "<model name>"
```

Submitting releases the lock. The result is `staging/ai/<run_id>/review_request.md`.

### 2a. A headless host session, run by the program (session 10)

`tenderpack ai host-session ADD-NN [--provisions ID,..] [--model M]` (`tenderpack/ai/hostsession.py`; for the workflow, `HostSession(ws, cfg).run_batch(packet)` returns the validated, staged proposal set) runs Claude Code without a person at the keyboard:

```
claude -p --mcp-config <session folder>/mcp.json --strict-mcp-config \
    --tools "" --allowedTools "mcp__tenderpack__*" \
    --disallowedTools mcp__tenderpack__get_task_packet,mcp__tenderpack__request_review \
    --permission-prompts none --no-session-persistence \
    --output-format stream-json --verbose --max-turns 40 --system-prompt "<the controller's rules + the host rules>" [--model M]
# mcp.json names one server: <repo>/.venv/bin/python -m tenderpack ai serve-mcp --evidence <abs> --pack <abs> --out <staging> --worklog <log>
# the task packet goes on stdin; a wall-clock timeout (900 s) applies
```

- **No file, shell or web tool.** `--tools ""` removes every built-in tool; the host works only through the MCP tools. `--permission-prompts none` denies anything else that would ask.
- **Images.** The packet lists `image_targets` (candidate targets read from an image); the host is told to call `get_crop` for them and say in `model_rationale` what the image shows.
- **Submission.** The host submits once with `submit_proposals`; the controller validates it exactly as an API run. The lock on the addendum is held for the session (route host) and released by the submission, or by the program when the session ends without one.
- **stream-json, not json.** It records every tool call and tool result; its final `result` message has the json fields (turns, usage, `modelUsage`, `total_cost_usd`).
- **Who pays.** The host's own plan. `total_cost_usd` is recorded as the host plan's figure, never as the application's spend.
- **What is recorded.** In the session folder `staging/ai/<session run id>/` and `worklog/model_calls/<session run id>.jsonl` (redacted like every run log): the command, `mcp.json`, the prompt, every tool call (images by sha256 and size, not their data), the host's text, the result, the submission's run id and statuses, the crops read and the elapsed time. The model is recorded as the CLI reports it (init and `modelUsage`).

**Run for real twice (4 Oct 2026)** on blind rehearsal 03. Both runs:

- **Scope:** ADD-03 provisions 4.1, 4.2 and 5.1 (Form 4-C and Table 2-4).
- **Where they wrote:** the evidence was built into a scratch folder, with staging and the work log pointed there. Nothing was written to the repository's `staging/`.
- **Host model:** the CLI's default, recorded as the CLI reported it.
- **Controller:** `s10-ai-1`.

| | Run 1 (14:02:43–14:03:54 UTC) | Run 2 (14:11:47–14:12:51 UTC, after the duplicate-image fix) |
|---|---|---|
| session / submission | `ADD-03-hostsession-20261004T140243Z-3955` / `ADD-03-host-20261004T140346Z-dd1a` | `ADD-03-hostsession-20261004T141147Z-99f4` / `ADD-03-host-20261004T141245Z-09c6` |
| elapsed, turns | 71.2 s, 11 turns | 63.9 s, 9 turns |
| MCP tool calls | 10: `get_group` ×2, `get_crop` ×2, `get_unit` ×2, `simulate_amendment` ×3, `submit_proposals` | 8: `get_group` ×2, `get_crop` ×2, `get_unit`, `simulate_amendment` ×2, `submit_proposals` |
| crops read (image blocks received) | `VOL-II:T2-4`, `VOL-IV:F4-C/image/decl4` (6; the table's crop was sent twice, since fixed) | the same two (5) |
| 4.1 | `insufficient_evidence`: a fact statement it wrote without evidence | `interpretation_pending` (set_status deleted, as curated) |
| 4.2 | `escalated`: missed the curated `insert_unit` with an anchor and `new_text_from` | `escalated`, the same miss |
| 5.1 | `evidence_verified` (set_value 1 → 0.5) | `insufficient_evidence`: it quoted the row label as the Limit cell; a fact statement without evidence |

- **The host CLI re-encodes a large image.** It passed a 582,564-byte PNG crop on as a 424,162-byte JPEG. The log records what the server sent (by file sha256) and what the model received.
- **Both runs described what the images showed.** Both noted that the Table 2-4 image prints the Total Nitrogen limit as 5, where the text after Addendum No. 2 reads 3. That is the issued page as amended, not an error.
- **A real critic run on run 1's submission.** Critic run `critic-20261004T140551Z-c340` (host route, 9.8 s) reviewed the one item selected (4.1, a removal). It agreed, with three concerns.

Statuses are the controller's; nothing was approved.

## 3. Coding host: Codex (MCP)

In `~/.codex/config.toml`:

```toml
[mcp_servers.tenderpack]
command = "/path/to/tender-pack-reader/.venv/bin/python"
args = ["-m", "tenderpack", "ai", "serve-mcp"]
# for another pack:
# args = ["-m", "tenderpack", "ai", "serve-mcp", "--evidence", "/abs/rehearsals/blind-02/build", "--pack", "/abs/rehearsals/blind-02/work/pack.yaml"]
```

Then follow the same steps as in §2. The package is installed in editable mode, so the server finds the repository from any working directory. A Codex-assisted review is logged like any other host session:

- every tool call goes to `worklog/model_calls/mcp-<session>.jsonl`;
- the submission goes to `worklog/model_calls/<run_id>.jsonl`, with the declared model.

**A host without MCP** can use the same functions through the CLI:

```
.venv/bin/python -m tenderpack ai task ADD-03 --claim --host-model "<model>" > /tmp/task.json
.venv/bin/python -m tenderpack ai tool get_unit --json '{"unit_id": "VOL-I:6.1", "stage": "ADD-02"}'
.venv/bin/python -m tenderpack ai tool simulate_amendment --json '{"addendum": "ADD-03", "ops": [...]}'
.venv/bin/python -m tenderpack ai submit /tmp/ADD-03.proposals.json --route host --host-model "<model>"
```

## 4. Application route: Anthropic Messages API (paid)

**Credential.** It is read from the environment only. Set it in your own shell, never in a file, a chat or Git:

```
read -rs ANTHROPIC_API_KEY && export ANTHROPIC_API_KEY
```

**Dry run.** This makes no paid call: it checks the key and `GET /v1/models/{id}`, which gives the context window, the output cap, image input and structured outputs. If there is no key, the call fails, the model is not listed, or the reply omits `max_input_tokens` or `max_tokens`, the answer is `REFUSED: ... capabilities unverified` (§12).

```
.venv/bin/python -m tenderpack ai capabilities --route anthropic --model claude-opus-5-5
```

**A run.** It refuses to start until you set limits. With the list prices in `config/ai.yaml` (to confirm against your console), `--max-usd` is enforced from the usage the endpoint reports; `--max-calls` is always required. The numbers below are examples: the limits are yours to choose.

```
.venv/bin/python -m tenderpack ai propose ADD-03 --route anthropic --model claude-opus-5-5 \
    --max-calls 20 --max-input-tokens 600000 --max-output-tokens 60000 --timeout-s 1800
```

**Example configuration** (`config/ai.yaml`, `routes.anthropic.models`):

- `propose: claude-opus-5-5`, with `request_extra: {output_config: {effort: high}}`;
- `check: claude-haiku-4-5-20251001`.

**Behaviour.**

- The assistant's content is replayed unchanged from turn to turn.
- No server-side model fallback is requested. A refusal ends the run `provider_failed`; it is never answered silently by another model.
- 408, 409, 429, 5xx and 529 responses and timeouts are retried up to `retries` (2), with backoff that honours `retry-after`.
- **Structured output** (`structured_output: {mode: native}`): when the models endpoint reports structured outputs, every request carries `output_config.format` (`{type: "json_schema", schema}`) merged with the configured effort, beside the tools (§13).
- **Token counting.** `POST /v1/messages/count_tokens` (free) calibrates the batch planner with `--count-tokens` (§14).

## 5. Application route: OpenRouter (paid)

```
read -rs OPENROUTER_API_KEY && export OPENROUTER_API_KEY
.venv/bin/python -m tenderpack ai capabilities --route openrouter --model anthropic/claude-opus-5.5
.venv/bin/python -m tenderpack ai propose ADD-03 --route openrouter --model anthropic/claude-opus-5.5 \
    --max-calls 20 --max-input-tokens 600000 --max-output-tokens 60000
```

- **Capabilities** (images, tools, structured outputs, context) come from `GET https://openrouter.ai/api/v1/models`, fetched once per run.
- **No fallback.** If the listing cannot be reached, does not list the model, or gives no `context_length`, live use is refused.
- **Structured output.** `response_format: {type: "json_schema", json_schema: {name, strict: true, schema}}`, only when the listing's `supported_parameters` name `structured_outputs` (`response_format` alone is not taken as JSON-schema support). This request shape is OpenRouter's OpenAI-compatible convention; it has **not** been checked from here.
- **Unverified here.** The slugs in `config/ai.yaml` are marked "unverified". This cloud environment's policy blocks `openrouter.ai`, so the `capabilities` call above was **refused here** (observed on 4 Oct 2026).
- **Cost.** The prices in the listing are reported but never used for cost.

## 6. Application route: Ollama on the owner's Mac (local)

This route runs **on the Mac only** (M5 Pro, 48 GB). The cloud session cannot reach the Mac's `localhost`, and nothing assumes it can.

```
ollama pull qwen3-vl:32b        # vision candidate, about 20 GB at 4-bit (published size; not measured here)
ollama pull qwen3:30b-a3b       # text candidate
ollama serve                    # default http://127.0.0.1:11434 (or export TENDERPACK_OLLAMA_URL=...)
.venv/bin/python -m tenderpack ai capabilities --route ollama --model qwen3-vl:32b
.venv/bin/python -m tenderpack ai propose ADD-03 --route ollama --model qwen3-vl:32b
```

- **Capabilities** come from `/api/show`. A task with image crops and a model without `vision` is refused, and so is a model without `tools`. A reply without a context length is refused too (the `num_ctx` bound cannot be checked), unless `--allow-unverified-capabilities` is given.
- **Structured output.** `format: <schema>` on `/api/chat`. With `with_tools: false` (the default) it is withheld on a turn that offers tools, because a format grammar may stop the model emitting tool calls; requests without tools (the critic) carry it. Check this on the Mac, then set `with_tools: true`.
- **Context.** `num_ctx` is bounded at 32768 (`config/ai.yaml`), and never set above what `/api/show` reports.
- **Packet size.** The blind-02 ADD-03 task packet is 47,443 characters. That is about 13,600 tokens, estimated at 3.5 characters per token (not a tokenizer count). With 16,000 output tokens it fits 32768 only at the start. The controller stops the run (`budget_exhausted`, "context bound") before the conversation outgrows the bound.
- **Smaller tasks.** `--provisions ADD-03:2,ADD-03:3` sends part of an addendum. The other provisions are still listed as unaccounted.

**Measurement protocol** (to run on the Mac; no performance is claimed until it is done). For each candidate, three runs each:

1. Record `ollama show <model>`: the digest, the quantization and the context.
2. Run `propose` on the blind-02 pack (or the next sealed rehearsal).
3. From the run log (`worklog/model_calls/<run_id>.jsonl`, `response.usage.detail`), record:
   - wall time per call (`total_duration`);
   - prompt and output tokens;
   - tokens per second (`eval_count / eval_duration`).
4. Record peak memory (Activity Monitor or `vm_stat`).
5. Record the statuses, and the `reference` comparison in `proposals.yaml` (same / partly / different / missed against the curated op file).
6. Once the owner has approved the readings, run the reading benchmark of PLAN §4.6 as well: Table 2-4 cell accuracy, Form 4-C character accuracy and the ٤-x digit.

## 7. Recorded route (offline tests only)

```
.venv/bin/python -m tenderpack ai propose ADD-03 --route recorded --cassette tests/fixtures/ai_cassettes/add03_propose.yaml \
    --evidence rehearsals/blind-02/build --pack rehearsals/blind-02/work/pack.yaml --out /tmp/tp-staging --worklog /tmp/tp-worklog
```

- **What a cassette is.** A cassette (`tests/fixtures/ai_cassettes/*.yaml`) is a hand-written sequence of provider turns. It is **not** a live model's output, and the recorded route is **not** a working live integration.
- **What it tests.** That the controller, the tools, the validation and the staging behave correctly whatever a model returns:
  - malformed output;
  - fabricated citations;
  - wrong numbers;
  - prompt injection;
  - stale evidence;
  - rejected ops;
  - provider failure;
  - budget exhaustion;
  - missing capabilities;
  - the lock.

## 8. What is mocked, recorded or live

| Path | Status (4 Oct 2026) |
|---|---|
| Controller, tools, validation, impact, staging, promote, lock, budget | built and tested offline: `tests/test_session09_ai_*.py` |
| MCP server | tested over a subprocess (JSON-RPC over stdin/stdout); `get_crop` image content tested offline (`tests/test_session10_routes.py`) and received by a real headless host (§2a) |
| Capability policy, structured outputs, batches, critic (session 10) | **recorded**: HTTP cassettes replayed through the real adapters (`tests/fixtures/ai_cassettes/s10_*.yaml`) and a recorded stand-in for the `claude` CLI (`fake_claude_host.py`, not a model); `tests/test_session10_routes.py` |
| Headless host session (session 10) | **host-executed** twice for real on blind rehearsal 03 (§2a): `claude -p` over MCP only, 3 provisions, crops read, submitted, 71 s and 64 s |
| Critic, host route (session 10) | **host-executed** once for real on that submission (4 Oct 2026, 14:05:51 UTC): critic run `critic-20261004T140551Z-c340`, 1 item selected (4.1, a removal), 9.8 s, the critic agreed with 3 concerns; no status changed |
| Structured outputs, live | **not executed live**: no key (Anthropic), blocked (OpenRouter), not reachable (Ollama); the request shapes are recorded only |
| Recorded route | hand-written cassettes; offline. The demonstration run on blind-02: `staging/ai/ADD-03-recorded-20261004T101121Z-1df6/` |
| Blind rehearsal 03 | the host-route run above, curated and scored against a sealed key: `rehearsals/blind-03/COMPARISON.md` (31 hits, 3 partial, 0 missed of 34, pre-key) |
| Host route | `submit` is tested with the recorded run's set (same statuses). **Run once for real** on blind rehearsal 03 (4 Oct 2026, 10:14–10:27 UTC): a Claude Code subagent (declared model Opus 5.5) used the CLI tools (`ai task`, `ai tool`, `ai submit`) and produced `staging/ai/ADD-03-host-20261004T102718Z-97c1/` (35 of 35 provisions accounted for). The MCP server was driven by hand over stdio (initialize, tools/list, get_unit); an interactive session registered with `claude mcp add` or a Codex session has **not** been run; a headless `claude -p --mcp-config` session has (session 10, §2a) |
| Anthropic | adapter written over `urllib`; **no live call made** (no key in this environment) |
| OpenRouter | adapter written; the model listing is **blocked by policy** here, so live use is refused |
| Ollama | adapter written; **not reachable** from the cloud; to be run and measured on the Mac |

## 9. Budgets, spend and cost

**Caps.** They are set in `config/ai.yaml` (`defaults.caps` < `routes.<route>.caps` < the command line):

- run limits: `max_calls`, `max_input_tokens`, `max_output_tokens`, `max_usd`, `timeout_s`, `max_turns`, `concurrency`;
- per call: `max_tokens_per_call`, `call_timeout_s`, `retries`, `backoff_s`.

**What happens at a cap.** Each retry counts as a call. Exceeding a cap stops the run with status `budget_exhausted`; the partial log and an empty proposal record stay in staging.

**Prices.** `prices: {model: {input_per_mtok, output_per_mtok}}` holds the first-party list prices for the two configured Anthropic models (from the API reference, cached 2026-09-25; confirm them on your console). For a model without a price:

- `cost_usd` is `null`, with `cost_basis: "no price configured"`;
- a paid route refuses to start unless `max_calls` and both token caps are set.

**Spend meter.** Every call, including each failed attempt, is appended to `staging/ai/spend.jsonl`.

## 10. Statuses (assigned by the controller, never by the model)

`invalid` > `conflicting` > `escalated` > `insufficient_evidence` > `interpretation_pending` > `evidence_verified`.

- **`evidence_verified`** means that three things hold:
  - every quotation is verbatim in the named unit at the state before the addendum, on the stated page;
  - the state identity matches;
  - for an op, the engine dry run is valid (C21–C27, C47).

  It is **not** an acceptance, and it does not verify meaning.
- **`interpretation_pending`** covers:
  - row readings;
  - annotations that interpret or add obligations;
  - old words located in the target rather than quoted;
  - anything that depends on an interpretation or an assumption.
- **`conflicting`** covers:
  - an op or row whose latest decision is a rejection;
  - a contradiction with an accepted decision;
  - a conflict the proposer itself declares between provisions.
- **An amendment to an approved reading** (a change to a unit read from an image whose transcription you approved) is not a conflict: the approval covers the transcription of the issued page, and an addendum may change the words. The `approvals` check records the region and the approval, the status comes from the other checks, and the review request shows the record. (Changed on 4 Oct 2026 after the host-route run on blind rehearsal 03 had marked ADD-03 5.1 `conflicting` for this reason; that run is kept as made.)
- **Model-supplied values.** A model's own `verification_status` or `validation` is overwritten, and the overwrite is logged. Since session 10, so is a `review` (only the critic writes one, §15).
- **The semantic check (session 10).** A "no change" answer (a `no_effect` disposition, or an annotation that changes nothing) is checked against what the provision's own words do, as the pattern drafter reads them. These records carry `aspect: semantic` and are kept apart from the evidence checks.
  - **`invalid`**: a `no_effect` on words from which the drafter drafts a change. That covers a substitution, deletion, insertion, reissue, value change, reinstatement or revocation, so the answer contradicts the evidence.
  - **`interpretation_pending`**: a `no_effect` on other amendment, obligation or exception language whose reason quotes the provision. Such language includes a quoted old/new pair, "is amended", "shall" and "unless".
  - **`insufficient_evidence`**: the same case when the reason quotes none of the provision's words.
  - **A `no_effect` on amendment language never verifies.** A printed change needs its op.
- **Resolution (session 10), apart from coverage.** `ProposalSet.resolution` puts each provision of the addendum in exactly one class:
  - **resolved**: every answer is `evidence_verified`, consistent with the provision's own words, and decides it;
  - **pending**: answered, but a person must still decide;
  - **invalid**: an answer to it is invalid, and an invalid answer accounts for nothing;
  - **unaccounted**: no answer.

  It also lists the provisions answered "no change" despite amendment language. A set is `complete` only when every provision is accounted for **and** resolved. `resolution.approved` is always 0, because approval is a named person's decision. Coverage (accounted for), evidence verification (verbatim quotations), semantic resolution and approval are four separate things.
- **The state identity (session 10).** Besides the pack id, the evidence build's identity, the validated and working stages and the decisions file, it carries sha256s of:
  - the assumptions file (calendar, holidays, counting policy, durations);
  - the activity templates;
  - the approvals and reading files;
  - the earlier addenda's op files;
  - any image crops the build's manifest does not record.

  A proposal or a calculation made under other inputs is `stale`. A running workspace re-checks its inputs on every evidence read and refuses with "workspace stale: reload". `get_crop` verifies each file against the manifest's recorded hash and refuses with "integrity failure". `submit`, `propose` and `promote` re-check freshness, and a stale set cannot be promoted.

## 11. Credentials and logs

- **Where keys live.** Keys live in the environment only: `ANTHROPIC_API_KEY` and `OPENROUTER_API_KEY`. They are never in `config/ai.yaml`, a file in the repository, a chat, a log or Git.
- **What is logged.** Every prompt (with the full task packet), tool call (with the result truncated to 4,000 characters), raw response, usage, error, overwrite and validation. Logs go to `worklog/model_calls/<run_id>.jsonl` and `staging/ai/<run_id>/log.jsonl`.
- **Redaction.** `Authorization`, `x-api-key`, `*_api_key`, `Bearer …` and `sk-…` strings, and the values of the key variables, are redacted before anything is written.
- **Confidentiality.** Logs and staging hold the tender's words and stay in the repository. Whether `staging/` and `worklog/model_calls/` are committed is the owner's decision.

## 12. Capability policy (session 10)

- **Where capabilities come from.** A live route's capabilities come from its endpoint: `GET /v1/models/{id}` (Anthropic), `GET /models` (OpenRouter), `POST /api/show` (Ollama).
- **Refused, not filled in.** Live use is refused with the reason ("capabilities unverified") when:
  - the endpoint cannot be reached, or there is no key to call it;
  - it does not list the model;
  - it omits the context window (Anthropic also the output cap).

  A capability leaf the endpoint does not report (image input, structured outputs) is unknown. It is never taken from the configuration.
- **The configured `capabilities:` block** is used only in two cases:
  - by the recorded route (its cassette);
  - when a person passes `--allow-unverified-capabilities` (`propose(..., allow_unverified_capabilities=True)`).
- **What the flag leaves behind.** The run log's `capabilities` event says `UNVERIFIED (...; --allow-unverified-capabilities)` and `details.unverified: true`. A `route_notices` event is logged, `proposals.yaml` gets `controller.route_notices`, and the review request has a "Route notices" section reading "capabilities unverified".
- **Tool use on the Messages API.** It is taken as a feature of every model the endpoint lists. The documented models response has no tool-use leaf. A model that rejected `tools` would fail its first call visibly.

## 13. Structured outputs, beside the local validation (session 10)

- **The schema.** It is derived from `contract.ProposalSet.model_json_schema()`, trimmed to what the proposer fills (`contract.model_fill_schema()`). `tenderpack/ai/providers/structured.py` then fits it to the provider's limits:
  - `additionalProperties: false` on every object;
  - no numeric, length or pattern constraints, and no titles or defaults;
  - recursion refused.
- **The payload.** An item's free-form `payload` cannot be expressed under those limits, so it travels as a JSON-encoded string. The controller decodes it before its strict parse and then validates it against the payload schemas as before.
- **Validation is unchanged.** The controller parses and validates every answer itself, whether or not the provider constrained it. Native structured output never replaces that validation.

| Route | Setting | Request field | When |
|---|---|---|---|
| anthropic | `structured_output: {mode: native}` | `output_config.format = {type: "json_schema", schema}`, merged with `output_config.effort`; sent with the tools on every turn | `GET /v1/models/{id}` reports `structured_outputs` |
| openrouter | `structured_output: {mode: native}` | `response_format = {type: "json_schema", json_schema: {name: "proposal_set", strict: true, schema}}` | the listing names `structured_outputs` |
| ollama | `structured_output: {mode: native, with_tools: false}` | `format = <schema>` (free-form objects allowed there) | a request without tools, or any request once `with_tools: true` |
| recorded / host | none | the cassette replays turns; a host session submits through `submit_proposals` | — |

- **Where the shapes come from.** Anthropic's is from the bundled claude-api skill:
  - `python/claude-api/tool-use.md`, "Structured Outputs": "Raw Schema" and "Using Both Together";
  - its limits: `shared/tool-use-concepts.md`, "JSON Schema Limitations".

  The OpenRouter and Ollama shapes are their documented request fields. Neither was checked from this environment.
- **A rejected schema.** A 4xx naming the schema or the structured-output field switches the run to the plain tool-use path for the rest of the run, where the answer is text parsed locally:
  - the attempt is retried without the field and counted as a call;
  - a route notice reaches the run log, `proposals.yaml` and the review request. Nothing is silent.
- **Not used natively.** When native output is not used (the capability is not reported, the mode is `off`, or the schema cannot be fitted), a route notice says so.

## 14. Bounded batches (session 10)

`tenderpack ai plan-batches ADD-NN [--route R --model M | --context-tokens N --max-output-tokens N] [--count-tokens]` (`tenderpack/ai/batching.py`; the workflow calls `plan_batches(provisions, capabilities, overhead) -> list[Batch]` and runs one propose per batch with a checkpoint).

- **The fit test.** A batch fits when its output is within the output cap and its input plus output is within the context window less `context_margin`.
  - Input: system, tools, the packet without its provisions, the batch's provisions and their crops, and `prior_turns_tokens`.
  - Output: `output_tokens_fixed`, plus `output_tokens_per_provision` for each provision.
- **Where the limits come from.** The verified capabilities. A plan is refused without a context window. Figures given with `--context-tokens` are labelled as a person's.
- **Nothing is dropped.** Every provision is in exactly one batch, in addendum order (`assignment`). A provision that cannot fit even alone is its own batch with `fits: false` and the note "too large: needs a person to split", with its size. The note also says when the overhead alone leaves no room.
- **Sizes are estimates.** They use 3.5 characters per token, 4,800 tokens per image crop and 700 output tokens per provision (from the blind-03 host run: 68,854 characters for 35 provisions). `--count-tokens` (Anthropic, with a key) measures the packet with `POST /v1/messages/count_tokens` and records the source on every batch.
- **Settings.** In `config/ai.yaml` `batching:`. A route may override them; Ollama sets `prior_turns_tokens: 8000` for its 32,768 bound.

## 15. The independent critic (session 10)

`tenderpack ai critic RUN_ID [--route host|recorded|anthropic|openrouter|ollama] [--model M] [--max-items N]` (`tenderpack/ai/critic.py`; `config/ai.yaml` `critic:`) is a second model pass over **selected** items only.

**Which items.** Each reason is recorded on the review:

| Reason | What selects an item |
|---|---|
| removal | `set_status` deleted or revoked; an interpretation recording `removed` words |
| conflicting | the controller's status `conflicting`, or a conflict the proposer declares |
| consequential_interpretation | a row interpretation stating a consequence; an annotation that interprets or adds an obligation; a `no_effect` disposition resting on an interpretation or assumption statement |
| uncertain_target | from the controller's validation records and the previous state: old words located in the target rather than quoted; a target that is a group or is resolved through one; a heading target; a target the provision does not cite |

`invalid` items are left out.

**How it reads them.**

- **No tools.** The evidence is inline: the item, the provision's text, the target's text before the addendum, the statements relied on, and the controller's validation records.
- **Its own system prompt** (`critic.CRITIC_SYSTEM`).
- **Its own route and model**, where `critic.route` / `critic.model` are configured:
  - `host`: `claude -p --tools "" --system-prompt <critic> --json-schema <answer> --output-format json`, under a timeout;
  - `recorded`: a cassette;
  - API routes: the same provider interface, with `response_schema`.

**What it writes.**

- **The answer.** `{agrees, concerns[], evidence_checked[]}` is written to the item's `review.critic` (with route, model and reasons) in the run's `proposals.yaml`. It also goes to the "Independent critic" section of `review_request.md`, and to `critic_*` events in the run log.
- **No status changes.** A guard refuses to write if any status differs. Agreement between models is not approval.
- **Model-supplied reviews are dropped.** A `review` supplied by a proposer is dropped when the set is parsed, and recorded as an overwrite.

## 16. The run command (session 10)

One runnable, resumable workflow from a new addendum PDF and the preceding tender state to candidate A1–A5 outputs and a review packet (`tenderpack/ai/workflow.py`, with `candidate.py`, `checkpoint.py` and `downstream.py`). Nothing it does touches the real `curation/`, `config/` or `out/`, and nothing is approved, accepted, sent or published.

### The commands

```
.venv/bin/python -m tenderpack ai run ADD-04 --pdf sources/incoming/ADD-04.pdf [--route host|recorded|anthropic|openrouter|ollama] \
    [--pack config/pack.yaml] [--evidence build] [--run-id ID] [--batch-size 8] [--downstream-batch-size 12] \
    [--model M] [--cassette P] [--host-model NAME] [--host-model-alias M] [--host-manual] \
    [--stop-after STEP] [--no-background] [--no-cache] [caps as for propose] [--allow-unverified-capabilities]
.venv/bin/python -m tenderpack ai resume RUN_ID [--stop-after STEP] [--no-retry]
.venv/bin/python -m tenderpack ai submit-batch RUN_ID FILE --by "Name or host session" [--host-model NAME] [--batch ID]
.venv/bin/python -m tenderpack ai run-status RUN_ID
```

- `--pack` and `--evidence` name the **preceding state**: the pack configuration as it stands and its evidence build. The PDF is the new addendum. `--out` is the staging root (default `staging/ai`); a run lives in `staging/ai/runs/<run_id>/`.
- **Exit codes:**
  - 0: the run finished (complete or partial) or stopped where `--stop-after` asked;
  - 1: a step failed, or the candidate outputs build was refused;
  - 2: refused before anything ran, or ingest found a structural failure;
  - 4: the run waits for a host submission.
- **The caps** bound the whole run, not each batch: every batch gets what is left.

### The steps

Each step is checkpointed.

1. **ingest.** The candidate workspace is a disposable copy, under `runs/<run_id>/candidate/`, of every file the pack configuration names:
   - the op files, register rows and their per-document files, pins, the id ledger, issues, dispositions, proposals and evidence items;
   - the activity templates, the clarification register, the decisions file and the relationships file;
   - the assumptions, scenarios, furniture rules and manifest;
   - the owner's approvals, readings and reading snapshots, copied unchanged and used read-only.

   The PDF is added as a document: a copy in `candidate/input/`, a `documents:` entry, and its sha256 and page count in the candidate's manifest. Then `ingest` builds `candidate/build/`. A structural failure stops the run with the reason. A second copy (`candidate/before/`, without the PDF) starts building the pre-addendum outputs, `candidate/out-before/`, in a background process from the previous evidence build. These are built once per run, or copied from `runs/_cache/` when the previous build, the copied files and the code are the same.
1a. **readings** (only when the addendum carries an image region with no text layer). Ingest refuses such a candidate (C05 "unread"). When C05 is the only failure and only unread regions caused it, the run does not stop: one batch per region proposes a reading (`tenderpack/ai/regionread.py`).
   - **Tools** (MCP and the readings step; read-only; they read the refused build `candidate/build.failed/` and nothing of the stage 2 state):
     - `get_region(region_id, bands, cells)`: the region's doc, page, bbox, native image size and sha256, the text and rule bands measured from pixels with their crops, the ruled grid if any, and a content-type guess. It returns the images too: the native image and the page context, or the band (and cell) crops asked for, three per call. Every file is checked against `BUILD_MANIFEST.json`.
     - `validate_reading(reading)`: `readings.check_reading` (RD1–RD9) on a draft; writes nothing.
   - **What is proposed.** A `region_reading` (`contract.RegionReadingProposal`) whose `reading` is a `readings.Reading` in the exact shape of the pack's own readings (a table and a form are in the packet as examples). The packet's `state` is the region's source (doc, page, bbox, native sha256), copied as `reading.source`.
   - **Routes.** On the host route, a headless host session per region over the two MCP tools, its final message the proposal; with `--host-manual`, the packet `batches/reading-<region>.packet.json` and `submit-batch`. The recorded and API routes run the same tools in the workflow's own turn loop.
   - **Validation.** The controller rewrites `prepared_by` (AI-assisted, the session, the run). A proposal that is not a Reading, names another region or unit, or fails RD1/RD2 is `invalid`; any other failed check makes it `insufficient_evidence`; otherwise it is `interpretation_pending`, never higher: a reading interprets an image.
   - **Writing.** A usable reading is written into the candidate's `curation/readings/<region>.yaml`, headed "AI-PROPOSED READING — PENDING HUMAN REVIEW". No approval entry is written, and every unit made from it carries `reading.status: pending`. Then ingest runs again. A region without a usable reading, or a second refusal, stops the run with the reason; `resume` asks again.
   - **Review.** The review packet lists each reading with its status and checks, and links the build's own packet (`candidate/build/review/<region>/packet.html`), which shows the reading beside its crops, marked pending.
2. **analysis.** The provisions are split into bounded batches, in document order, keeping a section together and at most `--batch-size` per batch.
   - **What is covered.** Every provision: cover lines, notes, table rows, form rows and image readings. The addendum's other units (headings, table containers) are listed as structure.
   - **API routes.** A batch is also split when the verified context or output cap cannot take it (`batching.plan_batches`). Each batch is one `controller.propose` run.
   - **Host route.** A headless host session per batch (`hostsession.HostSession.run_batch`) when the host CLI is installed, unless `--host-manual`. Otherwise the run writes `batches/<id>.packet.json` and waits for `submit-batch`.
   - **Recorded route.** One cassette session per batch (`sessions:`, each matched on the batch's provisions).
3. **validation.** The items of every batch are validated as one set by `controller.validate_set`, with the controller's statuses, coverage and resolution (`ai/<run_id>-combined/`). An op whose change type the engine does not have becomes an escalation, keeping its evidence. It is never forced into a known type.
4. **downstream.** The ops and dispositions that can be promoted are dry-run together. Their impact becomes tasks:
   - every row citing a changed unit or STALE at the addendum (re-make its reading);
   - every C46 gap (a new or amended obligation without a row);
   - every clarification entry citing a changed unit;
   - the A5 activities needing those rows;
   - every escalated or contested provision, with its affected scope (units, rows, activities, clarification entries).

   The proposals for these tasks come in bounded batches as a `DownstreamSet` (`contract.py`): `row_reading`, `row_new`, `issue`, `clarification_item`, `evidence_item`, `activity` (its duration a PROVISIONAL ASSUMPTION) and `dependency` (a relationships-file entry).
5. **downstream_validation** (`downstream.validate`), in the candidate, against the state the promotable ops produce:
   - the register's own checks: quotes verbatim in the effective text at the stage, the consequence class with its quote, date rules that parse and whose words are in their unit, ids new and absent from the ledger;
   - `clarify.check` on the candidate register;
   - the schedule checks (C40, C44, C45) with the proposals;
   - `relationships.validate`.

   **Interactions.** A reading of a row an op makes REMOVED or DELETED is invalid. A new row whose units are not in the effective text is invalid. An activity needing a row that is neither existing nor proposed is invalid. An item depending on one that cannot be promoted is held back.

   **Statuses.** Rows, readings, activities and relationships are never above `interpretation_pending`. A question is forced to `draft, not sent`, and a relationship to `proposed`, with the overwrite recorded.
6. **promotion**, into the candidate only:
   - the op file: the promoted items PROPOSED, origin `assistant`; every other provision `unresolved` with its reason;
   - new rows (`register/rows/<ADD>-ai.yaml`) and re-made readings, inserted into the rows' own files;
   - issues, evidence items, templates and lead times;
   - clarification entries;
   - relationships, through `relationships.append_proposed`.

   Promotion is idempotent: it starts from a snapshot of the candidate taken before the first promotion.
7. **pin, check_register.** `pin` and `check-register --update-ids` run on the candidate, against its own pins and id ledger.
8. **outputs.** The pre-addendum outputs are joined first.
   - **Pre-flight.** The structural checks that need no output (E01, C16, C25, C12, C47) are run first; a failure refuses the build.
   - **Build.** `outputs` builds `candidate/out/`. A refused build keeps `out-before/` as the last validated state, and the review says so.
   - **Marking.** Every candidate file carries the banner "CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted". A1 gets a candidate status column, `PROPOSED BY THE AI WORKFLOW`, `UNRESOLVED`, `DECIDED` or `proposed (existing row)`, and a `Candidate statuses` sheet.
9. **diff.** `diff` runs from the previous stage to the addendum in the candidate, and `out-before` is compared with `out`.
10. **review.** `review/index.md` (and `index.html`) shows the unresolved and escalated provisions first. Then, per provision, the chain: source evidence, proposed transition, validation, downstream impact, output difference. It also gives the downstream items, what was promoted, the check-register findings, coverage, the timings, every manual intervention, the diff, and links to the candidate A1–A5 and to `out-before`.

When the addendum is PARTIAL in the candidate (any provision unresolved), A3 and the A5 programme show the validated (previous) state. The addendum as proposed is in A1's column for it, in A2, in `a5/working/<ADD>.json` and in the diff.

### The checkpoint (`runs/<run_id>/checkpoint.json`, format `tenderpack-ai-run/1`)

It is rewritten atomically after every change. It holds:

- `settings`: what the run started with; `resume` reuses them;
- `inputs`: the PDF's path, sha256 and pages; the preceding pack and evidence build; and the sha256 of every real input copied, used to report anything another process changed during the run;
- `steps`: the status, start, finish, attempts and wall-clock seconds of each step, with each step's own detail (exit codes, counts, the refusal reason);
- `batches`: phase, provisions or tasks, status (`pending` / `running` / `waiting_for_host` / `done` / `failed` / `skipped` / `interrupted`), attempts, the staged controller run, the recorded session or host session, and seconds;
- `provisions`: per provision, `pending` → `proposed` → `validated` (or `unaccounted` when its batch answered nothing for it), with the history, items and statuses, and `accounted_by` for content of another item's op;
- `structure`: the units that are not provisions;
- `downstream`: per task and per item (`proposed` → `validated`);
- `interventions`, `usage`, `events` (started, resumed, a stale lock taken over).

### Resumption

`resume` skips what is done and never asks twice:

- a provision that is not `pending` is not asked again;
- a batch whose result was received is not re-run;
- a batch that failed or was interrupted is asked again, and the steps after it are recomputed from the candidate as it was before promotion. `--no-retry` keeps failures as they are.

The run lock (`run.lock`) lets one process drive a run. A lock whose process is dead is taken over by `resume`, and the takeover is recorded in `events`.

### The manual host path

On the host route without a host CLI (or with `--host-manual`), the run stops with exit 4 at the first batch and prints the packet path. A coding assistant without MCP, or a person, answers with a proposal set: a `ProposalSet` for an analysis batch, a `DownstreamSet` for a downstream one. Then:

```
.venv/bin/python -m tenderpack ai submit-batch RUN_ID answer.json --by "Who submits" --host-model "<the model used>"
```

The set is validated exactly as an API run's. The submission (who, when, the batch, the file and its sha256, the declared model) is recorded under `interventions` and listed in the review packet. The run then continues to the next batch.

### Candidate and real

| | Where | What |
|---|---|---|
| Candidate | `runs/<run_id>/candidate/` (`pack.yaml`, `build/`, the copied curation, `out/`) | proposed by the run; every output carries the banner |
| Last validated state | `candidate/out-before/` (else the real `out/`) | the pre-addendum outputs, never modified by the run |
| Real | `curation/`, `config/`, `out/`, `build/` | only read; their sha256 at the start is in the checkpoint |
| Logs | `runs/<run_id>/log.jsonl`, `logs/`, `ai/<batch run>/`, `worklog/model_calls/` | every batch's prompt, tool calls, responses, validation |

**Taking anything over.** Nothing is applied to the real curation. A person adds the PDF to the pack (OPERATING_GUIDE §3 steps 1–2), reviews and copies the files `promotion.json` lists, then runs `pin`, `check-register` and `outputs`, and decides with `accept` / `reject`.
