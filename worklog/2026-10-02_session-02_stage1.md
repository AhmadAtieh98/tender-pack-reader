# Work log: session 02, plan revision 2 and Stage 1 implementation

- **Started:** 2026-10-01 ~21:40 UTC (2026-10-02 ~00:40 Riyadh).
- **Entry written:** 2026-10-01 ~22:40 UTC (2026-10-02 ~01:40 Riyadh).
- **Assistant:** Claude Code, cloud session. The model identifier is not written into the repository by the assistant.
- **Programmatic model API calls:** none. AI assistance was the coding assistant itself; see §6.
- **Status at end:** Stage 1 implemented. Two image readings are **PENDING HUMAN REVIEW**. Stages 2–6 are **PROPOSED**. Stopped at the checkpoint, as instructed.

## 1. Prompt (verbatim, as received)

~~~~text
@"/root/.claude/uploads/51ac768d-d630-5aa7-8c52-469fdeb8335c/ce151f9a-Gmail_-_Lamar_Holding___PPP_AI_Partner_Round_2_assignment.pdf" i’m comfortable with the overall direction. lets proceed with stage 1 only, with a few adjustments before we build on it

use the assumptions and output formats in my sent email,including excel for a1. bidder details remain configurable assumptions, not established facts. keep explicit disqualifiers separate from obligations without a stated consequence, and leave unresolved legal or commercial questions with people. (attached pdf) or challenge them

there are three engineering points i want tightened:

- finding an amendment’s quotation and changing its declared target does not prove it targeted the correct clause. explain how we catch an operation pointing to the wrong clause containing the same wording.
- keep original evidence separate from effective amended text. an assembled sentence may not exist verbatim on any single page, and image-only text cannot be checked through text-layer extraction
- a clause’s own hash is not enough to detect every stale interpretation. track the relevant dependencies too,and keep partially applied changes separate from the last fully validated state.

also, withdraw the claim that the amended TN limit necessarily satisfies the missing environmental permit. we cannot establish compliance with a document we do not have.

images, arabic and image based tables need to work properly from the foundation. dont tailor the solution only to the two images already found.

preserve source crops and their page references alongside the readings. for tables, retain the row and column relationships, headings, units, limits, assessment basis and notes. keep arabic source text separate from its translation and normalized matching text. check numerals, right-to-left order and actual rendered output,not just whether the characters were stored.

i read arabic and will review the transcription. give me the crops and proposed readings together, with uncertainties marked . leave sign-off pending until i actually approve it. don’t discard all rotated text either, identify the watermark specifically and show what was excluded.

eventually, i want the same program runnable through claude code in the app, with optional model calls through openrouter or local models through ollama on my macbook. keep a small common interface for these routes, with the same validation and review rules. check model capabilities rather than assuming every model supports images. implement the integrations later, the reviewed build must still work offline without a model. models should run on my m5 pro 48 vram mac, check best models as of oct 2026,, maybe latest qwen

keep the work log accurate: preserve prompts, replies, decisions, actual errors and verification evidence, including ai-assisted preparation and review. finding the second image was an additional finding, not a correction to a claim that only one existed.

update the plan, then implement stage 1. show me the extracted units, coverage and exclusions, both image-review packets, and the tests you actually ran. include split tables, footnotes, legitimate rotated text and a new mixed text/image example.

pending human review should not stop the ingestion work,but it must remain visibly pending. stop after this checkpoint so i can review the evidence before stage 2.
~~~~

- **Attachment:** the Gmail thread PDF (4 pages), stored as `sources/correspondence/Gmail - Lamar Holding - PPP AI Partner Round 2 assignment (thread to 2026-10-02).pdf`, sha256 `7c57cb29…7d19`.
- **Previous reply:** the session 01 reply is preserved verbatim in `worklog/2026-10-01_session-01_reply.md`.

## 2. Decisions

**By the owner (this prompt):**
- Direction accepted; proceed with Stage 1 only.
- Adopt the sent email's assumptions and formats, with Excel for A1.
- Bidder details are assumptions.
- Explicit disqualifiers are kept separate.
- Legal and commercial questions stay with people.
- Three engineering tightenings.
- TN/Permit claim withdrawn.
- Generic image, Arabic and table foundation.
- Review packets, with sign-off pending.
- Watermark identified specifically, and exclusions shown.
- Model routes later, with capability checks.
- Accurate work log.
- Stop at this checkpoint.

**By the assistant (operational, reversible; open to the owner's veto):**

| Decision | Reason |
|---|---|
| The email's assumptions are adopted rather than challenged | The only nuance: Appendix 1 has one two-member consortium. The member count stays editable, as the email says. |
| Package `tenderpack`; commands `ingest`, `show`, `approve` | — |
| Approvals live in `curation/approvals.yaml`, never inside readings | Each is pinned to the reading's content hash. |
| Arabic rendering checks use the Noto Naskh Arabic font bundled in PyMuPDF | Not system fonts, so the Linux and Mac results match. |
| numpy added as a runtime dependency | Pixel analysis: skew, grid, bands, despeckle, glyph shapes. |
| openpyxl deferred | Not needed until A1 is written. |
| `build/` committed at this checkpoint | It is the evidence the owner asked to see. Whether to keep committing it is an open question. |
| `uv.lock` added; Makefile with `setup`, `evidence`, `test`, `verify` | — |

## 3. Completed (done, not proposed)

1. **Thread read.** Read the Gmail thread and added it to `sources/`. Facts established:
   - the second path was offered on 17 Sep 20:00 and chosen on 17 Sep 20:12;
   - the session is "a ninety-minute slot in the week of 6 October (we will confirm once the panel locks times)";
   - the 1 Oct email was sent at 12:50;
   - a 2 Oct 00:05 draft exists (content hidden).
2. **Plan revised** (`docs/PLAN.md` revision 2):
   - **§R2:** the 12 adjustments;
   - **§R2-A:** citation-resolution target check;
   - **§R2-B:** evidence vs effective text;
   - **§R2-C:** dependency pins and validated/working states;
   - **§R2-D:** image/Arabic/table foundation;
   - **§R2-E:** model routes design;
   - **§9:** the Stage 1 checkpoint;
   - **F8 TN claim** withdrawn in place (struck through);
   - **O5 wording** corrected.
3. **Stage 1 implemented** (`tenderpack/`):
   - extraction with declared, audited furniture rules;
   - region detection (images, vector graphics, invisible text, unexplained ink), with crops;
   - segmentation (clauses, list items, footnotes with marker pairing, unit exponents, split tables, captions across pages, form fields, Q&A rows, notes, small print, rotated content);
   - readings with checks RD1–RD7;
   - numeral render checks and a glyph advisory;
   - review packets;
   - coverage checks C01–C06 and reports.
4. **Readings proposed:** `curation/readings/VOL-II-p3-r1.yaml` (Table 2-4) and `VOL-IV-p6-r1.yaml` (Form 4-C). Both are **pending**.
5. **Synthetic fixture:** `tests/fixtures/make_fixture.py`, which records what it placed. It holds a split table, a footnote, a unit exponent, a legitimate 90° rotated note, a colour-only watermark decoy, a mixed page (text, bilingual raster table, vector curve, text) and an OCR-style invisible layer.
6. **Tests:** 39 tests written and run (see §5). Mutation checks run (see §5).
7. **Model research** for §R2-E: web search and the GitHub Qwen and Ollama documentation. `ollama.com` and `openrouter.ai` are blocked by this environment's egress policy.

## 4. Errors and corrections (actual)

Numbering continues from session 01 (E1–E4).

| # | What was wrong | How it was caught | Correction |
|---|---|---|---|
| E5 | **Characterisation error (session 01):** I said O5 "missed a second image" / "you missed a second image". The owner's observation never claimed only one image existed. | Owner. | PLAN O5 now reads "Additional finding". The session 01 reply is preserved as sent, and this entry records the error. |
| E6 | **Unsupported claim (session 01, F8):** "Designing to the stricter 3 mg/l satisfies either reading." Compliance with a Permit that is not in the pack cannot be established. | Owner. | Withdrawn in place (R2.6). |
| E7 | First furniture-config comment said the watermark angle was 45° and the footer was 6.8 pt; written from the session-01 impression. | Inventory of every grey or rotated span. | Measured values are 52.0° and 6.4 pt. Corrected before any run. |
| E8 | **Premature claim to the owner mid-task:** "the left digit matches ٣ (three), not ٢". It rested on one template-overlap score (0.583 vs 0.492). | Second method (chamfer distance; 3 thresholds, all favour ٢) plus a side-by-side visual. | Reading now proposes ٢ (§4.2), marked **uncertain**, with ٣ (§4.3) as the alternative and the evidence image. Session 01's "٤-٢" had been asserted without pixel checks: the order is now verified by rendering; the identity stays with the reviewer. |
| E9 | **Wrong claim to the owner mid-task:** "spot-check found hamza differences… 'ادناه', 'اي', 'اعضاء' without hamza, 'كاملا' without tanween". | A 300 dpi sheet disagreed; I then checked native pixels at 2×. The 220 dpi render had been displayed at half scale. | All four words carry their hamza/tanween. Design consequence: packets show crops at native resolution only, never downscaled; the reading's uncertainties tell the reviewer to use native crops. |
| E10 | **Segmenter bugs on first runs:** (a) a superscript joined the line above by 0.01 pt of overlap, so footnote 12 was keyed to `VOL-I:S8/para1` and the m³ inside it became a "footnote marker 3"; (b) ADD-02 notes were not small print, because body size was measured including 8.2 pt table text; (c) duplicate IDs `F4-A/para1`; (d) banner lines merged ("…014Issued…"). | Problems list, unassigned-span count, and reading the unit listing. | Structural fixes: baseline grouping; "satellite" spans attach to the span they touch; body size measured on flow text only; separate ID schemes. |
| E11 | Band detection (fixed threshold 110) **missed the faint grey footer inside the Form 4-C image**. Then rule bands were not recognised (skewed rules have no long pixel runs). | Overlay image; band list checked against the image. | Threshold relative to the image's own background, plus despeckle and ruling-line erasure; rules classified by shape. |
| E12 | **Footnote marker fused into matching text:** NFKC turned "¹²" into "12", giving "Form 4-B.12". | Test `test_footnote_12_keeps_its_rejection_rule` failed. | Matching text is now built from spans with markers dropped. |
| E13 | Golden expectation incomplete: listed 2 units with "seventy-two (72) hours"; ADD-02 §4.1 quotes it too. | Test failed. | Expectation scoped to the volumes (the addendum's quote is the amendment source, not a target). Recorded as an oracle correction, not a code fix. |
| E14 | Rebuild not location-independent: builds outside the repo wrote absolute paths. | `test_rebuild_is_byte_identical` failed. | All evidence paths made relative to the build directory. |
| E15 | Trace test bug: looked for the column heading "Ref:", which we add, in table rows. | Test failed on `VOL-I:T1-1/A`. | Test uses the first cell value instead. |
| E16 | A careless bulk replace inserted literal `%s` placeholders into `regions.py` / `packets.py`. | Read the grep output immediately after. | Replaced with a `relpath()` helper. |
| E17 | **Weak test:** the watermark decoy differed in size (20 pt) as well as colour, so removing the colour attribute did not fail the test (mutation survived). | Mutation run. | Decoy now differs only in colour; the same mutation now fails the test. |
| E18 | Fixture: base-14 Helvetica cannot encode an em dash (renders "·"). | Inspection of fixture spans. | Fixture uses ASCII and its own rule text (documented in the fixture). |
| E19 | Packet notes used a Latin-only font, so Arabic showed as dots; two labels overlapped. | Viewing the generated images. | HTML rendering with font fallback; layout fixed. |
| E20 | First version of `worklog/2026-10-01_session-01_reply.md` was a **reconstruction from memory**, not the sent text. | Re-read against the transcript before commit. | Replaced with the transcript text. |
| E21 | **ADD-01 Appendix B (minutes) collapsed into one paragraph unit**: the continuation rule ran before the bold lead-in rule, so "Present:" and Items 1–7 were absorbed. | Spot-check of `build/units.md` before commit; no automated check covered it. | A lead-in now starts a new unit only after a paragraph, not inside a clause (where ADD-01 §2.1 wraps onto a bold line). New test `test_minutes_items_are_separate_units` covers both cases. Units 517 → 525. |

## 5. Verification evidence (commands actually run)

**`python -m tenderpack ingest` on the real pack:**

```
C01 pass  6 documents match sources/manifest.json (sha256, pages)
C02 pass  32 pages accounted for out of 32
C03 pass  1240 of 1240 content spans assigned to exactly one unit
C04 pass  160 spans excluded, all by declared rules: {'FOOTER-DISCLAIMER': 32, 'FOOTER-PAGE': 32, 'HEADER-REF': 32, 'HEADER-TITLE': 32, 'WATERMARK': 32}; expected-count problems: none
C05 pass  2 regions; unread none; readings failing checks none; PENDING HUMAN REVIEW: ['VOL-II-p3-r1', 'VOL-IV-p6-r1']
C06 pass  12 superscripts: 11 unit exponents, 1 footnote markers (all paired: True); unclassified 0
```

**Synthetic fixture.** C05 **fails by design**: 3 regions are unread and visibly reported.

```
C03 pass  43 of 43 content spans assigned to exactly one unit
C04 pass  15 spans excluded, all by declared rules: {'FOOTER-PAGE': 5, 'HEADER-SYN': 5, 'WATERMARK': 5}
C05 FAIL  3 regions; unread ['SYN-01-p4-r1', 'SYN-01-p4-r2', 'SYN-01-p5-r1']
C06 pass  2 superscripts: 1 unit exponents, 1 footnote markers (all paired: True)
```

**Test suite and mutations:**

| Run | Result |
|---|---|
| `pytest -q` (final) | **39 passed** (about 21 s). Earlier runs: 34 passed / 4 failed (E12–E15); then 38 passed before E21's test was added. |
| Mutation 1: colour attribute removed from the WATERMARK rule | Before E17: 7 passed (mutation survived). After: **1 failed** (killed). |
| Mutation 2: unit-exponent recognition disabled | **3 failed** (killed). |
| `make verify`: two clean rebuilds | Output hashes **identical**. |

**Reading checks (both readings):**
- RD1–RD6 all pass.
- RD4: Form 4-C has 23 text bands and 9 rule bands; all 32 text segments (9 split left/right) are read. Table 2-4: grid 12 × 5 rules = 11 × 4 cells at skew −0.34°.
- RD7: **WARNING** on Table 2-4, because Note 1 touches the image's bottom edge.

**Numeral evidence for "٤-x" (VOL-IV p6, crop [293, 410, 310, 433] pt):**

| Method | ٢ | ٣ |
|---|---|---|
| Chamfer distance (lower = closer), thresholds 100 / 130 / 160 | 0.0162 / 0.0153 / 0.0124 | 0.0187 / 0.0181 / 0.0171 |
| Template overlap (higher = closer) | 0.492 | 0.583 |

- The rendered visual order of the stored logical "٤-٢" is "٢-٤", which matches the crop.

**Native-pixel checks:** hamza on "أدناه", "أي", "أعضاء" and tanween on "كاملاً" are present (2× native crops).

## 6. AI-assisted preparation and review

- **Readings:** both proposed readings were prepared by the coding assistant reading the native images visually. No OCR and no separate model API.
  - The Arabic was cross-checked on native-pixel crops.
  - Digits were checked by two shape methods and a visual comparison.
  - The status is **pending**: the owner reads Arabic and will review.
- **Model research:** WebSearch (secondary blogs, flagged as such in the plan); GitHub `QwenLM/Qwen3.8` README; `ollama/ollama` `docs/api.md`.
- **Review of this work:** not yet done by a person.

## 7. Unresolved questions

1. **Owner's review** of the two packets, especially the ٢/٣ digit (VOL-I §4.2 vs §4.3) and the hamza and tanween marks.
2. **Session date and time:** week of 6 Oct, to be confirmed by the panel.
3. **D3** (A1 granularity and scope) and **D4** (counting conventions) are still open.
4. Keep committing `build/`, or regenerate it only?
5. OpenRouter capability field names are unverified here (host blocked). If wanted, the owner can allow `openrouter.ai` and `ollama.com` in the environment's network settings.

## 8. Proposed next actions (not done; awaiting the owner)

- **Stage 2**, after review:
  - a thin end-to-end slice through the hard amendments;
  - include the §R2-A citation resolver and §R2-C dependency pins / two-state build from the start;
  - treat ADD-02 as unseen and draft it through the drafter.
