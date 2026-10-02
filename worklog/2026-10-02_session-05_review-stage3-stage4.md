# Session 05: the owner's code review (five findings), Stage 3 (full register) and Stage 4 (A5)

- **Date:** 2 Oct 2026, from 13:31 UTC (16:31 Riyadh); work paused at a usage limit and continued from about 17:30 UTC.
- **Who:**
  - The owner reviewed the code and outputs; the five findings below are the owner's.
  - The assistant (Claude Code, in the cloud container) acted as the single orchestrator: it reproduced the findings, wrote the failing tests, made the code fixes, built the Stage 3 infrastructure, integrated the subagents' work and ran every check.
  - Subagents (each with a written brief, its own files and a validator to run; results checked by the orchestrator):
    - **register VOL-I**, **register VOL-II/VOL-V**, **register VOL-IV and addendum-created obligations**: rows, unit dispositions, evidence items and issues, each in its own files;
    - **A5 (Stage 4)**: templates for every evidence item, programme extensions (document counts, resources, infeasibility drivers), scenarios;
    - **drill B fixture**: a second synthetic Addendum No. 3 with two changes in one paragraph, a new obligation, an image-table change and two change types not seen in ADD-01/ADD-02.
  - Four of the five agents were stopped by an API usage limit; the VOL-I agent had finished its files by then, the others were resumed with their context after the reset (§8, E36).
- **Scope:** reproduce the five findings with failing tests first, fix them; complete Stage 3 and the connected Stage 4 work; labelled working drafts; a strict release gate; a second drill with rehearsal results; stop before final submission. Approve nothing and refresh no review status on the owner's behalf.

## 1. The exchanges (verbatim)

**Owner.** Message text as received:

~~~~text
while checking the code and outputs these came up. reproduce them first and tell me if i’m wrong(with evidence)

1-in amend.py, tn can become 999 instead of 3, the wrong column can change, and the evaluation table can be replaced with the hydraulic table, all passing validation. check values, columns and replacement content against the amendment itself. failed annotations also leave changes behind; failed operations must change nothing, including history and dependencis. 

2-in draft.py, a paragrph with two recognised changes produces only the first operation, but the whole paragraph is marked covered. process both or flag the remaining text as unresolved

3-checking stage2.load_evidence, changing a saved clause’s page to 99 still passes. verify intermediate files against their manifest. also, register.pin_value loses the image review fingerprint: a changed reading needs to keep dependent interpretations stale even after its transcription is approved again.

4-in the generated a3, the lcc consequence points to the original clause page, although that wording comes from add-02. cite the actual supporting page and amendment. keep original quotations separate from assembled effective text in a1–a3. Make always to reference the latest file reference for eachj point 

5-checking schedule.py, removing the lcc template makes its activities disappear while the build passes. check both directions: activities need requirements, and required deliverables need activities or a justified exception. missing templates and dependencies must be visible failure modes

add focused failing tests, fix these, then complete stage 3 and the connected stage 4 work. keep progressing where my answers aren’t needed

over all six documents, forms, footnotes, tables and addendum provisions. give every source unit a disposition and every independently testable obligation a stable row, evidence, owner and stage history.

replace “outside the slice” with actual treatment, and run english and arabic consequencce sweeps for omissions.

regenerate the full a1 excel/csv/json, a2, one-page a3 and a5 programme and marshalling plan. keep a3 readable without tiny text, with supporting detail linked. include the missing drawings and their impact

a5 should cover both envelopes, document counts, issuers, dependencies and resource assumptions. keep lead times provisional, show what drives infeasibility, and demonstrate changes to consortium size, lead times and the working calendar flowing through

proposed operations can run in labelled working drafts. structurally checked doesn’t mean human-approved. strict release must reject incomplete coverage, stale interpretations and required approvals still pending. don’t approve or refresh review status for me

run another synthetic addendum with two changes in one paragraph, a new obligation and an image/table change. show new rows, affected activities, stale dependencies and preservation of any previous approved state. (also add a couple of unseen before change cases  (in add1 or add2) 

keep the work log accurate, model integrations can wait

return the completed working outputs, remaining gaps, rehearsal results and a short prioritised decision list for me. stop before final submission

Use subagents smartly for this task with one master orchestrator opus 5.5 agent driving all processess
~~~~

**Later owner message:** "I hit my usage limit while you were working, but it has reset now. Please continue from where you left off."

## 2. Reproduction on commit 160242f (before any fix)

A script (session scratchpad `s05/repro.py`) ran each finding against the code as committed, in memory or on disposable copies. Output, verbatim:

~~~~text
== 1a  TN set to 999 (provision says 3 mg/l)
   valid: True | stage: APPLIED | TN limit: 999
== 1b  wrong column (Unit instead of Limit)
   valid: True | stage: APPLIED | TN cells: {'Basis of assessment': '30-day rolling average', 'Limit': '5', 'Parameter': 'Total Nitrogen (TN)', 'Unit': '3'}
== 1c  Table 1-1 replaced by VOL-II Table 2-6 (hydraulic design flows)
   valid: True | stage: APPLIED | VOL-I:T1-1/B superseded_by: VOL-II:T2-6 | T2-6 rows now carry history: ['VOL-II:T2-6/2-6.1', 'VOL-II:T2-6/2-6.2', 'VOL-II:T2-6/2-6.3']
== 1d  failed annotation leaves its annotation behind
   valid: False | failed check: ['C27'] | VOL-I:11.3 annotations after the failed op: ['ADD-02/T1-1-rev/note(1)']
== 1e  failed insert leaves history on its content
   valid: False | ADD-02:F4-G/T1/1 history after the failed op: []
== 2   one paragraph, two recognised changes
   ops: [('ADD-09/2.1', 'VOL-I:9.2', 'one hundred and twenty (120) pages', 'one hundred and fifty (150) pages')]
   dispositions for ADD-09:2.1: []
   coverage of ADD-09:2.1: op | VOL-V:36.2 changed: False
== 3a  saved clause page changed to 99 in units.json
   load_evidence problems: none
   E01 check: {'id': 'E01', 'ok': True, 'detail': 'evidence build structurally OK and built from the current inputs'}
== 3b  pin ignores the image review fingerprint
   pin before: 3cd0bd71a365346a | pin after the reading changed: 3cd0bd71a365346a
   pin after it is approved again: 3cd0bd71a365346a
== 4   A3 LCC consequence source
   A3 cites: VOL-I 8.6 p4 | quote: Failure to submit the certificate shall render the Proposal non-responsive.
   in the original VOL-I 8.6 text: False | in ADD-02 9.1 (p3): True
== 5   LCC template removed
   build status: ok | lcc activities: [] | VOL-I-8.6-01 in force: REINSTATED-AMENDED (ADD-02/9.1)
~~~~

**All five findings are confirmed; none is disputed.** Two notes: 1e was my own extra probe of the insert path — that path happened not to leak (C22 rejects the anchor first), but the same "change first, check later" pattern existed there, so all ops were made transactional; in 3b, approving the reading again also leaves the pin unchanged, which is correct (the fault was that the fingerprint was not pinned at all).

## 3. Failing tests first

`tests/test_session05_review.py` (19 tests) was written before any fix. First run: **17 failed, 2 passed**. The two that passed are guards: a reinstatement whose text is not in the provision, and an insert whose group does not exist, already fail before touching the state, and must keep passing.

## 4. Fixes

(continued below)
