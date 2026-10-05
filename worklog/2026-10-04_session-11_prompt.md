# Session 11: the owner's message (verbatim)

Received 4 Oct 2026, about 18:27 UTC, after the session 10 commit `a57f118`.

---

Continue from session 10 and everything I've already instructed before. I want to make real, substantial progress now on the AI-assisted unseen-addendum workflow, and once that is working properly, do a thorough audit of the real submission through ADD-02.

Start by reading the latest work log, session-10 report, blind-04 comparison and the current code. The original brief, volumes, ADD-01, ADD-02 and correspondence are still the main references. Keep all of my confirmed readings, decisions, labelled assumptions and unresolved questions exactly as they are. Cost work should still stay provisional.

Use Fable 5.1 to coordinate the work, with Opus 5.5 agents used for focused implementation and independent review where they're available. Record which models actually run, not just what was requested. Give me a short sequence of what you're going to do and then proceed with the work. If you find a material uncertainty, raise it with me and show me the relevant evidence/options, but keep progressing on everything else that doesn't depend on my answer.

1. Finish the downstream workflow properly

Blind-04's post-key resume produced 57 downstream items, but the candidate build then failed because a new ADD-03 requirement was being treated as if it had already existed from BASE.

Fix the way requirement introduction and applicability are handled so this is explicit and supported by evidence. Don't make checks pass by simply changing citation order. Any proposed row should be validated across all of the stages where it is relevant before it can be promoted.

The review also reproduced a few specific problems that need to be fixed properly:

- ai/downstream.py is finding rows through literal YAML indentation. That means rows created by its own serializer can later be missed when another addendum tries to update them. Move this to proper structured, ID-based updates.
- ai/workflow.py can say the workflow is complete even when downstream batches failed, tasks are still unanswered, or C46 findings remain. Completion needs to reflect downstream coverage and candidate checks. Execution status, completeness and human approval should remain seperate things.
- ai/tools.py can load a changed register but still keep the same proposal fingerprint. The state bindings need to include the relevant register, interpretation, relationship and other curated inputs. Then revalidate the combined proposals immediately before promoting the candidate.

For each of these, reproduce the problem first with a failing test, then fix it.

Also add a consecutive-addenda test where a requirement is introduced, later changed, removed, and then reinstated. The full history, supporting evidence and related activities need to survive through all of those states.

I also want a succesful host-driven run where AI-generated rows, interpretations, issues, evidence items and activities actually reach a usable candidate build. If there is any manual intervention along the way, record it honestly. Manually writing YAML should not be counted as an automated success.

2. Make the AI phases follow the same controls

Right now analysis, image reading and downstream generation are going through different request paths. The review found that workflow._converse is missing native response schemas, has incomplete context accounting, and doesn't explicitly require image capability for the reading phase.

Bring these paths under the same safeguards.

That means using the correct task schemas, validating locally, checking modality/capabilities, enforcing complete request and context limits, using bounded response repair, and making capability notices visible. If something is too large for the allowed context, split it safely or escalate it clearly. Do not silently squeeze or truncate important content.

Host rate limits, provider failures and malformed responses should also be handled differently because they're not the same failure. Add bounded backoff and resumable checkpoints so batches that already succeeded don't have to be run again. Reduce repeated context and unnecessary sessions as well, and dont assume that throwing more concurrent Opus calls at the problem will fix rate limiting.

The selective critic should become part of the workflow for the cases that actually matter: consequential interpretations, uncertain targets, removals and conflicting evidence. Its findings need to stay visible. If the critic and primary agent agree that still does not mean the result is approved.

Keep Claude Code/Codex, OpenRouter and Ollama working through the common workflow. If credentials aren't available, or my Mac isn't available for a local run, continue with whatever host/offline implementation can still be done. Just make it clear which routes were actually tested and which are still unverified.

3. Extend the reasoning, but keep calculations and dependencies controlled

Add narrowly defined deterministic tools for the missing calculation types: percentage, threshold, ratio, cap, unit conversion and approved formula calculations.

Every calculated result should carry the source operands, units, formula or approved method used, assumptions and input version. If a formula is not supported, or an input is missing, leave it unresolved. Never execute model-generated code.

Relationship discovery and propagation also needs to go beyond the few curated examples we have now.

The review found that relationships.trace() silently stops after four links. That is dangerous because the system can make an indirect chain look complete when it isn't. Replace this with cycle-safe traversal and explicit completeness reporting.

There is also another issue where missing-document blockers can disappear when a requirement is only reached indirectly. Those blockers need to propagate through the relationship chain instead of getting lost.

Support conditional amendments and effective-dated amendments as well, including an amendment that later amends an earlier amendment. This needs to preserve the trigger, applicability, alternative states, affected obligations and any related decision milestones.

Do not assume that a trigger occured. And don't rewrite the historical state just because a later state supersedes it.

Also distinguish between an answer that simply confirms what was already required and an answer that actually changes the requirement. Use the critic here as well, especially to challenge misleading cover wording. For example, if a numerical change is described as "relaxing" a requirement, the system should check whether the actual numbers support that statement instead of repeating it.

4. Make partial results useful, and show that the workflow is actually improving

Keep the last validated outputs intact, but also produce clearly labelled candidate A3 consequences and A5 programme impacts as the new addendum is processed. These should show blockers and conditional scenarios as well.

Even if an addendum is only partially processed, I still want a useful explanation of what may be changing. Partial should not mean useless.

Keep the source crops, Arabic text, translations, relationships between tables, units and review notes available. The maxima/range ambiguity needs to stay unresolved unless the evidence genuinely resolves it, and the missing Environmental Permit should remain visible.

Use blind-04 as post-key regression material.

After that, run another addendum which is independently authored, with the answer key kept inaccessible until the first outputs have already been frozen. I want this to be a proper unseen test rather than another test where the implementation can indirectly drift toward the answer.

Measure the time from receiving the PDF to producing a working update, and compare it against the brief's 30-minute exercise.

Report the detection results, missed effects, unresolved decisions, manual interventions and review effort seperately. Also include an interrupted or rate-limited run, then demonstrate that it can resume successfully without losing the work that already passed.

Do not weaken validation just to hit the 30-minute target.

5. After that, have Fable orchestrate the final deliverable audit

Once the implementation work is done, use Fable to coordinate an independent audit of the real package from BASE through ADD-02 only. And the emails

Synthetic ADD-03 and ADD-04 material must stay completely separate from this audit.

Fable should assign independent Opus reviewers, plus any other relevant specialists where useful. Where practical, the reviewers should be different from the agents that implemented the affected areas.

I don't want them simply checking whether the files look internally consistent. Each reviewer should first derive what they expect from the original brief, correspondence and source documents, and only then compare that against the produced outputs.

The audit needs to cover all five deliverables:

- A1: Check source-to-register completeness and whether every row is properly supported by a source. Review all stage statuses, original versus amended evidence, dates, assumptions and interpretation boundaries.
- A2: Check every addendum provision, note, table, form and image. Make sure the full amendment chain is preserved, including superseded answers and indirect effects.
- A3: Check that rejection, disqualification and non-responsiveness triggers are genuinely supported and correctly distinguished from one another. Unresolved issues should be readable with the reason visible directly on the page. The current condensed issue IDs need specific attention because a linked detailed explanation may not be enough for the brief. Deduplicate overlapping issues before shrinking the text.
- A4: This should show the actual development history: prompts, model/tool calls, errors, corrections and how the work developed. The clarification register can support this, but it is not the whole work-history deliverable.
- A5: Check requirement-to-activity coverage, backward planning, calendars, fixed versus relative dates, durations, dependencies, resources, marshalling, infeasibility and consistency between the data and the Gantt charts.

Also inspect the actual rendered Excel and PDF outputs, not only the underlying data. Check Arabic rendering, tables and cross-document consistency as well.

There are also stale statements that need to be corrected if they're still present, particularly anything saying the confirmed image readings are still waiting for approval, or saying that the approvals file doesn't exist when it does.

Produce a brief-requirement-to-artifact audit matrix showing the evidence and a clear pass/fail/pending result for each requirement.

Where reviewers disagree, Fable should reconcile the disagreement, arrange the fix if needed and then have the affected area independently rechecked. Keep the agent orchestration behind the scenes though; the actual deliverables should remain A1–A5, not a collection of agent reports.

Finally, run the relevant regressions, the full suite, a fresh rebuild and the strict check.

Keep genuine human-approval blockers seperate from actual defects. Do not approve pending rows or operations just to make the result green.

When everything that can be done is done, return the working outputs, runnable commands, audit findings, fixes that were made, verification results and the specific remaining decisions that genuinely need my input.

Keep the work log accurate and honestDo not invent answers,

Leave all new changes uncommitted. Do not commit, push, amend or rewrite history until I explicitly authorize it.

(Typographic note, added in session 11 after the audit's finding A4-11: curly apostrophes in the owner's message were straightened when the text was pasted; the words are otherwise unchanged.)
