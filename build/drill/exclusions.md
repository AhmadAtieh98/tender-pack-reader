# Excluded text — NUPA-ISTP-2026-014-DRILL

Every span below was excluded from content because it matched a declared rule in `config/furniture.yaml` on all of the rule's attributes. Nothing else is excluded; in particular, rotated text that does not match the WATERMARK rule stays content.

## Rules

- **WATERMARK**: diagonal watermark printed on every page. Attributes: `{'text': 'FICTIONAL — ASSESSMENT PACK', 'color': '#dbdbdb', 'size': [30.0, 40.0], 'angle': [47.0, 57.0], 'expect_per_page': 1}`
- **HEADER-TITLE**: running header (document title), top margin. Attributes: `{'max_y1': 45.0, 'color': '#5a5a5a', 'size': [6.0, 7.5], 'pattern': '^(Volume I — Instructions to Bidders|Volume II — Technical Requirements \\(extract\\)|Volume IV — Form Sheets|Volume V — Draft Project Agreement \\(extract\\)|Addendum No\\. [0-9]+)$'}`
- **HEADER-REF**: running header (tender reference), top margin. Attributes: `{'max_y1': 45.0, 'color': '#5a5a5a', 'size': [6.0, 7.5], 'pattern': '^NUPA/ISTP/2026/014$'}`
- **FOOTER-DISCLAIMER**: running footer disclaimer, bottom margin. Attributes: `{'min_y0': 790.0, 'color': '#5a5a5a', 'size': [6.0, 7.5], 'pattern': '^FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment\\. Not a real tender\\.$'}`
- **FOOTER-PAGE**: running footer printed page number, bottom margin (captured as printed_page). Attributes: `{'min_y0': 790.0, 'color': '#5a5a5a', 'size': [6.0, 7.5], 'pattern': '^Page (?P<printed_page>[0-9]+)$'}`

## All exclusions (170 spans)

| Span | Rule | Text | Angle | Colour | Size | BBox |
|---|---|---|---|---|---|---|
| VOL-I/p1/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-I/p1/s002 | HEADER-TITLE | Volume I — Instructions to Bidders | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 161.4, 41.7] |
| VOL-I/p1/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-I/p1/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-I/p1/s005 | FOOTER-PAGE | Page 1 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-I/p2/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-I/p2/s002 | HEADER-TITLE | Volume I — Instructions to Bidders | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 161.4, 41.7] |
| VOL-I/p2/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-I/p2/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-I/p2/s005 | FOOTER-PAGE | Page 2 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-I/p3/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-I/p3/s002 | HEADER-TITLE | Volume I — Instructions to Bidders | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 161.4, 41.7] |
| VOL-I/p3/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-I/p3/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-I/p3/s005 | FOOTER-PAGE | Page 3 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-I/p4/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-I/p4/s002 | HEADER-TITLE | Volume I — Instructions to Bidders | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 161.4, 41.7] |
| VOL-I/p4/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-I/p4/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-I/p4/s005 | FOOTER-PAGE | Page 4 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-I/p5/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-I/p5/s002 | HEADER-TITLE | Volume I — Instructions to Bidders | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 161.4, 41.7] |
| VOL-I/p5/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-I/p5/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-I/p5/s005 | FOOTER-PAGE | Page 5 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-I/p6/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-I/p6/s002 | HEADER-TITLE | Volume I — Instructions to Bidders | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 161.4, 41.7] |
| VOL-I/p6/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-I/p6/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-I/p6/s005 | FOOTER-PAGE | Page 6 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-I/p7/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-I/p7/s002 | HEADER-TITLE | Volume I — Instructions to Bidders | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 161.4, 41.7] |
| VOL-I/p7/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-I/p7/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-I/p7/s005 | FOOTER-PAGE | Page 7 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-II/p1/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-II/p1/s002 | HEADER-TITLE | Volume II — Technical Requirements (extract) | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 196.1, 41.7] |
| VOL-II/p1/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-II/p1/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-II/p1/s005 | FOOTER-PAGE | Page 1 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-II/p2/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-II/p2/s002 | HEADER-TITLE | Volume II — Technical Requirements (extract) | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 196.1, 41.7] |
| VOL-II/p2/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-II/p2/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-II/p2/s005 | FOOTER-PAGE | Page 2 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-II/p3/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-II/p3/s002 | HEADER-TITLE | Volume II — Technical Requirements (extract) | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 196.1, 41.7] |
| VOL-II/p3/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-II/p3/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-II/p3/s005 | FOOTER-PAGE | Page 3 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-II/p4/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-II/p4/s002 | HEADER-TITLE | Volume II — Technical Requirements (extract) | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 196.1, 41.7] |
| VOL-II/p4/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-II/p4/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-II/p4/s005 | FOOTER-PAGE | Page 4 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-II/p5/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-II/p5/s002 | HEADER-TITLE | Volume II — Technical Requirements (extract) | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 196.1, 41.7] |
| VOL-II/p5/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-II/p5/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-II/p5/s005 | FOOTER-PAGE | Page 5 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-IV/p1/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-IV/p1/s002 | HEADER-TITLE | Volume IV — Form Sheets | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 137.6, 41.7] |
| VOL-IV/p1/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-IV/p1/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-IV/p1/s005 | FOOTER-PAGE | Page 1 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-IV/p2/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-IV/p2/s002 | HEADER-TITLE | Volume IV — Form Sheets | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 137.6, 41.7] |
| VOL-IV/p2/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-IV/p2/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-IV/p2/s005 | FOOTER-PAGE | Page 2 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-IV/p3/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-IV/p3/s002 | HEADER-TITLE | Volume IV — Form Sheets | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 137.6, 41.7] |
| VOL-IV/p3/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-IV/p3/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-IV/p3/s005 | FOOTER-PAGE | Page 3 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-IV/p4/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-IV/p4/s002 | HEADER-TITLE | Volume IV — Form Sheets | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 137.6, 41.7] |
| VOL-IV/p4/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-IV/p4/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-IV/p4/s005 | FOOTER-PAGE | Page 4 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-IV/p5/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-IV/p5/s002 | HEADER-TITLE | Volume IV — Form Sheets | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 137.6, 41.7] |
| VOL-IV/p5/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-IV/p5/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-IV/p5/s005 | FOOTER-PAGE | Page 5 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-IV/p6/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-IV/p6/s002 | HEADER-TITLE | Volume IV — Form Sheets | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 137.6, 41.7] |
| VOL-IV/p6/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-IV/p6/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-IV/p6/s005 | FOOTER-PAGE | Page 6 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-IV/p7/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-IV/p7/s002 | HEADER-TITLE | Volume IV — Form Sheets | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 137.6, 41.7] |
| VOL-IV/p7/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-IV/p7/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-IV/p7/s005 | FOOTER-PAGE | Page 7 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-IV/p8/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-IV/p8/s002 | HEADER-TITLE | Volume IV — Form Sheets | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 137.6, 41.7] |
| VOL-IV/p8/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-IV/p8/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-IV/p8/s005 | FOOTER-PAGE | Page 8 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-IV/p9/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-IV/p9/s002 | HEADER-TITLE | Volume IV — Form Sheets | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 137.6, 41.7] |
| VOL-IV/p9/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-IV/p9/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-IV/p9/s005 | FOOTER-PAGE | Page 9 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-V/p1/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-V/p1/s002 | HEADER-TITLE | Volume V — Draft Project Agreement (extract) | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 196.5, 41.7] |
| VOL-V/p1/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-V/p1/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-V/p1/s005 | FOOTER-PAGE | Page 1 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-V/p2/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-V/p2/s002 | HEADER-TITLE | Volume V — Draft Project Agreement (extract) | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 196.5, 41.7] |
| VOL-V/p2/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-V/p2/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-V/p2/s005 | FOOTER-PAGE | Page 2 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-V/p3/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-V/p3/s002 | HEADER-TITLE | Volume V — Draft Project Agreement (extract) | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 196.5, 41.7] |
| VOL-V/p3/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-V/p3/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-V/p3/s005 | FOOTER-PAGE | Page 3 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| VOL-V/p4/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| VOL-V/p4/s002 | HEADER-TITLE | Volume V — Draft Project Agreement (extract) | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 196.5, 41.7] |
| VOL-V/p4/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| VOL-V/p4/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| VOL-V/p4/s005 | FOOTER-PAGE | Page 4 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| ADD-01/p1/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| ADD-01/p1/s002 | HEADER-TITLE | Addendum No. 1 | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 107.7, 41.7] |
| ADD-01/p1/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| ADD-01/p1/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| ADD-01/p1/s005 | FOOTER-PAGE | Page 1 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| ADD-01/p2/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| ADD-01/p2/s002 | HEADER-TITLE | Addendum No. 1 | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 107.7, 41.7] |
| ADD-01/p2/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| ADD-01/p2/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| ADD-01/p2/s005 | FOOTER-PAGE | Page 2 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| ADD-01/p3/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| ADD-01/p3/s002 | HEADER-TITLE | Addendum No. 1 | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 107.7, 41.7] |
| ADD-01/p3/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| ADD-01/p3/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| ADD-01/p3/s005 | FOOTER-PAGE | Page 3 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| ADD-01/p4/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| ADD-01/p4/s002 | HEADER-TITLE | Addendum No. 1 | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 107.7, 41.7] |
| ADD-01/p4/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| ADD-01/p4/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| ADD-01/p4/s005 | FOOTER-PAGE | Page 4 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| ADD-02/p1/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| ADD-02/p1/s002 | HEADER-TITLE | Addendum No. 2 | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 107.7, 41.7] |
| ADD-02/p1/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| ADD-02/p1/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| ADD-02/p1/s005 | FOOTER-PAGE | Page 1 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| ADD-02/p2/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| ADD-02/p2/s002 | HEADER-TITLE | Addendum No. 2 | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 107.7, 41.7] |
| ADD-02/p2/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| ADD-02/p2/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| ADD-02/p2/s005 | FOOTER-PAGE | Page 2 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| ADD-02/p3/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| ADD-02/p3/s002 | HEADER-TITLE | Addendum No. 2 | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 107.7, 41.7] |
| ADD-02/p3/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| ADD-02/p3/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| ADD-02/p3/s005 | FOOTER-PAGE | Page 3 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| ADD-03/p1/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| ADD-03/p1/s002 | HEADER-TITLE | Addendum No. 3 | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 107.7, 41.7] |
| ADD-03/p1/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| ADD-03/p1/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| ADD-03/p1/s005 | FOOTER-PAGE | Page 1 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
| ADD-03/p2/s001 | WATERMARK | FICTIONAL — ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [92.2, 172.3, 482.6, 653.6] |
| ADD-03/p2/s002 | HEADER-TITLE | Addendum No. 3 | 0.0 | #5a5a5a | 6.8 | [56.7, 32.4, 107.7, 41.7] |
| ADD-03/p2/s003 | HEADER-REF | NUPA/ISTP/2026/014 | 0.0 | #5a5a5a | 6.8 | [472.4, 32.4, 538.6, 41.7] |
| ADD-03/p2/s004 | FOOTER-DISCLAIMER | FICTIONAL DOCUMENT — prepared solely for a Lamar Holding internal capability assessment. Not a real tender. | 0.0 | #5a5a5a | 6.4 | [56.7, 802.4, 380.7, 811.2] |
| ADD-03/p2/s005 | FOOTER-PAGE | Page 2 | 0.0 | #5a5a5a | 6.4 | [518.3, 802.4, 538.6, 811.2] |
