"""Build the MINIMAL INTERVIEW FOLDER for the owner's Mac (session 13): an operating copy, not the submission.

Usage: python scripts/make_interview_folder.py DEST [--label TEXT]

  LAMAR-PPP-R2-INTERVIEW_<base>+wt_<UTC stamp>/      (and the same as a .zip beside it)
    README.md              what it is, the launch steps, the connected/offline choice, the smoke test, the focused
                           tests and their command, what was left out, the checks still PENDING on the Mac
    RECOVERY.md            an interrupted run: run-status, resume, the lock takeover, the deferral exit 5, the panel's
                           resume button, where the logs are, what never to delete
    INTERVIEW.json         the base revision, the time, the label, the file count
    MANIFEST.sha256        sha256 of every file (`shasum -a 256 -c MANIFEST.sha256`)
    tenderpack/            the editable code
    tests/                 a focused subset (FOCUSED, the session-13 tests and the fixtures they import)
    sources/ config/ curation/ (approvals included)   the original sources, configuration, curated data
    build/ out/            the baseline evidence and outputs (the drill and fixture builds left out)
    docs/                  the runtime instructions (DOCS)
    pyproject.toml uv.lock requirements.lock.txt [wheels/]    the exact dependencies (setup.sh installs the lock)
    scripts/mac/           setup.sh, checks.sh, launch.command, lockcheck.py, pathlink.py
    scripts/make_interview_folder.py                          this builder
    smoke-test/            ONE labelled synthetic addendum ("SMOKE TEST: synthetic, not tender content"), its
                           expected result and run_smoke.sh (no model call)
    staging/ai/runs/ worklog/model_calls/ logs/               for new runs and logs (a .keep; staging/ai/runs/ also
                           holds the blind-05 candidate INPUTS of TEST_MATERIAL, no checkpoint: not a run)
    worklog/README.md      the A4 index (the panel links it)
    TEST_MATERIAL          the synthetic regression inputs the focused tests read, at the paths they read them

Left out: every historical run under staging/ai/runs/, rehearsals/ (outputs and answer keys), out-drill*,
build/drill*, build/fixture*, worklog/ (the session records; the submitted repository keeps them), wt-*, .git,
__pycache__, and any virtual environment: a .venv found anywhere in what would be copied is REFUSED (the environment is
built in the final location by scripts/mac/setup.sh; a copied one is not portable). The zip keeps the executable bit of
*.command and *.sh (0755), and of the files executable at their source (the tests' fake CLIs), and is checked
against the folder (verify()). Reads git only (`rev-parse`); writes only under
DEST; refuses a DEST inside the repository."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PREFIX = "LAMAR-PPP-R2-INTERVIEW"
TREES = ("tenderpack", "sources", "config", "curation", "build", "out", "scripts/mac", "scripts/smoke_test")
FILES = ("pyproject.toml", "uv.lock", "requirements.lock.txt", "scripts/make_interview_folder.py", "worklog/README.md",
         "worklog/ERROR_INDEX.md",
         "scripts/bench_workflow.py")          # session 14: the timing tool two focused tests run (and the owner can)
DOCS = ["OPERATING_GUIDE.md", "AI_ROUTES.md", "PANEL.md", "MAC_SETUP.md", "VERIFY_ON_MAC.md",
        "QUICK_REVIEW.md", "MAC_CHECKLIST.md"]           # session 14 (W6): the quick review and the one-page checklist
OPTIONAL_DOCS = ["RUNTIME_INSTRUCTIONS.md"]
OPTIONAL_TREES = ("wheels",)
FOCUSED = ("tests/test_session12_panel.py", "tests/test_session12_mac_checks.py",
           "tests/test_session12_computed_dates.py", "tests/test_session12_human_owned.py",
           "tests/test_session12_closed_window.py", "tests/test_session12_concurrency.py")
# The slow ones: the tests that need a whole recorded workflow run (their fixtures cost 30-80 s each in the cloud
# container; session 13 --durations). The quick command (under three minutes) deselects them; the full command runs
# everything (about ten minutes there). A fixture's cost moves to the next test using it, so every user is listed.
_PANEL_FULL_RUN = ("test_the_run_page_follows_the_run_and_then_lists_the_candidate_outputs",
                   "test_upload_to_results_runs_a_real_ai_run_job_to_completion",
                   "test_the_candidate_review_is_labelled_and_never_writes_out",
                   "test_an_interrupted_run_is_resumed_from_the_panel", "test_runs_and_jobs_pages_say_what_each_needs",
                   "test_the_token_appears_only_under_its_own_prefix_and_never_in_logs",
                   "test_the_run_page_offers_the_review_packet_first_when_the_run_is_finished")
SLOW = tuple(f"tests/test_session12_concurrency.py::{n}" for n in (
    "test_batches_run_at_once_within_the_bound_and_give_the_sequential_result",
    "test_host_route_batches_at_once_hold_one_run_lock_and_match_one_at_a_time",
    "test_batches_at_once_get_past_a_reading_and_a_blocked_stop_does_not_exit_0",
    "test_a_rate_limit_pauses_every_worker_defers_cleanly_and_resumes")) + tuple(
    f"tests/test_session12_human_owned.py::{n}" for n in (
        "test_d_the_run_promotes_the_proposals_as_proposals_and_keeps_the_question_open",
        "test_d_the_rendered_register_candidate_a3_and_review_packet_say_human_decision_pending",
        "test_e_deterministic_facts_stay_evidence_verified_and_promotable")) + tuple(
    f"tests/test_session12_panel.py::{n}" for n in _PANEL_FULL_RUN) + (
    # session 14 (W6): the session-14 tests that need a whole workflow run or many workspace refreshes (measured in the
    # cloud container: 250 s and 70 s); every other test_session14_* file runs in the quick command. When a new
    # session-14 test makes the quick command pass three minutes, scripts/mac/verify_package.sh names the slowest:
    # list them here (a deselect list, never a time limit).
    "tests/test_session14_mac_levels.py::test_level3_a_partial_offline_run_that_exits_zero_is_partial_never_success",
    "tests/test_session14_mac_levels.py::test_level3_complete_only_when_the_checkpoint_the_outputs_and_the_packet_agree",
    "tests/test_session14_offline_never_hosted.py::test_every_command_refuses_a_hosted_route_offline_before_any_call"
    "[flag]",
    # session 14 (the package's self-verification of 8 Oct: the quick command took 14 min with these; each runs a whole
    # recorded workflow or more, 24-104 s apiece in the container): still in the full command, never skipped
    "tests/test_session13_speed.py::test_the_result_does_not_depend_on_the_arrival_order",
    "tests/test_session13_speed.py::test_sigterm_after_a_submission_keeps_the_step_time_and_the_answer",
    "tests/test_session13_speed.py::test_a_reused_set_whose_evidence_changed_is_revalidated_and_asked_again_with_the_reason",
    "tests/test_session13_speed.py::test_kill_before_submission_is_asked_again",
    "tests/test_session13_speed.py::test_kill_after_submission_resume_reuses_the_staged_set",
    "tests/test_session13_speed.py::test_no_session_starts_for_a_batch_whose_provisions_are_all_accounted_for",
    "tests/test_session13_speed.py::test_no_worker_idles_while_an_earlier_answer_is_awaited",
    "tests/test_session14_owner_answers.py::test_the_workflow_consumes_an_offered_answer_at_its_checkpoint_and_re_asks_the_batch",
    "tests/test_session12_human_owned.py::test_a_an_issue_declaring_the_concession_conflicts_resolved_is_not_evidence_verified",
    "tests/test_session13_correctness_analysis_rows.py::test_every_analysis_item_not_promoted_carries_an_explicit_reason")
TEST_SUPPORT_TREES = ("tests/fixtures", "tests/golden")
# Synthetic regression inputs the focused tests read at fixed paths (tests/fixtures/ai_fixture.py: blind-02's pack and
# its addendum; tests/fixtures/s12_blind05.py: blind-05's candidate pack and curation). Inputs only: never a SEALED
# key, a COMPARISON, a run's outputs, batches or logs. ADD-03.yaml of blind-02 (its curated answer) is left out.
TEST_MATERIAL = ("rehearsals/blind-02/input/", "rehearsals/blind-02/work/",
                 "staging/ai/runs/ADD-03-run-host-blind05-20261005T025444Z/candidate/pack.yaml",
                 "staging/ai/runs/ADD-03-run-host-blind05-20261005T025444Z/candidate/config/",
                 "staging/ai/runs/ADD-03-run-host-blind05-20261005T025444Z/candidate/curation/",
                 "staging/ai/runs/ADD-03-run-host-blind05-20261005T025444Z/candidate/input/",
                 "staging/ai/runs/ADD-03-run-host-blind05-20261005T025444Z/candidate/sources/")
# session 14 (the package's self-verification found 14 failures and 6 errors in the packaged copy): the run RECORDS some
# session-13/14 focused tests read (a recorded run's checkpoint and log, its review index, a candidate reading, one
# comparison), the blind-06 input PDF the quick-review page tests render, and the test modules the runtime policy's
# enforcement table names (read for their test names only; not run). No sealed key, comparison or candidate output is
# among them (the tests that read those skip without them).
TEST_RECORDS = ("rehearsals/blind-06/input/", "rehearsals/blind-06/checkpoint.json", "rehearsals/blind-06/log.jsonl",
                "rehearsals/blind-07/checkpoint.json", "rehearsals/blind-07/log.jsonl",
                "rehearsals/blind-07/review/index.md", "rehearsals/blind-07/candidate-curation/readings/",
                "rehearsals/blind-07/downstream/proposals.yaml", "rehearsals/blind-07/promotion.json",
                "rehearsals/blind-06/proposals/",
                "tests/test_session09_ai_propose.py", "tests/test_session10_relationships.py",
                "tests/test_session12_blind06_fixes.py", "tests/test_session13_correctness_enforcement.py",
                "tests/test_session13_policy.py")
MATERIAL_LEFT_OUT = ("rehearsals/blind-02/work/amendments/ADD-03.yaml",)
SKIP_PREFIXES = ("build/drill", "build/fixture")
SKIP_NAMES = ("__pycache__", ".pytest_cache", ".DS_Store", ".git")
BACKUP_SUFFIXES = (".orig", ".rej", "~", ".swp", ".bak")     # session 13: patch backups and editor leftovers never ship


def is_backup(name: str) -> bool:
    """A patch backup or an editor leftover (requests.py.orig after `patch -p1`, a .rej, a ~ file): never copied."""
    return name.endswith(BACKUP_SUFFIXES)
EMPTY = ("staging/ai/runs", "worklog/model_calls", "logs")
LABEL = "SMOKE TEST: synthetic, not tender content"
EXCLUDED = ("every historical run under staging/ai/runs/ (bulky candidate runs; the submitted repository keeps them)",
            "rehearsals/ (rehearsal outputs, sealed answer keys, comparisons), except the synthetic test inputs listed "
            "under TEST_MATERIAL", "out-drill*/, build/drill*/, build/fixture*/ (drill and fixture builds)",
            "worklog/ session records (only worklog/README.md and ERROR_INDEX.md, the A4 index and error note the "
            "panel links)",
            "docs/ other than the runtime instructions", "every other test file", "any .venv (built here by setup.sh)",
            "wt-* worktrees, .git, __pycache__, patch backups and editor leftovers (*.orig, *.rej, *~)")


class Refused(RuntimeError):
    pass


def _git(repo: Path, *args: str) -> str | None:
    try:
        r = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def base_revision(repo: Path) -> str:
    """The short commit the folder is built from (`git rev-parse`, read only); in a folder without git, the base its
    INTERVIEW.json records (a folder rebuilt from itself keeps the original base)."""
    sha = _git(repo, "rev-parse", "--short", "HEAD")
    if sha:
        return sha
    try:
        return json.loads((repo / "INTERVIEW.json").read_text(encoding="utf-8"))["base"]
    except (OSError, ValueError, KeyError):
        return "0000000"


def focused_tests(repo: Path) -> list[str]:
    """The focused set: every session-13 AND session-14 test file (session 14, W6: all of them, by glob, so a new one
    cannot be left out), then FOCUSED."""
    recent = sorted(p.relative_to(repo).as_posix() for pat in ("test_session13_*.py", "test_session14_*.py")
                    for p in (repo / "tests").glob(pat))
    return recent + [t for t in FOCUSED if (repo / t).is_file()]


def _imported_test_modules(repo: Path, tests: list[str]) -> list[str]:
    """test_*.py modules a focused test imports for their fixtures (e.g. test_session11_downstream), transitively."""
    seen, todo = set(), list(tests)
    while todo:
        t = todo.pop()
        for m in re.findall(r"^\s*from (test_[A-Za-z0-9_]+) import|^\s*import (test_[A-Za-z0-9_]+)",
                            (repo / t).read_text(encoding="utf-8"), re.M):
            rel = f"tests/{(m[0] or m[1])}.py"
            if (repo / rel).is_file() and rel not in seen and rel not in tests:
                seen.add(rel)
                todo.append(rel)
    return sorted(seen)


def _walk(repo: Path, top: str) -> list[str]:
    out = []
    root = repo / top
    if root.is_file():
        return [top]
    for d, dirs, files in os.walk(root):
        rel_d = Path(d).relative_to(repo).as_posix()
        if ".venv" in dirs or "pyvenv.cfg" in files:
            bad = f"{rel_d}/.venv" if ".venv" in dirs else f"{rel_d}/pyvenv.cfg"
            raise Refused(f"refused: a virtual environment ({bad}) is inside what would be copied; a .venv is never "
                          "copied (it is not portable: scripts/mac/setup.sh builds it in the final location). "
                          f"Remove it from {rel_d} and run again")
        dirs[:] = sorted(x for x in dirs if x not in SKIP_NAMES)
        for f in sorted(files):
            rel = f"{rel_d}/{f}"
            if f in SKIP_NAMES or f.endswith(".pyc") or is_backup(f) or rel.startswith(SKIP_PREFIXES) \
                    or (Path(d) / f).is_symlink():
                continue
            out.append(rel)
    return out


def select(repo: Path = REPO) -> list[str]:
    """Every file the folder takes from the repository (relative POSIX paths, sorted). Raises Refused on a .venv."""
    repo = Path(repo)
    paths: set[str] = set()
    for top in TREES + OPTIONAL_TREES + TEST_SUPPORT_TREES:
        if (repo / top).exists():
            paths.update(_walk(repo, top))
    for f in FILES:
        if (repo / f).is_file():
            paths.add(f)
    for d in DOCS + OPTIONAL_DOCS:
        if (repo / "docs" / d).is_file():
            paths.add(f"docs/{d}")
    tests = focused_tests(repo)
    paths.update(tests)
    paths.update(_imported_test_modules(repo, tests))
    if (repo / "tests/conftest.py").is_file():
        paths.add("tests/conftest.py")
    for m in TEST_MATERIAL + TEST_RECORDS:
        if (repo / m).exists():
            paths.update(_walk(repo, m.rstrip("/")))
    paths -= set(MATERIAL_LEFT_OUT)
    return sorted(paths)


def executable(name: str, src: Path | None = None) -> bool:
    """A launcher or shell script (*.command, *.sh), or a file executable at its source (the fake CLIs of the tests)."""
    return name.endswith((".command", ".sh")) or bool(src is not None and src.is_file() and src.stat().st_mode & 0o100)


def zip_mode(name: str, src: Path | None = None) -> int:
    """A regular file, 0755 when executable() (always for *.command and *.sh), else 0644."""
    return (0o100000 | (0o755 if executable(name, src) else 0o644)) << 16


def write_zip(folder: Path, dest: Path, stamp: tuple) -> None:
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for f in sorted(p for p in folder.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(f"{folder.name}/{f.relative_to(folder).as_posix()}", date_time=stamp)
            info.compress_type, info.external_attr = zipfile.ZIP_DEFLATED, zip_mode(f.name, f)
            info.create_system = 3
            z.writestr(info, f.read_bytes())


def _files(folder: Path) -> list[str]:
    return sorted(p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file())


def verify(folder: Path, zpath: Path) -> list[str]:
    """Problems ([] when none): the manifest against the files, the zip against the folder (names, bytes, modes)."""
    probs = []
    listed = {}
    for ln in (folder / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        h, p = ln.split("  ", 1)
        listed[p] = h
    files = [p for p in _files(folder) if p != "MANIFEST.sha256"]
    if sorted(listed) != files:
        probs.append(f"the manifest lists {len(listed)} file(s), the folder holds {len(files)}")
    for p in files:
        if listed.get(p) != hashlib.sha256((folder / p).read_bytes()).hexdigest():
            probs.append(f"manifest mismatch: {p}")
    with zipfile.ZipFile(zpath) as z:
        names = {i.filename: i for i in z.infolist() if not i.is_dir()}
        want = {f"{folder.name}/{p}" for p in _files(folder)}
        if set(names) != want:
            probs.append(f"the zip differs from the folder: {sorted(set(names) ^ want)[:10]}")
        for n, i in names.items():
            if n in want and z.read(n) != (folder / n.split("/", 1)[1]).read_bytes():
                probs.append(f"zip content differs: {n}")
            if n in want and (i.external_attr >> 16) & 0o777 != (zip_mode(n, folder / n.split("/", 1)[1]) >> 16) & 0o777:
                probs.append(f"zip mode {oct((i.external_attr >> 16) & 0o777)}: {n}")
    return probs


def _smoke(stage: Path, repo: Path) -> dict:
    """smoke-test/: the drill's synthetic Addendum No. 3, its record, the label, the expected result, the runner."""
    spec = importlib.util.spec_from_file_location("make_drill_for_interview", repo / "tests/fixtures/make_drill.py")
    md = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(md)
    d = stage / "smoke-test"
    d.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as tmp:
        expected = md.build(Path(tmp) / "drill")
        shutil.copy(Path(tmp) / "drill" / md.PDF_NAME, d / md.PDF_NAME)
        shutil.copy(Path(tmp) / "drill" / "expected.yaml", d / "expected.yaml")
    (d / "LABEL.txt").write_text(LABEL + "\n", encoding="utf-8")
    for f in ("run_smoke.sh", "check_smoke.py"):
        shutil.copy(repo / "scripts/smoke_test" / f, d / f)
    provs = expected.get("provisions") or []
    structural = len(expected.get("units") or []) - len(provs)
    (d / "EXPECTED.md").write_text("\n".join([
        f"# {LABEL}", "",
        "The synthetic Addendum No. 3 was invented for a drill (`tests/fixtures/make_drill.py`); it is laid out like the "
        "real addenda and is NOT tender content. Its record, `expected.yaml`, is the builder's own (what it printed), "
        "never the program's output.", "",
        "## Run it", "", "```", "bash smoke-test/run_smoke.sh", "```", "",
        "## Expected candidate result (no model is called)", "",
        "- exit 0; the run's status `stopped` after the ingest step (`--stop-after ingest`); every later step pending;",
        f"- the line `candidate built: {len(provs)} provisions of ADD-03 (+{structural} structural units listed)`;",
        f"- the {len(provs)} provisions, each `pending` (nothing proposed, nothing accepted; approval `none`): "
        + ", ".join(f"`{p}`" for p in provs) + ";",
        "- the candidate inside the run's own folder (in a scratch folder under `$TMPDIR`; `staging/`, `out/` and "
        "`curation/` untouched); no model, host-session or network event in the run's log;",
        "- `check_smoke.py` prints one PASS line per check and `smoke test: PASS`; about 20 to 60 seconds.", "",
        "A FAIL line names what differs. The smoke test proves the installation and the deterministic first step "
        "work on this machine; it says nothing about a model's answers (the connected and offline checks in "
        "`docs/VERIFY_ON_MAC.md` do that).", ""]), encoding="utf-8")
    return {"provisions": len(provs), "structural": structural}


def recovery_md() -> str:
    return """# RECOVERY: an interrupted run, and what never to delete

Everything below uses `.venv/bin/python -m tenderpack` (written `tp` here) from this folder. Nothing in this file
accepts, approves or rejects anything: those are a person's commands (`tp accept|reject|approve`).

## 1. See where a run stands

```
tp ai run-status RUN_ID          # the checkpoint: each step, each batch, the timings, what it waits for
```
The run id is printed when a run starts, is the folder name under `staging/ai/runs/`, and is listed on the panel's
Runs page. A run whose checkpoint says `running` but whose process is gone is shown **interrupted** there.

## 2. Resume it

```
tp ai resume RUN_ID              # continue from the checkpoint; a batch that succeeded is never asked again
tp ai resume RUN_ID --from STEP  # rerun STEP and the later ones (after a code change); answered batches are kept
```
The panel's run page has the same **Resume** button (it runs `tp ai resume RUN_ID`). Resume an offline run with
`--offline` (it stays offline); a connected run resumes on its own route.

## 3. The lock

One orchestrator per addendum: `staging/ai/.lock-ADD-NN`. When the process that held it has died on this machine
(a crash, a closed Terminal, a restart), the next `tp ai run` / `tp ai resume` **takes the lock over** and records the
takeover in the new lock. A lock whose process is still alive is never taken: wait for it (`tp ai run-status`). A lock
older than 120 minutes, or from another machine, is reported STALE; only a person removes it:
`tp ai propose ADD-NN ... --break-lock --by "Your Name"` (recorded in `staging/ai/locks.jsonl`).

## 4. Exit 5: deferred by a rate limit

A host or API rate limit is backed off (about 7.5 minutes at most), then the batch is **deferred**: the run stops
cleanly with **exit 5**, everything done so far checkpointed. Run `tp ai resume RUN_ID` after the reset time the
message names; deferred batches are asked again, finished ones never. Exit 4: waiting for a host submission (the manual
path: `tp ai submit-batch RUN_ID FILE --by "Your Name"`). Exit 6: stopped because the run cannot go on by itself (a
reading or a decision a person must make); the run page says what it needs.

## 5. Reset a run that went wrong

A run writes only inside its own folder `staging/ai/runs/RUN_ID/`. To start again, start a NEW run (a new id) and leave
the old folder: it is the record of what happened. Move an unwanted run folder aside rather than deleting it.

## 6. Where the logs are

- `staging/ai/runs/RUN_ID/log.jsonl` and `.../logs/` (each step), `.../checkpoint.json` (the state)
- `worklog/model_calls/RUN_ID.jsonl` (every prompt, tool call, response and usage; keys redacted)
- `logs/` (launcher and check logs you choose to keep); `checks.sh` writes to `$TMPDIR/tenderpack-checks-<time>/`
- the panel's jobs: `staging/panel/jobs/`

## 7. What never to delete (never delete these; move aside if you must)

- `curation/approvals.yaml`, `curation/readings/`, `curation/reading-snapshots/`, `curation/` as a whole (the curated
  data and every recorded decision)
- `sources/` (the original PDFs), `config/` (including `config/assumptions.yaml`, your labelled assumptions)
- `build/` and `out/` (the baseline evidence and outputs; rebuild with options 1 and 2 of the launcher if in doubt,
  never by deleting)
- a run's `checkpoint.json` and `log.jsonl` while it may be resumed; `worklog/model_calls/`
- `.venv` may be deleted and rebuilt at any time: `rm -rf .venv && bash scripts/mac/setup.sh`
"""


def quick_argv(tests: list[str]) -> list[str]:
    """Session 14 (W6): the quick command's arguments after the interpreter (INTERVIEW.json quick_tests_argv, which
    scripts/mac/verify_package.sh runs): the focused tests without the SLOW ones, the ten slowest durations reported."""
    slow = [s for s in SLOW if s.split("::")[0] in tests]
    return (["-m", "pytest", "-q", "-p", "no:cacheprovider", "--durations=10", *tests]
            + [x for s in slow for x in ("--deselect", s)])


def commands(tests: list[str]) -> tuple[str, str]:
    """(quick, full): the focused tests without the SLOW ones (under three minutes), and all of them."""
    full = ".venv/bin/python -m pytest -q -p no:cacheprovider " + " ".join(tests)
    slow = [s for s in SLOW if s.split("::")[0] in tests]
    return full + "".join(f" --deselect {s}" for s in slow), full


def load_routes(repo: Path) -> dict:
    """config/routes_status.yaml's routes (session 14, W6: the README quotes it rather than restating it)."""
    import yaml
    try:
        return (yaml.safe_load((Path(repo) / "config/routes_status.yaml").read_text(encoding="utf-8")) or {}).get(
            "routes") or {}
    except (OSError, yaml.YAMLError):
        return {}


def route_lines(routes: dict) -> list[str]:
    """One numbered entry per route: its label and status, where it ran, what works, what never ran, what is ready."""
    out = []
    for i, (name, r) in enumerate(routes.items(), 1):
        f = {k: " ".join(str(r.get(k) or "-").split()) for k in ("label", "status", "where", "works", "never_run",
                                                                  "ready")}
        out.append(f"{i}. **{f['label']}** (`{name}`): **{f['status']}**; last exercised: {f['where']}. Works: "
                   f"{f['works']}. Never run: {f['never_run']}. Ready: {f['ready']}. On this Mac: PENDING until you "
                   "run it (`docs/MAC_CHECKLIST.md`).")
    return out


def readme(name: str, base: str, label: str, tests: list[str], support: list[str], n_files: int, smoke: dict,
           routes: dict | None = None) -> str:
    quick, cmd = commands(tests)
    routes = load_routes(REPO) if routes is None else routes
    return "\n".join([
        f"# {name}", "",
        "**The minimal interview folder: an OPERATING COPY for the owner's Mac, not the submission.** The submitted "
        f"repository is preserved separately (base revision `{base}`; its history, session records, rehearsals and "
        "candidate runs stay there). Nothing in this folder is accepted, approved or sent.", "",
        f"- Label: {label or '(none)'}", f"- Files: {n_files} (`MANIFEST.sha256`; `shasum -a 256 -c MANIFEST.sha256`)", "",
        "## Launch (on the Mac)", "",
        "1. Unzip (Finder or `unzip`); keep the folder where it will stay: the environment is built IN PLACE.",
        "2. `bash scripts/mac/setup.sh` builds `.venv` here from the lock (`uv sync --frozen`, or "
        "`pip install -r requirements.lock.txt`) and links this folder into it (a `.pth` file, so the host route's "
        "MCP server imports the package wherever it starts); never copy a `.venv` from elsewhere.",
        "3. `bash scripts/mac/checks.sh --no-ai` (or without `--no-ai` when Ollama is installed): every check reads "
        "its command's exit code and the blockers; the two human-approval blockers are expected.",
        "4. Double-click `scripts/mac/launch.command` (or `bash scripts/mac/launch.command`).", "",
        "## The route choice", "",
        "The launcher asks first: **connected** (Claude Code first, the host route; Codex, an API key and Ollama when "
        "usable) or **offline** (the local Ollama only; `TENDERPACK_OFFLINE=1`, so every phase refuses a hosted route "
        "before any call). Option 5 (`tenderpack ai routes`) shows each route's live state here and its recorded "
        "status from `config/routes_status.yaml` (each route below, quoted from that file). "
        "Keys only through the environment or a chmod-600 `~/.config/tenderpack/keys.env` outside this folder "
        "(`docs/AI_ROUTES.md`), never in chat or a log.", "",
        "## Trying each route (the owner, 6 Oct: the Mac, Codex, the API route, Ollama)", "",
        "Each route runs the same addendum through the same code; only the model exchange differs. Use the smoke-test "
        "PDF first (`smoke-test/ADD-03_Addendum_No_3.pdf`, synthetic), then a real one. Every run is a candidate under "
        "`staging/ai/runs/<run id>/` with its review packet; nothing is approved or accepted by a run.", "",
        ] + route_lines(routes) + ["",
        "`.venv/bin/python -m tenderpack ai routes` prints each route's live state on this machine beside its recorded "
        "status; `tenderpack ai run-status <run id>` and the panel show a run's steps, timings and what it waits for.", "",
        "## The smoke test", "",
        f"`smoke-test/`: **{LABEL}**. `bash smoke-test/run_smoke.sh` runs the synthetic Addendum No. 3 through the "
        f"deterministic first step (no model call) and checks the result against `smoke-test/expected.yaml`: "
        f"{smoke['provisions']} provisions, all pending, approval none (`smoke-test/EXPECTED.md`).", "",
        "## The focused tests", "",
        "Quick (under three minutes; the tests that need a whole recorded workflow run, named by `--deselect`, "
        "left out):", "",
        "```", quick, "```", "",
        "Full (everything below, about ten minutes in the cloud container):", "",
        "```", cmd, "```", "",
        "Run:"] + [f"- `{t}`" for t in tests] + ["", "Imported for their fixtures (not run): "
        + (", ".join(f"`{s}`" for s in support) or "none") + "; `tests/conftest.py`, `tests/fixtures/`, "
        "`tests/golden/`. The synthetic regression inputs those tests read are kept at the paths they read them: "
        + ", ".join(f"`{m}`" for m in TEST_MATERIAL) + " (inputs only; blind-02's curated `ADD-03.yaml` is left out); and the run records a few tests read: "
        + ", ".join(f"`{m}`" for m in TEST_RECORDS) + " (no sealed key; the test modules there are read for their "
        "names, not run).", "",
        "## What was excluded", ""] + [f"- {x}" for x in EXCLUDED] + ["",
        "## Recovery", "", "`RECOVERY.md`: an interrupted run (run-status, resume, the lock takeover, exit 5), where "
        "the logs are and what never to delete. New runs go to `staging/ai/runs/` (it holds no run: only the "
        "blind-05 candidate INPUTS the focused tests read, without a checkpoint, so the panel and `ai run-status` do "
        "not list them), model-call logs to `worklog/model_calls/`, your own logs to `logs/` (both empty).", "",
        "## The Mac checklist and verifying this package", "",
        "`docs/MAC_CHECKLIST.md`: one page, every step in order with its command and the line to expect, each marked "
        "PENDING ON THE MAC. `bash scripts/mac/verify_package.sh <this zip>` verifies the packaged copy itself: it "
        "unzips it into a fresh place, checks the manifest, the executable bits and the contents, then runs the setup, "
        "the focused quick tests, the checks and the smoke test there.", "",
        "## Checks PENDING on the Mac", "",
        "Nothing here has run on the owner's Mac; a cloud test proves nothing about Mac readiness. "
        "`docs/VERIFY_ON_MAC.md` (section \"The interview folder\") lists each check with its expected output, each "
        "PENDING: unzip and the executable bits, setup from the lock, `checks.sh`, the smoke test, the panel in "
        "Safari, the connected route with Claude Code, the offline route with Ollama.", ""])


def build(dest: Path, label: str = "", repo: Path = REPO, now: datetime | None = None) -> dict:
    repo, now = Path(repo).resolve(), now or datetime.now(timezone.utc)
    dest = Path(dest).resolve()
    if dest == repo or repo in dest.parents:
        raise Refused(f"refused: {dest} is inside the repository {repo}; build the folder somewhere else")
    files = select(repo)
    base = base_revision(repo)
    name = f"{PREFIX}_{base}+wt_{now.strftime('%Y%m%dT%H%MZ')}"
    stage = dest / name
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    for rel in files:
        dst = stage / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repo / rel, dst)
    for d in EMPTY:
        (stage / d).mkdir(parents=True, exist_ok=True)
        (stage / d / ".keep").write_text("", encoding="utf-8")
    smoke = _smoke(stage, repo)
    tests = focused_tests(repo)
    support = _imported_test_modules(repo, tests)
    (stage / "RECOVERY.md").write_text(recovery_md(), encoding="utf-8")
    n_files = len(_files(stage)) + 3                                   # README, INTERVIEW.json, MANIFEST
    (stage / "README.md").write_text(readme(name, base, label, tests, support, n_files, smoke, load_routes(repo)),
                                     encoding="utf-8")
    (stage / "INTERVIEW.json").write_text(json.dumps({"base": base, "built_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                                      "label": label, "files": n_files, "name": name,
                                                      # session 14 (W6): read by scripts/mac/verify_package.sh
                                                      "focused_tests": tests, "quick_tests_argv": quick_argv(tests)},
                                                     indent=1) + "\n", encoding="utf-8")
    for p in stage.rglob("*"):
        if p.is_file():
            rel = p.relative_to(stage).as_posix()
            p.chmod(0o755 if executable(p.name, repo / rel if rel in files else None) else 0o644)
    sums = [f"{hashlib.sha256((stage / p).read_bytes()).hexdigest()}  {p}" for p in _files(stage)]
    (stage / "MANIFEST.sha256").write_text("\n".join(sums) + "\n", encoding="utf-8")
    zpath = dest / f"{name}.zip"
    write_zip(stage, zpath, (now.year, now.month, now.day, now.hour, now.minute, 0))
    probs = verify(stage, zpath)
    if probs:
        raise Refused("the zip or the manifest does not match the folder: " + "; ".join(probs[:10]))
    size = sum((stage / p).stat().st_size for p in _files(stage))
    return {"folder": str(stage), "zip": str(zpath), "files": len(_files(stage)), "bytes": size,
            "zip_bytes": zpath.stat().st_size, "base": base, "tests": tests, "excluded": list(EXCLUDED)}


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    label = argv[argv.index("--label") + 1] if "--label" in argv else ""
    try:
        res = build(Path(argv[0]), label)
    except Refused as e:
        print(str(e))
        return 2
    print(f"interview folder: {res['folder']}\n  {res['files']} files, {res['bytes'] / 1e6:.1f} MB; zip "
          f"{res['zip']} ({res['zip_bytes'] / 1e6:.1f} MB); base {res['base']}\n  focused tests: {len(res['tests'])}"
          "\n  excluded: " + "; ".join(res["excluded"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
