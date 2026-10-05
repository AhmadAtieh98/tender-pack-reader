# Subagent brief 36: Audit reviewer A1: register

Launched 2026-10-04 22:53:10 UTC; model option requested: `opus`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

You are an independent reviewer auditing deliverable A1 (the obligations and compliance register) of a tender-reading system. You implemented nothing in this repository. Your id is A1.

Read first, in this order, and follow them exactly:
1. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/COMMON.md (the method, boundaries and report format; `<scratch>` in these files means /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11)
2. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/SCOPE_A1.md (your scope)
3. /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/MATRIX_SKELETON.md (the brief-requirement rows you fill for A1 and the general rows named in your scope)

Current outputs: the fresh rebuild at /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/fresh/out (and its evidence build at .../fresh/build) is the current state; /home/user/tender-pack-reader/out is the committed reference and differs only in README.md, a2/a2.md and three a5 files. Use the Python at /home/user/tender-pack-reader/.venv/bin/python (openpyxl, yaml available) and pdftotext/pdftoppm for PDFs.

Hard rules: read-only on the repository (no edits, no git write commands, no `tenderpack approve/accept/reject`, no new files under /home/user/tender-pack-reader); never read rehearsals/, staging/, out-drill*, or anything named ADD-03/ADD-04/blind; derive your expectations from the brief, the email and the six source PDFs BEFORE opening the outputs, and keep those notes in your scratch folder. Write your report to /tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s11/audit/reports/A1.md in the format COMMON.md gives, then reply with a short summary (counts of findings by severity, the matrix results, the model you ran as by your own instructions, and the time spent). Be economical with turns: the plan's rate limit is shared with a live run.
