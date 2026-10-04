# Blind rehearsal 04: an independently written Addendum No. 3, processed by the workflow alone

**Synthetic, not tender content.** An independent subagent wrote this addendum (5 pages, "Issued 9 November 2026") on the base pack (Volumes I, II, IV, V as amended by Addenda 1 and 2), without seeing the implementation; its answer key was frozen by hash in `FROZEN.md` before the addendum was opened. Unlike blind-01 to blind-03, nobody curated: `tenderpack ai run` did the whole path from the PDF to candidate A1–A5 outputs and a review packet, with headless host sessions that had only the MCP tools. The first candidate outputs were frozen (`FROZEN-OUTPUTS.md`) before the key was opened.

| Path | What it is |
|---|---|
| `input/ADD-03_Addendum_No_3.pdf` | The blind addendum, as received |
| `FROZEN.md` | Hashes of the addendum and of the sealed answer key, recorded before the rehearsal |
| `FROZEN-OUTPUTS.md`, `FROZEN-OUTPUTS.sha256` | Hashes of the run folder's files at the freeze, before the key was opened |
| `SEALED/` | The answer key, author notes and builder script, added unchanged after the freeze (`cd SEALED && sha256sum -c --ignore-missing SHA256SUMS`; the PDF line from the repository root) |
| `run.log`, `run2.log`, `clock.txt` | Attempt 1 (refused at ingest: an unread image region), the live fix, attempt 2, the freeze, the unseal, the post-key resume |
| `out-candidate/` | The candidate A1–A5 and checks as the run published them (banners; A1's status column). **The scored output** |
| `review/` | The review packet (`index.md`, `index.html`), the diff (`diff.md`, `diff.json`) and the before/after summary |
| `proposals/` | The staged proposal runs per batch (`ADD-03-host-*`: `proposals.yaml`, `review_request.md`, `log.jsonl`), the reading session, the batch packets and the downstream packets |
| `candidate-curation/` | What the run wrote into the candidate: the op file (16 ops, 29 dispositions, 24 unresolved), the AI-proposed reading of the Form 4-H image (`readings/ADD-03-p4-r1.yaml`, pending), the relationships file, the templates and the clarification register as copied |
| `checkpoint.json`, `promotion.json`, `log.jsonl` | The run's checkpoint (every step, batch and provision with its state and timing), the promotion record, the run log |
| `COMPARISON.md` | Results against the answer key, the timeline, what the workflow did and did not do, the follow-ups |

The full run folder, including the candidate workspace with its evidence build and the pre-addendum outputs, is `staging/ai/runs/ADD-03-run-host-blind04-20261004T152505Z/` (about 54 MB).

## Reproduce

```
python -m tenderpack ai run ADD-03 --pdf rehearsals/blind-04/input/ADD-03_Addendum_No_3.pdf --route host --host-model-alias opus
python -m tenderpack ai run-status <run_id>
python -m tenderpack ai resume <run_id>          # re-asks failed batches; never repeats a done provision
```

A run on the host route needs the `claude` CLI; the recorded route replays a cassette (`--route recorded --cassette …`). Nothing here is accepted, approved or sent; every op, disposition and reading is PROPOSED in the candidate, and the real `curation/`, `config/` and `out/` are only read.
