# The recall under the writes, by item: qwen35_122b_x8_write_g75

After the data, descriptive (Dan 26 Oct ~14:50). Changed recalls (top token not O's answer) by whose legs they give: the item at the target slot, the third slot, the original slot (first match in that order), other. Scenes: the C2 cases of qwen35_122b_x6_routes_g75 (entity and slot checked on every scene). UNVERIFIED.

| arm | s | changed recalls | target item | third item | original item | other |
|---|---|---|---|---|---|---|
| random | 1 | 10 | 3 | 3 | 0 | 4 |
| random | 4 | 19 | 9 | 6 | 0 | 4 |
| write | 1 | 19 | 15 | 2 | 0 | 2 |
| write | 2 | 136 | 109 | 13 | 0 | 14 |
| write | 4 | 268 | 211 | 31 | 0 | 26 |

Writes whose target item has as many legs as the original: 94 of 600 (a followed pointer cannot show as a changed recall there).

Dose at the norm of a real pointer change (median ||U U^T Delta|| = 1.4382): s* = 0-1 1.55, 0-2 1.37, 1-0 1.55, 1-2 2.76, 2-0 1.37, 2-1 2.76. The primary dose s = 1 was below it on every pair: a design error in batch 44, not a finding.
