# d1_verdict / qwen36_27b_jlens_d1_topics2_parts

Decisive cell (fixed in advance): context at layer 32 (C's whole copy flips 81% of lookups)

**Verdict:** not interpretable: the positive control fails

Per topic: animals: replicates; elements: not interpretable: the positive control fails; greek: not interpretable: the positive control fails

Per format: prose: not interpretable: the positive control fails

| family | part | switched [95%] | n |
|---|---|---|---|
| PP | full | 83% [77, 88] | 180 |
| PP | jspace | 0% [0, 2] | 180 |
| PP | not_jspace | 81% [74, 86] | 180 |
| PP | rand_omp | 0% [0, 2] | 180 |
| PM | full | 78% [71, 83] | 180 |
| PM | jspace | 18% [13, 24] | 180 |
| PM | not_jspace | 56% [49, 63] | 180 |
| PM | rand_omp | 0% [0, 2] | 180 |

By topic (reported, not decisive):

| topic | cell | switched | n |
|---|---|---|---|
| animals | PP_full | 79% [65, 89] | 43 |
| animals | PP_jspace | 0% [0, 8] | 43 |
| animals | PP_not_jspace | 72% [57, 83] | 43 |
| animals | PM_full | 79% [65, 89] | 43 |
| animals | PM_jspace | 37% [24, 52] | 43 |
| animals | PM_not_jspace | 44% [30, 59] | 43 |
| elements | PP_full | 80% [69, 87] | 74 |
| elements | PP_jspace | 0% [0, 5] | 74 |
| elements | PP_not_jspace | 82% [72, 89] | 74 |
| elements | PM_full | 77% [66, 85] | 74 |
| elements | PM_jspace | 15% [9, 25] | 74 |
| elements | PM_not_jspace | 72% [60, 81] | 74 |
| greek | PP_full | 89% [79, 95] | 63 |
| greek | PP_jspace | 0% [-0, 6] | 63 |
| greek | PP_not_jspace | 84% [73, 91] | 63 |
| greek | PM_full | 78% [66, 86] | 63 |
| greek | PM_jspace | 8% [3, 17] | 63 |
| greek | PM_not_jspace | 46% [34, 58] | 63 |

By numbers (reported, not decisive):

| numbers | cell | switched | n |
|---|---|---|---|
| digits | PP_full | 83% [74, 89] | 92 |
| digits | PP_jspace | 0% [-0, 4] | 92 |
| digits | PP_not_jspace | 83% [74, 89] | 92 |
| digits | PM_full | 74% [64, 82] | 92 |
| digits | PM_jspace | 18% [12, 28] | 92 |
| digits | PM_not_jspace | 60% [50, 69] | 92 |
| words | PP_full | 83% [74, 89] | 88 |
| words | PP_jspace | 0% [0, 4] | 88 |
| words | PP_not_jspace | 78% [69, 86] | 88 |
| words | PM_full | 82% [72, 88] | 88 |
| words | PM_jspace | 17% [11, 26] | 88 |
| words | PM_not_jspace | 52% [42, 62] | 88 |

By format (reported, not decisive):

| format | cell | switched | n |
|---|---|---|---|
| prose | PP_full | 83% [77, 88] | 180 |
| prose | PP_jspace | 0% [0, 2] | 180 |
| prose | PP_not_jspace | 81% [74, 86] | 180 |
| prose | PM_full | 78% [71, 83] | 180 |
| prose | PM_jspace | 18% [13, 24] | 180 |
| prose | PM_not_jspace | 56% [49, 63] | 180 |
