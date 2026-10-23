# C1 specificity: J-lens (paper10, qwen35_9b_natural_v1_chat_ko_v1) vs unembedding (unembed10, qwen35_9b_natural_v1_chat_ko_unembed_v1)

712 items in both runs (0 whose unedited answer differs between them). Accuracy % on the whole question [95% CI over bridge entities]; gap = memory-final minus prompt-final loss (points).

| band | condition | P->P | M->P | P->M | M->M | gap |
|---|---|---|---|---|---|---|
| - | unedited (paper10 run) | 99 | 100 | 100 | 100 | |
| - | unedited (unembed10 run) | 99 | 100 | 100 | 100 | |
| L12-16 | paper10 | 86 [80-92] (n=175) | 92 [88-96] (n=181) | 45 [36-54] (n=175) | 61 [50-70] (n=181) | 37 |
| L12-16 | paper10_rot | 89 [84-94] (n=175) | 95 [91-98] (n=181) | 98 [96-100] (n=175) | 99 [98-100] (n=181) | -6 |
| L12-16 | unembed10 | 92 [88-96] (n=175) | 96 [92-99] (n=181) | 99 [97-100] (n=175) | 99 [97-100] (n=181) | -5 |
| L12-16 | unembed10_rot | 89 [84-93] (n=175) | 97 [94-99] (n=181) | 98 [95-99] (n=175) | 99 [98-100] (n=181) | -6 |

L12-16: of the 168 memory-final items paper10 breaks, unembed10 breaks 3 (2%).

Descriptive (no rule). Output from commit d2cbf82.
