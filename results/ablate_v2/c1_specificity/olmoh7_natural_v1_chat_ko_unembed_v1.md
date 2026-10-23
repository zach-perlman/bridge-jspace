# C1 specificity: J-lens (paper10, olmoh7_natural_v1_chat_ko_v1) vs unembedding (unembed10, olmoh7_natural_v1_chat_ko_unembed_v1)

388 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 99 | 100 | 98 | 99 | |
| - | unedited (unembed10 run) | 99 | 100 | 98 | 99 | |
| L4-8 | paper10 | 95 [91-99] (n=105) | 84 [76-91] (n=89) | 86 [78-92] (n=105) | 90 [81-97] (n=89) | 1 |
| L4-8 | paper10_rot | 94 [90-98] (n=105) | 91 [83-97] (n=89) | 94 [90-98] (n=105) | 97 [92-100] (n=89) | -4 |
| L4-8 | unembed10 | 97 [93-100] (n=105) | 94 [88-99] (n=89) | 87 [80-94] (n=105) | 94 [89-99] (n=89) | 4 |
| L4-8 | unembed10_rot | 96 [92-99] (n=105) | 98 [94-100] (n=89) | 94 [89-98] (n=105) | 100 [100-100] (n=89) | -1 |

L4-8: of the 23 memory-final items paper10 breaks, unembed10 breaks 7 (30%).

Descriptive (no rule). Output from commit c34be5d.
