# Cost and effort (honest breakdown, as of session 06)

## Where the numbers come from

- The work logs, the commit timestamps, the rehearsal clock, and the subagents' own reports.
- **Money is not stated.** The sessions ran under the owner's Claude subscription, and token usage was not metered per session, so a currency figure would be invented. Token counts are given only where a tool reported them.

## Assistant time (wall clock, from the work logs and commits)

| Session | When (UTC) | Wall clock | Main work |
|---|---|---|---|
| 01 | 1 Oct 20:56–21:20 | ~0.5 h | Source analysis and engineering plan |
| 02 | 1 Oct 21:40–22:30 | ~1 h | Stage 1: evidence, units, image readings (pending) |
| 03 | 1 Oct 22:59–2 Oct 01:10 | ~2.2 h | Owner's Stage 1 review: six gaps, fixed |
| 04 | 2 Oct 07:32–13:00 | ~5.5 h | Second review repairs; adversarial review; Stage 2 slice; drill A |
| 05 | 2 Oct 13:31–18:25, with a pause at a usage limit (~1 h) | ~4 h of work | Five review findings; Stage 3 (full register) and Stage 4 (A5) with subagents; drill B |
| 06 | 3 Oct 00:42–01:54 and from 05:41, with a pause at a usage limit (3 h 47 min) | about 1 h 55 min of work (00:42–01:54 and 05:41–about 06:05) | Four findings; accept workflow; `show`/`diff`; C12/C30/C32/C46/C47; blind rehearsal; archive |
| 07 | 3 Oct from 08:32 | about 1 h (see the work log) | C28 cover-summary check; drafter cover rule; review packets in the review folder; archive rebuilt and verified; Mac wheels split |
| **Total so far** | | **about 16 h of assistant wall-clock time** | |

**Subagents** (each started cold from a written brief; the orchestrator checked their output):

| Session | Agents |
|---|---|
| 04 | 3: dates, an independent oracle, an adversarial reviewer |
| 05 | 5: three register agents, A5, a drill-B fixture author |
| 06 | 1: the blind-addendum author. It reported about 302,000 tokens and 22 minutes |

Four session 05 agents were stopped by a usage limit and resumed.

## The owner's time

- **So far:** reading the reports and outputs; the code reviews of sessions 03, 05 and 06 (the findings were the owner's); correspondence with the hiring team.
- **Not yet spent, and needed before submission:**

| Review | Items | Estimate |
|---|---|---|
| The two image readings (batch 1) | 2 readings: Table 2-4 (12 units) and Form 4-C (28 units) | 30–45 min, with the crops |
| Disqualifiers (batch 2) | 19 rows | 45–60 min |
| Amendment ops (batch 3) | 37 ops | 45–60 min |
| STALE-row proposals (batch 4) | 3 | 10 min |
| Remaining rows (batches 5–9) | 183 | 3–4 h at about 1 minute each; can be split by owner role |
| Legal and commercial calls (issues on A3) | 10 | Depends on advisers |

These estimates are mine, untested against a real reviewer.

## What the assistant produced

| Item | Size |
|---|---|
| Code | 31 modules, about 9,600 lines (`tenderpack/`) |
| Tests and fixtures | about 5,700 lines; the suite runs in about 6 minutes |
| Curation | about 6,500 lines of YAML: 202 register rows, dispositions for every unit, op files for ADD-01/ADD-02, evidence items, A5 templates, assumptions, issues. **All of it is a proposal** until you decide on it |
| Outputs | A1–A5 working drafts, review batches, two drills, one blind rehearsal |

## Running cost of the tool itself

- **Compute:** a laptop. Stage 1 takes about 13 s and the outputs about 12 s. The tests take about 6 minutes.
- **Network:** none at run time. One download at setup (about 45 MB of wheels per Mac architecture), or none with the wheelhouse.
- **Model calls:** none (integrations deferred).

## Where the effort went that was not planned

- Repairs after three owner code reviews, about 6 hours in total. Each review found real gaps, and the work log records them as errors E1–E50+.
- Making every check two-way, and making the release gate refuse what is unreviewed.
- **Risk:** the register was drafted at scale by subagents. Its quality is only as good as your review of it.
