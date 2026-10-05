# Blind rehearsal 04 as post-key regression material (session 11)

**Synthetic, not tender content.** The key of this rehearsal was opened in session 10 (`COMPARISON.md`); nothing run here
is scored as an unseen test. The purpose: run the same Addendum No. 3 through the workflow as it stands after the
session-11 changes, end to end on the host route, until AI-generated rows, interpretations, issues, evidence items and
activities reach a usable candidate build, and record every interruption and intervention honestly.

## The run

`python -m tenderpack ai run ADD-03 --pdf rehearsals/blind-04/input/ADD-03_Addendum_No_3.pdf --route host --host-model-alias opus --run-id ADD-03-run-host-blind04-s11-20261004T222214Z`
(log `run-s11.log`, clock `clock-s11.txt`, run folder `staging/ai/runs/ADD-03-run-host-blind04-s11-20261004T222214Z/`).

A resume of the session-10 run was not possible: under the session-11 state identity (register, relationships and every
curated input in the bindings) its staged sets are STALE and promotion refuses them, which is the intended behaviour.

| UTC | What happened |
|---|---|
| 22:22:14 | Started. Ingest refused the candidate for the image region without a reading; the readings step proposed one in a host session (190 s; interpretation_pending; PENDING HUMAN REVIEW) and ingested again (613 units). |
| 22:26–22:58 | Analysis: 70 provisions in 10 batches of at most 8; 5 batches ran as host sessions (001, 002, 004, 005, 009), 5 were skipped because every provision of the batch was already accounted for by an earlier session's items (the shared context is sent once per session and a session proposes beyond its batch). Combined set 41 items, 70/70 provisions accounted for (evidence_verified 11, interpretation_pending 27, insufficient_evidence 1, escalated 2). The critic ran once per batch (25 items reviewed, 1 disagreement). 33 min against 47 min for the same phase in session 10. |
| 22:58–23:10 | Downstream: batches 001 (15 items, 263 s) and 002 (14 items, 373 s) done. |
| about 23:10 | **Interrupted by a container restart** (E134) during downstream-003. |
| 23:12:40 | `tenderpack ai resume`: the dead process's run lock was taken over; done batches were not asked again. **E135:** every later host session was refused by the addendum's staging lock still held by the dead process, and the workflow recorded downstream-003/004/005 as done with 0 items; the run went on to promotion, check-register, outputs (candidate outputs published, exit 0) and ended `partial` at 23:15:47 with 27 of 51 tasks unanswered. |
| 23:17–23:19 | E135 fixed in the main tree with failing tests first (`tests/test_session11_locks.py`): lock takeover for a dead holder; a refusal is the class `refused` and raises; a done batch with an errored session and no items is reclassified `failed` on resume. |
| 23:19:19 | Resumed: the three batches reclassified and asked again. downstream-003 met the **host plan's session limit** (HTTP 429, reset 02:30): the request layer backed off, saw the named reset beyond the 300 s it honours, DEFERRED the batch and stopped cleanly (exit 5) at 23:22:15 with everything checkpointed (E136). |
| 02:33:04 (5 Oct) | Resumed after the reset: downstream-003 (25 items), 004 (18), 005 (3) answered; downstream validation; the critic step; promotion (revalidated against the current identity: set partial, downstream complete, no status change); pin; check-register; candidate outputs published (101 files with the banner); diff; review packet. Ended 02:53:54, exit 0, status `partial`. |

## Outcome

- **Execution:** every step done; batches: reading 1 done; analysis 5 done, 5 skipped; downstream 5 done.
- **Completeness (partial), with the reasons the run itself states:** 1 provision unresolved in the candidate; 51
  downstream tasks, 34 answered by promotable items, 17 answered only by items that cannot be promoted (among them the
  new Form 4-H rows of ADD-03 8.1–8.4 and the Table 1-1 reissue of 6.1), 0 unanswered, 5 answered `no_change`;
  check-register on the candidate exit 1 with 12 findings (11 C46: the obligations ADD-03 6.1 and 8.1–8.4 create are
  held by no A1 row in force at ADD-03 because the proposed new rows were not promotable; 1 disposition); candidate
  outputs published.
- **Approval:** none (nothing is approved by the program; every promoted item is proposed).
- **Time:** steps 3,777 s = 63 min of work, of which model latency dominates (analysis 1,969 s, downstream 1,319 s);
  wall clock 4 h 32 min including a 2-minute restart gap and a 3 h 11 min wait for the plan's reset. The session-10 run
  took 45.6 min to its first outputs and 76.4 min after its post-key resume, and its candidate build was refused.
- **Manual interventions:** none in the run. The coordinator ran `ai resume` three times (after the restart, after the
  E135 fix, after the reset) and fixed E135 in code between the first and the second resume; no YAML was written by
  hand; the 15 interventions the checkpoint records are the automatic host sessions.
- **What this shows:** the fixed workflow takes an addendum from PDF to a published candidate build with AI-generated
  rows, readings, issues, evidence items and activities, survives a crash and a rate limit without losing passed work,
  and says what it could not do. What it does not show: a complete candidate (17 tasks need a person or a better
  proposal; the C46 findings name them).
