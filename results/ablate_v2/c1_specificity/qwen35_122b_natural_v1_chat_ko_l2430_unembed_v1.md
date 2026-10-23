# C1 specificity: J-lens (paper10, qwen35_122b_natural_v1_chat_ko_l2430_v1) vs unembedding (unembed10, qwen35_122b_natural_v1_chat_ko_l2430_unembed_v1)

926 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 99 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 99 | 100 | 100 | |
| L24-30 | paper10 | 11 [7-15] (n=231) | 10 [6-15] (n=232) | 1 [0-3] (n=231) | 3 [2-6] (n=232) | 9 |
| L24-30 | paper10_rot | 95 [92-98] (n=231) | 95 [92-98] (n=232) | 98 [96-100] (n=231) | 99 [97-100] (n=232) | -3 |
| L24-30 | unembed10 | 97 [94-99] (n=231) | 97 [94-98] (n=232) | 99 [98-100] (n=231) | 99 [98-100] (n=232) | -2 |
| L24-30 | unembed10_rot | 97 [95-99] (n=231) | 96 [93-99] (n=232) | 99 [97-100] (n=231) | 100 [99-100] (n=232) | -2 |

L24-30: of the 452 memory-final items paper10 breaks, unembed10 breaks 4 (1%).

Descriptive (no rule). Output from commit 07f486e.
