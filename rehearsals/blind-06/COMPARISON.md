# Blind rehearsal 06: the workflow's candidate against the sealed answer key (ADD-03)

**Synthetic, not tender content.** I scored this after the freeze, using only the frozen copies in this folder. Nothing under `out-candidate/`, `review/`, `proposals/`, `candidate-curation/`, `downstream/` or `batches/` was changed, and nothing was re-run. Scorer: a separate agent session (Opus 5.5, `claude-opus-5-5`, by its own instructions). It read the key only after the freeze.

Paths are relative to `rehearsals/blind-06/`. Short names in the evidence column:

| Short name | File |
|---|---|
| `ops` | `candidate-curation/amendments/ADD-03.yaml` |
| `P` | `proposals/ADD-03-run-host-blind06-20261005T173226Z-combined/proposals.yaml` (83 analysis items, 75 statements) |
| `DS` | `downstream/proposals.yaml` (64 downstream items, 42 statements, 48 tasks) |
| `pkt` | `review/index.md` |
| `iss` | `candidate-curation/register/issues/ADD-03-ai.yaml` |
| `new` | `candidate-curation/register/rows/ADD-03-ai.yaml` |
| `CQ` | `candidate-curation/clarifications/register.yaml` |
| `rd` | `candidate-curation/readings/ADD-03-p4-r1.yaml` |
| `a1` | `out-candidate/a1/a1.csv` |
| `a2` | `out-candidate/a2/a2.md` |
| `a3c` | `out-candidate/a3/a3_candidate.md` |
| `a5c/` | `out-candidate/a5/candidate/` |
| `ckpt` | `checkpoint.json` |

L means line.

## What was frozen and when

### The addendum

An independent author wrote Addendum No. 3 from the pack's PDFs, the brief and the correspondence, without reading the tool (`SEALED/author_notes.md` L18–49). It is 5 pages and "Issued 10 November 2026", a Tuesday. That is two Working Days *before* the VOL-I 5.2 clarification cut-off of Thu 12 Nov, so bidders could still ask questions about it. Its subjects:

- VOL-II 1.3 is extended. An image-only Arabic Table 1-3 from the Network Operator (letter 312/2026) is incorporated by reference. Its English convenience translation differs from the Arabic on TP-2's maximum shutdown: 4 h in the Arabic, 6 h in the English. The English also omits the Eid holidays.
- Free-standing provisions 2.3–2.7:
  - an election of method per tie-in point;
  - a "maximum transfer flow" that the table does not state;
  - a Network Operator Shutdown Acceptance Letter, applied for 8 Working Days before the PDD;
  - a deemed method (a) where the letter is missing;
  - rejection of a Proposal that interrupts flow for too long.
- VOL-II 7.2 gets an 85–110 % band, and 3.2 adds a counting rule. Together they create DA1, which has no correct answer.
- VOL-II 8.1–8.3 are replaced by 8.1 and 8.3 only, so 8.2 is silently deleted.
- VOL-V 31.1 gains a new limb (d), and 31.3 is changed to match.
- Six answers. Answer 19 cites the deleted 8.2, which is the internal inconsistency II1.
- Three new cover-error mechanisms.

The author also wrote an Addendum No. 4. It is not scored here (last section).

### Timeline and checks

- **Before the run.** `FROZEN.md`, 2026-10-05 09:53:37 UTC, records the sha256 of both PDFs and of the sealed `SHA256SUMS` (`b57023ad…84b68a3`, L23).
- **The run.** `tenderpack ai run ADD-03 --route host`, alias opus, `max_parallel_sessions=2`, from 17:32:26 to 18:28:15 UTC (`clock.txt` L1–2; `run.log`). Nobody curated.
  - 15 headless host sessions ran: one image reading, ten analysis batches and four downstream batches. They had only the MCP tools.
  - A second model, the critic (claude-sonnet-5-5, `pkt` L194), answered 13 requests and changed no status.
- **The freeze.** `FROZEN-OUTPUTS.sha256` (367 files) was written at 18:29:34.3 UTC. `FROZEN-OUTPUTS.md` says "Recorded 2026-10-05 18:30:42 UTC" (L3), but its file time is 18:31:22.9.
  - **Correction note.** The note's own last paragraph (L20) is labelled: two sentences were corrected at 18:31:22, after the key was copied and before any scoring. One concerned the status distribution, which had been read from the step field. The other was the intervention count, which had not said that the entries are the automatic sessions.
  - **Record slip.** The note also records one (L17): the launch script wrote the exit line and the end time to wrongly named files. They were appended to `run.log` and `clock.txt`, whose file times are 18:29:57.
- **The key.** The `SEALED/` folder's time is 18:30:44.6 UTC. That is after `FROZEN-OUTPUTS.sha256` (18:29:34.3) and after the note's recorded time (18:30:42). The three sealed files keep their authoring times (09:44:36–09:53:13) because they were copied with their times kept. I checked this with `ls -la --time-style=full-iso`.
- **Hash checks run for this scoring:**
  - `sha256sum -c --ignore-missing SHA256SUMS` inside `SEALED/`: `author_notes.md`, `build_addendum.py` and `expected_findings.yaml` all OK.
  - From the repository root, `sha256sum -c --ignore-missing rehearsals/blind-06/SEALED/SHA256SUMS`: both PDFs OK.
  - `sha256sum SEALED/SHA256SUMS` = `b57023adcfb0d984e339005d9cf0dbab2a5e26dff293f23efc0d6ba9b84b68a3`, the value in `FROZEN.md` L23.
  - `sha256sum -c FROZEN-OUTPUTS.sha256`, run from this folder: **367 of 367 OK (exit 0).**
- **Files that are not hashed.** `run.log`, `clock.txt`, `run.id` and the two `FROZEN*` notes are not in the hash list (`FROZEN-OUTPUTS.md` L17 says so for the first two). Hashed files corroborate them:
  - `ckpt` `steps` carries the same per-step seconds as `run.log` L53–65.
  - `ckpt`'s file time (18:28:15.27, kept by the copy) and the last `log.jsonl` event ("review …", 18:28:11) match the end in `clock.txt`.
  - `run.id`'s file time (17:32:26.7) matches the start.
  - `ckpt`, `log.jsonl` and `promotion.json` are byte-identical to the copies in the staging run folder.
- **Nothing is decided.** Every op, disposition, reading, row, issue, activity and clarification is PROPOSED. Human approval: none (`pkt` L15).

## The key

`SEALED/expected_findings.yaml` holds:

- 13 keyed provisions: 2.1–2.7, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2. Recitals 1.1–1.2 are not keyed.
- 6 answers (15–20).
- 3 planted cover errors (E1 phantom provision, E2 wrong temporal anchor, E3 actor substitution).
- 31 Arabic strings, with 2 discrepancies (AR1, AR2).
- 10 secondary undisclosed effects (U1–U10).
- 8 indirect effects (IE1–IE8).
- 3 missing-evidence items (ME1–ME3).
- One deliberate ambiguity with no correct answer (DA1), one internal inconsistency (II1) and two human-judgment items (HJ1, HJ2).
- 8 derived dates and 3 figures.
- 5 marshalling effects.
- An A3 delta: 1 item added, 4 not-added traps and 5 unresolved items.
- 23 "must not report" traps for ADD-03.
- An `addendum_4` section, not scored.

The author's intended reasoning (`author_notes.md` L164–189):

- 8.2 is deleted by the range, and answer 19's reference to it is a clash to flag and escalate.
- Match 31.1's old words across the line break; the cover's Ramp-Up claim is false.
- Take the tie-in values from the image (TP-2 is 4 h).
- A missing letter is not a disqualifier. 2.7 is the only new A3 item, and it applies only when there is an interruption.
- The letter must be applied for by Mon 16 Nov, and its issuer is the Network Operator.
- Never borrow a transfer flow from Table 2-6.
- DA1 has no correct answer.

## Scoring method

- **N = 35**: the 13 provisions, 6 answers, 3 cover errors, 3 Arabic items (the reading, AR1, AR2) and 10 secondary effects. This is blind-05's method, adapted to this key: blind-05 had 15 provisions and 7 answers. Indirect effects, missing evidence, the ambiguity, inconsistency and judgment items, dates, marshalling, the A3 delta and the traps are scored in their own tables. They are not added to N.
- **Hit**: the frozen outputs state the effect correctly (target, words, values, consequence).
- **Partial**: the effect is detected but incomplete, wrongly targeted, or left unresolved or escalated where the key expects a definite change. Each row says which.
- **Missed**: absent, or present only in a form that contradicts the key.
- Where the right statement exists only in an unpromoted analysis statement or escalation, the row says so. Such a statement counts as detection, not as an applied change (section 2).

## 1. Detection

**Count: 35 expected findings: 20 hits, 14 partial, 1 missed.**

| Group | Hit | Partial | Missed |
|---|---|---|---|
| Provisions (13) | 6 | 7 | 0 |
| Answers (6) | 4 | 2 | 0 |
| Cover errors (3) | 3 | 0 | 0 |
| Arabic (3) | 3 | 0 | 0 |
| Secondary effects (10) | 4 | 5 | 1 |

Scored separately:

| Group | Result |
|---|---|
| Indirect effects (8) | 1 hit, 5 partial, 2 missed |
| Missing evidence (3) | 2 hit, 0 partial, 1 missed |
| DA1 / II1 / HJ1 / HJ2 | partial / hit / hit / hit |
| Dates (8) | 5 right, 1 partial, 2 missed |
| Marshalling (5) | 4 hit, 1 partial |
| A3 delta | the added item partial; 4 of 4 not-added traps avoided; 4 of 5 unresolved items shown |
| Traps | 23 of 23 avoided (two borderline) |
| Wrong statements | 3 false positives and 5 false signals (tables below) |

### Provisions (13): 6 hit, 7 partial, 0 missed

| Key | Expected | Result | Evidence in the frozen outputs |
|---|---|---|---|
| 2.1 | VOL-II 1.3 + the sentence; Table 1-3 incorporated; rows for the TP-1/TP-2 conditions (window, maximum duration, notice, one shutdown, Ramadan/Eid) | **partial** | The `append_text` is verbatim and evidence_verified (`ops` L26–42; `pkt` L232–240). The conditions reach no row. The six conditional rows proposed from the pending reading (TP-1, TP-2, the Ramadan/Eid ban, one shutdown per point, portal requests, Riyadh time) and the matching issue are all invalid: "provision: ADD-03:p4-image is not a provision of ADD-03" (`pkt` L926–932; `DS` L4503–5134). VOL-II-1.3-01 is not re-made, because no reading is approved (`pkt` L875); it is UNRESOLVED in A1 (`a1` L137) |
| 2.2 | the Arabic governs; take values from the image; report AR1 and AR2 and resolve them for the Arabic | **partial** (conflicting) | The analysis applies the rule: "the governing maximum shutdown duration for TP-2, which ADD-03:2.7 uses as the threshold for rejection, is 4 hours (Arabic), not the 6 hours in the English convenience translation" (`P` L209–215; again L949). The 2.2 annotate is held `conflicting` (`pkt` L242–245; `ops` L516). Downstream then hands the rule back to a person: "Which rendering governs, and which figure applies, is a person's decision" (`DS` L4269 D-05, L4389 D-07). The promoted issue ends "Legal decides what follows" (`iss` L21–27) |
| 2.3 | a Technical Proposal content requirement (construction methodology), conditional, no stated consequence | **hit** | New row ADD-03-2.3-01: TP-1/TP-2, `consequence: none_stated`, citing ADD-03 2.3 itself (`new` L51–97; `a1` L41). The technical-proposal activity names the election (`DS` L2843; `a5c/README.md` L35). The analysis item stays unresolved only because it asked for this row (`ops` L523). Noise: "Whether 6.2 covers this election is a human decision" (`new` L79–81) |
| 2.4 | register the requirement with the value UNKNOWN (ME1) | **partial** | The gap was read from both renderings: the Arabic heading row "has no column for a maximum transfer flow" (`P` L713; `pkt` L109–111). Promoted issue I-ADD03-TRANSFER-FLOW (`iss` L35–44) and draft CQ-ADD03-TRANSFER-FLOW, "No figure is assumed" (`CQ` L1066–1094). There is no register row for the requirement: "A row would have no parameter to carry" (`DS` L3262) |
| 2.5 | conditional Envelope A letter from the Network Operator; apply by Mon 16 Nov; response within 5 WD (Mon 23 Nov); marshalling M1 | **partial** (escalated) | Detected in full: Network Operator, Envelope A, the condition and 2026-11-16 computed (`pkt` L113–115, L171; `DS` L501). Not applied: <ul><li>The escalation also waits for "Confirmation that the operative 2.5 … prevails over the cover summary" (`pkt` L295).</li><li>The proposed row is invalid: "kind 'deadline' not in ('anchor', 'relative', …)" (`pkt` L934).</li><li>The activity is invalid: "computed_from matches no deadline the program computed" (`pkt` L936).</li><li>The evidence item is held back (`pkt` L935).</li><li>A5 has only an undated decision milestone (`a5c/milestones.csv` L16).</li></ul>Mon 23 Nov is not computed |
| 2.6 | missing letter → deemed method (a), not non-responsive; 2.4 then binds with a missing value | **partial** (escalated) | Read right: "method (b) without a Shutdown Acceptance Letter in Envelope A is deemed an election of method (a)" (`pkt` L117). It "ties back to 2.4, whose design flow is not stated" (`DS` L3576). Escalated for want of a target unit. The downstream item leaves open "Whether it displaces any Envelope A non-responsiveness rule (VOL-I-6.2-02, ADD-02-7.2-01)", which 2.6's own words settle |
| 2.7 | A3 rejection: interruption longer than 6 h at TP-1 or 4 h at TP-2 (the Arabic governs) | **partial** (conflicting) | The threshold is stated right in the analysis (`P` L209–215) and in the unpromoted 2.7-issue (`pkt` L320). The op is held `conflicting` (`pkt` L311–314). A3 gains no row (`pkt` L1458–1460; `a3c` L11–13). It appears on A3 only through the open issue I-ADD03-T13-ARABIC-ENGLISH, without the values (`a3c` L151). The downstream escalation misreads it (false positive 1) |
| 3.1 | VOL-II 7.2: daily average flow at the inlet works of 85–110 % of nominal capacity (102,000–132,000 m3/day) | **hit** | `ops` L43–59, verbatim and evidence_verified (`pkt` L334–337); A1 shows "AMENDED (ADD-03/3.1)" (`a1` L224). The row reading failed its check, so the row is STALE (section 2). The band in m3/day is not computed anywhere |
| 3.2 | register the counting rule as an ADD-03 requirement; 7.3 unchanged; DA1 escalated, not resolved | **partial** | 3.2(b), "7.3 is unchanged", was promoted as `confirms` (`ops` L60–74). 3.2(a) was escalated with both readings: "an out-of-range day might pause the run or might break its continuity" (`P` L257–263; `pkt` L121–124). That is right for DA1, but the counting rule is not registered. Because 3.2(b) was promoted, the provision counts as answered (`pkt` L350; `a2` L525), so DA1 is missing from the candidate A3's unresolved list (`a3c` L65–88) |
| 4.1 | 8.1 replaced (18 months; recorded in the 7.4 asset register); **8.2 deleted**; 8.3 replaced (degree, 10 years; plant manager named, CV appendix) | **hit** | `ops` L75–129: two verbatim `replace_text` ops and `set_status` VOL-II:8.2 `deleted`. "Clause 8.2 (the CMMS requirement) is deleted outright, and the 8.2 number stays vacant" (`P` L304). A1 shows "DELETED (ADD-03/4.1(b))" (`a1` L227). Blind-05's follow-up 1 (clause lists and ranges) holds |
| 4.2 | not renumbered; 8.4 and 8.5 unchanged | **hit** | `ops` L130–146 (`confirms`); CONFIRMED (unchanged) for the four 8.4/8.5 rows (`pkt` L1416–1419) |
| 5.1 | 31.1(b)–(c) replaced across the line break; (d) added; letters (a)–(c) kept | **hit** | `ops` L147–166, verbatim; A1 shows "AMENDED (ADD-03/5.1)" (`a1` L422–424) |
| 5.2 | 31.3: only the second sentence replaced | **hit** | `ops` L167–182; the (a) and (c) cure periods are re-read as unchanged (`DS` L1911, L1973) |

### Clarification answers (6): 4 hit, 2 partial

| Key | Expected | Result | Evidence |
|---|---|---|---|
| Q15 | decoy: no effect | **hit** | `ops` L232–239 `no_effect` |
| Q16 | confirms 3.3; no new requirement | **hit** | `ops` L183–198 `annotate confirms`. A5 shows "CONFIRMED (unchanged)", not REWORK (`a5c/README.md` L37–39); blind-05 false signal 2 is fixed here. A false signal remains: the semantic check says "annotated 'confirms', but the answer adds" and marks HUMAN DECISION PENDING (`pkt` L443) |
| Q17 | VOL-V 12.3 carve-out: IE costs of any run after the first fall on the Project Company; linked to DA1 | **partial** | The meaning is stated exactly (`P` L425–431). The annotate is held `insufficient_evidence` because the addendum "prints no replacement or added text" (`pkt` L447–450; `ops` L561). The escalation calls it "a person's decision" whether the answer amends the contract (`DS` L3677), although the answer says "is amended accordingly". VOL-V-12.3-01 still reads "borne equally" and is UNRESOLVED (`a1` L403). The DA1 link exists only in the unpromoted DS-11 (`DS` L2778–2781) |
| Q18 | human judgment: escalate; no yes or no; 34.1 gives time only | **hit** | "Whether that shortfall is a Relief Event (for example, 'failure of a utility') is a legal question" (`DS` L3741). "Clause 34.1 gives an extension of time but no compensation" (`P` L432). Unresolved (`ops` L569). The Form 4-E choice is not mentioned |
| Q19 | 7.4 changed for the asset register only (before the reliability run); the format goes to the Preferred Bidder; II1 flagged and escalated | **partial** | The meaning is exact: "This brings the 7.4 deadline (sixty days after PCOD) forward for the asset register only. The documentation and manuals keep the 7.4 deadline" (`P` L498–504). II1 is flagged and escalated (`DS` L3806). The 8.2 escalation says "decide whether a CMMS is still expected anywhere else in the pack" (`DS` L1208). But the 7.4 change itself is held `conflicting` with 7.4 (`ops` L577; `pkt` L470–473), so VOL-II-7.4-01 still says 60 days after PCOD (`a1` L225) |
| Q20 | points to a value Table 1-3 does not contain; report it missing and never substitute a figure | **hit** | `pkt` L125–127; `CQ` L1066–1094; no number anywhere (`7,500`/`1,800` absent from `P` and `DS`) |

### The cover's planted errors (3): 3 hit

| Key | Mechanism | Result | Evidence |
|---|---|---|---|
| E1 | phantom "no deduction during the Ramp-Up Period" | **hit** | Promoted issue: "no operative provision says so, and VOL-V 29.3 covers only rolling-average Table 2-4 parameters … price 31.1(d) deductions as applying in the Ramp-Up Period" (`iss` L8–11). Part (b) of the draft clarification (`CQ` L1053–1058). C28: "not found" (`pkt` L1380). Caveat: "Which text governs is a decision for Legal" (`iss` L10) |
| E2 | "within eight (8) Working Days of the date of this Addendum" against 8 WD before the PDD | **hit** | "the summary says within 8 Working Days of the date of the Addendum; 2.5 says not later than 8 Working Days before the Proposal Due Date" (`iss` L6–8; `P` L40). The cover's own date (Sun 22 Nov) is not computed (D4) |
| E3 | the Authority's acceptance against a Network Operator letter | **hit** | "the summary says the Authority's acceptance of the shutdown programme; ADD-03 2.5 requires a Network Operator Shutdown Acceptance Letter" (`iss` L4–6). I-ADD-03-COVER-01: the cover "is never an operative provision" (`iss` L45–62) |

### The Arabic image (3): 3 hit

| Key | Expected | Result | Evidence |
|---|---|---|---|
| Reading | every Arabic string verbatim, translations kept apart, pending | **hit** | `rd`: 35 blocks. 30 of the key's 31 strings match verbatim (checked by script). The lead-in differs by one vowel mark (تُحدِّد read for تُحدَّد, `rd` L103), the same slip as in blind-05. The grid-detector mismatch and the diacritics are named as uncertainties (`pkt` L99–103). Status pending, never approved |
| AR1 | TP-2: ٤ (4 h) in the Arabic, 6 h in the English; the Arabic governs | **hit** | "The governing Arabic Table 1-3 prints '٤' (4 hours) … the convenience English translation … prints … 6"; "A person must record that the Arabic value (4 h) governs for TP-2" (`pkt` L129–130; `P` L110, L209). The promoted issue does not state the value ("a different TP-2 maximum shutdown duration", `iss` L22–24) |
| AR2 | Arabic note 1 also bars the Eid al-Fitr and Eid al-Adha holidays | **hit** | `pkt` L133–135; `P` L137. In the promoted issue it appears only as "more wording than the English note (1)" (`iss` L24–25) |

### Secondary, undisclosed effects (10): 4 hit, 5 partial, 1 missed

| Key | Expected | Result | Evidence |
|---|---|---|---|
| U1 | 8.2 (CMMS) deleted by the range | **hit** | `ops` L94–108; `a1` L227 |
| U2 | lower bound relaxed from 90 % to 85 %; upper bound of 110 % added | **hit** | `ops` L43–59; "The old single minimum of 90% is replaced" (`DS` L55) |
| U3 | spares cut from 2 years to 18 months; inventory recorded in the 7.4 register | **hit** | `ops` L75–93; `DS` L88 |
| U4 | plant manager named in the Technical Proposal with a CV appendix; degree and 10 years | **hit** | `ops` L109–129. The technical-proposal activity lists "named plant manager with CV appendix" (`DS` L2843; promoted, `pkt` L950) |
| U5 | 12.3 carve-out | **partial** | as Q17 |
| U6 | asset register due before the run | **partial** | as Q19 |
| U7 | the Unavailability Event definition (VOL-V 1.6) widened | **partial** | The widened event reaches the payment rows through curated 31.1 links (VOL-I-10.2/10.3, F4E, F4F, `calc:availability-payment`; `pkt` L1439–1451). The definition at 1.6 is named nowhere in the run's items |
| U8 | ADD-01 response 6 ("does not depend on volume delivered") becomes wrong | **missed** | Not among the earlier answers to re-read (`pkt` L160–164); `out-candidate/a2/a2_answers_to_review.csv` L7–9 lists only Q18–Q20 |
| U9 | a new conditional rejection ground (2.7) governed by the Arabic | **partial** | as 2.7 |
| U10 | the free-standing 2.3–2.7 and 3.2 are registered citing ADD-03 itself | **partial** | Only 2.3 has a row (`new` L51–97). 2.4, 2.5, 2.6 and 3.2(a) are escalated for want of a cited target (`pkt` L109–124: "fails C22 ('not cited: [VOL-II:7.2]')"). The 2.5 row was rejected (`pkt` L934). 2.7 is held |

### False positives (stated effects the key does not contain)

**Three, none of them promoted into an op or a row. The third reaches the candidate A3.**

| # | What is stated | Where | Why it is wrong |
|---|---|---|---|
| 1 | "For TP-2 the permitted window (01:00 to 05:00, 4 hours) is shorter than the stated maximum duration (6 hours). Which limit binds is a question for a person." | ADD-03-DS-ESC-2.7 (`DS` L3627; statement L532–536), status conflicting, not promoted | It takes the English 6 h as Table 1-3's value and invents a window-against-duration conflict. The governing Arabic says 4 h. The critic disagreed (`pkt` L326–332) |
| 2 | The 8.1 re-read calls the asset register "a post-PCOD deliverable" | `DS` L1156 (insufficient_evidence, not promoted) | Q19 moves it to before the reliability run (U6, IE5) |
| 3 | C28 reports "contradicted" for two cover statements that are accurate: the 7.2 flow range and the new 31.1 event | `pkt` L1379, L1381; copied to the candidate A3 "Conflicts" (`a3c` L140–141) | The key lists both as accurate parts (`accurate_parts_not_errors`). C28 calls a cover claim "contradicted" whenever the operative provision amends the claimed target |

**False signals.** These are not claims about the tender, but each one costs a reviewer time:

| # | Signal | Evidence |
|---|---|---|
| 4 | A `confirms` annotation is reported as a change. The reason text reads like trap 10 although the op is right | "VOL-II:7.3 changed since BASE (by ADD-03/3.2(b))" (`pkt` L1424; `a2` L406); 3.2 says "Volume II Clause 7.3 is unchanged" |
| 5 | The Q16 semantic flag ("the answer adds") on a confirmation | `pkt` L443 |
| 6 | check-register exits 1 on the cover's own phantom word. C46 demands a row consequence for the cover's "deduction" because the cover's Form 4-A annotate is `adds_obligation` | `pkt` L958; `run.log` L47 |
| 7 | Points the documents settle are handed to a person | <ul><li>the Arabic precedence (D-05, D-07, D-08, DS-13; `iss` L26–27);</li><li>cover against operative text (`iss` L10; `new` L34–35: "Which governs is a human decision, so no date rule is planned from either here");</li><li>whether Q17 amends 12.3 (`DS` L3677);</li><li>whether VOL-I 6.2 or ADD-02 7.2 applies to 2.5, 2.6 or 2.3 (`DS` L518, L3509, L3576; `new` L79–81)</li></ul> |
| 8 | The same kind of Table 1-3 cell is treated two ways, depending on its batch | The TP-2 window and notice and notes 2–4 are settled `no_effect` (analysis-008, `ops` L375–427). The TP-1 cells and three TP-2 cells are unresolved as "reading pending" (analysis-007, `ops` L592–649) |

### Indirect effects (8): 1 hit, 5 partial, 2 missed

| Key | Result | Evidence |
|---|---|---|
| IE1: 7.2 band → VOL-V 1.5 PCOD → 12.1, 18.1, 18.3 and 29.x → VOL-I 12.1 | **partial** | The chain to VOL-V 1.5, 18.1 (SAR 180,000 a day) and 18.3 appears only in the unpromoted DS-11 (`DS` L2749–2781). The 7.2 row note names 1.5 (`a1` L224). No PCOD-dependent row is marked |
| IE2: 31.1(d) → 1.6 → 31.2 → 24.3 → 31.4 → 39.3; 29.3 does not cover (d); ADD-01 response 6 wrong; Financial Model and water balance | **partial** | <ul><li>31.2 uncapped (`DS` L236).</li><li>29.3 does not cover (d) (`iss` L8–9).</li><li>(d) "may produce one Unavailability Event per day for the persistent-breach count in 31.4" (`DS` L444), but CQ-PERSISTENT-BREACH was held by a check (`pkt` L897).</li><li>Financial Model REWORK/REVIEW (`a5c/README.md` L29–30, L45–46).</li></ul>Absent: 24.3, ADD-01 response 6 and the water balance |
| IE3: "replaces 8.1 to 8.3" also touches 8.2; Q19 relies on it | **hit** | `ops` L94–108; `pkt` L163; `DS` L3806 |
| IE4: CV appendix → Technical Proposal deliverable → page-limit exclusion → criterion E | **partial** | In the activity (`DS` L2843). "Appears to be a bid-stage submission requirement" (`DS` L139). The duration is kept as a PROVISIONAL ASSUMPTION (`DS` L457). No page-limit statement, no criterion E, no recruitment lead time |
| IE5: asset register before the run → spares recorded before the run | **missed** | The 8.1 re-read says the register is post-PCOD (`DS` L1156; false positive 2) |
| IE6: election → letter by 16 Nov → Arabic maximum durations → rejection; or deemed (a) → missing flow | **partial** | Every link is detected separately (`pkt` L109–137), and the 2.6 escalation ties back to 2.4 (`DS` L3576). The chain is not assembled in any promoted item or on A3/A5 |
| IE7: Q17 IE costs depend on DA1 → commissioning cost | **partial** | DS-11 ties Q17 to restarts and suggests holding IE cost for one restart (`DS` L2778–2791). It was not promoted (clarify.check) |
| IE8: band and 4.3 streams (flag only) | **missed** | nothing |

### Missing evidence (3): 2 hit, 1 missed

| Key | Result | Evidence |
|---|---|---|
| ME1: maximum transfer flow (2.4, Q20) | **hit** | Read from the Arabic and the English; issue, clarification, "No figure is assumed" (`iss` L35–44; `CQ` L1066–1094) |
| ME2: contents and channel of a "complete application" | **missed** | The phrase is quoted (`DS` L738), but not flagged as missing. Instead: "PROVISIONAL ASSUMPTION: preparing a complete application … takes 5 Working Days" (`DS` L757). Note 3 is read as construction-stage (`DS` L792) |
| ME3: the asset-register format | **hit** | "the Authority's standard format will be issued only to the Preferred Bidder" (`P` L467). I-VOL-II-MISSING is reached through VOL-II-7.4-01 (`a3c` L128) |

### Ambiguity, inconsistency, human judgment

| Key | Result | Evidence |
|---|---|---|
| DA1: out-of-range days (no correct answer) | **partial** | Escalated; no reading picked; both readings named (`pkt` L121–123). DS-11 adds "whether a Table 2-4 failure on a non-counting day restarts it", Q17 and the PCOD/LD exposure (`DS` L2771–2791). Missing: <ul><li>DS-11 was rejected by clarify.check, so no draft question reaches A4;</li><li>DA1 is absent from the candidate A3 (3.2 counted as answered);</li><li>nothing says the route is still open until Thu 12 Nov</li></ul> |
| II1: Q19 cites the deleted 8.2 | **hit** | 8.2 deleted (promoted); the clash escalated; the CMMS question left to a person; neither reinstated nor dropped (`DS` L1208, L3806; `a1` L227 "DELETED", candidate status UNRESOLVED) |
| HJ1: Q18 relief | **hit** | as Q18 |
| HJ2: whether to rely on method (b) | **hit** | "Whether the bidder will elect method (b) at all (a bid strategy decision)" (`DS` L3509) |

### Dates (8): 5 right, 1 partial, 2 missed

- **Right:**
  - D1: cut-off Thu 12 Nov, unchanged (`a5c/milestones.csv` L8). That ADD-03 came two Working Days earlier is not said.
  - D5: planning date 10 Nov ("status date 2026-10-22 -> 2026-11-10", `pkt` L1468).
  - D6: 12 Working Days from issue to the PDD (`pkt` L170).
  - D7: letter date 5 Nov (`rd` L56; `ops` L272–278).
  - D8: PDD Thu 26 Nov 14:00, unchanged (`a3c` L22).
- **Partial:** D2, the application deadline Mon 16 Nov. It is computed and shown as PROPOSED (`pkt` L171; `a5c/README.md` L14), but it is neither a row nor a milestone (D-17 and D-19 invalid).
- **Missed:**
  - D3, the latest response Mon 23 Nov;
  - D4, the date the cover implies (Sun 22 Nov, or Thu 19 Nov).
- **Figures:**
  - The band in m3/day (102,000–132,000) is not computed.
  - 31.1(d) is stated as a percentage only.
  - The maximum interruptions are stated right: TP-1 6 h and TP-2 4 h (`P` L110, L209).

### Marshalling (5): 4 hit, 1 partial

- **M1, the Shutdown Acceptance Letter: partial.** The evidence item has issuer Network Operator, Envelope A, one letter per point where (b) is elected, and the condition. It is held back because "no promotable row or activity uses EV-SHUTDOWN-ACCEPTANCE" (`DS` L5443; `pkt` L935). There is no marshalling row.
- **M2, the CV appendix: hit.** It is in the activity (`DS` L2843). That it falls outside the 150 pages is not said.
- **M3, the election and the over-pumping design: hit.** The activity names the election, and the design flow is ME1.
- **M4, Form 4-A acknowledgement: hit.** ADD-03-cover-para3-01 (`new` L7–50); form-4a REWORK (`a5c/README.md` L31–32).
- **M5, planning date and Working Days: hit.**
- The "unchanged" items (Bid Bond, copies, Forms 4-C and 4-G, Envelope B, PDD, cut-off) are not touched.

### A3

The validated A3 stays at ADD-02, because ADD-03 is PARTIAL. The candidate A3 gains 0 rows, loses 0 and changes 0 (`a3c` L9–13).

- **Added: A3-1, 2.7 rejection (TP-1 6 h; TP-2 4 h; only where flow is interrupted): partial.** It is not a trigger row. It appears only as the open issue I-ADD03-T13-ARABIC-ENGLISH, which names 2.7 but not the values (`a3c` L151; `iss` L31–32).
- **Must not be added (4): all avoided.**
  - A missing letter: not added; the deeming is read right (`pkt` L117).
  - The election: the row's consequence is `none_stated` (`new` L76).
  - The CV: not added.
  - The band, 31.1(d), 12.3 and the asset register: "No bid-out consequence stated" (`DS` L5594, L5641).
- **Unresolved list (5): 4 shown.**
  - DA1: **no** (absent from `a3c` L65–88).
  - II1: yes (`a3c` L75, L101).
  - ME1: yes (`a3c` L69, L76).
  - HJ1: yes (`a3c` L74).
  - E1–E3: yes (`a3c` L150).

### Traps: 23 of 23 avoided (two borderline)

Each trap was avoided:

- The PDD and its time are unchanged; so is the cut-off.
- No 29.3 change and no Ramp-Up exemption for (d).
- No 22 Nov or 19 Nov deadline, and no count from the addendum's date.
- The Authority does not issue the letter.
- A missing letter does not make the Proposal non-responsive.
- No conflict with 4.1's "pumped bypass".
- No transfer flow figure.
- No definite rule for out-of-range days.
- Nominal capacity is unchanged.
- 8.2 is not retained.
- 8.4 and 8.5 are unchanged, and nothing is renumbered.
- Q16 does not amend 3.3, and Q15 has no effect.
- Q18 gets no yes or no.
- 12.3 is not deleted, and the first run's split is kept.
- The (a) and (c) cure periods and the letters are kept.
- ADD-02 response 12 and ADD-01 response 2 are not made wrong.
- No Form is reissued.
- The Bid Bond, copies, Envelope B, Form 4-C and local content are unchanged.

The two borderline cases:

- **TP-2 at 6 h:** stated as Table 1-3's value only in the unpromoted ADD-03-DS-ESC-2.7 (false positive 1).
- **"7.3 amended":** only in a staleness reason ("VOL-II:7.3 changed since BASE"; false signal 4). The op says `confirms`.

## 2. Usable updates

What was promoted into the candidate (`pkt` L943–953), all PROPOSED:

- 11 ops: cover/para3 (Form 4-A), 2.1, 3.1, 3.2(b), 4.1(a), 4.1(b), 4.1(c), 4.2, 5.1, 5.2 and Q16;
- 39 dispositions;
- 2 new rows;
- 11 re-made readings: VOL-II-3.3-01, VOL-II-8.3-02, the four 8.4/8.5 rows, the three 31.1 rows, and 31.3-01/02;
- 4 issues;
- 1 activity (technical-proposal);
- 2 clarifications;
- 1 relationship (REL-AI-001);
- the image reading (pending).

Of the 34 detected key items (35 less U8):

| Class | Key items | Count |
|---|---|---|
| **Applied, and a person could accept it as is** | 2.3 (row), 3.1, 4.1, 4.2, 5.1, 5.2 (ops), Q15, Q16, Q20 (issue + draft question), E1, E2, E3 (issue + draft question + row note), the reading (pending its approval), U1, U2, U3, U4 (ops + activity) | 17 |
| **Applied in part** | 2.1 (the op, without the tie-in condition rows), 2.4 (issue and question, no row), AR1 and AR2 (issue without the 4 h value or the Eid wording), U7 (through relationships, not the definition) | 5 |
| **Detection only** (an analysis statement, an escalation or an unpromoted item) | 2.2, 2.5 (with 16 Nov), 2.6, 2.7, 3.2(a)/DA1, Q17, Q18, Q19, U5, U6, U9, U10. For Q18 and DA1 an escalation is the expected final form | 12 |
| **Wrong as applied** | none of the key's effects is applied with wrong content. One promoted group would mislead if accepted as is (below) | 0 (+1 group) |

**Promoted items that would mislead if accepted as is:**

- The `no_effect` dispositions on `ADD-03:p4-image/note2` and `note3` and their English renderings `T1-3/note(2)` and `note(3)` (`ops` L399–418, L484–500). These notes carry obligations: one shutdown per tie-in point, and requests through the portal with a programme and a contingency plan. The dispositions themselves say "The note does restrict" and "The note does oblige", and say the obligation "enters Volume II through ADD-03 2.1". But the rows that would carry those obligations (D-12, D-13) were rejected. Accepting these dispositions settles the notes while the obligations reach no row.
- The same applies to `tp2-window` and `tp2-notice` (`ops` L375–391), while the TP-1 cells stay unresolved.
- The new row ADD-03-cover-para3-01 carries a date note: "Which governs is a human decision, so no date rule is planned from either here" (`new` L31–35). Accepted as is, it leaves the shutdown application without a date, although 2.5 (which governs) gives Mon 16 Nov.

**Flagged, not wrong.** Four amended rows keep their pre-ADD-03 readings: VOL-II-7.2-01, 8.1-01, 8.3-01 and VOL-V-31.3-03 (`a1` L224, L226, L228, L426). All four are marked STALE and UNRESOLVED. Their re-readings existed but failed validation (section 3).

## 3. Missed effects and why

**No trace, or a wrong trace:**

| Key item | Reason as far as the frozen files show it |
|---|---|
| U8: ADD-01 response 6 made wrong (also IE2) | **Not read.** The re-read list covers only answers that cite a changed unit (`pkt` L160–164). ADD-01 Q6 annotates VOL-V 29.1–29.5 (`a2` L31), not 31.1 |
| IE5: spares recorded before the run | **Read, contradicted.** The downstream re-read of 8.1 treats the register as post-PCOD (`DS` L1156). Q19's change was not promoted, so the downstream batch had nothing to read it against |
| IE8: 4.3 streams at 132,000 m3/day | **Not proposed** (a flag-only item in the key) |
| ME2: contents and channel of a complete application | **Read, not proposed.** Replaced by a 5-WD PROVISIONAL ASSUMPTION (`DS` L757) |
| D3 (Mon 23 Nov), D4 (Sun 22 Nov), the band in m3/day | **Not computed.** The one computed_date task covers only the "before the PDD" deadline (`run.log` L36; `pkt` L171). A forward period and the cover's anchor get no calculation |

**Detected, not applied** (the reasons behind the 14 partials):

- **Rejected by a downstream check:**
  - All three `replace_requirement` row readings (VOL-II-7.2-01, 8.1-01, 8.3-01): "replace_requirement.old is not the row's requirement (or new is empty)" (`pkt` L878–881).
  - All three re-read clarification drafts (CQ-VOL-III-DRAWINGS, CQ-PERSISTENT-BREACH and CQ-PCOD-RELIABILITY-RUN, the DA1 question) failed "not verbatim in VOL-…". They quote the text as amended by ADD-03 (`pkt` L896–898).
  - Six conditional rows and an issue from the image: "ADD-03:p4-image is not a provision of ADD-03" (`pkt` L926–932).
  - The 2.5 row (the date-rule kind "deadline"), its activity (fingerprint) and its evidence item (held back) (`pkt` L934–936).
  - D-16 (a fact not verbatim, `pkt` L933).
  - DS-05, whose basis quote predates 5.2 (`pkt` L892).
- **Held by a declared conflict or missing words (analysis):**
  - 2.2, 2.7 and Q19 are `conflicting`;
  - Q17 has no printed wording;
  - 2.3 asked for a row.
- **Escalated for want of a target unit** (free-standing ADD-03 text): 2.4, 2.5, 2.6 and 3.2(a). An example is C22 "not cited: [VOL-II:7.2]" (`pkt` L121).
- **Pending reading (by design):** 8 cells in analysis-007, plus tp2-duration, note1, T1-3/tp-2 and T1-3/note(1).
- **Split by a batch boundary:**
  - The same kind of Table 1-3 cell is unresolved in analysis-007 but `no_effect` in analysis-006 and analysis-008 (`ops` L367–427 against L592–649).
  - Analyses 002, 008 and 010 say the Arabic governs (`P` L209, L949). Downstream-004 says "Which rendering governs … is a person's decision" (`DS` L4269, L4389).
- **Dropped by provision-level resolution:** 3.2 is counted as answered because 3.2(b) was promoted (`a2` L525). Its escalation 3.2(a), DA1, therefore does not reach the candidate A3 or A4.

## 4. Pending decisions

**Volume.**

- 22 provisions are unresolved, listed first (`pkt` L105–158).
- There are 9 analysis escalations and 25 downstream escalation items (22 tasks).
- HUMAN DECISION PENDING is marked on 12 analysis items (`pkt` L178–870) and 9 downstream items (`pkt` L893–932, one of them invalid).

| Item | Candidate | Key | Verdict |
|---|---|---|---|
| DA1 (no correct answer) | escalated, no reading picked (`pkt` L121–123) | escalate; a question is still possible until 12 Nov | right handling; incompletely surfaced (section 1) |
| II1 | 8.2 deleted; the Q19 clash and the CMMS question escalated (`DS` L1208, L3806) | flag and escalate | right |
| HJ1 (Q18) | escalated, no yes or no (`DS` L3741) | a person | right |
| HJ2 (method (b) at all) | "a bid strategy decision" (`DS` L3509) | a person | right |
| The image reading | pending (`rd` L1–3) | approval by a person | right |
| Arabic against English (2.2) | "a person's decision" (`DS` L4269, L4389); "Legal decides" (`iss` L26–27) | settled by 2.2: the Arabic governs | **over-escalated** |
| Cover against operative (E1–E3) | "Which text governs is a decision for Legal" (`iss` L10; `new` L34–35) | the operative provision governs; report the cover's error | **over-escalated**. The candidate's own I-ADD-03-COVER-01 states the rule (`iss` L55–57) |
| Q17 ("is amended accordingly") | "a person's decision" whether it amends (`DS` L3677) | it amends 12.3 | **over-escalated**, together with a tool gap (no op for an amendment without printed words) |
| 2.5, 2.6, 2.3 against VOL-I 6.2 / ADD-02 7.2 | "a person's decision" / "a legal question" (`DS` L518, L3509, L3576; `new` L79–81) | 2.6 deems method (a); no rejection | **over-escalated** |

**System judgments the key reserves for a person: none found.** The interim advice is labelled and leaves the decision to its owner:

- "plan … to the earlier of the two deadlines", "price 31.1(d) deductions as applying in the Ramp-Up Period" (`iss` L10–11);
- DS-11's "Hold programme float and Independent Engineer cost for at least one full restart" (`DS` L2790–2791).

The promoted `no_effect` dispositions on the Table 1-3 notes say "A person should confirm". They are proposals, not decisions; section 2 describes the risk in accepting them.

## 5. Interventions

**None manual.**

- `ckpt` `interventions` has 15 entries, each "host session (automatic) … not a person" (`pkt` L1328–1344): reading 1, analysis 10, downstream 4.
- Every batch ran once (attempts 1 in `ckpt` `batches`). Downstream-003 was repaired once, a re-ask for one problem (`pkt` L1309). There were no deferrals and no rate-limit failures (`pkt` L1307–1326 lists none).
- The critic's 13 requests changed no status (run.log L10–28, L40–42: 65 analysis items reviewed with 6 disagreements; 9 downstream items with 2).
- The coordinator states there was no manual step (`FROZEN-OUTPUTS.md` L16).
- The only edits after the run were bookkeeping outside the PDF-to-outputs path, both labelled:
  - the exit line and end time appended to `run.log` and `clock.txt` at 18:29:57 (`FROZEN-OUTPUTS.md` L17);
  - the 18:31:22 correction of two sentences of `FROZEN-OUTPUTS.md` (L20).

## 6. Time

| Step (run.log L52–66) | Seconds | Note |
|---|---|---|
| ingest | 29.7 | refused once for the unread image region, then re-run inside readings |
| readings | 211.4 | one host session read page 4 (198.8 s, `ckpt`) |
| analysis | 2,170.6 | 10 host sessions, at most 2 in flight, each followed by a critic request in the collection loop |
| validation | 6.0 | |
| downstream | 838.9 | 4 host sessions, at most 2 in flight |
| downstream_validation | 0.7 | |
| critic (downstream) | 47.2 | 3 requests, after downstream |
| promotion, pin, check_register | 22.4 | check-register exit 1 (C46 on the cover) |
| outputs | 12.4 | exit 0; 103 files carry the banner |
| diff, review | 6.3 | |
| **Total of the steps** | **3,345.6 (55.8 min)** | |
| **Clock, PDF to candidate outputs and review packet** (`clock.txt`) | **17:32:26 → 18:28:15 = 55 min 49 s** | no interruption; `max_parallel_sessions=2` (`clock.txt` L1) |

**Against the brief's 30 minutes: missed by 25 min 49 s.** Against blind-05 (72 min 27 s at one session in flight): 16 min 38 s faster, 23 % less. The addenda differ, though: 70 provisions here against 54, and 10 + 4 batches against 9 + 5.

- Host sessions (reading, analysis, downstream, critic) took 3,268.1 s, 97.7 % of the steps. Every deterministic step together took 77.5 s.
- 15 host sessions and 13 critic requests: 28 model requests.

**What the second session in flight bought.** These are my inferences from the proposal-set ids, which carry each session's finishing time, and from the `batch_asked_ahead` events in `log.jsonl`.

- The ten analysis sessions ran for about 3,211 s in total, within 2,171 s of wall clock (about 1.48 in flight on average).
- The four downstream sessions ran for about 1,474 s within 839 s (about 1.76 in flight).
- Run one after another, as in blind-05, the two phases would have taken about 3,388 s (with the 177 s of analysis critics) and 1,474 s. **The second slot saved about 1,850 s (31 min)**; this run would otherwise have taken about 86 min.

**What did not speed up:**

- **The image reading** (211 s) runs alone before any analysis.
- **Each session's own latency**: analysis sessions took 176–483 s each, downstream sessions 274–435 s.
- **Results are taken in order, and the critic runs inside the collection loop** (about 177 s in analysis, 47 s after downstream). The next batch is asked only when the earlier batch and its critic are done. Three batches finished early and waited: 005 about 260 s, 007 about 60 s, 009 about 200 s. That is about 8.7 min of the second slot idle in analysis.
- **The phase barrier**: downstream starts only after all of analysis.
- **The deterministic steps** (77.5 s) were already small.

**To reach 30 minutes** (an estimate): about 4,880 s of session time has to fit into about 1,500 s after the reading and the deterministic steps. That needs about 3 sessions in flight on average with no idle slot. In practice that means 3–4 in flight, collection as sessions finish, the critic outside the collection loop, or fewer and larger batches.

## Review effort (what a person must look at; nothing accepted)

| Item | Count | By status |
|---|---|---|
| Image reading ADD-03-p4-r1 | 1 (35 blocks; 36 units touched, `pkt` L57) | pending |
| Analysis items (`P`) | 83 over 70 provisions | interpretation_pending 45, evidence_verified 15, insufficient_evidence 11, conflicting 7, escalated 5 (`run.log` L30). By type: 47 dispositions, 17 ops, 9 escalations, 7 issues, 3 clarifications |
| Statements behind them | 75 (`P`) + 42 (`DS`) | 84 facts, 25 interpretations, 8 assumptions |
| Downstream items (`DS`) | 64 for 48 tasks | escalated 22, interpretation_pending 19, invalid 10, insufficient_evidence 9, conflicting 3, evidence_verified 1 (`run.log` L38) |
| Promoted into the candidate | 71 | 11 ops, 39 dispositions, 2 rows, 11 readings, 4 issues, 1 activity, 2 clarifications, 1 relationship; plus 22 unresolved records (`promotion.json`) |
| Critic opinions | 74 reviewed | 66 agree, 8 do not |
| Approved | 0 | |

I have not estimated a review time. The packet is shorter than blind-05's in decisions (about five), but longer in noise: 22 escalations, 8 of which simply wait for the reading.

The five decisions:

1. approve or correct the reading;
2. confirm that the Arabic governs (4 h; Eid);
3. confirm the cover errors;
4. DA1;
5. the CMMS (II1).

## Follow-ups: defects in the workflow (stated generally)

1. **A provision counts as answered when one sub-item is promoted and a sibling is escalated.** The escalation then drops off the unresolved list, the A2 coverage and the candidate A3 and A4. Here that hid DA1, the only no-correct-answer item (`a2` L525; `a3c` L65–88).
2. **clarify.check compares a draft's quoted words with the printed unit, not with the effective text at the working stage.** Every re-read clarification that quotes amended text fails (3 of 3, `pkt` L896–898).
3. **The downstream `replace_requirement` payload is untyped in the packet schema** (`batches/downstream-001.packet.json` L1386–1396), while the validator needs `old` (the row's requirement) and `new`. All 3 such row readings failed, and the amended rows stay STALE.
4. **reading_rows proposals cannot validate.** The provision check refuses the region's parent unit ("ADD-03:p4-image is not a provision"), although its blocks are provisions. All 7 items were invalid, so blind-05's follow-up 6 is still unmet in practice.
5. **The computed_date task's output does not fit the register or the programme.** The date-rule kind "deadline" is not accepted, and the activity's `computed_from` fingerprint does not match the program's own calculation. A computed deadline (16 Nov) therefore never becomes a row or a milestone (blind-05 follow-up 7). Forward periods ("within 5 WD of receipt") and the cover's own anchor are not computed.
6. **No consistency check across batches or phases.**
   - Identical Table 1-3 cells get opposite treatment depending on their batch.
   - Downstream reverses an analysis conclusion (the Arabic governs) by handing it to a person.
   - A promoted `no_effect` can settle a note whose obligation reaches no row.
7. **C28 marks accurate cover claims "contradicted"** when the operative provision amends the claimed target, and the A3 candidate lists them as conflicts.
8. **The cover's `adds_obligation` annotate (for Form 4-A) brings the whole cover paragraph under C46,** so the cover's phantom "deduction" makes check-register exit 1.
9. **A `confirms` annotation is reported as "changed since BASE" in staleness reasons** (7.3).
10. **The semantic check flags a confirming answer as "adds"** (Q16).
11. **The re-read list misses earlier answers whose basis a change overturns** without citing the changed unit (ADD-01 Q6 on 29.x against the new 31.1(d)).
12. **Over-escalation.** The rule "operative text governs over the cover" and an addendum's own precedence clause (2.2) are known to the analysis prompts, but issues and escalations still present them as decisions for Legal.
13. **The free-standing addendum provisions (2.4–2.7, 3.2(a)) still have no op or row path.** They are escalated for want of a cited unit (blind-05 follow-up 5).
14. **Time.** In-order collection and the critic inside the collection loop leave the second slot idle about 8.7 min. With 2 in flight the host route cannot reach 30 minutes on a 70-provision addendum.

## Where the key and the candidate disagree

I found no item where I think the key is wrong. Two points where the candidate's method differs and the number agrees:

- **Working Days left.** The key counts 10 Nov inclusive to 26 Nov exclusive; the candidate counts the issue date excluded and the PDD included (`pkt` L170). Both give 12.
- **Q17's "is amended accordingly".** The key reads it as an amendment of 12.3, and I agree. The candidate's objection, that no words are printed, is a real representational gap in the op types, not a reason to doubt the key.

I have checked three date counts against VOL-I 2.4 and agree with the key:

- Mon 16 Nov (8 WD before the PDD);
- Mon 23 Nov (5 WD forward);
- Sun 22 Nov or Thu 19 Nov (the cover's anchor).

## ADD-04

The key's `addendum_4` items are not scored, on the owner's instruction: Addendum No. 4 was dropped from this rehearsal ("no need for addendum 04, continue only with addendum 03 stuff").
