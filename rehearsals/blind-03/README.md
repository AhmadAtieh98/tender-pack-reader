# Blind rehearsal 03: an independently written Addendum No. 3, processed with the AI layer in the loop

**Synthetic, not tender content.** An independent subagent wrote this addendum from the pack's PDFs, the brief and the correspondence, without seeing the implementation. Before the addendum was opened, its answer key was frozen by hash in `FROZEN.md`. It is the first rehearsal run through the session 09 workflow: the pattern drafter, then a model proposing through the narrow tools (the host route, no application API call), the deterministic controller validating and staging, a curator checking every proposal against the evidence, and the normal path to published outputs. It differs from blind-01 and blind-02 in kind: a change inside a definition (Working Day), a notified office closure that moves a derived deadline the cover says is unaffected, an Arabic text-layer substitution in an image-only form with a translation that differs from the governing Arabic, an image-only table value changed in words, a whole-clause deletion with cross-references, a form added by an earlier addendum reissued with an unmentioned new item, an earlier answer amended, and two deadlines for one application inside the same addendum.

| Path | What it is |
|---|---|
| `input/ADD-03_Addendum_No_3.pdf` | The blind addendum, as received |
| `FROZEN.md` | Hashes of the addendum and of the sealed answer key, recorded before the rehearsal |
| `SEALED/` | The answer key, author notes and builder script, added unchanged after the curated outputs (`cd SEALED && sha256sum -c --ignore-missing SHA256SUMS`; the PDF line from the repository root) |
| `setup_pack.py` | Builds `work/`: the received pack plus ADD-03, with copies of the curation. It uses the owner's reading approvals read-only. The real `curation/` and `config/` stay untouched |
| `work/` | The rehearsal's curation. `amendments/ADD-03.yaml` holds 27 ops and 4 dispositions. The register has 12 new rows (`rows/ADD-03.yaml`), 32 re-made readings, `issues/ADD-03.yaml` (7) and `evidence_items/ADD-03.yaml`; the A5 templates and assumptions; the clarification register as re-read at ADD-03 (cut-off 11 Nov 2026; 2 new draft questions; nothing sent) |
| `drafted-ADD-03.yaml` | What `tenderpack draft` proposed: 6 ops, 29 provisions left for a person |
| `out-drafted/` | Working draft with ADD-03 drafted (PARTIAL), published blind |
| `../../staging/ai/ADD-03-host-20261004T102718Z-97c1/` | The AI proposal run (host route): `review_request.md`, `proposals.yaml`, `log.jsonl`. Made before the live fixes; kept as made |
| `ai-proposals-used.md` | The curator's record of every AI item: used, corrected or rejected, and why |
| `out-curated/` | Working draft with ADD-03 curated (APPLIED), published blind at 11:01:55 UTC. **The scored output** |
| `diff-ADD-02-to-ADD-03.md` | `tenderpack diff` output, written blind |
| `out-after-fixes/`, `diff-after-fixes-ADD-02-to-ADD-03.md` | The same curation rebuilt after the post-key fixes listed in `COMPARISON.md`. Not scored; `scripts/verify_archive.py` rebuilds it |
| `clock.txt`, `*.log` | Wall-clock timestamps and command logs, including the AI run, the live fixes, the `pin --rows` crash and the post-key fixes |
| `COMPARISON.md` | Results against the answer key, with the timeline, the AI layer's measured contribution and the human review time |

The review packets (`out-*/review/`) and the evidence build (`build/`) are not committed; the commands below rebuild them.

## Reproduce

```
python rehearsals/blind-03/setup_pack.py          # only on a fresh checkout without work/ (work/ is committed)
python -m tenderpack ingest --pack rehearsals/blind-03/work/pack.yaml --out rehearsals/blind-03/build
python -m tenderpack outputs --evidence rehearsals/blind-03/build --pack rehearsals/blind-03/work/pack.yaml --out /tmp/blind03-out
python -m tenderpack diff --evidence rehearsals/blind-03/build --pack rehearsals/blind-03/work/pack.yaml --from ADD-02 --to ADD-03
# the AI step (host route, any coding assistant; see docs/AI_ROUTES.md §2-3):
python -m tenderpack ai task ADD-03 --claim --host-model "<model>" --evidence rehearsals/blind-03/build --pack rehearsals/blind-03/work/pack.yaml
```

Nothing here is accepted, approved or sent. Every op and row is PROPOSED; the release blockers in `outputs-curated.log` say so.
