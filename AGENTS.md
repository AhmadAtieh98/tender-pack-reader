# Coding-agent instructions

This repository reads and reconciles the LAMAR PPP R2 tender pack. For the current implementation, operating procedure, verification evidence and remaining work, read **docs/INTERVIEW_DEMO_HANDOVER.md** before making changes. Claude Code should use the same handover.

- Preserve `worklog/` without adding or editing entries. Repository documentation must describe technical state, not reproduce conversation transcripts or verbatim user messages.
- Keep runtime session captures, generated prompts, credentials and private local artifacts out of commits. Stage explicit implementation files rather than the entire working directory.
- Simulated approvals belong only in an explicitly enabled disposable interview-demo copy. They never settle missing evidence, genuine document conflicts or interpretation choices. Keep ordinary source curation and real approvals separate.
- Reproduce a software defect with a failing regression before fixing it. Verify the affected behavior and retain explicit unresolved states.
- Run `scripts/mac/checks.sh` and `scripts/mac/pathlink.py` only in a disposable packaged copy, never in a Git worktree.
- Preserve code-identity checks on resume. A run measured before a code change is not a timing measurement of the new version.
- Commit or push only with explicit authorization for that action. Never rewrite remote history as part of routine continuation.
