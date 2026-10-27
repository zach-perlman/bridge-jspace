# d1_verdict (late-switch) / qwen35_122b_d1_late_parts

Map qwen35_122b_d1_topics2_map; decisive cells (in transit for lookups on the map): bind_bridge:30, bind_bridge:33, context:30, context:33, context:36

**Verdict:** inconclusive: the split holds at bind_bridge:33, context:33, context:36 but fails there: bind_bridge:33 recall_control; context:33 recall_control; context:36 recall_control

Per format (reported): prose: inconclusive: the split holds at bind_bridge:33, context:33, context:36 but fails there: bind_bridge:33 recall_control; context:33 recall_control; context:36 recall_control

Per topic (reported): animals: inconclusive; elements: late switch holds at bind_bridge:33; greek: inconclusive: the split holds at bind_bridge:33, context:36 but fails there: bind_bridge:33 recall_control, subspace_control_recall; context:36 recall_control, subspace_control_recall

| cell | role | map: whole copy flips lookups | family | full | jspace | not_jspace | not_jspace_matched | rand_sub | jspace_matched | rand_omp | jspace null | n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bind_bridge:30 | decisive | 78% | PP | 79% [72, 84] | 15% [11, 21] | 40% [33, 47] | 3% [1, 6] | 1% [0, 4] | 2% [1, 5] | 1% [0, 3] | 0% [0, 2] | 180 |
| bind_bridge:30 | decisive | 78% | PM | 94% [90, 97] | 37% [30, 44] | 49% [42, 56] | 6% [3, 10] | 4% [2, 9] | 4% [2, 8] | 1% [0, 4] | 0% [0, 2] | 180 |
| bind_bridge:33 | decisive | 52% | PP | 51% [43, 58] | 0% [0, 2] | 42% [35, 50] | 3% [2, 7] | 2% [1, 5] | 1% [0, 4] | 1% [0, 3] | 1% [0, 3] | 180 |
| bind_bridge:33 | decisive | 52% | PM | 94% [89, 97] | 26% [20, 33] | 57% [49, 64] | 6% [3, 10] | 3% [2, 7] | 3% [1, 6] | 1% [0, 4] | 0% [0, 2] | 180 |
| bind_bridge:36 | not in transit | 36% | PP | 34% [28, 42] | 0% [0, 2] | 35% [28, 42] | 4% [2, 9] | 0% [0, 2] | 1% [0, 3] | 1% [0, 3] | 1% [0, 3] | 180 |
| bind_bridge:36 | not in transit | 36% | PM | 85% [79, 89] | 12% [8, 17] | 54% [47, 62] | 3% [2, 7] | 2% [1, 5] | 2% [1, 5] | 1% [0, 4] | 0% [0, 2] | 180 |
| context:30 | decisive | 98% | PP | 98% [95, 99] | 16% [11, 22] | 89% [83, 93] | 7% [4, 11] | 3% [1, 6] | 2% [1, 5] | 1% [0, 4] | 0% [0, 2] | 180 |
| context:30 | decisive | 98% | PM | 97% [93, 98] | 29% [23, 36] | 59% [52, 66] | 7% [4, 11] | 3% [2, 7] | 3% [2, 7] | 1% [0, 4] | 1% [0, 4] | 180 |
| context:33 | decisive | 99% | PP | 99% [96, 100] | 1% [0, 3] | 98% [95, 99] | 8% [5, 13] | 1% [0, 4] | 2% [1, 5] | 1% [0, 3] | 1% [0, 3] | 180 |
| context:33 | decisive | 99% | PM | 95% [91, 97] | 21% [16, 28] | 63% [56, 70] | 5% [3, 9] | 2% [1, 6] | 2% [1, 6] | 1% [0, 3] | 1% [0, 4] | 180 |
| context:36 | decisive | 70% | PP | 70% [63, 76] | 0% [0, 2] | 68% [61, 75] | 9% [6, 14] | 0% [0, 2] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| context:36 | decisive | 70% | PM | 78% [71, 83] | 8% [5, 13] | 51% [43, 58] | 4% [2, 9] | 1% [0, 4] | 2% [1, 5] | 0% [0, 2] | 1% [0, 3] | 180 |
| context:24 | reference | 99% | PP | 99% [97, 100] | 34% [27, 41] | 74% [68, 80] | 2% [1, 6] | 1% [0, 4] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| context:24 | reference | 99% | PM | 98% [94, 99] | 38% [32, 46] | 58% [51, 65] | 2% [1, 5] | 2% [1, 6] | 2% [1, 5] | 1% [0, 3] | 0% [0, 2] | 180 |

Median share of the change's squared norm (lookup rows): bind_bridge:30: jspace 0.264, rand_sub 0.265, rand_omp 0.134; bind_bridge:33: jspace 0.217, rand_sub 0.218, rand_omp 0.134; bind_bridge:36: jspace 0.183, rand_sub 0.184, rand_omp 0.135; context:30: jspace 0.186, rand_sub 0.186, rand_omp 0.135; context:33: jspace 0.141, rand_sub 0.142, rand_omp 0.135; context:36: jspace 0.128, rand_sub 0.128, rand_omp 0.135; context:24: jspace 0.186, rand_sub 0.186, rand_omp 0.134
