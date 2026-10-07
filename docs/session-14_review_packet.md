# Session 14: the consolidated review packet (decisions that genuinely need the owner)

**Status: in progress** (started 18:34 UTC; completed at the end of the session with the rehearsal results and the final review). Nothing here is decided; every item is PROPOSED or PENDING in the outputs until a person records a decision through the panel's decisions form or `tenderpack approve`. The three groups are the ones the owner asked for. Each item names where it shows in the outputs.

## A. Software failures (what the tool got wrong or cannot do; fixed where marked, otherwise known)

| # | What | State | Where |
|---|---|---|---|
| A1 | Session 14's own code had slowed every model-free step of a run by 25–55 % (one unmemoised scan reached twice as often). | FIXED (E167); the recorded run 131 s from 416 s. | work log §6 |
| A2 | The package's smoke check mistook the run lock's empty `ai/` folder for a session when two sessions may run at once. | FIXED, with a test. | `tests/test_session14_smoke_check.py` |
| A3 | The W2/W3 join overwrote the workflow's own provision records in conditional impact tasks. | FIXED (one basis vocabulary). | `tenderpack/ai/downstream.py` |
| A4 | A1's new Value column showed a row deleted by one addendum and reinstated by the next as "unchanged since BASE" (VOL-I-8.6-01, the Local Content Certificate, 30 % → deleted → 35 % with a non-responsive consequence). | FIX IN PROGRESS (F1; R1-1, R2-M2, R3-1). | `out/a1/`, the batch-02 card |
| A5 | A1 and A2 disagreed on which rows the missing Permit's issue reaches (A2's relationship-impact table said three rows blocked; A1 and A2's rows-moved omitted it). | FIX IN PROGRESS (F1; R1-2, R2-M3): one rule for an issue's reach. Whether I-PERMIT applies to those rows is C3 below. | `out/a1/`, `out/a2/` |
| A6 | The Form 4-E findings (three documents finishing after Form 4-E starts; a strict ordering infeasible by 14 WD, of which 12 WD are the LCC's own) were not on the form-4e activity in the programme, the Gantt or marshalling ("timing OK, float 1"). | FIX IN PROGRESS (F2; R3-2). | `out/a5/` |
| A7 | `form_4e_checks` printed "final on <date>" for eight documents whose finalisation is gated or needs a decision (Form 4-A/4-B finalise-by 23 Nov, after Form 4-E starts on 19 Nov). | FIX IN PROGRESS (F2). | `out/a5/form_4e_checks.*` |
| A8 | The concession-term decision (I-CONCESSION) did not reach the Financial Model chain or Form 4-F in A5 although A1, A4 and A3 say it sets the term start in the Financial Model. | FIX IN PROGRESS (F2; R3-3). | `out/a5/` |
| A9 | Minor presentation defects: the value column against the row's status on four rows; "(confirms) … (not a confirmation)" side by side; the A3 heading's "25 open issues" against 50; the † decide-by against A5's finalisation dates; CQ-ENV-PERMIT tied to 3 rows instead of the 13 its answer would change; Arabic in the cards not marked right-to-left; the Form 4-G citation quoting the form heading. | FIX IN PROGRESS (F1, F2). | A1, A3, A4, the cards |
| A10 | Not fixed, known: `documents.csv` has no flags column; the Gantt's fonts are small (one A4 landscape page, nothing cut). | KNOWN, carried over. | `out/a5/` |
| A11 | The blind-07 regression's results and the sealed blind-08's: PENDING (this section is completed from the scorers' reports). | PENDING | `rehearsals/` |

## B. Missing evidence (what the documents do not give; nothing can settle these without the document or the person)

| # | What | Where it shows |
|---|---|---|
| B1 | The Environmental Permit is not in the pack; VOL-II's Table 2-4 is a reproduction and "the Environmental Permit shall prevail". Every Table 2-4 row's reading stays conditional on it (I-PERMIT; the clarification CQ-ENV-PERMIT drafted, not sent). | A1 Issues, A2, A4, A5 |
| B2 | The two image readings (VOL-II p3 Table 2-4, VOL-IV p6 Form 4-C Arabic) are approved as TRANSCRIPTIONS only; their interpretations are not approved and stay pending. | A1's Approval column, the cards |
| B3 | The durations, effort, waiting parties and capacity in A5 are labelled assumptions (`config/assumptions.yaml`); the lead times await the owner (A5-7, pending by design). | A5 README, the Gantt legend |
| B4 | Bidder facts (the bidder's own figures: local content ratio, bond issuer, financial standing) are not in the pack; the rows that need them say so (I-BIDDER-FACTS). | A1 |
| B5 | The sealed blind-08 run's "missing evidence" findings: PENDING (from the scorer). | `rehearsals/blind-08/` |

## C. Human approvals and judgments (yours or your named owners'; the tool proposes, never decides)

| # | Decision | Owner named in the outputs | What the tool shows meanwhile |
|---|---|---|---|
| C1 | The 205 register rows and the 38 amendment ops: accept, reject or defer each, as named decisions bound to the content (the two release blockers). | Bid manager and the row owners | `outputs --strict` refuses release (exit 3) until then |
| C2 | The ramp-up scope ruling: VOL-V 29.3 relieves only the rolling-average parameters, so the maxima/range issue (chlorine and pH, "Continuous at outlet") no longer reaches VOL-V-29.3-01 (`scope_words` on REL-T24-RAMP-UP-DEDUCTIONS, a PROPOSED curation; all three reviewers' own readings support it). Accept, or keep the issue on 29.3-01. | Process engineer / Legal counsel | labelled "(scope PROPOSED, not reviewed; the owner may keep the issue on the row)" after F1 |
| C3 | Whether I-PERMIT (the missing Permit prevails over VOL-II's reproduction) applies to VOL-V-29.3-01, VOL-II-2.5-01 and VOL-II-4.3-02 through the Table 2-4 relationships. | Process engineer / Legal counsel | carried as the open issue it is on every row the one rule reaches, never settled (after F1) |
| C4 | The Form 4-E commercial-qualification tension: VOL-I 9.6 requires a commercial qualification to be listed in Form 4-E (Envelope A), 6.2 makes commercial information in Envelope A non-responsive, 10.5 makes a conditional price in Envelope B non-responsive, Form 4-F is "not subject to any qualification". | Legal counsel, with Commercial | the PROPOSED issue I-FORM-4E-COMMERCIAL-QUALIFICATION, HUMAN DECISION PENDING, on VOL-I-9.6-01, 10.5-01, 6.2-02 and VOL-IV-F4F-02 (after F1) |
| C5 | How Form 4-E is cross-checked against documents that finish after it starts (lcc-certificate, form-4f, model-audit-opinion); a strict ordering is infeasible by 14 WD on the assumed durations (12 WD are the LCC's own; the ordering itself costs 2). | Bid manager, Legal counsel | the PROPOSED issue I-FORM-4E-CROSS-CHECK on the form-4e activity (after F1/F2) |
| C6 | The page-limit issue I-VOL-I-PAGE-LIMIT-Q2 (session 13 §9 H): all three reviewers read VOL-I 9.2 as amended by ADD-02 2.1 ("excluding the Form Sheets and the appendices expressly permitted by Volume II") as settling the point by its own words. Confirm the application of that clause, or keep the issue open. | Bid manager | re-presented as "PROPOSED BASIS (applied rule; a person confirms the application)" with the clause quoted (after F1); never closed by the tool |
| C7 | The concession term start (I-CONCESSION: term from PCOD, VOL-I 12.1, or from the Effective Date, VOL-V 3.1): the decision sets the term start in the Financial Model and Form 4-F. | Legal counsel / Commercial | an open decision on the Financial Model chain and Form 4-F in A5 (after F2) |
| C8 | "At all times" (VOL-II 2.4: the reading of the Table 2-4 limits as maxima at every instant or as the stated averaging basis). | Process engineer | HUMAN DECISION PENDING; interim basis labelled proposed |
| C9 | Programme readiness: whether an activity may be gated on an open decision (`planning.gate_on_open_decisions`, off by default). | Bid manager | off; "OPEN DECISION" tags only |
| C10 | Whether CONFIRMED stays A2's label for a row whose confirming op is only proposed, or reads NOT SETTLED until accepted. | the owner (presentation rule) | CONFIRMED with "(proposed op, awaiting a person's acceptance)" on every such line |
| C11 | Software choices awaiting your preference: level 3 of the Mac check (a whole offline run with a local model) on by default or opt-in; an all-escalated set as PARTIAL or FAIL at level 2; the extra downstream work for every unapplied change and analysis issue (blind-07: about 9 extra tasks; a run stays partial until answered) accepted or capped; the closed-window note on judgment items kept or restricted to the clarification class. | the owner | today: on by default; PARTIAL; uncapped; kept |
| C12 | The decisions the sealed blind-08 run leaves to a person: PENDING (from the run's review packet and the scorer). | | `rehearsals/blind-08/` |
