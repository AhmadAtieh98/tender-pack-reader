# Review packet: VOL-II-p3-r1 — Table 2-4 (image): Minimum Effluent Quality Parameters at the Point of Discharge

**STATUS: PENDING** (not yet reviewed by a person). Units derived from this reading carry `reading.status = pending`.

| | |
|---|---|
| Source | VOL-II page 3, bbox [56.7, 143.2, 538.6, 446.1] pt (PDF points) |
| Native image | 1750x1100 px, sha256 `27373c58a989d8ddc62ac537efca5551184ed992ae34ee3cc0b4fb33ff3acec6` |
| Crop | `regions/VOL-II-p3-r1/crop.png` (200 dpi render), page context `regions/VOL-II-p3-r1/context.png` |
| Reading file | `curation/readings/VOL-II-p3-r1.yaml` |
| Content sha256 | `be491090615b274806ab7721e0fe6f20b0292af42ac2ff3b7e85612a80aa69c3` (an approval pins this value) |
| Prepared by | AI-assisted: Claude Code session 02 (2026-10-02), read visually from the native 1750x1100 px image |
| Method | Visual reading of the embedded image at native resolution. No OCR. Grid structure (rows, columns) measured from pixels by tenderpack.regions.detect_grid; band positions by text_bands. |

## Checks run on this reading

| Check | Result | Detail |
|---|---|---|
| RD1 | pass | region VOL-II p3 [56.7, 143.2, 538.6, 446.1]; reading says VOL-II p3 [56.7, 143.2, 538.6, 446.1] |
| RD2 | pass | native image sha256 27373c58a989d8dd…; reading made from 27373c58a989d8dd… |
| RD3 | pass | grid from pixels: 12 horizontal x 5 vertical rules = 11 rows x 4 cols (skew -0.34 deg); reading: header + 10 rows x 4 columns |
| RD7 | WARNING | text bands [24] touch the image edge (1750x1100 px): content may continue beyond the image; cannot be established from the pack |
| RD4 | pass | 14 text bands and 11 rule bands detected; outside-grid text segments needing a reading: 3; unread: none |

All checks pass: **yes**. Passing checks do not approve the reading; they show the reading is complete, positioned and renders as printed. Whether each word and value is right is the reviewer's call.

## Uncertainties to resolve

1. The table is a scan with speckle and a measured skew of about -0.34 degrees; values were read at native resolution.
2. Table 2-4 is stated to be reproduced from an Environmental Permit that is not in the pack; this reading says what the image shows, nothing about the Permit.
3. `note1`: Note 1 is the last line of the image and touches its bottom edge; the image may be cropped. The page continues with 'End of reproduction.' in the text layer, but whether a further note was cut off cannot be established from the pack.
4. row `FaecalColiforms`: decimal point in 2.2: clear at native resolution, but a speckled scan can imitate a point; reviewer to confirm
5. row `ResidualChlorine`: printed as a range although the qualifier says 'all values are maxima'; whether 0.5 is a binding minimum is an interpretation for a person, not a reading question
6. row `pH`: unit cell shows a dash, read as 'no unit'
7. row `pH`: range printed under a 'maxima' qualifier (see Residual Chlorine)

## Side-by-side

![compare](compare-1.png)

## Line by line

| Segment | Source crop | Proposed source | Translation / notes |
|---|---|---|---|
| row `BOD5` | ![row](rows/r01.png)<br>![c0](cells/r01c0.png) ![c1](cells/r01c1.png) ![c2](cells/r01c2.png) ![c3](cells/r01c3.png) | Parameter: Biochemical Oxygen Demand (BOD5)<br>Unit: mg/l<br>Limit: 10<br>Basis of assessment: 30-day rolling average |  |
| row `COD` | ![row](rows/r02.png)<br>![c0](cells/r02c0.png) ![c1](cells/r02c1.png) ![c2](cells/r02c2.png) ![c3](cells/r02c3.png) | Parameter: Chemical Oxygen Demand (COD)<br>Unit: mg/l<br>Limit: 50<br>Basis of assessment: 30-day rolling average |  |
| row `TSS` | ![row](rows/r03.png)<br>![c0](cells/r03c0.png) ![c1](cells/r03c1.png) ![c2](cells/r03c2.png) ![c3](cells/r03c3.png) | Parameter: Total Suspended Solids (TSS)<br>Unit: mg/l<br>Limit: 10<br>Basis of assessment: 30-day rolling average |  |
| row `TN` | ![row](rows/r04.png)<br>![c0](cells/r04c0.png) ![c1](cells/r04c1.png) ![c2](cells/r04c2.png) ![c3](cells/r04c3.png) | Parameter: Total Nitrogen (TN)<br>Unit: mg/l<br>Limit: 5<br>Basis of assessment: 30-day rolling average |  |
| row `TP` | ![row](rows/r05.png)<br>![c0](cells/r05c0.png) ![c1](cells/r05c1.png) ![c2](cells/r05c2.png) ![c3](cells/r05c3.png) | Parameter: Total Phosphorus (TP)<br>Unit: mg/l<br>Limit: 1<br>Basis of assessment: 30-day rolling average |  |
| row `Turbidity` | ![row](rows/r06.png)<br>![c0](cells/r06c0.png) ![c1](cells/r06c1.png) ![c2](cells/r06c2.png) ![c3](cells/r06c3.png) | Parameter: Turbidity<br>Unit: NTU<br>Limit: 2<br>Basis of assessment: Maximum instantaneous |  |
| row `FaecalColiforms` | ![row](rows/r07.png)<br>![c0](cells/r07c0.png) ![c1](cells/r07c1.png) ![c2](cells/r07c2.png) ![c3](cells/r07c3.png) | Parameter: Faecal Coliforms<br>Unit: MPN/100 ml<br>Limit: 2.2<br>Basis of assessment: Maximum, any single sample | decimal point in 2.2: clear at native resolution, but a speckled scan can imitate a point; reviewer to confirm |
| row `ResidualChlorine` | ![row](rows/r08.png)<br>![c0](cells/r08c0.png) ![c1](cells/r08c1.png) ![c2](cells/r08c2.png) ![c3](cells/r08c3.png) | Parameter: Residual Chlorine<br>Unit: mg/l<br>Limit: 0.5 - 1.0<br>Basis of assessment: Continuous at outlet | printed as a range although the qualifier says 'all values are maxima'; whether 0.5 is a binding minimum is an interpretation for a person, not a reading question |
| row `pH` | ![row](rows/r09.png)<br>![c0](cells/r09c0.png) ![c1](cells/r09c1.png) ![c2](cells/r09c2.png) ![c3](cells/r09c3.png) | Parameter: pH<br>Unit: -<br>Limit: 6.0 - 9.0<br>Basis of assessment: Continuous at outlet | unit cell shows a dash, read as 'no unit'; range printed under a 'maxima' qualifier (see Residual Chlorine) |
| row `OilGrease` | ![row](rows/r10.png)<br>![c0](cells/r10c0.png) ![c1](cells/r10c1.png) ![c2](cells/r10c2.png) ![c3](cells/r10c3.png) | Parameter: Oil and Grease<br>Unit: mg/l<br>Limit: 1<br>Basis of assessment: Maximum, any single sample |  |
| `title` band 0 full | ![b](bands/b00-full.png) | Table 2-4   Minimum Effluent Quality Parameters at the Point of Discharge |  |
| `qualifier` band 1 full | ![b](bands/b01-full.png) | (all values are maxima; compliance assessed as a 30-day rolling average unless stated) |  |
| `note1` band 24 full | ![b](bands/b24-full.png) | Note 1:  Where a parameter is not listed above, the limit stated in the Environmental Permit shall apply. |  |

## How to approve or correct

1. Correct `curation/readings/VOL-II-p3-r1.yaml` directly if anything is wrong (the content sha256 will change).
2. When it is right, record approval: `python -m tenderpack approve VOL-II-p3-r1 --reviewer "<name>"`. This appends to `curation/approvals.yaml` with today's date and the current content sha256.
3. Re-run `python -m tenderpack ingest`. Any later edit to the reading voids the approval automatically.
