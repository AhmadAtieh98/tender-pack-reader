# Analysis checklist (repeated in the task packet's `instructions`, one line each)

- Every provision is accounted for by an op, a disposition or an escalation.
- Cite exact words (verbatim quotations with unit id, document and page).
- Say 'insufficient evidence' (escalate, or a disposition 'unresolved' with the reason) rather than complete a plausible answer.
- Facts, assumptions and interpretations are separate statements; never merge them.
- Unknown structures and unsupported change types are escalated, never turned into guessed operations.
- The reference below is pattern drafter output, unverified: check it against the evidence before using any of it.
- Read targets as they stand before this addendum: get_unit(unit_id, stage=<previous_stage>); quote that text.
- A no_effect disposition on words that amend, oblige or except never verifies: a printed change needs its op; otherwise quote, in the reason, the words that show it changes nothing (a person confirms it).
- A free-standing provision (an obligation of the addendum's own that amends no volume unit) is answered by a row_new whose primary unit is that provision's own unit id (the register holds rows on addendum units), introduced at this addendum, with its consequence quoted; it is never escalated for want of a cited unit.
- Every payload follows its full schema in `payload_schemas` (a row_new's `row` is a register.Row: `scope` a list, `discipline`, `confidence` and `confidence_reason` given, a `consequence` an object or "none_stated"); check items with validate_proposal.
- A fact quotes its evidence verbatim (a fact with empty evidence is refused); dependencies name units, rows, ops or ids of this set's items and statements, never an issue or a question for a change, and never in a cycle.
