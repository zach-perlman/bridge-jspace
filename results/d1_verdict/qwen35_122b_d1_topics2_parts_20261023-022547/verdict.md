# d1_verdict / qwen35_122b_d1_topics2_parts

Decisive cell (chosen from map qwen35_122b_d1_topics2_map): context at layer 24 (C's whole copy flips 99% of lookups)

**Verdict:** does not replicate

Per topic: animals: not interpretable: the positive control fails; elements: does not replicate; greek: does not replicate

Per format: prose: does not replicate

| family | part | switched [95%] | n |
|---|---|---|---|
| PP | full | 99% [97, 100] | 180 |
| PP | jspace | 29% [23, 36] | 180 |
| PP | not_jspace | 75% [68, 81] | 180 |
| PP | rand_omp | 0% [0, 2] | 180 |
| PM | full | 97% [94, 99] | 180 |
| PM | jspace | 38% [31, 45] | 180 |
| PM | not_jspace | 57% [50, 64] | 180 |
| PM | rand_omp | 1% [0, 4] | 180 |

By topic (reported, not decisive):

| topic | cell | switched | n |
|---|---|---|---|
| animals | PP_full | 96% [82, 99] | 28 |
| animals | PP_jspace | 14% [6, 31] | 28 |
| animals | PP_not_jspace | 71% [53, 85] | 28 |
| animals | PM_full | 96% [82, 99] | 28 |
| animals | PM_jspace | 18% [8, 36] | 28 |
| animals | PM_not_jspace | 61% [42, 76] | 28 |
| elements | PP_full | 100% [95, 100] | 73 |
| elements | PP_jspace | 40% [29, 51] | 73 |
| elements | PP_not_jspace | 71% [60, 80] | 73 |
| elements | PM_full | 100% [95, 100] | 73 |
| elements | PM_jspace | 52% [41, 63] | 73 |
| elements | PM_not_jspace | 49% [38, 61] | 73 |
| greek | PP_full | 100% [95, 100] | 79 |
| greek | PP_jspace | 25% [17, 36] | 79 |
| greek | PP_not_jspace | 80% [70, 87] | 79 |
| greek | PM_full | 95% [88, 98] | 79 |
| greek | PM_jspace | 32% [22, 43] | 79 |
| greek | PM_not_jspace | 63% [52, 73] | 79 |

By numbers (reported, not decisive):

| numbers | cell | switched | n |
|---|---|---|---|
| digits | PP_full | 100% [96, 100] | 92 |
| digits | PP_jspace | 28% [20, 38] | 92 |
| digits | PP_not_jspace | 79% [70, 86] | 92 |
| digits | PM_full | 96% [89, 98] | 92 |
| digits | PM_jspace | 37% [28, 47] | 92 |
| digits | PM_not_jspace | 61% [51, 70] | 92 |
| words | PP_full | 99% [94, 100] | 88 |
| words | PP_jspace | 31% [22, 41] | 88 |
| words | PP_not_jspace | 70% [60, 79] | 88 |
| words | PM_full | 99% [94, 100] | 88 |
| words | PM_jspace | 39% [29, 49] | 88 |
| words | PM_not_jspace | 53% [43, 63] | 88 |

By format (reported, not decisive):

| format | cell | switched | n |
|---|---|---|---|
| prose | PP_full | 99% [97, 100] | 180 |
| prose | PP_jspace | 29% [23, 36] | 180 |
| prose | PP_not_jspace | 75% [68, 81] | 180 |
| prose | PM_full | 97% [94, 99] | 180 |
| prose | PM_jspace | 38% [31, 45] | 180 |
| prose | PM_not_jspace | 57% [50, 64] | 180 |
