# d1_verdict / qwen3_32b_d1_topics_parts

Decisive cell (map qwen3_32b_d1_topics_map): context at layer 32 (C's whole copy flips 100% of lookups)

**Verdict:** not interpretable: the positive control fails

| family | part | switched [95%] | n |
|---|---|---|---|
| PP | full | 100% [97, 100] | 120 |
| PP | jspace | 3% [1, 8] | 120 |
| PP | not_jspace | 92% [86, 96] | 120 |
| PP | rand_omp | 1% [0, 5] | 120 |
| PM | full | 98% [94, 100] | 120 |
| PM | jspace | 5% [2, 10] | 120 |
| PM | not_jspace | 88% [80, 92] | 120 |
| PM | rand_omp | 0% [-0, 3] | 120 |

By topic (reported, not decisive):

| topic | cell | switched | n |
|---|---|---|---|
| animals | PP_full | 100% [89, 100] | 31 |
| animals | PP_jspace | 10% [3, 25] | 31 |
| animals | PP_not_jspace | 94% [79, 98] | 31 |
| animals | PM_full | 100% [89, 100] | 31 |
| animals | PM_jspace | 16% [7, 33] | 31 |
| animals | PM_not_jspace | 81% [64, 91] | 31 |
| elements | PP_full | 100% [93, 100] | 51 |
| elements | PP_jspace | 2% [0, 10] | 51 |
| elements | PP_not_jspace | 92% [81, 97] | 51 |
| elements | PM_full | 98% [90, 100] | 51 |
| elements | PM_jspace | 2% [0, 10] | 51 |
| elements | PM_not_jspace | 92% [81, 97] | 51 |
| greek | PP_full | 100% [88, 100] | 29 |
| greek | PP_jspace | 0% [0, 12] | 29 |
| greek | PP_not_jspace | 90% [74, 96] | 29 |
| greek | PM_full | 100% [88, 100] | 29 |
| greek | PM_jspace | 0% [0, 12] | 29 |
| greek | PM_not_jspace | 90% [74, 96] | 29 |
| planets | PP_full | 100% [70, 100] | 9 |
| planets | PP_jspace | 0% [0, 30] | 9 |
| planets | PP_not_jspace | 100% [70, 100] | 9 |
| planets | PM_full | 89% [56, 98] | 9 |
| planets | PM_jspace | 0% [0, 30] | 9 |
| planets | PM_not_jspace | 78% [45, 94] | 9 |

By numbers (reported, not decisive):

| numbers | cell | switched | n |
|---|---|---|---|
| digits | PP_full | 100% [94, 100] | 65 |
| digits | PP_jspace | 3% [1, 11] | 65 |
| digits | PP_not_jspace | 95% [87, 98] | 65 |
| digits | PM_full | 97% [89, 99] | 65 |
| digits | PM_jspace | 5% [2, 13] | 65 |
| digits | PM_not_jspace | 86% [76, 93] | 65 |
| words | PP_full | 100% [93, 100] | 55 |
| words | PP_jspace | 4% [1, 12] | 55 |
| words | PP_not_jspace | 89% [78, 95] | 55 |
| words | PM_full | 100% [93, 100] | 55 |
| words | PM_jspace | 5% [2, 15] | 55 |
| words | PM_not_jspace | 89% [78, 95] | 55 |
