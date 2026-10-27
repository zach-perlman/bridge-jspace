# d1_verdict (necessity) / olmo3_7b_instruct_jpp_d1_necessity_parts_r2

Map olmo3_7b_instruct_jpp_d1_topics2_map; decisive cells (--decisive None, if in transit): bridge_word:6, bridge_word:8, bridge_word:10, bridge_word:12, bridge_word:14, bind_bridge:6, bind_bridge:8, bind_bridge:10, bind_bridge:12, bind_bridge:14

**Verdict:** does not hold (cells where it holds: bridge_word 0/5; bind_bridge 0/5)

| cell | verdict | lookups: F(full), drop without J | recalls: drop without J, without the random part, difference [95% paired bootstrap] | shares of the change: J, random part |
|---|---|---|---|---|
| bridge_word:6 | does not hold | 53%, +18 pts | +29, -1, +30 [+22, +40] pts | 0.1529, 0.1527 |
| bridge_word:8 | not interpretable: the whole change switches < 50% of lookups here | 47%, +11 pts | +28, +2, +26 [+16, +34] pts | 0.1429, 0.143 |
| bridge_word:10 | not interpretable: the whole change switches < 50% of lookups here | 41%, +9 pts | +25, -3, +28 [+20, +36] pts | 0.1222, 0.1222 |
| bridge_word:12 | not interpretable: the whole change switches < 50% of lookups here | 34%, +8 pts | +35, +3, +32 [+23, +41] pts | 0.1285, 0.1284 |
| bridge_word:14 | not interpretable: the whole change switches < 50% of lookups here | 16%, +3 pts | +15, +1, +14 [+8, +21] pts | 0.1085, 0.1084 |
| bind_bridge:6 | does not hold | 66%, +23 pts | +35, +3, +33 [+24, +41] pts | 0.1461, 0.1463 |
| bind_bridge:8 | does not hold | 54%, +14 pts | +30, +2, +28 [+19, +38] pts | 0.1363, 0.1362 |
| bind_bridge:10 | does not hold | 52%, +10 pts | +29, -1, +30 [+22, +39] pts | 0.1121, 0.1121 |
| bind_bridge:12 | not interpretable: the whole change switches < 50% of lookups here | 37%, +6 pts | +34, +3, +31 [+22, +41] pts | 0.1154, 0.1154 |
| bind_bridge:14 | not interpretable: the whole change switches < 50% of lookups here | 22%, +4 pts | +15, +4, +10 [+4, +16] pts | 0.0992, 0.0991 |

| cell | role | map: whole copy flips lookups | family | full | jspace | not_jspace | not_jspace_matched | rand_sub | not_rand_sub | jspace_matched | rand_omp | jspace null | n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge_word:6 | decisive | 53% | PP | 53% [44, 62] | 3% [1, 9] | 35% [27, 44] | 0% [0, 3] | 0% [0, 3] | 49% [40, 58] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 116 |
| bridge_word:6 | decisive | 53% | PM | 82% [74, 88] | 19% [13, 27] | 53% [44, 61] | 2% [0, 6] | 0% [0, 3] | 83% [75, 89] | 1% [0, 5] | 0% [0, 3] | 0% [0, 3] | 116 |
| bridge_word:8 | decisive | 47% | PP | 47% [39, 56] | 2% [0, 6] | 36% [28, 45] | 0% [0, 3] | 0% [0, 3] | 44% [35, 53] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 116 |
| bridge_word:8 | decisive | 47% | PM | 82% [74, 88] | 12% [7, 19] | 54% [45, 63] | 1% [0, 5] | 0% [0, 3] | 80% [72, 86] | 1% [0, 5] | 1% [0, 5] | 0% [0, 3] | 116 |
| bridge_word:10 | decisive | 41% | PP | 41% [33, 50] | 0% [0, 3] | 33% [25, 42] | 1% [0, 5] | 0% [0, 3] | 37% [29, 46] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 116 |
| bridge_word:10 | decisive | 41% | PM | 80% [72, 86] | 7% [4, 13] | 55% [46, 64] | 2% [0, 6] | 1% [0, 5] | 83% [75, 89] | 1% [0, 5] | 0% [0, 3] | 0% [0, 3] | 116 |
| bridge_word:12 | decisive | 34% | PP | 34% [26, 44] | 1% [0, 5] | 27% [20, 35] | 0% [0, 3] | 0% [0, 3] | 30% [23, 39] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 116 |
| bridge_word:12 | decisive | 34% | PM | 83% [75, 89] | 17% [11, 25] | 47% [39, 56] | 1% [0, 5] | 0% [0, 3] | 79% [71, 86] | 1% [0, 5] | 0% [0, 3] | 0% [0, 3] | 116 |
| bridge_word:14 | decisive | 16% | PP | 16% [10, 23] | 0% [0, 3] | 13% [8, 20] | 0% [0, 3] | 0% [0, 3] | 11% [7, 18] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 116 |
| bridge_word:14 | decisive | 16% | PM | 70% [61, 77] | 1% [0, 5] | 55% [46, 64] | 1% [0, 5] | 0% [0, 3] | 69% [60, 77] | 0% [0, 3] | 0% [0, 3] | 1% [0, 5] | 116 |
| bind_bridge:6 | decisive | 66% | PP | 66% [57, 74] | 3% [1, 9] | 43% [34, 52] | 1% [0, 5] | 0% [0, 3] | 62% [53, 70] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 116 |
| bind_bridge:6 | decisive | 66% | PM | 89% [82, 93] | 19% [13, 27] | 53% [44, 62] | 1% [0, 5] | 0% [0, 3] | 86% [79, 91] | 1% [0, 5] | 0% [0, 3] | 0% [0, 3] | 116 |
| bind_bridge:8 | decisive | 54% | PP | 54% [45, 63] | 2% [0, 6] | 41% [32, 50] | 0% [0, 3] | 0% [0, 3] | 47% [39, 56] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 116 |
| bind_bridge:8 | decisive | 54% | PM | 85% [78, 91] | 14% [9, 21] | 55% [46, 64] | 1% [0, 5] | 0% [0, 3] | 84% [76, 89] | 1% [0, 5] | 1% [0, 5] | 1% [0, 5] | 116 |
| bind_bridge:10 | decisive | 52% | PP | 52% [43, 61] | 0% [0, 3] | 41% [33, 50] | 1% [0, 5] | 0% [0, 3] | 47% [38, 56] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 116 |
| bind_bridge:10 | decisive | 52% | PM | 88% [81, 93] | 8% [4, 14] | 59% [50, 67] | 2% [0, 6] | 1% [0, 5] | 89% [82, 93] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 116 |
| bind_bridge:12 | decisive | 37% | PP | 37% [29, 46] | 1% [0, 5] | 31% [23, 40] | 1% [0, 5] | 0% [0, 3] | 37% [29, 46] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 116 |
| bind_bridge:12 | decisive | 37% | PM | 84% [77, 90] | 18% [12, 26] | 50% [41, 59] | 1% [0, 5] | 0% [0, 3] | 81% [73, 87] | 1% [0, 5] | 0% [0, 3] | 0% [0, 3] | 116 |
| bind_bridge:14 | decisive | 22% | PP | 22% [15, 30] | 0% [0, 3] | 17% [11, 25] | 0% [0, 3] | 0% [0, 3] | 17% [11, 25] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 116 |
| bind_bridge:14 | decisive | 22% | PM | 72% [64, 80] | 1% [0, 5] | 58% [49, 66] | 1% [0, 5] | 0% [0, 3] | 68% [59, 76] | 0% [0, 3] | 1% [0, 5] | 0% [0, 3] | 116 |

Median share of the change's squared norm (lookup rows): bridge_word:6: jspace 0.153, rand_sub 0.153, rand_omp 0.091, not_jspace 0.847, not_rand_sub 0.847; bridge_word:8: jspace 0.143, rand_sub 0.143, rand_omp 0.091, not_jspace 0.857, not_rand_sub 0.857; bridge_word:10: jspace 0.122, rand_sub 0.122, rand_omp 0.090, not_jspace 0.878, not_rand_sub 0.878; bridge_word:12: jspace 0.129, rand_sub 0.128, rand_omp 0.091, not_jspace 0.871, not_rand_sub 0.872; bridge_word:14: jspace 0.108, rand_sub 0.108, rand_omp 0.091, not_jspace 0.891, not_rand_sub 0.892; bind_bridge:6: jspace 0.146, rand_sub 0.146, rand_omp 0.091, not_jspace 0.854, not_rand_sub 0.854; bind_bridge:8: jspace 0.136, rand_sub 0.136, rand_omp 0.091, not_jspace 0.864, not_rand_sub 0.864; bind_bridge:10: jspace 0.112, rand_sub 0.112, rand_omp 0.090, not_jspace 0.888, not_rand_sub 0.888; bind_bridge:12: jspace 0.115, rand_sub 0.115, rand_omp 0.091, not_jspace 0.885, not_rand_sub 0.885; bind_bridge:14: jspace 0.099, rand_sub 0.099, rand_omp 0.091, not_jspace 0.901, not_rand_sub 0.901
