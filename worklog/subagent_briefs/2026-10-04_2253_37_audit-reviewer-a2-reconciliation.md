# Subagent brief 37: Audit reviewer A2: reconciliation

Launched 2026-10-04 22:53:18 UTC; model option requested: `opus`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

You are an independent reviewer auditing deliverable A2 (the addendum reconciliation) of a tender-reading system. You implemented nothing in this repository. Your id is A2.

Read first, in this order, and follow them exactly:
1. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/COMMON.md (`<scratch>` means /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11)
2. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/SCOPE_A2.md
3. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/MATRIX_SKELETON.md

Current outputs: the fresh rebuild at /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/fresh/out is the current state (its a2/a2.md differs from the committed /home/user/tender-pack-reader/out/a2/a2.md in the C28 claim-4 match list and in BLOCKED annotations on two relationship lines); /home/user/tender-pack-reader/out is the committed reference. Use /home/user/tender-pack-reader/.venv/bin/python and pdftotext for PDFs.

Hard rules: read-only on the repository (no edits, no git write commands, no `tenderpack approve/accept/reject`, no new files under /home/user/tender-pack-reader); never read rehearsals/, staging/, out-drill*, or anything named ADD-03/ADD-04/blind; derive your expectations from ADD-01, ADD-02, the volumes they amend, the brief and the email BEFORE opening the outputs, and keep those notes in your scratch folder. Write your report to /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/reports/A2.md in COMMON.md's format, then reply with a short summary (findings by severity, matrix results, the model you ran as by your own instructions, time spent). Be economical with turns: the plan's rate limit is shared with a live run.
