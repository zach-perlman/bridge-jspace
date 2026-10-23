# d1_verdict (necessity) / d1_necessity_parts_27b_r2

Map d1_topics2_map_27b; decisive cells (--decisive None, if in transit): bridge_word:16, bridge_word:20, bridge_word:24, bridge_word:28, bind_bridge:16, bind_bridge:20, bind_bridge:24, bind_bridge:28

**Verdict:** does not hold (cells where it holds: bridge_word 0/4; bind_bridge 0/4)

| cell | verdict | lookups: F(full), drop without J | recalls: drop without J, without the random part, difference [95% paired bootstrap] | shares of the change: J, random part |
|---|---|---|---|---|
| bridge_word:16 | does not hold | 84%, +80 pts | +90, -1, +91 [+86, +94] pts | 0.1835, 0.1835 |
| bridge_word:20 | does not hold | 72%, +32 pts | +39, +2, +37 [+31, +44] pts | 0.1816, 0.1817 |
| bridge_word:24 | does not hold | 63%, +16 pts | +20, +1, +19 [+13, +25] pts | 0.1697, 0.1698 |
| bridge_word:28 | not interpretable: the whole change switches < 50% of lookups here | 48%, +15 pts | +64, +4, +60 [+53, +67] pts | 0.2085, 0.2085 |
| bind_bridge:16 | does not hold | 84%, +81 pts | +90, +0, +90 [+86, +94] pts | 0.1663, 0.1664 |
| bind_bridge:20 | does not hold | 76%, +35 pts | +41, +3, +38 [+31, +45] pts | 0.1653, 0.1661 |
| bind_bridge:24 | does not hold | 70%, +19 pts | +20, +2, +18 [+13, +24] pts | 0.1537, 0.1538 |
| bind_bridge:28 | does not hold | 54%, +17 pts | +66, +4, +61 [+54, +68] pts | 0.1877, 0.1877 |

| cell | role | map: whole copy flips lookups | family | full | jspace | not_jspace | not_jspace_matched | rand_sub | not_rand_sub | jspace_matched | rand_omp | jspace null | n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge_word:16 | decisive | 85% | PP | 84% [78, 89] | 59% [52, 66] | 4% [2, 8] | 0% [0, 2] | 0% [0, 2] | 76% [69, 82] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:16 | decisive | 85% | PM | 98% [94, 99] | 84% [78, 89] | 8% [5, 13] | 0% [0, 2] | 0% [0, 2] | 98% [95, 99] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:20 | decisive | 72% | PP | 72% [65, 78] | 7% [4, 12] | 40% [33, 47] | 0% [0, 2] | 0% [0, 2] | 61% [54, 68] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:20 | decisive | 72% | PM | 95% [91, 97] | 17% [12, 23] | 56% [48, 63] | 0% [0, 2] | 0% [0, 2] | 93% [88, 96] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:24 | decisive | 63% | PP | 63% [56, 70] | 1% [0, 3] | 47% [40, 54] | 0% [0, 2] | 0% [0, 2] | 57% [49, 64] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:24 | decisive | 63% | PM | 91% [86, 94] | 9% [6, 15] | 71% [64, 77] | 1% [0, 3] | 0% [0, 2] | 90% [85, 94] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:28 | decisive | 48% | PP | 48% [41, 56] | 0% [0, 2] | 33% [27, 41] | 2% [1, 6] | 0% [0, 2] | 43% [36, 50] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bridge_word:28 | decisive | 48% | PM | 93% [88, 96] | 40% [33, 47] | 29% [23, 36] | 1% [0, 3] | 1% [0, 3] | 89% [83, 93] | 1% [0, 4] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:16 | decisive | 85% | PP | 84% [78, 89] | 61% [53, 67] | 4% [2, 8] | 0% [0, 2] | 0% [0, 2] | 78% [71, 83] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:16 | decisive | 85% | PM | 98% [95, 99] | 83% [77, 88] | 8% [5, 13] | 0% [0, 2] | 0% [0, 2] | 98% [95, 99] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:20 | decisive | 75% | PP | 76% [69, 81] | 7% [4, 12] | 41% [34, 48] | 0% [0, 2] | 0% [0, 2] | 63% [56, 70] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:20 | decisive | 75% | PM | 96% [92, 98] | 17% [12, 23] | 56% [48, 63] | 0% [0, 2] | 0% [0, 2] | 93% [89, 96] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:24 | decisive | 70% | PP | 70% [63, 76] | 1% [0, 3] | 51% [43, 58] | 0% [0, 2] | 0% [0, 2] | 61% [53, 67] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:24 | decisive | 70% | PM | 94% [90, 97] | 9% [6, 15] | 74% [68, 80] | 1% [0, 3] | 0% [0, 2] | 93% [88, 96] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:28 | decisive | 54% | PP | 54% [47, 61] | 0% [0, 2] | 37% [30, 44] | 2% [1, 6] | 0% [0, 2] | 48% [41, 56] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 180 |
| bind_bridge:28 | decisive | 54% | PM | 94% [90, 97] | 40% [33, 47] | 29% [23, 36] | 1% [0, 3] | 1% [0, 3] | 90% [85, 94] | 1% [0, 3] | 0% [0, 2] | 0% [0, 2] | 180 |

Median share of the change's squared norm (lookup rows): bridge_word:16: jspace 0.183, rand_sub 0.183, rand_omp 0.082, not_jspace 0.817, not_rand_sub 0.817; bridge_word:20: jspace 0.182, rand_sub 0.182, rand_omp 0.082, not_jspace 0.818, not_rand_sub 0.818; bridge_word:24: jspace 0.170, rand_sub 0.170, rand_omp 0.082, not_jspace 0.830, not_rand_sub 0.830; bridge_word:28: jspace 0.208, rand_sub 0.208, rand_omp 0.082, not_jspace 0.791, not_rand_sub 0.791; bind_bridge:16: jspace 0.166, rand_sub 0.166, rand_omp 0.082, not_jspace 0.834, not_rand_sub 0.834; bind_bridge:20: jspace 0.165, rand_sub 0.166, rand_omp 0.082, not_jspace 0.835, not_rand_sub 0.834; bind_bridge:24: jspace 0.154, rand_sub 0.154, rand_omp 0.082, not_jspace 0.846, not_rand_sub 0.846; bind_bridge:28: jspace 0.188, rand_sub 0.188, rand_omp 0.082, not_jspace 0.812, not_rand_sub 0.812
