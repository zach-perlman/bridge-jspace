# C1 specificity: J-lens (paper10, natural_v1_chat_ko_v1) vs unembedding (unembed10, natural_v1_chat_ko_unembed_v1)

942 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 99 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 99 | 100 | 100 | 100 | |
| L32-40 | paper10 | 97 [95-99] (n=230) | 89 [85-93] (n=241) | 43 [35-52] (n=230) | 42 [33-51] (n=241) | 51 |
| L32-40 | paper10_rot | 97 [95-99] (n=230) | 95 [92-98] (n=241) | 96 [92-99] (n=230) | 100 [99-100] (n=241) | -1 |
| L32-40 | unembed10 | 99 [98-100] (n=230) | 98 [96-100] (n=241) | 99 [96-100] (n=230) | 100 [99-100] (n=241) | 0 |
| L32-40 | unembed10_rot | 99 [97-100] (n=230) | 98 [96-100] (n=241) | 100 [99-100] (n=230) | 100 [100-100] (n=241) | -1 |

L32-40: of the 271 memory-final items paper10 breaks, unembed10 breaks 4 (1%).

Descriptive (no rule). Output from commit 07f486e.
