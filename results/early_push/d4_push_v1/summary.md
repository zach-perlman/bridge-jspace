# early_push

P* = ('clean', 'push', 'lens', 24, 4.0, 'a', None); emb* = ('clean', 'emb_add', 'lens', -1, 1.0, 'b', None)

Verdict (manifest rule): **push writes the intermediate**; calls (K1 RL, K2 RL, K3) ['gate failed', 'write', 'write']; K3 BL - RL flips -0.37 [-0.48, -0.25]

## BL (W-copy* = ('clean', 'copy', None, 48, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|edit|None|None|None|None|E-name | 60 | 100% [94, 100] | 0.97 | {'b': 60} |
| clean|edit|None|None|None|None|E-insert | 60 | 0% [-0, 6] | 0.41 | {'A': 60} |
| clean|edit|None|None|None|None|E-head | 60 | 78% [66, 87] | 0.53 | {'A': 13, 'b': 47} |
| clean|edit|None|None|None|None|E-cue | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|edit|None|None|None|None|E-unrelated | 60 | 0% [-0, 6] | 0.09 | {'A': 60} |
| clean|push|lens|16|4.0|r|None | 60 | 8% [4, 18] | 0.16 | {'A': 54, 'b': 5, 'oc': 1} |
| clean|push|random|16|4.0|r|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|16|4.0|a|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|random|16|4.0|a|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|push|lens|16|4.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|random|16|4.0|b|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|16|8.0|r|None | 60 | 27% [17, 39] | 0.32 | {'b': 16, 'A': 39, 'oc': 5} |
| clean|push|random|16|8.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|16|8.0|a|None | 60 | 5% [2, 14] | 0.25 | {'A': 55, 'b': 3, 'oc': 1, 'other': 1} |
| clean|push|random|16|8.0|a|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|lens|16|8.0|b|None | 60 | 8% [4, 18] | 0.20 | {'A': 53, 'b': 5, 'oc': 2} |
| clean|push|random|16|8.0|b|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|16|16.0|r|None | 60 | 48% [36, 61] | 0.50 | {'b': 29, 'A': 25, 'oc': 6} |
| clean|push|random|16|16.0|r|None | 60 | 2% [0, 9] | 0.11 | {'A': 58, 'oc': 1, 'b': 1} |
| clean|push|lens|16|16.0|a|None | 60 | 8% [4, 18] | 0.47 | {'other': 47, 'b': 5, 'A': 6, 'oc': 2} |
| clean|push|random|16|16.0|a|None | 60 | 0% [-0, 6] | 0.12 | {'A': 60} |
| clean|push|lens|16|16.0|b|None | 60 | 47% [35, 59] | 0.46 | {'b': 28, 'A': 24, 'oc': 8} |
| clean|push|random|16|16.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|20|4.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|random|20|4.0|r|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|4.0|a|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|random|20|4.0|a|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|20|4.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|random|20|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|8.0|r|None | 60 | 0% [-0, 6] | 0.08 | {'A': 59, 'oc': 1} |
| clean|push|random|20|8.0|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|20|8.0|a|None | 60 | 0% [-0, 6] | 0.15 | {'A': 60} |
| clean|push|random|20|8.0|a|None | 60 | 0% [-0, 6] | 0.11 | {'A': 60} |
| clean|push|lens|20|8.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|random|20|8.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|16.0|r|None | 60 | 28% [19, 41] | 0.32 | {'A': 39, 'b': 17, 'oc': 4} |
| clean|push|random|20|16.0|r|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|lens|20|16.0|a|None | 60 | 2% [0, 9] | 0.27 | {'A': 49, 'other': 9, 'b': 1, 'oc': 1} |
| clean|push|random|20|16.0|a|None | 60 | 0% [-0, 6] | 0.19 | {'A': 60} |
| clean|push|lens|20|16.0|b|None | 60 | 8% [4, 18] | 0.20 | {'A': 55, 'b': 5} |
| clean|push|random|20|16.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|24|4.0|r|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|random|24|4.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|24|4.0|a|None | 60 | 0% [-0, 6] | 0.08 | {'A': 60} |
| clean|push|random|24|4.0|a|None | 60 | 0% [-0, 6] | 0.06 | {'A': 60} |
| clean|push|lens|24|4.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|random|24|4.0|b|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|24|8.0|r|None | 60 | 5% [2, 14] | 0.13 | {'A': 57, 'b': 3} |
| clean|push|random|24|8.0|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|24|8.0|a|None | 60 | 0% [-0, 6] | 0.19 | {'A': 60} |
| clean|push|random|24|8.0|a|None | 60 | 0% [-0, 6] | 0.13 | {'A': 60} |
| clean|push|lens|24|8.0|b|None | 60 | 0% [-0, 6] | 0.08 | {'A': 60} |
| clean|push|random|24|8.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|24|16.0|r|None | 60 | 25% [16, 37] | 0.32 | {'b': 15, 'A': 44, 'oc': 1} |
| clean|push|random|24|16.0|r|None | 60 | 0% [-0, 6] | 0.12 | {'A': 60} |
| clean|push|lens|24|16.0|a|None | 60 | 5% [2, 14] | 0.30 | {'A': 45, 'other': 12, 'b': 3} |
| clean|push|random|24|16.0|a|None | 60 | 0% [-0, 6] | 0.23 | {'A': 59, 'other': 1} |
| clean|push|lens|24|16.0|b|None | 60 | 28% [19, 41] | 0.34 | {'b': 17, 'A': 43} |
| clean|push|random|24|16.0|b|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|28|4.0|r|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|push|random|28|4.0|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|28|4.0|a|None | 60 | 0% [-0, 6] | 0.10 | {'A': 60} |
| clean|push|random|28|4.0|a|None | 60 | 0% [-0, 6] | 0.09 | {'A': 60} |
| clean|push|lens|28|4.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|random|28|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|28|8.0|r|None | 60 | 7% [3, 16] | 0.15 | {'A': 55, 'oc': 1, 'b': 4} |
| clean|push|random|28|8.0|r|None | 60 | 0% [-0, 6] | 0.06 | {'A': 60} |
| clean|push|lens|28|8.0|a|None | 60 | 2% [0, 9] | 0.24 | {'A': 59, 'b': 1} |
| clean|push|random|28|8.0|a|None | 60 | 0% [-0, 6] | 0.14 | {'A': 60} |
| clean|push|lens|28|8.0|b|None | 60 | 0% [-0, 6] | 0.09 | {'A': 60} |
| clean|push|random|28|8.0|b|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|push|lens|28|16.0|r|None | 60 | 30% [20, 43] | 0.42 | {'b': 18, 'A': 34, 'oc': 8} |
| clean|push|random|28|16.0|r|None | 60 | 3% [1, 11] | 0.25 | {'A': 58, 'b': 2} |
| clean|push|lens|28|16.0|a|None | 60 | 8% [4, 18] | 0.44 | {'A': 18, 'other': 35, 'b': 5, 'oc': 2} |
| clean|push|random|28|16.0|a|None | 60 | 0% [-0, 6] | 0.33 | {'A': 49, 'other': 9, 'oc': 2} |
| clean|push|lens|28|16.0|b|None | 60 | 22% [13, 34] | 0.38 | {'A': 43, 'b': 13, 'oc': 4} |
| clean|push|random|28|16.0|b|None | 60 | 0% [-0, 6] | 0.20 | {'A': 60} |
| clean|push|lens|band|4.0|r|None | 60 | 35% [24, 48] | 0.40 | {'b': 21, 'A': 31, 'oc': 8} |
| clean|push|random|band|4.0|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|band|4.0|a|None | 60 | 13% [7, 24] | 0.37 | {'A': 47, 'other': 4, 'b': 8, 'oc': 1} |
| clean|push|random|band|4.0|a|None | 60 | 0% [-0, 6] | 0.12 | {'A': 60} |
| clean|push|lens|band|4.0|b|None | 60 | 23% [14, 35] | 0.34 | {'A': 44, 'b': 14, 'oc': 2} |
| clean|push|random|band|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|band|8.0|r|None | 60 | 58% [46, 70] | 0.56 | {'b': 35, 'A': 18, 'oc': 7} |
| clean|push|random|band|8.0|r|None | 60 | 0% [-0, 6] | 0.11 | {'A': 60} |
| clean|push|lens|band|8.0|a|None | 60 | 0% [-0, 6] | 0.53 | {'other': 60} |
| clean|push|random|band|8.0|a|None | 60 | 0% [-0, 6] | 0.21 | {'A': 55, 'other': 5} |
| clean|push|lens|band|8.0|b|None | 60 | 72% [59, 81] | 0.60 | {'b': 43, 'oc': 8, 'A': 9} |
| clean|push|random|band|8.0|b|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|lens|band|16.0|r|None | 60 | 60% [47, 71] | 0.57 | {'b': 36, 'A': 11, 'oc': 13} |
| clean|push|random|band|16.0|r|None | 60 | 7% [3, 16] | 0.36 | {'A': 52, 'b': 4, 'oc': 4} |
| clean|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | 0.53 | {'other': 60} |
| clean|push|random|band|16.0|a|None | 60 | 0% [-0, 6] | 0.46 | {'other': 59, 'A': 1} |
| clean|push|lens|band|16.0|b|None | 60 | 83% [72, 91] | 0.63 | {'b': 50, 'oc': 9, 'A': 1} |
| clean|push|random|band|16.0|b|None | 60 | 0% [-0, 6] | 0.34 | {'A': 56, 'oc': 4} |
| clean|emb_diff|lens|-1|1.0|b|None | 60 | 37% [26, 49] | 0.39 | {'A': 38, 'b': 22} |
| clean|emb_diff|random|-1|1.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|emb_add|lens|-1|1.0|b|None | 60 | 37% [26, 49] | 0.31 | {'A': 37, 'b': 22, 'oc': 1} |
| clean|emb_add|random|-1|1.0|b|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|emb_diff|lens|-1|4.0|b|None | 60 | 93% [84, 97] | 0.66 | {'b': 56, 'oc': 3, 'A': 1} |
| clean|emb_diff|random|-1|4.0|b|None | 60 | 30% [20, 43] | 0.49 | {'A': 25, 'b': 18, 'oc': 17} |
| clean|emb_add|lens|-1|4.0|b|None | 60 | 100% [94, 100] | 0.89 | {'b': 60} |
| clean|emb_add|random|-1|4.0|b|None | 60 | 20% [12, 32] | 0.46 | {'b': 12, 'A': 33, 'oc': 15} |
| clean|copy|None|16|None|r|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|copy|None|20|None|r|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|copy|None|24|None|r|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|copy|None|28|None|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|copy|None|32|None|r|None | 60 | 15% [8, 26] | 0.20 | {'A': 51, 'b': 9} |
| clean|copy|None|36|None|r|None | 60 | 5% [2, 14] | 0.17 | {'A': 57, 'b': 3} |
| clean|copy|None|40|None|r|None | 60 | 10% [5, 20] | 0.19 | {'A': 54, 'b': 6} |
| clean|copy|None|44|None|r|None | 60 | 17% [9, 28] | 0.26 | {'A': 50, 'b': 10} |
| clean|copy|None|48|None|r|None | 60 | 40% [29, 53] | 0.42 | {'A': 36, 'b': 24} |
| clean|patch|None|16|None|a|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|patch|None|16|4.0|a|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|patch|None|16|8.0|a|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|patch|None|16|16.0|a|None | 60 | 0% [-0, 6] | 0.13 | {'A': 60} |
| clean|patch|None|20|None|a|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|patch|None|20|4.0|a|None | 60 | 0% [-0, 6] | 0.06 | {'A': 60} |
| clean|patch|None|20|8.0|a|None | 60 | 0% [-0, 6] | 0.13 | {'A': 60} |
| clean|patch|None|20|16.0|a|None | 60 | 3% [1, 11] | 0.23 | {'A': 58, 'b': 2} |
| clean|patch|None|24|None|a|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|patch|None|24|4.0|a|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|patch|None|24|8.0|a|None | 60 | 0% [-0, 6] | 0.17 | {'A': 60} |
| clean|patch|None|24|16.0|a|None | 60 | 15% [8, 26] | 0.37 | {'A': 40, 'other': 7, 'oc': 4, 'b': 9} |
| clean|patch|None|28|None|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|patch|None|28|4.0|a|None | 60 | 2% [0, 9] | 0.14 | {'A': 59, 'b': 1} |
| clean|patch|None|28|8.0|a|None | 60 | 18% [11, 30] | 0.34 | {'A': 46, 'b': 11, 'oc': 3} |
| clean|patch|None|28|16.0|a|None | 60 | 30% [20, 43] | 0.50 | {'b': 18, 'other': 15, 'A': 22, 'oc': 5} |
| off|push|lens|16|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|16|8.0|a|None | 60 | 5% [2, 14] | nan | {'A': 55, 'b': 3, 'bO': 2} |
| off|push|lens|16|16.0|a|None | 60 | 3% [1, 11] | nan | {'other': 48, 'bO': 4, 'A': 6, 'b': 2} |
| off|push|lens|20|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|20|8.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|20|16.0|a|None | 60 | 2% [0, 9] | nan | {'A': 50, 'other': 9, 'b': 1} |
| off|push|lens|24|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|24|8.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|24|16.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 45, 'other': 12, 'bO': 3} |
| off|push|lens|28|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|28|8.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|28|16.0|a|None | 60 | 2% [0, 9] | nan | {'A': 18, 'other': 36, 'bO': 5, 'b': 1} |
| off|push|lens|band|4.0|a|None | 60 | 2% [0, 9] | nan | {'A': 47, 'other': 4, 'bO': 8, 'b': 1} |
| off|push|lens|band|8.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |
| off|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-insert: k -, J - (ref rate 0.00); E-head: k -, J +0.00 [+0.00, +0.00] (ref rate 0.78); E-cue: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-unrelated: k -, J - (ref rate 0.00); W-copy*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.40); emb*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.37); patch_matched: k -, J - (ref rate 0.00); low_margin: k -
K1 - -> untestable; gate -; K2 nb - a/2 +0.00 [+0.00, +0.00], b - nb +0.00 [+0.00, +0.00] -> inconclusive; K4 -0.19 [-0.22, -0.16]
JS(P*, .) {"clean": 0.001, "E-name": 0.687, "E-insert": 0.068, "E-head": 0.318, "E-cue": 0.687, "E-unrelated": 0.001}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [0.0332, -0.0732, -0.0817, -0.0557], "E-insert": [0.104, 0.1531, 0.1531, 0.1311], "E-head": [0.177, 0.1942, 0.1599, 0.1341], "E-cue": [0.1878, 0.1557, 0.1257, 0.1233], "E-unrelated": [0.1034, 0.2249, 0.2162, 0.208]}
transit proj on C's delta [44, 48, 52]: P*_b [0.0284, 0.0198, 0.0175], P* [0.1548, 0.1432, 0.131], edits {"E-name": [0.6508, 0.6661, 0.7253], "E-insert": [0.474, 0.4625, 0.4687], "E-head": [0.5311, 0.5258, 0.5739], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.2421, 0.2116, 0.1796]}

## BR (W-copy* = ('clean', 'copy', None, 40, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|edit|None|None|None|None|E-name | 60 | 100% [94, 100] | 1.01 | {'b': 60} |
| clean|edit|None|None|None|None|E-insert | 60 | 97% [89, 99] | 0.74 | {'b': 58, 'A': 2} |
| clean|edit|None|None|None|None|E-head | 60 | 47% [35, 59] | 0.81 | {'other': 32, 'b': 28} |
| clean|edit|None|None|None|None|E-cue | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|edit|None|None|None|None|E-unrelated | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|16|4.0|r|None | 60 | 18% [11, 30] | 0.20 | {'other': 5, 'A': 44, 'b': 11} |
| clean|push|random|16|4.0|r|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|16|4.0|a|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|random|16|4.0|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|16|4.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|random|16|4.0|b|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|16|8.0|r|None | 60 | 45% [33, 58] | 0.51 | {'b': 27, 'A': 24, 'other': 8, 'oc': 1} |
| clean|push|random|16|8.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|16|8.0|a|None | 60 | 7% [3, 16] | 0.29 | {'A': 42, 'other': 13, 'b': 4, 'oc': 1} |
| clean|push|random|16|8.0|a|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|16|8.0|b|None | 60 | 7% [3, 16] | 0.23 | {'A': 47, 'other': 8, 'b': 4, 'oc': 1} |
| clean|push|random|16|8.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|16|16.0|r|None | 60 | 85% [74, 92] | 0.74 | {'b': 51, 'other': 8, 'oc': 1} |
| clean|push|random|16|16.0|r|None | 60 | 0% [-0, 6] | 0.10 | {'A': 58, 'other': 2} |
| clean|push|lens|16|16.0|a|None | 60 | 17% [9, 28] | 0.71 | {'other': 48, 'b': 10, 'A': 2} |
| clean|push|random|16|16.0|a|None | 60 | 2% [0, 9] | 0.10 | {'A': 59, 'b': 1} |
| clean|push|lens|16|16.0|b|None | 60 | 72% [59, 81] | 0.67 | {'b': 43, 'other': 10, 'A': 6, 'oc': 1} |
| clean|push|random|16|16.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|4.0|r|None | 60 | 2% [0, 9] | 0.05 | {'A': 59, 'b': 1} |
| clean|push|random|20|4.0|r|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|4.0|a|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|random|20|4.0|a|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|20|4.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|random|20|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|8.0|r|None | 60 | 13% [7, 24] | 0.20 | {'b': 8, 'A': 52} |
| clean|push|random|20|8.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|20|8.0|a|None | 60 | 5% [2, 14] | 0.16 | {'A': 55, 'b': 3, 'other': 2} |
| clean|push|random|20|8.0|a|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|20|8.0|b|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|push|random|20|8.0|b|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|20|16.0|r|None | 60 | 52% [39, 64] | 0.52 | {'b': 31, 'A': 26, 'other': 2, 'oc': 1} |
| clean|push|random|20|16.0|r|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|20|16.0|a|None | 60 | 15% [8, 26] | 0.40 | {'b': 9, 'other': 26, 'A': 25} |
| clean|push|random|20|16.0|a|None | 60 | 0% [-0, 6] | 0.10 | {'A': 59, 'other': 1} |
| clean|push|lens|20|16.0|b|None | 60 | 18% [11, 30] | 0.26 | {'A': 48, 'b': 11, 'other': 1} |
| clean|push|random|20|16.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|24|4.0|r|None | 60 | 5% [2, 14] | 0.11 | {'A': 57, 'b': 3} |
| clean|push|random|24|4.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|24|4.0|a|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|random|24|4.0|a|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|push|lens|24|4.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|random|24|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|24|8.0|r|None | 60 | 12% [6, 22] | 0.22 | {'A': 51, 'oc': 1, 'b': 7, 'other': 1} |
| clean|push|random|24|8.0|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|24|8.0|a|None | 60 | 2% [0, 9] | 0.23 | {'A': 54, 'other': 5, 'b': 1} |
| clean|push|random|24|8.0|a|None | 60 | 0% [-0, 6] | 0.06 | {'A': 60} |
| clean|push|lens|24|8.0|b|None | 60 | 2% [0, 9] | 0.09 | {'A': 59, 'b': 1} |
| clean|push|random|24|8.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|24|16.0|r|None | 60 | 35% [24, 48] | 0.47 | {'b': 21, 'A': 28, 'other': 10, 'oc': 1} |
| clean|push|random|24|16.0|r|None | 60 | 2% [0, 9] | 0.09 | {'A': 59, 'b': 1} |
| clean|push|lens|24|16.0|a|None | 60 | 22% [13, 34] | 0.46 | {'b': 13, 'other': 30, 'A': 17} |
| clean|push|random|24|16.0|a|None | 60 | 0% [-0, 6] | 0.13 | {'A': 57, 'other': 3} |
| clean|push|lens|24|16.0|b|None | 60 | 42% [30, 54] | 0.50 | {'b': 25, 'other': 3, 'A': 31, 'oc': 1} |
| clean|push|random|24|16.0|b|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|push|lens|28|4.0|r|None | 60 | 17% [9, 28] | 0.23 | {'A': 49, 'b': 10, 'other': 1} |
| clean|push|random|28|4.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|28|4.0|a|None | 60 | 17% [9, 28] | 0.28 | {'A': 50, 'b': 10} |
| clean|push|random|28|4.0|a|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|28|4.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|random|28|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|28|8.0|r|None | 60 | 42% [30, 54] | 0.46 | {'b': 25, 'A': 32, 'other': 3} |
| clean|push|random|28|8.0|r|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|lens|28|8.0|a|None | 60 | 48% [36, 61] | 0.49 | {'A': 23, 'b': 29, 'other': 8} |
| clean|push|random|28|8.0|a|None | 60 | 0% [-0, 6] | 0.08 | {'A': 60} |
| clean|push|lens|28|8.0|b|None | 60 | 2% [0, 9] | 0.09 | {'A': 59, 'b': 1} |
| clean|push|random|28|8.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|28|16.0|r|None | 60 | 63% [51, 74] | 0.65 | {'other': 12, 'b': 38, 'A': 10} |
| clean|push|random|28|16.0|r|None | 60 | 3% [1, 11] | 0.17 | {'A': 57, 'b': 2, 'other': 1} |
| clean|push|lens|28|16.0|a|None | 60 | 8% [4, 18] | 0.61 | {'other': 51, 'b': 5, 'oc': 2, 'A': 2} |
| clean|push|random|28|16.0|a|None | 60 | 0% [-0, 6] | 0.29 | {'A': 43, 'other': 17} |
| clean|push|lens|28|16.0|b|None | 60 | 55% [42, 67] | 0.53 | {'b': 33, 'A': 27} |
| clean|push|random|28|16.0|b|None | 60 | 0% [-0, 6] | 0.15 | {'A': 60} |
| clean|push|lens|band|4.0|r|None | 60 | 67% [54, 77] | 0.64 | {'b': 40, 'A': 13, 'other': 7} |
| clean|push|random|band|4.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|band|4.0|a|None | 60 | 57% [44, 68] | 0.64 | {'b': 34, 'other': 18, 'A': 8} |
| clean|push|random|band|4.0|a|None | 60 | 0% [-0, 6] | 0.06 | {'A': 60} |
| clean|push|lens|band|4.0|b|None | 60 | 62% [49, 73] | 0.53 | {'b': 37, 'A': 23} |
| clean|push|random|band|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|band|8.0|r|None | 60 | 68% [56, 79] | 0.78 | {'b': 41, 'other': 19} |
| clean|push|random|band|8.0|r|None | 60 | 0% [-0, 6] | 0.08 | {'A': 58, 'other': 1, 'oc': 1} |
| clean|push|lens|band|8.0|a|None | 60 | 0% [-0, 6] | 0.61 | {'other': 60} |
| clean|push|random|band|8.0|a|None | 60 | 0% [-0, 6] | 0.13 | {'A': 53, 'other': 7} |
| clean|push|lens|band|8.0|b|None | 60 | 87% [76, 93] | 0.83 | {'b': 52, 'other': 7, 'A': 1} |
| clean|push|random|band|8.0|b|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|push|lens|band|16.0|r|None | 60 | 20% [12, 32] | 0.64 | {'other': 48, 'b': 12} |
| clean|push|random|band|16.0|r|None | 60 | 13% [7, 24] | 0.35 | {'other': 13, 'b': 8, 'A': 38, 'oc': 1} |
| clean|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | 0.55 | {'other': 60} |
| clean|push|random|band|16.0|a|None | 60 | 0% [-0, 6] | 0.47 | {'other': 60} |
| clean|push|lens|band|16.0|b|None | 60 | 78% [66, 87] | 0.84 | {'b': 47, 'other': 13} |
| clean|push|random|band|16.0|b|None | 60 | 3% [1, 11] | 0.31 | {'A': 52, 'other': 6, 'b': 2} |
| clean|emb_diff|lens|-1|1.0|b|None | 60 | 43% [32, 56] | 0.49 | {'A': 27, 'b': 26, 'other': 7} |
| clean|emb_diff|random|-1|1.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|emb_add|lens|-1|1.0|b|None | 60 | 32% [21, 44] | 0.39 | {'A': 33, 'b': 19, 'other': 8} |
| clean|emb_add|random|-1|1.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|emb_diff|lens|-1|4.0|b|None | 60 | 55% [42, 67] | 0.64 | {'other': 24, 'b': 33, 'oc': 2, 'A': 1} |
| clean|emb_diff|random|-1|4.0|b|None | 60 | 55% [42, 67] | 0.50 | {'A': 24, 'b': 33, 'oc': 3} |
| clean|emb_add|lens|-1|4.0|b|None | 60 | 0% [-0, 6] | 0.60 | {'other': 29, 'oc': 28, 'A': 3} |
| clean|emb_add|random|-1|4.0|b|None | 60 | 47% [35, 59] | 0.48 | {'A': 28, 'b': 28, 'oc': 3, 'other': 1} |
| clean|copy|None|16|None|r|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|copy|None|20|None|r|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|copy|None|24|None|r|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|copy|None|28|None|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|copy|None|32|None|r|None | 60 | 5% [2, 14] | 0.12 | {'A': 57, 'b': 3} |
| clean|copy|None|36|None|r|None | 60 | 22% [13, 34] | 0.30 | {'A': 47, 'b': 13} |
| clean|copy|None|40|None|r|None | 60 | 33% [23, 46] | 0.43 | {'A': 40, 'b': 20} |
| clean|copy|None|44|None|r|None | 60 | 25% [16, 37] | 0.42 | {'A': 45, 'b': 15} |
| clean|copy|None|48|None|r|None | 60 | 25% [16, 37] | 0.44 | {'A': 45, 'b': 15} |
| clean|patch|None|16|None|a|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|patch|None|16|4.0|a|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|patch|None|16|8.0|a|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|patch|None|16|16.0|a|None | 60 | 2% [0, 9] | 0.11 | {'A': 59, 'b': 1} |
| clean|patch|None|20|None|a|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|patch|None|20|4.0|a|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|patch|None|20|8.0|a|None | 60 | 0% [-0, 6] | 0.08 | {'A': 60} |
| clean|patch|None|20|16.0|a|None | 60 | 15% [8, 26] | 0.29 | {'A': 46, 'other': 5, 'b': 9} |
| clean|patch|None|24|None|a|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|patch|None|24|4.0|a|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|patch|None|24|8.0|a|None | 60 | 2% [0, 9] | 0.16 | {'A': 59, 'b': 1} |
| clean|patch|None|24|16.0|a|None | 60 | 38% [27, 51] | 0.50 | {'b': 23, 'A': 24, 'other': 12, 'oc': 1} |
| clean|patch|None|28|None|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|patch|None|28|4.0|a|None | 60 | 2% [0, 9] | 0.12 | {'A': 59, 'b': 1} |
| clean|patch|None|28|8.0|a|None | 60 | 35% [24, 48] | 0.42 | {'b': 21, 'A': 37, 'oc': 1, 'other': 1} |
| clean|patch|None|28|16.0|a|None | 60 | 33% [23, 46] | 0.59 | {'b': 20, 'other': 28, 'A': 12} |
| off|push|lens|16|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|16|8.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 42, 'other': 13, 'bO': 4, 'oc': 1} |
| off|push|lens|16|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 48, 'bO': 10, 'A': 2} |
| off|push|lens|20|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|20|8.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 57, 'other': 3} |
| off|push|lens|20|16.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 8, 'other': 27, 'A': 25} |
| off|push|lens|24|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|24|8.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 53, 'other': 4, 'bO': 3} |
| off|push|lens|24|16.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 14, 'other': 29, 'A': 17} |
| off|push|lens|28|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 50, 'bO': 10} |
| off|push|lens|28|8.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 23, 'bO': 29, 'other': 8} |
| off|push|lens|28|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 50, 'bO': 6, 'oc': 2, 'A': 2} |
| off|push|lens|band|4.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 32, 'other': 18, 'A': 10} |
| off|push|lens|band|8.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |
| off|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-insert: k -, J +0.00 [+0.00, +0.00] (ref rate 0.97); E-head: k -, J +0.00 [+0.00, +0.00] (ref rate 0.47); E-cue: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-unrelated: k -, J - (ref rate 0.00); W-copy*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.33); emb*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.32); patch_matched: k -, J - (ref rate 0.00); low_margin: k -
K1 - -> untestable; gate -0.14 [-0.39, +0.12]; K2 nb - a/2 +0.00 [+0.00, +0.00], b - nb +0.00 [+0.00, +0.00] -> inconclusive; K4 -0.11 [-0.14, -0.08]
JS(P*, .) {"clean": 0.007, "E-name": 0.67, "E-insert": 0.551, "E-head": 0.621, "E-cue": 0.668, "E-unrelated": 0.006}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [0.0936, 0.1012, 0.079, 0.0953], "E-insert": [0.0939, 0.0951, 0.0967, 0.1063], "E-head": [0.1874, 0.1622, 0.1392, 0.1378], "E-cue": [0.2079, 0.2037, 0.1801, 0.1912], "E-unrelated": [0.137, 0.1741, 0.1811, 0.2225]}
transit proj on C's delta [44, 48, 52]: P*_b [0.0329, 0.036, 0.0475], P* [0.2549, 0.2587, 0.2322], edits {"E-name": [0.8444, 0.8218, 0.8078], "E-insert": [0.7366, 0.7212, 0.7131], "E-head": [0.7193, 0.6983, 0.6887], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.105, 0.1207, 0.1186]}

## RL (W-copy* = ('clean', 'copy', None, 36, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|edit|None|None|None|None|E-name | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|edit|None|None|None|None|E-insert | 60 | 100% [94, 100] | 0.59 | {'b': 60} |
| clean|edit|None|None|None|None|E-head | 60 | 72% [59, 81] | 0.53 | {'b': 43, 'A': 17} |
| clean|edit|None|None|None|None|E-cue | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|edit|None|None|None|None|E-unrelated | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|16|4.0|r|None | 60 | 7% [3, 16] | 0.15 | {'A': 56, 'b': 4} |
| clean|push|random|16|4.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|16|4.0|a|None | 60 | 17% [9, 28] | 0.26 | {'b': 10, 'A': 49, 'oc': 1} |
| clean|push|random|16|4.0|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|16|4.0|b|None | 60 | 13% [7, 24] | 0.23 | {'b': 8, 'A': 51, 'oc': 1} |
| clean|push|random|16|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|16|8.0|r|None | 60 | 40% [29, 53] | 0.44 | {'b': 24, 'A': 36} |
| clean|push|random|16|8.0|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|16|8.0|a|None | 60 | 92% [82, 96] | 0.74 | {'b': 55, 'A': 4, 'oc': 1} |
| clean|push|random|16|8.0|a|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|16|8.0|b|None | 60 | 92% [82, 96] | 0.80 | {'b': 55, 'A': 5} |
| clean|push|random|16|8.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|16|16.0|r|None | 60 | 60% [47, 71] | 0.50 | {'b': 36, 'A': 24} |
| clean|push|random|16|16.0|r|None | 60 | 0% [-0, 6] | 0.10 | {'A': 60} |
| clean|push|lens|16|16.0|a|None | 60 | 25% [16, 37] | 0.74 | {'other': 45, 'b': 15} |
| clean|push|random|16|16.0|a|None | 60 | 0% [-0, 6] | 0.15 | {'A': 59, 'other': 1} |
| clean|push|lens|16|16.0|b|None | 60 | 100% [94, 100] | 0.95 | {'b': 60} |
| clean|push|random|16|16.0|b|None | 60 | 2% [0, 9] | 0.05 | {'A': 59, 'b': 1} |
| clean|push|lens|20|4.0|r|None | 60 | 2% [0, 9] | 0.07 | {'A': 59, 'b': 1} |
| clean|push|random|20|4.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|20|4.0|a|None | 60 | 10% [5, 20] | 0.21 | {'A': 54, 'b': 6} |
| clean|push|random|20|4.0|a|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|lens|20|4.0|b|None | 60 | 10% [5, 20] | 0.18 | {'A': 54, 'b': 6} |
| clean|push|random|20|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|8.0|r|None | 60 | 15% [8, 26] | 0.25 | {'A': 51, 'b': 9} |
| clean|push|random|20|8.0|r|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|lens|20|8.0|a|None | 60 | 82% [70, 89] | 0.66 | {'b': 49, 'A': 11} |
| clean|push|random|20|8.0|a|None | 60 | 0% [-0, 6] | 0.10 | {'A': 60} |
| clean|push|lens|20|8.0|b|None | 60 | 82% [70, 89] | 0.69 | {'b': 49, 'A': 11} |
| clean|push|random|20|8.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|20|16.0|r|None | 60 | 37% [26, 49] | 0.42 | {'b': 22, 'A': 37, 'oc': 1} |
| clean|push|random|20|16.0|r|None | 60 | 0% [-0, 6] | 0.16 | {'A': 59, 'oc': 1} |
| clean|push|lens|20|16.0|a|None | 60 | 80% [68, 88] | 0.77 | {'b': 48, 'other': 12} |
| clean|push|random|20|16.0|a|None | 60 | 0% [-0, 6] | 0.20 | {'A': 59, 'oc': 1} |
| clean|push|lens|20|16.0|b|None | 60 | 100% [94, 100] | 0.92 | {'b': 60} |
| clean|push|random|20|16.0|b|None | 60 | 0% [-0, 6] | 0.06 | {'A': 60} |
| clean|push|lens|24|4.0|r|None | 60 | 2% [0, 9] | 0.11 | {'A': 59, 'b': 1} |
| clean|push|random|24|4.0|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|24|4.0|a|None | 60 | 37% [26, 49] | 0.38 | {'A': 38, 'b': 22} |
| clean|push|random|24|4.0|a|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|lens|24|4.0|b|None | 60 | 33% [23, 46] | 0.35 | {'A': 40, 'b': 20} |
| clean|push|random|24|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|24|8.0|r|None | 60 | 17% [9, 28] | 0.32 | {'A': 50, 'b': 10} |
| clean|push|random|24|8.0|r|None | 60 | 0% [-0, 6] | 0.08 | {'A': 60} |
| clean|push|lens|24|8.0|a|None | 60 | 90% [80, 95] | 0.68 | {'b': 54, 'A': 6} |
| clean|push|random|24|8.0|a|None | 60 | 0% [-0, 6] | 0.11 | {'A': 60} |
| clean|push|lens|24|8.0|b|None | 60 | 83% [72, 91] | 0.79 | {'b': 50, 'A': 10} |
| clean|push|random|24|8.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|24|16.0|r|None | 60 | 27% [17, 39] | 0.45 | {'b': 16, 'A': 40, 'oc': 4} |
| clean|push|random|24|16.0|r|None | 60 | 0% [-0, 6] | 0.24 | {'A': 59, 'oc': 1} |
| clean|push|lens|24|16.0|a|None | 60 | 70% [57, 80] | 0.67 | {'b': 42, 'other': 16, 'oc': 2} |
| clean|push|random|24|16.0|a|None | 60 | 0% [-0, 6] | 0.25 | {'A': 57, 'other': 3} |
| clean|push|lens|24|16.0|b|None | 60 | 100% [94, 100] | 0.82 | {'b': 60} |
| clean|push|random|24|16.0|b|None | 60 | 0% [-0, 6] | 0.08 | {'A': 60} |
| clean|push|lens|28|4.0|r|None | 60 | 15% [8, 26] | 0.31 | {'A': 51, 'b': 9} |
| clean|push|random|28|4.0|r|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|28|4.0|a|None | 60 | 22% [13, 34] | 0.29 | {'A': 47, 'b': 13} |
| clean|push|random|28|4.0|a|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|lens|28|4.0|b|None | 60 | 10% [5, 20] | 0.15 | {'A': 54, 'b': 6} |
| clean|push|random|28|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|28|8.0|r|None | 60 | 18% [11, 30] | 0.38 | {'b': 11, 'A': 48, 'oc': 1} |
| clean|push|random|28|8.0|r|None | 60 | 0% [-0, 6] | 0.17 | {'A': 60} |
| clean|push|lens|28|8.0|a|None | 60 | 67% [54, 77] | 0.55 | {'b': 40, 'A': 20} |
| clean|push|random|28|8.0|a|None | 60 | 0% [-0, 6] | 0.16 | {'A': 60} |
| clean|push|lens|28|8.0|b|None | 60 | 28% [19, 41] | 0.34 | {'b': 17, 'A': 43} |
| clean|push|random|28|8.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|28|16.0|r|None | 60 | 7% [3, 16] | 0.35 | {'A': 52, 'b': 4, 'oc': 4} |
| clean|push|random|28|16.0|r|None | 60 | 2% [0, 9] | 0.29 | {'A': 58, 'oc': 1, 'b': 1} |
| clean|push|lens|28|16.0|a|None | 60 | 22% [13, 34] | 0.51 | {'b': 13, 'other': 35, 'A': 10, 'oc': 2} |
| clean|push|random|28|16.0|a|None | 60 | 2% [0, 9] | 0.36 | {'A': 53, 'b': 1, 'oc': 1, 'other': 5} |
| clean|push|lens|28|16.0|b|None | 60 | 43% [32, 56] | 0.45 | {'b': 26, 'A': 30, 'oc': 4} |
| clean|push|random|28|16.0|b|None | 60 | 0% [-0, 6] | 0.11 | {'A': 60} |
| clean|push|lens|band|4.0|r|None | 60 | 55% [42, 67] | 0.51 | {'b': 33, 'A': 27} |
| clean|push|random|band|4.0|r|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|lens|band|4.0|a|None | 60 | 97% [89, 99] | 0.79 | {'b': 58, 'other': 2} |
| clean|push|random|band|4.0|a|None | 60 | 0% [-0, 6] | 0.11 | {'A': 60} |
| clean|push|lens|band|4.0|b|None | 60 | 100% [94, 100] | 0.94 | {'b': 60} |
| clean|push|random|band|4.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|band|8.0|r|None | 60 | 35% [24, 48] | 0.45 | {'b': 21, 'A': 34, 'oc': 5} |
| clean|push|random|band|8.0|r|None | 60 | 0% [-0, 6] | 0.18 | {'A': 60} |
| clean|push|lens|band|8.0|a|None | 60 | 0% [-0, 6] | 0.58 | {'other': 60} |
| clean|push|random|band|8.0|a|None | 60 | 0% [-0, 6] | 0.24 | {'A': 58, 'other': 2} |
| clean|push|lens|band|8.0|b|None | 60 | 100% [94, 100] | 0.84 | {'b': 60} |
| clean|push|random|band|8.0|b|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|lens|band|16.0|r|None | 60 | 5% [2, 14] | 0.42 | {'other': 37, 'A': 18, 'b': 3, 'oc': 2} |
| clean|push|random|band|16.0|r|None | 60 | 5% [2, 14] | 0.32 | {'A': 57, 'b': 3} |
| clean|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | 0.54 | {'other': 60} |
| clean|push|random|band|16.0|a|None | 60 | 0% [-0, 6] | 0.50 | {'other': 60} |
| clean|push|lens|band|16.0|b|None | 60 | 95% [86, 98] | 0.74 | {'b': 57, 'oc': 3} |
| clean|push|random|band|16.0|b|None | 60 | 10% [5, 20] | 0.42 | {'A': 47, 'b': 6, 'oc': 7} |
| clean|emb_diff|lens|-1|1.0|b|None | 60 | 98% [91, 100] | 0.84 | {'b': 59, 'A': 1} |
| clean|emb_diff|random|-1|1.0|b|None | 60 | 5% [2, 14] | 0.16 | {'A': 52, 'oc': 5, 'b': 3} |
| clean|emb_add|lens|-1|1.0|b|None | 60 | 88% [78, 94] | 0.83 | {'b': 53, 'A': 7} |
| clean|emb_add|random|-1|1.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|emb_diff|lens|-1|4.0|b|None | 60 | 88% [78, 94] | 0.65 | {'b': 53, 'oc': 7} |
| clean|emb_diff|random|-1|4.0|b|None | 60 | 35% [24, 48] | 0.50 | {'oc': 16, 'b': 21, 'A': 23} |
| clean|emb_add|lens|-1|4.0|b|None | 60 | 100% [94, 100] | 0.94 | {'b': 60} |
| clean|emb_add|random|-1|4.0|b|None | 60 | 37% [26, 49] | 0.50 | {'oc': 17, 'b': 22, 'A': 21} |
| clean|copy|None|16|None|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|copy|None|20|None|r|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|copy|None|24|None|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|copy|None|28|None|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|copy|None|32|None|r|None | 60 | 22% [13, 34] | 0.36 | {'A': 47, 'b': 13} |
| clean|copy|None|36|None|r|None | 60 | 52% [39, 64] | 0.49 | {'b': 31, 'A': 29} |
| clean|copy|None|40|None|r|None | 60 | 67% [54, 77] | 0.53 | {'b': 40, 'A': 20} |
| clean|copy|None|44|None|r|None | 60 | 97% [89, 99] | 0.68 | {'b': 58, 'A': 2} |
| clean|copy|None|48|None|r|None | 60 | 100% [94, 100] | 0.78 | {'b': 60} |
| clean|patch|None|16|None|a|None | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|patch|None|16|4.0|a|None | 60 | 2% [0, 9] | 0.05 | {'A': 59, 'b': 1} |
| clean|patch|None|16|8.0|a|None | 60 | 70% [57, 80] | 0.62 | {'b': 42, 'A': 17, 'oc': 1} |
| clean|patch|None|16|16.0|a|None | 60 | 100% [94, 100] | 0.87 | {'b': 60} |
| clean|patch|None|20|None|a|None | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|patch|None|20|4.0|a|None | 60 | 5% [2, 14] | 0.12 | {'A': 57, 'b': 3} |
| clean|patch|None|20|8.0|a|None | 60 | 87% [76, 93] | 0.75 | {'b': 52, 'A': 7, 'oc': 1} |
| clean|patch|None|20|16.0|a|None | 60 | 97% [89, 99] | 0.88 | {'b': 58, 'other': 2} |
| clean|patch|None|24|None|a|None | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|patch|None|24|4.0|a|None | 60 | 13% [7, 24] | 0.17 | {'A': 52, 'b': 8} |
| clean|patch|None|24|8.0|a|None | 60 | 78% [66, 87] | 0.69 | {'b': 47, 'A': 13} |
| clean|patch|None|24|16.0|a|None | 60 | 85% [74, 92] | 0.85 | {'b': 51, 'other': 9} |
| clean|patch|None|28|None|a|None | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|patch|None|28|4.0|a|None | 60 | 27% [17, 39] | 0.38 | {'A': 44, 'b': 16} |
| clean|patch|None|28|8.0|a|None | 60 | 100% [94, 100] | 0.88 | {'b': 60} |
| clean|patch|None|28|16.0|a|None | 60 | 80% [68, 88] | 0.82 | {'b': 48, 'other': 11, 'oc': 1} |
| off|push|lens|16|4.0|a|None | 60 | 2% [0, 9] | nan | {'bO': 9, 'A': 50, 'b': 1} |
| off|push|lens|16|8.0|a|None | 60 | 2% [0, 9] | nan | {'bO': 55, 'A': 4, 'b': 1} |
| off|push|lens|16|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 46, 'bO': 14} |
| off|push|lens|20|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 55, 'bO': 5} |
| off|push|lens|20|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 50, 'A': 10} |
| off|push|lens|20|16.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 48, 'other': 12} |
| off|push|lens|24|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 38, 'bO': 22} |
| off|push|lens|24|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 53, 'A': 7} |
| off|push|lens|24|16.0|a|None | 60 | 3% [1, 11] | nan | {'bO': 40, 'other': 18, 'b': 2} |
| off|push|lens|28|4.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 12, 'A': 48} |
| off|push|lens|28|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 38, 'A': 22} |
| off|push|lens|28|16.0|a|None | 60 | 3% [1, 11] | nan | {'bO': 12, 'other': 37, 'A': 9, 'b': 2} |
| off|push|lens|band|4.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 58, 'other': 2} |
| off|push|lens|band|8.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |
| off|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.37 [+0.25, +0.48] (ref rate 1.00); E-insert: k -, J +0.37 [+0.25, +0.48] (ref rate 1.00); E-head: k -0.11 [-0.31, +0.09], J +0.27 [+0.16, +0.40] (ref rate 0.72); E-cue: k -, J +0.37 [+0.25, +0.48] (ref rate 1.00); E-unrelated: k -, J +0.00 [+0.00, +0.00] (ref rate 0.00); W-copy*: k +0.17 [-0.07, +0.40], J +0.36 [+0.21, +0.51] (ref rate 0.52); emb*: k +0.03 [-0.09, +0.16], J +0.36 [+0.24, +0.49] (ref rate 0.88); patch_matched: k +0.34 [+0.12, +0.55], J +0.30 [+0.12, +0.50] (ref rate 0.13); low_margin: k +0.13 [-0.10, +0.36]
K1 - -> untestable; gate -; K2 nb - a/2 -0.18 [-0.24, -0.12], b - nb +0.33 [+0.22, +0.45] -> write; K4 -0.33 [-0.37, -0.29]
JS(P*, .) {"clean": 0.218, "E-name": 0.413, "E-insert": 0.256, "E-head": 0.184, "E-cue": 0.412, "E-unrelated": 0.217}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [-0.0757, -0.1313, -0.0852, -0.0364], "E-insert": [0.088, 0.1707, 0.2134, 0.1794], "E-head": [0.2938, 0.3343, 0.3155, 0.2698], "E-cue": [0.2199, 0.23, 0.2208, 0.2406], "E-unrelated": [0.1501, 0.2435, 0.2514, 0.2669]}
transit proj on C's delta [44, 48, 52]: P*_b [0.1994, 0.2152, 0.2117], P* [0.329, 0.3304, 0.3296], edits {"E-name": [0.501, 0.5327, 0.5658], "E-insert": [0.4885, 0.514, 0.5171], "E-head": [0.4323, 0.4555, 0.4351], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.1607, 0.1668, 0.145]}

## RR (W-copy* = ('clean', 'copy', None, 48, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|edit|None|None|None|None|E-name | 60 | 100% [94, 100] | 1.06 | {'b': 60} |
| clean|edit|None|None|None|None|E-insert | 60 | 92% [82, 96] | 0.74 | {'b': 55, 'A': 4, 'oc': 1} |
| clean|edit|None|None|None|None|E-head | 60 | 48% [36, 61] | 0.70 | {'other': 29, 'b': 29, 'A': 2} |
| clean|edit|None|None|None|None|E-cue | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|edit|None|None|None|None|E-unrelated | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|16|4.0|r|None | 60 | 12% [6, 22] | 0.19 | {'A': 49, 'b': 7, 'other': 4} |
| clean|push|random|16|4.0|r|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|16|4.0|a|None | 60 | 37% [26, 49] | 0.39 | {'b': 22, 'A': 37, 'other': 1} |
| clean|push|random|16|4.0|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|16|4.0|b|None | 60 | 25% [16, 37] | 0.32 | {'b': 15, 'A': 44, 'other': 1} |
| clean|push|random|16|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|16|8.0|r|None | 60 | 43% [32, 56] | 0.56 | {'b': 26, 'A': 24, 'other': 9, 'oc': 1} |
| clean|push|random|16|8.0|r|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|16|8.0|a|None | 60 | 95% [86, 98] | 0.87 | {'b': 57, 'A': 3} |
| clean|push|random|16|8.0|a|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|16|8.0|b|None | 60 | 95% [86, 98] | 0.88 | {'b': 57, 'A': 3} |
| clean|push|random|16|8.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|16|16.0|r|None | 60 | 75% [63, 84] | 0.72 | {'b': 45, 'other': 10, 'A': 5} |
| clean|push|random|16|16.0|r|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|16|16.0|a|None | 60 | 23% [14, 35] | 0.86 | {'other': 45, 'b': 14, 'A': 1} |
| clean|push|random|16|16.0|a|None | 60 | 0% [-0, 6] | 0.12 | {'A': 60} |
| clean|push|lens|16|16.0|b|None | 60 | 100% [94, 100] | 0.96 | {'b': 60} |
| clean|push|random|16|16.0|b|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|push|lens|20|4.0|r|None | 60 | 3% [1, 11] | 0.09 | {'A': 58, 'b': 2} |
| clean|push|random|20|4.0|r|None | 60 | 0% [-0, 6] | -0.01 | {'A': 60} |
| clean|push|lens|20|4.0|a|None | 60 | 13% [7, 24] | 0.26 | {'A': 52, 'b': 8} |
| clean|push|random|20|4.0|a|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|20|4.0|b|None | 60 | 12% [6, 22] | 0.23 | {'A': 53, 'b': 7} |
| clean|push|random|20|4.0|b|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|20|8.0|r|None | 60 | 22% [13, 34] | 0.34 | {'A': 43, 'b': 13, 'other': 4} |
| clean|push|random|20|8.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|20|8.0|a|None | 60 | 83% [72, 91] | 0.74 | {'b': 50, 'A': 7, 'other': 3} |
| clean|push|random|20|8.0|a|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|20|8.0|b|None | 60 | 95% [86, 98] | 0.81 | {'b': 57, 'A': 3} |
| clean|push|random|20|8.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|16.0|r|None | 60 | 57% [44, 68] | 0.60 | {'b': 34, 'A': 20, 'other': 6} |
| clean|push|random|20|16.0|r|None | 60 | 0% [-0, 6] | 0.10 | {'A': 60} |
| clean|push|lens|20|16.0|a|None | 60 | 58% [46, 70] | 0.80 | {'b': 35, 'other': 22, 'A': 3} |
| clean|push|random|20|16.0|a|None | 60 | 0% [-0, 6] | 0.13 | {'A': 58, 'other': 2} |
| clean|push|lens|20|16.0|b|None | 60 | 100% [94, 100] | 0.96 | {'b': 60} |
| clean|push|random|20|16.0|b|None | 60 | 3% [1, 11] | 0.08 | {'A': 58, 'b': 2} |
| clean|push|lens|24|4.0|r|None | 60 | 10% [5, 20] | 0.19 | {'A': 54, 'b': 6} |
| clean|push|random|24|4.0|r|None | 60 | 0% [-0, 6] | -0.01 | {'A': 60} |
| clean|push|lens|24|4.0|a|None | 60 | 43% [32, 56] | 0.50 | {'A': 30, 'b': 26, 'other': 4} |
| clean|push|random|24|4.0|a|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|24|4.0|b|None | 60 | 47% [35, 59] | 0.45 | {'A': 31, 'b': 28, 'other': 1} |
| clean|push|random|24|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|24|8.0|r|None | 60 | 40% [29, 53] | 0.47 | {'A': 29, 'b': 24, 'other': 7} |
| clean|push|random|24|8.0|r|None | 60 | 0% [-0, 6] | 0.06 | {'A': 60} |
| clean|push|lens|24|8.0|a|None | 60 | 85% [74, 92] | 0.78 | {'b': 51, 'A': 8, 'oc': 1} |
| clean|push|random|24|8.0|a|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|lens|24|8.0|b|None | 60 | 97% [89, 99] | 0.88 | {'b': 58, 'A': 2} |
| clean|push|random|24|8.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|24|16.0|r|None | 60 | 42% [30, 54] | 0.49 | {'b': 25, 'A': 30, 'other': 4, 'oc': 1} |
| clean|push|random|24|16.0|r|None | 60 | 2% [0, 9] | 0.15 | {'A': 59, 'b': 1} |
| clean|push|lens|24|16.0|a|None | 60 | 47% [35, 59] | 0.76 | {'b': 28, 'other': 32} |
| clean|push|random|24|16.0|a|None | 60 | 3% [1, 11] | 0.18 | {'A': 53, 'other': 5, 'b': 2} |
| clean|push|lens|24|16.0|b|None | 60 | 93% [84, 97] | 0.91 | {'b': 56, 'other': 4} |
| clean|push|random|24|16.0|b|None | 60 | 0% [-0, 6] | 0.10 | {'A': 60} |
| clean|push|lens|28|4.0|r|None | 60 | 38% [27, 51] | 0.39 | {'A': 37, 'b': 23} |
| clean|push|random|28|4.0|r|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|28|4.0|a|None | 60 | 62% [49, 73] | 0.53 | {'A': 23, 'b': 37} |
| clean|push|random|28|4.0|a|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|28|4.0|b|None | 60 | 15% [8, 26] | 0.23 | {'A': 51, 'b': 9} |
| clean|push|random|28|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|28|8.0|r|None | 60 | 50% [38, 62] | 0.45 | {'b': 30, 'A': 28, 'other': 2} |
| clean|push|random|28|8.0|r|None | 60 | 0% [-0, 6] | 0.12 | {'A': 60} |
| clean|push|lens|28|8.0|a|None | 60 | 83% [72, 91] | 0.82 | {'b': 50, 'other': 5, 'A': 5} |
| clean|push|random|28|8.0|a|None | 60 | 3% [1, 11] | 0.13 | {'A': 58, 'b': 2} |
| clean|push|lens|28|8.0|b|None | 60 | 65% [52, 76] | 0.61 | {'b': 39, 'A': 20, 'other': 1} |
| clean|push|random|28|8.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|28|16.0|r|None | 60 | 30% [20, 43] | 0.38 | {'b': 18, 'A': 40, 'other': 2} |
| clean|push|random|28|16.0|r|None | 60 | 2% [0, 9] | 0.21 | {'A': 59, 'b': 1} |
| clean|push|lens|28|16.0|a|None | 60 | 12% [6, 22] | 0.66 | {'b': 7, 'other': 51, 'oc': 2} |
| clean|push|random|28|16.0|a|None | 60 | 2% [0, 9] | 0.30 | {'A': 44, 'b': 1, 'other': 15} |
| clean|push|lens|28|16.0|b|None | 60 | 83% [72, 91] | 0.70 | {'b': 50, 'A': 10} |
| clean|push|random|28|16.0|b|None | 60 | 0% [-0, 6] | 0.15 | {'A': 60} |
| clean|push|lens|band|4.0|r|None | 60 | 72% [59, 81] | 0.69 | {'b': 43, 'A': 6, 'other': 11} |
| clean|push|random|band|4.0|r|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|band|4.0|a|None | 60 | 80% [68, 88] | 0.86 | {'b': 48, 'other': 8, 'oc': 2, 'A': 2} |
| clean|push|random|band|4.0|a|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|lens|band|4.0|b|None | 60 | 100% [94, 100] | 0.97 | {'b': 60} |
| clean|push|random|band|4.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|band|8.0|r|None | 60 | 57% [44, 68] | 0.57 | {'b': 34, 'A': 16, 'other': 10} |
| clean|push|random|band|8.0|r|None | 60 | 2% [0, 9] | 0.14 | {'A': 59, 'b': 1} |
| clean|push|lens|band|8.0|a|None | 60 | 0% [-0, 6] | 0.61 | {'other': 60} |
| clean|push|random|band|8.0|a|None | 60 | 0% [-0, 6] | 0.20 | {'A': 53, 'other': 7} |
| clean|push|lens|band|8.0|b|None | 60 | 95% [86, 98] | 0.92 | {'b': 57, 'other': 3} |
| clean|push|random|band|8.0|b|None | 60 | 2% [0, 9] | 0.12 | {'A': 59, 'b': 1} |
| clean|push|lens|band|16.0|r|None | 60 | 10% [5, 20] | 0.40 | {'other': 35, 'oc': 2, 'A': 17, 'b': 6} |
| clean|push|random|band|16.0|r|None | 60 | 3% [1, 11] | 0.23 | {'A': 58, 'b': 2} |
| clean|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | 0.57 | {'other': 60} |
| clean|push|random|band|16.0|a|None | 60 | 0% [-0, 6] | 0.50 | {'other': 60} |
| clean|push|lens|band|16.0|b|None | 60 | 82% [70, 89] | 0.85 | {'b': 49, 'other': 11} |
| clean|push|random|band|16.0|b|None | 60 | 3% [1, 11] | 0.40 | {'A': 42, 'other': 16, 'b': 2} |
| clean|emb_diff|lens|-1|1.0|b|None | 60 | 97% [89, 99] | 0.83 | {'b': 58, 'A': 2} |
| clean|emb_diff|random|-1|1.0|b|None | 60 | 8% [4, 18] | 0.16 | {'A': 54, 'b': 5, 'other': 1} |
| clean|emb_add|lens|-1|1.0|b|None | 60 | 88% [78, 94] | 0.81 | {'b': 53, 'A': 6, 'other': 1} |
| clean|emb_add|random|-1|1.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|emb_diff|lens|-1|4.0|b|None | 60 | 55% [42, 67] | 0.60 | {'A': 6, 'oc': 7, 'b': 33, 'other': 14} |
| clean|emb_diff|random|-1|4.0|b|None | 60 | 50% [38, 62] | 0.52 | {'A': 26, 'b': 30, 'oc': 4} |
| clean|emb_add|lens|-1|4.0|b|None | 60 | 2% [0, 9] | 0.48 | {'A': 26, 'other': 23, 'oc': 10, 'b': 1} |
| clean|emb_add|random|-1|4.0|b|None | 60 | 53% [41, 65] | 0.52 | {'A': 26, 'b': 32, 'oc': 2} |
| clean|copy|None|16|None|r|None | 60 | 0% [-0, 6] | -0.01 | {'A': 60} |
| clean|copy|None|20|None|r|None | 60 | 0% [-0, 6] | -0.01 | {'A': 60} |
| clean|copy|None|24|None|r|None | 60 | 0% [-0, 6] | -0.01 | {'A': 60} |
| clean|copy|None|28|None|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|copy|None|32|None|r|None | 60 | 0% [-0, 6] | 0.19 | {'A': 60} |
| clean|copy|None|36|None|r|None | 60 | 7% [3, 16] | 0.30 | {'A': 56, 'b': 4} |
| clean|copy|None|40|None|r|None | 60 | 13% [7, 24] | 0.34 | {'A': 52, 'b': 8} |
| clean|copy|None|44|None|r|None | 60 | 13% [7, 24] | 0.36 | {'A': 52, 'b': 8} |
| clean|copy|None|48|None|r|None | 60 | 28% [19, 41] | 0.46 | {'A': 43, 'b': 17} |
| clean|patch|None|16|None|a|None | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|patch|None|16|4.0|a|None | 60 | 2% [0, 9] | 0.03 | {'A': 59, 'b': 1} |
| clean|patch|None|16|8.0|a|None | 60 | 68% [56, 79] | 0.67 | {'b': 41, 'A': 19} |
| clean|patch|None|16|16.0|a|None | 60 | 100% [94, 100] | 0.93 | {'b': 60} |
| clean|patch|None|20|None|a|None | 60 | 100% [94, 100] | 0.98 | {'b': 60} |
| clean|patch|None|20|4.0|a|None | 60 | 5% [2, 14] | 0.09 | {'A': 57, 'b': 3} |
| clean|patch|None|20|8.0|a|None | 60 | 90% [80, 95] | 0.81 | {'b': 54, 'A': 6} |
| clean|patch|None|20|16.0|a|None | 60 | 93% [84, 97] | 0.91 | {'b': 56, 'other': 4} |
| clean|patch|None|24|None|a|None | 60 | 100% [94, 100] | 0.97 | {'b': 60} |
| clean|patch|None|24|4.0|a|None | 60 | 12% [6, 22] | 0.13 | {'A': 53, 'b': 7} |
| clean|patch|None|24|8.0|a|None | 60 | 85% [74, 92] | 0.74 | {'b': 51, 'A': 9} |
| clean|patch|None|24|16.0|a|None | 60 | 90% [80, 95] | 0.90 | {'b': 54, 'other': 6} |
| clean|patch|None|28|None|a|None | 60 | 100% [94, 100] | 0.98 | {'b': 60} |
| clean|patch|None|28|4.0|a|None | 60 | 17% [9, 28] | 0.30 | {'A': 50, 'b': 10} |
| clean|patch|None|28|8.0|a|None | 60 | 100% [94, 100] | 0.91 | {'b': 60} |
| clean|patch|None|28|16.0|a|None | 60 | 83% [72, 91] | 0.87 | {'b': 50, 'other': 10} |
| off|push|lens|16|4.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 21, 'A': 38, 'other': 1} |
| off|push|lens|16|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 57, 'A': 3} |
| off|push|lens|16|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 44, 'bO': 16} |
| off|push|lens|20|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 51, 'bO': 9} |
| off|push|lens|20|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 52, 'A': 6, 'other': 2} |
| off|push|lens|20|16.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 35, 'other': 22, 'A': 3} |
| off|push|lens|24|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 30, 'bO': 26, 'other': 4} |
| off|push|lens|24|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 51, 'A': 8, 'oc': 1} |
| off|push|lens|24|16.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 28, 'other': 32} |
| off|push|lens|28|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 23, 'bO': 36, 'other': 1} |
| off|push|lens|28|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 48, 'A': 6, 'other': 6} |
| off|push|lens|28|16.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 7, 'other': 51, 'oc': 2} |
| off|push|lens|band|4.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 48, 'other': 8, 'oc': 2, 'A': 2} |
| off|push|lens|band|8.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |
| off|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.43 [+0.30, +0.55] (ref rate 1.00); E-insert: k +0.01 [-0.12, +0.14], J +0.42 [+0.29, +0.55] (ref rate 0.92); E-head: k +0.03 [-0.21, +0.27], J +0.31 [+0.18, +0.46] (ref rate 0.48); E-cue: k -, J +0.43 [+0.30, +0.55] (ref rate 1.00); E-unrelated: k -, J +0.00 [+0.00, +0.00] (ref rate 0.00); W-copy*: k -0.17 [-0.40, +0.07], J +0.13 [+0.03, +0.26] (ref rate 0.28); emb*: k +0.00 [-0.14, +0.15], J +0.41 [+0.28, +0.54] (ref rate 0.88); patch_matched: k +0.29 [+0.12, +0.49], J +0.27 [+0.11, +0.44] (ref rate 0.12); low_margin: k +0.27 [+0.01, +0.50]
K1 +0.18 [-0.10, +0.43] -> inconclusive; gate +0.13 [-0.11, +0.42]; K2 nb - a/2 -0.22 [-0.28, -0.15], b - nb +0.47 [+0.35, +0.58] -> write; K4 -0.23 [-0.26, -0.20]
JS(P*, .) {"clean": 0.289, "E-name": 0.353, "E-insert": 0.248, "E-head": 0.304, "E-cue": 0.35, "E-unrelated": 0.287}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [-0.0182, 0.0327, 0.0622, 0.1616], "E-insert": [0.1252, 0.2517, 0.2982, 0.3402], "E-head": [0.3005, 0.3309, 0.3453, 0.331], "E-cue": [0.209, 0.2667, 0.2692, 0.3166], "E-unrelated": [0.1426, 0.138, 0.1765, 0.2204]}
transit proj on C's delta [44, 48, 52]: P*_b [0.2668, 0.2707, 0.2944], P* [0.351, 0.3627, 0.3777], edits {"E-name": [0.7142, 0.7036, 0.7028], "E-insert": [0.6211, 0.6076, 0.6006], "E-head": [0.4973, 0.4909, 0.4802], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.0854, 0.0954, 0.102]}

## R (W-copy* = ('clean', 'copy', None, 36, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|edit|None|None|None|None|E-name | 60 | 100% [94, 100] | 1.14 | {'b': 60} |
| clean|edit|None|None|None|None|E-insert | 60 | 90% [80, 95] | 0.58 | {'b': 54, 'A': 2, 'other': 4} |
| clean|edit|None|None|None|None|E-cue | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|edit|None|None|None|None|E-unrelated | 60 | 0% [-0, 6] | 0.07 | {'A': 58, 'other': 2} |
| clean|push|lens|16|4.0|r|None | 60 | 28% [19, 41] | 0.35 | {'A': 42, 'b': 17, 'other': 1} |
| clean|push|random|16|4.0|r|None | 60 | 2% [0, 9] | 0.01 | {'A': 59, 'b': 1} |
| clean|push|lens|16|4.0|a|None | 60 | 90% [80, 95] | 0.91 | {'b': 54, 'A': 5, 'other': 1} |
| clean|push|random|16|4.0|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 59, 'other': 1} |
| clean|push|lens|16|4.0|b|None | 60 | 88% [78, 94] | 0.85 | {'b': 53, 'A': 7} |
| clean|push|random|16|4.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|16|8.0|r|None | 60 | 78% [66, 87] | 0.66 | {'b': 47, 'A': 9, 'other': 4} |
| clean|push|random|16|8.0|r|None | 60 | 2% [0, 9] | 0.03 | {'A': 59, 'b': 1} |
| clean|push|lens|16|8.0|a|None | 60 | 40% [29, 53] | 1.08 | {'b': 24, 'other': 36} |
| clean|push|random|16|8.0|a|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|lens|16|8.0|b|None | 60 | 100% [94, 100] | 1.06 | {'b': 60} |
| clean|push|random|16|8.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|16|16.0|r|None | 60 | 85% [74, 92] | 0.81 | {'b': 51, 'A': 6, 'other': 3} |
| clean|push|random|16|16.0|r|None | 60 | 2% [0, 9] | 0.19 | {'A': 59, 'b': 1} |
| clean|push|lens|16|16.0|a|None | 60 | 0% [-0, 6] | 0.87 | {'other': 60} |
| clean|push|random|16|16.0|a|None | 60 | 0% [-0, 6] | 0.12 | {'other': 14, 'A': 46} |
| clean|push|lens|16|16.0|b|None | 60 | 97% [89, 99] | 1.03 | {'b': 58, 'other': 2} |
| clean|push|random|16|16.0|b|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|20|4.0|r|None | 60 | 22% [13, 34] | 0.37 | {'b': 13, 'A': 45, 'other': 2} |
| clean|push|random|20|4.0|r|None | 60 | 2% [0, 9] | 0.03 | {'A': 59, 'b': 1} |
| clean|push|lens|20|4.0|a|None | 60 | 98% [91, 100] | 0.99 | {'b': 59, 'other': 1} |
| clean|push|random|20|4.0|a|None | 60 | 0% [-0, 6] | 0.03 | {'A': 59, 'other': 1} |
| clean|push|lens|20|4.0|b|None | 60 | 95% [86, 98] | 0.93 | {'b': 57, 'A': 2, 'other': 1} |
| clean|push|random|20|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|8.0|r|None | 60 | 48% [36, 61] | 0.47 | {'b': 29, 'A': 31} |
| clean|push|random|20|8.0|r|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|lens|20|8.0|a|None | 60 | 85% [74, 92] | 1.09 | {'b': 51, 'other': 9} |
| clean|push|random|20|8.0|a|None | 60 | 0% [-0, 6] | 0.06 | {'A': 58, 'other': 2} |
| clean|push|lens|20|8.0|b|None | 60 | 100% [94, 100] | 1.06 | {'b': 60} |
| clean|push|random|20|8.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|20|16.0|r|None | 60 | 72% [59, 81] | 0.70 | {'b': 43, 'other': 4, 'A': 13} |
| clean|push|random|20|16.0|r|None | 60 | 0% [-0, 6] | 0.22 | {'A': 57, 'other': 3} |
| clean|push|lens|20|16.0|a|None | 60 | 12% [6, 22] | 1.04 | {'other': 53, 'b': 7} |
| clean|push|random|20|16.0|a|None | 60 | 0% [-0, 6] | 0.20 | {'other': 35, 'A': 25} |
| clean|push|lens|20|16.0|b|None | 60 | 100% [94, 100] | 1.06 | {'b': 60} |
| clean|push|random|20|16.0|b|None | 60 | 0% [-0, 6] | 0.10 | {'A': 57, 'other': 3} |
| clean|push|lens|24|4.0|r|None | 60 | 55% [42, 67] | 0.54 | {'b': 33, 'A': 21, 'other': 6} |
| clean|push|random|24|4.0|r|None | 60 | 0% [-0, 6] | 0.04 | {'A': 59, 'other': 1} |
| clean|push|lens|24|4.0|a|None | 60 | 100% [94, 100] | 1.10 | {'b': 60} |
| clean|push|random|24|4.0|a|None | 60 | 2% [0, 9] | 0.03 | {'A': 59, 'b': 1} |
| clean|push|lens|24|4.0|b|None | 60 | 100% [94, 100] | 1.01 | {'b': 60} |
| clean|push|random|24|4.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|24|8.0|r|None | 60 | 85% [74, 92] | 0.75 | {'b': 51, 'A': 7, 'other': 2} |
| clean|push|random|24|8.0|r|None | 60 | 0% [-0, 6] | 0.13 | {'A': 57, 'other': 3} |
| clean|push|lens|24|8.0|a|None | 60 | 77% [65, 86] | 1.10 | {'b': 46, 'other': 14} |
| clean|push|random|24|8.0|a|None | 60 | 0% [-0, 6] | 0.12 | {'A': 58, 'other': 2} |
| clean|push|lens|24|8.0|b|None | 60 | 100% [94, 100] | 1.05 | {'b': 60} |
| clean|push|random|24|8.0|b|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|lens|24|16.0|r|None | 60 | 95% [86, 98] | 0.83 | {'b': 57, 'other': 2, 'A': 1} |
| clean|push|random|24|16.0|r|None | 60 | 0% [-0, 6] | 0.28 | {'A': 57, 'other': 3} |
| clean|push|lens|24|16.0|a|None | 60 | 3% [1, 11] | 0.98 | {'other': 58, 'b': 2} |
| clean|push|random|24|16.0|a|None | 60 | 0% [-0, 6] | 0.32 | {'other': 50, 'A': 10} |
| clean|push|lens|24|16.0|b|None | 60 | 95% [86, 98] | 1.01 | {'b': 57, 'other': 3} |
| clean|push|random|24|16.0|b|None | 60 | 0% [-0, 6] | 0.21 | {'A': 54, 'other': 6} |
| clean|push|lens|28|4.0|r|None | 60 | 83% [72, 91] | 0.79 | {'b': 50, 'A': 3, 'other': 7} |
| clean|push|random|28|4.0|r|None | 60 | 0% [-0, 6] | 0.08 | {'A': 60} |
| clean|push|lens|28|4.0|a|None | 60 | 95% [86, 98] | 1.14 | {'b': 57, 'other': 3} |
| clean|push|random|28|4.0|a|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|28|4.0|b|None | 60 | 95% [86, 98] | 0.88 | {'b': 57, 'A': 2, 'other': 1} |
| clean|push|random|28|4.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|28|8.0|r|None | 60 | 83% [72, 91] | 0.90 | {'b': 50, 'other': 10} |
| clean|push|random|28|8.0|r|None | 60 | 0% [-0, 6] | 0.20 | {'A': 59, 'other': 1} |
| clean|push|lens|28|8.0|a|None | 60 | 63% [51, 74] | 1.21 | {'b': 38, 'other': 22} |
| clean|push|random|28|8.0|a|None | 60 | 0% [-0, 6] | 0.14 | {'A': 54, 'other': 6} |
| clean|push|lens|28|8.0|b|None | 60 | 100% [94, 100] | 1.04 | {'b': 60} |
| clean|push|random|28|8.0|b|None | 60 | 0% [-0, 6] | 0.09 | {'A': 60} |
| clean|push|lens|28|16.0|r|None | 60 | 53% [41, 65] | 0.64 | {'other': 15, 'A': 11, 'oc': 2, 'b': 32} |
| clean|push|random|28|16.0|r|None | 60 | 5% [2, 14] | 0.35 | {'A': 53, 'b': 3, 'other': 4} |
| clean|push|lens|28|16.0|a|None | 60 | 0% [-0, 6] | 1.07 | {'other': 60} |
| clean|push|random|28|16.0|a|None | 60 | 0% [-0, 6] | 0.33 | {'other': 52, 'A': 8} |
| clean|push|lens|28|16.0|b|None | 60 | 95% [86, 98] | 1.00 | {'b': 57, 'other': 3} |
| clean|push|random|28|16.0|b|None | 60 | 0% [-0, 6] | 0.24 | {'A': 53, 'other': 7} |
| clean|push|lens|band|4.0|r|None | 60 | 97% [89, 99] | 1.06 | {'b': 58, 'other': 2} |
| clean|push|random|band|4.0|r|None | 60 | 0% [-0, 6] | 0.12 | {'A': 59, 'other': 1} |
| clean|push|lens|band|4.0|a|None | 60 | 40% [29, 53] | 1.18 | {'other': 36, 'b': 24} |
| clean|push|random|band|4.0|a|None | 60 | 0% [-0, 6] | 0.09 | {'A': 58, 'other': 2} |
| clean|push|lens|band|4.0|b|None | 60 | 100% [94, 100] | 1.10 | {'b': 60} |
| clean|push|random|band|4.0|b|None | 60 | 2% [0, 9] | 0.03 | {'A': 59, 'b': 1} |
| clean|push|lens|band|8.0|r|None | 60 | 85% [74, 92] | 0.92 | {'b': 51, 'A': 3, 'other': 6} |
| clean|push|random|band|8.0|r|None | 60 | 3% [1, 11] | 0.32 | {'A': 56, 'other': 2, 'b': 2} |
| clean|push|lens|band|8.0|a|None | 60 | 0% [-0, 6] | 0.91 | {'other': 60} |
| clean|push|random|band|8.0|a|None | 60 | 0% [-0, 6] | 0.27 | {'other': 49, 'A': 11} |
| clean|push|lens|band|8.0|b|None | 60 | 92% [82, 96] | 1.08 | {'b': 55, 'other': 5} |
| clean|push|random|band|8.0|b|None | 60 | 0% [-0, 6] | 0.17 | {'A': 57, 'other': 3} |
| clean|push|lens|band|16.0|r|None | 60 | 8% [4, 18] | 0.55 | {'other': 55, 'b': 5} |
| clean|push|random|band|16.0|r|None | 60 | 10% [5, 20] | 0.40 | {'A': 39, 'b': 6, 'oc': 6, 'other': 9} |
| clean|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | 1.09 | {'other': 60} |
| clean|push|random|band|16.0|a|None | 60 | 0% [-0, 6] | 0.46 | {'other': 60} |
| clean|push|lens|band|16.0|b|None | 60 | 93% [84, 97] | 1.06 | {'b': 56, 'other': 3, 'oc': 1} |
| clean|push|random|band|16.0|b|None | 60 | 5% [2, 14] | 0.39 | {'other': 29, 'A': 25, 'oc': 3, 'b': 3} |
| clean|emb_diff|lens|-1|1.0|b|None | 60 | 88% [78, 94] | 0.85 | {'b': 53, 'other': 7} |
| clean|emb_diff|random|-1|1.0|b|None | 60 | 3% [1, 11] | 0.07 | {'A': 58, 'b': 2} |
| clean|emb_add|lens|-1|1.0|b|None | 60 | 88% [78, 94] | 0.81 | {'b': 53, 'other': 7} |
| clean|emb_add|random|-1|1.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|emb_diff|lens|-1|4.0|b|None | 60 | 83% [72, 91] | 0.76 | {'b': 50, 'oc': 2, 'other': 8} |
| clean|emb_diff|random|-1|4.0|b|None | 60 | 20% [12, 32] | 0.50 | {'oc': 17, 'A': 12, 'b': 12, 'other': 19} |
| clean|emb_add|lens|-1|4.0|b|None | 60 | 100% [94, 100] | 1.10 | {'b': 60} |
| clean|emb_add|random|-1|4.0|b|None | 60 | 15% [8, 26] | 0.51 | {'b': 9, 'other': 31, 'A': 12, 'oc': 8} |
| clean|copy|None|16|None|r|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|copy|None|20|None|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|copy|None|24|None|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|copy|None|28|None|r|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|copy|None|32|None|r|None | 60 | 2% [0, 9] | 0.10 | {'A': 59, 'b': 1} |
| clean|copy|None|36|None|r|None | 60 | 62% [49, 73] | 0.54 | {'b': 37, 'A': 22, 'other': 1} |
| clean|copy|None|40|None|r|None | 60 | 90% [80, 95] | 0.67 | {'b': 54, 'A': 6} |
| clean|copy|None|44|None|r|None | 60 | 98% [91, 100] | 0.75 | {'b': 59, 'A': 1} |
| clean|copy|None|48|None|r|None | 60 | 100% [94, 100] | 0.81 | {'b': 60} |
| clean|patch|None|16|None|a|None | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|patch|None|16|4.0|a|None | 60 | 2% [0, 9] | 0.07 | {'A': 58, 'b': 1, 'other': 1} |
| clean|patch|None|16|8.0|a|None | 60 | 93% [84, 97] | 0.94 | {'b': 56, 'A': 1, 'other': 3} |
| clean|patch|None|16|16.0|a|None | 60 | 72% [59, 81] | 0.98 | {'b': 43, 'other': 17} |
| clean|patch|None|20|None|a|None | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|patch|None|20|4.0|a|None | 60 | 12% [6, 22] | 0.25 | {'b': 7, 'A': 53} |
| clean|patch|None|20|8.0|a|None | 60 | 98% [91, 100] | 0.94 | {'b': 59, 'other': 1} |
| clean|patch|None|20|16.0|a|None | 60 | 45% [33, 58] | 0.94 | {'other': 33, 'b': 27} |
| clean|patch|None|24|None|a|None | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|patch|None|24|4.0|a|None | 60 | 32% [21, 44] | 0.44 | {'b': 19, 'A': 34, 'other': 7} |
| clean|patch|None|24|8.0|a|None | 60 | 93% [84, 97] | 0.94 | {'b': 56, 'other': 4} |
| clean|patch|None|24|16.0|a|None | 60 | 18% [11, 30] | 0.93 | {'other': 49, 'b': 11} |
| clean|patch|None|28|None|a|None | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|patch|None|28|4.0|a|None | 60 | 63% [51, 74] | 0.64 | {'b': 38, 'A': 19, 'other': 3} |
| clean|patch|None|28|8.0|a|None | 60 | 92% [82, 96] | 0.93 | {'b': 55, 'other': 5} |
| clean|patch|None|28|16.0|a|None | 60 | 17% [9, 28] | 0.91 | {'other': 50, 'b': 10} |
| off|push|lens|16|4.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 53, 'A': 5, 'oc': 1, 'other': 1} |
| off|push|lens|16|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 24, 'other': 36} |
| off|push|lens|16|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |
| off|push|lens|20|4.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 58, 'other': 1, 'A': 1} |
| off|push|lens|20|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 51, 'other': 9} |
| off|push|lens|20|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 54, 'bO': 6} |
| off|push|lens|24|4.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 60} |
| off|push|lens|24|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 46, 'other': 14} |
| off|push|lens|24|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 57, 'bO': 3} |
| off|push|lens|28|4.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 59, 'other': 1} |
| off|push|lens|28|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 40, 'other': 20} |
| off|push|lens|28|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |
| off|push|lens|band|4.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 36, 'bO': 24} |
| off|push|lens|band|8.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |
| off|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +1.00 [+1.00, +1.00] (ref rate 1.00); E-insert: k -, J +0.90 [+0.82, +0.97] (ref rate 0.90); E-cue: k -, J +1.00 [+1.00, +1.00] (ref rate 1.00); E-unrelated: k -, J +0.00 [+0.00, +0.00] (ref rate 0.00); W-copy*: k -, J +0.62 [+0.50, +0.73] (ref rate 0.62); emb*: k -, J +0.88 [+0.80, +0.97] (ref rate 0.88); patch_matched: k -, J +0.32 [+0.20, +0.43] (ref rate 0.32); low_margin: k -
K1 - -> untestable; gate +0.88 [+0.51, +1.15]; K2 nb - a/2 -0.38 [-0.45, -0.30], b - nb +0.88 [+0.80, +0.95] -> write; K4 -0.25 [-0.28, -0.23]
JS(P*, .) {"clean": 0.603, "E-name": 0.016, "E-insert": 0.163, "E-cue": 0.02, "E-unrelated": 0.597}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [0.1036, 0.1903, 0.2329, 0.3668], "E-insert": [0.1064, 0.1867, 0.1894, 0.2766], "E-cue": [0.3337, 0.4691, 0.5644, 0.6566], "E-unrelated": [0.1369, 0.0478, 0.0702, 0.1184]}
transit proj on C's delta [44, 48, 52]: P*_b [0.6215, 0.629, 0.6844], P* [0.5791, 0.5832, 0.6544], edits {"E-name": [0.6379, 0.6283, 0.6736], "E-insert": [0.5753, 0.5557, 0.5598], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.2772, 0.2953, 0.2654]}

## B (W-copy* = ('clean', 'copy', None, 40, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|edit|None|None|None|None|E-name | 60 | 100% [94, 100] | 1.01 | {'b': 60} |
| clean|edit|None|None|None|None|E-insert | 60 | 92% [82, 96] | 0.55 | {'b': 55, 'A': 5} |
| clean|edit|None|None|None|None|E-cue | 60 | 100% [94, 100] | 1.00 | {'b': 60} |
| clean|edit|None|None|None|None|E-unrelated | 60 | 0% [-0, 6] | 0.08 | {'A': 60} |
| clean|push|lens|16|4.0|r|None | 60 | 13% [7, 24] | 0.26 | {'other': 12, 'b': 8, 'A': 40} |
| clean|push|random|16|4.0|r|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|16|4.0|a|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|random|16|4.0|a|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|16|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|random|16|4.0|b|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|16|8.0|r|None | 60 | 38% [27, 51] | 0.54 | {'b': 23, 'A': 22, 'other': 15} |
| clean|push|random|16|8.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|16|8.0|a|None | 60 | 0% [-0, 6] | 0.11 | {'A': 59, 'other': 1} |
| clean|push|random|16|8.0|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|16|8.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|random|16|8.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|16|16.0|r|None | 60 | 82% [70, 89] | 0.76 | {'b': 49, 'other': 7, 'A': 4} |
| clean|push|random|16|16.0|r|None | 60 | 0% [-0, 6] | 0.10 | {'A': 59, 'oc': 1} |
| clean|push|lens|16|16.0|a|None | 60 | 3% [1, 11] | 0.41 | {'b': 2, 'other': 35, 'A': 23} |
| clean|push|random|16|16.0|a|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|push|lens|16|16.0|b|None | 60 | 10% [5, 20] | 0.25 | {'other': 12, 'b': 6, 'A': 42} |
| clean|push|random|16|16.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|4.0|r|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|random|20|4.0|r|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|4.0|a|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|random|20|4.0|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|20|4.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|random|20|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|8.0|r|None | 60 | 5% [2, 14] | 0.21 | {'A': 57, 'b': 3} |
| clean|push|random|20|8.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|20|8.0|a|None | 60 | 0% [-0, 6] | 0.14 | {'A': 60} |
| clean|push|random|20|8.0|a|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|20|8.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|random|20|8.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|20|16.0|r|None | 60 | 37% [26, 49] | 0.50 | {'other': 3, 'b': 22, 'A': 35} |
| clean|push|random|20|16.0|r|None | 60 | 0% [-0, 6] | 0.10 | {'A': 60} |
| clean|push|lens|20|16.0|a|None | 60 | 0% [-0, 6] | 0.22 | {'A': 58, 'other': 2} |
| clean|push|random|20|16.0|a|None | 60 | 0% [-0, 6] | 0.08 | {'A': 60} |
| clean|push|lens|20|16.0|b|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|push|random|20|16.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|24|4.0|r|None | 60 | 0% [-0, 6] | 0.20 | {'A': 60} |
| clean|push|random|24|4.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|24|4.0|a|None | 60 | 0% [-0, 6] | 0.10 | {'A': 60} |
| clean|push|random|24|4.0|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|24|4.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|random|24|4.0|b|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|push|lens|24|8.0|r|None | 60 | 12% [6, 22] | 0.38 | {'A': 51, 'other': 2, 'b': 7} |
| clean|push|random|24|8.0|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|24|8.0|a|None | 60 | 0% [-0, 6] | 0.24 | {'A': 60} |
| clean|push|random|24|8.0|a|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|lens|24|8.0|b|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|random|24|8.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|24|16.0|r|None | 60 | 72% [59, 81] | 0.66 | {'b': 43, 'other': 2, 'A': 15} |
| clean|push|random|24|16.0|r|None | 60 | 0% [-0, 6] | 0.14 | {'A': 60} |
| clean|push|lens|24|16.0|a|None | 60 | 5% [2, 14] | 0.35 | {'A': 47, 'other': 10, 'b': 3} |
| clean|push|random|24|16.0|a|None | 60 | 0% [-0, 6] | 0.09 | {'A': 60} |
| clean|push|lens|24|16.0|b|None | 60 | 0% [-0, 6] | 0.19 | {'A': 60} |
| clean|push|random|24|16.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|28|4.0|r|None | 60 | 17% [9, 28] | 0.37 | {'A': 50, 'b': 10} |
| clean|push|random|28|4.0|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|28|4.0|a|None | 60 | 0% [-0, 6] | 0.18 | {'A': 60} |
| clean|push|random|28|4.0|a|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|28|4.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|random|28|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|28|8.0|r|None | 60 | 67% [54, 77] | 0.63 | {'b': 40, 'A': 18, 'other': 2} |
| clean|push|random|28|8.0|r|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|lens|28|8.0|a|None | 60 | 22% [13, 34] | 0.40 | {'b': 13, 'A': 43, 'other': 4} |
| clean|push|random|28|8.0|a|None | 60 | 0% [-0, 6] | 0.05 | {'A': 60} |
| clean|push|lens|28|8.0|b|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|push|random|28|8.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|28|16.0|r|None | 60 | 83% [72, 91] | 0.90 | {'b': 50, 'other': 6, 'oc': 1, 'A': 3} |
| clean|push|random|28|16.0|r|None | 60 | 2% [0, 9] | 0.23 | {'A': 57, 'b': 1, 'oc': 2} |
| clean|push|lens|28|16.0|a|None | 60 | 58% [46, 70] | 0.71 | {'b': 35, 'other': 18, 'A': 7} |
| clean|push|random|28|16.0|a|None | 60 | 0% [-0, 6] | 0.10 | {'A': 59, 'other': 1} |
| clean|push|lens|28|16.0|b|None | 60 | 3% [1, 11] | 0.20 | {'A': 57, 'other': 1, 'b': 2} |
| clean|push|random|28|16.0|b|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|band|4.0|r|None | 60 | 67% [54, 77] | 0.83 | {'b': 40, 'other': 8, 'A': 12} |
| clean|push|random|band|4.0|r|None | 60 | 0% [-0, 6] | 0.02 | {'A': 60} |
| clean|push|lens|band|4.0|a|None | 60 | 18% [11, 30] | 0.44 | {'b': 11, 'A': 48, 'other': 1} |
| clean|push|random|band|4.0|a|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|push|lens|band|4.0|b|None | 60 | 0% [-0, 6] | 0.14 | {'A': 60} |
| clean|push|random|band|4.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|push|lens|band|8.0|r|None | 60 | 90% [80, 95] | 1.03 | {'b': 54, 'other': 6} |
| clean|push|random|band|8.0|r|None | 60 | 0% [-0, 6] | 0.17 | {'A': 59, 'oc': 1} |
| clean|push|lens|band|8.0|a|None | 60 | 38% [27, 51] | 0.77 | {'other': 31, 'b': 23, 'A': 6} |
| clean|push|random|band|8.0|a|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|push|lens|band|8.0|b|None | 60 | 47% [35, 59] | 0.54 | {'b': 28, 'other': 6, 'A': 26} |
| clean|push|random|band|8.0|b|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|push|lens|band|16.0|r|None | 60 | 35% [24, 48] | 0.96 | {'other': 39, 'b': 21} |
| clean|push|random|band|16.0|r|None | 60 | 7% [3, 16] | 0.38 | {'A': 38, 'other': 13, 'b': 4, 'oc': 5} |
| clean|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | 0.89 | {'other': 60} |
| clean|push|random|band|16.0|a|None | 60 | 0% [-0, 6] | 0.19 | {'A': 26, 'other': 34} |
| clean|push|lens|band|16.0|b|None | 60 | 88% [78, 94] | 0.91 | {'b': 53, 'other': 5, 'A': 2} |
| clean|push|random|band|16.0|b|None | 60 | 0% [-0, 6] | 0.07 | {'A': 60} |
| clean|emb_diff|lens|-1|1.0|b|None | 60 | 22% [13, 34] | 0.24 | {'A': 47, 'b': 13} |
| clean|emb_diff|random|-1|1.0|b|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|emb_add|lens|-1|1.0|b|None | 60 | 50% [38, 62] | 0.41 | {'A': 29, 'b': 30, 'other': 1} |
| clean|emb_add|random|-1|1.0|b|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|emb_diff|lens|-1|4.0|b|None | 60 | 95% [86, 98] | 0.78 | {'b': 57, 'other': 3} |
| clean|emb_diff|random|-1|4.0|b|None | 60 | 23% [14, 35] | 0.52 | {'other': 20, 'oc': 12, 'b': 14, 'A': 14} |
| clean|emb_add|lens|-1|4.0|b|None | 60 | 100% [94, 100] | 0.98 | {'b': 60} |
| clean|emb_add|random|-1|4.0|b|None | 60 | 32% [21, 44] | 0.51 | {'other': 21, 'b': 19, 'A': 11, 'oc': 9} |
| clean|copy|None|16|None|r|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|copy|None|20|None|r|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|copy|None|24|None|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|copy|None|28|None|r|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|copy|None|32|None|r|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|copy|None|36|None|r|None | 60 | 10% [5, 20] | 0.23 | {'A': 54, 'b': 6} |
| clean|copy|None|40|None|r|None | 60 | 82% [70, 89] | 0.64 | {'b': 49, 'A': 11} |
| clean|copy|None|44|None|r|None | 60 | 90% [80, 95] | 0.67 | {'b': 54, 'A': 6} |
| clean|copy|None|48|None|r|None | 60 | 93% [84, 97] | 0.70 | {'b': 56, 'A': 4} |
| clean|patch|None|16|None|a|None | 60 | 0% [-0, 6] | -0.00 | {'A': 60} |
| clean|patch|None|16|4.0|a|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|patch|None|16|8.0|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|patch|None|16|16.0|a|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|patch|None|20|None|a|None | 60 | 0% [-0, 6] | 0.00 | {'A': 60} |
| clean|patch|None|20|4.0|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|patch|None|20|8.0|a|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|patch|None|20|16.0|a|None | 60 | 0% [-0, 6] | 0.08 | {'A': 59, 'other': 1} |
| clean|patch|None|24|None|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|patch|None|24|4.0|a|None | 60 | 0% [-0, 6] | 0.03 | {'A': 60} |
| clean|patch|None|24|8.0|a|None | 60 | 0% [-0, 6] | 0.08 | {'A': 60} |
| clean|patch|None|24|16.0|a|None | 60 | 7% [3, 16] | 0.24 | {'A': 52, 'b': 4, 'other': 4} |
| clean|patch|None|28|None|a|None | 60 | 0% [-0, 6] | 0.01 | {'A': 60} |
| clean|patch|None|28|4.0|a|None | 60 | 0% [-0, 6] | 0.04 | {'A': 60} |
| clean|patch|None|28|8.0|a|None | 60 | 7% [3, 16] | 0.20 | {'A': 56, 'b': 4} |
| clean|patch|None|28|16.0|a|None | 60 | 33% [23, 46] | 0.49 | {'A': 31, 'other': 8, 'b': 20, 'oc': 1} |
| off|push|lens|16|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|16|8.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 59, 'other': 1} |
| off|push|lens|16|16.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 2, 'other': 35, 'A': 23} |
| off|push|lens|20|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|20|8.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|20|16.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 58, 'other': 2} |
| off|push|lens|24|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|24|8.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|24|16.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 47, 'other': 10, 'bO': 3} |
| off|push|lens|28|4.0|a|None | 60 | 0% [-0, 6] | nan | {'A': 60} |
| off|push|lens|28|8.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 17, 'A': 38, 'other': 5} |
| off|push|lens|28|16.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 32, 'other': 20, 'A': 8} |
| off|push|lens|band|4.0|a|None | 60 | 0% [-0, 6] | nan | {'bO': 16, 'A': 43, 'other': 1} |
| off|push|lens|band|8.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 31, 'bO': 21, 'A': 8} |
| off|push|lens|band|16.0|a|None | 60 | 0% [-0, 6] | nan | {'other': 60} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-insert: k -, J +0.00 [+0.00, +0.00] (ref rate 0.92); E-cue: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-unrelated: k -, J - (ref rate 0.00); W-copy*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.82); emb*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.50); patch_matched: k -, J - (ref rate 0.00); low_margin: k -
K1 - -> untestable; gate +0.07 [-0.12, +0.24]; K2 nb - a/2 +0.00 [+0.00, +0.00], b - nb +0.00 [+0.00, +0.00] -> inconclusive; K4 -0.24 [-0.26, -0.22]
JS(P*, .) {"clean": 0.009, "E-name": 0.635, "E-insert": 0.369, "E-cue": 0.633, "E-unrelated": 0.014}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [-0.0123, -0.0644, -0.0573, 0.0066], "E-insert": [0.1218, 0.1648, 0.1567, 0.1548], "E-cue": [0.2279, 0.1735, 0.1422, 0.1601], "E-unrelated": [0.1462, 0.1574, 0.1493, 0.1585]}
transit proj on C's delta [44, 48, 52]: P*_b [0.04, 0.065, 0.0725], P* [0.0814, 0.0945, 0.1139], edits {"E-name": [0.6586, 0.6432, 0.7493], "E-insert": [0.6244, 0.6075, 0.6345], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.2473, 0.2493, 0.2257]}

## Plain-text loss under the push (nats)

{"none": 2.3307, "lens/16/x4": 2.36, "random/16/x4": 2.3346, "lens/16/x8": 2.5891, "random/16/x8": 2.3577, "lens/16/x16": 5.3065, "random/16/x16": 2.4952, "lens/20/x4": 2.3527, "random/20/x4": 2.3353, "lens/20/x8": 2.4987, "random/20/x8": 2.3654, "lens/20/x16": 3.3688, "random/20/x16": 2.5345, "lens/24/x4": 2.4007, "random/24/x4": 2.3369, "lens/24/x8": 2.6509, "random/24/x8": 2.3725, "lens/24/x16": 3.4117, "random/24/x16": 2.6688, "lens/28/x4": 2.4167, "random/28/x4": 2.3474, "lens/28/x8": 2.7787, "random/28/x8": 2.4245, "lens/28/x16": 4.4191, "random/28/x16": 2.842, "lens/band/x4": 3.3257, "random/band/x4": 2.3838, "lens/band/x8": 6.7324, "random/band/x8": 2.6544, "lens/band/x16": 10.558, "random/band/x16": 5.2692}

## Diagnostics

{"max_none_vs_clean_logit": 0.9375, "max_zero_scale_vs_none_logit": null, "n_zero_scale": 0}
