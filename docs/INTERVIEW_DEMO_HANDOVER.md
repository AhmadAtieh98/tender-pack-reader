# Interview demo: implementation handover

## Current state

The application has a prepared ADD02 interview profile, a signed-in Codex host transport and an incremental ADD03 workflow. Demo approvals are explicitly labelled and editable. A partial result remains partial when evidence or interpretation is missing. The normal source pack and its approval files have not been changed.

The implementation was developed from `509be48`. Code, tests and reproducible preparation scripts are included in this revision. Generated operating folders, model exchanges, historical run outputs and private conversation records are not included. Worklogs are not updated by this revision. This document is the technical continuation entry point for Claude Code and other coding agents.

## Run from a fresh checkout

Create a Python 3.11+ environment and install the locked dependencies. With uv available:

```sh
uv sync --frozen --extra dev --no-install-project
.venv/bin/python scripts/prepare_interview_demo.py /absolute/path/outside-checkout/interview-release
```

Use an absolute destination outside the source checkout. Preparation creates a portable folder and zip, ingests the baseline, enables the explicit demo profile, builds ADD02 outputs and freezes their hashes. It does not change source curation. In the generated folder:

```sh
bash scripts/mac/setup.sh
.venv/bin/python -m tenderpack interview verify
.venv/bin/python -m tenderpack panel --open
```

On macOS, `INTERVIEW_START.command` handles setup and opens the panel. `RESTORE_ADD02.command` verifies and restores the frozen baseline while retaining prior run/history files. Restoration and decision editing refuse while a run is active.

At Home, verify validated ADD02 and no working stage. Open the existing A1–A5 files, then upload only ADD03 with the host/Codex route selected. The host requires an installed, signed-in Codex CLI and network access. Its configuration lives in `config/interview-ai.yaml`, copied into the operating folder as `config/ai.yaml`. Check the available model/configuration on the intended machine; configured identity is distinct from the model identity actually reported at runtime.

The interview profile has two total concurrent host sessions, six-item analysis/downstream batches and a 2,700-second overall guard. The guard is a limit, not a runtime promise. Resume interrupted work from Runs or with `tenderpack ai resume RUN_ID`. Preserve its checkpoint and evidence. Do not bypass the code-change check to conceal a mixed-version benchmark.

## Implementation map

| Area | Main files | Behavior |
| --- | --- | --- |
| Demo preparation and recovery | `scripts/prepare_interview_demo.py`, `tenderpack/interview.py` | Freeze/verify/restore ADD02; explicit simulated reviews; atomic validated rebuilds; reversible decisions and planning edits. |
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
