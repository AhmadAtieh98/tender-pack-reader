# Session 12: the owner's message (verbatim)

Received 5 Oct 2026, about 09:14 UTC, after the session 11 commit `6053493` (committed and pushed at 08:20 UTC on the owner's one-word authorisation "commit").

---

Let's continue and get this ready to run and submit. I want substantial working progress, with correctness and the live addendum exercise taking priority.
Read the latest report, work log, current code and blind-05 comparison first. Our main references are still the original brief, emails, volumes, ADD-01 and ADD-02. Preserve my recorded decisions and confirmed readings, keep assumptions labelled and unanswered questions open. Costs stay provisional.
Use Fable 5.1 to coordinate, with Opus 5.5 agents for focused implementation and independent review where available. Use other models where useful, but record what actually ran. Give me a short sequence first, then proceed. Ask me about any material uncertainties while continuing everything that doesnt depend on my answer.
1. Close the legal/commercial review gap
Section 6 of the brief requires people to own legal and commercial judgments. Extraction and calculations can run automatically, but the system must not make or settle those judgments itself.
The latest review reproduced two problems in ai/downstream.py:

* An issue claiming that all concession-term conflicts are resolved received evidence_verified just because it included a genuine Q7 quotation.
* An existing CQ-CONCESSION-TERM entry could become "answered by addendum" or "withdrawn (not sent)" without a human decision. The draft-only restriction currently applies only to new clarification IDs.

These are still candidate changes, not actual human approvals, but they can still be misleading to someone reading the results.
Write failing regressions and fix this across proposals, issues, clarifications and rendered outputs. Valid evidence should not automatically validate the conclusion. Legal/commercial interpretations, precedence disputes, waivers and decisions to close an ambiguity must stay visibly human-owned, regardless of the model's labels. Recording an answer in an addendum is different from declaring that the answer resolves the question.
Keep deterministic facts and calculations usable. Require an explicit recorded human decision before presenting a human-owned question as settled. Preserve candidate isolation and the existing approval restrictions.
2. Finish the unseen-addendum workflow
Blind-05 detected much more than it successfully carried through into the outputs. Use that comparison as regression material and fix the underlying limitations:

* Replacements split across clauses/list items, including obligations referring to units introduced by the same addendum.
* Complete clause-list/range targeting: citations.py currently reads "29.1 to 29.3" as only the two endpoints and rejects 29.2, even when that clause exists. Resolve ranges against the document structure, or flag incomplete scope.
* Cover discrepancies holding up otherwise clear operative changes: use the pack's actual authority rules, retain the discrepancy and distinguish it from a genuine unresolved conflict.
* Image-table readings feeding proposed requirements and activities while human sign-off is still pending.
* Calculated deadlines reaching A1/A5, conditional obligations and indirect effects reaching affected rows, and superseded answers being reconsidered.
* Confirmations producing false CHANGED/REWORK signals, broken issue references, and clarifications being suggested without acknowledging that their submission window has already closed.

Keep Arabic, translations, crops, table headings, units and notes traceable. Preserve the maxima/range ambiguity and missing Environmental Permit. Don't invent an interpretation or rejection consequence just to complete the workflow.
Support unexpected changes through evidence and controlled state transitions, not rehearsal-specific answers. Keep useful candidate A3/A5 results seperate from the last structurally validated state, and show approval status separately.
The latest rehearsal took 72 minutes against the 30-minute exercise. Reduce unnecessary sessions and repeated context, improve batching and task routing and test bounded concurrency only where safe. Keep rate-limit handling, checkpoints and selective criticism. Don't weaken checks or count manual YAML edits as automation.
Rerun blind-05 as a labelled post-key regression, then use a genuinely new independently authored addendum with its key inaccessible until the outputs are frozen. Report detection, usable updates, missed effects, pending decisions, interventions and total time separately. Also verify consecutive addenda and interrupted-run recovery.
3. Make the Mac version genuinely runnable offline
My machine is an M5 Pro MacBook Pro with 48 GB unified memory. Ollama and local models are already installed. OpenRouter keys will come later.
There is a specific offline problem: config/ai.yaml selects a host critic, and _critic_route can still choose Claude during an Ollama run. Fix this with an explicit offline mode covering every phase, including criticism, repairs and capability checks. There must be no hosted calls or silent provider fallback. Use a suitable local critic, or clearly show the review that could not run.
Provide a straighforward Mac setup and launcher. After setup, the deterministic build, exports and local interface must work without internet or an API key. Local AI should use the available Ollama models after checking their capabilities, context limits and practical memory requirements. Don't assume a model supports images or tools, and don't download large models automatically.
Keep Claude Code, Codex, OpenRouter and Ollama using the same validation rules. Distinguish connected coding-host routes from offline local inference. Don't describe automated Codex execution as tested if only its MCP interface was tested.
Test locally where you actually have access. If you're still in the cloud, prepare the exact Mac checks for me and mark them pending. Cloud access cannot reach my Mac's localhost, recorded responses are tests not proof of a working live integration.
4. Independently audit the real submission through ADD-02
After the core fixes, assign independent reviewers who derive expectations from the brief, emails and original PDFs before they look at the outputs. Keep synthetic addenda separate.
Check:

* A1: completeness, evidence, Excel/CSV/JSON agreement, original versus amended text, and status at every stage.
* A2: every provision, full amendment chains, deletions, reinstatements, indirect effects and earlier answers that became wrong.
* A3: only supported bid-out consequences, confidence, and unresolved matters with understandable reasons on the page. Check actual readability, not just whether it technically fits.
* A4: authentic prompts, model/tool calls, errors, corrections and development history.
* A5: activities derived from A1, requirement coverage, backward dates, calendars, dependancies, owners, resources, marshalling, assumed lead times, infeasibility and agreement with the Gantt.

Inspect the rendered PDFs, Excel and browser views, including Arabic and source links. Reconcile findings, fix defects and independently recheck the affected areas. Update the requirement-to-artifact matrix with evidence and pass/fail/pending results.
Bring me the remaining decisions in manageable groups, with the source, proposed interpretation and practical effect. The 205 rows and 37 operations still awaiting recorded acceptance must not become approved just because tests pass. Preserve existing image approvals, don't silently reapprove changed files.
Prepare the factual A4 history-disclosure correction identified in session 11 for my review, without rewriting history or restoring wording I previously asked to remove. Keep clarification questions as drafts about package discrepancies, ambiguities and missing material. Send nothing externally.
5. Then build the simple local control panel
Once the core corrections and audit are finished, assign an agent to build a small practical localhost interface using the existing engine and workflow.
The brief allows an interface for working with the artifacts but rejects a dashboard product replacing them. This is my operating panel, A1–A5 remain the deliverables. Keep it plain, with no product branding or multi-agent presentation.
I want to:

* Run the build and checks, and open/download A1–A5, Gantt, clarification register and review packets.
* Select BASE, ADD-01, ADD-02 and later stages, compare changes and open their sources.
* Upload the live ADD-03 PDF, select the available processing route/model and start ingestion.
* See progress, failures and pending questions, then resume interupted work.
* Review candidate results without overwriting earlier stages or confusing them with approved results.

Use real backend jobs, not demo buttons. Preserve versioned outputs and isolate rehearsal data. Clearly seperate execution, completeness, structural validation and human approval. Human decisions must be explicit and recorded.
Keep uploads and model-produced text safely handled, bind the interface locally and keep credentials out of files and logs. Test the full upload-to-results flow and output parity after adding the interface.
6. Finish with a usable handover
Run focused regressions, the full suite on the final code, a fresh rebuild, the strict check and the offline checks available to you. Keep failed checks and genuine approval blockers visible.
Prepare a runnable working-tree review package without committing. The existing archive script requires a clean commit, so preserve that release safeguard and provide a separately labelled snapshot with its base revision, uncommitted-change disclosure and file manifest.
Also fix the archive's hardcoded blind-01–03 list so the relevent blind-04/05 and newer evidence is included. Check that setup dependencies, instructions, links and outputs match the version actually packaged.
Finish with a compact report covering what works, what changed, actual verification, remaining blockers, how I launch it and the specific decisions you need from me. Update the operating instructions and work log honestly.
Leave everything uncommitted. Do not commit, push, amend or rewrite history until I explicitly authorize it.

(Typographic note: curly apostrophes and quotation marks in the owner's message were straightened when the text was pasted; the words, spelling and line breaks are otherwise unchanged.)
