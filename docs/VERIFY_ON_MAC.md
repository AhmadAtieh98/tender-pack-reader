# Verify the draft archive on a Mac

**What was tested in the cloud container (Linux x86_64, Python 3.11)** by `scripts/verify_archive.py`:

- extraction and checksums;
- the links in A3 and the review pages;
- a fresh clone from the bundle with the full history;
- an offline install from a wheelhouse, inside a namespace with no network at all (`unshare -n`);
- an offline regeneration of everything committed (evidence, outputs, both drills, the blind rehearsal's `out-after-fixes`): every file byte-identical to the committed one;
- the rebuilt outputs compared byte for byte with the archive's A1, A2, A3, A5 and REVIEW;
- the test suite, offline.

The results are in the session 06 work log, §7.

**What could not be tested:** a Mac. The commands below do the same there. Expect identical outputs; if anything differs, `compare_outputs.py` names the file.

Replace `<sha>` with the commit in the archive's name.

## 1. Unpack and check

```
cd ~/Downloads
mkdir lamar-draft && cd lamar-draft
unzip ../LAMAR-PPP-R2-DRAFT_<sha>.zip
cd LAMAR-PPP-R2-DRAFT_<sha>
shasum -a 256 -c SHA256SUMS | grep -v ': OK$' ; echo "checksums done (no lines above = all OK)"
open 00_README.md A3_disqualification_sheet/a3.pdf REVIEW/index.html
open A1_compliance_register/a1.xlsx
```

In `a3.pdf`, clicking a row id opens `a3_detail.html` at that row. Preview may ask to open the browser.

## 2. Get the repository with its history

```
git clone A4_work_log/repository.bundle tender-pack-reader
cd tender-pack-reader
git log --oneline | head -20        # the real history, session by session
git status                           # clean
```

## 3. Set up Python

**Option A, with network once (simplest):**

```
brew install uv            # or: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --extra dev        # creates .venv from uv.lock (Python 3.11+)
```

**Option B, fully offline, with the wheelhouse archive.** This needs `python3` 3.11, 3.12 or 3.13 (`python3 --version`; e.g. `brew install python@3.12` beforehand):

```
unzip ../../LAMAR-PPP-R2-DRAFT_<sha>_wheels-macos.zip -d ../wheels
python3 -m venv .venv
ARCH=$(uname -m)                     # arm64 (Apple silicon) or x86_64 (Intel)
.venv/bin/python -m pip install --no-index --find-links ../wheels/macos-$ARCH -r ../wheels/requirements.txt
```

The package runs from the repository folder (`python -m tenderpack`), so no install of `tenderpack` itself is needed.

## 4. Rebuild offline and compare

Turn Wi-Fi off first, e.g. `networksetup -setairportpower en0 off`, or use Control Centre.

```
make evidence  PY=.venv/bin/python            # Stage 1: STRUCTURE OK, readings PENDING (also rebuilds build/fixture)
make outputs   PY=.venv/bin/python            # WORKING DRAFT published; release blockers listed
make drill     PY=.venv/bin/python            # drill A (ingest replaced build/, so this restores build/drill*)
make rehearsal PY=.venv/bin/python            # drill B
git status --short                            # nothing printed = every regenerated file equals the committed one
.venv/bin/python scripts/compare_outputs.py out ..      # compares out/ with the archive's A1, A2, A3, A5 and REVIEW
make test      PY=.venv/bin/python            # about 6 minutes; every test should pass
```

Turn Wi-Fi back on afterwards.

**Expected:** `git status --short` prints nothing, "outputs identical to the archive", and all tests passing.

**If anything differs:** the script lists the files. A difference in only `a1.xlsx` or `a3.pdf` would point to a library build difference on macOS, not to content. Compare `a1.csv` and `a3.json`, which are plain text.

## 5. Try a live command

```
.venv/bin/python -m tenderpack show VOL-I-8.6-01        # pages, crops, amendment chain, A5
.venv/bin/python -m tenderpack diff                      # what ADD-02 changed against ADD-01
.venv/bin/python -m tenderpack outputs --strict ; echo "exit $?"   # 3: release refused until you have reviewed
```

## 6. Your decisions (these are yours; nothing is decided for you)

See `OPERATING_GUIDE.md` §4. Example:

```
.venv/bin/python -m tenderpack approve VOL-II-p3-r1 --reviewer "Your Name"
.venv/bin/python -m tenderpack accept VOL-I-8.6-01 --reviewer "Your Name" --note "checked p4 and ADD-02 p3"
```
