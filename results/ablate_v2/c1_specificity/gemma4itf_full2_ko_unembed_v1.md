# C1 specificity: J-lens (paper10, gemma4itf_full2_ko_v1) vs unembedding (unembed10, gemma4itf_full2_ko_unembed_v1)

722 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M | gap |
|---|---|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 100 | 100 | 100 | |
| L11-19 | paper10 | 4 [1-8] (n=141) | 3 [0-7] (n=92) | 4 [0-10] (n=141) | 8 [2-14] (n=92) | 6 [2-11] (n=128) | 6 [1-13] (n=128) | -2 |
| L11-19 | paper10_rot | 3 [1-6] (n=141) | 10 [4-16] (n=92) | 6 [1-13] (n=141) | 3 [0-7] (n=92) | 7 [3-11] (n=128) | 6 [2-11] (n=128) | 1 |
| L11-19 | unembed10 | 9 [5-12] (n=141) | 12 [6-18] (n=92) | 16 [5-29] (n=141) | 12 [4-24] (n=92) | 18 [10-26] (n=128) | 11 [3-21] (n=128) | -4 |
| L11-19 | unembed10_rot | 6 [3-10] (n=141) | 8 [2-15] (n=92) | 5 [1-10] (n=141) | 10 [0-23] (n=92) | 4 [1-8] (n=128) | 7 [2-14] (n=128) | -0 |
| L19-27 | paper10 | 6 [3-10] (n=141) | 8 [2-14] (n=92) | 10 [4-16] (n=141) | 8 [3-14] (n=92) | 5 [1-9] (n=128) | 9 [3-15] (n=128) | -2 |
| L19-27 | paper10_rot | 30 [23-38] (n=141) | 23 [14-30] (n=92) | 26 [16-35] (n=141) | 46 [32-60] (n=92) | 33 [25-41] (n=128) | 42 [32-54] (n=128) | -9 |
| L19-27 | unembed10 | 100 [100-100] (n=141) | 95 [89-99] (n=92) | 85 [77-92] (n=141) | 93 [89-98] (n=92) | 97 [93-100] (n=128) | 85 [78-92] (n=128) | 8 |
| L19-27 | unembed10_rot | 8 [5-11] (n=141) | 10 [4-16] (n=92) | 14 [7-23] (n=141) | 41 [25-57] (n=92) | 16 [10-21] (n=128) | 29 [19-39] (n=128) | -19 |
| L48-56 | paper10 | 7 [2-13] (n=141) | 7 [2-12] (n=92) | 10 [4-17] (n=141) | 7 [1-12] (n=92) | 9 [4-14] (n=128) | 14 [7-23] (n=128) | -1 |
| L48-56 | paper10_rot | 100 [100-100] (n=141) | 100 [100-100] (n=92) | 100 [100-100] (n=141) | 100 [100-100] (n=92) | 99 [98-100] (n=128) | 100 [100-100] (n=128) | 0 |
| L48-56 | unembed10 | 0 [0-0] (n=141) | 0 [0-0] (n=92) | 0 [0-0] (n=141) | 0 [0-0] (n=92) | 0 [0-0] (n=128) | 0 [0-0] (n=128) | 0 |
| L48-56 | unembed10_rot | 0 [0-0] (n=141) | 0 [0-0] (n=92) | 0 [0-0] (n=141) | 0 [0-0] (n=92) | 0 [0-0] (n=128) | 0 [0-0] (n=128) | 0 |

L11-19: of the 220 memory-final items paper10 breaks, unembed10 breaks 187 (85%).
L19-27: of the 212 memory-final items paper10 breaks, unembed10 breaks 22 (10%).
L48-56: of the 213 memory-final items paper10 breaks, unembed10 breaks 213 (100%).

Descriptive (no rule). Output from commit 1249d90.
