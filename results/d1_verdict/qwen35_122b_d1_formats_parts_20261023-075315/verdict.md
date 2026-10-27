# d1_verdict / qwen35_122b_d1_formats_parts

Decisive cell (chosen from map qwen35_122b_d1_formats_map): context at layer 24 (C's whole copy flips 100% of lookups)

**Verdict:** does not replicate

Per topic: animals: does not replicate; elements: does not replicate; greek: not interpretable: the positive control fails

Per format: json: does not replicate; table: does not replicate

| family | part | switched [95%] | n |
|---|---|---|---|
| PP | full | 100% [98, 100] | 180 |
| PP | jspace | 41% [34, 48] | 180 |
| PP | not_jspace | 58% [50, 65] | 180 |
| PP | rand_omp | 1% [0, 3] | 180 |
| PM | full | 99% [97, 100] | 180 |
| PM | jspace | 41% [34, 48] | 180 |
| PM | not_jspace | 58% [50, 65] | 180 |
| PM | rand_omp | 0% [0, 2] | 180 |

By topic (reported, not decisive):

| topic | cell | switched | n |
|---|---|---|---|
| animals | PP_full | 100% [89, 100] | 31 |
| animals | PP_jspace | 52% [35, 68] | 31 |
| animals | PP_not_jspace | 68% [50, 81] | 31 |
| animals | PM_full | 97% [84, 99] | 31 |
| animals | PM_jspace | 52% [35, 68] | 31 |
| animals | PM_not_jspace | 52% [35, 68] | 31 |
| elements | PP_full | 100% [96, 100] | 85 |
| elements | PP_jspace | 46% [36, 56] | 85 |
| elements | PP_not_jspace | 52% [41, 62] | 85 |
| elements | PM_full | 100% [96, 100] | 85 |
| elements | PM_jspace | 47% [37, 58] | 85 |
| elements | PM_not_jspace | 56% [46, 67] | 85 |
| greek | PP_full | 100% [94, 100] | 64 |
| greek | PP_jspace | 30% [20, 42] | 64 |
| greek | PP_not_jspace | 61% [49, 72] | 64 |
| greek | PM_full | 100% [94, 100] | 64 |
| greek | PM_jspace | 28% [19, 40] | 64 |
| greek | PM_not_jspace | 62% [50, 73] | 64 |

By numbers (reported, not decisive):

| numbers | cell | switched | n |
|---|---|---|---|
| digits | PP_full | 100% [96, 100] | 96 |
| digits | PP_jspace | 38% [28, 47] | 96 |
| digits | PP_not_jspace | 62% [53, 72] | 96 |
| digits | PM_full | 99% [94, 100] | 96 |
| digits | PM_jspace | 34% [26, 44] | 96 |
| digits | PM_not_jspace | 58% [48, 68] | 96 |
| words | PP_full | 100% [96, 100] | 84 |
| words | PP_jspace | 45% [35, 56] | 84 |
| words | PP_not_jspace | 52% [42, 63] | 84 |
| words | PM_full | 100% [96, 100] | 84 |
| words | PM_jspace | 49% [38, 59] | 84 |
| words | PM_not_jspace | 57% [46, 67] | 84 |

By format (reported, not decisive):

| format | cell | switched | n |
|---|---|---|---|
| json | PP_full | 100% [96, 100] | 92 |
| json | PP_jspace | 34% [25, 44] | 92 |
| json | PP_not_jspace | 61% [51, 70] | 92 |
| json | PM_full | 100% [96, 100] | 92 |
| json | PM_jspace | 35% [26, 45] | 92 |
| json | PM_not_jspace | 61% [51, 70] | 92 |
| table | PP_full | 100% [96, 100] | 88 |
| table | PP_jspace | 49% [39, 59] | 88 |
| table | PP_not_jspace | 55% [44, 65] | 88 |
| table | PM_full | 99% [94, 100] | 88 |
| table | PM_jspace | 48% [38, 58] | 88 |
| table | PM_not_jspace | 55% [44, 65] | 88 |
