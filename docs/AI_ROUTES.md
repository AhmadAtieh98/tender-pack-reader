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
2. Read with the read-only tools: `search_evidence`, `get_unit` (pass `stage` = the packet's `previous_stage`), `get_group`, `get_crop`, `compare_state`, `calculate`.
3. Check with `simulate_amendment`, `simulate_programme` and `validate_proposal`.
4. Submit the set with `submit_proposals` (`{"proposal_set": {...}, "host_model": "..."}`), or save it to a file and run:

```
.venv/bin/python -m tenderpack ai submit /tmp/ADD-03.proposals.json --route host --host-model "<model name>"
```

Submitting releases the lock. The result is `staging/ai/<run_id>/review_request.md`.

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

**Dry run.** This makes no paid call: it checks the key and `GET /v1/models/{id}`, which gives the context window, the output cap and image input.

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

## 5. Application route: OpenRouter (paid)

```
read -rs OPENROUTER_API_KEY && export OPENROUTER_API_KEY
.venv/bin/python -m tenderpack ai capabilities --route openrouter --model anthropic/claude-opus-5.5
.venv/bin/python -m tenderpack ai propose ADD-03 --route openrouter --model anthropic/claude-opus-5.5 \
    --max-calls 20 --max-input-tokens 600000 --max-output-tokens 60000
```

- **Capabilities** (images, tools, structured outputs, context) come from `GET https://openrouter.ai/api/v1/models`, fetched once per run.
- **No fallback.** If the listing cannot be reached, or does not list the model, live use is refused.
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

- **Capabilities** come from `/api/show`. A task with image crops and a model without `vision` is refused, and so is a model without `tools`.
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
| MCP server | tested over a subprocess (JSON-RPC over stdin/stdout) |
| Recorded route | hand-written cassettes; offline. The demonstration run on blind-02: `staging/ai/ADD-03-recorded-20261004T101121Z-1df6/` |
| Blind rehearsal 03 | the host-route run above, curated and scored against a sealed key: `rehearsals/blind-03/COMPARISON.md` (31 hits, 3 partial, 0 missed of 34, pre-key) |
| Host route | `submit` is tested with the recorded run's set (same statuses). **Run once for real** on blind rehearsal 03 (4 Oct 2026, 10:14–10:27 UTC): a Claude Code subagent (declared model Opus 5.5) used the CLI tools (`ai task`, `ai tool`, `ai submit`) and produced `staging/ai/ADD-03-host-20261004T102718Z-97c1/` (35 of 35 provisions accounted for). The MCP server was driven by hand over stdio (initialize, tools/list, get_unit); a session registered with `claude mcp add` or a Codex session has **not** been run |
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
- **Model-supplied values.** A model's own `verification_status` or `validation` is overwritten, and the overwrite is logged.

## 11. Credentials and logs

- **Where keys live.** Keys live in the environment only: `ANTHROPIC_API_KEY` and `OPENROUTER_API_KEY`. They are never in `config/ai.yaml`, a file in the repository, a chat, a log or Git.
- **What is logged.** Every prompt (with the full task packet), tool call (with the result truncated to 4,000 characters), raw response, usage, error, overwrite and validation. Logs go to `worklog/model_calls/<run_id>.jsonl` and `staging/ai/<run_id>/log.jsonl`.
- **Redaction.** `Authorization`, `x-api-key`, `*_api_key`, `Bearer …` and `sk-…` strings, and the values of the key variables, are redacted before anything is written.
- **Confidentiality.** Logs and staging hold the tender's words and stay in the repository. Whether `staging/` and `worklog/model_calls/` are committed is the owner's decision.
