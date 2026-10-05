# Review packet: ADD-03, AI workflow run ADD-03-run-host-blind04-s11-20261004T222214Z

> **CANDIDATE: proposed by the AI workflow; not reviewed; nothing accepted.** Statuses are the controller's; a person decides every item. The real `curation/`, `config/` and `out/` were only read: everything below lives in this run's folder.

- PDF: `/home/user/tender-pack-reader/rehearsals/blind-04/input/ADD-03_Addendum_No_3.pdf` (sha256 99728136b5653acd…, 5 pages); preceding state: pack `/home/user/tender-pack-reader/config/pack.yaml` (NUPA-ISTP-2026-014), previous evidence build `/home/user/tender-pack-reader/build`
- route **host**; model requested `claude-code headless (opus)`, reported `None`; host sessions report: claude-opus-5-5
- status **partial**: 1 provision(s) unresolved in the candidate (listed first in the review packet); 17 downstream task(s) answered only by items that cannot be promoted: row:ADD-02-T1-1-N3-01, row:VOL-II-5.2-01, row:VOL-IV-F4D-01, row:VOL-IV-F4D-02, row:VOL-IV-F4D-03, row:VOL-IV-F4D-04, row:VOL-IV-F4D-05, c46:ADD-03/6.1 …; check-register on the candidate: exit 1, 12 finding(s) {'disposition': 1, 'C46': 11}; C46: [C46] ADD-03/cover/para3: [A3] ADD-03/cover/para3 brings in consequence words ['liquidated damages'] that no row's consequence carries at ADD-03: 'This Addendu…; [C46] ADD-03/6.1: [A1] ADD-03/6.1 (replace_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Table 1-1 (revised) and the Notes to…; [C46] ADD-03/8.1: [A1] ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-I:9.1; a r…
- usage: 0 call(s), 0 input / 0 output tokens; cost not computed

## Execution, completeness and approval (three separate things)

- **Execution** (what ran): ingest done, readings done, analysis done, validation done, downstream done, downstream_validation done, critic done, promotion done, pin done, check_register done, outputs done, diff done, review running; batches reading: {'done': 1}; analysis: {'done': 5, 'skipped': 5}; downstream: {'done': 5}
- **Completeness** (what the run completed): **partial**: 1 provision(s) unresolved in the candidate (listed first in the review packet); 17 downstream task(s) answered only by items that cannot be promoted: row:ADD-02-T1-1-N3-01, row:VOL-II-5.2-01, row:VOL-IV-F4D-01, row:VOL-IV-F4D-02, row:VOL-IV-F4D-03, row:VOL-IV-F4D-04, row:VOL-IV-F4D-05, c46:ADD-03/6.1 …; check-register on the candidate: exit 1, 12 finding(s) {'disposition': 1, 'C46': 11}; C46: [C46] ADD-03/cover/para3: [A3] ADD-03/cover/para3 brings in consequence words ['liquidated damages'] that no row's consequence carries at ADD-03: 'This Addendu…; [C46] ADD-03/6.1: [A1] ADD-03/6.1 (replace_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Table 1-1 (revised) and the Notes to…; [C46] ADD-03/8.1: [A1] ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-I:9.1; a r…
  - downstream tasks: 51; answered 34; unanswered 0; answered only by items that cannot be promoted 17; answered 'no change' 5
- **Human approval**: **none** (nothing approved, accepted, rejected or sent); no decision is recorded in the candidate's decisions file

## What is candidate and what is real

- **Candidate** (proposed by this run, nothing accepted): `../candidate/` — a copy of the curation and configuration with ADD-03 added, its evidence build, its op file, rows, issues, templates and outputs.
- **Last validated state**: `../candidate/out-before/` (the pre-addendum outputs built from the copied curation and the previous evidence build; done)
- **Real** (untouched): `curation/`, `config/`, `out/`; the owner's approvals and readings were copied unchanged and used read-only.

- real inputs changed since the run started: none

## Candidate outputs

Exit 0 (WORKING DRAFT (not releasable)); every file carries the banner (`../candidate/out/CANDIDATE.md`); A1 has a candidate status column {'proposed (existing row; not changed by this run; not reviewed)': 176, 'PROPOSED BY THE AI WORKFLOW': 23, 'UNRESOLVED': 9}.

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

- before → after: {"a1": {"rows_before": 205, "rows_after": 208, "new": 3, "gone": 0}, "a3": {"before": 17, "after": 17, "enters": 0, "leaves": 0}, "a5": {"activities_before": 43, "activities_after": 43, "new": 0, "gone": 0}}

- ADD-03 is **PARTIAL** in the candidate (provisions unresolved): A3 and the A5 programme show the validated state (ADD-02); ADD-03 as proposed is in A1's `Status after ADD-03` column, in A2, in the candidate A3 and A5 below, in `a5/working/ADD-03.json` and in the diff below.

### Validated and candidate A3 / A5 (partial should not mean useless)

- **Validated** (unchanged; ADD-02): [a3/a3.pdf](../candidate/out/a3/a3.pdf) (one page), [a5/README.md](../candidate/out/a5/README.md), [a5/gantt.html](../candidate/out/a5/gantt.html)
- **Candidate** (CANDIDATE — NOT VALIDATED; ADD-03 as proposed): [a3/a3_candidate.pdf](../candidate/out/a3/a3_candidate.pdf) (9 page(s)), [a3/a3_candidate.md](../candidate/out/a3/a3_candidate.md), [a5/candidate/README.md](../candidate/out/a5/candidate/README.md), [a5/candidate/gantt.html](../candidate/out/a5/candidate/gantt.html)

**What may be changing.** ADD-03 is PARTIAL: 1 of 70 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 23 op(s) that are valid there stood (each still a proposal: review proposed 23), A3 would gain 2 row(s) (ADD-03-6.2-01 (ADD-03/6.2(b), ADD-03/6.2(a)), ADD-03-cover-01 (ADD-03/cover/para3)), lose 0 (none) and change 3 (VOL-I-11.3-01 (ADD-03/6.2(a), ADD-03/S6/para1(a), ADD-03/6.2(b)), VOL-I-8.4-01 (ADD-03/3.1), VOL-IV-F4D-01 (ADD-03/Q15)); A5, replanned at ADD-03's issue date (2026-11-09), would move the latest dates of 0 activities (none), add 0 (none) and remove 0 (none), and marks 6 REVIEW through relationships. Not settled: 5 activities blocked by an unresolved row (pcg-wording, technical-proposal, pcg-execution, fin-statements and 1 more), 9 STALE row(s), 11 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 2 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 5 more; conditional or effective-dated: ADD-03:7.2 (conditional amendment, decision by 2026-11-12); ADD-03:7.2 (conditional amendment, decision by 2026-11-12); ADD-03:5.2 (effective-dated amendment, effective 2026-10-08); ADD-03:Q16 (conditional amendment, decision by 2026-11-12). Nothing here is validated, accepted or applied to the real state.

- ENTERS ADD-03-6.2-01: score (Envelope B returned unopened): “A Proposal whose technical score is less than seventy per cent (70%) of the total marks available in Table 1-1 shall not proceed to commercial evaluation”; ops ADD-03/6.2(b) (interpretation_pending), ADD-03/6.2(a) (interpretation_pending)
- ENTERS ADD-03-cover-01: gate (pass/fail gate); ops ADD-03/cover/para3 (interpretation_pending)
- CHANGES VOL-I-11.3-01: now STALE; ops ADD-03/6.2(a) (interpretation_pending), ADD-03/S6/para1(a) (interpretation_pending), ADD-03/6.2(b) (interpretation_pending)
- CHANGES VOL-I-8.4-01: now STALE; ops ADD-03/3.1 (evidence_verified)
- CHANGES VOL-IV-F4D-01: now STALE; ops ADD-03/Q15 (interpretation_pending)

- blockers: 1 unresolved provision(s), 5 blocked activit(y/ies), 9 STALE row(s), 11 C46 gap(s), 0 relationship chain(s) blocked or incomplete, 2 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT, I-VOL-III, I-VOL-II-MISSING, I-VOL-V-MISSING, I-VOL-IV-SCALE, I-OP-ADD-01/Q4
- conditional scenarios: 4; ADD-03:7.2 (conditional amendment, decision by 2026-11-12); ADD-03:7.2 (conditional amendment, decision by 2026-11-12); ADD-03:5.2 (effective-dated amendment); ADD-03:Q16 (conditional amendment, decision by 2026-11-12)

**Image-read units** (the review packet of each region shows every crop beside its reading; translations are proposals, not evidence):

- ADD-03-p4-r1 (ADD-03 p4; reading pending): [packet](../candidate/build/review/ADD-03-p4-r1/packet.html); 29 unit(s) touched
  - `ADD-03:F4-H/image`: “Form 4-H (image, Arabic with English labels): Beneficial Ownership Declaration”
  - `ADD-03:F4-H/image/hdr-en`: “NORTHERN UTILITIES PROCUREMENT AUTHORITY”
  - `ADD-03:F4-H/image/hdr-ar`: “الهيئة الشمالية للمشتريات المرفقية”; translation (apart): ‘Northern Utilities Procurement Authority’
  - `ADD-03:F4-H/image/ref-en`: “Tender Ref: NUPA/ISTP/2026/014”
  - `ADD-03:F4-H/image/ref-ar`: “مناقصة رقم: NUPA/ISTP/2026/014”; translation (apart): ‘Tender number: NUPA/ISTP/2026/014’
  - `ADD-03:F4-H/image/form-en`: “FORM 4-H”
  - `ADD-03:F4-H/image/form-ar`: “النموذج ٤-ح”; translation (apart): ‘Form 4-H (the Arabic letter ح, eighth in abjad order, is used for H)’; uncertain: numeral '٤-ح': Stored as logical ٤-ح (number first in reading order, matching FORM 4-H), which renders ح-٤ left to right. The preparer could not settle the left-to-right glyph order with confidence o…
  - `ADD-03:F4-H/image/title`: “إقرار المستفيد الحقيقي”; translation (apart): ‘Beneficial Owner Declaration’
  - `ADD-03:F4-H/image/intro`: “نحن الموقعون أدناه، بصفتنا ممثلين مفوضين عن العضو المذكور أدناه في ائتلاف مقدم العرض، نقر ونتعهد بما يلي:”; translation (apart): ‘We, the undersigned, in our capacity as authorised representatives of the member named below in the Bidder's consortium, declare and undertake the following:’
  - `ADD-03:F4-H/image/decl1`: “أولاً: أن الأشخاص الطبيعيين المبينين في الجدول أدناه هم جميع المستفيدين الحقيقيين من العضو، والمستفيد الحقيقي هو كل شخص طبيعي يملك، بصورة مباشرة أو غير مباشرة، ما نسبته عشرة في المائة (١٠٪) أو أكثر م…”; translation (apart): ‘First: that the natural persons shown in the table below are all the beneficial owners of the member; a beneficial owner is every natural person who owns, dire…’
  - `ADD-03:F4-H/image/decl2`: “ثانياً: أنه لا يملك أيٌّ من المستفيدين الحقيقيين، بصورة مباشرة أو غير مباشرة، أي حصة في عضو في ائتلاف آخر يقدم عرضاً لهذه المناقصة.”; translation (apart): ‘Second: that none of the beneficial owners owns, directly or indirectly, any share in a member of another consortium submitting a proposal for this tender.’
  - `ADD-03:F4-H/image/decl3`: “ثالثاً: أننا أرفقنا بهذا الإقرار نسخة مصدقة من سجل الشركاء أو المساهمين في العضو، صادرة خلال الثلاثين (٣٠) يوماً السابقة لتاريخ تقديم العروض.”; translation (apart): ‘Third: that we have attached to this declaration a certified copy of the register of partners or shareholders of the member, issued within the thirty (30) days…’; uncertain: 'the date of submission of proposals' is read as printed; which deadline it refers to (and whether as moved by an addendum) is for a person to decide
  - … 17 more in `a3/a3_candidate.md`
- VOL-II-p3-r1 (VOL-II p3; reading approved): [packet](../candidate/build/review/VOL-II-p3-r1/packet.html); not touched by this addendum
- VOL-IV-p6-r1 (VOL-IV p6; reading approved): [packet](../candidate/build/review/VOL-IV-p6-r1/packet.html); 4 unit(s) touched
  - `VOL-IV:F4-C/image`: “Form 4-C (image, Arabic with English labels): Conflict of Interest and Debarment Declaration”; issues I-BIDDER-FACTS
  - `VOL-IV:F4-C/image/decl2`: “ثانياً: أن الشركة لم تشارك، بصورة مباشرة أو غير مباشرة، في أكثر من عرض واحد لهذه المناقصة.”; translation (apart): ‘Second: that the company has not participated, directly or indirectly, in more than one proposal for this tender.’; issues I-BIDDER-FACTS, I-NO-CONSEQUENCE, I-READING-F4C
  - `VOL-IV:F4-C/image/decl3`: “ثالثاً: أن الشركة غير مدرجة، ولم تكن مدرجة خلال الخمس سنوات السابقة، في أي قائمة حظر صادرة عن جهة حكومية في المملكة.”; translation (apart): ‘Third: that the company is not listed, and has not been listed during the previous five years, on any debarment list issued by a government body in the Kingdom.’; issues I-BIDDER-FACTS, I-NO-CONSEQUENCE, I-READING-F4C
  - `VOL-IV:F4-C/image/note`: “ملاحظة: يجب تقديم هذا النموذج باللغة العربية عن كل عضو من أعضاء الائتلاف. عدم تقديمه كاملاً يجعل العرض غير مستجيب.”; translation (apart): ‘Note: this form must be submitted in Arabic for each member of the consortium. Failure to submit it complete renders the proposal non-responsive.’; issues I-READING-F4C

## Timings (wall clock per step)

| Step | Seconds | Status |
|---|---|---|
| ingest | 16.7 | done |
| readings | 204.8 | done |
| analysis | 1968.6 | done |
| validation | 3.9 | done |
| downstream | 1319.4 | done |
| downstream_validation | 1.2 | done |
| critic | 16.1 | done |
| promotion | 36.5 | done |
| pin | 2.5 | done |
| check_register | 7.4 | done |
| outputs | 186.3 | done |
| diff | 5.0 | done |
| review | 1.5 | running |
| **total** | **3769.9** (62.8 min) | target 30 min from the PDF to candidate outputs and this packet, human review excluded |

## Readings of the addendum's image regions (AI-proposed, PENDING HUMAN REVIEW)

Ingest first refused the candidate because these image regions had no reading (C05): ADD-03-p4-r1. Each reading below was proposed by the route of this run, checked by readings.check_reading and written into the candidate's readings; it is an interpretation of an image, never approved, and every unit made from it carries `reading.status: pending`.

- **ADD-03-p4-r1** — done; controller status **interpretation_pending**; unit `ADD-03:F4-H/image`; file `../candidate/curation/readings/ADD-03-p4-r1.yaml`
  - the reading beside its crops (the build's review packet): [../candidate/build/review/ADD-03-p4-r1/packet.html](../candidate/build/review/ADD-03-p4-r1/packet.html)
  - form reading, languages ['ar', 'en']; prepared by: AI-assisted: headless host session ADD-03-hostsession-20261004T222232Z-03e4 (claude-code headless (opus); the CLI reported claude-opus-5-5), in AI workflow run ADD-03-run-host-blind04-s11-20261004T222214Z (reading-ADD-03-p4-r1), 2026-10-04T22:25:42Z; proposed for a person's review, not approved
  - uncertainty: The beneficial-owner table (5 columns, 4 numbered rows, all data cells blank) was not detected as a ruled grid; only its header row (band 15) and the row holding ٤ (band 19) were measured as text bands. Row numbers ١, ٢, ٣ are printed in t…
  - uncertainty: Bands 22, 23, 24, 27 and 28 each hold an English label at the left and an Arabic label at the right but were not split; both labels are given as full-band lines in separate blocks.
  - uncertainty: Diacritics (tanween on أولاً, ثانياً, ثالثاً, عرضاً, يوماً, كاملاً; shadda and tanween on أيٌّ) were read on the enlarged crops; reviewer to confirm on native pixels.
  - uncertainty: Blank fill-in lines under each field label are rule bands (structure), not text.

## First: unresolved provisions and escalations

1 of 70 provisions are not answered by a promoted item (each is `unresolved` in the candidate op file with the reason); 2 escalation(s).

- **ESCALATED ADD-03/7.2(c)** (ADD-03:7.2): 7.2(c) says that, if Section 7 has effect, 'the cost of the grid connection works forms part of the Estimated Project Cost'. Estimated Project Cost is defined in VOL-V 1.3 (also being amended by ADD-03 Section 2 in another batch). 7.2 does not cite VOL-V 1.3, so the engine rejects a conditional ann…
  - unsupported: A conditional consequence for a defined term in an uncited unit (VOL-V:1.3) that also feeds other caps (e.g. VOL-V 18.4 delay LDs at 10% of EPC). A person should decide where to record it: a relationship, or a conditional row on the EPC/financial capacity rows.
  - evidence: ADD-03:7.2 p2: “(c) the cost of the grid connection works forms part of the Estimated Project Cost.”; VOL-V:1.3 p2: “Estimated Project Cost means the aggregate capital cost of the Facility as set out in the agreed Financial Model at Financial Close.”
  - affected scope: units VOL-II:1.4; rows VOL-II-1.4-01; activities technical-proposal; clarifications none
- **ESCALATED ADD-03/Q17** (ADD-03:Q17): Insufficient evidence. Q17 says the reference specific energy consumption 'is stated in Appendix C to this Addendum', but the evidence build of ADD-03 contains no Appendix C (only Appendix A, Form 4-H Arabic, and Appendix B, English translation). The value and the Energy Performance Statement forma…
  - unsupported: A reference to an appendix that is not in the evidence build: no unit to annotate or to take a value from. A person should check whether Appendix C was issued and, if not, raise a clarification with the Authority.
  - evidence: ADD-03:Q17 p3: “The reference specific energy consumption, in kWh per cubic metre of treated effluent, is stated in Appendix C to this Addendum together with the format of the…”
  - affected scope: units none; rows none; activities none; clarifications none

## Per provision: source evidence → proposed transition → validation → downstream impact → output difference

### ADD-03:cover/para1 (paragraph, p1) — answered
- source: “Issued 9 November 2026”
- transition: `ADD-03/cover/para1` disposition no_effect: Issue date line 'Issued 9 November 2026'; dates the addendum and changes no provision.
  - validation: **evidence_verified**

### ADD-03:cover/para2 (paragraph, p1) — answered
- source: “Tender NUPA/ISTP/2026/014”
- transition: `ADD-03/cover/para2` disposition no_effect: Title/tender reference 'Tender NUPA/ISTP/2026/014'; changes nothing.
  - validation: **evidence_verified**

### ADD-03:cover/para3 (paragraph, p1) — answered
- source: “This Addendum amends the definition of Estimated Project Cost, the financial capacity requirement in Volume I Clause 8.4 and the delay liquidated damages in Volume V Clause 18.1, relaxes the velocity limit for the treated effluent transmission main, amends Section 5.1 of Addendum No. 1, reissues the technical evaluation table to add a criterion for energy e…”
- transition: `ADD-03/cover/para3` amendment_op annotate ADD-03:cover/para3 effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Target is the provision itself, which is acceptable for an annotation. The ADD-02 precedent in the rationale is not in the evidence shown, but the obligation follows from the quoted words alone.
    - concern: The same paragraph also contains the Form 4-H timing statement, which conflicts with 8.3 and is handled in the separate issue item.
- transition: `ADD-03/cover/para3-issue` issue {"text": "Internal discrepancy in ADD-03 on Form 4-H timing. The cover says 'all Bidders may submit through the Portal within five Working Days after the Proposal Due Date'. Section 8.3 requires Form…
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real. The cover says all Bidders may submit Form 4-H through the Portal within 5 Working Days. Section 8.3 requires it with Envelope A and allows the later Portal submission only for a member incorporated outside the Kingdom.
    - concern: The issue text says Section 8.4 makes a late Form 4-H non-responsive. ADD-03:8.4 is listed as a dependency but is not among the units printed, so that consequence is not verified by the evidence shown.
    - concern: Planning on 8.3 as the stricter reading is a prudent recommendation, not something the text settles. The cover also says the Addendum takes precedence, and the evidence shown does not rank the cover against Section 8.3.
  - downstream proposal `DS-ADD03-09` row_new (c46:ADD-03/cover/para3): **interpretation_pending**
  - downstream proposal `DS-ADD03-10` issue (c46:ADD-03/cover/para3): **interpretation_pending**
  - downstream proposal `DS-ADD03-11` clarification_item (c46:ADD-03/cover/para3): **interpretation_pending**
  - output difference: NEW ADD-03-cover-01; A5 REWORK form-4a; A5 REWORK form-4a-prep

### ADD-03:1.1 (clause, p1) — answered
- source: “This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.”
- transition: `ADD-03/1.1` disposition no_effect: Recital: 'This Addendum is issued under Volume I Clause 5.3 and takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.' It restates…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The text reads as a recital of authority and precedence, and no amendment wording appears in it.
    - concern: The claim that it restates existing rules rests on VOL-I 5.3 and 3.2, whose text is not shown. A person should confirm against those clauses.

### ADD-03:1.2 (clause, p1) — answered
- source: “A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Addenda Nos. 1 and 2, unless otherwise stated.”
- transition: `ADD-03/1.2` disposition no_effect: A rule for reading references within this Addendum: 'A reference in this Addendum to a Clause, Table or Form is to that Clause, Table or Form as amended by Add…
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'unless')
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: It is a reading rule and amends no RFP text, so no_effect is reasonable.
    - concern: The 'unless otherwise stated' exception is real. It could displace the ADD-02 stage reading for a particular reference elsewhere in ADD-03, and the evidence shown does not let me check that. This is why the controller semantic check failed, and a person must confirm.

### ADD-03:2.1 (clause, p1) — answered
- source: “In Volume V Clause 1.3, ‘as set out in the agreed Financial Model at Financial Close’ is deleted and ‘as stated by the Bidder in Form 4-F, excluding financing costs, interest during construction and development fees’ is substituted.”
- transition: `ADD-03/2.1` amendment_op replace_text VOL-V:1.3 “as set out in the agreed Financial Model at Financial Close” → “as stated by the Bidder in Form 4-F, excluding financing costs, interest during…”
  - validation: **evidence_verified**
  - downstream: units changed VOL-V:1.3; rows citing them none
  - downstream proposal `DS-DEP-EPC-NETWORTH` dependency (act:fin-standing): **insufficient_evidence** — held back: endpoints not promotable: ['fin-standing']
  - downstream proposal `DS-ADD03-ACT-FIN-MODEL-BUILD` no_change (act:fin-model-build): **interpretation_pending**

### ADD-03:2.2 (clause, p1) — answered
- source: “The definition in Volume V Clause 1.3, as amended by Section 2.1, applies wherever the expression Estimated Project Cost is used in the RFP Documents.”
- transition: `ADD-03/2.2` amendment_op annotate VOL-V:1.3 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: VOL-V:1.3 is the right target. The provision extends the reach of the definition and does not change its words.
    - concern: The annotation note names VOL-I 8.4 as amended by ADD-03 3.1 and VOL-V 18.4 as applications of the term. Sections 2.1 and 3.1, VOL-I 8.4 and VOL-V 18.4 are not printed, so these specifics are unverified.
    - concern: The effect 'interprets' may understate this. Applying a Volume V definition across all RFP Documents could widen its scope, and a person should confirm.

### ADD-03:3.1 (clause, p1) — answered
- source: “In Volume I Clause 8.4, ‘SAR 800,000,000’ is deleted and ‘twenty-five per cent (25%) of the Estimated Project Cost’ is substituted. Limb (b) of Clause 8.4 is unchanged.”
- transition: `ADD-03/3.1` amendment_op replace_text VOL-I:8.4 “SAR 800,000,000” → “twenty-five per cent (25%) of the Estimated Project Cost”
  - validation: **evidence_verified**
  - downstream: units changed VOL-I:8.4; rows citing them VOL-I-8.4-01, VOL-I-8.4-02
  - downstream proposal `D-ADD03-0841-R` row_reading (row:VOL-I-8.4-01): **insufficient_evidence**
  - downstream proposal `D-ADD03-0841-ISSUE` issue (row:VOL-I-8.4-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The conflict depends on Form 4-F being an Envelope B document and on 8.4 being assessed at Envelope A. The item itself says VOL-I 10.1 is 'not quoted here', and the evidence shown does not support either point.
      - concern: The evidence does support that 8.4(a) is now 25% of the Estimated Project Cost, that limb (b) is unchanged, and that ADD-03 2.1 substitutes 'as stated by the Bidder in Form 4-F'. 11.3A also supports Envelope B staying unopened for Proposals that fail the technical stage.
      - concern: The statement that Envelope B is opened only for Proposals that pass technical evaluation is inferred from 11.3A. The base opening procedure is not shown.
      - concern: The ADD-03 2.1 text is only quoted in part, so the full redefinition of Estimated Project Cost cannot be checked. A person should confirm against VOL-I 10.1 and the opening procedure.
  - downstream proposal `D-ADD03-0841-CQ` clarification_item (row:VOL-I-8.4-01): **insufficient_evidence**
  - downstream proposal `D-ADD03-0842-R` row_reading (row:VOL-I-8.4-02): **interpretation_pending**
  - downstream proposal `DS-ADD03-05` issue (row:VOL-IV-F4F-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-06` clarification_item (row:VOL-IV-F4F-01): **interpretation_pending**
  - downstream proposal `DS-ACT-FIN-STATEMENTS-NOCHANGE` no_change (act:fin-statements): **interpretation_pending**
  - downstream proposal `DS-ACT-FIN-STANDING` activity (act:fin-standing): **insufficient_evidence**
  - downstream proposal `DS-ISSUE-EPC-ENVELOPE-A` issue (act:fin-standing): **interpretation_pending**
  - downstream proposal `DS-ADD03-ACT-FIN-MODEL-FREEZE` activity (act:fin-model-freeze): **insufficient_evidence**
  - output difference: CHANGED VOL-I-8.4-01; CHANGED VOL-I-8.4-02; A5 REWORK fin-standing; A5 REWORK fin-statements; A5 REVIEW (possible impact) fin-standing; A5 REVIEW (possible impact) fin-statements

### ADD-03:4.1 (clause, p1) — answered
- source: “In Volume V Clause 18.1, ‘SAR 180,000 for each day of delay’ is deleted and ‘one-twentieth of one per cent (0.05%) of the Estimated Project Cost for each day of delay’ is substituted. Volume V Clause 18.4 is unchanged.”
- transition: `ADD-03/4.1(a)` amendment_op replace_text VOL-V:18.1 “SAR 180,000 for each day of delay” → “one-twentieth of one per cent (0.05%) of the Estimated Project Cost for each da…”
  - validation: **evidence_verified**
- transition: `ADD-03/4.1(b)` amendment_op annotate VOL-V:18.4 effect confirms
  - validation: **evidence_verified**
  - downstream: units changed VOL-V:18.1; rows citing them none
  - downstream proposal `DS-ADD03-08` row_reading (row:VOL-V-12.1-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-12` row_new (c46:ADD-03/4.1(a)): **interpretation_pending**
  - downstream proposal `DS-CQ-PCOD-RELIABILITY-RUN` clarification_item (clar:CQ-PCOD-RELIABILITY-RUN): **insufficient_evidence**
  - output difference: NEW ADD-03-4.1-01

### ADD-03:5.1 (clause, p1) — answered
- source: “In Volume II Clause 5.2, ‘2.0 m/s’ is deleted and ‘1.5 m/s’ is substituted. The minimum residual head of 15 m at the delivery point is unchanged.”
- transition: `ADD-03/5.1` amendment_op replace_text VOL-II:5.2 “2.0 m/s” → “1.5 m/s”
  - validation: **evidence_verified**
  - downstream: units changed VOL-II:5.2; rows citing them VOL-II-5.2-01, VOL-II-5.2-02
  - downstream proposal `DS-ADD03-R-52-01` row_reading (row:VOL-II-5.2-01): **insufficient_evidence**
  - downstream proposal `DS-ADD03-ISSUE-DN-VEL` issue (row:VOL-II-5.2-01): **insufficient_evidence**
  - downstream proposal `DS-ADD03-R-52-02` row_reading (row:VOL-II-5.2-02): **interpretation_pending**
  - downstream proposal `DS-CQ-DWF-NOCHANGE` no_change (clar:CQ-DWF-STORM-FLOW): **interpretation_pending**
  - downstream proposal `DS-CQ-VOL-III-DRAWINGS` clarification_item (clar:CQ-VOL-III-DRAWINGS): **evidence_verified**
  - downstream proposal `DS-ACT-TECHNICAL-PROPOSAL` activity (act:technical-proposal): **insufficient_evidence**
  - output difference: CHANGED VOL-II-5.2-01; CHANGED VOL-II-5.2-02; A5 REWORK technical-proposal

### ADD-03:5.2 (clause, p1) — answered
- source: “With effect from 8 October 2026, Section 5.1 of Addendum No. 1 is amended by deleting ‘for the buried sections of the transmission main’ and substituting ‘for the buried sections of the transmission main other than the trenchless crossings required by Volume II Clause 5.4, at which ductile iron only shall be used’.”
- transition: `ADD-03/5.2` amendment_op replace_text ADD-01:5.1 “for the buried sections of the transmission main” → “for the buried sections of the transmission main other than the trenchless cros…”
  - validation: **interpretation_pending**
  - downstream: units changed ADD-01:5.1, VOL-II:5.3; rows citing them VOL-II-5.3-01, VOL-II-5.3-02
  - downstream proposal `DS-ADD03-R-53-01` row_reading (row:VOL-II-5.3-01): **insufficient_evidence**
  - downstream proposal `DS-ADD03-DEP-53-54` dependency (row:VOL-II-5.3-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-R-53-02` row_reading (row:VOL-II-5.3-02): **interpretation_pending**
  - output difference: CHANGED VOL-II-5.3-01; CHANGED VOL-II-5.3-02; A5 REWORK technical-proposal; A5 REVIEW (proposed relationship) technical-proposal

### ADD-03:6.1 (clause, p2) — answered
- source: “Table 1-1 (revised) and the Notes to it, issued by Section 3 of Addendum No. 2, are deleted and replaced by the table and Notes below, which add criterion G (energy efficiency). The marks for criteria A to F are unchanged.”
- transition: `ADD-03/6.1` amendment_op replace_unit ADD-02:T1-1-rev
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The target is right: ADD-03:6.1 names 'Table 1-1 (revised) ... issued by Section 3 of Addendum No. 2', which matches ADD-02:T1-1-rev. The replacement ADD-03:T1-1 is 'Table 1-1 (second revision)'.
    - concern: The provision deletes and replaces the table AND its Notes. The op only maps the table group to ADD-03:T1-1. The new Notes (ADD-03:S6/para1) are not part of the replacement, so the ADD-02 notes would be removed with no replacement in this op. This is a real gap that the item flags correctly and tha…
    - concern: The notes change is substantive. The old note says the threshold is 'seventy (70) marks'. The new note says 'seventy per cent (70%)'. With a total of 120 that is 84 marks, not 70. The wording 'unchanged' in the new note does not match the old note.
    - concern: The rationale's claims are not shown in the printed evidence. These are: rows A-F being 25/15/20/20/10/10, the old 65/35 weighting versus the new 70/30, and the 12-unit versus 9-unit counts. Only G=20 and total=120 are quoted, so I could not verify these.
    - concern: The unit status of ADD-03:6.1 is printed as 'not_issued'. The evidence does not explain this, and a person should check it.
  - downstream: units changed ADD-02:T1-1-rev, ADD-02:T1-1-rev/A, ADD-02:T1-1-rev/B, ADD-02:T1-1-rev/C, ADD-02:T1-1-rev/D, ADD-02:T1-1-rev/E, ADD-02:T1-1-rev/F, ADD-02:T1-1-rev/note(1), ADD-02:T1-1-rev/note(2), ADD-02:T1-1-rev/note(3), ADD-02:T1-1-rev/notes, ADD-02:T1-1-rev/total, ADD-03:T1-1, ADD-03:T1-1/A, ADD-03:T1-1/B, ADD-03:T1-1/C, ADD-03:T1-1/D, ADD-03:T1-1/E, ADD-03:T1-1/F, ADD-03:T1-1/G, ADD-03:T1-1/total; rows citing them ADD-02-T1-1-N3-01, VOL-I-T1-1-A, VOL-I-T1-1-B, VOL-I-T1-1-C, VOL-I-T1-1-D, VOL-I-T1-1-E, VOL-I-T1-1-F
  - downstream proposal `D-ADD03-N3-ESC` escalation (row:ADD-02-T1-1-N3-01): **escalated**
  - downstream proposal `D-ADD03-T11A-R` row_reading (row:VOL-I-T1-1-A): **interpretation_pending**
  - downstream proposal `D-ADD03-T11B-R` row_reading (row:VOL-I-T1-1-B): **interpretation_pending**
  - downstream proposal `D-ADD03-T11C-R` row_reading (row:VOL-I-T1-1-C): **interpretation_pending**
  - downstream proposal `D-ADD03-T11D-R` row_reading (row:VOL-I-T1-1-D): **interpretation_pending**
  - downstream proposal `D-ADD03-T11E-R` row_reading (row:VOL-I-T1-1-E): **interpretation_pending**
  - downstream proposal `D-ADD03-T11F-R` row_reading (row:VOL-I-T1-1-F): **interpretation_pending**
  - downstream proposal `DS-ADD03-13` row_new (c46:ADD-03/6.1): **insufficient_evidence**
  - downstream proposal `DS-ADD03-14` issue (c46:ADD-03/6.1): **invalid**
  - downstream proposal `DS-CQ-SCORING-METHOD` clarification_item (clar:CQ-SCORING-METHOD): **insufficient_evidence**
  - output difference: OUT ADD-02-T1-1-N3-01; CHANGED VOL-I-T1-1-B; CHANGED VOL-I-T1-1-D; CHANGED VOL-I-T1-1-A; CHANGED VOL-I-T1-1-C; CHANGED VOL-I-T1-1-E; CHANGED VOL-I-T1-1-F; A5 REWORK technical-proposal

### ADD-03:T1-1/A (table_row, p2) — answered
- source: “Ref: A | Criterion: Process design, treatment performance and compliance with Volume II | Marks: 25”
- transition: content of ADD-03/6.1

### ADD-03:T1-1/B (table_row, p2) — answered
- source: “Ref: B | Criterion: Construction methodology, programme and interface management | Marks: 15”
- transition: content of ADD-03/6.1

### ADD-03:T1-1/C (table_row, p2) — answered
- source: “Ref: C | Criterion: Operations and maintenance philosophy and lifecycle strategy | Marks: 20”
- transition: content of ADD-03/6.1

### ADD-03:T1-1/D (table_row, p2) — answered
- source: “Ref: D | Criterion: Environmental and social management | Marks: 20”
- transition: content of ADD-03/6.1

### ADD-03:T1-1/E (table_row, p2) — answered
- source: “Ref: E | Criterion: Organisation, key personnel and consortium governance | Marks: 10”
- transition: content of ADD-03/6.1

### ADD-03:T1-1/F (table_row, p2) — answered
- source: “Ref: F | Criterion: Health, safety and security of supply | Marks: 10”
- transition: content of ADD-03/6.1

### ADD-03:T1-1/G (table_row, p2) — answered
- source: “Ref: G | Criterion: Energy efficiency and specific energy consumption | Marks: 20”
- transition: content of ADD-03/6.1

### ADD-03:T1-1/total (table_row, p2) — answered
- source: “Criterion: Total | Marks: 120”
- transition: content of ADD-03/6.1

### ADD-03:S6/para1 (paragraph, p2) — answered
- source: “Notes to Table 1-1 (second revision): (1) The technical score threshold in Volume I Clause 11.3 is unchanged at seventy per cent (70%). (2) The combined score weighting stated in Volume I Clause 11.2 is amended to seventy per cent (70%) technical and thirty per cent (30%) commercial. (3) Marks are awarded on the Authority's standard five-point scale and mul…”
- transition: `ADD-03/S6/para1(a)` amendment_op annotate VOL-I:11.3 effect confirms
  - validation: **interpretation_pending**
- transition: `ADD-03/S6/para1(b)` amendment_op replace_text VOL-I:11.2 “sixty-five per cent (65%) technical and thirty-five per cent (35%) commercial” → “seventy per cent (70%) technical and thirty per cent (30%) commercial”
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The provision does not quote the old words. They come from VOL-I:11.2 at ADD-02, which prints 65/35, and they match the target.
- transition: `ADD-03/S6/para1(c)` amendment_op annotate ADD-03:T1-1 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Note (3) is a scoring rule, so an interpreting annotation fits. The 'standard five-point scale' is not defined in the evidence shown.
    - concern: Table 1-1 is not named by 7.x, but the notes are headed 'Notes to Table 1-1', so the target is reasonable.
- transition: `ADD-03/S6/para1(d)` amendment_op annotate ADD-03:T1-1/G effect adds_obligation
  - validation: **insufficient_evidence** — missing_information: the proposer declares missing: Appendix C (format of the Energy Performance Statement) was not found as a unit in this batch's evidence; C46 reports no A1 row holds this obligation.
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The words 'shall shall be included' are not in the evidence. The shown text 'shall be included in the Technical Proposal in the format at Appendix C' does support a new deliverable tied to criterion G.
    - concern: Appendix C is not in the evidence, so the format and any further requirements cannot be checked. This is already declared as missing information.
    - concern: The controller status is insufficient_evidence. A person should obtain Appendix C before relying on the item.
- transition: `ADD-03/S6/para1/issue` issue {"text": "Note (1) calls the technical threshold 'unchanged at seventy per cent (70%)'. In marks it rises from 70 out of 100 (VOL-I 11.3 at ADD-02; ADD-02 Note (1) 'unchanged at seventy (70) marks') …
  - validation: **interpretation_pending**
  - downstream: units changed VOL-I:11.2; rows citing them VOL-I-11.2-01
  - downstream proposal `D-ADD03-1102-R` row_reading (row:VOL-I-11.2-01): **interpretation_pending**
  - output difference: CHANGED VOL-I-11.2-01

### ADD-03:6.2 (clause, p2) — answered
- source: “Volume I Clause 11.3 is deleted and replaced by the following two Clauses: ‘11.3 A Proposal whose technical score is less than seventy per cent (70%) of the total marks available in Table 1-1 shall not proceed to commercial evaluation.’ ‘11.3A The Envelope B of a Proposal that does not proceed to commercial evaluation shall be retained unopened by the Autho…”
- transition: `ADD-03/6.2(a)` amendment_op replace_text VOL-I:11.3 “A Proposal scoring less than seventy (70) marks out of one hundred (100) at the…” → “A Proposal whose technical score is less than seventy per cent (70%) of the tot…”
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The old 11.3 text matches the target. The new text matches the quoted new 11.3. The Envelope B sentence moves to 11.3A.
    - concern: The threshold changes from '70 marks out of 100' to '70% of total marks available in Table 1-1'. These are equal only if Table 1-1 totals 100 marks. The evidence shown does not give that total.
- transition: `ADD-03/6.2(b)` amendment_op insert_unit VOL-I:11.3 “The Envelope B of a Proposal that does not proceed to commercial evaluation shall be retained unopened by the Authority…”
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The new text matches the quoted 11.3A. The timing change (retained, then returned after the Preferred Bidder Notification) follows from the words.
    - concern: The label 11.3A is carried by the renumber map, not by the new_text.
  - downstream: units changed VOL-I:11.3, VOL-I:11.3+ADD-03; rows citing them VOL-I-11.3-01
  - downstream proposal `D-ADD03-1103-R` row_reading (row:VOL-I-11.3-01): **insufficient_evidence**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The controller's replace_requirement check failed: the stated old requirement is not the row's requirement (or new is empty), and the controller status is insufficient_evidence.
      - concern: The 120 total and the 84-mark threshold depend on criterion G being worth 20 marks. The printed evidence only shows 'which add criterion G (energy efficiency)' and never states the 20 marks or the table total. The 20 marks and the 70% x 120 calculation are asserted, not shown.
      - concern: The pack does not define the five-point scale or weight, so the derived mark figure is not settled. The item acknowledges this, which supports a person deciding rather than the reading standing alone.
      - concern: The wording replacement of 11.3 and the new 11.3A (Envelope B retained unopened) do match the ADD-03 6.2 text. The 70% reading is also consistent with note (1).
  - downstream proposal `D-ADD03-1103-ISSUE` issue (row:VOL-I-11.3-01): **interpretation_pending**
    - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
      - concern: The issue's core claim (84/120, up from 70/100, criterion G counting) needs criterion G's 20 marks and the 120 total. The cited evidence only says criterion G is added and that the marks for A to F are unchanged. The weight of G is not in the evidence shown.
      - concern: The note that 'unchanged at seventy per cent' hides a rise in the mark threshold follows only if the total grew to 120. That cannot be checked from the quoted text.
      - concern: The 11.3 text does tie the threshold to a percentage of total marks in Table 1-1, so the direction of the issue is plausible. Showing the table or the weight of G would be needed to confirm it.
  - downstream proposal `DS-ADD03-15` row_new (c46:ADD-03/6.2(b)): **interpretation_pending**
  - output difference: NEW ADD-03-6.2-01; CHANGED VOL-I-11.3-01; A5 REWORK technical-proposal

### ADD-03:7.1 (clause, p2) — answered
- source: “This Section 7 has effect only if the Authority notifies Bidders through the Portal, not later than ten (10) Working Days before the Proposal Due Date, that the grid connection point referred to in Volume II Clause 1.4 will not be energised at least twelve (12) months before the Scheduled PCOD. If no such notice is given by that time, this Section 7 lapses.”
- transition: `ADD-03/7.1` disposition no_effect: 7.1 prints no change of its own. It is the trigger and lapse rule for Section 7: 'This Section 7 has effect only if the Authority notifies Bidders through the …
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'notifies' (cites VOL-II:1.4))
- transition: `ADD-03/7.1/issue` issue {"text": "Section 7 (conditional deletion of the Authority-provided grid connection point) is triggered only by an Authority Portal notice given not later than 10 Working Days before the PDD. By calc…
  - validation: **interpretation_pending**

### ADD-03:7.2 (clause, p2) — answered
- source: “Where this Section 7 has effect: (a) in Volume II Clause 1.4, the words ‘together with a grid connection point at the site boundary’, and the comma before them, are deleted; (b) the grid connection is a utility to be procured by the Project Company under the second sentence of Volume II Clause 1.4; and (c) the cost of the grid connection works forms part of…”
- transition: `ADD-03/7.2(a)` amendment_op replace_text VOL-II:1.4 “, together with a grid connection point at the site boundary” → “”
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The deletion of the words and the preceding comma matches 7.2(a). The triggered result 'free of encumbrance. All other utilities…' is correct.
    - concern: The 12 Nov 2026 deadline depends on a PDD of 26 Nov 2026 and on the Working Day calendar. Neither is shown here, and A1 is an unchecked assumption. A person should confirm both.
    - concern: The text of 7.1 is not among the printed units. It is relied on only through the quoted span, which the controller verified.
- transition: `ADD-03/7.2(b)` amendment_op annotate VOL-II:1.4 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: It is a conditional interpretation that depends on 7.1 and on 7.2(a).
- transition: `ADD-03/7.2(c)` escalation why: 7.2(c) says that, if Section 7 has effect, 'the cost of the grid connection works forms part of the Estimated Project Cost'. Estimated Project Cost is defined in VOL-V 1.3 (also being amended by ADD-…
  - validation: **escalated**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Escalating is reasonable. 7.2(c) says the grid cost forms part of the Estimated Project Cost, and VOL-V:1.3 defines that term but is not cited by 7.2.
    - concern: The claims that VOL-V 1.3 is also amended by ADD-03 Section 2 and that VOL-V 18.4 caps delay LDs at 10% of EPC are not in the evidence shown. They are unverified context.
    - concern: The consequence is conditional on Section 7 having effect, so it is tied to the 7.1 notice.

### ADD-03:8.1 (clause, p2) — answered
- source: “A new Form 4-H (Declaration of Beneficial Ownership) is added to Volume IV and to the list at Volume I Clause 9.1, to be inserted after Form 4-G. Form 4-H is reproduced at Appendix A to this Addendum.”
- transition: `ADD-03/8.1` amendment_op insert_unit VOL-I:9.1
  - validation: **evidence_verified**
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The evidence shown for VOL-I:9.1 is only the lead-in line. It does not show the list items, so I cannot confirm that VOL-I:9.1(e)+ADD-02 is Form 4-G, which the 'after' position depends on.
    - concern: The claims that the new group ADD-03:F4-H has 37 units and that this follows the ADD-02/7.1 pattern are not verifiable from the evidence shown.
    - concern: The provision does say Form 4-H is added to the 9.1 list after Form 4-G, so the intent is clear. A person must check the placement.
  - downstream: units changed ADD-03:F4-H/T1, ADD-03:F4-H/T1/1, ADD-03:F4-H/T1/2, ADD-03:F4-H/T1/3, ADD-03:F4-H/T1/4, ADD-03:F4-H/image, ADD-03:F4-H/image/decl1, ADD-03:F4-H/image/decl2, ADD-03:F4-H/image/decl3, ADD-03:F4-H/image/field-capacity-ar, ADD-03:F4-H/image/field-capacity-en, ADD-03:F4-H/image/field-cr-ar, ADD-03:F4-H/image/field-cr-en, ADD-03:F4-H/image/field-date-ar, ADD-03:F4-H/image/field-date-en, ADD-03:F4-H/image/field-member-ar, ADD-03:F4-H/image/field-member-en, ADD-03:F4-H/image/field-signatory-ar, ADD-03:F4-H/image/field-signatory-en, ADD-03:F4-H/image/field-signature-ar, ADD-03:F4-H/image/field-signature-en, ADD-03:F4-H/image/form-ar, ADD-03:F4-H/image/form-en, ADD-03:F4-H/image/hdr-ar, ADD-03:F4-H/image/hdr-en, ADD-03:F4-H/image/image-footer, ADD-03:F4-H/image/intro, ADD-03:F4-H/image/note, ADD-03:F4-H/image/ref-ar, ADD-03:F4-H/image/ref-en, ADD-03:F4-H/image/table-header, ADD-03:F4-H/image/table-row4, ADD-03:F4-H/image/table-row4-cells, ADD-03:F4-H/image/title, ADD-03:F4-H/para1, ADD-03:F4-H/para2, ADD-03:H:F4-H, VOL-I:9.1+ADD-03; rows citing them none
  - downstream proposal `DS-ADD03-16` row_new (c46:ADD-03/8.1): **insufficient_evidence**
  - downstream proposal `DS-ADD03-17` row_new (c46:ADD-03/8.1): **insufficient_evidence**
  - downstream proposal `DS-ADD03-18` issue (c46:ADD-03/8.1): **interpretation_pending**
  - downstream proposal `DS-ADD03-19` clarification_item (c46:ADD-03/8.1): **interpretation_pending**
  - downstream proposal `DS-ADD03-20` evidence_item (c46:ADD-03/8.1): **insufficient_evidence** — held back: no promotable row or activity uses EV-FORM-4H
  - downstream proposal `DS-ADD03-21` evidence_item (c46:ADD-03/8.1): **insufficient_evidence** — held back: no promotable row or activity uses EV-BO-REGISTER
  - downstream proposal `DS-ADD03-22` activity (c46:ADD-03/8.1): **insufficient_evidence** — held back: rows not promotable: ['ADD-03-8.1-01', 'ADD-03-8.1-02']
  - downstream proposal `DS-ADD03-23` activity (c46:ADD-03/8.1): **insufficient_evidence** — held back: neighbouring activities not promotable: ['form-4h-sign']

### ADD-03:8.2 (clause, p2) — answered
- source: “Form 4-H shall be completed in the Arabic language, signed and stamped by an authorised signatory of each member of the Bidder. The Arabic text governs. The English translation at Appendix B is provided for convenience only.”
- transition: `ADD-03/8.2` amendment_op annotate ADD-03:F4-H effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The provision requires Arabic, a signature and stamp from each member, Arabic governing, and an English translation for convenience only. The Arabic note matches.
    - concern: The Arabic image reading is still pending approval.
    - concern: The target is the form group, which 8.2 does not cite by unit id. It names Form 4-H, so this is acceptable.
- transition: `ADD-03/8.2/issue` issue {"text": "The Arabic and English versions of Form 4-H disagree on the beneficial-ownership threshold. The governing Arabic (Appendix A, decl1) says ten per cent (١٠٪ / 10%); the English (p.5) says tw…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The Arabic reading says 'ten per cent (١٠٪)' and the English says 25%, and 8.2 says the Arabic governs. The conflict is real and the conclusion follows.
    - concern: The Arabic reading comes from an image reading that is still pending approval. A person should check it against the image.
    - concern: The advice to prepare to 10% is a recommendation, not something the provision states.
  - downstream proposal `DS-ADD03-24` activity (c46:ADD-03/8.2): **insufficient_evidence** — held back: neighbouring activities not promotable: ['bo-register-copy']
  - downstream proposal `DS-ADD03-25` row_new (c46:ADD-03/8.2): **insufficient_evidence** — held back: evidence items with no activity (C44 would fail): ['EV-FORM-4H']
  - downstream proposal `DS-ISSUE-F4H-THRESHOLD` issue (c46:ADD-03/8.3): **conflicting**

### ADD-03:8.3 (clause, p2) — answered
- source: “Form 4-H shall be submitted with Envelope A. A member of the Bidder that is incorporated outside the Kingdom may instead submit its Form 4-H through the Portal not later than five (5) Working Days after the Proposal Due Date.”
- transition: `ADD-03/8.3` amendment_op annotate ADD-03:F4-H effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The default and the exception for members incorporated outside the Kingdom follow from the words.
    - concern: The 2 or 3 Dec 2026 dates depend on the PDD (A1) and the Working Day calendar, neither of which is shown. The pack's forward-counting convention is unstated, as the item itself says.
    - concern: The Portal route is optional ('may instead'), so the 5-Working-Day window applies only to foreign-incorporated members.
  - downstream proposal `DS-ROW-ADD-03-8.3-01` row_new (c46:ADD-03/8.3): **insufficient_evidence** — held back: issues not promotable: ['I-F4H-BO-THRESHOLD']
  - downstream proposal `DS-EV-FORM-4H` evidence_item (c46:ADD-03/8.3): **invalid**
  - downstream proposal `DS-ACT-FORM-4H-PREP` activity (c46:ADD-03/8.3): **invalid**
  - downstream proposal `DS-ISSUE-F4H-THRESHOLD` issue (c46:ADD-03/8.3): **conflicting**

### ADD-03:8.4 (clause, p2) — answered
- source: “Failure to submit a complete and properly executed Form 4-H for each member of the Bidder by the time required by Section 8.3 shall render the Proposal non-responsive.”
- transition: `ADD-03/8.4` amendment_op annotate ADD-03:F4-H effect adds_obligation
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: Non-responsiveness follows from the words. It ties to the time set by 8.3, so it depends on the 8.3 reading.
    - concern: The Arabic note says only that failing to submit it complete makes the Proposal non-responsive. The English adds 'properly executed'. The English text in 8.4 is the stronger statement.
  - downstream proposal `DS-ACT-FORM-4H-SIGN` activity (c46:ADD-03/8.4): **invalid**
  - downstream proposal `DS-ROW-ADD-03-8.4-01` row_new (c46:ADD-03/8.4): **insufficient_evidence** — held back: issues not promotable: ['I-F4H-BO-THRESHOLD']

### ADD-03:Q15 (table_row, p3) — answered
- source: “No: 15 | Bidder question: Volume I Clause 8.7 requires a Parent Company Guarantee that is unconditional as to the EPC Contractor's obligations during the construction period. Will the Authority accept a guarantee limited to a fixed amount? | Authority response: No. The Parent Company Guarantee shall be unlimited as to the guaranteed obligations and shall no…”
- transition: `ADD-03/Q15` amendment_op annotate VOL-I:8.7, VOL-IV:F4-D effect confirms
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The words "unlimited as to the guaranteed obligations" appear in Form 4-D, not in the text of Clause 8.7. Clause 8.7 says only "unconditional as to the EPC Contractor's obligations during the construction period". Annotating both units with effect 'confirms' is still reasonable, because Q15 itself …
  - downstream proposal `D-ADD03-087-R` row_reading (row:VOL-I-8.7-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-R-F4D-01` row_reading (row:VOL-IV-F4D-01): **insufficient_evidence**
  - downstream proposal `DS-ADD03-R-F4D-02` row_reading (row:VOL-IV-F4D-02): **insufficient_evidence**
  - downstream proposal `DS-ADD03-R-F4D-03` row_reading (row:VOL-IV-F4D-03): **insufficient_evidence**
  - downstream proposal `DS-ADD03-R-F4D-04` row_reading (row:VOL-IV-F4D-04): **insufficient_evidence**
  - downstream proposal `DS-ADD03-R-F4D-05` row_reading (row:VOL-IV-F4D-05): **insufficient_evidence**
  - downstream proposal `DS-ADD03-01` row_reading (row:VOL-IV-F4D-06): **interpretation_pending**
  - downstream proposal `DS-ADD03-02` row_reading (row:VOL-IV-F4D-07): **interpretation_pending**
  - downstream proposal `DS-ADD03-03` row_reading (row:VOL-IV-F4D-08): **interpretation_pending**
  - downstream proposal `DS-ACT-PCG-WORDING-NOCHANGE` no_change (act:pcg-wording): **interpretation_pending**
  - downstream proposal `DS-ACT-PCG-EXECUTION-NOCHANGE` no_change (act:pcg-execution): **interpretation_pending**
  - output difference: CHANGED VOL-IV-F4D-01; A5 REWORK pcg-execution; A5 REWORK pcg-wording

### ADD-03:Q16 (table_row, p3) — answered
- source: “No: 16 | Bidder question: Does the Estimated Project Cost to be stated in Form 4-F include the cost of the grid connection works? | Authority response: Only if Section 7 of this Addendum has effect. Otherwise the grid connection point is provided by the Authority in accordance with Volume II Clause 1.4.”
- transition: `ADD-03/Q16` amendment_op annotate VOL-IV:F4-F, VOL-II:1.4 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The evidence shows only the Section 7.1 trigger and 7.2(c). It does not show the rest of Section 7, so "excluded unless Section 7 has effect" rests on Q16's own wording, which does support it.
    - concern: The item states that Section 7's own operation is made elsewhere, which is correct. The annotation sets no value.
  - downstream proposal `DS-ADD03-R-14-01` row_reading (row:VOL-II-1.4-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-04` row_reading (row:VOL-IV-F4F-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-07` row_reading (row:VOL-IV-F4F-02): **interpretation_pending**
  - downstream proposal `DS-ACT-FORM-4F` activity (act:form-4f): **insufficient_evidence**
  - output difference: CHANGED VOL-II-1.4-01; CHANGED VOL-IV-F4F-01; A5 REWORK fin-model-build; A5 REWORK fin-model-freeze; A5 REWORK form-4f; A5 REWORK technical-proposal

### ADD-03:Q17 (table_row, p3) — UNRESOLVED
- source: “No: 17 | Bidder question: Will the Authority publish the reference specific energy consumption against which criterion G of Table 1-1 will be assessed? | Authority response: The reference specific energy consumption, in kWh per cubic metre of treated effluent, is stated in Appendix C to this Addendum together with the format of the Energy Performance Statem…”
- transition: `ADD-03/Q17` escalation why: Insufficient evidence. Q17 says the reference specific energy consumption 'is stated in Appendix C to this Addendum', but the evidence build of ADD-03 contains no Appendix C (only Appendix A, Form 4-…
  - validation: **escalated** — missing_information: the proposer declares missing: ADD-03 Appendix C (reference specific energy consumption in kWh/m3 and Energy Performance Statement format)
  - downstream proposal `DS-ADD03-ESC-Q17` escalation (esc:ADD-03:Q17): **escalated**

### ADD-03:Q18 (table_row, p3) — answered
- source: “No: 18 | Bidder question: Does the maximum velocity in Volume II Clause 5.2 apply to the trenchless crossings? | Authority response: Yes. Volume II Clause 5.2, as amended by Section 5.1 of this Addendum, applies to the whole length of the transmission main, including the crossings required by Volume II Clause 5.4.”
- transition: `ADD-03/Q18` amendment_op annotate VOL-II:5.2, VOL-II:5.4 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The new velocity value comes from ADD-03 5.1, which is not shown here. The item correctly sets no value and treats this only as a scope interpretation.
  - downstream proposal `DS-ADD03-R-54-01` row_reading (row:VOL-II-5.4-01): **interpretation_pending**
  - downstream proposal `DS-ADD03-R-54-02` row_reading (row:VOL-II-5.4-02): **interpretation_pending**
  - output difference: A5 REWORK technical-proposal; A5 REVIEW (proposed relationship) technical-proposal

### ADD-03:Q19 (table_row, p3) — answered
- source: “No: 19 | Bidder question: How is compliance with Volume I Clause 8.4(a), as amended, to be demonstrated in Envelope A, given that the Estimated Project Cost is stated only in Form 4-F? | Authority response: The Authority notes the question. Volume I Clauses 6.2 and 11.1 apply. The Authority does not consider further amendment necessary at this stage.”
- transition: `ADD-03/Q19` disposition no_effect: The response amends nothing: 'The Authority does not consider further amendment necessary at this stage.' It only points to existing clauses ('Volume I Clauses…
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The response only points to Clauses 6.2 and 11.1 and declines further amendment, so no_effect is consistent with its words. The text of Clauses 6.2 and 11.1 is not shown, so I cannot check whether they actually answer the bidder's question. The item rightly flags that the question stays unanswered …
- transition: `ADD-03/Q19-clarification` clarification {"gap": "Q19 asked how compliance with VOL-I 8.4(a), as amended, is shown in Envelope A when the Estimated Project Cost is stated only in Form 4-F; the Authority only replied that Clauses 6.2 and 11.…
  - validation: **interpretation_pending**

### ADD-03:Q20 (table_row, p3) — answered
- source: “No: 20 | Bidder question: Must the certified copy of the register of shareholders attached to Form 4-H be legalised where the member is incorporated outside the Kingdom? | Authority response: No. Legalisation is not required for the purposes of Form 4-H.”
- transition: `ADD-03/Q20` amendment_op annotate ADD-03:F4-H/image/decl3, ADD-03:F4-H/para1 effect interprets
  - validation: **interpretation_pending**
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: S-Q20-F1 calls the Arabic text "governing". Nothing in the evidence shown establishes which language governs.
    - concern: The target is a unit inside ADD-03 itself, namely the Form 4-H text the addendum introduces. That is plausible, but the person deciding should confirm it is the right unit to annotate.
    - concern: The Arabic reading and the English paragraph both require a "certified copy" and say nothing on legalisation, so the interpretation follows.

### ADD-03:AppA/para1 (paragraph, p3) — answered
- source: “Form 4-H is reproduced on the following page as issued. It shall be completed in the Arabic language in accordance with Section 8 of this Addendum.”
- transition: `ADD-03/AppA/para1` amendment_op annotate ADD-03:F4-H/image/note effect confirms
  - validation: **interpretation_pending**
- transition: `ADD-03/AppA/para1-issue` issue {"text": "The Arabic Form 4-H (governing, per ADD-03 8.2) sets the beneficial-owner threshold at ten per cent (10%), but the English translation in Appendix B says twenty-five per cent (25%). Declara…
  - validation: **evidence_verified**

### ADD-03:F4-H/image/hdr-en (reading_block, p4) — answered
- source: “NORTHERN UTILITIES PROCUREMENT AUTHORITY”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/hdr-ar (reading_block, p4) — answered
- source: “الهيئة الشمالية للمشتريات المرفقية”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/ref-en (reading_block, p4) — answered
- source: “Tender Ref: NUPA/ISTP/2026/014”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/ref-ar (reading_block, p4) — answered
- source: “مناقصة رقم: NUPA/ISTP/2026/014”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/form-en (reading_block, p4) — answered
- source: “FORM 4-H”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/form-ar (reading_block, p4) — answered
- source: “النموذج ٤-ح”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/title (reading_block, p4) — answered
- source: “إقرار المستفيد الحقيقي”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/intro (reading_block, p4) — answered
- source: “نحن الموقعون أدناه، بصفتنا ممثلين مفوضين عن العضو المذكور أدناه في ائتلاف مقدم العرض، نقر ونتعهد بما يلي:”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/decl1 (reading_block, p4) — answered
- source: “أولاً: أن الأشخاص الطبيعيين المبينين في الجدول أدناه هم جميع المستفيدين الحقيقيين من العضو، والمستفيد الحقيقي هو كل شخص طبيعي يملك، بصورة مباشرة أو غير مباشرة، ما نسبته عشرة في المائة (١٠٪) أو أكثر من رأس مال العضو أو من حقوق التصويت فيه، أو يسيطر على العضو بأي وسيلة أخرى.”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/decl2 (reading_block, p4) — answered
- source: “ثانياً: أنه لا يملك أيٌّ من المستفيدين الحقيقيين، بصورة مباشرة أو غير مباشرة، أي حصة في عضو في ائتلاف آخر يقدم عرضاً لهذه المناقصة.”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/decl3 (reading_block, p4) — answered
- source: “ثالثاً: أننا أرفقنا بهذا الإقرار نسخة مصدقة من سجل الشركاء أو المساهمين في العضو، صادرة خلال الثلاثين (٣٠) يوماً السابقة لتاريخ تقديم العروض.”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/table-header (reading_block, p4) — answered
- source: “م | اسم المستفيد الحقيقي | الجنسية | نسبة الملكية (٪) | مباشرة / غير مباشرة”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/table-row4 (reading_block, p4) — answered
- source: “٤”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/table-row4-cells (reading_block, p4) — answered
- source: “”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-member-en (reading_block, p4) — answered
- source: “Name of consortium member”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-member-ar (reading_block, p4) — answered
- source: “اسم العضو في الائتلاف :”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-cr-en (reading_block, p4) — answered
- source: “Commercial registration number”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-cr-ar (reading_block, p4) — answered
- source: “رقم السجل التجاري :”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-signatory-en (reading_block, p4) — answered
- source: “Name of authorised signatory”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-signatory-ar (reading_block, p4) — answered
- source: “اسم المفوض بالتوقيع :”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-capacity-en (reading_block, p4) — answered
- source: “Capacity”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-capacity-ar (reading_block, p4) — answered
- source: “الصفة :”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-date-en (reading_block, p4) — answered
- source: “Date”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-date-ar (reading_block, p4) — answered
- source: “التاريخ :”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-signature-en (reading_block, p4) — answered
- source: “Signature and company seal”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/field-signature-ar (reading_block, p4) — answered
- source: “التوقيع والختم :”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/note (reading_block, p4) — answered
- source: “ملاحظة: يجب تقديم هذا النموذج باللغة العربية عن كل عضو من أعضاء الائتلاف، والنص العربي هو المعتمد. عدم تقديمه كاملاً يجعل العرض غير مستجيب.”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/image/image-footer (reading_block, p4) — answered
- source: “FICTIONAL DOCUMENT - Lamar Holding internal assessment pack - not a real tender.”
- transition: content of ADD-03/8.1

### ADD-03:AppB/para1 (paragraph, p5) — answered
- source: “This translation is provided for convenience only. The Arabic text of Form 4-H at Appendix A governs.”
- transition: `ADD-03/AppB-para1` disposition no_effect: Appendix B paragraph is a precedence note on the English translation of the new Form 4-H; it prints no change (no quoted old/new, no deletion, substitution or …
  - validation: **interpretation_pending** — semantic: no_effect on amendment language: a person must confirm (its words carry 'provided' (cites ADD-03:F4-H))
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The words of AppB/para1 are a precedence/convenience note. They quote no old/new text and contain no deletion, substitution or reissue. 'provided' only appears in 'provided for convenience only', so the controller's semantic flag is a keyword match, not amending language.
    - concern: ADD-03:8.2 is printed only in the evidence quotation. Its full text is not in the units, and the 8.1 text is not shown. The claim that 8.1/8.2 introduce Form 4-H cannot be checked here, and 8.2 is only partly shown.
    - concern: The named target ADD-03:F4-H is not printed in the units, and the candidates list includes 8.2, so the target is a group or uncertain. no_effect is acceptable because no unit as it stood at ADD-02 is changed. A person should confirm that F4-H is the right target label.
    - concern: The restatement is close but not word-for-word: AppB names Form 4-H and Appendix A, while 8.2 says only 'The Arabic text governs'. The AppB paragraph also adds the Appendix A reference, which is a slight extension. It still does not change a unit.
    - concern: This depends on interpretation S3, which a person must confirm.

### ADD-03:F4-H/para1 (paragraph, p5) — answered
- source: “We, the undersigned, as the authorised representatives of the member of the Bidder's consortium named below, declare and undertake as follows: First: that the natural persons listed in the table below are all of the beneficial owners of the member, a beneficial owner being each natural person who owns, directly or indirectly, twenty-five per cent (25%) or m…”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/T1/1 (table_row, p5) — answered
- source: “No: 1”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/T1/2 (table_row, p5) — answered
- source: “No: 2”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/T1/3 (table_row, p5) — answered
- source: “No: 3”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/T1/4 (table_row, p5) — answered
- source: “No: 4”
- transition: content of ADD-03/8.1

### ADD-03:F4-H/para2 (paragraph, p5) — answered
- source: “Name of consortium member: _______________________ Commercial registration number: _______________ Name of authorised signatory: _______________________ Capacity: _______________ Date: ____________ Signature and company seal: _______________ Note: This Form shall be submitted in the Arabic language for each member of the consortium, and the Arabic text gove…”
- transition: content of ADD-03/8.1

## Downstream proposals (validated in the candidate)

| Item | Type | Task | Status | First failed check, or what a person confirms |
|---|---|---|---|---|
| D-ADD03-N3-ESC | escalation | row:ADD-02-T1-1-N3-01 | escalated |  |
| D-ADD03-1102-R | row_reading | row:VOL-I-11.2-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD03-1103-R | row_reading | row:VOL-I-11.3-01 | insufficient_evidence | replace_requirement: replace_requirement.old is not the row's requirement (or new is empty) |
| D-ADD03-1103-ISSUE | issue | row:VOL-I-11.3-01 | interpretation_pending |  |
| D-ADD03-0841-R | row_reading | row:VOL-I-8.4-01 | insufficient_evidence | replace_requirement: replace_requirement.old is not the row's requirement (or new is empty) |
| D-ADD03-0841-ISSUE | issue | row:VOL-I-8.4-01 | interpretation_pending |  |
| D-ADD03-0841-CQ | clarification_item | row:VOL-I-8.4-01 | insufficient_evidence | clarify.check: CQ-ADD03-NETWORTH-01: not verbatim in VOL-I:8.4: 'twenty-five per cent (25%) of the Estimated Project Cost' |
| D-ADD03-0842-R | row_reading | row:VOL-I-8.4-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD03-087-R | row_reading | row:VOL-I-8.7-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD03-T11A-R | row_reading | row:VOL-I-T1-1-A | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD03-T11B-R | row_reading | row:VOL-I-T1-1-B | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD03-T11C-R | row_reading | row:VOL-I-T1-1-C | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD03-T11D-R | row_reading | row:VOL-I-T1-1-D | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD03-T11E-R | row_reading | row:VOL-I-T1-1-E | interpretation_pending | a row reading is an interpretation: a person decides it |
| D-ADD03-T11F-R | row_reading | row:VOL-I-T1-1-F | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R-14-01 | row_reading | row:VOL-II-1.4-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R-52-01 | row_reading | row:VOL-II-5.2-01 | insufficient_evidence | replace_requirement: replace_requirement.old is not the row's requirement (or new is empty) |
| DS-ADD03-ISSUE-DN-VEL | issue | row:VOL-II-5.2-01 | insufficient_evidence | missing_information: the proposer declares missing: Internal bore of the lined pipe for the selected pressure class |
| DS-ADD03-R-52-02 | row_reading | row:VOL-II-5.2-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R-53-01 | row_reading | row:VOL-II-5.3-01 | insufficient_evidence | replace_requirement: replace_requirement.old is not the row's requirement (or new is empty) |
| DS-ADD03-DEP-53-54 | dependency | row:VOL-II-5.3-01 | interpretation_pending | an inferred relationship stays `proposed`: a person confirms or rejects it |
| DS-ADD03-R-53-02 | row_reading | row:VOL-II-5.3-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R-54-01 | row_reading | row:VOL-II-5.4-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R-54-02 | row_reading | row:VOL-II-5.4-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-R-F4D-01 | row_reading | row:VOL-IV-F4D-01 | insufficient_evidence | statements: fact downstream-002/S-F-F4D-Q15 is not supported verbatim |
| DS-ADD03-R-F4D-02 | row_reading | row:VOL-IV-F4D-02 | insufficient_evidence | evidence VOL-IV:F4-D/guaranteed-obligations p7: row key 'Guaranteed obligations' is not this row ('guaranteed-obligations') |
| DS-ADD03-R-F4D-03 | row_reading | row:VOL-IV-F4D-03 | insufficient_evidence | statements: fact downstream-002/S-F-F4D-Q15 is not supported verbatim |
| DS-ADD03-R-F4D-04 | row_reading | row:VOL-IV-F4D-04 | insufficient_evidence | evidence VOL-IV:F4-D/expiry p7: row key 'Expiry' is not this row ('expiry') |
| DS-ADD03-R-F4D-05 | row_reading | row:VOL-IV-F4D-05 | insufficient_evidence | statements: fact downstream-002/S-F-F4D-Q15 is not supported verbatim |
| DS-ADD03-01 | row_reading | row:VOL-IV-F4D-06 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-02 | row_reading | row:VOL-IV-F4D-07 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-03 | row_reading | row:VOL-IV-F4D-08 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-04 | row_reading | row:VOL-IV-F4F-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-05 | issue | row:VOL-IV-F4F-01 | interpretation_pending |  |
| DS-ADD03-06 | clarification_item | row:VOL-IV-F4F-01 | interpretation_pending |  |
| DS-ADD03-07 | row_reading | row:VOL-IV-F4F-02 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-08 | row_reading | row:VOL-V-12.1-01 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-09 | row_new | c46:ADD-03/cover/para3 | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-10 | issue | c46:ADD-03/cover/para3 | interpretation_pending |  |
| DS-ADD03-11 | clarification_item | c46:ADD-03/cover/para3 | interpretation_pending |  |
| DS-ADD03-12 | row_new | c46:ADD-03/4.1(a) | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-13 | row_new | c46:ADD-03/6.1 | insufficient_evidence | register (C16): ADD-03: quote not found in the effective text at ADD-03: 'Ref: G / Criterion: Energy efficiency and specific energy co' |
| DS-ADD03-14 | issue | c46:ADD-03/6.1 | invalid | id: issue id I-ADD03-TECH-THRESHOLD is not a new I-... id |
| DS-ADD03-15 | row_new | c46:ADD-03/6.2(b) | interpretation_pending | a row reading is an interpretation: a person decides it |
| DS-ADD03-16 | row_new | c46:ADD-03/8.1 | insufficient_evidence | register (C16): ADD-03: quote not found in the effective text at ADD-03: 'A new Form 4-H (Declaration of Beneficial Ownership) is adde' |
| DS-ADD03-17 | row_new | c46:ADD-03/8.1 | insufficient_evidence | register (C16): ADD-03: quote not found in the effective text at ADD-03: 'ما نسبته عشرة في المائة (١٠٪) أو أكثر من رأس مال العضو أو من' |
| DS-ADD03-18 | issue | c46:ADD-03/8.1 | interpretation_pending |  |
| DS-ADD03-19 | clarification_item | c46:ADD-03/8.1 | interpretation_pending |  |
| DS-ADD03-20 | evidence_item | c46:ADD-03/8.1 | insufficient_evidence | held back: no promotable row or activity uses EV-FORM-4H |
| DS-ADD03-21 | evidence_item | c46:ADD-03/8.1 | insufficient_evidence | held back: no promotable row or activity uses EV-BO-REGISTER |
| DS-ADD03-22 | activity | c46:ADD-03/8.1 | insufficient_evidence | held back: rows not promotable: ['ADD-03-8.1-01', 'ADD-03-8.1-02'] |
| DS-ADD03-23 | activity | c46:ADD-03/8.1 | insufficient_evidence | held back: neighbouring activities not promotable: ['form-4h-sign'] |
| DS-ADD03-24 | activity | c46:ADD-03/8.2 | insufficient_evidence | held back: neighbouring activities not promotable: ['bo-register-copy'] |
| DS-ADD03-25 | row_new | c46:ADD-03/8.2 | insufficient_evidence | held back: evidence items with no activity (C44 would fail): ['EV-FORM-4H'] |
| DS-ROW-ADD-03-8.3-01 | row_new | c46:ADD-03/8.3 | insufficient_evidence | held back: issues not promotable: ['I-F4H-BO-THRESHOLD'] |
| DS-EV-FORM-4H | evidence_item | c46:ADD-03/8.3 | invalid | id: evidence item id EV-FORM-4H is not a new EV-... id |
| DS-ACT-FORM-4H-PREP | activity | c46:ADD-03/8.3 | invalid | id: activity form-4h-prep proposed twice |
| DS-ACT-FORM-4H-SIGN | activity | c46:ADD-03/8.4 | invalid | id: activity form-4h-sign proposed twice |
| DS-ISSUE-F4H-THRESHOLD | issue | c46:ADD-03/8.3 | conflicting | declared_conflicts: the proposer declares: ADD-03:F4-H/image/decl1 vs ADD-03:F4-H/para1 |
| DS-ROW-ADD-03-8.4-01 | row_new | c46:ADD-03/8.4 | insufficient_evidence | held back: issues not promotable: ['I-F4H-BO-THRESHOLD'] |
| DS-CQ-DWF-NOCHANGE | no_change | clar:CQ-DWF-STORM-FLOW | interpretation_pending |  |
| DS-CQ-VOL-III-DRAWINGS | clarification_item | clar:CQ-VOL-III-DRAWINGS | evidence_verified |  |
| DS-CQ-PCOD-RELIABILITY-RUN | clarification_item | clar:CQ-PCOD-RELIABILITY-RUN | insufficient_evidence | clarify.check: CQ-PCOD-RELIABILITY-RUN: not verbatim in VOL-V:18.1: 'delay liquidated damages at the rate of one-twentieth of one per cent (0.05%) of' |
| DS-CQ-SCORING-METHOD | clarification_item | clar:CQ-SCORING-METHOD | insufficient_evidence | clarify.check: CQ-SCORING-METHOD: not verbatim in VOL-I:11.2: 'seventy per cent (70%) technical and thirty per cent (30%) commercial' |
| DS-ACT-TECHNICAL-PROPOSAL | activity | act:technical-proposal | insufficient_evidence | missing_information: the proposer declares missing: No A1 row yet holds criterion G or Note (4) (Energy Performance Statement); the ADD-03/6.1 task should add one and list EV-TECH-PROPOSAL so this ac… |
| DS-ACT-FIN-STATEMENTS-NOCHANGE | no_change | act:fin-statements | interpretation_pending |  |
| DS-ACT-FIN-STANDING | activity | act:fin-standing | insufficient_evidence | missing_information: the proposer declares missing: The method of showing compliance with 8.4(a) in Envelope A, given that the Estimated Project Cost appears only in the Envelope B Form 4-F, is not s… |
| DS-ISSUE-EPC-ENVELOPE-A | issue | act:fin-standing | interpretation_pending |  |
| DS-DEP-EPC-NETWORTH | dependency | act:fin-standing | insufficient_evidence | held back: endpoints not promotable: ['fin-standing'] |
| DS-ACT-PCG-WORDING-NOCHANGE | no_change | act:pcg-wording | interpretation_pending |  |
| DS-ACT-PCG-EXECUTION-NOCHANGE | no_change | act:pcg-execution | interpretation_pending |  |
| DS-ACT-FORM-4F | activity | act:form-4f | insufficient_evidence | missing_information: the proposer declares missing: Whether ADD-03 Section 7 takes effect depends on an Authority notice due not later than ten Working Days before the Proposal Due Date. Until then, … |
| DS-ADD03-ACT-FIN-MODEL-BUILD | no_change | act:fin-model-build | interpretation_pending |  |
| DS-ADD03-ACT-FIN-MODEL-FREEZE | activity | act:fin-model-freeze | insufficient_evidence | missing_information: the proposer declares missing: Whether the Bidder's financial-standing demonstration in Envelope A must be computed against the exact Estimated Project Cost later stated in Form … |
| DS-ADD03-ESC-Q17 | escalation | esc:ADD-03:Q17 | escalated | missing_information: the proposer declares missing: ADD-03 Appendix C (reference specific energy consumption; format of the Energy Performance Statement) |

## Promoted into the candidate (PROPOSED; nothing accepted)

- ops: ADD-03/cover/para3, ADD-03/2.1, ADD-03/2.2, ADD-03/3.1, ADD-03/4.1(a), ADD-03/4.1(b), ADD-03/5.1, ADD-03/5.2, ADD-03/6.1, ADD-03/S6/para1(a), ADD-03/S6/para1(b), ADD-03/S6/para1(c), ADD-03/6.2(a), ADD-03/6.2(b), ADD-03/7.2(a), ADD-03/7.2(b), ADD-03/8.1, ADD-03/8.2, ADD-03/8.3, ADD-03/8.4, ADD-03/Q15, ADD-03/Q16, ADD-03/Q18, ADD-03/Q20, ADD-03/AppA/para1
- dispositions: ADD-03:cover/para1: no_effect, ADD-03:cover/para2: no_effect, ADD-03:1.1: no_effect, ADD-03:1.2: no_effect, ADD-03:7.1: no_effect, ADD-03:Q19: no_effect, ADD-03:AppB/para1: no_effect
- rows new: ADD-03-cover-01, ADD-03-4.1-01, ADD-03-6.2-01
- readings: VOL-I-11.2-01, VOL-I-8.4-02, VOL-I-8.7-01, VOL-I-T1-1-A, VOL-I-T1-1-B, VOL-I-T1-1-C, VOL-I-T1-1-D, VOL-I-T1-1-E, VOL-I-T1-1-F, VOL-II-1.4-01, VOL-II-5.2-02, VOL-II-5.3-02, VOL-II-5.4-01, VOL-II-5.4-02, VOL-IV-F4D-06, VOL-IV-F4D-07, VOL-IV-F4D-08, VOL-IV-F4F-01, VOL-IV-F4F-02, VOL-V-12.1-01
- issues: I-ADD03-EPC-ENVELOPE, I-ADD03-F4H-PORTAL, I-ADD03-F4H-THRESHOLD, I-ADD03-NETWORTH-EPC, I-ADD03-TECH-THRESHOLD, I-EPC-ENVELOPE-A
- clarifications: CQ-ADD03-EPC-ENVELOPE, CQ-ADD03-F4H-PORTAL, CQ-ADD03-F4H-THRESHOLD, CQ-VOL-III-DRAWINGS
- relationships: REL-AI-001
- no change: clar:CQ-DWF-STORM-FLOW, act:fin-statements, act:pcg-wording, act:pcg-execution, act:fin-model-build
- unresolved provisions: 1

## check-register on the candidate

- exit 1; 12 finding(s) {'disposition': 1, 'C46': 11}
  - [disposition] VOL-V: row ADD-03-4.1-01 uses VOL-V:18.1, whose disposition does not list it as a requirement
  - [C46] ADD-03/cover/para3: [A3] ADD-03/cover/para3 brings in consequence words ['liquidated damages'] that no row's consequence carries at ADD-03: 'This Addendum amends the definition of Estimated Project Cost, the financial c…
  - [C46] ADD-03/6.1: [A1] ADD-03/6.1 (replace_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Table 1-1 (revised) and the Notes to it, issued by Section 3 of Addendum No. 2, are deleted an…
  - [C46] ADD-03/8.1: [A1] ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-I:9.1; a row of the anchor VOL-I:9.1 does not count): 'A new Form 4-…
  - [C46] ADD-03/8.1: [A1] ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the new ADD-03:F4-H; a row of the anchor VOL-I:9.1 does not count): 'A new Form 4-H (Declaration…
  - [C46] ADD-03/8.1: [A3] ADD-03/8.1 brings in consequence words ['non-responsive', 'غير مستجيب'] that no row's consequence carries at ADD-03: 'A new Form 4-H (Declaration of Beneficial Ownership) is added to Volume IV a…
  - [C46] ADD-03/8.2: [A1] ADD-03/8.2 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Form 4-H shall be completed in the Arabic language, signed and stamped by an authorised signatory …
  - [C46] ADD-03/8.2: [A3] ADD-03/8.2 brings in consequence words ['non-responsive', 'غير مستجيب'] that no row's consequence carries at ADD-03: 'Form 4-H shall be completed in the Arabic language, signed and stamped by an…
  - [C46] ADD-03/8.3: [A1] ADD-03/8.3 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Form 4-H shall be submitted with Envelope A. A member of the Bidder that is incorporated outside t…
  - [C46] ADD-03/8.3: [A3] ADD-03/8.3 brings in consequence words ['non-responsive', 'غير مستجيب'] that no row's consequence carries at ADD-03: 'Form 4-H shall be submitted with Envelope A. A member of the Bidder that is …
  - [C46] ADD-03/8.4: [A1] ADD-03/8.4 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Failure to submit a complete and properly executed Form 4-H for each member of the Bidder by the t…
  - [C46] ADD-03/8.4: [A3] ADD-03/8.4 brings in consequence words ['non-responsive', 'غير مستجيب'] that no row's consequence carries at ADD-03: 'Failure to submit a complete and properly executed Form 4-H for each member …

## Coverage

- provisions: 70; accounted for by the combined set: 70; states {'validated': 70}
- resolution (controller): resolved 50, pending 20, invalid 0, unaccounted 0; approved 0
- structural units of ADD-03 that are not provisions (listed so nothing is dropped): ADD-03:H:cover (heading), ADD-03:H:cover-2 (heading), ADD-03:H:S1 (heading), ADD-03:H:S2 (heading), ADD-03:H:S3 (heading), ADD-03:H:S4 (heading), ADD-03:H:S5 (heading), ADD-03:H:S6 (heading), ADD-03:T1-1 (table), ADD-03:H:S7 (heading), ADD-03:H:S8 (heading), ADD-03:H:S9 (heading), ADD-03:S9/QA (table), ADD-03:H:AppA (heading), ADD-03:region:ADD-03-p4-r1 (region), ADD-03:F4-H/image (image_text), ADD-03:H:AppB (heading), ADD-03:H:F4-H (heading), ADD-03:F4-H/T1 (table)
- batches: reading-ADD-03-p4-r1 done, analysis-001 done, analysis-002 done, analysis-003 skipped, analysis-004 done, analysis-005 done, analysis-006 skipped, analysis-007 skipped, analysis-008 skipped, analysis-009 done, analysis-010 skipped, downstream-001 done, downstream-002 done, downstream-003 done, downstream-004 done, downstream-005 done

## Critic (a second model over the selected items; it changed no status)

**Agreement between the critic and the proposer is not approval**: every item still needs a person's decision, and a disagreement is a concern for that person, not a rejection. The critic reviews only the selected classes (consequential interpretations, uncertain targets, removals, conflicting evidence), in one request per batch.

| Batch | Critic | Selected | Reviewed | Agrees | Does not agree | Note |
|---|---|---|---|---|---|---|
| analysis-001 | done | 5 | 5 | 5 | 0 |  |
| analysis-002 | done | 1 | 1 | 1 | 0 |  |
| analysis-004 | done | 13 | 13 | 12 | 1 |  |
| analysis-005 | done | 5 | 5 | 5 | 0 |  |
| analysis-009 | done | 1 | 1 | 1 | 0 |  |
| downstream-001 | done | 3 | 3 | 0 | 3 |  |
| downstream-002 | not_needed | 0 | - | - | - |  |
| downstream-003 | not_needed | 0 | - | - | - |  |
| downstream-004 | not_needed | 0 | - | - | - |  |
| downstream-005 | not_needed | 0 | - | - | - |  |

- **ADD-03/cover/para3** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Target is the provision itself, which is acceptable for an annotation. The ADD-02 precedent in the rationale is not in the evidence shown, but the obligation follows from the quoted words alone.
    - concern: The same paragraph also contains the Form 4-H timing statement, which conflicts with 8.3 and is handled in the separate issue item.
- **ADD-03/cover/para3-issue** (analysis-001; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The conflict is real. The cover says all Bidders may submit Form 4-H through the Portal within 5 Working Days. Section 8.3 requires it with Envelope A and allows the later Portal submission only for a member incorporated outside the Kingdom.
    - concern: The issue text says Section 8.4 makes a late Form 4-H non-responsive. ADD-03:8.4 is listed as a dependency but is not among the units printed, so that consequence is not verified by the evidence shown.
    - concern: Planning on 8.3 as the stricter reading is a prudent recommendation, not something the text settles. The cover also says the Addendum takes precedence, and the evidence shown does not rank the cover against Section 8.3.
- **ADD-03/1.1** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The text reads as a recital of authority and precedence, and no amendment wording appears in it.
    - concern: The claim that it restates existing rules rests on VOL-I 5.3 and 3.2, whose text is not shown. A person should confirm against those clauses.
- **ADD-03/1.2** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: It is a reading rule and amends no RFP text, so no_effect is reasonable.
    - concern: The 'unless otherwise stated' exception is real. It could displace the ADD-02 stage reading for a particular reference elsewhere in ADD-03, and the evidence shown does not let me check that. This is why the controller semantic check failed, and a person must confirm.
- **ADD-03/2.2** (analysis-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: VOL-V:1.3 is the right target. The provision extends the reach of the definition and does not change its words.
    - concern: The annotation note names VOL-I 8.4 as amended by ADD-03 3.1 and VOL-V 18.4 as applications of the term. Sections 2.1 and 3.1, VOL-I 8.4 and VOL-V 18.4 are not printed, so these specifics are unverified.
    - concern: The effect 'interprets' may understate this. Applying a Volume V definition across all RFP Documents could widen its scope, and a person should confirm.
- **ADD-03/6.1** (analysis-002; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The target is right: ADD-03:6.1 names 'Table 1-1 (revised) ... issued by Section 3 of Addendum No. 2', which matches ADD-02:T1-1-rev. The replacement ADD-03:T1-1 is 'Table 1-1 (second revision)'.
    - concern: The provision deletes and replaces the table AND its Notes. The op only maps the table group to ADD-03:T1-1. The new Notes (ADD-03:S6/para1) are not part of the replacement, so the ADD-02 notes would be removed with no replacement in this op. This is a real gap that the item flags correctly and tha…
    - concern: The notes change is substantive. The old note says the threshold is 'seventy (70) marks'. The new note says 'seventy per cent (70%)'. With a total of 120 that is 84 marks, not 70. The wording 'unchanged' in the new note does not match the old note.
    - concern: The rationale's claims are not shown in the printed evidence. These are: rows A-F being 25/15/20/20/10/10, the old 65/35 weighting versus the new 70/30, and the 12-unit versus 9-unit counts. Only G=20 and total=120 are quoted, so I could not verify these.
    - concern: The unit status of ADD-03:6.1 is printed as 'not_issued'. The evidence does not explain this, and a person should check it.
- **ADD-03/S6/para1(b)** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The provision does not quote the old words. They come from VOL-I:11.2 at ADD-02, which prints 65/35, and they match the target.
- **ADD-03/S6/para1(c)** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Note (3) is a scoring rule, so an interpreting annotation fits. The 'standard five-point scale' is not defined in the evidence shown.
    - concern: Table 1-1 is not named by 7.x, but the notes are headed 'Notes to Table 1-1', so the target is reasonable.
- **ADD-03/S6/para1(d)** (analysis-004; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: The words 'shall shall be included' are not in the evidence. The shown text 'shall be included in the Technical Proposal in the format at Appendix C' does support a new deliverable tied to criterion G.
    - concern: Appendix C is not in the evidence, so the format and any further requirements cannot be checked. This is already declared as missing information.
    - concern: The controller status is insufficient_evidence. A person should obtain Appendix C before relying on the item.
- **ADD-03/6.2(a)** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The old 11.3 text matches the target. The new text matches the quoted new 11.3. The Envelope B sentence moves to 11.3A.
    - concern: The threshold changes from '70 marks out of 100' to '70% of total marks available in Table 1-1'. These are equal only if Table 1-1 totals 100 marks. The evidence shown does not give that total.
- **ADD-03/6.2(b)** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The new text matches the quoted 11.3A. The timing change (retained, then returned after the Preferred Bidder Notification) follows from the words.
    - concern: The label 11.3A is carried by the renumber map, not by the new_text.
- **ADD-03/7.2(a)** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: old words located in the target; model claude-sonnet-5-5
    - concern: The deletion of the words and the preceding comma matches 7.2(a). The triggered result 'free of encumbrance. All other utilities…' is correct.
    - concern: The 12 Nov 2026 deadline depends on a PDD of 26 Nov 2026 and on the Working Day calendar. Neither is shown here, and A1 is an unchecked assumption. A person should confirm both.
    - concern: The text of 7.1 is not among the printed units. It is relied on only through the quoted span, which the controller verified.
- **ADD-03/7.2(b)** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: It is a conditional interpretation that depends on 7.1 and on 7.2(a).
- **ADD-03/7.2(c)** (analysis-004; controller status **escalated**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is not among the units the provision cites; model claude-sonnet-5-5
    - concern: Escalating is reasonable. 7.2(c) says the grid cost forms part of the Estimated Project Cost, and VOL-V:1.3 defines that term but is not cited by 7.2.
    - concern: The claims that VOL-V 1.3 is also amended by ADD-03 Section 2 and that VOL-V 18.4 caps delay LDs at 10% of EPC are not in the evidence shown. They are unverified context.
    - concern: The consequence is conditional on Section 7 having effect, so it is tied to the 7.1 notice.
- **ADD-03/8.1** (analysis-004; controller status **evidence_verified**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The evidence shown for VOL-I:9.1 is only the lead-in line. It does not show the list items, so I cannot confirm that VOL-I:9.1(e)+ADD-02 is Form 4-G, which the 'after' position depends on.
    - concern: The claims that the new group ADD-03:F4-H has 37 units and that this follows the ADD-02/7.1 pattern are not verifiable from the evidence shown.
    - concern: The provision does say Form 4-H is added to the 9.1 list after Form 4-G, so the intent is clear. A person must check the placement.
- **ADD-03/8.2** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The provision requires Arabic, a signature and stamp from each member, Arabic governing, and an English translation for convenience only. The Arabic note matches.
    - concern: The Arabic image reading is still pending approval.
    - concern: The target is the form group, which 8.2 does not cite by unit id. It names Form 4-H, so this is acceptable.
- **ADD-03/8.2/issue** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The Arabic reading says 'ten per cent (١٠٪)' and the English says 25%, and 8.2 says the Arabic governs. The conflict is real and the conclusion follows.
    - concern: The Arabic reading comes from an image reading that is still pending approval. A person should check it against the image.
    - concern: The advice to prepare to 10% is a recommendation, not something the provision states.
- **ADD-03/8.3** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The default and the exception for members incorporated outside the Kingdom follow from the words.
    - concern: The 2 or 3 Dec 2026 dates depend on the PDD (A1) and the Working Day calendar, neither of which is shown. The pack's forward-counting convention is unstated, as the item itself says.
    - concern: The Portal route is optional ('may instead'), so the 5-Working-Day window applies only to foreign-incorporated members.
- **ADD-03/8.4** (analysis-004; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: Non-responsiveness follows from the words. It ties to the time set by 8.3, so it depends on the 8.3 reading.
    - concern: The Arabic note says only that failing to submit it complete makes the Proposal non-responsive. The English adds 'properly executed'. The English text in 8.4 is the stronger statement.
- **ADD-03/Q15** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The words "unlimited as to the guaranteed obligations" appear in Form 4-D, not in the text of Clause 8.7. Clause 8.7 says only "unconditional as to the EPC Contractor's obligations during the construction period". Annotating both units with effect 'confirms' is still reasonable, because Q15 itself …
- **ADD-03/Q16** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The evidence shows only the Section 7.1 trigger and 7.2(c). It does not show the rest of Section 7, so "excluded unless Section 7 has effect" rests on Q16's own wording, which does support it.
    - concern: The item states that Section 7's own operation is made elsewhere, which is correct. The annotation sets no value.
- **ADD-03/Q18** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: The new velocity value comes from ADD-03 5.1, which is not shown here. The item correctly sets no value and treats this only as a scope interpretation.
- **ADD-03/Q19** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The response only points to Clauses 6.2 and 11.1 and declines further amendment, so no_effect is consistent with its words. The text of Clauses 6.2 and 11.1 is not shown, so I cannot check whether they actually answer the bidder's question. The item rightly flags that the question stays unanswered …
- **ADD-03/Q20** (analysis-005; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: resolved through a group; model claude-sonnet-5-5
    - concern: S-Q20-F1 calls the Arabic text "governing". Nothing in the evidence shown establishes which language governs.
    - concern: The target is a unit inside ADD-03 itself, namely the Form 4-H text the addendum introduces. That is plausible, but the person deciding should confirm it is the right unit to annotate.
    - concern: The Arabic reading and the English paragraph both require a "certified copy" and say nothing on legalisation, so the interpretation follows.
- **ADD-03/AppB-para1** (analysis-009; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): agrees — selected because consequential_interpretation, uncertain_target, uncertain_target: target is a group; model claude-sonnet-5-5
    - concern: The words of AppB/para1 are a precedence/convenience note. They quote no old/new text and contain no deletion, substitution or reissue. 'provided' only appears in 'provided for convenience only', so the controller's semantic flag is a keyword match, not amending language.
    - concern: ADD-03:8.2 is printed only in the evidence quotation. Its full text is not in the units, and the 8.1 text is not shown. The claim that 8.1/8.2 introduce Form 4-H cannot be checked here, and 8.2 is only partly shown.
    - concern: The named target ADD-03:F4-H is not printed in the units, and the candidates list includes 8.2, so the target is a group or uncertain. no_effect is acceptable because no unit as it stood at ADD-02 is changed. A person should confirm that F4-H is the right target label.
    - concern: The restatement is close but not word-for-word: AppB names Form 4-H and Appendix A, while 8.2 says only 'The Arabic text governs'. The AppB paragraph also adds the Appendix A reference, which is a slight extension. It still does not change a unit.
    - concern: This depends on interpretation S3, which a person must confirm.
- **D-ADD03-1103-R** (downstream-001; controller status **insufficient_evidence**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The controller's replace_requirement check failed: the stated old requirement is not the row's requirement (or new is empty), and the controller status is insufficient_evidence.
    - concern: The 120 total and the 84-mark threshold depend on criterion G being worth 20 marks. The printed evidence only shows 'which add criterion G (energy efficiency)' and never states the 20 marks or the table total. The 20 marks and the 70% x 120 calculation are asserted, not shown.
    - concern: The pack does not define the five-point scale or weight, so the derived mark figure is not settled. The item acknowledges this, which supports a person deciding rather than the reading standing alone.
    - concern: The wording replacement of 11.3 and the new 11.3A (Envelope B retained unopened) do match the ADD-03 6.2 text. The 70% reading is also consistent with note (1).
- **D-ADD03-1103-ISSUE** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The issue's core claim (84/120, up from 70/100, criterion G counting) needs criterion G's 20 marks and the 120 total. The cited evidence only says criterion G is added and that the marks for A to F are unchanged. The weight of G is not in the evidence shown.
    - concern: The note that 'unchanged at seventy per cent' hides a rise in the mark threshold follows only if the total grew to 120. That cannot be checked from the quoted text.
    - concern: The 11.3 text does tie the threshold to a percentage of total marks in Table 1-1, so the direction of the issue is plausible. Showing the table or the weight of G would be needed to confirm it.
- **D-ADD03-0841-ISSUE** (downstream-001; controller status **interpretation_pending**, unchanged)
  - critic (a second model; agreement is not approval): DOES NOT agree — selected because consequential_interpretation; model claude-sonnet-5-5
    - concern: The conflict depends on Form 4-F being an Envelope B document and on 8.4 being assessed at Envelope A. The item itself says VOL-I 10.1 is 'not quoted here', and the evidence shown does not support either point.
    - concern: The evidence does support that 8.4(a) is now 25% of the Estimated Project Cost, that limb (b) is unchanged, and that ADD-03 2.1 substitutes 'as stated by the Bidder in Form 4-F'. 11.3A also supports Envelope B staying unopened for Proposals that fail the technical stage.
    - concern: The statement that Envelope B is opened only for Proposals that pass technical evaluation is inferred from 11.3A. The base opening procedure is not shown.
    - concern: The ADD-03 2.1 text is only quoted in part, so the full redefinition of Estimated Project Cost cannot be checked. A person should confirm against VOL-I 10.1 and the opening procedure.

## Requests: failures, deferrals, repairs and route notices

- **downstream-002** (done): repaired once (1 problem(s) before the re-ask)
- **downstream-003** (done): 1 failed call(s) (rate_limit); DEFERRED 2026-10-04T23:22:15Z: host rate limit (the host ended with an error (success: 429) You've hit your session limit · resets 2:30am (UTC)); the host names a reset in 11264.9 s, beyond 300 s (reset named in about 188 min)

Route notices (how the requests were served; they change no status):
- **capabilities_declared** (reading-ADD-03-p4-r1): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the reading request was checked a…
- **capabilities_declared** (analysis-001): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-002): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-004): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-005): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (analysis-009): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the analysis request was checked …
- **capabilities_declared** (downstream-001): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-002): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-003): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-004): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…
- **capabilities_declared** (downstream-005): capabilities declared, not verified: host claude-code headless (opus) (config/ai.yaml host_session.capabilities: DECLARED, not verified by this tool (a host's model cannot be queried; image input and tool use as observed in real host sessions); basis: observed in real headless host sessions on 4 Oct 2026 (session 10: crops read over MCP); declared, not verified); the downstream request was checke…

## Manual interventions (and automatic host sessions, named as such: not a person)

- 2026-10-04T22:25:42Z: host session (automatic) — batch reading-ADD-03-p4-r1 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session reading an image; not a person
- 2026-10-04T22:30:48Z: host session (automatic) — batch analysis-001 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T22:34:55Z: host session (automatic) — batch analysis-002 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T22:48:44Z: host session (automatic) — batch analysis-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T22:57:11Z: host session (automatic) — batch analysis-005 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T22:58:36Z: host session (automatic) — batch analysis-009 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session over the MCP tools; not a person
- 2026-10-04T23:03:15Z: host session (automatic) — batch downstream-001 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-04T23:09:28Z: host session (automatic) — batch downstream-002 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-04T23:13:15Z: host session (automatic) — batch downstream-003 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-04T23:13:28Z: host session (automatic) — batch downstream-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-04T23:13:41Z: host session (automatic) — batch downstream-005 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-04T23:22:15Z: host session (automatic) — batch downstream-003 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T02:42:54Z: host session (automatic) — batch downstream-003 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T02:49:59Z: host session (automatic) — batch downstream-004 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person
- 2026-10-05T02:51:35Z: host session (automatic) — batch downstream-005 by tenderpack.ai.hostsession; host model claude-code headless (opus); a headless host session; not a person

## The diff (ADD-02 → ADD-03; [diff.md](diff.md))

## What changed from ADD-02 to ADD-03

### ADD-03: PARTIAL (issued 2026-11-09)

- ops: 25 (0 invalid); provisions: 70 (1 unresolved)
- validated state: ADD-02 — this addendum does NOT replace it until every provision is treated and every op is valid
- UNRESOLVED ADD-03:Q17: No: 17 | Bidder question: Will the Authority publish the reference specific energy consumption against which criterion G of Table 1-1 will be assessed? | Author
- CONDITIONAL ADD-03/7.2(a): CONDITIONAL (pending): not in effect unless the Authority notifies Bidders through the Portal, not later than ten (10) Working Days before the Proposal Due Date, that the grid connect… (ADD-03:7.1); decide by 2026-11-12; nothing assumes the trigger occurred; if triggered: VOL-II:1.4: “The Authority will provide the site free of encumbrance, together wit…” -> “The Authority will provide the site free of encumbrance. All other ut…”; if not: If no such notice is given by that time, this Section 7 lapses.
- CONDITIONAL ADD-03/7.2(b): CONDITIONAL (pending): not in effect unless the Authority notifies Bidders through the Portal, not later than ten (10) Working Days before the Proposal Due Date, that the grid connect… (ADD-03:7.1); decide by 2026-11-12; nothing assumes the trigger occurred; if not: If no such notice is given by that time, this Section 7 lapses.
- cover summary vs provisions (C28, report only): 4 finding(s)
  - consequence not mentioned: ADD-03:8.4 states 'Failure to submit a complete and properly executed Form 4-H for each member of the Bidder by the time required by Section 8.3 shall render the Proposal non-responsive.'; the summary says only 'adds a Declaration of Beneficial Ownership (Form 4-H) which all Bidders may submit through the Portal within five Working Days after the Proposal Due Date'
  - omitted: ADD-03/2.1 amends VOL-V:1.3; the summary does not mention it: 'In Volume V Clause 1.3, ‘as set out in the agreed Financial Model at Financial Close’ is deleted and ‘as stated by the Bidder in Form 4-F, excluding financing costs, interest during construction and development fees’ is substituted.'
  - omitted: ADD-03/S6/para1(b) amends VOL-I:11.2; the summary does not mention it: 'Notes to Table 1-1 (second revision): (1) The technical score threshold in Volume I Clause 11.3 is unchanged at seventy per cent (70%). (2) The combined score weighting stated in Volume I Clause 11.2 is amended to seventy per cent (70%) te…'
  - contradicted: 'relaxes the velocity limit for the treated effluent transmission main', but contradicted by the numbers: ADD-03/5.1 lowered a maximum in VOL-II 5.2 (2.0 m/s -> 1.5 m/s; 'maximum'), which tightens the requirement

#### Validated vs candidate (partial should not mean useless)

- validated (unchanged, ADD-02): `<outputs>/a3/a3.pdf` (one page), `<outputs>/a5/`
- candidate (CANDIDATE — NOT VALIDATED, ADD-03 as proposed): `<outputs>/a3/a3_candidate.pdf` / `.md`, `<outputs>/a5/candidate/`

**What may be changing.** ADD-03 is PARTIAL: 1 of 70 provisions unresolved, so A3 and A5 stay validated at ADD-02. If the 23 op(s) that are valid there stood (each still a proposal: review proposed 23), A3 would gain 2 row(s) (ADD-03-6.2-01 (ADD-03/6.2(b), ADD-03/6.2(a)), ADD-03-cover-01 (ADD-03/cover/para3)), lose 0 (none) and change 3 (VOL-I-11.3-01 (ADD-03/6.2(a), ADD-03/S6/para1(a), ADD-03/6.2(b)), VOL-I-8.4-01 (ADD-03/3.1), VOL-IV-F4D-01 (ADD-03/Q15)); A5, replanned at ADD-03's issue date (2026-11-09), would move the latest dates of 0 activities (none), add 0 (none) and remove 0 (none), and marks 6 REVIEW through relationships. Not settled: 5 activities blocked by an unresolved row (pcg-wording, technical-proposal, pcg-execution, fin-statements and 1 more), 9 STALE row(s), 11 obligation(s) reaching no output (C46), 0 relationship chain(s) blocked or incomplete, 2 conflict(s); documents not supplied: the Environmental Permit issued for the site, Volume V Schedule 11 (Project Company Events of Default), Volume V Schedule 7 (deductions), I-PERMIT and 5 more; conditional or effective-dated: ADD-03:7.2 (conditional amendment, decision by 2026-11-12); ADD-03:7.2 (conditional amendment, decision by 2026-11-12); ADD-03:5.2 (effective-dated amendment, effective 2026-10-08); ADD-03:Q16 (conditional amendment, decision by 2026-11-12). Nothing here is validated, accepted or applied to the real state.

### Requirements

- new: 3; out of force: 1; changed: 17

- NEW ADD-03-cover-01: NEW (introduced by ADD-03/cover/para3)
- NEW ADD-03-4.1-01: NEW (introduced by ADD-03/4.1(a)) (by ADD-03/4.1(a))
- NEW ADD-03-6.2-01: NEW (introduced by ADD-03/6.2(b)) (by ADD-03/6.2(b))
- OUT ADD-02-T1-1-N3-01: REPLACED (by ADD-03:T1-1)
- CHANGED VOL-I-11.2-01: wording; quoted words (by ADD-03/S6/para1(b))
- CHANGED VOL-I-11.3-01: wording (by ADD-03/6.2(a))
- CHANGED VOL-I-T1-1-B: amended (by ADD-03/6.1)
- CHANGED VOL-I-T1-1-D: amended (by ADD-03/6.1)
- CHANGED VOL-I-8.4-01: wording (by ADD-03/3.1)
- CHANGED VOL-I-8.4-02: wording (by ADD-03/3.1)
- CHANGED VOL-I-T1-1-A: amended (by ADD-03/6.1)
- CHANGED VOL-I-T1-1-C: amended (by ADD-03/6.1)
- CHANGED VOL-I-T1-1-E: amended (by ADD-03/6.1)
- CHANGED VOL-I-T1-1-F: amended (by ADD-03/6.1)
- CHANGED VOL-II-1.4-01: TRIGGER-ADD-03-S7 None -> 2026-11-12
- CHANGED VOL-II-5.2-01: wording (by ADD-03/5.1)
- CHANGED VOL-II-5.2-02: wording (by ADD-03/5.1)
- CHANGED VOL-II-5.3-01: wording (by ADD-03/5.2)
- CHANGED VOL-II-5.3-02: wording (by ADD-03/5.2)
- CHANGED VOL-IV-F4D-01: secondary units VOL-IV:F4-D/guarantor-ultimate-parent-of-epc-contractor, VOL-IV:F4-D/jurisdiction-of-incorporation, VOL-IV:F4-D/epc-contractor-guaranteed, VOL-IV:F4-D/guaranteed-obligations, VOL-IV:F4-D/limit-of-liability, VOL-IV:F4-D/expiry, VOL-IV:F4-D/governing-law, VOL-IV:F4-D/signature, VOL-IV:F4-D/name-and-capacity, VOL-IV:F4-D/date, VOL-IV:F4-D/corporate-authority-reference annotated by ADD-03/Q15 (by ADD-03/Q15)
- CHANGED VOL-IV-F4F-01: secondary units VOL-IV:F4-F/bidder, VOL-IV:F4-F/availability-payment-sar-per-annum-year-1-of-operations, VOL-IV:F4-F/availability-payment-in-words, VOL-IV:F4-F/estimated-project-cost-sar, VOL-IV:F4-F/assumed-senior-debt-tenor-years-from-financial-close, VOL-IV:F4-F/assumed-senior-debt-margin-bps, VOL-IV:F4-F/assumed-gearing-debt-equity, VOL-IV:F4-F/project-irr-nominal-post-tax, VOL-IV:F4-F/equity-irr-nominal-post-tax, VOL-IV:F4-F/indexation-basis-assumed, VOL-IV:F4-F/model-auditor, VOL-IV:F4-F/date-of-model-audit-opinion, VOL-IV:F4-F/signature, VOL-IV:F4-F/name-and-capacity, VOL-IV:F4-F/date annotated by ADD-03/Q16 (by ADD-03/Q16)

### Stale readings and decisions

- STALE VOL-I-11.3-01: ADD-02:T1-1-rev/note(1) changed since ADD-02 (by ADD-03/6.1); new dependency ADD-03:S6/para1; VOL-I:11.3 changed since ADD-02 (by ADD-03/6.2(a), ADD-03/S6/para1(a)); quote not found in the effective text at ADD-03: 'scor
- STALE VOL-I-8.4-01: VOL-I:8.4 changed since BASE (by ADD-03/3.1); quote not found in the effective text at ADD-03: '(a) a consolidated tangible net worth of not less than SAR 8' (expected: the interpretation predates the change)
- STALE VOL-II-5.2-01: new dependency ADD-03:Q18; VOL-II:5.2 changed since BASE (by ADD-03/5.1, ADD-03/Q18); quote not found in the effective text at ADD-03: 'The main shall be sized for the peak hourly flow in Table 2-' (expected: the interpr
- STALE VOL-II-5.3-01: VOL-II:5.3 changed since ADD-01 (by ADD-03/5.2); quote not found in the effective text at ADD-03: 'Glass reinforced plastic pipe of an equivalent pressure clas' (expected: the interpretation predates the change)
- STALE VOL-IV-F4D-01: new dependency ADD-03:Q15; new dependency VOL-IV:F4-D/T1; new dependency VOL-IV:F4-D/T2; VOL-IV:F4-D/corporate-authority-reference changed since BASE (by ADD-03/Q15); VOL-IV:F4-D/date changed since BASE (by ADD-03/Q15); 
- STALE VOL-IV-F4D-02: new dependency ADD-03:Q15; new dependency VOL-IV:F4-D/T1; VOL-IV:F4-D/guaranteed-obligations changed since BASE (by ADD-03/Q15)
- STALE VOL-IV-F4D-03: new dependency ADD-03:Q15; new dependency VOL-IV:F4-D/T1; VOL-IV:F4-D/limit-of-liability changed since BASE (by ADD-03/Q15)
- STALE VOL-IV-F4D-04: new dependency ADD-03:Q15; new dependency VOL-IV:F4-D/T1; VOL-IV:F4-D/expiry changed since BASE (by ADD-03/Q15)
- STALE VOL-IV-F4D-05: new dependency ADD-03:Q15; new dependency VOL-IV:F4-D/T1; VOL-IV:F4-D/governing-law changed since BASE (by ADD-03/Q15)

### Obligations not reaching the outputs (C46)

- ADD-03/cover/para3 [A3]: ADD-03/cover/para3 brings in consequence words ['liquidated damages'] that no row's consequence carries at ADD-03: 'This Addendum amends the definition of Estimated Project Cost, the financial capacity requirement in Volume I Clause 8.4 and
- ADD-03/6.1 [A1]: ADD-03/6.1 (replace_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Table 1-1 (revised) and the Notes to it, issued by Section 3 of Addendum No. 2, are deleted and replaced by the table and Notes below, which
- ADD-03/8.1 [A1]: ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the item inserted after VOL-I:9.1; a row of the anchor VOL-I:9.1 does not count): 'A new Form 4-H (Declaration of Beneficial Ownership) is add
- ADD-03/8.1 [A1]: ADD-03/8.1 (insert_unit) creates or amends an obligation that no A1 row in force at ADD-03 holds (the new ADD-03:F4-H; a row of the anchor VOL-I:9.1 does not count): 'A new Form 4-H (Declaration of Beneficial Ownership) is added to Volume I
- ADD-03/8.1 [A3]: ADD-03/8.1 brings in consequence words ['non-responsive', 'غير مستجيب'] that no row's consequence carries at ADD-03: 'A new Form 4-H (Declaration of Beneficial Ownership) is added to Volume IV and to the list at Volume I Clause 9.1, to be i
- ADD-03/8.2 [A1]: ADD-03/8.2 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Form 4-H shall be completed in the Arabic language, signed and stamped by an authorised signatory of each member of the Bidder. The Arabic text 
- ADD-03/8.2 [A3]: ADD-03/8.2 brings in consequence words ['non-responsive', 'غير مستجيب'] that no row's consequence carries at ADD-03: 'Form 4-H shall be completed in the Arabic language, signed and stamped by an authorised signatory of each member of the Bi
- ADD-03/8.3 [A1]: ADD-03/8.3 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Form 4-H shall be submitted with Envelope A. A member of the Bidder that is incorporated outside the Kingdom may instead submit its Form 4-H thr
- ADD-03/8.3 [A3]: ADD-03/8.3 brings in consequence words ['non-responsive', 'غير مستجيب'] that no row's consequence carries at ADD-03: 'Form 4-H shall be submitted with Envelope A. A member of the Bidder that is incorporated outside the Kingdom may instead s
- ADD-03/8.4 [A1]: ADD-03/8.4 (annotate) creates or amends an obligation that no A1 row in force at ADD-03 holds: 'Failure to submit a complete and properly executed Form 4-H for each member of the Bidder by the time required by Section 8.3 shall render the P
- ADD-03/8.4 [A3]: ADD-03/8.4 brings in consequence words ['non-responsive', 'غير مستجيب'] that no row's consequence carries at ADD-03: 'Failure to submit a complete and properly executed Form 4-H for each member of the Bidder by the time required by Section 

### Reached through relationships (indirect: for review, not direct citations)

Curated links (relationships file) followed from what changed. The requirements above cite a changed unit; these are reached through another provision, in three classes that are never merged. A5 marks the activities that serve them REVIEW with their dates unchanged.

#### Confirmed dependency (0)
- none

#### Proposed relationship (1)
- VOL-II-5.4-01 (row; ACTIVE) <- VOL-II-5.3-01 via REL-AI-001 [cites; link proposed]; also changed directly

#### Possible impact (10)
- VOL-I-8.10-01 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-DEBARMENT [member_scope; link possible]
- VOL-I-8.2-01 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-MULTIPLE-PARTICIPATION [member_scope; link possible]
- VOL-I-8.4-01 (row; AMENDED (ADD-03/3.1)) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FIN-STANDING [member_scope; link possible]; also changed directly
- VOL-I-8.4-02 (row; AMENDED (ADD-03/3.1)) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FIN-STANDING [member_scope; link possible]; also changed directly
- VOL-I-8.9-01 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-INVESTMENT-LICENCE [member_scope; link possible]
- VOL-I-9.4-01 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FORM-4C [member_scope; link possible]
- VOL-IV-F4C-02 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-MULTIPLE-PARTICIPATION [member_scope; link possible]
- VOL-IV-F4C-03 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-DEBARMENT [member_scope; link possible]
- VOL-IV-F4C-N1 (row; ACTIVE) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FORM-4C [member_scope; link possible]
- calc:financial-standing (calculation) <- words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FIN-STANDING [member_scope; link possible]

#### Referenced but not supplied: conclusions in play that cannot be established (0)
- none

### Disqualifiers (A3)

- no change

### Programme impact (status date 2026-10-22 -> 2026-11-09)

- REWORK fin-model-build: requirement changed: VOL-IV-F4F-02
- REWORK fin-model-freeze: requirement changed: VOL-IV-F4F-02
- REWORK fin-standing: requirement changed: VOL-I-8.4-01, VOL-I-8.4-02
- REWORK fin-statements: requirement changed: VOL-I-8.4-01, VOL-I-8.4-02
- REWORK form-4a: requirement changed: ADD-03-cover-01
- REWORK form-4a-prep: requirement changed: ADD-03-cover-01
- REWORK form-4f: requirement changed: VOL-IV-F4F-01, VOL-IV-F4F-02
- REWORK pcg-execution: requirement changed: VOL-I-8.7-01, VOL-IV-F4D-01, VOL-IV-F4D-02, VOL-IV-F4D-03, VOL-IV-F4D-04, VOL-IV-F4D-05, VOL-IV-F4D-06, VOL-IV-F4D-07, VOL-IV-F4D-08
- REWORK pcg-wording: requirement changed: VOL-I-8.7-01, VOL-IV-F4D-01, VOL-IV-F4D-02, VOL-IV-F4D-03, VOL-IV-F4D-04, VOL-IV-F4D-05, VOL-IV-F4D-06, VOL-IV-F4D-07, VOL-IV-F4D-08
- REWORK technical-proposal: requirement changed: VOL-I-11.3-01, VOL-I-T1-1-A, VOL-I-T1-1-B, VOL-I-T1-1-C, VOL-I-T1-1-D, VOL-I-T1-1-E, VOL-I-T1-1-F, VOL-II-1.4-01, VOL-II-5.2-01, VOL-II-5.2-02, VOL-II-5.3-01, VOL-II-5.3-02, VOL-II-5.4-01, VOL-II-5.4-02
- REVIEW (possible impact) fin-standing: VOL-I-8.4-01, VOL-I-8.4-02 reached from words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FIN-STANDING; dates unchanged
- REVIEW (possible impact) fin-statements: VOL-I-8.4-01, VOL-I-8.4-02 reached from words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-FIN-STANDING; dates unchanged
- REVIEW (possible impact) form-4c-prep: VOL-I-8.10-01, VOL-I-8.2-01, VOL-I-9.4-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-N1 reached from words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-DEBARMENT, REL-MEMBER-FORM-4C, REL-MEMBER-MULTIPLE-PARTICIPATION; dates unchanged
- REVIEW (possible impact) form-4c-sign: VOL-I-8.10-01, VOL-I-8.2-01, VOL-I-9.4-01, VOL-IV-F4C-02, VOL-IV-F4C-03, VOL-IV-F4C-N1 reached from words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-DEBARMENT, REL-MEMBER-FORM-4C, REL-MEMBER-MULTIPLE-PARTICIPATION; dates unchanged
- REVIEW (possible impact) investment-licence: VOL-I-8.9-01 reached from words:consortium member, words:member of the Bidder, words:member of the consortium via REL-MEMBER-INVESTMENT-LICENCE; dates unchanged
- REVIEW (proposed relationship) technical-proposal: VOL-II-5.4-01 reached from VOL-II-5.3-01 via REL-AI-001; dates unchanged
- FEASIBILITY lcc-ratio: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD
- FEASIBILITY lcc-certificate: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD
- FEASIBILITY fin-model-build: OK -> INFEASIBLE by 10 WD
- FEASIBILITY model-auditor-appoint: OK -> INFEASIBLE by 9 WD
- FEASIBILITY pcg-wording: OK -> INFEASIBLE by 9 WD
- FEASIBILITY technical-proposal: OK -> INFEASIBLE by 9 WD
- FEASIBILITY ground-dd: OK -> INFEASIBLE by 5 WD
- FEASIBILITY lender-terms: OK -> INFEASIBLE by 5 WD
- FEASIBILITY completion-certs: OK -> INFEASIBLE by 4 WD
- FEASIBILITY model-audit-review: OK -> INFEASIBLE by 9 WD
- FEASIBILITY poa-resolutions: OK -> INFEASIBLE by 4 WD
- FEASIBILITY references: OK -> INFEASIBLE by 3 WD
- FEASIBILITY bond-approval: OK -> INFEASIBLE by 2 WD
- FEASIBILITY deviations-review: OK -> INFEASIBLE by 1 WD
- FEASIBILITY pcg-execution: OK -> INFEASIBLE by 9 WD
- FEASIBILITY poa: OK -> INFEASIBLE by 4 WD
- FEASIBILITY fin-model-freeze: OK -> INFEASIBLE by 10 WD
- FEASIBILITY investment-licence: OK -> INFEASIBLE by 4 WD
- FEASIBILITY model-audit-opinion: OK -> INFEASIBLE by 10 WD
- FEASIBILITY form-4b-prep: OK -> INFEASIBLE by 3 WD
- FEASIBILITY bond-issue: OK -> INFEASIBLE by 2 WD
- FEASIBILITY form-4c-sign: OK -> INFEASIBLE by 2 WD
- FEASIBILITY fin-assumptions: OK -> INFEASIBLE by 7 WD
- FEASIBILITY form-4e: OK -> INFEASIBLE by 1 WD
- FEASIBILITY form-4f: OK -> INFEASIBLE by 7 WD
- FEASIBILITY form-4b: OK -> INFEASIBLE by 3 WD
- FEASIBILITY assemble-envelope-a: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD
- FEASIBILITY assemble-envelope-b: OK -> INFEASIBLE by 10 WD
- FEASIBILITY copies: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD
- FEASIBILITY seal-and-mark: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD
- FEASIBILITY deliver: INFEASIBLE by 12 WD -> INFEASIBLE by 24 WD

## Next (a person)

- read the unresolved and escalated provisions first, then each item against its evidence (`../ai/ADD-03-run-host-blind04-s11-20261004T222214Z-combined/proposals.yaml`, `../downstream/proposals.yaml`)
- nothing here is applied to the real curation: to take an item over, add the PDF to the pack (OPERATING_GUIDE §3 steps 1-2) and copy the reviewed files listed in `promotion.json`; then `pin`, `check-register`, `outputs` and decide with `accept` / `reject` as usual
