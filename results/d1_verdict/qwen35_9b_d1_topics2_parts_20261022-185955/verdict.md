# d1_verdict / qwen35_9b_d1_topics2_parts

Decisive cell (chosen from map qwen35_9b_d1_topics2_map): context at layer 16 (C's whole copy flips 56% of lookups)

**Verdict:** replicates

Per topic: animals: does not replicate; elements: replicates; greek: does not replicate

| family | part | switched [95%] | n |
|---|---|---|---|
| PP | full | 56% [48, 63] | 180 |
| PP | jspace | 1% [0, 3] | 180 |
| PP | not_jspace | 52% [45, 59] | 180 |
| PP | rand_omp | 1% [0, 3] | 180 |
| PM | full | 64% [57, 71] | 180 |
| PM | jspace | 56% [48, 63] | 180 |
| PM | not_jspace | 11% [7, 16] | 180 |
| PM | rand_omp | 0% [0, 2] | 180 |

By topic (reported, not decisive):

| topic | cell | switched | n |
|---|---|---|---|
| animals | PP_full | 54% [38, 69] | 37 |
| animals | PP_jspace | 3% [0, 14] | 37 |
| animals | PP_not_jspace | 49% [33, 64] | 37 |
| animals | PM_full | 68% [51, 80] | 37 |
| animals | PM_jspace | 54% [38, 69] | 37 |
| animals | PM_not_jspace | 16% [8, 31] | 37 |
| elements | PP_full | 59% [48, 69] | 78 |
| elements | PP_jspace | 0% [0, 5] | 78 |
| elements | PP_not_jspace | 56% [45, 67] | 78 |
| elements | PM_full | 68% [57, 77] | 78 |
| elements | PM_jspace | 63% [52, 73] | 78 |
| elements | PM_not_jspace | 5% [2, 12] | 78 |
| greek | PP_full | 52% [40, 64] | 65 |
| greek | PP_jspace | 0% [0, 6] | 65 |
| greek | PP_not_jspace | 49% [37, 61] | 65 |
| greek | PM_full | 57% [45, 68] | 65 |
| greek | PM_jspace | 48% [36, 60] | 65 |
| greek | PM_not_jspace | 14% [7, 24] | 65 |

By numbers (reported, not decisive):

| numbers | cell | switched | n |
|---|---|---|---|
| digits | PP_full | 51% [41, 61] | 88 |
| digits | PP_jspace | 1% [0, 6] | 88 |
| digits | PP_not_jspace | 47% [37, 57] | 88 |
| digits | PM_full | 61% [51, 71] | 88 |
| digits | PM_jspace | 48% [38, 58] | 88 |
| digits | PM_not_jspace | 12% [7, 21] | 88 |
| words | PP_full | 60% [50, 69] | 92 |
| words | PP_jspace | 0% [-0, 4] | 92 |
| words | PP_not_jspace | 58% [47, 67] | 92 |
| words | PM_full | 66% [56, 75] | 92 |
| words | PM_jspace | 63% [53, 72] | 92 |
| words | PM_not_jspace | 9% [4, 16] | 92 |
