# Blind rehearsal 07: the workflow's candidate against the sealed answer key (ADD-03)

**Synthetic, not tender content.** This is a **sealed rehearsal, scored after the freeze**. I used only the frozen copies in this folder and the key opened after the freeze. Nothing under `out-candidate/`, `review/`, `proposals/`, `candidate-curation/`, `downstream/` or `batches/` was changed, and nothing was re-run. The only command executed against the run is the read-only `scripts/bench_workflow.py --from-run`.

- **Scorer:** a separate agent session that neither wrote the addendum nor built the tool. Model **Opus 5.5 (`claude-opus-5-5`)**; the runtime showed a reasoning-effort setting of **40**.
- **Elapsed:** scoring started 20:36:03 UTC and ended 20:56:21 UTC (**20 min 18 s**).

Paths are relative to `rehearsals/blind-07/`; L means line. Short names in the evidence columns:

| Short name | File |
|---|---|
| `pkt` | `review/index.md` (the review packet, 881 lines) |
| `P` | `proposals/ADD-03-run-host-20261006T201359Z-2503-combined/proposals.yaml` (57 analysis items, 8 statements) |
| `DS` | `downstream/proposals.yaml` (23 downstream items, 5 statements, 17 tasks) |
| `ops` | `candidate-curation/amendments/ADD-03.yaml` (the candidate op file) |
| `rd` | `candidate-curation/readings/ADD-03-p3-r1.yaml` (the image reading) |
| `a1` | `out-candidate/a1/a1.csv` (physical line numbers) |
| `a3c` | `out-candidate/a3/a3_candidate.md` |
| `a5m` | `out-candidate/a5/candidate/milestones.csv` |
| `a2cov` | `out-candidate/a2/a2_cover_summary_check.csv` |
| `ckpt` | `checkpoint.json` |
| `log` | `log.jsonl` |
| `bench` | the output of `.venv/bin/python scripts/bench_workflow.py --from-run <run folder>` (main tree's Python), run by me at 20:40:56 UTC |

## What was frozen and when

### The addendum

The independent author's Addendum No. 3 is 4 pages and "Issued 17 November 2026", a Tuesday. That is three Working Days **after** the VOL-I 5.2 clarification cut-off (Thu 12 Nov). No Bidder can clarify it, so the key reserves its ambiguity (DA1) and its judgment item (HJ1) for a person. Its subjects:

- **The Change in Law threshold.** 2.1 applies a relative delta ("reduced by SAR 1,000,000") to VOL-V 36.2 as ADD-02 amended it (2,500,000 → 1,500,000). The cover says 4,000,000.
- **The handback survey.** VOL-II 8.5 is relocated, with its text unchanged, to a new VOL-V 42.3.
- **Table 42-1.** VOL-V 42.1 gets a new per-class schedule held only in an Arabic image on page 3. The image governs; its English convenience translation on page 4 differs:
  - row 4: 7 years in the Arabic, 5 in the English;
  - row 5: 24 months in the Arabic, "24" under a years heading in the English;
  - an English-only note (4).
- **Ground conditions.** A new VOL-V 12.5 gives relief against a Geotechnical Baseline Report Revision C that the pack does not supply.
- **Core inspection.** 4.3 sets up appointments with a forward-counted deadline. 4.4 disapplies VOL-I 4.2 for those appointments only.
- **Answers 15–19:** a decoy, two confirming answers, one changing answer (Envelope B and the DSCR) and one judgment answer (the Direct Agreement against VOL-V 40.2).

### Timeline and checks

- **The sealed key.** `cd SEALED && sha256sum -c --ignore-missing SHA256SUMS`: `build_addendum.py`, `expected_findings.yaml` and `author_notes.md` are all OK.
  - The PDF line is checked from the repository root: `06afe32f…bc8d`, OK.
  - `sha256sum SEALED/SHA256SUMS` = `03174efc…adaab`. This is the value in `FROZEN.md`.
- **The frozen outputs.** `sha256sum FROZEN-OUTPUTS.sha256` = `5365cea5…512e`, the value in `FROZEN.md`.
  - `sha256sum -c FROZEN-OUTPUTS.sha256` run **from this folder** gives **313 of 313 OK**.
  - **Record slip:** `FROZEN.md` says to run the check "from the repository root". The listed paths are relative to `rehearsals/blind-07/`, so from the root every line fails.
- **Order of events** (`clock.txt`):
  - freeze 20:34:15;
  - key copied into `SEALED/` 20:34:46;
  - the three sealed files carry 20:34 file times;
  - I opened the key after verifying the hashes.
- **Files that are not hashed:** `run.log`, `run.log.attempt1`, `clock.txt`, `run.id`, `run.id.attempt1`, `FROZEN.md`. Hashed files corroborate them:
  - `ckpt`, `log` and `promotion.json` are byte-identical (`cmp`) to the copies in the run folder in the session scratchpad (`…/unzipped4/…/staging/ai/runs/ADD-03-run-host-20261006T201359Z-2503`);
  - `ckpt` `created` 20:13:59 and `updated` 20:33:47 match `clock.txt` (upload 20:13:57, end 20:33:48);
  - `ckpt` `events` hold the SIGTERM (`interrupted` 20:20:32) and the resume (`resumed` 20:20:41, pid 18147).
- **What `run.log` holds.** It is cumulative: the four attempts' job logs in order (L1–173 attempt 1 and its failed resume; L175–261 attempt 2; L262–400 attempt 3; L401–583 attempt 4). `run.log.attempt1` equals its first 173 lines.
- **What is scored.** Only attempt 4, run `ADD-03-run-host-20261006T201359Z-2503` (`run.id`).
- **Nothing is decided.** Every op, disposition, reading, row and issue is PROPOSED. Human approval: none (`pkt` L16; `ckpt` `approval`).

## The key

`SEALED/expected_findings.yaml` holds:

- 15 provisions (1.1–1.3, 2.1–2.2, 3.1–3.6, 4.1–4.4);
- 5 answers (15 decoy, 16 confirming, 17 changing, 18 human judgment, 19 confirming of 4.3);
- 3 planted cover errors (E1 stale-base arithmetic, E2 modality downgrade, E3 cardinality);
- 7 change types (CT1–CT7);
- 6 secondary undisclosed effects (SU1–SU6) and 9 indirect effects (IE1–IE9);
- 7 derived dates (D0–D5 and a holiday assumption);
- 7 marshalling effects (M1–M7) and a 4-item A3 delta;
- 3 missing-evidence items (ME1–ME3), one deliberate ambiguity (DA1) and one human-judgment item (HJ1);
- 3 Arabic discrepancies (AR1–AR3) and 37 Arabic strings of the image;
- 24 must-not-report traps and 3 acceptable-if-raised points.

## Scoring method

**N = 33 detection items:**
- 15 provisions;
- 5 answers;
- 3 cover errors;
- 4 image items: the reading, AR1, AR2 and AR3;
- 6 secondary effects.

The following are scored in their own tables and not added to N, as blind-06 did: indirect effects, dates, marshalling, the A3 delta, missing evidence, DA1, HJ1 and the traps.

The verdicts follow blind-06's rules:

- **Hit:** the frozen outputs state the effect correctly (target, words, values, consequence).
- **Partial:** the effect is detected but incomplete, wrongly targeted, or left unresolved or escalated where the key expects a definite change.
- **Missed:** absent, or present only in a form that contradicts the key.

Applied as blind-06 applied them:

- **Provisions and answers.** These expect a definite change or disposition. A hit needs the right effect in a **promoted** item (op, row, disposition, issue or computed milestone), or an escalation where the key itself expects one. The right content only in an unpromoted or invalid item scores **partial** ("detected, not applied").
- **Cover errors, the image items and secondary or indirect effects.** Detection anywhere in the frozen outputs counts. They score partial when the run keeps open a reading the key rules out.

## 1. Detection

**Count: 33 expected findings: 11 hits, 17 partial, 5 missed.**

| Group | Hit | Partial | Missed |
|---|---|---|---|
| Provisions (15) | 5 | 10 | 0 |
| Answers (5): decoy / confirming ×2 / changing / human judgment | 2 | 3 | 0 |
| Cover planted errors (3) | 1 | 1 | 1 |
| Arabic image: reading, AR1, AR2, AR3 (4) | 2 | 2 | 0 |
| Secondary undisclosed effects (6) | 1 | 1 | 4 |

Scored separately:

| Group | Result |
|---|---|
| Indirect effects (9) | 2 hit, 3 partial, 4 missed |
| Derived dates (7) | 7 right (D2 with both readings and the earlier date planned) |
| Marshalling (7) | 2 hit, 4 partial, 1 missed |
| A3 delta (4) | 2 hit, 2 partial |
| Missing evidence (3) | 1 hit, 1 partial, 1 missed |
| DA1 (deliberate ambiguity) / HJ1 (human judgment) | **missed** / **hit** |
| Must-not-report traps (24) | 24 avoided as assertions; 4 borderline (section 4) |
| Wrong statements | 5 false positives, 10 false signals (section 4) |

### Provisions (15): 5 hit, 10 partial, 0 missed

| Key | Change type | Expected | Result | Evidence |
|---|---|---|---|---|
| 1.1 | recital | ordinary precedence recital; decides nothing between non-RFP documents | **hit** | `no_effect`: "it restates the existing Clause 3.2 order of precedence and edits no unit" (`ops` L60–70; `P` L437) |
| 1.2 | interpretation | every reference is to the clause as amended, so 2.1 operates on SAR 2,500,000 | **partial** | Effect named, not applied. The promoted disposition is `unresolved`: "It bears on the base of ADD-03:2.1 (VOL-V:36.2 at ADD-02 is SAR 2,500,000) and conflicts with the cover figure; a person must confirm its effect" (`ops` L71–80). The issue says 1.2 is "favouring the ADD-02 base" (`P` L372) |
| 1.3 | recital | requests 15–19 were in time; ADD-03 is issued after the 12 Nov cut-off | **hit** | `no_effect` (`ops` L81–89). The packet computes "the clarification window closed on 2026-11-12 (VOL-I 5.2) … (ADD-03 issued 2026-11-17 …)" (`pkt` L108) |
| 2.1 | CT1 delta on an ADD-02 value | 36.2 threshold SAR 1,500,000 (5.0M → 2.5M → 1.5M) | **partial** | <ul><li>Read: "2.1 prints a change ('is reduced by SAR 1,000,000') to VOL-V:36.2, whose ADD-02 text states SAR 2,500,000" (`ops` L90–99).</li><li>No figure is proposed: "Reading B: 2.1 reduces the ADD-02 amount by SAR 1,000,000 (result to be computed by a person/approved method)" (`P` L344–372).</li><li>**SAR 1,500,000 appears in no frozen file.**</li><li>A1 still shows SAR 2,500,000 at ADD-03 (`a1` L456; false signal 1). The candidate A3 lists the row as not settled (`a3c` L136)</li></ul> |
| 2.2 | instruction | price the Availability Payment on 1.5M; no rejection consequence | **partial** | Row proposed with "none stated in this provision" and "Depends on the unresolved figure in ADD-03:2.1" (`P` L677–715). It is **invalid**: "Consequence Input should be a valid dictionary" (`pkt` L210) |
| 3.1 | CT2 relocation | VOL-V 42.3 with the same text; the obligation continues; now Volume V, rank 3.2(c); A1 traced to 42.3 | **partial** | <ul><li>Escalated as a software limitation: "Text is stated unchanged from VOL-II:8.5, so no new obligation is created, only a new location" (`P` L761; `pkt` L110–114).</li><li>The paired `set_status VOL-II:8.5 deleted` is invalid (`P` L856–881; `pkt` L220–221).</li><li>The rank change and Form 4-E are not stated.</li><li>VOL-II-8.5-01/02 are UNRESOLVED (`a1` L259; `a3c` L131–132)</li></ul> |
| 3.2 | numbering rule | 8.5 vacant; nothing renumbered | **hit** | `no_effect`: "The number 8.5 is not reused in Volume II, and the Clauses of Volume II are not renumbered" (`ops` L100–108). Its reason leans on the invalid deletion op ("the vacancy of 8.5 is handled by ADD-03/3.1(b)"). A semantic false signal fires on it (`pkt` L227) |
| 3.3 | CT2 repoint | 42.1: "Volume II Clause 8.5" → "Clause 42.3" | **partial** | The op is exactly right: `replace_text VOL-V:42.1 "Volume II Clause 8.5" → "Clause 42.3"` (`P` L1004–1029). It is held **conflicting** for "dependencies: unknown ids ['ADD-03/3.1(a)']" and a same-unit consistency flag with 3.4 (`pkt` L231–232). The critic: "The replace_text op matches the provision wording" (`pkt` L234) |
| 3.4 | CT3 single value → per-class Arabic schedule | 42.1 new words; five classes from the image: 20/20/5/**7**/**24 months** | **partial** | <ul><li>The op is exactly right (`P` L1118–1144). It is held conflicting because "fact analysis-002/S1 is not supported verbatim" (`pkt` L244).</li><li>The table insertion is escalated as a software limitation (`pkt` L115–117).</li><li>Five rows were made from the reading, with the Arabic values. They are **conditional, not in force**: `ADD-03-T42-1-01`…`05` (`DS` L995–1558; `a1` L57, L62; `pkt` L153–157)</li></ul> |
| 3.5 | language precedence | the Arabic image governs over Appendix B | **partial** (over-escalated) | <ul><li>The promoted disposition is `unresolved`: "which rendering governs is a person's decision (Legal)" (`ops` L109–118).</li><li>The analysis statement says it outright: "the 3.5 wording is not applied here" (`P` L71).</li><li>The controller applies the rule only downstream ("applied rule: ADD-03 3.5 provides: 'The Arabic text governs.' (applied, not decided)", `pkt` L371)</li></ul> |
| 3.6 | new mandatory content | "shall demonstrate"; criterion C; no rejection consequence | **partial** | Row proposed as mandatory with "the pack states no consequence for non-compliance in 3.6 itself" (`P` L1551–1588). It is **invalid**: "scope Input should be a valid list … discipline Field required" (`pkt` L278). Criterion C is not linked |
| 4.1 | CT7 new clause | new 12.5: Scheduled PCOD extension **and** costs, notice within 5 WD; GBR Rev C | **hit** | `insert_unit` after VOL-V:12.4 with the clause text verbatim, evidence_verified and promoted (`ops` L26–44; `pkt` L280–283). Row ADD-03-4.1-01 NEW (`a1` L41; `DS` L199). A5 REWORK deviations-review and form-4e (`pkt` L798, L815). Caveat: the new text omits the label "12.5" (critic, `pkt` L620) |
| 4.2 | new mandatory content | state the assumed ground conditions by reference to the GBR; no consequence | **partial** | Row proposed with `consequence: none_stated`. It is **invalid**: "confidence Field required" (`P` L3503; `pkt` L297). The GBR is not flagged as missing |
| 4.3 | optional procedure + deadlines | request within 3 WD of 17 Nov (Sun 22 or Thu 19; no forward rule); appointments by Mon 23 Nov | **hit** | <ul><li>Promoted rows ADD-03-4.3-01 (23 Nov) and -02 (`DS` L1628, L1729; `a1` L67–68).</li><li>`pkt` L147–148: "AMBIGUOUS: 2026-11-22 (event_day_excluded); 2026-11-19 (event_day_counted) … no rule … for Working Days counted after a date".</li><li>A5 plans 19 Nov and keeps the other reading (`a5m` L9–10).</li><li>The analysis row itself was invalid (`P` L3584); downstream's computed-date tasks recovered it</li></ul> |
| 4.4 | CT4 bounded disapplication | VOL-I 4.2 not applied to core-appointment communications only; A3 item narrows; 4.1 not disapplied; Form 4-C read with the carve-out | **partial** | <ul><li>Escalated as "a partial disapplication of a clause that carries disqualification … no op type represents a scoped exception" (`P` L3679–3701).</li><li>A scope issue was raised (acceptable-if-raised; `P` L3762–3787).</li><li>VOL-I-4.2-01 is UNRESOLVED (`a1` L90; `a3c` L126), but the diff says "Disqualifiers (A3) — no change" (`pkt` L778–780).</li><li>VOL-I 4.1 and Form 4-C are not mentioned anywhere</li></ul> |

### Answers (5): 2 hit, 3 partial

| Key | Class | Expected | Result | Evidence |
|---|---|---|---|---|
| Q15 | decoy | no effect | **partial** | Read right: "The response confirms ADD-01 3.2 and adds no new obligation" (`P` L3821–3895). The `annotate … confirms` op is **invalid**: "previous_value: no target to compare the previous value … with" (`pkt` L318–319). Q15 is therefore UNRESOLVED (`pkt` L704) |
| Q16 | confirming (imperative) | no new or changed row | **partial** | Read right: "The response restates the same three elements as the clause; no wording differs in substance" (`P` L3898–3972). It is invalid on the same check, so VOL-II-9.3-01 shows **UNRESOLVED** in A1 (`a1` L264; false signal 3) |
| Q17 | changing | (a) the schedule is part of Form 4-F in Envelope B; (b) + minimum annual DSCR; (c) in Envelope A → VOL-I 6.2, non-responsive | **partial** | <ul><li>(a) and (b) are stated: "New obligation: the DSCR statement is not in 10.6 … Placement in Envelope B is consistent with 10.1 only if the schedule is treated as part of Form 4-F (the Authority's words)" (`P` L4075–4076).</li><li>(c) is hedged: "Q17 does not itself say a schedule in Envelope A is non-responsive, and whether it is 'commercial information' is for a person" (`P` L4077–4078).</li><li>The annotate is invalid (`pkt` L328–329), so VOL-I-10.1/10.6/6.2 and the Form 4-F rows stay UNRESOLVED (`a3c` L124–128, L134–135), and I-VOL-I-ENV-B stays open (`a3c` L194)</li></ul> |
| Q18 | human judgment | escalate; no winner; the DA is not an RFP Document and does not exist yet | **hit** | <ul><li>`unresolved`: "does not say which of Volume V Clause 40.2 or a Direct Agreement prevails … Which governs is a person's decision (Legal)" (`P` L4081).</li><li>The issue lists Reading A and Reading B without choosing (`P` L4166–4190).</li><li>DS-007: "The response does not say that the Direct Agreement, which is not yet negotiated, ranks in that order" (`DS` L528–553).</li><li>Nothing records "Volume V prevails"</li></ul> |
| Q19 | confirming of 4.3 | points to 4.3; late requests are not accommodated; plan to Thu 19 Nov | **hit** | Promoted disposition: "Section 4.3 … applies. Requests made after the period … will not be accommodated … Not no_effect because the words oblige" (`ops` L276–287; `P` L4259). A5 plans the request deadline at 2026-11-19, with "2026-11-22 if the ADD-03 issue day is excluded" (`a5m` L9) |

### The cover's planted errors (3): 1 hit, 1 partial, 1 missed

| Key | Mechanism | Result | Evidence |
|---|---|---|---|
| E1 | stale-base arithmetic: "to SAR 4,000,000" | **partial** | <ul><li>The mechanism is found exactly: Reading A, 4,000,000, "would be consistent with a reduction of SAR 1,000,000 from the as-issued SAR 5,000,000".</li><li>The cover's figure is still offered as a reading: "The cover does not amend; which governs is a person's decision. No op proposed for VOL-V:36.2" (`P` L344–372).</li><li>The issue is **not promoted** ("an analysis issue is not promoted", `pkt` L536, L552). The promoted cover op points to "a separate issue" that was dropped (`ops` L20–21)</li></ul> |
| E2 | modality downgrade: "invites Bidders to describe" against 3.6 "shall demonstrate" | **missed** | No item compares the two verbs. C28 reports the whole comma segment "not found: … no provision of ADD-03 does this" (`a2cov`; `pkt` L731). The same message appears for segments that are accurate (false positive 3) |
| E3 | cardinality: "four asset classes" against five rows | **hit** | Promoted disposition AppB/para2: "cover/para3 says 'four asset classes' while Table 42-1 lists five rows; reported, not resolved" (`ops` L211–220; `P` L2515). It is repeated in the unpromoted Table issue (`P` L3238) |

### The Arabic image (4): 2 hit, 2 partial

| Key | Expected | Result | Evidence |
|---|---|---|---|
| Reading | every Arabic string verbatim, translations apart, pending | **hit** | <ul><li>`rd`: **35 of the key's 37 strings verbatim** (checked by script).</li><li>Two vowel-mark slips:<ul><li>the qualifier reads مبيِّن for مبيَّن;</li><li>note ٣ reads كلَّ for كلُّ.</li></ul></li><li>Uncertainties declared: "Row 5 life is printed in months under a years heading", "Vocalisation marks … not verified" (`pkt` L100–102).</li><li>The reading is pending; 109.7 s, read at the first call (`bench`)</li></ul> |
| AR1 | row 4: Arabic ٧ (7) against English 5; the Arabic governs | **hit** | "Crop viewed: the cell clearly shows ٧. Clause 3.5 says Arabic governs; a person (Legal/Technical) must confirm which value applies" (`P` L1883–1907). Conditional row ADD-03-T42-1-04 carries `min_remaining_life_years: 7` (`DS` L1328; `a1` L57). The rule itself is over-escalated (section 5) |
| AR2 | row 5: ٢٤ شهراً = 24 months governs | **partial** | Detected. But the run keeps "24 years" open: "Readings: 24 months, or 24 years; a person … must decide; not chosen here" (`P` L1960). ESC-T42-5 says "24 years and 24 months are both supported by the words" (`DS` L882). The promoted issue I-ADD-03-T42-5-UNIT does the same (`DS` L1558) |
| AR3 | the English-only note (4) has no force; VOL-II 2.2 unchanged | **partial** | Detected: "The note appears only in the English translation; the governing Arabic page has three notes only (crop viewed) … Readings: (a) note (4) is a binding amendment … (b) it has no force … No op is proposed until a person (Legal) decides" (`P` L3073–3100). Downstream then treats the note as operative (ESC-NOTE4, `DS` L923–945). VOL-II-2.2-01/02 are UNRESOLVED (`a1` L179–180) |

### Secondary undisclosed effects (6): 1 hit, 1 partial, 4 missed

| Key | Expected | Result | Evidence |
|---|---|---|---|
| SU1 | ADD-01 response 4 ("Bidders shall satisfy themselves") is made incomplete by 12.5 | **missed** | "Earlier answers to re-read against the new text — none" (`pkt` L782–784). A3 lists I-OP-ADD-01/Q4 as "not reached by this addendum's changes" (`a3c` L176) |
| SU2 | the relocated survey falls within Form 4-E (deemed acceptance) and rises in rank from (d) to (c) | **partial** | Only DS-003: "Existing rules VOL-I:9.6 and VOL-I:10.5 (non_responsive) are shared with Volume V, so a person decides whether either covers this" (`DS` L294–319). Neither the deemed acceptance nor the rank change is stated |
| SU3 | 12.5 moves the Scheduled PCOD → 18.1 / 18.3 / 39.2; time and cost (not a Relief Event); 3.3 not engaged | **missed** | "downstream: units changed VOL-V:12.4+ADD-03; rows citing them none" (`pkt` L290). 18.1, 18.3, 39.2, "Relief Event" and 34.1 appear in no item (`P`, `DS`) |
| SU4 | Arabic row 4 (7 years) against VOL-II 2.2 forces electrical/I&C replacement before handback; lifecycle capex, AP, 42.2 reserve | **missed** | VOL-II 2.2 is reached only through note (4). No item links row 4 to 2.2, lifecycle or 42.2 |
| SU5 | VOL-I 4.1 not disapplied; Form 4-C decl. 5 (البند ٤-٢, in an image) read with the carve-out | **missed** | VOL-I 4.1 and Form 4-C appear in no item. The 4.4 escalation's scope is "rows VOL-I-4.2-01; activities none" (`pkt` L124) |
| SU6 | Q17 removes the 10.1 / Form 4-F "only" conflict; the schedule gains the DSCR | **hit** | `P` L4075–4076 (as Q17) |

### Indirect effects (9): 2 hit, 3 partial, 4 missed

| Key | Result | Evidence |
|---|---|---|
| IE1 (12.5 → ADD-01 response 4 superseded in part; VOL-I 5.5 qualified) | **missed** | as SU1 |
| IE2 (relocation → Form 4-E → deemed acceptance → rank (d)→(c)) | **partial** | as SU2 |
| IE3 (12.5 → Scheduled PCOD → 18.1, 18.3, 39.2) | **missed** | as SU3; the 4.1 rationale stops at "Scheduled PCOD and any A5 milestone relying on it are not changed by this op" (`P` L3313ff) |
| IE4 (row 4 → VOL-II 2.2 → lifecycle plan, Financial Model, AP, 42.2 reserve) | **missed** | as SU4 |
| IE5 (row 5 months → compatible with VOL-II 3.2's 7-year membrane warranty; "24 years" would bar membranes) | **missed** | VOL-II 3.2 is in no item; "24 years" is kept as a live reading (AR2) |
| IE6 (2.1 + 1.2 → 2.5M → 1.5M → Form 4-F pricing; Form 4-E) | **partial** | The chain to the ADD-02 base is there (`P` L368–372) and 2.2 ties it to Form 4-F (`P` L677). deviations-review and form-4e are blocked by VOL-V-36.2-01 (`a3c` L145, L148). No 1.5M |
| IE7 (4.4 → A3 4.2 narrows → Form 4-C decl. 5 → 4.1 still applies) | **partial** | VOL-I-4.2-01 is marked UNRESOLVED by 4.4 (`a3c` L126). No Form 4-C, no 4.1 |
| IE8 (Q17 → 10.1/Form 4-F → part of Form 4-F → DSCR → 6.2 if in Envelope A) | **hit** | every link is in one item (`P` L3975–4078), with the 6.2 consequence hedged |
| IE9 (4.3 forward count → no forward rule → 22 or 19 Nov → Q19 → plan to 19 Nov, flag) | **hit** | `pkt` L148; ESC-DATE-4.3-WITHIN (`DS` L1834–1858); `a5m` L9 plans 19 Nov with "2026-11-22 if the ADD-03 issue day is excluded"; Q19 is tied to 4.3 (`ops` L276) |

### Derived dates (7): 7 right

| Key | Expected | Result | Evidence |
|---|---|---|---|
| D0 | cut-off Thu 12 Nov (backward, stated date not counted); ADD-03 issued after it | **right** | "the clarification window closed on 2026-11-12 … ADD-03 issued 2026-11-17" (`pkt` L108). No question is offered as sendable |
| D1 | latest appointment Mon 23 Nov | **right** | "three (3) Working Days before the Proposal Due Date -> 2026-11-23" (`pkt` L147; `a5m` L10) |
| D2 | request deadline: Sun 22 Nov (not counted) or Thu 19 Nov (counted); rule not stated; plan to 19 Nov | **right** | `pkt` L148, escalated "the counting rules do not settle it"; A5 milestone at 19 Nov, with readings_differ TRUE and the 22 Nov alternative (`a5m` L9) |
| D3 | 12.5 notice: event-based, rule not stated | **right** | "not computed: no rule … for Working Days counted after a date …; its anchor 'encountering them' is an event" (`pkt` L149; `DS` L199ff `date_notes`) |
| D4 | letter No. 417/2026 of Sun 15 Nov | **right** | "التاريخ: ١٥ نوفمبر ٢٠٢٦م" (`pkt` L59; `rd` title lines); "No. 417/2026 dated 15 November 2026" (`P` L2426) |
| D5 | 7 Working Days from issue to the PDD | **right** | "Working Days left from the issue date (2026-11-17) to the PDD (2026-11-26): 7 (the issue date not counted, the PDD counted …)" (`pkt` L146). The count convention is the mirror of the key's; the number is the same |
| holidays | none assumed (an editable external assumption) | **right** | "holidays none declared" (`pkt` L146). Planning date moved to 2026-11-17 (`pkt` L786) |

### Marshalling (7): 2 hit, 4 partial, 1 missed

- **M1, core-appointment request: hit.**
  - Rows ADD-03-4.3-01/-02.
  - Milestones 19 Nov (with 22 Nov) and 23 Nov (`a5m` L9–10).
  - No activity carries them: C48 (`pkt` L525–526).
- **M2, obtain the GBR Revision C or flag it: missed.** It is never listed as not supplied (`a3c` L165–176 lists 10 documents, not this one).
- **M3, Form 4-F with the 10.6 schedule attached (+DSCR), Envelope B only: partial.**
  - It is detected through Q17.
  - The evidence item is unchanged: "Schedule of principal financing assumptions (tenor, margin, gearing)" in Envelope B, with no DSCR (`out-candidate/a5/candidate/marshalling.csv` L9).
- **M4, the Technical Proposal items (3.6 lifecycle demonstration, 4.2 ground conditions): partial.** Both rows are invalid, and technical-proposal is blocked (`a3c` L143).
- **M5, Form 4-E review (12.5, 36.2, 42.1, 42.3; unlisted means accepted): partial.**
  - REWORK deviations-review and form-4e through ADD-03-4.1-01 (`pkt` L798, L815).
  - Both are blocked by the 36.2 and 42.1 rows (`a3c` L145, L148).
  - 42.3 and the deemed acceptance are not named for ADD-03.
- **M6, Form 4-A acknowledging Addenda 1–3: hit.** Row ADD-03-cover-para3-01 (`a1` L40); REWORK form-4a and form-4a-prep: "Addenda to acknowledge: ADD-03 issued since ADD-02" (`pkt` L805, L808).
- **M7, Availability Payment on the 1.5M threshold: partial.** The 2.2 row is invalid and 1.5M is never computed.

### A3 delta (4): 2 hit, 2 partial

- **VOL-I 4.2 narrowed by 4.4: partial.**
  - Escalated, and the row is UNRESOLVED (`a3c` L126).
  - The diff says "Disqualifiers (A3) — no change" (`pkt` L780).
  - The validated A3 stays at ADD-02 because the run is PARTIAL.
- **VOL-I 6.2 now expressly applies to the 10.6 schedule: partial.** Q17 hedges whether it is "commercial information" (`P` L4077).
- **VOL-I 9.3 / Form 4-A now acknowledges ADD-03: hit** (M6).
- **No new A3 items: hit.**
  - 3.6 and 4.2 rows carry `none_stated` (`P` L1588; `P` L3503ff).
  - 4.3 is "Optional for a Bidder ('wishes to inspect')" (`P` L3630).
  - A3 gains 0 rows (`pkt` L41).

### Missing evidence (3): 1 hit, 1 partial, 1 missed

- **ME1, GBR Revision C: partial.**
  - Only "the Geotechnical Baseline Report Revision C is defined by reference only" (`DS` L249).
  - The critic: "Whether the report was supplied in the pack is not shown here and should be checked separately" (`P` L3402).
  - No issue is raised and no "referenced but not supplied" entry is made.
  - Its possible identity with ADD-01 response 4's data-room report is not raised. The existing I-OP-ADD-01/Q4 is "not reached by this addendum's changes" (`a3c` L176).
- **ME2, the five-point condition grading scale: missed.** Note 1 is described ("Authority's five-point scale, grade 1 = new", `P` L2094–2117). Nothing says that grades 2–5, which the table's maxima use, are undefined.
- **ME3, the Direct Agreement: hit.** "not yet negotiated" (`DS` L553); the pre-existing I-VOL-V-MISSING names it (`a3c` L173).

### The deliberate ambiguity and the human judgment

- **DA1: missed.** The composite asset question (mechanical 5 years against electrical/I&C 7 years) is not raised anywhere.
  - No item uses "composite", "pump", "motor", "blower" or "actuat", or compares rows 3 and 4.
  - Rows 3 and 4 exist only as separate conditional rows (`DS` L1218, L1328).
  - This was the one item with no correct answer, and it cannot be clarified.
- **HJ1: hit** (as Q18). The **precedence-wording trap is avoided**:
  - "The order of precedence at Volume I Clause 3.2 applies" is quoted and not treated as an answer;
  - recital 1.1 is read as deciding nothing ("edits no unit");
  - no winner is recorded.

### Must-not-report traps (24): 24 avoided as assertions, 4 borderline

**Avoided, with no trace:**

- **Handback survey (traps 3–4):** VOL-II is not renumbered (3.2), and the survey text is unchanged.
- **Table 42-1 values (traps 5, 7, 8):** no English value is taken as governing (the conditional rows use the Arabic). Membranes are not "prohibited". There are five classes, and "four" is reported as the cover's.
- **3.6 and 4.2 (traps 9–10):** neither is optional or pass/fail.
- **12.5 (traps 11–12):** it is not said to conflict with 3.3, and it is time and cost (not time-only, not a Relief Event).
- **The 4.2 blackout (traps 13–15):** it is not suspended generally (the scope is kept narrow); 4.1 is not disapplied; no Form 4-C reissue.
- **Answers (traps 16–18):**
  - Q15 and Q16 add nothing;
  - Q18 is not settled;
  - DA1 is not "resolved", though it is not raised at all.
- **Dates and validity (traps 19, 21, 24):** the PDD, its time and the cut-off are unchanged; the addendum is not called invalid; D2 is never given as a single date.
- **Values (traps 22–23):** no GBR or grade value is invented, and 36.1 and 36.3 are untouched.

**Borderline (none asserted; each is a display or a proposal):**

1. **Trap 1 (CiL at 4.0M or 2.5M).** The analysis lists 4,000,000 as "Reading A" (`P` L368, unpromoted). The A1 working column shows 36.2 at **SAR 2,500,000**, "ACTIVE (as amended by ADD-02/8.1)", "not changed by this run" (`a1` L456).
2. **Trap 2 (8.5 deleted).** A `set_status VOL-II:8.5 deleted` op was proposed. It is invalid and not promoted (`P` L856–881), and it was paired with the 42.3 insertion escalation.
3. **Trap 6 (VOL-II 2.2 at 25 years).** Downstream records "Note (4) increases the design life of electrical equipment in VOL-II 2.2 to 25 years" as a *fact* (`DS` L48–50). ESC-NOTE4 asks only whether "the cap survives" (`DS` L945).
4. **Trap 20 (clarifications still possible).** Two unpromoted analysis issues suggest a clarification: "consider a clarification" (`P` L4166ff), and "whether to raise a clarification question with the Authority" (`P` L3213ff). The controller's route note overrides both: "this question cannot be submitted as a clarification" (`pkt` L108, L133).

## 2. Usable updates

What was promoted into the candidate (`pkt` L528–534; `promotion.json`; `log` "promoted into the candidate: 2 op(s), 11 disposition(s), 19 unresolved, 9 new row(s), 0 reading(s), 1 issue(s), 0 activit(y/ies), 0 clarification(s), 0 relationship(s)"). Everything is PROPOSED.

- **2 ops:**
  - `ADD-03/cover/para3`: annotate, `adds_obligation`, "Bidders shall acknowledge receipt in Form 4-A";
  - `ADD-03/4.1`: `insert_unit` of 12.5 after VOL-V:12.4.
- **28 analysis dispositions in the op file:**
  - 11 `no_effect`: cover/para1–2, 1.1, 1.3, 3.2 and six Table 42-1 furniture units;
  - 17 `unresolved`: 1.2, 2.1, 3.5, AppA/para1, image r1 and r3, notes 1–3, AppB/para1–2, English rows 1 and 3, English notes (1)–(3), and Q19.
- **19 controller `unresolved` entries** for the provisions whose items failed.
- **9 new rows:**
  - ADD-03-cover-para3-01 and ADD-03-4.1-01;
  - ADD-03-T42-1-01…05, conditional on the pending reading and "not in force; not planned";
  - ADD-03-4.3-01/-02.
- **1 issue:** I-ADD-03-T42-5-UNIT.
- **The image reading ADD-03-p3-r1,** pending.
- **2 A5 candidate milestones:** 19 Nov and 23 Nov (`a5m` L9–10).
- **None of:** activities, evidence items, clarifications, relationships, or re-made readings of existing rows.

Per key item (N = 33; the 5 missed items are not counted):

| Class | Key items | Count |
|---|---|---|
| **Applied; a person could accept it as is** | 1.1, 1.3, 3.2 (`no_effect`); 4.1 (op + row; A5 REWORK); 4.3 (two rows, both dates, the escalation and the planned 19 Nov); the reading (pending its approval; two vowel marks to correct) | 6 |
| **Applied in part** | 3.4 (five conditional rows carry the Arabic values; the 42.1 text change and the table insertion are not applied); AR1 (row 4 = 7, conditional; the rule left to a person); AR2 (row 5 printed as ٢٤ شهراً, but I-ADD-03-T42-5-UNIT keeps 24 years open); E3 (inside a promoted `unresolved` disposition, not an issue); Q19 (the disposition stays `unresolved`; the planning date is in A5) | 5 |
| **Detection only** (an unpromoted or invalid item, an escalation, or a promoted `unresolved` disposition that decides nothing) | 1.2, 2.1, 2.2, 3.1, 3.3, 3.5, 3.6, 4.2, 4.4, Q15, Q16, Q17, Q18 (an escalation is the expected final form), E1, AR3, SU2, SU6 | 17 |
| **Wrong as applied** | none: no promoted item has content the key contradicts | 0 |

**Promoted items that would mislead if accepted as is:**

- **VOL-V-36.2-01.** Not touched by any promoted op, it stays at SAR 2,500,000 with the candidate status "proposed (existing row; not changed by this run; not reviewed)" (`a1` L456). Accepting the candidate as it stands keeps the ADD-02 threshold, which is a trap value.
- **The `unresolved` dispositions on 3.5, AppA/para1 and AppB/para1** (`ops` L109–126, L203–210). They record that "which rendering governs is a person's decision (Legal)", although 3.5 settles it. Accepting them leaves the governing-language rule open.
- **I-ADD-03-T42-5-UNIT** (`DS` L1558). It frames row 5 as 24 months or 24 years. The key excludes 24 years, and that reading would bar membrane processes.
- **The 3.2 `no_effect`.** It is right, but its reason says "the vacancy of 8.5 is handled by ADD-03/3.1(b)" (`ops` L100–108). That op is the invalid `set_status … deleted`, which the key rejects (trap 2).
- **Four new rows have no evidence item or activity.** check-register exits 1 on eight "deliverable" findings for the run's own rows (`pkt` L540–548), and C48 says no activity carries ADD-03-4.3-01/-02 (`pkt` L525–526).

## 3. Missed effects and why

These come from the run's own files. The class follows the policy's three-way split: a software limitation, missing evidence, or a genuine ambiguity. Where neither the tool nor the documents explain the loss, it is a **model miss**.

**Not detected (5 of N, plus the separately scored items):**

| Key item | Stage that lost it | Reason recorded in the run's files | Class |
|---|---|---|---|
| E2 (invites against shall demonstrate) | analysis + C28 | The cover was handled in analysis-001 ("Other cover content is answered by other batches", `P` L241ff). 3.6 was in analysis-002, which proposed "shall demonstrate" but did not compare the cover. C28 splits the cover at commas (even inside "SAR 4, 000, 000") and reports "not found" for whole segments, accurate and inaccurate alike (`pkt` L729–732) | software limitation (the cover check cannot compare modality; batch boundary) |
| SU1 / IE1 (ADD-01 response 4) | downstream task generation | "Earlier answers to re-read … none" (`pkt` L782–784). The re-read list is built from answers that cite a changed unit, and the new unit VOL-V:12.4+ADD-03 is cited by none. I-OP-ADD-01/Q4 is "not reached by this addendum's changes" (`a3c` L176) | software limitation |
| SU3 / IE3 (12.5 → PCOD → 18.1/18.3/39.2) | downstream | "units changed VOL-V:12.4+ADD-03; rows citing them none" (`pkt` L290). A new unit has no curated relationship, so nothing follows from it. The analysis rationale stops at "Scheduled PCOD … not changed by this op" | software limitation |
| SU4 / IE4 (row 4 against VOL-II 2.2 lifecycle) | downstream | The table values are conditional on a pending reading ("not in force; not planned", `pkt` L151). No task asks what the values imply for other rows | software limitation (by design, but nothing replaces it) |
| SU5 / IE7 (4.1 not disapplied; Form 4-C decl. 5) | analysis/downstream | The 4.4 escalation's scope is "rows VOL-I-4.2-01; activities none" (`pkt` L124). Form 4-C's reference (البند ٤-٢) sits in an approved image reading and is not a cross-reference link to VOL-I 4.2 | software limitation |
| IE5 (row 5 against VOL-II 3.2) | analysis | The unit question was left open (AR2), so its consequence was never examined | model miss (over-escalation) |
| DA1 (composite assets) | analysis | Rows 3 and 4 were compared only Arabic against English (`P` L1830–1960); no item considers an asset that falls in both classes | model miss; a genuine ambiguity not found |
| ME2 (grading scale) | analysis | Note 1 is described ("grade 1 = new", `P` L2117) without noting that grades 2 and 3, used by the table, are undefined | model miss; missing evidence not flagged |
| M2 / ME1 (GBR Rev C) | analysis/downstream | "defined by reference only" (`DS` L249); the critic's "should be checked separately" (`P` L3402) is not acted on | model miss; missing evidence not flagged |

**Detected, not applied (the reasons behind the 17 partials):**

1. **Row payload shape (software).** All five analysis `row_new` items are invalid on the Row schema, and none was repaired or re-asked ("every request was answered at the first call", `pkt` L668):
   - 2.2: a consequence string instead of an object;
   - 3.6: scope as a string, discipline missing;
   - 4.1, 4.2 and 4.3: `confidence` and `confidence_reason` missing (`pkt` L210, L278, L289, L297, L302).
   
   4.1 and 4.3 were recovered downstream (the c46 and computed-date tasks). 2.2, 3.6 and 4.2 were not.
2. **`annotate` refused on `previous_value` (software).** Q15, Q16 and Q17 fail with "previous_value: no target to compare the previous value … with" (`pkt` L319, L324, L329). All three answers were read correctly.
3. **Dependencies on non-op ids (software).** 3.3 depends on the escalation `ADD-03/3.1(a)`, 2.2 on the disposition `ADD-03/2.1/disp`, and 3.1(b) on `3.1(a)`. All fail with "unknown ids" (`P` L677ff, L856ff, L1004ff).
4. **A same-unit consistency flag on disjoint spans (software).** "VOL-V:42.1: ADD-03/3.3, ADD-03/3.4 change the same unit in different ways across the set". The two spans do not overlap (critic, `pkt` L236).
5. **One unsupported fact sinks every item that cites it (software, triggered by the model).**
   - analysis-003/S2 is a summary "fact" with `evidence: []` that paraphrases row 2 as "treated water transmission line" (`P` L88–93). It fails "not supported verbatim" and takes nine items with it: image r2, r4, r5; English rows 2, 4, 5; note (4); and the Table issue (`pkt` L357, L368, L370, L383, L439, L450, L463, L489).
   - analysis-002/S1 likewise sinks 3.4, 3.5-issue and 3.6 (`pkt` L244, L264, L278).
6. **No op type (software, declared as such).** 3.1(a) relocation and insertion of an uncited clause, 3.4 table insertion, 4.4 scoped disapplication (`pkt` L110–124).
7. **Over-escalation of settled matters (model; misclassified as "ambiguous").** 1.2, 2.1/E1 ("which governs is a person's decision"), 3.5 and AR1–AR3 ("which rendering governs"), Q17(c) ("whether it is 'commercial information' is for a person").
8. **Analysis issues are never promoted and seed no downstream task (software).** The cover-against-2.1 issue (E1) and the Q18 issue were "dropped: an analysis issue is not promoted" (`pkt` L133, L536). The downstream phase had 17 tasks and none of them concerned 2.1 (`ckpt` `downstream.tasks`).

**How the run classified its own losses:**

- **Software limitations are labelled correctly** where the run declared them (3.1(a), 3.4-issue, 4.4/esc, ESC-DATE-4.3-WITHIN).
- **"Missing evidence" is never used,** although two items in the key are exactly that (ME1, ME2).
- **"Ambiguous" is used for matters the documents settle,** and the one genuine ambiguity was not found:
  - the 3.5 rule in ten analysis items and six downstream items;
  - the cover against the operative text;
  - 1.2;
  - row 2's class.
- **Mislabelled escalations:**
  - DS-004 calls a tool defect "insufficient evidence" (`DS` L353ff);
  - the critic calls DS-009/DS-012 "mislabelled" because they file a human decision under "software limitation" (`pkt` L376, L456).

## 4. False positives and false signals

**False positives (effects the key does not support): five, none promoted into an op or a row in force.**

| # | What is stated | Where | Why it is wrong |
|---|---|---|---|
| 1 | Table 42-1 row 2's class "may differ in scope": Arabic خط نقل المياه المعالجة, "treated water transmission line", against English "Treated effluent transmission main" | `P` L88–93 (S2), L1752, L2613; DS-008, DS-011 (`DS` L588, L747); the Table issue (`P` L3213); a HUMAN DECISION PENDING item (`pkt` L370) | The letter's own subject is a sewage treatment plant (محطة معالجة مياه الصرف الصحي, `pkt` L59). Its "treated water" is the treated effluent, and the key records no row-2 discrepancy (AR1–AR3 only). The paraphrase is also what failed the verbatim check and sank nine items |
| 2 | `set_status VOL-II:8.5 deleted` for a relocation | `P` L856–881 (invalid) | The key: relocation is not deletion; the A1 row must be traced to 42.3 with its history kept (trap 2) |
| 3 | C28: "not found: … no provision of ADD-03 does this" for three cover segments | `a2cov` (ADD-03 "not found" 1, 2, 4); `pkt` L729–732 | Each segment holds accurate claims that the key lists under `accurate_parts`: the relocation, the foundations statement, and core inspection with a 4.2 exception. The cover was split at the commas inside "SAR 4, 000, 000". No planted error is named by C28 |
| 4 | "Note (4) increases the design life of electrical equipment in VOL-II 2.2 to 25 years" recorded as a **fact**; ESC-NOTE4 asks whether "the cap survives" | `DS` L48–50, L923–945 | The note is English-only and has no force (AR3, CT6); VOL-II 2.2 is unchanged. Borderline trap 6 |
| 5 | Row 5: "24 years and 24 months are both supported by the words"; the promoted issue keeps both | `DS` L859–882; I-ADD-03-T42-5-UNIT (`DS` L1558) | The governing Arabic cell states its own unit, ٢٤ شهراً. "24 years" exists only in the convenience translation, and it would make membrane processes impossible (IE5) |

**False signals** (not claims about the tender, but each costs a reviewer time or misleads):

| # | Signal | Evidence |
|---|---|---|
| 1 | VOL-V 36.2 shown unchanged at ADD-03. Status "ACTIVE (as amended by ADD-02/8.1)", SAR 2,500,000, "not changed by this run", while the candidate A3 lists it as not settled by 2.1. Borderline trap 1 | `a1` L456 against `a3c` L136 |
| 2 | Provisions labelled "answered" when their only promoted item is an `unresolved` disposition (2.1, 1.2, 3.5, Q19, AppA/AppB, image r1/r3, notes). There are three different unresolved counts in one packet: "19 of 49" (`pkt` L7, L106), "36 of 49" (`pkt` L50, L691; `a3c` L70), and "resolved 11, pending 30, invalid 4, unaccounted 4" (`pkt` L558) | `pkt` L200 "ADD-03:2.1 … — answered" |
| 3 | Rows the key leaves unchanged shown UNRESOLVED: VOL-II-9.3-01 by a confirming answer (Q16), VOL-II-2.2-01/02 by a no-force note | `a1` L264, L179–180 |
| 4 | The governing-language rule (3.5) handed to a person by ten analysis items and six downstream items (section 5). The controller itself flags two of them as reversals | `pkt` L371, L451, L509, L512 |
| 5 | The closed-window note "this question cannot be submitted as a clarification; it is a bid-decision for a person" attached to schema errors and tool limitations, which are not bid decisions | `pkt` L125–140, L503–514 |
| 6 | The 3.2 semantic flag "no_effect on amendment language … (its words carry 'renumbered')" on a provision that says nothing is renumbered | `pkt` L227 |
| 7 | ADD-03-T42-1-05 is marked HUMAN DECISION PENDING because its note contains "resolved" (in "unit not resolved") | `pkt` L519; critic `pkt` L662 |
| 8 | Two analysis issues suggest a clarification after the cut-off (borderline trap 20); the controller overrides them | `P` L3213ff, L4166ff; `pkt` L108 |
| 9 | check-register exit 1 on the run's own new rows (8 "deliverable" findings) | `pkt` L540–548 |
| 10 | Interruption records that misstate what happened (detailed in section 6): "(made before the interruption)" for submissions made after the resume; a closing `prefetch_not_taken` for batches that were taken | `log` L26, L29; `ckpt` L4813 |

**Asserted as settled although the key reserves it for a person: none.**

- **The precedence-wording trap (HJ1) is avoided.** Q18's "The order of precedence at Volume I Clause 3.2 applies", recital 1.1 and the standard paragraph are not used to pick a winner. Both readings are listed and Legal decides (`P` L4081–4190; `DS` L528–553).
- **The D2 counting rule** is left to a person, with both dates shown.
- **The 4.4 scope** is left to a person.

## 5. Pending decisions

What the packet lists for a person:

- **9 items marked HUMAN DECISION PENDING** (`pkt` L264, L313, L336, L347, L370, L424, L429, L519, L520).
- **19 provisions listed first** (`pkt` L104–140): 3 ESCALATED and 16 UNRESOLVED.
- **13 downstream escalation items for 12 tasks plus one date escalation** (`pkt` L503–523).
- **The pending image reading.**

| HUMAN DECISION PENDING item | What it asks | Key | Verdict |
|---|---|---|---|
| ADD-03/Q18-issue (`pkt` L336) | Direct Agreement against VOL-V 40.2 | HJ1: a person | **right** |
| ADD-03/4.4/issue (`pkt` L313) | scope of the 4.2 exception during appointments | acceptable if raised | **right** (a fair question for Legal) |
| ADD-03/3.5-issue (`pkt` L264) | which rendering of rows 4 and 5 prevails | 3.5 settles it: the Arabic | **over-escalated** |
| ADD-03/AppA/para1 (`pkt` L347) | "which text prevails is a person's decision" | settled by 3.5 | **over-escalated** |
| ADD-03/AppB/para1 (`pkt` L424) | the same, from the English side | settled by 3.5 | **over-escalated** |
| ADD-03/AppB/para2 (`pkt` L429) | the English qualifier; four against five classes | the Arabic governs; "four" is the cover's error (E3) | **over-escalated** (the E3 note is right) |
| ADD-03/ISSUE/T42-1-arabic-english (`pkt` L370) | rows 2, 4, 5, note (4), four/five | AR1–AR3 and E3 are settled by 3.5; row 2 is no discrepancy | **over-escalated**; it also carries false positive 1 |
| ADD-03-T42-1-05 (`pkt` L519) | the row 5 conditional row | 24 months | **over-escalated** (keyword trigger) |
| I-ADD-03-T42-5-UNIT (`pkt` L520) | months or years for row 5 | 24 months | **over-escalated** (false positive 5) |

**Judgments the key reserves for a person:**

- **HJ1:** left to a person. Right.
- **DA1:** **not raised.** The one point with no correct answer, which cannot be clarified after the cut-off, never reaches the person who must decide it.
- **D2:** both readings, the rule flagged as unstated, and the earlier date planned. Right.
- **The reading's approval:** pending. Right.
- **The closed clarification route** (ADD-03 issued after 12 Nov) is stated on every item. Right in substance, though over-applied (false signal 5).

**Over-escalated: points the documents settle.**

- **The 3.5 rule:** ten analysis items (the dispositions on 3.5, AppA/para1, AppB/para1, image r4 and r5, English rows 4 and 5 and note (4), plus the 3.5-issue and the Table issue) and six downstream items (DS-009, DS-010, DS-012, ESC-T42-5, ESC-NOTE4 and I-ADD-03-T42-5-UNIT). The critic notes twice that "The item ignores ADD-03 3.5, 'The Arabic text governs.'" (`pkt` L374, L454).
- **The cover against the operative 2.1, and the base set by 1.2:** "which governs is a person's decision" (`P` L368–372; `ops` L71–80).
- **Q17's Envelope A consequence** (`P` L4077).
- **Row 2's class** (false positive 1).

**The packet is not short.**

- **A person must read** 19 provisions, 13 downstream escalations and 9 HUMAN DECISION PENDING items, plus the critic's 14 reviews (7 disagreements).
- **Only about five decisions are real:**
  1. approve the reading (two vowel marks);
  2. apply 3.5, so that rows 4 and 5 and note (4) follow and the row-2 point drops;
  3. adopt SAR 1,500,000 under 1.2 and reject the cover's 4.0M;
  4. HJ1;
  5. DA1, which the packet does not contain.

## 6. Interventions

### Interventions of the session (the three earlier attempts; not the run's misses)

| Attempt | Run | What stopped it | Fix before the next attempt |
|---|---|---|---|
| 1 | `…183015Z-9ae8` (`run.id.attempt1`), upload 18:30:14 | readings: "the proposed reading is invalid: RD1: … reading says ADD-03 p3 []; RD2: …; RD9: graphic reading: description MISSING" (`run.log` L4–5); exit 6 after 31.5 s of steps. See the note below | **E159**: the host CLI started the MCP server where the package was not importable. Fixed with failing tests first; the folder was rebuilt from the fixed tree |
| 2 | `…194853Z-633b`, upload 19:48:52 | readings: "insufficient_evidence: RD3: grid from pixels: 8 horizontal x 5 vertical rules = 7 rows x 4 cols …; reading: header + 5 rows x 4 columns" (`run.log` L179); the job ended 19:51:38 | **E160**: the grid detector counted the letterhead's rule as a table rule. Fixed; folder rebuilt |
| 3 | `…195810Z-0b6a`, upload 19:58:09 | reached analysis. SIGTERM at 20:06:19; Resume at 20:06:28. "two host sessions started 3 s after the SIGTERM; the run process stays alive". The coordinator **killed the two claude children by hand** at 20:08:19, and the resume job exited 1 at 20:08:22 (`clock.txt`; `run.log` L262–400) | **E161**: interrupted workers retried and kept the process alive. Fixed; folder rebuilt |

**Note on attempt 1's clock lines.** `clock.txt` records "SIGTERM after analysis-002 (planned interruption) to pid 7921 2026-10-06 19:30:38 UTC". No analysis ran in that attempt: the job had stopped at the readings step about an hour earlier.

The Resume at 19:30:47 stopped the same way (`run.log` L88–173, exit 6 at 19:31:05). So the clock line is misleading. Attempt 1 occupied 18:30–19:31 on the clock but did about 46 s of work.

The brief says "the clock lines before 'attempt 3 start'". `FROZEN.md` says "before 'attempt 4 start'". The second is the right boundary for the frozen run.

### Interventions in the scored run (attempt 4)

Manual steps: exactly the three that were planned.

1. **Upload** through the panel's *New addendum* form, route host, at 20:13:57.
2. **The planned SIGTERM** to pid 16620 at 20:20:31. It came after analysis-002 had been taken at 20:20:30 (`log` L17–18).
   - The job stopped two host sessions: `interrupted` … `"host_sessions_stopped": 2` (`ckpt` L4767ff).
   - The job ended at 20:20:40, 9 s later. **The E161 fix held.**
3. **Resume** from the panel at 20:20:40: `resumed` by pid 18147 at 20:20:41.

Nothing else: no curation, no file edit, no second resume, no kill. `rate_gate`: no pauses or waits.

**The checkpoint's own record.**
- `interventions` has 5 entries, each a "host session (automatic) … not a person": the reading, analysis-001, analysis-003 and downstream-001/-002 (`pkt` L677–683).
- The person's SIGTERM and Resume are recorded only as `events`. The packet's "Manual interventions" section therefore lists none.
- The two killed sessions and the three sessions whose answers were reused are missing from it. `bench` counts **10 host sessions started**.

**Was any batch asked twice? Yes, two analysis batches and one critic request, and none of them had answered:**

- **analysis-003** was dispatched at 20:19:53 (`log` L12; session `…201953Z-ad30`). It was stopped by the SIGTERM after 38.7 s without submitting, and asked again at 20:21:04 (`…202104Z-b683`, 409.5 s).
- **analysis-004** was dispatched at 20:20:03 (`…202003Z-d433`). It was stopped after 29.3 s without submitting, and asked again at 20:21:05 (`…202105Z-3d41`, 195.8 s, submitted 20:24:15) (`bench`).
- **The analysis-002 critic request** was cut by the SIGTERM. The traceback runs through `_critic_analysis` → `review_batch` → `ask_host` → `Terminated` (`run.log` L413–470). It was asked again after the resume ("analysis-002 critic: done (5 reviewed, 3 disagree)", 20:21:03).

**Were the submitted answers of killed sessions kept and revalidated? Not exercised.** Neither killed session had submitted. The reuse path ran three times, each for a session that had finished normally. All three have equal `statuses_at_submission` and `statuses` after revalidation (`ckpt` `batches.*.submission`).

| Batch | Submitted | Taken (revalidated) | Segment |
|---|---|---|---|
| analysis-002 | 20:19:48 | 20:20:30 | 1, **before** the SIGTERM; not re-asked after the resume |
| analysis-004 | 20:24:15 | 20:28:04 | 2, after the resume, taken in order after analysis-003 |
| analysis-005 | 20:26:17 | 20:28:29 | 2, the same |

**Wrong records of the interruption** (false signal 10):

- The log calls all three reused submissions "(made before the interruption)" (`log` L17, L26, L29). For analysis-004 and -005 that is false: they were made after the resume.
- The `interrupted` event's `prefetch_not_taken` names analysis-002, which had been taken; only its critic was pending.
- A closing `prefetch_not_taken` at 20:33:46 names analysis-004 and -005 as "the run stopped before their answers were taken". Both were taken at 20:28 (`ckpt` L4813).

**`concurrency`** (`ckpt`, the last drive only, so segment 1's four dispatches are not in it):

| Phase | Dispatched | Taken | Busy | Window | Idle slots |
|---|---|---|---|---|---|
| Analysis | 3 | 1 (the other two by reuse) | 725.2 s | 409.8 s | 94.4 s |
| Downstream | 2 | 2 | 335.3 s | 178.9 s | 22.5 s |

Both phases ran with max_parallel 2, lookahead 4, at most 2 running and 0 discarded.

**Code identity: both segments ran the same code.**
- Segment 1 ("run started", 20:13:59) and segment 2 ("resumed on the same code", 20:20:41) both have content `f5e50e87…` over 98 files and policy `1bf971b4…`; `"differ": false` (`ckpt` L4903–4906).
- Attempt 1 had run `55b7cf33…` (`run.log` L60), the code before the fixes.

## 7. Time

| Step (`bench`; `ckpt` `steps`) | Seconds | Note |
|---|---|---|
| ingest | 16.4 | refused once for the unread image region, as designed |
| readings | 124.6 | one host session read page 3 (109.7 s) |
| analysis | 719.5 | 2 attempts (the interruption). 7 host sessions, 1,224 s of session time, 68 s of it in the two killed sessions; at most 2 in flight. Critics for 001, 002 and 004 run inside the loop |
| validation | 13.6 | |
| downstream | 190.6 | 2 host sessions in parallel (156.4 s, 178.8 s) |
| downstream_validation | 0.6 | |
| critic (downstream) | 38.6 | 2 requests |
| promotion, pin, check_register | 26.7 | check-register exit 1 (8 findings on the run's own rows) |
| outputs | 35.4 | exit 0; 105 files carry the banner |
| diff, review | 11.9 | |
| **Steps' sum** | **1,177.9 s (19.6 min)** | the packet's own table says 1,176.7 with "review 0.0 running" (`pkt` L90–91), because it was written before its own step finished |

**Wall clock.**

| Measure | Value |
|---|---|
| PDF upload → end (`clock.txt`) | 20:13:57 → 20:33:48 = **19 min 51 s** (1,191 s) |
| `ckpt` created → updated | 1,188.0 s |
| Segment 1 | 393.0 s |
| Segment 2 | 786.0 s |
| **Without the 9 s interruption gap** (20:20:32 → 20:20:41) | **1,179.0 s = 19 min 39 s** |
| Against the brief's 30 minutes | met by about 10 min 9 s on the wall clock |

**Sessions started: 10 host sessions** (`bench`):
- 1 reading;
- 7 analysis, of which 2 were killed and re-asked;
- 2 downstream.

There were also 6 critic requests: analysis-001, analysis-002 twice (one killed), analysis-004, and downstream-001 and -002.

- **Fixed overhead per analysis session:** 7–13 s (process start → MCP server → first tool call, and submission → end). That is 71 s in all, 5.8 % of session time.
- **The deterministic steps** together took about 120 s.

**Time of the first useful output:**

| Output | At | After the upload |
|---|---|---|
| The image reading | 20:16:05 | 2 min 08 s |
| The first analysis set (analysis-001) | 20:20:03 | 6 min 06 s |
| The candidate outputs | about 20:33:34 | about 19 min 37 s |
| **The review packet** | 20:33:46 | **19 min 49 s** |

Nothing a person can review as a whole appears before the packet.

**What set the critical path:**
- **The reading.** 109.7 s alone, before any analysis.
- **analysis-003.** 26 provisions ("one structure kept whole … (26)", `ckpt` `steps.analysis.plan_notes`), a 409.5 s session. analysis-004 and -005 had finished at 20:24:15 and 20:26:17 and waited for it, because results are collected in order (94.4 s of idle slots).
- **The interruption.** It cost, by my estimate, about 80 s of wall clock:
  - the 9 s gap;
  - analysis-003 restarting 71 s after its first dispatch;
  - the repeated critic request.

**Against blind-06's 55 min 49 s:** 36 min less (−64 %). The comparison holds only with these caveats:

1. **A different host model.** blind-06's sessions ran the alias opus (`../blind-06/COMPARISON.md` L49). These ran the CLI's default model, which reported claude-sonnet-5-5 (`pkt` L6; `ckpt` `model_reported`).
2. **A smaller addendum.** 49 provisions against 70, and 4 pages against 5. 5 analysis batches (one of 26 provisions) against 10. 17 downstream tasks in 2 batches against 48 in 4.
3. **The failures bought part of the speed.** With 2 valid ops, downstream had almost no rows to re-read: 12 of its 17 tasks were escalations. A run that had applied 2.1, 3.1–3.4 and the answers would have had re-read, relationship and programme tasks that this run never asked.
4. **Different code and conditions.** blind-07 includes an interruption and a resume, which blind-06 did not have. The code is session 13's, with lookahead, reused submissions and the before-outputs built in the background.
5. **The session as a whole.** The four attempts took the session from 18:30:13 to 20:33:48 (4 h 3 min) of clock time. That is the cost of the three tool defects, not of the run.

## 8. General workflow defects seen in this run

1. **Row payloads are not checked against the Row schema at submission, and a schema failure is neither repaired nor re-asked.** All five analysis `row_new` items failed on shape: a consequence as a string, scope as a string, and missing discipline, confidence and confidence_reason. Three provisions lost their only row.
2. **`annotate` ops on answers are refused by the previous_value check** ("no target to compare the previous value … with"). Correctly read decoy, confirming and changing answers all end UNRESOLVED, and so do the rows they name.
3. **Item dependencies may name only op ids.** A dependency on an escalation or a disposition in the same set fails as "unknown ids" and holds a correct op as conflicting.
4. **The same-unit consistency check flags two `replace_text` ops on one unit even when their spans are disjoint.**
5. **One statement that fails its evidence check invalidates every item that cites it.** A "fact" with `evidence: []`, partly a paraphrase of a translation, is accepted as a shared basis. Its blast radius (12 items here) is not reported as such.
6. **No op types** for:
   - the relocation of a clause between volumes, with history;
   - the insertion of a clause the provision does not cite as a target;
   - the insertion of a table into a volume;
   - a scoped disapplication of a clause;
   - a relative change of an amount ("reduced by").
   
   Each becomes an escalation. For the relative change, not even a computed value is offered to the person.
7. **A promoted `unresolved` disposition counts as an answer.** The packet marks the provision "answered", and A1's candidate status does not flag the rows it names: a superseded value shows as "not changed by this run". The diff and the candidate A3 count it unresolved. Three inconsistent unresolved counts appear in one packet.
8. **Analysis issues are never promoted, and no downstream task is made for them.** An issue that is the only record of a planted cover error, or of a judgment item, does not reach the candidate's register.
9. **Downstream tasks come only from valid ops, escalations and readings.** When ops fail, the indirect analysis disappears without a warning: re-reads of earlier answers, rows reached through relationships, and programme and pricing effects. A newly inserted unit has no curated relationships, so nothing follows from it.
10. **Values from a pending image reading produce conditional rows but no impact analysis** against the rows they bear on (design life, warranties, reserves). Their consequences are examined only after a person approves the reading.
11. **Stated precedence rules are still handed to a person by analysis and downstream items:**
    - an addendum's own "the Arabic text governs";
    - the operative text over the cover summary;
    - an "as amended by" recital.
    
    The controller's rule application flags only downstream reversals of an analysis item, not analysis items that decline the rule. This is blind-06 defect 12, persisting.
12. **The cover check splits the summary at commas, including those inside numbers.** It reports "not found" for mixed segments and compares no figure, count or modality against the operative provisions, so none of the three planted cover errors is named by it.
13. **The closed-clarification-window note is attached to every unresolved item regardless of its class,** schema errors and tool limitations included. Analysis issues may still suggest a clarification after the cut-off.
14. **Keyword triggers fire on negated words.** HUMAN DECISION PENDING fires on "unit not resolved"; the `no_effect on amendment language` check fires on "not renumbered".
15. **The interruption bookkeeping is unreliable:**
    - the reuse message always says "made before the interruption";
    - the `interrupted` event lists a batch already taken as "not taken";
    - a closing `prefetch_not_taken` names batches that were taken;
    - the `concurrency` record covers only the last drive;
    - `interventions` omits killed sessions, sessions whose answers were reused, and the person's stop and resume.
16. **The run's own new rows fail check-register** (no evidence item, blank evidence-needed, no activity). The downstream phase does not propose the evidence items and activities its rows need.
17. **In-order collection lets one oversized batch hold finished answers** (94 s here). The planner keeps a 26-unit image table and its translation whole in one batch.
18. **The packet's usage line reports "0 call(s), 0 input / 0 output tokens"** although 10 host sessions and 6 critic requests ran. The host's own usage per session, which `bench` reads, is not carried into the run record.
19. **"Documents referenced but not supplied" comes only from curated entries.** A document that a new clause defines ("Revision C of the report of that name issued by the Authority") is not checked against the pack and is never flagged.

## 9. Where the key and the run disagree

**I found no item where I think the key is wrong.** Where the run's reading differs, the pack's own words support the key:

- **Row 2's class** (false positive 1). The run reads خط نقل المياه المعالجة as "treated water", different in scope from "treated effluent". The letter's subject is "محطة معالجة مياه الصرف الصحي" (a sewage treatment plant, `pkt` L59). In that context the treated water *is* the treated effluent. This is a translation choice, not a discrepancy, and the key lists none.
- **Row 5's unit.** The run sees an inconsistency inside the Arabic: ٢٤ شهراً under a column headed "(سنة)". The key's CT3 records the same mismatch and answers it.
  - The cell states its own unit. The only "24 years" is in the translation, which 3.5 makes "for convenience only".
  - 24 years of residual membrane life could not be met against VOL-II 3.2's seven-year warranty.
  - I agree with the key. The heading mismatch deserves a note, not an open reading.
- **Note (4).** The run keeps "a binding amendment of VOL-II 2.2" as reading (a). 3.5 says "The English translation at Appendix B is provided for convenience only", and note (4) has no Arabic counterpart (`P` L3100). I agree with the key: it has no force.
- **1.2 and 2.1.** The run keeps the cover's 4,000,000 as a reading because the cover "says" it. 1.2 refers every reference to the clause "as amended by Addenda Nos. 1 and 2, unless otherwise stated". A summary on the cover is not a statement otherwise. I agree with the key: SAR 1,500,000.
- **Q17(c).** The run doubts that a financing-assumptions schedule is "commercial information". The response says "A schedule placed in Envelope A will be treated in accordance with Volume I Clause 6.2". 6.2 covers "any price, rate, or other commercial information", and a debt margin and a DSCR are commercial. I agree with the key.

**Points where only the method differs:**

- **D5.** The run counts the issue date excluded and the PDD included; the key counts the reverse. Both give 7.
- **Q19.** The key calls it confirming. The run keeps it `unresolved` "because the words oblige" and plans the earlier date in A5. The outcome is the same.
- **The 4.4 scope question.** The run raises whether other topics during an appointment stay barred, which the key accepts if raised.

**One record point for the rehearsal, not the key:** the corrections to `FROZEN.md` and `clock.txt` noted in "Timeline and checks" and section 6 (the hash-check directory, attempt 1's SIGTERM line, the attempt boundary).
