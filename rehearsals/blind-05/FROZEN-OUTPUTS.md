# Blind rehearsal 05: the first outputs, frozen before the key was opened

Recorded 2026-10-05 04:08:13 UTC. The key (`SEALED/`, hashed in `FROZEN.md` before the run) had not been opened by the coordinator or
any processing agent when this file was written. `FROZEN-OUTPUTS.sha256` holds the sha256 of every file listed below
(327 files); `sha256sum -c FROZEN-OUTPUTS.sha256` from this folder verifies them.

- Run: `ADD-03-run-host-blind05-20261005T025444Z` (`run.log`, `clock.txt`, `checkpoint.json`, `log.jsonl`, `promotion.json`).
- Clock: PDF received 02:54:44 UTC (the frozen PDF of 4 Oct 19:19); the run ended 04:07:11 UTC: **72 min 27 s** wall clock
  from the PDF to the candidate outputs and the review packet, with no interruption; the steps add up to 4,345 s
  (72.4 min), analysis 2,676 s (nine host sessions, each with a critic request), downstream 1,260 s (five sessions),
  readings 209 s, outputs 86 s. The brief's segment is 30 minutes.
- Outcome as the run states it: status `partial`; 54 provisions, 54/54 accounted for (evidence_verified 14, conflicting 13,
  interpretation_pending 18, escalated 4, insufficient_evidence 8); 23 provisions unresolved in the candidate; promoted
  12 ops, 19 dispositions, 2 new rows, 12 readings, 3 issues, 7 activities, 1 clarification; 54 downstream tasks, 31
  answered by promotable items, 23 only by unpromotable ones, 0 unanswered, 8 `no_change`; check-register 1 finding
  (quote); candidate outputs published (101 files with the banner); the critic reviewed 15 downstream items, 2
  disagreements, visible in the packet. No manual intervention; 15 automatic host sessions.
- Copies: `out-candidate/` (the candidate A1–A5, README, checks), `review/` (the packet), `proposals/` (the staged
  sets), `candidate-curation/` (the candidate's curation after promotion), `downstream/`, `batches/`.

Anything changed after this point is labelled and not scored.
