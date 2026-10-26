# The recall under the writes, by item: x8_write_27b

After the data, descriptive (Dan 26 Oct ~14:50). Changed recalls (top token not O's answer) by whose legs they give: the item at the target slot, the third slot, the original slot (first match in that order), other. Scenes: the C2 cases of x6_routes_27b (entity and slot checked on every scene). UNVERIFIED.

| arm | s | changed recalls | target item | third item | original item | other |
|---|---|---|---|---|---|---|
| random | 4 | 3 | 2 | 0 | 0 | 1 |
| write | 1 | 4 | 1 | 0 | 0 | 3 |
| write | 2 | 26 | 16 | 3 | 0 | 7 |
| write | 4 | 68 | 55 | 6 | 0 | 7 |

Writes whose target item has as many legs as the original: 95 of 600 (a followed pointer cannot show as a changed recall there).

Dose at the norm of a real pointer change (median ||U U^T Delta|| = 17.4325): s* = 0-1 1.28, 0-2 1.04, 1-0 1.28, 1-2 2.08, 2-0 1.04, 2-1 2.08. The primary dose s = 1 was below it on every pair: a design error in batch 44, not a finding.
