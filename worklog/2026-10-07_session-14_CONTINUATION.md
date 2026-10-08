# Session 14: continuation instructions for Codex or any other agent (final, 8 October 2026)

**Purpose.** The owner asked that work can continue in Codex, or any other agent, exactly where this session stopped. This file is that handover. `AGENTS.md` at the repository root points here. The session ended at the closing commit `1413457` on branch `claude/hopeful-curie-7oki9q`; this file was last updated by the commit after it.

## 1. Where the session stopped

**Every part of the owner's session-14 brief is done.** Nothing is half-finished in the tree, and no background job, worktree or agent is left running.

| Item | State | Where |
|---|---|---|
| The brief, verbatim, with the owner's later messages | read first | `worklog/2026-10-07_session-14_prompt.md` |
| The report: before/after, rechecks, rehearsals, verification, package | final | `docs/session-14_report.md` |
| The decisions that need the owner (software failures, missing evidence, human approvals) | final; nothing decided | `docs/session-14_review_packet.md` |
| The work log: timeline to the minute, models that ran, errors E166–E174 | final | `worklog/2026-10-07_session-14_finalisation.md` |
| Every error of every session, one line each (183 entries) | final | `worklog/ERROR_INDEX.md` |
| Every subagent brief, verbatim (116–151 for this session) | exported | `worklog/subagent_briefs/` |
| Reviews, briefs, decisions raw, patches, logs of this session | kept | `worklog/continuation-s14/` |
| Blind-07 regression (open key) | scored: 18 hit / 14 partial / 1 missed of 33 | `rehearsals/blind-07/regression-s14/COMPARISON-S14.md` |
| Sealed blind-08 (frozen by hash before the key was opened) | scored: 29 / 28 / 6 of 63; 45.0 min against 30 | `rehearsals/blind-08/COMPARISON.md`, `FROZEN.md` |

**Verification at the close, on the final code:**

- The full suite: 1,575 passed, 1 skipped, 0 failed (73 min in the cloud container).
- The closing chain: green; `out/` byte-identical to the chain on the frozen code; strict exit 3 with only the two approval blockers (expected until the owner approves).
- The interview package `LAMAR-PPP-R2-INTERVIEW_be97bec+wt_20261008T0944Z.zip`: `scripts/mac/verify_package.sh --no-ai` 8 PASS on the packaged copy; its full focused tests 594 passed. The zip was sent to the owner. It is not in the repository; rebuild it with the command in §2.

**Post-freeze code changes.** E173 (the word-based reach by stage, `tenderpack/programme.py`) and E174 (the output reservation, `tenderpack/ai/requests.py`) were made after the blind-08 run was frozen; the run did not use them. E174 has not met a real Ollama yet.

## 2. How to pick up

**Environment in a fresh clone** (Python 3.11 or later):

```
bash scripts/mac/setup.sh          # builds .venv from the lock (uv if present, else venv + pip)
.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_session14_*.py     # about 10 min here
```

**The commands the session closed with** (each writes its temporary files under `$SCRATCH`, default `/tmp/tenderpack-s14`):

```
bash worklog/continuation-s14/scripts/run_suite.sh > suite.log 2>&1          # the full suite, about 73 min
bash worklog/continuation-s14/scripts/rebuild_chain_final.sh                 # ingest, outputs, drill, strict, check-register, diff, Mac checks
.venv/bin/python scripts/make_interview_folder.py <dir> --label "<text>"     # the package (folder + zip)
bash scripts/mac/verify_package.sh <zip> --into <dir> --no-ai                # its self-verification: expect 8 PASS
```

Never run `ingest` alone; run the whole chain. Never run `scripts/mac/checks.sh` or `scripts/mac/pathlink.py` from a git worktree (they rewrite the shared `.venv`'s path file). The other scripts in `worklog/continuation-s14/scripts/` are records of how the session ran its rehearsals; several hold the cloud container's absolute paths and need them changed before reuse.

**What is next is the owner's, not an agent's:**

1. The decisions in `docs/session-14_review_packet.md` (groups B and C), recorded by the owner through the panel's decisions form or `tenderpack approve`. An agent never records them.
2. The checks marked PENDING ON THE MAC in `docs/MAC_CHECKLIST.md`, among them the first real Ollama run since E174.
3. Known software gaps the owner may ask to fix next: packet group A rows marked KNOWN or found by blind-08 (A10, A12: the clause-level consistency check, derived arithmetic and dates, items lost when batches combine, the resume asking one batch twice, too many pending markers; the 30-minute target, packet C13).

If the owner asks for new work, start a new session log (`worklog/<date>_session-15_<topic>.md`), keep the owner's message verbatim beside it, and follow §3.

## 3. Standing constraints (the owner's, in force for any continuation)

Never approve, accept or reject anything on the owner's behalf; never create `curation/reviews/decisions.yaml`; never edit `curation/approvals.yaml`, `curation/readings/`, `curation/reading-snapshots/`; keep the two source-image approvals as transcription approvals only; keep "at all times", programme readiness, the Permit and the maxima/ranges pending; clarification questions stay drafts; durations and bidder settings stay labelled assumptions; no new amendment language; a failing test first for every fix; no model identifiers in code comments beyond "session 14" or in commit text beyond the attribution trailers; nothing sent externally; no credentials in files, logs or chat; agents never write in the main tree and never run git writes; never run `scripts/mac/checks.sh` or `scripts/mac/pathlink.py` from a worktree (they rewrite the shared `.venv`'s `tenderpack-folder.pth`; it must name the main tree); the runtime model for rehearsals is chosen and recorded separately from the development agents (work log §4); costs provisional; never mark unresolved work complete; never invent answers; a rehearsal's host sessions count as agents against the plan limit (E169).
