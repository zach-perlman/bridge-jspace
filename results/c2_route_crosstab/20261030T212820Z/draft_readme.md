# DRAFT, not applied (post hoc; Dan 30 Oct). Source: results/c2_route_crosstab/20261030T212820Z/tables.json

## Paragraph (3 lines; for Part III, after the address table)

The README's route shares are shares of all scenes; following the same scenes one by one (another item moved, lookup), most of the lookups that took the position route under the whole change leave it when the address is removed, and far fewer do when a random part of the same size goes: 9B 131/153 vs 8, 27B 85/101 vs 26, Muse 83/163 vs 5, Lightning 135/166 vs 8, 122B 101/115 vs 14.
Going the other way, lookups that took the identity route and go to the position route are rare without the address (9B 3, 27B 2, Muse 2, Lightning 0, 122B 0 of the scenes), and more common without J++ (9B 35, 27B 36, Muse 8, Lightning 22, 122B 26), each beside its random part (Appendix B, post hoc).
Counts, not a test: the paired differences with 95% intervals (bootstrap over the bridge entity) are in the table.

## Appendix B table (draft)

| | whole = position: n | leave position, without the address | leave position, random part | difference [95% interval] | whole = identity: n | go to position, without J++ | go to position, random part | difference [95% interval] |
|---|---|---|---|---|---|---|---|---|
| 9B | 153 | 131 | 8 | +0.80 [+0.74, +0.87] | 144 | 35 | 17 | +0.12 [+0.07, +0.18] |
| 27B | 101 | 85 | 26 | +0.58 [+0.49, +0.67] | 197 | 36 | 0 | +0.18 [+0.13, +0.23] |
| Muse | 163 | 83 | 5 | +0.48 [+0.40, +0.55] | 131 | 8 | 4 | +0.03 [+0.01, +0.06] |
| Lightning ○ | 166 | 135 | 8 | +0.77 [+0.71, +0.82] | 133 | 22 | 11 | +0.08 [+0.02, +0.15] |
| 122B ○ | 115 | 101 | 14 | +0.76 [+0.67, +0.83] | 184 | 26 | 5 | +0.11 [+0.06, +0.17] |
