# C1 specificity: J-lens (paper10, olmoh7_natplus_v1_chat_ko_cand_v1) vs unembedding (unembed10, olmoh7_natplus_v1_chat_ko_cand_v1)

770 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 99 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 99 | 100 | 100 | 100 | |
| L4-8 | paper10 | 93 [89-96] (n=261) | 76 [69-84] (n=124) | 92 [89-96] (n=261) | 92 [86-97] (n=124) | -7 |
| L4-8 | paper10_rot | 92 [88-95] (n=261) | 87 [81-93] (n=124) | 97 [95-99] (n=261) | 99 [97-100] (n=124) | -9 |
| L4-8 | unembed10 | 95 [92-98] (n=261) | 93 [88-97] (n=124) | 98 [97-100] (n=261) | 97 [92-100] (n=124) | -3 |
| L4-8 | unembed10_rot | 95 [92-97] (n=261) | 95 [91-98] (n=124) | 97 [94-99] (n=261) | 100 [100-100] (n=124) | -3 |

L4-8: of the 30 memory-final items paper10 breaks, unembed10 breaks 5 (17%).

Descriptive (no rule). Output from commit df93f52.
