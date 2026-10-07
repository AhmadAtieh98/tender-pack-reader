"""Export every session-14 subagent brief (Agent launches) and follow-up message (SendMessage) from the session
transcript, verbatim, into worklog/subagent_briefs/ with the session-11 naming, and append the README rows.

Usage: export_briefs.py [--dry-run]   (dry run writes to the scratchpad's s14/briefs_export/ instead)
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

TRANSCRIPT = Path("/root/.claude/projects/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c.jsonl")
REPO = Path("/home/user/tender-pack-reader")
OUT = REPO / "worklog" / "subagent_briefs"
SCRATCH = Path("/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s14/briefs_export")
SESSION_START = datetime(2026, 10, 7, 6, 50, tzinfo=timezone.utc)
FIRST_NO = 116


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:50]


def main(dry: bool) -> int:
    out = SCRATCH if dry else OUT
    out.mkdir(parents=True, exist_ok=True)
    items = []
    with TRANSCRIPT.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("type") != "assistant":
                continue
            ts = rec.get("timestamp")
            if not ts:
                continue
            when = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if when < SESSION_START:
                continue
            msg = rec.get("message") or {}
            for block in msg.get("content") or []:
                if block.get("type") != "tool_use":
                    continue
                name, inp = block.get("name"), block.get("input") or {}
                if name == "Agent":
                    items.append(("launch", when, inp.get("description") or "(no description)", inp.get("prompt") or "",
                                  inp.get("model") or "(default)", inp.get("subagent_type") or "(default)", None))
                elif name == "SendMessage" and inp.get("to") and inp.get("message"):
                    to = inp["to"]
                    if to in ("main",) or to.startswith("a") and len(to) < 8:
                        continue
                    items.append(("follow-up", when, inp.get("summary") or "(no summary)", inp["message"], None, None, to))
    items.sort(key=lambda x: x[1])
    rows = []
    for n, (kind, when, desc, text, model, stype, to) in enumerate(items, FIRST_NO):
        fname = f"{when.strftime('%Y-%m-%d_%H%M')}_{n:02d}_{slug(desc)}.md"
        if kind == "launch":
            head = (f"# Subagent brief {n}: {desc}\n\nLaunched {when.strftime('%Y-%m-%d %H:%M:%S')} UTC; model option "
                    f"requested: `{model}`; subagent type: `{stype}`.\nThe text below is the prompt exactly as sent by "
                    f"the coordinator (exported from the session transcript on 6 Oct 2026, session 13).\n\n---\n\n")
        else:
            head = (f"# Follow-up message {n}: {desc}\n\nSent {when.strftime('%Y-%m-%d %H:%M:%S')} UTC to agent "
                    f"`{to}` (a resume or an added instruction to an agent launched earlier; the agent's brief is the "
                    f"launch file it belongs to).\nThe text below is the message exactly as sent (exported from the "
                    f"session transcript on 6 Oct 2026, session 13).\n\n---\n\n")
        (out / fname).write_text(head + text + "\n", encoding="utf-8")
        rows.append(f"| {n} | {when.strftime('%Y-%m-%d %H:%M')} | {desc} | `{fname}` | `{model or 'follow-up'}` |")
    print(f"{len(items)} items -> {out}")
    if not dry:
        readme = OUT / "README.md"
        s = readme.read_text(encoding="utf-8")
        missing = [r for r in rows if r.split("|")[1].strip() + " |" not in {x.split("|")[1].strip() + " |" for x in s.splitlines() if x.startswith("| ")}]
        if missing:                      # a later run appends only the rows not yet in the index
            s = s.rstrip("\n") + "\n" + "\n".join(missing) + "\n"
            s = s.replace("Exported from the session transcript in session 11 (4 Oct 2026).",
                          "Exported from the session transcript in session 11 (4 Oct 2026) and, from brief 45 on, in "
                          "session 13 (6 Oct 2026; follow-up messages to running agents included).")
            readme.write_text(s, encoding="utf-8")
            print("README rows appended:", len(missing))
    else:
        print("\n".join(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main("--dry-run" in sys.argv))
