# C1 specificity: J-lens (paper10, olmo3d7_natplus_v1_chat_ko_cand_v1) vs unembedding (unembed10, olmo3d7_natplus_v1_chat_ko_cand_v1)

504 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 100 | |
| L10-14 | paper10 | 82 [76-88] (n=175) | 90 [82-96] (n=77) | 87 [82-92] (n=175) | 94 [87-99] (n=77) | -4 |
| L10-14 | paper10_rot | 91 [87-95] (n=175) | 90 [81-96] (n=77) | 93 [88-97] (n=175) | 99 [96-100] (n=77) | -5 |
| L10-14 | unembed10 | 94 [90-97] (n=175) | 92 [86-97] (n=77) | 98 [96-100] (n=175) | 99 [96-100] (n=77) | -6 |
| L10-14 | unembed10_rot | 93 [89-96] (n=175) | 96 [91-100] (n=77) | 99 [97-100] (n=175) | 100 [100-100] (n=77) | -5 |

L10-14: of the 28 memory-final items paper10 breaks, unembed10 breaks 2 (7%).

Descriptive (no rule). Output from commit 2b95595.
