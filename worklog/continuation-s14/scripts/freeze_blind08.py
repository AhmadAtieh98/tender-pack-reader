"""Freeze a blind-08 run's first outputs by hash before the key is opened (the blind-05 procedure).
Usage: freeze_blind08.py RUN_ID [--root FOLDER] [--suffix add04]   (copies the run's folders into rehearsals/blind-08[/add04] and writes FROZEN-OUTPUTS.sha256)
"""
import hashlib, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/user/tender-pack-reader")
run_id = sys.argv[1]
suffix = sys.argv[sys.argv.index("--suffix") + 1] if "--suffix" in sys.argv else ""
dest = REPO / "rehearsals" / "blind-08" / (suffix or ".")
dest = dest.resolve()
ROOT = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else REPO   # session 13: the run may live in the interview folder
src = ROOT / "staging" / "ai" / "runs" / run_id
assert src.is_dir(), src
stamp = run_id.rsplit("-", 1)[-1]  # e.g. 20261006T000000Z
copies = {
    "out-candidate": src / "candidate" / "out",
    "review": src / "review",
    "downstream": src / "downstream",
    "batches": src / "batches",
    "candidate-curation": src / "candidate" / "curation",
}
files = {"checkpoint.json": src / "checkpoint.json", "promotion.json": src / "promotion.json", "log.jsonl": src / "log.jsonl"}
dest.mkdir(parents=True, exist_ok=True)
copied = []
for name, path in copies.items():
    if path.is_dir():
        if (dest / name).exists():
            shutil.rmtree(dest / name)
        shutil.copytree(path, dest / name)
        copied.append(name)
    else:
        print("missing", name, path)
# proposal sets staged by this run: the per-session proposal folders under ai/ (ADD-0x-host-*) and the combined set
ai_dir = src / "ai"
add = run_id.split("-run-")[0]
sets = sorted(p for p in ai_dir.iterdir() if p.is_dir() and (p.name.startswith(f"{add}-host-") or p.name == f"{run_id}-combined"))
pdest = dest / "proposals"
if pdest.exists():
    shutil.rmtree(pdest)
pdest.mkdir()
for p in sets:
    shutil.copytree(p, pdest / p.name)
for name, path in files.items():
    if path.exists():
        shutil.copy2(path, dest / name)
        copied.append(name)
# hash everything copied
lines = []
for base in sorted(copied) + ["proposals"]:
    b = dest / base
    paths = sorted(q for q in b.rglob("*") if q.is_file()) if b.is_dir() else [b]
    for q in paths:
        h = hashlib.sha256(q.read_bytes()).hexdigest()
        lines.append(f"{h}  {q.relative_to(dest).as_posix()}")
(dest / "FROZEN-OUTPUTS.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"), "frozen", len(lines), "files;", len(sets), "proposal sets:", [p.name for p in sets])
