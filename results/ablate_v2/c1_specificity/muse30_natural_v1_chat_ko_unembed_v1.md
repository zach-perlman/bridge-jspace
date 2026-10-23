# C1 specificity: J-lens (paper10, muse30_natural_v1_chat_ko_v1) vs unembedding (unembed10, muse30_natural_v1_chat_ko_unembed_v1)

556 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 99 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 99 | 100 | 100 | 100 | |
| L36-42 | paper10 | 91 [85-96] (n=136) | 97 [92-100] (n=142) | 9 [4-15] (n=136) | 11 [5-18] (n=142) | 85 |
| L36-42 | paper10_rot | 98 [95-100] (n=136) | 94 [89-98] (n=142) | 96 [92-99] (n=136) | 97 [93-100] (n=142) | -1 |
| L36-42 | unembed10 | 82 [75-89] (n=136) | 94 [88-98] (n=142) | 20 [13-28] (n=136) | 46 [36-57] (n=142) | 55 |
| L36-42 | unembed10_rot | 97 [94-99] (n=136) | 93 [88-97] (n=142) | 99 [97-100] (n=136) | 96 [92-99] (n=142) | -2 |

L36-42: of the 251 memory-final items paper10 breaks, unembed10 breaks 185 (74%).

Descriptive (no rule). Output from commit 07f486e.
