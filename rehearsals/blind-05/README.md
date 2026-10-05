# Blind rehearsal 05: an independently written Addendum No. 3, processed by the workflow alone

**Synthetic, not tender content.** An independent author wrote this addendum (5 pages, "Issued 15 November 2026") on the base pack (Volumes I, II, IV, V as amended by Addenda 1 and 2), without reading the tool; its answer key was frozen by hash in `FROZEN.md` before the addendum was ingested. Nobody curated: `tenderpack ai run` took the PDF to candidate A1–A5 outputs and a review packet with fifteen headless host sessions that had only the MCP tools. The first candidate outputs were frozen (`FROZEN-OUTPUTS.md`) before the key was opened, then scored against it in `COMPARISON.md`.

**Result in one line:** of 38 expected findings, 21 hits, 16 partial, 1 missed; 1 false positive (the deleted VOL-I 6.7 left live in the candidate A1 and A5); 23 of 54 provisions unresolved, every reason honest; no manual intervention; about four hours of review estimated; 72 min 27 s against the brief's 30 minutes.

| Path | What it is |
|---|---|
| `input/ADD-03_Addendum_No_3.pdf` | The blind addendum, as received |
| `FROZEN.md` | Hashes of the addendum and of the sealed answer key, recorded before the run (4 Oct 2026, 19:20:22 UTC) |
| `FROZEN-OUTPUTS.md`, `FROZEN-OUTPUTS.sha256` | Hashes of the 327 copied run files at the freeze (5 Oct 2026, 04:08:13 UTC), before the key was opened. `clock.txt` fails the check only because the freeze line was appended to it; its first two lines match |
| `SEALED/` | The answer key (`expected_findings.yaml`), author notes and builder script, added unchanged after the freeze (`cd SEALED && sha256sum -c --ignore-missing SHA256SUMS`; the PDF line from the repository root) |
| `run.id`, `run.log`, `clock.txt`, `log.jsonl` | The run's id, its console log with the step timings, the wall clock (02:54:44 to 04:07:11 UTC) and the event log |
| `checkpoint.json`, `promotion.json` | Every step, batch, provision and intervention with its state and timing; the promotion record |
| `out-candidate/` | The candidate A1–A5 and checks as the run published them (banners; A1's candidate status column; the candidate A3 `a3/a3_candidate.md` and A5 `a5/candidate/`; the batch review packet `review/`). **The scored output** |
| `review/` | The run's review packet (`index.md`, `index.html`), the diff (`diff.md`, `diff.json`) and the before/after summary |
| `proposals/` | The staged analysis sets per host session (`ADD-03-host-*`) and the combined set (`ADD-03-run-host-blind05-…-combined/proposals.yaml`: 57 items, 74 statements) |
| `downstream/` | The downstream tasks, the 60 proposals, the critic's opinions, the answers, the impact and the promoted ops |
| `batches/` | The request packets and results of the reading, analysis and downstream batches |
| `candidate-curation/` | What the run wrote into the candidate: the op file (12 ops, 19 dispositions, 23 unresolved), the pending Arabic reading of the page-4 image, 2 new rows, 12 re-made readings, 3 issues, 7 activities, 1 clarification draft |
| `COMPARISON.md` | The scoring against the key: detection results, missed effects, unresolved decisions, manual interventions and review effort, separately; false positives, timing and follow-ups |

The full run folder, including the candidate workspace with its evidence build and the pre-addendum outputs, is `staging/ai/runs/ADD-03-run-host-blind05-20261005T025444Z/` (about 55 MB).

## Reproduce

```
python -m tenderpack ai run ADD-03 --pdf rehearsals/blind-05/input/ADD-03_Addendum_No_3.pdf --route host --host-model-alias <alias>
python -m tenderpack ai run-status <run_id>
python -m tenderpack ai resume <run_id>          # re-asks failed batches; never repeats a done provision
```

A run on the host route needs the host CLI; the alias used is recorded in `checkpoint.json` (`settings`). Nothing here is accepted, approved or sent; every op, disposition, row and reading is PROPOSED in the candidate, and the real `curation/`, `config/` and `out/` are only read.
