# Blind-07 regression (session 14): the run against the open answer key (ADD-03), before and after

**Synthetic, not tender content.** This is a **regression on an open key, scored after the run**. The key of blind-07 (`../SEALED/expected_findings.yaml`, `../SEALED/author_notes.md`) has been open since session 13, and the session-14 fixes were written with the session-13 scorer's report (`../COMPARISON.md`) in hand. A better result here shows that the fixes work on this addendum. It is not a blind measure of the workflow.

- **Scorer:** a separate agent that neither wrote the addendum nor built the tool. Model **Opus 5.5 (`claude-opus-5-5`)**; the runtime shows a reasoning-effort setting of **40**.
- **Elapsed:** scoring started 18:51:58 UTC and ended 19:14:11 UTC (**22 min 13 s**).
- **What I ran:** only `.venv/bin/python scripts/bench_workflow.py --from-run rehearsals/blind-07/regression-s14` (18:53:01 UTC), the same command on the live run folder (identical output apart from the folder line), and read-only scripts in my scratch folder. I changed nothing else. I ran no `tenderpack ai` command and no git write, and I approved nothing.
- **Before** means the session-13 run scored in `../COMPARISON.md` (run `ADD-03-run-host-20261006T201359Z-2503`, attempt 4). **After** means this run, `ADD-03-run-host-20261007T161946Z-e884` (`run.id`).

Paths are relative to `rehearsals/blind-07/regression-s14/` unless they start with `../`. L means line. Short names:

| Short name | File |
|---|---|
| `pkt` | `review/index.md` (the review packet, 1,555 lines) |
| `P` | the combined analysis set, `ai/ADD-03-run-host-20261007T161946Z-e884-combined/proposals.yaml` in the **live** run folder (`…/s14/pkg/reg07b/unzipped/LAMAR-PPP-R2-INTERVIEW_a918d5e+wt_20261007T1619Z/staging/ai/runs/ADD-03-run-host-20261007T161946Z-e884/`). It holds 80 analysis items and 12,218 lines. **It is not in this copy:** there is no `proposals/` folder here |
| `DS` | `downstream/proposals.yaml` (78 downstream items, 44 tasks) |
| `ops` | `candidate-curation/amendments/ADD-03.yaml` (the candidate op file) |
| `iss` | `candidate-curation/register/issues/ADD-03-ai.yaml` (the 23 promoted ADD-03 issues) |
| `rd` | `candidate-curation/readings/ADD-03-p3-r1.yaml` (the image reading) |
| `a1` | `out-candidate/a1/a1.csv` (physical lines) |
| `a3c` | `out-candidate/a3/a3_candidate.md` |
| `a5m`, `a5p`, `a5mar` | `out-candidate/a5/candidate/milestones.csv`, `programme.csv`, `marshalling.csv` |
| `a2cov` | `out-candidate/a2/a2_cover_summary_check.csv` |
| `ckpt`, `log` | `checkpoint.json`, `log.jsonl` (byte-identical to the live run folder's, checked with `cmp`) |
| `jobs/<id>` | the package's panel job folders, `…/staging/panel/jobs/<id>/` (`output.log`, `job.json`) |
| `bench` | the output of the bench command above |

## What was run and when

### Records and checks

- **Code identity:** all three segments ran content `64dbc541…` over 99 files with policy `02236955…`. The records are "run started", "resumed on the same code" twice, and `"differ": false` (`ckpt` L8489, L8517, L8545, L8549).
- **Models:** the host and the critic were pinned to `claude-opus-5-5`, and every host session reported `claude-opus-5-5` (`pkt` L7; `ckpt` `host_usage`).
  - The run-level "reported" field reads `None` (`pkt` L7).
  - The session-13 run's sessions reported **claude-sonnet-5-5** (`../COMPARISON.md` §7). That model difference matters for the time comparison.
- **Byte checks:** `ckpt`, `log`, `promotion.json`, `batches/`, `downstream/` and `review/` in this copy are byte-identical to the live run folder's (`cmp`, `diff -rq`).
- **Human approval:** none. The record reads "nothing approved, accepted, rejected or sent" (`ckpt` `approval`; `pkt` L17).

### Timeline (UTC)

| Time | Event | Source |
|---|---|---|
| 16:19:43 | Package `reg07b` and its panel started | `clock.txt` L1–2 |
| 16:19:45 | The PDF uploaded through the panel's *New addendum* form, route host. Run `…161946Z-e884`, job pid 27238 | `clock.txt` L3–4 |
| 16:20:11–16:24:14 | The reading session (223.3 s) and re-ingest. 57 provisions, 6 analysis batches | `log` L3–9 |
| 16:24:35 | analysis-001 and -002 **deferred** by the workflow's own 429 handling: "You've hit your session limit · resets 5:40pm (UTC)" is 4,527 s away, "beyond 300 s". analysis-003 and -004 had been "asked ahead" at 16:24:34–35, but no host session was ever started for them (no session folder) | `log` L10–17; `run.log` L10–11 |
| about 16:30 | **The container was reclaimed** (work log E170) and the job died with no further output. Its `job.json` reads "interrupted", finished null | `jobs/20261007T161946Z-ai-run-bbe08f/job.json`; `../../../worklog/2026-10-07_session-14_finalisation.md` L89 |
| 17:43:17 / 17:43:22 | Panel restarted; **Resume 1** from the panel. The checkpoint's `status_before` is "running" | `clock.txt` L5–6; `ckpt` L8377 |
| 17:43:31–18:12:09 | Analysis, 6 of 6 batches. analysis-002 and -004 were taken from staged submissions ("reused after revalidation") made at 17:49:31 and 18:00:38, **after** the resume | `jobs/20261007T174322Z-ai-resume-b7f5d3/output.log` L1–18; `ckpt` L8398, L8406 |
| 18:12:19–about 18:24 | Downstream attempt 1. Two sessions started at 18:12:28 and 18:12:29. The **container was reclaimed again** at about 18:24 (E170). The two session folders hold only `log.jsonl`, `mcp.json` and `prompt.txt` | `log` L45–47; `ai/ADD-03-hostsession-20261007T181228Z-5fc3`, `…181229Z-3051` |
| 18:26:46 / 18:26:50 | Panel restarted; **Resume 2**. `status_before` is "running" | `clock.txt` L7–8; `ckpt` L8416 |
| 18:27:04–18:47:02 | Downstream asked again from scratch (4 batches, 44 tasks). One repair re-ask (downstream-002) | `log` L49–62; `pkt` L1298 |
| 18:47:02–18:50:27 | Validation, critic, promotion, check-register, outputs, diff, packet | `log` L63–78 |
| 18:50:29 | End: the resume job finished, exit 0, status **partial** | `clock.txt` L9; `jobs/20261007T182650Z-ai-resume-5d30bf/job.json` |

**The planned interruption was not performed.** That was a SIGTERM right after an analysis submission is recorded, so that the resume reuses it. `clock.txt` has no SIGTERM line, and `ckpt` has no `interrupted` event. The run instead had two unplanned stops, both container reclaims (SIGKILL-like: no handler ran).

### Record slips (the rehearsal's records, not the tool)

1. **The copy lacks `proposals/`**, which the brief lists. The combined analysis set exists only in the live run folder (`P`).
2. **`run.log` lacks Resume 1's job log.** It holds the run job (L1–11) and Resume 2's job (L13–120). Resume 1's 19 lines (17:43–18:12, the whole analysis phase) are only in `jobs/20261007T174322Z-ai-resume-b7f5d3/output.log`.
3. **`clock.txt` records neither kill.** It records only the resumes and their reasons.
4. **The work log says two things the records contradict.** It says the steps' total of 57.0 min "includes the limit's dead time and the two kills" (worklog L63). It does not (§7). It also says "analysis-003 running when the container restarted" (worklog L61). No analysis-003 session existed before 17:49:45: it was only "asked ahead" (`log` L12).
5. **The packet's timing table was written before its own last step finished.** It reads "review 0.0 running" and a total of 3,411.1 s, against 3,417.0 s in `run.log` L51 (`pkt` L92–93). The session-13 packet had the same slip.

## Scoring method

This is the same method as `../COMPARISON.md`: N = 33 detection items (15 provisions, 5 answers, 3 cover errors, 4 image items, 6 secondary effects). Indirect effects, dates, marshalling, the A3 delta, missing evidence, DA1, HJ1 and the traps are scored in their own tables and not added to N.

The verdicts:

- **Hit:** the outputs state the effect correctly.
- **Partial:** the effect is detected but incomplete, wrongly targeted, or left unresolved or escalated where the key expects a definite change.
- **Missed:** absent, or present only in a form the key contradicts.

How the rules apply by item class:

- **Provisions and answers:** a hit needs the right effect in a **promoted** item, or an escalation where the key expects one.
- **Cover errors, image items and secondary or indirect effects:** detection anywhere counts. They score partial when the run keeps open a reading the key rules out.

## 1. Detection, before and after

**Count (N = 33): before 11 hit, 17 partial, 5 missed. After 18 hit, 14 partial, 1 missed.**

| Group | Before H / P / M | After H / P / M |
|---|---|---|
| Provisions (15) | 5 / 10 / 0 | **10 / 5 / 0** |
| Answers (5) | 2 / 3 / 0 | **3 / 2 / 0** |
| Cover planted errors (3) | 1 / 1 / 1 | **2 / 1 / 0** |
| Arabic image: reading, AR1–AR3 (4) | 2 / 2 / 0 | 2 / 2 / 0 |
| Secondary undisclosed effects (6) | 1 / 1 / 4 | **1 / 4 / 1** |
| **Total (33)** | **11 / 17 / 5** | **18 / 14 / 1** |

| Scored separately | Before | After |
|---|---|---|
| Indirect effects (9) | 2 hit, 3 partial, 4 missed | 2 hit, 6 partial, 1 missed |
| Derived dates (7) | 7 right | 6 right, 1 partial (D2 no longer planned in A5) |
| Marshalling (7) | 2 / 4 / 1 | 4 / 3 / 0 |
| A3 delta (4) | 2 hit, 2 partial | 2 hit, 2 partial |
| Missing evidence (3) | 1 / 1 / 1 | 2 / 1 / 0 |
| DA1 / HJ1 | **missed** / hit | **hit\*** / hit |
| Traps (24) | 24 avoided as assertions; 4 borderline | 24 avoided as assertions; 6 borderline |
| False positives / false signals | 5 / 10 | 5 / 13 (section 4) |

\* DA1 is raised by a deterministic rule written in session 14 after the key was open (W4, "fires on blind-07's own reading file"). It appears only in the candidate A3 (`a3c` L231), not in the review packet (0 hits) and not in the candidate register.

### Provisions (15): before 5 / 10 / 0, after 10 / 5 / 0

| Key | Before | After | Evidence (after) |
|---|---|---|---|
| 1.1 recital | hit | **hit** | `no_effect` with "applied rule: ADD-03 1.1 … (applied, not decided)" (`ops` L272; `pkt` L197–201) |
| 1.2 interpretation (2.1 operates on 2.5M) | partial | **hit** | `no_effect`: "it governs how the Addendum's other provisions are read (applied in ADD-03/2.1, which reads VOL-V:36.2 at its ADD-02 effective text)" (`P` L1519–1530; `ops` L283). A keyword flag fires on "unless" (`pkt` L202ff) |
| 2.1 delta on the ADD-02 value | partial | **hit** | <ul><li>`adjust_value` promoted, evidence_verified. "SAR 2,500,000 -> **SAR 1,500,000** — SAR 2,500,000 - SAR 1,000,000 = SAR 1,500,000 … as amended by ADD-02/8.1" (`ops` L25–39; `pkt` L158, L212–216).</li><li>The row VOL-V-36.2-01 is flagged "UNRESOLVED: STALE at ADD-03" (`a1` L209). Its re-reading with 1,500,000 (DS-07) was held "conflicting" because the proposer also declared the cover issue (`DS` L1171).</li><li>The cover's 4.0M survives as a pricing reading (see E1 and M7)</li></ul> |
| 2.2 instruction (price on 1.5M) | partial | partial | <ul><li>`annotate … adds_obligation` promoted (`ops` L40).</li><li>No A1 row holds the obligation: DS-13 was held back ("issue references not among the promoted issues") and DS-22-ROW was refused as a duplicate id (`DS` L5587). check-register C46 says "no A1 row in force … holds" it (`pkt` L964).</li><li>The pricing basis is left open between 4.0M and 1.5M (`iss` L100)</li></ul> |
| 3.1 relocation | partial | partial | <ul><li>`relocate_unit VOL-II:8.5` promoted (`ops` L56–70). VOL-II-8.5-01/02 read "REPLACED (by VOL-V:42.3)" (`a1` L156–157).</li><li>**No A1 row in force carries 42.3.** DS-14/15 are invalid with "unknown anchor End of the concession period" and "… Transfer of the Facility" (`DS` L1818, L1963), and C46 fires on 3.1 (`pkt` L965).</li><li>The rank change is only "may change" (`DS` L691; `iss` L111). Form 4-E is not linked</li></ul> |
| 3.2 numbering | hit | **hit** | `no_effect`, evidence_verified, no keyword flag now (`pkt` L266–273). Its reason now rests on the relocation, not on a deletion |
| 3.3 repoint 42.1 | partial | **hit** | `replace_text VOL-V:42.1 "Volume II Clause 8.5" → "Clause 42.3"` promoted beside 3.4(a) on the same unit (`ops` L71; `pkt` L275–284) |
| 3.4 per-class Arabic schedule | partial | partial | <ul><li>3.4(a)'s `replace_text` is promoted (`ops` L87).</li><li>3.4(b)'s `insert_table` was refused: "unsupported: insert_table of a table read from an image whose number is printed in Arabic-Indic digits". It is escalated (`pkt` L113–114).</li><li>One conditional row, ADD-03-T42-1-01, carries the Arabic values r4 ٧ and r5 ٢٤ شهراً, "PENDING READING" (`a1` L39)</li></ul> |
| 3.5 the Arabic governs | partial | partial | <ul><li>Promoted `annotate` with `precedence: governs ADD-03:p3-image over ADD-03:T42-1, words: The Arabic text governs.` (`ops` L103–123).</li><li>It is validated **HUMAN DECISION PENDING** (`pkt` L316–320).</li><li>It is not applied: r4, r5, T42-1/4, T42-1/5 and note (4) stay UNRESOLVED (`pkt` L120–124)</li></ul> |
| 3.6 shall demonstrate | partial | **hit** | <ul><li>Row ADD-03-3.6-01 promoted: "none stated", assessment *scored* (`a1` L34). Criterion C is named in I-ADD03-T42-1 (`iss` L29).</li><li>The provision itself still reads "UNRESOLVED (accounted for, not applied)" (`pkt` L117, L333): new defect N3</li></ul> |
| 4.1 new 12.5 | hit | **hit** | <ul><li>`insert_unit` after VOL-V:12.4 (`ops` L124). Row ADD-03-4.1-01 (`a1` L33; its candidate status wrongly reads "(invalid)", N2). GBR Rev C flagged (ME1).</li><li>REL-AI-008 links it to VOL-V-12.1-01 and 18.3-01 (`pkt` L1410–1411)</li></ul> |
| 4.2 state ground conditions | partial | **hit** | Row ADD-03-4.2-01 promoted, "none stated", "The Geotechnical Baseline Report (Revision C …) is not in the pack" (`a1` L35) |
| 4.3 request + appointment | hit | **hit** | <ul><li>Row ADD-03-4.3-01 promoted with "lesser consequence: 'Requests made after the period … will not be accommodated.'" (`a1` L36).</li><li>The packet shows "-> **2026-11-23**" and "AMBIGUOUS: 2026-11-22 (event_day_excluded); 2026-11-19 (event_day_counted) … ESCALATED" (`pkt` L135–136). A5 has 23 Nov (`a5m` L9).</li><li>The request date is not planned (see Q19, D2)</li></ul> |
| 4.4 bounded disapplication | partial | partial | <ul><li>`annotate VOL-I:4.2 effect disapplies` with exactly the provision's scope is promoted (`ops` L144–160; `P` L7011–7040).</li><li>But VOL-I-4.2-01 reads "CONFIRMED (unchanged)" (`pkt` L442, L1386), "Disqualifiers (A3) — no change" (`pkt` L1429–1431), and the candidate A3 prints the unqualified blackout (`a3c` L53).</li><li>VOL-I 4.1 and Form 4-C appear in no item</li></ul> |

### Answers (5): before 2 / 3 / 0, after 3 / 2 / 0

| Key | Before | After | Evidence (after) |
|---|---|---|---|
| Q15 decoy | partial | **hit** | `annotate ADD-01:3.2 effect interprets` promoted (`ops` L161). No row is changed or made UNRESOLVED |
| Q16 confirming | partial | **hit** | `annotate VOL-II:9.3 effect confirms`. VOL-II-9.3-01 reads "CONFIRMED (unchanged)" (`ops` L177; `pkt` L452–458; `a1` L161) |
| Q17 changing | partial | partial | <ul><li>(a) and (b) are applied: Q17(a) `interprets` 10.1/10.6; Q17(b) `adds_obligation` "minimum annual debt service cover ratio"; row ADD-03-Q17-01 "forms part of Form 4-F and shall be attached to it in Envelope B" (`ops` L192–224; `a1` L37).</li><li>(c) is hedged again: I-ADD03-Q17-ENV "Reading 2: Clause 6.2 applies only to the extent the schedule contains price, rate or other commercial information" (`iss` L41).</li><li>I-VOL-I-ENV-B is kept open on 10.1/10.6 (`a1` L75, L82)</li></ul> |
| Q18 human judgment | hit | hit | <ul><li>`annotate VOL-I:3.2 interprets`, HUMAN DECISION PENDING.</li><li>I-ADD-03-Q18-ISSUE-ANA lists "Reading 1: VOL-V:40.2 prevails" and Reading 2, and chooses none (`iss` L331; `pkt` L503–518).</li><li>No winner is recorded anywhere</li></ul> |
| Q19 confirming of 4.3 | hit | **partial (regressed)** | <ul><li>`annotate ADD-03:4.3 interprets` promoted (`ops` L241).</li><li>A5 no longer plans 19 Nov. The request milestone `ADD03-4.3-request` has "event-dependent (no date: unresolved)" (`a5m` L16). The new `core-inspection-request` activity has a latest start of **2026-10-28**, before the addendum was issued, and reads "INFEASIBLE by 14 WD" (`a5p` L10).</li><li>The 19 Nov plan survives only in unpromoted analysis text ("Plan to request by Thursday 19 November 2026 (conservative reading)", the 4.3/q-count clarification, `pkt` L404ff)</li></ul> |

### The cover's planted errors (3): before 1 / 1 / 1, after 2 / 1 / 0

| Key | Before | After | Evidence (after) |
|---|---|---|---|
| E1 stale-base arithmetic | partial | partial | <ul><li>C28 now names the mechanism: "figure differs … reduced by SAR 1,000,000 gives SAR 1,500,000 (arithmetic for a person to check); SAR 4,000,000 is the earlier figure 'SAR 5,000,000' reduced by SAR 1,000,000" (`pkt` L1350; `a2cov` L11). I-ADD03-COVER-DIFF: "The cover summarises and does not amend" (`iss` L88).</li><li>**But two promoted issues keep the cover's figure as a live pricing reading.** I-ADD03-COL-THRESHOLD has "Reading 1: the cover's figure, 'to SAR 4,000,000' … Which provision governs is not decided here" (`iss` L100); I-ADD-03-COVER-PARA3-ISSUE-ANA does the same (`iss` L159)</li></ul> |
| E2 modality downgrade | **missed** | **hit** | C28 reads "modality differs: the summary says 'invites Bidders to describe …' (permission); ADD-03:3.6 says 'The Bidder shall demonstrate …' (obligation)" (`pkt` L1353; `a2cov` L14). It is also point (3) of I-ADD03-COVER-DIFF |
| E3 four classes | hit | hit | C28 reads "count differs … ADD-03:T42-1 has 5 row(s)" (`pkt` L1351). It is also point (2) of I-ADD03-COVER-DIFF |

### The Arabic image (4): 2 / 2 / 0 before and after

| Key | Before | After | Evidence (after) |
|---|---|---|---|
| Reading | hit | hit | <ul><li>`rd`: **34 of the key's 37 strings verbatim** (checked by script; before 35).</li><li>Three vowel-mark slips:<ul><li>مبيِّن for مبيَّن (as before);</li><li>تُقيِّم for تُقيَّم (new);</li><li>كلَّ for كلُّ (as before).</li></ul></li><li>Pending, with uncertainties declared (`pkt` L95–104). 223.3 s</li></ul> |
| AR1 row 4 = 7 | hit | hit | <ul><li>The conditional row carries r4 ٧ (`a1` L39).</li><li>The r4 disposition is unresolved: "Reading A: 7 years, under ADD-03:3.5 … Reading B: 5 years, as the translation states, with the Arabic being an error" (`pkt` L120). The rule is over-escalated (section 5)</li></ul> |
| AR2 row 5 = 24 months | partial | partial | I-ADD03-T42-1-MEMBRANE-UNIT keeps "Reading 2: 24 years, under the heading's unit" (`iss` L148) |
| AR3 note (4) has no force | partial | partial | <ul><li>Readings (a) no effect and (b) "amends Volume II Clause 2.2" are both kept (`iss` L230, L278).</li><li>The analysis "fact" S-F4 says "The English translation carries a note (4) that amends Volume II Clause 2.2" (`P` L147).</li><li>VOL-II-2.2-01/02 read "UNRESOLVED (value in question)" (`a1` L98–99)</li></ul> |

### Secondary undisclosed effects (6): before 1 / 1 / 4, after 1 / 4 / 1

| Key | Before | After | Evidence (after) |
|---|---|---|---|
| SU1 ADD-01 response 4 incomplete | missed | partial | <ul><li>I-ADD-03-4-1-ISSUE-Q4-ANA quotes ADD-01:Q4 against 12.5. Its Reading 1 is the key's.</li><li>Reading 2 adds "VOL-V:3.3 needs a conforming change", which the key rules out (trap 11).</li><li>"which governs … is a person's decision" (`iss` L295; `P` L6487–6510).</li><li>"Earlier answers to re-read" still lists only Q17 (`pkt` L126–128)</li></ul> |
| SU2 survey: Form 4-E deemed acceptance; rank (d)→(c) | partial | partial | <ul><li>The rank change is seen: "Its place in the Volume I Clause 3.2 order of precedence may change" (`DS` L691; `iss` L111).</li><li>The deemed acceptance of unlisted deviations is not stated</li></ul> |
| SU3 12.5 → Scheduled PCOD → 18.1 / 18.3 / 39.2; time and cost | missed | partial | <ul><li>DS-41-DEP-PCOD: "The Scheduled PCOD is defined in VOL-V 12.1, and VOL-V 18.1 and 18.3 measure delay damages and termination from it" (`DS` L6287–6320). Promoted as REL-AI-008 (`pkt` L1410–1411).</li><li>The 12.5 proviso is compared with 34.3 (`iss` L122).</li><li>39.2 is absent, and 3.3 is kept open (SU1)</li></ul> |
| SU4 row 4 (7 yrs) against VOL-II 2.2 → lifecycle capex, AP, 42.2 reserve | missed | partial | <ul><li>I-ADD-03-T42-1-LIFECYCLE-PRICING (conditional): "the residual lives for electrical, instrumentation and control equipment (Arabic ٧ vs English 5) … would set the late-term lifecycle replacement profile. That profile feeds the lifecycle plan … the Financial Model … and the Availability Payment" (`iss` L72).</li><li>VOL-II 2.2's 20-year design life, the forced replacement before handback and the 42.2 reserve are not named</li></ul> |
| SU5 VOL-I 4.1 not disapplied; Form 4-C decl. 5 | missed | missed | VOL-I 4.1 and Form 4-C appear in no item (`P`, `DS` and `pkt`: 0 hits) |
| SU6 Q17 removes the 10.1 conflict; DSCR | hit | hit | <ul><li>Q17(a)/(b) (`ops` L192–224).</li><li>EV-FIN-ASSUMPTIONS reads "incl. minimum annual DSCR assumed (part of Form 4-F)", and EV-FORM-4F "with the VOL-I 10.6 schedule attached" (`a5mar` L10, L25)</li></ul> |

### Scored separately

| Key | Before | After | Evidence (after) |
|---|---|---|---|
| IE1 (12.5 → ADD-01 r4 superseded in part) | missed | partial | as SU1 |
| IE2 (relocation → Form 4-E → rank) | partial | partial | as SU2 |
| IE3 (12.5 → PCOD → 18.1/18.3/39.2) | missed | partial | as SU3 |
| IE4 (row 4 → VOL-II 2.2 → lifecycle, FM, AP, 42.2) | missed | partial | as SU4 |
| IE5 (row 5 months vs VOL-II 3.2 membrane warranty) | missed | missed | VOL-II 3.2 is in no item; "24 years" is still a live reading |
| IE6 (2.1 + 1.2 → 1.5M → Form 4-F, Form 4-E) | partial | partial | <ul><li>The chain is complete: "CHANGED VOL-IV-F4E-01: VOL-V 36.2: '2,500,000' -> '1,500,000'" (`pkt` L1382), and REL-AI-001 links 36.2 to fin-model-build.</li><li>But the 4.0M pricing reading stays (`iss` L100)</li></ul> |
| IE7 (4.4 → A3 narrows → Form 4-C → 4.1) | partial | partial | The op is applied; A3 is not narrowed; Form 4-C and 4.1 are absent |
| IE8 (Q17 chain) | hit | hit | Q17 ops, row, EV items; 6.2 hedged |
| IE9 (4.3 forward count → 22/19 → Q19 → plan 19 Nov) | hit | hit (by detection) | <ul><li>`pkt` L136; the 4.3/q-count clarification plans 19 Nov.</li><li>A5 no longer plans it (Q19)</li></ul> |
| D0 cut-off 12 Nov; ADD-03 after it | right | right | "the clarification window closed on 2026-11-12 (VOL-I 5.2) … ADD-03 issued 2026-11-17" (`pkt` L111) |
| D1 appointment Mon 23 Nov | right | right | `pkt` L135; `a5m` L9 |
| D2 Sun 22 or Thu 19 Nov; rule unstated; plan 19 Nov | right | **partial (regressed)** | The packet keeps both dates and the unstated rule (`pkt` L136). A5's milestone has no date (`a5m` L16) |
| D3 12.5 notice: event-based | right | right | "not computed … its anchor 'encountering them' is an event" (`pkt` L137) |
| D4 letter 417/2026 of 15 Nov | right | right | `rd` date-ar and ref-ar; `pkt` L69–70 |
| D5 7 WD | right | right | "Working Days left … 7" (`pkt` L134) |
| Holidays none | right | right | "holidays none declared" (`pkt` L134) |
| M1 request / appointment | hit | **partial (regressed)** | 23 Nov is planned. The request activity's latest start is 28 Oct, INFEASIBLE (`a5p` L10). The request milestone is undated |
| M2 GBR Rev C | missed | **hit** | "NOT SUPPLIED: Geotechnical Baseline Report (Revision C)" (`pkt` L1427); I-ADD03-GBR (`iss` L15) |
| M3 Form 4-F + 10.6 schedule + DSCR, Envelope B | partial | **hit** | `a5mar` L10, L25, envelope B |
| M4 Technical Proposal: 3.6 + 4.2 | partial | **hit** | <ul><li>technical-proposal is renamed "… lifecycle plan against the Table 42-1 residual service lives; foundation ground conditions by reference to the Geotechnical Baseline Report" (`a5p`).</li><li>The activity is BLOCKED by the "unresolved" 3.6/4.2 (N3)</li></ul> |
| M5 Form 4-E review (12.5, 36.2, 42.1, 42.3; unlisted = accepted) | partial | partial | deviations-review and form-4e show REWORK through ADD-03-4.1-01, VOL-IV-F4E-01, 36.2-01 and 42.1-01/02 (`a5p`). 42.3 and the deemed acceptance are not named |
| M6 Form 4-A acknowledges ADD-03 | hit | hit | Rows ADD-03-cover-para3-01 and ADD-03-cover-01 (`a1` L32, L38); REWORK form-4a |
| M7 AP on 1.5M | partial | partial | 1.5M is computed, but the pricing basis is left open (`iss` L100). The 2.2 obligation has no row (C46) |
| A3 delta: 4.2 narrowed | partial | partial | Op applied; A3 and the diff show no change (`a3c` L53; `pkt` L1431) |
| A3 delta: 6.2 applies to the schedule | partial | partial | Hedged (`iss` L41) |
| A3 delta: Form 4-A / ADD-03 | hit | hit | M6 |
| A3 delta: no new A3 items | hit | hit | "A3 would gain 0 row(s)" (`pkt` L51); 3.6 is scored, 4.2 procedural, 4.3 a "lesser consequence" |
| ME1 GBR Rev C | partial | **hit** | <ul><li>"the pack does not supply it; only the ADD-03 provisions and ADD-01 Q4 mention it".</li><li>Its relation to ADD-01 Q4's data-room report is raised (`iss` L15, L55)</li></ul> |
| ME2 grading scale | missed | partial | Only the critic: "The item does not say whether that scale is supplied in the pack. If it is not, this is missing evidence" (`pkt` L646). No item records it |
| ME3 Direct Agreement | hit | hit | Q18 issue (`iss` L331) |
| DA1 composite asset | **missed** | **hit\*** | "An item that falls in more than one class (a composite asset, an assembly of parts of two classes) takes different values by the class it is read into … Which value applies is a person's judgment … the program chooses none" (`a3c` L231). \*A rule, in A3 only (see above) |
| HJ1 | hit | hit | as Q18 |

### Must-not-report traps (24): 24 avoided as assertions, 6 borderline (before 4)

**Borderline (none asserted; each is a reading, a display or a proposal):**

1. **Trap 1 (CiL at 4.0M or 2.5M).** The cover's 4.0M is "Reading 1" for pricing in two promoted issues (`iss` L100, L159). The A1 row still quotes SAR 2,500,000 but is flagged STALE (`a1` L209).
2. **Trap 2 (8.5 lapsed).** VOL-II-8.5-01/02 are "REPLACED (by VOL-V:42.3)", but no row in force carries 42.3 (C46, `pkt` L965). In A1 the obligation has no live row.
3. **Trap 6 (VOL-II 2.2 at 25 years).** The analysis "fact" S-F4 says note (4) "amends Volume II Clause 2.2" (`P` L147). The critic objects (`pkt` 3.5 section).
4. **Trap 8 (four classes), new.** "Open question: which minimum residual life applies to membranes, and whether membranes form a fifth class" (`iss` L263). "whether the cover's count matters, e.g. if row 5 applies only 'where provided'" (`iss` L215).
5. **Trap 11 (12.5 conflicts with 3.3), new.** "Reading 2: … VOL-V:3.3 needs a conforming change" (`iss` L295).
6. **Trap 20 (clarifications still possible).** Two issues still suggest asking the Authority: "should the Authority be asked to confirm?" (`iss` L199) and "or seek correction from the Authority" (`iss` L248). The controller's route note overrides them ("this question cannot be submitted as a clarification", `pkt` L111).

**Avoided, with no trace:** traps 3–5, 7, 9–10, 12–19 and 21–24.

- VOL-II is not renumbered, and the relocated text is unchanged.
- Table 42-1 values: no English value is taken as governing (the conditional row uses the Arabic), and membranes are not "prohibited".
- 3.6 is scored and 4.2 is procedural, neither pass/fail nor optional. The analysis 3.6 row said `pass_fail` and was not promoted.
- 12.5 is time and cost, not a Relief Event. The 4.2 blackout is not suspended generally, VOL-I 4.1 is not disapplied, and Form 4-C is not reissued.
- Answers: Q15 and Q16 add nothing, Q18 is not settled, and DA1 is not resolved.
- Dates and values: the PDD and the cut-off are unchanged, the addendum is not called invalid, D2 is not given as a single date, no GBR or grade value is invented, and 36.1 and 36.3 are untouched.

## 2. Usable updates

**Promoted into the candidate** (everything PROPOSED):

| Item | Before (`../COMPARISON.md` §2) | After (`log` L71; `pkt` L938–957) |
|---|---|---|
| Ops | 2 | **15**, 0 invalid |
| Analysis dispositions | 11 `no_effect` + 17 `unresolved`, and 19 controller `unresolved` | **35**; 9 provisions unresolved (2 accounted dispositions, 3 rows carried downstream, 3 conflicting translation rows, 1 escalation) |
| New rows | 9 | 8 |
| Re-made readings of existing rows | 0 | 6 |
| Issues | 1 | **23**, all HUMAN DECISION PENDING |
| Activities | 0 | 4 |
| Evidence items | 0 | 1 |
| Relationships | 0 | 10 (one `missing_document`) |
| The pending image reading | 1 | 1 |

Per key item (N = 33; missed items not counted):

| Class | Before | After | After: key items |
|---|---|---|---|
| **Applied; a person could accept it as is** | 6 | **17** | 1.1, 1.2, 1.3, 2.1, 3.2, 3.3, 3.6, 4.1, 4.2, 4.3, Q15, Q16, Q18 (the escalation is the expected form), E2, E3, the reading (three vowel marks to correct), SU6 |
| **Applied in part** | 5 | **9** | <ul><li>2.2: op, no row.</li><li>3.1: op; 42.3 has no row in force.</li><li>3.4: 42.1 words applied; the table escalated; one conditional row.</li><li>3.5: op, HUMAN DECISION PENDING, not applied to rows 4/5/note 4.</li><li>4.4: op; A3 and the diff unchanged.</li><li>Q17: (a) and (b) applied, (c) hedged.</li><li>Q19: op; the planning date lost.</li><li>AR1: conditional row 7; the disposition unresolved.</li><li>SU3: proposed relationship</li></ul> |
| **Detection only** | 17 | **6** | E1, AR2, AR3, SU1, SU2, SU4 |
| **Wrong as applied** | 0 | 0 | No promoted op, row or disposition has content the key contradicts |

**Promoted items that would mislead if accepted as is:**

- **The cover's SAR 4,000,000 as a pricing reading.** I-ADD03-COL-THRESHOLD and I-ADD-03-COVER-PARA3-ISSUE-ANA keep it (`iss` L100, L159). Choosing Reading 1 prices the trap value.
- **A5's `core-inspection-request`.** Its latest start, 2026-10-28, is before ADD-03's issue date, and it reads "INFEASIBLE by 14 WD". It is driven by ground-dd (`a5p` L10–11). The real request window, 17 Nov to 19 or 22 Nov, appears nowhere in A5.
- **VOL-I-4.2-01 "CONFIRMED (unchanged)".** Its quote and A3 line omit the 4.4 carve-out (`pkt` L1386; `a3c` L53). The critic: "A1 or A3 output that uses just the quote and the disqualification consequence would overstate the prohibition at ADD-03" (`pkt` 4.4 section).
- **VOL-II-8.5-01/02 OUT with no successor row for VOL-V 42.3** (C46).
- **I-ADD03-T42-1-MEMBRANE-UNIT's "24 years"** (`iss` L148) and **I-ADD03-HANDBACK-RELOCATION**, which asks "Whether the relocation changes the survey's effect" although 3.1 says "Its text is unchanged" (`iss` L111).
- **A1 candidate status "(invalid)" on three promoted rows** (ADD-03-4.1-01, -4.3-01, -Q17-01; `a1` L33, L36, L37). It invites a reviewer to discard valid rows (N2).

## 3. Missed effects and why (after)

**Still not detected:**

| Key item | Stage | Reason in the run's files | Class |
|---|---|---|---|
| SU5 / IE7 (VOL-I 4.1; Form 4-C decl. 5) | analysis / downstream | <ul><li>The 4.4 op's scope is VOL-I:4.2 only (`ops` L144).</li><li>No task asks which other clauses govern the same communications.</li><li>Form 4-C's "البند ٤-٢" sits in an approved image reading and is not a cross-reference link</li></ul> | software limitation (unchanged) |
| IE5 (row 5 vs VOL-II 3.2) | analysis / downstream | The row-5 unit is left open (AR2). The conditional lifecycle issue stops at the Financial Model (`iss` L72) | model miss (over-escalation) |

**Why the 14 partials are not hits:**

1. **Stated rules still handed to a person.** This is a design choice ("applied, not decided; a person confirms the application", W1) combined with model over-escalation.
   - It covers 3.5 / AR1–AR3, E1 / M7 (the cover against the operative 2.1), Q17(c) (6.2) and SU1 (ADD-01 Q4).
   - The controller now quotes the rule on these items (`pkt` L120–121, L529ff). It also flags two downstream reversals (DS-08, DS-APPB-ESC; `ckpt` `steps.downstream_validation.interactions`). It still leaves the provisions unresolved.
2. **Downstream items failing the controller's checks are not re-asked (software).** This affects 3.1 (DS-14/15, unknown date anchors) and 2.2 (DS-13 held back; DS-22-ROW a duplicate id). Two C46 gaps follow (`pkt` L959–965).
3. **`insert_table` refuses an Arabic-Indic table number (software).** This affects 3.4(b) (`pkt` L114).
4. **A3 and the diff do not render a scoped disapplication (software).** This affects 4.4 and the A3 delta.
5. **A5 lost the earlier reading of a forward count (software; regression).** This affects Q19, D2 and M1.
   - DS-ADD03-4.3-row: "date rule: ADD03-4.3-request: planning value None (unresolved)".
   - DS-43-MILESTONE is invalid: "no listed row needs EV-GROUND-DD" (`pkt` table at L852ff; `DS` L7144).
6. **Impact chains stop one link short (model).** This affects SU2 (no Form 4-E deemed acceptance), SU3 (no 39.2) and SU4 (no VOL-II 2.2 or 42.2).

**How the run classified its own losses:**

- **"Software limitation"** is used correctly for 3.4(b).
- **"Insufficient evidence"** is now used, rightly, for the GBR (`iss` L15).
- **"Ambiguous" is still used for matters the documents settle:** the 3.5 family, the cover figure, Q17(c), ADD-01 Q4 and the four/five classes.
- **One mislabel:** DS-APPB-ESC is an escalation whose `what_is_unsupported` reads "nothing is unsupported by the software" (critic, `pkt` 728ff).

## 4. False positives and false signals (after)

**False positives (5; before 5):** two fixed, three persist in a reduced form, two are new.

| # | What is stated | Where | Status against session 13 |
|---|---|---|---|
| 1 | C28 marks two accurate cover segments wrong. (a) "not found: 'replaces the remaining design life … for four asset classes set out in Table 42-1 (issued in Arabic)': no provision of ADD-03 does this", although 3.4(a) does it; the paired "omitted: ADD-03/3.4(a)" is the same error. (b) "contradicted: 'provides for … a limited exception to Volume I Clause 4.2'", although 4.4 is exactly a limited exception. The key lists both as `accurate_parts` | `a2cov` L13, L17, L21; `pkt` L1352, L1354 | persists, reduced (3 segments before) |
| 2 | Note (4) "amends Volume II Clause 2.2", stated as a **fact** | `P` L147 (analysis-002/S-F4) | persists (was in DS before) |
| 3 | Row 5: "Reading 2: 24 years" | `iss` L148; `pkt` L121 (r5) | persists |
| 4 | "whether membranes form a fifth class" / "if row 5 applies only 'where provided'" | `iss` L215, L263 | **new** |
| 5 | "VOL-V:3.3 needs a conforming change" for 12.5 | `iss` L295 | **new** (trap 11) |

**Fixed false positives:**

- Row 2's class ("treated water"): 0 hits in `P`, `DS` and `pkt`.
- `set_status VOL-II:8.5 deleted`: replaced by `relocate_unit`.

**False signals (13; before 10):**

| # | Signal | Evidence | Against session 13 |
|---|---|---|---|
| 1 | Three provisions whose rows were promoted (3.6, 4.2, 4.3) are listed first as "UNRESOLVED (accounted for, not applied)", and they BLOCK technical-proposal and core-inspection-request | `pkt` L117–119; `a5p` | new (N3) |
| 2 | A1 shows "(invalid)" on promoted rows ADD-03-4.1-01, -4.3-01 and -Q17-01 | `a1` L33, L36, L37 | new (N2) |
| 3 | A5 `core-inspection-request`: latest start 2026-10-28, INFEASIBLE by 14 WD; the request milestone undated | `a5p` L10; `a5m` L16 | new (N1) |
| 4 | VOL-I-4.2-01 "CONFIRMED (unchanged)"; "Disqualifiers (A3) — no change" | `pkt` L1386, L1431 | persists (before: "no change") |
| 5 | The 3.5 rule handed to a person: 13 items in the 3.5 family are HUMAN DECISION PENDING | section 5 | persists |
| 6 | VOL-II-2.2-01/02 UNRESOLVED from an English-only note | `a1` L98–99 | persists. VOL-II-9.3-01 is fixed (CONFIRMED) |
| 7 | Keyword triggers on quoted, non-deciding words: HUMAN DECISION PENDING on "governs" inside quotations of 3.5 (DS-10, DS-11, DS-ADD03-3.6-row; the 3.5 op); "no_effect on amendment language" on "unless" (1.2) and on "provided" in "provided for convenience only" (AppB/para1) | `pkt` L852ff (table), L205, AppB/para1 section | persists in a new form. The negations are fixed |
| 8 | The closed-window note attached to rows awaiting confirmation (3.6, 4.2, 4.3), which are not questions; two issue texts still suggest asking the Authority | `pkt` L117–119; `iss` L199, L248 | persists, reduced (tool limitations are now clean) |
| 9 | A malformed conditional task: "`impact:?` conditional on reading ? (pending_reading: the reading ? of ADD-03 …)". The model's answer to it is invalid ("ADD-03:region:ADD-03-p3-r1 is not a provision") | `pkt` L153; `DS` L4659 | new (N8) |
| 10 | "C45: the programme cannot be planned with the proposals: AttributeError: 'str' object has no attribute 'get'" | `pkt` L935–936; `ckpt` L314 | new (N7) |
| 11 | Two unresolved counts: "9 of 57" (`pkt` L108) against "8 of 57" (`pkt` L51, L1365). Validation says "54/57 provisions accounted", and the states line "unaccounted 0" | `pkt` L108–109; `ckpt` `steps.validation` | persists, much reduced and explained (3.4 partly applied; rows accounted downstream) |
| 12 | check-register exit 1: 2 C46 on the run's own ops (before: 8 deliverable findings) | `pkt` L959–965 | persists, reduced |
| 13 | Records of the stops: analysis-002's batch record still names the 429 session as its host session; the 2 killed downstream sessions and the killed segment's drive are absent; bench shows 13 sessions | `ckpt` `batches.analysis-002.host_session`; `bench` | persists in part (defect 15) |

**Asserted as settled although the key reserves it for a person: none.**

- HJ1 has no winner.
- DA1 is left to a person ("the program chooses none").
- D2 keeps both dates.
- The reading stays pending.
- The 4.4 scope's application is left to Legal ("whether a particular communication falls inside the exception", `pkt` 4.4 critic).

## 5. Pending decisions (after)

| Measure | Before | After |
|---|---|---|
| Provisions listed first | 19 (3 escalated, 16 unresolved) | **9** (1 escalated, 8 unresolved; `pkt` L108) |
| Distinct items marked HUMAN DECISION PENDING in the per-provision section | 9 | **35** (by script over `pkt` L160–852) |
| Promoted issues (all HUMAN DECISION PENDING) | 1 | **23** (`iss`) |
| Downstream items escalated | 13 | 13 (`run.log` L22) |
| Critic | 14 reviews, 7 disagreements | 51 reviews, 17 disagreements (`log` L25–42, L66–69) |
| The pending reading | 1 | 1 |

The 35 HUMAN DECISION PENDING items:

- **Right or fair (9):**
  - Q18, Q18/issue, Q18/question (HJ1);
  - 4.3/q-count (D2);
  - the GBR group: 4.1/issue-gbr, DS-41-ISSUE-GBR, DS-GROUND-ISSUE, DS-ADD03-4.1-issue (ME1);
  - DS-41-ISSUE-PROVISO, the 12.5 notice proviso. It is outside the key and is a fair Legal question.
- **Over-escalated: the documents settle it (26):**
  - **The 3.5 family (13):** 3.5; issue/3.5; ISS-ADD03-T42-1-r4/-r5/-note4; ISS-T42-row4/-row5/-note4; Q-ADD03-T42-1-r4-r5; Q-T42-row5; DS-READ-ISSUE-RENDER; DS-READ-ISSUE-UNIT; DS-APPA-ISSUE.
  - **The cover against 2.1 (3):** cover/para3/issue, DS-COVER-ISSUE, DS-22-ISSUE.
  - **Q17's 6.2 (2):** Q17/issue, DS-ADD03-Q17-issue.
  - **Four against five classes (1):** ISS-ADD03-cover-four-classes.
  - **ADD-01 Q4 with 3.3 (1):** 4.1/issue-q4.
  - **The relocation's "effect" (1):** DS-31-ISSUE.
  - **Keyword triggers (4):** DS-10, DS-11, DS-ADD03-3.6-row and DS-ADD03-3.6-issue.
  - **An invalid clarification (1):** DS-CQ-HANDBACK.
- **Not in the packet:** the one point with no correct answer (DA1, I-AUTO-CLASS-SCOPE) is HUMAN DECISION PENDING only in `a3c` L231.

**The real decisions are about the same as before:**

1. approve the reading (three vowel marks);
2. apply 3.5, so that rows 4 and 5 and note (4) follow;
3. confirm SAR 1,500,000 and drop the cover's 4.0M;
4. HJ1;
5. DA1, now raised but outside the packet;
6. D2's counting rule;
7. GBR Rev C (missing).

**The substance improved, but the packet a person must read grew:** about 26 of its 35 HUMAN DECISION PENDING items are over-escalated, against 7 of 9 before.

## 6. Interventions

**Manual steps:**

1. **The upload** through the panel (16:19:45).
2. **Resume 1** from the panel (17:43:22), after the coordinator restarted the panel (17:43:17).
3. **Resume 2** from the panel (18:26:50), after a second panel restart (18:26:46).

There was no curation, no file edit, no kill by hand and **no planned SIGTERM**. Both stops were container reclaims (work log E170).

The checkpoint records the two resumes as "resume (the person's action)" and lists them first in the packet (`ckpt` `interventions`; `pkt` L1312–1315).

**Batches asked twice:**

- **analysis-001 and -002.** At 16:24:17 both got the 429 (about 15 s each). Both were asked again at 17:43:31.
- **downstream-001 and -002.** They were started at 18:12:28/29 and killed at about 18:24. Both were asked again from scratch at 18:27:04 (`log` L46–51).
  - A downstream session "submits nothing: its final message is the set" (`ckpt` `batches.downstream-001.host_session.note`).
  - So about 11–12 minutes of two sessions' work could not be reused (N5).
- **analysis-003 and -004.** They were "asked ahead" at 16:24:34–35 but never started a session.

**Reused submissions:** two, analysis-002 (submitted 17:49:31, taken 17:50:32) and analysis-004 (submitted 18:00:38, taken 18:05:12).

- Both were made **after** Resume 1 by sessions asked ahead in the same drive, and both are recorded as such: "made after the resume at 2026-10-07T17:43:24Z" (`ckpt` `interventions`).
- The case the driver was meant to test, a submission made just before a stop and reused on resume, **did not occur**.

**Unplanned stops, as the run recorded them:**

- **The deferral.** It is recorded and explained in the packet: "DEFERRED … reset named in about 75 min" (`pkt` L1296–1297).
- **What followed.** The run then neither stopped (configured `on_deferred: stop`, exit 5) nor started the two batches it had asked ahead. Its last record is 16:24:35, and the resume found `status_before: running`.
  - With only about 5–6 minutes before the reclaim, the records cannot show whether it would have stopped.
  - This should be checked with a test (N9).

## 7. Time

**Steps** (`ckpt` `steps`; `run.log` L37–51; `bench` agrees: 3,417.2 s):

| Step | Before (s) | After (s) | Note (after) |
|---|---|---|---|
| ingest | 16.4 | 23.6 | |
| readings | 124.6 | 243.7 | Reading session 223.3 s (before 109.7) |
| analysis | 719.5 | 1,724.6 | = 17:43:24 → 18:12:09 (1,725 s), Resume 1's attempt only. 6 batches; 6 useful sessions of 371–870 s, 3,163 s in all |
| validation | 13.6 | 10.5 | |
| downstream | 190.6 | 1,210.8 | = 18:26:51 → 18:47:02 (1,211 s), Resume 2's attempt only. 44 tasks in 4 sessions (302–526 s), plus one repair session of 258.6 s |
| downstream_validation | 0.6 | 2.1 | |
| critic (downstream) | 38.6 | 118.8 | 4 requests |
| promotion, pin, check_register | 26.7 | 35.1 | |
| outputs | 35.4 | 34.9 | 107 files carry the banner |
| diff, review | 11.9 | 12.9 | |
| **Steps' sum** | **1,177.9 (19.6 min)** | **3,417.0 (57.0 min)** | |

**How I computed the active time.** The steps' sum is the time of the attempt of each step that **completed**:

- analysis's 1,724.6 s equals Resume 1's window to the second;
- downstream's 1,210.8 s equals Resume 2's.

So the 57.0 min **does not include** the deferral gap or the dead time, contrary to the work log (L63) and the brief's note. Nor does it include the work the kills destroyed. From the segment boundaries (`bench`; `ckpt` events; `log`):

| Interval | Seconds | Kind |
|---|---|---|
| Segment 1, 16:19:47 → 16:24:35 | 288 | active: ingest 23.6 + readings 243.7 + analysis attempt 1 (about 21 s, two 429 sessions) |
| 16:24:35 → 17:43:24 | 4,729 | **deferred, then dead.** The process stayed with no output until the reclaim at about 16:30, then nothing ran |
| Segment 2, 17:43:24 → about 18:24:00 | about 2,436 | active: analysis 1,724.6 + validation 10.5 + downstream attempt 1 (about 700 s, **lost**) |
| About 18:24:00 → 18:26:51 | about 171 | dead (restart) |
| Segment 3, 18:26:51 → 18:50:27 | 1,416 | active |

- **Active time:** about 4,140 s = **69.0 min**, with ±1 min because the second kill's time is not recorded.
  - **Kept work** is 3,417 s (57.0 min).
  - **Lost work** is about 720 s (12 min): the 21 s analysis attempt and the about 700 s downstream attempt of segment 2.
- **Dead or deferred time:** about 4,900 s (81.7 min).
- **Wall clock**, upload to end (`clock.txt`): 16:19:45 → 18:50:29 = **2 h 30 min 44 s**.
- `ckpt` created → updated: 9,040 s.
- `bench`'s segment 2 ends at 18:05:12, its last event, which hides the 19 min of work after it (N6).

**Sessions:**

- **13 primary host sessions** recorded (`bench`): 1 reading, 8 analysis (2 of them the 429s), 4 downstream.
- **1 repair session and 10 critic sessions.** That makes 24 with usage (`pkt` L9; `ckpt` L9007–9008: known 24, unknown 0).
- **2 killed downstream sessions with no record.** **26 sessions were started in all**, against 10 + 6 before.
- **Fixed overhead per analysis session:** 12–21 s, 131 s in all, 4.1 % (`bench`).

**Time to the first useful output:**

| Output | At | After the upload |
|---|---|---|
| The image reading | 16:23:56 | 4 min 11 s |
| The first analysis set (analysis-001) | 17:49:55 | 1 h 30 min 10 s; 6 min 31 s after Resume 1 |
| The review packet | 18:50:27 | 2 h 30 min 42 s; about 69 min of active time |

**The 30-minute target is missed on every measure:** by 27 min on kept steps, by about 39 min on active time and by 2 h on the wall clock.

**What made the active time almost three times longer (57.0 against 19.6 min):**

1. **The model.** Sessions were pinned to Opus, against the Sonnet the session-13 sessions reported.
   - analysis-003 took 869.5 s for 21 units, against 409.5 s for 26 units before.
   - The reading took 223.3 s against 109.7 s.
2. **More work.**
   - 57 provisions against 49: the reading now yields 20 image units, the letterhead blocks included.
   - 6 analysis batches against 5.
   - **44 downstream tasks against 17**, including W2's 6 conditional and 5 obligation tasks, in 4 sessions against 2, plus a repair re-ask.
   - 10 critic requests against 6.
3. **In-order collection.** analysis-004 finished at 18:00:38 and was taken at 18:05:12. The downstream phase had 502.8 s of idle slots (`ckpt` `concurrency`).
4. **What else the machine was doing.** `clock.txt` records **nothing** about other load. Its nine lines cover only the run, plus the labels E169 (the plan's 429) and E170 (the container restart).
   - The work log §2 says the fixers F1 and F2 ran in-process beside segment 2 (relaunched 17:41, died about 18:24). They ran again briefly from 18:26 to 18:30, beside segment 3.
   - Merge check 6 ran beside segment 1 (16:13 onward, 11 min 23 s).
   - All of this shared 4 cores and the same plan limit as the host sessions.

**The deterministic steps** together took about 119 s, against about 120 s before.

## 8. The 19 workflow defects of `../COMPARISON.md` §8

**Tally: FIXED 13 · NOT EXERCISED 1 · STILL PRESENT 5 · REGRESSED 0.** A regression outside the 19 is new defect N1.

| # | Defect (short) | Verdict | Evidence from this run |
|---|---|---|---|
| 1 | Row payloads not checked against the Row schema; not repaired or re-asked | **FIXED** | <ul><li>All 7 analysis `row_new` items are valid ("combined set: 80 item(s) … {'evidence_verified': 24, 'interpretation_pending': 52, 'escalated': 1, 'conflicting': 3}", `log` L44). No row failed on shape downstream.</li><li>The re-ask path ran once: "downstream-002 (done): repaired once (1 problem(s) before the re-ask)" (`pkt` L1298). The problem was the answer's format.</li><li>The MCP submit gate's repair was not needed by any analysis batch</li></ul> |
| 2 | `annotate` on answers refused by `previous_value` | **FIXED** | Q15, Q16, Q17(a), Q17(b), Q18 and Q19 annotates are all promoted (`ops` L161–257; `pkt` L444–528) |
| 3 | Dependencies may name only op ids | **FIXED** | <ul><li>22 items depend on issues, dispositions, rows or clarifications of the same set and pass, for example `Q-ADD03-T42-1-r4-r5 -> ISS-ADD03-T42-1-r4 …` and `ISS-ADD03-T42-1-r4 -> ADD-03/p3-image/r4` (script over `P`).</li><li>All 80 items are `ready: True`</li></ul> |
| 4 | Same-unit check flags disjoint `replace_text` spans | **FIXED** | 3.3 and 3.4(a) on VOL-V:42.1 are both evidence_verified and promoted (`pkt` L275–290; `ops` L71, L87) |
| 5 | One failed statement sinks every item that cites it | **NOT EXERCISED** | <ul><li>No statement failed its check (`P` controller `blast_radius: []`).</li><li>It would be reached by a fact with empty evidence or a paraphrase cited by several items.</li><li>Note: an interpretive "fact" passed because its quote is verbatim (`P` L147; N10)</li></ul> |
| 6 | No op types for relocation, uncited insertion, table insertion, scoped disapplication, relative change | **STILL PRESENT (in part)** | <ul><li>Four of five are now applied: `relocate_unit` (`ops` L56), `insert_unit` (`ops` L124), `annotate … disapplies` with scope (`ops` L144), and `adjust_value` with the computed 1,500,000 (`ops` L25; `pkt` L158).</li><li>The table insertion still fails: "unsupported: insert_table of a table read from an image whose number is printed in Arabic-Indic digits" (`pkt` L114)</li></ul> |
| 7 | A promoted `unresolved` disposition counts as an answer; A1 does not flag it; three counts | **FIXED** | <ul><li>"states (session 14: kept distinct): applied 13, no effect 35, partly applied 1, unresolved but accounted for 8, unaccounted 0" (`pkt` L109).</li><li>A1 reads "UNRESOLVED (value in question)" and "UNRESOLVED: STALE at ADD-03" (`a1` L98–99, L209).</li><li>The remaining 9/8 difference is explained by 3.4. Residuals are new defects N2 and N3</li></ul> |
| 8 | Analysis issues never promoted; no downstream task | **FIXED** | "it is written into the candidate's register as a PROPOSED issue (I-…-ANA; HUMAN DECISION PENDING) and its possible effects get a conditional downstream task" (`pkt` L967ff). 11 analysis issues are in `iss` |
| 9 | Downstream tasks only from valid ops; indirect analysis disappears; a new unit has no relationships | **FIXED** | <ul><li>44 tasks, including `conditional_impact` 6, `obligation_impact` 5 and `ana:` tasks (`run.log` L20).</li><li>The new unit VOL-V:12.4+ADD-03 reaches VOL-V-12.1-01 and 18.3-01 through REL-AI-008 (`pkt` L1410–1411).</li><li>Residual: "Earlier answers to re-read" still misses ADD-01 Q4 (`pkt` L126–128), which reaches the packet only through issues</li></ul> |
| 10 | Values from a pending reading make conditional rows but no impact analysis | **FIXED** | <ul><li>`impact:ADD-03-p3-r1` (`pkt` L154).</li><li>I-ADD-03-T42-1-LIFECYCLE-PRICING (conditional) reaches the lifecycle plan, the Financial Model and the AP (`iss` L72).</li><li>REL-AI-009 links ADD-03-T42-1-01 to fin-model-build and technical-proposal (`pkt` L1422, L1424).</li><li>Residual: VOL-II 2.2, 3.2 and 42.2 are not reached</li></ul> |
| 11 | Stated precedence rules still handed to a person | **STILL PRESENT** | <ul><li>The 3.5 op records "governs ADD-03:p3-image over ADD-03:T42-1" yet is HUMAN DECISION PENDING (`pkt` L316–320).</li><li>r4, r5, T42-1/4, T42-1/5 and note (4) stay UNRESOLVED (`pkt` L120–124) with the rule "(applied, not decided)".</li><li>The cover figure stays a pricing reading (`iss` L100). Q17(c) is hedged (`iss` L41).</li><li>Improvement: 1.2 is applied, and analysis-side reversals are now flagged (DS-08, DS-APPB-ESC)</li></ul> |
| 12 | Cover check splits at commas; compares no figure, count or modality | **FIXED** | <ul><li>"figure differs … SAR 4,000,000 is the earlier figure 'SAR 5,000,000' reduced by …", "count differs … 5 row(s)", "modality differs … (permission) … (obligation)" (`pkt` L1350–1353).</li><li>Two segments are still misjudged (false positive 1)</li></ul> |
| 13 | Closed-window note on every unresolved item; analysis issues suggest a clarification after the cut-off | **STILL PRESENT (reduced)** | <ul><li>The software escalation 3.4(b) and DS-3.4-ESC no longer carry the note (`pkt` L113; L852ff table).</li><li>But rows awaiting confirmation carry it: "UNRESOLVED ADD-03:3.6 … — the clarification window closed … it is a bid-decision for a person" (`pkt` L117–119).</li><li>Issues still say "should the Authority be asked to confirm?" (`iss` L199) and "or seek correction from the Authority" (`iss` L248)</li></ul> |
| 14 | Keyword triggers fire on negated words | **FIXED** | <ul><li>"not renumbered" raises no flag on 3.2 (`pkt` L266–273).</li><li>DS-HB-ESC, whose text says "the difference is reported, not resolved" (`DS` L5079), is escalated with no HUMAN DECISION PENDING (`pkt` L852ff table).</li><li>A wider keyword problem remains (N4)</li></ul> |
| 15 | Interruption bookkeeping unreliable | **STILL PRESENT (in part)** | <ul><li>**Fixed:** the reuse note reads "made after the resume at 2026-10-07T17:43:24Z", and the person's resumes are recorded and listed first (`ckpt` `interventions`; `pkt` L1312–1315).</li><li>**Still present:** `concurrency_drives` has one drive, the last, labelled `"segment": 1` although it was segment 3 (`ckpt` L8670–8673). The code numbers drives by count and records one only at a clean `close()` (`workflow.py` L568–583 of the package). Segment 2's analysis drive is lost.</li><li>**Still present:** the two killed downstream sessions are in no intervention, not in `host_usage` ("known 24, unknown 0", `ckpt` L9007–9008) and not in `bench`.</li><li>**Still present:** analysis-002's batch record names the 429 session `…162417Z-dc33` as its host session, not `…174331Z-457e`, which made the reused set. `bench` therefore shows analysis-002 at 14.6 s and analysis-004 with no session.</li><li>**Not exercised:** the `interrupted` event and the closing `prefetch_not_taken`, because no signal stop occurred</li></ul> |
| 16 | The run's own new rows fail check-register | **FIXED** | <ul><li>"missing because the downstream phase did not propose them (the run's own new rows): 0" (`pkt` L962).</li><li>Every new row names its evidence (`a1` L32–39). EV-CORE-INSPECTION-REQUEST and core-inspection-request are proposed.</li><li>The 2 remaining C46 findings are new defect N2/N12</li></ul> |
| 17 | In-order collection lets one oversized batch hold finished answers | **STILL PRESENT** | <ul><li>analysis-004 was submitted at 18:00:38 and taken at 18:05:12, after analysis-003 (21 units, 869.5 s; `ckpt` L8406; `log` L31–35).</li><li>Plan: "2 batch(es) of one structure kept whole beyond 8 provisions … (21), … (13)" (`ckpt` L176)</li></ul> |
| 18 | Usage line reports 0 calls | **FIXED** | "usage (application routes): none: the run's route is host …"; "host sessions: 24 (their own records); usage of the 24 that reported it: … output 510058 tokens" (`pkt` L8–9). Residual: killed sessions are absent (15) |
| 19 | "Documents referenced but not supplied" only from curated entries | **FIXED** | <ul><li>"Referenced but not supplied … NOT SUPPLIED: Geotechnical Baseline Report (Revision C)" via REL-REF-GEOTECHNICAL-BASELINE-REPORT-REV-C (`pkt` L1425–1427). It is also in the blockers line (`pkt` L54).</li><li>Residual: the grading scale, named only inside the Arabic image, is not checked (ME2)</li></ul> |

## 9. New defects (general)

1. **N1 (regression against session 13): a forward-counted deadline with two readings is no longer planned at the earlier one.**
   - The request milestone is "event-dependent (no date: unresolved)" (`a5m` L16). The downstream row's date rule has "planning value None (unresolved)" and the milestone activity is invalid (`DS` L7144).
   - The new request activity is made a predecessor of an activity that must finish before the window opens. Its latest start is therefore 2026-10-28, "INFEASIBLE by 14 WD", for a request that can only be made from the issue date (`a5p` L10–11).
   - Session 13 planned 19 Nov with 22 Nov kept.
2. **N2: one obligation gets several tasks, and A1 then marks the promoted row invalid.**
   - The same obligation reaches downstream as `c46:<op>`, `oblig:<op>` and `ana:<row>` tasks. Each proposes the same row.
   - The second is refused on the id ledger ("row id ADD-03-4.1-01 already exists or was listed before", `DS` L5587, L5959, L6357, L6916), and its dependency is then held back ("endpoints not promotable").
   - A1's candidate status then shows the **promoted** row as "(invalid)" (`a1` L33, L36, L37).
3. **N3: a provision whose obligation row is promoted downstream stays "UNRESOLVED (accounted for, not applied)".**
   - This happens for 3.6, 4.2 and 4.3 (`ops` L592–617; `pkt` L117–119).
   - It blocks the A5 activities that carry those rows: technical-proposal and core-inspection-request read "BLOCKED" (`a5p`).
4. **N4: keyword triggers fire on quoted words that decide nothing.**
   - HUMAN DECISION PENDING fires on "governs" inside a quotation of the governing-language rule (DS-10, DS-11, DS-ADD03-3.6-row; `pkt` L852ff).
   - "no_effect on amendment language" fires on "unless" in a reference recital and on "provided" in "provided for convenience only" (`pkt` L205; AppB/para1).
5. **N5: work in flight in a downstream or critic session cannot survive a stop.**
   - A downstream session "submits nothing: its final message is the set", so a kill discards it whole.
   - At 18:24 two sessions of about 11.5 min each were lost and asked again from scratch (`log` L46–51; the session folders hold only the prompt).
6. **N6: a segment ended by a kill leaves no end record, and its lost work is invisible.**
   - `bench` reports segment 2 as 17:43:24 → 18:05:12 (its last event), though the process worked until about 18:24.
   - The steps' timings keep only the completed attempt (downstream 1,210.8 s is segment 3's).
   - So neither the run nor `bench` shows the about 12 min of destroyed work or when the stop happened.
7. **N7: an exception is reported as a programme finding.**
   - "C45: the programme cannot be planned with the proposals: AttributeError: 'str' object has no attribute 'get'" (`ckpt` L314; `pkt` L935–936).
   - The downstream proposals' programme effects were therefore never checked.
8. **N8: conditional tasks are generated for a structural region unit.** The result is "`impact:?` conditional on reading ? (… the reading ? of ADD-03 …)" (`pkt` L153). The model's answer was invalid ("ADD-03:region:ADD-03-p3-r1 is not a provision of ADD-03", `DS` L4659).
9. **N9 (to confirm with a test): after deferring batches beyond the reset limit with `on_deferred: stop`, the run neither stopped nor ran.**
   - The two batches it had asked ahead never started a session, and nothing was logged after 16:24:35.
   - The resume found `status_before: running` (`ckpt` L8377; `jobs/20261007T161946Z-ai-run-bbe08f/job.json`).
   - The 5–6 minutes before the reclaim do not prove a hang.
10. **N10: a statement labelled "fact" can carry an interpretation and still pass, because the check tests only the verbatim quote.** Example: "The English translation carries a note (4) that amends Volume II Clause 2.2" (`P` L147). The critic caught it; the controller did not.
11. **N11: the same question is promoted as several issues.**
    - The governing-rendering question appears as I-ADD03-T42-1-RENDERINGS, I-ADD-03-3-5-3-5-ANA, I-ADD-03-P3-IMAGE-R4-ISSUE-ANA, I-ADD-03-T42-1-4-ISSUE-ANA, I-ADD-03-T42-1-5-ISSUE-ANA, I-ADD-03-T42-1-NOTE-4-ISSUE-ANA and I-ADD03-T42-1-MEMBRANE-UNIT.
    - The threshold appears as I-ADD03-COL-THRESHOLD, I-ADD-03-COVER-PARA3-ISSUE-ANA and I-ADD03-COVER-DIFF.
    - Analysis issues are promoted beside the downstream issues on the same point with no merging (`iss`; 23 issues against 1).
12. **N12: an issue raised only at output time does not reach the review packet.** The class-scope ambiguity (DA1's rule) is HUMAN DECISION PENDING in the candidate A3 (`a3c` L231) but appears neither in the packet nor in the candidate register.

## 10. Over-escalated, and settled when reserved

**Over-escalated (the documents settle it):**

- **The 3.5 rule and its 13 items** (section 5). The critic itself says: "Section 3.5 says 'The Arabic text governs.', so the Arabic is not itself unclear" (`pkt` r4 section).
- **The cover figure against 2.1 and 1.2** (`iss` L100, L159).
- **Q17's Envelope A consequence** (`iss` L41).
- **Four against five classes** (`iss` L215, L263).
- **ADD-01 Q4 against 12.5, with the 3.3 reading** (`iss` L295).
- **Whether the relocation changes the survey's effect** (`iss` L111), although the text is "unchanged".
- **I-VOL-I-ENV-B kept open after Q17** (`a1` L75, L82).

**Asserted as settled although the key reserves it for a person:** none (section 4).

## 11. Where the key and the run disagree

**I found no item where I think the key is wrong.** Where the run differs, the pack's words support the key:

- **Row 5's unit, note (4), Q17(c), and 1.2/2.1 against the cover:** as in `../COMPARISON.md` §9, I agree with the key.
  - "24 years" is the translation's.
  - Note (4) has no Arabic counterpart, and 3.5 makes the English "for convenience only".
  - A schedule with margin and DSCR is commercial information.
  - A cover summary is not a statement "otherwise" under 1.2.
- **ADD-01 Q4 and VOL-V 3.3.** 3.3 bars an extension of "the term". 12.5 extends "the Scheduled PCOD". Nothing in 12.5 touches 3.3, so the run's "conforming change" reading is unsupported. I agree with the key.
- **The fifth class.** "(where provided)" conditions where row 5 applies; it does not make the row a non-class. Five classes, as the key says.
- **The cover's 4.4 segment.** The cover says "a limited exception to Volume I Clause 4.2". 4.4 is exactly that. C28's "contradicted" is the tool's error.

**Points the run raises that the key does not cover (fair, not scored against the run):**

- **The 12.5 notice proviso** (I-ADD03-12.5-PROVISO): whether a missed 5-WD notice forfeits relief, where 34.3 says so expressly and 12.5 does not. It is a fair Legal question.
- **The scope of the GBR definition.** The critic says: "The provision limits its definition with 'In this Clause' … whether [4.2 and 4.3] mean Revision C is open" (`pkt` 4.1 section). The key lists Revision C for 4.1–4.3 (ME1). I read the same capitalised term in the same addendum as the same report. The run's note is a fair caution, not an error.

**Method-only differences:**

- **The 4.3 appointment date:** the same 23 Nov.
- **D5:** the same count convention as session 13, and the same 7.
