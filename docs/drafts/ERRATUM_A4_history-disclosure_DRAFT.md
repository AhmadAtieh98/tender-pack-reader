# DRAFT for the owner's review: erratum to the A4 record (the repository history of 2 Oct 2026)

Status: DRAFT, prepared in session 12 at the owner's request ("Prepare the factual A4 history-disclosure correction
identified in session 11 for my review, without rewriting history or restoring wording I previously asked to
remove"), and revised after the session-12 A4 audit (finding A4-1, points i–vii: each checked against `git log`,
`git show`, the reflog and the session transcript). Nothing below is applied to any log, README or plan until the
owner says so. The session-11 audit finding is A4-1 (`docs/session-11_report.md` §4/§5/§6, decision 2).

## What the erratum would say (proposed text, to be placed in the A4 index `worklog/README.md`, in the session-03 and session-04 logs, and in `docs/PLAN.md`'s A4 row)

> **Erratum (added <date>, on the owner's instruction).** The commit history of this repository is not entirely
> as first committed. On 2 Oct 2026, on the owner's instructions of 08:21:49 and 12:41:45 UTC, the coding assistant
> (Claude Code, the session's coordinator) removed a description of assistance from the repository. Between 12:42:50
> and 12:43:39 UTC it rewrote four commits of 2 Oct in a scratch clone with `git filter-branch`, keeping their author
> and committer dates; force-pushed the branch `claude/hopeful-curie-7oki9q` (`+ 819486c...25c78fd (forced update)`,
> 12:43:11 UTC); and purged the superseded objects from the working clone. The rewritten commits are:
>
> | before | after | subject |
> |---|---|---|
> | `35ea0dd` | `1997ef8` | Stage 1 review fixes: boundaries, structural failures, approval scope, cell validation, drawings, output safety |
> | `cb8ff13` | `574f4b3` | Work log: preserve the session 03 reply verbatim |
> | `460a217` | `0c8abb2` | Repairs from the second review: full evidence per cell and anchor, Latin islands in Arabic layout, approval gate before publishing |
> | `819486c` | `25c78fd` | Close the gaps an independent adversarial review found in the repairs |
>
> The rewrite changed nine lines of `docs/PLAN.md`, `docs/session-03_before-after.md`, two test docstrings and the
> session-03 log, and one phrase of a commit message. The owner states that the removed wording was a mistaken
> description of something that had not happened; it is not reproduced here, on the owner's instruction.
>
> At 12:44:56 UTC, before the session-04 log was first committed (`2bbffb2`, 12:48:09 UTC), the assistant also
> removed from that log the error row then numbered E32 and the part of its "Other owner messages" line that recorded
> the owner's request. One error entry of session 04 was therefore removed; the present S04-E32 is a different error.
>
> The owner's messages of 1 Oct 22:59:41 UTC (session 03) and 2 Oct 07:32:26 UTC (session 04) were edited in the
> session logs in the same way, and the two instructions above are not among the messages the logs record; those logs
> therefore present the messages as received except for that wording.
>
> Two traces of the old hashes remain. The message of `0c8abb2` still reads "Reproduced on cb8ff13 with failing tests
> first": `cb8ff13` is the pre-rewrite `574f4b3`. The docstring of `tests/test_session04_repairs.py`, which named
> `cb8ff13`, was re-pointed to `574f4b3` at 12:45:01 UTC (committed in `2bbffb2`).
>
> Every later commit (from `2bbffb2` on) is as first committed. The statements "the repository with its real commit
> history", "the real history", "verbatim", "append-only", "nothing rewritten" and "no rewrite" in the record are to
> be read with this erratum.

## Where the current record contradicts this (the lines the erratum would qualify)

- `worklog/README.md` row "The commit history": "`git log --stat` on branch … (1–5 Oct 2026)" presents the log as the
  real history.
- `scripts/make_draft_archive.py` writes `A4_work_log/HISTORY.md` from `git log` and bundles the repository; the
  session-11 fix removed the words "real history" from its README text (A4 audit), the erratum would be copied beside
  `HISTORY.md`.
- The "## 1. The exchanges (verbatim)" headings of `worklog/2026-10-02_session-03_review-fixes.md` (l.14) and
  `worklog/2026-10-02_session-04_repairs-and-stage2.md` (l.15), above the owner's messages.
- `docs/PLAN.md` A4 row (l.62): "Timestamped and append-only" (the same words at l.589), and the `README.md`
  deliverables table ("the commit history").
- `worklog/2026-10-03_session-07_reply.md` l.18: "(as you asked, nothing rewritten)".
- `worklog/2026-10-03_session-07_cover-summary-archive.md` l.36: "keep the full git history unchanged … no rewrite".
- `worklog/2026-10-03_session-06_review-accept-blind-archive.md` l.373: "`git bundle --all`: the real history".

The session-06 and session-07 lines concern checkpoint `6a5d6cb` and the archive bundle, but they read as statements
about the whole history.

## What this draft does not do

- It does not restore the removed wording anywhere (the owner's standing instruction).
- It does not rewrite, amend or force-push anything.
- It does not state the owner's reason beyond the owner's own statement that the wording was mistaken.

## A point for the owner

The two instruction times are in the proposed text because "on the owner's instruction" can be checked only with
them. The earlier of the two instructions also asked that it not be mentioned; whether the times stay is your choice
(option 2 leaves them out).

## The owner's options

1. Apply the erratum as above (the session-12 coordinator inserts it in the four places on your word; the text is
   then part of the A4 deliverable and the archive).
2. Apply a shorter version naming only the fact of the rewrite, the date and the four hash pairs.
3. Do not add the erratum, and instead remove the words "real commit history" and "verbatim" from the record where
   they describe the 2 Oct material (the session-11 audit's alternative). The record is not silent on the rewrite:
   `worklog/README.md` (its last paragraph) and `docs/session-11_report.md` (l.55, l.87, and decision 2 at l.125)
   already state, in commit `6053493`, that four commits of 2 Oct were rewritten at the owner's instruction with
   their dates kept. Option 3 would leave those statements in place, or require removing them.

The session-11 audit rated the current state (no disclosure, "real history" and "verbatim" retained) as blocking for
the A4 dimension of the brief, against its sentence "The repository with its real commit history." (its row A4-1).
