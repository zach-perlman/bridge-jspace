# C1 specificity: J-lens (paper10, natplus_v1_chat_ko_cand2_v1) vs unembedding (unembed10, natplus_v1_chat_ko_cand2_v1)

1672 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 100 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 100 | 100 | 100 | 100 | |
| L32-40 | paper10 | 98 [96-99] (n=423) | 90 [87-93] (n=413) | 42 [36-47] (n=423) | 42 [35-49] (n=413) | 52 |
| L32-40 | paper10_rot | 97 [95-98] (n=423) | 98 [96-100] (n=413) | 98 [96-99] (n=423) | 99 [98-100] (n=413) | -1 |
| L32-40 | unembed10 | 99 [98-100] (n=423) | 99 [98-100] (n=413) | 99 [97-100] (n=423) | 99 [98-100] (n=413) | 0 |
| L32-40 | unembed10_rot | 99 [98-100] (n=423) | 99 [98-100] (n=413) | 99 [98-100] (n=423) | 98 [97-100] (n=413) | 0 |

L32-40: of the 484 memory-final items paper10 breaks, unembed10 breaks 9 (2%).

Descriptive (no rule). Output from commit 55e0f9a.
