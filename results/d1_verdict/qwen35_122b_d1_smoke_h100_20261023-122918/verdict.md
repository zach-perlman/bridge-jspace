# d1_verdict / qwen35_122b_d1_smoke_h100

Decisive cell (fixed in advance): context at layer 30 (C's whole copy flips 98% of lookups)

**Verdict:** not interpretable: the positive control fails

Per topic: animals: not interpretable: the positive control fails; elements: does not replicate; greek: not interpretable: the positive control fails

Per format: prose: not interpretable: the positive control fails

| family | part | switched [95%] | n |
|---|---|---|---|
| PP | full | 98% [95, 99] | 180 |
| PP | jspace | 16% [11, 22] | 180 |
| PP | not_jspace | 89% [83, 93] | 180 |
| PP | rand_omp | 1% [0, 4] | 180 |
| PM | full | 97% [93, 98] | 180 |
| PM | jspace | 29% [23, 36] | 180 |
| PM | not_jspace | 59% [52, 66] | 180 |
| PM | rand_omp | 1% [0, 4] | 180 |

By topic (reported, not decisive):

| topic | cell | switched | n |
|---|---|---|---|
| animals | PP_full | 93% [77, 98] | 28 |
| animals | PP_jspace | 11% [4, 27] | 28 |
| animals | PP_not_jspace | 79% [60, 90] | 28 |
| animals | PM_full | 96% [82, 99] | 28 |
| animals | PM_jspace | 25% [13, 43] | 28 |
| animals | PM_not_jspace | 39% [24, 58] | 28 |
| elements | PP_full | 100% [95, 100] | 73 |
| elements | PP_jspace | 14% [8, 23] | 73 |
| elements | PP_not_jspace | 90% [82, 95] | 73 |
| elements | PM_full | 100% [95, 100] | 73 |
| elements | PM_jspace | 38% [28, 50] | 73 |
| elements | PM_not_jspace | 59% [47, 69] | 73 |
| greek | PP_full | 99% [93, 100] | 79 |
| greek | PP_jspace | 20% [13, 30] | 79 |
| greek | PP_not_jspace | 91% [83, 96] | 79 |
| greek | PM_full | 94% [86, 97] | 79 |
| greek | PM_jspace | 23% [15, 33] | 79 |
| greek | PM_not_jspace | 67% [56, 76] | 79 |

By numbers (reported, not decisive):

| numbers | cell | switched | n |
|---|---|---|---|
| digits | PP_full | 98% [92, 99] | 92 |
| digits | PP_jspace | 15% [9, 24] | 92 |
| digits | PP_not_jspace | 95% [88, 98] | 92 |
| digits | PM_full | 96% [89, 98] | 92 |
| digits | PM_jspace | 36% [27, 46] | 92 |
| digits | PM_not_jspace | 60% [50, 69] | 92 |
| words | PP_full | 99% [94, 100] | 88 |
| words | PP_jspace | 17% [11, 26] | 88 |
| words | PP_not_jspace | 83% [74, 89] | 88 |
| words | PM_full | 98% [92, 99] | 88 |
| words | PM_jspace | 23% [15, 33] | 88 |
| words | PM_not_jspace | 59% [49, 69] | 88 |

By format (reported, not decisive):

| format | cell | switched | n |
|---|---|---|---|
| prose | PP_full | 98% [95, 99] | 180 |
| prose | PP_jspace | 16% [11, 22] | 180 |
| prose | PP_not_jspace | 89% [83, 93] | 180 |
| prose | PM_full | 97% [93, 98] | 180 |
| prose | PM_jspace | 29% [23, 36] | 180 |
| prose | PM_not_jspace | 59% [52, 66] | 180 |
