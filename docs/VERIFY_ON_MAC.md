# Verify the draft archive on a Mac

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
