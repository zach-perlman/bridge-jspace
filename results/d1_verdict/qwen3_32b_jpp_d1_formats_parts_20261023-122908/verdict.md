# d1_verdict / qwen3_32b_jpp_d1_formats_parts

Decisive cell (chosen from map qwen3_32b_jpp_d1_formats_map): context at layer 32 (C's whole copy flips 100% of lookups)

**Verdict:** not interpretable: the positive control fails

Per topic: animals: not interpretable: the positive control fails; elements: not interpretable: the positive control fails; greek: not interpretable: the positive control fails

Per format: json: not interpretable: the positive control fails; table: not interpretable: the positive control fails

| family | part | switched [95%] | n |
|---|---|---|---|
| PP | full | 100% [98, 100] | 180 |
| PP | jspace | 6% [3, 10] | 180 |
| PP | not_jspace | 92% [87, 95] | 180 |
| PP | rand_omp | 0% [0, 2] | 180 |
| PM | full | 100% [98, 100] | 180 |
| PM | jspace | 11% [7, 16] | 180 |
| PM | not_jspace | 88% [83, 92] | 180 |
| PM | rand_omp | 1% [0, 3] | 180 |

By topic (reported, not decisive):

| topic | cell | switched | n |
|---|---|---|---|
| animals | PP_full | 100% [92, 100] | 45 |
| animals | PP_jspace | 7% [2, 18] | 45 |
| animals | PP_not_jspace | 93% [82, 98] | 45 |
| animals | PM_full | 100% [92, 100] | 45 |
| animals | PM_jspace | 22% [13, 36] | 45 |
| animals | PM_not_jspace | 91% [79, 96] | 45 |
| elements | PP_full | 100% [96, 100] | 88 |
| elements | PP_jspace | 6% [2, 13] | 88 |
| elements | PP_not_jspace | 90% [82, 95] | 88 |
| elements | PM_full | 100% [96, 100] | 88 |
| elements | PM_jspace | 2% [1, 8] | 88 |
| elements | PM_not_jspace | 88% [79, 93] | 88 |
| greek | PP_full | 100% [92, 100] | 47 |
| greek | PP_jspace | 4% [1, 14] | 47 |
| greek | PP_not_jspace | 94% [83, 98] | 47 |
| greek | PM_full | 100% [92, 100] | 47 |
| greek | PM_jspace | 15% [7, 28] | 47 |
| greek | PM_not_jspace | 87% [75, 94] | 47 |

By numbers (reported, not decisive):

| numbers | cell | switched | n |
|---|---|---|---|
| digits | PP_full | 100% [96, 100] | 89 |
| digits | PP_jspace | 6% [2, 12] | 89 |
| digits | PP_not_jspace | 91% [83, 95] | 89 |
| digits | PM_full | 100% [96, 100] | 89 |
| digits | PM_jspace | 4% [2, 11] | 89 |
| digits | PM_not_jspace | 87% [78, 92] | 89 |
| words | PP_full | 100% [96, 100] | 91 |
| words | PP_jspace | 5% [2, 12] | 91 |
| words | PP_not_jspace | 92% [85, 96] | 91 |
| words | PM_full | 100% [96, 100] | 91 |
| words | PM_jspace | 16% [10, 25] | 91 |
| words | PM_not_jspace | 90% [82, 95] | 91 |

By format (reported, not decisive):

| format | cell | switched | n |
|---|---|---|---|
| json | PP_full | 100% [96, 100] | 95 |
| json | PP_jspace | 5% [2, 12] | 95 |
| json | PP_not_jspace | 93% [86, 96] | 95 |
| json | PM_full | 100% [96, 100] | 95 |
| json | PM_jspace | 8% [4, 16] | 95 |
| json | PM_not_jspace | 87% [79, 93] | 95 |
| table | PP_full | 100% [96, 100] | 85 |
| table | PP_jspace | 6% [3, 13] | 85 |
| table | PP_not_jspace | 91% [83, 95] | 85 |
| table | PM_full | 100% [96, 100] | 85 |
| table | PM_jspace | 13% [7, 22] | 85 |
| table | PM_not_jspace | 89% [81, 94] | 85 |
