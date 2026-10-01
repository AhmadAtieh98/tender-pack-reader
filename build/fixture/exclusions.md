# Excluded text — SYNTHETIC-FIXTURE (not tender content)

Every span below was excluded from content because it matched a declared rule in `config/furniture.yaml` on all of the rule's attributes. Nothing else is excluded; in particular, rotated text that does not match the WATERMARK rule stays content.

## Rules

- **WATERMARK**: diagonal watermark printed on every page. Attributes: `{'text': 'FICTIONAL - ASSESSMENT PACK', 'color': '#dbdbdb', 'size': [30.0, 40.0], 'angle': [47.0, 57.0], 'expect_per_page': 1}`
- **FOOTER-PAGE**: running footer printed page number, bottom margin (captured as printed_page). Attributes: `{'min_y0': 790.0, 'color': '#5a5a5a', 'size': [6.0, 7.5], 'pattern': '^Page (?P<printed_page>[0-9]+)$'}`
- **HEADER-SYN**: synthetic running header. Attributes: `{'max_y1': 45.0, 'color': '#5a5a5a', 'size': [6.0, 7.5], 'pattern': '^Synthetic Test Volume$'}`

## All exclusions (15 spans)

| Span | Rule | Text | Angle | Colour | Size | BBox |
|---|---|---|---|---|---|---|
| SYN-01/p1/s001 | HEADER-SYN | Synthetic Test Volume | 0.0 | #5a5a5a | 6.8 | [62.7, 30.7, 130.7, 40.0] |
| SYN-01/p1/s002 | FOOTER-PAGE | Page 1 | 0.0 | #5a5a5a | 6.4 | [62.7, 799.1, 83.0, 807.9] |
| SYN-01/p1/s003 | WATERMARK | FICTIONAL - ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [121.3, 183.0, 497.8, 646.4] |
| SYN-01/p2/s001 | HEADER-SYN | Synthetic Test Volume | 0.0 | #5a5a5a | 6.8 | [62.7, 30.7, 130.7, 40.0] |
| SYN-01/p2/s002 | FOOTER-PAGE | Page 2 | 0.0 | #5a5a5a | 6.4 | [62.7, 799.1, 83.0, 807.9] |
| SYN-01/p2/s003 | WATERMARK | FICTIONAL - ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [121.3, 183.0, 497.8, 646.4] |
| SYN-01/p3/s001 | HEADER-SYN | Synthetic Test Volume | 0.0 | #5a5a5a | 6.8 | [62.7, 30.7, 130.7, 40.0] |
| SYN-01/p3/s002 | FOOTER-PAGE | Page 3 | 0.0 | #5a5a5a | 6.4 | [62.7, 799.1, 83.0, 807.9] |
| SYN-01/p3/s003 | WATERMARK | FICTIONAL - ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [121.3, 183.0, 497.8, 646.4] |
| SYN-01/p4/s001 | HEADER-SYN | Synthetic Test Volume | 0.0 | #5a5a5a | 6.8 | [62.7, 30.7, 130.7, 40.0] |
| SYN-01/p4/s002 | FOOTER-PAGE | Page 4 | 0.0 | #5a5a5a | 6.4 | [62.7, 799.1, 83.0, 807.9] |
| SYN-01/p4/s003 | WATERMARK | FICTIONAL - ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [121.3, 183.0, 497.8, 646.4] |
| SYN-01/p5/s001 | HEADER-SYN | Synthetic Test Volume | 0.0 | #5a5a5a | 6.8 | [62.7, 30.7, 130.7, 40.0] |
| SYN-01/p5/s002 | FOOTER-PAGE | Page 5 | 0.0 | #5a5a5a | 6.4 | [62.7, 799.1, 83.0, 807.9] |
| SYN-01/p5/s003 | WATERMARK | FICTIONAL - ASSESSMENT PACK | 52.0 | #dbdbdb | 34.0 | [121.3, 183.0, 497.8, 646.4] |
