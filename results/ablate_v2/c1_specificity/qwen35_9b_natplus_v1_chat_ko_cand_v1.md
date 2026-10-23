# C1 specificity: J-lens (paper10, qwen35_9b_natplus_v1_chat_ko_cand_v1) vs unembedding (unembed10, qwen35_9b_natplus_v1_chat_ko_cand_v1)

1116 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 100 | |
| L12-16 | paper10 | 91 [88-94] (n=301) | 89 [85-93] (n=257) | 51 [44-58] (n=301) | 53 [44-61] (n=257) | 38 |
| L12-16 | paper10_rot | 91 [88-94] (n=301) | 91 [88-94] (n=257) | 96 [93-98] (n=301) | 98 [97-100] (n=257) | -5 |
| L12-16 | unembed10 | 94 [91-96] (n=301) | 95 [92-97] (n=257) | 99 [98-100] (n=301) | 100 [100-100] (n=257) | -5 |
| L12-16 | unembed10_rot | 95 [92-97] (n=301) | 97 [95-99] (n=257) | 96 [94-98] (n=301) | 100 [99-100] (n=257) | -2 |

L12-16: of the 266 memory-final items paper10 breaks, unembed10 breaks 1 (0%).

Descriptive (no rule). Output from commit 466b6e0.
