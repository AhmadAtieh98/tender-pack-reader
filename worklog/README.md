# A4: the work log (index)

The brief's A4 is "the repository with its real commit history, the prompts and model calls you used, and a short
written note of every place your system was wrong while you were building it, and how you caught it". It is spread
over the repository; this page says where each part is.

| Part | Where | Notes |
|---|---|---|
| The commit history | `git log --stat` on branch `claude/hopeful-curie-7oki9q` (1–5 Oct 2026) | Sessions 01–08 commit per step; sessions 09 and 10 were committed as one commit each (`a41e104`, `a57f118`) at the owner's instruction, on the owner's authorisation recorded in their logs; session 11 as `6053493` (5 Oct, on the authorisation recorded in the session-12 log §0); session 12 is uncommitted until the owner authorises it. The commit trailers name the model that ran each session. |
| The owner's prompts, verbatim | `worklog/<date>_session-NN_prompt.md` (sessions 08–12) and the "exchanges" sections of the earlier session logs | Sessions 10 and 11: curly apostrophes were straightened when pasted (noted in the files). The session-05 model-name redaction is disclosed on the line itself. |
| The briefs given to subagents, verbatim | `worklog/subagent_briefs/` (44 briefs exported from the session transcript in session 11, and from brief 45 on the session-12 briefs and follow-up messages, exported at the end of session 12; session 13's 87–115 and session 14's 116–151 exported at the end of each session; one index) | The register, A5, the rehearsal addenda, the AI layer, the session-11 audit and its fixes were largely drafted by these agents from these briefs; the coordinator checked their output. |
| Model and tool calls | `worklog/model_calls/*.jsonl` (runtime logs of every host and MCP session), `staging/ai/runs/<run>/ai/*/` (per-session logs, prompts, transcripts, declared and reported models), `docs/AI_ROUTES.md` §8 (what was run live and what was recorded) | No API-key call was made; the host route ran for real on the host's own plan (blind rehearsals 03–05). Each subagent's model is recorded as its own report (the launching session cannot verify it). |
| Every place the system was wrong, and how it was caught | `worklog/ERROR_INDEX.md` (one line per error, 146 entries at the end of session 11, 164 at the end of session 12 (E138–E155), session 13 E156–E165, session 14 E166–E174 (183 entries at the end of session 14), with the log and line of the full row) and the error tables of each session log | The index prefixes ids with the session because sessions 03 and 04 both numbered from E22. |
| How the work developed, session by session | `worklog/<date>_session-NN_*.md` (timeline, exchanges, what was built, verification, errors) and `docs/session-NN_report.md` (the owner-facing report per session) | `docs/PLAN.md` is the engineering plan with a status section per session (revisions 1–11). |
| Cost and effort | `docs/COST_AND_EFFORT.md` | Wall-clock per session, subagents and their reported token counts, the owner's time; money is not stated (the sessions ran on a subscription; the host reported its own plan cost per session where it did). |
| Supporting record | `out/a4/clarification_register.*` (21 draft questions, NOT SENT) | A record of what the system could not resolve and would ask the Authority; not the whole of A4. |

What this index does not settle: the audit of session 11 (`docs/session-11_report.md`, audit A4) found that four commits
of 2 Oct 2026 were rewritten at the owner's instruction with their dates kept, and that the record does not say so; how
the record discloses this is the owner's decision and is listed among the decisions the owner must take.
