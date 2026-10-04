# Review packet: ADD-03, AI workflow run ADD-03-run-host-blind03-20261004T143235Z

> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted.** Statuses are the controller's; a person decides every item. The real `curation/`, `config/` and `out/` were only read: everything below lives in this run's folder.

- PDF: `/home/user/tender-pack-reader/rehearsals/blind-03/input/ADD-03_Addendum_No_3.pdf` (sha256 ecdf3e24b35faca2…, 4 pages); preceding state: pack `/home/user/tender-pack-reader/config/pack.yaml` (NUPA-ISTP-2026-014), previous evidence build `/home/user/tender-pack-reader/build`
- route **host**; model requested `claude-code headless (the CLI's default model; recorded from the CLI output)`, reported `None`; host sessions report: claude-sonnet-5-5
- status **partial**: 13 provision(s) unresolved in the candidate (listed first in the review packet)
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed

## What is candidate and what is real

- **Candidate** (proposed by this run, nothing accepted): `../candidate/` — a copy of the curation and configuration with ADD-03 added, its evidence build, its op file, rows, issues, templates and outputs.
- **Last validated state**: `../candidate/out-before/` (the pre-addendum outputs built from the copied curation and the previous evidence build; done)
- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged and used read-only.

- real inputs changed since the run started: none

## Candidate outputs

Exit 0 (WORKING DRAFT (not releasable)); every file carries the banner (`../candidate/out/CANDIDATE.md`); A1 has a candidate status column {'proposed (existing row; not changed by this run; not reviewed)': 175, 'UNRESOLVED': 30}.

| Output | Candidate | Before (ADD-03 not applied) |
|---|---|---|
| A1 register | [../candidate/out/a1/a1.xlsx](../candidate/out/a1/a1.xlsx) | [../candidate/out-before/a1/a1.xlsx](../candidate/out-before/a1/a1.xlsx) |
| A2 changes | [../candidate/out/a2/a2.md](../candidate/out/a2/a2.md) | [../candidate/out-before/a2/a2.md](../candidate/out-before/a2/a2.md) |
| A3 consequences | [../candidate/out/a3/a3.pdf](../candidate/out/a3/a3.pdf) | [../candidate/out-before/a3/a3.pdf](../candidate/out-before/a3/a3.pdf) |
| A4 clarification register | [../candidate/out/a4/clarification_register.md](../candidate/out/a4/clarification_register.md) | [../candidate/out-before/a4/clarification_register.md](../candidate/out-before/a4/clarification_register.md) |
| A5 programme | [../candidate/out/a5/README.md](../candidate/out/a5/README.md) | [../candidate/out-before/a5/README.md](../candidate/out-before/a5/README.md) |
| A5 Gantt | [../candidate/out/a5/gantt.html](../candidate/out/a5/gantt.html) | [../candidate/out-before/a5/gantt.html](../candidate/out-before/a5/gantt.html) |
| A5 marshalling | [../candidate/out/a5/marshalling.csv](../candidate/out/a5/marshalling.csv) | [../candidate/out-before/a5/marshalling.csv](../candidate/out-before/a5/marshalling.csv) |
| Checks | [../candidate/out/checks.json](../candidate/out/checks.json) | [../candidate/out-before/checks.json](../candidate/out-before/checks.json) |

- before → after: {"a1": {"rows_before": 205, "rows_after": 205, "new": 0, "gone": 0}, "a3": {"before": 17, "after": 17, "enters": 0, "leaves": 0}, "a5": {"activities_before": 43, "activities_after": 43, "new": 0, "gone": 0}}

- ADD-03 is **PARTIAL** in the candidate (provisions unresolved): A3 and the A5 programme show the validated state (ADD-02); ADD-03 as proposed is in A1's `Status after ADD-03` column, in A2, in `a5/working/ADD-03.json` and in the diff below.

## Timings (wall clock per step)

| Step | Seconds | Status |
|---|---|---|
| ingest | 17.1 | done |
| analysis | 337.8 | done |
| validation | 2.9 | done |
| downstream | 280.8 | done |
| downstream_validation | 0.4 | done |
| promotion | 1.7 | done |
| pin | 1.3 | done |
| check_register | 4.0 | done |
| outputs | 111.8 | done |
| diff | 2.4 | done |
| review | 0.5 | running |
| **total** | **760.7** (12.7 min) | target 30 min from the PDF to candidate outputs and this packet, human review excluded |

## First: unresolved provisions and escalations

13 of 35 provisions are not answered by a promoted item (each is `unresolved` in the candidate op file with the reason); 2 escalation(s).

- **ESCALATED ADD-03/4.1** (ADD-03:4.1): 4.1 deletes the fourth declaration and 4.2 substitutes a new one. The engine's replace_text requires the old and new words in the same provision (C21); here they are in separate provisions, and the target is an image reading (page 6). I looked at the crop: declaration 4 is the Arabic sentence endin…
  - unsupported: A deletion in 4.1 paired with a substitution in 4.2 on an image-read declaration cannot be expressed as one valid op; a person must decide the op form. Also open: how 'استبعاد العرض' maps to the pack's rejection/non-responsive categories.
  - evidence: ADD-03:4.1 p1: “the fourth numbered declaration, which as issued reads as follows, is deleted: رابعاً: أن جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة، وندرك أن أي بيان غي…”; VOL-IV:F4-C/image/decl4 p6: “رابعاً: أن جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة، وندرك أن أي بيان غير صحيح يؤدي إلى استبعاد العرض.”
  - affected scope: units VOL-IV:F4-C/image, VOL-IV:F4-C/image/decl1, VOL-IV:F4-C/image/decl2, VOL-IV:F4-C/image/decl3, VOL-IV:F4-C/image/decl4, VOL-IV:F4-C/image/decl5, VOL-IV:F4-C/image/field-capacity-ar, VOL-IV:F4-C/image/field-capacity-en, VOL-IV:F4-C/image/field-cr-ar, VOL-IV:F4-C/image/field-cr-en, VOL-IV:F4-C/image/field-date-ar, VOL-IV:F4-C/image/field-date-en; rows VOL-I-9.4-01, VOL-IV-F4C-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-04, VOL-IV-F4C-05, VOL-IV-F4C-N1; activities form-4c-prep, form-4c-sign; clarifications CQ-F4C-EXCLUSION
- **ESCALATED ADD-03/4.2** (ADD-03:4.2): 4.2 substitutes the fourth declaration (adds a 3-working-day Portal notification undertaking and a breach-leads-to-exclusion limb). Pairs with 4.1; a dry-run replace_text citing the old words failed C21 because the old words are not in 4.2, and citing the new words in 4.1 failed likewise.
  - unsupported: Replacement of an image-read declaration with new text printed in a separate provision; a person must write the op. Note the English '3 days' in 4.3 vs Arabic 'ثلاثة أيام عمل' (three working days) in 4.2.
  - evidence: ADD-03:4.2 p2: “The following fourth declaration is substituted: رابعاً: أن جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة، ونتعهد بإخطار الهيئة عبر البوابة خلال ثلاثة أيام …”; VOL-IV:F4-C/image/decl4 p6: “رابعاً: أن جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة، وندرك أن أي بيان غير صحيح يؤدي إلى استبعاد العرض.”
  - affected scope: units VOL-IV:F4-C/image, VOL-IV:F4-C/image/decl1, VOL-IV:F4-C/image/decl2, VOL-IV:F4-C/image/decl3, VOL-IV:F4-C/image/decl4, VOL-IV:F4-C/image/decl5, VOL-IV:F4-C/image/field-capacity-ar, VOL-IV:F4-C/image/field-capacity-en, VOL-IV:F4-C/image/field-cr-ar, VOL-IV:F4-C/image/field-cr-en, VOL-IV:F4-C/image/field-date-ar, VOL-IV:F4-C/image/field-date-en; rows VOL-I-9.4-01, VOL-IV-F4C-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-04, VOL-IV-F4C-05, VOL-IV-F4C-N1; activities form-4c-prep, form-4c-sign; clarifications CQ-F4C-EXCLUSION
- **UNRESOLVED ADD-03:1.2** (clause, p1): not promotable: ADD-03/1.2 insufficient_evidence (semantic: no_effect on amendment language (its words carry 'unless'), and the reason quotes none of the provision's words: insufficient evidence that it changes nothing)
- **UNRESOLVED ADD-03:3.1** (clause, p1): not promotable: ADD-03/3.1 invalid (state: the item's state differs from the set's state)
- **UNRESOLVED ADD-03:3.2** (clause, p1): not promotable: ADD-03/3.2 invalid (state: the item's state differs from the set's state)
- **UNRESOLVED ADD-03:3.3** (clause, p1): not promotable: ADD-03/3.3 invalid (state: the item's state differs from the set's state)
- **UNRESOLVED ADD-03:3.4** (clause, p1): not promotable: ADD-03/3.4 invalid (state: the item's state differs from the set's state)
- **UNRESOLVED ADD-03:4.3** (clause, p2): not promotable: ADD-03/4.3 invalid (state: the item's state differs from the set's state)
- **UNRESOLVED ADD-03:4.4** (clause, p2): not promotable: ADD-03/4.4 invalid (state: the item's state differs from the set's state)
- **UNRESOLVED ADD-03:5.1** (clause, p2): not promotable: ADD-03/5.1 insufficient_evidence (evidence VOL-II:T2-4/TP p3: the words are not verbatim in VOL-II:T2-4/TP cell Limit at ADD-02: 'Parameter: Total Phosphorus (TP) | Unit: mg/l | Limit: 1 | Basis of assessment: 30-day roll…)
- **UNRESOLVED ADD-03:5.2** (clause, p2): not promotable: ADD-03/5.2 insufficient_evidence (missing_information: the proposer declares missing: a unit-level target in Volume II Section 3)
- **UNRESOLVED ADD-03:6.2** (clause, p2): not promotable: ADD-03/6.2(a) invalid (previous_value: 'active' does not match VOL-V:31.4 at ADD-02 (it reads: 'Persistent breach, being three (3) or more Unavailability Events in any rolling ninety (90) day period…); ADD-03/6.2(b) invalid (previous_value: 'active' does not match VOL-V:39.3 at ADD-02 (it reads: 'The Authority may terminate for persistent breach in the circumstances described in Clause 31.4.'))
- **UNRESOLVED ADD-03:7.1** (clause, p2): not promotable: ADD-03/7.1 invalid (previous_value: no target to compare the previous value 'FORM 4-G (9 units, six undertakings, Bidder signature only)' with)

## Per provision: source evidence → proposed transition → validation → downstream impact → output difference

### ADD-03:cover/para1 (paragraph, p1) — answered
- source: “Issued 1 November 2026”
- transition: `ADD-03/cover/para1` disposition no_effect: Issue date line only; prints no change and no obligation.
  - validation: **evidence_verified**

### ADD-03:cover/para2 (paragraph, p1) — answered
- source: “Tender NUPA/ISTP/2026/014”
- transition: `ADD-03/cover/para2` disposition no_effect: Cover title/tender reference only; prints no change and no obligation.
  - validation: **evidence_verified**

### ADD-03:cover/para3 (paragraph, p1) — answered
- source: “This Addendum amends the definition of Working Day and notifies a closure of the Authority's offices, requires the proposed O&M Operator to be a member of the Bidder, replaces the fourth declaration in Form 4-C, amends Volume II Table 2-4, deletes Volume V Clause 31.4, reissues Form 4-G, and responds to clarification requests 15 to 19. The closure of the Au…”
- transition: `ADD-03/cover/para3` disposition unresolved: Summary paragraph; the changes it lists are made by the numbered sections (other batches and 2.1/2.2). Two points need a person: (1) 'The closure of the Author…
  - validation: **interpretation_pending**

### ADD-03:1.1 (clause, p1) — answered
- source: “This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.”
- transition: `ADD-03/1.1` disposition no_effect: Recital stating the legal basis and ranking; it edits no text. The words 'takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2' ap…
  - validation: **evidence_verified**

### ADD-03:1.2 (clause, p1) — UNRESOLVED
- source: “A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.”
- transition: `ADD-03/1.2` disposition no_effect: Interpretive rule on how this Addendum's references are read (as amended by Addenda 1 and 2); it edits no text. Words that qualify: 'unless otherwise stated'. …
  - validation: **insufficient_evidence** — semantic: no_effect on amendment language (its words carry 'unless'), and the reason quotes none of the provision's words: insufficient evidence that it changes nothing
  - downstream proposal `ESC-ADD-03-1.2` escalation (esc:ADD-03:1.2): **escalated**

### ADD-03:2.1 (clause, p1) — answered
- source: “In Volume I Clause 2.4, ‘other than a day declared a public holiday in the Kingdom’ is deleted and ‘other than a day declared a public holiday in the Kingdom or a day notified by the Authority in an Addendum as a day on which its offices are closed’ is substituted. The second sentence of Clause 2.4 is unchanged.”
- transition: `ADD-03/2.1` amendment_op replace_text VOL-I:2.4 “other than a day declared a public holiday in the Kingdom” → “other than a day declared a public holiday in the Kingdom or a day notified by …”
  - validation: **evidence_verified**
  - downstream: units changed VOL-I:2.4; rows citing them none

### ADD-03:2.2 (clause, p1) — answered
- source: “The Authority's offices will be closed on Sunday 22 November 2026. That day is notified for the purposes of Volume I Clause 2.4 as amended by Section 2.1. The Portal will remain available on that day.”
- transition: `ADD-03/2.2` amendment_op annotate VOL-I:2.4 effect non_working_day
  - validation: **evidence_verified**

### ADD-03:3.1 (clause, p1) — UNRESOLVED
- source: “Volume I Clause 8.8 is amended by adding at the end: ‘The proposed O&M Operator shall be a member of the Bidder and shall hold, from Financial Close until the second anniversary of PCOD, not less than ten per cent (10%) of the shares in the Project Company.’”
- transition: `ADD-03/3.1` amendment_op append_text VOL-I:8.8 “” → “The proposed O&M Operator shall be a member of the Bidder and shall hold, from …”
  - validation: **invalid** — state: the item's state differs from the set's state

### ADD-03:3.2 (clause, p1) — UNRESOLVED
- source: “A Bidder whose proposed O&M Operator is not a member of the Bidder shall apply through the Portal for the Authority's consent under Volume I Clause 8.1 to the admission of the O&M Operator as a member, not later than four (4) Working Days before the Proposal Due Date.”
- transition: `ADD-03/3.2` amendment_op annotate VOL-I:8.1 effect adds_obligation
  - validation: **invalid** — state: the item's state differs from the set's state

### ADD-03:3.3 (clause, p1) — UNRESOLVED
- source: “A Bidder that intends to apply under Section 3.2 shall notify the Authority of that intention through the Portal within five (5) Working Days of the date of this Addendum.”
- transition: `ADD-03/3.3` amendment_op annotate ADD-03:3.3 effect adds_obligation
  - validation: **invalid** — state: the item's state differs from the set's state

### ADD-03:3.4 (clause, p1) — UNRESOLVED
- source: “If, at any time before the Preferred Bidder Notification, the proposed O&M Operator ceases to be a member of the Bidder, the Bidder shall notify the Authority through the Portal within two (2) Working Days of that event. Volume I Clause 8.1 applies.”
- transition: `ADD-03/3.4` amendment_op annotate VOL-I:8.1 effect adds_obligation
  - validation: **invalid** — state: the item's state differs from the set's state

### ADD-03:4.1 (clause, p1) — UNRESOLVED
- source: “In Form 4-C, the fourth numbered declaration, which as issued reads as follows, is deleted: رابعاً: أن جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة، وندرك أن أي بيان غير صحيح يؤدي إلى استبعاد العرض.”
- transition: `ADD-03/4.1` escalation why: 4.1 deletes the fourth declaration and 4.2 substitutes a new one. The engine's replace_text requires the old and new words in the same provision (C21); here they are in separate provisions, and the t…
  - validation: **invalid** — state: the item's state differs from the set's state
  - downstream proposal `ESC-ADD-03-4.1` escalation (esc:ADD-03:4.1): **escalated**

### ADD-03:4.2 (clause, p2) — UNRESOLVED
- source: “The following fourth declaration is substituted: رابعاً: أن جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة، ونتعهد بإخطار الهيئة عبر البوابة خلال ثلاثة أيام عمل من تاريخ علمنا بأي تغيير يطرأ على أي من تلك المعلومات قبل صدور إشعار مقدم العرض المفضل، وندرك أن أي بيان غير صحيح أو أي إخلال بهذا التعهد يؤدي إلى استبعاد العرض.”
- transition: `ADD-03/4.2` escalation why: 4.2 substitutes the fourth declaration (adds a 3-working-day Portal notification undertaking and a breach-leads-to-exclusion limb). Pairs with 4.1; a dry-run replace_text citing the old words failed …
  - validation: **invalid** — state: the item's state differs from the set's state
  - downstream proposal `ESC-CQ-F4C-EXCLUSION` escalation (clar:CQ-F4C-EXCLUSION): **escalated**
  - downstream proposal `ESC-form-4c-sign` escalation (act:form-4c-sign): **escalated**
  - downstream proposal `ESC-ADD-03-4.2` escalation (esc:ADD-03:4.2): **escalated**

### ADD-03:4.3 (clause, p2) — UNRESOLVED
- source: “An English translation of the substituted declaration is given below for convenience only. The Arabic text governs, in accordance with Volume I Clause 9.4. ‘Fourth: that all the information provided in this Proposal is correct and complete; that we undertake to notify the Authority through the Portal within three (3) days of the date on which we become awar…”
- transition: `ADD-03/4.3` disposition no_effect: Convenience translation only: 'is given below for convenience only. The Arabic text governs, in accordance with Volume I Clause 9.4.' This restates VOL-I:9.4 '…
  - validation: **invalid** — state: the item's state differs from the set's state

### ADD-03:4.4 (clause, p2) — UNRESOLVED
- source: “Each member of the Bidder shall give the fourth declaration as substituted. A Form 4-C that contains the fourth declaration as issued is not a properly executed Form 4-C for the purposes of Volume I Clause 9.4.”
- transition: `ADD-03/4.4` amendment_op annotate VOL-I:9.4, VOL-IV:F4-C effect adds_obligation
  - validation: **invalid** — state: the item's state differs from the set's state

### ADD-03:5.1 (clause, p2) — UNRESOLVED
- source: “In Volume II Table 2-4, in the row for Total Phosphorus (TP), the limit is amended from 1 mg/l to 0.5 mg/l. The unit and the basis of assessment (30-day rolling average) are unchanged. All other entries in Table 2-4, including the Total Nitrogen limit as amended by Addendum No. 2, are unchanged.”
- transition: `ADD-03/5.1` amendment_op set_value VOL-II:T2-4/TP “1” → “0.5”
  - validation: **insufficient_evidence** — evidence VOL-II:T2-4/TP p3: the words are not verbatim in VOL-II:T2-4/TP cell Limit at ADD-02: 'Parameter: Total Phosphorus (TP) | Unit: mg/l | Limit: 1 | Basis of assessment: 30-day rolling average'
  - downstream proposal `ESC-ADD-03-5.1` escalation (esc:ADD-03:5.1): **escalated**

### ADD-03:5.2 (clause, p2) — UNRESOLVED
- source: “Bidders shall reflect the amended limit in the process design submitted under Volume II Section 3.”
- transition: `ADD-03/5.2` disposition unresolved: The provision says 'Bidders shall reflect the amended limit in the process design submitted under Volume II Section 3.' It obliges bidders but prints no change…
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: a unit-level target in Volume II Section 3
  - downstream proposal `ESC-ADD-03-5.2` escalation (esc:ADD-03:5.2): **escalated**

### ADD-03:6.1 (clause, p2) — answered
- source: “In Volume V Clause 29.3, ‘ninety per cent (90%)’ is deleted and ‘eighty-five per cent (85%)’ is substituted. The duration of the Ramp-Up Period is unchanged.”
- transition: `ADD-03/6.1` amendment_op replace_text VOL-V:29.3 “ninety per cent (90%)” → “eighty-five per cent (85%)”
  - validation: **evidence_verified**
  - downstream: units changed VOL-V:29.3; rows citing them VOL-V-29.3-01
  - downstream proposal `RR-VOL-V-29.3-01` row_reading (row:VOL-V-29.3-01): **insufficient_evidence**
  - output difference: CHANGED VOL-V-29.3-01

### ADD-03:6.2 (clause, p2) — UNRESOLVED
- source: “Volume V Clause 31.4 is deleted in its entirety. Volume V Clause 39.3, which provides for termination for persistent breach in the circumstances described in Clause 31.4, is also deleted. The remaining Clauses of Volume V are not renumbered.”
- transition: `ADD-03/6.2(a)` amendment_op set_status VOL-V:31.4
  - validation: **invalid** — previous_value: 'active' does not match VOL-V:31.4 at ADD-02 (it reads: 'Persistent breach, being three (3) or more Unavailability Events in any rolling ninety (90) day period, entitles the Authority to require a remediation plan an…')
- transition: `ADD-03/6.2(b)` amendment_op set_status VOL-V:39.3
  - validation: **invalid** — previous_value: 'active' does not match VOL-V:39.3 at ADD-02 (it reads: 'The Authority may terminate for persistent breach in the circumstances described in Clause 31.4.')

### ADD-03:7.1 (clause, p2) — UNRESOLVED
- source: “Form 4-G, added to Volume IV by Section 7 of Addendum No. 2, is deleted and replaced by the reissued Form 4-G at Appendix A to this Addendum, which provides for its countersignature by the proposed O&M Operator. Bidders shall use the reissued Form.”
- transition: `ADD-03/7.1` amendment_op replace_unit ADD-02:F4-G
  - validation: **invalid** — previous_value: no target to compare the previous value 'FORM 4-G (9 units, six undertakings, Bidder signature only)' with

### ADD-03:7.2 (clause, p2) — answered
- source: “Section 7.2 of Addendum No. 2 applies to the reissued Form 4-G. A Form 4-G that is not countersigned by the proposed O&M Operator shall be treated as not submitted.”
- transition: `ADD-03/7.2` disposition unresolved: The provision says 'A Form 4-G that is not countersigned by the proposed O&M Operator shall be treated as not submitted.' This adds a responsiveness consequenc…
  - validation: **evidence_verified**

### ADD-03:Q15 (table_row, p2) — answered
- source: “No: 15 | Bidder question: Response 9 in Addendum No. 2 states that an English translation of Form 4-C may be attached for convenience. Must a translation be attached where the member is incorporated outside the Kingdom? | Authority response: Yes. The response to clarification request 9 in Addendum No. 2 is amended by adding at the end: ‘A member incorporate…”
- transition: `ADD-03/Q15` amendment_op append_text ADD-02:Q9 “” → “A member incorporated outside the Kingdom shall attach an English translation t…” effect adds_obligation
  - validation: **evidence_verified**
  - downstream: units changed ADD-02:Q9; rows citing them none
  - downstream proposal `RR-VOL-I-9.4-01` row_reading (row:VOL-I-9.4-01): **insufficient_evidence**
  - downstream proposal `RR-VOL-IV-F4C-01` row_reading (row:VOL-IV-F4C-01): **insufficient_evidence**
  - downstream proposal `RR-VOL-IV-F4C-02` row_reading (row:VOL-IV-F4C-02): **insufficient_evidence**
  - downstream proposal `RR-VOL-IV-F4C-03` row_reading (row:VOL-IV-F4C-03): **insufficient_evidence**
  - downstream proposal `RR-VOL-IV-F4C-04` row_reading (row:VOL-IV-F4C-04): **insufficient_evidence**
  - downstream proposal `RR-VOL-IV-F4C-05` row_reading (row:VOL-IV-F4C-05): **insufficient_evidence**
  - downstream proposal `RR-VOL-IV-F4C-N1` row_reading (row:VOL-IV-F4C-N1): **insufficient_evidence**
  - downstream proposal `ESC-form-4c-prep` escalation (act:form-4c-prep): **escalated**
  - output difference: A5 REWORK form-4c-prep; A5 REWORK form-4c-sign

### ADD-03:Q16 (table_row, p2) — answered
- source: “No: 16 | Bidder question: May construction water be abstracted from the local aquifer if it is treated on site before use? | Authority response: No. Volume II Clause 9.4 applies. Construction water shall be sourced from tankered supply or treated effluent and shall not be abstracted from the local aquifer, whether or not it is treated before use.”
- transition: `ADD-03/Q16` disposition no_effect: Confirms the existing clause; no change is printed. Authority response: 'Volume II Clause 9.4 applies.' VOL-II:9.4 already says 'Construction water shall not b…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'shall' (cites VOL-II:9.4))

### ADD-03:Q17 (table_row, p2) — answered
- source: “No: 17 | Bidder question: Volume I Clause 8.1 requires the Authority's prior written consent to any change in the composition of a prequalified consortium. By when must a Bidder apply for consent to admit an additional member? | Authority response: Bidders are referred to Section 3 of this Addendum. An application for consent to the admission of the propose…”
- transition: `ADD-03/Q17` disposition no_effect: Refers to Section 3 and restates its deadline; it prints no change to VOL-I:8.1. The response 'Bidders are referred to Section 3 of this Addendum' and the date…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'must' (cites VOL-I:8.1))

### ADD-03:Q18 (table_row, p3) — answered
- source: “No: 18 | Bidder question: Under Volume V Clause 31.4, does the rolling ninety (90) day period restart once the Authority has approved a remediation plan? | Authority response: Volume V Clause 31.4 is deleted by Section 6.2 of this Addendum. The question does not arise.”
- transition: `ADD-03/Q18` amendment_op set_status VOL-V:31.4
  - validation: **interpretation_pending**
  - downstream: units changed VOL-V:31.4; rows citing them VOL-V-31.4-01
  - downstream proposal `ESC-VOL-V-31.4-01` escalation (row:VOL-V-31.4-01): **escalated**
  - downstream proposal `ESC-CQ-PERSISTENT-BREACH` escalation (clar:CQ-PERSISTENT-BREACH): **escalated**
  - output difference: OUT VOL-V-31.4-01

### ADD-03:Q19 (table_row, p3) — answered
- source: “No: 19 | Bidder question: May the lead member give the declarations in Form 4-C on behalf of all members of the Bidder? | Authority response: No. Volume I Clause 9.4 requires a complete and properly executed Form 4-C for each member of the Bidder, signed and stamped by an authorised signatory of that member.”
- transition: `ADD-03/Q19` disposition no_effect: Confirms VOL-I 9.4 without change. The response says 'Volume I Clause 9.4 requires a complete and properly executed Form 4-C for each member of the Bidder', ma…
  - validation: **evidence_verified**

### ADD-03:AppA/para1 (paragraph, p4) — answered
- source: “Form 4-G is reissued below in accordance with Section 7 of this Addendum. Bidders shall use this version.”
- transition: `ADD-03/AppA/para1` amendment_op replace_unit ADD-02:F4-G
  - validation: **evidence_verified**
  - downstream: units changed ADD-02:F4-G/T1, ADD-02:F4-G/T1/1, ADD-02:F4-G/T1/2, ADD-02:F4-G/T1/3, ADD-02:F4-G/T1/4, ADD-02:F4-G/T1/5, ADD-02:F4-G/T1/6, ADD-02:F4-G/para1, ADD-02:H:F4-G, ADD-03:F4-G/T1, ADD-03:F4-G/T1/1, ADD-03:F4-G/T1/2, ADD-03:F4-G/T1/3, ADD-03:F4-G/T1/4, ADD-03:F4-G/T1/5, ADD-03:F4-G/T1/6, ADD-03:F4-G/T1/7, ADD-03:F4-G/para1, ADD-03:H:F4-G; rows citing them ADD-02-F4G-01, ADD-02-F4G-02, ADD-02-F4G-03, ADD-02-F4G-04, ADD-02-F4G-05, ADD-02-F4G-06, ADD-02-F4G-07
  - downstream proposal `ESC-F4G-01` escalation (row:ADD-02-F4G-01): **escalated**
  - downstream proposal `ESC-F4G-02` escalation (row:ADD-02-F4G-02): **escalated**
  - downstream proposal `ESC-F4G-03` escalation (row:ADD-02-F4G-03): **escalated**
  - downstream proposal `ESC-F4G-04` escalation (row:ADD-02-F4G-04): **escalated**
  - downstream proposal `ESC-F4G-05` escalation (row:ADD-02-F4G-05): **escalated**
  - downstream proposal `ESC-F4G-06` escalation (row:ADD-02-F4G-06): **escalated**
  - downstream proposal `ESC-F4G-07` escalation (row:ADD-02-F4G-07): **escalated**
  - downstream proposal `ROW-ADD-03-AppA-01` row_new (c46:ADD-03/AppA/para1): **insufficient_evidence**
  - downstream proposal `ACT-form-4g-review` activity (act:form-4g-review): **interpretation_pending**
  - downstream proposal `ACT-form-4g-sign` activity (act:form-4g-sign): **insufficient_evidence**
  - output difference: OUT ADD-02-F4G-01; OUT ADD-02-F4G-05; OUT ADD-02-F4G-06; OUT ADD-02-F4G-07; OUT ADD-02-F4G-02; OUT ADD-02-F4G-03; OUT ADD-02-F4G-04

### ADD-03:F4-G/T1/1 (table_row, p4) — answered
- source: “Item: 1 | Undertaking: The operational technology environment will be segregated from any business network in accordance with Volume II Clause 6.2. | Confirmed: Yes / No”
- transition: content of ADD-03/AppA/para1

### ADD-03:F4-G/T1/2 (table_row, p4) — answered
- source: “Item: 2 | Undertaking: An information security management system covering the operational technology environment will be implemented before commissioning. | Confirmed: Yes / No”
- transition: content of ADD-03/AppA/para1

### ADD-03:F4-G/T1/3 (table_row, p4) — answered
- source: “Item: 3 | Undertaking: A named accountable security officer will be appointed for the concession period. | Confirmed: Yes / No”
- transition: content of ADD-03/AppA/para1

### ADD-03:F4-G/T1/4 (table_row, p4) — answered
- source: “Item: 4 | Undertaking: Security incidents affecting the Facility will be notified to the Authority within twenty-four (24) hours of detection. | Confirmed: Yes / No”
- transition: content of ADD-03/AppA/para1

### ADD-03:F4-G/T1/5 (table_row, p4) — answered
- source: “Item: 5 | Undertaking: An independent penetration test of the operational technology environment will be carried out annually and the report provided to the Authority. | Confirmed: Yes / No”
- transition: content of ADD-03/AppA/para1

### ADD-03:F4-G/T1/6 (table_row, p4) — answered
- source: “Item: 6 | Undertaking: Remote access to the control system will require multi-factor authentication and will be logged. | Confirmed: Yes / No”
- transition: content of ADD-03/AppA/para1

### ADD-03:F4-G/T1/7 (table_row, p4) — answered
- source: “Item: 7 | Undertaking: Personnel with privileged or remote access to the control system will be subject to security screening approved by the Authority before access is granted. | Confirmed: Yes / No”
- transition: content of ADD-03/AppA/para1

### ADD-03:F4-G/para1 (paragraph, p4) — answered
- source: “Signed for and on behalf of the Bidder: _______________________ Name: _______________________ Date: ____________ Countersigned for and on behalf of the proposed O&M Operator: _______________________ Name: _______________________ Date: ____________”
- transition: content of ADD-03/AppA/para1

## Downstream proposals (validated in the candidate)

| Item | Type | Task | Status | First failed check, or what a person confirms |
|---|---|---|---|---|
| ESC-F4G-01 | escalation | row:ADD-02-F4G-01 | escalated | evidence: no evidence given |
| ESC-F4G-02 | escalation | row:ADD-02-F4G-02 | escalated | evidence: no evidence given |
| ESC-F4G-03 | escalation | row:ADD-02-F4G-03 | escalated | evidence: no evidence given |
| ESC-F4G-04 | escalation | row:ADD-02-F4G-04 | escalated | evidence: no evidence given |
| ESC-F4G-05 | escalation | row:ADD-02-F4G-05 | escalated | evidence: no evidence given |
| ESC-F4G-06 | escalation | row:ADD-02-F4G-06 | escalated | evidence: no evidence given |
| ESC-F4G-07 | escalation | row:ADD-02-F4G-07 | escalated | evidence: no evidence given |
| RR-VOL-I-9.4-01 | row_reading | row:VOL-I-9.4-01 | insufficient_evidence | statements: unknown statement Fact: Q15 adds a translation obligation for members incorporated outside the Kingdom. |
| RR-VOL-IV-F4C-01 | row_reading | row:VOL-IV-F4C-01 | insufficient_evidence | statements: unknown statement Fact: declaration text unchanged. |
| RR-VOL-IV-F4C-02 | row_reading | row:VOL-IV-F4C-02 | insufficient_evidence | statements: unknown statement Fact: declaration text unchanged. |
| RR-VOL-IV-F4C-03 | row_reading | row:VOL-IV-F4C-03 | insufficient_evidence | statements: unknown statement Fact: declaration text unchanged. |
| RR-VOL-IV-F4C-04 | row_reading | row:VOL-IV-F4C-04 | insufficient_evidence | statements: unknown statement Fact: declaration text unchanged. |
| RR-VOL-IV-F4C-05 | row_reading | row:VOL-IV-F4C-05 | insufficient_evidence | statements: unknown statement Fact: declaration text unchanged. |
| RR-VOL-IV-F4C-N1 | row_reading | row:VOL-IV-F4C-N1 | insufficient_evidence | statements: unknown statement Fact: Q15 adds a translation requirement for foreign-incorporated members. |
| RR-VOL-V-29.3-01 | row_reading | row:VOL-V-29.3-01 | insufficient_evidence | statements: unknown statement Fact: VOL-V 29.3 now reads 85%. |
| ESC-VOL-V-31.4-01 | escalation | row:VOL-V-31.4-01 | escalated | evidence: no evidence given |
| ROW-ADD-03-AppA-01 | row_new | c46:ADD-03/AppA/para1 | insufficient_evidence | missing_information: the proposer declares missing: ADD-03 Section 7.1 wording not checked against the reissued form |
| ESC-CQ-F4C-EXCLUSION | escalation | clar:CQ-F4C-EXCLUSION | escalated | missing_information: the proposer declares missing: Applied effective text of Form 4-C declaration 4 after ADD-03 4.1/4.2 |
| ESC-CQ-PERSISTENT-BREACH | escalation | clar:CQ-PERSISTENT-BREACH | escalated | missing_information: the proposer declares missing: ADD-03 Section 6.2 text |
| ACT-form-4g-review | activity | act:form-4g-review | interpretation_pending | the duration is a PROVISIONAL ASSUMPTION (a person confirms it) |
| ACT-form-4g-sign | activity | act:form-4g-sign | insufficient_evidence | missing_information: the proposer declares missing: Whether the countersignatory needs its own PoA (not stated) |
| ESC-form-4c-prep | escalation | act:form-4c-prep | escalated | missing_information: the proposer declares missing: row for the Q15 translation obligation |
| ESC-form-4c-sign | escalation | act:form-4c-sign | escalated | missing_information: the proposer declares missing: applied Form 4-C declaration 4 |
| ESC-ADD-03-1.2 | escalation | esc:ADD-03:1.2 | escalated |  |
| ESC-ADD-03-4.1 | escalation | esc:ADD-03:4.1 | escalated | missing_information: the proposer declares missing: applied declaration 4 text |
| ESC-ADD-03-4.2 | escalation | esc:ADD-03:4.2 | escalated | missing_information: the proposer declares missing: applied declaration 4 text; meaning of exclusion |
| ESC-ADD-03-5.1 | escalation | esc:ADD-03:5.1 | escalated | missing_information: the proposer declares missing: applied cell change to VOL-II:T2-4/TP |
| ESC-ADD-03-5.2 | escalation | esc:ADD-03:5.2 | escalated | missing_information: the proposer declares missing: unit-level target in Volume II Section 3; applied TP limit (5.1) |

## Promoted into the candidate (PROPOSED; nothing accepted)

- ops: ADD-03/2.1, ADD-03/2.2, ADD-03/6.1, ADD-03/Q15, ADD-03/Q18, ADD-03/AppA/para1
- dispositions: ADD-03:cover/para1: no_effect, ADD-03:cover/para2: no_effect, ADD-03:1.1: no_effect, ADD-03:Q16: no_effect, ADD-03:Q17: no_effect, ADD-03:Q19: no_effect
- activities: form-4g-review
- unresolved provisions: 13

## check-register on the candidate

- exit 1; 1 finding(s) {'C46': 1}
  - [C46] ADD-03/AppA/para1: [A1] ADD-03/AppA/para1 (replace_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Form 4-G is reissued below in accordance with Section 7 of this Addendum. Bidders shall…

## Coverage

- provisions: 35; accounted for by the combined set: 25; states {'validated': 35}
- resolution (controller): resolved 17, pending 8, invalid 10, unaccounted 0; approved 0
- structural units of ADD-03 that are not provisions (listed so nothing is dropped): ADD-03:H:cover (heading), ADD-03:H:cover-2 (heading), ADD-03:H:S1 (heading), ADD-03:H:S2 (heading), ADD-03:H:S3 (heading), ADD-03:H:S4 (heading), ADD-03:H:S5 (heading), ADD-03:H:S6 (heading), ADD-03:H:S7 (heading), ADD-03:H:S8 (heading), ADD-03:S8/QA (table), ADD-03:H:AppA (heading), ADD-03:H:F4-G (heading), ADD-03:F4-G/T1 (table)
- batches: analysis-001 done, analysis-002 done, analysis-003 done, analysis-004 done, analysis-005 skipped, downstream-001 done, downstream-002 done

## Manual interventions (and automatic host sessions, named as such: not a person)

- 2026-10-04T14:34:05Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model claude-code headless (the CLI's default model; recorded from the CLI output); a headless host session over the MCP tools; not a person
- 2026-10-04T14:35:22Z: host session (automatic) — batch analysis-002 by tenderpack.ai.hostsession; host model claude-code headless (the CLI's default model; recorded from the CLI output); a headless host session over the MCP tools; not a person
- 2026-10-04T14:36:53Z: host session (automatic) — batch analysis-003 by tenderpack.ai.hostsession; host model claude-code headless (the CLI's default model; recorded from the CLI output); a headless host session over the MCP tools; not a person
- 2026-10-04T14:38:30Z: host session (automatic) — batch analysis-004 by tenderpack.ai.hostsession; host model claude-code headless (the CLI's default model; recorded from the CLI output); a headless host session over the MCP tools; not a person
- 2026-10-04T14:40:53Z: host session (automatic) — batch downstream-001 by tenderpack.ai.hostsession; host model claude-code headless (the CLI's default model; recorded from the CLI output); a headless host session; not a person
- 2026-10-04T14:43:14Z: host session (automatic) — batch downstream-002 by tenderpack.ai.hostsession; host model claude-code headless (the CLI's default model; recorded from the CLI output); a headless host session; not a person

## The diff (ADD-02 → ADD-03; [diff.md](diff.md))

## What changed from ADD-02 to ADD-03

### ADD-03: PARTIAL (issued 2026-11-01)

- ops: 6 (0 invalid); provisions: 35 (15 unresolved)
- validated state: ADD-02 — this addendum does NOT replace it until every provision is treated and every op is valid
- UNRESOLVED ADD-03:cover/para3: This Addendum amends the definition of Working Day and notifies a closure of the Authority's offices, requires the proposed O&M Operator to be a member of the B
- UNRESOLVED ADD-03:1.2: A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.
- UNRESOLVED ADD-03:3.1: Volume I Clause 8.8 is amended by adding at the end: ‘The proposed O&M Operator shall be a member of the Bidder and shall hold, from Financial Close until the s
- UNRESOLVED ADD-03:3.2: A Bidder whose proposed O&M Operator is not a member of the Bidder shall apply through the Portal for the Authority's consent under Volume I Clause 8.1 to the a
- UNRESOLVED ADD-03:3.3: A Bidder that intends to apply under Section 3.2 shall notify the Authority of that intention through the Portal within five (5) Working Days of the date of thi
- UNRESOLVED ADD-03:3.4: If, at any time before the Preferred Bidder Notification, the proposed O&M Operator ceases to be a member of the Bidder, the Bidder shall notify the Authority t
- UNRESOLVED ADD-03:4.1: In Form 4-C, the fourth numbered declaration, which as issued reads as follows, is deleted: رابعاً: أن جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة، وندرك أ
- UNRESOLVED ADD-03:4.2: The following fourth declaration is substituted: رابعاً: أن جميع المعلومات المقدمة في هذا العرض صحيحة وكاملة، ونتعهد بإخطار الهيئة عبر البوابة خلال ثلاثة أيام ع
- UNRESOLVED ADD-03:4.3: An English translation of the substituted declaration is given below for convenience only. The Arabic text governs, in accordance with Volume I Clause 9.4. ‘Fou
- UNRESOLVED ADD-03:4.4: Each member of the Bidder shall give the fourth declaration as substituted. A Form 4-C that contains the fourth declaration as issued is not a properly executed
- UNRESOLVED ADD-03:5.1: In Volume II Table 2-4, in the row for Total Phosphorus (TP), the limit is amended from 1 mg/l to 0.5 mg/l. The unit and the basis of assessment (30-day rolling
- UNRESOLVED ADD-03:5.2: Bidders shall reflect the amended limit in the process design submitted under Volume II Section 3.
- UNRESOLVED ADD-03:6.2: Volume V Clause 31.4 is deleted in its entirety. Volume V Clause 39.3, which provides for termination for persistent breach in the circumstances described in Cl
- UNRESOLVED ADD-03:7.1: Form 4-G, added to Volume IV by Section 7 of Addendum No. 2, is deleted and replaced by the reissued Form 4-G at Appendix A to this Addendum, which provides for
- UNRESOLVED ADD-03:7.2: Section 7.2 of Addendum No. 2 applies to the reissued Form 4-G. A Form 4-G that is not countersigned by the proposed O&M Operator shall be treated as not submit
- cover summary vs provisions (C28, report only): 8 finding(s)
  - not found: 'requires the proposed O&M Operator to be a member of the Bidder': no provision of ADD-03 does this
  - not found: 'replaces the fourth declaration in Form 4-C': no provision of ADD-03 does this
  - not found: 'amends Volume II Table 2-4': no provision of ADD-03 does this
  - not found: 'deletes Volume V Clause 31.4': no provision of ADD-03 does this
  - understated: 'responds to clarification requests 15 to 19', but ADD-03/Q15 adds text to ADD-02:Q9: 'Yes. The response to clarification request 9 in Addendum No. 2 is amended by adding at the end: ‘A member incorporated outside the Kingdom shall attach an English translation to its Form 4-C.’ The Arabic text of Form 4-C governs in accorda…'
  - understated: 'responds to clarification requests 15 to 19', but ADD-03/Q18 deletes VOL-V:31.4: 'Volume V Clause 31.4 is deleted by Section 6.2 of this Addendum. The question does not arise.'
  - omitted: ADD-03/6.1 amends VOL-V:29.3; the summary does not mention it: 'In Volume V Clause 29.3, ‘ninety per cent (90%)’ is deleted and ‘eighty-five per cent (85%)’ is substituted. The duration of the Ramp-Up Period is unchanged.'
  - contradicted: 'The closure of the Authority's offices does not affect any deadline under the RFP Documents', but CLARIFICATION-CUTOFF (row VOL-I-5.2-01, VOL-I 5.2) moves from 2026-11-12 to 2026-11-11

### Requirements

- new: 0; out of force: 8; changed: 2

- OUT ADD-02-F4G-01: REPLACED (by ADD-03:F4-G/T1/3)
- OUT ADD-02-F4G-05: REPLACED (by ADD-03:F4-G/T1/4)
- OUT ADD-02-F4G-06: REPLACED (by ADD-03:F4-G/T1/5)
- OUT ADD-02-F4G-07: REPLACED (by ADD-03:F4-G/T1/6)
- OUT ADD-02-F4G-02: REPLACED (by ADD-03:F4-G/T1/1)
- OUT ADD-02-F4G-03: REPLACED (by ADD-03:F4-G/T1/2)
- OUT ADD-02-F4G-04: REPLACED (by ADD-03:F4-G)
- OUT VOL-V-31.4-01: DELETED (ADD-03/Q18)
- CHANGED VOL-I-5.2-01: CLARIFICATION-CUTOFF 2026-11-12 -> 2026-11-11
- CHANGED VOL-V-29.3-01: wording (by ADD-03/6.1)

### Stale readings and decisions

- STALE VOL-I-9.4-01: ADD-02:Q9 changed since ADD-02 (by ADD-03/Q15)
- STALE VOL-IV-F4C-04: ADD-02:Q9 changed since ADD-02 (by ADD-03/Q15)
- STALE VOL-IV-F4C-N1: ADD-02:Q9 changed since ADD-02 (by ADD-03/Q15)
- STALE VOL-IV-F4C-01: ADD-02:Q9 changed since ADD-02 (by ADD-03/Q15)
- STALE VOL-IV-F4C-02: ADD-02:Q9 changed since ADD-02 (by ADD-03/Q15)
- STALE VOL-IV-F4C-03: ADD-02:Q9 changed since ADD-02 (by ADD-03/Q15)
- STALE VOL-IV-F4C-05: ADD-02:Q9 changed since ADD-02 (by ADD-03/Q15)
- STALE VOL-V-29.3-01: VOL-V:29.3 changed since ADD-02 (by ADD-03/6.1); quote not found in the effective text at ADD-03: 'During the first twelve (12) months after PCOD (the Ramp-Up ' (expected: the interpretation predates the change)

### Obligations not reaching the outputs (C46)

- ADD-03/AppA/para1 [A1]: ADD-03/AppA/para1 (replace_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Form 4-G is reissued below in accordance with Section 7 of this Addendum. Bidders shall use this version.'

### Reached through relationships (indirect: for review, not direct citations)

Curated links (relationships file) followed from what changed. The requirements above cite a changed unit; these are reached through another provision, in three classes that are never merged. A5 marks the activities that serve them REVIEW with their dates unchanged.

#### Confirmed dependency (3)
- VOL-I-10.2-01 (row; ACTIVE) <- VOL-V:29.3 via REL-PAY-MECHANISM > REL-PAY-QUOTED-PRICE [feeds_calculation; link confirmed]
- VOL-IV-F4F-01 (row; ACTIVE) <- VOL-V:29.3 via REL-PAY-MECHANISM > REL-PAY-FORM-4F [feeds_calculation; link confirmed]
- calc:availability-payment (calculation) <- VOL-V:29.3 via REL-PAY-MECHANISM [feeds_calculation; link confirmed]

#### Proposed relationship (7)
- VOL-I-10.2-01 (row; ACTIVE) <- VOL-V:31.4 via REL-PAY-DEDUCTIONS > REL-PAY-QUOTED-PRICE [feeds_calculation; link proposed]
- VOL-I-10.3-01 (row; ACTIVE) <- VOL-V:31.4 via REL-PAY-DEDUCTIONS > REL-PAY-FINANCIAL-MODEL [depends_on; link proposed]
- VOL-I-10.3-01 (row; ACTIVE) <- VOL-V:29.3 via REL-PAY-MECHANISM > REL-PAY-FINANCIAL-MODEL [depends_on; link proposed]
- VOL-IV-F4F-01 (row; ACTIVE) <- VOL-V:31.4 via REL-PAY-DEDUCTIONS > REL-PAY-FORM-4F [feeds_calculation; link proposed]
- VOL-IV-F4F-02 (row; ACTIVE) <- VOL-V:31.4 via REL-PAY-DEDUCTIONS > REL-PAY-FINANCIAL-MODEL > REL-MODEL-FORM-4F [feeds_calculation; link proposed]
- VOL-IV-F4F-02 (row; ACTIVE) <- VOL-V:29.3 via REL-PAY-MECHANISM > REL-PAY-FINANCIAL-MODEL > REL-MODEL-FORM-4F [feeds_calculation; link proposed]
- calc:availability-payment (calculation) <- VOL-V:31.4 via REL-PAY-DEDUCTIONS [depends_on; link proposed]

#### Possible impact (2)
- VOL-I-10.6-01 (row; ACTIVE) <- VOL-V:31.4 via REL-PAY-DEDUCTIONS > REL-PAY-FINANCING-ASSUMPTIONS [depends_on; link possible]
- VOL-I-10.6-01 (row; ACTIVE) <- VOL-V:29.3 via REL-PAY-MECHANISM > REL-PAY-FINANCING-ASSUMPTIONS [depends_on; link possible]

#### Referenced but not supplied: conclusions in play that cannot be established (1)
- VOL-V-31.4-01 (row; DELETED (ADD-03/Q18)) <- target changed via REL-MISSING-SCHEDULE-11-PERSISTENT-BREACH [missing_document; link proposed]; also changed directly. NOT SUPPLIED: Volume V Schedule 11 (Project Company Events of Default); cannot be established: whether persistent breach (three or more Unavailability Events in a rolling 90 days) is also an Event of Default listed in Schedule 11, giving a termination right under 39.1 independent of 31.4 and 39.3; so an amendment or deletion of 31.4 or 39.3 cannot be concluded to remove that exposure

### Disqualifiers (A3)

- no change

### Programme impact (status date 2026-10-22 -> 2026-11-01)

- MOVED bond-approval: latest start 2026-11-05 -> 2026-11-04
- MOVED bond-issue: latest start 2026-11-19 -> 2026-11-18
- REWORK clarifications: requirement changed: VOL-I-5.2-01
- MOVED clarifications: latest start 2026-11-11 -> 2026-11-10
- MOVED completion-certs: latest start 2026-11-03 -> 2026-11-02
- MOVED deviations-review: latest start 2026-11-08 -> 2026-11-05
- MOVED fin-assumptions: latest start 2026-11-22 -> 2026-11-19
- MOVED fin-model-build: latest start 2026-10-26 -> 2026-10-25
- MOVED fin-model-freeze: latest start 2026-11-16 -> 2026-11-15
- MOVED fin-standing: latest start 2026-11-19 -> 2026-11-18
- MOVED fin-statements: latest start 2026-11-12 -> 2026-11-11
- MOVED form-4a-prep: latest start 2026-11-22 -> 2026-11-19
- MOVED form-4b-prep: latest start 2026-11-18 -> 2026-11-17
- REWORK form-4c-prep: requirement changed: VOL-I-9.4-01, VOL-IV-F4C-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-04, VOL-IV-F4C-05, VOL-IV-F4C-N1
- MOVED form-4c-prep: latest start 2026-11-17 -> 2026-11-16
- REWORK form-4c-sign: requirement changed: VOL-I-9.4-01, VOL-IV-F4C-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-04, VOL-IV-F4C-05, VOL-IV-F4C-N1
- MOVED form-4c-sign: latest start 2026-11-19 -> 2026-11-18
- MOVED form-4e: latest start 2026-11-22 -> 2026-11-19
- MOVED form-4f: latest start 2026-11-22 -> 2026-11-19
- MOVED form-4g-review: latest start 2026-11-16 -> 2026-11-15
- MOVED ground-dd: latest start 2026-11-02 -> 2026-11-01
- MOVED investment-licence: latest start 2026-11-17 -> 2026-11-16
- MOVED iso-copy: latest start 2026-11-22 -> 2026-11-19
- MOVED lcc-certificate: latest start 2026-10-13 -> 2026-10-12
- MOVED lcc-ratio: latest start 2026-10-06 -> 2026-10-05
- MOVED lender-terms: latest start 2026-11-02 -> 2026-11-01
- MOVED model-audit-opinion: latest start 2026-11-17 -> 2026-11-16
- MOVED model-audit-review: latest start 2026-11-03 -> 2026-11-02
- MOVED model-auditor-appoint: latest start 2026-10-27 -> 2026-10-26
- MOVED om-evidence: latest start 2026-11-10 -> 2026-11-09
- MOVED pcg-execution: latest start 2026-11-10 -> 2026-11-09
- MOVED pcg-wording: latest start 2026-10-27 -> 2026-10-26
- MOVED poa: latest start 2026-11-10 -> 2026-11-09
- MOVED poa-resolutions: latest start 2026-11-03 -> 2026-11-02
- MOVED references: latest start 2026-11-04 -> 2026-11-03
- MOVED spoc: latest start 2026-11-22 -> 2026-11-19
- MOVED technical-proposal: latest start 2026-10-27 -> 2026-10-26
- REVIEW (possible impact) fin-assumptions: VOL-I-10.6-01 reached from VOL-V:29.3, VOL-V:31.4 via REL-PAY-DEDUCTIONS, REL-PAY-FINANCING-ASSUMPTIONS, REL-PAY-MECHANISM; dates unchanged
- REVIEW (proposed relationship) fin-model-build: VOL-I-10.3-01, VOL-IV-F4F-02 reached from VOL-V:29.3, VOL-V:31.4 via REL-MODEL-FORM-4F, REL-PAY-DEDUCTIONS, REL-PAY-FINANCIAL-MODEL, REL-PAY-MECHANISM; dates unchanged
- REVIEW (proposed relationship) fin-model-freeze: VOL-I-10.3-01, VOL-IV-F4F-02 reached from VOL-V:29.3, VOL-V:31.4 via REL-MODEL-FORM-4F, REL-PAY-DEDUCTIONS, REL-PAY-FINANCIAL-MODEL, REL-PAY-MECHANISM; dates unchanged
- REVIEW (confirmed dependency) form-4f: VOL-I-10.2-01, VOL-IV-F4F-01 reached from VOL-V:29.3 via REL-PAY-FORM-4F, REL-PAY-MECHANISM, REL-PAY-QUOTED-PRICE; dates unchanged
- REVIEW (proposed relationship) form-4f: VOL-I-10.2-01, VOL-IV-F4F-01, VOL-IV-F4F-02 reached from VOL-V:29.3, VOL-V:31.4 via REL-MODEL-FORM-4F, REL-PAY-DEDUCTIONS, REL-PAY-FINANCIAL-MODEL, REL-PAY-FORM-4F, REL-PAY-MECHANISM, REL-PAY-QUOTED-PRICE; dates unchanged
- REVIEW (possible impact) lender-terms: VOL-I-10.6-01 reached from VOL-V:29.3, VOL-V:31.4 via REL-PAY-DEDUCTIONS, REL-PAY-FINANCING-ASSUMPTIONS, REL-PAY-MECHANISM; dates unchanged
- FEASIBILITY lcc-ratio: INFEASIBLE by 12 WD -> INFEASIBLE by 19 WD
- FEASIBILITY lcc-certificate: INFEASIBLE by 12 WD -> INFEASIBLE by 19 WD
- FEASIBILITY fin-model-build: OK -> INFEASIBLE by 5 WD
- FEASIBILITY model-auditor-appoint: OK -> INFEASIBLE by 4 WD
- FEASIBILITY pcg-wording: OK -> INFEASIBLE by 4 WD
- FEASIBILITY technical-proposal: OK -> INFEASIBLE by 4 WD
- FEASIBILITY model-audit-review: OK -> INFEASIBLE by 4 WD
- FEASIBILITY pcg-execution: OK -> INFEASIBLE by 4 WD
- FEASIBILITY fin-model-freeze: OK -> INFEASIBLE by 5 WD
- FEASIBILITY model-audit-opinion: OK -> INFEASIBLE by 5 WD
- FEASIBILITY fin-assumptions: OK -> INFEASIBLE by 2 WD
- FEASIBILITY form-4f: OK -> INFEASIBLE by 2 WD
- FEASIBILITY assemble-envelope-a: INFEASIBLE by 12 WD -> INFEASIBLE by 19 WD
- FEASIBILITY assemble-envelope-b: OK -> INFEASIBLE by 5 WD
- FEASIBILITY copies: INFEASIBLE by 12 WD -> INFEASIBLE by 19 WD
- FEASIBILITY seal-and-mark: INFEASIBLE by 12 WD -> INFEASIBLE by 19 WD
- FEASIBILITY deliver: INFEASIBLE by 12 WD -> INFEASIBLE by 19 WD

## Next (a person)

- read the unresolved and escalated provisions first, then each item against its evidence (`../ai/ADD-03-run-host-blind03-20261004T143235Z-combined/proposals.yaml`, `../downstream/proposals.yaml`)
- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE §3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` and decide with `accept` / `reject` as usual
