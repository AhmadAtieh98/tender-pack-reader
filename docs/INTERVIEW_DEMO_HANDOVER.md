# Interview demo: implementation handover

> **Live-result update, 15 October 2026:** the actual ADD-03 run completed all 13 steps after timeout/resume and remains PARTIAL. See the [published result and review actions](../staging/ai/runs/ADD-03-run-host-20261015T131927Z-745a/README.md) and [before/after output diff](../staging/ai/runs/ADD-03-run-host-20261015T131927Z-745a/OUTPUT_DIFF.md). Its primary candidate A3 is HTML; the live one-page candidate PDF fit failed. The timings, counts and one-page success below describe earlier rehearsals, not this live result.

## Current state

The application has a prepared ADD02 interview profile, a signed-in Claude Code host route (the interview default), the signed-in Codex host transport (kept as a second profile) and an incremental ADD03 workflow. Demo approvals are explicitly labelled and editable. A partial result remains partial when evidence or interpretation is missing. The normal source pack and its approval files have not been changed.

The implementation was developed from `509be48`. Code, tests and reproducible preparation scripts are included in this revision. Generated operating folders, model exchanges, historical run outputs and private conversation records are not included. Worklogs are not updated by this revision. This document is the technical continuation entry point for Claude Code and other coding agents.

## Run from a fresh checkout

Create a Python 3.11+ environment and install the locked dependencies. With uv available:

```sh
uv sync --frozen --extra dev --no-install-project
.venv/bin/python scripts/prepare_interview_demo.py /absolute/path/outside-checkout/interview-release
```

The default host is Claude Code (`config/interview-ai.yaml`). `--host codex` prepares the Codex profile instead (`config/interview-ai-codex.yaml`); both profiles share the interview, batching, concurrency and failure settings.

Use an absolute destination outside the source checkout. Preparation creates a portable folder and zip, ingests the baseline, enables the explicit demo profile, builds ADD02 outputs and freezes their hashes. It does not change source curation. In the generated folder:

```sh
bash scripts/mac/setup.sh
.venv/bin/python -m tenderpack interview verify
.venv/bin/python -m tenderpack panel --open
```

On macOS, `INTERVIEW_START.command` handles setup and opens the panel. `RESTORE_ADD02.command` verifies and restores the frozen baseline while retaining prior run/history files. Restoration and decision editing refuse while a run is active.

At Home, verify validated ADD02 and no working stage. Open the existing A1–A5 files, then upload only ADD03 with the host route selected. The Claude Code profile requires the `claude` CLI on PATH, signed in (`claude auth status`), at a version that accepts `--permission-prompts` and the configured model (2.1.206 rejected both; 2.1.296 worked; `claude update` updates it), and network access. The Codex profile requires an installed, signed-in Codex CLI. The chosen profile is copied into the operating folder as `config/ai.yaml`. Start the panel from an ordinary terminal or the launcher: a host CLI started from inside another Claude Code session inherits that session's environment and could not authenticate here. Check the available model/configuration on the intended machine; configured identity is distinct from the model identity actually reported at runtime.

The interview profile has two total concurrent host sessions, six-item analysis/downstream batches and a 2,700-second overall guard. The guard is a limit, not a runtime promise. Resume interrupted work from Runs or with `tenderpack ai resume RUN_ID`. Preserve its checkpoint and evidence. Do not bypass the code-change check to conceal a mixed-version benchmark.

## Implementation map

| Area | Main files | Behavior |
| --- | --- | --- |
| Demo preparation and recovery | `scripts/prepare_interview_demo.py`, `tenderpack/interview.py` | Freeze/verify/restore ADD02; explicit simulated reviews; atomic validated rebuilds; reversible decisions and planning edits. |
| Claude Code transport | `hostsession.py` | `claude -p` with only the phase's tenderpack MCP tools (`--tools ""`, `--strict-mcp-config`, `--permission-prompts none`), the configured model and `--effort`; a CLI that rejects its command line is a named `setup` failure. |
| Codex transport | `tenderpack/ai/codex.py`, `hostsession.py`, `cli_routes.py` | Phase-scoped MCP, native-event normalization, transport image validation, compatible schema handling, bounded repair, and configured/reported identity separation. |
| Incremental execution | `workflow.py`, `checkpoint.py`, `requests.py`, `tools.py` | State-bound answer reuse, compact shared state, bounded concurrency, context sizing, dry-run validation and correct resume dispatch. |
| Downstream context and promotion | `downstream.py`, `contract.py` | Current row/issue/review records, A5 requirement mapping, submission-scoped predecessor context, relationship closure and consistent shared-activity replacement. |
| A3 and unresolved reach | `partial.py`, `stage2.py`, `render.py` | Possible unresolved targets flag affected outputs; candidate one-page briefing retains identifiers and abbreviated reasons with full linked detail. |
| A5 | `programme.py`, `schedule.py` | Generated requirement-linked programme/marshalling, backward working-day calculation, explicit assumptions, interpretation gates, infeasibility and resource warnings. |
| Panel and review state | `panel/server.py`, `panel/views.py`, `review.py`, `human_owned.py` | Editable demo decisions, planning controls, retained history, visible critic disagreements and safe inline PDF links. |

AI filenames in the table are under `tenderpack/ai/`. Other runtime files are under `tenderpack/`.

## Important fixes and invariants

- A3 tries one- and two-column issue layouts before sacrificing reason text. Candidate condensation stops at level 2; issue excerpts link to full detail. Excessive content still returns an explicit fit failure. The full candidate diagnostic remains available. The validated ADD02 A3 is not replaced by an unvalidated ADD03 candidate.
- Inline generated PDFs resolve relative detail links against the current loopback panel URL. Downloaded PDF bytes and source tender PDFs remain unchanged. Safari PDF links work; use HTML detail if the embedded PDF viewer is blank. Excel opened the eight-sheet A1 workbook without repair.
- A packaging task reached through EV-DELIVERY receives the actual shared activity's A5 requirement IDs and evidence associations, including EV-COPIES. Direct-input context includes submission/forms requirements, without expanding an assembly task into all technical and contract clauses.
- An activity ID is global in A5. Editing a shared activity updates every existing evidence association identically in validation and candidate promotion. It cannot silently add a new association. The previous one-association update caused C45 for copies.
- Relationship proposals whose endpoints/issues are not promotable are held back rather than introducing dangling references. Current reviews retain their status and demo origin; accepting an open issue does not resolve it.
- Codex transport diagnostics must not fabricate image bytes, evidence, handling instructions or model identity. Keep malformed-image and bounded-repair regressions when changing the transport.

## Verification evidence and boundaries

The final local package passed 109 focused tests in 27.37 seconds, setup 10/10, smoke 9/9 and all eight package-verification groups. The final archive had 1,215 hash entries and eight executable scripts. Runtime Python matched the source. A later empty-register test-fixture correction changed no runtime code; the re-exported archive's inventory, hashes and executable bits were checked again.

Source verification included 35 context/A3/partial-output tests and a final 12-test scoped-context suite. A broader downstream suite produced 29 passes plus two failures: a code-identity guard correctly detected a concurrent source edit, and an old minimal fixture lacked its empty `evals` collection. Both cases passed on recheck with source held constant and the fixture completed. This does not claim a rerun of the entire historical suite.

Useful commands from the source environment:

```sh
.venv/bin/python -m pytest -q tests/test_session18_context_layout.py tests/test_session18_pdf_view.py tests/test_session16_downstream_context.py tests/test_session17_audit.py
.venv/bin/python -m pytest -q tests/test_session15_interview.py tests/test_session15_demo_decision_guards.py tests/test_session15_planning_editor.py tests/test_session15_codex_runtime.py tests/test_session15_host_repair.py
```

For a freshly created archive, `scripts/mac/verify_package.sh ARCHIVE.zip --into FRESH_DIRECTORY --no-ai` unpacks and runs checks in a disposable copy. It may need normal access to the dependency cache. Do not execute the underlying Mac checks in the source worktree.

The full unchanged v4 rehearsal took **1,203.975 seconds (20:03.975)** including deliberate SIGTERM and resume. All 13 steps completed; completed analysis/downstream batches were reused. The result remained PARTIAL: 10/12 provisions and 33/38 downstream tasks had promotable answers, with zero register errors. It used a disclosed two-page synthetic fixture. The final implementation includes subsequent fixes; it has not had another full timed AI run. The earlier 15:27.513 observation belongs to a different version. Neither is a speed guarantee for an unseen addendum.

A focused packaging check took 98.612 seconds and exposed the shared-activity defect. Revalidating its saved answer after correction produced no state, schedule or register errors, while genuine missing instructions remained conflicting. No proposals from that focused check were promoted. Seven scoped batches fit the configured context estimate: maximum input 113,137 tokens, input plus reserved output 120,037, declared usable limit 180,000. These are estimates and declared capabilities, not independently measured model limits.

Panel duration edit/restore and approval rejection/restoration succeeded in 8–10 seconds per rebuild without AI calls. Changing five to six working days moved the affected latest start one working day earlier; restoration reversed it. All reversals remained in history. Only a disposable rehearsal candidate was edited.

## Claude Code host route: observations

Observed on 11 Oct 2026 on the development Mac with Claude Code CLI 2.1.296 (claude.ai sign-in), the interview profile and the drill ADD03 (`build/drill-src/ADD-03_Addendum_No_3.pdf`, two pages, 12 provisions) in a disposable probe copy:

- Tools: each analysis session's init listed exactly the ten tenderpack analysis tools and the tenderpack MCP server as connected; no built-in file, shell, web, agent or skill tool was offered. The CLI's skill and slash-command lists are not tools and cannot be invoked without one.
- Page and image access: both analysis sessions fetched the image-only VOL-II Table 2-4 with `get_crop`; the crop PNG the model received had the same SHA-256 and size as the file the server sent. The drill ADD03 has no addendum image region, so the reading phase made no call.
- Model identity: requested `claude-opus-5-5`; the CLI reported `claude-opus-5-5` in both its init message and `modelUsage` (context window 1,000,000, maximum output 128,000 as reported by the CLI). The profile keeps a declared 200,000/32,000 bound for request sizing.
- Bounded repair: one plain no-tool session turned a non-JSON critic answer into JSON that validates against the critic batch schema in 13.7 s; without evidence in the repair turn it disagreed rather than inventing support.
- Resume: a SIGTERM during promotion saved the checkpoint as stopped (the signal is re-raised, so the process prints a traceback and exits 1); `tenderpack ai resume` completed the run without asking any host session again.
- The probe run (code before the session-19 changes, which affect only `--effort` and failure naming) took 894.5 s of step time and ended PARTIAL: 2 provisions unresolved (6.1, 7.1) and two register defects of kind `pending_settled` in model-written issue text, both left visible.

### Timed ADD03 run on the Claude Code route (current code)

The demo was prepared with `scripts/prepare_interview_demo.py` (default host, Claude Code); `interview verify` reported no problems and `verify_package.sh --no-ai` passed 8/8 (109 focused tests, setup 10/10, smoke 9/9). The ADD03 run used a disposable unzipped copy of that archive, its panel started from an ordinary terminal and the drill ADD03 uploaded to `addendum/start` with route host (the panel added the interview profile's batch sizes and its 2,700 s guard). Code identity `e6b203db2c8f…` over 103 files in one segment, base `cbe0e94`; no edit to runtime code during or after the run.

- Upload to review packet: **1,234.1 s (20:34.1)**, under 30 minutes; the guard was not reached and nothing was interrupted or resumed. Steps: ingest 7.1 s, readings 0 s, analysis 280.8 s, downstream 789.8 s, critic 130.7 s, the deterministic steps about 25 s. The full source test suite was running on one core at the same time. A single run on a synthetic two-page addendum is not a speed guarantee for an unseen addendum.
- Result PARTIAL: 12/12 provisions accounted for, 10 settled and 6.1 and 7.1 unresolved with their reasons; 42 of 47 downstream tasks had promotable answers (5 answered only by items that cannot be promoted); register check 1 `pending_settled` defect (I-ADD03-BID-SECURITY-PERIOD, model wording), left visible. No item was approved by the run.
- Sessions: 10 tool sessions (2 analysis, 8 downstream) and 10 critic sessions; no failure, retry or repair was needed. Every tool session's init offered only its phase's tenderpack tools with the server connected; all 10 crop deliveries of Table 2-4 reached the model byte-identical.
- Model identity: configured `claude-opus-5-5`. The CLI reported `claude-opus-5-5` as the session model in every init message and on all 197 assistant messages. Its `modelUsage` also listed `claude-haiku-5-5` in every tool and critic session (tool sessions: 553,561 input and 333 output tokens in total, no assistant message), which the review packet prints as "claude-haiku-5-5, claude-opus-5-5". The host plan's own cost figure for the tool sessions was USD 12.21 (the plan's list figure, not the application's spend).

### Changes after the timed run (not measured)

The timed run above measured code identity `e6b203db2c8f…`. These later changes have not had a timed AI run:

- Reported models: a host session's `model_reported` is now the model(s) its init and assistant messages name (a plain json session: the model with the most output tokens); other `modelUsage` entries are kept in `model_auxiliary` and the review packet names them separately ("also in the host CLI's usage, with no answer turn"). Codex usage without token counts is reported unchanged.
- A3 regression from `cbe0e94`: the level-2 count-line rewrite lengthened the validated ADD-02 A3 (103 to 129 characters with one gate-note id), which then fell to level 3 and dropped every issue's reason on a source rebuild (six A3 tests failed). The rewrite now applies only when it shortens the line. The committed `out/` predates `cbe0e94` and was not rebuilt.
- `config/routes_status.yaml`, `cli_routes.py` and the route docs record the Claude Code route on the owner's Mac (11 Oct 2026) and that automated Codex runs as the host route with the Codex driver; the manual Codex MCP path is still unverified. `docs/RUNTIME_INSTRUCTIONS.md` was regenerated from the policy files.
- The demo folder was prepared again from this code (`interview verify` clean; package verification 8/8, 110 focused tests).

### Second timed ADD03 run (after the follow-up changes)

Same procedure on an unzipped copy of the package prepared from the follow-up code (code identity `5c49fbdb6064…`, one segment), with nothing else running on the machine:

- Upload to review packet: **1,161.7 s (19:21.7)**, under 30 minutes; guard not reached. Steps: ingest 7.2 s, analysis 309.7 s, downstream 715.9 s, critic 103.5 s, the deterministic steps about 25 s.
- PARTIAL: 6.1 and 7.1 unresolved with their reasons; 3 downstream tasks answered only by items that cannot be promoted (the two escalations and the ADD-01 Q1 re-read); register check exit 0 (no finding). No approval by a person.
- 10 tool sessions and 8 critic sessions, no failure or retry; only the phase's tenderpack tools, server connected; 11/11 crop deliveries byte-identical. Every session's `model_reported` was `claude-opus-5-5`, with `claude-haiku-5-5` in `model_auxiliary`; the packet reads "host sessions report: claude-opus-5-5; also in the host CLI's usage, with no answer turn: claude-haiku-5-5". Host plan cost figure for the tool sessions USD 12.39.
- Found by the run: the candidate's A3 at the validated ADD-02 state lists the run's new open issues (60 open, 29 listed) and fell to level 3, dropping every issue's reason; the first timed run did the same. The main A3 now tries two issue columns at each level-2 step before level 3 (`stage2.a3_pages`, `stage2.fit_a3`; the candidate briefing uses the same order). Re-rendering this run's outputs with that code in a duplicate copy (`ai resume --from outputs --allow-code-change`, no model call) gave a one-page A3 at level 2 in two columns. That layout change has not had a timed AI run; it affects only the deterministic outputs step.

### Live interview ADD03 run (15 Oct 2026, Claude Code route)

The interviewer's ADD-03 (19 provisions, not the practice fixture) ran on the prepared T1109Z interview folder through its panel with route host and `max_parallel_sessions`/`max_total_host_sessions` raised from 2 to 4 for that run only. Upload to review packet took 24 min 17 s with no failed, retried or deferred request; 14 tool sessions and 11 critic sessions all reported `claude-opus-5-5`. The result is PARTIAL: 2 provisions unresolved (2.2, 4.3), 2 escalated as software limitations (3.1 whole-form withdrawal; 4.1 table-row citation), register check 4 `pending_settled` findings, and the one-page candidate A3 briefing returned its explicit fit failure (18 unresolved items) with the full diagnostic kept. Nothing was approved by a person. The run, with a summary of what needs a human decision, is committed under `staging/ai/runs/ADD-03-run-host-20261015T140902Z-ab89/` (README.md there); session transcripts and prompts are not committed. The same day's rehearsal on the practice ADD-03 with the default two sessions took 23:12.0 and ended PARTIAL with 6.1 and 7.1 unresolved; the panel's AI quick review was also run once on the real host route (2 min 06 s, one session, `claude-opus-5-5`).

## A1–A5 status

- A1: 206 unique rows in the audited candidate, with source/confidence fields and JSON/CSV/XLSX exports.
- A2: six reconciliation data tables.
- A3: validated one-page ADD02; corrected candidate one-page ADD03, explicitly NOT VALIDATED, plus seven-page full diagnostic. The corrected page retained all 17 A3 requirement IDs, 30 listed issue IDs and both unresolved-provision IDs at minimum 7.66 pt, with ten-word issue excerpts and complete linked reasons.
- A4: the real repository/history and implementation. A portable operating folder is not a substitute for Git history. Current publication excludes private session artifacts and does not amend worklogs.
- A5: independent requirement-ID, mandatory-field, dependency, backward-date, marshalling lead-time and source-inventory checks passed. ADD02: 44 activities/26 items. ADD03 candidate: 42/25. Six ADD02 activities remain infeasible under assumptions; each stage has five overload periods. Bond approval, bond issue and technical proposal retain candidate interpretation blocks. Programme and marshalling CSV/JSON are the deliverables; charts are supporting views.

## Remaining work / next actions

1. Use the prepared baseline for the interviewer's ADD03. If another whole-workflow speed claim is needed, time a fresh final-version run without editing its runtime code.
2. Keep ADD03 6.1's security target/period/trigger and 7.1's replacement of already-superseded wording unresolved until there is an explicit interpretation or new evidence.
3. Keep USB placement/decryption and filename handling, Envelope B placement of audit/financing documents, form lettering and Form 4-A correction/execution instructions visible. Simulated approval cannot supply missing answers. Preserve feasibility warnings unless the actual planning assumptions change.
4. For further defects: failing regression, smallest implementation change, focused validation, then regenerate and verify a disposable demo package. Do not modify ordinary curation to force a green result.

## Existing local artifacts (not in Git)

On the development machine, paths below are relative to the source checkout's parent directory, `staging/interview-509be48/`:

- `release-v7/LAMAR-PPP-R2-INTERVIEW_509be48+wt_20261010T2047Z/`: clean ready operating folder; sibling zip.
- `s18-output-final/out/`: final deterministic rebuild of the rehearsal candidate.
- `s18-measured-out/`, `s18-measured-checkpoint.json`: preserved measured v4 result.
- `s18-audit.json`, `s18-final-audit.json`: original and rebuilt independent data checks.
- `s18-context-native/`: isolated focused check and deterministic revalidation; its private exchanges stay local.

These paths are optional local evidence. A fresh clone must regenerate the operating folder using the preparation command above. Runtime code and all necessary regression inputs are in the repository; no prior AI answer cache is required.
