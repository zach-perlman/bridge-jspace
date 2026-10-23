# C1 specificity: J-lens (paper10, muse30_natplus_v1_chat_ko_cand_v1) vs unembedding (unembed10, muse30_natplus_v1_chat_ko_cand_v1)

984 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 100 | |
| L36-42 | paper10 | 97 [95-99] (n=281) | 98 [96-100] (n=211) | 30 [24-37] (n=281) | 38 [30-46] (n=211) | 63 |
| L36-42 | paper10_rot | 97 [95-99] (n=281) | 97 [94-99] (n=211) | 98 [96-99] (n=281) | 98 [95-100] (n=211) | -1 |
| L36-42 | unembed10 | 95 [92-98] (n=281) | 98 [95-99] (n=211) | 49 [41-57] (n=281) | 65 [57-73] (n=211) | 39 |
| L36-42 | unembed10_rot | 96 [94-98] (n=281) | 96 [94-99] (n=211) | 98 [96-100] (n=281) | 99 [98-100] (n=211) | -2 |

L36-42: of the 326 memory-final items paper10 breaks, unembed10 breaks 205 (63%).

Descriptive (no rule). Output from commit df93f52.
