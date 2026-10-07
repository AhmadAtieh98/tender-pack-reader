# tenderpack on the Mac: setup, launcher and offline checks

For the owner's M5 Pro MacBook Pro (48 GB unified memory), with Ollama and local models already installed. After the
one-time setup, the deterministic build, the exports (A1–A5) and the checks run **without internet and without an API
key**. Local AI runs only through the local Ollama, in offline mode. Nothing here downloads a model, calls a hosted
service or sends anything anywhere.

**Status of this guide (session 12, 5 Oct 2026).** The scripts were written and checked in a Linux cloud container,
which cannot reach your Mac or its `localhost`. There, `setup.sh --dry-run` ran, and `checks.sh --no-ai` ran checks
0–5 and 8 against the real pack: 6 PASS, 5 PENDING, 0 FAIL. (A first run reported one FAIL because the script looked
for the wrong line in the `outputs` log; that was fixed and the run repeated.) The Ollama paths were tested against a
fake local server that replays recorded answers. Every item marked **PENDING ON THE MAC** below has not been run on your machine.
A recorded answer is a test. It is not proof that a live local model works.

**Session 14 (7 Oct 2026).** The AI checks now have three levels, each printed on its own line (§3), and the launcher's
option 6 reads the run's checkpoint instead of its exit code. The one-page order of everything to run on the Mac,
each step with its command and the line to expect, is `docs/MAC_CHECKLIST.md`. Everything below was run in the cloud
container only (cloud-tested); every Mac step is **PENDING ON THE MAC**.

## 1. One-time setup (needs the network once, unless you bring a wheelhouse)

```
cd /path/to/tender-pack-reader
bash scripts/mac/setup.sh            # or: bash scripts/mac/setup.sh --dry-run   (checks only; installs nothing)
```

What it does, in order. Each step prints a PASS, PENDING or FAIL line:

1. Finds `python3` 3.11 or newer. If there is none, install one: `brew install python@3.12`, or the python.org
   installer.
2. Reads the `pymupdf` pin from `pyproject.toml` (`pymupdf==1.28.2`). The version is never copied into the scripts.
3. Builds `.venv` **in this folder** (session 13). A `.venv` copied from another folder or machine is not portable:
   setup refuses it (its `activate` names another folder, or its Python no longer runs) and prints the one command
   that rebuilds it: `rm -rf "<folder>/.venv" && bash "<folder>/scripts/mac/setup.sh"`.
4. Installs **exactly the locked set** and never resolves afresh from `pyproject.toml` (session 13; before, the
   network path ran `pip install -e ".[dev]"`, which ignored `uv.lock`):
   - **a local wheelhouse** when one is there (no network): `pip`/`uv pip install --no-index --find-links <wheels>
     -r requirements.lock.txt`. The script looks for `wheels/*.whl`, or for the draft archive's macOS wheel parts,
     joined and unzipped as in `docs/VERIFY_ON_MAC.md` §3 (`wheels/*/macos-<arch>/` or `../wheels/*/macos-<arch>/`).
   - **`uv` on PATH**: `uv sync --frozen --extra dev --no-install-project` from `uv.lock` (the uv cache, else PyPI
     once). If that fails while `.venv` exists (for example offline, with the wheels cached under the index rather
     than the lock's file addresses), the same locked set is installed with `uv pip install -r requirements.lock.txt`.
   - **neither**: `python3 -m venv .venv`, then `pip install -r requirements.lock.txt` (PyPI once).

   `requirements.lock.txt` is exported from `uv.lock` (`uv export --frozen --no-hashes --extra dev
   --no-emit-project`); a test checks that the two agree. The project itself is not installed: it runs from the
   folder (`python -m tenderpack`). `TENDERPACK_SETUP_PYTHON=python3.12 bash scripts/mac/setup.sh` chooses the
   interpreter. After the install, `scripts/mac/lockcheck.py` compares every installed version with the lock and
   fails the setup on any difference, naming each package.
5. Checks that `pymupdf`, `openpyxl`, `pydantic`, `yaml` and `numpy` import, and that the installed `pymupdf` matches
   the pin. Then (session 13, E159) `scripts/mac/pathlink.py` writes `tenderpack-folder.pth` into the `.venv`'s
   site-packages, naming this folder, so `import tenderpack` resolves to the folder's package from ANY working
   directory, and verifies it from outside the folder. The host route's MCP server is started by the host CLI in the
   run's session folder (the CLI ignores the server config's `cwd`), and the server is also started with the folder on
   `PYTHONPATH`; without either, the server died with "No module named tenderpack" and the reading session had no
   tools (the first sealed blind-07 attempt).
6. Checks that `ollama` is on PATH and lists the models **already installed** (`ollama list`). It never pulls a model.

PENDING ON THE MAC: the real setup run (steps 3–6) and its checklist. In the cloud container (session 13) the setup
ran offline (`UV_OFFLINE=1`) in an unzipped interview folder: 7 PASS, 1 PENDING (no Ollama), 0 FAIL, through the
`uv pip install -r requirements.lock.txt` door because the container's uv cache was filled by `uv pip`; after E159,
8 PASS (the folder link added), 1 PENDING, 0 FAIL in the rebuilt folders (`uv sync --frozen`).

## 2. The launcher

Double-click `scripts/mac/launch.command` in Finder, or run it in Terminal. The first time, macOS may ask you to allow
it: right-click it, choose Open, then confirm. Session 13:

- **It checks before the menu**, and every failure prints `PROBLEM:` (exactly what is wrong) and `NEXT:` (the one
  command to run): the launcher not inside a tenderpack folder; no `.venv` (NEXT: the setup command); a `.venv` whose
  Python does not run or that was built in another folder (NEXT: `rm -rf "<folder>/.venv" && bash
  "<folder>/scripts/mac/setup.sh"`); the dependencies not importing (NEXT: setup).
- **It asks how AI steps run**: `1 connected` (Claude Code first, the host route; Codex, an API key and Ollama when
  usable) or `2 offline` (the local Ollama only: `TENDERPACK_OFFLINE=1`, so every phase refuses a hosted route
  before any call). `m` switches. A pre-set `TENDERPACK_OFFLINE=1` starts it offline.
- **It lists the routes** (`tenderpack ai routes --brief`): each one usable now or why not (offline mode, no `claude`
  on PATH, no key configured, the paid caps not set, Ollama not answering), and its recorded status from
  `config/routes_status.yaml` (Claude Code: tested in the cloud container; Codex: built, unverified; the API key:
  untested; OpenRouter: blocked here, unverified; Ollama: pending on the Mac).

| | Action | Command it runs |
|---|---|---|
| 1 | Rebuild the evidence | `tenderpack ingest` (into `build/`) |
| 2 | Build the outputs A1–A5 | `tenderpack outputs --evidence build --out out` |
| 3 | Strict check | `tenderpack outputs --evidence build --out out --strict` (exit 3 while approvals are pending) |
| 4 | Check the register | `tenderpack check-register` |
| 5 | AI routes | `tenderpack ai routes` (live state, status, why not, what to do) |
| 6 | Run an addendum | offline: `tenderpack ai run ADD-NN --pdf PATH --offline`; connected: `... --route host` (or the route you type). Refused with PROBLEM/NEXT when the file is missing or a run on that addendum is already live (NEXT: `tenderpack ai run-status RUN`) |
| 7 | Start the local panel | `tenderpack panel --open` (127.0.0.1 only, a new token each start; `docs/PANEL.md`). With `TENDERPACK_PANEL_PORT=N`, a busy port is reported with the next command; otherwise a free port is used |
| 8 | Run the offline checks | `bash scripts/mac/checks.sh` |
| 9 | The smoke test | `bash smoke-test/run_smoke.sh` (interview folder; synthetic, no model call) |

After each command the launcher prints its exit code and what it means (3 approvals pending, 4 waiting for a host
submission, 5 deferred by a rate limit, 6 stopped for a person; `RECOVERY.md`). After option 6 (session 14) it reads the
run's checkpoint instead (`scripts/mac/levels.py workflow`): `level 3 (complete workflow) PASS` only when the run is
complete, its candidate outputs published and its review packet written; a run that exits 0 but is partial prints
`level 3 (complete workflow) PARTIAL: exit 0; run ... ended PARTIAL, not a success: <the first reason>`; a run that
stopped or waits prints PENDING with what it needs.

PENDING ON THE MAC: the double-click (Gatekeeper prompt) and each menu item on your machine. The error paths were
tested in the container by a bash harness (`tests/test_session13_mac_scripts.py`).

## 3. The offline checks

Turn Wi-Fi off, then run:

```
bash scripts/mac/checks.sh            # --plan lists the checks; --no-ai skips the two Ollama checks
bash scripts/mac/checks.sh --only 6,7 # (session 14) only the Ollama checks; --no-workflow skips level 3
```

Everything is written to a scratch folder, `$TMPDIR/tenderpack-checks-<time>`. Your `build/`, `out/` and `staging/` are
not touched.

**How a check decides (session 13).** Each check captures its command's exit code at once (never after a pipe), reads
the blocker lines from its log, and passes only when the exit code is the expected one **and** the blockers are exactly
the human-approval ones (`RELEASE BLOCKER [approval] ...`). Any other blocker (coverage, stale, a register defect) or
a structural `FAIL` line fails the check and is printed under it. Before, check 2 passed on exit 0 and "published"
whatever the blockers said, and check 3 passed on any exit 3.

**The three levels of the AI checks (session 14).** Before, check 7 printed "answered and validated" for any exit 0 of
`ai propose`, which also exits 0 for a set whose items all failed the validation. Now `scripts/mac/levels.py` reads the
records and each level has its own line:

| Level | Line | PASS only when |
|---|---|---|
| 1 connectivity (check 6) | `PASS 6 level 1 (connectivity) PASS: ...` | Ollama answers `/api/tags`, the models are installed and `/api/show` reports their vision, tools and context for every phase (PENDING when Ollama does not answer or a phase has no model; the model the level-2 request will use is named) |
| 2 valid content (check 7) | `PASS 7 level 2 (valid content) PASS: N item(s) passed the controller's validation, none failed [model; the request's exit 0 after Ns]` | the one-batch request's proposal set (`proposals.yaml`) holds items and every one passed the validation (`evidence_verified` or `interpretation_pending`); `PARTIAL` when some did and some did not (each failed item is listed), `FAIL` when none did or the set is malformed |
| 3 complete workflow (check 7) | `PASS 7 level 3 (complete workflow) PASS: ...` | a whole `ai run --offline` of the smoke-test addendum is complete in its checkpoint (completeness complete, the candidate outputs published, the review packet written); a partial run that exits 0 is `PARTIAL ... not a success`; it runs only after levels 1 and 2 PASS and can take long with a local model (`--no-workflow` skips it) |

The summary line counts the four kinds: `offline checks: N PASS, N PARTIAL, N PENDING, N FAIL`; only a FAIL makes the
script exit non-zero.

| # | Check | Pass when | Where it stands |
|---|---|---|---|
| 0 | Network off | no default route (checked locally, nothing contacted) | Passed in the cloud (it has no default route; it reaches the internet only through a proxy). **PENDING ON THE MAC** with Wi-Fi off |
| 1 | `ingest` | exit 0 and `STRUCTURE OK` (524 units) | Passed in the cloud container. **PENDING ON THE MAC** |
| 2 | `outputs` | exit 0, published, no structural FAIL, only approval blockers | Passed in the cloud container. **PENDING ON THE MAC** |
| 3 | `outputs --strict` | exit 3 with only the two human-approval blockers (205 rows, 37 ops) | Passed in the cloud container. **PENDING ON THE MAC** |
| 4 | The A1 xlsx opens | openpyxl loads it; then look at it in Numbers or Excel yourself | openpyxl passed in the cloud; the visual look is **PENDING ON THE MAC** |
| 5 | The HTML opens | every `.html` parses; then open one in a browser yourself (Arabic, links) | Parsing passed in the cloud (14 files); the browser view is **PENDING ON THE MAC** |
| 6 | Level 1: `ai ollama-models --offline` | Ollama answers; every INSTALLED model (`/api/tags`) with its reported capabilities and context (`/api/show`) and its estimated memory against this Mac's memory (read with sysctl/sysconf); which model can serve each phase (reading: vision + tools; analysis, downstream: tools; critic: none; each at its configured context). Exit 0 PASS (every phase served), 1 PENDING (some phase without an installed model), 3 PENDING (Ollama not answering). Never pulls | Tested with a fake local server only. **PENDING ON THE MAC** |
| 7 | Levels 2 and 3 | level 2: `ai run --offline --stop-after ingest` on the smoke-test's synthetic Addendum No. 3 (`smoke-test/`, or made by `tests/fixtures/make_drill.py`), then one `ai propose --route ollama --offline --model <the model level 1 named>` request for one provision; PASS only when its `proposals.yaml` shows every item passed the validation (the exit code and the time are printed, not believed). Level 3: a whole `ai run --offline` of the same addendum, read from its checkpoint | Cloud-tested against a fake local server (`tests/test_session14_mac_levels.py`). **PENDING ON THE MAC** (no Ollama in the cloud) |
| 8 | The panel | `tenderpack panel --help` works; the pages open in the browser at the printed address | `--help` and every page tested in the container by HTTP (`tests/test_session12_panel.py`, 11 tests); the browser, `--open` and launcher item 7 **PENDING ON THE MAC** (`docs/PANEL.md`) |
| 9 | The locked set | `scripts/mac/lockcheck.py requirements.lock.txt`: every installed version equals the lock | Passed in the cloud container (the main `.venv` and an interview folder's). **PENDING ON THE MAC** |
| 10 | The folder link | `scripts/mac/pathlink.py --root <folder>`: `import tenderpack` from outside the folder resolves to the folder's package (the host route's MCP server starts in the session folder) | Passed in the cloud container (the rebuilt interview folders; session 13, E159). **PENDING ON THE MAC** |

## 4. Local models: what tenderpack checks and what it never assumes

`config/ai.yaml` `routes.ollama.models` names one model per role:

- `text`: the analysis and downstream phases. It must report **tool use**.
- `vision`: the readings of image regions. It must report **vision**.
- `critic`: the independent review. It needs no tools and no images.

The shipped choices (`qwen3:30b-a3b`, `qwen3-vl:32b`) are **candidates, unmeasured**. Replace them with models you have
installed.

For each model, tenderpack asks the local endpoint (`/api/tags` and `/api/show`). It never assumes any of the
following:

- **Installed?** A missing model stops the run with "model X is not installed; install it yourself with
  `ollama pull X` if you want it", followed by the list of installed models. tenderpack never runs `ollama pull`.
- **Vision and tool use?** These come only from the `capabilities` that `/api/show` reports.
  - A text model without tools is refused for the analysis.
  - A reading model without vision does not stop silently. The readings step reports "cannot run locally with this
    model" and the image regions are **escalated to a person**. Without those readings, ingest refuses the candidate,
    so the run stops with the way on.
- **Context?** The bound is `num_ctx`, never more than the model reports. Every request is sized against it. A batch
  that does not fit is split, and one provision that does not fit alone is escalated. Nothing is ever truncated.
- **Memory?** This is an **estimate**, not a measurement:
  - weights at the reported quantisation, plus an f16 KV cache at `num_ctx`, plus 1 GB;
  - compared with 48 GB × 0.75. The 0.75 is an **assumption** about macOS's GPU working-set limit; adjust
    `routes.ollama.machine` after measuring;
  - a model that cannot hold its context is refused, with the numbers;
  - `tenderpack ai routes --offline` shows the estimate and the largest context that fits.

PENDING ON THE MAC: which models you actually have, their reported capabilities, real memory use (Activity Monitor
while a run is going) and real timings. Nothing about local model quality or speed is claimed.

## 5. Offline mode (what it guarantees)

Offline mode is on with `--offline`, with `offline: true` in `config/ai.yaml`, or with `TENDERPACK_OFFLINE=1` (set by
the launcher and by `checks.sh`). It guarantees the following:

- Every AI phase runs on the local `ollama` route: readings, analysis, downstream, the critic, the bounded repair and
  the capability checks.
- Hosted routes are refused **before any process or network call**. The host route is Claude Code or Codex, a
  connected coding host. The `anthropic` and `openrouter` routes are hosted APIs. Asking for any of them raises an
  error that starts with "offline mode", and no fallback is attempted.
- The Ollama URL must be a loopback address. It is reached directly, never through an HTTP proxy.
- The critic runs on `routes.ollama.models.critic`. If that model is not configured, not installed, or cannot hold the
  request, the review is recorded as **SKIPPED**: "independent review did not run: <reason>". It appears in the run
  log, the checkpoint, the review packet and the candidate `out/README.md`. A skipped review is never shown as
  agreement.

Tested in the cloud with a fake local server and a guard that refuses any connection except the fake's loopback port
and any `claude` or `codex` process. PENDING ON THE MAC: the same with your real Ollama, with Wi-Fi off.

## 6. If something fails

- **`setup.sh` FAIL on python:** install Python 3.12 (`brew install python@3.12`) and run the script again.
- **Install FAIL without network:** bring a `wheels/` folder (see step 4 above), or connect once.
- **`checks.sh` 6 or 7 PENDING with "could not be reached":** start the Ollama app, or run `ollama serve`.
- **Check 7 level 2 PARTIAL or FAIL:** the local model answered, but not every item passed the validation; the failed
  items are listed under the line, and `$TMPDIR/tenderpack-checks-<time>/staging-propose/<run>/review_request.md` says
  why. That is a fact about the model's answer, not about the installation.
- **"model X is not installed":** either install it yourself (`ollama pull X`), or point `routes.ollama.models.<role>.id`
  in `config/ai.yaml` at a model you have. `tenderpack ai routes --offline` lists them.
- **"estimated memory … exceeds":** lower that model's `num_ctx` in `config/ai.yaml`, or choose a smaller model.
