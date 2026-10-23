# C1 specificity: J-lens (paper10, olmo3d7_full2_ko_v1) vs unembedding (unembed10, olmo3d7_full2_ko_unembed_v1)

258 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M | gap |
|---|---|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 95 | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 95 | 100 | 100 | 100 | 100 | |
| L6-10 | paper10 | 86 [77-95] (n=66) | 85 [74-95] (n=20) | 95 [88-100] (n=66) | 90 [70-100] (n=20) | 91 [81-100] (n=43) | 86 [77-95] (n=43) | -5 |
| L6-10 | paper10_rot | 94 [84-100] (n=66) | 95 [80-100] (n=20) | 97 [91-100] (n=66) | 100 [100-100] (n=20) | 100 [100-100] (n=43) | 95 [90-100] (n=43) | -2 |
| L6-10 | unembed10 | 100 [100-100] (n=66) | 95 [89-100] (n=20) | 98 [94-100] (n=66) | 100 [100-100] (n=20) | 100 [100-100] (n=43) | 91 [84-97] (n=43) | 1 |
| L6-10 | unembed10_rot | 95 [89-100] (n=66) | 95 [89-100] (n=20) | 100 [100-100] (n=66) | 100 [100-100] (n=20) | 100 [100-100] (n=43) | 95 [89-100] (n=43) | -2 |
| L10-14 | paper10 | 91 [80-98] (n=66) | 80 [67-100] (n=20) | 92 [86-98] (n=66) | 95 [80-100] (n=20) | 95 [86-100] (n=43) | 88 [80-95] (n=43) | -6 |
| L10-14 | paper10_rot | 91 [82-98] (n=66) | 95 [80-100] (n=20) | 100 [100-100] (n=66) | 100 [100-100] (n=20) | 95 [89-100] (n=43) | 91 [80-100] (n=43) | -5 |
| L10-14 | unembed10 | 100 [100-100] (n=66) | 100 [100-100] (n=20) | 98 [94-100] (n=66) | 100 [100-100] (n=20) | 100 [100-100] (n=43) | 95 [89-100] (n=43) | 3 |
| L10-14 | unembed10_rot | 97 [92-100] (n=66) | 95 [89-100] (n=20) | 98 [94-100] (n=66) | 100 [100-100] (n=20) | 98 [91-100] (n=43) | 95 [88-100] (n=43) | -1 |

L6-10: of the 5 memory-final items paper10 breaks, unembed10 breaks 1 (20%).
L10-14: of the 6 memory-final items paper10 breaks, unembed10 breaks 1 (17%).

Descriptive (no rule). Output from commit 2d65551.
