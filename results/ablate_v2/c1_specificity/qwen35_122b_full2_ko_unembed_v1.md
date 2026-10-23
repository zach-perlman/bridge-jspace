# C1 specificity: J-lens (paper10, qwen35_122b_full2_ko_v1) vs unembedding (unembed10, qwen35_122b_full2_ko_unembed_v1)

758 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M | gap |
|---|---|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 99 | 99 | 99 | 100 | 99 | 99 | |
| - | unedited (unembed10 run) | 99 | 99 | 99 | 100 | 99 | 99 | |
| L39-45 | paper10 | 99 [97-100] (n=143) | 100 [100-100] (n=100) | 87 [79-93] (n=143) | 95 [91-99] (n=100) | 99 [98-100] (n=136) | 91 [84-97] (n=136) | 9 |
| L39-45 | paper10_rot | 99 [97-100] (n=143) | 97 [94-100] (n=100) | 99 [96-100] (n=143) | 98 [95-100] (n=100) | 99 [98-100] (n=136) | 99 [97-100] (n=136) | 0 |
| L39-45 | unembed10 | 99 [97-100] (n=143) | 98 [95-100] (n=100) | 86 [78-92] (n=143) | 96 [91-100] (n=100) | 100 [100-100] (n=136) | 93 [87-97] (n=136) | 8 |
| L39-45 | unembed10_rot | 100 [100-100] (n=143) | 97 [94-100] (n=100) | 98 [96-100] (n=143) | 98 [95-100] (n=100) | 100 [100-100] (n=136) | 99 [96-100] (n=136) | 1 |

L39-45: of the 23 memory-final items paper10 breaks, unembed10 breaks 13 (57%).

Descriptive (no rule). Output from commit 7c7360d.
