# C1 specificity: J-lens (paper10, nem35l_natplus_v1_chat_ko_cand2_v1) vs unembedding (unembed10, nem35l_natplus_v1_chat_ko_cand2_v1)

1266 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 99 | 99 | 99 | 100 | |
| - | unedited (unembed10 run) | 99 | 99 | 99 | 100 | |
| L27-33 | paper10 | 97 [95-99] (n=304) | 97 [95-99] (n=329) | 37 [31-45] (n=304) | 55 [46-63] (n=329) | 52 |
| L27-33 | paper10_rot | 95 [93-97] (n=304) | 94 [91-97] (n=329) | 94 [91-96] (n=304) | 98 [97-100] (n=329) | -1 |
| L27-33 | unembed10 | 96 [94-98] (n=304) | 97 [95-99] (n=329) | 85 [81-89] (n=304) | 93 [89-96] (n=329) | 8 |
| L27-33 | unembed10_rot | 96 [94-98] (n=304) | 96 [94-98] (n=329) | 91 [87-94] (n=304) | 96 [94-98] (n=329) | 3 |

L27-33: of the 338 memory-final items paper10 breaks, unembed10 breaks 56 (17%).

Descriptive (no rule). Output from commit b83f3cc.
