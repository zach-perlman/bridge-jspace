# C1 specificity: J-lens (paper10, qwen35_122b_natural_v1_chat_ko_cand_v1) vs unembedding (unembed10, qwen35_122b_natural_v1_chat_ko_cand_v1)

950 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 100 | |
| L24-30 | paper10 | 93 [89-96] (n=231) | 84 [79-89] (n=244) | 97 [94-99] (n=231) | 96 [91-100] (n=244) | -8 |
| L24-30 | paper10_rot | 95 [92-97] (n=231) | 95 [91-98] (n=244) | 98 [96-100] (n=231) | 98 [95-100] (n=244) | -3 |
| L24-30 | unembed10 | 96 [93-98] (n=231) | 96 [93-98] (n=244) | 99 [98-100] (n=231) | 98 [97-100] (n=244) | -3 |
| L24-30 | unembed10_rot | 97 [95-99] (n=231) | 96 [93-99] (n=244) | 99 [97-100] (n=231) | 99 [98-100] (n=244) | -2 |

L24-30: of the 17 memory-final items paper10 breaks, unembed10 breaks 3 (18%).

Descriptive (no rule). Output from commit 6ba91f2.
