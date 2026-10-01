# Tender Pack Reader: Engineering Plan

> **STATUS (revision 2, session 02, 2026-10-02):**
> - **Direction:** accepted by the owner.
> - **Stage 1:** approved with adjustments, and implemented (see §9).
> - **Stages 2–6:** remain PROPOSED and wait for the owner's review of the Stage 1 evidence.
> - **Revision 1:** session 01, planning only, recorded in `worklog/2026-10-01_session-01_planning.md`.
> - **This revision:** the owner's adjustments and their effects are listed in §R2 directly below. Where a §R2 item conflicts with older text further down, §R2 wins.

## §R2 Revision 2: owner adjustments and corrections (2026-10-02)

| # | Owner instruction or correction | Effect on this plan |
|---|---|---|
| R2.1 | Use the assumptions and output formats in the sent email of 1 Oct (thread PDF now in `sources/correspondence/`). Bidder details remain configurable assumptions, not facts. | **Adopted, not challenged.** Planning date = latest addendum date (22 Oct 2026; the ADD-03 date in the session). Unnamed **three-member** consortium, with name and member count editable (note: Appendix 1 has one two-member consortium). Bidder facts flagged for confirmation. External assumptions (holidays, durations, roles) labelled with their basis. **Formats:** A1 CSV + JSON + **Excel**; A2 Markdown + CSV/JSON; A3 one-page PDF; A5 CSV + JSON; A4 = repository, commit history, prompts, model-call log, work log. Offline rebuild, no API key. This settles D1 and the format question. |
| R2.2 | Keep explicit disqualifiers separate from obligations with no stated consequence. Leave unresolved legal/commercial questions with people. | **D2 settled as recommended:** the A3 main list holds explicit wording only; a separate labelled block lists mandatory items with no stated consequence. Legal and commercial questions become Issues owned by a person. |
| R2.3 | Matching a quotation and changing the declared target does not prove the target is the right clause. | New **target-verification** design: §R2-A. |
| R2.4 | Keep original evidence separate from effective amended text. Assembled text may exist on no single page; image text cannot be checked through the text layer. | New **evidence model**: §R2-B. The old check C10 ("verbatim is a substring of the effective text and on the cited page") is replaced. |
| R2.5 | A clause's own hash is not enough to detect stale interpretations. Track dependencies, and keep partially applied changes separate from the last fully validated state. | New **dependency pins** and **two-state build**: §R2-C. Refines D5. |
| R2.6 | Withdraw the claim that the amended TN limit necessarily satisfies the missing Environmental Permit. | **Withdrawn** (F8 corrected). The Permit is not in the pack, so compliance with it cannot be established. The system will say "Permit not supplied; compliance with it cannot be established", not "3 mg/l satisfies either reading". |
| R2.7 | Images, Arabic and image-based tables must work from the foundation, not only for the two known images. | Implemented generically in Stage 1: §R2-D. Exercised on a synthetic mixed page as well as the pack. |
| R2.8 | Preserve crops and page references beside readings. Tables keep row/column relations, headings, units, limits, basis and notes. Arabic source is kept separate from translation and matching text. Check numerals, RTL order and rendered output. | Implemented in Stage 1: §R2-D. |
| R2.9 | The owner reads Arabic and will review. Give crops and proposed readings together, with uncertainties marked; sign-off stays pending until approved. | Review packets in `build/review/<region>/`. Approval only through `curation/approvals.yaml`, pinned to the reading's content hash. |
| R2.10 | Do not discard all rotated text. Identify the watermark specifically and show what was excluded. | Watermark rule matches text, colour, size and angle together. Everything excluded is listed in `build/exclusions.md`. A decoy identical except for colour is kept (tested, including by mutation). |
| R2.11 | Later: the same program runnable through Claude Code in the app, with optional model calls via OpenRouter or local Ollama on the owner's M5 Pro (48 GB). Small common interface, same validation and review rules, capabilities checked rather than assumed. Implement later; the reviewed build must stay offline-capable. | Design only in this revision: §R2-E. Nothing implemented. |
| R2.12 | Keep the work log accurate. Finding the second image was an *additional* finding, not a correction of a claim that only one existed. | O5 wording corrected below. Recorded as a characterisation error in the session 02 work log. |

### §R2-A: Catching an operation that points at the wrong clause with the same wording

A quotation found in the declared target, plus a change confined to that target, proves only that the operation is *internally consistent*. It does not prove the addendum meant that clause. In this pack, "seventy-two (72) hours" occurs in VOL-II §4.4 and VOL-V §31.3; an op aimed at §31.3 would pass the substring, uniqueness and scope-leak checks. The defence must come from evidence that is independent of the op author:

1. **Citation resolution (primary).**
   - The program extracts the target citation from the addendum's own provision text (for example, "In Volume II Clause 4.4, …") and from its section heading ("4. AMENDMENT TO VOLUME II CLAUSE 4.4").
   - It resolves each, deterministically, to a unit ID, using a grammar covering Volume/Clause/Table/Form/footnote/Appendix and row names inside tables ("the limit for Total Nitrogen (TN)" → `VOL-II:T2-4/TN`).
   - The op's declared target must equal the resolved target. Body and heading citations must agree with each other.
   - **On failure:** the op is invalid, with the message "declared target X ≠ cited target Y".
2. **Ambiguity disclosure (secondary).**
   - For every quoted "old" text, the program lists *all* units in the pack that contain it.
   - With more than one candidate, the review view shows the others ("also in VOL-V §31.3 — not targeted") and requires the citation to pick exactly one of them.
3. **Self-consistency claims in the addendum.**
   - Statements such as "Volume I Clause 8.6, deleted by Addendum No. 1 Section 4" are checked against the op ledger (was it deleted, and by that provision?).
   - Statements such as "marks for D increased and B reduced correspondingly" are checked against the data.
4. **When the addendum cites wrongly itself** (its cited clause does not contain the quoted text): the op cannot be validated. It becomes `unresolved`, with an Issue "addendum citation and quotation disagree", for a person to resolve. Nothing is auto-corrected.
5. **Tests:**
   - an op aimed at VOL-V §31.3 using ADD-02 §4.1's quote must fail on citation mismatch;
   - a synthetic addendum whose citation and quote disagree must produce `unresolved`.

### §R2-B: Original evidence is kept apart from effective (amended) text

Each A1 row and unit carries two different things:

- **Evidence items.** Each is checkable on its own, against the place it came from:
  - `text_layer`: verbatim span IDs on one page of one document. Checked by re-extracting those spans from the PDF (hash-pinned source).
  - `image_reading`: a region, a crop (sha256), and the reading's content hash. Checked against the reading record and its approval status, **not** the text layer. A pending reading is evidence marked *pending*, never silently trusted.
- **Effective text.** Derived, labelled "assembled by ops [...]". It is checked by **replaying the ops** from the original evidence, never by looking for it on a page, because, for example, "… ninety-six (96) hours" after ADD-02 exists on no single page.

A2's chain therefore shows the effective text with its evidence items: the original clause span on VOL-II p4 and the replacement span on ADD-02 p1, each verifiable where it lives.

### §R2-C: Dependency pins and two build states

- **Dependency set per interpretation.** Each reviewed interpretation pins a dependency set, not just its own clause text. The set includes:
  - its own unit's effective text;
  - units its text cites, extracted automatically (e.g. fn 12 → the PDD definition §2.6 and §6.1; §2.5 → the Table 2-4 *basis* column);
  - units that supply its consequence (e.g. VOL-I §9.4 and the Form 4-C Arabic note);
  - clarification answers and rules that annotate any of these (e.g. ADD-01 §4.2, until ADD-02 §9.2 revoked it);
  - readings and their approval status;
  - date-rule anchor values.
- **Staleness.** A row is STALE when the combined hash of its dependency set changes. Automatically extracted dependencies can be extended by a reviewer, but removing one needs a recorded reason.
- **Two states.**
  - `validated/` holds the last state in which every op was accepted and valid and every affected row re-pinned.
  - `working/` holds the in-progress state, for example ADD-03 half-applied.
  - Working outputs are labelled DRAFT/PARTIAL and written separately. They never overwrite `validated/`. A3 from the validated state stays available while the working state shows what ADD-03 breaks.

### §R2-D: Image, Arabic and image-table foundation (built in Stage 1)

- **Region detection, generic, not keyed to the two known pages:**
  - every embedded raster image;
  - non-structural vector graphics;
  - invisible text layers (an OCR layer is recorded, never used as content);
  - ink in a page render that no text, image or drawing explains.
  - A page that has text can still have unread regions; Form 4-C's page has header, footer and watermark text.
- **Evidence:** native image bytes as embedded (hashed), a rendered crop, page context with the region outlined, and per-band, per-row and per-cell crops at native resolution.
- **Raster structure:**
  - **Skew** is estimated from projection profiles.
  - **Grid** rules are detected along the skew, giving rows × columns.
  - **Text bands** are found after despeckling (ink relative to the image's own background, so faint grey text is kept) and after erasing ruling lines.
  - **Rule bands** are told apart from text by shape.
  - **Bilingual rows** are split into left and right halves.
- **Readings:** `curation/readings/<region>.yaml`.
  - Tables keep title, qualifier, columns (heading + key), rows of cells, and notes. Parsed limits are derived by code (`10` → max 10; `0.5 - 1.0` → range).
  - Text and forms are blocks of lines, each tied to a band and side.
  - Arabic `source` is stored as logical Unicode; `translation` is a separate field; matching text is computed by code.
- **Reading checks:**

  | Check | What it verifies |
  |---|---|
  | RD1 | Region position |
  | RD2 | Native image hash |
  | RD3 | Grid rows × columns match the reading |
  | RD4 | Every text band (each side) is read |
  | RD5 | Logical Unicode (no presentation forms, no undeclared bidi controls); translation present |
  | RD6 | Every numeral declared; the rendered glyph order matches the order seen in the crop |
  | RD7 | Warning when text touches the image edge (possible cropping) |

- **Numeral identity:**
  - It is advisory only: shape comparison against reference glyphs, with the margin reported.
  - It never decides; a person does.
  - **Approval** is pinned to the content hash in `curation/approvals.yaml`, and any later edit voids it.

### §R2-E: Model routes (design only; to be implemented in a later stage)

- **Routes.** One small interface, `propose(task_packet) -> proposal_file`, with three routes:
  - `claude_code`: the coding assistant in the app fills the proposal file directly. This is how session 02's readings were prepared, and it is logged as AI-assisted.
  - `openrouter`: an HTTP API.
  - `ollama`: local on the Mac.
- **What every route shares:**
  - the same task packet (instructions, the schema of the expected YAML, crops);
  - the same output path into `curation/`, always `pending`;
  - the same validation (the RD/C checks);
  - the same approval rule.
- **Separation from the build.** No route is ever called by `ingest`/`build`.
- **Capability checks before use:**
  - **Ollama:** `/api/show` returns a `capabilities` list (e.g. `"vision"`). Confirmed from Ollama's API documentation on GitHub; `ollama.com` itself is blocked from this cloud environment.
  - **OpenRouter:** the models listing reports input modalities per model. This could not be verified here (`openrouter.ai` is blocked from this environment) and must be confirmed when the route is built.
  - A model without image input is refused for reading tasks rather than given text-only context.
- **Local candidates for an M5 Pro with 48 GB unified memory.** These come from search results and the Qwen GitHub repository, not from tests, so they are a shortlist, not a choice:
  - Qwen3.8-27B (dense, Aug 2026; image input reported by secondary sources);
  - Qwen3.6-35B-A3B and Qwen3.5-35B-A3B / 27B (MoE/dense, native vision-language per the Qwen repo; Apache-2.0);
  - Qwen3-VL-32B and 8B (dedicated vision-language, 2025; reported strong on OCR including Arabic).
  - At 4-bit, the 27–35B models need about 17–24 GB, so they fit in 48 GB with room for context.
- **Choosing a model.** Benchmark the shortlist on the owner's Mac against the two readings *after the owner approves them*, scoring:
  - cell accuracy on Table 2-4;
  - character accuracy on Form 4-C;
  - digit identity on ٤-x.

  Keep the measured results; don't rely on blog rankings.

---

Conventions used throughout:

- **Doc IDs:** `VOL-I`, `VOL-II`, `VOL-IV`, `VOL-V`, `ADD-01` and `ADD-02` are the six tender PDFs in `sources/candidate_pack/`.
- **Pages:** "p4" is the **PDF page index**. In the tender pack the printed footer "Page N" equals the PDF page. In the brief, printed page N is PDF page N+1, because the schedule page is inserted at the front.
- **Fact labels:** **[F]** marks what a document says. **[I]** marks my interpretation, which needs human confirmation. **[D]** marks a design proposal. Human decisions are listed explicitly.
- **Quotations** are verbatim from the PDFs, apart from whitespace and line breaks.

---

## 0. Time budget (drives every trade-off below)

- **Original schedule** (brief PDF p1; covering email): deadline 17:00 Wed 23 Sep 2026; session 12:00 Fri 25 Sep 2026, Riyadh time.
- **Revised schedule** (`sources/correspondence/2026-09-29_reply_to_hiring.md`): the owner chose "the second path", starting Tue 29 Sep, "with 17:00 Monday 5 October as the outside limit".
- **Time left:** at the time of writing (00:11 Fri 2 Oct, Riyadh) about 3 days 17 hours remain.
- **Correspondence, revision 2:** the Gmail thread PDF (now in `sources/correspondence/`) shows:
  - the hiring team offered the second path on 17 Sep 20:00, and the owner chose it on 17 Sep 20:12;
  - the session is "a ninety-minute slot in the week of 6 October (we will confirm once the panel locks times)", so it is **still to be confirmed**;
  - the 1 Oct email was **sent** (12:50);
  - the note file `2026-09-29_reply_to_hiring.md` is headed "29 September", but the reply it quotes was sent on 17 September.

The plan is sized for roughly 3.5 working days, with a hard requirement that the session environment runs offline on the owner's Mac.

---

## 1. Understanding of the assignment

### 1.1 Deliverables (verified against the brief, §3, PDF p4–p5)

| Artefact | What the brief requires (quoted or closely paraphrased) | Notes |
|---|---|---|
| **A1** Obligations and compliance register | "One row per requirement." Columns: identifier; **verbatim source text**; **document, clause and page**; **pass/fail or scored**; **discipline that owns it**; **evidence needed**; **status after each addendum**; **confidence**. "Machine-readable — CSV or JSON — plus whatever interface you prefer." | "Status after each addendum" requires one status column per stage, not just a final value. |
| **A2** Addendum reconciliation | "What each addendum changed, added and deleted. Which register rows move as a result. Which earlier answers are now wrong. We must be able to trace any row back through the chain to the original document." | Needs the full operation history, not a before/after diff alone. |
| **A3** One page: what would disqualify us | "Every requirement whose breach would put a bid out — **the ones the documents themselves say cause rejection, disqualification or non-responsiveness, not every obligation in the pack** — with your confidence in each. And, explicitly, the list of things your system could not resolve, and why. We read this page first." | The inclusion test is explicit document wording. One page is a hard constraint. |
| **A4** Work log | "The repository with its real commit history. The prompts and model calls you used. And a short written note of every place your system was wrong while you were building it, and how you caught it." | Timestamped and append-only. Kept separate from the deterministic outputs. |
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
- **Missing correspondence:**
  - The hiring team's rescheduling email is absent.
  - `2026-10-01_questions_to_hiring.md` is labelled as a *draft*. I do not know whether it was sent as written; it promises A1 in Excel and A3 as a one-page PDF.
  - No reply to it is in the files.
- **Arabic:** my reading of Form 4-C is a model reading. It must be verified by a competent Arabic reader before it is relied on.
- **No OCR engine** is installed in this container. The two images were read visually by me, not by OCR.
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
| O5 | **Confirmed. Additional finding: a second image region exists** (the observation did not claim there was only one). VOL-IV p6 is a single raster image. The page is *not* text-empty: it carries the running header, the footer and the rotated watermark as text, so a "page has text ⇒ covered" heuristic would wrongly pass it. Coverage must be judged per image region (C05), not per page. My reading (to be verified by an Arabic reader) is listed after this table. **Declaration 4 carries an exclusion consequence that appears nowhere in the English text.** **Additional finding:** VOL-II p3 **Table 2-4 (effluent limits) is also an image.** ADD-02 §5.1 amends TN "from the value shown", so the old value (5 mg/l) exists **only in the image**. | VOL-IV p5–p6; VOL-II p3; ADD-02 §5.1 p1; ADD-02 Q9 p2 | Form 4-C decl. 4: "وندرك أن أي بيان غير صحيح يؤدي إلى استبعاد العرض" ("we acknowledge that any incorrect statement leads to the exclusion of the proposal"). Note: "عدم تقديمه كاملاً يجعل العرض غير مستجيب" ("failure to submit it completely renders the proposal non-responsive"). ADD-02 §5.1: "the limit for Total Nitrogen (TN) is amended from the value shown to 3 mg/l, assessed on the same basis." | [F] Form 4-C remains mandatory in Arabic, one per member (ADD-02 Q9). TN = 3 mg/l, 30-day rolling average ("same basis" resolved from the image). | Arabic transcription and translation need **human verification**. The digit order of "البند ٤-٢" in right-to-left text reads as 4-2, i.e. VOL-I §4.2. That is consistent with "communication rules"; §2.4 is the Working Day definition. Must be verified, not assumed. |
| O6 | **Confirmed. ADD-01's list is explicitly non-exhaustive** ("including without limitation"). **Added:** VOL-I §8.3, "ISO 9001:2015 … current as at the Proposal Due Date", also moves but is not in ADD-01's list. **Added:** the new clarification cut-off falls on **Thu 12 Nov 2026, the old PDD**. A naive stale-value scan for "12 November 2026" would mis-flag it. | ADD-01 §2.2 p1; VOL-I §2.4, §2.6, §3.4, §5.2, §6.3, §6.7, §7.1, §8.3, fn 12, App 3; VOL-IV Form 4-A ¶2 | ADD-01 §2.2: "Every period in the RFP Documents that is calculated by reference to the Proposal Due Date is adjusted accordingly, including without limitation…" VOL-I §2.4: "Where a period expressed in Working Days is to be counted backwards from a stated date, the stated date itself shall not be counted." | See §2.5 (date inventory): computed values before and after, fixed dates, and dates anchored to unknown future events. | "days" is undefined (calendar days assumed). Whether "from the PDD" makes the PDD day 0 is unstated. The forward Working-Day convention is unstated. No time-of-day for the cut-off. Public holidays "declared" in the Kingdom need a calendar input (assumption). |

**My reading of Form 4-C (VOL-IV p6). Model transcription; human verification required.** Header: "الهيئة الشمالية للمشتريات المرفقية" / "النموذج ٤-ج" / "إقرار عدم تضارب المصالح وعدم الإدراج في قوائم الحظر" (declaration of no conflict of interest and non-listing on debarment lists). The signatories, as authorised representatives of the named consortium member, declare:

1. There is no actual or potential conflict of interest between them and the Authority or any of its advisors regarding this project.
2. The company has not participated, directly or indirectly, in more than one proposal for this tender.
3. The company is not, and has not been in the previous five years, listed on any debarment list issued by a government entity in the Kingdom.
4. All information in the proposal is correct and complete, and any incorrect statement leads to exclusion of the proposal.
5. The signatories commit to the communication rules in clause 4-2 of Volume I. **(Revision 2: the left digit's identity, ٢ or ٣, is uncertain; ٣ would mean clause 4-3, VOL-I §4.3. See the review packet for VOL-IV-p6-r1.)**

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
| F8 | [F] **Table 2-4 is "reproduced" from an Environmental Permit that is not supplied, and the Permit prevails over the reproduction.** ADD-02 amends the reproduction. | VOL-II §2.4 p2; p3 header; ADD-02 §5.1; ADD-01 App B Item 5 | "In the event of any discrepancy between this reproduction and the Environmental Permit, the Environmental Permit shall prevail." Minutes: "the permit was under review by the regulator". | ~~[I] Addenda prevail among RFP Documents (§3.2(a)). Designing to the stricter 3 mg/l satisfies either reading.~~ **WITHDRAWN (R2.6):** the Permit is not in the pack, so whether 3 mg/l, or any other design, complies with it cannot be established. What can be said: the amended reproduction says 3 mg/l, and VOL-II §2.4 says the Permit prevails over the reproduction. | Human decision; clarification on which governs, and the Permit itself, should be requested. |
| F9 | [F] **The Table 2-4 "basis" column (image only) drives obligations elsewhere.** | VOL-II §2.5 p2, §7.2–7.3 p4; VOL-V §29.3, §31.1(b), §31.2, §31.3 p3 | §2.5: "for those parameters identified in Table 2-4 as assessed on a continuous basis". VOL-V §29.3: "a parameter listed in Table 2-4 as assessed on a rolling average basis". §31.2: "not subject to any cap". §31.3: "No cure period applies to an event under Clause 31.1(b)." | The TN tightening propagates to the reliability run (PCOD), Unavailability Events and uncapped deductions. | [I] Continuous monitoring applies to residual chlorine and pH; ramp-up relief applies to BOD5/COD/TSS/TN/TP. Both readings rest on the image. |
| F10 | [F] **Form 4-G (new) has a non-responsive consequence and new obligations.** It is inserted "after item (e)" of VOL-I §9.1, with re-lettering unspecified. The VOL-IV index ("Forms 4-A to 4-F") is not updated. Undertakings 3–6 (security officer, 24 h incident notice, annual OT penetration test, MFA) are not in VOL-II §6. | ADD-02 §7 p3 | "Failure to submit Form 4-G shall render the Proposal non-responsive." | A new A3 row and new A1 rows. | [I] The effect of answering "No" on an undertaking is undefined. Human decision. |
| F11 | [F] **Bid Bond.** Valid 180 days from the PDD; SAR 4,500,000; unconditional, first demand; Kingdom-licensed bank rated ≥ A-. The clause states **no rejection consequence**. | VOL-I §6.3–6.4 p3; ADD-01 Q3; ADD-02 Q8 | "…shall remain valid for one hundred and eighty (180) days from the Proposal Due Date…" | [I] A bond drafted against 12 Nov expires about 14 days early. That is a rework item after ADD-01. | Whether it belongs in A3 depends on the decision in §7 (no explicit consequence wording). |
| F12 | [F] **Mandatory items with no stated consequence.** §11.1(i) makes a "responsiveness and mandatory compliance check on a pass or fail basis", but these clauses do not say what failure causes. | VOL-I §6.3–6.5, §8.3, §8.4, §8.7–8.10, §10.1, §10.3 | "Proposals will be evaluated in three stages: (i) a responsiveness and mandatory compliance check on a pass or fail basis…" | n/a | **Classification decision** (see §7). The brief limits A3 to explicit document wording. |
| F13 | [F] **Referenced but not supplied:** Volume III (Drawings, incl. Drawing 03-C-114); the Environmental Permit; the ESIA and geotechnical report ("data room"); VOL-V Schedules 7, 9, 11 and 12; the Direct Agreement; RFQ NUPA/ISTP/2025/031; the "Authority's standard five-point scale"; and "appendices expressly permitted by Volume II" (none found in the extract). | VOL-I §3.1, §3.2(f), §3.4; VOL-II §2.4, §5.1, §9.1; ADD-01 Q4; VOL-V §29.2, §31.2, §39.1, §39.5, §40.1; ADD-02 note (3) | VOL-I §3.4: "No claim arising from an alleged omission shall be entertained after the Proposal Due Date." | Gaps must be raised before the clarification cut-off (12 Nov). | Owner's 1 Oct email already asks about Volume III. No reply is on file. |
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

**Window from ADD-02 issue to PDD:** 35 calendar days, 24 Working Days.

---

## 3. Critique of the proposed direction

| Direction | Verdict | Why | Where it could fail, and what I'd change |
|---|---|---|---|
| **A. Evidence before interpretation** | **Sound; keep it light.** | Hashes, page counts and page/bbox anchors are cheap, and they are exactly what the "show me the page within a minute" check needs. | **Watermark contamination.** In layout mode, pdftotext interleaves watermark letters ("CK", "PA", "EN", "SS", …) into clause text. Extraction must be rotation-aware (drop lines whose direction ≠ horizontal) or verbatim matching will fail. **Keep normalisation minimal and declared:** de-hyphenation, whitespace, quote marks, superscript marking, watermark/header/footer removal by **exact, audited patterns**. Don't build a general normaliser. |
| **B. Original units + ordered typed amendments → derived effective state** | **Sound and recommended.** This is the core of the system. | It is the only representation that answers "what did it say, what changed it, what is it now" without drift. | (1) **Not all amendments are text patches.** The pack has clarification answers, a global re-anchoring rule (ADD-01 §2.2), a suppression rule and its revocation (ADD-01 §4.2 / ADD-02 §9.2), a new form, a table reissue, a value restated without quoting the old text (note 2, TN), and non-binding minutes. The op vocabulary must cover these with ~8 types (§4.4), not an open-ended DSL. (2) **The biggest failure mode is not the text; it is the interpretation drifting from the text.** A register row's reviewed attributes (consequence, parameters, evidence) can silently go stale when the unit underneath is amended. Fix: **pin every reviewed interpretation to the hash of the unit text it was reviewed against**. A changed hash makes the row STALE until a person re-reviews it. This is the mechanism that prevents stale downstream values. (3) **Atomicity:** an addendum is one legal act. Apply its ops in section order, but report it as APPLIED only if every provision is accounted for. Anything else is PARTIAL, labelled at the top of A3. |
| **C. Deterministic trusted build from reviewed inputs; models propose** | **Sound. The manual-work worry is real but manageable.** | Building ~100 rows by hand is too slow, and an un-reviewed model build is indefensible. | **Practical balance:** a model (or pattern) **drafts**, the build only consumes records marked `accepted`, and checks catch what review misses. Review depth is tiered: every A3 candidate, every amended row and every image transcription gets full review; other rows get mechanical verbatim checks plus spot review, and their confidence says so. For the live 30 minutes: a pattern drafter handles the common phrasings seen in ADD-01/02; anything else becomes an `unresolved` op carrying its verbatim text, which a person converts to a typed op or `no_effect` in minutes. The model drafter is an accelerator, not a dependency, so the build works offline. |
| **D. Coverage over retrieval; no vector DB/RAG** | **Agree.** | 32 pages, roughly 25k tokens: everything fits in one model context and in one person's afternoon (brief §2). Retrieval would only add a way to miss things. | "The parser found text" ≠ "every obligation captured". Coverage is shown by **accounting** (every line and image region belongs to a unit; every unit has a disposition) and by **sweeps** (every obligation or consequence phrase, in English and Arabic, maps to a row or an explicit disposition). Correctness is shown separately, by independently written golden tests. |
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
sources/*.pdf ──(1) ingest──► build/extract/*.json        spans: text, font, size, bbox, superscript, direction
     │ sha256, pages                │                      furniture removed by audited rules
     ▼                              ▼
sources/manifest.json        (2) segment ──► build/units.json   SourceUnits with stable IDs (clause, footnote,
                                    ▲                            table row, form field, list item, note, Q&A)
curation/transcriptions/*.yaml ─────┘  image regions → units (human-verified)
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
                         out/ (deterministic; no timestamps) + out/BUILD_MANIFEST.json (input/output hashes)

New addendum:  sources/ADD-03.pdf → ingest/segment → (8) draft ops (patterns → optional model → `unresolved`)
               → person reviews/accepts → build → `diff ADD-02..ADD-03` = "what it broke" → A5 replan.
```

### 4.2 Modules (one responsibility each)

Package `tpr/`; final name to be confirmed, and there is no product naming.

| Module | Responsibility | Why separate |
|---|---|---|
| `ingest.py` | Hash and page manifest; span extraction; furniture removal by declared patterns; image-region detection | The only module touching the PDF library. It can be swapped (e.g. for pdfplumber) without touching anything else. |
| `segment.py` | Spans → SourceUnits: clause numbering from bold leading numbers, footnote pairing (marker ↔ body by number and page), unit-exponent marking, table rows (white-on-dark header detection), form fields, list items, Q&A rows | Segmentation errors are the most likely ingest bug, so they get their own tests. |
| `model.py` | Typed records (pydantic) and JSON Schema export | A single definition of every entity. |
| `amend.py` | Applies accepted ops per stage; pre/post-condition checks; scope-leak diff; op ledger | Core correctness logic, kept pure. |
| `dates.py` | Calendar (weekend, holidays), date rules (fixed / relative / external-anchor), conventions, per-stage evaluation | Date errors are high-impact; pure functions. |
| `register.py` | Joins interpretations with stage states; verbatim and pin checks; status per stage | — |
| `checks.py` | Registry of check functions plus data lexicons (obligation and consequence phrases in EN/AR, unit tokens) | This is where the live "catch this kind of error" change happens. |
| `schedule.py` | Evidence → activity templates → backward pass → A5 programme and marshalling | — |
| `render/` | `a1.py`, `a2.py`, `a3.py` (one-page PDF), `a5.py` | Presentation only; no logic. |
| `draft.py` | Pattern drafter for ops; `unresolved` stubs; optional model drafter that writes proposals and logs prompts | Never imported by `build`. |
| `cli.py` | `ingest`, `draft ADD-0N`, `build [--strict]`, `show ID`, `diff A..B`, `verify` | — |

### 4.3 Essential entities

- **SourceDocument**
  - Fields: `doc_id`, `path`, `sha256`, `pages`, `kind` (volume/addendum), `number`, `issue_date`.
- **Region**
  - Fields: `doc_id`, `page`, `bbox`, `kind` (text/image).
  - Image regions need a **Transcription**: `text`, `lang`, `translation`, `method` (model/human), `verified_by`, `source_sha`.
- **SourceUnit**
  - Fields: `unit_id`, `doc_id`, `kind`, `parent`, `pages` and `bboxes`, `verbatim`, `normalized`, `origin` (text-layer / transcription), `lang`, `binding` (e.g. minutes = false).
  - Example IDs: `VOL-I:8.5`, `VOL-I:8.5#fn12`, `VOL-II:T2-4:TN`, `VOL-IV:F4-C:decl4`, `ADD-01:AppA:F4-A:pdd`, `ADD-02:3:note2`, `ADD-02:Q7`.
- **Operation**
  - Fields: `op_id`, `addendum`, `provision` (unit of the addendum), `source_quote`, `type`, `target`, `params` (`old`, `new`, `occurrence`, `new_unit`, `status`), `expect` (optional assertions), `review` (`status`: proposed/accepted/rejected/unresolved; `origin`: pattern/model/human; `by`).
- **UnitState** (derived)
  - Fields: `unit_id`, `stage`, `status` (active/deleted/revoked), `text`, `text_sha`, `history` (op IDs).
- **Requirement** (A1 row)
  - Fields:
    - identity and source: `req_id`, `units`, `verbatim` (must match stage text);
    - classification: `kind`, `assessment` (pass_fail / scored / contractual-post-award / procedural / informational);
    - `consequence`: `{class, quote, unit}` or `none_stated`;
    - ownership and evidence: `discipline`, `evidence` (EvidenceItem IDs), `parameters`;
    - links: `date_rules`, `depends_on`, `issues`;
    - confidence: `read_confidence` `{level, reasons}`;
    - review: `reviewed` `{by, against_sha, stage}`.
  - Per-stage overrides are stored only where the interpretation differs.
- **EvidenceItem**
  - Fields: `ev_id`, `type`, `issuer` (internal role / external body), `per` (bidder / member / signatory / reference / envelope), `multiplicity`, `req_ids`.
- **DateRule**
  - Fields: `rule_id`, `kind` (fixed / relative / external_anchor), `anchor` (PDD / ADD-01-issue / PBN / NTP / PCOD), `offset`, `unit` (calendar_day / working_day / month / year), `direction`, `convention` (`day0`, `stated_date_excluded`, `unresolved`), `source_unit`.
- **Issue**
  - Fields: `issue_id`, `kind` (inconsistency / ambiguity / missing_source / untranscribed / human_decision / bidder_fact), `units`, `statement`, `options`, `owner` (a person's role), `status`, `decision`, `decided_by`.
- **Assumption**
  - Fields: `key`, `value`, `basis`, `owner`.
  - Used for: planning date, bidder, holidays, lead times, resources.
- **Activity** (derived)
  - Fields: `act_id`, `req_ids`, `ev_id`, `owner_discipline`, `issuer`, `duration` (+ assumption key), `predecessors`, `LS`/`LF`, `flags` (OK / INFEASIBLE(n WD) / REWORK / NEW / REMOVED).

### 4.4 Operation types: a small closed set

| Type | Covers (examples from the pack) | Preconditions checked |
|---|---|---|
| `replace_text` | ADD-01 §2.1 (date), ADD-02 §2.1 (pages), §4.1 (72→96 h), §8.1 (SAR 5m→2.5m) | `old` occurs **exactly once** in the target unit's normalised text (or `occurrence` is given) |
| `set_value` | ADD-02 note (2) (11.2 → 65/35), §5.1 (TN "from the value shown" → 3 mg/l, same basis) | Target is a value-bearing unit (a parameter in clause text, or a table cell from a verified transcription). The old value is resolved and recorded. |
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
- C22: the preconditions hold.
- C25: no other unit changed.

The text sha of `VOL-I:8.6` is now s2 ≠ s0. The row is **STALE** until a person re-reviews it at stage ADD-02: `parameters.local_content_min_pct: 35`, `consequence: {class: non_responsive, quote: "Failure to submit the certificate shall render the Proposal non-responsive.", unit: VOL-I:8.6}`, `reviewed.against = s2`.

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

### 4.6 Model use

- **Drafting only:**
  - requirement rows (discipline, evidence, assessment type) from unit text;
  - op proposals for provisions the patterns don't recognise;
  - first-pass image transcriptions.
- **Outputs are YAML records** with `origin: model:<call-id>` and `review.status: proposed`.
- **Logging:** every prompt and response is logged under `worklog/model_calls/` with hashes and token counts.
- **The build never calls a model.** If the network or API is unavailable in the session, the pattern drafter plus `unresolved` stubs plus manual typing still work.

### 4.7 Checks: what is checked and what happens on failure

**Failure actions:**

- **ABORT:** the build stops and prints offending items.
- **FLAG:** the build continues; the item is marked in A1/A2 and listed in A3 "could not resolve".
- **Strict mode** (`build --strict`, used for submission) turns every FLAG into ABORT, except the Issues that are *meant* to stay open for a person.

| ID | Check | Failure action |
|---|---|---|
| C01 | Source sha256 and page count match `sources/manifest.json` (curated records are pinned to these hashes) | ABORT |
| C02 | Every page is classified (content / cover / boilerplate) and has ≥1 unit unless it is a cover | ABORT |
| C03 | Every non-furniture text line belongs to exactly one unit | ABORT, listing orphan lines with page and bbox |
| C04 | Every line removed as furniture matches a declared pattern exactly (header, footer, watermark); per-page counts reported | ABORT (prevents a rule from eating content) |
| C05 | Every image region has a Transcription with `verified_by` set | FLAG ("page X region not read") |
| C06 | Every superscript is either a unit exponent (preceded by a unit token) or a footnote marker paired with a body of the same number on the same page; footnote bodies without markers are also reported | ABORT |
| C07 | Obligation-language sweep: every sentence containing obligation markers (shall, must, required, mandatory, failure to, not acceptable, will not, …) lies in a unit with a disposition (requirement / definition / informational, with reason) | FLAG |
| C08 | Consequence-language sweep, EN + AR lexicon (reject, disqualif, non-responsive, disregard, returned unopened, removed before evaluation, own risk, taken as accepted, استبعاد, غير مستجيب, …): every hit is linked to a requirement's `consequence` or explicitly dispositioned | ABORT |
| C10 | **Unsupported requirement:** each row's `verbatim` is a normalised substring of its unit's effective text at every stage where the row is active, and the cited page contains it | ABORT |
| C11 | **Stale interpretation:** `reviewed.against` ≠ current unit-text sha | FLAG (row status STALE) |
| C12 | Row IDs are unique and never disappear between builds (deleted rows keep their ID and status) | ABORT |
| C13 | A row appears in the A3 main list only if `consequence.class` is explicit and its `quote` is found verbatim in a unit | ABORT |
| C20 | **Provision coverage:** every provision of each addendum (paragraphs, table notes, appendix items, Q&A rows, form items) is referenced by ≥1 op | FLAG → addendum PARTIAL |
| C21 | Op `source_quote` is found verbatim in its provision | op invalid (FLAG) |
| C22 | Target exists and state preconditions hold (delete⇒active, reinstate⇒deleted, revoke⇒active) | op invalid (FLAG) |
| C23 | `replace_text`: `old` found exactly once in the scoped unit. Zero ⇒ "not found"; >1 ⇒ "ambiguous" | op invalid (FLAG) |
| C24 | Post-conditions: `old` count falls by 1; `new` present; re-application would fail | ABORT (bug) |
| C25 | **Scope leak:** the set of units changed by an addendum equals the set of declared targets | ABORT |
| C26 | Addenda are applied in number order with non-decreasing issue dates; ops reference only earlier or same addenda | ABORT |
| C27 | `expect` assertions hold (e.g. Table 1-1 deltas, total = 100) | op invalid (FLAG) |
| C28 | Cover-summary cross-check: summary claims vs enumerated provisions; mismatches reported in A2 | report only |
| C29 | Only `accepted` ops are applied; `proposed` and `unresolved` are listed | report; ABORT in strict |
| C30 | Every date-bearing phrase in an active unit maps to a DateRule or a disposition | FLAG |
| C31 | Printed fixed dates that equal a superseded anchor value raise an Issue (inconsistency); never auto-corrected | Issue (always surfaced in A3) |
| C32 | Every relative rule declares its counting convention; `unresolved` conventions are computed both ways, shown as a range, and scheduled on the conservative reading | FLAG |
| C40 | A3 ⊆ A1; every A5 activity cites ≥1 A1 row that is ACTIVE at the latest stage; activities citing DELETED rows are removed with a delta note | ABORT |
| C41 | No literal dates in A5 inputs except tender facts and assumptions; any activity whose latest start is before the planning date is marked INFEASIBLE(n WD) | FLAG (always surfaced) |
| C42 | Build manifest: input hashes, code commit and output hashes; outputs contain no timestamps; `verify` rebuilds in a temporary directory and compares | ABORT on mismatch |
| C43 | A3 renders to exactly one page | ABORT (forces prioritisation; no silent overflow) |

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
- **openpyxl.** Only because the owner's draft email promises A1 in Excel. It can be dropped if that promise was not sent.

**Dev dependency:** pytest.

**Excluded:** pandas, any DB, web framework, vector store, LangChain, OCR engine. Images are handled by verified transcription records, not OCR, at this scale.

**Optional extra:** the `anthropic` SDK, for the drafter only.

**Reproducibility:**

- Python 3.12 pinned.
- `uv` with a hash-locked `uv.lock` (fallback: `pip` with a `--require-hashes` lock file).
- `make verify` performs a clean rebuild and compares output hashes with the committed `out/BUILD_MANIFEST.json`.
- Outputs carry no timestamps and use sorted keys, so Linux (cloud) and macOS should produce byte-identical outputs. This is verified on the Mac, not assumed.

**Offline:** on the Mac, install while online, then run `make verify && pytest` with networking disabled, before submission and again before the session.

**Log separation:**

- `worklog/` is timestamped, append-only and human-written: prompts, model calls, errors.
- `out/` is deterministic generated deliverables.
- `build/` holds intermediates, regenerated rather than edited. Whether it is committed is decided in Stage 1; the proposal is to commit `build/units.json` only, because it is the audit trail for segmentation.

---

## 5. Verification strategy (designed to disprove the design)

**Independence rules:**

- **Golden facts are written from the rendered pages** into `tests/golden/*.yaml`, with page citations, **before** the corresponding code. They never import curated data.
- **Who writes them:** I write the first set, and the owner independently writes at least 10 rows blind.
- **Disagreements** between the owner's set and mine are logged in the work log as findings.
- **Mutation tests** change *inputs* (synthetic PDFs built with PyMuPDF, or edited op files), not the code under test.

| Risk | Test(s) | Independent oracle | Deliberate input change |
|---|---|---|---|
| Missed footnote | `fn12` unit exists with marker pairing. The row has consequence `rejection` and parameters (2 plants, ≥80,000 m³/day, COD within 10 y of PDD). The C08 sweep maps "rejected without further evaluation" on p4. | Golden YAML from p4 render | Synthetic page with an extra footnote 13 and no matching marker ⇒ C06 ABORT. Footnote text removed ⇒ C03/C08 fail. Footnote moved to the next page ⇒ pairing error reported, not silently orphaned. |
| Unit superscript mistaken for footnote (and vice versa) | All 11 m³ exponents classified as unit exponents (the pack has 12 superscript spans: 11 × "3" after "m" and 1 × "12" after "Form 4-B."; in Table 2-6 the "m" is a separate span, so look-behind must cross spans); "Form 4-B.¹²" yields marker 12 and never a form ID "4-B.12" | Font-level evidence table (§2.1 O1) | Synthetic "Clause 3.1²" with no body ⇒ ABORT. Synthetic "50 m²" ⇒ unit. |
| Missed image region | With transcription records present, the Form 4-C decl. 4 row exists with consequence `exclusion` and the Table 2-4 TN unit exists | Owner's (or a second reader's) verified Arabic reading | Delete the Form 4-C transcription ⇒ C05 FLAG, A3 lists "VOL-IV p6 not read". The decl. 4 row must **disappear with an explicit gap**, never be replaced by "no consequence". Delete the Table 2-4 transcription ⇒ ADD-02/5.1 becomes `unresolved` ("target only in unread image"). |
| Wrong occurrence of repeated text | After ADD-02: VOL-II §4.4 = 96 h **and** VOL-V §31.3 still 72 h; VOL-I §11.2 = 65/35 **and** VOL-V §29.2 still 60/40; Table 2-4 TN = 3 **and** Table 2-2 TN = 55/80; §12.2 still 120 days | Golden values from the pages | Synthetic op targeting VOL-V §31.3 with ADD-02's quote ⇒ provenance mismatch (C21/C25). Synthetic unit containing "seventy-two (72) hours" twice ⇒ C23 "ambiguous". A deliberately buggy global replace in a test double ⇒ C25 ABORT. |
| Deadline change moves dependent dates, preserves fixed ones | Table §2.5 values at BASE and ADD-01 stages; fixed dates unchanged; printed Form 4-A dates raise Issues, not edits | Hand calculation (§2.5), cross-checked against a printed calendar | Synthetic ADD-03 moving the PDD to Thu 3 Dec 2026 ⇒ all relative rules move, fixed don't. Add a holiday on 9 Nov to config ⇒ cut-off moves back one WD. Change convention day0→day1 ⇒ ranges displayed and flagged. |
| Deletion and reinstatement | LCC lifecycle per §4.5 across three stages (A1 statuses, A3 membership only at ADD-02, A5 removal then rework); ADD-01 §4.2 revoked | Golden lifecycle YAML | Swap addendum order ⇒ C26 ABORT. Reinstate a never-deleted unit ⇒ C22. Delete twice ⇒ C22. Drop ADD-02/9.2 ⇒ C20 PARTIAL. |
| Unresolved or unfamiliar wording | Drafter emits `unresolved` for unseen phrasings; build (working mode) applies nothing for them and marks candidate rows AMENDMENT-PENDING; strict build fails | Synthetic provisions written to defeat the patterns | e.g. "Clause 7.1 shall be read as though 'one hundred and fifty' were 'one hundred and eighty'"; "The bid security period is extended by thirty days" (no clause cited). A model-proposed op whose `old` text does not exist ⇒ C23. |
| Traceability | For every A1 row: unit → page → bbox re-extraction contains `verbatim`; amended rows' chains resolve to addendum provisions whose `source_quote` re-extracts from their pages. Timed drill: 3 random rows in under 60 s total. | The PDFs themselves | Inject a row with no unit ⇒ C10 ABORT. Inject a row whose verbatim was "improved" by a model ⇒ C10 ABORT. |
| Reproducible rebuild | `verify`: two clean builds produce identical output hashes; Linux vs macOS manifests compare equal; network disabled | Hash comparison | Flip one byte in a source PDF ⇒ C01 ABORT. Edit a curated file without re-review ⇒ C11 STALE. |
| Live adaptability | **Rehearsals:** (1) treat ADD-02 as unseen early, drafting ops through `draft` rather than by hand; (2) synthetic ADD-03-A written to hit known weak spots; (3) a blind synthetic ADD-03-B written by someone else or a separate model session without sight of this design. Each is timed against the 30-minute budget, with defects logged. | Separately authored addenda | Includes: an image page, a small-print note, a deletion of a reinstated clause, a new form, a clarification answer that changes substance, an incomplete cover summary. |

---

## 6. Staged implementation plan (times in Riyadh time)

Each stage ends with a commit and a work-log entry. **Inspect** means what the owner should look at before the next stage starts.

| Stage | Output | Depends on | Main risk | Acceptance evidence | Owner inspects |
|---|---|---|---|---|---|
| **1. Evidence and units** (Fri 2 Oct AM) | `ingest`, `segment`; `build/units.json`; page/line/image coverage report; transcription records for Table 2-4 and Form 4-C | Plan approval; Python env | Segmentation of tables, forms and footnotes; watermark removal eating content | C01–C06 pass; golden unit tests (fn 12, m³ ×11, TN row, Form 4-C decl. 4, both "72 hours" units, Form 4-A pdd fields) | Coverage report; 10 random units against pages; **Arabic transcription verified by a competent reader** |
| **2. Thin end-to-end slice through the hard amendments** (Fri 2 Oct PM) | `amend`, `dates`, minimal `register`, `checks`; ~12 rows (LCC, PDD and dependants, fn 12, 72 h, weighting, TN, Form 4-G, Form 4-C); first A1/A2/A3/A5 renders. **ADD-02 drafted through `draft` as if unseen.** | Stage 1 | The op model is the wrong shape; better found now than on Sunday | Golden tests: LCC lifecycle, scope traps, date table, Form 4-A Issue; C20 reports exactly the not-yet-mapped provisions | LCC chain in A2; dates table; A3 draft layout |
| **3. Full register and Issues** (Sat 3 Oct) | All units dispositioned; all ADD-01/02 provisions mapped; ~80–120 rows (model-drafted, reviewed in tiers); `issues.yaml` with human-decision items assigned to roles | Stage 2 | Review time; over- or under-splitting rows | `build --strict` passes except deliberate open Issues; C07/C08 sweeps clean; A3 fits one page | A3 candidates (all); Issues list; 15 random rows; the owner's 10 blind golden rows compared |
| **4. A5 programme and marshalling** (Sat 3 Oct PM – Sun 4 Oct AM) | `schedule`; activity templates; `assumptions.yaml` (with basis and owner); per-stage A5 with replan deltas; optional Gantt rendered from the same data | Stage 3 | Lead-time assumptions dominate the result; infeasibility must be shown, not hidden | Tests: backward pass, the clarification "must finish by" constraint, INFEASIBLE detection, LCC rework, bond re-issue rework, deleted-row activity removal | **The assumption values (owner's call)**; the infeasibility list |
| **5. Unseen-addendum readiness** (Sun 4 Oct) | `show`, `diff`; drafter hardening; synthetic ADD-03-A and a blind ADD-03-B; two timed rehearsals; one rehearsed "live fix" (add a check and its test) | Stages 2–4 | Live time overrun; brittle patterns | Each rehearsal completes within 30 minutes with all provisions accounted for; defects fixed and logged | Rehearsal timings and work-log error notes |
| **6. Packaging and Mac verification** (Mon 5 Oct, by 14:00) | Strict build; A3 PDF; A1 CSV/JSON (+XLSX); A2 MD+CSV/JSON; A5 CSV/JSON; one-page operating procedure; final work log; archive | Stage 5 | Environment drift on the Mac; time | `make verify` on the Mac with networking off; manifests equal to cloud build | Final A3 read cold; archive contents |

**If behind schedule, cut in this order:** XLSX → Gantt → model drafter (keep patterns plus `unresolved`) → second rehearsal. Never cut: C10/C13/C25 checks, A3 unresolved list, Stage 5 rehearsal 1.

---

## 7. Decisions needed from the owner

| # | Decision | Options | Recommendation and trade-off |
|---|---|---|---|
| D1 | **Planning basis for A5:** status date and bidder | (a) Status date = latest addendum issue date (22 Oct 2026; becomes the ADD-03 date live), unnamed bidder with a configurable member count (default 3). (b) A named Appendix 1 consortium. (c) Real-world date. | **(a)**, as in the owner's 1 Oct email. Keep member count and names in config. Note that 4 of 5 prequalified consortia have 3 members and Northwind has 2. Real-world 1 Oct 2026 precedes both addenda, so (c) makes the programme meaningless. |
| D2 | **A3 inclusion rule** | (a) Explicit document wording only (rejection / disqualification / non-responsive / exclusion, including the footnote and the Arabic image), plus a separate line for §11.3 score elimination. (b) Also include mandatory Section 8 / bond items with no stated consequence. | **(a)**, with a short labelled block "Mandatory under §11.1(i) but no stated consequence; human to judge". This matches the brief's test ("the documents themselves say") and avoids asserting consequences the pack does not state, while still surfacing them. |
| D3 | **A1 scope and granularity** | (a) One row per independently evidenced obligation (e.g. bond: amount; form/terms; issuer rating), including VOL-II technical and VOL-V contractual obligations, tagged by assessment type. (b) One row per clause. (c) Bid-stage only. | **(a)**. It gives atomic evidence links for A5 and precise A3 rows, and covers the "one row per requirement" key. Costs more rows (~100) and more review. Sub-row IDs keep clause grouping visible. |
| D4 | **Conservative-reading policy for unresolved counting conventions** (day 0, inclusive look-back, forward WD, holidays) | (a) Block until a person decides. (b) Compute every reading, schedule on the most conservative, and flag. (c) Pick one silently. | **(b)**. It never hides the ambiguity, and the programme stays usable. The person can override per rule. |
| D5 | **Build strictness** | (a) Always strict. (b) Working mode emits with FLAGs and labelled PARTIAL addenda; `--strict` for submission. | **(b)**. In the live session the panel needs to see what broke, not a stack trace. PARTIAL is labelled at the top of A3, so nothing is silently partial. |
| D6 | **Model use in the live session** | (a) Hosted model drafter allowed, with offline fallback. (b) Patterns and manual only. | **(a)**, with every call logged and the fallback rehearsed with networking off. |

**Kept visibly with people:**

- These are surfaced as Issues, not as decisions the system makes.
- **The issues:** Form 4-A date and missing fields (O4); Envelope B contents (F4); Form 4-B contract value (F5); concession term (F6); design flows (F7); Permit vs Table 2-4 (F8); Form 4-G "No" answers (F10); what to raise as clarifications before 12 Nov 2026; Arabic verification (O5).
- **Bidder facts:** all bidder facts.

---

## 8. Recommended first implementation step (after approval)

**Stage 1, with a 2-hour time box.** Implement `ingest` and `segment` for the six PDFs, producing `build/units.json` and the coverage report. The first tests are the golden unit tests for:

- the footnote 12 pairing;
- the eleven m³ unit exponents;
- the two "seventy-two (72) hours" units;
- the two Form 4-A printed-PDD fields;
- the image-region detection on VOL-II p3 and VOL-IV p6.

These are the inputs every later decision rests on, and they are the cheapest place to discover that the extraction strategy is wrong.

In parallel, the owner verifies the Arabic transcription of Form 4-C and the Table 2-4 transcription in §2.1, and answers D1–D6.


---

## 9. Stage 1 checkpoint (implemented in session 02; for the owner's review)

**Built:**

- **Package and commands.** `tenderpack/` (extract, regions, segment, readings, arabic, packets, coverage, cli). Commands: `ingest`, `show`, `approve`.
- **Environment.** `pyproject.toml` with `uv.lock`; a `Makefile` with targets `setup`, `evidence`, `test`, `verify`.
- **Dependencies.**
  - Runtime: PyMuPDF 1.28.2, numpy, pydantic, PyYAML.
  - Dev: pytest.
  - openpyxl is deferred to the stage that writes A1.

**Evidence to review** (regenerate with `make evidence`):

| File | Contents |
|---|---|
| `build/units.md` / `build/units.json` | All 525 units of the real pack, including units derived from the two readings, marked PENDING |
| `build/coverage.md` | Checks C01–C06, page accounting, regions, superscripts, footnotes, split tables, small print |
| `build/exclusions.md` | The 160 excluded spans (5 rules × 32 pages), with rule, text, angle, colour and size |
| `build/review/VOL-II-p3-r1/` | Table 2-4 packet: native row and cell crops, side-by-side, checks, uncertainties |
| `build/review/VOL-IV-p6-r1/` | Form 4-C packet: band crops, side-by-side (Arabic rendered by the program), numeral evidence |
| `build/fixture/` | The same reports for the synthetic mixed example (`tests/fixtures/make_fixture.py`) |

**Tests:**

- 39 tests: `make test`.
- Mutation checks were run by hand and are recorded in the session 02 work log.

**Not done in Stage 1 (by design):** amendment operations, dates, register, A1–A5, model routes. **Next, after the owner's review:** Stage 2 (thin end-to-end slice through the hard amendments), which must now include the §R2-A citation resolver and the §R2-C dependency pins and two-state build.

**Decisions still open:**

- **D3:** A1 granularity and scope; recommendation unchanged.
- **D4:** conservative reading of counting conventions; recommendation unchanged.
- **Arabic and Table 2-4 sign-off:** with the owner.
