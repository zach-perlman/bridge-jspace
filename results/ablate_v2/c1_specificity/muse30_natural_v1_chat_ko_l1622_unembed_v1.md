# C1 specificity: J-lens (paper10, muse30_natural_v1_chat_ko_l1622_v1) vs unembedding (unembed10, muse30_natural_v1_chat_ko_l1622_unembed_v1)

556 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 99 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 99 | 100 | 100 | 100 | |
| L16-22 | paper10 | 91 [86-96] (n=136) | 89 [82-95] (n=142) | 96 [92-99] (n=136) | 95 [91-98] (n=142) | -5 |
| L16-22 | paper10_rot | 85 [77-91] (n=136) | 79 [72-86] (n=142) | 98 [95-100] (n=136) | 96 [92-99] (n=142) | -15 |
| L16-22 | unembed10 | 95 [90-98] (n=136) | 88 [81-94] (n=142) | 97 [94-99] (n=136) | 97 [94-99] (n=142) | -5 |
| L16-22 | unembed10_rot | 96 [92-99] (n=136) | 84 [77-90] (n=142) | 97 [94-99] (n=136) | 99 [96-100] (n=142) | -8 |

L16-22: of the 12 memory-final items paper10 breaks, unembed10 breaks 3 (25%).

Descriptive (no rule). Output from commit 23daf0c.
