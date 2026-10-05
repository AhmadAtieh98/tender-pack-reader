# Blind rehearsal 06: the first outputs, frozen before the key was opened

Recorded 2026-10-05 18:30:42 UTC. The key (`SEALED/`, hashed in `FROZEN.md` before the run) had not been opened by the coordinator or
any processing agent when this file was written. `FROZEN-OUTPUTS.sha256` holds the sha256 of every file listed below
(367 files, hashed at 18:29:34 UTC by the freeze script `freeze_blind06.py` kept in the coordinator's scratchpad); `sha256sum -c FROZEN-OUTPUTS.sha256` from this folder verifies them.

- Run: `ADD-03-run-host-blind06-20261005T173226Z` (`run.log`, `clock.txt`, `checkpoint.json`, `log.jsonl`, `promotion.json`); host route, alias opus, `max_parallel_sessions: 2` (the first timed run with two host sessions in flight).
- Clock: the PDF received 17:32:26 UTC (the frozen PDF of 09:53); the run ended 18:28:15 UTC: **55 min 49 s** wall clock
  from the PDF to the candidate outputs and the review packet, with no interruption; the steps add up to 3,345.6 s
  (55.8 min): analysis 2,170.6 s (ten batches of at most 8 provisions, each with a critic request, two in flight at a time), downstream 838.9 s (four batches),
  readings 211.4 s (one image region, ADD-03-p4-r1, refused by ingest until read), ingest 29.7 s, outputs 12.4 s. The brief's segment is 30 minutes; blind-05 took 72 min 27 s at one session in flight.
- Outcome as the run states it: status `partial`; 70 provisions; 83 items with statuses: interpretation_pending 45, evidence_verified 15, insufficient_evidence 11, conflicting 7, escalated 5; 22 provisions unresolved in the candidate; promoted
  11 ops, 39 dispositions, 2 new rows, 11 readings, 4 issues, 1 activities, 2 clarifications, 1 relationships; 48 downstream tasks,
  30 answered only by unpromotable items (named in the status reason); check-register 1 finding (C46: the cover's "deduction" carried by no row's consequence at ADD-03);
  candidate outputs published (103 files with the banner). The critic reviewed items after every analysis batch and after downstream validation (disagreements per batch in `run.log`: 1, 0, 0, 3, 0, 0, 1, 0, 0, 1; downstream 1, 0, 1), visible in the packet, changing no status.
  No manual intervention: the 15 `interventions` entries of `checkpoint.json` are the automatic host sessions themselves ("host session (automatic) … not a person"); automatic host sessions: 10 analysis, 13 critic, 4 downstream, 1 reading (15 host-session records).
- A record slip, corrected before this note: the launch script wrote the run's exit line and the end time to `runnew.log`/`clocknew.txt` (a wrong suffix substitution); both lines were appended to `run.log` and `clock.txt` at 18:30 and the stray files removed (E149 in the session log). Neither file is among the hashed outputs.
- Copies: `out-candidate/` (the candidate A1–A5, README, checks), `review/` (the packet), `proposals/` (the ten staged sets and the combined set), `candidate-curation/` (the candidate's curation after promotion), `downstream/`, `batches/`.

(Two sentences of this note were corrected at 18:31:22 UTC, after the key was copied but before any scoring: the status distribution had been read from the step field, and the intervention count had been printed without saying that the entries are the automatic sessions.)

Anything changed after this point is labelled and not scored.
