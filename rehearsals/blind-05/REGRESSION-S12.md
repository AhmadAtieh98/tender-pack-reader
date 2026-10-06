# Blind rehearsal 05, post-key regression of session 12: the candidate against the open key

**Synthetic, not tender content.** **This is a labelled regression, not a blind score.** The key (`rehearsals/blind-05/SEALED/`) had been open since 5 Oct 04:08 UTC, and the session-12 fixes were written with it in view. Nothing here measures performance on an unseen addendum.

Scorer: a separate agent session, Opus 5.5 (`claude-opus-5-5`), by its own instructions. It only read files (no run, resume or git command) and wrote only this file.

**The baseline** is `rehearsals/blind-05/COMPARISON.md`: the session-11 sealed run `ADD-03-run-host-blind05-20261005T025444Z`. Its scores were 21 hit / 16 partial / 1 missed of 38, with 1 false positive, 23 provisions unresolved and 72 min 27 s. In the tables, "s11" cites that file and "s12" cites the regression run.

**The run scored here** is `ADD-03-run-host-blind05-s12-20261005T183535Z`, read in place under `staging/ai/runs/` (not frozen). Short names:

| Short name | File |
|---|---|
| `R/` | `staging/ai/runs/ADD-03-run-host-blind05-s12-20261005T183535Z/` |
| `ops` | `R/candidate/curation/amendments/ADD-03.yaml` |
| `P` | `R/ai/ADD-03-run-host-blind05-s12-20261005T183535Z-combined/proposals.yaml` (77 items, 78 statements) |
| `DS` | `R/downstream/proposals.yaml` (79 items, 83 statements, 62 tasks) |
| `pkt` | `R/review/index.md` |
| `iss` | `R/candidate/curation/register/issues/ADD-03-ai.yaml` |
| `new` | `R/candidate/curation/register/rows/ADD-03-ai.yaml` |
| `a1` | `R/candidate/out/a1/a1.csv` (physical line numbers) |
| `a3c` | `R/candidate/out/a3/a3_candidate.md` |
| `a5c/` | `R/candidate/out/a5/candidate/` |
| `ckpt` | `R/checkpoint.json` |
| `log` | `R/log.jsonl` |
| `run.log` | `rehearsals/blind-05/run-s12.log` (the run starts at L144) |
| `clock` | `rehearsals/blind-05/clock-s12.txt` |
| `base` | `rehearsals/blind-05/COMPARISON.md` |

L means line.

## What ran, and on which code

- **Start.** `clock` L5: 18:35:35 UTC, `max_parallel_sessions=2`. Ingest refused the unread image, then the reading (one host session) and analysis batches 001–003 ran (`run.log` L144–157).
- **Planned interruption.** SIGTERM at 18:48:25 (`clock` L6–8; exit 143, `run.log` L158). It was sent by the coordinator's script after analysis-003's critic. That script is `run_blind05_interrupted.sh`, in the coordinator's scratchpad.
- **First resume.** 18:48:31 (`clock` L10). "the run lock of process 19577 (no longer running) was taken over" (`run.log` L209; `ckpt` events `stale_run_lock_taken_over` 18:48:32).
- **Deferral.** At 18:55:13–14 the host plan's limit hit analysis-004 and analysis-005: "You've hit your session limit · resets 10:30pm (UTC)"; reset named in 12,886.5 s, beyond the 300 s backoff. The run was DEFERRED, exit 5 (`run.log` L213, L270; `clock` L11).
- **Second resume.** 21:11:05, ending 22:10:34 with exit 0. Status `partial`, 17 provisions unresolved (`clock` L12–13; `run.log` L271–365).
- **Concurrency after the deferral.** The brief says `max_parallel_sessions` was 1 after the deferral. **The run's own files show 2 in flight after the 21:11 resume:**
  - `ckpt` event `run_lock_scoped` at 21:11:06 records `max_parallel_sessions: 2`;
  - `log` records `batch_asked_ahead … in_flight 2` at 21:11:08, 21:17:44, 21:23:49, 21:24:03, 21:34:50 and 21:46:45;
  - host sessions overlap (pairs started 21:11:08, 21:23:49/21:24:03, 21:46:44/45 and 21:56:34/35; session folders in `R/ai/`).

  I report what the files show.
- **Mixed code.** The first two segments (18:35–18:55) ran on the tree as it stood at 18:35. The resume (21:11–22:10) ran after commits `eaea64d` (20:08) and `2cff460` (20:46), which landed during the deferral. Those commits include fixes from the blind-06 scoring; for example, `tenderpack/ai/downstream.py` now cites "blind-06 follow-up 6 b". So analysis 004–009, downstream, promotion and outputs ran on the 21:11 code. I cannot reconstruct any uncommitted state at 21:11.
- **Inputs moved during the run.** The packet says the real inputs changed during the run (`pkt` L23: `config/assumptions.yaml`, several `curation/` files); the candidate used the copies made at the start.
- **Nothing is decided.** Human approval: none (`pkt` L15). Every item is PROPOSED.

## Scoring method

The key items and the hit / partial / missed rules are those of `base` (L18–22).

- **N = 38**: 15 provisions, 7 answers, 3 cover errors, 3 Arabic items and 10 secondary effects.
- The "s11 → s12" column reads **better**, **same** or **worse**, with the evidence line.
- Where s12's evidence sits only in an unpromoted item, the row says so.

## 1. Detection

| Group | s11 hit / partial / missed | s12 hit / partial / missed |
|---|---|---|
| Provisions (15) | 6 / 9 / 0 | **11 / 4 / 0** |
| Answers (7) | 7 / 0 / 0 | 6 / 1 / 0 |
| Cover errors (3) | 2 / 1 / 0 | **3 / 0 / 0** |
| Arabic (3) | 3 / 0 / 0 | 3 / 0 / 0 |
| Secondary (10) | 3 / 6 / 1 | 3 / 7 / 0 |
| **Total (38)** | **21 / 16 / 1** | **26 / 12 / 0** |
| Indirect effects (8) | 0 / 5 / 3 | 1 / 5 / 2 |
| Missing evidence (3) | 2 / 1 / 0 | 2 / 1 / 0 |
| Ambiguities D1 / D2 / D3 / D4 | partial / missed / hit / not used | hit / hit / **missed** / not used |
| Dates (10) right / partial / missed | 5 / 4 / 1 | 7 / 3 / 0 |
| Traps avoided | 19 of 19 | 19 of 19 |
| False positives | 1 | 1 (the same defect, smaller) |
| Unresolved provisions | 23 of 54 | 17 of 57 |

### Provisions (15): 11 hit, 4 partial

| Key | s11 | s12 | s11 → s12 | Evidence (s12) |
|---|---|---|---|---|
| 1.3 | partial | **hit** | better | `no_effect` (`ops` L371; `pkt` L198–201). Every unresolved provision now carries "the clarification window closed on 2026-11-12 (VOL-I 5.2) … it is a bid-decision for a person" (`pkt` L108–128); so do the A3 unresolved heading (`a3c` L76) and A5's "Clarification route" section (`a5c/README.md` L18) |
| 2.1 | partial | **hit** | better | `replace_text` VOL-I 6.6 (`ops` L25–43) and `set_status` VOL-I 6.7 `deleted`, evidence_verified (`ops` L44–58). VOL-I-6.7-01 is "DELETED (ADD-03/2.1(b))" (`pkt` L1415). New row ADD-03-2.1-01: "This replaces the obligation of row VOL-I-6.7-01", rejection consequence, "planning reading Tuesday 24 November 2026" (`new` L7–75). The candidate A3 has "ENTERS ADD-03-2.1-01 — explicit (rejection)" (`a3c` L13). Caveat: A5 plans the modification cut-off on 26 Nov (false positive below) |
| 2.2 | hit | hit | same | `no_effect` (`ops` L380) |
| 3.1 | hit | hit | same | `ops` L59–74 |
| 3.2 | hit | hit | same (the row is worse) | `insert_unit` evidence_verified (`ops` L75–90). The Base Date is computed as 2026-10-29 (`pkt` L146). The new row is now invalid, "kind 'deadline' not in (…)" (`pkt` L873; `DS` L3650), which leaves a C46 gap (`pkt` L947) where s11 had row ADD-03-3.2-01 |
| 3.3 | partial (escalated) | **hit** | better | One `replace_text` on 29.2 that `covers: ADD-03:3.3(b)` (`ops` L91–113). The row is re-made with the band, the election and both stages, `indexed_proportion_years_1_10_min_pct: 50` … (`DS` L7675; L3343). A1 shows "AMENDED (ADD-03/3.3)" (`a1` L35) |
| 3.4 | hit | hit | same | `annotate adds_obligation` VOL-I 10.3 (`ops` L114–129); fin-model-build activity "reflecting ADD-03 Section 3" (`DS` L4057; promoted) |
| 4.1 | hit | hit | same | `ops` L130–147; A1 shows "AMENDED (ADD-03/4.1)" (`a1` L172) |
| 4.2 | hit | hit | same | `ops` L148–163 |
| 5.1 | partial | partial | same (different reason) | The `replace_text` is right but held `conflicting` for another reason. In s11 the cover's error held it. Now it is "consistency: VOL-II:3.4: ADD-03/5.1, ADD-03/5.2 change the same unit in different ways across the set" (`pkt` L330–333; `ops` L518). Issue I-ADD03-ODOUR-OP is promoted, and its text says "the effective text still shows 5 OU/m³" (`iss` L18–31) |
| 5.2 | partial | **hit** | better | `annotate adds_obligation` promoted (`ops` L164–179) |
| 7.1 | partial | partial | same | 5.6 inserted, evidence_verified (`ops` L281–297). The Table 5-1 values are proposed as rows with their numbers: Zone A 25 m, Zone B 40 m, lighting, natural ground and the 30-day crane notice. They come from the analysis (`pkt` L646–667) and from the reading (`DS` L6451–6981). None was promoted (section 3). VOL-II-5.6-01 (`pkt` L474) was not promoted either |
| 7.2 | partial (escalated) | **hit** | better | The `annotate interprets` op carries a `precedence` block: `governs: ADD-03:p4-image`, `over: ADD-03:T5-1` (`ops` L298–319). It is promoted, labelled HUMAN DECISION PENDING (`pkt` L495–496). Blind-05 follow-up 5 asked for a precedence record |
| 7.3 | partial | partial | same | Computed as a CONDITIONAL deadline on 2026-11-23 (`pkt` L145). The analysis row ADD-03-7.3-01 is not promoted, "(dropped: )" with an empty reason (`pkt` L114). The downstream row is invalid (kind 'deadline', `pkt` L917), and its activity and evidence item are held back (`pkt` L918–919) |
| 7.4 | partial | partial | same | Row ADD-03-7.4-01 is proposed but not promoted, again with an empty "(dropped: )" reason (`pkt` L115, L535–536) |

### Answers (7): 6 hit, 1 partial

| Key | s11 | s12 | s11 → s12 | Evidence (s12) |
|---|---|---|---|---|
| Q15 | hit | hit | same, better signal | `interprets` VOL-II 6.4 (`ops` L180–195); "CONFIRMED (unchanged) VOL-II-6.4-01" (`pkt` L1430) |
| Q16 | hit | hit | same, better signal | `interprets` VOL-I 9.6 and Form 4-E (`ops` L196–212). Not marked CHANGED. VOL-I-9.6-01 is "NOT SETTLED … open: I-CONCESSION" (`pkt` L1433), an odd blocker for a confirmation |
| Q17 | hit | **partial** | worse | The op is promoted with the right words (`ops` L213–228). The row re-read is held `insufficient_evidence`: "whether the proposed EPC Contractor is an unincorporated joint venture … (bidder fact)" (`pkt` L855; `DS` L2095). The key treats that as an editable assumption. VOL-I-8.3-01 is UNRESOLVED / STALE (`a1` L9; `a3c` L17) and the iso-copy activity is not promoted (`pkt` L886). In s11 both were re-made |
| Q18 | hit | hit | same | `interprets` VOL-II 3.4 (`ops` L229–246); no value anywhere |
| Q19 | hit | hit | same, better content | Issue I-ADD03-AP-PRICE-BASIS: both horns, "The clarification window is closed", owner Commercial, "whether VOL-I 10.5 / 11.5 is engaged", HUMAN DECISION PENDING (`iss` L32–44; `DS` L5415, L5523). The analysis op stays `conflicting` (`ops` L526) |
| Q20 | hit | hit | same | `ops` L247–264. VOL-I-6.2-02 gets `named_by_addendum: the Indexed Proportion` (`DS` L1684); F4F-01 re-read (`DS` L3176) |
| Q21 | hit | hit | same (activity worse) | `ops` L265–280. Row VOL-I-9.7-01 is re-made with "a crane and lifting plan" (`DS` L2271). The technical-proposal activity is held `insufficient_evidence` (`pkt` L889) |

### Cover errors (3): 3 hit

| Key | s11 | s12 | s11 → s12 | Evidence (s12) |
|---|---|---|---|---|
| E1 | hit | hit | same; the check improved | Promoted issue I-ADD03-6.6-SUBSTANCE, shown on A3 (`iss` L3–17; `a3c` L156). C28 now finds the sentence: "unknown verb: 'consolidates'" and "consequence not mentioned" (`pkt` L1388–1389). Blind-05 follow-up 4 |
| E2 | hit | hit | same, better signal | C28 "not found: 'replaces the odour criterion in Volume II Clause 3.5'" (`pkt` L1390); `P` L143. VOL-II-3.5-01 is no longer flagged: "proposed (existing row; not changed by this run)" (`a1` L191). s11's false signal 3 is gone |
| E3 | partial | **hit** | better | C28: "scope (governing language): … its scope word(s) permanent are printed in ADD-03:T5-1, which does not govern" (`pkt` L1391) |

### The Arabic image (3): 3 hit

| Key | s11 | s12 | s11 → s12 | Evidence (s12) |
|---|---|---|---|---|
| Reading | hit | hit | same | 20 blocks. 23 of the key's 24 strings are verbatim (checked by script). The lead-in again reads يُحدِّد for يُحدَّد, now flagged as uncertain by the reading itself (`pkt` L617) |
| AR1 (datum) | hit | hit | same (no promoted issue) | "Under Clause 7.2 the Arabic governs, so the Table 5-1 limits are measured from natural (pre-grading) ground level" (`P` L1096; also L648, L668, L734). In s11 a datum issue was promoted (I-ADD03-T51-DATUM). Here the datum issues are labelled HUMAN DECISION PENDING and not promoted (`pkt` L629–630, L706–707) |
| AR2 (scope) | hit | hit | same | "the Table 5-1 limits apply to temporary structures, cranes and construction equipment" (`P` L981; L1262) |

### Secondary effects (10): 3 hit, 7 partial

| Key | s11 | s12 | s11 → s12 | Evidence (s12) |
|---|---|---|---|---|
| S1 (modify to Tue 24 Nov; late modification rejected) | partial | partial | better in A1/A3, still wrong in A5 | The row and A3 are right (2.1 above). A5 milestone `ADD03-MODIFY-CUTOFF,2026-11-26,…,as_stated` (`a5c/milestones.csv` L9). The deleted row VOL-I-6.7-01 still lists "MODIFY-CUTOFF: 2026-11-26" (`a1` L72) |
| S2 (Base Date Thu 29 Oct) | partial (two dates) | partial | better | One date, 2026-10-29, calendar days (`pkt` L146; `DS` L454). There is no row (invalid, see 3.2) |
| S3 (indexation, band, election, 75 %) | partial | **hit** | better | as 3.3 |
| S4 (odour at the receptor; value missing) | partial | partial | same | as 5.1; VOL-II-3.4-01 UNRESOLVED / STALE (`a1` L190) |
| S5 (VOL-II 3.2 switches on; ADD-01 r.1 partly wrong) | **missed** | partial | better | "condition changed by ADD-03/4.1: re-read (VOL-II:3.2 … the condition may now always hold; a person decides)" (`pkt` L149–151). The 3.2 rows are re-made with the condition kept (`DS` L7505, L7591). ADD-01 Q1 is listed for re-reading (`pkt` L132; `DS` L6325). It is not stated that 3.2 now applies |
| S6 (7.3 notice Mon 23 Nov) | partial | partial | same, computed | `pkt` L145; no row or milestone (7.3 above) |
| S7 (Arabic datum, scope, 30-day crane notice) | partial | partial | same | Stated (`P` L1088, L1096, L1262). The rows were not promoted. The crane notice's day type is left open: "days (calendar or working not stated)" (`DS` L7023) |
| S8 (Q17 per JV member) | hit | **partial** | worse | as Q17 |
| S9 (Q20) | hit | hit | same | as Q20 |
| S10 (Q21) | hit | hit | same | as Q21 |

### Indirect effects (8): 1 hit, 5 partial, 2 missed

| Key | s11 | s12 | s11 → s12 | Evidence (s12) |
|---|---|---|---|---|
| IE1 the definition reaches every use | partial | partial | better | "definition of 'Availability Payment' changed by ADD-03/3.1: re-read" (`pkt` L152; `a3c` L25). The escalation lists VOL-I-10.2-01, 10.6-01, 11.5-01, F4F-01/02 and VOL-V-29.3-01 for re-reading (`DS` L7768). The rows are not re-made ("their own units' text is not in units_after") |
| IE2 band → 6.2 and 10.5 on A3 | partial | partial | better | 6.2 is named (`DS` L1684). The 10.5 consequence of an out-of-band figure is proposed as row ADD-03-3.3-01 (`pass_fail`, `non_responsive`, HUMAN DECISION PENDING), but it is insufficient_evidence and not promoted (`DS` L7848; `pkt` L924). The packet section "Bands and the existing bid-out rules" lists 9.6, 10.5 and 11.5 (`pkt` L154–157) |
| IE3 3.2 applies; ADD-01 r.1 in A2 | partial | partial | better | as S5 |
| IE4 cranes, Portal notice, crane notice | partial | partial | same | Q21 row (`DS` L2271); 7.3 computed (`pkt` L145); the crane notice is not in A5 |
| IE5 lifecycle and handback | missed | missed | same | nothing on handback or major assets |
| IE6 no clarification route anywhere | partial | **hit** | better | `pkt` L108–128; `a3c` L76; `a5c/README.md` L18, which lists the activities "that relied on it". Blind-05 follow-up 12 |
| IE7 6.7 re-pointed; 24 Nov in A5; late modification on A3 | missed | partial | better | Re-pointed and on A3 (2.1). A5 shows 26 Nov (S1) |
| IE8 odour against stack heights | missed | missed | same | nothing |

### Missing evidence (3), ambiguities, dates

| Key | s11 | s12 | s11 → s12 | Evidence (s12) |
|---|---|---|---|---|
| ME1 ESIA Figure 7-2 | hit | hit | same, label fixed | `P` L333; issue (`iss` L18–31). I-VOL-II-MISSING is now "reached by this addendum: VOL-II-9.1" (`a3c` L136); s11's false signal 4 is gone |
| ME2 zone line and ground levels | partial | partial | same or slightly weaker | The datum issue says "Where the site is filled, the Arabic datum reduces the usable structure height … must be checked against natural ground levels" (`P` L8697–8704; not promoted). Missing levels are not declared, and I-VOL-III is "not reached by this addendum's changes" (`a3c` L135) |
| ME3 Schedule 9 | hit | hit | same | "Schedule 9 is still not supplied (I-VOL-V-MISSING)" (`DS` L3379) |
| D1 price basis (no correct answer) | partial | **hit** | better | Owner Commercial; both horns; route closed; 10.5 and 11.5 named; Form 4-F's "not subject to any qualification" re-read (`DS` L3266); no canon, "Which provision governs is not decided here" (`DS` L5415). Display caveat: on the candidate A3 it shows as unresolved Q19 and in the conflicts (`a3c` L79, L144). The issue's text appears only in `a3_detail.html` and, by id, in the A3 gate note; the s11 candidate A3 listed it (`base` L116) |
| D2 time of day of the cut-off | missed | **hit** | better | "the clause states no time of day" (`iss` L7–8; `new` L35–37) |
| D3 datum of 7.3's 30 m | hit | **missed** | worse | Nothing ties 7.3's 30 m to a datum (`P` 7.3 row at L4698ff names the zone, not the datum). The s11 datum issue was not reproduced |
| D4 | not used | not used | same | |

**Dates (10): 7 right, 3 partial, 0 missed.** s11: 5 / 4 / 1.

- **Right:**
  - DD1: planning date 15 Nov (`a5c/README.md` L5).
  - DD2: cut-off 12 Nov, passed (`a5c/milestones.csv` L8; `pkt` L108).
  - DD3: Base Date 29 Oct, one reading (`pkt` L146).
  - DD6: withdrawal until the PDD (`a5c/milestones.csv` L10).
  - DD7: PDD unchanged.
  - DD8: 9 Working Days left (`pkt` L144); s11 missed this.
  - DD9: letter date 10 Nov (reading).
- **Partial:**
  - DD4: 24 Nov is computed (`pkt` L145) but planned as 26 Nov.
  - DD5: 23 Nov is computed and conditional, with no milestone.
  - DD10: the 30-day crane notice is read but its day type is left open and it is not planned.

### A3

The validated A3 stays at ADD-02. The candidate A3 gains 1 row and changes 1 (s11: 0 and 1) (`a3c` L9–17).

| Key | s11 | s12 | Evidence (s12) |
|---|---|---|---|
| Merged 6.6: late modification rejected | missed | **hit** | ENTERS ADD-03-2.1-01 (`a3c` L13, L36) |
| 6.2: Indexed Proportion in Envelope A | hit | hit | VOL-I-6.2-02 "flags: see ADD-03/Q20" (`a3c` L53) |
| 10.5: out-of-band figure (derived) | missed | partial | proposed, HUMAN DECISION PENDING, not promoted (`DS` L7848) |
| 9.6 confirmed | hit | hit | `a3c` L54 |
| 8.3: evidence per JV member | hit | hit | "CHANGES VOL-I-8.3-01 — now STALE" (`a3c` L17) |
| 11.5 tied to D1 | missed | partial | named in the D1 issue (`iss` L36–37); the A3 row is flagged for the definition change (`a3c` L56) |
| Must not be added (7.3, Table 5-1, odour, membranes, Q15) | avoided | avoided | only ADD-03-2.1-01 enters |
| Unresolved: D1 / ME1 / ME2 / D2 / "no route" | yes / yes / no / no / no | yes (by id and as Q19) / yes / no / yes / yes | `a3c` L76–94, L156 |

### Traps: 19 of 19 avoided (same)

- **VOL-II 3.5 not amended:** avoided, and now not flagged at all (`a1` L191).
- **No odour value:** avoided as before. The effective text of VOL-II 3.4 still holds 5 OU/m³ because 5.1 is held, but the row is UNRESOLVED / STALE and the issue says the substitution is not applied (`iss` L19–22).
- **Heights from natural ground, not permanent structures only:** avoided.
- **No sea-level height or site elevation:** none in `P` or `DS`.
- **Q15 registers no 10 years; Q16 adds no requirement:** avoided.
- **Withdrawal not moved:** 26 Nov (`a5c/milestones.csv` L10).
- **No renumbering:** avoided.
- **PDD and cut-off unchanged:** avoided.
- **75 % not called an inconsistency:** avoided.
- **D1 not resolved and no canon applied:** avoided.
- **7.3 not a disqualifier:** avoided.
- **Q17 not extended** to the O&M Operator: avoided.
- **Tables 2-4 and 2-6 unchanged; odour not an Unavailability Event:** avoided.
- **No membrane replacement count:** avoided.
- **Base Date in calendar days, before the issue date:** avoided.
- **Form 4-F not altered:** "it does not alter the printed form text" (`P` L580).
- **No claim that ADD-03 can still be clarified:** avoided; the route is said to be closed everywhere.

### False positives and false signals

**False positive (1, the s11 defect in a smaller form).** The modification cut-off is planned on the PDD, as if 2.1 had not moved it:

- A5 `ADD03-MODIFY-CUTOFF,2026-11-26,…,as_stated` (`a5c/milestones.csv` L9);
- the deleted VOL-I-6.7-01 keeps "MODIFY-CUTOFF: 2026-11-26" in A1's Dates column (`a1` L72).

The cause: the promoted row's date rule is `kind: anchor`, `offset: 2`, `unit: working_day`, `direction: before` (`new` L51–60), and the planner places it on the anchor date. In s11 the 6.7 row stayed ACTIVE and unflagged. Now the row is DELETED, the new row and A3 are right, and only the A5 date and the dead row's Dates cell are wrong.

**False signals:**

1. **A1 shows a valid row as invalid.** A1's candidate status for ADD-03-2.1-01 reads "new row at ADD-03 (invalid)" (`a1` L40). The promoted proposal P-ADD03-ROW-2.1-01 is interpretation_pending. The "invalid" seems to come from a second proposal with the same id, DS-ADD03-008, rejected by the id ledger (`pkt` L871). My reading of the cause is an inference.
2. **check-register exits 1 on four findings** (`pkt` L944–948). Two are on that row: VOL-I 6.6's disposition does not list it, and its assessment is `procedural` "but a breach puts the Proposal out (rejection): pass_fail". Two are C46 gaps for 3.2 and 7.1 (their rows were rejected or not promoted).
3. **A consistency check treats two ADD-03 provisions as a conflict.** 5.1 (`replace_text`) and 5.2 (`annotate adds_obligation`) on the same unit are called "change the same unit in different ways" (`pkt` L333). The key has no conflict there, and this is now what holds 5.1.
4. **VOL-V-29.2-01 is promoted twice.** "readings: … VOL-V-29.2-01 … VOL-V-29.2-01" (`pkt` L935). One copy comes from the row task (`DS` L3343), the other from the definition task (`DS` L7675).
5. **The issue date is said to be missing.** "ADD-03's own issue date was not found" in two image escalations (`DS` statement L889; `pkt` L571). The run computes from 2026-11-15 everywhere else.
6. **Settled points carry HUMAN DECISION PENDING.**
   - 1.3, a statement of fact (`pkt` L201).
   - The AppA para 1 confirmation (`pkt` L545).
   - The Q21 and 3.1 row readings, triggered by the words "settled", "governs" and "are to be read" (`pkt` L857–858).
   - Downstream-005's "Which rendering applies, and the effect of the Section 7.2 words, is a legal question" (`DS` L1020), although 7.2 says the Arabic governs and the promoted 7.2 op records it.

**s11 false signals that are fixed:**

- 2 (confirmations shown as changes): Q15 and VOL-I-6.2-01 are CONFIRMED (`pkt` L1427, L1430).
- 3 (VOL-II 3.5 flagged).
- 4 ("not reached" on the ESIA).
- 5 (two Base Dates).
- 6 (unpromoted issue ids in row notes): this is now enforced, "held back: issue references not among the promoted issues" (`pkt` L911–915). The check that fixes it also holds back three reading rows.

## 2. Usable updates

**Promoted** (`run.log` L302; `pkt` L930–941):

| Item | s12 | s11 (`base` L186) |
|---|---|---|
| ops | 19 | 12 |
| dispositions | 21 | 19 |
| new rows | 1 | 2 |
| readings | 19 | 12 |
| issues | 3 | 3 |
| activities | 4 | 7 |
| clarifications | 0 | 1 |
| relationships | 0 | 0 |
| no_change | 10 | 8 |

All are PROPOSED.

**By key item (38).** The baseline did not split usable updates this way, so only s12 is classed.

| Class | Key items | Count |
|---|---|---|
| **Applied, a person could accept it as is** | 1.3, 2.2, 3.1, 3.3, 3.4, 4.1, 4.2, 5.2, 7.2 (ops or dispositions); Q15, Q16, Q18, Q20, Q21 (ops; Q20 and Q21 with re-made rows); Q19 (the promoted D1 issue is the expected form); E1 and E2 (promoted issues); E3 (C28 finding in A2 and the packet); the reading (pending approval); S3, S9, S10 | 22 |
| **Applied in part** | 2.1 and S1 (ops and row right; A5 date wrong); 3.2 and S2 (op right; Base Date row rejected); Q17 and S8 (op right; row STALE, activity not promoted); AR1 and AR2 (the 7.2 precedence op applies the Arabic in general; the datum and scope issues are not promoted); S5 (3.2 rows flagged and re-made with the condition kept) | 9 |
| **Detection only** | 5.1 and S4 (op held by the consistency check; issue promoted); 7.1 and S7 (Table 5-1 rows proposed, none promoted); 7.3 and S6 (row not promoted or invalid; date computed); 7.4 (row not promoted) | 7 |
| **Wrong as applied** | the modification-cut-off date in A5 and in the deleted row's Dates cell (part of 2.1 and S1) | 1 (counted inside 2.1 and S1) |

## 3. Missed effects and why

**No trace among the 38:** none. The two misses of s11 (S5 and the 6.7 row) now have a trace.

**Scored separately:**

- **IE5 and IE8:** no trace.
- **D3:** not proposed. The s11 issue that carried it was not reproduced.
- **ME2:** the missing site levels are not declared.

**Detected but not applied**, by reason from the run's files:

- **Analysis-phase `row_new` items are never promoted.** 7.3/row, 7.4/row, the Table 5-1 rows (row-a-left, row-a-right, row-b-left, note1, note2, note3) and VOL-II-5.6-01 are all interpretation_pending. They appear as "(dropped: )" with an empty reason (`pkt` L114–128).
  - `promoted_ops()` in `tenderpack/ai/downstream.py` (read for this) collects only `amendment_op` and `disposition` items from the analysis set. A `row_new` therefore lands in "not promotable … (dropped: )" with no reason.
  - The coverage line also counts 7.3, 7.4, p4-image/note2 and note3 as "unaccounted" by the combined set (`pkt` L952; `P` coverage) while they hold such rows.
- **Downstream date rules of kind "deadline" are refused by the register:** DS-ROW-73 and DS-ADD03-010 (`pkt` L873, L917). Blind-06 showed the same refusal.
- **Reading rows held back because their issue was not promoted:** DS-ROW-P4-01, 02 and 05 (`pkt` L911–915). The renderings issue itself is `conflicting` (`pkt` L916).
- **A clarification draft that quotes amended text fails clarify.check "not verbatim":** P-ADD03-CQ-6.6 and DS-ADD03-012 (`pkt` L854, L875). Blind-06 showed the same.
- **Held on a bidder fact the key treats as an editable assumption:** VOL-I-8.3-01 and the iso-copy activity (Q17).
- **Held by the new consistency check:** 5.1.

## 4. Pending decisions

**Volume.**

- 17 unresolved provisions (s11: 23), each now ending with the closed-route sentence (`pkt` L108–128).
- 0 analysis escalations (s11: 8).
- 14 downstream items `escalated` and 9 `conflicting` (`run.log` L295).

**HUMAN DECISION PENDING labels.** This label is new in session 12; the s11 packet has none (`grep` count 0 in `rehearsals/blind-05/review/index.md`).

- **17 analysis items** (`pkt` L159–842): cover/para3 clarification-substance and issue-odour, 1.3, 3.3-form, 5.1-clar, Q19-issue, 7.2, 7.2/issue, 7.2/clar, AppA/para1, th-left/issue, note1/issue, note2-issue, T5-1/note(1)/issue and /clar, T5-1/note(2)/issue and /clar.
- **13 downstream items** (`pkt` L845–925): P-ADD03-ROW-2.1-01, P-ADD03-ISSUE-6.6-SUBSTANCE, P-ADD03-VOL-I-9.7-01, P-ADD03-VOL-II-3.1-01, P-ADD03-ISSUE-ODOUR, DS-ADD03-003, 008, 009, 011, 012, DS-ADD03-ISSUE-AP-BASIS, DS-ISSUE-RENDERINGS and D1.

Against the key:

| Item | s12 handling | Key | Verdict |
|---|---|---|---|
| D1 | escalated to Commercial, both horns, constraints named | no correct answer; a person | right (better than s11) |
| D2 | "time of day not stated", left open | flag, do not assert | right |
| Arabic approval | pending | a person | right |
| 10.5 for an out-of-band figure | "A person decides whether VOL-I 10.5 covers that value" (`DS` L1322) | derived, medium confidence | acceptable |
| VOL-II 3.2 applicability | left to a person (`pkt` L151) | the key says it applies | over-cautious |
| Arabic over English (7.2 words) | the op records the precedence, yet downstream calls it "a legal question" (`DS` L1020) | the Arabic governs | over-escalated |
| Cover against 6.6 ("Which text governs … for a person", `iss` L7–8) | | the operative text governs; report E1 | over-escalated |

**System judgments the key reserves for a person:** none found. D1 is not resolved; the 3.2 condition and 10.5 are left open.

## 5. Interventions

| Event (UTC) | What it was | Cost | Batches asked again? |
|---|---|---|---|
| 18:48:25 SIGTERM (planned, coordinator's script) | Killed the run after analysis-003's critic. Analysis-004 (asked 18:46:08) and analysis-005 (asked 18:48:21) were in flight. Their sessions (`R/ai/…184608Z-cf72`, `…184821Z-fd11`) have no `session.json` | about 2 min 17 s of analysis-004 session time lost. In the step timer, the in-progress analysis step showed "0.0 s running" at the kill (`run.log` L162), so its ~566 s (18:38:59 → 18:48:25) are missing from the steps' sum | 004 and 005 were re-asked; 001–003 were not (attempts 1, `ckpt` batches) |
| 18:48:31 resume (coordinator's script) | Took over the dead process's lock (`ckpt` events 18:48:32). Re-asked 004 and 005 with 2 in flight | 6 s gap | — |
| 18:55:13 deferral (automatic) | Both sessions ended with 429 after 335 s and 399 s. Before that, the two sessions had staged four proposal sets (`R/ai/ADD-03-host-20261005T185308Z-d215`, `…185316Z-4a90`, `…185405Z-231d`, `…185511Z-17d3`), unused | about 12 min of session work discarded; then 2 h 15 min 51 s waiting for the plan's reset | — |
| 21:11:05 resume (coordinator) | Re-asked 004 and 005 from scratch, then 006–009 and downstream | — | `ckpt` attempts: analysis-004 **3**, analysis-005 **2**. The session folders show three starts each; 005's SIGTERM-killed start (4 s) is not counted |

- Downstream-001 was repaired once (`pkt` L1321).
- `ckpt` `interventions` has 18 entries, all "host session (automatic) … not a person" (`pkt` L1341–1360). They include the two 429 sessions, recorded at 18:55:13.
- **Manual steps:** the planned SIGTERM and the two resume commands, all by the coordinator. No content was edited between the PDF and the outputs.

## 6. Time

**Steps' sum: 4,171.2 s (69.5 min)** (`run.log` L313–324).

| Step | s12 | s11 (`base` L203–211) |
|---|---|---|
| analysis | 2,529.0 s; 9 batches, 13 host sessions started (9 used, 2 killed, 2 ended by 429) | 2,675.7 s; 9 sessions, 1 in flight |
| downstream | 1,315.8 s; 6 batches, 6 sessions, 2 in flight | 1,260.1 s; 5 sessions |
| readings | 186.8 s | 209.3 s |
| critic | 67.8 s; 13 requests (9 analysis, 4 downstream) | 66.4 s; 14 requests |

**Wall clock: 18:35:35 → 22:10:34 = 3 h 34 min 59 s.** **It is not comparable with s11's 72 min 27 s**, because it contains:

- the 6-second interruption;
- the 2 h 15 min 51 s deferral (18:55:14 → 21:11:05).

The three running segments total **79 min 2 s**: 12:50, 6:43 and 59:29. The steps' sum is about 9.5 min lower, because the analysis time of the first segment was lost on the SIGTERM.

**Analysis.**

- The 2,529.0 s comprise 401.9 s of the 18:48–18:55 segment, whose work was discarded, and 2,127 s after the reset (6 batches at 2 in flight).
- The analysis sessions that were used ran 143.6–737.8 s each (`R/ai/*/session.json`).

**Downstream** was slower than s11 despite 2 in flight. It had 6 batches against 5 and 62 tasks against 60. Downstream-001 took 589.6 s including a repair (`ckpt`). Its sessions ran 125–514 s.

## What the session-12 fixes changed: session 11's follow-ups 1–8 (`base` L220–227)

| # | Follow-up | Status | Evidence (s12) |
|---|---|---|---|
| 1 | Clause lists: delete both 6.6/6.7 citations; mark rows citing 6.7 | **met** | `set_status` 6.7, evidence_verified (`ops` L44–58); "OUT VOL-I-6.7-01: DELETED" (`pkt` L1415). The A5 date is a separate defect |
| 2 | One quotation, one op (29.2 across the clause and its list item) | **met** | `covers: ADD-03:3.3(b)` (`ops` L91–113); 3.3(b) answered through 3.3 (`pkt` L290–292) |
| 3 | The cover never holds an operative op | **met** | 2.1 is promoted despite E1; the cover findings are report-only (C28). 5.1 is now held by a different check (follow-up 3 of this file) |
| 4 | C28 finds "This Addendum <verb>", reports unknown verbs, checks scope words against the governing text | **met** | `pkt` L1388–1391 |
| 5 | Ops for what a new unit carries (row_new for 7.3/7.4; precedence between renderings) | **partly** | Precedence is met (`ops` L298–319). The 7.3 and 7.4 rows are proposed but not promotable from the analysis set (empty "dropped" reason). The downstream 7.3 row is invalid (date-rule kind) |
| 6 | Image tables into the register, conditional on approval | **partly** | Rows with values are proposed from the reading (`DS` L6451–6981) and from the analysis (`pkt` L646–720). None is promoted: held back on an unpromoted issue, conflicting, or analysis `row_new` |
| 7 | Computed dates into A5; one reading of "N days before X"; Working Days left | **partly** | 24 Nov, 23 Nov and 29 Oct are computed once each, and 9 WD is stated (`pkt` L142–147). Milestones: 23 Nov none (row invalid); 24 Nov planned as 26 Nov; Base Date row invalid |
| 8 | Conditional clauses switched on; earlier answers re-read | **met (as flags)** | `pkt` L149–151; `DS` L7505, L7591; ADD-01 Q1 and Q6 re-read and escalated (`pkt` L131–132; `DS` L6325, L6386). The key's stronger "3.2 now applies" is left to a person |

**Session 11's follow-ups 9–14:**

- 9 (derived consequences on A3): partly; 10.5 proposed, not promoted.
- 10 (confirmations are not changes): met for Q15, 6.2-01 and 10.3; one odd "NOT SETTLED" on 9.6.
- 11 ("not reached"): met for the ESIA; I-VOL-III still "not reached".
- 12 (closed route said everywhere): met.
- 13 (issue ids checked): met; it now also blocks rows.
- 14 (parallel sessions): 2 in flight. Not measurable here because of the deferral.

## Defects seen in this run (general)

1. **The step timer loses a running step's elapsed time on SIGTERM** ("analysis 0.0 s running"), so the steps' sum understates an interrupted run.
2. **A host session that submitted proposals but ended with a 429 is discarded whole.** Its staged sets are not used after the resume (four sets, about 12 min).
3. **Analysis `row_new` items cannot be promoted, and the reason printed is empty** ("dropped: "). Coverage also counts their provisions as unaccounted.
4. **The planner places a date rule of `kind: anchor` with a working-day offset on the anchor itself** (24 Nov → 26 Nov). A deleted row keeps its old planning date in A1.
5. **The register refuses the date-rule kind "deadline"** that downstream date tasks propose (also seen in blind-06).
6. **A1's candidate status shows "invalid" for a promoted row** when a second proposal of the same id was invalid.
7. **The consistency check treats a `replace_text` and an `annotate` on the same unit as conflicting** (5.1 and 5.2).
8. **One row is promoted twice** from two tasks (VOL-V-29.2-01).
9. **The HUMAN DECISION PENDING trigger words fire on statements of fact** and on settled precedence ("settled", "governs", "are to be read").
10. **The code changed between the run's segments.** A resumed run picks up whatever tree is current, and nothing in the checkpoint records the code version per segment.

## Where the key and this run disagree

I found no item where I think the key is wrong. Two caveats about scoring this run at all:

- **The key was open,** so it scores a regression and not detection.
- **The run mixes code from before and after the 20:08 and 20:46 commits,** so a per-fix attribution beyond the follow-up table above is not possible from these files.
