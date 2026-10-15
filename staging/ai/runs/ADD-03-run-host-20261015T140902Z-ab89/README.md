# Live ADD-03 run on the Claude Code host route (15 Oct 2026)

> **Runtime: 24 min 17 s from upload to review packet, with no server errors (no timeout, retry, repair or deferral).**
> **Results match the Codex run on the same ADD-03** (identical amendments, the same unresolved provisions, an identical A5 programme). **What changed:** [review/diff.md](review/diff.md).

> **CANDIDATE: proposed by the AI workflow, NOT VALIDATED, nothing approved by a person.**
> The validated state is still **ADD-02**. Approvals marked "Interview demo assumption" are SIMULATED (interview demo profile) and are not human decisions.

| | |
|---|---|
| Run id | `ADD-03-run-host-20261015T140902Z-ab89` |
| Input | the interviewer's ADD-03 (`candidate/input/6f9f9d7c….pdf`, 19 provisions). Not the synthetic practice addendum (sha256 `0c1a4917…`), which has 12. |
| Route / model | host route through the Claude Code CLI 2.1.296. Configured `claude-opus-5-5`. All 14 tool sessions and 11 critic sessions **reported `claude-opus-5-5`**, with no auxiliary model. |
| Result | **PARTIAL** (13/13 steps done; partial because provisions are unresolved, not because anything failed) |
| Time | upload 17:09:02 to review packet 17:33:19 local: **24 min 17 s**, under the 45-minute guard |
| Errors | **none**: every request was answered at the first call (no failure, retry, repair, rate limit or deferral) |
| Code | identity `b6165e419b11…` over 103 files, one segment, package base `cbe0e94` plus the session-19 working-tree changes committed alongside. The identity hashes `config/*.yaml` too. It differs from the rehearsal's `d2f02b0b…` only because this run used `concurrency.max_parallel_sessions: 4` and `max_total_host_sessions: 4` (the profile default is 2). The Python and policy files are byte-identical. |

Steps (seconds): ingest 7.1 · readings 0 · analysis 558.5 (4 batches, 4 at a time) · validation 2.2 · downstream 534.6 (10 batches, 4 at a time) · downstream validation 0.4 · critic 326.5 (11 sessions; 3 batches had nothing selected) · promotion 8.6 · pin 0.6 · check_register 1.9 · outputs 9.9 · diff 1.8 · review 1.6.

Tool sessions: each was offered only its phase's `mcp__tenderpack__` tools, with the tenderpack MCP server connected. The critic sessions had no tools. Both crop images reached the model byte-identical (sha256) to what the server sent.

## Where to look

| What | File |
|---|---|
| **Start here: the review packet** (unresolved first, then per-provision evidence, then the diff) | [`review/index.md`](review/index.md) ([`index.html`](review/index.html)) |
| What changed ADD-02 → ADD-03 | [`review/diff.md`](review/diff.md), `review/diff.json` |
| Candidate A1 register | `candidate/out/a1/a1.xlsx` (`a1.csv`, `a1.json`) |
| Candidate A2 reconciliation | `candidate/out/a2/a2.md` |
| Candidate A3 | `candidate/out/a3/a3.pdf` (1 page at condensation level 3, reasons in `a3_detail.html`). Full diagnostic `a3_candidate.pdf` (6 pages). |
| Candidate A4 clarification register (DRAFT, NOT SENT) | `candidate/out/a4/clarification_register.md` |
| Candidate A5 programme / marshalling | `candidate/out/a5/` (`programme.csv`, `marshalling.csv`, `gantt.html`) |
| Analysis proposals (model output, PROPOSED) | `ai/ADD-03-run-host-20261015T140902Z-ab89-combined/proposals.yaml` |
| Downstream proposals and critic notes | `downstream/proposals.yaml`, `downstream/critic.yaml` |
| What promotion would copy (nothing has been copied) | `promotion.json` |
| Step record and timings | `checkpoint.json`, `log.jsonl`, `logs/` |

## Needs a person (human decisions)

**Unresolved provisions (not applied):**
- **ADD-03:2.2**: "Every period calculated by reference to the Proposal Due Date is adjusted accordingly." Names no clause, so the affected periods are an interpretation.
- **ADD-03:4.3**: "Volume I Clause 1.3 is amended correspondingly." Prints no old or new words.

**Escalated, software limitation (not guessed):**
- **ADD-03:3.1** withdraws the whole of Form 4-G, the 9-unit group added by ADD-02. The engine cannot change the status of a whole group named only by its form number. Partly applied: ADD-02-7.2-01 is revoked, and the Form 4-G rows and activities are held back (12 downstream tasks answered only by items that cannot be promoted).
- **ADD-03:4.1** changes Table 2-6 row 2-6.1 from 120,000 to 150,000 m³/day. The citation resolver does not link "row 2-6.1" to `VOL-II:T2-6/2-6.1`. Partly applied: VOL-II:2.1 changed, the table cell did not.

**Also for a person:**
- **85 lines marked HUMAN DECISION PENDING** in the review packet: proposed issues, interpretations and clarification entries.
- **6 earlier answers to re-read** against the new text (ADD-01 Q1, Q3, Q5; ADD-02 Q7, Q8, Q11). None is revoked.
- **Register check: exit 1 with 4 `pending_settled` findings.** Issues labelled HUMAN DECISION PENDING are worded as if settled, for example I-ADD03-F4G-SCOPE and I-ADD03-TIE-BAND. This is model wording, left visible to be reworded or decided.
- **Cover summary vs provisions (C28, report only): 8 findings.** The checker reports "not found" for the cover's 'withdraws Form 4-G' and 'adds a new Clause 11.6' (report only; a person checks these against 3.1 and 6.1). Q17 adds an obligation the summary understates. Provisions 5.1, 5.2 and 6.1 are not mentioned in the summary.
- **Critic** (a second model, changes no status): 33 items reviewed, 14 disagreements.

## What changed (proposed, ADD-02 → ADD-03)

- 19 provisions: 9 applied, 2 partly applied, 6 no effect, 2 unresolved. 13 ops, 0 invalid.
- Requirements: 5 new (ADD-03-cover-para3-01, ADD-03-6.1-01, ADD-03-Q17-01, ADD-03-3.1-01, ADD-03-3.2-01), 1 out of force (ADD-02-7.2-01, revoked by 3.1(a)), 20 changed.
- Changed dates and amounts include: Proposal Due Date 2026-11-26 → 2026-12-10 (2.1), clarification cut-off 2026-11-12 → 2026-11-26, VOL-I 6.4 amount SAR 4,500,000 → SAR 5,600,000 (5.1), and VOL-I 6.3 period 180 → 210 days, which moves the bid-bond validity date 2027-05-25 → 2027-07-08 (5.2(a)). New Clause 11.6 adds a tie band within 2% (6.1).
- A3 and A5 stay **validated at ADD-02**. The ADD-03 versions are the candidate files above.

## Not included in this commit

Host session transcripts, generated prompts and request packets (`ai/*hostsession*`, `ai/*-critic`, `batches/*.packet.json`), per AGENTS.md. The rebuildable parts are also left out (`candidate/build`, `candidate/out-before`, `candidate/before`), so links to `../candidate/out-before/` in the packet need a rebuild (`tenderpack ai resume … --from outputs`).
