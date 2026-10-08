# Instructions for coding agents (Codex and others)

This repository is a tender-pack reader for the LAMAR PPP R2 tender. Its owner continues work across Claude Code and Codex sessions.

**Start here:** `worklog/2026-10-07_session-14_CONTINUATION.md`. It says where the last session stopped, how to set up and verify, what is next, and the owner's standing constraints. Read it before changing anything.

The owner's rules that apply in every session (the full list is in the handover's §3):

- Never approve, accept or reject anything on the owner's behalf. Never create `curation/reviews/decisions.yaml`. Never edit `curation/approvals.yaml`, `curation/readings/` or `curation/reading-snapshots/`.
- Every fix starts with a failing test.
- Commit or push only when the owner says so. When the owner asks for progress commits, title them "codex continuation: ..." and keep the handover file current.
- Nothing is sent to an external service, and no credential goes into a file, a log or a message.
- Never run `scripts/mac/checks.sh` or `scripts/mac/pathlink.py` from a git worktree.
- Never mark unresolved work complete, and never invent an answer the documents do not give.
