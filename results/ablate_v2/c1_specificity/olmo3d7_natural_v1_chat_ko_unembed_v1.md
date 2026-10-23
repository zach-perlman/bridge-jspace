# C1 specificity: J-lens (paper10, olmo3d7_natural_v1_chat_ko_v1) vs unembedding (unembed10, olmo3d7_natural_v1_chat_ko_unembed_v1)

274 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 100 | |
| L10-14 | paper10 | 91 [84-97] (n=75) | 89 [78-96] (n=62) | 68 [56-79] (n=75) | 77 [65-89] (n=62) | 17 |
| L10-14 | paper10_rot | 88 [81-96] (n=75) | 95 [89-100] (n=62) | 80 [69-89] (n=75) | 94 [87-98] (n=62) | 5 |
| L10-14 | unembed10 | 89 [82-97] (n=75) | 95 [87-100] (n=62) | 92 [86-97] (n=75) | 98 [95-100] (n=62) | -3 |
| L10-14 | unembed10_rot | 97 [94-100] (n=75) | 95 [89-100] (n=62) | 92 [84-98] (n=75) | 98 [95-100] (n=62) | 1 |

L10-14: of the 38 memory-final items paper10 breaks, unembed10 breaks 5 (13%).

Descriptive (no rule). Output from commit c34be5d.
