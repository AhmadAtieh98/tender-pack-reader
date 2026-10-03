# Verify the draft archive on a Mac

## Tested here vs. what you still need to check

| Check | Tested in the cloud container (Linux x86_64, Python 3.11) | Still to check on your Mac |
|---|---|---|
| Unzip; every file matches `SHA256SUMS` | yes (`scripts/verify_archive.py`) | yes, step 1 |
| A3 links open `a3_detail.html` at the row | link targets checked in the PDF; **not clicked in a viewer** | yes: click a row id in Preview |
| Review pages: every image and link resolves | yes | open `REVIEW/index.html` |
| `a1.xlsx` opens | written and re-read by openpyxl; **not opened in Excel** | yes: open it in Excel |
| Repository bundle clones with full history | yes | step 2 |
| Offline install, rebuild, outputs identical, tests pass | yes, with no network at all (`unshare -n`) | step 3 (Wi-Fi off) |
| macOS wheels install | **no** (no Mac here) | step 3 |

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
.venv/bin/python scripts/compare_outputs.py out .. # expected: "outputs identical to the archive"
make test PY=.venv/bin/python                      # about 6 minutes; expected: all passed
```

**If you have network instead:** `brew install uv && uv sync --extra dev` replaces the wheel steps.

**If something differs:** `compare_outputs.py` names the files. A difference only in `a1.xlsx` or `a3.pdf` would point to a library build difference on macOS. Compare `a1.csv` and `a3.json`, which are plain text.

## 4. Optional: a live command

```
.venv/bin/python -m tenderpack show VOL-I-8.6-01
.venv/bin/python -m tenderpack diff                # includes the cover-summary check (C28)
.venv/bin/python -m tenderpack outputs --strict; echo "exit $?"   # 3 = release refused until you have reviewed
```

Nothing here approves or accepts anything. Your decisions are recorded only by the commands in `OPERATING_GUIDE.md` §4.
