# d1_verdict / qwen35_9b_d1_formats_parts

Decisive cell (chosen from map qwen35_9b_d1_formats_map): context at layer 16 (C's whole copy flips 60% of lookups)

**Verdict:** replicates

Per topic: animals: replicates; elements: replicates; greek: replicates

Per format: json: replicates; table: replicates

| family | part | switched [95%] | n |
|---|---|---|---|
| PP | full | 60% [53, 67] | 180 |
| PP | jspace | 0% [0, 2] | 180 |
| PP | not_jspace | 58% [50, 65] | 180 |
| PP | rand_omp | 0% [0, 2] | 180 |
| PM | full | 66% [58, 72] | 180 |
| PM | jspace | 62% [55, 69] | 180 |
| PM | not_jspace | 11% [7, 17] | 180 |
| PM | rand_omp | 0% [0, 2] | 180 |

By topic (reported, not decisive):

| topic | cell | switched | n |
|---|---|---|---|
| animals | PP_full | 50% [36, 64] | 42 |
| animals | PP_jspace | 0% [0, 8] | 42 |
| animals | PP_not_jspace | 50% [36, 64] | 42 |
| animals | PM_full | 57% [42, 71] | 42 |
| animals | PM_jspace | 45% [31, 60] | 42 |
| animals | PM_not_jspace | 29% [17, 44] | 42 |
| elements | PP_full | 61% [51, 71] | 93 |
| elements | PP_jspace | 0% [0, 4] | 93 |
| elements | PP_not_jspace | 58% [48, 68] | 93 |
| elements | PM_full | 69% [59, 77] | 93 |
| elements | PM_jspace | 72% [62, 80] | 93 |
| elements | PM_not_jspace | 4% [2, 11] | 93 |
| greek | PP_full | 67% [52, 79] | 45 |
| greek | PP_jspace | 0% [0, 8] | 45 |
| greek | PP_not_jspace | 64% [50, 77] | 45 |
| greek | PM_full | 67% [52, 79] | 45 |
| greek | PM_jspace | 58% [43, 71] | 45 |
| greek | PM_not_jspace | 9% [4, 21] | 45 |

By numbers (reported, not decisive):

| numbers | cell | switched | n |
|---|---|---|---|
| digits | PP_full | 64% [54, 72] | 108 |
| digits | PP_jspace | 0% [0, 3] | 108 |
| digits | PP_not_jspace | 61% [52, 70] | 108 |
| digits | PM_full | 68% [58, 76] | 108 |
| digits | PM_jspace | 66% [56, 74] | 108 |
| digits | PM_not_jspace | 11% [6, 18] | 108 |
| words | PP_full | 54% [43, 65] | 72 |
| words | PP_jspace | 0% [0, 5] | 72 |
| words | PP_not_jspace | 53% [41, 64] | 72 |
| words | PM_full | 62% [51, 73] | 72 |
| words | PM_jspace | 57% [45, 68] | 72 |
| words | PM_not_jspace | 11% [6, 20] | 72 |

By format (reported, not decisive):

| format | cell | switched | n |
|---|---|---|---|
| json | PP_full | 60% [49, 69] | 87 |
| json | PP_jspace | 0% [0, 4] | 87 |
| json | PP_not_jspace | 57% [47, 67] | 87 |
| json | PM_full | 67% [56, 76] | 87 |
| json | PM_jspace | 59% [48, 68] | 87 |
| json | PM_not_jspace | 14% [8, 23] | 87 |
| table | PP_full | 60% [50, 70] | 93 |
| table | PP_jspace | 0% [0, 4] | 93 |
| table | PP_not_jspace | 58% [48, 68] | 93 |
| table | PM_full | 65% [54, 73] | 93 |
| table | PM_jspace | 66% [55, 74] | 93 |
| table | PM_not_jspace | 9% [4, 16] | 93 |
