# d1_verdict (necessity) / qwen35_9b_d1_necessity_parts_r2

Map qwen35_9b_d1_topics2_map; decisive cells (--decisive None, if in transit): bridge_word:6, bridge_word:8, bridge_word:10, bridge_word:12, bridge_word:14, bind_bridge:6, bind_bridge:8, bind_bridge:10, bind_bridge:12, bind_bridge:14

**Verdict:** does not hold (cells where it holds: bridge_word 0/5; bind_bridge 0/5)

| cell | verdict | lookups: F(full), drop without J | recalls: drop without J, without the random part, difference [95% paired bootstrap] | shares of the change: J, random part |
|---|---|---|---|---|
| bridge_word:6 | does not hold | 74%, +64 pts | +87, +7, +81 [+74, +86] pts | 0.3301, 0.3299 |
| bridge_word:8 | does not hold | 55%, +26 pts | +69, +1, +68 [+61, +75] pts | 0.283, 0.2828 |
| bridge_word:10 | does not hold | 52%, +19 pts | +67, -1, +67 [+60, +73] pts | 0.2808, 0.2808 |
| bridge_word:12 | not interpretable: the whole change switches < 50% of lookups here | 47%, +8 pts | +61, +3, +58 [+50, +65] pts | 0.2274, 0.2275 |
| bridge_word:14 | not interpretable: the whole change switches < 50% of lookups here | 38%, +3 pts | +72, +2, +71 [+64, +77] pts | 0.2067, 0.2067 |
| bind_bridge:6 | does not hold | 78%, +68 pts | +88, +7, +81 [+74, +86] pts | 0.3141, 0.314 |
| bind_bridge:8 | does not hold | 57%, +28 pts | +68, +3, +66 [+58, +72] pts | 0.2617, 0.262 |
| bind_bridge:10 | does not hold | 56%, +19 pts | +66, +1, +64 [+57, +71] pts | 0.2514, 0.2515 |
| bind_bridge:12 | not interpretable: the whole change switches < 50% of lookups here | 46%, +7 pts | +60, +2, +58 [+50, +65] pts | 0.2066, 0.2066 |
| bind_bridge:14 | not interpretable: the whole change switches < 50% of lookups here | 47%, +6 pts | +70, +3, +67 [+59, +73] pts | 0.1833, 0.1834 |

| cell | role | map: whole copy flips lookups | family | full | jspace | not_jspace | not_jspace_matched | rand_sub | not_rand_sub | jspace_matched | rand_omp | jspace null | n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge_word:6 | decisive | 74% | PP | 74% [68, 80] | 37% [30, 44] | 10% [6, 15] | 1% [0, 4] | 2% [1, 5] | 50% [43, 57] | 4% [2, 8] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:6 | decisive | 74% | PM | 97% [94, 99] | 83% [77, 88] | 10% [6, 15] | 1% [0, 4] | 3% [1, 6] | 91% [85, 94] | 2% [1, 5] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:8 | decisive | 55% | PP | 55% [48, 62] | 8% [5, 13] | 29% [23, 36] | 2% [1, 5] | 0% [0, 2] | 47% [40, 54] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:8 | decisive | 55% | PM | 98% [94, 99] | 54% [47, 61] | 28% [22, 35] | 2% [1, 6] | 1% [0, 4] | 97% [93, 98] | 2% [1, 5] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:10 | decisive | 52% | PP | 52% [45, 59] | 3% [2, 7] | 33% [27, 41] | 2% [1, 6] | 1% [0, 4] | 47% [40, 54] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:10 | decisive | 52% | PM | 97% [93, 98] | 56% [48, 63] | 30% [24, 37] | 1% [0, 4] | 1% [0, 3] | 97% [94, 99] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:12 | decisive | 47% | PP | 47% [40, 54] | 0% [0, 2] | 39% [32, 46] | 5% [3, 9] | 0% [0, 2] | 40% [33, 47] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:12 | decisive | 47% | PM | 99% [96, 100] | 45% [38, 52] | 38% [31, 45] | 2% [1, 5] | 1% [0, 3] | 96% [91, 98] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:14 | decisive | 38% | PP | 38% [31, 45] | 1% [0, 3] | 34% [28, 42] | 5% [3, 9] | 0% [0, 2] | 31% [25, 38] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:14 | decisive | 38% | PM | 94% [90, 97] | 53% [46, 60] | 22% [17, 29] | 2% [1, 6] | 1% [0, 3] | 93% [88, 96] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:6 | decisive | 78% | PP | 78% [71, 83] | 39% [32, 46] | 10% [6, 15] | 2% [1, 5] | 2% [1, 5] | 53% [46, 60] | 4% [2, 8] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:6 | decisive | 78% | PM | 98% [95, 99] | 85% [79, 89] | 11% [7, 16] | 2% [1, 6] | 3% [1, 6] | 91% [86, 94] | 3% [1, 6] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:8 | decisive | 57% | PP | 57% [49, 64] | 8% [5, 13] | 29% [23, 36] | 2% [1, 5] | 1% [0, 3] | 47% [40, 54] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:8 | decisive | 57% | PM | 98% [95, 99] | 54% [47, 62] | 30% [24, 37] | 2% [1, 6] | 1% [0, 4] | 96% [91, 98] | 2% [1, 5] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:10 | decisive | 56% | PP | 56% [48, 63] | 3% [2, 7] | 36% [29, 43] | 2% [1, 5] | 1% [0, 4] | 48% [41, 55] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:10 | decisive | 56% | PM | 99% [96, 100] | 56% [48, 63] | 33% [27, 41] | 1% [0, 4] | 1% [0, 3] | 98% [94, 99] | 2% [1, 5] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:12 | decisive | 46% | PP | 46% [39, 53] | 0% [0, 2] | 39% [33, 47] | 6% [3, 10] | 0% [0, 2] | 39% [33, 47] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:12 | decisive | 46% | PM | 99% [96, 100] | 46% [38, 53] | 39% [32, 46] | 2% [1, 6] | 1% [0, 3] | 97% [93, 98] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:14 | decisive | 47% | PP | 47% [40, 54] | 1% [0, 3] | 42% [35, 49] | 6% [3, 10] | 0% [0, 2] | 44% [37, 52] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:14 | decisive | 47% | PM | 99% [97, 100] | 53% [46, 60] | 29% [23, 36] | 2% [1, 6] | 1% [0, 4] | 96% [92, 98] | 1% [0, 4] | 0% [0, 2] | 0% [0, 2] | 180 |

Median share of the change's squared norm (lookup rows): bridge_word:6: jspace 0.330, rand_sub 0.330, rand_omp 0.102, not_jspace 0.670, not_rand_sub 0.670; bridge_word:8: jspace 0.283, rand_sub 0.283, rand_omp 0.102, not_jspace 0.717, not_rand_sub 0.717; bridge_word:10: jspace 0.281, rand_sub 0.281, rand_omp 0.102, not_jspace 0.719, not_rand_sub 0.719; bridge_word:12: jspace 0.227, rand_sub 0.228, rand_omp 0.101, not_jspace 0.773, not_rand_sub 0.772; bridge_word:14: jspace 0.207, rand_sub 0.207, rand_omp 0.102, not_jspace 0.793, not_rand_sub 0.793; bind_bridge:6: jspace 0.314, rand_sub 0.314, rand_omp 0.101, not_jspace 0.686, not_rand_sub 0.686; bind_bridge:8: jspace 0.262, rand_sub 0.262, rand_omp 0.102, not_jspace 0.738, not_rand_sub 0.738; bind_bridge:10: jspace 0.251, rand_sub 0.252, rand_omp 0.102, not_jspace 0.749, not_rand_sub 0.748; bind_bridge:12: jspace 0.207, rand_sub 0.207, rand_omp 0.101, not_jspace 0.793, not_rand_sub 0.793; bind_bridge:14: jspace 0.183, rand_sub 0.183, rand_omp 0.102, not_jspace 0.817, not_rand_sub 0.817
