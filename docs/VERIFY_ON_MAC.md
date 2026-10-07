# Verify the draft archive and the interview folder on a Mac

## Tested here vs. what you still need to check

| Check | Tested in the cloud container (Linux x86_64, Python 3.11) | Still to check on your Mac |
|---|---|---|
| Unzip; every file matches `SHA256SUMS` | yes (`scripts/verify_archive.py`) | yes, step 1 |
| A3 links open `a3_detail.html` at the row | link targets checked in the PDF; **not clicked in a viewer** | yes: click a row id in Preview |
| Review pages: every image and link resolves | yes | open `REVIEW/index.html` |
| `a1.xlsx` opens | written and re-read by openpyxl; **not opened in Excel** | yes: open it in Excel |
| Repository bundle clones with full history | yes | step 2 |
| Offline install, rebuild, outputs identical, tests pass | yes, with no network at all (`unshare -n`), on Linux x86_64 only | step 3 (Wi-Fi off) |
| Same content on another platform | not checkable here: only one platform was available | step 3: `compare_outputs.py` separates **content** (CSV, JSON, Markdown, HTML must be byte-identical) from **rendering** (PDF, PNG, XLSX: if the bytes differ, the text, links and cell values are compared; a difference there only is reported as platform-dependent rendering) |
| macOS wheel files | parts joined and checksum OK; every requirement resolves **offline** for Apple silicon (macOS 11+) and Intel (macOS 14+) with Python 3.11, 3.12 and 3.13 (uv resolver, no network). **Not installed or imported on a Mac** | step 3 |

## 1. Unpack and check

```
cd ~/Downloads && mkdir lamar && cd lamar
unzip ../LAMAR-PPP-R2-DRAFT_<sha>.zip && cd LAMAR-PPP-R2-DRAFT_<sha>
shasum -a 256 -c SHA256SUMS | grep -v ': OK$'; echo "checksums done (nothing above = all OK)"
open 00_README.md A3_disqualification_sheet/a3.pdf REVIEW/index.html A1_compliance_register/a1.xlsx
```

## 2. Clone the repository

```
git clone A4_work_log/repository.bundle repo && cd repo && git log --oneline | head
```

## 3. Install offline, rebuild, compare, test

The wheel files come split into parts. Put every `…wheels-macos-<arch>.zip.part*` file and its `.sha256` in `~/Downloads`. Then:

```
ARCH=$(uname -m)                                   # arm64 (Apple silicon) or x86_64 (Intel, macOS 14+)
W=$(ls ~/Downloads/*wheels-macos-$ARCH.zip.part01 | sed 's/\.part01$//')
cat "$W".part* > "$W" && shasum -a 256 -c "$W.sha256"
unzip -q "$W" -d ../wheels
python3 -m venv .venv                              # Python 3.11, 3.12 or 3.13
.venv/bin/python -m pip install --no-index --find-links ../wheels/*/macos-$ARCH -r ../wheels/*/requirements.txt
# turn Wi-Fi off now
make evidence outputs drill rehearsal PY=.venv/bin/python
git status --short                                 # expected: nothing printed (every rebuilt file identical)
.venv/bin/python scripts/compare_outputs.py out .. # expected: "outputs identical to the archive in content (...)"
make test PY=.venv/bin/python                      # about 6 minutes; expected: all passed
```

**If you have network instead:** `brew install uv && uv sync --extra dev` replaces the wheel steps.

**If something differs:** `compare_outputs.py` names each file and says whether its **content** differs (a real difference: report it) or only its **rendering** (bytes of a PDF, PNG or XLSX differ but the text, links and cells are the same: a library or font difference on macOS, not a content change). `git status` in step 3 may then also list those rendered files; the CSV, JSON and Markdown files must still be unchanged.

## 4. Optional: a live command

```
.venv/bin/python -m tenderpack show VOL-I-8.6-01
.venv/bin/python -m tenderpack diff                # includes the cover-summary check (C28)
.venv/bin/python -m tenderpack outputs --strict; echo "exit $?"   # 3 = release refused until you have reviewed
```

Nothing here approves or accepts anything. Your decisions are recorded only by the commands in `OPERATING_GUIDE.md` §4.

## 5. The interview folder (session 13): the checks still PENDING on your Mac

The interview folder (`LAMAR-PPP-R2-INTERVIEW_<base>+wt_<stamp>.zip`, built by `scripts/make_interview_folder.py`) is
the operating copy for the Mac; the submitted repository is preserved separately. Everything below was prepared in a
Linux cloud container, which cannot reach your Mac: **every check is PENDING until you run it there**, and a pass in the
container proves nothing about the Mac. Run them in order; each says what you should see. Keep the folder where it
will stay before step B: the environment is built in place.

| # | Check | Command (in Terminal) | Expected | State |
|---|---|---|---|---|
| A | Unzip; the executable bits; the manifest | `cd ~/Documents && unzip -q ~/Downloads/LAMAR-PPP-R2-INTERVIEW_*.zip && cd LAMAR-PPP-R2-INTERVIEW_*/ && ls -l scripts/mac/launch.command scripts/mac/*.sh smoke-test/run_smoke.sh && shasum -a 256 -c MANIFEST.sha256 \| grep -v ': OK$'; echo done` | `-rwxr-xr-x` on `launch.command`, `setup.sh`, `checks.sh` and `run_smoke.sh`; nothing printed before `done`. (Finder's Archive Utility should keep the same bits: double-click the zip and check `launch.command` opens) | PENDING |
| B | Setup from the lock | `bash scripts/mac/setup.sh` | `PASS uv.lock and requirements.lock.txt present`, `PASS locked set installed from ...`, `PASS installed versions match requirements.lock.txt (all 15 applicable pins match the lock ...)` (14 on Python 3.12+ where numpy has one pin; the count is the lock's lines for your Python), the imports and the pymupdf pin PASS, then `PASS tenderpack imports from <this folder> wherever the interpreter starts (... tenderpack-folder.pth)` (session 13, E159: the folder linked into `.venv`); `0 FAIL`. Network once unless uv's cache or a wheelhouse holds the wheels | PENDING |
| C | The offline checks | Wi-Fi off; `bash scripts/mac/checks.sh --no-ai` | `PASS 1 ingest: exit 0, STRUCTURE OK (units: 524 ...)`; `PASS 2 outputs: exit 0, 2 approval blocker(s) only` followed by the two lines `RELEASE BLOCKER [approval] 205 of 205 register rows ...` and `... 37 of 37 amendment op(s) ...`; `PASS 3 outputs --strict: exit 3, 2 approval blocker(s) only`; 4, 5, 8 PASS with their PENDING looks; `PASS 9 installed versions match requirements.lock.txt`; `PASS 10 tenderpack imports from <this folder> wherever the interpreter starts` (the host route's MCP server starts in the session folder, not here); `0 FAIL`. Any other blocker is a FAIL printed under its check: report it | PENDING |
| D | The smoke test | `bash smoke-test/run_smoke.sh` | the label `SMOKE TEST: synthetic, not tender content`, then PASS lines (exit 0; status stopped after ingest; 12 provisions of ADD-03, all pending; approval none; no model, host-session or network event; the candidate inside its run folder) and `smoke test: PASS (9 of 9 checks ...)` in about 20 to 60 s | PENDING |
| E | The panel in Safari | double-click `scripts/mac/launch.command`, choose `1` (connected) or `2` (offline), then `7` | Safari opens `http://127.0.0.1:<port>/t/<token>/`; Home shows the Deliverables strip with **A4 Work log (the repository history, prompts, model calls, errors)** and, separately, **Clarification register (supporting record, drafts not sent)**; the New addendum box lists host, codex, anthropic, openrouter and ollama, each with its status in brackets and, when it cannot be chosen, why; the A4 "commit history" link says the operating copy has no .git (the submitted repository has it); Stages, Runs, Jobs and Decisions open; Ctrl-C in Terminal stops it | PENDING |
| F | The connected route with Claude Code (first route to rehearse) | launcher `1` (connected), option `5`, then option `6` with `smoke-test/ADD-03_Addendum_No_3.pdf`, id `ADD-03`, route `host` (Enter) | option 5: `host usable now` (`claude` found) and `[tested; last exercised: the cloud container of sessions 10-12 ...]`; option 6: `[run] ingest ...`, the batches asked through headless `claude -p` sessions on your plan, a candidate and a review packet under `staging/ai/runs/<run>/`, every item PROPOSED, nothing accepted; exit 0, or 5 if a rate limit defers it (then `tenderpack ai resume <run>` later) | PENDING |
| G | The offline route with Ollama | Ollama running; `bash scripts/mac/checks.sh` (without `--no-ai`), then launcher `2` (offline), option `6` with the smoke-test PDF | check 6: `ai ollama-models` lists your installed models with capabilities, context, memory against 48 GB, and per phase which can serve it; PASS only if every phase has one (else PENDING with what is missing; nothing is pulled); check 7: one offline request answered and validated, with its time. Option 6: the run uses only `ollama`; no `claude` process starts (Activity Monitor), no hosted call | PENDING |

Report each row's result (PASS, or the exact lines that differ). Until then, `config/routes_status.yaml` keeps Claude
Code at "tested" in the cloud container only and Ollama at "pending on the Mac"; update it by hand with the date and
the result once a row has run on the Mac.
