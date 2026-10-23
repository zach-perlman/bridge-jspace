# C1 specificity: J-lens (paper10, muse30_natplus_v1_chat_ko_cand2_v1) vs unembedding (unembed10, muse30_natplus_v1_chat_ko_cand2_v1)

1038 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 100 | |
| L36-42 | paper10 | 97 [95-99] (n=287) | 97 [95-99] (n=232) | 31 [25-38] (n=287) | 37 [28-45] (n=232) | 63 |
| L36-42 | paper10_rot | 97 [95-99] (n=287) | 97 [95-99] (n=232) | 98 [96-99] (n=287) | 97 [95-99] (n=232) | -1 |
| L36-42 | unembed10 | 95 [92-97] (n=287) | 98 [96-100] (n=232) | 49 [42-57] (n=287) | 64 [56-72] (n=232) | 40 |
| L36-42 | unembed10_rot | 97 [95-99] (n=287) | 97 [95-99] (n=232) | 99 [97-100] (n=287) | 99 [97-100] (n=232) | -2 |

L36-42: of the 343 memory-final items paper10 breaks, unembed10 breaks 217 (63%).

Descriptive (no rule). Output from commit 12bdc15.
