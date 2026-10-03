# Session 06: reply to the owner (verbatim, as sent)

The draft package is ready and verified in a fresh location. I've sent the archive (`LAMAR-PPP-R2-DRAFT_4397987.zip`, 22 MB), the session report, the one-page A3 and the blind-rehearsal comparison. Nothing has been approved, accepted or refreshed for you.

**The optional macOS offline setup files (51–118 MB) were not delivered.** The upload server returned 502 errors, even after I split them into one zip per Mac type. They are only needed for an install without network (`VERIFY_ON_MAC.md` §3, option B); with network, `uv sync --extra dev` does the same. The 502 may be temporary, so ask me to send them again in a few minutes, or I can split them into smaller pieces.

**Still waiting on your review**

| Item | Status |
|---|---|
| Image readings (Table 2-4, Form 4-C) | 2 **pending** |
| Register rows | 202 **proposed** |
| Amendment ops | 37 **proposed** |
| STALE rows | 3 (proposals prepared, **not applied**) |

`outputs --strict` refuses a release until you've decided. The decisions file doesn't exist yet; only `accept` and `reject` create it.

**Results**

- **Your four findings:** all reproduced on `3c97a8d`, none disputed. I wrote 12 failing tests first, then fixed the rules:
  - **Inserted text:** the addendum must print all of it. A new check (C47) also refuses any word a clause gains that the addendum doesn't print.
  - **"Except that…" wording** is now left unresolved for a person instead of being dropped.
  - **New check C46:** every new or amended obligation must reach A1, A3 (where it has a consequence) and A5. Drill B without its good-standing row now fails visibly.
  - **The release gate** counts only named decisions tied to the content. A3 shows every item's confidence and the LCC's 35%. The "slice" labels are gone.
  - **On `dispositions.py`:** it was correct for what it does (accounting for provisions). The missing step was from op to rows, so the fix is a new trace, not a change to that file.
- **`accept` / `reject`:** each decision is tied to a fingerprint of the row or op, its evidence and its dependencies. Any later change voids it, and a rejected op makes its addendum PARTIAL.
- **Review batches** (`REVIEW/index.html`): 244 items in 9 batches. Images come first, then disqualifiers, then amendment ops, each with crops beside the reading and the exact command.
- **Live commands and coverage:**
  - `show VOL-I-8.6-01` gives the source pages, crops and amendment chain.
  - `diff` explains changed requirements, stale rows and readings, and the programme impact.
  - Row ids can no longer disappear (C12).
  - Every date or period phrase must be planned or explicitly treated (C30). Unsupported periods stay **unresolved**, never computed.
- **Blind rehearsal:** an independent agent wrote Addendum No. 3 from the sources and the brief. Its answer key was frozen by hash before I started.
  - **Score:** 22 hits, 4 partials, 1 miss (a clause renumbering).
  - **Time:** 12 min 13 s from receipt to replanned outputs, with four live fixes.
  - **A3 errors:** a stale "80,000" summary and the old clause number. Both are fixed now, but not counted in the score.
  - **Limits:** the author's brief named the kinds of change to include, and I did the curation. Your review time comes on top: 28 rows went STALE.
- **Archive verification** (on Linux):
  - Built from `4397987` and checked in a fresh folder: all 209 checksums match, and every A3 link and review-page link works. The repository bundle clones to that commit with its 16-commit history. Then, with no network at all, it installed from the offline package, rebuilt everything byte-identical to what's committed and to the archive (163 files), and passed all 339 tests.
  - I couldn't test on a Mac, in Preview or in Excel. The exact Mac commands are in `VERIFY_ON_MAC.md`.
- **Tests and determinism:** all 339 tests pass, and the outputs rebuild byte-identical.

**Decisions I need from you**

1. **Image readings:** approve or correct them (batch 1).
2. **Disqualifiers and amendment ops:** `accept` or `reject` the 19 disqualifier rows and 37 ops (batches 2–3).
3. **The three STALE-row proposals:** apply and accept them, or reject them (batch 4).
4. **LCC certificate lead time and issuer.** At the provisional 30 Working Days, the certificate is 7 WD short and the ratio chain 12 WD short. They fit at 23 WD or less (18 or less with the ratio calculation).
5. **Legal calls before the 12 Nov cut-off:**
   - the Form 4-C exclusion category;
   - what to sign on Form 4-A;
   - what goes in Envelope B;
   - prices in Envelope A;
   - the concession term;
   - the Volume III gap.
6. **A5 assumptions:** consortium size, copy counting and capacities.
7. **The remaining 183 rows:** who reviews which.
8. **Repository history:** do you want checkpoint `6a5d6cb` rewritten before a final archive? The bundle includes it, and in it your session 05 message, as first recorded, names a model.
9. **Generated outputs:** keep committing them, or rebuild them from sources and curation instead?

The full record is in `docs/session-06_report.md` and the work log. The Claude Code app, OpenRouter and Ollama integrations are still deferred, as you asked.
