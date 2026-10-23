# C1 specificity: J-lens (paper10, qwen35_9b_natplus_v1_chat_ko_cand2_v1) vs unembedding (unembed10, qwen35_9b_natplus_v1_chat_ko_cand2_v1)

1194 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 100 | |
| L12-16 | paper10 | 92 [89-95] (n=302) | 91 [87-93] (n=295) | 50 [43-57] (n=302) | 51 [44-60] (n=295) | 40 |
| L12-16 | paper10_rot | 91 [88-94] (n=302) | 92 [88-94] (n=295) | 96 [94-98] (n=302) | 98 [95-99] (n=295) | -5 |
| L12-16 | unembed10 | 94 [91-96] (n=302) | 95 [93-98] (n=295) | 99 [98-100] (n=302) | 100 [99-100] (n=295) | -5 |
| L12-16 | unembed10_rot | 95 [92-97] (n=302) | 96 [94-98] (n=295) | 97 [94-99] (n=302) | 100 [99-100] (n=295) | -3 |

L12-16: of the 293 memory-final items paper10 breaks, unembed10 breaks 2 (1%).

Descriptive (no rule). Output from commit a6db0d6.
