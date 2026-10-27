# d1_verdict (late-switch) / qwen35_122b_d1_formats_late_parts_r2

Map qwen35_122b_d1_formats_map; decisive cells (in transit for lookups on the map): bind_bridge:30, context:30, context:33, context:36

**Verdict:** inconclusive: the split holds at context:33, context:36 but fails there: context:33 recall_control; context:36 recall_control

Per format (reported): json: inconclusive; table: inconclusive: the split holds at context:33 but fails there: context:33 recall_control

Per topic (reported): animals: inconclusive; elements: inconclusive: the split holds at context:33, context:36 but fails there: context:33 recall_control; context:36 recall_control, subspace_control_recall; greek: inconclusive

| cell | role | map: whole copy flips lookups | family | full | jspace | not_jspace | not_jspace_matched | rand_sub | not_rand_sub | jspace_matched | rand_omp | jspace null | n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bind_bridge:30 | decisive | 82% | PP | 83% [77, 88] | 18% [13, 24] | 32% [25, 39] | 2% [1, 6] | 1% [0, 3] | 58% [51, 65] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:30 | decisive | 82% | PM | 97% [93, 98] | 29% [23, 36] | 46% [38, 53] | 5% [3, 9] | 1% [0, 3] | 86% [80, 90] | 2% [1, 5] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:33 | not in transit | 48% | PP | 47% [40, 54] | 0% [0, 2] | 46% [38, 53] | 11% [7, 16] | 0% [0, 2] | 45% [38, 52] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:33 | not in transit | 48% | PM | 97% [94, 99] | 24% [19, 31] | 61% [53, 67] | 8% [5, 13] | 3% [1, 6] | 92% [87, 95] | 3% [1, 6] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:36 | not in transit | 44% | PP | 44% [37, 52] | 0% [0, 2] | 45% [38, 52] | 9% [6, 15] | 0% [0, 2] | 44% [37, 52] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:36 | not in transit | 44% | PM | 81% [75, 86] | 12% [8, 17] | 56% [48, 63] | 6% [3, 10] | 2% [1, 5] | 78% [71, 83] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| context:30 | decisive | 100% | PP | 99% [97, 100] | 27% [21, 34] | 82% [75, 87] | 5% [3, 9] | 2% [1, 5] | 98% [94, 99] | 1% [0, 4] | 1% [0, 3] | 0% [0, 2] | 180 |
| context:30 | decisive | 100% | PM | 99% [97, 100] | 36% [29, 43] | 63% [56, 70] | 6% [3, 10] | 2% [1, 5] | 94% [89, 97] | 3% [2, 7] | 0% [0, 2] | 0% [0, 2] | 180 |
| context:33 | decisive | 100% | PP | 100% [98, 100] | 1% [0, 3] | 99% [97, 100] | 17% [12, 23] | 1% [0, 4] | 98% [95, 99] | 1% [0, 4] | 1% [0, 4] | 0% [0, 2] | 180 |
| context:33 | decisive | 100% | PM | 99% [96, 100] | 23% [17, 29] | 77% [71, 83] | 12% [8, 18] | 2% [1, 6] | 94% [89, 97] | 3% [1, 6] | 0% [0, 2] | 0% [0, 2] | 180 |
| context:36 | decisive | 78% | PP | 76% [69, 82] | 1% [0, 4] | 78% [71, 83] | 16% [11, 22] | 1% [0, 4] | 78% [72, 84] | 1% [0, 4] | 1% [0, 4] | 0% [0, 2] | 180 |
| context:36 | decisive | 78% | PM | 77% [70, 82] | 8% [5, 13] | 59% [52, 66] | 8% [5, 13] | 2% [1, 5] | 77% [71, 83] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| context:24 | reference | 100% | PP | 99% [97, 100] | 42% [35, 50] | 58% [51, 65] | 2% [1, 5] | 1% [0, 3] | 100% [98, 100] | 0% [0, 2] | 1% [0, 3] | 0% [0, 2] | 180 |
| context:24 | reference | 100% | PM | 100% [98, 100] | 40% [33, 47] | 62% [55, 69] | 3% [1, 6] | 1% [0, 3] | 96% [91, 98] | 2% [1, 5] | 0% [0, 2] | 0% [0, 2] | 180 |

Median share of the change's squared norm (lookup rows): bind_bridge:30: jspace 0.281, rand_sub 0.281, rand_omp 0.135; bind_bridge:33: jspace 0.227, rand_sub 0.227, rand_omp 0.134; bind_bridge:36: jspace 0.193, rand_sub 0.193, rand_omp 0.134; context:30: jspace 0.232, rand_sub 0.232, rand_omp 0.135; context:33: jspace 0.174, rand_sub 0.174, rand_omp 0.134; context:36: jspace 0.147, rand_sub 0.147, rand_omp 0.134; context:24: jspace 0.235, rand_sub 0.235, rand_omp 0.134
