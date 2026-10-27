# early_push

P* = ('clean', 'push', 'lens', 24, 4.0, 'a', None); emb* = ('clean', 'emb_add', 'lens', -1, 1.0, 'b', None)

Verdict (manifest rule): **push writes the intermediate**; calls (K1 RL, K2 RL, K3) ['gate failed', 'write', 'write']; K3 BL - RL flips -0.40 [-0.50, -0.31]

## BL (W-copy* = ('clean', 'copy', None, 48, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|edit|None|None|None|None|E-name | 100 | 100% [96, 100] | 0.98 | {'b': 100} |
| clean|edit|None|None|None|None|E-insert | 100 | 66% [56, 75] | 0.52 | {'b': 66, 'A': 34} |
| clean|edit|None|None|None|None|E-head | 100 | 86% [78, 91] | 0.55 | {'b': 86, 'A': 14} |
| clean|edit|None|None|None|None|E-cue | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|edit|None|None|None|None|E-unrelated | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|push|lens|16|4.0|r|None | 100 | 14% [9, 22] | 0.25 | {'A': 81, 'oc': 5, 'b': 14} |
| clean|push|random|16|4.0|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|16|4.0|a|None | 100 | 1% [0, 5] | 0.06 | {'A': 99, 'b': 1} |
| clean|push|random|16|4.0|a|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|16|4.0|b|None | 100 | 1% [0, 5] | 0.02 | {'A': 99, 'b': 1} |
| clean|push|random|16|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|16|8.0|r|None | 100 | 60% [50, 69] | 0.52 | {'A': 27, 'oc': 12, 'b': 60, 'other': 1} |
| clean|push|random|16|8.0|r|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|16|8.0|a|None | 100 | 40% [31, 50] | 0.43 | {'A': 54, 'b': 40, 'oc': 6} |
| clean|push|random|16|8.0|a|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|lens|16|8.0|b|None | 100 | 37% [28, 47] | 0.39 | {'A': 59, 'b': 37, 'oc': 4} |
| clean|push|random|16|8.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|16|16.0|r|None | 100 | 93% [86, 97] | 0.61 | {'b': 93, 'oc': 5, 'A': 2} |
| clean|push|random|16|16.0|r|None | 100 | 2% [1, 7] | 0.14 | {'A': 96, 'oc': 2, 'b': 2} |
| clean|push|lens|16|16.0|a|None | 100 | 22% [15, 31] | 0.62 | {'other': 74, 'b': 22, 'A': 3, 'oc': 1} |
| clean|push|random|16|16.0|a|None | 100 | 0% [0, 4] | 0.12 | {'A': 100} |
| clean|push|lens|16|16.0|b|None | 100 | 95% [89, 98] | 0.63 | {'b': 95, 'A': 5} |
| clean|push|random|16|16.0|b|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|20|4.0|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|random|20|4.0|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|20|4.0|a|None | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|push|random|20|4.0|a|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|lens|20|4.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|random|20|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|20|8.0|r|None | 100 | 3% [1, 8] | 0.12 | {'A': 97, 'b': 3} |
| clean|push|random|20|8.0|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|20|8.0|a|None | 100 | 1% [0, 5] | 0.16 | {'A': 99, 'b': 1} |
| clean|push|random|20|8.0|a|None | 100 | 0% [0, 4] | 0.09 | {'A': 100} |
| clean|push|lens|20|8.0|b|None | 100 | 1% [0, 5] | 0.07 | {'A': 99, 'b': 1} |
| clean|push|random|20|8.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|20|16.0|r|None | 100 | 33% [25, 43] | 0.40 | {'A': 65, 'b': 33, 'oc': 2} |
| clean|push|random|20|16.0|r|None | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|push|lens|20|16.0|a|None | 100 | 2% [1, 7] | 0.36 | {'other': 34, 'A': 64, 'b': 2} |
| clean|push|random|20|16.0|a|None | 100 | 0% [0, 4] | 0.15 | {'A': 98, 'other': 2} |
| clean|push|lens|20|16.0|b|None | 100 | 25% [18, 34] | 0.35 | {'A': 73, 'b': 25, 'oc': 2} |
| clean|push|random|20|16.0|b|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|lens|24|4.0|r|None | 100 | 1% [0, 5] | 0.05 | {'A': 99, 'b': 1} |
| clean|push|random|24|4.0|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|24|4.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 100} |
| clean|push|random|24|4.0|a|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|lens|24|4.0|b|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|random|24|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|24|8.0|r|None | 100 | 3% [1, 8] | 0.15 | {'A': 97, 'b': 3} |
| clean|push|random|24|8.0|r|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|24|8.0|a|None | 100 | 1% [0, 5] | 0.22 | {'A': 99, 'b': 1} |
| clean|push|random|24|8.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 100} |
| clean|push|lens|24|8.0|b|None | 100 | 0% [0, 4] | 0.13 | {'A': 100} |
| clean|push|random|24|8.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|24|16.0|r|None | 100 | 26% [18, 35] | 0.36 | {'A': 69, 'b': 26, 'oc': 4, 'other': 1} |
| clean|push|random|24|16.0|r|None | 100 | 0% [0, 4] | 0.16 | {'A': 100} |
| clean|push|lens|24|16.0|a|None | 100 | 9% [5, 16] | 0.35 | {'A': 67, 'other': 24, 'b': 9} |
| clean|push|random|24|16.0|a|None | 100 | 0% [0, 4] | 0.21 | {'A': 96, 'oc': 1, 'other': 3} |
| clean|push|lens|24|16.0|b|None | 100 | 16% [10, 24] | 0.32 | {'A': 81, 'b': 16, 'oc': 3} |
| clean|push|random|24|16.0|b|None | 100 | 0% [0, 4] | 0.10 | {'A': 99, 'oc': 1} |
| clean|push|lens|28|4.0|r|None | 100 | 1% [0, 5] | 0.03 | {'A': 99, 'b': 1} |
| clean|push|random|28|4.0|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|28|4.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 100} |
| clean|push|random|28|4.0|a|None | 100 | 0% [0, 4] | 0.08 | {'A': 100} |
| clean|push|lens|28|4.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|random|28|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|28|8.0|r|None | 100 | 5% [2, 11] | 0.17 | {'A': 95, 'b': 5} |
| clean|push|random|28|8.0|r|None | 100 | 0% [0, 4] | 0.06 | {'A': 100} |
| clean|push|lens|28|8.0|a|None | 100 | 6% [3, 12] | 0.26 | {'A': 93, 'b': 6, 'other': 1} |
| clean|push|random|28|8.0|a|None | 100 | 0% [0, 4] | 0.13 | {'A': 100} |
| clean|push|lens|28|8.0|b|None | 100 | 1% [0, 5] | 0.08 | {'A': 99, 'b': 1} |
| clean|push|random|28|8.0|b|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|28|16.0|r|None | 100 | 41% [32, 51] | 0.46 | {'A': 46, 'oc': 13, 'b': 41} |
| clean|push|random|28|16.0|r|None | 100 | 3% [1, 8] | 0.26 | {'A': 96, 'b': 3, 'oc': 1} |
| clean|push|lens|28|16.0|a|None | 100 | 11% [6, 19] | 0.46 | {'other': 65, 'A': 18, 'b': 11, 'oc': 6} |
| clean|push|random|28|16.0|a|None | 100 | 1% [0, 5] | 0.33 | {'A': 79, 'other': 16, 'oc': 4, 'b': 1} |
| clean|push|lens|28|16.0|b|None | 100 | 27% [19, 36] | 0.43 | {'A': 63, 'b': 27, 'oc': 10} |
| clean|push|random|28|16.0|b|None | 100 | 2% [1, 7] | 0.23 | {'A': 97, 'oc': 1, 'b': 2} |
| clean|push|lens|band|4.0|r|None | 100 | 68% [58, 76] | 0.56 | {'A': 23, 'b': 68, 'oc': 8, 'other': 1} |
| clean|push|random|band|4.0|r|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|band|4.0|a|None | 100 | 53% [43, 62] | 0.51 | {'other': 13, 'A': 33, 'b': 53, 'oc': 1} |
| clean|push|random|band|4.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 100} |
| clean|push|lens|band|4.0|b|None | 100 | 66% [56, 75] | 0.51 | {'b': 66, 'A': 31, 'oc': 3} |
| clean|push|random|band|4.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|band|8.0|r|None | 100 | 79% [70, 86] | 0.62 | {'b': 79, 'oc': 14, 'other': 3, 'A': 4} |
| clean|push|random|band|8.0|r|None | 100 | 3% [1, 8] | 0.15 | {'A': 97, 'b': 3} |
| clean|push|lens|band|8.0|a|None | 100 | 1% [0, 5] | 0.55 | {'other': 99, 'b': 1} |
| clean|push|random|band|8.0|a|None | 100 | 0% [0, 4] | 0.20 | {'A': 92, 'other': 8} |
| clean|push|lens|band|8.0|b|None | 100 | 80% [71, 87] | 0.61 | {'b': 80, 'oc': 17, 'A': 3} |
| clean|push|random|band|8.0|b|None | 100 | 1% [0, 5] | 0.09 | {'A': 99, 'b': 1} |
| clean|push|lens|band|16.0|r|None | 100 | 70% [60, 78] | 0.59 | {'b': 70, 'other': 7, 'oc': 19, 'A': 4} |
| clean|push|random|band|16.0|r|None | 100 | 13% [8, 21] | 0.41 | {'A': 74, 'b': 13, 'oc': 13} |
| clean|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | 0.49 | {'other': 100} |
| clean|push|random|band|16.0|a|None | 100 | 0% [0, 4] | 0.45 | {'other': 97, 'A': 3} |
| clean|push|lens|band|16.0|b|None | 100 | 69% [59, 77] | 0.64 | {'b': 69, 'oc': 27, 'A': 4} |
| clean|push|random|band|16.0|b|None | 100 | 8% [4, 15] | 0.40 | {'A': 79, 'oc': 13, 'b': 8} |
| clean|emb_diff|lens|-1|1.0|b|None | 100 | 49% [39, 59] | 0.43 | {'A': 47, 'b': 49, 'oc': 4} |
| clean|emb_diff|random|-1|1.0|b|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|emb_add|lens|-1|1.0|b|None | 100 | 49% [39, 59] | 0.44 | {'A': 49, 'b': 49, 'oc': 2} |
| clean|emb_add|random|-1|1.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|emb_diff|lens|-1|4.0|b|None | 100 | 97% [92, 99] | 0.70 | {'b': 97, 'oc': 2, 'A': 1} |
| clean|emb_diff|random|-1|4.0|b|None | 100 | 27% [19, 36] | 0.49 | {'A': 42, 'oc': 31, 'b': 27} |
| clean|emb_add|lens|-1|4.0|b|None | 100 | 100% [96, 100] | 0.90 | {'b': 100} |
| clean|emb_add|random|-1|4.0|b|None | 100 | 17% [11, 26] | 0.48 | {'A': 45, 'oc': 38, 'b': 17} |
| clean|copy|None|16|None|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|copy|None|20|None|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|copy|None|24|None|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|copy|None|28|None|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|copy|None|32|None|r|None | 100 | 10% [6, 17] | 0.20 | {'A': 90, 'b': 10} |
| clean|copy|None|36|None|r|None | 100 | 13% [8, 21] | 0.19 | {'A': 87, 'b': 13} |
| clean|copy|None|40|None|r|None | 100 | 15% [9, 23] | 0.21 | {'A': 84, 'b': 15, 'oc': 1} |
| clean|copy|None|44|None|r|None | 100 | 11% [6, 19] | 0.22 | {'A': 88, 'b': 11, 'oc': 1} |
| clean|copy|None|48|None|r|None | 100 | 18% [12, 27] | 0.32 | {'A': 81, 'b': 18, 'oc': 1} |
| clean|patch|None|16|None|a|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|patch|None|16|4.0|a|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|patch|None|16|8.0|a|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|patch|None|16|16.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 98, 'other': 2} |
| clean|patch|None|20|None|a|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|patch|None|20|4.0|a|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|patch|None|20|8.0|a|None | 100 | 0% [0, 4] | 0.10 | {'A': 100} |
| clean|patch|None|20|16.0|a|None | 100 | 5% [2, 11] | 0.23 | {'A': 92, 'b': 5, 'other': 3} |
| clean|patch|None|24|None|a|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|patch|None|24|4.0|a|None | 100 | 0% [0, 4] | 0.06 | {'A': 100} |
| clean|patch|None|24|8.0|a|None | 100 | 0% [0, 4] | 0.15 | {'A': 100} |
| clean|patch|None|24|16.0|a|None | 100 | 12% [7, 20] | 0.37 | {'other': 20, 'A': 66, 'b': 12, 'oc': 2} |
| clean|patch|None|28|None|a|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|patch|None|28|4.0|a|None | 100 | 5% [2, 11] | 0.16 | {'A': 95, 'b': 5} |
| clean|patch|None|28|8.0|a|None | 100 | 26% [18, 35] | 0.36 | {'A': 72, 'b': 26, 'other': 1, 'oc': 1} |
| clean|patch|None|28|16.0|a|None | 100 | 33% [25, 43] | 0.51 | {'other': 26, 'A': 30, 'oc': 11, 'b': 33} |
| off|push|lens|16|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 99, 'bO': 1} |
| off|push|lens|16|8.0|a|None | 100 | 6% [3, 12] | nan | {'A': 48, 'bO': 45, 'b': 6, 'other': 1} |
| off|push|lens|16|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 73, 'bO': 24, 'A': 3} |
| off|push|lens|20|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 100} |
| off|push|lens|20|8.0|a|None | 100 | 0% [0, 4] | nan | {'A': 99, 'bO': 1} |
| off|push|lens|20|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 32, 'A': 62, 'bO': 6} |
| off|push|lens|24|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 100} |
| off|push|lens|24|8.0|a|None | 100 | 0% [0, 4] | nan | {'A': 99, 'bO': 1} |
| off|push|lens|24|16.0|a|None | 100 | 0% [0, 4] | nan | {'A': 65, 'other': 26, 'bO': 9} |
| off|push|lens|28|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 100} |
| off|push|lens|28|8.0|a|None | 100 | 0% [0, 4] | nan | {'A': 94, 'bO': 5, 'other': 1} |
| off|push|lens|28|16.0|a|None | 100 | 5% [2, 11] | nan | {'other': 65, 'A': 19, 'bO': 11, 'b': 5} |
| off|push|lens|band|4.0|a|None | 100 | 4% [2, 10] | nan | {'other': 15, 'A': 33, 'b': 4, 'bO': 48} |
| off|push|lens|band|8.0|a|None | 100 | 0% [0, 4] | nan | {'other': 98, 'bO': 2} |
| off|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 100} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-insert: k -, J +0.00 [+0.00, +0.00] (ref rate 0.66); E-head: k -, J +0.00 [+0.00, +0.00] (ref rate 0.86); E-cue: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-unrelated: k -, J - (ref rate 0.00); W-copy*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.18); emb*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.49); patch_matched: k -, J - (ref rate 0.00); low_margin: k -
K1 - -> untestable; gate -0.10 [-0.33, +0.15]; K2 nb - a/2 +0.00 [+0.00, +0.00], b - nb +0.00 [+0.00, +0.00] -> inconclusive; K4 -0.25 [-0.28, -0.22]
JS(P*, .) {"clean": 0.003, "E-name": 0.679, "E-insert": 0.275, "E-head": 0.367, "E-cue": 0.679, "E-unrelated": 0.003}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [-0.0379, -0.1765, -0.1532, -0.0951], "E-insert": [0.1123, 0.2123, 0.2097, 0.1774], "E-head": [0.2431, 0.2877, 0.2234, 0.1718], "E-cue": [0.1562, 0.1293, 0.1178, 0.1221], "E-unrelated": [0.1863, 0.3086, 0.3168, 0.3119]}
transit proj on C's delta [44, 48, 52]: P*_b [0.0616, 0.0525, 0.0582], P* [0.2175, 0.2194, 0.1924], edits {"E-name": [0.5548, 0.5747, 0.663], "E-insert": [0.5137, 0.5151, 0.549], "E-head": [0.4723, 0.4937, 0.5553], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.2266, 0.2139, 0.207]}

## BR (W-copy* = ('clean', 'copy', None, 40, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|edit|None|None|None|None|E-name | 100 | 100% [96, 100] | 1.08 | {'b': 100} |
| clean|edit|None|None|None|None|E-insert | 100 | 32% [24, 42] | 0.56 | {'other': 8, 'oc': 39, 'A': 21, 'b': 32} |
| clean|edit|None|None|None|None|E-head | 100 | 30% [22, 40] | 0.85 | {'b': 30, 'other': 70} |
| clean|edit|None|None|None|None|E-cue | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|edit|None|None|None|None|E-unrelated | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|lens|16|4.0|r|None | 100 | 5% [2, 11] | 0.28 | {'A': 61, 'other': 34, 'b': 5} |
| clean|push|random|16|4.0|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|16|4.0|a|None | 100 | 1% [0, 5] | 0.06 | {'A': 99, 'b': 1} |
| clean|push|random|16|4.0|a|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|16|4.0|b|None | 100 | 1% [0, 5] | 0.03 | {'A': 99, 'b': 1} |
| clean|push|random|16|4.0|b|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|16|8.0|r|None | 100 | 39% [30, 49] | 0.65 | {'other': 56, 'b': 39, 'A': 5} |
| clean|push|random|16|8.0|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|16|8.0|a|None | 100 | 24% [17, 33] | 0.55 | {'other': 48, 'b': 24, 'A': 28} |
| clean|push|random|16|8.0|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|16|8.0|b|None | 100 | 27% [19, 36] | 0.51 | {'b': 27, 'other': 44, 'A': 29} |
| clean|push|random|16|8.0|b|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|16|16.0|r|None | 100 | 75% [66, 82] | 0.81 | {'b': 75, 'other': 25} |
| clean|push|random|16|16.0|r|None | 100 | 2% [1, 7] | 0.12 | {'A': 93, 'other': 5, 'b': 2} |
| clean|push|lens|16|16.0|a|None | 100 | 20% [13, 29] | 0.80 | {'other': 80, 'b': 20} |
| clean|push|random|16|16.0|a|None | 100 | 0% [0, 4] | 0.08 | {'A': 98, 'other': 2} |
| clean|push|lens|16|16.0|b|None | 100 | 79% [70, 86] | 0.82 | {'b': 79, 'other': 21} |
| clean|push|random|16|16.0|b|None | 100 | 1% [0, 5] | 0.02 | {'A': 99, 'b': 1} |
| clean|push|lens|20|4.0|r|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|random|20|4.0|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|20|4.0|a|None | 100 | 0% [0, 4] | 0.04 | {'A': 98, 'other': 2} |
| clean|push|random|20|4.0|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|20|4.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|random|20|4.0|b|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|20|8.0|r|None | 100 | 2% [1, 7] | 0.15 | {'A': 90, 'other': 8, 'b': 2} |
| clean|push|random|20|8.0|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|20|8.0|a|None | 100 | 1% [0, 5] | 0.18 | {'A': 89, 'other': 10, 'b': 1} |
| clean|push|random|20|8.0|a|None | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|push|lens|20|8.0|b|None | 100 | 2% [1, 7] | 0.12 | {'A': 97, 'other': 1, 'b': 2} |
| clean|push|random|20|8.0|b|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|20|16.0|r|None | 100 | 35% [26, 45] | 0.48 | {'A': 41, 'other': 24, 'b': 35} |
| clean|push|random|20|16.0|r|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|lens|20|16.0|a|None | 100 | 11% [6, 19] | 0.48 | {'other': 55, 'A': 34, 'b': 11} |
| clean|push|random|20|16.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 93, 'other': 7} |
| clean|push|lens|20|16.0|b|None | 100 | 26% [18, 35] | 0.43 | {'A': 55, 'other': 19, 'b': 26} |
| clean|push|random|20|16.0|b|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|24|4.0|r|None | 100 | 0% [0, 4] | 0.08 | {'A': 98, 'other': 2} |
| clean|push|random|24|4.0|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|24|4.0|a|None | 100 | 1% [0, 5] | 0.08 | {'A': 92, 'other': 7, 'b': 1} |
| clean|push|random|24|4.0|a|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|24|4.0|b|None | 100 | 0% [0, 4] | 0.06 | {'A': 100} |
| clean|push|random|24|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|24|8.0|r|None | 100 | 3% [1, 8] | 0.16 | {'A': 87, 'other': 10, 'b': 3} |
| clean|push|random|24|8.0|r|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|24|8.0|a|None | 100 | 3% [1, 8] | 0.22 | {'A': 82, 'other': 15, 'b': 3} |
| clean|push|random|24|8.0|a|None | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|push|lens|24|8.0|b|None | 100 | 5% [2, 11] | 0.19 | {'A': 95, 'b': 5} |
| clean|push|random|24|8.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|24|16.0|r|None | 100 | 32% [24, 42] | 0.44 | {'A': 34, 'other': 33, 'b': 32, 'oc': 1} |
| clean|push|random|24|16.0|r|None | 100 | 1% [0, 5] | 0.13 | {'A': 98, 'b': 1, 'other': 1} |
| clean|push|lens|24|16.0|a|None | 100 | 17% [11, 26] | 0.49 | {'other': 59, 'b': 17, 'A': 24} |
| clean|push|random|24|16.0|a|None | 100 | 2% [1, 7] | 0.18 | {'A': 89, 'other': 9, 'b': 2} |
| clean|push|lens|24|16.0|b|None | 100 | 32% [24, 42] | 0.45 | {'A': 53, 'other': 15, 'b': 32} |
| clean|push|random|24|16.0|b|None | 100 | 0% [0, 4] | 0.08 | {'A': 100} |
| clean|push|lens|28|4.0|r|None | 100 | 4% [2, 10] | 0.14 | {'A': 94, 'other': 2, 'b': 4} |
| clean|push|random|28|4.0|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|28|4.0|a|None | 100 | 3% [1, 8] | 0.21 | {'A': 94, 'other': 3, 'b': 3} |
| clean|push|random|28|4.0|a|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|28|4.0|b|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|random|28|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|28|8.0|r|None | 100 | 37% [28, 47] | 0.44 | {'A': 58, 'b': 37, 'other': 5} |
| clean|push|random|28|8.0|r|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|28|8.0|a|None | 100 | 44% [35, 54] | 0.52 | {'A': 34, 'b': 44, 'other': 22} |
| clean|push|random|28|8.0|a|None | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|push|lens|28|8.0|b|None | 100 | 5% [2, 11] | 0.13 | {'A': 95, 'b': 5} |
| clean|push|random|28|8.0|b|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|28|16.0|r|None | 100 | 76% [67, 83] | 0.75 | {'A': 5, 'other': 18, 'b': 76, 'oc': 1} |
| clean|push|random|28|16.0|r|None | 100 | 3% [1, 8] | 0.23 | {'A': 97, 'b': 3} |
| clean|push|lens|28|16.0|a|None | 100 | 13% [8, 21] | 0.65 | {'other': 85, 'A': 2, 'b': 13} |
| clean|push|random|28|16.0|a|None | 100 | 4% [2, 10] | 0.31 | {'A': 66, 'b': 4, 'other': 30} |
| clean|push|lens|28|16.0|b|None | 100 | 57% [47, 66] | 0.56 | {'A': 37, 'b': 57, 'other': 5, 'oc': 1} |
| clean|push|random|28|16.0|b|None | 100 | 1% [0, 5] | 0.20 | {'A': 99, 'b': 1} |
| clean|push|lens|band|4.0|r|None | 100 | 74% [65, 82] | 0.78 | {'b': 74, 'other': 19, 'A': 6, 'oc': 1} |
| clean|push|random|band|4.0|r|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|band|4.0|a|None | 100 | 55% [45, 64] | 0.74 | {'b': 55, 'other': 41, 'A': 3, 'oc': 1} |
| clean|push|random|band|4.0|a|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|lens|band|4.0|b|None | 100 | 80% [71, 87] | 0.74 | {'b': 80, 'A': 12, 'other': 7, 'oc': 1} |
| clean|push|random|band|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|band|8.0|r|None | 100 | 66% [56, 75] | 0.84 | {'b': 66, 'other': 33, 'oc': 1} |
| clean|push|random|band|8.0|r|None | 100 | 1% [0, 5] | 0.12 | {'A': 99, 'b': 1} |
| clean|push|lens|band|8.0|a|None | 100 | 2% [1, 7] | 0.65 | {'other': 98, 'b': 2} |
| clean|push|random|band|8.0|a|None | 100 | 0% [0, 4] | 0.15 | {'A': 84, 'other': 16} |
| clean|push|lens|band|8.0|b|None | 100 | 77% [68, 84] | 0.86 | {'b': 77, 'other': 23} |
| clean|push|random|band|8.0|b|None | 100 | 0% [0, 4] | 0.08 | {'A': 98, 'other': 2} |
| clean|push|lens|band|16.0|r|None | 100 | 25% [18, 34] | 0.67 | {'other': 75, 'b': 25} |
| clean|push|random|band|16.0|r|None | 100 | 16% [10, 24] | 0.38 | {'A': 71, 'other': 6, 'b': 16, 'oc': 7} |
| clean|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | 0.57 | {'other': 100} |
| clean|push|random|band|16.0|a|None | 100 | 0% [0, 4] | 0.48 | {'other': 100} |
| clean|push|lens|band|16.0|b|None | 100 | 69% [59, 77] | 0.86 | {'b': 69, 'other': 30, 'A': 1} |
| clean|push|random|band|16.0|b|None | 100 | 15% [9, 23] | 0.38 | {'other': 24, 'A': 58, 'oc': 3, 'b': 15} |
| clean|emb_diff|lens|-1|1.0|b|None | 100 | 45% [36, 55] | 0.47 | {'A': 43, 'b': 45, 'other': 12} |
| clean|emb_diff|random|-1|1.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|emb_add|lens|-1|1.0|b|None | 100 | 51% [41, 61] | 0.51 | {'A': 35, 'b': 51, 'other': 14} |
| clean|emb_add|random|-1|1.0|b|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|emb_diff|lens|-1|4.0|b|None | 100 | 59% [49, 68] | 0.58 | {'b': 59, 'A': 21, 'oc': 12, 'other': 8} |
| clean|emb_diff|random|-1|4.0|b|None | 100 | 27% [19, 36] | 0.47 | {'A': 55, 'oc': 11, 'b': 27, 'other': 7} |
| clean|emb_add|lens|-1|4.0|b|None | 100 | 3% [1, 8] | 0.50 | {'other': 42, 'A': 35, 'oc': 20, 'b': 3} |
| clean|emb_add|random|-1|4.0|b|None | 100 | 37% [28, 47] | 0.48 | {'A': 51, 'oc': 9, 'b': 37, 'other': 3} |
| clean|copy|None|16|None|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|copy|None|20|None|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|copy|None|24|None|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|copy|None|28|None|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|copy|None|32|None|r|None | 100 | 5% [2, 11] | 0.12 | {'A': 95, 'b': 5} |
| clean|copy|None|36|None|r|None | 100 | 7% [3, 14] | 0.23 | {'A': 93, 'b': 7} |
| clean|copy|None|40|None|r|None | 100 | 22% [15, 31] | 0.35 | {'A': 78, 'b': 22} |
| clean|copy|None|44|None|r|None | 100 | 8% [4, 15] | 0.33 | {'A': 92, 'b': 8} |
| clean|copy|None|48|None|r|None | 100 | 16% [10, 24] | 0.36 | {'A': 84, 'b': 16} |
| clean|patch|None|16|None|a|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|patch|None|16|4.0|a|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|patch|None|16|8.0|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|patch|None|16|16.0|a|None | 100 | 0% [0, 4] | 0.09 | {'A': 98, 'other': 2} |
| clean|patch|None|20|None|a|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|patch|None|20|4.0|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|patch|None|20|8.0|a|None | 100 | 0% [0, 4] | 0.07 | {'A': 98, 'other': 2} |
| clean|patch|None|20|16.0|a|None | 100 | 8% [4, 15] | 0.25 | {'A': 79, 'oc': 1, 'other': 12, 'b': 8} |
| clean|patch|None|24|None|a|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|patch|None|24|4.0|a|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|patch|None|24|8.0|a|None | 100 | 4% [2, 10] | 0.15 | {'A': 95, 'b': 4, 'other': 1} |
| clean|patch|None|24|16.0|a|None | 100 | 26% [18, 35] | 0.45 | {'A': 42, 'other': 32, 'b': 26} |
| clean|patch|None|28|None|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|patch|None|28|4.0|a|None | 100 | 5% [2, 11] | 0.17 | {'A': 95, 'b': 5} |
| clean|patch|None|28|8.0|a|None | 100 | 31% [23, 41] | 0.41 | {'A': 65, 'b': 31, 'other': 3, 'oc': 1} |
| clean|patch|None|28|16.0|a|None | 100 | 36% [27, 46] | 0.61 | {'other': 44, 'A': 18, 'b': 36, 'oc': 2} |
| off|push|lens|16|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 98, 'other': 2} |
| off|push|lens|16|8.0|a|None | 100 | 0% [0, 4] | nan | {'other': 45, 'bO': 27, 'A': 28} |
| off|push|lens|16|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 80, 'bO': 20} |
| off|push|lens|20|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 98, 'other': 2} |
| off|push|lens|20|8.0|a|None | 100 | 0% [0, 4] | nan | {'A': 89, 'other': 10, 'bO': 1} |
| off|push|lens|20|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 56, 'A': 32, 'bO': 12} |
| off|push|lens|24|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 92, 'other': 7, 'bO': 1} |
| off|push|lens|24|8.0|a|None | 100 | 0% [0, 4] | nan | {'A': 81, 'other': 14, 'bO': 5} |
| off|push|lens|24|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 58, 'bO': 17, 'A': 25} |
| off|push|lens|28|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 94, 'other': 3, 'bO': 3} |
| off|push|lens|28|8.0|a|None | 100 | 0% [0, 4] | nan | {'A': 33, 'bO': 46, 'other': 21} |
| off|push|lens|28|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 85, 'A': 2, 'bO': 13} |
| off|push|lens|band|4.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 56, 'other': 40, 'A': 3, 'oc': 1} |
| off|push|lens|band|8.0|a|None | 100 | 0% [0, 4] | nan | {'other': 98, 'bO': 2} |
| off|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 100} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.01 [+0.00, +0.03] (ref rate 1.00); E-insert: k +0.04 [+0.03, +0.15], J +0.03 [+0.00, +0.11] (ref rate 0.32); E-head: k +0.05 [+0.03, +0.16], J +0.03 [+0.00, +0.12] (ref rate 0.30); E-cue: k -, J +0.01 [+0.00, +0.03] (ref rate 1.00); E-unrelated: k -, J +0.00 [+0.00, +0.00] (ref rate 0.00); W-copy*: k +0.07 [+0.05, +0.23], J +0.05 [+0.00, +0.15] (ref rate 0.22); emb*: k -0.02 [-0.08, -0.02], J +0.00 [+0.00, +0.00] (ref rate 0.51); patch_matched: k -, J +0.00 [+0.00, +0.00] (ref rate 0.00); low_margin: k +0.02 [+0.01, +0.08]
K1 -0.03 [-0.12, -0.00] -> write; gate -0.12 [-0.30, +0.05]; K2 nb - a/2 -0.01 [-0.01, +0.00], b - nb +0.00 [+0.00, +0.00] -> inconclusive; K4 -0.16 [-0.18, -0.14]
JS(P*, .) {"clean": 0.041, "E-name": 0.652, "E-insert": 0.445, "E-head": 0.578, "E-cue": 0.642, "E-unrelated": 0.035}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [0.0432, -0.0098, -0.0365, -0.0156], "E-insert": [0.0923, 0.122, 0.1374, 0.1639], "E-head": [0.1963, 0.2267, 0.2069, 0.2009], "E-cue": [0.1697, 0.1762, 0.1418, 0.1453], "E-unrelated": [0.1516, 0.1728, 0.1783, 0.2265]}
transit proj on C's delta [44, 48, 52]: P*_b [0.0737, 0.0734, 0.077], P* [0.224, 0.2226, 0.2154], edits {"E-name": [0.8136, 0.7771, 0.7684], "E-insert": [0.6162, 0.5939, 0.547], "E-head": [0.7099, 0.6859, 0.6713], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.1171, 0.1408, 0.1451]}

## RL (W-copy* = ('clean', 'copy', None, 44, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|edit|None|None|None|None|E-name | 100 | 100% [96, 100] | 1.02 | {'b': 100} |
| clean|edit|None|None|None|None|E-insert | 100 | 100% [96, 100] | 0.69 | {'b': 100} |
| clean|edit|None|None|None|None|E-head | 100 | 67% [57, 75] | 0.55 | {'A': 33, 'b': 67} |
| clean|edit|None|None|None|None|E-cue | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|edit|None|None|None|None|E-unrelated | 100 | 0% [0, 4] | 0.06 | {'A': 100} |
| clean|push|lens|16|4.0|r|None | 100 | 5% [2, 11] | 0.16 | {'A': 95, 'b': 5} |
| clean|push|random|16|4.0|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|16|4.0|a|None | 100 | 22% [15, 31] | 0.36 | {'A': 74, 'b': 22, 'oc': 4} |
| clean|push|random|16|4.0|a|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|16|4.0|b|None | 100 | 20% [13, 29] | 0.33 | {'A': 76, 'b': 20, 'oc': 4} |
| clean|push|random|16|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|16|8.0|r|None | 100 | 21% [14, 30] | 0.35 | {'A': 79, 'b': 21} |
| clean|push|random|16|8.0|r|None | 100 | 0% [0, 4] | 0.03 | {'A': 99, 'oc': 1} |
| clean|push|lens|16|8.0|a|None | 100 | 94% [88, 97] | 0.75 | {'b': 94, 'A': 4, 'oc': 2} |
| clean|push|random|16|8.0|a|None | 100 | 0% [0, 4] | 0.06 | {'A': 100} |
| clean|push|lens|16|8.0|b|None | 100 | 93% [86, 97] | 0.79 | {'b': 93, 'A': 5, 'oc': 2} |
| clean|push|random|16|8.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 99, 'oc': 1} |
| clean|push|lens|16|16.0|r|None | 100 | 49% [39, 59] | 0.47 | {'A': 51, 'b': 49} |
| clean|push|random|16|16.0|r|None | 100 | 0% [0, 4] | 0.10 | {'A': 99, 'oc': 1} |
| clean|push|lens|16|16.0|a|None | 100 | 30% [22, 40] | 0.73 | {'other': 70, 'b': 30} |
| clean|push|random|16|16.0|a|None | 100 | 0% [0, 4] | 0.15 | {'A': 99, 'other': 1} |
| clean|push|lens|16|16.0|b|None | 100 | 100% [96, 100] | 0.91 | {'b': 100} |
| clean|push|random|16|16.0|b|None | 100 | 0% [0, 4] | 0.06 | {'A': 100} |
| clean|push|lens|20|4.0|r|None | 100 | 2% [1, 7] | 0.08 | {'A': 97, 'oc': 1, 'b': 2} |
| clean|push|random|20|4.0|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|20|4.0|a|None | 100 | 18% [12, 27] | 0.27 | {'A': 81, 'b': 18, 'oc': 1} |
| clean|push|random|20|4.0|a|None | 100 | 0% [0, 4] | 0.04 | {'A': 99, 'oc': 1} |
| clean|push|lens|20|4.0|b|None | 100 | 13% [8, 21] | 0.22 | {'A': 86, 'b': 13, 'oc': 1} |
| clean|push|random|20|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|20|8.0|r|None | 100 | 19% [13, 28] | 0.28 | {'A': 81, 'b': 19} |
| clean|push|random|20|8.0|r|None | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|push|lens|20|8.0|a|None | 100 | 78% [69, 85] | 0.62 | {'b': 78, 'A': 20, 'oc': 2} |
| clean|push|random|20|8.0|a|None | 100 | 0% [0, 4] | 0.12 | {'A': 100} |
| clean|push|lens|20|8.0|b|None | 100 | 73% [64, 81] | 0.63 | {'b': 73, 'A': 25, 'oc': 2} |
| clean|push|random|20|8.0|b|None | 100 | 0% [0, 4] | 0.02 | {'A': 99, 'oc': 1} |
| clean|push|lens|20|16.0|r|None | 100 | 35% [26, 45] | 0.43 | {'A': 62, 'b': 35, 'oc': 3} |
| clean|push|random|20|16.0|r|None | 100 | 1% [0, 5] | 0.14 | {'A': 98, 'oc': 1, 'b': 1} |
| clean|push|lens|20|16.0|a|None | 100 | 70% [60, 78] | 0.71 | {'b': 70, 'other': 30} |
| clean|push|random|20|16.0|a|None | 100 | 0% [0, 4] | 0.21 | {'A': 94, 'other': 5, 'oc': 1} |
| clean|push|lens|20|16.0|b|None | 100 | 100% [96, 100] | 0.82 | {'b': 100} |
| clean|push|random|20|16.0|b|None | 100 | 0% [0, 4] | 0.10 | {'A': 98, 'oc': 2} |
| clean|push|lens|24|4.0|r|None | 100 | 6% [3, 12] | 0.13 | {'A': 93, 'b': 6, 'oc': 1} |
| clean|push|random|24|4.0|r|None | 100 | 0% [0, 4] | 0.02 | {'A': 99, 'oc': 1} |
| clean|push|lens|24|4.0|a|None | 100 | 40% [31, 50] | 0.42 | {'A': 57, 'b': 40, 'oc': 3} |
| clean|push|random|24|4.0|a|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|lens|24|4.0|b|None | 100 | 33% [25, 43] | 0.37 | {'A': 64, 'b': 33, 'oc': 3} |
| clean|push|random|24|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|24|8.0|r|None | 100 | 24% [17, 33] | 0.35 | {'A': 76, 'b': 24} |
| clean|push|random|24|8.0|r|None | 100 | 0% [0, 4] | 0.08 | {'A': 99, 'oc': 1} |
| clean|push|lens|24|8.0|a|None | 100 | 94% [88, 97] | 0.67 | {'b': 94, 'A': 3, 'oc': 3} |
| clean|push|random|24|8.0|a|None | 100 | 0% [0, 4] | 0.12 | {'A': 100} |
| clean|push|lens|24|8.0|b|None | 100 | 95% [89, 98] | 0.74 | {'b': 95, 'A': 4, 'oc': 1} |
| clean|push|random|24|8.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|24|16.0|r|None | 100 | 26% [18, 35] | 0.44 | {'A': 66, 'b': 26, 'oc': 8} |
| clean|push|random|24|16.0|r|None | 100 | 0% [0, 4] | 0.21 | {'A': 97, 'oc': 3} |
| clean|push|lens|24|16.0|a|None | 100 | 66% [56, 75] | 0.66 | {'b': 66, 'other': 30, 'oc': 4} |
| clean|push|random|24|16.0|a|None | 100 | 1% [0, 5] | 0.26 | {'A': 88, 'oc': 4, 'other': 7, 'b': 1} |
| clean|push|lens|24|16.0|b|None | 100 | 98% [93, 99] | 0.77 | {'b': 98, 'oc': 2} |
| clean|push|random|24|16.0|b|None | 100 | 0% [0, 4] | 0.10 | {'A': 100} |
| clean|push|lens|28|4.0|r|None | 100 | 16% [10, 24] | 0.32 | {'A': 84, 'b': 16} |
| clean|push|random|28|4.0|r|None | 100 | 0% [0, 4] | 0.05 | {'A': 99, 'oc': 1} |
| clean|push|lens|28|4.0|a|None | 100 | 35% [26, 45] | 0.39 | {'A': 64, 'b': 35, 'oc': 1} |
| clean|push|random|28|4.0|a|None | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|push|lens|28|4.0|b|None | 100 | 13% [8, 21] | 0.23 | {'A': 87, 'b': 13} |
| clean|push|random|28|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|28|8.0|r|None | 100 | 30% [22, 40] | 0.42 | {'A': 64, 'b': 30, 'oc': 6} |
| clean|push|random|28|8.0|r|None | 100 | 0% [0, 4] | 0.17 | {'A': 99, 'oc': 1} |
| clean|push|lens|28|8.0|a|None | 100 | 74% [65, 82] | 0.58 | {'A': 20, 'b': 74, 'oc': 5, 'other': 1} |
| clean|push|random|28|8.0|a|None | 100 | 0% [0, 4] | 0.15 | {'A': 100} |
| clean|push|lens|28|8.0|b|None | 100 | 48% [38, 58] | 0.46 | {'A': 49, 'b': 48, 'oc': 3} |
| clean|push|random|28|8.0|b|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|28|16.0|r|None | 100 | 11% [6, 19] | 0.36 | {'A': 82, 'oc': 7, 'b': 11} |
| clean|push|random|28|16.0|r|None | 100 | 1% [0, 5] | 0.29 | {'A': 95, 'oc': 4, 'b': 1} |
| clean|push|lens|28|16.0|a|None | 100 | 15% [9, 23] | 0.53 | {'other': 69, 'b': 15, 'A': 9, 'oc': 7} |
| clean|push|random|28|16.0|a|None | 100 | 0% [0, 4] | 0.36 | {'other': 22, 'A': 76, 'oc': 2} |
| clean|push|lens|28|16.0|b|None | 100 | 67% [57, 75] | 0.55 | {'A': 29, 'b': 67, 'oc': 4} |
| clean|push|random|28|16.0|b|None | 100 | 0% [0, 4] | 0.17 | {'A': 100} |
| clean|push|lens|band|4.0|r|None | 100 | 48% [38, 58] | 0.50 | {'A': 49, 'b': 48, 'oc': 3} |
| clean|push|random|band|4.0|r|None | 100 | 0% [0, 4] | 0.07 | {'A': 99, 'oc': 1} |
| clean|push|lens|band|4.0|a|None | 100 | 91% [84, 95] | 0.75 | {'b': 91, 'other': 8, 'oc': 1} |
| clean|push|random|band|4.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 100} |
| clean|push|lens|band|4.0|b|None | 100 | 100% [96, 100] | 0.88 | {'b': 100} |
| clean|push|random|band|4.0|b|None | 100 | 0% [0, 4] | 0.02 | {'A': 99, 'oc': 1} |
| clean|push|lens|band|8.0|r|None | 100 | 32% [24, 42] | 0.44 | {'A': 58, 'b': 32, 'oc': 10} |
| clean|push|random|band|8.0|r|None | 100 | 1% [0, 5] | 0.17 | {'A': 98, 'oc': 1, 'b': 1} |
| clean|push|lens|band|8.0|a|None | 100 | 3% [1, 8] | 0.59 | {'other': 97, 'b': 3} |
| clean|push|random|band|8.0|a|None | 100 | 2% [1, 7] | 0.26 | {'A': 89, 'other': 8, 'b': 2, 'oc': 1} |
| clean|push|lens|band|8.0|b|None | 100 | 98% [93, 99] | 0.77 | {'b': 98, 'oc': 2} |
| clean|push|random|band|8.0|b|None | 100 | 0% [0, 4] | 0.11 | {'A': 98, 'oc': 2} |
| clean|push|lens|band|16.0|r|None | 100 | 8% [4, 15] | 0.40 | {'other': 61, 'A': 27, 'oc': 4, 'b': 8} |
| clean|push|random|band|16.0|r|None | 100 | 3% [1, 8] | 0.27 | {'A': 93, 'b': 3, 'oc': 4} |
| clean|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | 0.50 | {'other': 100} |
| clean|push|random|band|16.0|a|None | 100 | 0% [0, 4] | 0.47 | {'other': 98, 'A': 2} |
| clean|push|lens|band|16.0|b|None | 100 | 91% [84, 95] | 0.68 | {'b': 91, 'oc': 9} |
| clean|push|random|band|16.0|b|None | 100 | 11% [6, 19] | 0.43 | {'A': 76, 'oc': 13, 'b': 11} |
| clean|emb_diff|lens|-1|1.0|b|None | 100 | 98% [93, 99] | 0.79 | {'b': 98, 'A': 2} |
| clean|emb_diff|random|-1|1.0|b|None | 100 | 6% [3, 12] | 0.18 | {'A': 89, 'b': 6, 'oc': 5} |
| clean|emb_add|lens|-1|1.0|b|None | 100 | 94% [88, 97] | 0.80 | {'b': 94, 'A': 6} |
| clean|emb_add|random|-1|1.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|emb_diff|lens|-1|4.0|b|None | 100 | 97% [92, 99] | 0.73 | {'b': 97, 'oc': 2, 'A': 1} |
| clean|emb_diff|random|-1|4.0|b|None | 100 | 26% [18, 35] | 0.49 | {'A': 35, 'b': 26, 'oc': 39} |
| clean|emb_add|lens|-1|4.0|b|None | 100 | 100% [96, 100] | 0.94 | {'b': 100} |
| clean|emb_add|random|-1|4.0|b|None | 100 | 24% [17, 33] | 0.49 | {'A': 40, 'oc': 36, 'b': 24} |
| clean|copy|None|16|None|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|copy|None|20|None|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 99, 'oc': 1} |
| clean|copy|None|24|None|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 99, 'oc': 1} |
| clean|copy|None|28|None|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|copy|None|32|None|r|None | 100 | 1% [0, 5] | 0.15 | {'A': 98, 'oc': 1, 'b': 1} |
| clean|copy|None|36|None|r|None | 100 | 27% [19, 36] | 0.41 | {'b': 27, 'A': 73} |
| clean|copy|None|40|None|r|None | 100 | 39% [30, 49] | 0.45 | {'b': 39, 'A': 61} |
| clean|copy|None|44|None|r|None | 100 | 54% [44, 63] | 0.52 | {'b': 54, 'A': 46} |
| clean|copy|None|48|None|r|None | 100 | 85% [77, 91] | 0.63 | {'b': 85, 'A': 15} |
| clean|patch|None|16|None|a|None | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|patch|None|16|4.0|a|None | 100 | 2% [1, 7] | 0.08 | {'A': 97, 'b': 2, 'oc': 1} |
| clean|patch|None|16|8.0|a|None | 100 | 69% [59, 77] | 0.65 | {'A': 28, 'b': 69, 'oc': 3} |
| clean|patch|None|16|16.0|a|None | 100 | 100% [96, 100] | 0.89 | {'b': 100} |
| clean|patch|None|20|None|a|None | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|patch|None|20|4.0|a|None | 100 | 4% [2, 10] | 0.14 | {'A': 95, 'b': 4, 'oc': 1} |
| clean|patch|None|20|8.0|a|None | 100 | 90% [83, 94] | 0.77 | {'b': 90, 'A': 9, 'oc': 1} |
| clean|patch|None|20|16.0|a|None | 100 | 96% [90, 98] | 0.88 | {'b': 96, 'other': 4} |
| clean|patch|None|24|None|a|None | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|patch|None|24|4.0|a|None | 100 | 6% [3, 12] | 0.17 | {'A': 94, 'b': 6} |
| clean|patch|None|24|8.0|a|None | 100 | 85% [77, 91] | 0.74 | {'b': 85, 'A': 14, 'oc': 1} |
| clean|patch|None|24|16.0|a|None | 100 | 92% [85, 96] | 0.86 | {'b': 92, 'other': 8} |
| clean|patch|None|28|None|a|None | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|patch|None|28|4.0|a|None | 100 | 27% [19, 36] | 0.39 | {'A': 72, 'b': 27, 'oc': 1} |
| clean|patch|None|28|8.0|a|None | 100 | 99% [95, 100] | 0.87 | {'b': 99, 'A': 1} |
| clean|patch|None|28|16.0|a|None | 100 | 82% [73, 88] | 0.82 | {'other': 18, 'b': 82} |
| off|push|lens|16|4.0|a|None | 100 | 4% [2, 10] | nan | {'A': 74, 'bO': 22, 'b': 4} |
| off|push|lens|16|8.0|a|None | 100 | 3% [1, 8] | nan | {'bO': 93, 'A': 4, 'b': 3} |
| off|push|lens|16|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 69, 'bO': 31} |
| off|push|lens|20|4.0|a|None | 100 | 2% [1, 7] | nan | {'A': 82, 'bO': 16, 'b': 2} |
| off|push|lens|20|8.0|a|None | 100 | 2% [1, 7] | nan | {'bO': 77, 'A': 21, 'b': 2} |
| off|push|lens|20|16.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 72, 'other': 28} |
| off|push|lens|24|4.0|a|None | 100 | 3% [1, 8] | nan | {'A': 55, 'bO': 42, 'b': 3} |
| off|push|lens|24|8.0|a|None | 100 | 2% [1, 7] | nan | {'bO': 94, 'A': 4, 'b': 2} |
| off|push|lens|24|16.0|a|None | 100 | 4% [2, 10] | nan | {'bO': 66, 'other': 30, 'b': 4} |
| off|push|lens|28|4.0|a|None | 100 | 2% [1, 7] | nan | {'A': 65, 'bO': 33, 'b': 2} |
| off|push|lens|28|8.0|a|None | 100 | 6% [3, 12] | nan | {'A': 21, 'bO': 72, 'b': 6, 'other': 1} |
| off|push|lens|28|16.0|a|None | 100 | 7% [3, 14] | nan | {'other': 68, 'bO': 17, 'A': 8, 'b': 7} |
| off|push|lens|band|4.0|a|None | 100 | 1% [0, 5] | nan | {'bO': 90, 'other': 9, 'b': 1} |
| off|push|lens|band|8.0|a|None | 100 | 0% [0, 4] | nan | {'other': 97, 'bO': 3} |
| off|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 100} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.40 [+0.31, +0.50] (ref rate 1.00); E-insert: k -, J +0.40 [+0.31, +0.50] (ref rate 1.00); E-head: k -0.10 [-0.29, +0.07], J +0.29 [+0.19, +0.40] (ref rate 0.67); E-cue: k -, J +0.40 [+0.31, +0.50] (ref rate 1.00); E-unrelated: k -, J +0.00 [+0.00, +0.00] (ref rate 0.00); W-copy*: k -0.02 [-0.21, +0.18], J +0.29 [+0.19, +0.40] (ref rate 0.54); emb*: k -0.09 [-0.19, -0.01], J +0.35 [+0.26, +0.45] (ref rate 0.94); patch_matched: k +0.13 [+0.01, +0.26], J +0.12 [+0.03, +0.23] (ref rate 0.06); low_margin: k +0.08 [-0.11, +0.27]
K1 - -> untestable; gate -; K2 nb - a/2 -0.20 [-0.25, -0.15], b - nb +0.33 [+0.24, +0.42] -> write; K4 -0.30 [-0.33, -0.28]
JS(P*, .) {"clean": 0.24, "E-name": 0.371, "E-insert": 0.299, "E-head": 0.156, "E-cue": 0.367, "E-unrelated": 0.228}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [-0.0519, -0.1095, -0.0749, 0.0109], "E-insert": [0.0847, 0.1709, 0.2192, 0.2388], "E-head": [0.2095, 0.2792, 0.2986, 0.2688], "E-cue": [0.2182, 0.2269, 0.2093, 0.238], "E-unrelated": [0.1634, 0.2034, 0.2267, 0.2368]}
transit proj on C's delta [44, 48, 52]: P*_b [0.193, 0.2045, 0.2233], P* [0.3071, 0.3086, 0.3104], edits {"E-name": [0.5812, 0.5923, 0.6057], "E-insert": [0.5343, 0.5419, 0.5447], "E-head": [0.4204, 0.4384, 0.454], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.1849, 0.184, 0.1727]}

## RR (W-copy* = ('clean', 'copy', None, 48, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|edit|None|None|None|None|E-name | 100 | 100% [96, 100] | 1.07 | {'b': 100} |
| clean|edit|None|None|None|None|E-insert | 100 | 94% [88, 97] | 0.77 | {'other': 1, 'b': 94, 'A': 5} |
| clean|edit|None|None|None|None|E-head | 100 | 57% [47, 66] | 0.68 | {'other': 40, 'b': 57, 'A': 3} |
| clean|edit|None|None|None|None|E-cue | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|edit|None|None|None|None|E-unrelated | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|push|lens|16|4.0|r|None | 100 | 8% [4, 15] | 0.15 | {'A': 90, 'b': 8, 'other': 2} |
| clean|push|random|16|4.0|r|None | 100 | 0% [0, 4] | -0.01 | {'A': 100} |
| clean|push|lens|16|4.0|a|None | 100 | 32% [24, 42] | 0.39 | {'A': 66, 'b': 32, 'other': 2} |
| clean|push|random|16|4.0|a|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|16|4.0|b|None | 100 | 24% [17, 33] | 0.32 | {'A': 75, 'b': 24, 'other': 1} |
| clean|push|random|16|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|16|8.0|r|None | 100 | 41% [32, 51] | 0.46 | {'A': 49, 'other': 10, 'b': 41} |
| clean|push|random|16|8.0|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|16|8.0|a|None | 100 | 97% [92, 99] | 0.90 | {'b': 97, 'A': 3} |
| clean|push|random|16|8.0|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|16|8.0|b|None | 100 | 95% [89, 98] | 0.88 | {'b': 95, 'A': 3, 'other': 2} |
| clean|push|random|16|8.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|16|16.0|r|None | 100 | 70% [60, 78] | 0.64 | {'A': 19, 'b': 70, 'other': 11} |
| clean|push|random|16|16.0|r|None | 100 | 0% [0, 4] | 0.03 | {'A': 99, 'oc': 1} |
| clean|push|lens|16|16.0|a|None | 100 | 27% [19, 36] | 0.85 | {'other': 73, 'b': 27} |
| clean|push|random|16|16.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 97, 'oc': 1, 'other': 2} |
| clean|push|lens|16|16.0|b|None | 100 | 98% [93, 99] | 0.96 | {'b': 98, 'other': 2} |
| clean|push|random|16|16.0|b|None | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|push|lens|20|4.0|r|None | 100 | 3% [1, 8] | 0.07 | {'A': 97, 'b': 3} |
| clean|push|random|20|4.0|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|20|4.0|a|None | 100 | 14% [9, 22] | 0.25 | {'A': 82, 'b': 14, 'other': 4} |
| clean|push|random|20|4.0|a|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|20|4.0|b|None | 100 | 15% [9, 23] | 0.21 | {'A': 85, 'b': 15} |
| clean|push|random|20|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|20|8.0|r|None | 100 | 16% [10, 24] | 0.23 | {'A': 79, 'other': 5, 'b': 16} |
| clean|push|random|20|8.0|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|20|8.0|a|None | 100 | 71% [61, 79] | 0.67 | {'A': 20, 'other': 9, 'b': 71} |
| clean|push|random|20|8.0|a|None | 100 | 0% [0, 4] | 0.06 | {'A': 100} |
| clean|push|lens|20|8.0|b|None | 100 | 84% [76, 90] | 0.71 | {'b': 84, 'A': 15, 'other': 1} |
| clean|push|random|20|8.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|20|16.0|r|None | 100 | 46% [37, 56] | 0.51 | {'A': 43, 'b': 46, 'other': 11} |
| clean|push|random|20|16.0|r|None | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|push|lens|20|16.0|a|None | 100 | 52% [42, 62] | 0.76 | {'other': 43, 'b': 52, 'A': 3, 'oc': 2} |
| clean|push|random|20|16.0|a|None | 100 | 1% [0, 5] | 0.15 | {'A': 94, 'b': 1, 'other': 5} |
| clean|push|lens|20|16.0|b|None | 100 | 99% [95, 100] | 0.92 | {'b': 99, 'other': 1} |
| clean|push|random|20|16.0|b|None | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|push|lens|24|4.0|r|None | 100 | 5% [2, 11] | 0.15 | {'A': 95, 'b': 5} |
| clean|push|random|24|4.0|r|None | 100 | 0% [0, 4] | -0.01 | {'A': 100} |
| clean|push|lens|24|4.0|a|None | 100 | 36% [27, 46] | 0.43 | {'A': 58, 'other': 5, 'b': 36, 'oc': 1} |
| clean|push|random|24|4.0|a|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|24|4.0|b|None | 100 | 32% [24, 42] | 0.38 | {'A': 62, 'other': 6, 'b': 32} |
| clean|push|random|24|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|24|8.0|r|None | 100 | 21% [14, 30] | 0.32 | {'A': 70, 'other': 9, 'b': 21} |
| clean|push|random|24|8.0|r|None | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|push|lens|24|8.0|a|None | 100 | 85% [77, 91] | 0.75 | {'b': 85, 'A': 11, 'other': 3, 'oc': 1} |
| clean|push|random|24|8.0|a|None | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|push|lens|24|8.0|b|None | 100 | 96% [90, 98] | 0.85 | {'b': 96, 'A': 3, 'other': 1} |
| clean|push|random|24|8.0|b|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|24|16.0|r|None | 100 | 42% [33, 52] | 0.48 | {'A': 47, 'other': 10, 'b': 42, 'oc': 1} |
| clean|push|random|24|16.0|r|None | 100 | 0% [0, 4] | 0.13 | {'A': 100} |
| clean|push|lens|24|16.0|a|None | 100 | 45% [36, 55] | 0.71 | {'other': 50, 'b': 45, 'oc': 2, 'A': 3} |
| clean|push|random|24|16.0|a|None | 100 | 1% [0, 5] | 0.20 | {'A': 86, 'other': 12, 'b': 1, 'oc': 1} |
| clean|push|lens|24|16.0|b|None | 100 | 93% [86, 97] | 0.91 | {'b': 93, 'other': 7} |
| clean|push|random|24|16.0|b|None | 100 | 2% [1, 7] | 0.11 | {'A': 98, 'b': 2} |
| clean|push|lens|28|4.0|r|None | 100 | 26% [18, 35] | 0.35 | {'A': 72, 'b': 26, 'oc': 2} |
| clean|push|random|28|4.0|r|None | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|push|lens|28|4.0|a|None | 100 | 48% [38, 58] | 0.51 | {'A': 50, 'b': 48, 'other': 2} |
| clean|push|random|28|4.0|a|None | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|push|lens|28|4.0|b|None | 100 | 15% [9, 23] | 0.24 | {'A': 84, 'b': 15, 'other': 1} |
| clean|push|random|28|4.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|28|8.0|r|None | 100 | 45% [36, 55] | 0.44 | {'A': 50, 'b': 45, 'other': 3, 'oc': 2} |
| clean|push|random|28|8.0|r|None | 100 | 1% [0, 5] | 0.11 | {'A': 98, 'b': 1, 'oc': 1} |
| clean|push|lens|28|8.0|a|None | 100 | 80% [71, 87] | 0.80 | {'A': 7, 'b': 80, 'other': 11, 'oc': 2} |
| clean|push|random|28|8.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 100} |
| clean|push|lens|28|8.0|b|None | 100 | 63% [53, 72] | 0.58 | {'A': 35, 'b': 63, 'other': 2} |
| clean|push|random|28|8.0|b|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|28|16.0|r|None | 100 | 34% [25, 44] | 0.39 | {'A': 62, 'b': 34, 'other': 3, 'oc': 1} |
| clean|push|random|28|16.0|r|None | 100 | 3% [1, 8] | 0.20 | {'A': 96, 'b': 3, 'oc': 1} |
| clean|push|lens|28|16.0|a|None | 100 | 12% [7, 20] | 0.68 | {'other': 88, 'b': 12} |
| clean|push|random|28|16.0|a|None | 100 | 4% [2, 10] | 0.30 | {'A': 69, 'other': 27, 'b': 4} |
| clean|push|lens|28|16.0|b|None | 100 | 81% [72, 87] | 0.71 | {'A': 12, 'b': 81, 'other': 7} |
| clean|push|random|28|16.0|b|None | 100 | 0% [0, 4] | 0.16 | {'A': 100} |
| clean|push|lens|band|4.0|r|None | 100 | 59% [49, 68] | 0.65 | {'b': 59, 'A': 15, 'other': 26} |
| clean|push|random|band|4.0|r|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|band|4.0|a|None | 100 | 77% [68, 84] | 0.90 | {'other': 19, 'b': 77, 'oc': 2, 'A': 2} |
| clean|push|random|band|4.0|a|None | 100 | 0% [0, 4] | 0.06 | {'A': 100} |
| clean|push|lens|band|4.0|b|None | 100 | 99% [95, 100] | 0.97 | {'b': 99, 'other': 1} |
| clean|push|random|band|4.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|band|8.0|r|None | 100 | 61% [51, 70] | 0.62 | {'A': 17, 'b': 61, 'other': 21, 'oc': 1} |
| clean|push|random|band|8.0|r|None | 100 | 2% [1, 7] | 0.12 | {'A': 97, 'b': 2, 'oc': 1} |
| clean|push|lens|band|8.0|a|None | 100 | 3% [1, 8] | 0.65 | {'other': 97, 'b': 3} |
| clean|push|random|band|8.0|a|None | 100 | 1% [0, 5] | 0.19 | {'A': 78, 'other': 20, 'b': 1, 'oc': 1} |
| clean|push|lens|band|8.0|b|None | 100 | 94% [88, 97] | 0.93 | {'b': 94, 'other': 6} |
| clean|push|random|band|8.0|b|None | 100 | 2% [1, 7] | 0.13 | {'A': 96, 'other': 1, 'oc': 1, 'b': 2} |
| clean|push|lens|band|16.0|r|None | 100 | 17% [11, 26] | 0.41 | {'other': 62, 'b': 17, 'A': 19, 'oc': 2} |
| clean|push|random|band|16.0|r|None | 100 | 3% [1, 8] | 0.22 | {'A': 96, 'b': 3, 'oc': 1} |
| clean|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | 0.56 | {'other': 100} |
| clean|push|random|band|16.0|a|None | 100 | 1% [0, 5] | 0.49 | {'other': 96, 'A': 3, 'b': 1} |
| clean|push|lens|band|16.0|b|None | 100 | 83% [74, 89] | 0.86 | {'b': 83, 'other': 16, 'A': 1} |
| clean|push|random|band|16.0|b|None | 100 | 9% [5, 16] | 0.39 | {'A': 72, 'oc': 3, 'b': 9, 'other': 16} |
| clean|emb_diff|lens|-1|1.0|b|None | 100 | 92% [85, 96] | 0.77 | {'b': 92, 'A': 2, 'other': 6} |
| clean|emb_diff|random|-1|1.0|b|None | 100 | 6% [3, 12] | 0.17 | {'A': 91, 'b': 6, 'oc': 2, 'other': 1} |
| clean|emb_add|lens|-1|1.0|b|None | 100 | 91% [84, 95] | 0.76 | {'b': 91, 'A': 6, 'other': 3} |
| clean|emb_add|random|-1|1.0|b|None | 100 | 1% [0, 5] | 0.01 | {'A': 99, 'b': 1} |
| clean|emb_diff|lens|-1|4.0|b|None | 100 | 47% [38, 57] | 0.56 | {'b': 47, 'A': 14, 'other': 27, 'oc': 12} |
| clean|emb_diff|random|-1|4.0|b|None | 100 | 29% [21, 39] | 0.48 | {'A': 55, 'oc': 11, 'b': 29, 'other': 5} |
| clean|emb_add|lens|-1|4.0|b|None | 100 | 2% [1, 7] | 0.47 | {'other': 43, 'A': 35, 'oc': 20, 'b': 2} |
| clean|emb_add|random|-1|4.0|b|None | 100 | 32% [24, 42] | 0.48 | {'A': 52, 'oc': 10, 'b': 32, 'other': 6} |
| clean|copy|None|16|None|r|None | 100 | 0% [0, 4] | -0.01 | {'A': 100} |
| clean|copy|None|20|None|r|None | 100 | 0% [0, 4] | -0.01 | {'A': 100} |
| clean|copy|None|24|None|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|copy|None|28|None|r|None | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|copy|None|32|None|r|None | 100 | 3% [1, 8] | 0.17 | {'A': 97, 'b': 3} |
| clean|copy|None|36|None|r|None | 100 | 5% [2, 11] | 0.27 | {'A': 95, 'b': 5} |
| clean|copy|None|40|None|r|None | 100 | 6% [3, 12] | 0.29 | {'A': 94, 'b': 6} |
| clean|copy|None|44|None|r|None | 100 | 3% [1, 8] | 0.32 | {'A': 97, 'b': 3} |
| clean|copy|None|48|None|r|None | 100 | 17% [11, 26] | 0.41 | {'A': 83, 'b': 17} |
| clean|patch|None|16|None|a|None | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|patch|None|16|4.0|a|None | 100 | 6% [3, 12] | 0.05 | {'A': 94, 'b': 6} |
| clean|patch|None|16|8.0|a|None | 100 | 71% [61, 79] | 0.65 | {'A': 28, 'b': 71, 'oc': 1} |
| clean|patch|None|16|16.0|a|None | 100 | 99% [95, 100] | 0.95 | {'b': 99, 'other': 1} |
| clean|patch|None|20|None|a|None | 100 | 100% [96, 100] | 0.98 | {'b': 100} |
| clean|patch|None|20|4.0|a|None | 100 | 6% [3, 12] | 0.09 | {'A': 94, 'b': 6} |
| clean|patch|None|20|8.0|a|None | 100 | 89% [81, 94] | 0.79 | {'b': 89, 'A': 11} |
| clean|patch|None|20|16.0|a|None | 100 | 94% [88, 97] | 0.93 | {'b': 94, 'other': 6} |
| clean|patch|None|24|None|a|None | 100 | 100% [96, 100] | 0.98 | {'b': 100} |
| clean|patch|None|24|4.0|a|None | 100 | 7% [3, 14] | 0.12 | {'A': 93, 'b': 7} |
| clean|patch|None|24|8.0|a|None | 100 | 88% [80, 93] | 0.78 | {'b': 88, 'A': 12} |
| clean|patch|None|24|16.0|a|None | 100 | 86% [78, 91] | 0.90 | {'b': 86, 'other': 12, 'A': 2} |
| clean|patch|None|28|None|a|None | 100 | 100% [96, 100] | 0.98 | {'b': 100} |
| clean|patch|None|28|4.0|a|None | 100 | 26% [18, 35] | 0.35 | {'A': 74, 'b': 26} |
| clean|patch|None|28|8.0|a|None | 100 | 98% [93, 99] | 0.89 | {'b': 98, 'A': 2} |
| clean|patch|None|28|16.0|a|None | 100 | 77% [68, 84] | 0.85 | {'other': 21, 'b': 77, 'A': 2} |
| off|push|lens|16|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 69, 'bO': 29, 'other': 2} |
| off|push|lens|16|8.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 97, 'A': 3} |
| off|push|lens|16|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 72, 'bO': 28} |
| off|push|lens|20|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 82, 'bO': 14, 'other': 4} |
| off|push|lens|20|8.0|a|None | 100 | 0% [0, 4] | nan | {'A': 20, 'other': 8, 'bO': 72} |
| off|push|lens|20|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 44, 'bO': 51, 'A': 3, 'oc': 2} |
| off|push|lens|24|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 57, 'other': 4, 'bO': 38, 'oc': 1} |
| off|push|lens|24|8.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 87, 'A': 10, 'other': 2, 'oc': 1} |
| off|push|lens|24|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 51, 'bO': 45, 'oc': 2, 'A': 2} |
| off|push|lens|28|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 50, 'bO': 49, 'other': 1} |
| off|push|lens|28|8.0|a|None | 100 | 0% [0, 4] | nan | {'A': 6, 'bO': 80, 'other': 12, 'oc': 2} |
| off|push|lens|28|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 87, 'bO': 13} |
| off|push|lens|band|4.0|a|None | 100 | 0% [0, 4] | nan | {'other': 19, 'bO': 77, 'oc': 2, 'A': 2} |
| off|push|lens|band|8.0|a|None | 100 | 0% [0, 4] | nan | {'other': 97, 'bO': 3} |
| off|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 100} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.36 [+0.27, +0.46] (ref rate 1.00); E-insert: k +0.04 [-0.03, +0.10], J +0.37 [+0.28, +0.47] (ref rate 0.94); E-head: k +0.17 [-0.01, +0.35], J +0.37 [+0.26, +0.48] (ref rate 0.57); E-cue: k -, J +0.36 [+0.27, +0.46] (ref rate 1.00); E-unrelated: k -, J +0.00 [+0.00, +0.00] (ref rate 0.00); W-copy*: k +0.04 [-0.13, +0.23], J +0.15 [+0.06, +0.27] (ref rate 0.17); emb*: k +0.04 [-0.04, +0.12], J +0.37 [+0.27, +0.47] (ref rate 0.91); patch_matched: k +0.24 [+0.09, +0.40], J +0.19 [+0.07, +0.33] (ref rate 0.07); low_margin: k +0.30 [+0.12, +0.48]
K1 -0.01 [-0.20, +0.17] -> inconclusive; gate +0.05 [-0.12, +0.31]; K2 nb - a/2 -0.18 [-0.23, -0.14], b - nb +0.32 [+0.23, +0.42] -> write; K4 -0.22 [-0.24, -0.20]
JS(P*, .) {"clean": 0.228, "E-name": 0.383, "E-insert": 0.282, "E-head": 0.273, "E-cue": 0.376, "E-unrelated": 0.22}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [-0.0153, 0.0268, 0.0482, 0.1436], "E-insert": [0.1205, 0.2254, 0.2694, 0.3159], "E-head": [0.2794, 0.3282, 0.3642, 0.3463], "E-cue": [0.2111, 0.2345, 0.2268, 0.268], "E-unrelated": [0.1391, 0.1448, 0.1958, 0.246]}
transit proj on C's delta [44, 48, 52]: P*_b [0.2226, 0.2216, 0.236], P* [0.3336, 0.3257, 0.3065], edits {"E-name": [0.7328, 0.7094, 0.6886], "E-insert": [0.6668, 0.6482, 0.6279], "E-head": [0.5442, 0.5364, 0.5191], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.1378, 0.1617, 0.1704]}

## R (W-copy* = ('clean', 'copy', None, 36, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|edit|None|None|None|None|E-name | 100 | 100% [96, 100] | 1.13 | {'b': 100} |
| clean|edit|None|None|None|None|E-insert | 100 | 90% [83, 94] | 0.57 | {'b': 90, 'A': 4, 'other': 6} |
| clean|edit|None|None|None|None|E-cue | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|edit|None|None|None|None|E-unrelated | 100 | 0% [0, 4] | 0.07 | {'A': 94, 'other': 6} |
| clean|push|lens|16|4.0|r|None | 100 | 29% [21, 39] | 0.36 | {'A': 70, 'b': 29, 'other': 1} |
| clean|push|random|16|4.0|r|None | 100 | 1% [0, 5] | 0.01 | {'A': 99, 'b': 1} |
| clean|push|lens|16|4.0|a|None | 100 | 91% [84, 95] | 0.92 | {'b': 91, 'A': 5, 'other': 4} |
| clean|push|random|16|4.0|a|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|16|4.0|b|None | 100 | 93% [86, 97] | 0.88 | {'b': 93, 'A': 7} |
| clean|push|random|16|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|16|8.0|r|None | 100 | 74% [65, 82] | 0.66 | {'b': 74, 'A': 17, 'other': 8, 'oc': 1} |
| clean|push|random|16|8.0|r|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|16|8.0|a|None | 100 | 42% [33, 52] | 1.07 | {'b': 42, 'other': 58} |
| clean|push|random|16|8.0|a|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|16|8.0|b|None | 100 | 100% [96, 100] | 1.06 | {'b': 100} |
| clean|push|random|16|8.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|16|16.0|r|None | 100 | 85% [77, 91] | 0.80 | {'b': 85, 'A': 8, 'other': 7} |
| clean|push|random|16|16.0|r|None | 100 | 0% [0, 4] | 0.21 | {'A': 95, 'other': 4, 'oc': 1} |
| clean|push|lens|16|16.0|a|None | 100 | 0% [0, 4] | 0.84 | {'other': 100} |
| clean|push|random|16|16.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 68, 'other': 32} |
| clean|push|lens|16|16.0|b|None | 100 | 98% [93, 99] | 1.03 | {'b': 98, 'other': 2} |
| clean|push|random|16|16.0|b|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|lens|20|4.0|r|None | 100 | 17% [11, 26] | 0.35 | {'b': 17, 'A': 81, 'other': 2} |
| clean|push|random|20|4.0|r|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|20|4.0|a|None | 100 | 99% [95, 100] | 0.98 | {'b': 99, 'other': 1} |
| clean|push|random|20|4.0|a|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|20|4.0|b|None | 100 | 97% [92, 99] | 0.93 | {'b': 97, 'A': 2, 'other': 1} |
| clean|push|random|20|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|20|8.0|r|None | 100 | 42% [33, 52] | 0.44 | {'b': 42, 'A': 58} |
| clean|push|random|20|8.0|r|None | 100 | 0% [0, 4] | 0.04 | {'A': 95, 'other': 5} |
| clean|push|lens|20|8.0|a|None | 100 | 82% [73, 88] | 1.08 | {'b': 82, 'other': 18} |
| clean|push|random|20|8.0|a|None | 100 | 0% [0, 4] | 0.06 | {'A': 95, 'other': 5} |
| clean|push|lens|20|8.0|b|None | 100 | 100% [96, 100] | 1.05 | {'b': 100} |
| clean|push|random|20|8.0|b|None | 100 | 1% [0, 5] | 0.01 | {'A': 99, 'b': 1} |
| clean|push|lens|20|16.0|r|None | 100 | 76% [67, 83] | 0.73 | {'b': 76, 'other': 8, 'A': 16} |
| clean|push|random|20|16.0|r|None | 100 | 0% [0, 4] | 0.22 | {'A': 94, 'other': 6} |
| clean|push|lens|20|16.0|a|None | 100 | 8% [4, 15] | 1.03 | {'other': 92, 'b': 8} |
| clean|push|random|20|16.0|a|None | 100 | 0% [0, 4] | 0.20 | {'other': 68, 'A': 32} |
| clean|push|lens|20|16.0|b|None | 100 | 100% [96, 100] | 1.06 | {'b': 100} |
| clean|push|random|20|16.0|b|None | 100 | 0% [0, 4] | 0.12 | {'A': 95, 'other': 5} |
| clean|push|lens|24|4.0|r|None | 100 | 55% [45, 64] | 0.54 | {'b': 55, 'A': 37, 'other': 8} |
| clean|push|random|24|4.0|r|None | 100 | 0% [0, 4] | 0.04 | {'A': 99, 'other': 1} |
| clean|push|lens|24|4.0|a|None | 100 | 100% [96, 100] | 1.09 | {'b': 100} |
| clean|push|random|24|4.0|a|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|24|4.0|b|None | 100 | 100% [96, 100] | 1.01 | {'b': 100} |
| clean|push|random|24|4.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|24|8.0|r|None | 100 | 90% [83, 94] | 0.77 | {'b': 90, 'A': 7, 'other': 3} |
| clean|push|random|24|8.0|r|None | 100 | 0% [0, 4] | 0.13 | {'A': 95, 'other': 5} |
| clean|push|lens|24|8.0|a|None | 100 | 80% [71, 87] | 1.09 | {'b': 80, 'other': 20} |
| clean|push|random|24|8.0|a|None | 100 | 1% [0, 5] | 0.10 | {'A': 97, 'b': 1, 'other': 2} |
| clean|push|lens|24|8.0|b|None | 100 | 100% [96, 100] | 1.05 | {'b': 100} |
| clean|push|random|24|8.0|b|None | 100 | 1% [0, 5] | 0.04 | {'A': 99, 'b': 1} |
| clean|push|lens|24|16.0|r|None | 100 | 94% [88, 97] | 0.83 | {'b': 94, 'other': 4, 'A': 1, 'oc': 1} |
| clean|push|random|24|16.0|r|None | 100 | 0% [0, 4] | 0.28 | {'A': 94, 'other': 5, 'oc': 1} |
| clean|push|lens|24|16.0|a|None | 100 | 4% [2, 10] | 0.97 | {'other': 96, 'b': 4} |
| clean|push|random|24|16.0|a|None | 100 | 0% [0, 4] | 0.28 | {'other': 90, 'A': 10} |
| clean|push|lens|24|16.0|b|None | 100 | 96% [90, 98] | 1.01 | {'b': 96, 'other': 4} |
| clean|push|random|24|16.0|b|None | 100 | 0% [0, 4] | 0.19 | {'A': 89, 'other': 11} |
| clean|push|lens|28|4.0|r|None | 100 | 89% [81, 94] | 0.80 | {'b': 89, 'A': 3, 'other': 8} |
| clean|push|random|28|4.0|r|None | 100 | 0% [0, 4] | 0.09 | {'A': 99, 'other': 1} |
| clean|push|lens|28|4.0|a|None | 100 | 96% [90, 98] | 1.14 | {'b': 96, 'other': 4} |
| clean|push|random|28|4.0|a|None | 100 | 0% [0, 4] | 0.06 | {'A': 99, 'other': 1} |
| clean|push|lens|28|4.0|b|None | 100 | 97% [92, 99] | 0.87 | {'b': 97, 'A': 2, 'other': 1} |
| clean|push|random|28|4.0|b|None | 100 | 1% [0, 5] | 0.02 | {'A': 99, 'b': 1} |
| clean|push|lens|28|8.0|r|None | 100 | 84% [76, 90] | 0.91 | {'b': 84, 'other': 16} |
| clean|push|random|28|8.0|r|None | 100 | 0% [0, 4] | 0.22 | {'A': 97, 'other': 3} |
| clean|push|lens|28|8.0|a|None | 100 | 65% [55, 74] | 1.21 | {'b': 65, 'other': 35} |
| clean|push|random|28|8.0|a|None | 100 | 0% [0, 4] | 0.14 | {'A': 94, 'other': 6} |
| clean|push|lens|28|8.0|b|None | 100 | 100% [96, 100] | 1.03 | {'b': 100} |
| clean|push|random|28|8.0|b|None | 100 | 0% [0, 4] | 0.08 | {'A': 100} |
| clean|push|lens|28|16.0|r|None | 100 | 50% [40, 60] | 0.63 | {'other': 28, 'A': 18, 'oc': 4, 'b': 50} |
| clean|push|random|28|16.0|r|None | 100 | 2% [1, 7] | 0.34 | {'other': 10, 'A': 82, 'oc': 6, 'b': 2} |
| clean|push|lens|28|16.0|a|None | 100 | 0% [0, 4] | 1.07 | {'other': 100} |
| clean|push|random|28|16.0|a|None | 100 | 0% [0, 4] | 0.34 | {'other': 92, 'A': 8} |
| clean|push|lens|28|16.0|b|None | 100 | 97% [92, 99] | 0.99 | {'b': 97, 'other': 3} |
| clean|push|random|28|16.0|b|None | 100 | 0% [0, 4] | 0.23 | {'A': 93, 'other': 7} |
| clean|push|lens|band|4.0|r|None | 100 | 98% [93, 99] | 1.06 | {'b': 98, 'other': 2} |
| clean|push|random|band|4.0|r|None | 100 | 0% [0, 4] | 0.11 | {'A': 96, 'other': 4} |
| clean|push|lens|band|4.0|a|None | 100 | 35% [26, 45] | 1.16 | {'other': 65, 'b': 35} |
| clean|push|random|band|4.0|a|None | 100 | 0% [0, 4] | 0.08 | {'A': 95, 'other': 5} |
| clean|push|lens|band|4.0|b|None | 100 | 100% [96, 100] | 1.10 | {'b': 100} |
| clean|push|random|band|4.0|b|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|band|8.0|r|None | 100 | 84% [76, 90] | 0.92 | {'b': 84, 'A': 4, 'other': 12} |
| clean|push|random|band|8.0|r|None | 100 | 2% [1, 7] | 0.32 | {'A': 91, 'b': 2, 'other': 6, 'oc': 1} |
| clean|push|lens|band|8.0|a|None | 100 | 0% [0, 4] | 0.92 | {'other': 100} |
| clean|push|random|band|8.0|a|None | 100 | 0% [0, 4] | 0.30 | {'other': 83, 'A': 17} |
| clean|push|lens|band|8.0|b|None | 100 | 93% [86, 97] | 1.08 | {'b': 93, 'other': 7} |
| clean|push|random|band|8.0|b|None | 100 | 1% [0, 5] | 0.20 | {'A': 90, 'b': 1, 'other': 9} |
| clean|push|lens|band|16.0|r|None | 100 | 5% [2, 11] | 0.55 | {'other': 92, 'b': 5, 'oc': 1, 'A': 2} |
| clean|push|random|band|16.0|r|None | 100 | 7% [3, 14] | 0.39 | {'b': 7, 'A': 70, 'oc': 9, 'other': 14} |
| clean|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | 1.08 | {'other': 100} |
| clean|push|random|band|16.0|a|None | 100 | 0% [0, 4] | 0.45 | {'other': 100} |
| clean|push|lens|band|16.0|b|None | 100 | 95% [89, 98] | 1.05 | {'b': 95, 'other': 3, 'oc': 2} |
| clean|push|random|band|16.0|b|None | 100 | 1% [0, 5] | 0.39 | {'other': 44, 'A': 51, 'oc': 4, 'b': 1} |
| clean|emb_diff|lens|-1|1.0|b|None | 100 | 91% [84, 95] | 0.85 | {'b': 91, 'other': 9} |
| clean|emb_diff|random|-1|1.0|b|None | 100 | 0% [0, 4] | 0.12 | {'A': 90, 'oc': 6, 'other': 4} |
| clean|emb_add|lens|-1|1.0|b|None | 100 | 91% [84, 95] | 0.81 | {'b': 91, 'other': 9} |
| clean|emb_add|random|-1|1.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|emb_diff|lens|-1|4.0|b|None | 100 | 88% [80, 93] | 0.75 | {'b': 88, 'oc': 2, 'other': 10} |
| clean|emb_diff|random|-1|4.0|b|None | 100 | 21% [14, 30] | 0.50 | {'other': 31, 'oc': 33, 'b': 21, 'A': 15} |
| clean|emb_add|lens|-1|4.0|b|None | 100 | 100% [96, 100] | 1.09 | {'b': 100} |
| clean|emb_add|random|-1|4.0|b|None | 100 | 16% [10, 24] | 0.49 | {'other': 44, 'b': 16, 'A': 20, 'oc': 20} |
| clean|copy|None|16|None|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|copy|None|20|None|r|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|copy|None|24|None|r|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|copy|None|28|None|r|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|copy|None|32|None|r|None | 100 | 1% [0, 5] | 0.09 | {'A': 99, 'b': 1} |
| clean|copy|None|36|None|r|None | 100 | 63% [53, 72] | 0.54 | {'b': 63, 'A': 36, 'other': 1} |
| clean|copy|None|40|None|r|None | 100 | 93% [86, 97] | 0.67 | {'b': 93, 'A': 7} |
| clean|copy|None|44|None|r|None | 100 | 99% [95, 100] | 0.75 | {'b': 99, 'A': 1} |
| clean|copy|None|48|None|r|None | 100 | 100% [96, 100] | 0.81 | {'b': 100} |
| clean|patch|None|16|None|a|None | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|patch|None|16|4.0|a|None | 100 | 1% [0, 5] | 0.08 | {'A': 97, 'b': 1, 'other': 2} |
| clean|patch|None|16|8.0|a|None | 100 | 95% [89, 98] | 0.95 | {'b': 95, 'A': 1, 'other': 4} |
| clean|patch|None|16|16.0|a|None | 100 | 73% [64, 81] | 0.97 | {'b': 73, 'other': 27} |
| clean|patch|None|20|None|a|None | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|patch|None|20|4.0|a|None | 100 | 13% [8, 21] | 0.27 | {'b': 13, 'A': 87} |
| clean|patch|None|20|8.0|a|None | 100 | 97% [92, 99] | 0.93 | {'b': 97, 'other': 3} |
| clean|patch|None|20|16.0|a|None | 100 | 43% [34, 53] | 0.94 | {'other': 57, 'b': 43} |
| clean|patch|None|24|None|a|None | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|patch|None|24|4.0|a|None | 100 | 32% [24, 42] | 0.44 | {'b': 32, 'A': 61, 'other': 7} |
| clean|patch|None|24|8.0|a|None | 100 | 94% [88, 97] | 0.94 | {'b': 94, 'other': 6} |
| clean|patch|None|24|16.0|a|None | 100 | 15% [9, 23] | 0.92 | {'other': 85, 'b': 15} |
| clean|patch|None|28|None|a|None | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|patch|None|28|4.0|a|None | 100 | 66% [56, 75] | 0.63 | {'b': 66, 'A': 31, 'other': 3} |
| clean|patch|None|28|8.0|a|None | 100 | 91% [84, 95] | 0.93 | {'b': 91, 'other': 9} |
| clean|patch|None|28|16.0|a|None | 100 | 18% [12, 27] | 0.89 | {'other': 81, 'b': 18, 'A': 1} |
| off|push|lens|16|4.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 89, 'A': 5, 'oc': 1, 'other': 5} |
| off|push|lens|16|8.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 42, 'other': 58} |
| off|push|lens|16|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 100} |
| off|push|lens|20|4.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 98, 'other': 1, 'A': 1} |
| off|push|lens|20|8.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 81, 'other': 19} |
| off|push|lens|20|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 93, 'bO': 7} |
| off|push|lens|24|4.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 100} |
| off|push|lens|24|8.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 82, 'other': 18} |
| off|push|lens|24|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 95, 'bO': 5} |
| off|push|lens|28|4.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 98, 'other': 2} |
| off|push|lens|28|8.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 67, 'other': 33} |
| off|push|lens|28|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 100} |
| off|push|lens|band|4.0|a|None | 100 | 0% [0, 4] | nan | {'other': 65, 'bO': 35} |
| off|push|lens|band|8.0|a|None | 100 | 0% [0, 4] | nan | {'other': 100} |
| off|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 100} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +1.00 [+1.00, +1.00] (ref rate 1.00); E-insert: k -, J +0.90 [+0.84, +0.96] (ref rate 0.90); E-cue: k -, J +1.00 [+1.00, +1.00] (ref rate 1.00); E-unrelated: k -, J +0.00 [+0.00, +0.00] (ref rate 0.00); W-copy*: k -, J +0.63 [+0.54, +0.72] (ref rate 0.63); emb*: k -, J +0.91 [+0.85, +0.96] (ref rate 0.91); patch_matched: k -, J +0.32 [+0.23, +0.41] (ref rate 0.32); low_margin: k -
K1 - -> untestable; gate +0.78 [+0.45, +1.00]; K2 nb - a/2 -0.38 [-0.44, -0.31], b - nb +0.88 [+0.81, +0.94] -> write; K4 -0.26 [-0.28, -0.24]
JS(P*, .) {"clean": 0.607, "E-name": 0.015, "E-insert": 0.16, "E-cue": 0.019, "E-unrelated": 0.6}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [0.1077, 0.1922, 0.2371, 0.3711], "E-insert": [0.106, 0.1902, 0.1883, 0.2764], "E-cue": [0.3413, 0.4741, 0.5723, 0.6621], "E-unrelated": [0.1368, 0.0466, 0.0657, 0.1186]}
transit proj on C's delta [44, 48, 52]: P*_b [0.6276, 0.6373, 0.6899], P* [0.5962, 0.6011, 0.6572], edits {"E-name": [0.6364, 0.6265, 0.6732], "E-insert": [0.5661, 0.5435, 0.5516], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.2838, 0.3018, 0.2822]}

## B (W-copy* = ('clean', 'copy', None, 40, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|edit|None|None|None|None|E-name | 100 | 100% [96, 100] | 1.01 | {'b': 100} |
| clean|edit|None|None|None|None|E-insert | 100 | 89% [81, 94] | 0.55 | {'b': 89, 'A': 9, 'other': 2} |
| clean|edit|None|None|None|None|E-cue | 100 | 100% [96, 100] | 1.00 | {'b': 100} |
| clean|edit|None|None|None|None|E-unrelated | 100 | 0% [0, 4] | 0.08 | {'A': 100} |
| clean|push|lens|16|4.0|r|None | 100 | 13% [8, 21] | 0.23 | {'other': 16, 'b': 13, 'A': 71} |
| clean|push|random|16|4.0|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|16|4.0|a|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|random|16|4.0|a|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|16|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|random|16|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|16|8.0|r|None | 100 | 35% [26, 45] | 0.54 | {'b': 35, 'A': 34, 'other': 31} |
| clean|push|random|16|8.0|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|16|8.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 98, 'other': 2} |
| clean|push|random|16|8.0|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 99, 'other': 1} |
| clean|push|lens|16|8.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|random|16|8.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|16|16.0|r|None | 100 | 74% [65, 82] | 0.76 | {'b': 74, 'other': 16, 'A': 10} |
| clean|push|random|16|16.0|r|None | 100 | 0% [0, 4] | 0.13 | {'other': 4, 'A': 96} |
| clean|push|lens|16|16.0|a|None | 100 | 2% [1, 7] | 0.40 | {'b': 2, 'other': 61, 'A': 37} |
| clean|push|random|16|16.0|a|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|16|16.0|b|None | 100 | 10% [6, 17] | 0.24 | {'other': 19, 'b': 10, 'A': 71} |
| clean|push|random|16|16.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|20|4.0|r|None | 100 | 0% [0, 4] | 0.08 | {'A': 100} |
| clean|push|random|20|4.0|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|20|4.0|a|None | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|push|random|20|4.0|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|20|4.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|random|20|4.0|b|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|20|8.0|r|None | 100 | 3% [1, 8] | 0.19 | {'A': 96, 'b': 3, 'other': 1} |
| clean|push|random|20|8.0|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|20|8.0|a|None | 100 | 0% [0, 4] | 0.14 | {'A': 100} |
| clean|push|random|20|8.0|a|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|20|8.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|random|20|8.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|20|16.0|r|None | 100 | 33% [25, 43] | 0.49 | {'other': 5, 'b': 33, 'A': 61, 'oc': 1} |
| clean|push|random|20|16.0|r|None | 100 | 0% [0, 4] | 0.09 | {'A': 98, 'oc': 1, 'other': 1} |
| clean|push|lens|20|16.0|a|None | 100 | 0% [0, 4] | 0.22 | {'A': 95, 'other': 5} |
| clean|push|random|20|16.0|a|None | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|push|lens|20|16.0|b|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|random|20|16.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|24|4.0|r|None | 100 | 0% [0, 4] | 0.20 | {'A': 100} |
| clean|push|random|24|4.0|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|24|4.0|a|None | 100 | 0% [0, 4] | 0.10 | {'A': 100} |
| clean|push|random|24|4.0|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|24|4.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|random|24|4.0|b|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|24|8.0|r|None | 100 | 14% [9, 22] | 0.38 | {'A': 81, 'other': 5, 'b': 14} |
| clean|push|random|24|8.0|r|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|24|8.0|a|None | 100 | 0% [0, 4] | 0.24 | {'A': 100} |
| clean|push|random|24|8.0|a|None | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|push|lens|24|8.0|b|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|random|24|8.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|24|16.0|r|None | 100 | 71% [61, 79] | 0.66 | {'b': 71, 'other': 4, 'A': 25} |
| clean|push|random|24|16.0|r|None | 100 | 0% [0, 4] | 0.15 | {'A': 98, 'other': 2} |
| clean|push|lens|24|16.0|a|None | 100 | 7% [3, 14] | 0.36 | {'A': 79, 'other': 14, 'b': 7} |
| clean|push|random|24|16.0|a|None | 100 | 0% [0, 4] | 0.08 | {'A': 100} |
| clean|push|lens|24|16.0|b|None | 100 | 0% [0, 4] | 0.18 | {'A': 100} |
| clean|push|random|24|16.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|28|4.0|r|None | 100 | 20% [13, 29] | 0.39 | {'A': 80, 'b': 20} |
| clean|push|random|28|4.0|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|28|4.0|a|None | 100 | 0% [0, 4] | 0.19 | {'A': 100} |
| clean|push|random|28|4.0|a|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|28|4.0|b|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|random|28|4.0|b|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|push|lens|28|8.0|r|None | 100 | 70% [60, 78] | 0.65 | {'b': 70, 'A': 27, 'other': 3} |
| clean|push|random|28|8.0|r|None | 100 | 0% [0, 4] | 0.05 | {'A': 100} |
| clean|push|lens|28|8.0|a|None | 100 | 20% [13, 29] | 0.40 | {'b': 20, 'A': 73, 'other': 7} |
| clean|push|random|28|8.0|a|None | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|push|lens|28|8.0|b|None | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|push|random|28|8.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|28|16.0|r|None | 100 | 83% [74, 89] | 0.90 | {'b': 83, 'other': 13, 'oc': 1, 'A': 3} |
| clean|push|random|28|16.0|r|None | 100 | 1% [0, 5] | 0.23 | {'A': 97, 'oc': 1, 'b': 1, 'other': 1} |
| clean|push|lens|28|16.0|a|None | 100 | 61% [51, 70] | 0.73 | {'b': 61, 'other': 30, 'A': 9} |
| clean|push|random|28|16.0|a|None | 100 | 0% [0, 4] | 0.11 | {'A': 99, 'other': 1} |
| clean|push|lens|28|16.0|b|None | 100 | 3% [1, 8] | 0.20 | {'A': 96, 'other': 1, 'b': 3} |
| clean|push|random|28|16.0|b|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|band|4.0|r|None | 100 | 74% [65, 82] | 0.84 | {'b': 74, 'other': 11, 'A': 15} |
| clean|push|random|band|4.0|r|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|push|lens|band|4.0|a|None | 100 | 19% [13, 28] | 0.43 | {'b': 19, 'A': 80, 'other': 1} |
| clean|push|random|band|4.0|a|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|push|lens|band|4.0|b|None | 100 | 0% [0, 4] | 0.14 | {'A': 100} |
| clean|push|random|band|4.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|push|lens|band|8.0|r|None | 100 | 90% [83, 94] | 1.03 | {'b': 90, 'other': 10} |
| clean|push|random|band|8.0|r|None | 100 | 0% [0, 4] | 0.14 | {'A': 96, 'oc': 2, 'other': 2} |
| clean|push|lens|band|8.0|a|None | 100 | 35% [26, 45] | 0.78 | {'other': 57, 'b': 35, 'A': 8} |
| clean|push|random|band|8.0|a|None | 100 | 0% [0, 4] | 0.07 | {'A': 99, 'other': 1} |
| clean|push|lens|band|8.0|b|None | 100 | 49% [39, 59] | 0.54 | {'b': 49, 'other': 7, 'A': 44} |
| clean|push|random|band|8.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|push|lens|band|16.0|r|None | 100 | 35% [26, 45] | 0.96 | {'other': 65, 'b': 35} |
| clean|push|random|band|16.0|r|None | 100 | 13% [8, 21] | 0.38 | {'A': 69, 'b': 13, 'oc': 9, 'other': 9} |
| clean|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | 0.89 | {'other': 100} |
| clean|push|random|band|16.0|a|None | 100 | 0% [0, 4] | 0.21 | {'A': 41, 'other': 59} |
| clean|push|lens|band|16.0|b|None | 100 | 90% [83, 94] | 0.91 | {'b': 90, 'other': 8, 'A': 2} |
| clean|push|random|band|16.0|b|None | 100 | 0% [0, 4] | 0.08 | {'A': 99, 'other': 1} |
| clean|emb_diff|lens|-1|1.0|b|None | 100 | 22% [15, 31] | 0.24 | {'A': 75, 'b': 22, 'other': 3} |
| clean|emb_diff|random|-1|1.0|b|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|emb_add|lens|-1|1.0|b|None | 100 | 49% [39, 59] | 0.41 | {'A': 47, 'b': 49, 'other': 4} |
| clean|emb_add|random|-1|1.0|b|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|emb_diff|lens|-1|4.0|b|None | 100 | 92% [85, 96] | 0.77 | {'b': 92, 'other': 5, 'oc': 2, 'A': 1} |
| clean|emb_diff|random|-1|4.0|b|None | 100 | 29% [21, 39] | 0.51 | {'A': 24, 'other': 27, 'b': 29, 'oc': 20} |
| clean|emb_add|lens|-1|4.0|b|None | 100 | 100% [96, 100] | 0.98 | {'b': 100} |
| clean|emb_add|random|-1|4.0|b|None | 100 | 26% [18, 35] | 0.50 | {'A': 22, 'other': 31, 'b': 26, 'oc': 21} |
| clean|copy|None|16|None|r|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|copy|None|20|None|r|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|copy|None|24|None|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|copy|None|28|None|r|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|copy|None|32|None|r|None | 100 | 0% [0, 4] | 0.03 | {'A': 100} |
| clean|copy|None|36|None|r|None | 100 | 11% [6, 19] | 0.24 | {'A': 89, 'b': 11} |
| clean|copy|None|40|None|r|None | 100 | 79% [70, 86] | 0.65 | {'b': 79, 'A': 21} |
| clean|copy|None|44|None|r|None | 100 | 88% [80, 93] | 0.67 | {'b': 88, 'A': 12} |
| clean|copy|None|48|None|r|None | 100 | 93% [86, 97] | 0.70 | {'b': 93, 'A': 7} |
| clean|patch|None|16|None|a|None | 100 | 0% [0, 4] | -0.00 | {'A': 100} |
| clean|patch|None|16|4.0|a|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|patch|None|16|8.0|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|patch|None|16|16.0|a|None | 100 | 0% [0, 4] | 0.04 | {'A': 99, 'other': 1} |
| clean|patch|None|20|None|a|None | 100 | 0% [0, 4] | 0.00 | {'A': 100} |
| clean|patch|None|20|4.0|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|patch|None|20|8.0|a|None | 100 | 0% [0, 4] | 0.04 | {'A': 99, 'other': 1} |
| clean|patch|None|20|16.0|a|None | 100 | 0% [0, 4] | 0.09 | {'A': 98, 'other': 2} |
| clean|patch|None|24|None|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|patch|None|24|4.0|a|None | 100 | 0% [0, 4] | 0.02 | {'A': 100} |
| clean|patch|None|24|8.0|a|None | 100 | 0% [0, 4] | 0.07 | {'A': 100} |
| clean|patch|None|24|16.0|a|None | 100 | 6% [3, 12] | 0.23 | {'A': 87, 'b': 6, 'other': 7} |
| clean|patch|None|28|None|a|None | 100 | 0% [0, 4] | 0.01 | {'A': 100} |
| clean|patch|None|28|4.0|a|None | 100 | 0% [0, 4] | 0.04 | {'A': 100} |
| clean|patch|None|28|8.0|a|None | 100 | 5% [2, 11] | 0.19 | {'A': 95, 'b': 5} |
| clean|patch|None|28|16.0|a|None | 100 | 33% [25, 43] | 0.48 | {'A': 52, 'other': 14, 'b': 33, 'oc': 1} |
| off|push|lens|16|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 100} |
| off|push|lens|16|8.0|a|None | 100 | 0% [0, 4] | nan | {'A': 98, 'other': 2} |
| off|push|lens|16|16.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 2, 'other': 61, 'A': 37} |
| off|push|lens|20|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 100} |
| off|push|lens|20|8.0|a|None | 100 | 0% [0, 4] | nan | {'A': 100} |
| off|push|lens|20|16.0|a|None | 100 | 0% [0, 4] | nan | {'A': 95, 'other': 5} |
| off|push|lens|24|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 100} |
| off|push|lens|24|8.0|a|None | 100 | 0% [0, 4] | nan | {'A': 100} |
| off|push|lens|24|16.0|a|None | 100 | 0% [0, 4] | nan | {'A': 80, 'other': 15, 'bO': 5} |
| off|push|lens|28|4.0|a|None | 100 | 0% [0, 4] | nan | {'A': 100} |
| off|push|lens|28|8.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 24, 'A': 70, 'other': 6} |
| off|push|lens|28|16.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 57, 'other': 32, 'A': 11} |
| off|push|lens|band|4.0|a|None | 100 | 0% [0, 4] | nan | {'bO': 20, 'A': 77, 'other': 3} |
| off|push|lens|band|8.0|a|None | 100 | 0% [0, 4] | nan | {'other': 55, 'bO': 30, 'A': 15} |
| off|push|lens|band|16.0|a|None | 100 | 0% [0, 4] | nan | {'other': 100} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-insert: k -, J +0.00 [+0.00, +0.00] (ref rate 0.89); E-cue: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-unrelated: k -, J - (ref rate 0.00); W-copy*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.79); emb*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.49); patch_matched: k -, J - (ref rate 0.00); low_margin: k -
K1 - -> untestable; gate +0.08 [-0.07, +0.23]; K2 nb - a/2 +0.00 [+0.00, +0.00], b - nb +0.00 [+0.00, +0.00] -> inconclusive; K4 -0.24 [-0.26, -0.23]
JS(P*, .) {"clean": 0.01, "E-name": 0.638, "E-insert": 0.37, "E-cue": 0.637, "E-unrelated": 0.018}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [-0.0079, -0.0622, -0.0543, 0.0086], "E-insert": [0.121, 0.1626, 0.156, 0.1538], "E-cue": [0.238, 0.1788, 0.1431, 0.1615], "E-unrelated": [0.1448, 0.1582, 0.1551, 0.1659]}
transit proj on C's delta [44, 48, 52]: P*_b [0.0362, 0.0582, 0.0647], P* [0.1013, 0.1215, 0.1419], edits {"E-name": [0.6685, 0.6562, 0.7538], "E-insert": [0.6381, 0.6241, 0.6374], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.2526, 0.2577, 0.2181]}

## Plain-text loss under the push (nats)

{"none": 2.3307, "lens/16/x4": 2.3548, "random/16/x4": 2.3346, "lens/16/x8": 2.6263, "random/16/x8": 2.3552, "lens/16/x16": 5.4481, "random/16/x16": 2.4761, "lens/20/x4": 2.3593, "random/20/x4": 2.3351, "lens/20/x8": 2.4969, "random/20/x8": 2.364, "lens/20/x16": 3.6119, "random/20/x16": 2.5175, "lens/24/x4": 2.3941, "random/24/x4": 2.3368, "lens/24/x8": 2.6483, "random/24/x8": 2.3685, "lens/24/x16": 3.3078, "random/24/x16": 2.6334, "lens/28/x4": 2.4466, "random/28/x4": 2.3466, "lens/28/x8": 2.8667, "random/28/x8": 2.4193, "lens/28/x16": 4.4636, "random/28/x16": 2.8101, "lens/band/x4": 3.5355, "random/band/x4": 2.3807, "lens/band/x8": 7.2785, "random/band/x8": 2.6209, "lens/band/x16": 9.7923, "random/band/x16": 5.0473}

## Diagnostics

{"max_none_vs_clean_logit": 0.9375, "max_zero_scale_vs_none_logit": null, "n_zero_scale": 0}
