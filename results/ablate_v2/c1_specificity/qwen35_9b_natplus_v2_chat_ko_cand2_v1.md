# C1 specificity: J-lens (paper10, qwen35_9b_natplus_v2_chat_ko_cand2_v1) vs unembedding (unembed10, qwen35_9b_natplus_v2_chat_ko_cand2_v1)

1214 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 100 | |
| L12-16 | paper10 | 92 [88-94] (n=308) | 88 [84-91] (n=299) | 46 [38-53] (n=308) | 56 [48-64] (n=299) | 39 |
| L12-16 | paper10_rot | 90 [86-93] (n=308) | 95 [93-98] (n=299) | 97 [95-99] (n=308) | 97 [95-99] (n=299) | -4 |
| L12-16 | unembed10 | 94 [91-96] (n=308) | 95 [92-97] (n=299) | 99 [98-100] (n=308) | 99 [98-100] (n=299) | -5 |
| L12-16 | unembed10_rot | 95 [93-97] (n=308) | 95 [92-97] (n=299) | 98 [96-99] (n=308) | 98 [97-100] (n=299) | -3 |

L12-16: of the 299 memory-final items paper10 breaks, unembed10 breaks 4 (1%).

Descriptive (no rule). Output from commit 12bdc15.
