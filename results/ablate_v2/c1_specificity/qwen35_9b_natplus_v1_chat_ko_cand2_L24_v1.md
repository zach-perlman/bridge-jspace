# C1 specificity: J-lens (paper10, qwen35_9b_natplus_v1_chat_ko_cand2_L24_v1) vs unembedding (unembed10, qwen35_9b_natplus_v1_chat_ko_cand2_L24_v1)

1194 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 100 | |
| L24-28 | paper10 | 80 [75-84] (n=302) | 72 [67-78] (n=295) | 37 [29-44] (n=302) | 35 [27-43] (n=295) | 40 |
| L24-28 | paper10_rot | 97 [96-99] (n=302) | 96 [94-98] (n=295) | 97 [95-99] (n=302) | 98 [96-99] (n=295) | -1 |
| L24-28 | unembed10 | 89 [86-92] (n=302) | 87 [83-91] (n=295) | 68 [62-74] (n=302) | 85 [79-90] (n=295) | 11 |
| L24-28 | unembed10_rot | 98 [96-99] (n=302) | 97 [95-99] (n=295) | 98 [96-99] (n=302) | 99 [97-100] (n=295) | -1 |

L24-28: of the 382 memory-final items paper10 breaks, unembed10 breaks 97 (25%).

Descriptive (no rule). Output from commit 9e2913b.
