# C1 specificity: J-lens (paper10, natplus_v1_chat_ko_cand_v1) vs unembedding (unembed10, natplus_v1_chat_ko_cand_v1)

1572 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 99 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 99 | |
| L32-40 | paper10 | 95 [92-97] (n=420) | 90 [87-93] (n=366) | 42 [37-48] (n=420) | 42 [35-49] (n=366) | 50 |
| L32-40 | paper10_rot | 96 [95-98] (n=420) | 97 [95-99] (n=366) | 98 [97-99] (n=420) | 98 [96-99] (n=366) | -1 |
| L32-40 | unembed10 | 99 [98-100] (n=420) | 99 [98-100] (n=366) | 99 [97-100] (n=420) | 99 [99-100] (n=366) | -0 |
| L32-40 | unembed10_rot | 99 [97-100] (n=420) | 99 [98-100] (n=366) | 99 [98-100] (n=420) | 98 [97-99] (n=366) | -0 |

L32-40: of the 452 memory-final items paper10 breaks, unembed10 breaks 7 (2%).

Descriptive (no rule). Output from commit 2b95595.
