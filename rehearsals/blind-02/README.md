# Blind rehearsal 02: an independently written Addendum No. 3

**Synthetic, not tender content.** An independent subagent wrote this addendum from the pack's PDFs and the brief, without seeing the implementation. Before the addendum was opened, its answer key was frozen by hash in `FROZEN.md`. This rehearsal differs from blind-01: the time moves on the same date, an appendix is replaced, an earlier addendum's change is revoked, list items are re-lettered and later referred to by their new letter, there is a deletion and a post-award insertion, clarification answers withdraw or create obligations, and notes to a reissued table change things the narrative does not mention.

| Path | What it is |
|---|---|
| `input/ADD-03_Addendum_No_3.pdf` | The blind addendum, as received |
| `FROZEN.md` | Hashes of the addendum and of the sealed answer key, recorded before the rehearsal |
| `SEALED/` | The answer key, author notes and builder script, added unchanged after the curated outputs (`cd SEALED && sha256sum -c --ignore-missing SHA256SUMS`; the PDF line from the repository root) |
| `setup_pack.py` | Builds `work/`: the received pack plus ADD-03, with copies of the curation. It uses the owner's reading approvals read-only. The real `curation/` and `config/` stay untouched |
| `work/` | The rehearsal's curation. `amendments/ADD-03.yaml` holds 31 ops and 5 dispositions. The register has 8 new rows (`rows/ADD-03.yaml`), 42 re-made readings and `issues/ADD-03.yaml`. Also the A5 templates and assumptions, and the clarification register as re-read at ADD-03 |
| `drafted-ADD-03.yaml` | What `tenderpack draft` proposed: 9 ops, 32 provisions left for a person |
| `out-drafted/` | Working draft with ADD-03 drafted (PARTIAL), published blind |
| `out-curated/` | Working draft with ADD-03 curated (APPLIED), published blind. **The scored output** (commit `ec8085b`) |
| `diff-ADD-02-to-ADD-03.md` | `tenderpack diff` output, written blind |
| `out-after-fixes/` | The same pack after the post-key fixes listed in `COMPARISON.md`. Not scored; `scripts/verify_archive.py` rebuilds it |
| `clock.txt`, `*.log` | Wall-clock timestamps and command logs, including the refused build (C47) and the live fixes |
| `COMPARISON.md` | Results against the answer key, with the timeline |

The review packets (`out-*/review/`) and the evidence build (`build/`) are not committed; the commands below rebuild them.

## Reproduce

```
python rehearsals/blind-02/setup_pack.py          # only on a fresh checkout without work/ (work/ is committed)
python -m tenderpack ingest --pack rehearsals/blind-02/work/pack.yaml --out rehearsals/blind-02/build
python -m tenderpack outputs --evidence rehearsals/blind-02/build --pack rehearsals/blind-02/work/pack.yaml --out /tmp/blind02-out
python -m tenderpack diff --evidence rehearsals/blind-02/build --pack rehearsals/blind-02/work/pack.yaml --from ADD-02 --to ADD-03
```

To reproduce the scored (pre-key) state, check out commit `ec8085b` first.

Nothing here is reviewed or accepted. Every op and every row is PROPOSED.
