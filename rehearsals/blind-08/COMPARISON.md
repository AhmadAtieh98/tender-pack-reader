# Blind rehearsal 08: the frozen run against the sealed key (ADD-03)

**Synthetic, not tender content.** This is a **sealed rehearsal scored after the freeze**. The run's outputs were frozen by hash at 06:23:01 UTC on 8 October 2026 (`FROZEN.md`); the key under `SEALED/` was committed unread before the run, and I opened it only after verifying both hash lists (below). Nobody involved in building the tool or running the rehearsal had read the key.

- **Scorer:** S8, a separate agent that neither wrote the addendum nor built the tool. Model **Opus 5.5 (`claude-opus-5-5`)**; the runtime shows a reasoning-effort setting of **15**.
- **Elapsed:** scoring started 06:23:47 UTC and this file was finished at 06:34:25 UTC (**10 min 38 s**).
- **What I ran:** `sha256sum -c` on both hash lists; `.venv/bin/python scripts/bench_workflow.py --from-run <live run folder>` (06:27:02 UTC) and the same command on `rehearsals/blind-08` (identical output apart from the folder line); `cmp` of the live and frozen `checkpoint.json` and `log.jsonl` (byte-identical); PyMuPDF text extraction of `input/ADD-03_Addendum_No_3.pdf`; read-only scripts. I ran no `tenderpack ai` command and no git write command, approved nothing, and wrote only this file and scratch notes under `…/scratchpad/s14/s8/`.
- **Run:** `ADD-03-run-host-20261008T053735Z-77b2` (`run.id`), host route, two sessions in flight, host and critic pinned to `claude-opus-5-5` (every host session reported `claude-opus-5-5`: `review/index.md` L6). Status **partial**.

## Verification before scoring

| Check | Result |
|---|---|
| `FROZEN-OUTPUTS.sha256` own hash | `ef5acade01ebe9a3d8da7157348031c6ac946f15d76818faca46dead105e6610`, as `FROZEN.md` states |
| `sha256sum -c FROZEN-OUTPUTS.sha256` | **337 of 337 OK** |
| `SEALED/SHA256SUMS` | **4 of 4 OK** (PDF `6a7adf78…`, `build_addendum.py`, `expected_findings.yaml`, `author_notes.md`) |
| `input/ADD-03_Addendum_No_3.pdf` against the sealed PDF | same sha256 (`6a7adf78…4b74164`) |
| Live `checkpoint.json`, `log.jsonl` against the frozen copies | byte-identical (`cmp`) |
| Approval state | none: "nothing approved, accepted, rejected or sent" (`checkpoint.json` `approval`; `review/index.md` L17) |

## Short names and method

Paths are relative to `rehearsals/blind-08/`. L means line.

| Short name | File |
|---|---|
| `pkt` | `review/index.md` (the review packet, 1,428 lines) |
| `P` | `proposals/ADD-03-run-host-20261008T053735Z-77b2-combined/proposals.yaml` (the combined analysis set, 48 items) |
| `DS` | `downstream/proposals.yaml` (55 downstream items) |
| `iss` | `candidate-curation/register/issues/ADD-03-ai.yaml` (the 17 promoted ADD-03 issues) |
| `rows` | `candidate-curation/register/rows/ADD-03-ai.yaml` |
| `a1` | `out-candidate/a1/a1.csv` (physical lines) |
| `a3c` | `out-candidate/a3/a3_candidate.md` |
| `a5p`, `a5mar` | `out-candidate/a5/candidate/programme.csv`, `marshalling.csv` |
| `ckpt`, `log` | `checkpoint.json`, `log.jsonl` |
| `bench` | the bench output above (kept at `…/scratchpad/s14/s8/bench.txt`) |

The rules are those of `../blind-07/COMPARISON.md` and `../blind-07/regression-s14/COMPARISON-S14.md`:

- **Hit:** the outputs state the effect correctly. For a provision or an answer, the effect must be in a **promoted** item, or escalated where the key expects an escalation.
- **Partial:** detected but incomplete, wrongly targeted, or left unresolved or escalated where the key expects a definite change. A cover error, image item, settled point or indirect effect is also partial when the run keeps open a reading the key rules out.
- **Missed:** absent, or present only in a form the key contradicts.
- **Computed values:** hit = the value is produced with its derivation; partial = the inputs are laid out but no value is produced; missed = not addressed.
- **Decoys, must-not-report items and acceptable-if-raised points** are scored on their own and are not added to the detection count.

## 1. Detection

### Summary by class

| Class (key) | n | Hit | Partial | Missed |
|---|---|---|---|---|
| Provisions (P-COVER … P4.2) | 17 | 11 | 6 | 0 |
| Clarification responses (Q15–Q19) | 5 | 3 | 2 | 0 |
| Image item (IMG1) | 1 | 1 | 0 | 0 |
| Computed values (C1–C4) | 4 | 1 | 3 | 0 |
| Derived dates (D0–D8) | 9 | 5 | 0 | 4 |
| New obligations (N1–N6) | 6 | 1 | 5 | 0 |
| Indirect effects (IE1–IE8) | 8 | 1 | 5 | 2 |
| Genuine ambiguity (GA1) | 1 | 1 | 0 | 0 |
| Settled points (S1–S5) | 5 | 4 | 1 | 0 |
| Structural changes (ST1–ST4) | 4 | 1 | 3 | 0 |
| Cover errors (E1–E3) | 3 | 0 | 3 | 0 |
| **Total** | **63** | **29** | **28** | **6** |

Scored separately:

| Class | Result |
|---|---|
| Decoys (DC1–DC9) | 8 not reported as a change; DC8 (the test label) is carried as an "unresolved provision" |
| Must-not-report (MNR01–MNR22) | 22 of 22 avoided as assertions; 5 borderline, held open as readings |
| Acceptable if raised (AIR1–AIR9) | 3 raised (AIR1 in part, AIR4, AIR5) |

The pattern in one line: **nearly everything was seen and correctly quoted.** The losses are in what reached the candidate: one controller rule (§3, R1) holds back the whole Section 2 cluster, and the arithmetic and dates the key weighs most were not produced.

### Provisions (17): 11 / 6 / 0

| Key | Evidence (file L: quoted words) | Verdict |
|---|---|---|
| P-COVER | `pkt` L1232–1234, the C28 cover check: "figure differs: … SAR 8,000,000", "contradicted: 'responds to clarification requests 15 to 20' … the addendum answers 15, 16, 17, 18, 19", "omitted: ADD-03/2.6". Every issue carries "the cover summarises and does not amend" (`iss` L3, L82). | **Hit.** No value is sourced from the cover's errors. However, segmentation merged the label, the summary and the precedence paragraph into one unit, `ADD-03:cover/para3` (`pkt` L214). See defect 8. |
| P-PREC | `a1` L40, `ADD-03-cover-01`: "Bidders shall acknowledge receipt of Addendum No. 3 in Form 4-A." `pkt` L1335: "REWORK form-4a: … ADD-01-AppA-01 (Addenda to acknowledge: ADD-03 issued since ADD-02: 'Bidders shall acknowledge receipt in Form 4-A.')" | **Hit.** The critic rightly notes that the row text is not verbatim (`pkt` L225). |
| P1.1 (DC9) | `pkt` L238–241: "disposition no_effect: Recital … (applied, not decided)" | **Hit** |
| P1.2 | `pkt` L243–246: "disposition no_effect: Interpretation rule …" | **Hit.** The critic notes that S2 depends on it (`pkt` L248–249). |
| P1.3 (DC1) | `pkt` L262: "disposition no_effect: Recital of fact: 'Clarification requests 15 to 19 …'" | **Hit** |
| P2.1 | `pkt` L268–269: "`ADD-03/2.1` amendment_op replace_text VOL-I:8.9 'The Bidder shall submit either evidence…' → 'Each member of the Bidder that is incorporated outside the Kingdom shall submit…'", then "validation: **conflicting** — consistency: VOL-I:8.9: ADD-03/2.1, ADD-03/2.4 change the same unit in different ways" | **Partial.** The op is right (the critic checked old and new: `pkt` L274) but was **not promoted**. The candidate VOL-I 8.9 keeps its ADD-02 text (`a1` L109). |
| P2.2 | `pkt` L298–299: "`ADD-03/2.2` amendment_op insert_table ADD-03:p3-image — **insufficient_evidence** … dependencies: unknown ids ['S-F3']" | **Partial.** The op is right but was lost to the combine defect (§3, R2). Table 8-1 is not part of Volume I in the candidate (`DS` L2270, D-01). |
| P2.3 | `a1` L42, `ADD-03-2.3-01`: "Applications for a Certificate of Investment Registration shall be made by the member to the Office." | **Partial.** The A1 row is promoted. The A5 lead times (3 / 5 or 3 / 8 WD from the Working Day after receipt) are absent; see IE3. |
| P2.4 | `a1` L43, `ADD-03-2.4-01`: "Such a member shall submit with Envelope A the signed undertaking described in Volume I Clause 8.9 as issued."; `pkt` L362–363: "annotate VOL-I:8.9 effect disapplies … not ready … depends on ADD-03/2.1 (conflicting)" | **Partial.** The row is in A1 but UNRESOLVED; the exception op is held. |
| P2.5 | `a1` L44, `ADD-03-2.5-01` (consequence "none stated in the documents"); `pkt` L159: "'three (3) Working Days before the Proposal Due Date' -> **2026-11-23**"; `a5p` L47: "cir-portal-notification … BLOCKED … NO DEADLINE REACHED" | **Partial.** The row is right and the date is right, but the A5 milestone carries no date. |
| P2.6 (DC2) | `pkt` L411, L419: "annotate VOL-I:12.2 effect confirms … CONFIRMED (unchanged) VOL-I-12.2-01" | **Hit** |
| P3.1 | `pkt` L423–424: "insert_unit VOL-II:4.5 'The treated effluent storage reservoir … not less than six (6…' — **evidence_verified**"; `a1` L41, `ADD-03-3.1-01` | **Hit.** Both limbs (volume, and two isolatable compartments) are in the row; GA1 is raised. |
| P3.2 (DC3) | `pkt` L440: "disposition no_effect … 'does not renumber any other Clause'" | **Hit** |
| P3.3 | `pkt` L445–446: "escalation why: software limitation … 'the period of thirty-six (36) months is increased by six (6) months' … **escalated**"; `a1` L426 VOL-V-12.1-01 "UNRESOLVED (value in question)" | **Partial.** The key expects a definite change (42 months). The run declined to compute it ("The resulting period is not typed here": `P` L4826–4834). |
| P3.4 | `a1` L45, `ADD-03-3.4-01`: "Bidders shall reflect ADD-03 Sections 3.1 … and 3.3 … in the Financial Model."; `pkt` L469: "A5 REWORK fin-model-build; A5 REWORK fin-model-freeze; A5 REWORK technical-proposal" | **Hit** |
| P4.1 | `pkt` L199: "SAR 20,000,000 -> **SAR 12,000,000** — SAR 20,000,000 x (1 - 40%)"; `pkt` L1255: "CHANGED VOL-IV-F4E-01: VOL-V 39.4: '20,000,000' -> '12,000,000'" | **Hit** |
| P4.2 (DC4) | `pkt` L482: "annotate VOL-V:39.4 effect confirms" | **Hit** |

### Clarification responses (5): 3 / 2 / 0

| Key | Evidence | Verdict |
|---|---|---|
| Q15 | `pkt` L487: "`ADD-03/Q15` amendment_op annotate VOL-I:8.9 effect interprets"; `rows` L161–162: "Q15 adds that such a member 'shall give its own undertaking'" | **Partial.** Both limbs are read correctly (the route is closed; the 2.4 member gives its own undertaking). The first limb is not in force, because 8.9 is not replaced; the annotation sits on a unit that 2.1 deletes (the critic: `pkt` L491). |
| Q16 | `pkt` L498–499: "escalation why: software limitation: Q16 prints a relative change … that applies only 'for an application lodged not later than Sunday 22 November 2026'"; `iss` L189: "(1) Row 2 of the Arabic … prints the issue period as '٥'; … English … '3'. … (2) Reading A: Q16 amends Table 8-1 …; Reading B: it reports the Office's confirmation" | **Partial.** Correctly targeted and the lodging condition is kept, but the base is left open (5 or 3) and C3 is not produced. |
| Q17 (DC5) | `pkt` L520, L523: "annotate VOL-V:44.2 effect confirms … CONFIRMED (unchanged) VOL-V-44.2-01" | **Hit** |
| Q18 (DC7) | `pkt` L527: "The response only cross-refers: 'See new Volume II Clause 4.6…'" | **Hit.** It is not used to settle GA1. |
| Q19 (DC6) | `pkt` L532: "disposition no_effect: The response only cross-refers: 'Yes. See Section 4 of this Addendum.'" | **Hit** |

### Image item (1): 1 / 0 / 0

| Key | Evidence | Verdict |
|---|---|---|
| IMG1 | `pkt` L61–64 and L552–721. The reading gives: the title "جدول ٨-١: مدد إصدار شهادة تسجيل الاستثمار"; row 1 "…مجلس التعاون الخليجي … السجل التجاري مصدقاً … ٣"; row 2 "…خارج دول مجلس التعاون الخليجي … السجل التجاري والقوائم المالية المدققة لآخر سنة مالية، مصدقة … ٥"; row 3 "فرع مسجل في المملكة لشركة أجنبية … ٨"; note 1 "…من يوم العمل التالي ليوم استلام الطلب المكتمل."; note 2 "…تسعين (٩٠) يوماً…"; ref "الرقم: ٢٢٨/٢٠٢٦"; date "التاريخ: ١٦ نوفمبر ٢٠٢٦م". | **Hit.** All ten key strings match. One diacritic differs: note 3 is read "تُقدِّم" where the key has "تُقدَّم" (active for passive voice; the meaning is unchanged). The reading stays pending a person's approval, by the tool's policy (`pkt` L104). Sub-item **AR1** (Arabic ٥ against English 3) is detected (`iss` L223) but kept open: **partial**; see S1. Row 2's own A1 row (D-ROW-02) was **not promoted** ("conflicting": `pkt` L319). Of the AppA rows, only 01, 03, 04 and 05 are in A1 (`a1` L46–65), so the governing value that matters is the one missing. |

### Computed values (4): 1 / 3 / 0

| Key | Evidence | Verdict |
|---|---|---|
| C1 = SAR 12,000,000 | `pkt` L199 (above); `out-candidate/a2/a2.md` L422: "SAR 20,000,000 -> SAR 12,000,000 (computed: SAR 20,000,000 x (1 - 40%) …; PROPOSED, never typed)" | **Hit.** Computed by the engine, with its derivation. |
| C2 = 42 months | `P` L4826–4834: "The adjust_value op was simulated and refused (C24): 'the previous value is also written in words …' The resulting period is not typed here." | **Partial.** The inputs (36, +6) and the cover's "forty-two (42)" are laid side by side; no value is produced. The long-stop (42 months + 365 days) is not given, though 18.3's "365 days after the Scheduled PCOD" is cited. |
| C3 = 3 WD (row 2, lodged by 22 Nov) | `iss` L225–230: "Reading (a): the translation is wrong; the period is 5, reduced by 2 only for applications lodged by 22 November 2026. Reading (b): the translation shows the post-Q16 figure." | **Partial.** The right reading is stated, but no value is produced, and the wrong base is kept open as reading (b). The wrong result "1 WD" is not asserted. |
| C4 = 30,000 or 45,000 m3 | `iss` L18–23: "Reading 1: the volume is sized on the average daily flow. Reading 2: it is sized on the peak hourly design flow. … No volume is computed." | **Partial.** Both bases are named and neither is asserted. Neither volume is computed. |

### Derived dates (9): 5 / 0 / 4

| Key | Evidence | Verdict |
|---|---|---|
| D0 Thu 12 Nov (cut-off) | `pkt` L118: "the clarification window closed on 2026-11-12 (VOL-I 5.2)" | **Hit** |
| D1 Wed 18 Nov (planning date) | `pkt` L1312: "Programme impact (status date 2026-10-22 -> 2026-11-18)" | **Hit** |
| D2 Sun 22 Nov (Q16 lodging limit) | `pkt` L498: "'for an application lodged not later than Sunday 22 November 2026'" | **Hit** (stated) |
| D3 Mon 23 Nov (2.5 notification) | `pkt` L159: "-> **2026-11-23** (computed: … anchor PDD = 2026-11-26, rule working-days-before)" | **Hit.** Not carried into A5: `a5p` L47 reads "NO DEADLINE REACHED". |
| D4 Sun 22 Nov (row 1 latest lodging) | none. `DS` L5282 (D-ESC-01): "So I propose no 'issue' activity and no successor" | **Missed** |
| D5 Sun 22 Nov (row 2) | none | **Missed** |
| D6 row 3 infeasible (Sun 15 Nov) | none. Row 3 is raised only as a class question (`iss` L128) | **Missed** |
| D7 Wed 25 Nov (certificate in hand) | none | **Missed** |
| D8 6 WD issue → PDD | `pkt` L158: "Working Days left from the issue date (2026-11-18) to the PDD (2026-11-26): 6" | **Hit.** The run uses a different convention (issue day not counted, PDD counted); the count is the same. |

### New obligations (6): 1 / 5 / 0

| Key | Evidence | Verdict |
|---|---|---|
| N1 licence or Certificate, else rejection | `iss` L42–48: "ADD-03 2.1 deletes and replaces VOL-I 8.9 … with the words 'A Proposal that does not include the evidence … shall be rejected.'"; `a3c` L11–16: one change only (ADD-03-2.4-01 as a general gate) | **Partial.** Quoted and understood, but it reaches neither A1 in force nor A3. |
| N2 Office application, drop-dates | `a1` L42 (row 2.3); `pkt` L167: "activity `investment-registration-application` conditional on reading ADD-03-p3-r1" | **Partial.** Row and activity, but no lodging dates. |
| N3 Portal notification by Mon 23 Nov | `a1` L44; `a5mar` L29: "EV-CIR-NOTIFICATION … NO DEADLINE REACHED" | **Partial.** Correctly not in A3, but blocked behind 2.1. |
| N4 2.4 undertaking (member's own) | `a1` L43; `rows` L158–162 | **Partial.** Correct content, UNRESOLVED. |
| N5 reservoir volume and compartments | `a1` L41 | **Hit** |
| N6 reflect 4.6 and 42 months | `a1` L45; `pkt` L469 | **Partial.** The obligation is carried, but its 42-month content is unavailable (3.3 escalated). |

### Indirect effects (8): 1 / 5 / 2

| Key | Evidence | Verdict |
|---|---|---|
| IE1 Envelope A, never B | `candidate-curation/evidence_items/ADD-03-ai.yaml`, EV-INVESTMENT-REG-CERT: "envelope: A … Envelope A is taken from ADD-03:2.1"; `a5mar` L21 EV-INVESTMENT-LICENCE in envelope A | **Hit.** The marshalling slot 9.1(i) is not named. |
| IE2 modality change → new A3 entry; undertaking superseded | `DS` L2402 (D-03): "VOL-I:8.9 therefore keeps its ADD-02 text, and row VOL-I-8.9-01 and activity investment-licence stay on that text"; `iss` L42 | **Partial.** Stated as conditional, not applied. |
| IE3 image values → drop-dead dates (row 3 infeasible) | `DS` L5282 (D-ESC-01): "An A5 activity's duration can only name a single lead-time assumption key" | **Missed** (a software limitation the run recorded) |
| IE4 Q16 changes a value that exists only in the image | `pkt` L121: "unsupported: an adjust_value on a cell of a table inserted by the same addendum from a pending image reading" | **Partial.** Exactly identified, but the base is kept open (S1). |
| IE5 18.1 / 18.3 / 39.2 move with the Scheduled PCOD | `DS` L2722: "VOL-V:18.1 (delay liquidated damages run from the Scheduled PCOD); VOL-V:18.3 (period counted from the Scheduled PCOD)" | **Partial.** Named as conditional dependents; no values; 39.2 is not named. |
| IE6 Form 4-D / PCG exposure | none ("Form 4-D", "F4D" and "PCG" appear in no ADD-03 item; `pcg-*` appears only in timing lines) | **Missed** |
| IE7 criterion B (15 marks) and Form 4-F | `iss` L22: "This affects the process design, the construction programme and the capex in the Financial Model (ADD-03 3.4)" | **Partial.** The Financial Model is reached. Criterion B and Form 4-F are not named, and `form-4f` is not marked REWORK. |
| IE8 40.1 and Form 4-E deemed acceptance | `pkt` L1325: "REWORK deviations-review: requirement changed: VOL-IV-F4E-01 (dependency: VOL-V 39.4: '20,000,000' -> '12,000,000' …)"; L1345 "REWORK form-4e" | **Partial.** Form 4-E is reached through a confirmed curated relationship. 40.1 compensation is not named. |

### Genuine ambiguity (1): 1 / 0 / 0

| Key | Evidence | Verdict |
|---|---|---|
| GA1 "design flow" | `iss` L18–29: "ambiguous: inserted VOL-II 4.6 requires 'a working volume of not less than six (6) hours of the design flow'. … Reading 1 … average daily flow. Reading 2 … peak hourly design flow. … HUMAN DECISION PENDING (Technical)"; `a3c` L191 (in A3's open issues) | **Hit.** Surfaced, both readings, routed to a person, nothing decided, and not claimed to be settled by Q18 or ADD-02 Q11. The missing volumes are scored under C4. |

### Settled points (5): 4 / 1 / 0

| Key | Evidence | Verdict |
|---|---|---|
| S1 Arabic governs: row 2 = 5 | The analysis applied it (`pkt` L795: "applied rule: … ADD-03 2.2 provides: 'The Arabic text governs.' (applied, not decided)"). Downstream reversed it (`pkt` L330: "D-ISS-01 … reverses ADD-03/2.2-issue … this item hands the point back to a person"); `iss` L223 "Pending a human decision; the program does not choose." | **Partial.** A settled point is re-opened as HUMAN DECISION PENDING four times (2.2-issue, T8-1/2:issue, T8-1/2:q, D-ISS-01, plus D-CQ-01). |
| S2 "as issued" = the base undertaking | `iss` L64–75: "The undertaking itself is described only by the deleted words 'a signed undertaking to obtain such licence prior to Financial Close'" | **Hit** |
| S3 Mon 23 Nov (PDD not counted) | `pkt` L159 | **Hit** |
| S4 forward counting from the Working Day after receipt | `iss` L98ff (I-ADD-03-INVLIC-EVIDENCE-SCOPE (2)): "Table 8-1 Note 1 (Arabic, pending) counts the issue period from the working day after receipt of a complete application" | **Hit.** Read correctly, not escalated, not used for dates. |
| S5 ADD-03 valid after the cut-off | `pkt` L118: the cut-off only closes the clarification route; ADD-03 is processed as in force | **Hit** |

### Structural changes (4): 1 / 3 / 0

| Key | Evidence | Verdict |
|---|---|---|
| ST1 VOL-II 4.6 inserted, no renumbering | `pkt` L423–426: "insert_unit VOL-II:4.5 … 'number' 4.6 matches the provision" | **Hit.** Applied. |
| ST2 scoped exception 2.4 | `pkt` L362 "annotate VOL-I:8.9 effect disapplies"; held (`pkt` L363) | **Partial.** Drafted correctly. The controller treats it as a competing change (§3, R1). |
| ST3 Table 8-1 forms part of Volume I | `pkt` L298 "insert_table ADD-03:p3-image"; held (L299) | **Partial.** Drafted correctly, lost in combine. |
| ST4 8.9 deleted and replaced | `pkt` L268 | **Partial.** Drafted correctly, held. |

### Cover errors (3): 0 / 3 / 0 (all detected; all held open)

| Key | Evidence | Verdict |
|---|---|---|
| E1 SAR 8,000,000 | `pkt` L1232 (C28 "figure differs"); `iss` L206–210: "calculate (percentage_of) gives 40% x SAR 20,000,000 = SAR 8,000,000, which is the amount of the reduction"; but `iss` L241–247: "which figure the Authority intends is not decided here" | **Partial.** The candidate carries 12,000,000, but the cover's figure is kept open for Legal. |
| E2 requests "15 to 20" | `pkt` L1233; `iss` L169–180: "Reading 1: the cover's '20' is a misprint. Reading 2: a request 20 exists but was not answered … Reading 3: … intended but omitted" | **Partial** (held open) |
| E3 2.5 "failing which … rejected" | `iss` L3–9 and L82–90: "Operative Section 2.5 prints the notification obligation with no consequence. The cover summarises and does not amend. Open question: does any bid-out consequence attach …" | **Partial.** The row says "none stated", and 2.5 is correctly kept out of A3, but the point is held open twice. |

### Decoys (9) and must-not-report (22)

| Key | Run | Result |
|---|---|---|
| DC1 1.3 | no_effect (`pkt` L262) | not reported |
| DC2 2.6 | confirms (`pkt` L411) | not reported |
| DC3 3.2 | no_effect (`pkt` L440) | not reported |
| DC4 4.2 | confirms (`pkt` L482) | not reported |
| DC5 Q17 | confirms (`pkt` L520) | not reported |
| DC6 Q19 | no_effect (`pkt` L532) | not reported (its issue concerns E1) |
| DC7 Q18 | no_effect, flagged "a person must confirm (its words carry 'but')" (`pkt` L528) | not reported; trivial over-flag |
| DC8 test label | the image footer "FICTIONAL DOCUMENT … SYNTHETIC: not tender content." is listed as "**UNRESOLVED** ADD-03:p3-image/image-footer … no item proposed for it" (`pkt` L148, L759–760); the cover label is merged into `cover/para3` | **partly reported** (as an unresolved unit, not as an effect) |
| DC9 1.1 | no_effect (`pkt` L240) | not reported |

None of MNR01–MNR22 is asserted. Five are borderline: the run holds them open as readings, never as the candidate's value.

- **MNR01:** "which figure the Authority intends is not decided here" (`iss` L241).
- **MNR02:** "Reading 2: a request 20 exists" (`iss` L169).
- **MNR03:** "whether a rejection consequence attaches" (`iss` L82).
- **MNR04 / MNR18:** "Reading (b): the translation shows the post-Q16 figure" (`iss` L230). That reading would apply the reduction regardless of lodging date.
- **MNR16:** the candidate's VOL-I-8.9-01 is re-made at ADD-03 "with the same words" and still reads "or a signed undertaking to obtain one before Financial Close" (`a1` L109). A5 reads "CONFIRMED (unchanged) investment-licence" (`pkt` L1353), and DS-17 proposes "no_change" for that activity (`DS` L2059). All three are caveated NOT SETTLED / CONDITIONAL.

The others are clean:
- MNR05–MNR15 and MNR17 are not asserted.
- The PDD stays 2026-11-26 (MNR13).
- Form 4-D is never touched (MNR11).
- Q18 and ADD-02 Q11 are not used to settle GA1 (MNR22).

### Acceptable if raised (9): 3

- **Raised:**
  - **AIR1, in part:** 90-day validity, with no comparison to the 150-day Proposal validity (`iss` L158).
  - **AIR4:** whether the rejection reaches a missing 2.4 undertaking (`iss` L64).
  - **AIR5:** the class of a Kingdom branch (row 3) (`iss` L128; `iss` L143).
- **Not raised:** AIR2, AIR3, AIR6, AIR7, AIR8, AIR9.

## 2. Usable updates

What was promoted (`pkt` L919–937): 7 ops, 22 dispositions, 10 new rows, 4 readings, 17 issues, 2 evidence items, 2 activities, 2 lead times, 8 relationships, 0 clarifications; 23 provisions unresolved. Nothing is approved.

| Verdict | Key items |
|---|---|
| **Applied as a person could accept it as is** | P1.1, P1.2, P1.3, P2.6, P3.2, P4.2, Q17, Q18, Q19 (dispositions and confirmations); P3.1 / ST1 / N5 (insert_unit after 4.5 plus row `ADD-03-3.1-01`, both limbs); P4.1 / C1 (adjust_value, SAR 20,000,000 × (1 − 40%) = **SAR 12,000,000**, plus the Form 4-E dependency); GA1 (issue I-ADD03-DESIGN-FLOW) |
| **Applied in part** | P-PREC (row `ADD-03-cover-01`, not verbatim and sourced from the merged cover unit); P2.3 / N2 (row; the activity `investment-registration-application` is conditional, with no dates); P2.4 / N4 (row with the right content, UNRESOLVED); P2.5 / N3 (row plus computed date 2026-11-23, but the A5 activity is BLOCKED with no deadline); P3.4 / N6 (row plus REWORK of technical-proposal and fin-model-build/freeze; the 42 months are missing); Q15 (annotate promoted, effect not in force); IMG1 (rows AppA-01/03/04/05 conditional on the pending reading; row 2 withheld) |
| **Detection only** | P2.1 / ST4 / N1 / IE2 (replace_text correct, held as "conflicting"); P2.2 / ST3 (insert_table correct, held as "insufficient_evidence"); ST2 (annotate disapplies, held); P3.3 / C2 (escalated); Q16 / C3 / IE4 (escalated); C4 (no volumes); IE5, IE7, IE8 (named as dependents or REWORK only) |
| **Wrong as applied** | VOL-I-8.9-01 re-made at ADD-03 "with the same words, values, parameters, dates and consequence" (`pkt` L1353). The investment-licence activity is marked "CONFIRMED (unchanged)" and DS-17 proposes no change, so the candidate shows the deleted undertaking route as unchanged. It is caveated NOT SETTLED, but it is the opposite of the addendum. |

**Structural changes as applied:**

- **Relocation / insertion (ST1):** applied.
- **Scoped exception (ST2):** not applied.
- **Table made part of a volume (ST3):** not applied.
- **Replacement (ST4):** not applied.

**Computed values:** only C1 is produced (with its derivation). C2, C3 and C4 are laid out without values. One date is computed: D3 = 2026-11-23, by `calc deadline` from the PDD 2026-11-26.

**A3:** the candidate A3 gains only `ADD-03-2.4-01`, as a "General gate — mandatory, pass or fail; no bid-out consequence stated" (`a3c` L13, L100). That placement is acceptable under AIR4. The rejection that the key adds (new 8.9) is absent, because 2.1 is not applied, and GA1 appears only among the open issues (`a3c` L191). The 2.5 notification and VOL-II 4.6 are correctly not added.

## 3. Missed effects and why (from the run's own files)

| # | What was lost | Stage | The run's recorded reason | Class |
|---|---|---|---|---|
| R1 | 2.1, 2.4 and 2.5 (and with them N1, IE2, ST2, ST4, the A3 rejection, and the undertaking route's retirement) | validation (consistency) | "VOL-I:8.9: ADD-03/2.1, ADD-03/2.4 change the same unit in different ways across the set" (`pkt` L269). D-03: "The consistency check treats op ADD-03/2.1 (replace_text) and op ADD-03/2.4 (annotate, disapplies) as changing the same unit in different ways, so neither is applied" (`DS` L2402). The critic: "2.4 does not rewrite the text of 8.9. It disapplies Section 2.1 for one class of member … an exception to scope, not a competing text change" (`pkt` L272). | **Software limitation**, correctly named "software limitation" by DS-19 (`DS` L2216) |
| R2 | 2.2 insert_table (ST3), the 2.2 / 2.4 / 2.5 analysis issues | combine / validation | "dependencies: unknown ids ['S-F3']" (`pkt` L299); D-01: "not promoted, because its analysis statements were missing" (`DS` L2270). At batch level the same items were `interpretation_pending` (`proposals/ADD-03-host-20261008T054750Z-c3d5/log.jsonl`, `revalidated_for_reuse`). In the combined set the statements are renamed `analysis-002/S-F3`, but the bare ids in `dependencies` are not. | **Software defect** (the run reports it as insufficient evidence) |
| R3 | C2 = 42 months; IE5 values; N6 content | analysis | "adjust_value cannot rewrite a previous value stated in both words and figures … a person writes the op" (`pkt` L125) | **Software limitation**, stated |
| R4 | C3 = 3 WD; IE4 | analysis | "an adjust_value on a cell of a table inserted by the same addendum from a pending image reading, applying per application by lodging date" (`pkt` L121) | **Software limitation**, stated. It also folds in a settled point (S1) as "ambiguous", which the critic objects to (`pkt` L509). |
| R5 | D4–D7, IE3, row 3 infeasibility | downstream (A5) | D-ESC-01: "An A5 activity's duration can only name a single lead-time assumption key. The Office wait cannot be modelled as a pack-stated, class-dependent period" (`DS` L5282) | **Software limitation**, stated |
| R6 | C4 volumes | analysis / downstream | "No volume is computed." (`iss` L23). The rationale given is not to compute under an open ambiguity. | Policy choice. The key wants both values shown. |
| R7 | IE6 (Form 4-D / PCG), IE7 (criterion B, Form 4-F), IE5 39.2, IE8 40.1 | downstream | No task was generated for them: the 7 conditional impact tasks follow units changed directly and curated relationships, and no relationship links VOL-V 12.1 to Form 4-D or Table 1-1 B (`pkt` L1269–1300) | **Missing evidence path** (relationships), not stated as such |
| R8 | 2.5 deadline into A5 | outputs | The activity's row is unresolved, so "NO DEADLINE REACHED" (`a5p` L47), though the packet computed 2026-11-23 | **Software defect** (propagation) |
| R9 | Row 2 of Table 8-1 in A1 (AppA-02) | downstream validation | "conflicting — declared_conflicts: the proposer declares: ADD-03:T8-1/2; ADD-03:Q16" (`pkt` L904) | A settled point treated as a conflict |

Only GA1 is a **genuine ambiguity**, and the run handles it as one.

## 4. False positives and false signals

- **No false change was proposed.** Every promoted op is supported by the key.
- **The deleted undertaking route is shown as current.** The candidate keeps it alive: "Wrong as applied" in §2; MNR16 borderline.
- **Settled points re-opened as a person's decision:**
  - S1 (four to five items);
  - E1 ("which figure the Authority intends");
  - E2 ("a request 20 exists" as Reading 2);
  - E3 (twice: `iss` L3, L82);
  - 2.1 against 2.4 framed as a "conflict" for Legal (`iss` L42; DS-18): the documents settle this, since 2.4 is an express carve-out;
  - Q16 "Reading B (reports only)": the response is an Addendum answer under VOL-I 5.3 and the key treats it as changing.
- **Noise:**
  - 16 image units (letterhead, addressee, stamp, footer, "ملاحظات:") count as "unresolved provisions" (`pkt` L132–148). That inflates "23 unresolved" to look worse than it is: 7 operative provisions are truly unresolved.
  - The same 6-concern critic block is repeated 16 times (`pkt` L551–770).
  - Two generic "composite asset" class-scope issues are attached to a member-class table (`iss` L258, L274).
- **The C46 check-register defect is a false signal.** It reads the cover's "rejected" as an obligation reaching no output (`pkt` L944), because the cover was merged with an operative paragraph.
- **The A5 programme now shows 39 activities INFEASIBLE (and the clarifications activity DEADLINE PASSED)** at the 18 Nov planning date (`pkt` L1312–1423). This follows from 6 Working Days against PROVISIONAL lead times, not from ADD-03's content. It is labelled, but it buries the four activities ADD-03 actually touches.
- **Nothing the key reserves for a person is asserted as settled.** GA1, bidder facts, member class and the 2.4 consequence are all left open.

## 5. Pending decisions

- **What is pending:**
  - 8 analysis items and 13 downstream items carry **HUMAN DECISION PENDING** (`pkt` L255–513; L856–916).
  - There are 11 escalations: 2 in analysis (3.3, Q16) and 9 downstream (DS-19, D-01, D-03, D-06, D-07, D-08, D-14, D-16, D-ESC-01).
  - 17 issues are promoted, all pending (`iss`).
  - 23 provisions are unresolved (7 operative ones: 2.1, 2.2, 2.4, 2.5, 3.3, Q16, and the image rows behind 2.2).
  - 1 image reading awaits approval.
- **Every judgment the key reserves for a person is left to a person:** GA1, the bidder facts and member classes (AIR5), the 2.4 consequence (AIR4) and certificate validity (AIR1). The row-3 escalation the key expects (D6) is **not** raised as an infeasibility; it is raised only as a class question.
- **Over-escalated** (the documents settle these):
  - S1, five items;
  - E1, two;
  - E2, one;
  - E3, two;
  - the 2.1 / 2.4 "conflict", three (I-ADD03-8.9-CONDITIONAL, DS-18, D-03);
  - 3.3's 42 months, two (I-ADD03-PCOD-3.3, D-07);
  - Q16 "Reading B", one.
- **What a person must really decide, by my count: about 5.**
  1. GA1, the design flow.
  2. Approve or correct the Table 8-1 reading.
  3. The bidder facts: which members are foreign, their class and licence status, and 2.4 eligibility.
  4. The row-3 route (licence or 2.4 only).
  5. Whether to treat a missing 2.4 undertaking as a rejection risk.

  Everything else is either (a) accepting the proposed ops, or (b) writing three ops the software could not: 2.1 together with 2.4, 3.3 as 42 months, and Q16 on row 2. That is document control, not judgment. Against ~49 pending markers, the person faces mostly duplicates.

## 6. Interventions

| Time (UTC) | Event | Source |
|---|---|---|
| 05:37:33–34 | Panel started; PDF uploaded through *New addendum*, route host, job pid 4329 | `clock.txt` L1–4 |
| 05:45:18 | The driver waits for the next analysis submission | `clock.txt` L5 |
| 05:47:50–55 | analysis-002's host session (`…054029Z-9311`) staged set `…054750Z-c3d5`; coverage event 05:47:54, end 05:47:55 | `proposals/ADD-03-host-20261008T054750Z-c3d5/log.jsonl` |
| 05:47:55 | **Planned SIGTERM** to pid 4329. The checkpoint records "interrupted … SIGTERM, host_sessions_stopped 2" (analysis-002 and analysis-003) | `clock.txt` L6; `ckpt` L6695; `pkt` L1182 |
| 05:48:00 | The interrupted job ended "status failed". `run.log` L53–54 shows a Python traceback ending `Terminated: signal 15 (SIGTERM)`, while the checkpoint records `segment_ended … status: stopped` | `clock.txt` L7; `run.log` L1–54 |
| 05:48:01 | **Resume** through the panel's Resume (pid 6988, status before "stopped") | `clock.txt` L8; `ckpt` events "resumed" |
| 05:48:03 / 05:48:05 | analysis-003 and analysis-004 asked ahead | `log` |
| 05:48:10 | **analysis-002's submission reused after revalidation.** `revalidated_for_reuse`: the statuses equal `statuses_at_submission`; no new session for analysis-002 (`bench`: "reused yes", session "-") | `ckpt` L6730; `run.log` L58 |
| 06:00:53 | `prefetch_discarded` analysis-004: "the batch's packet changed before its turn (an earlier batch answered part of it); asked again". That was the 768.1 s session `…054805Z-a40f` (19 units, 62.5k output tokens); the re-ask took 89.9 s for 2 provisions | `ckpt` L6738; `bench` |
| 06:22:46 | The resume job finished, exit 0, status partial | `clock.txt` L9 |

Questions the brief asks:

- **Was any batch asked twice? Yes, two:**
  1. **analysis-003.** Its first session (`…054515Z-3dc7`, 160.8 s) was stopped by the SIGTERM before submitting and was asked again (`…054803Z-6882`, 399.7 s). That is the code's stated behaviour ("else it is asked again").
  2. **analysis-004.** It was asked on a stale packet. The resume dispatched it 5 s **before** folding in the reused analysis-002, whose 2.2 op accounts for most of analysis-004's units.
- **analysis-002 was not asked twice.**
- **Was the submission made just before the stop reused after revalidation, as the code claims?** Yes:
  - the `submission_reused` and `revalidated_for_reuse` events;
  - `set_status: partial` is the batch's coverage of all 52 provisions, not an error;
  - the reused items are present in the combined set.
- **Concurrency records** (`ckpt` L6931–7010; `bench`):

  | Segment | Dispatched | Taken | Discarded | Max running | Busy | Window | Idle slots |
  |---|---|---|---|---|---|---|---|
  | 1, analysis (interrupted) | 3 | 1 | 0 | 2 | — | — | — |
  | 2, analysis | 4 | 4 | 1 | 2 | 1977.1 s | 1167.4 s | 357.6 s |
  | 2, downstream | 3 | 3 | 0 | 2 | 1196.6 s | 707.5 s | 218.5 s |

  The rate gate never paused.
- **Did both segments run on the same code?** Yes. Content `a9ebd02ab0cbf8a7…` over 99 files and policy `072b3f8e…` in both, with `"differ": false` (`ckpt` L6834). The package identity matches `FROZEN.md` (commit `7c721d4`).
- **Anything else manual?** No. There was no other stop, edit or approval. The run had no 429, no repair re-ask and no deferral (`pkt` L1167: "every request was answered at the first call").

## 7. Time

**Run timeline:**

| Measure | Value | Source |
|---|---|---|
| Steps' sum | **2,698.9 s (45.0 min)**: analysis 1,638.4; downstream 712.4; readings 156.7; critic 117.6; the rest 73.8 | `run.log` L92–105; `bench` |
| Wall clock, upload → job end | 05:37:34 → 06:22:46 = **45 min 12 s** (2,712 s) | `clock.txt` |
| Wall clock, checkpoint created → updated | 2,706.0 s | `bench` |
| Interruption gap | segment 1 ended 05:47:56, segment 2 began 05:48:01: **5 s** (6 s by `clock.txt`) | `bench` |
| Wall clock without the gap | 620.0 + 2,081.0 = **2,701 s (45.0 min)** | `bench` |
| Host sessions started | **12**: 1 reading, 8 analysis (2 of them wasted: the stopped analysis-003 and the discarded analysis-004 prefetch), 3 downstream | `bench` |
| First useful output | The image reading was staged at 05:40:14 (+2 min 40 s), but it is not reviewable output. The candidate A1–A5 were published at **06:22:34** (+45 min 0 s) and the review packet at 06:22:39–42. Nothing usable reaches a person before then. | `log`; `pkt` L106 |

**Session-level cost:**

- 8 analysis sessions, 2,959 s in all.
- Fixed overhead per session 5–16 s (3.1%).
- Downstream sessions waited 214–442 s at the tail (`bench` "tail").

**What the interruption cost:**

- About 2.7 min of analysis-003's progress.
- The prefetch discard tied up one of the two slots for 12.8 min. Its rework (89.9 s) was on the critical path.

Even removing ~5 min for both, the run is ~40 min.

**Machine load.** `clock.txt` records nothing else running on the machine during the run; the brief states nothing else ran. The full test suite runs only now, while I score, and does not touch the recorded times.

**Record slip.** The packet's timing table (`pkt` L83–98) was written before its own last step finished: "review 0.0 running; total 2696.4", against 2,698.9 s in `run.log` L105. Earlier sessions had the same slip.

**Verdict:** **the 30-minute target is missed by about 15 minutes (45.0 min, +50%)** on an unloaded machine. Analysis alone (27.3 min) nearly fills the budget, and the interruption accounts for at most ~5 of the 15 minutes over.

## 8. General workflow defects seen in this run

1. **A scoped exception is treated as a conflicting change.** The consistency check flags a `replace_text` and an `annotate … disapplies` on the same unit as "change the same unit in different ways". A deletion-and-replacement that carries its own carve-out therefore can never be promoted, and everything that depends on it falls to unresolved. The op vocabulary has no way to compose "replace, except for class X, which keeps the text as issued".
2. **Combining batch sets breaks intra-batch references.** Statement ids are prefixed with the batch id in `statements`, but not where the model cited them in `dependencies`. Items that validated at batch level become `insufficient_evidence` in the combined set, and no repair is attempted. Here that was 4 items, including a table-insertion op.
3. **The resume dispatches look-ahead batches before folding in reused staged submissions.** A batch whose packet depends on the reused one is asked on a stale packet and later discarded. Here that was the longest session of the run.
4. **A relative change cannot be computed when the previous value is written in words and figures.** The same applies to a cell of a table inserted from a pending image reading. The arithmetic is trivial (36 + 6; 5 − 2), but the value is withheld and handed to document control.
5. **Settled points are re-opened downstream.** A precedence rule applied by the analysis ("The Arabic text governs") is reversed by downstream items and handed back to a person. Cover-versus-operative differences are posed as "which figure governs" although the run itself records that "the cover summarises and does not amend". This produces 2–5 duplicates per point and ~49 pending markers for ~5 real decisions.
6. **Computed deadlines do not propagate.** The packet computes the 2.5 date (2026-11-23), but the A5 activity serving that row reports "NO DEADLINE REACHED" because the row is unresolved.
7. **A5 cannot carry a pack-stated, class-dependent lead time,** such as an issue period by member class counted from a stated event. As a result, the addendum's most time-critical consequences (lodging drop-dead dates and an infeasible class) are absent rather than escalated as infeasible.
8. **Segmentation merges the cover summary, the test label and the next operative paragraph into one unit.** Obligations are then sourced from "the cover", and check-register raises a C46 defect on the summary's words.
9. **Non-operative image units** (letterhead, addressee, stamp, footer, a heading) are counted as unresolved provisions, and the packet repeats one critic block per unit. The unresolved count overstates the real gap (16 of 23), and the packet loses readability.
10. **Indirect-effect discovery depends only on curated relationships and directly changed units.** An effect through a form (a guarantee covering the construction period) or through an evaluation criterion is not found unless someone curated the link beforehand.
11. **A requested stop surfaces as a Python traceback and a "failed" job** in the job log and panel, while the checkpoint records "stopped". The two status surfaces disagree.
12. **The packet's timing table is written before the review step ends.** Its total differs from the job log's.
13. **The genuine ambiguity's quantities are not computed,** so the decision-maker gets no cost scale. The run's rule is not to compute under ambiguity; computing both readings as labelled conditional values would not choose between them.
14. **The batch planner splits a provision from the units its op will account for.** Here the image units were in analysis-004 and the 2.2 insertion in analysis-002. A later batch's packet is then rewritten by an earlier one's answer.

## 9. Where the key and the run disagree

- **Q16, "Reading B".** The run (and its critic, `pkt` L510) holds that Q16 may only report "The Office has confirmed to the Authority that …", leaving Table 8-1 unchanged. The pack's words are "Section 2 of this Addendum applies. The Office has confirmed to the Authority that, for an application lodged not later than Sunday 22 November 2026, the issue period in row 2 of Table 8-1 is reduced by two (2) Working Days." I think **the key is right in effect**: the confirmation is published in an Addendum under VOL-I 5.3, so a bidder plans on 3 WD for lodging by 22 November. The run's Reading B is a drafting nicety, not a planning question.
- **E2, request 20.** The key's truth is "there is no request 20". The documents show only that ADD-03 answers 15 to 19 and that 1.3 says those were received in time ("Clarification requests 15 to 19 were received before the time stated in Volume I Clause 5.2."). Whether a late request 20 exists cannot be known from the pack. **The key slightly overstates.** Still, the run's Readings 2 and 3 do not belong in a person's queue, since nothing turns on them.
- **D8 counting convention.** The key counts the issue day in and the PDD out; the run counts the issue day out and the PDD in. Both give 6, so this is no disagreement on the value.
- **2.4 and the rejection sentence.** The run's Reading 2 ("the undertaking is the evidence required for that member, and the rejection words apply", `iss` L64ff) conflicts with "Section 2.1 does not apply to a member …", which disapplies all of 2.1, including its last sentence. **The key is right.** Flagging the omission as a risk (AIR4) is fair; offering the rejection as a reading is not.
- **P-PREC against P-COVER.** The key treats the precedence paragraph ("This Addendum forms part of the RFP Documents … Bidders shall acknowledge receipt in Form 4-A.") as separate from the cover summary. In the PDF it is a separate paragraph after the summary's last line ("requests 15 to 20."). **The key is right**; the run's segmentation is wrong (defect 8).

I found no item where I think the key is wrong on substance.
