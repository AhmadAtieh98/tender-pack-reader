# Cost and effort (honest breakdown, as of session 12 in progress; every figure provisional)

## Where the numbers come from

- The work logs, the commit timestamps, the rehearsal clock, and the subagents' own reports.
- **Money is not stated.** The sessions ran under the owner's Claude subscription, and token usage was not metered per session, so a currency figure would be invented. Token counts are given only where a tool reported them.

## Assistant time (wall clock, from the work logs and commits)

| Session | When (UTC) | Wall clock | Main work |
|---|---|---|---|
| 01 | 1 Oct 20:56–21:20 | ~0.5 h | Source analysis and engineering plan |
| 02 | 1 Oct 21:40–22:30 | ~1 h | Stage 1: evidence, units, image readings (proposed; approved by the owner on 3 Oct 2026, session 08) |
| 03 | 1 Oct 22:59–2 Oct 01:10 | ~2.2 h | Owner's Stage 1 review: six gaps, fixed |
| 04 | 2 Oct 07:32–13:00 | ~5.5 h | Second review repairs; adversarial review; Stage 2 slice; drill A |
| 05 | 2 Oct 13:31–18:25, with a pause at a usage limit (~1 h) | ~4 h of work | Five review findings; Stage 3 (full register) and Stage 4 (A5) with subagents; drill B |
| 06 | 3 Oct 00:42–01:54 and from 05:41, with a pause at a usage limit (3 h 47 min) | about 1 h 55 min of work (00:42–01:54 and 05:41–about 06:05) | Four findings; accept workflow; `show`/`diff`; C12/C30/C32/C46/C47; blind rehearsal; archive |
| 07 | 3 Oct from 08:32 | about 1 h (see the work log) | C28 cover-summary check; drafter cover rule; review packets in the review folder; archive rebuilt and verified; Mac wheels split |
| 08 | 3 Oct 19:30–20:27 and 4 Oct 05:17–about 08:15, with a pause at a usage limit (8 h 50 min) | about 4 h of work | Four findings; the owner's confirmations recorded; interpretations via proposals; A1–A3; A5 and Gantt; clarification register; blind rehearsal 02; archive |
| 09 | 4 Oct 08:42–about 13:00, no pause | about 4 h 20 min of work (the coordinator as Fable 5.1; seven Opus 5.5 subagents, five of them in parallel) | Six control findings (failing tests first); the AI layer (`tenderpack/ai/`), the MCP server and four routes; blind rehearsal 03 with a sealed key (31 hit / 3 partial / 0 missed of 34); post-key fixes; committed as `a41e104` on the owner's authorisation |
| 10 | 4 Oct 13:33–17:58, no pause (the session disconnected for about 30 min after the blind-04 run) | about 4 h 25 min of work (the coordinator as Fable 5.1; six Opus 5.5 subagents, by their own reports: W1 393,636 tokens; W2 559,500; W3 691,476 + 761,072 after its resume; W4 485,159; W5 228,008; W6 382,414) | Four controls (failing tests first); the runnable, resumable workflow `tenderpack ai run` with a candidate workspace and review packet; relationships with statuses and missing-document blockers; route hardening (capability policy, structured outputs, batching, critic, a real host/MCP session); disposable fixtures; blind rehearsal 04 with a sealed key (19 hit / 10 partial / 6 missed of 35 in 45.6 min; 7 batches killed by the host plan's HTTP 429); committed as `a57f118` at 17:58 on the owner's authorisation ("commit the session 10 work", 17:57) |
| 11 | 4 Oct 18:27–5 Oct about 07:55, with two pauses at the plan's limit (19:37–21:30, 04:45–07:30) and a container restart (23:10) | about 10 h of work (provisional) | the coordinator as Fable 5.1; Opus 5.5 subagents by their own reports: four implementers (D1–D4), the blind-05 author, six audit reviewers (A1–A5, R), three audit fixers; a 2-hour pause at the host plan's session limit (19:37–21:30) and a container restart at 23:10 | The downstream workflow finished; one request path with failure classes; calculation tools, relationships, conditional amendments; candidate A3/A5; blind-04 regression and blind-05 sealed run; the audit of the real package BASE → ADD-02 with fixes; committed as `6053493` at 08:20 on 5 Oct on the owner's authorisation ("commit", 08:13) |
| 12 | 5 Oct 09:14–6 Oct about 00:10, with four pauses at the plan's limit (11:49–12:30 and 13:57–17:30 for everything; 18:53–21:11 for the host models, the coordinator working on without them after a 3-minute stop; 22:18–23:52 for everything) | about 9 h 15 min of work (provisional): about 6 h 45 min to the second progress commit (20:07 UTC: 11 h of wall clock less 4 h 14 min of pauses) and about 2 h 30 min for the closing work (20:07–22:18 and 23:52–00:10; 15 h of wall clock in all) | the coordinator as Fable 5.1; Opus 5.5 subagents by their own reports: W1 (human-owned judgments), W2, W3a, W3b (the unseen-addendum workflow), W4 (offline, concurrency, Mac), W5 (consecutive addenda), the blind-06 author, six audit reviewers and their rechecks, fixers F1–F6 (F2 twice), the panel agent P and its follow-up, the scorer S (23 Opus 5.5 launches and resumes in this session's task records, whose usage fields add up to about 1,300 M cached input tokens read and 35 M written; their output-token counts are per-message partials and are not summed) | Human-owned judgments; the workflow finished; offline mode and the Mac setup; the audit through ADD-02 with fixes and rechecks; blind-06 sealed and timed; the blind-05 regression with an interruption; the local panel; the snapshot |
| 13 | 6 Oct 06:01–7 Oct about 00:30 UTC, with one pause at the plan's limit (07:45–11:46 for everything: E156) and one lost stretch (14:27–16:27: the closing chain killed at the harness's two-hour limit, E158) | about 12 h 30 min of work (provisional): 18 h 30 min of wall clock less the 4 h 1 min plan pause and the 2 h of the killed chain; the evening's two lost suite runs (E158's restart and E165's disk crash, about 3 h 30 min of machine time) overlapped with other work and are not subtracted | the coordinator as Fable 5.1; Opus 5.5 subagents by their own reports (runtime effort shown "40", transcripts `xhigh`): the three audit reviewers R1–R3 and their rechecks, the implementers A–E, the fixers F1–F4, the blind-07 author A7 and the scorer S7 (29 launches and follow-ups in the session's task records, briefs 87–115); the sealed run's own 10 host sessions on the host CLI's default model (reported Sonnet 5.5) | The audit of the outputs with fixes and rechecks; the correctness gaps and the runtime policy; speed; the AI quick review; the interview folder; the sealed blind-07 run from the folder with an interruption and a resume (four attempts; three tool defects found and fixed on the way); the full suite on the final code; the closing commit on the owner's instruction |
| **Total so far** | | **about 39 h of assistant wall-clock time through session 11** (sessions 01–08 about 20 h; 09 about 4 h 20 min; 10 about 4 h 25 min; 11 about 10 h), session 12 to be added when it ends | |

**Models.** Sessions 01–08: the coordinator ran as Opus 5.5 (the commit trailers of `95b8408` … `34f7bc4`; the session transcript's model field, checked in the session-11 audit); from session 09 (4 Oct 08:42) as Fable 5.1 (`a41e104`, `a57f118`). Every subagent of sessions 04–11 reported Opus 5.5 by its own instructions; the launching session cannot verify a subagent's model (session-10 log, E127). The headless host sessions report their model through the CLI (recorded per run in `worklog/model_calls/` and `staging/ai/runs/*/ai/*/session.json`).

**Subagents** (each started cold from a written brief; the orchestrator checked their output; every brief is in `worklog/subagent_briefs/`, exported verbatim in session 11):

| Session | Agents |
|---|---|
| 04 | 3: dates, an independent oracle, an adversarial reviewer |
| 05 | 5: three register agents, A5, a drill-B fixture author |
| 06 | 1: the blind-addendum author. It reported about 302,000 tokens and 22 minutes |
| 08 | 4: post-award evidence (reported 169,540 tokens), the blind-02 addendum author (254,315), the clarification register (276,780), A5 and Gantt (stopped by the usage limit and resumed; no total reported) |
| 09 | 7, all Opus 5.5: W1 PDD flow and Gantt (371,913 tokens), W2 clarify, bindings, diff (327,176), W3 C28, removed, insert_row, classes (541,592), W4 the AI layer (550,206), W5 the blind-03 author (328,534), P the proposer on the host route (214,440; the application paid nothing: no API call), C the curator (496,726); about 2.83 million tokens of subagent work, on the session's own plan, not the application's budget |

Four session 05 agents were stopped by a usage limit and resumed.

## The owner's time

- **So far:** reading the reports and outputs; the code reviews of sessions 03, 05 and 06 (the findings were the owner's); correspondence with the hiring team.
- **Done:** the two image readings (batch 1) were reviewed and approved on 3 Oct 2026 (`curation/approvals.yaml`); the session-06 STALE-row proposals were superseded in session 08 (no STALE row remains).
- **Not yet spent, and needed before submission:**

| Review | Items | Estimate |
|---|---|---|
| Disqualifiers (batch 2) | 19 rows | 45–60 min |
| Amendment ops (batch 3) | 37 ops | 45–60 min |
| Remaining rows (batches 5–9) | 183 | 3–4 h at about 1 minute each; can be split by owner role |
| Legal and commercial calls (issues on A3) | 10 | Depends on advisers |

These estimates are mine, untested against a real reviewer.

## What the assistant produced

| Item | Size |
|---|---|
| Code | 50 modules, about 16,600 lines (`tenderpack/`, of which the AI layer `tenderpack/ai/` and the MCP server, session 09, about 4,700) |
| Tests and fixtures | about 9,300 lines (the session 09 files: the six control findings, the AI layer's adversarial cassettes and MCP handshake, the blind-03 live and post-key fixes); the full suite runs in about 35 minutes on the cloud container (it rebuilds the real pack and the rehearsals several times) |
| Curation | about 9,100 lines of YAML: 205 register rows, the owner's two reading approvals, the clarification register (21 draft questions), dispositions for every unit, op files for ADD-01/ADD-02, evidence items, A5 templates, assumptions, issues. **All of it is a proposal** until you decide on it |
| Outputs | A1–A5 working drafts, the Gantt, the clarification register, review batches and packets, two drills, three blind rehearsals (the third with the AI layer in the loop, about 10,300 lines of rehearsal curation), two staged AI proposal runs (`staging/ai/`, recorded and host route; nothing applied) |

## Running cost of the tool itself

- **Compute:** a laptop. Stage 1 takes about 13 s and the outputs about 80 s on the cloud container (the A5 scenarios, the Gantt and the review packets were added since session 06). The full tests take about 30 minutes there.
- **Network:** none at run time. One download at setup (about 45 MB of wheels per Mac architecture), or none with the wheelhouse.
- **Model calls:** none in the deterministic build (`ingest`, `outputs`), which needs no model. No API-key call has been made (the Anthropic, OpenRouter and Ollama routes are tested with recorded responses only). The host route has run for real on the host's own plan since session 09 (`docs/AI_ROUTES.md` §8, `worklog/model_calls/`, `rehearsals/blind-03..05`), at no application cost; the host reported its own plan cost per session where it did. Since session 09 the AI layer can call a model to *propose* (Anthropic, OpenRouter or local Ollama; or a coding host's own model at no application cost); every paid run is capped (`config/ai.yaml`, `--max-usd`) and metered in `staging/ai/spend.jsonl`. No live call has been made: there is no key in the cloud environment, so no USD figure exists yet.

## Where the effort went that was not planned

- Repairs after three owner code reviews, about 6 hours in total. Each review found real gaps, and the work log records them as errors E1–E50+.
- Making every check two-way, and making the release gate refuse what is unreviewed.
- **Risk:** the register was drafted at scale by subagents. Its quality is only as good as your review of it.
