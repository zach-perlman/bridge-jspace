# The recall under the writes, by item: qwen35_9b_x8_write

After the data, descriptive (Dan 26 Oct ~14:50). Changed recalls (top token not O's answer) by whose legs they give: the item at the target slot, the third slot, the original slot (first match in that order), other. Scenes: the C2 cases of qwen35_9b_x6_routes (entity and slot checked on every scene). UNVERIFIED.

| arm | s | changed recalls | target item | third item | original item | other |
|---|---|---|---|---|---|---|
| random | 1 | 3 | 0 | 1 | 0 | 2 |
| random | 4 | 18 | 5 | 8 | 0 | 5 |
| write | 1 | 24 | 21 | 3 | 0 | 0 |
| write | 2 | 129 | 109 | 12 | 0 | 8 |
| write | 4 | 256 | 205 | 38 | 0 | 13 |

Writes whose target item has as many legs as the original: 93 of 600 (a followed pointer cannot show as a changed recall there).

Dose at the norm of a real pointer change (median ||U U^T Delta|| = 6.5605): s* = 0-1 1.60, 0-2 1.36, 1-0 1.60, 1-2 2.70, 2-0 1.36, 2-1 2.70. The primary dose s = 1 was below it on every pair: a design error in batch 44, not a finding.
