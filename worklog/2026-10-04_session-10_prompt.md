# Session 10: the owner's message (verbatim)

Received 4 Oct 2026, about 13:33 UTC, after the session 09 commit `a41e104` (the message was also attached as an image of the same text). The session's model remained Fable 5.1 for the coordinator.

---

Continue from the latest commit, while preserving any later work that is already present

The priority now is to complete the AI-assisted unseen-addendum workflow, starting from receiving a PDF all the way through to producing a sourced, reviewable A1–A5 working update. Continue following my earlier instructions. Leave cost analysis and pricing provisional for now.

Before doing anything, read the latest work log, session-09 report, blind-03 results and the current implementation. The brief, volumes, original addenda and correspondence remain our references. Preserve all my confirmed readings and decisions, labelled assumptions, and unresolved questions.

Use Fable 5.1 to coordinate with Opus 5.5 for focused implementation and independent review where availble; record what actually runs. Give me a short implementation sequence first, then proceed with the work. If there are material unknowns, ask me early and explain the evidence, options and why the answer matters, while continuing any independent work you can do in parallel.

1. Fix the controls that could undermine unseen-addendum analysis

my review reproduced the gaps below. Verify each one with a failing regression before fixing it, and challenge any finding if the actual evidence contradicts it.

- In ai/controller.py, marking all 40 ADD-02 provisions as no_effect, using genuine quotations but unsupported "no change" explanations, currently produces complete, evidence_verified and an APPLIED simulation with no changes. These labels are not the same as human approval, but substantive no-effect decisions still need comparable evidence-bound review safeguards. Prevent real amendments from disappearing through this path. Keep coverage, evidence verification, semantic resolution and approval as seperate concepts.
- In register.py, the removal validator accepts removal of the surviving Financial Model submission obligation when the operation actually deletes only the auditor-opinion requirement from the same clause. Require evidence for removal of the particular obligation being removed, while preserving any surviving requirements and activities.
- In ai/tools.py, changing calendar assumptions can alter a deadline without changing the proposal's state identity. A running workspace can also return a changed crop together with its cached old transcription without detecting the integrity failure. Bind proposals and calculations to the relevant inputs, keep evidence reads within a verfied version, and recheck freshness before promotion.
- clarify.check() currently accepts an empty source quotation and a whitespace-only owner. Reject both.

Keep these fixes general and focused. Don't overfit them specifically to blind-03.

2. Complete one runnable, resumable workflow

I should be able to give the system a new addendum PDF together with the preceding tender state and receive:

ingestion → AI analysis → sourced proposals → deterministic validation → downstream impact → isolated candidate outputs → human review

The workflow needs to account for every provision, including tables, notes, forms, images and cover statements. It should identify what changed, what remains unchanged, what conflicts and what cannot be determined from the evidence.

Finish and properly exercise the existing row_reading, row_new, issue and clarification paths. Add structured proposals for evidence items, activities and dependencies only where those are currently missing. The AI should draft the downstream work that the blind-03 curator previously had to write manually.

Validate the full combined proposal set inside a disposable candidate workspace, including interactions between operations and any dependent proposals. From that workspace produce working:

- A1 Excel
- A2 changes
- A3 consequences
- A4 audit records
- A5 schedule / Gantt / marshalling updates

Support checkpoints and resumption so a stopped run can continue without silently skipping or duplicating provisions. Preserve the last validated state. Candidate outputs must clearly distinguish between proposed, unresolved and approved information.

Unknown change types must escalate with their evidence and affected scope, rather than being forced into a known category.

3. Follow indirect effects through the tender

Address the blind-03 gaps using reusable, evidence-backed relationships rather than one-off rules.

In particular:

- membership changes affecting qualification evidence, weighting and member declarations;
- effluent-limit changes affecting reliability testing and contractual obligations;
- Ramp-Up/payment changes requiring Financial Model and Form 4-F review;
- missing referenced documents, including Schedule 11, appearing against the conclusions they prevent us from establishing.

Trace effects across requirements, calculations, deliverables and activities. Distinguish confirmed dependencies from proposed relationships and possible impacts. Do not silently accept AI-inferred links just because they seem reasonable.

Keep durations and bidder configuration clearly labelled as assumptions. Preserve the maxima/range ambiguity and the missing Environmental Permit.

For Arabic and image tables, retain the source crops, original text, seperate translations, cell relationships, units and notes. Rendered output should also remain available for human review.

4. Make the existing AI routes support this workflow

Continue using the shared Claude Code/Codex interface and the OpenRouter/Ollama adapters.

Exercise an actual host/MCP session where available, including images and proposal submission.

Fix the capability verification path where it currently falls back silently to unverified configuration. Use supported native structured outputs alongside our own local validation.

For larger tasks, use bounded batches and checkpoints while accounting for the full request context and the provider's output limits. Don't solve context or output-limit problems by silently dropping parts of the tender.

Use an independent critic selectively for consequential interpretations, removals, conflicts and uncertain targets. Agreement between models is not approval.

Continue host/offline work when credentials or my Mac are unavailable. Report these seperately:

- recorded tests;
- host execution;
- live API execution;
- measured local execution.

Cost work should not hold up this phase.

5. Demonstrate meaningful progress

Blind-03 took 50 minutes 31 seconds before the subsequent human review. The target now is to produce a useful candidate update, impact explanation and replan within the brief's 30-minute unseen-addendum segment.

Measure against that target, but do not weaken checks or claim human sign-off just to meet the timing.

Run the regressions and the full test suite. Make the tests generate disposable evidence fixtures instead of relying on ignored rehearsal build folders.

After that, run a fresh, independently authored addendum through the normal AI workflow. Its answer key must remain inaccessible to the procesing agent until the first outputs are frozen.

The new addendum should include:

- unfamiliar changes;
- indirect effects;
- misleading summaries;
- missing evidence;
- Arabic/image content.

For each significant change demonstrate the complete chain:

source evidence → proposed transition → validation → downstream impact → output difference

Record every manual intervention.

Report detection results, missed impacts, unsupported proposals, unresolved decisions and timings honestly. Keep the pre-key results clearly seperate from any fixes or improvements made after the answer key becomes available.

At the end return the runnable workflow, candidate outputs and review packets, along with a compact implementation report, remaining limitations and the specific inputs needed from me.

Keep the work log accurate . Do not invent answers, approve anything on my behalf

Most importantly: leave all new changes uncommitted. Do not create another commit, push, amend or rewrite history until I authorize it.
