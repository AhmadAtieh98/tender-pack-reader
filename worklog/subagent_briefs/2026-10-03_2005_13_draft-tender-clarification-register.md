# Subagent brief 13: Draft tender clarification register

Launched 2026-10-03 20:05:15 UTC; model option requested: `(default)`; subagent type: `general-purpose`.
The text below is the prompt exactly as sent by the coordinator (exported from the session transcript on 4 Oct 2026, session 11).

---

You are helping prepare a bid on a FICTIONAL tender (an internal assessment pack; confidential: do not publish, upload, search the web for, or send anything). Your job: research and DRAFT a tender clarification register. You write ONE output file and nothing else; you do not edit the repository.

## Where things are (repository /home/user/tender-pack-reader, Python venv at .venv/bin/python)
- The tender pack as text: `build/units.json` -> {"units": [...]}, each unit has `unit_id` (e.g. "VOL-I:6.5", "ADD-02:Q11", "VOL-II:T2-2/bod5"), `doc`, `pages` (list), `text`, and for table rows `cells`. Documents: VOL-I (Instructions to Bidders), VOL-II (Technical Requirements), VOL-IV (Form Sheets), VOL-V (Draft Project Agreement, an extract), ADD-01 (Addendum No. 1, issued 8 Oct 2026), ADD-02 (Addendum No. 2, issued 22 Oct 2026). Addendum clarification answers are units like ADD-01:Q1..Q6 and ADD-02:Q7..Q14 (each includes the question and the Authority response). The original PDFs are in `sources/candidate_pack/` if you need to look at layout.
- Two image units were read by hand and confirmed by the owner: Table 2-4 effluent limits (VOL-II:T2-4/* units, including the qualifier "all values are maxima; compliance assessed as a 30-day rolling average unless stated") and Form 4-C in Arabic (VOL-IV:F4-C/image/* units, with translations).
- Already-recorded open issues (proposed wording, useful context, not authoritative): `curation/register/issues.yaml` and `curation/register/issues/*.yaml`. Register rows (proposed interpretations): `curation/register/rows.yaml`, `curation/register/rows/*.yaml`.
- Correspondence: `sources/correspondence/2026-10-02_reply_from_hiring.md` — the hiring team confirmed the assessment pack is complete as provided.
- Key dates: the Proposal Due Date is 26 Nov 2026, 14:00 Riyadh time (VOL-I 6.1 as amended by ADD-01 2.1). The VOL-I 5.2 clarification cut-off (ten Working Days before the PDD; Working Days Sun-Thu, VOL-I 2.4, stated date not counted) is 12 Nov 2026 on the planning reading.

## The owner's instructions for this register (follow them exactly)
"Use this register only for discrepancies, ambiguities and missing information in the tender volumes and addenda. Draft the clarification questions and record their impact. Do not send anything to the hiring team or anyone else. Keep software defects and assessment administration out of this register.
Use these interim approaches:
* Form 4-A: use the reissued version as the baseline. Flag its stale printed date and omitted fields. The permitted correction method remains unresolved. Don't silently merge forms. Independent Volume-I obligations still apply.
* Envelope B: retain and prepare the model-auditor opinion and financing-assumptions schedule. Flag the question of how to package them alongside §10.1's restricted contents.
* Form 4-B: retain the conflict between historical contract values and Envelope A's commercial-information prohibition. Don't invent an exemption or automatically delete or relocate the field.
For each genuine unresolved matter, record the volume, clause, page, discrepancy or gap, practical impact, proposed question, interim handling and response status. Follow the fictional tender's clarification requirements in VOL-I 3.3 and 5 when drafting.
Check concession alignment, DWF/design flows, permit/table interpretation, Form 4-G 'no' answers, scoring, USB packaging, filenames, missing technical/contractual references, bond coverage, LCC evidence, page limits, counting conventions, repeated breaches, guarantee wording and handback. Include only questions that remain after checking the clauses, precedence and existing answers.
In ADD-02's clarification table, question 7 concerns the concession term and directs bidders to precedence. Question 11 concerns design flows, and question 13 concerns the financial-close timetable. Preserve those answers and distinguish any remaining follow-up from what has already been settled.
Also keep these distinctions: average and peak flows are not inherently contradictory; copy quantities are per proposal; Excel is required; and Form 4-G adds valid obligations. Don't manufacture questions about settled points.
The hiring email confirms that the assessment pack is complete as provided. Flag unavailable referenced material and its impact, without making access to it a prerequisite for completion. Unknown answers remain unknown."
Also: the Form 4-C Arabic declaration 4 says any incorrect statement "leads to the exclusion of the proposal" (استبعاد العرض); the English volumes never use "exclusion". Do not equate it with rejection/disqualification/non-responsiveness; decide whether a clarification question is warranted and if so draft it (suggested id CQ-F4C-EXCLUSION). The Environmental Permit is not in the pack; its precedence over the Table 2-4 reproduction is stated in the VOL-II p3 reproduction preamble (unit VOL-II:T2-4-heading/para1). The owner confirmed only that location, not the Permit's contents or compliance.

## Method
1. Read the relevant clauses for EVERY topic in the check list above (plus Form 4-A, Envelope B, Form 4-B, Form 4-C exclusion, Volume III / Drawing 03-C-114, ESIA/geotechnical report, VOL-V missing schedules). Apply VOL-I 3.2 precedence (Addenda, later prevailing; then VOL-I; VOL-V; VOL-II; VOL-IV; VOL-III) and the existing ADD-01/ADD-02 answers before deciding a question remains. A conflict that precedence plainly resolves, or that an answer already settles, is NOT a question (record it under checked_no_question with why). A follow-up is allowed only for what the answer leaves open, stated precisely.
2. Every quotation you rely on must be verbatim from a unit's `text` (whitespace-normalised). Verify each one with a short Python check against build/units.json before you finish; fix or drop any that fail. Give page numbers from the unit's `pages`.
3. Draft each question as a bidder would submit it under VOL-I 5.1: it must cite the Volume, Clause and page it relates to, be neutral, ask one thing (or tightly linked things), and not reveal bid strategy. Note that VOL-I 5.2 bars answers to requests after the cut-off and 5.3 says only Addenda bind.
4. Interim handling = what the bid team does now without an answer (conservative, never inventing an answer, never assuming the Authority's response).

## Output: write exactly one YAML file
`/tmp/claude-0/-home-user-tender-pack-reader/51ac768d-d630-5aa7-8c52-469fdeb8335c/scratchpad/s08/agents/clarifications.yaml` with this shape:
```yaml
cut_off: {rule: "VOL-I 5.2", date: "2026-11-12", note: "..."}
clarifications:
  - id: CQ-<SHORT-NAME>
    topic: "<check-list topic or other>"
    kind: discrepancy | ambiguity | missing_information
    volume: "Volume I"           # as the question must cite it
    clause: "6.5"
    page: 3
    units: ["VOL-I:6.5", ...]
    sources: [{unit: "VOL-I:6.5", page: 3, words: "<verbatim>"}, ...]
    gap: "<the discrepancy, ambiguity or missing information, precisely>"
    already_settled: "<what earlier answers/precedence settle, with the answer id; empty string if nothing>"
    practical_impact: "<what it affects in the bid: which deliverable, envelope, risk, deadline>"
    proposed_question: "Volume I, Clause 6.5, page 3: ...?"
    interim_handling: "<what we do meanwhile>"
    decision_owner: Legal | Technical | Commercial | Bid manager
    response_status: "draft, not sent"
    linked_issues: [I-...]       # existing issue ids where they match, else []
checked_no_question:
  - topic: "<topic>"
    finding: "<what was checked and why no question remains (e.g. settled by ADD-02 Q11: ...; precedence VOL-I 3.2 resolves ...)>"
    sources: [{unit, page, words}]
unavailable_material:
  - item: "<e.g. Volume III (Drawings); Drawing 03-C-114>"
    referenced_in: [{unit, page, words}]
    impact: "<...>"
    handling: "flagged; not a prerequisite for completing the bid documents; <what we do>"
```
Order clarifications by practical importance. Keep each field concise (one to three sentences). Expect roughly 8-20 genuine questions; do not pad. Then reply with a short summary (counts, the ids and one line each, any topic you were unsure about). Do not modify any file in the repository; do not commit; do not mention AI model names in the YAML.
