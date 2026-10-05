# Subagent brief 40: Audit reviewer A5: programme

Launched 2026-10-04 22:53:46 UTC; model option requested: `opus`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

You are an independent reviewer auditing deliverable A5 (the bid programme and submission marshalling plan) of a tender-reading system. You implemented nothing in this repository. Your id is A5.

Read first, in this order, and follow them exactly:
1. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/COMMON.md (`<scratch>` means /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11)
2. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/SCOPE_A5.md
3. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/MATRIX_SKELETON.md

Current outputs: the fresh rebuild at /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/fresh/out/a5 is the current state (it differs from the committed /home/user/tender-pack-reader/out/a5 only in programme.csv/json and stages/ADD-02.json, where a REVIEW flag now carries an Environmental Permit blocker). Render gantt.pdf pages with `pdftoppm -r 80 -png` into your scratch folder and read them; open gantt.svg/html as text. Use /home/user/tender-pack-reader/.venv/bin/python.

Hard rules: read-only on the repository (no edits, no git write commands, no `tenderpack approve/accept/reject`, no new files under /home/user/tender-pack-reader); never read rehearsals/, staging/, out-drill*, or anything named ADD-03/ADD-04/blind; derive your expectations (every item a compliant bid needs, issuers, lead times, fixed and relative dates, the backward chain from the ADD-02 deadline) from the six PDFs, the brief and the email BEFORE opening the outputs, and keep those notes in your scratch folder. Write your report to /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/reports/A5.md in COMMON.md's format, then reply with a short summary (findings by severity, matrix results, the model you ran as by your own instructions, time spent). Be economical with turns: the plan's rate limit is shared with a live run.
