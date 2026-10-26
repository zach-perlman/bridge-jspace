# The recall under the writes, by item: muse30b_x8_write

After the data, descriptive (Dan 26 Oct ~14:50). Changed recalls (top token not O's answer) by whose legs they give: the item at the target slot, the third slot, the original slot (first match in that order), other. Scenes: the C2 cases of muse30b_x6_routes (entity and slot checked on every scene). UNVERIFIED.

| arm | s | changed recalls | target item | third item | original item | other |
|---|---|---|---|---|---|---|
| random | 1 | 2 | 1 | 0 | 0 | 1 |
| random | 4 | 6 | 1 | 1 | 0 | 4 |
| write | 1 | 4 | 1 | 0 | 0 | 3 |
| write | 2 | 35 | 18 | 5 | 0 | 12 |
| write | 4 | 64 | 28 | 16 | 0 | 20 |

Writes whose target item has as many legs as the original: 122 of 600 (a followed pointer cannot show as a changed recall there).

Dose at the norm of a real pointer change (median ||U U^T Delta|| = 57.0782): s* = 0-1 1.38, 0-2 1.12, 1-0 1.38, 1-2 2.30, 2-0 1.12, 2-1 2.30. The primary dose s = 1 was below it on every pair: a design error in batch 44, not a finding.
