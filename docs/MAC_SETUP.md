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

## 1. One-time setup (needs the network once, unless you bring a wheelhouse)

```
cd /path/to/tender-pack-reader
bash scripts/mac/setup.sh            # or: bash scripts/mac/setup.sh --dry-run   (checks only; installs nothing)
```

What it does, in order. Each step prints a PASS, PENDING or FAIL line:

1. Finds `python3` 3.11 or newer. If there is none, install one: `brew install python@3.12`, or the python.org
   installer.
2. Reads the `pymupdf` pin from `pyproject.toml` (`pymupdf==1.28.2`). The version is never copied into the scripts.
3. Creates `.venv`, with `uv` when it is installed and `python3 -m venv` otherwise. An existing `.venv` is kept.
4. Installs the project from `pyproject.toml`:
   - **from a local wheelhouse** when one is there. This uses no network (`--no-index --find-links`). The script looks
     for `wheels/*.whl`, or for the draft archive's macOS wheel parts, joined and unzipped as in
     `docs/VERIFY_ON_MAC.md` §3 (`wheels/*/macos-<arch>/` or `../wheels/*/macos-<arch>/`, beside `requirements.txt`).
     Only the dependencies are installed; the project runs from the repository with `python -m tenderpack`.
   - **from PyPI otherwise**, installing the project from `pyproject.toml`. This is the only network use, and it
     happens once.

   To make a wheelhouse yourself on a Mac with network, run
   `python3 -m pip download -d wheels "pymupdf==1.28.2" "numpy>=2.0" "pydantic>=2.7" "pyyaml>=6.0" "openpyxl>=3.1.5" "pytest>=8"`
   (arm64 macOS wheels for your Python).
5. Checks that `pymupdf`, `openpyxl`, `pydantic`, `yaml` and `numpy` import, and that the installed `pymupdf` matches
   the pin.
6. Checks that `ollama` is on PATH and lists the models **already installed** (`ollama list`). It never pulls a model.

PENDING ON THE MAC: the real setup run (steps 3–6) and its checklist.

## 2. The launcher

Double-click `scripts/mac/launch.command` in Finder, or run it in Terminal. The first time, macOS may ask you to allow
it: right-click it, choose Open, then confirm. The launcher activates `.venv`, sets offline mode
(`TENDERPACK_OFFLINE=1`) and offers this menu:

| | Action | Command it runs |
|---|---|---|
| 1 | Rebuild the evidence | `tenderpack ingest` (into `build/`) |
| 2 | Build the outputs A1–A5 | `tenderpack outputs --evidence build --out out` |
| 3 | Strict check | `tenderpack outputs --evidence build --out out --strict` (exit 3 while approvals are pending) |
| 4 | Check the register | `tenderpack check-register` |
| 5 | AI routes and local model capabilities | `tenderpack ai routes --offline` |
| 6 | Run an addendum offline | `tenderpack ai run ADD-NN --pdf PATH --offline` (a candidate under `staging/ai/runs/`; nothing accepted) |
| 7 | Start the local panel | `tenderpack panel --open` (127.0.0.1 only, a new token each start; `docs/PANEL.md`; the launcher sets `TENDERPACK_OFFLINE=1`, so runs started from the panel are offline) |
| 8 | Run the offline checks | `bash scripts/mac/checks.sh` |

PENDING ON THE MAC: the double-click (Gatekeeper prompt) and each menu item on your machine.

## 3. The offline checks

Turn Wi-Fi off, then run:

```
bash scripts/mac/checks.sh            # --plan lists the checks; --no-ai skips the two Ollama checks
```

Everything is written to a scratch folder, `$TMPDIR/tenderpack-checks-<time>`. Your `build/`, `out/` and `staging/` are
not touched.

| # | Check | Pass when | Where it stands |
|---|---|---|---|
| 0 | Network off | no default route (checked locally, nothing contacted) | Passed in the cloud (it has no default route; it reaches the internet only through a proxy). **PENDING ON THE MAC** with Wi-Fi off |
| 1 | `ingest` | exit 0, 524 units | Passed in the cloud container. **PENDING ON THE MAC** |
| 2 | `outputs` | exit 0, published, no structural check failed | Passed in the cloud container. **PENDING ON THE MAC** |
| 3 | `outputs --strict` | exit 3 with only the two human-approval blockers (205 rows, 37 ops) | Passed in the cloud container. **PENDING ON THE MAC** |
| 4 | The A1 xlsx opens | openpyxl loads it; then look at it in Numbers or Excel yourself | openpyxl passed in the cloud; the visual look is **PENDING ON THE MAC** |
| 5 | The HTML opens | every `.html` parses; then open one in a browser yourself (Arabic, links) | Parsing passed in the cloud (14 files); the browser view is **PENDING ON THE MAC** |
| 6 | `ai routes --offline` | Ollama reachable and every configured model checked: installed, vision, tools, context, estimated memory | Tested with a fake local server only. **PENDING ON THE MAC** |
| 7 | One-batch offline run | `ai run --offline --stop-after ingest` on blind-02's synthetic Addendum No. 3, then one `ai propose --route ollama --offline` request for one provision against the installed model, answered and validated (the time is printed) | **PENDING ON THE MAC** (no Ollama in the cloud) |
| 8 | The panel | `tenderpack panel --help` works; the pages open in the browser at the printed address | `--help` and every page tested in the container by HTTP (`tests/test_session12_panel.py`, 11 tests); the browser, `--open` and launcher item 7 **PENDING ON THE MAC** (`docs/PANEL.md`) |

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
- **"model X is not installed":** either install it yourself (`ollama pull X`), or point `routes.ollama.models.<role>.id`
  in `config/ai.yaml` at a model you have. `tenderpack ai routes --offline` lists them.
- **"estimated memory … exceeds":** lower that model's `num_ctx` in `config/ai.yaml`, or choose a smaller model.
