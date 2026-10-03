# Tender Pack Reader: Engineering Plan

> **STATUS (revision 7, session 07, 2026-10-03):**
> - **Direction:** accepted by the owner (session 02).
> - **Stage 1 (evidence and units):** implemented in session 02, revised in sessions 03 and 04 after the owner's reviews (§9). Formal acceptance is still open. The two image readings are **pending the owner's review**; nothing has been approved.
> - **Stage 2 (the amendment path):** built in session 04 (§10). The owner's code reviews of it were reproduced and fixed: five findings in session 05 (§11), four in session 06 (§12).
> - **Stage 3 (full register) and Stage 4 (A5):** built in session 05 as working drafts (§11): every volume unit has a disposition, every addendum provision is treated, 202 A1 rows; A5 covers both envelopes with counts, issuers, resources, infeasibility drivers and scenarios. **Every row, op and lead time is a PROPOSAL**: structurally checked, not reviewed; a strict release is refused until people review them (§11). Session 06 added the named decision workflow (`accept`/`reject`, D8) and review batches; no decision has been recorded (§12).
> - **Stage 5 (unseen-addendum readiness):** two synthetic drills (A, session 04; B, session 05) and **one blind rehearsal** (session 06, §12): an Addendum No. 3 written by an independent agent, with its answer key frozen by hash before the start. 22 hits, 4 partials, 1 miss; 12 min 13 s from receipt to replanned outputs; four live fixes. `show ROW` and `diff` built.
> - **Stage 6 (packaging, Mac verification, final submission):** a **draft** archive organised around A1–A5 (session 06, §12), verified in the cloud container (extraction, links, a bundle clone, an offline install and rebuild, the tests). Mac verification is given as exact commands (`docs/VERIFY_ON_MAC.md`); it has not been run on a Mac. Final submission is not started.
> - **Integrations and model selection** (Claude Code in the app, OpenRouter, local Ollama): designed in §4.6, deliberately **not implemented**; the reviewed build runs offline with no model.
> - **Session 07:** C28 built (each addendum's cover summary against its provisions; report only, never applied); the drafter no longer drafts changes from cover text; the full packets of both image readings ship with the review batches (§13). The owner kept the full git history as it is.
> - This revision is one consistent document. Earlier revisions are summarised in the history below and kept in the work log; where they differed, the text below is current.

| Revision | Session | What changed | Record |
|---|---|---|---|
| 1 | 01 (1 Oct) | Planning only: findings, critique, architecture, staged plan | `worklog/2026-10-01_session-01_planning.md` |
| 2 | 02 (2 Oct) | Owner adjustments: email assumptions and formats adopted (A1 includes Excel; bidder details configurable); explicit disqualifiers kept apart from obligations with no stated consequence; target verification by citation (§4.4.1); evidence kept apart from effective text (§4.3); dependency pins and two build states (§4.10); image/Arabic foundation (§4.11); model routes designed (§4.6); TN/Permit claim withdrawn (F8); O5 wording corrected. Stage 1 built. | `worklog/2026-10-02_session-02_stage1.md` |
| 3 | 03 (2 Oct) | Owner's Stage 1 review: six gaps reproduced and fixed: numbered-paragraph and table-continuation boundaries; structural failures fail the build (C07–C10, exit codes); approvals cover reading + uncertainties + evidence and need a named reviewer; table readings validate every cell and keep numbers apart from meaning; drawings of straight lines and dark boxes stay visible; output paths guarded and builds swapped in only on success. Planned check IDs renumbered to avoid the new C07–C10. | `worklog/2026-10-02_session-03_review-fixes.md` |
| 4 | 04 (2 Oct) | Owner's second review: C10 extended to per-cell order, normalized text and anchor page/geometry/crops; Latin expressions inside Arabic laid out correctly, digits-only verification labelled PARTIAL; `--require-approved` gate applied before publishing. Stage 2 built (§10): amendment engine with one path for existing and future addenda, date rules with every counting reading, register slice with pinned interpretations and STALE, A1/A2/A3/A5; ADD-03 drill. D3, D4, D7 applied as the owner directed (§7). The hiring team's reply of 2 Oct recorded (§0). | `worklog/2026-10-02_session-04_repairs-and-stage2.md` |
| 5 | 05 (2 Oct) | Owner's code review: five findings reproduced, failing tests first, fixed (transactional ops; value, column and replacement-content checks; two changes in one paragraph; evidence verified against the manifest; review fingerprint pinned; latest source cited, original quotations kept apart from effective text; A5 checked in both directions, C44/C45). Stage 3 (dispositions for every unit, 202 rows, C14/C15 sweeps in English and Arabic, "outside the slice" replaced by treatment) and Stage 4 (both envelopes, counts, issuers, resources, drivers, scenarios) built as working drafts; release gate (`outputs --strict`, exit 3); readable one-page A3 with linked detail; drill B rehearsal (§11). | `worklog/2026-10-02_session-05_review-stage3-stage4.md` |
| 6 | 06 (3 Oct) | Owner's code review: four findings reproduced, failing tests first, fixed (inserted content needs evidence for the whole change, C21 and the new structural C47; an exception after "unchanged" wording is unresolved; new and amended obligations traced to A1/A3/A5, C46; the release gate counts only decisions bound to content; A3 keeps each item's confidence and the full requirement text; "slice" labels replaced). `accept`/`reject` (D8), stale-row proposals (`apply-proposal`), review batches; `show ROW`, `diff`; C12 (id ledger), C30 (date coverage, `unresolved` kept explicit), C32 (counting conventions); months and weeks; renumbering; summary currency. Blind rehearsal (§12). Draft archive, operating guide, cost and effort. | `worklog/2026-10-03_session-06_review-accept-blind-archive.md` |
| 7 | 07 (3 Oct) | C28 built: claims parsed from each cover summary and matched to the provisions' ops (citations, register anchors, answer ranges, best-matching description); omissions, understatements, unmentioned consequences, contradictions and unsupported claims reported in A2, A1 Issues, `diff` and checks.json, never applied. The drafter drafts no change from cover text. Review packets copied into the review folder. Archive rebuilt and verified. | `worklog/2026-10-03_session-07_cover-summary-archive.md` |

Conventions used throughout:

- **Doc IDs:** `VOL-I`, `VOL-II`, `VOL-IV`, `VOL-V`, `ADD-01` and `ADD-02` are the six tender PDFs in `sources/candidate_pack/`.
- **Pages:** "p4" is the **PDF page index**. In the tender pack the printed footer "Page N" equals the PDF page. In the brief, printed page N is PDF page N+1, because the schedule page is inserted at the front.
- **Fact labels:** **[F]** marks what a document says. **[I]** marks my interpretation, which needs human confirmation. **[D]** marks a design proposal. Human decisions are listed explicitly.
- **Quotations** are verbatim from the PDFs, apart from whitespace and line breaks.

---

## 0. Time budget (drives every trade-off below)

- **Original schedule** (brief PDF p1; covering email): deadline 17:00 Wed 23 Sep 2026; session 12:00 Fri 25 Sep 2026, Riyadh time.
- **Revised schedule** (`sources/correspondence/2026-09-29_reply_to_hiring.md`): the owner chose "the second path", starting Tue 29 Sep, "with 17:00 Monday 5 October as the outside limit".
- **Time left:** at revision 3 (04:00 Fri 2 Oct, Riyadh) about 3 days 13 hours remain to the outside limit.
- **Correspondence:** the Gmail thread PDF in `sources/correspondence/` shows:
  - the hiring team offered the second path on 17 Sep 20:00, and the owner chose it on 17 Sep 20:12;
  - the session is "a ninety-minute slot in the week of 6 October (we will confirm once the panel locks times)", so it is **still to be confirmed**;
  - the 1 Oct email was **sent** (12:50);
  - **the hiring team replied** on Thu 1 Oct 17:51 PDT (Fri 2 Oct 03:51 Riyadh; `sources/correspondence/2026-10-02_reply_from_hiring.eml`, recorded in session 04): tools as described are fine, including in the live session, if documented; the pack is complete as provided (Volume III and Drawing 03-C-114 to be treated as referenced but not supplied, with the gaps and their impact flagged, "part of the exercise"); Addendum 3 will be a PDF in the same format as Addenda 1 and 2, shared at the start of the live session; no written clarifications have been issued to other candidates; the A5 basis is fine (latest addendum date as planning date; consortium and external assumptions editable and clearly labelled); the single archive and formats work; delivery "by 17:00 Monday 5 October at the latest". The session slot is still not confirmed;
  - the note file `2026-09-29_reply_to_hiring.md` is headed "29 September", but the reply it quotes was sent on 17 September.

The plan is sized for roughly 3.5 working days, with a hard requirement that the session environment runs offline on the owner's Mac.

---

## 1. Understanding of the assignment

### 1.1 Deliverables (verified against the brief, §3, PDF p4–p5)

| Artefact | What the brief requires (quoted or closely paraphrased) | Notes |
|---|---|---|
| **A1** Obligations and compliance register | "One row per requirement." Columns: identifier; **verbatim source text**; **document, clause and page**; **pass/fail or scored**; **discipline that owns it**; **evidence needed**; **status after each addendum**; **confidence**. "Machine-readable — CSV or JSON — plus whatever interface you prefer." | "Status after each addendum" requires one status column per stage, not just a final value. **Formats (owner's sent email of 1 Oct): CSV + JSON + Excel.** |
| **A2** Addendum reconciliation | "What each addendum changed, added and deleted. Which register rows move as a result. Which earlier answers are now wrong. We must be able to trace any row back through the chain to the original document." | Needs the full operation history, not a before/after diff alone. Formats: Markdown + CSV/JSON. |
| **A3** One page: what would disqualify us | "Every requirement whose breach would put a bid out — **the ones the documents themselves say cause rejection, disqualification or non-responsiveness, not every obligation in the pack** — with your confidence in each. And, explicitly, the list of things your system could not resolve, and why. We read this page first." | The inclusion test is explicit document wording (D2). One page, PDF, is a hard constraint. |
| **A4** Work log | "The repository with its real commit history. The prompts and model calls you used. And a short written note of every place your system was wrong while you were building it, and how you caught it." | Timestamped and append-only, kept separate from the deterministic outputs. Records the owner's prompts for each session and every error, including the assistant's. |
| **A5** Bid programme and marshalling plan | "Generated by your system from A1 — not drawn by hand." **Programme:** activities, durations, dependencies, owners by discipline, resources. "Every activity must carry the requirement ID or IDs from A1 that it discharges, and **every date must be computed backwards from the deadline, not typed in**." **Marshalling plan:** "every physical and documentary item the pack requires, who issues it, how long that takes, and the drop-dead date to start it." Output is data (CSV/JSON); a chart is optional and is not the deliverable. | Scoring (§6): "does it survive the lead times the documents actually impose". |

### 1.2 Constraints (brief §4 and §6, PDF p5–p7)

- **Not allowed:** chat interface, multi-agent framing, components named after departments, a dashboard-as-product, a landing page, a logo, a product name, a roadmap, a strategy document, or "this could be extended to…".
- **Automatic fails:**
  1. Asserting a requirement with no source and no flag.
  2. Being unable to show the clause and page for a row within a minute.
  3. Being unable to make a code change in the session.
  4. Submitting anything other than the five artefacts.
  5. Letting the tool decide a commercial or legal question. "Some things in this pack cannot be settled by software, and one of them has no correct answer at all."
- **Marks:** accuracy 15, reconciliation 10, live change 30, programme 15, calibration 10, teach-back 10, cost/scale/automation line 10. Fifty marks depend on the live session.

### 1.3 Live-session demands and what they imply for design

| Minutes | Demand | Design implication [D] |
|---|---|---|
| 0–10 | Three random rows: show clause and page | A `show <ROW-ID>` command prints the verbatim text, doc/clause/page and the amendment chain, and renders a highlighted crop of the page region. Target: under 30 s. |
| 10–40 | Unseen ADD-03: ingest it, say what it broke, replan | The new-addendum path must be the same code path used for ADD-01/02. It must account for every provision (not trust the cover summary), produce a stage diff ("what broke"), mark stale rows, and re-run A5. Rehearsed on synthetic addenda before submission. |
| 40–58 | "We name something your system got wrong" → fix so it catches *that kind* of error | Checks live in a small registry of independent rule functions with data-driven lexicons. A new check is one function plus one test. Rehearsed. |
| 58–70 | Teach-back to a non-technical bid coordinator | A one-page operating procedure (5 commands, what to read first). A3 is designed to be read cold. |
| 70–85 | Cost per bid at 8 bids, where it falls over, what not to automate | Log real timings for human review minutes per row and per op, and model tokens per call. Answer from data. |

### 1.4 What I inspected, and how

- **All 32 tender pages, text:**
  - Extracted with `pdftotext` (raw and `-layout`) and with PyMuPDF span-level output (font, size, colour, superscript flag, bbox, text direction).
  - Every page's text read in full.
- **All 32 tender pages, non-text content:**
  - Image objects: exactly **two** raster images in the pack. VOL-II p3 (Table 2-4) and VOL-IV p6 (Form 4-C, Arabic). Both extracted at native resolution and read.
  - Vector drawings on every page: only greyscale table rules, header and label fills, and two thin black separators (the VOL-I p4 footnote rule and the ADD-02 p1 rule above the table notes). No highlights, stamps or strike-throughs.
  - Annotations, links, form widgets, embedded files: **none**. Optional-content layers: none listed.
  - White text not on a dark fill: **none**. Off-page text: **none**.
  - The rotated watermark "FICTIONAL — ASSESSMENT PACK" is present on every page.
- **Rendered pages viewed visually:** VOL-I p4, VOL-II p3, VOL-IV p3, ADD-01 p3, ADD-02 p1, plus both raw images. I did **not** visually inspect every rendered page. The checks above are why I believe nothing on the other pages exists outside the text layer, but that is a programmatic claim, not a visual one.
- **The brief** (7 PDF pages), the **covering email** image, and the two **correspondence** notes.

**Limitations:**

- **Volume III (Drawings) is not in the pack.** This is consistent with the brief's "Six documents, thirty-two pages" (7+5+9+4+4+3 = 32), but Volume III is referenced in VOL-I §3.1, §3.2(f) and VOL-II §5.1 (Drawing 03-C-114).
- **Correspondence:**
  - The 1 Oct email to the hiring team was **sent** (Gmail thread PDF in `sources/correspondence/`); its assumptions and formats are adopted (D1, §1.1). The markdown note `2026-10-01_questions_to_hiring.md` is labelled as a draft; the thread is the record.
  - The hiring team's reply (2 Oct) confirms the approach on all six points (§0).
- **Arabic:** my reading of Form 4-C is a model reading. The owner reads Arabic and will review it; until then it is pending and is not relied on.
- **No OCR engine** is used. The two images were read visually (AI-assisted) and are recorded as proposed readings with crops, pending the owner's review.
- **This is not a register.** The inventories below are findings from a careful read. I have **not** established complete coverage of every obligation; that is what the system's coverage checks are for.

---

## 2. Source-grounded findings

### 2.1 Your six observations: verdicts

| # | Finding | Doc · clause · PDF page | Supporting quotation | Effect after ADD-02 | Uncertainty / human decision |
|---|---|---|---|---|---|
| O1 | **Confirmed.** Footnote 12 carries a rejection rule that the clause body lacks. **Added:** in pdftotext the marker reads as "Form 4-B.12", which looks like a form ID. The marker is a 7.7 pt superscript. The footnote's own label "12" is 5.8 pt and is **not** flagged as a superscript, so superscript detection alone cannot pair marker and body. Unit superscripts (m³) appear at VOL-I p2 (§1.3), p4 (§8.8 and *inside the footnote*), VOL-II p2 (§2.1), p3 (§3.4 "OU/m³", Table 2-6), p4 (Table 2-6), VOL-IV p4 (Form 4-B) and ADD-02 p2 (Q11). There is a subscript in "BOD5" (VOL-II Table 2-2). | VOL-I §8.5 fn 12, p4 | "For the avoidance of doubt, a Bidder that does not evidence at least two (2) reference sewage treatment plants, each of nominal capacity not less than 80,000 m3/day and each having achieved commercial operation within the ten (10) years preceding the Proposal Due Date, shall be rejected without further evaluation." | [F] Rejection rule unchanged. The look-back is re-anchored to the new PDD by ADD-01 §2.2 (which names "footnote 12"). ADD-01 Q5: plants under construction do not count. [F] VOL-I §9.5: a reference without a completion certificate "will be disregarded", which can cascade into this rejection. | [I] Whether the boundary of "within the ten (10) years preceding" is inclusive. [I] Footnote says "sewage treatment plants"; body says "wastewater treatment facilities". The bidder's reference data is not in the pack. |
| O2 | **Confirmed.** The note sets 65/35 and is in small print: 7.2 pt against 9.6 pt body text. The cover summary says only "reissues the technical evaluation table". **Added:** ADD-01 Appendix B (minutes) Item 3 records a non-binding "seventy / thirty split" statement, a third competing value. The same words "sixty per cent (60%) … forty per cent (40%)" also appear in VOL-V §29.2 (indexation), which must **not** change. | ADD-02 §3, Notes to Table 1-1 (revised), note (2), p1 | "(2) The combined score weighting stated in Volume I Clause 11.2 is amended to sixty-five per cent (65%) technical and thirty-five per cent (35%) commercial." | [F] VOL-I §11.2 is effectively 65/35. The §11.3 threshold of 70 is unchanged (note 1). Table 1-1: B 20→15, D 15→20, total 100 (matches the narrative in ADD-02 §3.1). | None on the reading. It is a scored or evaluation parameter, not pass/fail, so it changes bid strategy, not compliance. |
| O3 | **Confirmed.** Original → deleted → reinstated, amended, with a new consequence. **Added:** ADD-01 §4.2 is itself a rule ("disregard references elsewhere"), and ADD-02 §9.2 **revokes** it, which is an amendment of an amendment. The threshold also rises from 30% to 35%. The original §8.6 had **no** stated consequence. The minutes record that bidders find the certificate hard to obtain in time. A grep shows no other LCC references exist in the pack, apart from the generic VOL-I §9.1(i) "certificates and evidence required under Section 8". | VOL-I §8.6 p4; ADD-01 §4.1–4.2 p1; ADD-01 App B Item 4 p4; ADD-02 §9.1–9.2 p3 | Original: "…not less than thirty per cent (30%) for the construction phase." ADD-01 §4.1: "is deleted in its entirety. No Local Content Certificate is required with the Proposal." ADD-02 §9.1: "…not less than thirty-five per cent (35%) for the construction phase. Failure to submit the certificate shall render the Proposal non-responsive." §9.2: "Section 4.2 of Addendum No. 1 ceases to have effect." Minutes: "A Bidder raised difficulty in obtaining a Local Content Certificate within the programme." | [F] Active, 35%, construction phase, explicit non-responsiveness. It enters A3 **only after ADD-02**. Between 8 Oct and 22 Oct it was deleted. | "Competent authority" is not named. Lead time is not stated, but the pack signals it is long. Only 24 Working Days separate ADD-02 issue and the PDD. The bidder's local-content ratio is unknown. **A5 feasibility is a real risk to surface, not assume away.** |
| O4 | **Confirmed, and larger than observed.** The reissued Form 4-A prints the old date. It is also a **much shorter form**. It drops commercial registration number, registered address, contact email/telephone, all six numbered confirmations (150-day validity, bid bond enclosed, no multiple participation, Pre-Bid attendance, Authority not bound), signatory name/capacity split, Power of Attorney reference and date, and company seal. Its stated purpose is "to add the acknowledgement of Addenda at paragraph 1", yet it has **no paragraph 1**, and the original already acknowledged addenda in its paragraph 1. | ADD-01 §2.1 p1; ADD-01 App A p3; VOL-IV Form 4-A p3; VOL-IV p2; VOL-I §9.3 p5 | ADD-01 §2.1: "deleting 'Thursday 12 November 2026' and substituting 'Thursday 26 November 2026'". App A: "Bidders shall use this version." … "Proposal Due Date \| 12 November 2026, 14:00 Riyadh time". VOL-IV p2: "Forms shall be reproduced without alteration to their wording. A Bidder that alters the wording of a Form does so at its own risk." VOL-I §9.3: "An unsigned or improperly executed Form 4-A shall render the Proposal non-responsive." | [F] PDD = Thu 26 Nov 2026, 14:00 (VOL-I §6.1 as amended; precedence §3.2(a)). The mandated form prints 12 Nov. ADD-02 again requires acknowledgement "in Form 4-A" but does not reissue it. | **Human decision:** what date to print and sign; whether to also give the dropped confirmations; whether to raise a clarification **before the 12 Nov cut-off**. The system must flag this, **never auto-correct** it. |
| O5 | **Confirmed. Additional finding: a second image region exists** (the observation did not claim there was only one). VOL-IV p6 is a single raster image. The page is *not* text-empty: it carries the running header, the footer and the rotated watermark as text, so a "page has text ⇒ covered" heuristic would wrongly pass it. Coverage must be judged per image region (C05), not per page. My reading (to be verified by an Arabic reader) is listed after this table. **Declaration 4 carries an exclusion consequence that appears nowhere in the English text.** **Additional finding:** VOL-II p3 **Table 2-4 (effluent limits) is also an image.** ADD-02 §5.1 amends TN "from the value shown", so the old value (5 mg/l) exists **only in the image**. | VOL-IV p5–p6; VOL-II p3; ADD-02 §5.1 p1; ADD-02 Q9 p2 | Form 4-C decl. 4: "وندرك أن أي بيان غير صحيح يؤدي إلى استبعاد العرض" ("we acknowledge that any incorrect statement leads to the exclusion of the proposal"). Note: "عدم تقديمه كاملاً يجعل العرض غير مستجيب" ("failure to submit it completely renders the proposal non-responsive"). ADD-02 §5.1: "the limit for Total Nitrogen (TN) is amended from the value shown to 3 mg/l, assessed on the same basis." | [F] Form 4-C remains mandatory in Arabic, one per member (ADD-02 Q9). TN = 3 mg/l, 30-day rolling average ("same basis" resolved from the image). | Arabic transcription and translation are **pending the owner's review**. The order of "البند ٤-٢" is settled (logical 4-x); whether the second digit is ٢ (§4.2) or ٣ (§4.3) is not, and is the owner's decision. |
| O6 | **Confirmed. ADD-01's list is explicitly non-exhaustive** ("including without limitation"). **Added:** VOL-I §8.3, "ISO 9001:2015 … current as at the Proposal Due Date", also moves but is not in ADD-01's list. **Added:** the new clarification cut-off falls on **Thu 12 Nov 2026, the old PDD**. A naive stale-value scan for "12 November 2026" would mis-flag it. | ADD-01 §2.2 p1; VOL-I §2.4, §2.6, §3.4, §5.2, §6.3, §6.7, §7.1, §8.3, fn 12, App 3; VOL-IV Form 4-A ¶2 | ADD-01 §2.2: "Every period in the RFP Documents that is calculated by reference to the Proposal Due Date is adjusted accordingly, including without limitation…" VOL-I §2.4: "Where a period expressed in Working Days is to be counted backwards from a stated date, the stated date itself shall not be counted." | See §2.5 (date inventory): computed values before and after, fixed dates, and dates anchored to unknown future events. | "days" is undefined (calendar days assumed). Whether "from the PDD" makes the PDD day 0 is unstated. The forward Working-Day convention is unstated. No time-of-day for the cut-off. Public holidays "declared" in the Kingdom need a calendar input (assumption). |

**My reading of Form 4-C (VOL-IV p6). AI-assisted reading; pending the owner's review.** Header: "الهيئة الشمالية للمشتريات المرفقية" / "النموذج ٤-ج" / "إقرار عدم تضارب المصالح وعدم الإدراج في قوائم الحظر" (declaration of no conflict of interest and non-listing on debarment lists). The signatories, as authorised representatives of the named consortium member, declare:

1. There is no actual or potential conflict of interest between them and the Authority or any of its advisors regarding this project.
2. The company has not participated, directly or indirectly, in more than one proposal for this tender.
3. The company is not, and has not been in the previous five years, listed on any debarment list issued by a government entity in the Kingdom.
4. All information in the proposal is correct and complete, and any incorrect statement leads to exclusion of the proposal.
5. The signatories commit to the communication rules in clause 4-2 of Volume I. **The left digit's identity, ٢ or ٣, is uncertain; ٣ would mean clause 4-3, VOL-I §4.3. It is one of the owner's review decisions (packet VOL-IV-p6-r1).**

Fields: member name, commercial registration number, authorised signatory, capacity, date, signature and seal. Note: the form must be submitted in Arabic for each member, and incomplete submission renders the proposal non-responsive.

**Table 2-4 (VOL-II p3). My reading.** Header: "(all values are maxima; compliance assessed as a 30-day rolling average unless stated)".

| Parameter | Limit | Basis of assessment |
|---|---|---|
| BOD5 | 10 mg/l | 30-day rolling average |
| COD | 50 mg/l | 30-day rolling average |
| TSS | 10 mg/l | 30-day rolling average |
| **TN** | **5 mg/l** | 30-day rolling average |
| TP | 1 mg/l | 30-day rolling average |
| Turbidity | 2 NTU | maximum instantaneous |
| Faecal coliforms | 2.2 MPN/100 ml | maximum, any single sample |
| Residual chlorine | 0.5–1.0 mg/l | continuous at outlet |
| pH | 6.0–9.0 | continuous at outlet |
| Oil and grease | 1 mg/l | maximum, any single sample |

Note 1: "Where a parameter is not listed above, the limit stated in the Environmental Permit shall apply."

### 2.2 Additional findings

| # | Finding | Doc · clause · PDF page | Supporting quotation | Effect after ADD-02 | Uncertainty / human decision |
|---|---|---|---|---|---|
| F1 | [F] **Repeated wording in unrelated clauses**: real wrong-occurrence traps. | VOL-II §4.4 p4 vs VOL-V §31.3 p3; VOL-I §11.2 p5 vs VOL-V §29.2 p3; VOL-II Table 2-2 p2 vs Table 2-4 p3 (image); VOL-I §9.2 p5 vs §12.2 p6; VOL-I §6.1 p3 vs VOL-IV p3 vs ADD-01 p3 | "seventy-two (72) hours" (standby power vs cure period); "sixty per cent (60%) … forty per cent (40%)" (weighting vs indexation); "Total Nitrogen" (influent 55/80 vs effluent limit); "one hundred and twenty (120)" (pages vs days to Commercial Close); "12 November 2026" | Only the first-named member of each pair is amended (ADD-02 §4.1, §3 note 2, §5.1, §2.1; ADD-01 §2.1). | None on the reading. The design must prove scope. |
| F2 | [F] **ADD-01's cover summary is incomplete too.** It omits the Form 4-A reissue (App A) and the new §3.1 notification obligation. ADD-02's summary omits note (2), the §9.2 revocation, and the §7.1 amendment of the VOL-I §9.1 list. | ADD-01 p1; ADD-02 p1 | ADD-01: "This Addendum amends the Proposal Due Date, deletes one qualification requirement, amends Volume II Clause 5.3, publishes the minutes of the Pre-Bid Conference, and responds to clarification requests 1 to 6." | n/a | [D] Enumerate provisions from the body. Never use the summary as the change list; use it only as a cross-check. |
| F3 | [F] **Minutes are inside ADD-01 but are not binding.** | ADD-01 §3.2 p1; App B p4 | "Statements recorded in the minutes at Appendix B are a record of what was said and do not bind the Authority unless the substance is confirmed in the body of an Addendum." | App B items produce no requirement changes, but they are retained as context (e.g. the LCC lead-time signal). | [D] An explicit `no_effect` classification with a reason. Silence is not acceptable. |
| F4 | [F] **Envelope B contents conflict.** §10.1 allows only two documents, but §10.3 requires an auditor's opinion "accompanied" with the model, §10.6 requires a schedule "with Form 4-F", and §6.2 makes commercial information in Envelope A non-responsive. | VOL-I §10.1, §10.3, §10.6, §6.2 p3–p5 | "Envelope B shall contain only (a) Form 4-F … and (b) the Financial Model. No other document shall be placed in Envelope B." / "…accompanied by an opinion from an independent model auditor addressed to the Authority." | Unchanged by the addenda. | **Human/clarification.** [I] Form 4-F has fields for tenor, margin, gearing, model auditor and opinion date, which partly absorbs §10.6. The auditor's opinion document has no permitted home. |
| F5 | [F] **Form 4-B (Envelope A) asks for "Contract value (SAR equivalent)"** while §6.2 says "any price, rate, or other commercial information within Envelope A shall render the Proposal non-responsive." | VOL-IV p4; VOL-I §6.2 p3 | "The appearance of any price, rate, or other commercial information within Envelope A shall render the Proposal non-responsive." | Unchanged. | **Human/clarification.** [I] Probably aimed at this bid's pricing, but the literal reading conflicts. |
| F6 | [F] **Concession-term conflict, and the Authority declined to resolve it.** | VOL-I §12.1 p6; VOL-V §3.1 p2; ADD-02 Q7 p2; VOL-V Note p2 | VOL-I: "twenty-five (25) years commencing on the Project Commercial Operation Date". VOL-V: "twenty-five (25) years from the Effective Date". Q7: "The order of precedence at Volume I Clause 3.2 applies. The Authority does not consider further amendment necessary at this stage." VOL-V Note: "A deviation not listed in Form 4-E will be taken as accepted." | [I] By precedence, VOL-I ranks above VOL-V. But the agreement to be executed says Effective Date, and unlisted deviations are "taken as accepted". | **Legal/commercial decision for a person.** It drives the financial model: up to about 3 years' revenue, given the 36-month Scheduled PCOD (VOL-V §12.1). |
| F7 | [F] **Hydraulic figures are questioned, and the Authority did not answer.** | VOL-II Table 2-6 p3–p4; §4.1, §4.2, §5.2; ADD-02 Q11 p2 | Table 2-6: average 120,000 m³/day; peak hourly (design) 7,500 m³/h; storm "3 x dry weather flow" to full treatment. Q11 answer: "Bidders shall design to the figures stated in Volume II. Volume II Clause 4.2 applies." | Unchanged. | **Engineering decision.** [I] 120,000 m³/day = 5,000 m³/h; if dry weather flow ≈ average, 3× = 15,000 m³/h, which exceeds the 7,500 design peak used to size the main (§5.2). |
| F8 | [F] **Table 2-4 is "reproduced" from an Environmental Permit that is not supplied, and the Permit prevails over the reproduction.** ADD-02 amends the reproduction. | VOL-II §2.4 p2; p3 header; ADD-02 §5.1; ADD-01 App B Item 5 | "In the event of any discrepancy between this reproduction and the Environmental Permit, the Environmental Permit shall prevail." Minutes: "the permit was under review by the regulator". | The Permit is not in the pack, so whether 3 mg/l, or any other design, complies with it **cannot be established**. What can be said: the amended reproduction says 3 mg/l, and VOL-II §2.4 says the Permit prevails over the reproduction. (Revision 1 claimed 3 mg/l "satisfies either reading"; that claim was withdrawn at the owner's instruction.) | Human decision; clarification on which governs, and the Permit itself, should be requested. |
| F9 | [F] **The Table 2-4 "basis" column (image only) drives obligations elsewhere.** | VOL-II §2.5 p2, §7.2–7.3 p4; VOL-V §29.3, §31.1(b), §31.2, §31.3 p3 | §2.5: "for those parameters identified in Table 2-4 as assessed on a continuous basis". VOL-V §29.3: "a parameter listed in Table 2-4 as assessed on a rolling average basis". §31.2: "not subject to any cap". §31.3: "No cure period applies to an event under Clause 31.1(b)." | The TN tightening propagates to the reliability run (PCOD), Unavailability Events and uncapped deductions. | [I] Continuous monitoring applies to residual chlorine and pH; ramp-up relief applies to BOD5/COD/TSS/TN/TP. Both readings rest on the image. |
| F10 | [F] **Form 4-G (new) has a non-responsive consequence and new obligations.** It is inserted "after item (e)" of VOL-I §9.1, with re-lettering unspecified. The VOL-IV index ("Forms 4-A to 4-F") is not updated. Undertakings 3–6 (security officer, 24 h incident notice, annual OT penetration test, MFA) are not in VOL-II §6. | ADD-02 §7 p3 | "Failure to submit Form 4-G shall render the Proposal non-responsive." | A new A3 row and new A1 rows. | [I] The effect of answering "No" on an undertaking is undefined. Human decision. |
| F11 | [F] **Bid Bond.** Valid 180 days from the PDD; SAR 4,500,000; unconditional, first demand; Kingdom-licensed bank rated ≥ A-. The clause states **no rejection consequence**. | VOL-I §6.3–6.4 p3; ADD-01 Q3; ADD-02 Q8 | "…shall remain valid for one hundred and eighty (180) days from the Proposal Due Date…" | [I] A bond drafted against 12 Nov expires about 14 days early. That is a rework item after ADD-01. | Whether it belongs in A3 depends on the decision in §7 (no explicit consequence wording). |
| F12 | [F] **Mandatory items with no stated consequence.** §11.1(i) makes a "responsiveness and mandatory compliance check on a pass or fail basis", but these clauses do not say what failure causes. | VOL-I §6.3–6.5, §8.3, §8.4, §8.7–8.10, §10.1, §10.3 | "Proposals will be evaluated in three stages: (i) a responsiveness and mandatory compliance check on a pass or fail basis…" | n/a | **Classification decision** (see §7). The brief limits A3 to explicit document wording. |
| F13 | [F] **Referenced but not supplied:** Volume III (Drawings, incl. Drawing 03-C-114); the Environmental Permit; the ESIA and geotechnical report ("data room"); VOL-V Schedules 7, 9, 11 and 12; the Direct Agreement; RFQ NUPA/ISTP/2025/031; the "Authority's standard five-point scale"; and "appendices expressly permitted by Volume II" (none found in the extract). | VOL-I §3.1, §3.2(f), §3.4; VOL-II §2.4, §5.1, §9.1; ADD-01 Q4; VOL-V §29.2, §31.2, §39.1, §39.5, §40.1; ADD-02 note (3) | VOL-I §3.4: "No claim arising from an alleged omission shall be entertained after the Proposal Due Date." | Gaps must be raised before the clarification cut-off (12 Nov). | The hiring team replied (2 Oct): the pack is complete as provided; treat Volume III and Drawing 03-C-114 as referenced but not supplied and flag the gaps and their impact. Flagged as Issue `I-VOL-III` from session 04; the full gap list is Stage 3 work. |
| F14 | [F] **Bidder identity affects counts.** Only Appendix 1 bidders are eligible. Four consortia have 3 members; **Northwind has 2**. Composition changes need consent. | VOL-I §1.4 p2; §8.1 p4; App 1 p7 | "A Proposal received from any other person shall be rejected without evaluation." | n/a | Drives the number of Form 4-C copies, Powers of Attorney and declarations. See decision D1. |
| F15 | [F] **Copies per envelope are not specified.** | VOL-I §6.2, §6.5 p3 | "one (1) marked original, three (3) hard copies, and one (1) searchable electronic copy on encrypted USB media" | n/a | The marshalling plan must state its assumption (per envelope or per Proposal). |
| F16 | [F] **File-naming convention forces `.pdf`, but the Financial Model must be Excel.** | VOL-I App 2 p7; §10.3 p5 | "Files shall be named: ISTP2026-014_[BIDDER]_[ENV]_[VOL]_[NN]_[YYYYMMDD].pdf" / "Non-conforming file names will be corrected by the Authority at the Bidder's risk." | Not disqualifying. | Flag. The meaning of [YYYYMMDD] is unstated. |
| F17 | [F] **Earlier answers inside the pack that are now stale:** ADD-01 Q2 ("the 120-page limit"; now 150, although its substance, forms excluded, still holds); ADD-01 App A date (12 Nov); minutes "seventy / thirty". | ADD-01 p1, p3, p4; ADD-02 §2.1 p1 | "Does the 120-page limit in Volume I Clause 9.2 include the Form Sheets?" | These go in A2's "earlier answers now wrong" list. | — |
| F18 | [F] **Pre-Bid attendance is a past, fixed-date disqualifier.** The minutes record all five bidders present (non-binding record). The window to contest the record closed on 15 Oct 2026. | VOL-I §5.4 p3; ADD-01 §3.1 p1; App B Item 1 p4 | "A Bidder that is not represented at the Pre-Bid Conference shall be disqualified." / "within five (5) Working Days of this Addendum" | Fixed; does not move with the PDD. | Our bidder's attendance is a bidder fact. The original Form 4-A ¶5 confirmation is missing from the reissued form (O4). |
| F19 | [I] **Table 2-4 internal tension.** "All values are maxima", yet residual chlorine and pH are ranges. Residual chlorine 0.5–1.0 mg/l "continuous at outlet" sits against VOL-II §3.3, which permits UV-only disinfection or dechlorination. | VOL-II p3 (image); §3.3 p3 | "Disinfection shall be by chlorination with provision for dechlorination, or by ultraviolet irradiation with a validated dose, or by a combination." | n/a | Engineering judgement. Lower priority. |

### 2.3 Explicit-consequence inventory (candidate A3 content; **not** a register)

Effective after ADD-02, by the strict test of "the documents themselves say":

- **Rejection:**
  - VOL-I §1.4: not prequalified.
  - §6.6: late, rejected unopened.
  - §8.1: unapproved consortium change.
  - §8.2: multiple participation.
  - §8.5 fn 12: reference plants.
- **Disqualification:**
  - VOL-I §4.2: blackout.
  - §5.4: Pre-Bid attendance.
- **Non-responsive:**
  - VOL-I §6.2: commercial information in Envelope A.
  - §8.6 as reinstated: LCC.
  - §9.3: Form 4-A execution.
  - §9.4: Form 4-C, also VOL-IV p5 and the Arabic note.
  - §9.6: 'no deviations' plus a qualification elsewhere.
  - §10.5: conditional or alternative price.
  - §11.5: a clarification response that changes the Availability Payment (post-submission).
  - ADD-02 §7.2: Form 4-G.
- **Exclusion:** Form 4-C declaration 4 (Arabic only): any incorrect statement.
- **Score-based elimination (separate category):** VOL-I §11.3, technical score below 70 means Envelope B is returned unopened.
- **Lesser or indirect consequences (not "bid out" on their own):**
  - §9.2: excess pages removed.
  - §9.5 and Form 4-B: reference disregarded, which can cascade to fn 12.
  - VOL-IV p2 and VOL-I §3.3: "at its own risk".
  - VOL-V Note: unlisted deviation "taken as accepted".
  - §12.2: Bid Bond called if Financial Close fails (post-award).

### 2.4 Things I have **not** established

- That the lists above are complete. Coverage will be shown by the system's checks (§4.7), not asserted.
- Anything about the bidder: references, certificates, local-content ratio, financials, attendance.
- Which item the brief means by "one of them has no correct answer at all". The candidates are O4 (Form 4-A), F4 (Envelope B), F5, F6 (concession term) and F7 (flows). The system's job is to surface all of them to a person, not to pick.

### 2.5 Date inventory (computed by me, independently of any code)

Assumptions:

- Working Days run Sun–Thu (VOL-I §2.4).
- No declared public holidays in the window (an assumption to be configured).
- "N days from the PDD" makes the PDD day 0.

| Item | Rule | PDD 12 Nov 2026 (base) | PDD 26 Nov 2026 (after ADD-01) |
|---|---|---|---|
| Clarification cut-off, VOL-I §5.2 | −10 WD, stated date not counted (§2.4) | Thu 29 Oct 2026 | **Thu 12 Nov 2026** |
| Bid Bond validity end, §6.3 | +180 days | 11 May 2027 | 25 May 2027 |
| Proposal validity end, §7.1, Form 4-A ¶2 | +150 days | 11 Apr 2027 | 25 Apr 2027 |
| Reference COD look-back start, fn 12 | −10 years | 12 Nov 2016 | 26 Nov 2016 |
| ISO 9001 currency, §8.3 | "as at" PDD | 12 Nov 2026 | 26 Nov 2026 |
| Withdraw or modify, §6.7; omission claims, §3.4 | before / after PDD | — | moves with PDD |

**Fixed dates (do not move):**

- Issue date of the volumes: 14 Sep 2026.
- Pre-Bid Conference: Wed 30 Sep 2026, 10:00.
- Site visit: Thu 1 Oct 2026 (§5.5, "the day following").
- ADD-01 issued: Thu 8 Oct 2026.
- ADD-01 §3.1 window: 5 WD after ADD-01, ending **Thu 15 Oct 2026** (forward convention assumed).
- ADD-02 issued: Thu 22 Oct 2026.

**Anchored to unknown future events (computed symbolically):**

- VOL-I §12.2: Preferred Bidder Notification (PBN) +120 / +270 days.
- §12.3: standstill of 10 WD after PBN.
- §12.4: 20 WD debrief window.
- VOL-V §12.1: Notice to Proceed +36 months.
- VOL-V §18.3, §29.3, §29.4, §34.3, §39.4, §42.2.

**Window from ADD-02 issue to PDD:** 35 calendar days; 25 Working Days after 22 Oct up to and including 26 Nov (24 strictly between the two dates). *Corrected in session 04: revisions 1–3 said "24 Working Days" without saying which days were counted.*

---

## 3. Critique of the proposed direction

| Direction | Verdict | Why | Where it could fail, and what I'd change |
|---|---|---|---|
| **A. Evidence before interpretation** | **Sound; keep it light.** | Hashes, page counts and page/bbox anchors are cheap, and they are exactly what the "show me the page within a minute" check needs. | **Watermark contamination.** In layout mode, pdftotext interleaves watermark letters ("CK", "PA", "EN", "SS", …) into clause text. Extraction must be rotation-aware (drop lines whose direction ≠ horizontal) or verbatim matching will fail. **Keep normalisation minimal and declared:** de-hyphenation, whitespace, quote marks, superscript marking, watermark/header/footer removal by **exact, audited patterns**. Don't build a general normaliser. |
| **B. Original units + ordered typed amendments → derived effective state** | **Sound and recommended.** This is the core of the system. | It is the only representation that answers "what did it say, what changed it, what is it now" without drift. | (1) **Not all amendments are text patches.** The pack has clarification answers, a global re-anchoring rule (ADD-01 §2.2), a suppression rule and its revocation (ADD-01 §4.2 / ADD-02 §9.2), a new form, a table reissue, a value restated without quoting the old text (note 2, TN), and non-binding minutes. The op vocabulary must cover these with ~8 types (§4.4), not an open-ended DSL. (2) **The biggest failure mode is not the text; it is the interpretation drifting from the text.** A register row's reviewed attributes (consequence, parameters, evidence) can silently go stale when the unit underneath is amended. Fix: **pin every reviewed interpretation to the hash of the unit text it was reviewed against**. A changed hash makes the row STALE until a person re-reviews it. This is the mechanism that prevents stale downstream values. (3) **Atomicity:** an addendum is one legal act. Apply its ops in section order, but report it as APPLIED only if every provision is accounted for. Anything else is PARTIAL, labelled at the top of A3. |
| **C. Deterministic trusted build from reviewed inputs; models propose** | **Sound. The manual-work worry is real but manageable.** | Building ~100 rows by hand is too slow, and an un-reviewed model build is indefensible. | **Practical balance:** a model (or pattern) **drafts**, the build only consumes records marked `accepted`, and checks catch what review misses. Review depth is tiered: every A3 candidate, every amended row and every image transcription gets full review; other rows get mechanical verbatim checks plus spot review, and their confidence says so. For the live 30 minutes: a pattern drafter handles the common phrasings seen in ADD-01/02; anything else becomes an `unresolved` op carrying its verbatim text, which a person converts to a typed op or `no_effect` in minutes. The model drafter is an accelerator, not a dependency, so the build works offline. |
| **D. Coverage over retrieval; no vector DB/RAG** | **Agree.** | 32 pages, roughly 25k tokens: everything fits in one model context and in one person's afternoon (brief §2). Retrieval would only add a way to miss things. | "The parser found text" ≠ "every obligation captured". Coverage is shown by **accounting** (every span and image region belongs to exactly one unit; every unit has a disposition) and by **sweeps** (every obligation or consequence phrase, in English and Arabic, maps to a row or an explicit disposition). Correctness is shown separately, by independently written golden tests. |
| **E. Outputs from shared structured data** | **Agree.** | A2, A3 and A5 must be pure functions of the A1 register plus the op history and assumptions. | Two distinctions are needed: (a) `consequence` (explicit, quoted, with source) vs `none_stated`, which keeps A3 honest; (b) `read_confidence` (how sure we are of what the pack says) vs `compliance_status` (the bidder's position: unknown by default). For A5, tender facts and assumptions must live in different files, and every assumption needs a basis and an owner. |
| **F. Small and inspectable: Python, typed records, schemas, CLI** | **Agree.** | — | Minimum dependency set and module boundaries are in §4.9. One caution: PyMuPDF is AGPL-licensed (see §4.9). |

**Alternatives considered:**

- **S (simplest): hand-maintained register snapshots per stage** (three CSVs), with a diff script for A2, a filter for A3 and a scheduler for A5.
  - Fast to start.
  - Fails the live session: ADD-03 would mean hand-editing a copy, with no target validation, no scope proof and no stale detection. Rejected.
- **M (recommended): your direction, pared down.**
  - Units, 8 op types, hash-pinned interpretations, explicit date rules, a check registry, and a pattern drafter with an optional model drafter.
- **L (over-built): general amendment DSL / clause graph store / NLP pipeline / LLM agents in the build.**
  - Rejected: no benefit at 32 pages, and harder to change live.

---

## 4. Architecture [D]

### 4.1 Data flow

```
sources/*.pdf ──(1) extract + regions──► spans (font, size, bbox, superscript, angle); furniture excluded by
     │ sha256, pages                │        audited rules; regions = images, drawings, invisible text, stray ink
     ▼                              ▼
sources/manifest.json        (2) segment ──► build/units.json   SourceUnits with stable IDs (clause, footnote,
                                    ▲                            table row, form field, list item, note, Q&A)
curation/readings/*.yaml ───────────┘  region readings → units (status pending until a person approves;
curation/approvals.yaml (written only by `approve`)    approval pins reading + uncertainties + evidence)
                                    │
curation/amendments/ADD-0N.yaml ─(3) amend──► build/states/{BASE,ADD-01,ADD-02,…}.json
   (typed ops, status=accepted)     │          effective unit text + status + op history + text sha per stage
                                    ▼
curation/requirements/*.yaml ──(4) register──► A1 (CSV/JSON[/XLSX]) one row per requirement,
   (interpretations pinned to       │            status per stage, verbatim checked against stage text
    unit-text sha per stage)        │
curation/issues.yaml ───────────────┤ human decisions, ambiguities, missing sources, bidder facts
config/assumptions.yaml ─(5) dates──┤ calendar, holidays, conventions, planning date, bidder, lead times
                                    ▼
                         (6) checks (registry) ──► build/checks.json  (fail → abort / flag, see §4.7)
                                    ▼
                         (7) render: A1, A2 (from op history + stage snapshots), A3 (filter + issues),
                                     A5 (backward scheduler over evidence→activity templates)
                                    ▼
                         build/ (deterministic; no timestamps) + build/BUILD_MANIFEST.json (input/output hashes);
                         written to a temporary sibling and swapped in only if every structural check passes

New addendum:  sources/ADD-03.pdf → ingest/segment → (8) draft ops (patterns → optional model → `unresolved`)
               → person reviews/accepts → build → `diff ADD-02..ADD-03` = "what it broke" → A5 replan.
```

### 4.2 Modules (one responsibility each)

Package `tenderpack/` (a working name for the code, not a product name). Built in Stage 1 unless marked *planned*.

| Module | Responsibility | Why separate |
|---|---|---|
| `sources.py` | Source integrity (C01): hashes and page counts against `sources/manifest.json` | Nothing runs on unverified inputs |
| `extract.py` | Span extraction; furniture exclusion by declared rules (text, colour, size, position, angle together) | The only text-layer reader; swappable |
| `regions.py` | Regions outside the text layer (images, non-structural drawings, invisible text, unexplained ink); evidence crops; raster grid and text bands | Image handling is generic, not keyed to known pages |
| `segment.py` | Spans → SourceUnits: clauses, footnotes (marker ↔ body), unit exponents, tables and split tables, form fields, list items, numbered paragraphs, notes, Q&A rows | Segmentation errors are the most likely ingest bug, so they get their own tests |
| `readings.py`, `arabic.py` | Reading records (pydantic), reading checks RD1–RD9, review subject and status, rendered right-to-left checks | One definition of what a reading is and what an approval covers |
| `packets.py` | Review packets: each crop beside the reading it supports, checks, decisions for the reviewer | Presentation for a person; no logic that decides |
| `coverage.py` | Checks C01–C10 and the coverage reports | Accounting is separate from segmentation |
| `cli.py` | `ingest`, `show`, `approve`; output-path guard; atomic build swap; exit codes | — |
| `amend.py` *(planned)* | Applies accepted ops per stage; pre/post-conditions; target verification (§4.4.1); scope-leak diff; op ledger | Core correctness logic, kept pure |
| `dates.py` *(planned)* | Calendar, date rules, conventions, per-stage evaluation | Date errors are high-impact; pure functions |
| `register.py` *(planned)* | Joins interpretations with stage states; evidence and pin checks; status per stage | — |
| `checks.py` *(planned)* | Registry of register-level checks plus data lexicons (EN/AR obligation and consequence phrases) | Where the live "catch this kind of error" change happens |
| `schedule.py` *(planned)* | Evidence → activity templates → backward pass → A5 | — |
| `render/` *(planned)* | A1 (CSV, JSON, Excel), A2, A3 (one-page PDF), A5 | Presentation only |
| `draft.py` *(planned)* | Pattern drafter and the model routes of §4.6; writes proposals only | Never imported by the build |

### 4.3 Essential entities

- **SourceDocument**
  - Fields: `doc_id`, `path`, `sha256`, `pages`, `kind` (volume/addendum), `number`, `issue_date`.
- **Region** (built)
  - Fields: `region_id`, `doc`, `page`, `bbox`, `kind` (image / vector_graphic / invisible_text / unexplained_ink), native image (sha256), crop, context.
  - Each region needs a **Reading** (`curation/readings/<region>.yaml`, §4.11): `content_type` (table / text / form / graphic), source claims, content, numerals, uncertainties, `prepared_by`, `method`. Its status is `pending` until an approval with a named reviewer matches its **review subject** (the reading, its uncertainties and its evidence).
- **SourceUnit** (built)
  - Fields: `unit_id`, `doc`, `kind`, `parent`, `pages`, `anchors` (page, bbox, span IDs), `label` and `label_span`, `text` (as printed), `normalized` (matching only), `origin` (text_layer / image_reading), `reading` status for image units; table rows carry `cells`, and image-table rows also `numeric` (the numbers a cell shows, no meaning) and `context` (headings, qualifier, notes; `interpretation: null` until a person decides).
  - Example IDs: `VOL-I:8.5`, `VOL-I:8.5#fn12`, `VOL-II:T2-4/TN`, `VOL-IV:F4-C/image/decl4`, `VOL-IV:F4-A/proposal-due-date`, `ADD-02:Q7`.
- **Evidence items vs effective text** (planned with the register). Each A1 row carries (a) **evidence items**, each checkable where it lives: `text_layer` items are span IDs re-extracted from their page; `image_reading` items are a region, its crop and the reading's review status (a pending reading is evidence marked *pending*, never silently trusted); and (b) **effective text**, labelled "assembled by ops [...]", checked by **replaying the ops** from the evidence, never by searching a page (e.g. "… ninety-six (96) hours" after ADD-02 exists on no single page).
- **Operation**
  - Fields: `op_id`, `addendum`, `provision` (unit of the addendum), `source_quote`, `type`, `target`, `params` (`old`, `new`, `occurrence`, `new_unit`, `status`), `expect` (optional assertions), `review` (`status`: proposed/accepted/rejected/unresolved; `origin`: pattern/model/human; `by`).
- **UnitState** (derived)
  - Fields: `unit_id`, `stage`, `status` (active/deleted/revoked), `text`, `text_sha`, `history` (op IDs).
- **Requirement** (A1 row)
  - Fields:
    - identity and source: `req_id`, `units`, `evidence_items`, `effective_text` (replayed from ops per stage);
    - classification: `kind`, `assessment` (pass_fail / scored / contractual-post-award / procedural / informational);
    - `consequence`: `{class, quote, unit}` or `none_stated`;
    - ownership and evidence: `discipline`, `evidence` (EvidenceItem IDs), `parameters`;
    - links: `date_rules`, `depends_on`, `issues`;
    - confidence: `read_confidence` `{level, reasons}`;
    - review: `reviewed` `{by, pins, stage}`, where `pins` is the dependency set of §4.10.
  - Per-stage overrides are stored only where the interpretation differs.
- **EvidenceItem**
  - Fields: `ev_id`, `type`, `issuer` (internal role / external body), `per` (bidder / member / signatory / reference / envelope), `multiplicity`, `req_ids`.
- **DateRule**
  - Fields: `rule_id`, `kind` (fixed / relative / external_anchor), `anchor` (PDD / ADD-01-issue / PBN / NTP / PCOD), `offset`, `unit` (calendar_day / working_day / month / year), `direction`, `convention` (`day0`, `stated_date_excluded`, `unresolved`), `source_unit`.
- **Issue**
  - Fields: `issue_id`, `kind` (inconsistency / ambiguity / missing_source / untranscribed / human_decision / bidder_fact), `units`, `statement`, `options`, `owner` (a person's role), `status`, `decision`, `decided_by`.
- **Assumption**
  - Fields: `key`, `value`, `basis`, `owner`.
  - Used for: planning date (latest addendum date), bidder (unnamed consortium, **default three members, editable**; all bidder details are assumptions, not facts), holidays, lead times, resources.
- **Activity** (derived)
  - Fields: `act_id`, `req_ids`, `ev_id`, `owner_discipline`, `issuer`, `duration` (+ assumption key), `predecessors`, `LS`/`LF`, `flags` (OK / INFEASIBLE(n WD) / REWORK / NEW / REMOVED).

### 4.4 Operation types: a small closed set

| Type | Covers (examples from the pack) | Preconditions checked |
|---|---|---|
| `replace_text` | ADD-01 §2.1 (date), ADD-02 §2.1 (pages), §4.1 (72→96 h), §8.1 (SAR 5m→2.5m) | `old` occurs **exactly once** in the target unit's normalised text (or `occurrence` is given) |
| `set_value` | ADD-02 note (2) (11.2 → 65/35), §5.1 (TN "from the value shown" → 3 mg/l, same basis) | Target is a value-bearing unit (a parameter in clause text, or a table cell from a reading; a pending reading makes the op's result pending). The old value is resolved and recorded. |
| `append_text` | ADD-01 §5.1 (GRP pipe sentence added to VOL-II §5.3) | Target active; appended text not already present |
| `set_status` | ADD-01 §4.1 (delete VOL-I §8.6); ADD-02 §9.1 (reinstate with new text); ADD-02 §9.2 (revoke ADD-01 §4.2) | delete ⇒ active; reinstate ⇒ deleted; revoke ⇒ active rule |
| `replace_unit` | ADD-02 §3.1 (Table 1-1 reissued); ADD-01 App A (Form 4-A reissued) | Target exists; replacement content is itself segmented into units |
| `insert_unit` | ADD-02 §7 (Form 4-G into VOL-IV; item into VOL-I §9.1 "after item (e)") | Anchor exists; no ID collision |
| `annotate` | Clarification answers (Q1–Q14); ADD-01 §2.2 (re-anchor rule); ADD-01 §3.1 (new obligation); ADD-02 note (1) (confirm unchanged) | Linked units exist. `effect` is one of: `none`, `confirms`, `adds_obligation`, `interprets` (an `interprets` effect requires a person's review) |
| `no_effect` | Recitals, minutes items (non-binding), cover summaries | A reason is required |
| `unresolved` | Anything the drafter cannot type, or whose target cannot be identified with confidence | **Never applied.** Candidate targets are flagged. Listed in A3 and A2. `--strict` fails. |

**How the hard cases are handled:**

- **Several changes in one paragraph.** One provision maps to **many ops**, each with its own `source_quote`. Example: ADD-02 §3 becomes `replace_unit` (Table 1-1) + `annotate(confirms)` (note 1) + `set_value` (note 2) + `annotate(none)` (note 3) + an `expect` assertion that D rises by 5, B falls by 5 and the total is 100. Check C20 requires every provision, *including table notes*, to be referenced by at least one op.
- **Repeated wording.** Ops are always scoped to a unit, never global. `old` must match exactly once inside the target. After each addendum, check C25 diffs **every** unit and aborts if any unit changed that no op targeted. That catches a global-replace bug even if a test author forgot that case.
- **Delete, then reinstate.** These are `set_status` ops with state preconditions. The unit keeps its full history, so A1 shows ACTIVE → DELETED → REINSTATED-AMENDED with the same row ID. Revoking ADD-01 §4.2 is a `set_status` op on the *addendum's own unit*.
- **Target not identifiable.** The op becomes `unresolved`. Nothing is applied, rows that are candidate targets are marked AMENDMENT-PENDING, and A3 lists it with the reason. A person resolves it by editing the op, not by editing outputs.
- **Duplicate application.** Op IDs are unique and applied once per build from a clean BASE. Post-conditions require the `old` count to fall by exactly one and `new` to be present. The ledger records the unit-text sha before and after each op, and a second application fails its own precondition.
- **Partial application.** Addendum status is APPLIED only if every provision is covered and every op is accepted and valid. Otherwise it is PARTIAL, with the exact unapplied provisions printed in A3's header. `--strict` refuses PARTIAL.

#### 4.4.1 Target verification: catching an op aimed at the wrong clause with the same wording

A quotation found in the declared target, plus a change confined to that target, proves only that the op is *internally consistent*, not that the addendum meant that clause. In this pack, "seventy-two (72) hours" occurs in VOL-II §4.4 and VOL-V §31.3; an op aimed at §31.3 would pass the substring, uniqueness and scope-leak checks. The defence uses evidence independent of the op author:

1. **Citation resolution (primary).** The program extracts the target citation from the addendum's own provision text ("In Volume II Clause 4.4, …") and its section heading, and resolves each to a unit ID with a small grammar (Volume/Clause/Table/Form/footnote/Appendix and row names inside tables, e.g. "the limit for Total Nitrogen (TN)" → `VOL-II:T2-4/TN`). The op's declared target must equal the resolved target, and body and heading citations must agree. Failure: op invalid, "declared target X ≠ cited target Y".
2. **Ambiguity disclosure (secondary).** For every quoted "old" text, list *all* units containing it; the review view shows the others ("also in VOL-V §31.3 — not targeted").
3. **Self-consistency claims** in the addendum ("Volume I Clause 8.6, deleted by Addendum No. 1 Section 4") are checked against the op ledger.
4. **When the addendum's own citation and quotation disagree**, the op is `unresolved`, with an Issue for a person. Nothing is auto-corrected.
5. **Tests:** an op aimed at VOL-V §31.3 with ADD-02 §4.1's quote fails on citation mismatch; a synthetic addendum whose citation and quote disagree yields `unresolved`.

### 4.5 Worked example: Local Content Certificate

**1. Source.** Unit `VOL-I:8.6` (p4, bbox stored), sha s0, text: "The Bidder shall submit a Local Content Certificate issued by the competent authority evidencing a local content ratio of not less than thirty per cent (30%) for the construction phase."

**2. Interpretation at BASE.** Requirement `VOL-I-8.6-01`:

- `assessment: pass_fail` (Section 8 heading, §11.1(i));
- `consequence: none_stated`;
- `parameters: {local_content_min_pct: 30, phase: construction}`;
- `evidence: [EV-LCC]`, where EV-LCC has issuer "competent authority (unnamed)", per bidder, and links to Issue I-LCC-ISSUER;
- `discipline: Commercial`;
- `read_confidence: high (verbatim)`;
- `reviewed.against = s0`.

**3. ADD-01 (8 Oct).** Three entries:

```yaml
- id: ADD-01/4.1
  provision: ADD-01:4.1
  source_quote: "Volume I Clause 8.6 (Local Content Certificate) is deleted in its entirety."
  type: set_status
  target: VOL-I:8.6
  expect_before: active
  status: deleted
- id: ADD-01/4.2
  provision: ADD-01:4.2
  source_quote: "any reference to a Local Content Certificate elsewhere in the RFP Documents shall be disregarded"
  type: annotate
  effect: interprets   # rule unit ADD-01:4.2 becomes active; the build lists the units it touches (none besides 8.6; §9.1(i) generic)
- id: ADD-01/AppB-4
  provision: ADD-01:AppB:item4
  type: no_effect
  reason: "minutes, non-binding (ADD-01 §3.2); retained as lead-time signal for A5 assumption basis"
```

Resulting state: `VOL-I:8.6` is DELETED. The row's status after ADD-01 is DELETED (by ADD-01/4.1). The row is kept, not removed. A3 is unaffected, because the row was never in A3. A5 drops the EV-LCC activities, and the delta records "removed by ADD-01 §4.1".

**4. ADD-02 (22 Oct).**

```yaml
- id: ADD-02/9.1
  provision: ADD-02:9.1
  source_quote: "Volume I Clause 8.6, deleted by Addendum No. 1 Section 4, is reinstated in the following amended form"
  type: set_status
  target: VOL-I:8.6
  expect_before: deleted
  status: active
  new_text: "8.6 The Bidder shall submit a Local Content Certificate issued by the competent authority evidencing a local content ratio of not less than thirty-five per cent (35%) for the construction phase. Failure to submit the certificate shall render the Proposal non-responsive."
- id: ADD-02/9.2
  provision: ADD-02:9.2
  source_quote: "Section 4.2 of Addendum No. 1 ceases to have effect."
  type: set_status
  target: ADD-01:4.2
  expect_before: active
  status: revoked
```

Check results:

- C21: both quotes are found verbatim in ADD-02 p3.
- C22: the preconditions hold; §4.4.1: the cited target ("Volume I Clause 8.6") resolves to `VOL-I:8.6`.
- C25: no other unit changed.

The row's pins (§4.10) include the text of `VOL-I:8.6`, which is now s2 ≠ s0. The row is **STALE** until a person re-reviews it at stage ADD-02: `parameters.local_content_min_pct: 35`, `consequence: {class: non_responsive, quote: "Failure to submit the certificate shall render the Proposal non-responsive.", unit: VOL-I:8.6}`, re-pinned at stage ADD-02.

**5. Outputs.**

- **A1:** one row `VOL-I-8.6-01` with three status columns:
  - BASE = ACTIVE (30%, no stated consequence);
  - ADD-01 = DELETED (ADD-01 §4.1, p1);
  - ADD-02 = REINSTATED-AMENDED (35%, non-responsive; ADD-02 §9.1, p3).

  The verbatim column shows the effective ADD-02 text. The source column cites VOL-I §8.6 p4 *as reinstated by* ADD-02 §9.1 p3.
- **A2:**
  - ADD-01 "deleted": §8.6.
  - ADD-02 "reinstated/changed": §8.6 (30→35, consequence added), plus revocation of ADD-01 §4.2.
  - "Earlier answers now wrong": *"No Local Content Certificate is required" (true 8–22 Oct)*.
  - Chain: `VOL-I-8.6-01 ← ADD-02/9.1 (p3) ← ADD-01/4.1 (p1) ← VOL-I §8.6 (p4)`.
- **A3:** the LCC row appears (non-responsive; confidence high on the reading). Unresolved items: issuer not named; lead time unknown; minutes record difficulty obtaining it.
- **A5:** EV-LCC activities return with flag **REWORK/RESTART** (or NEW if no progress was recorded) and are backward-scheduled from the Envelope A sealing date. If `lead_times.lcc` (assumption, with basis and owner) exceeds the time available from 22 Oct, the activity is flagged **INFEASIBLE by n WD** and listed in A3. It is never silently compressed.
- **Dependents:** VOL-I §9.1(i) (Envelope A contents) is now active for the LCC; ADD-01 §4.2 is revoked, so references are no longer disregarded.

**PDD in brief.** `VOL-I:6.1` is amended by `replace_text` (ADD-01/2.1). The PDD DateRule is re-parsed from the effective text; the change in sha forces re-review of the parse. Relative rules recompute: §5.2, §6.3, §7.1, fn 12, §8.3 and Form 4-A ¶2. Fixed rules don't. Printed copies of the old value (`VOL-IV:F4-A:pdd`, `ADD-01:AppA:F4-A:pdd`) trip check C31 and **raise an Issue**. They are never rewritten.

### 4.6 Model use and routes (design only; integrations and model selection deferred)

- **Models draft; people decide; the build never calls a model.** Drafts are YAML records with `origin` and `status: proposed` (readings: `pending`), checked by the same RD/C checks and approved only by a person. The offline build, with no model and no API key, is the reviewed path.
- **One small interface, three routes:** `propose(task_packet) -> proposal_file`.
  - `claude_code`: the coding assistant in the Claude Code app fills the proposal file directly (this is how the two Stage 1 readings were prepared, logged as AI-assisted);
  - `openrouter`: an HTTP API;
  - `ollama`: local on the owner's Mac (M5 Pro, 48 GB).
- **Shared by every route:** the same task packet (instructions, expected schema, crops), the same output path into `curation/` (always pending), the same validation, the same approval rule, and a log of every prompt and response under `worklog/model_calls/`.
- **Capabilities are checked, not assumed:** Ollama's `/api/show` reports `capabilities` (e.g. `vision`); OpenRouter's model listing reports input modalities (not verifiable from this cloud environment, whose network policy blocks `openrouter.ai` and `ollama.com`). A model without image input is refused for reading tasks.
- **Model selection is deferred.** The session 02 shortlist for the Mac (Qwen3.8-27B; Qwen3.6-35B-A3B and Qwen3.5-35B-A3B/27B; Qwen3-VL-32B/8B; about 17–24 GB at 4-bit) comes from search results, not tests. When the routes are built, candidates are benchmarked on the owner's Mac against the two readings *after the owner has approved them* (Table 2-4 cell accuracy, Form 4-C character accuracy, the ٤-x digit), and the measured results decide.

### 4.7 Checks: what is checked and what happens on failure

**Failure actions:**

- **ABORT (structural failure):** the build exits non-zero (2), prints the failing checks, keeps the previous build and writes this one to `<out>.failed` for inspection.
- **FLAG:** the build continues; the item is marked in A1/A2 and listed in A3 "could not resolve".
- **Strict mode** (`build --strict`, used for submission) turns every FLAG into ABORT, except the Issues that are *meant* to stay open for a person.
- **Pending human review is not a failure.** It is printed as PENDING HUMAN REVIEW and carried on every unit derived from a pending reading; `ingest --require-approved` exits 3 while anything is pending.

C01–C10 are built (Stage 1). Built by session 05 (§10, §11): C11, C13, C14 (reported), C15 (release blocker), C16, C20–C27, C31, C40, C43 (with a minimum text size), C44, C45. Built in session 06 (§12): C12 (structural, with the id ledger), C29 as the decision gate (D8), C30 (release blocker), C32 (reported), C46 (release blocker) and C47 (structural). Built in session 07 (§13): C28 (reported). Not built: C41, C42 beyond the determinism check. IDs were renumbered in revision 3 where they collided (old C07 → C14, old C08 → C15, old C10 → C16).

**Implemented action vs this table (session 05):** C15 and unit dispositions block a strict release and fail `check-register`; they do not abort a working draft, which is published labelled WORKING DRAFT with every blocker listed. `outputs --strict` refuses the release (exit 3) while any coverage, stale or approval blocker remains.

| ID | Check | Failure action |
|---|---|---|
| C01 | Source sha256 and page count match `sources/manifest.json` | ABORT (before anything runs) |
| C02 | Every page is accounted for (content spans, exclusions, regions) | ABORT |
| C03 | Every content span is assigned to exactly one unit | ABORT, listing orphan spans |
| C04 | Every excluded span matched a declared furniture rule on all its attributes; rules with an expected count matched it on every page | ABORT (prevents a rule from eating content) |
| C05 | Every region has a reading and every reading has a region; readings pass RD1–RD9; pending review is shown | ABORT on unread / failing / orphan; pending is shown, not a failure |
| C06 | Every superscript is a unit exponent or a footnote marker paired with its body on the same page | ABORT |
| C07 | Unit IDs are unique across the pack (text-layer and reading units); nothing renamed | ABORT |
| C08 | Every content span appears exactly once in exactly one unit's anchors; every anchored span exists | ABORT |
| C09 | Segmentation reported no problems | ABORT |
| C10 | **Full evidence:** each text-layer unit's whole printed and matching text equals its spans re-extracted from the PDF (tables, rows, form fields: same characters as their spans) | ABORT |
| C14 | Obligation-language sweep: every sentence containing obligation markers (shall, must, required, mandatory, failure to, not acceptable, will not, …) lies in a unit with a disposition (requirement / definition / informational, with reason) | FLAG |
| C15 | Consequence-language sweep, EN + AR lexicon (reject, disqualif, non-responsive, disregard, returned unopened, removed before evaluation, own risk, taken as accepted, استبعاد, غير مستجيب, …): every hit is linked to a requirement's `consequence` or explicitly dispositioned | ABORT |
| C16 | **Evidence items** (§4.3): text-layer items re-extract from their page; image-reading items match their reading and show its review status; effective text equals the replay of accepted ops over the evidence at every stage where the row is active | ABORT |
| C11 | **Stale interpretation:** the combined hash of a row's pins (§4.10) differs from the one it was reviewed against | FLAG (row status STALE) |
| C12 | Row IDs are unique and never disappear between builds (deleted rows keep their ID and status) | ABORT |
| C13 | A row appears in the A3 main list only if `consequence.class` is explicit and its `quote` is found verbatim in a unit | ABORT |
| C20 | **Provision coverage:** every provision of each addendum (paragraphs, table notes, appendix items, Q&A rows, form items) is referenced by ≥1 op | FLAG → addendum PARTIAL |
| C21 | Op `source_quote` is found verbatim in its provision | op invalid (FLAG) |
| C22 | Target exists and state preconditions hold (delete⇒active, reinstate⇒deleted, revoke⇒active); declared target equals the cited target (§4.4.1) | op invalid (FLAG) |
| C23 | `replace_text`: `old` found exactly once in the scoped unit. Zero ⇒ "not found"; >1 ⇒ "ambiguous" | op invalid (FLAG) |
| C24 | Post-conditions: `old` count falls by 1; `new` present; re-application would fail | ABORT (bug) |
| C25 | **Scope leak:** the set of units changed by an addendum equals the set of declared targets | ABORT |
| C26 | Addenda are applied in number order with non-decreasing issue dates; ops reference only earlier or same addenda | ABORT |
| C27 | `expect` assertions hold (e.g. Table 1-1 deltas, total = 100) | op invalid (FLAG) |
| C28 | Cover-summary cross-check: summary claims vs the provisions (tables, notes, appendices, answers); omissions and contradictions reported in A2, A1 Issues and `diff`; the summary is never applied | report only (built session 07) |
| C29 | Only `accepted` ops are applied; `proposed` and `unresolved` are listed | report; ABORT in strict |
| C30 | Every date-bearing phrase in an active unit maps to a DateRule or a disposition | FLAG |
| C31 | Printed fixed dates that equal a superseded anchor value raise an Issue (inconsistency); never auto-corrected | Issue (always surfaced in A3) |
| C32 | Every relative rule declares its counting convention; `unresolved` conventions are computed both ways, shown as a range, and scheduled on the conservative reading | FLAG |
| C40 | A3 ⊆ A1; every A5 activity cites ≥1 A1 row that is ACTIVE at the latest stage; activities citing DELETED rows are removed with a delta note | ABORT |
| C41 | No literal dates in A5 inputs except tender facts and assumptions; any activity whose latest start is before the planning date is marked INFEASIBLE(n WD) | FLAG (always surfaced) |
| C42 | Build manifest: input hashes, code commit and output hashes; outputs contain no timestamps; `verify` rebuilds in disposable directories and compares | ABORT on mismatch |
| C43 | A3 renders to exactly one page, no text below 7.5 pt | ABORT (forces prioritisation; no silent overflow) |
| C44 | Every deliverable needed by a row in force has A5 activities, or a justified exception (`_exceptions: {EV-ID: reason}` in the templates file) | ABORT (added session 05) |
| C45 | Every A5 dependency, lead time and resource role is defined; an activity listed under two items is defined identically; a dependency not needed at this stage is shown, never dropped | ABORT (added session 05) |
| C46 | Every obligation an op creates or amends reaches an A1 row in force, A3 when its provision carries consequence words, and an A5 activity or deliverable | release blocker (coverage); A3 issue (added session 06) |
| C47 | Every word a unit gains at a stage is printed in that stage's addendum | ABORT (added session 06) |

### 4.8 A5 scheduling approach

- **Derivation.** Each A1 row's `evidence` items map, through `curation/activity_templates.yaml` (tender-independent, reviewable), to activity chains. Each link carries an issuer, an owner discipline, a resource role and a duration *key* into `config/assumptions.yaml` (value, basis, owner). Multiplicities (members, signatories, reference projects, envelopes) come from config and from the pack.
- **Backward pass.**
  - The anchor is the PDD date and time at the Sakaka tender box (App 3), less a delivery buffer (an assumption).
  - Each activity's latest finish is the minimum of its successors' latest starts and any pack-imposed "must finish by" date (e.g. clarification requests by 12 Nov 2026).
  - Latest start = latest finish − duration, in Working Days on the configured calendar.
- **Impossible dates.** A latest start before the planning date gives INFEASIBLE with the shortfall in WD. This is reported, not compressed, and it appears in A3.
- **Unavailable evidence.** Bidder facts default to `unknown`. The activity exists, carries a `bidder_fact` Issue, and is not marked complete.
- **Rework after an amendment.** A5 is generated per stage. An optional `progress.yaml` records completed activities. If a completed activity's requirement sha changed (e.g. a bid bond drafted for 12 Nov), it is flagged REWORK. Stage-to-stage deltas (NEW / REMOVED / MOVED / REWORK / INFEASIBLE) form A5's "replan" view.
- **Marshalling plan.** This is the last-stretch subset: every physical and documentary item (forms, certificates, bond, Powers of Attorney, model, auditor opinion, USB, copies, sealed and marked envelopes), with issuer, lead time and drop-dead start date.

### 4.9 Dependencies, reproducibility, offline operation

**Runtime dependencies:**

- **PyMuPDF.** Spans with font, size, bbox and superscript flag; image extraction; page rendering for `show`; also writes the one-page A3 PDF, so no second PDF library is needed. **Licence: AGPL-3.0.** That is fine for this assessment. If Lamar later builds on it commercially, swap the `ingest`/`render` internals for pdfplumber + pypdfium2 (MIT/BSD-style licences), which is a one-module change.
- **pydantic.** Typed records and JSON Schema in one dependency.
- **PyYAML.** Curated inputs, using `safe_load`. Dates are kept as strings validated by the schema, to avoid YAML's implicit date typing.
- **numpy.** Raster structure of image regions (grid, bands).
- **openpyxl.** For A1 in Excel, as the owner's sent email specifies. Added in the stage that writes A1.

**Dev dependency:** pytest.

**Excluded:** pandas, any DB, web framework, vector store, LangChain, OCR engine. Images are handled by readings that a person reviews and approves, not by OCR, at this scale.

**Optional extras (later, §4.6):** HTTP clients for the OpenRouter and Ollama routes, for the drafter only.

**Reproducibility:**

- Python ≥ 3.11 (3.11 used in this environment), dependencies hash-locked in `uv.lock`.
- `make verify` runs the tests, then two clean rebuilds in disposable directories, and compares their output hashes.
- **Output safety:** the build directory may not be the repository, a parent of it, home, `/`, a protected folder (sources, config, curation, tenderpack, tests, docs, worklog, .git, .venv) or anything containing or inside an input. An existing directory is replaced only if it is empty or a previous build. Builds are written to a temporary sibling and swapped in only on success.
- Outputs carry no timestamps and use sorted keys, so Linux (cloud) and macOS should produce byte-identical outputs. This is verified on the Mac, not assumed.

**Offline:** on the Mac, install while online, then run `make verify && pytest` with networking disabled, before submission and again before the session.

**Log separation:**

- `worklog/` is timestamped, append-only and human-written: prompts, model calls, errors.
- `build/` holds deterministic generated evidence, regenerated rather than edited. It is committed for now so the owner can review it; whether to keep committing it is an open question for the owner (§7).
- The deliverables A1–A5 will be generated into their own directory by the later stages, under the same output rules.

### 4.10 Staleness and two build states (planned)

- **Dependency set per interpretation.** Each reviewed interpretation pins: its own unit's effective text; units its text cites (extracted automatically, e.g. fn 12 → the PDD definition; §2.5 → the Table 2-4 *basis* column); units that supply its consequence (e.g. VOL-I §9.4 and the Form 4-C Arabic note); clarification answers and rules that annotate any of these (e.g. ADD-01 §4.2 until ADD-02 §9.2 revoked it); readings and their review status; date-rule anchor values.
- **Staleness.** A row is STALE when the combined hash of its pins changes (C11). Reviewers may add dependencies; removing one needs a recorded reason.
- **Two states.** `validated/` holds the last state where every op was accepted and valid and every affected row re-pinned; `working/` holds an in-progress state (e.g. ADD-03 half-applied), labelled DRAFT/PARTIAL and never written over `validated/`.

### 4.11 Images, Arabic and image tables (built in Stage 1)

- **Regions, generic:** every embedded image; every drawing that is not structure (structure = axis-aligned rules, rectangles that are stroked only, lightly filled or thinner than 2.5 pt, and dark bands with text on them; so a triangle of straight lines, a curve, or a dark box with no text stays a region for review); invisible text layers (recorded, never content); ink nothing explains. A page with text can still have unread regions.
- **Evidence:** native image bytes (hashed), rendered crop, page context, and per-band, per-row and per-cell crops at native resolution; cell crops and positions follow the table's direction.
- **Readings** (`curation/readings/<region>.yaml`, unknown fields rejected): tables (direction ltr/rtl, optional title and qualifier, columns with key, heading and language, rows with every cell, explicit `blank` list, numerals per cell), text and forms (blocks of lines tied to bands), graphics (description). Arabic `source` in logical Unicode order; `translation` separate; matching text computed by code. Numbers in cells are recorded as read (`numeric`: single or range, values in logical order) with the table's headings, qualifier and notes beside them; **what a number means (maximum, minimum, target) is left for a person** (`interpretation: null`).
- **Reading checks:**

  | Check | What it verifies |
  |---|---|
  | RD1 | Region position (doc, page, bbox within 0.5 pt) |
  | RD2 | Native image hash |
  | RD3 | Grid rows × columns from pixels match the reading |
  | RD4 | Every text band (each side) outside a table grid is read (not for graphics) |
  | RD5 | Logical Unicode (no presentation forms, no undeclared bidi controls); translation present |
  | RD6 | Every numeral in Arabic text or Arabic/mixed cells is declared; rendering right to left reproduces the glyph order seen in the crop |
  | RD7 | Warning when text touches the image edge (possible cropping) |
  | RD8 | Unique column and row keys; every row has exactly one cell per column; empty cells only where declared in `blank` |
  | RD9 | Graphic readings carry a description and declare no text |

- **What the checks do not prove:** that any word, mark, digit or value is the one printed, that a translation is right, or what a value means. Numeral identity (e.g. ٢ vs ٣) is advisory only (shape comparison) and never decides.
- **Approval** is recorded only by a person running `tenderpack approve REGION --reviewer "Name"`. It refuses placeholder names and readings that fail checks, and pins the **review subject**: the whole reading (content, uncertainties, source claims, preparer, method) and its evidence (source PDF sha256, region page, bbox and kind, native image sha256). Any change to any of these, even with the transcription unchanged, makes the reading pending again. The program never writes an approval itself.

---

## 5. Verification strategy (designed to disprove the design)

**Independence rules:**

- **Golden facts are written from the rendered pages** into `tests/golden/*.yaml`, with page citations, **before** the corresponding code. They never import curated data.
- **Who writes them:** I write the first set, and the owner independently writes at least 10 rows blind.
- **Disagreements** between the owner's set and mine are logged in the work log as findings.
- **Mutation tests** change *inputs* (synthetic PDFs built with PyMuPDF, or edited op files), not the code under test.

| Risk | Test(s) | Independent oracle | Deliberate input change |
|---|---|---|---|
| Missed footnote | `fn12` unit exists with marker pairing. The row has consequence `rejection` and parameters (2 plants, ≥80,000 m³/day, COD within 10 y of PDD). The C15 sweep maps "rejected without further evaluation" on p4. | Golden YAML from p4 render | Synthetic page with an extra footnote 13 and no matching marker ⇒ C06 ABORT. Footnote text removed ⇒ C03/C15 fail. Footnote moved to the next page ⇒ pairing error reported, not silently orphaned. |
| Unit superscript mistaken for footnote (and vice versa) | All 11 m³ exponents classified as unit exponents (the pack has 12 superscript spans: 11 × "3" after "m" and 1 × "12" after "Form 4-B."; in Table 2-6 the "m" is a separate span, so look-behind must cross spans); "Form 4-B.¹²" yields marker 12 and never a form ID "4-B.12" | Font-level evidence table (§2.1 O1) | Synthetic "Clause 3.1²" with no body ⇒ ABORT. Synthetic "50 m²" ⇒ unit. |
| Missed image region | With readings present, the Form 4-C decl. 4 row exists with consequence `exclusion` (marked pending until approved) and the Table 2-4 TN unit exists | The owner's reviewed Arabic reading | Delete the Form 4-C reading ⇒ C05 structural failure, "VOL-IV p6 not read". The decl. 4 row must **disappear with an explicit gap**, never be replaced by "no consequence". Delete the Table 2-4 reading ⇒ ADD-02/5.1 becomes `unresolved` ("target only in unread image"). Built so far: a straight-line drawing, a dark box and an Arabic right-to-left image table in the synthetic fixture are detected and must be read. |
| Wrong occurrence of repeated text | After ADD-02: VOL-II §4.4 = 96 h **and** VOL-V §31.3 still 72 h; VOL-I §11.2 = 65/35 **and** VOL-V §29.2 still 60/40; Table 2-4 TN = 3 **and** Table 2-2 TN = 55/80; §12.2 still 120 days | Golden values from the pages | Synthetic op targeting VOL-V §31.3 with ADD-02's quote ⇒ provenance mismatch (C21/C25). Synthetic unit containing "seventy-two (72) hours" twice ⇒ C23 "ambiguous". A deliberately buggy global replace in a test double ⇒ C25 ABORT. |
| Deadline change moves dependent dates, preserves fixed ones | Table §2.5 values at BASE and ADD-01 stages; fixed dates unchanged; printed Form 4-A dates raise Issues, not edits | Hand calculation (§2.5), cross-checked against a printed calendar | Synthetic ADD-03 moving the PDD to Thu 3 Dec 2026 ⇒ all relative rules move, fixed don't. Add a holiday on 9 Nov to config ⇒ cut-off moves back one WD. Change convention day0→day1 ⇒ ranges displayed and flagged. |
| Deletion and reinstatement | LCC lifecycle per §4.5 across three stages (A1 statuses, A3 membership only at ADD-02, A5 removal then rework); ADD-01 §4.2 revoked | Golden lifecycle YAML | Swap addendum order ⇒ C26 ABORT. Reinstate a never-deleted unit ⇒ C22. Delete twice ⇒ C22. Drop ADD-02/9.2 ⇒ C20 PARTIAL. |
| Unresolved or unfamiliar wording | Drafter emits `unresolved` for unseen phrasings; build (working mode) applies nothing for them and marks candidate rows AMENDMENT-PENDING; strict build fails | Synthetic provisions written to defeat the patterns | e.g. "Clause 7.1 shall be read as though 'one hundred and fifty' were 'one hundred and eighty'"; "The bid security period is extended by thirty days" (no clause cited). A model-proposed op whose `old` text does not exist ⇒ C23. |
| Traceability | Built: C10 compares every text-layer unit in full with its re-extracted spans. Planned: for every A1 row, evidence items re-extract from their pages and effective text replays from the ops (C16). Timed drill: 3 random rows in under 60 s total. | The PDFs themselves | Built: a unit whose text or one table cell was altered ⇒ C10 structural failure. Planned: a row with no unit, or whose verbatim was "improved" by a model ⇒ C16 ABORT. |
| Reproducible rebuild | `verify`: two clean builds produce identical output hashes; Linux vs macOS manifests compare equal; network disabled | Hash comparison | Flip one byte in a source PDF ⇒ C01 ABORT. Edit a curated file without re-review ⇒ C11 STALE. |
| Live adaptability | **Rehearsals:** (1) treat ADD-02 as unseen early, drafting ops through `draft` rather than by hand; (2) synthetic ADD-03-A written to hit known weak spots; (3) a blind synthetic ADD-03-B written by someone else or a separate model session without sight of this design. Each is timed against the 30-minute budget, with defects logged. | Separately authored addenda | Includes: an image page, a small-print note, a deletion of a reinstated clause, a new form, a clarification answer that changes substance, an incomplete cover summary. |

---

## 6. Staged implementation plan (times in Riyadh time)

Each stage ends with a commit and a work-log entry. **Inspect** means what the owner should look at before the next stage starts.

| Stage | Output | Depends on | Main risk | Acceptance evidence | Owner inspects |
|---|---|---|---|---|---|
| **1. Evidence and units** (built sessions 02–03; awaiting the owner's acceptance) | `ingest`, `show`, `approve`; `build/units.json`; coverage, exclusions; review packets and proposed readings for Table 2-4 and Form 4-C | Plan approval; Python env | Segmentation of tables, forms and footnotes; watermark removal eating content; readings trusted before review | C01–C10 pass; golden and regression tests; byte-identical rebuild; readings pending | Coverage report; units against pages; **both readings reviewed and approved or corrected by the owner** |
| **2. Thin end-to-end slice through the hard amendments** (built session 04, §10; 26 rows) | `amend` with target verification (§4.4.1), `dates`, minimal `register` with evidence items and pins (§4.3, §4.10), `checks`; ~12 rows (LCC, PDD and dependants, fn 12, 72 h, weighting, TN, Form 4-G, Form 4-C); first A1/A2/A3/A5 renders. **ADD-02 drafted through `draft` as if unseen.** | Stage 1 | The op model is the wrong shape; better found now than later | Golden tests: LCC lifecycle, scope traps incl. the wrong-clause op, date table, Form 4-A Issue; C20 reports exactly the not-yet-mapped provisions | LCC chain in A2; dates table; A3 draft layout |
| **3. Full register and Issues** (built session 05 as a working draft, §11; 202 rows, all proposed) | All units dispositioned; all ADD-01/02 provisions mapped; ~80–120 rows (model-drafted, reviewed in tiers); `issues.yaml` with human-decision items assigned to roles | Stage 2 | Review time; over- or under-splitting rows | `build --strict` passes except deliberate open Issues; C14/C15 sweeps clean; A3 fits one page | A3 candidates (all); Issues list; 15 random rows; the owner's 10 blind golden rows compared |
| **4. A5 programme and marshalling** (built session 05 as a working draft, §11; lead times PROVISIONAL) | `schedule`; activity templates; `assumptions.yaml` (with basis and owner); per-stage A5 with replan deltas; optional Gantt rendered from the same data | Stage 3 | Lead-time assumptions dominate the result; infeasibility must be shown, not hidden | Tests: backward pass, the clarification "must finish by" constraint, INFEASIBLE detection, LCC rework, bond re-issue rework, deleted-row activity removal | **The assumption values (owner's call)**; the infeasibility list |
| **5. Unseen-addendum readiness** (partly done: drills A and B, one live fix; the blind addendum not run) | `show`, `diff`; drafter hardening; synthetic ADD-03-A and a blind ADD-03-B; two timed rehearsals; one rehearsed "live fix" (add a check and its test) | Stages 2–4 | Live time overrun; brittle patterns | Each rehearsal completes within 30 minutes with all provisions accounted for; defects fixed and logged | Rehearsal timings and work-log error notes |
| **6. Packaging and Mac verification** (Mon 5 Oct, by 14:00) | Strict build; A3 PDF; A1 CSV/JSON/Excel; A2 MD+CSV/JSON; A5 CSV/JSON; one-page operating procedure; final work log; archive | Stage 5 | Environment drift on the Mac; time | `make verify` on the Mac with networking off; manifests equal to cloud build | Final A3 read cold; archive contents |

**If behind schedule, cut in this order:** Gantt → model drafter (keep patterns plus `unresolved`) → second rehearsal. A1 Excel stays (owner's specified format). Never cut: C10/C13/C16/C25 checks, A3 unresolved list, Stage 5 rehearsal 1.

---

## 7. Decisions needed from the owner

| # | Decision | Options | Recommendation and trade-off |
|---|---|---|---|
| D1 | **Planning basis for A5:** status date and bidder | — | **Settled (owner, 1 Oct email; confirmed by the hiring team's reply, 2 Oct):** status date = latest addendum issue date (22 Oct 2026; the ADD-03 date live); unnamed bidder, **three members by default, editable in config**; all bidder details are configurable assumptions, flagged for confirmation, never facts. (4 of 5 prequalified consortia have 3 members; Northwind has 2.) |
| D2 | **A3 inclusion rule** | — | **Settled (owner, session 02):** explicit document wording only (rejection / disqualification / non-responsive / exclusion, including the footnote and the Arabic image), plus a separate line for §11.3 score elimination, and a separate labelled block "Mandatory under §11.1(i) but no stated consequence; human to judge". Unresolved legal and commercial questions stay with people. |
| D3 | **A1 scope and granularity** | (a) One row per independently evidenced obligation (e.g. bond: amount; form/terms; issuer rating), including VOL-II technical and VOL-V contractual obligations, tagged by assessment type. (b) One row per clause. (c) Bid-stage only. | **Applied (owner, session 04):** independently testable obligations, grouped by clause (`group`) and tagged by scope (`scope`), e.g. VOL-I 6.4 → `VOL-I-6.4-01` (amount and form) and `VOL-I-6.4-02` (issuer rating). |
| D4 | **Conservative-reading policy for unresolved counting conventions** (day 0, inclusive look-back, forward WD, holidays) | (a) Block until a person decides. (b) Compute every reading, schedule on the most conservative, and flag. (c) Pick one silently. | **Applied (owner, session 04):** every plausible counting reading is computed and shown (A1 Dates sheet); planning uses an explicit, configurable assumption, `planning.counting_policy: conservative` in `config/assumptions.yaml`. |
| D5 | **Build strictness** | (a) Always strict. (b) Working mode emits with FLAGs and labelled PARTIAL addenda; `--strict` for submission. | **(b)**, refined: structural failures always fail (exit 2, previous build kept); pending review is shown, not a failure (`--require-approved` exits 3); PARTIAL addenda are labelled at the top of A3 and written to `working/` (§4.10). |
| D6 | **Model use** | Routes of §4.6 | **Deferred by the owner** (the hiring team confirmed on 2 Oct that hosted APIs, local models and an AI coding assistant are fine, including live, if documented): the Claude Code / OpenRouter / Ollama routes and model selection come later; the reviewed build stays offline-capable without a model. |
| D7 | **Committing `build/`** | (a) Keep committing generated evidence. (b) Commit only `units.json` and the packets. (c) Commit nothing generated. | **(a) for now (owner, session 04):** review evidence stays committed: `build/` (Stage 1), `out/` (Stage 2) and the drills (`build/drill-src/`, `build/drill/`, `out-drill/`; drill B in `out-drill-b/`). |
| D8 | **How a person accepts rows and ops** (C29 deviation, §10) | (a) Edit `review:` flags. (b) A named `tenderpack accept` / `reject` command. | **Built as (b) in session 06** at the owner's direction: decisions bound to the fingerprint of the item, its evidence and its dependencies (`curation/reviews/decisions.yaml`); a later change voids them; flags never count. Using it is the owner's step. |
| D9 | **Provisional A5 assumptions** (lead times, resources, counting of copies) | Owner or a named person per discipline confirms or corrects `config/assumptions.yaml` | **Open (sessions 05, 06).** The LCC lead time decides the main infeasibility (§11). |

**Kept visibly with people:**

- These are surfaced as Issues, not as decisions the system makes.
- **The issues:** Form 4-A date and missing fields (O4); Envelope B contents (F4); Form 4-B contract value (F5); concession term (F6); design flows (F7); Permit vs Table 2-4 (F8); Form 4-G "No" answers (F10); what to raise as clarifications before 12 Nov 2026; the owner's review of both image readings (O5, Table 2-4), including what the Table 2-4 ranges under "all values are maxima" mean.
- **Bidder facts:** all bidder facts.

---

## 8. Next step

The owner's review, in the order of `out/review/index.html`: the two image readings, the disqualifier rows, the amendment ops, the three STALE-row proposals, then the remaining rows; the LCC lead time and the legal calls (`docs/session-06_report.md` §4). Then the Mac verification (`docs/VERIFY_ON_MAC.md`) and the live session. Final submission is not started; the owner asked to stop before it.


---

## 9. Stage 1 status (sessions 02 and 03; awaiting the owner's acceptance)

**Built:**

- **Package and commands.** `tenderpack/` (sources, extract, regions, segment, readings, arabic, packets, coverage, cli). Commands: `ingest [--require-approved]`, `show`, `approve --reviewer NAME [--approvals PATH]`.
- **Exit codes.** 0 structure OK (pending review printed); 2 structural failure (previous build kept, failed build in `<out>.failed`) or refused output path; 3 pending review with `--require-approved`.
- **Environment.** `pyproject.toml` with `uv.lock`; `Makefile` targets `setup`, `evidence`, `test`, `verify`. Runtime: PyMuPDF 1.28.2, numpy, pydantic, PyYAML. Dev: pytest. openpyxl comes with the A1 stage.

**Session 03 (owner's review):** six gaps reproduced, regression tests written first and seen failing, then fixed: §3.3 numbered-paragraph boundary and table continuation across intervening content (§2 of the session log); structural errors fail (C07–C10, exit codes) and C10 compares whole texts; approvals pin reading + uncertainties + evidence and need a named reviewer; RD8 cell validation and number-vs-meaning separation; straight-line drawings and dark boxes stay visible; the Arabic right-to-left image table exercised end to end; output paths guarded and builds atomic. Details, failures and test results: `worklog/2026-10-02_session-03_review-fixes.md`; summary: `docs/session-03_before-after.md`.

**Evidence to review** (regenerate with `make evidence`):

| File | Contents |
|---|---|
| `build/units.md` / `build/units.json` | All 524 units of the real pack, including units from the two readings, marked PENDING |
| `build/coverage.md` | Checks C01–C10, page accounting, regions, superscripts, footnotes, split tables, small print, full-evidence results |
| `build/exclusions.md` | The 160 excluded spans (5 rules × 32 pages) |
| `build/review/VOL-II-p3-r1/packet.html` (and `.md`) | Table 2-4: each heading, row and cell crop beside its reading; checks; points for decision |
| `build/review/VOL-IV-p6-r1/packet.html` (and `.md`) | Form 4-C: each band crop beside its reading and translation; numeral evidence; points for decision |
| `build/fixture/` | The same reports for the synthetic mixed example, including the Arabic RTL image table |

**Decisions still open with the owner:** acceptance of Stage 1; review of both readings (packets); D3 (A1 granularity); D4 (counting conventions); D7 (committing `build/`); the session slot once the panel confirms it.

---

## 10. Stage 2 status (session 04; a slice, not the full register)

**Commands:** `outputs` (A1/A2/A3/A5 from a published evidence build), `draft ADD-0N` (propose ops for an addendum), `pin` (pin interpretations to their dependencies); Makefile `outputs`, `drill`. Outputs: `out/`; drill: `build/drill-src/`, `build/drill/`, `out-drill/`.

**Modules:**

| Module | Responsibility |
|---|---|
| `citations.py` | Citations in addendum wording ("Volume I Clause 8.5", "footnote 12 to Clause 8.5", "Table 2-4 of Volume II", "Section 4.2 of Addendum No. 1", "Form 4-G", "after item (e)") resolved to unit ids; `verify_target` (§4.4.1) |
| `amend.py` | Op model (replace_text, set_value, append_text, set_status, replace_unit, insert_unit, annotate) and the engine: stages BASE → ADD-01 → ADD-02 → …, checks C20–C27, provision coverage, scope (C25), the validated vs working state |
| `draft.py` | Pattern drafter: proposes ops from the addendum's wording; anything it cannot type becomes `unresolved`. Used for every addendum with no curated op file; the curated ADD-01/ADD-02 files started from its output |
| `dates.py` | Working-Day calendar (VOL-I 2.4), date rules, every plausible counting reading, the planning reading under the configured policy |
| `register.py` | The A1 slice: rows evaluated at every stage; interpretations pinned to dependency hashes (STALE on change); separate statuses for the documents, the image reading, the interpretation and the ops; printed-date conflicts (C31) |
| `schedule.py` | A5: activities from the evidence items of rows in force; backward pass in Working Days; INFEASIBLE / DEADLINE PASSED flags; stage-to-stage deltas |
| `render.py`, `stage2.py` | Deterministic A1 xlsx/csv/json, A3 one-page PDF; orchestration, checks and safe publication |

**Checks implemented in this slice:** structural (nothing published, exit 2): E01 (evidence build OK and current), C16 (each interpretation and consequence quote found in the effective text at every stage where the row is in force), C25, C13, C40, C43. Reported: C20 and C21–C27 (they make an addendum PARTIAL), C11 (STALE), C31 (printed dates, raised as an Issue), C26 as an engine problem. Not yet built: C12, C14, C15, C28, C29 (see below), C30, C32 as a check, C41, C42 for Stage 2 outputs beyond the determinism test. *(Session 05 added C14, C15, C44, C45 and the release gate: §11.)*

**Deviation from §4.7 (C29), for the owner to decide:** no person has accepted any op, so applying only accepted ops would produce nothing. This slice applies PROPOSED ops and carries their review status into every output (A1 "Amendment ops review", A2 "Review", the banners of A1 and A3).

**Inputs written by the assistant (proposals, not reviewed):** `curation/amendments/ADD-01.yaml`, `ADD-02.yaml` (ops and dispositions, started from the drafter), `curation/register/rows.yaml` and `issues.yaml`, `curation/activity_templates.yaml`, `config/assumptions.yaml` (lead times with basis and owner). `curation/register/pins.yaml` is machine-written by `pin`.


---

## 11. Stage 3 and Stage 4 status (session 05; working drafts)

**The owner's code review of Stage 2:** five findings, reproduced, failing tests first, fixed:

- `amend.py`:
  - transactional ops;
  - value, column and replacement-content checks (C21, C22).
- `draft.py`: one op per change; any remaining text is flagged unresolved.
- `load_evidence`: verified against the build manifest and the anchors' pages.
- Pins include the image review fingerprint (pin format 2).
- Provenance: the latest source is cited, and original and effective text are kept apart in A1–A3.
- A5 is checked in both directions: C40, C44, C45.

Before/after evidence: work log §2 and §4.

**Stage 3 (register):**

- **Dispositions:**
  - every one of the 421 volume units has a disposition (`curation/register/dispositions/`);
  - links between dispositions and rows hold in both directions;
  - every ADD-01/ADD-02 provision is an op or a reasoned no-effect, and nothing is "outside the slice".
- **Rows:** 202, each with an owner, evidence (or a no-deliverable reason), scope, assessment and status at every stage.
- **Sweeps:**
  - C14 obligation sweep: 16 hits listed for a person;
  - C15 consequence sweep (English and Arabic): 45 hits, all linked.
- **Issues:** 23 curated issues, each with an owner.
- **Command:** `check-register`.

**Stage 4 (A5):**

- **Coverage:** activities for all 26 evidence items, documents per envelope (A: 16 items, 108 physical copies; B: 4, 16), issuers, multiplicities and resource load.
- **Assumptions:** PROVISIONAL capacities and lead times, each with basis and owner.
- **Drivers:** what would make each infeasible activity feasible.
- **Scenarios:** consortium size, LCC lead time, hypothetical holidays, combined.

**Release gate:**

- Working drafts list their blockers (coverage, stale, approval).
- `outputs --strict` refuses a release (exit 3).
- The program never approves or accepts anything.

**A3:** one page, at 7.5 pt minimum, with linked detail (`a3_detail.html`) and the documents referenced but not supplied.

**Rehearsal:**

- drill B (`make rehearsal`): two changes in one paragraph, a new obligation, an image-table change, and two change types not seen in ADD-01/ADD-02 (whole-clause replacement, new-clause insertion);
- one live fix of the drafter;
- results in `docs/session-05_report.md` §3.

**Open:** the owner's decisions in `docs/session-05_report.md` §5. These include D8 (how a person accepts rows and ops) and D9 (A5 assumptions).

## 12. Session 06 status (review fixes, decisions, live commands, blind rehearsal, draft archive)

**The owner's four findings:** reproduced on `3c97a8d`, then 12 failing tests (with 4 passing controls) before any fix. Each fix is a rule, not a case:

| Finding | Fix |
|---|---|
| 1 | The whole inserted text must be printed in the addendum (C21); every word a unit gains must be printed in that stage's addendum (C47, structural) |
| 2 | Benign wording must match a whole sentence; any qualifier or change words in the remainder make the provision unresolved |
| 3 | Obligation trace to A1, A3 and A5 (C46) |
| 4 | The release gate counts only decisions bound to content. A3 shows each item's confidence and the full requirement, and appends the current quote where its figures are missing; accurate status labels |

**D8 built:**

- `accept`/`reject` bind each decision to a fingerprint of the row or op, its evidence items and its dependency values; a change shows it as CHANGED;
- a rejected op is withdrawn and its addendum becomes PARTIAL;
- three STALE-row proposals are prepared and not applied (`apply-proposal`);
- review batches in `out/review/`.

**Live commands:**

- `show ROW`: pages, crops, amendment chain, A5;
- `diff`: requirements, STALE, voided decisions, image-read values, A3, programme.

**Coverage:**

- C12 (row-id ledger);
- C30 (every date or period phrase treated; an `unresolved` kind and note keep unsupported periods explicit, never computed);
- C32 (counting conventions reported);
- month and week units;
- renumbering as an annotation effect;
- requirement summaries checked against the effective text.

**Blind rehearsal** (`rehearsals/blind-01/COMPARISON.md`):

- An independent agent wrote Addendum No. 3 from the sources and the brief; its key was frozen by hash in `53ad76f` before the start.
- 22 hits, 4 partials, 1 miss (renumbering); 12 min 13 s; four generic live fixes; one refusal (A3 over one page) resolved before publication.
- Three fixes after the comparison are not counted.
- **Limits:** the brief named the categories of change; the curator was the assistant.

**Draft archive:** `scripts/make_draft_archive.py`; the verification is recorded in the session 06 work log §7.

**Open:** the owner's decisions in `docs/session-06_report.md` §4.

## 13. Session 07 status (cover-summary check, review packets, archive)

**C28** (`tenderpack/summary.py`):

- Each addendum's "This Addendum …" sentence is parsed into claims (verb + the things it names). Claims are matched to the provisions' ops by:
  - cited targets (including plural "Clauses 4.4 and Table 2-4");
  - the register's date anchors ("the Proposal Due Date" → VOL-I 6.1);
  - answer ranges;
  - for descriptive claims, the best-matching subject.
- It reports, for a person: **omitted** (a change or obligation no claim covers), **understated** (an answer that changes or adds something; a clause reinstated in an amended form), **consequence not mentioned**, **contradicted** (verb, range or count), **not found**, **claimed, not applied** (the op is invalid or rejected) and **unchecked** (a provision still unresolved).
- **Report only:** A2, the A1 Issues sheet (`I-AUTO-SUMMARY-<stage>`), `diff` and checks.json. Never structural, never a release blocker, never on A3.
- **The summary is never applied:** the engine does not read it, and the drafter now removes summary sentences before matching and drafts only obligations from cover text.

**Real pack:**

- **ADD-01:** Appendix A's reissue of Form 4-A and 3.1's five-Working-Day reporting duty are omitted; the answer to request 4 adds a duty.
- **ADD-02:** note (2) to the reissued table amends VOL-I 11.2 (60/40 → 65/35); 9.2 ends ADD-01 4.2; 5.2 adds a design duty — all omitted. 9.1 reinstates 8.6 in an amended form (35%, a new consequence) and 7.2's non-responsive consequence is not mentioned.

**Tests** (`tests/test_session07_summary.py`):

- the real-pack findings, written from the printed addenda before C28 existed;
- a misleading summary over the same provisions leaves every applied unit identical;
- a misleading synthetic Addendum No. 3, end to end: every planted error is reported;
- the drafter drafts no change from cover text;
- a regression on blind rehearsal 01, where the key's six summary omissions are reported. This is not blind evidence: C28 was written after the key was opened.

**Review packets:** `out/review/packets/` carries the full packets of both image readings (native crops beside every band, cell and numeral; Arabic right to left), linked from batch 1 and the index.

**Open:** the owner's review and the decisions in `docs/session-06_report.md` §4. Decision 8 is settled: keep the full history as it is.
