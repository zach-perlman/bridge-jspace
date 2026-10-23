# d1_verdict / qwen3_32b_jpp_d1_topics_parts

Decisive cell (fixed in advance): context at layer 32 (C's whole copy flips 100% of lookups)

**Verdict:** not interpretable: the positive control fails

Per topic: animals: not interpretable: the positive control fails; elements: not interpretable: the positive control fails; greek: not interpretable: the positive control fails; planets: not interpretable: the positive control fails

Per format: prose: not interpretable: the positive control fails

| family | part | switched [95%] | n |
|---|---|---|---|
| PP | full | 100% [97, 100] | 120 |
| PP | jspace | 5% [2, 10] | 120 |
| PP | not_jspace | 88% [81, 93] | 120 |
| PP | rand_omp | 1% [0, 5] | 120 |
| PM | full | 98% [94, 100] | 120 |
| PM | jspace | 9% [5, 16] | 120 |
| PM | not_jspace | 79% [71, 85] | 120 |
| PM | rand_omp | 0% [-0, 3] | 120 |

By topic (reported, not decisive):

| topic | cell | switched | n |
|---|---|---|---|
| animals | PP_full | 100% [89, 100] | 31 |
| animals | PP_jspace | 13% [5, 29] | 31 |
| animals | PP_not_jspace | 94% [79, 98] | 31 |
| animals | PM_full | 100% [89, 100] | 31 |
| animals | PM_jspace | 23% [11, 40] | 31 |
| animals | PM_not_jspace | 81% [64, 91] | 31 |
| elements | PP_full | 100% [93, 100] | 51 |
| elements | PP_jspace | 2% [0, 10] | 51 |
| elements | PP_not_jspace | 86% [74, 93] | 51 |
| elements | PM_full | 98% [90, 100] | 51 |
| elements | PM_jspace | 4% [1, 13] | 51 |
| elements | PM_not_jspace | 84% [72, 92] | 51 |
| greek | PP_full | 100% [88, 100] | 29 |
| greek | PP_jspace | 3% [1, 17] | 29 |
| greek | PP_not_jspace | 83% [65, 92] | 29 |
| greek | PM_full | 100% [88, 100] | 29 |
| greek | PM_jspace | 7% [2, 22] | 29 |
| greek | PM_not_jspace | 72% [54, 85] | 29 |
| planets | PP_full | 100% [70, 100] | 9 |
| planets | PP_jspace | 0% [0, 30] | 9 |
| planets | PP_not_jspace | 100% [70, 100] | 9 |
| planets | PM_full | 89% [56, 98] | 9 |
| planets | PM_jspace | 0% [0, 30] | 9 |
| planets | PM_not_jspace | 67% [35, 88] | 9 |

By numbers (reported, not decisive):

| numbers | cell | switched | n |
|---|---|---|---|
| digits | PP_full | 100% [94, 100] | 65 |
| digits | PP_jspace | 6% [2, 15] | 65 |
| digits | PP_not_jspace | 91% [81, 96] | 65 |
| digits | PM_full | 97% [89, 99] | 65 |
| digits | PM_jspace | 9% [4, 19] | 65 |
| digits | PM_not_jspace | 78% [67, 87] | 65 |
| words | PP_full | 100% [93, 100] | 55 |
| words | PP_jspace | 4% [1, 12] | 55 |
| words | PP_not_jspace | 85% [74, 92] | 55 |
| words | PM_full | 100% [93, 100] | 55 |
| words | PM_jspace | 9% [4, 20] | 55 |
| words | PM_not_jspace | 80% [68, 88] | 55 |

By format (reported, not decisive):

| format | cell | switched | n |
|---|---|---|---|
| prose | PP_full | 100% [97, 100] | 120 |
| prose | PP_jspace | 5% [2, 10] | 120 |
| prose | PP_not_jspace | 88% [81, 93] | 120 |
| prose | PM_full | 98% [94, 100] | 120 |
| prose | PM_jspace | 9% [5, 16] | 120 |
| prose | PM_not_jspace | 79% [71, 85] | 120 |
