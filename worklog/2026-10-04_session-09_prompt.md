# Session 09: the owner's message (verbatim, as received)

Received 4 Oct 2026 at 08:42:11 UTC (from the session transcript's timestamps; the first tool call followed at 08:42:40).
Preserved here at 08:44 UTC, before any change was made, so that nothing in it depends on a later summary.

The session's model was switched by the owner to Fable 5.1 immediately before this message.

~~~~text
Let’s start the AI integration and make substantial working progress.
First read the latest work log, my previous prompt, the current code and outputs and the blind-02 results. Our references remain the original brief, volumes, both addenda and correspondence. Preserve my confirmed readings, agreed interpretations and labelled assumptions. Don’t invent missing facts or resolve open questions for me.
Use Fable 5.1 to coordinate, with Opus 5.5 for focused implementation and review, where available. If this enviroment cannot select those models, tell me what is actually running. Keep the application’s model choices configurable.
Give me a short implementation sequence, then proceed. Ask early about anything material you cannot establish, including credentials or a spending limit while continuing independent work. Don’t stop at another proposal or just a collection of instruction files.
1. Tighten the existing controls first
The latest review found the issues below. Reproduce them with focused regressions before fixing them, and challenge a finding if the evidence disagrees:

* In `rehearsals/blind-02/out-after-fixes/`, A1 correctly changes the PDD to 11:00, but A5 milestones and README still say 14:00. Make the date, time, timezone and effective source flow consistently through the programme, Gantt, marshalling and labels.
* `clarify.check()` accepts missing sources/owner, an “answered” status without answer evidence, and an incorrect clarification cutoff. Enforce evidence-backed response states and the effective cutoff. Unknown answers must stay unknown.
* Moving `VOL-I:T1-1/B`’s source bbox without changing its text leaves the approval binding for `ADD-02/3.1` unchanged. Bind all relevent target/replacement members to their source identity, location and version, not just content. Test this without bypassing evidence-build validation.
* Finish the blind-02 follow-ups: secondary-unit changes missing from `diff`; deleted obligations inside surviving clauses leaving inappropriate activities; cover claims about “unchanged” deadlines, proposal versus bond validity and compound changes; and table/index entries described in prose.
* Seperate document refusal, criterion-level zero marks and proposal rejection. Preserve supported mandatory-compliance gates without inventing automatic disqualification.
* `gantt.py` replaces non-ASCII text with question marks. Address this before claiming Arabic output support.

Keep the repairs general and focused. Reconcile stale current-status documentation without rewriting historical results.
2. Build AI around the existing engine
The model should retrieve evidence, reason and propose changes. Deterministic code must own calculations, dates, comparisons, validation, state transitions and publication.
Implement one shared, typed contract for claims and change proposals: tender/state identity, statement type, document/page/clause, exact supporting spans/cells/crops, previous and proposed values, dependencies, conflicts, missing information and validation results.
Keep facts, assumptions and interpretations seperate. The controller—not the model—assigns verification status. A valid quotation or JSON response does not prove an interpretation. Prefer “insufficient evidence” over completing a plausible answer.
Expose narrow tools for evidence search, clause/table/crop retrieval, complete state comparison, approved calculations, amendment simulation, programme simulation, validation and review requests. Reuse the current modules and register.
Models may write proposals to staging only. They must not approve themselves, edit source evidence, change validation policy, execute arbitrary generated code or publish accepted outputs. Preserve the current review gates; don’t bulk-approve the pending rows or operations.
3. Make the same application usable through all four routes
Implement a common CLI/service and controlled MCP interface usable by Claude Code and Codex, plus application adapters for an OpenRouter key and local Ollama. Add a direct provider adapter if needed for the selected models.
Distinguish a coding host using its own model from the application making paid API calls. Avoid accidently running two orchestrators for the same task.
Check capabilities for the actual model/provider/endpoint: images, structured output, tools, context and retention. Don’t assume API compatibility or silently fall back to weaker behavior. Include bounded retries, timeouts, concurrency and spending controls.
Provide a fake/recorded-response adapter for offline tests, but don’t present that as a working live integration. My local target is an M5 Pro MacBook with 48 GB unified memory. Choose a realistic Qwen candidate and bounded context; don’t claim local performance without measuring it. Cloud access to my Mac’s localhost must not be assumed.
Ask for secure credential configuration when needed; never put keys in chat, logs or Git.
4. Make unfamiliar addenda the main end-to-end demonstration
The workflow should answer “what changed from the previous tender state?” across requirements, dates/times, quantities, technical/commercial conditions, forms, tables, authority and relationships.
Account for every provision, including notes and images. Retrieval alone is not completeness. Propose targets with evidence, simulate supported changes and propagate their effects through A1–A5, stale decisions and clarification items. Retain the last validated state when processing is partial.
Unknown structures or unsupported change types must remain visible and escalate. Don’t turn them into guessed operations or runtime-generated code.
Preserve Arabic source text separately from translation and matching text. Retain table relationships, units, headings and notes, and check actual rendered RTL output. Keep the maxima/range ambiguity and missing Permit unresolved.
5. Demonstrate and report actual progress
Deliver a working evidence → AI proposal → validation → impact → review workflow, not just adapter stubs. Test malformed responses, fabricated citations, numerical changes, prompt injection, stale evidence, rejected operations, provider failure and budget exhaustion.
Run the relevent regressions and full suite. Then use a new independently authored addendum with a sealed answer key through the normal path; blind-02 is now regression material. Distinguish pre-key results from later fixes, and include unresolved items and human review time.
Log actual models, prompts, tool calls, evidence, errors, validations, usage and decisions, including Codex-assisted review. Report mocked, recorded, live API and actual local testing seperately.
Come back with a compact implementation report, runnable commands for each route, measured results, remaining defects and the specific inputs you need from me. Keep A1–A5 and the offline rebuild intact. Don’t send any clarification questions externally.
Do not commit, push or rewrite Git history until I explicitly authorize it. Leave the changes uncommitted. When authorized, the next commit title must start with `AI IMPLEMENTATION START`.
~~~~
