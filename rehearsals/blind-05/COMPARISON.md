# Blind rehearsal 05: the workflow's candidate against the sealed answer key

**Synthetic, not tender content.** Scored after the freeze, from the frozen copies in this folder only; nothing under `out-candidate/`, `review/`, `proposals/`, `candidate-curation/`, `downstream/` or `batches/` was changed. Paths are relative to `rehearsals/blind-05/`. Short names used in the evidence column: `ops` = `candidate-curation/amendments/ADD-03.yaml`; `P` = `proposals/ADD-03-run-host-blind05-20261005T025444Z-combined/proposals.yaml` (the 57 analysis items and their 74 statements); `DS` = `downstream/proposals.yaml` (the 60 downstream items); `pkt` = `review/index.md` (the review packet); `iss` = `candidate-curation/register/issues/ADD-03-ai.yaml`; `new` = `candidate-curation/register/rows/ADD-03-ai.yaml`; `rows/…` = `candidate-curation/register/rows/…`; `CQ` = `candidate-curation/clarifications/register.yaml`; `act` = `candidate-curation/activity_templates.yaml`; `rd` = `candidate-curation/readings/ADD-03-p4-r1.yaml`; `a1`, `a2`, `a3c`, `a5c/` = `out-candidate/a1/a1.csv`, `out-candidate/a2/a2.md`, `out-candidate/a3/a3_candidate.md`, `out-candidate/a5/candidate/`. L = line.

## What was frozen and when

- **The addendum.** An independent author wrote Addendum No. 3 ("Issued 15 November 2026", a Sunday, 5 pages) from the pack's PDFs, the brief and the correspondence, without reading the tool (`SEALED/author_notes.md`). Its subjects: VOL-I 6.6 and 6.7 merged into one 6.6 "without change of substance" (the modification cut-off in fact moves to two Working Days before the PDD); the Availability Payment definition put on Base Date prices, a new Base Date (PDD less 28 days) and VOL-V 29.2 replaced by a bidder-elected Indexed Proportion of 50–70 % to year 10, then 75 %; a mandatory membrane filtration step (which switches on the conditional VOL-II 3.2); the odour limit replaced by a value in ESIA Figure 7-2, which is not in the pack; a new VOL-II 5.6 incorporating an image-only Arabic Table 5-1 whose English translation differs on the datum and on the scope; a design-dependent Portal notice (7.3); seven answers (a decoy, a confirmation, three changing answers, a missing-evidence pointer, and Q19, which conflicts with Section 3: the deliberate ambiguity D1); and three new cover-error mechanisms.
- **Before the run.** `FROZEN.md`, 2026-10-04 19:20:22 UTC: the sha256 of the PDF (`9c5e22d5…`) and of the sealed `SHA256SUMS` (`0ed6f3ab…`), recorded before the addendum was ingested.
- **The run.** `tenderpack ai run ADD-03 --route host`, 5 Oct 2026, 02:54:44 to 04:07:11 UTC (`clock.txt`, `run.log`). Nobody curated. Fifteen headless host sessions (one image reading, nine analysis batches, five downstream batches) had only the MCP tools and could not reach the key; a second model (the critic) gave opinions on 58 selected items and changed no status.
- **The freeze.** `FROZEN-OUTPUTS.md` and `FROZEN-OUTPUTS.sha256` (327 files) at 04:08:13 UTC, before the key was opened; the run folder's outputs were copied here.
- **The key.** The files in `SEALED/` are timestamped 04:08:13.6–.9 UTC, after `FROZEN-OUTPUTS.sha256` (04:08:13.45). Checked for this scoring: the three sealed files and the PDF match `SEALED/SHA256SUMS`, and the sha256 of `SEALED/SHA256SUMS` is `0ed6f3ab…`, as in `FROZEN.md`. `sha256sum -c FROZEN-OUTPUTS.sha256`: 326 of 327 OK; `clock.txt` fails because the line "…; frozen 2026-10-05 04:08:13 UTC" was appended to it at the freeze. Its first two lines hash to the frozen value (`a3de270e…`), so no scored file changed.
- **Nothing is decided.** Every op, disposition, reading, row, issue and activity is PROPOSED in the candidate; human approval: none (`pkt` L15); the real `curation/`, `config/` and `out/` were only read.

## The key

`SEALED/expected_findings.yaml`: 15 keyed provisions (1.3 to 7.4; recitals 1.1 and 1.2 are not keyed), 7 answers (Q15–Q21), 3 planted cover errors (E1–E3), the image's 24 Arabic strings with 2 discrepancies (AR1 datum, AR2 scope), 10 secondary effects (S1–S10), 8 indirect effects (IE1–IE8), 3 missing-evidence items (ME1–ME3), 4 ambiguities (D1 has no correct answer), 10 derived dates (DD1–DD10), an A3 delta and 19 "must not report" traps. The author's intent (`author_notes.md`): diff the merged 6.6 against 6.6 + 6.7 rather than trust the label; register the band, the election and both stages, never a single percentage; escalate D1 with both horns and no canon; take Table 5-1 from the Arabic; note that VOL-II 3.2 now applies and that ADD-01 response 1 is partly overtaken; never state an odour value.

## Scoring method

- **N = 38**: the 15 provisions, 7 answers, 3 cover errors, 3 Arabic items (the reading, AR1, AR2) and 10 secondary effects. Indirect effects, missing evidence, ambiguities, dates, the A3 delta and the traps are scored in their own tables, not added to N.
- **Hit**: the frozen outputs state the effect correctly, with the right target, words, dates or consequence. **Partial**: detected but incomplete, wrongly targeted, or left unresolved or escalated where the key expects a definite change (each row says which). **Missed**: absent, or present only in a form that contradicts the key.
- Every row cites the frozen file and line. Where the right statement exists only in an unpromoted analysis statement or escalation, the row says so; such a statement is detection, not an applied change.

## 1. Detection results

**Count: 38 expected findings: 21 hits, 16 partial, 1 missed.** Separately: indirect effects 0 hit / 5 partial / 3 missed of 8; missing evidence 2 / 1 / 0 of 3; ambiguities D1 partial, D2 missed, D3 hit, D4 not used; dates 5 right / 4 partial / 1 missed of 10; traps 19 of 19 avoided; false positives 1, plus 6 false signals (below).

### Provisions (15): 6 hit, 9 partial, 0 missed

| Key | Expected | Result | Evidence in the frozen outputs |
|---|---|---|---|
| 1.3 | no change to 5.2; record that the cut-off (Thu 12 Nov) passed before issue, so no clarification route remains | **partial** | `ops` L244–252 `no_effect` (right). The closed route is recorded only for D1 (`iss` L10–11: "The clarification cut-off (2026-11-12) passed before ADD-03 issued on 2026-11-15"; `CQ` L1043) and in A5 (`pkt` L1248: "FEASIBILITY clarifications: OK -> DEADLINE PASSED"), not as a point that covers every ADD-03 ambiguity; three items still suggest a clarification without saying the route closed (`P` L78, L6345; `DS` L3830) |
| 2.1 | 6.6 replaced; 6.7 deleted, number unused; rows citing 6.7 re-pointed; modification only to Tue 24 Nov; a late modification rejected unopened | **partial** (escalated) | Detection complete: `P` L40–60 (old 6.7 against the new 6.6), L73–79 ("the modification cut-off moves from any time before the Proposal Due Date to two Working Days before it, and late modifications are now rejected unopened"), L81–85 ("Tuesday 24 November 2026"). The `replace_text` on 6.6 is verbatim but held `conflicting` because of the cover (`pkt` L208–216); the deletion of 6.7 is escalated: "the engine rejects set_status on VOL-I:6.7 under C22 ('declared target VOL-I:6.7 is not cited; the provision cites [VOL-I:6.6, VOL-I:6.1]')" (`pkt` L111). Unresolved: `ops` L365–371 |
| 2.2 | no renumbering; 6.7 a gap | **hit** | `ops` L253–260 |
| 3.1 | VOL-V 1.1 amended | **hit** | `ops` L9–24, old and new words verbatim |
| 3.2 | VOL-V 1.1A (Base Date) added | **hit** (its date: DD3) | `ops` L25–41 `insert_unit` after VOL-V 1.1; new row ADD-03-3.2-01 (`new` L7–57: "The Base Date moves with the PDD"; "'days' are read as calendar days") |
| 3.3 | 29.2 replaced: an Indexed Proportion elected in 50–70 % to year 10, 75 % from year 11, indexation from the Base Date; the register holds the band, the election and both stages | **partial** (escalated) | Limb (a) proposed verbatim but `insufficient_evidence`; limb (b) escalated because the quoted replacement is split across the clause and its list item (`pkt` L115; `ops` L373–387). The issue states the content and that it is not applied: "the Bidder chooses the Indexed Proportion within 50–70% for years 1–10 … from year 11 it is 75%" and "VOL-V:29.2 at ADD-03 still reads 60% indexed / 40% fixed" (`iss` L21–34) |
| 3.4 | Financial Model row: Base Date basis, staged indexation, flag D1 | **hit** | `ops` L42–57; `rows/VOL-I.yaml` L690–699: "Availability Payment expressed at Base Date prices; indexation under the new VOL-V 29.2 with the Indexed Proportion. The price basis conflicts with ADD-03 Q19" |
| 4.1 | VOL-II 3.1 amended (membrane step, ≤ 0.1 µm, tertiary or MBR) | **hit** | `ops` L58–75 verbatim; `a2` "Register rows that move": VOL-II-3.1-01 "AMENDED (ADD-03/4.1)" |
| 4.2 | confirming instruction | **hit** | `ops` L76–91, `annotate adds_obligation` on VOL-II Section 3 |
| 5.1 | VOL-II 3.4 amended: the limit is the ESIA Figure 7-2 value at the nearest receptor (not in the pack); basis unchanged; status amended, value unresolved | **partial** (held by the cover's error) | The `replace_text` has the right target and words and declares the figure missing (`pkt` L317–324), but it is not promotable: "ADD-03:cover/para3 names Volume II Clause 3.5 for the odour criterion; the operative provision 5.1 names Clause 3.4" (`ops` L389–395). A1 marks VOL-II-3.4-01 UNRESOLVED (`a1` L189) |
| 5.2 | confirming instruction | **partial** | `annotate adds_obligation` proposed, held `insufficient_evidence` ("Demonstrating compliance needs the ESIA Figure 7-2 concentration", `ops` L397–403); the critic did not agree with the "new obligation" reading (`pkt` L332–341) |
| 7.1 | VOL-II 5.6 added; Table 5-1 added with its values read from the image (25 m / 40 m above natural ground, lighting, permanent and temporary structures including cranes, 30 days' crane notice) | **partial** | 5.6 inserted verbatim (`ops` L193–209) with a new row ADD-03-7.1-01 (`new` L58–114), but the table's content is not registered: "The height values are not taken as parameters here" (`new` L80), and every row and note of Table 5-1, Arabic and English, is unresolved (`ops` L437–535) |
| 7.2 | where Appendix B differs, record the Arabic; report AR1 and AR2 | **partial** (escalated) | Both discrepancies reported (AR1, AR2 below) and the rule applied in reasoning: "the height datum and the scope of the limits must be taken from the Arabic" (`P` L947–953); escalated because "No op type records a language-precedence rule between two renderings of a table inside the same addendum" (`pkt` L119–122; `ops` L413–419). The promoted issue still says "The datum then needs to be confirmed" (`iss` L41–43) |
| 7.3 | new conditional obligation: notice by Mon 23 Nov of zone and height for anything above 30 m; no consequence; not an A3 item | **partial** (escalated) | "notify the Authority through the Portal of the zone and height of any structure, plant or equipment over 30 m, not later than three Working Days before the PDD … It needs an A1 register row (row_new) and an A5 programme milestone, which a person must create" (`pkt` L123–126); 2026-11-23 computed (`P` L650–655); no row and no A5 activity (`a5c/README.md`: 0 new); correctly kept off A3 |
| 7.4 | confirming instruction | **partial** (escalated) | "annotate (adds_obligation) on the new Clause 5.6 fails C22 (no target at ADD-02)" (`pkt` L127–130; `ops` L429–435) |

### Clarification answers (7): 7 hit

| Key | Expected | Result | Evidence |
|---|---|---|---|
| Q15 | decoy: 6.4 stays seven years; no 10 years | **hit** | `ops` L92–107 `interprets`; `rows/VOL-II.yaml` L918–925, `retention_years_min: 7`. It still marks A5 REWORK (false signal 2) |
| Q16 | confirms 9.6; no new requirement | **hit** | `ops` L108–125 `interprets` on VOL-I 9.6 and Form 4-E; `rows/VOL-I.yaml` L570–580 keeps 9.6's own consequence. CHANGED and REWORK marks follow (false signal 2) |
| Q17 | one compliant certificate per member of an unincorporated EPC JV; copies in Envelope A | **hit** | `ops` L126–141; `candidate-curation/register/rows.yaml` L199–203; activity iso-copy (`act` L420–432: "one per EPC JV member where the EPC Contractor is an unincorporated JV"); not extended to the O&M Operator or an incorporated EPC Contractor |
| Q18 | receptor and value only in ESIA Figure 7-2; nothing inferred | **hit** (detection) | `ops` L405–411: "ESIA Figure 7-2 content (receptor and concentration) is not in the evidence build"; no value anywhere |
| Q19 | report as conflicting with 3.1 and 3.3; do not resolve; escalate (D1) | **hit** | Issue I-ADD03-PRICE-BASIS (`iss` L3–20): both bases, "The pack does not say which governs", owner Commercial lead, shown on the candidate A3 (`a3c` L165); clarification draft CQ-ADD03-01: "Not settled. Q19 and Section 3 are issued in the same addendum, and neither says it prevails over the other" (`CQ` L1009–1048). Caveat: the promoted op ADD-03/Q19 (`ops` L142–158) states Q19's basis as a plain interpretation; the conflict is carried by the issue and the row notes, not by the op |
| Q20 | the Form 4-F row carries the Indexed Proportion; never in Envelope A (6.2) | **hit** | `ops` L159–176; `rows/VOL-I.yaml` L224–236 (`named_by_addendum: the Indexed Proportion (ADD-03 Q20)`, with 6.2's consequence); `rows/VOL-IV.yaml` L450–462; A3 VOL-I-6.2-02 "see ADD-03/Q20" (`a3c` L42) |
| Q21 | 9.7 extended: crane and lifting plan against Table 5-1 | **hit** | `ops` L177–192; `rows/VOL-I.yaml` L616–630; activity technical-proposal (`act` L385; `a3c` L115) |

### The cover's planted errors (3): 2 hit, 1 partial

| Key | Mechanism | Result | Evidence |
|---|---|---|---|
| E1 | "consolidates … without change of substance" is false | **hit** | Declared on the cover and on 2.1: "The cover says the 6.6/6.7 consolidation is 'without change of substance', but ADD-03:2.1 shortens the modification window to two Working Days before the Proposal Due Date" (`P` L1277–1278; `pkt` L143, L171–185), first in the packet. The deterministic cover check compared nothing: "ADD-03's cover has no 'This Addendum ...' sentence" (`pkt` L1154), because "consolidates" is not one of its verbs |
| E2 | the cover names 3.5 (noise) for the change to 3.4 (odour) | **hit** | "names Volume II Clause 3.5 for the odour criterion; the operative provision 5.1 names Clause 3.4 and quotes words found only in 3.4 (3.5 is the noise clause)" (`pkt` L320); VOL-II 3.5 not amended |
| E3 | the cover's "permanent structures" repeats the non-governing translation | **partial** | Stated in an analysis statement: the Arabic scope is "wider than English note (1) … and wider than the cover note's 'permanent structures'" (`P` L683–689), and in an escalation's rationale ("It also bears on … cover/para3 ('permanent structures')", `P` L6418–6421). It is not among the cover's declared conflicts (`P` L1276–1280 lists only E1 and E2), so the packet's cover entry does not show it |

### The Arabic image (3): 3 hit

| Key | Expected | Result | Evidence |
|---|---|---|---|
| Reading | every Arabic string verbatim, translations apart, pending | **hit** | `rd`: 23 of the key's 24 strings verbatim (checked by script); the lead-in differs by one vowel mark (يُحدِّد read for يُحدَّد). Ref, letter date, zones, 25 / 40, the 30 m lighting rule and all three notes read; the separator in ١٬٥٠٠ flagged uncertain (`rd` L140–143); translations kept apart; status pending, never approved |
| AR1 | datum: natural ground (Arabic) against finished ground (English); report, do not quantify | **hit** | Promoted issue I-ADD03-T51-DATUM (`iss` L35–46): "Where the site is filled, these datums give different allowable heights"; escalations on T5-1/note(2), the Arabic header and note 2 (`pkt` L139). One unpromoted statement overreached ("the Arabic is the more restrictive reading", `P` L691–696); the critic corrected it |
| AR2 | scope: the Arabic adds temporary structures, cranes and construction equipment | **hit** | Escalation on T5-1/note(1) (`pkt` L135–138) and the 7.2 issue: "construction cranes and temporary works fall under the 25 m (Zone A) and 40 m (Zone B) limits" (`P` L4051–4058). Reported in the packet's first section; not in a promoted issue |

### Secondary, undisclosed effects (10): 3 hit, 6 partial, 1 missed

| Key | Expected | Result | Evidence |
|---|---|---|---|
| S1 | modification cut-off Tue 24 Nov; late modification rejected and returned | **partial** | Computed and stated (`P` L73–85), not applied. The candidate A1 and A5 still carry VOL-I-6.7-01 "MODIFY-CUTOFF: 2026-11-26", unflagged (`a1` L73; `a5c/milestones.csv` L10): false positive 1 |
| S2 | Base Date Thu 29 Oct 2026, already past at issue | **partial** | `new` L32–33: "it falls on 2026-10-29 (PDD as day 0) or 2026-10-30 (PDD as day 1); the pack does not state the counting" |
| S3 | indexation from the Base Date; band and election to year 10; 75 % from year 11 | **partial** | Stated in `iss` L4–8 and L21–34; not applied (VOL-V-29.2-01 STALE in `a1`) |
| S4 | assessment point moves to the receptor; 5 OU/m3 gone; value not in the pack | **partial** | The 5.1 op carries the new words (`pkt` L317–324), held by the cover conflict; VOL-II-3.4-01 UNRESOLVED (`a1` L189); no value stated |
| S5 | VOL-II 3.2 (7-year warranted membrane life, replacement in the lifecycle plan) switches from conditional to always applicable; ADD-01 response 1 partly wrong | **missed** | VOL-II-3.2-01/02 untouched (`a1` L186–187) and nothing says 3.2 now applies; the re-made 3.1 reading says the opposite of the second half: "The ADD-01 Q1 statement that an MBR is not required remains consistent" (`rows/VOL-II.yaml` L384–392). A2's mechanical "ADD-01:Q1 … REVIEW" (`a2` L410) is credited under IE3 |
| S6 | Portal notice by Mon 23 Nov for anything above 30 m; design-dependent; no consequence | **partial** | `P` L650–655 (2026-11-23); `pkt` L123; no row, no milestone |
| S7 | Arabic: natural ground datum; temporary structures, cranes, equipment included; 30 days' notice before a crane | **partial** | All three read and stated (`P` L1002–1021, L4051–4058; `pkt` L601–611); only the datum reached a promoted issue; the crane notice left open on "whether 'days' are calendar or working days" (`ops` L529–535) |
| S8 | Q17: certificate per JV member | **hit** | as Q17 |
| S9 | Q20: Form 4-F row completed; never in Envelope A | **hit** | as Q20; envelope check in assemble-envelope-a: "in particular no Indexed Proportion" (`act` L128; `a3c` L120) |
| S10 | Q21: crane and lifting plan | **hit** | as Q21 |

### Indirect effects (8): 0 hit, 5 partial, 3 missed

| Key | Result | Evidence |
|---|---|---|
| IE1 definition change reaches every use (Form 4-F rows, VOL-I 10.2, the Financial Model); raise D1 | **partial** | D1 raised; the Form 4-F row notes the conflict (`rows/VOL-IV.yaml` L450–462). VOL-I 10.2 and Form 4-F are reached only through relationships from VOL-V 29.2 (`pkt` L1182–1197), not from the amended definition in VOL-V 1.1 |
| IE2 band → A3 picks up 6.2 and 10.5; the elected figure in Envelope B only | **partial** | 6.2 on A3 (`a3c` L42) and in the envelope checks (`act` L128, L582); the derived 10.5 consequence of an out-of-band figure is absent (A3 VOL-I-10.5-01 unchanged, `a3c` L44) |
| IE3 3.2 applies; ADD-01 response 1 listed in A2 | **partial** | `a2` L410 lists ADD-01:Q1 for review; 3.2's status change, 4.3's four streams and the lifecycle plan are absent |
| IE4 cranes in the construction methodology; conditional Portal notice; 30-day crane notice | **partial** | technical-proposal activity: "construction methodology with a crane and lifting plan demonstrating compliance with Table 5-1" (`a3c` L115); the 7.2 issue ties cranes, Q21 and 7.3 together (`P` L4056–4058); no notice milestone; the crane notice is not in the programme |
| IE5 membrane lifecycle and handback (optional) | **missed** | nothing |
| IE6 no clarification route for any ADD-03 ambiguity, in A3 and A5 | **partial** | stated for D1 (`iss` L10–11; `CQ` L1043) and as A5's DEADLINE PASSED (`pkt` L1248); not on D2, D3, ME1, ME2 or the A3 unresolved list |
| IE7 6.7 rows re-pointed; 24 Nov in A5; late modification on A3 | **missed** | only 2.2's "no renumbering" is right; VOL-I-6.7-01 stays ACTIVE and unflagged at ADD-03 (`a1` L73); no packet item names it |
| IE8 odour at the receptor against stack heights | **missed** | nothing |

### Missing evidence (3): 2 hit, 1 partial

| Key | Result | Evidence |
|---|---|---|
| ME1 ESIA Figure 7-2 | **hit** | 5.1, 5.2 and Q18 declare it missing (`ops` L389–411); 5 OU/m3 not carried as the ADD-03 value. Mislabel: the candidate A3 lists I-VOL-II-MISSING (the ESIA) as "not reached by this addendum's changes" (`a3c` L142) |
| ME2 zone line and ground levels (Volume III) | **partial** | "Site grading and fill depths, needed to size the datum effect" declared missing in the unpromoted 7.2 issue (`P` L4107–4109); the eastern boundary / zone line and Volume III are not connected (I-VOL-III "not reached by this addendum's changes", `a3c` L140) |
| ME3 Schedule 9 | **hit** | "Schedule 9 is still not supplied (I-VOL-V-MISSING)" (`iss` L25) |

### Ambiguities

| Key | Result | Evidence |
|---|---|---|
| D1 price basis (no correct answer) | **partial** | Escalated as intended: both horns, the same addendum, neither prevails, the cut-off passed, owner Commercial lead, no default (`iss` L3–20; `CQ` L1009–1048; fin-model-build "the price basis follows the decision on I-ADD03-PRICE-BASIS", `a3c` L114). Missing: the non-responsiveness constraints that stop a bidder qualifying the price (10.5, the Form 4-F confirmation, Form 4-E and 6.2, 11.5); only "A price on the wrong basis risks being treated as conditional or non-comparable" (`CQ` L1036–1037) |
| D2 time of day of the 24 Nov cut-off | **missed** | not raised (2.1 unresolved) |
| D3 datum of 7.3's 30 m | **hit** | "The datum then needs to be confirmed before plant heights, the Q21 crane plan and the 7.3 notification are fixed" (`iss` L41–43) |
| D4 membranes as major assets | not used | nothing asserted, nothing to flag |

### Dates (10): 5 right, 4 partial, 1 missed

Right: DD1 issue and planning date 15 Nov (`pkt` L1206: "status date 2026-10-22 -> 2026-11-15"); DD2 cut-off 12 Nov, passed (`iss` L10; `pkt` L1248); DD6 withdrawal until the PDD (nothing moves it); DD7 PDD Thu 26 Nov 14:00 unchanged (`a3c` L20); DD9 letter date 10 Nov (`rd`; translation "Date: 10 November 2026 AD"). Partial: DD3 Base Date (29 or 30 Oct); DD4 Tue 24 Nov (computed in statements, not in A1 or A5, where the 26 Nov cut-off stays); DD5 Mon 23 Nov (computed, not planned); DD10 the 30-day crane notice (read; calendar or working days left open; not planned). Missed: DD8, the nine Working Days from issue to the PDD (A5 does flag each latest start before 15 Nov as INFEASIBLE and "not compressed", which is the key's marshalling expectation).

### A3

The validated A3 stays at ADD-02 (ADD-03 is PARTIAL); the candidate A3 gains 0 rows, loses 0 and changes 1 (VOL-IV-F4F-02, STALE) (`a3c` L9–16).

- New or changed disqualifiers (3): the Indexed Proportion as a 6.2 trigger, **hit** (`a3c` L42); the merged 6.6 late-modification consequence, **missed** (2.1 unresolved); 10.5 for an out-of-band figure, **missed**.
- Unchanged but now relevant (3): 9.6 confirmed by Q16, **hit** (`a3c` L43); 8.3 evidence per JV member, **hit** (VOL-I-8.3-01 re-read, listed in the pass/fail gate, `a3c` L59); 11.5 tied to D1, **missed**.
- Must not be added (3): **avoided**: 7.3, the Table 5-1 limits, odour, membranes and Q15 add nothing to A3.
- Unresolved list (5): D1 yes (`a3c` L165); ME1 yes (5.1, 5.2, Q18 in the unresolved list, `a3c` L69–71); ME2 no; D2 no; "no clarification route remains" no (only inside the D1 issue).

### Traps: 19 of 19 avoided

VOL-II 3.5 not amended (but see false signal 3); no odour value after ADD-03; heights neither from finished ground nor for permanent structures only; no sea-level height or site elevation; Q15 registers no 10 years; Q16 creates no new requirement (but see false signal 2); withdrawal not moved; no renumbering; PDD, time and cut-off unchanged; 75 % not called an inconsistency; D1 not resolved and no canon applied ("operative words govern over the cover" is used only for E1, where it is right); 7.3 neither a disqualifier nor general; Q17 not extended; Tables 2-4 and 2-6 unchanged; odour not an Unavailability Event; no membrane replacement count; the Base Date in calendar days and before the issue date; Form 4-F wording not altered ("Stating the Indexed Proportion is a field of the Form, not a qualification of the price", `DS` L2014–2020); no claim that ADD-03 can still be clarified under 5.2 (CQ-ADD03-01: "The clarification cut-off has passed").

## False positives (what the outputs assert that the key and the addendum do not support)

**One substantive.**

1. **The deleted 6.7 stays live in the candidate.** The candidate A1 shows VOL-I-6.7-01 at ADD-03 as "ACTIVE" with "MODIFY-CUTOFF: 2026-11-26" and candidate status "proposed (existing row; not changed by this run)" (`a1` L73); the candidate A5 keeps the milestone "Last moment to withdraw or modify the Proposal through the Portal (VOL-I 6.7)" on 2026-11-26 (`a5c/milestones.csv` L10). ADD-03 2.1 deletes 6.7 and ends modification on Tue 24 Nov. The row is not even marked "not settled": that mark follows the units an unresolved provision cites, and the citation parser read 2.1 as citing VOL-I 6.6 and 6.1 only. The escalation knows the consequence ("Without it VOL-I:6.7 stays active", `pkt` L112) but no item names the row.

**False signals** (not claims about the tender, but they cost a reviewer time or mislead a quick reader):

2. Confirmations and unchanged re-readings are shown as changes: Q15 (the decoy) and Q16 put technical-proposal, deviations-review and form-4e on REWORK and mark VOL-IV-F4E-01 CHANGED (`pkt` L1170, L1222; `a5c/README.md` L21–37); the VOL-I-6.2-01 re-reading ("Words unchanged … it does not change the two-envelope requirement", `rows/VOL-I.yaml` L189–197) puts assemble-envelope-b, copies, deliver and seal-and-mark on REWORK (`pkt` L1209–1221). Blind-04's follow-up 6, still open.
3. VOL-II-3.5-01 (noise) is flagged UNRESOLVED because the unresolved cover paragraph names 3.5 (`a1` L190; `a3c` L98); nothing says it is amended.
4. The candidate A3 labels I-VOL-II-MISSING (the ESIA) and I-ADD03-29.2-NO-OP "not reached by this addendum's changes" (`a3c` L141–142), although 5.1 and Q18 make the ESIA figure the odour limit and the second is the addendum's own issue.
5. The Base Date is given two dates (29 or 30 Oct) on a counting doubt that "twenty-eight (28) days before" does not raise (`new` L32–33).
6. Row notes cite I-ADD03-AP-PRICE-BASIS (`rows/VOL-I.yaml` L697; `rows/VOL-IV.yaml` L450–462), an issue that was not promoted; the promoted one is I-ADD03-PRICE-BASIS. And ADD-03-7.1-01's proposed post-award evidence speaks of "permanent structures and equipment" (`new` L94–96), narrower than the Arabic's permanent and temporary structures (it does include crane records).

## 2. Missed effects

- **Detected, not applied, because of a tool gap:** the deletion of 6.7 (2.1; the clause list "6.6 and 6.7" is parsed as one citation); the 29.2 replacement (3.3; one quotation split across a clause and its list item); language precedence between two renderings issued together (7.2, Appendix B); obligations that attach to a unit the same addendum inserts (7.3, 7.4).
- **Detected, not applied, because the cover's error held the operative op:** 5.1 (odour) and the 6.6 replacement in 2.1.
- **Detected, not applied, by design until a person approves the image reading:** Table 5-1's zones, heights, datum, scope and notes (7.1, S7; 12 units).
- **Not detected:** VOL-II 3.2 becoming applicable and the second sentence of ADD-01 response 1 being overtaken (S5, IE3; the outputs say the answer "remains consistent"); VOL-II 4.3 for the membrane stage; the lifecycle and handback chain (IE5); the odour and stack-height interplay (IE8); the time of day of the 24 Nov cut-off (D2); the nine Working Days left (DD8); 10.5 for an out-of-band Indexed Proportion and 11.5 for D1; the row VOL-I-6.7-01 (IE7, false positive 1); E3 on the cover entry itself.
- **Computed, not planned:** Tue 24 Nov (modification), Mon 23 Nov (7.3 notice), Thu 29 Oct (Base Date), the 30-day crane notice: none became an A1 date or an A5 milestone.

## 3. Unresolved decisions

23 of 54 provisions are unresolved in the candidate (`ops` L357–535; listed first in `pkt` L107–157); 31 are answered by promoted items (12 ops, 19 `no_effect`). The reasons, grouped, and whether they are honest:

| Group | Provisions | Reason given | Honest? |
|---|---|---|---|
| Cover errors | cover/para3 | E1 and E2 declared as conflicts | Yes, and right |
| Clause list not parsed | 2.1 | C22 refuses `set_status` on 6.7, quoting the parser's citation list | Yes: it names the tool's own limit. Not said: the 6.7 row stays live (false positive 1) |
| Quotation split across a clause and its list item | 3.3, 3.3(b) | C22/C21 on limb (b) | Yes; the issue says the register still reads 60/40 |
| Cover error holding an operative op | 5.1 (and 2.1's 6.6 text) | declared conflict with the cover | True, but the hold is the design's choice: the cover never governs, yet its wrong clause number blocks the right change |
| Missing evidence | 5.2, Q18 | ESIA Figure 7-2 not in the pack | Yes; right for Q18. 5.2's annotation could stand with the value unknown |
| No op type for what a new unit carries | 7.2, AppB/para1, 7.3, 7.4 | no op records precedence between two units issued together; C22, no target at ADD-02 | Yes |
| The image reading not yet approved, or Arabic against English | p4-image/table-header, row-a, row-b, note1, note2, note3, stamp; T5-1/a, T5-1/b, note(1), note(2), note(3) (12) | reading pending; declared conflict with the English | Yes; by design nothing rests on an unapproved reading. The stamp is over-cautious (an empty outline prints nothing) |

No reason hides a failure, and none claims a check that did not run. The decisions now with a person: D1 (Commercial lead: which price basis; the clarification route is closed); approve or correct the Arabic reading (it gates 12 units); the datum (I-ADD03-T51-DATUM); obtain ESIA Figure 7-2 from the data room; write the 6.7 deletion and the full 29.2 replacement by hand; create rows and milestones for 7.3 (Mon 23 Nov) and the modification cut-off (Tue 24 Nov); confirm the two cover errors.

## 4. Manual interventions

**None.** `checkpoint.json` `interventions` has 15 entries, all "host session (automatic)": one image reading, nine analysis batches, five downstream batches (`pkt` L1104–1120). Every batch ran once (attempts 1, no failure class); one downstream answer was re-asked once for a schema problem (`pkt` L1085); the critic's 14 requests changed no status. The host route meters no usage (`pkt` L8: "0 call(s) … cost not computed").

## 5. Review effort

What a person must look at before anything is accepted:

| Item | Count | By status |
|---|---|---|
| Image reading ADD-03-p4-r1 | 1 (24 Arabic blocks; 18 units touched) | pending |
| Analysis items (`P`) | 57, over 54 provisions | evidence_verified 14, interpretation_pending 18, conflicting 13, insufficient_evidence 8, escalated 4 (29 dispositions, 18 ops, 8 escalations, 1 clarification, 1 issue) |
| Statements behind them | 74 | 44 facts, 26 interpretations, 4 assumptions |
| Downstream items (`DS`) | 60 | interpretation_pending 32, escalated 15, conflicting 11, insufficient_evidence 1, evidence_verified 1 (24 escalations, 13 row readings, 8 no_change, 7 activities, 4 issues, 2 clarification items, 2 new rows) |
| Promoted into the candidate | 64 | 12 ops, 19 dispositions, 2 new rows, 12 readings, 3 issues, 7 activities, 1 clarification, 8 no_change; all PROPOSED |
| Unresolved provisions a person writes | 23 | 8 of them also escalations |
| Critic opinions | 58 reviewed (43 analysis, 15 downstream) | 52 agree, 6 do not (4 analysis, 2 downstream) |
| Approved | 0 | |

The candidate's batch review packet over the whole register (`out-candidate/review/items.json`) holds 265 items (207 rows, 49 ops, 6 proposals, 3 readings): 256 proposed, 3 applied, 3 superseded, 2 approved, 1 pending.

**Estimate (untested):** about four hours (three to five) before any legal or commercial call: the reading beside its crops (about 20 minutes); 117 proposal items, of which about 40 conflicting or escalated need several minutes each; then the 23 unresolved provisions, where 12 collapse into about three decisions once the reading is approved and the rest need ops or rows written by hand (6.7, 29.2, 7.3, 7.4, 5.1).

## Timing against the brief's 30 minutes

| Step | Start (UTC) | Seconds |
|---|---|---|
| ingest (refused once for the unread image region, then re-run inside readings) | 02:54:44 | 17.9 |
| readings: one host session read the page-4 image (197.6 s) | 02:55:02 | 209.3 |
| analysis: 9 host sessions of 112–358 s, one after another, each with a critic request | 02:58:31 | 2,675.7 |
| validation | 03:43:07 | 3.4 |
| downstream: 5 host sessions of 77–438 s | 03:43:10 | 1,260.1 |
| downstream validation | 04:04:11 | 0.8 |
| critic on the downstream items (5 requests) | 04:04:11 | 66.4 |
| promotion, pin, check-register (exit 1: one quote finding on ADD-03-7.1-01) | 04:05:18 | 21.3 |
| outputs (exit 0; 101 files with the banner) | 04:05:39 | 85.6 |
| diff, review | 04:07:05 | 4.7 |
| **Total of the steps** | | **4,345.1 (72.4 min)** |
| **Clock, PDF to candidate outputs and review packet** (`clock.txt`) | 02:54:44 → 04:07:11 | **72 min 27 s**, no interruption |

**Against the 30-minute target: missed by 42 min 27 s.** The host sessions (reading, analysis, downstream, critic) took 4,211.6 s (70.2 min, 97 %); every deterministic step together took 133.6 s (2.2 min). Unlike blind-04 (45:35, two analysis batches and the whole downstream phase lost to rate limits), every session here answered on the first attempt, so the time is the cost of running fifteen sessions one after another.

## Follow-ups (what each missed or partial finding would have needed, stated generally)

1. **Clause lists in a citation**: "Clauses 6.6 and 6.7 are deleted" must yield both clauses, so a deletion passes C22 and every row citing a deleted clause is marked not settled (2.1, S1, IE7, DD4, false positive 1).
2. **One quotation, one op**: a quoted replacement that ingest splits into a clause and its list items must be applicable as a single replacement (3.3, S3).
3. **The cover never holds an operative op**: a conflict between the cover and a provision should be reported on the cover only (2.1, 5.1, S1, S4).
4. **The cover check must find its sentence**: C28 should match "This Addendum <any verb>" and report an unknown verb instead of "no summary" ("consolidates" here, "relaxes" in blind-04), and compare scope words in the cover against a governing-language text (E3).
5. **Ops for what a new unit carries**: a downstream `row_new` task for obligations that attach to a unit the same addendum inserts (7.3, 7.4), and a record of precedence between two renderings issued together (7.2, Appendix B).
6. **Image tables into the register**: propose the row parameters (zones, heights, datum, scope, notices) from a pending reading, conditional on its approval, instead of leaving every cell unresolved (7.1, S7, DD10).
7. **Computed dates into A5**: a deadline the analysis calculated becomes a milestone proposal (conditional where the obligation is), "N days before X" has one reading, and the Working Days left from issue to the PDD are stated (S1, S2, S6, DD3–DD5, DD8).
8. **Conditional clauses switched on**: when an op makes another clause's condition always true (a mandatory membrane step and VOL-II 3.2), traversal should flag that clause's rows, and an earlier answer listed in A2 should be read against the new text (S5, IE3).
9. **Derived consequences on A3**: an elected value outside a stated band read with an existing non-responsiveness rule (10.5), and a price-basis conflict read with 11.5 and the Form 4-F confirmation (IE2, D1, A3 delta).
10. **Confirmations are not changes**: a `confirms` or `interprets` annotation, or a re-reading whose words are unchanged, must not mark CHANGED or REWORK (false signal 2; blind-04 follow-up 6).
11. **"Not reached" must count unresolved provisions' citations** (false signal 4, ME1, ME2).
12. **A closed clarification route is said everywhere**: when the addendum issues after the cut-off, every escalation and the A3 unresolved list should say so (1.3, IE6).
13. **Issue ids in notes are checked** against the promoted issues (false signal 6); the quote check should accept the inserting provision's page for an inserted unit (check-register's one finding).
14. **Time**: bounded parallel analysis and downstream sessions (and the critic alongside) are the only route to 30 minutes on the host route; the deterministic steps already take about two minutes.

## After the key (labelled; not scored)

Opened after the freeze. One general fix was made in the main tree at 04:26 UTC on 5 Oct, with a failing test first
(`tests/test_session11_blind05_postkey_fixes.py`): the citation parser did not read the plural list "Volume I Clauses
6.6 and 6.7" (it matched nothing for "Clauses", so the sentence's only citation was the later "single Clause 6.6"), which
is why clause 6.7 was never a target and row VOL-I-6.7-01 stayed in the candidate unflagged (false positive 1). It now
cites every clause listed ("Clauses N and M", "Clauses N, M and K"; a range "Clauses N to M" cites its two ends). The
frozen outputs above are unchanged; the candidate was not re-run. The other follow-ups (the confirming-vs-changing
signal in the candidate's replan deltas, the planning of computed dates, the image-read Table 5-1 waiting on a person,
the indirect effect on VOL-II 3.2) are recorded as follow-ups, not fixed here.

