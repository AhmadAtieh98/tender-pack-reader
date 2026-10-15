# PRELIMINARY AI BRIEFING — unverified: not a decision, not a validation; calculations and interpretations unchecked

**preliminary; model output; not a tool result**

Quick review `ADD-03-qr-host-20261015T131927Z-37e3` of ADD-03 (PDF sha256 `6f9f9d7c7d68bc83…`), read against the published ADD-02 workspace; route host, model the host CLI's default; written 2026-10-15T13:26:22Z.

Nothing here edits curation/, approves an item or marks the main workflow's work complete. Each item is a prediction by a model; the program checked only whether the quoted words are on the page named and whether a target id exists. Compare it with a run: `tenderpack ai quick-review compare ADD-03-qr-host-20261015T131927Z-37e3 <run id>` (model agreement is not proof).

## Predicted changes

### cover-summary: provision ADDENDUM NO. 3 — cover summary (page 1): annotate, confidence high
- quotation: “This Addendum amends the Proposal Due Date and Bid Bond, withdraws Form 4-G, increases the nominal capacity with
a consequential change to the reference project threshold, amends Table 2-4, adds a new Clause 11.6, and responds to
clarification requests 15 to 18.” (verbatim on page 1 of the addendum's text layer)
- target guess: none (no target guessed)
- deliverables affected: A2, A4
- uncertainty: none
- what depends on it: Use as an inventory of the operative provisions below, without treating the summary as an independent amendment.

### cover-acknowledgement: provision ADDENDUM NO. 3 — acknowledgement and unchanged terms (page 1): annotate, confidence high
- quotation: “This Addendum forms part of the RFP Documents and takes precedence in accordance with Volume I Clause 3.2. Bidders
shall acknowledge receipt in Form 4-A. All other terms of the RFP Documents remain unchanged.” (verbatim on page 1 of the addendum's text layer)
- target guess: ADD-01:AppA/addenda-acknowledged-numbers (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “Addenda acknowledged (numbers):”
- deliverables affected: A1, A2, A4, A5; rows/activities: ADD-01:AppA/addenda-acknowledged-numbers, VOL-I:3.2
- uncertainty: none
- what depends on it: Proposed A5 work: include ADD-03 in the Form 4-A acknowledgement and submission check.; Record the unchanged-terms reservation alongside each scoped amendment; any application of precedence remains for Legal.

### 1.1: provision 1.1 (page 1): annotate, confidence high
- quotation: “This Addendum takes precedence over Addenda Nos. 1 and 2 in accordance with Volume I Clause 3.2.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-I:3.2(a) (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “(a) the Addenda, a later Addendum prevailing over an earlier one;”
- deliverables affected: A2, A4; rows/activities: VOL-I:3.2(a)
- uncertainty: none
- what depends on it: Record the recital against the existing precedence provision; it does not itself determine any particular conflict or reopen earlier decisions.

### 2.1: provision 2.1 (page 1): replace, confidence high
- quotation: “Volume I Clause 6.1 is amended by deleting ‘Thursday 26 November 2026’ and substituting ‘Thursday 10
December 2026’, 14:00 Riyadh time.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-I:6.1 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “Proposals shall be received by the Authority not later than 14:00 hours Riyadh time on Thursday 26 November 2026 at the address given in Appendix 3.”
- deliverables affected: A1, A2, A3, A4, A5; rows/activities: VOL-I:6.1, VOL-I:6.6, ADD-01:AppA/proposal-due-date
- uncertainty: none
- what depends on it: Proposed A5 work: recompute submission and all dependent milestones through date rules, then review preparation dependencies.; A3 rejection dependency, VOL-I:6.6: “A Proposal received after the time stated in Clause 6.1 will be rejected unopened and returned to the Bidder.”; Document control review: ADD-01:AppA/proposal-due-date still says “Proposal Due Date: 12 November 2026, 14:00 Riyadh time” at ADD-02. Do not silently rewrite this separate form field.; Review deadline-dependent evidence and permissions in VOL-I:3.4, VOL-I:6.7 and VOL-I:8.3.

### 2.2: provision 2.2 (page 1): annotate, confidence high
- quotation: “Every period calculated by reference to the Proposal Due Date is adjusted accordingly.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-I:5.2 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “Requests for clarification shall be submitted no later than ten (10) Working Days before the Proposal Due Date. Requests received after that time will not be answered.”
- deliverables affected: A1, A2, A3, A4, A5; rows/activities: VOL-I:5.2, VOL-I:6.3, VOL-I:7.1, VOL-I:8.5#fn12
- uncertainty: none
- what depends on it: Recompute the clarification cut-off, bond expiry, Proposal validity expiry and reference-project look-back using the amended due-date rule.; Apply Section 5.2's separately printed change to the bond duration when recomputing its expiry.; Review clarification-register deadlines and A5 activities for clarification preparation, bank issuance, reference evidence and submission.; VOL-I:8.3 requires the ISO certificate to be “current as at the Proposal Due Date”; its evidence check follows the new date.

### 3.1-form: provision 3.1 — Form 4-G withdrawal (page 1): delete, confidence high
- quotation: “Form 4-G (Cybersecurity Compliance Undertaking), added by Addendum No. 2 Section 7, is withdrawn. Bidders
shall disregard it and shall not submit it.” (verbatim on page 1 of the addendum's text layer)
- target guess: ADD-02:H:F4-G (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “FORM 4-G — CYBERSECURITY COMPLIANCE UNDERTAKING”
- deliverables affected: A1, A2, A4, A5; rows/activities: ADD-02:H:F4-G, ADD-02:F4-G/T1, ADD-02:F4-G/T1/1, ADD-02:F4-G/T1/2, ADD-02:F4-G/T1/3, ADD-02:F4-G/T1/4, ADD-02:F4-G/T1/5, ADD-02:F4-G/T1/6, ADD-02:F4-G/para1, ADD-02:7.1, VOL-I:9.1
- uncertainty: none
- what depends on it: Predict withdrawal of the form, including its undertaking rows, confirmation column and signature fields.; Reconcile its insertion into the Envelope A list: ADD-02:7.1 says “A new Form 4-G is added to Volume IV and to the list at Volume I Clause 9.1, to be inserted after item (e).”; Proposed A5 work: revise the form preparation, signature and submission checklist; preserve the separate Section 6 narrative work required by Section 3.2.; Do not infer that every undertaking formerly printed in the form survives as a separate substantive obligation.

### 3.1-consequence: provision 3.1 — cessation of Section 7.2 (page 1): delete, confidence high
- quotation: “Section 7.2 of Addendum No. 2 ceases to have effect.” (verbatim on page 1 of the addendum's text layer)
- target guess: ADD-02:7.2 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “Form 4-G shall be completed and submitted with Envelope A. Failure to submit Form 4-G shall render the Proposal non-responsive.”
- deliverables affected: A1, A2, A3, A4, A5; rows/activities: ADD-02:7.2
- uncertainty: none
- what depends on it: Predict removal of this submission obligation and its expressly stated A3 non-responsiveness consequence from the ADD-03 effective requirements, retaining their earlier-stage history.; Review any clarification answer or submission check relying on ADD-02:7.2; no consequence for the new narrative requirement is stated in Section 3.2.

### 3.2: provision 3.2 (page 1): annotate, confidence high
- quotation: “The substantive requirements of Volume II Section 6 are unchanged and shall be addressed in the Technical Proposal
narrative.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-II:H:S6 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “SECTION 6 — SCADA, CONTROL AND CYBER SECURITY”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-II:6.1, VOL-II:6.2, VOL-II:6.3, VOL-I:9.2
- uncertainty: none
- what depends on it: Proposed A5 work: prepare narrative coverage of SCADA, network segregation, the information security management system and security architecture.; VOL-II:6.2 says “The industrial control system shall be segregated from any business network by a demilitarised zone with unidirectional data flow to the Authority's monitoring interface.”; VOL-II:6.3 says “The Project Company shall implement and maintain an information security management system covering the operational technology environment, and shall submit its security architecture for the Authority's review prior to commissioning.”; Review narrative allocation against VOL-I:9.2's ADD-02 effective limit: “one hundred and fifty (150) pages of A4”.

### 4.1-clause: provision 4.1 — Volume II Clause 2.1 (page 1): replace, confidence high
- quotation: “In Volume II Clause 2.1 and in Table 2-6 row 2-6.1, ‘120,000 m3/day’ is deleted and ‘150,000 m3/day’ is
substituted.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-II:2.1 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “The Facility shall be designed for a nominal treatment capacity of 120,000 m³/day average daily flow, measured at the inlet works, at the design year influent characteristics stated in Table 2-2.”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-II:2.1, VOL-II:2.3, VOL-II:3.1, VOL-II:7.2
- uncertainty: none
- what depends on it: Proposed A5 work: revisit process sizing, hydraulic design, technical narrative and pricing inputs using the printed amended nominal capacity.; Recompute quantities dependent on nominal capacity under VOL-II:2.3 and VOL-II:7.2; no derived quantity is calculated here.; Review design against the unchanged Table 2-2 concentrations, unchanged peak hourly flow and unchanged construction duration.

### 4.1-table: provision 4.1 — Table 2-6 row 2-6.1 (page 1): replace, confidence high
- quotation: “In Volume II Clause 2.1 and in Table 2-6 row 2-6.1, ‘120,000 m3/day’ is deleted and ‘150,000 m3/day’ is
substituted.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-II:T2-6/2-6.1 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “Ref: 2-6.1 | Criterion: Average daily flow | Value: 120,000 | Unit: m³/day”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-II:T2-6/2-6.1 — Value
- uncertainty: none
- what depends on it: Predict a change only to row 2-6.1, column Value, retaining its Criterion and Unit.; Proposed A5 work: reconcile the hydraulic schedule and design calculations with the revised Clause 2.1.

### 4.1-peak: provision 4.1 — peak hourly flow reservation (page 1): annotate, confidence high
- quotation: “The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-II:T2-6/2-6.2 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “Ref: 2-6.2 | Criterion: Peak hourly flow (design) | Value: 7,500 | Unit: m³/h”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-II:T2-6/2-6.2 — Value and Unit
- uncertainty: none
- what depends on it: Retain this explicit reservation in the hydraulic design review; any comparison with the revised daily capacity needs a checked unit conversion.; No proportional increase to this row is predicted.

### 4.2: provision 4.2 (page 1): replace, confidence high
- quotation: “Consequentially, footnote 12 to Volume I Clause 8.5 is amended by deleting ‘80,000 m3/day’ and substituting
‘100,000 m3/day’. The requirement for two (2) reference plants and the ten (10) year look-back are unchanged.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-I:8.5#fn12 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “For the avoidance of doubt, a Bidder that does not evidence at least two (2) reference sewage treatment plants, each of nominal capacity not less than 80,000 m³/day and each having achieved commercial operation within the ten (10) years preceding the Proposal Due Date, shall be rejected without further evaluation.”
- deliverables affected: A1, A2, A3, A4, A5; rows/activities: VOL-I:8.5#fn12, VOL-I:9.5, VOL-IV:F4-B/nominal-treatment-capacity-m3-day
- uncertainty: none
- what depends on it: Review reference-project evidence and Form 4-B against the printed amended threshold, retaining the plant-count and look-back duration.; A3 rejection consequence remains the footnote's express words: “shall be rejected without further evaluation.”; Recompute the look-back boundary from the revised due date and review the dependency of ADD-01:Q5.; VOL-I:9.5 says “A separate Form 4-B shall be submitted for each reference project relied upon under Clause 8.5, accompanied by a client completion certificate. A reference project not evidenced by a completion certificate will be disregarded.”

### 4.3: provision 4.3 (page 1): replace, confidence medium
- quotation: “Volume I Clause 1.3 is amended correspondingly.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-I:1.3 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “The Project comprises a sewage treatment plant of nominal capacity one hundred and twenty thousand cubic metres per day (120,000 m³/day), associated inlet and conveyance works, sludge handling facilities, and a treated effluent transmission main of approximately eighteen (18) kilometres, all as more particularly described in Volume II.”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-I:1.3
- uncertainty: none: The target is explicit; the predicted edit is to the nominal-capacity expression corresponding to Section 4.1. Section 4.3 supplies no full replacement sentence.
- what depends on it: Review the capacity expressed in both words and numerals in the project description.; Keep the edit scoped to nominal capacity; the transmission-main length and associated works are not named for amendment.

### 5.1: provision 5.1 (page 1): replace, confidence high
- quotation: “In Volume I Clause 6.4, ‘SAR 4,500,000 (four million five hundred thousand Saudi Riyals)’ is deleted and ‘SAR
5,600,000 (five million six hundred thousand Saudi Riyals)’ is substituted.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-I:6.4 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “The Bid Bond shall be in the amount of SAR 4,500,000 (four million five hundred thousand Saudi Riyals), shall be unconditional and payable on first written demand, and shall be issued by a bank licensed to operate in the Kingdom holding a long-term credit rating of not lower than A- from a recognised international rating agency.”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-I:6.4, ADD-02:Q8
- uncertainty: none
- what depends on it: Proposed A5 work: revise the bank instruction and bond-document review for the printed replacement amount.; Review the fixed-amount clarification in ADD-02:Q8 and bond confirmations in submission documentation.; The issuing-bank and rating requirements are outside this amount substitution.

### 5.2-bond: provision 5.2 — Bid Bond validity (page 1): replace, confidence high
- quotation: “In Volume I Clause 6.3, ‘one hundred and eighty (180) days’ is deleted and ‘two hundred and ten (210) days’ is
substituted.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-I:6.3 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “Envelope A shall be accompanied by a Bid Bond which shall remain valid for one hundred and eighty (180) days from the Proposal Due Date and shall be extended on demand where the Authority extends the period of Proposal validity.”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-I:6.3
- uncertainty: none
- what depends on it: Recompute bond expiry using both the revised due date and the printed replacement duration.; Proposed A5 work: revise bank issuance instructions, expiry verification and any subsequent extension checks.

### 5.2-proposal: provision 5.2 — Proposal validity reservation (page 1): annotate, confidence high
- quotation: “The Proposal validity period in Clause 7.1 is unchanged.” (verbatim on page 1 of the addendum's text layer)
- target guess: VOL-I:7.1 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “Each Proposal shall remain open for acceptance for one hundred and fifty (150) days from the Proposal Due Date.”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-I:7.1
- uncertainty: none
- what depends on it: Retain the Proposal-validity duration while recomputing its expiry from the amended due date.; Link this reservation to clarification response 18; do not substitute the bond duration into Proposal validity.

### 6.1: provision 6.1 — new Volume I Clause 11.6 (page 2): insert, confidence medium
- quotation: “‘11.6  Where, on completion of the combined evaluation, two or more Proposals are within two per cent (2%) of
one another, the Authority may apply such further criteria as it considers appropriate to determine the
Preferred Bidder, and its determination shall be final.’” (verbatim on page 2 of the addendum's text layer)
- target guess: none (no target guessed)
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-I:H:S11, VOL-I:11.2, VOL-I:11.4
- uncertainty: genuine ambiguity: ambiguous: “within two per cent (2%) of one another” can describe a relative percentage difference between scores or a difference measured in percentage points on a scoring scale. The comparator and grouping method for multiple Proposals are not specified. No existing VOL-I:11.6 was returned at ADD-02, consistent with an insertion.
- what depends on it: Record a proposed new evaluation provision and a DRAFT clarification for Legal and Bid management.; Preserve the ADD-02 effective weighting in VOL-I:11.2: “Proposals reaching stage (iii) will be ranked on a combined score calculated on a weighting of sixty-five per cent (65%) technical and thirty-five per cent (35%) commercial.”; Review evaluation planning and its relationship to the existing Best and Final Offer discretion; infer no new rejection or disqualification consequence.; No score comparison or Preferred Bidder outcome is calculated or selected.

### 7.1: provision 7.1 (page 2): replace, confidence high
- quotation: “In Volume II Table 2-4, the limit for Total Phosphorus (TP) is amended from the value shown to 0.5 mg/l, assessed
on the same basis.” (verbatim on page 2 of the addendum's text layer)
- target guess: VOL-II:T2-4/TP (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “Parameter: Total Phosphorus (TP) | Unit: mg/l | Limit: 1 | Basis of assessment: 30-day rolling average”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-II:T2-4/TP — Limit
- uncertainty: none
- what depends on it: Predict replacement only of the TP row's Limit cell, retaining Unit “mg/l” and Basis of assessment “30-day rolling average”.; The inspected TP row and cell crops show the existing limit and basis; the full table image shows its headings, maxima qualifier and note.; Review treatment design and reliability testing under VOL-II:3.1 and VOL-II:7.2.; Review contract dependencies: VOL-V:31.1 includes “the treated effluent fails any parameter in Volume II Table 2-4”; VOL-V:29.3 states “no availability deduction shall apply to a parameter listed in Table 2-4 as assessed on a rolling average basis.” These are contract-payment dependencies, not an invented A3 bid-out consequence.; Revisit the TP-specific dependency of ADD-02:5.1's unchanged-other-parameters annotation; preserve the ADD-02 effective TN amendment.

### Q15: provision 8 — response 15 (page 2): annotate, confidence high
- quotation: “Following the capacity increase, will the Authority extend
the construction period in Volume V Clause 12.1?
No. The period of thirty-six (36) months is unchanged.” (verbatim on page 2 of the addendum's text layer)
- target guess: VOL-V:12.1 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “The Project Company shall achieve PCOD within thirty-six (36) months of the Notice to Proceed (the Scheduled PCOD).”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-V:12.1
- uncertainty: none
- what depends on it: Record the response against the construction-period requirement and clarification register without deciding that any existing question is resolved.; Proposed A5 work: review the construction programme for the revised capacity within the retained duration; do not shift its Notice to Proceed anchor to the Proposal Due Date.

### Q16: provision 8 — response 16 (page 2): annotate, confidence high
- quotation: “Does the increase in capacity change the design influent
characteristics in Table 2-2?
No. Table 2-2 is unchanged.” (verbatim on page 2 of the addendum's text layer)
- target guess: VOL-II:T2-2 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “Table 2-2 — Design influent characteristics — Parameter | Unit | Average | Peak (design)”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-II:T2-2/bod5, VOL-II:T2-2/cod, VOL-II:T2-2/total-suspended-solids, VOL-II:T2-2/total-nitrogen, VOL-II:T2-2/total-phosphorus, VOL-II:T2-2/temperature
- uncertainty: none
- what depends on it: Retain every retrieved Table 2-2 row, including its units and Average and Peak (design) columns.; Proposed A5 work: check process sizing using the increased flow and unchanged influent characteristics; the response does not state that derived mass loads remain unchanged.; Link to VOL-II:2.1, VOL-II:3.1 and the clarification register.

### Q17: provision 8 — response 17 (page 2): annotate, confidence medium
- quotation: “Will the Availability Payment be adjusted for the increased
capacity?
Bidders shall price the Project as amended by this Addendum.” (verbatim on page 2 of the addendum's text layer)
- target guess: VOL-IV:F4-F/para1 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “We confirm that the Availability Payment stated above is unconditional, is not subject to any qualification, and has been derived from the Financial Model submitted with this Form.”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-IV:F4-F/para1, VOL-IV:F4-F/availability-payment-sar-per-annum-year-1-of-operations, VOL-I:10.1
- uncertainty: none: The response names no replacement payment clause. Form 4-F is a guessed implementation dependency for the pricing instruction, not a proposed textual amendment to its declaration.
- what depends on it: Proposed A5 work: revise the Financial Model and Form 4-F pricing inputs for the amended capacity and effluent requirement.; Record the instruction in the clarification register without treating it as a stated payment-adjustment formula or a decision that the bidder's question is resolved.; No price, compensation entitlement or bidder financing fact is inferred.

### Q18: provision 8 — response 18 (page 2): annotate, confidence high
- quotation: “Please confirm the Proposal validity period following this
Addendum.
One hundred and fifty (150) days from the Proposal Due Date as
amended.” (verbatim on page 2 of the addendum's text layer)
- target guess: VOL-I:7.1 (a unit of the ADD-02 workspace (the guess itself is unchecked)); its words at the previous stage: “Each Proposal shall remain open for acceptance for one hundred and fifty (150) days from the Proposal Due Date.”
- deliverables affected: A1, A2, A4, A5; rows/activities: VOL-I:7.1
- uncertainty: none
- what depends on it: Link the response to Sections 2.1, 2.2 and 5.2 and to the Proposal-validity date rule.; Review validity confirmations and programme milestones after calculation; the response itself supplies no computed expiry date.

## Questions for a person (answer them on the panel's Quick review page)

- **Q-evaluation-method** For the proposed Clause 11.6, should a DRAFT clarification seek the score metric, denominator, rounding rule and comparison method intended by “within two per cent (2%) of one another”, together with the further criteria and their relationship to the existing evaluation provisions? (decision owner: Legal)
  - page 2: “two or more Proposals are within two per cent (2%) of
one another” (verbatim on page 2 of the addendum's text layer)
  - page 2: “the Authority may apply such further criteria as it considers appropriate” (verbatim on page 2 of the addendum's text layer)
  - page 5, VOL-I:11.2: “Proposals reaching stage (iii) will be ranked on a combined score calculated on a weighting of sixty-five per cent (65%) technical and thirty-five per cent (35%) commercial.” (quoted from VOL-I:11.2 (a unit of the ADD-02 workspace; words unchecked))
- **Q-form-date** How should the bidder present the due-date field in the reissued Form 4-A when preparing the ADD-03 submission, and is an Authority clarification or corrected form needed? (decision owner: Document control)
  - page 1: “Volume I Clause 6.1 is amended by deleting ‘Thursday 26 November 2026’ and substituting ‘Thursday 10
December 2026’, 14:00 Riyadh time.” (verbatim on page 1 of the addendum's text layer)
  - page 3, ADD-01:AppA/proposal-due-date: “Proposal Due Date: 12 November 2026, 14:00 Riyadh time” (quoted from ADD-01:AppA/proposal-due-date (a unit of the ADD-02 workspace; words unchecked))
  - page 3, ADD-01:AppA/para1: “Form 4-A is reissued below to add the acknowledgement of Addenda at paragraph 1. Bidders shall use this version.” (quoted from ADD-01:AppA/para1 (a unit of the ADD-02 workspace; words unchecked))
- **Q-pricing-response** Does Commercial require a further DRAFT clarification on payment adjustment after response 17, or will it proceed with preparing the amended bid price while leaving any adjustment entitlement undetermined? (decision owner: Commercial)
  - page 2: “Will the Availability Payment be adjusted for the increased
capacity?
Bidders shall price the Project as amended by this Addendum.” (verbatim on page 2 of the addendum's text layer)
  - page 9, VOL-IV:F4-F/para1: “We confirm that the Availability Payment stated above is unconditional, is not subject to any qualification, and has been derived from the Financial Model submitted with this Form.” (quoted from VOL-IV:F4-F/para1 (a unit of the ADD-02 workspace; words unchecked))

## Unverified calculations (unchecked until the workflow's tools and a person check them)

- **C-clarification-cutoff** Recompute the clarification cut-off from the amended Proposal Due Date.: the model's figure (UNVERIFIED): none given; why unverified: No calculation tool is offered in quick review. The workflow must apply the working-day rule and relevant holiday calendar; no date has been calculated here.
  - input, page 1: “substituting ‘Thursday 10
December 2026’, 14:00 Riyadh time.” (verbatim on page 1 of the addendum's text layer)
  - input, page 3: “Requests for clarification shall be submitted no later than ten (10) Working Days before the Proposal Due Date. Requests received after that time will not be answered.” (NOT FOUND on page 3 of the addendum's text layer: treat the quotation as unverified)
  - input, page 2: “Working Day means any day from Sunday to Thursday inclusive, other than a day declared a public holiday in the Kingdom. Where a period expressed in Working Days is to be counted backwards from a stated date, the stated date itself shall not be counted.” (NOT FOUND on page 2 of the addendum's text layer: treat the quotation as unverified)
- **C-bond-expiry** Recompute Bid Bond expiry using the amended anchor and duration.: the model's figure (UNVERIFIED): none given; why unverified: No calculation tool is offered. The ADD-02 quotation supplies the anchor relationship; ADD-03 supplies the replacement duration. An expiry date remains unchecked.
  - input, page 1: “substituting ‘Thursday 10
December 2026’, 14:00 Riyadh time.” (verbatim on page 1 of the addendum's text layer)
  - input, page 1: “‘two hundred and ten (210) days’ is
substituted.” (verbatim on page 1 of the addendum's text layer)
  - input, page 3: “Envelope A shall be accompanied by a Bid Bond which shall remain valid for one hundred and eighty (180) days from the Proposal Due Date and shall be extended on demand where the Authority extends the period of Proposal validity.” (NOT FOUND on page 3 of the addendum's text layer: treat the quotation as unverified)
- **C-proposal-expiry** Recompute Proposal-validity expiry while retaining its printed duration.: the model's figure (UNVERIFIED): none given; why unverified: No calculation tool is offered; no expiry date or date-counting convention is supplied by this briefing.
  - input, page 1: “substituting ‘Thursday 10
December 2026’, 14:00 Riyadh time.” (verbatim on page 1 of the addendum's text layer)
  - input, page 2: “One hundred and fifty (150) days from the Proposal Due Date as
amended.” (verbatim on page 2 of the addendum's text layer)
- **C-reference-window** Recompute the reference-project commercial-operation look-back boundary.: the model's figure (UNVERIFIED): none given; why unverified: No calculation tool is offered. The boundary and any project-specific eligibility check require workflow calculation and human review; no bidder reference facts were supplied.
  - input, page 1: “substituting ‘Thursday 10
December 2026’, 14:00 Riyadh time.” (verbatim on page 1 of the addendum's text layer)
  - input, page 4: “each having achieved commercial operation within the ten (10) years preceding the Proposal Due Date” (NOT FOUND on page 4 of the addendum's text layer: treat the quotation as unverified)
  - input, page 1: “The requirement for two (2) reference plants and the ten (10) year look-back are unchanged.” (verbatim on page 1 of the addendum's text layer)
- **C-capacity-dependent** Recompute expansion-space capacity and minimum reliability-run throughput dependent on nominal capacity.: the model's figure (UNVERIFIED): none given; why unverified: No calculation tool is offered; no derived capacity or throughput is calculated.
  - input, page 1: “‘120,000 m3/day’ is deleted and ‘150,000 m3/day’ is
substituted.” (verbatim on page 1 of the addendum's text layer)
  - input, page 2: “The Facility shall be designed to accommodate a future expansion of 50% of nominal capacity without demolition of permanent structures. Space provision only is required; no expansion works form part of the Works.” (NOT FOUND on page 2 of the addendum's text layer: treat the quotation as unverified)
  - input, page 4: “PCOD shall not be certified until the Facility has completed a continuous reliability run of thirty (30) days at not less than 90% of nominal capacity, during which every parameter in Table 2-4 has been met.” (NOT FOUND on page 4 of the addendum's text layer: treat the quotation as unverified)
- **C-hydraulic-comparison** Check the relationship between amended daily capacity and unchanged peak hourly design flow.: the model's figure (UNVERIFIED): none given; why unverified: The comparison requires a unit conversion and an approved calculation method unavailable in quick review. No conversion, ratio or hydraulic inconsistency is asserted.
  - input, page 1: “‘120,000 m3/day’ is deleted and ‘150,000 m3/day’ is
substituted.” (verbatim on page 1 of the addendum's text layer)
  - input, page 3: “Ref: 2-6.2 | Criterion: Peak hourly flow (design) | Value: 7,500 | Unit: m³/h” (NOT FOUND on page 3 of the addendum's text layer: treat the quotation as unverified)
  - input, page 1: “The peak hourly flow in Table 2-6 row 2-6.2 is unchanged.” (verbatim on page 1 of the addendum's text layer)
- **C-influent-loads** Review derived influent loads using amended capacity and unchanged Table 2-2 inputs; Total Phosphorus is one identified dependency.: the model's figure (UNVERIFIED): none given; why unverified: No calculation tool or approved load-conversion method is offered. Selection of the applicable design inputs and derived loads remains for the workflow and Technical.
  - input, page 1: “‘120,000 m3/day’ is deleted and ‘150,000 m3/day’ is
substituted.” (verbatim on page 1 of the addendum's text layer)
  - input, page 2: “Parameter: Total Phosphorus | Unit: mg/l | Average: 9 | Peak (design): 14” (NOT FOUND on page 2 of the addendum's text layer: treat the quotation as unverified)
  - input, page 2: “No. Table 2-2 is unchanged.” (verbatim on page 2 of the addendum's text layer)
- **C-evaluation-proximity** Determine the method before evaluating the new score-proximity trigger.: the model's figure (UNVERIFIED): none given; why unverified: ambiguous: relative percentage and percentage-point readings remain open. A person must determine the intended method before workflow calculation; no Proposal scores were supplied.
  - input, page 2: “two or more Proposals are within two per cent (2%) of
one another” (verbatim on page 2 of the addendum's text layer)
  - input, page 5: “Proposals reaching stage (iii) will be ranked on a combined score calculated on a weighting of sixty-five per cent (65%) technical and thirty-five per cent (35%) commercial.” (NOT FOUND on page 5 of the addendum's text layer: treat the quotation as unverified)

## Not read

(nothing reported)

## The model's own account of what it read

PRELIMINARY AI BRIEFING — unverified: not a decision, not a validation; calculations and interpretations unchecked. Read both supplied ADD-03 pages, including the cover, recitals, all operative provisions and clarification rows 15–18. The packet lists no attachments, image regions or image pages requiring get_addendum_page. Retrieved target evidence at ADD-02, keeping effective text distinct from text as issued. Inspected the Table 2-4 TP row, Limit and Basis cell crops, and the full table crop and native image. These show TP, mg/l, the printed limit 1, the 30-day rolling average, the column headings, maxima qualifier and Note 1. The original image's TN value was not substituted for the separately retrieved ADD-02 effective TN value. Retrieved all members of Tables 2-2 and 2-6 and Form 4-G, including its undertaking rows and signature fields. No unread addendum material was identified. New Clause 11.6 has no prior-stage target, as expected for an insertion. Named programme work is proposed follow-on work, not an assertion that corresponding activity IDs already exist; no activity durations or bidder facts are invented. Citations with unit_id identify pack evidence and use that source's page; citations without unit_id refer to ADD-03 pages. No main-workflow proposals were requested, no calculation was performed, and no question, interpretation or amendment was decided.
