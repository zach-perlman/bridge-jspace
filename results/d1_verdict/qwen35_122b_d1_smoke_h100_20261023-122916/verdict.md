# d1_verdict / qwen35_122b_d1_smoke_h100

Decisive cell (fixed in advance): bind_bridge at layer 30 (C's whole copy flips 78% of lookups)

**Verdict:** does not replicate

Per topic: animals: does not replicate; elements: does not replicate; greek: not interpretable: the positive control fails

Per format: prose: does not replicate

| family | part | switched [95%] | n |
|---|---|---|---|
| PP | full | 79% [72, 84] | 180 |
| PP | jspace | 15% [11, 21] | 180 |
| PP | not_jspace | 40% [33, 47] | 180 |
| PP | rand_omp | 1% [0, 3] | 180 |
| PM | full | 94% [90, 97] | 180 |
| PM | jspace | 37% [30, 44] | 180 |
| PM | not_jspace | 49% [42, 56] | 180 |
| PM | rand_omp | 1% [0, 4] | 180 |

By topic (reported, not decisive):

| topic | cell | switched | n |
|---|---|---|---|
| animals | PP_full | 79% [60, 90] | 28 |
| animals | PP_jspace | 7% [2, 23] | 28 |
| animals | PP_not_jspace | 36% [21, 54] | 28 |
| animals | PM_full | 89% [73, 96] | 28 |
| animals | PM_jspace | 39% [24, 58] | 28 |
| animals | PM_not_jspace | 32% [18, 51] | 28 |
| elements | PP_full | 77% [66, 85] | 73 |
| elements | PP_jspace | 15% [9, 25] | 73 |
| elements | PP_not_jspace | 33% [23, 44] | 73 |
| elements | PM_full | 97% [91, 99] | 73 |
| elements | PM_jspace | 48% [37, 59] | 73 |
| elements | PM_not_jspace | 41% [31, 53] | 73 |
| greek | PP_full | 81% [71, 88] | 79 |
| greek | PP_jspace | 18% [11, 28] | 79 |
| greek | PP_not_jspace | 48% [37, 59] | 79 |
| greek | PM_full | 94% [86, 97] | 79 |
| greek | PM_jspace | 25% [17, 36] | 79 |
| greek | PM_not_jspace | 62% [51, 72] | 79 |

By numbers (reported, not decisive):

| numbers | cell | switched | n |
|---|---|---|---|
| digits | PP_full | 79% [70, 86] | 92 |
| digits | PP_jspace | 14% [8, 23] | 92 |
| digits | PP_not_jspace | 40% [31, 50] | 92 |
| digits | PM_full | 95% [88, 98] | 92 |
| digits | PM_jspace | 37% [28, 47] | 92 |
| digits | PM_not_jspace | 51% [41, 61] | 92 |
| words | PP_full | 78% [69, 86] | 88 |
| words | PP_jspace | 16% [10, 25] | 88 |
| words | PP_not_jspace | 40% [30, 50] | 88 |
| words | PM_full | 94% [87, 98] | 88 |
| words | PM_jspace | 36% [27, 47] | 88 |
| words | PM_not_jspace | 47% [37, 57] | 88 |

By format (reported, not decisive):

| format | cell | switched | n |
|---|---|---|---|
| prose | PP_full | 79% [72, 84] | 180 |
| prose | PP_jspace | 15% [11, 21] | 180 |
| prose | PP_not_jspace | 40% [33, 47] | 180 |
| prose | PM_full | 94% [90, 97] | 180 |
| prose | PM_jspace | 37% [30, 44] | 180 |
| prose | PM_not_jspace | 49% [42, 56] | 180 |
