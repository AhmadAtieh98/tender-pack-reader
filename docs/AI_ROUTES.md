# AI routes: how a model proposes, and how each route is run

**What the AI layer does.** It reads the evidence through narrow tools and proposes changes for an addendum. Deterministic code (`tenderpack/ai/controller.py`) validates every proposal, assigns its status, computes its impact and writes it to `staging/ai/<run_id>/`. A named person then decides.

**What it never does.**

- It never writes to `curation/`, `config/`, `build/` or `out/`.
- It never approves or accepts anything, and never edits source evidence.
- It never changes validation policy, never runs generated code and never publishes outputs.
- `tenderpack ai promote RUN_ID --by "Your Name"` is a person's step. It copies verified items into curation as PROPOSED drafts and never overwrites a file.

## 1. Two kinds of route

Session 12 names four kinds. `tenderpack ai routes` prints each route's kind, what has been verified and what is
pending on the Mac:

- **Connected coding host** (`host`): Claude Code or Codex, working with its own model over MCP or the CLI.
  - Claude Code headless sessions are started by the workflow and have run for real in the cloud container (sessions
    10–13; the sealed blind-07 run from a twin of the interview folder). On the Mac: pending.
  - For Codex, the MCP interface is tested; automated Codex execution is unverified. The workflow starts Claude Code
    only; Codex is the manual MCP / `submit-batch` path.
- **Hosted API** (`anthropic`, `openrouter`): the application makes paid calls.
- **Local inference** (`ollama`): a model on this machine. Offline mode (§17) runs every phase here and nothing hosted.
- **Recorded**: tests only.

**Session 13: the status of each route, and the connected/offline choice.** `config/routes_status.yaml` records where
and when each route was last exercised and with what result; `tenderpack ai routes` prints it beside the route's live
availability on this machine and why it is not usable (`--brief`: one line each, as the launcher shows it):

| Route | Status (config/routes_status.yaml) | Usable now when |
|---|---|---|
| `host` (Claude Code; the first route to rehearse) | tested: the cloud container, sessions 10–13, the last time the sealed blind-07 run from a twin of the interview folder; pending on the Mac | connected, and `claude` on PATH |
| `codex` (Codex over MCP) | built, unverified: the MCP server and the manual host path are tested, no Codex session has run | never automatically (the workflow starts Claude Code only); by hand, §3 |
| `anthropic` (API key) | untested: recorded responses only; ready: the dry run in §4 | connected, a key through the secure configuration (§11), the paid caps set |
| `openrouter` (API key) | blocked here, unverified; ready for a later key: the configuration and dry run in §5 | as `anthropic` |
| `ollama` (offline) | pending on the Mac: prepared for local use (§6), tested against a fake local server | a configured model installed and usable (`tenderpack ai ollama-models`) |

Session 14: each route's record also says what **works** (and where that was shown), what was **never run**, and
what is **ready** to try (the exact commands; tenderpack runs none of them by itself). `tenderpack ai routes` prints the
three; the launcher (its route list and option 5), the panel's addendum box, `docs/MAC_CHECKLIST.md` and the interview
folder's README read the same file, and `tests/test_session14_routes_status.py` holds them to it. Nothing in the cloud
container is a Mac result: every Mac step is pending until it is run there.

The launcher asks first: **connected** (Claude Code first) or **offline** (`TENDERPACK_OFFLINE=1`: every phase on the
local Ollama, a hosted route refused before any call, §17). `tenderpack ai ollama-models` discovers the INSTALLED
models (`/api/tags`), reads each one's capabilities and context (`/api/show`), estimates its memory at each phase's
configured context against this machine's memory, and says which phase each can serve; it never pulls a model.
Every construction site of a provider or host session in `tenderpack/` is enumerated by
`tests/test_session13_mac_scripts.py`, which fails when a new one appears without the offline guard.

All four use the same request layer and the controller's validation (tested in
`tests/test_session12_offline.py::test_every_route_applies_the_same_validation_to_the_same_answer`).

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
    --tools "" --allowedTools "<exactly the phase's tools, e.g. mcp__tenderpack__get_unit,...,mcp__tenderpack__submit_proposals>" \
    --disallowedTools "<every other tenderpack tool>" \
    --permission-prompts none --no-session-persistence \
    --output-format stream-json --verbose --max-turns 40 --system-prompt "<policy.compose(phase, 'host')>" [--model M]
# mcp.json names one server: <repo>/.venv/bin/python -m tenderpack ai serve-mcp --evidence <abs> --pack <abs> --out <staging> --worklog <log>
#   --tools <the same list> [--submit-once --require-crops <the packet's image_targets>]     (session 13; see §19)
#   with env PYTHONPATH=<the folder> (session 13, E159: the host CLI starts the server in the session folder and ignores
#   the config's cwd; the folder on PYTHONPATH keeps `-m tenderpack` importable where the package is not installed)
# the task packet goes on stdin; a wall-clock timeout (900 s) applies
```

- **No file, shell or web tool.** `--tools ""` removes every built-in tool; the host works only through the MCP tools. `--permission-prompts none` denies anything else that would ask.
- **A session without its tools is a setup failure, never an answer (session 13, E159).** The CLI's init message names each MCP server's status and the tools offered; when the tenderpack server did not connect, or none of the session's tools is offered, the session is classified `setup` with the cause (the server's stderr from the CLI's log when it logged one), its final text is not parsed, and the request layer raises at once instead of retrying (the environment must be fixed, then the run resumed).
- **Deny-by-default (session 13).** The allow list is exactly the phase's tools (`tenderpack.ai.policy.tools`), every other tenderpack tool is disallowed by name, and the session's MCP server offers only those (`serve-mcp --tools`). The analysis session's server accepts ONE submission (`--submit-once`) and refuses `submit_proposals` until `get_crop` was called for every image target (`--require-crops`).
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

**Status: built, unverified (MCP interface tested; automated Codex execution unverified).**

- Works (tested in the cloud container): the MCP server Codex would use, over stdio JSON-RPC
  (`tests/test_session09_ai_mcp.py`), and the manual host path: `ai run ... --route host --host-manual` stops with
  exit 4 at the first batch and names its task packet; `ai submit-batch RUN FILE --by NAME --host-model MODEL`
  validates the answer exactly as any route's and continues (`tests/test_session10_workflow.py`).
- Never run: a Codex session of any kind, the `~/.codex/config.toml` registration, Codex reading the runtime prompt.
  The workflow's automatic host sessions start Claude Code (`claude -p`) only; Codex is the manual path (MCP tools,
  then `tenderpack ai submit` or `submit-batch`), never chosen automatically.

Then follow the same steps as in §2. The package is installed in editable mode, so the server finds the repository from any working directory (in the interview folder, where nothing is installed, the `.pth` link that `scripts/mac/pathlink.py` writes does the same; session 13, E159).

**What Codex is told (session 13).** The MCP server's `initialize` returns only the short host entry
(`tenderpack/ai/policy/90_host_entry.md`): it points to the runtime prompt the program supplies explicitly, which is the
task packet's `system` (`get_task_packet`, `tenderpack ai task`, and the manual reading and downstream packets of a
workflow run): `policy.compose(phase, "mcp")`, the same shared rules every route receives (§19). A person's own MCP
client is offered every tool (the writers write to staging only); program-run sessions are restricted as in §2a. A Codex-assisted review is logged like any other host session:

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

**Status: untested** (recorded responses only; no API-key call has been made from this project). Ready: the dry run
below.

**Credential.** From the environment, or (session 13, `tenderpack/ai/keys.py`) from a chmod-600
`~/.config/tenderpack/keys.env` OUTSIDE the folder; never in a file inside the folder, a chat, a log or Git:

```
read -rs ANTHROPIC_API_KEY && export ANTHROPIC_API_KEY
```

**Dry run.** This makes no paid call (one `GET` of the model's description): it checks the key and `GET /v1/models/{id}`, which gives the context window, the output cap, image input and structured outputs. If there is no key, the call fails, the model is not listed, or the reply omits `max_input_tokens` or `max_tokens`, the answer is `REFUSED: ... capabilities unverified` (§12).

```
.venv/bin/python -m tenderpack ai capabilities --route anthropic --model claude-opus-5-5
```

**A run.** It refuses to start until you set limits (`routes.anthropic.caps` in `config/ai.yaml` are null). The prices in `config/ai.yaml` are **provisional** list prices (to confirm against your console); `--max-usd` is enforced from the usage the endpoint reports, so any cost figure is an estimate until a real run reports its usage. `--max-calls` is always required. The numbers below are examples: the limits are yours to choose.

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

**Status: blocked here, unverified** (`openrouter.ai` is blocked from the cloud container; recorded responses only).
Ready for a later key: `OPENROUTER_API_KEY` in the environment (or the chmod-600 `keys.env`), the model in
`config/ai.yaml` `routes.openrouter.models.propose` (`anthropic/claude-opus-5.5`, an unverified slug), the caps in
`routes.openrouter.caps` (null until you set them), then the dry run (the `capabilities` line below; no paid call).

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

This route runs **on the Mac only** (M5 Pro, 48 GB). The cloud session cannot reach the Mac's `localhost`, and nothing assumes it can. The setup, the launcher and the offline checks are in `docs/MAC_SETUP.md`; the one-page order of the Mac steps is `docs/MAC_CHECKLIST.md`. Offline mode is §17.

**Status: pending on the Mac; prepared for local use.** Prepared and tested against a fake local server: the model roles
in `config/ai.yaml` (`routes.ollama.models`: `text`, `vision`, `critic`), the discovery of the installed models with
their capabilities and context (`tenderpack ai ollama-models`), the memory estimate against 48 GB, offline mode, and the
three check levels of `scripts/mac/checks.sh` (session 14): **level 1** connectivity (Ollama answers, the model is
installed, `/api/show` reports vision, tools and context), **level 2** valid content (one batch whose proposal set
passed the controller's validation, read from `proposals.yaml`, never from the exit code) and **level 3** complete
workflow (a whole `ai run --offline` to the candidate outputs and the review packet, read from the checkpoint; a
partial run that exits 0 is reported PARTIAL). Never run: a real local model, on any machine.

The pull commands below are a person's choice. tenderpack never pulls a model; a missing one is reported with the command.

```
ollama pull qwen3-vl:32b        # vision candidate, about 20 GB at 4-bit (published size; not measured here)
ollama pull qwen3:30b-a3b       # text candidate
ollama serve                    # default http://127.0.0.1:11434 (or export TENDERPACK_OLLAMA_URL=...)
.venv/bin/python -m tenderpack ai capabilities --route ollama --model qwen3-vl:32b
.venv/bin/python -m tenderpack ai propose ADD-03 --route ollama --model qwen3-vl:32b
```

- **Capabilities** come from `/api/show`. A task with image crops and a model without `vision` is refused, and so is a model without `tools`. A reply without a context length is refused too (the `num_ctx` bound cannot be checked), unless `--allow-unverified-capabilities` is given.
- **Models per role (session 12).** `routes.ollama.models`:
  - `text` (or `propose`): the analysis and downstream phases. `--model` overrides it.
  - `vision`: the readings.
  - `critic`: the local critic. The critic has no fallback: when none is configured, the review is recorded as skipped.
- **Installed and memory (session 12).**
  - A model that `/api/show` does not know is **not installed**. The run stops with the `ollama pull` command and the installed list (`/api/tags`).
  - The memory a model needs at `num_ctx` is estimated: weights at the reported quantisation, plus an f16 KV cache, plus 1 GB. It is compared with `routes.ollama.machine` (48 GB × an assumed 0.75). A model that cannot hold its context is refused, with the numbers.
  - The workflow checks the analysis model at start (`ollama_preflight` in the checkpoint).
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
| Ollama | adapter written; **not reachable** from the cloud. Session 12: the adapter, offline mode, the capability and memory checks and a whole workflow run were tested against a FAKE local server on 127.0.0.1 (real HTTP; recorded answers; `tests/test_session12_offline.py`). A real local model: **PENDING ON THE MAC** (`docs/MAC_SETUP.md`) |
| Codex | **MCP interface tested; automated Codex execution unverified** (no Codex session has run; the workflow starts Claude Code only) |

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

- **Where keys live (session 13: the secure configuration).** `ANTHROPIC_API_KEY` and `OPENROUTER_API_KEY` come from
  the environment, or from a private key file OUTSIDE the tenderpack folder (`tenderpack/ai/keys.py`):
  `$TENDERPACK_KEYS_FILE`, else `~/.config/tenderpack/keys.env`, lines `NAME=value`, used only when it is your regular
  file with mode 600 (`chmod 600`) and outside the folder; a file that fails this is refused with the fix, and nothing
  is read from it. Create it yourself: `mkdir -p ~/.config/tenderpack && touch ~/.config/tenderpack/keys.env && chmod
  600 ~/.config/tenderpack/keys.env`, then add the line with a text editor (not `echo`: the shell history would keep
  it). Keys are never in `config/ai.yaml`, a file in the folder, a chat, a log or Git; `tenderpack ai routes` says
  only whether a key is configured and where from, never its value.
- **A paid route also needs its caps.** `routes.<route>.caps` (max_calls, max_input_tokens, max_output_tokens,
  max_usd) are null until you set them; the route refuses to start before that, and `ai routes`, the launcher and the
  panel say so.
- **What is logged.** Every prompt (with the full task packet), tool call (with the result truncated to 4,000 characters), raw response, usage, error, overwrite and validation. Logs go to `worklog/model_calls/<run_id>.jsonl` and `staging/ai/<run_id>/log.jsonl`.
- **Redaction.** `Authorization`, `x-api-key`, `*_api_key`, `Bearer …` and `sk-…` strings, the values of the key variables and (session 13) every value read from the key file are redacted before anything is written (`tests/test_session13_mac_scripts.py` writes a key that matches no generic pattern and checks the log).
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
- **Per phase, before any call (session 11).** Every request of every phase (the analysis, the reading of an image region, the downstream phase, the critic) goes through one capability check (`tenderpack/ai/requests.py`, `require`): tool use where tools are offered; image input where images are attached, and ALWAYS for the reading phase. A reading asked of a model that does not report image input is refused before any call, never degraded to text (session 10's downstream/reading loop checked tool use only).
- **Visible on every phase.** Capabilities used under `--allow-unverified-capabilities` carry their notice into the batch's run log, the checkpoint (`batches.<id>.notices` and the run's `notices`) and the review packet's "Requests" section, whatever the phase.
- **The host route's capabilities are declared** in `config/ai.yaml` `host_session.capabilities` (image input and tool use as observed in the real host sessions of 4 Oct 2026; a context window and output cap the accounting is held to). A host's model cannot be queried by this tool, so every host request carries the route notice "capabilities declared, not verified".

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
- **Every phase carries its own schema (session 11).** The request layer sends, on every request: the proposal set (analysis); the reading answer (`regionread.answer_schema()`: `{region_id, reading, model_rationale}`, `reading` being the `readings.Reading` schema itself); the downstream set (`contract.downstream_fill_schema()`); the critic's batch of reviews (`critic.CRITIC_BATCH_SCHEMA`). Free-form objects the limits forbid (an item's payload, a table row's cells) travel as JSON strings and are decoded before the strict local parse (`structured.decode_free_form`, which follows the original schema). Session 10's downstream and reading requests carried no schema.
- **The host route** carries the schema in the packet and validates locally; the critic's and the repair's plain host sessions pass the critic's schema with `--json-schema`.
- **Ollama on tool turns.** With `with_tools: false` the schema is withheld on a turn that offers tools, and a route notice now says so (`structured_output_withheld`).

## 14. Bounded batches (session 10)

`tenderpack ai plan-batches ADD-NN [--route R --model M | --context-tokens N --max-output-tokens N] [--count-tokens]` (`tenderpack/ai/batching.py`; the workflow calls `plan_batches(provisions, capabilities, overhead) -> list[Batch]` and runs one propose per batch with a checkpoint).

- **The fit test.** A batch fits when its output is within the output cap and its input plus output is within the context window less `context_margin`.
  - Input: system, tools, the packet without its provisions, the batch's provisions and their crops, and `prior_turns_tokens`.
  - Output: `output_tokens_fixed`, plus `output_tokens_per_provision` for each provision.
- **Where the limits come from.** The verified capabilities. A plan is refused without a context window. Figures given with `--context-tokens` are labelled as a person's.
- **Nothing is dropped.** Every provision is in exactly one batch, in addendum order (`assignment`). A provision that cannot fit even alone is its own batch with `fits: false` and the note "too large: needs a person to split", with its size. The note also says when the overhead alone leaves no room.
- **Sizes are estimates.** They use 3.5 characters per token, 4,800 tokens per image crop and 700 output tokens per provision (from the blind-03 host run: 68,854 characters for 35 provisions). `--count-tokens` (Anthropic, with a key) measures the packet with `POST /v1/messages/count_tokens` and records the source on every batch.
- **Settings.** In `config/ai.yaml` `batching:`. A route may override them; Ollama sets `prior_turns_tokens: 8000` for its 32,768 bound.
- **Every request of every phase (session 11).** The same rule is applied to each request before it is sent (`batching.request_size`, through `requests.size`): system + tool definitions + the packet as sent + the images attached + the later-turn allowance (tool phases only) + the phase's expected output (`batching.expected_output`: analysis 1,500 + 700 per provision; downstream 1,500 + 900 per task; a reading 8,000; the critic 300 + 350 per item; `batching.expected_output` in the configuration), against the context window (verified; a cassette's; the host's declared one) less the margin, and the output cap. A route's own `batching` (Ollama's `prior_turns_tokens: 8000`) applies to the requests too. During the turns the conversation itself is held to the same bound; one that outgrows it fails its batch with the sizes (class `too_large`).
- **Split, or escalated: never truncated.** The analysis is planned by provision and the downstream phase by task with these sizes (each downstream group's real packet is sized), on every route. A request that still does not fit is split in two, in order (batch status `split`, parts `<id>.1`, `<id>.2`); a single provision, task or image region that does not fit alone is `escalated` with its size, for a person. The downstream packet carries every unit of `units_after` in full: `downstream.packet` shortened a unit over 4,000 characters, and the workflow restores the full text and lists the units it restored (`units_after_note`).
- **Shared context once per session.** The analysis packet moves the candidate targets' texts into one `targets` map (a target cited by several provisions is sent once; each provision lists target ids) and keeps only the batch's own provisions in the pattern drafter's reference (`requests.compact_analysis`); the critic prints the units its items cite once per request.
- **Planned by structure (session 13).** The workflow plans the analysis batches with `batching.plan_structured(provisions, batch_size, units, fits)`:
  - a structure goes into one batch: an image region with its elements (`p4-image/...`), a table with its rows and notes (`T1-3/...`), a clause with its lettered items (`3.3`, `3.3(b)`), the answers printed under one heading (`Q15`–`Q20`), the cover lines, an appendix's paragraphs;
  - linked structures join it (`structure_links`, read from the evidence only): provisions printed under the same heading, and a provision whose words or heading name a table the addendum itself prints (Appendix B, "English translation of Table 1-3", with `T1-3`);
  - a group stays whole when it fits the token budget (the request accounting above, per route), even beyond `--batch-size`; different groups share a batch up to `--batch-size`. A group that does not fit is split at its structures first, then in document order; every provision is in exactly one batch and the plan is deterministic. The run log names every batch kept whole beyond the batch size;
  - blind-06 spread the 29 elements of one image region over four batches (each session read the region's crops again). With the image estimate of 4,800 tokens per crop the region does not fit one host request (29 × 4,800 for the images alone), so it is split at the budget, not at 8.
- **Answers collected as they arrive (session 13).** With `max_parallel_sessions` N, N exchanges run at once and up to 2N batches are dispatched ahead: an answer that comes back early waits without holding a worker, and the worker takes the next batch while the run's thread waits for an earlier one. The run's thread is still the one writer: it validates and applies the answers in plan order, so the result does not depend on the arrival order (`tests/test_session13_speed.py`, shuffled arrivals). The checkpoint's `concurrency` records per phase what ran (`dispatched`, `max_running`, `busy_s`, `held_s`, `idle_slots_s`, `discarded`). A batch whose provisions are all accounted for by then starts no session.

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

**Inside the workflow (session 11).** The critic runs after each analysis batch is validated, and in the workflow's `critic` step after the downstream items are validated, on that batch's selected items only, in ONE request per batch (`critic.review_batch`; not one per item): the shared context (the addendum, the stage, the units the items cite) once, the answer `{reviews: [{item, agrees, concerns, evidence_checked}]}`. It goes through the request layer like every phase (capabilities, size, the failure classes, one bounded repair), on `critic.route` (host by default; a recorded run replays the cassette's `phase: critic` sessions, and a batch without one is `skipped` with the reason).

- **Selection, extended.** `conflicting` also selects items whose evidence contradicts another item of the set (`critic.contradictions`: the same target or row with different new words, values or parameters). Downstream items are selected by `critic.select_downstream`: removals; consequential interpretations (a row whose interpretation states a consequence; an issue for the A3 sheet); conflicts; uncertain targets (a reading of a row other than its task's row; a task the run does not have).
- **Findings.** Analysis items: `review.critic` in the batch's staged set (and the combined set), and its review request. Downstream items: `downstream/critic.yaml` (`items.<id>.review.critic`; the downstream contract has no review field) and the checkpoint's downstream items. The review packet shows each finding under its item and in a "Critic" section that says agreement is not approval.
- **Bounded and resumable.** `critic.max_items` per batch; the critic's state is on its batch (`batches.<id>.critic`: pending, done, deferred, failed, not_needed, skipped). A rate-limited critic is deferred like a batch; a resume asks only the critics not done, never a batch again for its critic, and the reviews already written stay (they are in the staged sets).
- `tenderpack ai critic RUN_ID` (outside the workflow) is unchanged: one request per item.

## 16. The run command (session 10)

One runnable, resumable workflow from a new addendum PDF and the preceding tender state to candidate A1–A5 outputs and a review packet (`tenderpack/ai/workflow.py`, with `candidate.py`, `checkpoint.py` and `downstream.py`). Nothing it does touches the real `curation/`, `config/` or `out/`, and nothing is approved, accepted, sent or published.

### The commands

```
.venv/bin/python -m tenderpack ai run ADD-04 --pdf sources/incoming/ADD-04.pdf [--route host|recorded|anthropic|openrouter|ollama] \
    [--pack config/pack.yaml] [--evidence build] [--run-id ID] [--batch-size 8] [--downstream-batch-size 12] \
    [--model M] [--cassette P] [--host-model NAME] [--host-model-alias M] [--host-manual] \
    [--stop-after STEP] [--no-background] [--no-cache] [caps as for propose] [--allow-unverified-capabilities]
.venv/bin/python -m tenderpack ai resume RUN_ID [--stop-after STEP] [--no-retry] [--from STEP]
.venv/bin/python -m tenderpack ai submit-batch RUN_ID FILE --by "Name or host session" [--host-model NAME] [--batch ID]
.venv/bin/python -m tenderpack ai run-status RUN_ID
```

- `--pack` and `--evidence` name the **preceding state**: the pack configuration as it stands and its evidence build. The PDF is the new addendum. `--out` is the staging root (default `staging/ai`); a run lives in `staging/ai/runs/<run_id>/`.
- **Exit codes:**
  - 0: the run finished (complete or partial) or stopped where `--stop-after` asked;
  - 1: a step failed, or the candidate outputs build was refused;
  - 2: refused before anything ran, or ingest found a structural failure;
  - 4: the run waits for a host submission;
  - 5 (session 11): a batch was deferred for a rate limit and the run stopped cleanly (`status: deferred`); resume later.
  - 6 (session 12): the run stopped because it cannot go on until a person acts (`status: stopped`): an image region
    has no usable reading, or the readings were escalated to a person, or the inputs changed before promotion. The
    reason says what to do, then `resume`. Before session 12 such a stop exited 0, like a finished run. A stop asked
    for with `--stop-after` still exits 0, and a structural ingest refusal exits 2.
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
   - **API and recorded routes.** A batch is also split when the context or output cap cannot take it (session 11: on every route, with the request layer's complete accounting). Each batch is one request through the request layer (`requests.converse`); the controller then validates and stages it exactly as `propose` does (`validate_set`, the freshness re-check, `write_staging` with the route notices).
   - **Host route.** A headless host session per batch (`hostsession.HostSession.run_batch`) when the host CLI is installed, unless `--host-manual`. Otherwise the run writes `batches/<id>.packet.json` and waits for `submit-batch`.
   - **Recorded route.** One cassette session per batch (`sessions:`, each matched on the batch's provisions).
3. **validation.** The items of every batch are validated as one set by `controller.validate_set`, with the controller's statuses, coverage and resolution (`ai/<run_id>-combined/`). An op whose change type the engine does not have becomes an escalation, keeping its evidence. It is never forced into a known type.
4. **downstream.** The ops and dispositions that can be promoted are dry-run together. Their impact becomes tasks:
   - every row citing a changed unit or STALE at the addendum (re-make its reading);
   - every C46 gap (a new or amended obligation without a row);
   - every clarification entry citing a changed unit;
   - the A5 activities needing those rows;
   - every escalated or contested provision, with its affected scope (units, rows, activities, clarification entries).

   The proposals for these tasks come in bounded batches as a `DownstreamSet` (`contract.py`): `row_reading`, `row_new`, `issue`, `clarification_item`, `evidence_item`, `activity` (its duration a PROVISIONAL ASSUMPTION), `dependency` (a relationships-file entry) and, since session 11, `no_change` (`{why}` with a verbatim quotation: the task needs nothing; never for a row task, whose STALE reading is re-made, nor for an obligation without a row). A task with no item at all is **unanswered**.

   **A new row says where it comes into force** (session 11). `row_new` carries `introduced: {stage: <the addendum>, by: <the op id, or the provision unit>, evidence: {unit, page, words}}` (`register.Introduction`). Before that stage the row is NOT IN FORCE; at it, NEW (introduced by …). A row without the field is in force from the stage its first unit is issued in, so a new row that cites a volume unit (blind rehearsal 04: `VOL-V:18.1`, issued in BASE, read at ADD-03 only) is in force from BASE and refused below with the reason. Putting the addendum's provision first in `units` is a convention, not the evidence. The packet's `row_new` tasks carry an `introduce` hint (the stage and the op).
5. **downstream_validation** (`downstream.validate`), in the candidate, against the state the promotable ops produce:
   - the register's own checks at **every stage** of the candidate, not only at the addendum (session 11): quotes verbatim in the effective text of each stage where the row is in force, the consequence class with its quote, the `introduced` claim (the op applied at that stage or the provision that addendum's; the words printed there, new at that stage, in the introducing provision, a unit its op changed or names, or a unit of the row; no reading made earlier), date rules that parse and whose words are in their unit, ids new and absent from the ledger. A problem the proposals add at any stage holds the item back (`insufficient_evidence`), and the item's `stages` record lists its status at each stage;
   - `clarify.check` on the candidate register;
   - the schedule checks (C40, C44, C45) with the proposals, at the addendum and at every earlier stage where a proposed row is in force;
   - `relationships.validate`.

   **Interactions.** A reading of a row an op makes REMOVED or DELETED is invalid. A new row whose units are not in the effective text is invalid. An activity needing a row that is neither existing nor proposed is invalid. An item depending on one that cannot be promoted is held back. A `no_change` on a row task or a C46 task is invalid.

   **Statuses.** Rows, readings, activities, relationships and `no_change` answers are never above `interpretation_pending`. A question is forced to `draft, not sent`, and a relationship to `proposed`, with the overwrite recorded.
5a. **critic** (session 11): the selective critic over each downstream batch's selected items (one request per batch), and any analysis batch whose critic is still pending or was deferred (§15). It changes no status.
6. **promotion**, into the candidate only:
   - **validated again first** (session 11): the candidate is reloaded and its inputs' bytes compared with the state identity (`Workspace.check_fresh(deep=True)`); the COMBINED set, the ops and dispositions (`controller.validate_set`) and the downstream items (`downstream.validate`), is validated again against it. A set made against another state (an input edited after validation: the register, a reading, the relationships, ...) is STALE: nothing is promoted and the run stops with the differences (`steps.promotion.refused`, `stale`). A status that differs from the recorded one is listed (`steps.promotion.revalidated`) and the staged files are rewritten, so what is promoted is what was validated now;
   - the op file: the promoted items PROPOSED, origin `assistant`; every other provision `unresolved` with its reason;
   - new rows (`register/rows/<ADD>-ai.yaml`) and re-made readings, by row id through the YAML structure (session 11): a row is found by loading every file `register.load_rows` reads, never by matching text or indentation, and updated in place of its own node (the file's other rows and comments kept; the result reloaded and compared). A row id that another file holds is never written again; a `replace_requirement` is applied only when the row's requirement is the `old` given;
   - issues, evidence items, templates and lead times (the files' own leading comments kept);
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

### Execution, completeness and approval: three separate records (session 11)

The run's status is `complete` only when its **completeness** is complete (`workflow.completeness`):

1. every provision is answered by a promoted op or disposition (none `unresolved` in the candidate op file);
2. every downstream task is answered by a promotable item, and every downstream batch ran (`done`): a task with no item is listed as unanswered, one whose items are all escalated, insufficient, invalid, conflicting or held back as answered only by items that cannot be promoted, a failed or deferred batch with its error and its tasks;
3. check-register on the candidate is clean (exit 0, no finding; the C46 findings are listed);
4. the candidate outputs were published (built, exit 0, not refused).

Otherwise the run is `partial`, and every reason is given (the status line, the checkpoint, the review packet). The checkpoint keeps three records apart, rewritten at the end of every drive:

- `execution`: what ran: each step's status and the batches of each phase by status;
- `completeness`: `{status, reasons, provisions, downstream {tasks, answered, unanswered, unresolved, batches_not_done, no_change}, check_register {exit_code, findings, by_kind, c46}, outputs {published, refused, reason, exit_code}}`;
- `approval`: always `none` from the run (it approves, accepts and sends nothing), with the decisions a named person has recorded in the candidate's decisions file listed by name, if any.

The review packet opens with the same three, and `ai run` / `ai resume` print `completeness` and `approval` in their summary. A complete run is still unreviewed: completeness is not approval.

### The checkpoint (`runs/<run_id>/checkpoint.json`, format `tenderpack-ai-run/1`)

It is rewritten atomically after every change. It holds:

- `settings`: what the run started with; `resume` reuses them;
- `inputs`: the PDF's path, sha256 and pages; the preceding pack and evidence build; and the sha256 of every real input copied, used to report anything another process changed during the run;
- `steps`: the status, start, finish, attempts and wall-clock seconds of each step, with each step's own detail (exit codes, counts, the refusal reason);
- `batches`: phase, provisions or tasks, status (`pending` / `running` / `waiting_for_host` / `done` / `failed` / `skipped` / `interrupted`), attempts, the staged controller run, the recorded session or host session, and seconds;
- `provisions`: per provision, `pending` → `proposed` → `validated` (or `unaccounted` when its batch answered nothing for it), with the history, items and statuses, and `accounted_by` for content of another item's op;
- `structure`: the units that are not provisions;
- `downstream`: per task and per item (`proposed` → `validated`);
- `interventions`, `usage`, `events` (started, resumed, a stale lock taken over);
- `execution`, `completeness`, `approval` (session 11): the three separate records above.

**The state identity** (`contract.StateIdentity`) a proposal, a calculation and every staged set are bound to covers, besides the pack id, the evidence build, the stages, the decisions, the assumptions, the activity templates, the readings and approvals, the earlier amendment files and unrecorded crops (session 10), the curated inputs the register reads (session 11): `register_sha256` (rows.yaml, every row file its `include` names, pins.yaml), `relationships_sha256` and `curation_sha256` (the issues and per-document issue files, the dispositions, the evidence items, the clarification register, the row-id ledger, the scenarios). A set made before any of them changed is STALE.

### Resumption

`resume` skips what is done and never asks twice:

- a provision that is not `pending` is not asked again;
- a batch whose result was received is not re-run;
- a batch that failed or was interrupted is asked again, and the steps after it are recomputed from the candidate as it was before promotion. `--no-retry` keeps failures as they are;
- a batch `deferred` for a rate limit (session 11) is always asked again, even with `--no-retry`; a critic deferred or failed is asked again alone, its batch is not.
- `--from STEP` (session 11) reruns that step and every later one even when they are done, for a run made before a code change (the pre-promotion candidate is restored when the step is at or before promotion); batches that succeeded are never asked again, and `--from` does not by itself ask a failed batch again (that is `--no-retry`'s decision). The resumed event records `from_step`. A set made against another state identity is still refused at promotion (STALE): `--from` cannot promote proposals the current bindings do not cover.

The run lock (`run.lock`) lets one process drive a run. A lock whose process is dead is taken over by `resume`, and the takeover is recorded in `events`.

**Kept answers (session 13).** A host analysis session that reached `submit_proposals` has a set the controller staged and validated; it is no longer lost to what happens after:

- the MCP server of a workflow batch writes the submission (run id, status, staging folder) at once to `batches/<batch>.submission.json` (`serve-mcp --submission-record`);
- a session that submitted and then hit a 429 or another failure is a completed answer: the set is taken, the failure recorded with the note "after the submission", and a 429 still pauses the other workers (`requests.call_host`);
- after an interruption (SIGTERM, a crash), `resume` REUSES the recorded set after revalidating it against the current evidence and state (`controller.validate_set` and the freshness re-check, as for a new submission). The checkpoint records the staged set's folder and the validation result (`submission`: `run_id`, `staging`, `set_status`, `statuses`, `reused`, `revalidated`, `statuses_at_submission`; event `submission_reused`). It is not reused, and the batch is asked again with the reason (`reuse_refused`, event `submission_reuse_refused`), when the record or the set does not load, the set is stale, malformed or failed, the state identity changed since the submission, or an item is invalid now that was not then;
- a session stopped before its submission left no record: the batch is asked again.

**SIGTERM (session 13).** A SIGTERM is handled like Ctrl-C: the running step and batch keep their elapsed time (status `interrupted`; the step timer no longer shows "0.0 s running"), the batches in flight are marked interrupted, the host sessions still running are stopped (`hostsession.terminate_live`), and the event `interrupted` names the signal.

**Timing from data.** `python scripts/bench_workflow.py --from-run RUN_ID` prints a run's per-step, per-batch and per-session timing from its checkpoint, run log, session records and MCP server logs (steps' sum, segments, sessions started, context tokens, the fixed overhead per host session, concurrency). `--simulate` runs the same recorded run at `max_parallel_sessions` 1, 2, 3 with simulated latencies (`--rate-limit` adds a recorded 429); it measures the mechanism, not a host.

### Consecutive addenda: `--base-run` (session 12)

`ai run ADD-04 --pdf PATH --base-run RUN_ID` starts the run's candidate from another run's candidate instead of the real curation (`candidate.base_run`, `candidate.create(base=...)`): everything `PACK_PATHS` names is copied from the base candidate as it lays it out, and the base addendum's PDF is copied into this candidate's `input/` (same sha256), so the base addendum is the previous stage (`Workspace.prev_stage`) and the ops apply in number order as always. The base must have reached promotion and must not be driven by a live process (its `run.lock`); it is read, never written, and `--pack`/`--evidence` are refused with it (the base candidate's pack and evidence build are used). The state identity gains `base_run` and `base_candidate_sha256` (the base candidate's pack, every file it names and its build manifest, hashed when the identity is computed), so a change to the base makes the run's sets STALE and promotion refuses, like any other input. `out-before` is built from the base candidate's state and its evidence build (its cache key includes the base run and its fingerprint), the `diff` step compares base addendum → new addendum, and `settings.base_run`, `run-status`, the review packet and the candidate `README.md`/`CANDIDATE.md` name the base. `resume RUN_ID --base-run BASE` confirms the base recorded at the start (another is refused) and re-checks it (still promoted, not running; a changed fingerprint is recorded as `base_checked`). Validation, the critic, promotion (into this run's candidate only), the partial A3/A5 and the per-addendum locks are unchanged. A run whose addendum skips addenda the state does not hold records `settings.missing_addenda`; an unanswered provision that cites one ("Addendum No. 3", or a unit id of ADD-03 in its items) is unresolved with "ADD-03 is not in this state; run it first or pass --base-run". Tests: `tests/test_session12_consecutive.py`.

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

### The request layer and the three failure classes (session 11)

Every model request, whatever the entry point (the workflow; the standalone `tenderpack ai propose`, whose set is `deferred` after a rate limit outlasts the backoff, exit 1 as before; `tenderpack ai host-session`, which reports `failure_class` and `deferred`), the phase (readings, analysis, downstream, critic) and the route (recorded, anthropic, openrouter, ollama, the headless host, the manual host path), goes through `tenderpack/ai/requests.py`: the phase's schema (§13), the capability check (§12), the complete size (§14), then the failure policy (`config/ai.yaml` `failures`). Three failures, handled differently:

| Class | What it is | What happens |
|---|---|---|
| `rate_limit` | HTTP 429; a provider's rate-limit error; the host CLI's plan limit (`api_error_status` 429; blind-04: "You've hit your session limit · resets 4:30pm (UTC)") | bounded exponential backoff with jitter (30, 60, 120, 240 s, ±20 %; `max_tries` 4); a reset the provider names is waited for when within `honour_reset_up_to_s` (300 s), else the batch is deferred at once. Then the batch is **`deferred`**, never failed: the run stops cleanly, exit 5, everything done so far checkpointed (`on_deferred: stop`), or goes on (`continue`: later requests in the same drive get one try each, no backoff). `resume` asks the deferred batches again |
| `provider` | 5xx, 529, timeouts, connection errors; a host CLI that cannot start, times out or ends without a result | bounded retries (API routes: the run's `retries`/`backoff_s`; the host: one retry), then the batch **fails** (resume asks it again) |
| `malformed` | an answer that does not parse, fails its schema, or breaks a reference (an item's `statements` must be ids of the set's statements, never free text; a downstream item answers a task of its packet; a review names a requested item) | ONE re-ask carrying the validation errors: the same conversation on a provider route, a plain no-tool session given the answer on the host route, the submitter on the manual path (the submission is not taken; the batch keeps waiting). An item that still fails its schema after it is set aside **item by item** (`malformed_items`; the batch keeps its good items); an item whose only problem is a reference is kept and rated by the controller's own checks (an unknown statement is `insufficient_evidence`, with the reason), so nothing a person could read is dropped; an answer that is not a set at all fails the batch. A host session that ended with no answer at all is not "repaired" from nothing: the batch fails and resume asks it again |

**Batch states** (checkpoint): besides `pending`, `running`, `waiting_for_host`, `done`, `failed`, `skipped`, `interrupted`: `deferred` (with `deferrals`: when, the message, the reset named), `split` (with its `parts`), `escalated` (with its `size`). Each batch records its `failure_class`, every failed call (`failures`: class, kind, status, wait), and `request` (the size, the repair, the malformed items, the usage, the route notices). The review packet lists them under "Requests: failures, deferrals, repairs and route notices".

**Fewer and smaller sessions.** By default, batches run one at a time (`concurrency.batches: 1`; another value is refused: concurrent sessions do not lift a plan's rate limit, they reach it sooner). Session 12 adds bounded batches at once on the host route, `concurrency.max_parallel_sessions` (§18). After one deferral in a drive, later requests are tried once and deferred without backoff. The shared context is sent once per session (§14), the critic makes one request per batch (§15), and a batch that succeeded is never asked again.

**What is tested, and how** (`tests/test_session11_requests.py`; every exchange recorded or mocked):

| Route | Through the request layer | Evidence |
|---|---|---|
| recorded | analysis, reading, downstream, critic; 429 → backoff → deferred → resume asks only the deferred batch, the critic's findings survive | workflow cassettes (`workflow_add03.yaml` + `s11_workflow_critic.yaml`); hand-written, not a model |
| anthropic | downstream with native `output_config.format` (the downstream schema, payload as a string, decoded); `--allow-unverified-capabilities` notice in the log, checkpoint and packet | HTTP cassettes replayed through the real adapter; **no live call** (no key) |
| openrouter | downstream with `response_format` json_schema | HTTP cassette; **unverified live** (openrouter.ai blocked here) |
| ollama | downstream, `format` withheld on a tool turn with a notice, the route's 8,000-token later-turn allowance | HTTP cassette; **unverified live** (the Mac) |
| host (headless `claude -p`) | analysis over MCP; answer sessions; the plain repair session; the batched critic; the plan's 429 result → backoff / deferral; the reading phase refused when the declared capabilities have no image input | a recorded stand-in for the CLI (`tests/fixtures/ai_cassettes/fake_claude_s11.py`, not a model); a real headless session is recorded in the session 11 work log |
| manual host (`submit-batch`) | the answer's checks before anything is taken | session-10 workflow test |

**Taking anything over.** Nothing is applied to the real curation. A person adds the PDF to the pack (OPERATING_GUIDE §3 steps 1–2), reviews and copies the files `promotion.json` lists, then runs `pin`, `check-register` and `outputs`, and decides with `accept` / `reject`.

## 17. Offline mode (session 12)

Use offline mode on the owner's Mac, with no internet and no key. It is on when **any** of these holds:

- `--offline` is passed to `ai run`, `resume`, `propose`, `capabilities`, `critic`, `plan-batches` or `routes`;
- `offline: true` is set in `config/ai.yaml`;
- `TENDERPACK_OFFLINE=1` is set. The Mac launcher and `scripts/mac/checks.sh` set it.

The source is recorded in the run's settings and its `started` event.

```
.venv/bin/python -m tenderpack ai routes --offline                      # kinds; local models checked now; nothing pulled
.venv/bin/python -m tenderpack ai run ADD-03 --pdf PATH --offline       # --route defaults to ollama offline
.venv/bin/python -m tenderpack ai resume RUN_ID --offline               # an ollama run kept offline from now on
.venv/bin/python -m tenderpack ai critic RUN_ID --offline               # the local critic, or refused
```

What it forces (`tenderpack/ai/offline.py`):

- **Every phase on `ollama`.** That covers the readings, analysis, downstream, the critic, the bounded repair (on a
  provider route the repair is a turn of the same conversation) and the capability checks.
- **Hosted routes refused before anything starts.** `--route host|anthropic|openrouter` raises an OfflineError (a
  ConfigError, exit 2) before the run folder exists. The recorded route stays a test replay and is never a fallback.
- **Guards at every hosted entry point.** Each one refuses in offline mode **before** its process or connection:
  - `providers.make` for `host`, `anthropic` and `openrouter`;
  - every host session (`HostSession`, `AnswerSession`, `PlainSession`);
  - the host critic (`HostCritic`, `review_batch(route="host")`), with the message "offline mode: the host critic is
    not available; configure routes.ollama.models.critic or accept a skipped review";
  - the host repair (`requests.host_repair`).
- **Local address only.** The Ollama URL must be a loopback address, and a loopback URL is never sent through an HTTP
  proxy (`providers/base.http_json`).
- **The critic.** It runs on `routes.ollama.models.critic`; `critic.route` (host by default) is not consulted offline.
  - When no local critic is configured, or it is not installed, or it cannot hold the request (capabilities, context,
    memory), the batch's critic is **`skipped`** with "independent review did not run: <reason>".
  - The reason appears in the run log (`critic_skipped`), the checkpoint, the review packet ("Reviews that did not
    run") and the candidate `out/README.md` ("Independent review").
  - A skipped review is never counted as agreement, and a review was never needed when no item was selected.
- **Readings without vision.** When the reading model (`models.vision`, else the run's model) does not report image
  input, or is missing, the readings step is "cannot run locally with this model":
  - the image regions are **escalated to a person** (batch status `escalated`, the event
    `readings_escalated_to_person`), and nothing is asked of the model;
  - ingest refuses the candidate without these readings (C05), so the text phases cannot start, and the run stops
    with the way on: record the readings and `resume --from ingest`, or configure a vision model.
- **Not offline: an `ollama` run with a hosted critic.** Outside offline mode, an `ollama` run whose `critic.route` is
  hosted logs `critic_route_notice`, so the hosted call is visible.

**What is tested, and how.** `tests/test_session12_offline.py` uses a fake Ollama server on 127.0.0.1 (real HTTP),
replaying the hand-written recorded workflow. A guard records every socket connection and every process, and refuses
anything except the fake's port, and any `claude` or `codex` process. The tests show:

- a whole workflow run to the critic, with only localhost contacted;
- the local critic reviewing the selected items on the configured model;
- the same statuses as the recorded route;
- hosted routes and processes refused before any call;
- the skipped review with its reason;
- not-installed and oversized models refused with the exact text;
- readings escalated when the model has no vision;
- `ai routes`;
- the same validation outcome on the anthropic, openrouter, ollama and host routes.

PENDING ON THE MAC: all of the above with the real Ollama and the models actually installed, with Wi-Fi off
(`scripts/mac/checks.sh`). A recorded answer is a test, not proof of a live integration.

## 18. Time: less repeated context, batches at once (session 12)

Blind-05 took 72 min 27 s. The steps of its run (`staging/ai/runs/ADD-03-run-host-blind05-20261005T025444Z`):

| Step | Time | What ran |
|---|---|---|
| analysis | 2,676 s | 9 MCP host sessions of 112–358 s each (about 60 s fixed plus about 35 s per provision); 9 plain critic sessions of about 12 s |
| downstream | 1,260 s | 5 answer sessions (77–438 s) and 1 repair |
| readings | 209 s | 1 session |
| critic step | 66 s | 5 plain critic sessions |
| everything else | about 135 s | |

The time is model turns. The prompts are a small part of it.

**Less repeated context** (`requests.compact_shared`, applied to every analysis and downstream packet on every route):

- the packet's `tools` are now names only. The definitions already come with the request: the MCP tool list, or the
  API's `tools`.
- the `schema` and `payload_schemas` lose their generated `title` strings.
- every `$defs` entry is printed once, in `schema_defs`.

The batch's own provisions, targets, tasks, units and evidence are byte-identical. The schema sent natively and the
local validation are unchanged.

Measured on blind-05's 15 prompts, as sent (the script is in the session-12 report):

- total: 538,853 → 461,551 characters, −14.3% (about 154k → 132k tokens at 3.5 characters per token);
- analysis prompts: −17.5% to −22.2% each;
- downstream prompts: −8.2% to −14.0%;
- the reading prompt: −4.3%.

**Batches at once** (`concurrency.max_parallel_sessions`, 1–4, default **1**). Up to N analysis or downstream batches
of one run ask their sessions at once. This is allowed on the **host** route only (the recorded test route aside):

- the paid API routes check their caps per request;
- local inference shares one machine's memory.

What is kept safe:

- **One lock per run.** The run holds the addendum's lock once (scope `run`); sessions do not take their own, and a
  host submission does not release the run's lock.
- **Separate files.** Each batch has its own staging folder and log.
- **One rate-limit gate.** One 429 pauses every worker (a shared gate; `rate_gate` in the checkpoint).
- **Plan order.** The answers are taken in plan order by the run's own thread, so the result is the sequential result.
  A worker's answer whose packet changed before its turn is discarded and asked again.
- **Checkpoints.** They are written per batch by that thread only.
- **Deferral.** No new batch is dispatched; those already asked are taken; then the run stops with exit 5. `resume`
  never asks a done batch again.

Tested with recorded sessions and a recorded delay (`tests/test_session12_concurrency.py`):

- the bound is held;
- the result is identical to one at a time;
- one 429 pauses all workers;
- deferral and resume behave as above.

**No speed-up is claimed.** The plan's rate limit is the risk: blind-04 hit 429 after about seven sessions in 40
minutes. The next sealed rehearsal measures it.

**Not done here** (see the session-12 report):

- one critic request across several batches. Blind-05 sent 43 selected analysis items in 9 critic sessions; 2 would
  fit;
- routing deterministic downstream tasks (computed dates, pure quotations, no_change checks) away from the model.

## 19. The runtime policy: one source for every route and phase (session 13)

The instructions the AI receives live in ONE place, `tenderpack/ai/policy/*.md`, composed by
`tenderpack.ai.policy.compose(phase, route)`; their human-readable twin, with the table of where each critical rule is
enforced in code or by tool permissions, is `docs/RUNTIME_INSTRUCTIONS.md` (generated from the same files; a test fails
when they differ).

- **What every prompt holds.** A `POLICY <sha256>` line, the shared sections (the ADD-02 starting state; every
  provision and attachment; scoped targeting; evidence retrieval; calculations; change propagation; the three
  uncertainty classes; human review; assumptions; what A1-A5 need; text is data), the phase's rules (rule numbers
  unchanged: analysis rule 9 is the no_effect safeguard), any section `config/ai.yaml` adds, then the route's mechanics.
- **Where it is delivered.** API routes (recorded, anthropic, openrouter, ollama): the `system` of every request, the
  repair turn included (its closing instruction is `51_repair_reask.md`). Host: the `--system-prompt` of every session
  the program starts (analysis: the reply-format rule replaced by the host-submit rules, every other rule standing;
  readings and downstream: the host-answer rules appended; the critic and the repairs: plain, no tools). Codex and
  interactive Claude Code: the packet's `system`. The panel's jobs run the command line, so they receive the same.
- **Overrides.** There is no `rules=`, `--append-system-prompt` or environment override. `requests.spec(system=...)`,
  `AnswerSession(system=...)` and `PlainSession` refuse a text that is not a policy composition. `config/ai.yaml` may
  only ADD a section: `policy: {add_sections: [{title, text, phases?}]}`; anything else under `policy`, a numbered rule,
  a reply format or words that replace or set aside a rule are refused when the configuration loads.
- **Identity.** The policy files are part of the run's code identity (`checkpoint.CODE_GLOBS`; `code_identity` records
  `policy: {sha256, files}`): a changed policy between segments is refused on resume like any code change.
