# Subagent brief 132: F1 fixes for A1/A2 findings

Launched 2026-10-07 17:42:39 UTC; model option requested: `opus`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 8 Oct 2026, session 14).

---

You are fixer F1 of session 14 (a first launch of you was stopped by the plan's rate limit minutes after it started; nothing of it survives: your worktree's `git diff` is empty and your scratch folder does not exist, so start from the brief). Read and follow your brief at /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s14/briefs/F1.md (it points to the fixers' common brief, the reviewer's report, your worktree /home/user/wt-s14-f1 and your scratch folder). Your worktree's git INDEX already holds the merged session-14 baseline (the main tree's uncommitted work), so `git -C /home/user/wt-s14-f1 diff` shows exactly your own changes; new files you create are untracked and must be listed. Never commit, never run any git write command in the main tree /home/user/tender-pack-reader, never edit the main tree, never run scripts/mac/checks.sh or scripts/mac/pathlink.py. Export PYTHONPATH=/home/user/wt-s14-f1 for every python command so the code under test is yours. End with the final message the common brief asks for (at most 40 lines) and the path of your patch.
