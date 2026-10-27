# early_push

P* = ('clean', 'push', 'lens', 24, 16.0, 'a', None); emb* = ('clean', 'emb_add', 'lens', -1, 1.0, 'b', None)

Verdict (manifest rule): **mixed**; calls (K1 RL, K2 RL, K3) ['gate failed', 'inconclusive', 'inconclusive']; K3 BL - RL flips -0.50 [-1.00, +0.00]

## BL (W-copy* = ('clean', 'copy', None, 32, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|edit|None|None|None|None|E-name | 4 | 100% [51, 100] | 1.04 | {'b': 4} |
| clean|edit|None|None|None|None|E-insert | 4 | 0% [0, 49] | 0.44 | {'A': 4} |
| clean|edit|None|None|None|None|E-head | 4 | 50% [15, 85] | 0.54 | {'A': 2, 'b': 2} |
| clean|edit|None|None|None|None|E-cue | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|edit|None|None|None|None|E-unrelated | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|16|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|16|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|16|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|16|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|4.0|r|None | 4 | 0% [0, 49] | 0.16 | {'A': 4} |
| clean|push|random|16|4.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|4.0|a|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|random|16|4.0|a|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|16|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|16|4.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|8.0|r|None | 4 | 75% [30, 95] | 0.41 | {'b': 3, 'A': 1} |
| clean|push|random|16|8.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|8.0|a|None | 4 | 0% [0, 49] | 0.21 | {'A': 4} |
| clean|push|random|16|8.0|a|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|lens|16|8.0|b|None | 4 | 0% [0, 49] | 0.15 | {'A': 4} |
| clean|push|random|16|8.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|16.0|r|None | 4 | 75% [30, 95] | 0.70 | {'b': 3, 'A': 1} |
| clean|push|random|16|16.0|r|None | 4 | 25% [5, 70] | 0.26 | {'b': 1, 'A': 3} |
| clean|push|lens|16|16.0|a|None | 4 | 25% [5, 70] | 0.61 | {'other': 3, 'b': 1} |
| clean|push|random|16|16.0|a|None | 4 | 0% [0, 49] | 0.14 | {'A': 4} |
| clean|push|lens|16|16.0|b|None | 4 | 75% [30, 95] | 0.63 | {'b': 3, 'A': 1} |
| clean|push|random|16|16.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|20|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|20|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|20|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|4.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|20|4.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|4.0|a|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|random|20|4.0|a|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|lens|20|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|20|4.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|8.0|r|None | 4 | 0% [0, 49] | 0.11 | {'A': 4} |
| clean|push|random|20|8.0|r|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|20|8.0|a|None | 4 | 0% [0, 49] | 0.17 | {'A': 4} |
| clean|push|random|20|8.0|a|None | 4 | 0% [0, 49] | 0.13 | {'A': 4} |
| clean|push|lens|20|8.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|random|20|8.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|16.0|r|None | 4 | 50% [15, 85] | 0.47 | {'A': 2, 'b': 2} |
| clean|push|random|20|16.0|r|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|20|16.0|a|None | 4 | 0% [0, 49] | 0.32 | {'A': 3, 'other': 1} |
| clean|push|random|20|16.0|a|None | 4 | 0% [0, 49] | 0.18 | {'A': 4} |
| clean|push|lens|20|16.0|b|None | 4 | 50% [15, 85] | 0.27 | {'A': 2, 'b': 2} |
| clean|push|random|20|16.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|24|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|24|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|24|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|4.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|24|4.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|4.0|a|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|push|random|24|4.0|a|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|24|4.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|random|24|4.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|8.0|r|None | 4 | 0% [0, 49] | 0.08 | {'A': 4} |
| clean|push|random|24|8.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|8.0|a|None | 4 | 0% [0, 49] | 0.19 | {'A': 4} |
| clean|push|random|24|8.0|a|None | 4 | 0% [0, 49] | 0.15 | {'A': 4} |
| clean|push|lens|24|8.0|b|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|push|random|24|8.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|16.0|r|None | 4 | 50% [15, 85] | 0.52 | {'b': 2, 'A': 2} |
| clean|push|random|24|16.0|r|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|push|lens|24|16.0|a|None | 4 | 0% [0, 49] | 0.41 | {'A': 2, 'other': 2} |
| clean|push|random|24|16.0|a|None | 4 | 0% [0, 49] | 0.23 | {'A': 4} |
| clean|push|lens|24|16.0|b|None | 4 | 50% [15, 85] | 0.57 | {'b': 2, 'A': 2} |
| clean|push|random|24|16.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|28|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|28|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|28|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|28|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|4.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|28|4.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|4.0|a|None | 4 | 0% [0, 49] | 0.13 | {'A': 4} |
| clean|push|random|28|4.0|a|None | 4 | 0% [0, 49] | 0.11 | {'A': 4} |
| clean|push|lens|28|4.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|random|28|4.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|8.0|r|None | 4 | 0% [0, 49] | 0.14 | {'A': 4} |
| clean|push|random|28|8.0|r|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|push|lens|28|8.0|a|None | 4 | 0% [0, 49] | 0.30 | {'A': 4} |
| clean|push|random|28|8.0|a|None | 4 | 0% [0, 49] | 0.16 | {'A': 4} |
| clean|push|lens|28|8.0|b|None | 4 | 0% [0, 49] | 0.13 | {'A': 4} |
| clean|push|random|28|8.0|b|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|28|16.0|r|None | 4 | 75% [30, 95] | 0.58 | {'b': 3, 'A': 1} |
| clean|push|random|28|16.0|r|None | 4 | 0% [0, 49] | 0.26 | {'A': 4} |
| clean|push|lens|28|16.0|a|None | 4 | 25% [5, 70] | 0.46 | {'A': 2, 'other': 1, 'b': 1} |
| clean|push|random|28|16.0|a|None | 4 | 0% [0, 49] | 0.36 | {'A': 3, 'other': 1} |
| clean|push|lens|28|16.0|b|None | 4 | 50% [15, 85] | 0.51 | {'A': 2, 'b': 2} |
| clean|push|random|28|16.0|b|None | 4 | 0% [0, 49] | 0.32 | {'A': 4} |
| clean|push|lens|band|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|band|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|band|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|band|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|band|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|band|4.0|r|None | 4 | 75% [30, 95] | 0.54 | {'b': 3, 'A': 1} |
| clean|push|random|band|4.0|r|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|band|4.0|a|None | 4 | 0% [0, 49] | 0.48 | {'A': 3, 'other': 1} |
| clean|push|random|band|4.0|a|None | 4 | 0% [0, 49] | 0.16 | {'A': 4} |
| clean|push|lens|band|4.0|b|None | 4 | 50% [15, 85] | 0.48 | {'A': 2, 'b': 2} |
| clean|push|random|band|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|band|8.0|r|None | 4 | 75% [30, 95] | 0.70 | {'b': 3, 'A': 1} |
| clean|push|random|band|8.0|r|None | 4 | 0% [0, 49] | 0.08 | {'A': 4} |
| clean|push|lens|band|8.0|a|None | 4 | 0% [0, 49] | 0.61 | {'other': 4} |
| clean|push|random|band|8.0|a|None | 4 | 0% [0, 49] | 0.22 | {'A': 3, 'other': 1} |
| clean|push|lens|band|8.0|b|None | 4 | 100% [51, 100] | 0.73 | {'b': 4} |
| clean|push|random|band|8.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|band|16.0|r|None | 4 | 75% [30, 95] | 0.65 | {'b': 3, 'A': 1} |
| clean|push|random|band|16.0|r|None | 4 | 0% [0, 49] | 0.37 | {'A': 4} |
| clean|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | 0.57 | {'other': 4} |
| clean|push|random|band|16.0|a|None | 4 | 0% [0, 49] | 0.49 | {'other': 4} |
| clean|push|lens|band|16.0|b|None | 4 | 100% [51, 100] | 0.82 | {'b': 4} |
| clean|push|random|band|16.0|b|None | 4 | 0% [0, 49] | 0.36 | {'A': 4} |
| clean|emb_diff|lens|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_diff|random|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_add|lens|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_add|random|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_diff|lens|-1|1.0|b|None | 4 | 50% [15, 85] | 0.38 | {'A': 2, 'b': 2} |
| clean|emb_diff|random|-1|1.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_add|lens|-1|1.0|b|None | 4 | 50% [15, 85] | 0.37 | {'A': 2, 'b': 2} |
| clean|emb_add|random|-1|1.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_diff|lens|-1|4.0|b|None | 4 | 100% [51, 100] | 0.70 | {'b': 4} |
| clean|emb_diff|random|-1|4.0|b|None | 4 | 25% [5, 70] | 0.52 | {'A': 3, 'b': 1} |
| clean|emb_add|lens|-1|4.0|b|None | 4 | 100% [51, 100] | 0.95 | {'b': 4} |
| clean|emb_add|random|-1|4.0|b|None | 4 | 25% [5, 70] | 0.53 | {'A': 3, 'b': 1} |
| clean|copy|None|16|None|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|copy|None|20|None|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|copy|None|24|None|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|copy|None|28|None|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|copy|None|32|None|r|None | 4 | 50% [15, 85] | 0.30 | {'A': 2, 'b': 2} |
| clean|copy|None|36|None|r|None | 4 | 0% [0, 49] | 0.15 | {'A': 4} |
| clean|copy|None|40|None|r|None | 4 | 0% [0, 49] | 0.17 | {'A': 4} |
| clean|copy|None|44|None|r|None | 4 | 0% [0, 49] | 0.18 | {'A': 4} |
| clean|copy|None|48|None|r|None | 4 | 0% [0, 49] | 0.32 | {'A': 4} |
| clean|patch|None|16|None|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|16|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|16|4.0|a|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|patch|None|16|8.0|a|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|patch|None|16|16.0|a|None | 4 | 0% [0, 49] | 0.11 | {'A': 4} |
| clean|patch|None|20|None|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|20|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|20|4.0|a|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|patch|None|20|8.0|a|None | 4 | 0% [0, 49] | 0.16 | {'A': 4} |
| clean|patch|None|20|16.0|a|None | 4 | 0% [0, 49] | 0.28 | {'A': 4} |
| clean|patch|None|24|None|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|patch|None|24|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|24|4.0|a|None | 4 | 0% [0, 49] | 0.10 | {'A': 4} |
| clean|patch|None|24|8.0|a|None | 4 | 0% [0, 49] | 0.16 | {'A': 4} |
| clean|patch|None|24|16.0|a|None | 4 | 0% [0, 49] | 0.35 | {'A': 3, 'other': 1} |
| clean|patch|None|28|None|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|patch|None|28|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|28|4.0|a|None | 4 | 0% [0, 49] | 0.15 | {'A': 4} |
| clean|patch|None|28|8.0|a|None | 4 | 25% [5, 70] | 0.47 | {'A': 3, 'b': 1} |
| clean|patch|None|28|16.0|a|None | 4 | 50% [15, 85] | 0.58 | {'b': 2, 'other': 1, 'A': 1} |
| off|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|8.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 3, 'bO': 1} |
| off|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|8.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|16.0|a|None | 4 | 0% [0, 49] | nan | {'A': 3, 'other': 1} |
| off|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|8.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|16.0|a|None | 4 | 0% [0, 49] | nan | {'A': 2, 'other': 2} |
| off|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|28|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|28|8.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|28|16.0|a|None | 4 | 0% [0, 49] | nan | {'A': 2, 'other': 1, 'bO': 1} |
| off|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|band|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 3, 'other': 1} |
| off|push|lens|band|8.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |
| off|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-insert: k -, J - (ref rate 0.00); E-head: k -, J +0.00 [+0.00, +0.00] (ref rate 0.50); E-cue: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-unrelated: k -, J - (ref rate 0.00); W-copy*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.50); emb*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.50); patch_matched: k -, J - (ref rate 0.00); low_margin: k -
K1 - -> untestable; gate -; K2 nb - a/2 +0.00 [+0.00, +0.00], b - nb +0.50 [+0.00, +1.00] -> inconclusive; K4 +0.03 [-0.05, +0.07]
JS(P*, .) {"clean": 0.289, "E-name": 0.581, "E-insert": 0.264, "E-head": 0.339, "E-cue": 0.578, "E-unrelated": 0.287}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [0.2238, 0.2758, 0.181, 0.1806], "E-insert": [0.147, 0.2346, 0.3, 0.307], "E-head": [0.2332, 0.2956, 0.3218, 0.3171], "E-cue": [0.1769, 0.2699, 0.2621, 0.2755], "E-unrelated": [0.1006, 0.1673, 0.1999, 0.2308]}
transit proj on C's delta [44, 48, 52]: P*_b [0.5227, 0.4969, 0.4036], P* [0.6719, 0.6323, 0.5246], edits {"E-name": [0.5273, 0.5488, 0.6423], "E-insert": [0.5512, 0.5435, 0.5271], "E-head": [0.5918, 0.5687, 0.5525], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.2264, 0.2386, 0.2183]}

## BR (W-copy* = ('clean', 'copy', None, 36, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|edit|None|None|None|None|E-name | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|edit|None|None|None|None|E-insert | 4 | 75% [30, 95] | 0.71 | {'b': 3, 'A': 1} |
| clean|edit|None|None|None|None|E-head | 4 | 25% [5, 70] | 0.79 | {'other': 3, 'b': 1} |
| clean|edit|None|None|None|None|E-cue | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|edit|None|None|None|None|E-unrelated | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|16|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|16|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|16|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|16|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|4.0|r|None | 4 | 0% [0, 49] | 0.15 | {'other': 1, 'A': 3} |
| clean|push|random|16|4.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|4.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|16|4.0|a|None | 4 | 0% [0, 49] | -0.03 | {'A': 4} |
| clean|push|lens|16|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|16|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|8.0|r|None | 4 | 75% [30, 95] | 0.54 | {'b': 3, 'A': 1} |
| clean|push|random|16|8.0|r|None | 4 | 0% [0, 49] | -0.01 | {'A': 4} |
| clean|push|lens|16|8.0|a|None | 4 | 0% [0, 49] | 0.13 | {'A': 4} |
| clean|push|random|16|8.0|a|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|16|8.0|b|None | 4 | 0% [0, 49] | 0.15 | {'A': 4} |
| clean|push|random|16|8.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|16|16.0|r|None | 4 | 75% [30, 95] | 0.73 | {'b': 3, 'other': 1} |
| clean|push|random|16|16.0|r|None | 4 | 0% [0, 49] | 0.12 | {'A': 4} |
| clean|push|lens|16|16.0|a|None | 4 | 25% [5, 70] | 0.76 | {'other': 3, 'b': 1} |
| clean|push|random|16|16.0|a|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|16|16.0|b|None | 4 | 100% [51, 100] | 0.71 | {'b': 4} |
| clean|push|random|16|16.0|b|None | 4 | 0% [0, 49] | -0.01 | {'A': 4} |
| clean|push|lens|20|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|20|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|20|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|20|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|4.0|r|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|random|20|4.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|20|4.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|20|4.0|a|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|20|4.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|random|20|4.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|8.0|r|None | 4 | 50% [15, 85] | 0.38 | {'b': 2, 'A': 2} |
| clean|push|random|20|8.0|r|None | 4 | 0% [0, 49] | -0.02 | {'A': 4} |
| clean|push|lens|20|8.0|a|None | 4 | 25% [5, 70] | 0.14 | {'A': 3, 'b': 1} |
| clean|push|random|20|8.0|a|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|20|8.0|b|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|random|20|8.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|16.0|r|None | 4 | 75% [30, 95] | 0.66 | {'b': 3, 'A': 1} |
| clean|push|random|20|16.0|r|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|20|16.0|a|None | 4 | 25% [5, 70] | 0.44 | {'b': 1, 'other': 2, 'A': 1} |
| clean|push|random|20|16.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|16.0|b|None | 4 | 50% [15, 85] | 0.41 | {'A': 2, 'b': 2} |
| clean|push|random|20|16.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|24|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|24|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|24|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|24|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|4.0|r|None | 4 | 0% [0, 49] | 0.14 | {'A': 4} |
| clean|push|random|24|4.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|4.0|a|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|push|random|24|4.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|4.0|b|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|random|24|4.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|8.0|r|None | 4 | 0% [0, 49] | 0.19 | {'A': 4} |
| clean|push|random|24|8.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|8.0|a|None | 4 | 0% [0, 49] | 0.25 | {'A': 3, 'other': 1} |
| clean|push|random|24|8.0|a|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|24|8.0|b|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|push|random|24|8.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|16.0|r|None | 4 | 75% [30, 95] | 0.63 | {'b': 3, 'A': 1} |
| clean|push|random|24|16.0|r|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|24|16.0|a|None | 4 | 25% [5, 70] | 0.66 | {'b': 1, 'other': 3} |
| clean|push|random|24|16.0|a|None | 4 | 0% [0, 49] | 0.16 | {'A': 3, 'other': 1} |
| clean|push|lens|24|16.0|b|None | 4 | 75% [30, 95] | 0.75 | {'b': 3, 'other': 1} |
| clean|push|random|24|16.0|b|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|28|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|28|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|28|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|28|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|4.0|r|None | 4 | 25% [5, 70] | 0.26 | {'A': 3, 'b': 1} |
| clean|push|random|28|4.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|28|4.0|a|None | 4 | 25% [5, 70] | 0.31 | {'A': 3, 'b': 1} |
| clean|push|random|28|4.0|a|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|28|4.0|b|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|random|28|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|28|8.0|r|None | 4 | 50% [15, 85] | 0.55 | {'b': 2, 'A': 2} |
| clean|push|random|28|8.0|r|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|28|8.0|a|None | 4 | 50% [15, 85] | 0.50 | {'A': 2, 'b': 2} |
| clean|push|random|28|8.0|a|None | 4 | 0% [0, 49] | 0.12 | {'A': 4} |
| clean|push|lens|28|8.0|b|None | 4 | 0% [0, 49] | 0.16 | {'A': 4} |
| clean|push|random|28|8.0|b|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|28|16.0|r|None | 4 | 50% [15, 85] | 0.69 | {'other': 1, 'b': 2, 'A': 1} |
| clean|push|random|28|16.0|r|None | 4 | 25% [5, 70] | 0.25 | {'A': 3, 'b': 1} |
| clean|push|lens|28|16.0|a|None | 4 | 25% [5, 70] | 0.70 | {'other': 3, 'b': 1} |
| clean|push|random|28|16.0|a|None | 4 | 0% [0, 49] | 0.26 | {'A': 3, 'other': 1} |
| clean|push|lens|28|16.0|b|None | 4 | 75% [30, 95] | 0.68 | {'b': 3, 'A': 1} |
| clean|push|random|28|16.0|b|None | 4 | 0% [0, 49] | 0.18 | {'A': 4} |
| clean|push|lens|band|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|band|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|band|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|band|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|band|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|band|4.0|r|None | 4 | 75% [30, 95] | 0.66 | {'b': 3, 'A': 1} |
| clean|push|random|band|4.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|band|4.0|a|None | 4 | 50% [15, 85] | 0.68 | {'b': 2, 'other': 2} |
| clean|push|random|band|4.0|a|None | 4 | 0% [0, 49] | 0.08 | {'A': 4} |
| clean|push|lens|band|4.0|b|None | 4 | 75% [30, 95] | 0.66 | {'b': 3, 'A': 1} |
| clean|push|random|band|4.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|band|8.0|r|None | 4 | 75% [30, 95] | 0.72 | {'b': 3, 'other': 1} |
| clean|push|random|band|8.0|r|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|band|8.0|a|None | 4 | 0% [0, 49] | 0.51 | {'other': 4} |
| clean|push|random|band|8.0|a|None | 4 | 0% [0, 49] | 0.10 | {'A': 3, 'other': 1} |
| clean|push|lens|band|8.0|b|None | 4 | 100% [51, 100] | 0.83 | {'b': 4} |
| clean|push|random|band|8.0|b|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|band|16.0|r|None | 4 | 0% [0, 49] | 0.58 | {'other': 4} |
| clean|push|random|band|16.0|r|None | 4 | 50% [15, 85] | 0.36 | {'A': 2, 'b': 2} |
| clean|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | 0.47 | {'other': 4} |
| clean|push|random|band|16.0|a|None | 4 | 0% [0, 49] | 0.38 | {'other': 4} |
| clean|push|lens|band|16.0|b|None | 4 | 100% [51, 100] | 0.89 | {'b': 4} |
| clean|push|random|band|16.0|b|None | 4 | 25% [5, 70] | 0.34 | {'A': 3, 'b': 1} |
| clean|emb_diff|lens|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_diff|random|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_add|lens|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_add|random|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_diff|lens|-1|1.0|b|None | 4 | 50% [15, 85] | 0.52 | {'A': 2, 'b': 2} |
| clean|emb_diff|random|-1|1.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|emb_add|lens|-1|1.0|b|None | 4 | 50% [15, 85] | 0.43 | {'A': 2, 'b': 2} |
| clean|emb_add|random|-1|1.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_diff|lens|-1|4.0|b|None | 4 | 75% [30, 95] | 0.66 | {'other': 1, 'b': 3} |
| clean|emb_diff|random|-1|4.0|b|None | 4 | 50% [15, 85] | 0.44 | {'A': 2, 'b': 2} |
| clean|emb_add|lens|-1|4.0|b|None | 4 | 0% [0, 49] | 0.52 | {'other': 3, 'oc': 1} |
| clean|emb_add|random|-1|4.0|b|None | 4 | 25% [5, 70] | 0.45 | {'other': 1, 'b': 1, 'A': 2} |
| clean|copy|None|16|None|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|copy|None|20|None|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|copy|None|24|None|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|copy|None|28|None|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|copy|None|32|None|r|None | 4 | 0% [0, 49] | 0.13 | {'A': 4} |
| clean|copy|None|36|None|r|None | 4 | 25% [5, 70] | 0.29 | {'A': 3, 'b': 1} |
| clean|copy|None|40|None|r|None | 4 | 25% [5, 70] | 0.39 | {'A': 3, 'b': 1} |
| clean|copy|None|44|None|r|None | 4 | 25% [5, 70] | 0.39 | {'A': 3, 'b': 1} |
| clean|copy|None|48|None|r|None | 4 | 25% [5, 70] | 0.42 | {'A': 3, 'b': 1} |
| clean|patch|None|16|None|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|patch|None|16|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|16|4.0|a|None | 4 | 0% [0, 49] | -0.04 | {'A': 4} |
| clean|patch|None|16|8.0|a|None | 4 | 0% [0, 49] | -0.06 | {'A': 4} |
| clean|patch|None|16|16.0|a|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|patch|None|20|None|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|20|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|20|4.0|a|None | 4 | 0% [0, 49] | -0.01 | {'A': 4} |
| clean|patch|None|20|8.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|patch|None|20|16.0|a|None | 4 | 0% [0, 49] | 0.10 | {'A': 3, 'other': 1} |
| clean|patch|None|24|None|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|24|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|24|4.0|a|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|patch|None|24|8.0|a|None | 4 | 0% [0, 49] | 0.12 | {'A': 4} |
| clean|patch|None|24|16.0|a|None | 4 | 50% [15, 85] | 0.43 | {'b': 2, 'A': 1, 'other': 1} |
| clean|patch|None|28|None|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|patch|None|28|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|28|4.0|a|None | 4 | 0% [0, 49] | 0.12 | {'A': 4} |
| clean|patch|None|28|8.0|a|None | 4 | 50% [15, 85] | 0.53 | {'b': 2, 'A': 2} |
| clean|patch|None|28|16.0|a|None | 4 | 75% [30, 95] | 0.70 | {'b': 3, 'other': 1} |
| off|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|8.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 3, 'bO': 1} |
| off|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|8.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|16.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 1, 'other': 2, 'A': 1} |
| off|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|8.0|a|None | 4 | 0% [0, 49] | nan | {'A': 3, 'other': 1} |
| off|push|lens|24|16.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 1, 'other': 3} |
| off|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|28|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 3, 'bO': 1} |
| off|push|lens|28|8.0|a|None | 4 | 0% [0, 49] | nan | {'A': 2, 'bO': 2} |
| off|push|lens|28|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 3, 'bO': 1} |
| off|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|band|4.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 2, 'other': 2} |
| off|push|lens|band|8.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |
| off|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.25 [+0.00, +0.75] (ref rate 1.00); E-insert: k +0.20 [+0.20, +1.00], J +0.33 [+0.00, +1.00] (ref rate 0.75); E-head: k -0.33 [-1.00, -0.33], J +0.00 [+0.00, +0.00] (ref rate 0.25); E-cue: k -, J +0.25 [+0.00, +0.75] (ref rate 1.00); E-unrelated: k -, J +0.00 [+0.00, +0.00] (ref rate 0.00); W-copy*: k -0.33 [-1.00, -0.33], J +0.00 [+0.00, +0.00] (ref rate 0.25); emb*: k -0.50 [-1.00, -0.33], J +0.00 [+0.00, +0.00] (ref rate 0.50); patch_matched: k +0.50 [+0.20, +1.00], J +0.50 [+0.00, +1.00] (ref rate 0.50); low_margin: k +0.50 [+0.20, +1.00]
K1 +0.53 [+0.53, +1.00] -> inject; gate +0.00 [-0.50, +0.50]; K2 nb - a/2 -0.12 [-0.38, +0.00], b - nb +0.75 [+0.25, +1.00] -> inconclusive; K4 +0.16 [+0.08, +0.23]
JS(P*, .) {"clean": 0.682, "E-name": 0.509, "E-insert": 0.518, "E-head": 0.58, "E-cue": 0.51, "E-unrelated": 0.679}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [0.3201, 0.4125, 0.3769, 0.3975], "E-insert": [0.2497, 0.3255, 0.3495, 0.3874], "E-head": [0.3786, 0.4387, 0.4451, 0.4557], "E-cue": [0.1443, 0.2721, 0.3034, 0.3353], "E-unrelated": [0.1433, 0.1851, 0.1784, 0.1743]}
transit proj on C's delta [44, 48, 52]: P*_b [0.6906, 0.6566, 0.6521], P* [0.5141, 0.534, 0.5524], edits {"E-name": [0.8017, 0.7873, 0.7942], "E-insert": [0.7154, 0.7345, 0.6952], "E-head": [0.6261, 0.6259, 0.6369], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.1015, 0.1325, 0.1242]}

## RL (W-copy* = ('clean', 'copy', None, 32, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|edit|None|None|None|None|E-name | 4 | 100% [51, 100] | 0.99 | {'b': 4} |
| clean|edit|None|None|None|None|E-insert | 4 | 100% [51, 100] | 0.60 | {'b': 4} |
| clean|edit|None|None|None|None|E-head | 4 | 100% [51, 100] | 0.54 | {'b': 4} |
| clean|edit|None|None|None|None|E-cue | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|edit|None|None|None|None|E-unrelated | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|16|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|16|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|16|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|16|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|16|4.0|r|None | 4 | 25% [5, 70] | 0.21 | {'A': 3, 'b': 1} |
| clean|push|random|16|4.0|r|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|16|4.0|a|None | 4 | 75% [30, 95] | 0.41 | {'b': 3, 'A': 1} |
| clean|push|random|16|4.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|16|4.0|b|None | 4 | 50% [15, 85] | 0.41 | {'b': 2, 'A': 2} |
| clean|push|random|16|4.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|16|8.0|r|None | 4 | 75% [30, 95] | 0.47 | {'b': 3, 'A': 1} |
| clean|push|random|16|8.0|r|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|16|8.0|a|None | 4 | 100% [51, 100] | 0.78 | {'b': 4} |
| clean|push|random|16|8.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|8.0|b|None | 4 | 100% [51, 100] | 0.87 | {'b': 4} |
| clean|push|random|16|8.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|16.0|r|None | 4 | 75% [30, 95] | 0.49 | {'b': 3, 'A': 1} |
| clean|push|random|16|16.0|r|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|16|16.0|a|None | 4 | 25% [5, 70] | 0.78 | {'other': 3, 'b': 1} |
| clean|push|random|16|16.0|a|None | 4 | 0% [0, 49] | 0.16 | {'A': 4} |
| clean|push|lens|16|16.0|b|None | 4 | 100% [51, 100] | 0.92 | {'b': 4} |
| clean|push|random|16|16.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|20|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|20|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|20|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|4.0|r|None | 4 | 0% [0, 49] | 0.08 | {'A': 4} |
| clean|push|random|20|4.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|20|4.0|a|None | 4 | 25% [5, 70] | 0.17 | {'A': 3, 'b': 1} |
| clean|push|random|20|4.0|a|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|20|4.0|b|None | 4 | 25% [5, 70] | 0.15 | {'A': 3, 'b': 1} |
| clean|push|random|20|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|20|8.0|r|None | 4 | 25% [5, 70] | 0.23 | {'A': 3, 'b': 1} |
| clean|push|random|20|8.0|r|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|push|lens|20|8.0|a|None | 4 | 100% [51, 100] | 0.70 | {'b': 4} |
| clean|push|random|20|8.0|a|None | 4 | 0% [0, 49] | 0.08 | {'A': 4} |
| clean|push|lens|20|8.0|b|None | 4 | 100% [51, 100] | 0.76 | {'b': 4} |
| clean|push|random|20|8.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|20|16.0|r|None | 4 | 75% [30, 95] | 0.50 | {'b': 3, 'A': 1} |
| clean|push|random|20|16.0|r|None | 4 | 0% [0, 49] | 0.19 | {'A': 4} |
| clean|push|lens|20|16.0|a|None | 4 | 75% [30, 95] | 0.87 | {'b': 3, 'other': 1} |
| clean|push|random|20|16.0|a|None | 4 | 0% [0, 49] | 0.17 | {'A': 4} |
| clean|push|lens|20|16.0|b|None | 4 | 100% [51, 100] | 0.94 | {'b': 4} |
| clean|push|random|20|16.0|b|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|24|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|24|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|24|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|24|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|4.0|r|None | 4 | 0% [0, 49] | 0.15 | {'A': 4} |
| clean|push|random|24|4.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|4.0|a|None | 4 | 25% [5, 70] | 0.36 | {'A': 3, 'b': 1} |
| clean|push|random|24|4.0|a|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|24|4.0|b|None | 4 | 25% [5, 70] | 0.37 | {'A': 3, 'b': 1} |
| clean|push|random|24|4.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|8.0|r|None | 4 | 25% [5, 70] | 0.39 | {'A': 3, 'b': 1} |
| clean|push|random|24|8.0|r|None | 4 | 0% [0, 49] | 0.10 | {'A': 4} |
| clean|push|lens|24|8.0|a|None | 4 | 100% [51, 100] | 0.76 | {'b': 4} |
| clean|push|random|24|8.0|a|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|push|lens|24|8.0|b|None | 4 | 100% [51, 100] | 0.85 | {'b': 4} |
| clean|push|random|24|8.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|16.0|r|None | 4 | 25% [5, 70] | 0.44 | {'b': 1, 'A': 3} |
| clean|push|random|24|16.0|r|None | 4 | 0% [0, 49] | 0.29 | {'A': 3, 'oc': 1} |
| clean|push|lens|24|16.0|a|None | 4 | 50% [15, 85] | 0.75 | {'b': 2, 'other': 2} |
| clean|push|random|24|16.0|a|None | 4 | 0% [0, 49] | 0.28 | {'A': 3, 'other': 1} |
| clean|push|lens|24|16.0|b|None | 4 | 100% [51, 100] | 0.88 | {'b': 4} |
| clean|push|random|24|16.0|b|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|lens|28|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|28|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|28|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|28|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|28|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|28|4.0|r|None | 4 | 25% [5, 70] | 0.34 | {'A': 3, 'b': 1} |
| clean|push|random|28|4.0|r|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|28|4.0|a|None | 4 | 25% [5, 70] | 0.33 | {'A': 3, 'b': 1} |
| clean|push|random|28|4.0|a|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|28|4.0|b|None | 4 | 25% [5, 70] | 0.18 | {'A': 3, 'b': 1} |
| clean|push|random|28|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|28|8.0|r|None | 4 | 50% [15, 85] | 0.38 | {'b': 2, 'A': 2} |
| clean|push|random|28|8.0|r|None | 4 | 0% [0, 49] | 0.22 | {'A': 4} |
| clean|push|lens|28|8.0|a|None | 4 | 75% [30, 95] | 0.62 | {'b': 3, 'A': 1} |
| clean|push|random|28|8.0|a|None | 4 | 0% [0, 49] | 0.15 | {'A': 4} |
| clean|push|lens|28|8.0|b|None | 4 | 50% [15, 85] | 0.43 | {'b': 2, 'A': 2} |
| clean|push|random|28|8.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|28|16.0|r|None | 4 | 25% [5, 70] | 0.37 | {'A': 3, 'b': 1} |
| clean|push|random|28|16.0|r|None | 4 | 0% [0, 49] | 0.35 | {'A': 4} |
| clean|push|lens|28|16.0|a|None | 4 | 50% [15, 85] | 0.56 | {'b': 2, 'other': 1, 'A': 1} |
| clean|push|random|28|16.0|a|None | 4 | 0% [0, 49] | 0.36 | {'A': 3, 'other': 1} |
| clean|push|lens|28|16.0|b|None | 4 | 75% [30, 95] | 0.53 | {'b': 3, 'A': 1} |
| clean|push|random|28|16.0|b|None | 4 | 0% [0, 49] | 0.17 | {'A': 4} |
| clean|push|lens|band|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|band|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|band|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|band|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|band|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|band|4.0|r|None | 4 | 75% [30, 95] | 0.54 | {'b': 3, 'A': 1} |
| clean|push|random|band|4.0|r|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|band|4.0|a|None | 4 | 75% [30, 95] | 0.83 | {'b': 3, 'other': 1} |
| clean|push|random|band|4.0|a|None | 4 | 0% [0, 49] | 0.15 | {'A': 4} |
| clean|push|lens|band|4.0|b|None | 4 | 100% [51, 100] | 0.97 | {'b': 4} |
| clean|push|random|band|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|band|8.0|r|None | 4 | 50% [15, 85] | 0.50 | {'b': 2, 'A': 2} |
| clean|push|random|band|8.0|r|None | 4 | 0% [0, 49] | 0.24 | {'A': 4} |
| clean|push|lens|band|8.0|a|None | 4 | 0% [0, 49] | 0.64 | {'other': 4} |
| clean|push|random|band|8.0|a|None | 4 | 0% [0, 49] | 0.28 | {'A': 2, 'other': 2} |
| clean|push|lens|band|8.0|b|None | 4 | 100% [51, 100] | 0.92 | {'b': 4} |
| clean|push|random|band|8.0|b|None | 4 | 0% [0, 49] | 0.11 | {'A': 4} |
| clean|push|lens|band|16.0|r|None | 4 | 0% [0, 49] | 0.42 | {'other': 2, 'A': 2} |
| clean|push|random|band|16.0|r|None | 4 | 0% [0, 49] | 0.35 | {'A': 3, 'oc': 1} |
| clean|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | 0.54 | {'other': 4} |
| clean|push|random|band|16.0|a|None | 4 | 0% [0, 49] | 0.49 | {'other': 4} |
| clean|push|lens|band|16.0|b|None | 4 | 100% [51, 100] | 0.86 | {'b': 4} |
| clean|push|random|band|16.0|b|None | 4 | 25% [5, 70] | 0.46 | {'A': 2, 'oc': 1, 'b': 1} |
| clean|emb_diff|lens|-1|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|emb_diff|random|-1|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|emb_add|lens|-1|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|emb_add|random|-1|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|emb_diff|lens|-1|1.0|b|None | 4 | 100% [51, 100] | 0.82 | {'b': 4} |
| clean|emb_diff|random|-1|1.0|b|None | 4 | 25% [5, 70] | 0.34 | {'A': 2, 'oc': 1, 'b': 1} |
| clean|emb_add|lens|-1|1.0|b|None | 4 | 75% [30, 95] | 0.80 | {'b': 3, 'A': 1} |
| clean|emb_add|random|-1|1.0|b|None | 4 | 0% [0, 49] | 0.14 | {'A': 4} |
| clean|emb_diff|lens|-1|4.0|b|None | 4 | 100% [51, 100] | 0.68 | {'b': 4} |
| clean|emb_diff|random|-1|4.0|b|None | 4 | 50% [15, 85] | 0.51 | {'oc': 1, 'b': 2, 'A': 1} |
| clean|emb_add|lens|-1|4.0|b|None | 4 | 100% [51, 100] | 0.92 | {'b': 4} |
| clean|emb_add|random|-1|4.0|b|None | 4 | 25% [5, 70] | 0.53 | {'oc': 2, 'b': 1, 'A': 1} |
| clean|copy|None|16|None|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|copy|None|20|None|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|copy|None|24|None|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|copy|None|28|None|r|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|copy|None|32|None|r|None | 4 | 25% [5, 70] | 0.42 | {'A': 3, 'b': 1} |
| clean|copy|None|36|None|r|None | 4 | 100% [51, 100] | 0.52 | {'b': 4} |
| clean|copy|None|40|None|r|None | 4 | 100% [51, 100] | 0.56 | {'b': 4} |
| clean|copy|None|44|None|r|None | 4 | 100% [51, 100] | 0.72 | {'b': 4} |
| clean|copy|None|48|None|r|None | 4 | 100% [51, 100] | 0.79 | {'b': 4} |
| clean|patch|None|16|None|a|None | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|patch|None|16|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|patch|None|16|4.0|a|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|patch|None|16|8.0|a|None | 4 | 50% [15, 85] | 0.59 | {'b': 2, 'A': 2} |
| clean|patch|None|16|16.0|a|None | 4 | 100% [51, 100] | 0.89 | {'b': 4} |
| clean|patch|None|20|None|a|None | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|patch|None|20|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|patch|None|20|4.0|a|None | 4 | 25% [5, 70] | 0.19 | {'A': 3, 'b': 1} |
| clean|patch|None|20|8.0|a|None | 4 | 100% [51, 100] | 0.81 | {'b': 4} |
| clean|patch|None|20|16.0|a|None | 4 | 100% [51, 100] | 0.87 | {'b': 4} |
| clean|patch|None|24|None|a|None | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|patch|None|24|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|patch|None|24|4.0|a|None | 4 | 25% [5, 70] | 0.21 | {'A': 3, 'b': 1} |
| clean|patch|None|24|8.0|a|None | 4 | 100% [51, 100] | 0.76 | {'b': 4} |
| clean|patch|None|24|16.0|a|None | 4 | 75% [30, 95] | 0.85 | {'b': 3, 'other': 1} |
| clean|patch|None|28|None|a|None | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|patch|None|28|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|patch|None|28|4.0|a|None | 4 | 25% [5, 70] | 0.47 | {'A': 3, 'b': 1} |
| clean|patch|None|28|8.0|a|None | 4 | 100% [51, 100] | 0.89 | {'b': 4} |
| clean|patch|None|28|16.0|a|None | 4 | 75% [30, 95] | 0.87 | {'b': 3, 'other': 1} |
| off|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|4.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 2, 'A': 2} |
| off|push|lens|16|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 4} |
| off|push|lens|16|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 3, 'bO': 1} |
| off|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 4} |
| off|push|lens|20|16.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 3, 'other': 1} |
| off|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 3, 'bO': 1} |
| off|push|lens|24|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 4} |
| off|push|lens|24|16.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 2, 'other': 2} |
| off|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|28|4.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 2, 'A': 2} |
| off|push|lens|28|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 3, 'A': 1} |
| off|push|lens|28|16.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 2, 'other': 1, 'A': 1} |
| off|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|band|4.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 3, 'other': 1} |
| off|push|lens|band|8.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |
| off|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.50 [+0.00, +1.00] (ref rate 1.00); E-insert: k -, J +0.50 [+0.00, +1.00] (ref rate 1.00); E-head: k -, J +0.50 [+0.00, +1.00] (ref rate 1.00); E-cue: k -, J +0.50 [+0.00, +1.00] (ref rate 1.00); E-unrelated: k -, J +0.00 [+0.00, +0.00] (ref rate 0.00); W-copy*: k -0.50 [-1.00, -0.33], J +0.00 [+0.00, +0.00] (ref rate 0.25); emb*: k +0.50 [+0.20, +1.00], J +0.67 [+0.00, +1.00] (ref rate 0.75); patch_matched: k +0.50 [+0.20, +1.00], J +0.67 [+0.00, +1.00] (ref rate 0.75); low_margin: k +0.00 [-1.00, +1.00]
K1 - -> untestable; gate -; K2 nb - a/2 -0.25 [-0.50, +0.00], b - nb +1.00 [+1.00, +1.00] -> inconclusive; K4 -0.16 [-0.25, -0.07]
JS(P*, .) {"clean": 0.594, "E-name": 0.277, "E-insert": 0.251, "E-head": 0.289, "E-cue": 0.276, "E-unrelated": 0.594}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [0.1272, 0.0738, 0.1039, 0.1818], "E-insert": [0.2072, 0.2961, 0.2836, 0.2447], "E-head": [0.3897, 0.4532, 0.3832, 0.3257], "E-cue": [0.2136, 0.302, 0.3446, 0.3894], "E-unrelated": [0.1078, 0.1998, 0.2243, 0.2362]}
transit proj on C's delta [44, 48, 52]: P*_b [0.439, 0.4301, 0.4091], P* [0.4611, 0.4448, 0.4295], edits {"E-name": [0.5908, 0.6242, 0.621], "E-insert": [0.5598, 0.5633, 0.5569], "E-head": [0.5271, 0.5593, 0.5144], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.2386, 0.2586, 0.2209]}

## RR (W-copy* = ('clean', 'copy', None, 48, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|edit|None|None|None|None|E-name | 4 | 100% [51, 100] | 1.01 | {'b': 4} |
| clean|edit|None|None|None|None|E-insert | 4 | 75% [30, 95] | 0.73 | {'b': 3, 'A': 1} |
| clean|edit|None|None|None|None|E-head | 4 | 50% [15, 85] | 0.68 | {'other': 2, 'b': 2} |
| clean|edit|None|None|None|None|E-cue | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|edit|None|None|None|None|E-unrelated | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|16|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|16|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|16|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|16|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|16|4.0|r|None | 4 | 25% [5, 70] | 0.18 | {'A': 3, 'b': 1} |
| clean|push|random|16|4.0|r|None | 4 | 0% [0, 49] | -0.02 | {'A': 4} |
| clean|push|lens|16|4.0|a|None | 4 | 75% [30, 95] | 0.60 | {'b': 3, 'A': 1} |
| clean|push|random|16|4.0|a|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|16|4.0|b|None | 4 | 75% [30, 95] | 0.57 | {'b': 3, 'A': 1} |
| clean|push|random|16|4.0|b|None | 4 | 0% [0, 49] | -0.01 | {'A': 4} |
| clean|push|lens|16|8.0|r|None | 4 | 75% [30, 95] | 0.62 | {'b': 3, 'A': 1} |
| clean|push|random|16|8.0|r|None | 4 | 0% [0, 49] | -0.01 | {'A': 4} |
| clean|push|lens|16|8.0|a|None | 4 | 100% [51, 100] | 0.87 | {'b': 4} |
| clean|push|random|16|8.0|a|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|16|8.0|b|None | 4 | 100% [51, 100] | 0.91 | {'b': 4} |
| clean|push|random|16|8.0|b|None | 4 | 0% [0, 49] | -0.01 | {'A': 4} |
| clean|push|lens|16|16.0|r|None | 4 | 75% [30, 95] | 0.71 | {'b': 3, 'other': 1} |
| clean|push|random|16|16.0|r|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|lens|16|16.0|a|None | 4 | 25% [5, 70] | 0.75 | {'other': 3, 'b': 1} |
| clean|push|random|16|16.0|a|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|push|lens|16|16.0|b|None | 4 | 100% [51, 100] | 0.91 | {'b': 4} |
| clean|push|random|16|16.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|20|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|20|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|20|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|4.0|r|None | 4 | 25% [5, 70] | 0.14 | {'A': 3, 'b': 1} |
| clean|push|random|20|4.0|r|None | 4 | 0% [0, 49] | -0.02 | {'A': 4} |
| clean|push|lens|20|4.0|a|None | 4 | 25% [5, 70] | 0.29 | {'A': 3, 'b': 1} |
| clean|push|random|20|4.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|20|4.0|b|None | 4 | 50% [15, 85] | 0.37 | {'A': 2, 'b': 2} |
| clean|push|random|20|4.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|8.0|r|None | 4 | 25% [5, 70] | 0.37 | {'A': 3, 'b': 1} |
| clean|push|random|20|8.0|r|None | 4 | 0% [0, 49] | -0.02 | {'A': 4} |
| clean|push|lens|20|8.0|a|None | 4 | 100% [51, 100] | 0.75 | {'b': 4} |
| clean|push|random|20|8.0|a|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|push|lens|20|8.0|b|None | 4 | 100% [51, 100] | 0.88 | {'b': 4} |
| clean|push|random|20|8.0|b|None | 4 | 0% [0, 49] | -0.01 | {'A': 4} |
| clean|push|lens|20|16.0|r|None | 4 | 75% [30, 95] | 0.58 | {'b': 3, 'A': 1} |
| clean|push|random|20|16.0|r|None | 4 | 0% [0, 49] | 0.10 | {'A': 4} |
| clean|push|lens|20|16.0|a|None | 4 | 75% [30, 95] | 0.76 | {'b': 3, 'other': 1} |
| clean|push|random|20|16.0|a|None | 4 | 0% [0, 49] | 0.16 | {'A': 3, 'other': 1} |
| clean|push|lens|20|16.0|b|None | 4 | 100% [51, 100] | 0.93 | {'b': 4} |
| clean|push|random|20|16.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|24|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|24|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|24|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|4.0|r|None | 4 | 25% [5, 70] | 0.26 | {'A': 3, 'b': 1} |
| clean|push|random|24|4.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|4.0|a|None | 4 | 75% [30, 95] | 0.60 | {'A': 1, 'b': 3} |
| clean|push|random|24|4.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|4.0|b|None | 4 | 50% [15, 85] | 0.51 | {'A': 2, 'b': 2} |
| clean|push|random|24|4.0|b|None | 4 | 0% [0, 49] | -0.01 | {'A': 4} |
| clean|push|lens|24|8.0|r|None | 4 | 50% [15, 85] | 0.46 | {'A': 2, 'b': 2} |
| clean|push|random|24|8.0|r|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|push|lens|24|8.0|a|None | 4 | 75% [30, 95] | 0.65 | {'b': 3, 'A': 1} |
| clean|push|random|24|8.0|a|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|push|lens|24|8.0|b|None | 4 | 100% [51, 100] | 0.92 | {'b': 4} |
| clean|push|random|24|8.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|16.0|r|None | 4 | 75% [30, 95] | 0.46 | {'b': 3, 'A': 1} |
| clean|push|random|24|16.0|r|None | 4 | 0% [0, 49] | 0.18 | {'A': 4} |
| clean|push|lens|24|16.0|a|None | 4 | 25% [5, 70] | 0.70 | {'b': 1, 'other': 3} |
| clean|push|random|24|16.0|a|None | 4 | 25% [5, 70] | 0.21 | {'A': 3, 'b': 1} |
| clean|push|lens|24|16.0|b|None | 4 | 75% [30, 95] | 0.91 | {'b': 3, 'other': 1} |
| clean|push|random|24|16.0|b|None | 4 | 0% [0, 49] | 0.08 | {'A': 4} |
| clean|push|lens|28|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|28|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|28|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|28|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|28|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|28|4.0|r|None | 4 | 50% [15, 85] | 0.42 | {'A': 2, 'b': 2} |
| clean|push|random|28|4.0|r|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|28|4.0|a|None | 4 | 50% [15, 85] | 0.56 | {'A': 2, 'b': 2} |
| clean|push|random|28|4.0|a|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|28|4.0|b|None | 4 | 25% [5, 70] | 0.31 | {'A': 3, 'b': 1} |
| clean|push|random|28|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|28|8.0|r|None | 4 | 75% [30, 95] | 0.43 | {'b': 3, 'A': 1} |
| clean|push|random|28|8.0|r|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|push|lens|28|8.0|a|None | 4 | 100% [51, 100] | 0.83 | {'b': 4} |
| clean|push|random|28|8.0|a|None | 4 | 0% [0, 49] | 0.10 | {'A': 4} |
| clean|push|lens|28|8.0|b|None | 4 | 75% [30, 95] | 0.70 | {'b': 3, 'A': 1} |
| clean|push|random|28|8.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|16.0|r|None | 4 | 50% [15, 85] | 0.39 | {'b': 2, 'A': 2} |
| clean|push|random|28|16.0|r|None | 4 | 25% [5, 70] | 0.21 | {'A': 3, 'b': 1} |
| clean|push|lens|28|16.0|a|None | 4 | 50% [15, 85] | 0.63 | {'b': 2, 'other': 2} |
| clean|push|random|28|16.0|a|None | 4 | 0% [0, 49] | 0.23 | {'A': 3, 'other': 1} |
| clean|push|lens|28|16.0|b|None | 4 | 75% [30, 95] | 0.70 | {'b': 3, 'A': 1} |
| clean|push|random|28|16.0|b|None | 4 | 0% [0, 49] | 0.16 | {'A': 4} |
| clean|push|lens|band|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|band|0.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|band|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|band|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|random|band|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|band|4.0|r|None | 4 | 75% [30, 95] | 0.68 | {'b': 3, 'A': 1} |
| clean|push|random|band|4.0|r|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|push|lens|band|4.0|a|None | 4 | 75% [30, 95] | 0.87 | {'b': 3, 'other': 1} |
| clean|push|random|band|4.0|a|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|band|4.0|b|None | 4 | 100% [51, 100] | 0.95 | {'b': 4} |
| clean|push|random|band|4.0|b|None | 4 | 0% [0, 49] | -0.01 | {'A': 4} |
| clean|push|lens|band|8.0|r|None | 4 | 75% [30, 95] | 0.57 | {'b': 3, 'A': 1} |
| clean|push|random|band|8.0|r|None | 4 | 25% [5, 70] | 0.12 | {'A': 3, 'b': 1} |
| clean|push|lens|band|8.0|a|None | 4 | 0% [0, 49] | 0.46 | {'other': 4} |
| clean|push|random|band|8.0|a|None | 4 | 0% [0, 49] | 0.27 | {'A': 3, 'other': 1} |
| clean|push|lens|band|8.0|b|None | 4 | 100% [51, 100] | 0.89 | {'b': 4} |
| clean|push|random|band|8.0|b|None | 4 | 0% [0, 49] | 0.13 | {'A': 4} |
| clean|push|lens|band|16.0|r|None | 4 | 0% [0, 49] | 0.46 | {'other': 2, 'oc': 1, 'A': 1} |
| clean|push|random|band|16.0|r|None | 4 | 25% [5, 70] | 0.26 | {'A': 3, 'b': 1} |
| clean|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | 0.48 | {'other': 4} |
| clean|push|random|band|16.0|a|None | 4 | 0% [0, 49] | 0.42 | {'other': 4} |
| clean|push|lens|band|16.0|b|None | 4 | 100% [51, 100] | 0.84 | {'b': 4} |
| clean|push|random|band|16.0|b|None | 4 | 50% [15, 85] | 0.50 | {'A': 1, 'b': 2, 'other': 1} |
| clean|emb_diff|lens|-1|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|emb_diff|random|-1|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|emb_add|lens|-1|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|emb_add|random|-1|0.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|emb_diff|lens|-1|1.0|b|None | 4 | 100% [51, 100] | 0.76 | {'b': 4} |
| clean|emb_diff|random|-1|1.0|b|None | 4 | 25% [5, 70] | 0.13 | {'A': 3, 'b': 1} |
| clean|emb_add|lens|-1|1.0|b|None | 4 | 75% [30, 95] | 0.77 | {'b': 3, 'A': 1} |
| clean|emb_add|random|-1|1.0|b|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|emb_diff|lens|-1|4.0|b|None | 4 | 50% [15, 85] | 0.52 | {'A': 1, 'oc': 1, 'b': 2} |
| clean|emb_diff|random|-1|4.0|b|None | 4 | 50% [15, 85] | 0.50 | {'A': 2, 'b': 2} |
| clean|emb_add|lens|-1|4.0|b|None | 4 | 0% [0, 49] | 0.26 | {'A': 3, 'other': 1} |
| clean|emb_add|random|-1|4.0|b|None | 4 | 50% [15, 85] | 0.48 | {'A': 2, 'b': 2} |
| clean|copy|None|16|None|r|None | 4 | 0% [0, 49] | -0.03 | {'A': 4} |
| clean|copy|None|20|None|r|None | 4 | 0% [0, 49] | -0.04 | {'A': 4} |
| clean|copy|None|24|None|r|None | 4 | 0% [0, 49] | -0.03 | {'A': 4} |
| clean|copy|None|28|None|r|None | 4 | 0% [0, 49] | -0.02 | {'A': 4} |
| clean|copy|None|32|None|r|None | 4 | 0% [0, 49] | 0.12 | {'A': 4} |
| clean|copy|None|36|None|r|None | 4 | 0% [0, 49] | 0.27 | {'A': 4} |
| clean|copy|None|40|None|r|None | 4 | 25% [5, 70] | 0.31 | {'A': 3, 'b': 1} |
| clean|copy|None|44|None|r|None | 4 | 25% [5, 70] | 0.38 | {'A': 3, 'b': 1} |
| clean|copy|None|48|None|r|None | 4 | 50% [15, 85] | 0.49 | {'A': 2, 'b': 2} |
| clean|patch|None|16|None|a|None | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|patch|None|16|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|patch|None|16|4.0|a|None | 4 | 0% [0, 49] | -0.02 | {'A': 4} |
| clean|patch|None|16|8.0|a|None | 4 | 75% [30, 95] | 0.68 | {'b': 3, 'A': 1} |
| clean|patch|None|16|16.0|a|None | 4 | 100% [51, 100] | 0.95 | {'b': 4} |
| clean|patch|None|20|None|a|None | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|patch|None|20|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|patch|None|20|4.0|a|None | 4 | 25% [5, 70] | 0.13 | {'A': 3, 'b': 1} |
| clean|patch|None|20|8.0|a|None | 4 | 100% [51, 100] | 0.90 | {'b': 4} |
| clean|patch|None|20|16.0|a|None | 4 | 75% [30, 95] | 0.84 | {'b': 3, 'other': 1} |
| clean|patch|None|24|None|a|None | 4 | 100% [51, 100] | 0.99 | {'b': 4} |
| clean|patch|None|24|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|patch|None|24|4.0|a|None | 4 | 25% [5, 70] | 0.11 | {'A': 3, 'b': 1} |
| clean|patch|None|24|8.0|a|None | 4 | 100% [51, 100] | 0.75 | {'b': 4} |
| clean|patch|None|24|16.0|a|None | 4 | 75% [30, 95] | 0.83 | {'b': 3, 'other': 1} |
| clean|patch|None|28|None|a|None | 4 | 100% [51, 100] | 0.99 | {'b': 4} |
| clean|patch|None|28|0.0|a|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|patch|None|28|4.0|a|None | 4 | 25% [5, 70] | 0.38 | {'A': 3, 'b': 1} |
| clean|patch|None|28|8.0|a|None | 4 | 100% [51, 100] | 0.97 | {'b': 4} |
| clean|patch|None|28|16.0|a|None | 4 | 100% [51, 100] | 0.95 | {'b': 4} |
| off|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|4.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 3, 'A': 1} |
| off|push|lens|16|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 4} |
| off|push|lens|16|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 3, 'bO': 1} |
| off|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 3, 'bO': 1} |
| off|push|lens|20|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 4} |
| off|push|lens|20|16.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 3, 'other': 1} |
| off|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 1, 'bO': 3} |
| off|push|lens|24|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 3, 'A': 1} |
| off|push|lens|24|16.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 1, 'other': 3} |
| off|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|28|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 2, 'bO': 2} |
| off|push|lens|28|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 4} |
| off|push|lens|28|16.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 2, 'other': 2} |
| off|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|band|4.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 3, 'other': 1} |
| off|push|lens|band|8.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |
| off|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.25 [+0.00, +0.75] (ref rate 1.00); E-insert: k +0.20 [+0.20, +1.00], J +0.33 [+0.00, +1.00] (ref rate 0.75); E-head: k -0.50 [-1.00, -0.33], J +0.00 [+0.00, +0.00] (ref rate 0.50); E-cue: k -, J +0.25 [+0.00, +0.75] (ref rate 1.00); E-unrelated: k -, J +0.00 [+0.00, +0.00] (ref rate 0.00); W-copy*: k -0.50 [-1.00, -0.33], J +0.00 [+0.00, +0.00] (ref rate 0.50); emb*: k +0.20 [+0.20, +1.00], J +0.33 [+0.00, +1.00] (ref rate 0.75); patch_matched: k +0.20 [+0.20, +1.00], J +0.33 [+0.00, +1.00] (ref rate 0.75); low_margin: k +0.50 [+0.20, +1.00]
K1 +0.70 [+0.53, +2.00] -> inject; gate +0.17 [-0.17, +0.17]; K2 nb - a/2 -0.12 [-0.38, +0.00], b - nb +0.75 [+0.25, +1.00] -> inconclusive; K4 -0.06 [-0.14, +0.01]
JS(P*, .) {"clean": 0.681, "E-name": 0.515, "E-insert": 0.507, "E-head": 0.569, "E-cue": 0.514, "E-unrelated": 0.681}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [0.178, 0.1908, 0.1977, 0.3308], "E-insert": [0.249, 0.3468, 0.3414, 0.4085], "E-head": [0.4003, 0.4486, 0.4154, 0.4227], "E-cue": [0.1999, 0.2932, 0.2969, 0.378], "E-unrelated": [0.0862, 0.1396, 0.1722, 0.2048]}
transit proj on C's delta [44, 48, 52]: P*_b [0.4844, 0.4586, 0.5018], P* [0.456, 0.4917, 0.5494], edits {"E-name": [0.7531, 0.7662, 0.7953], "E-insert": [0.6239, 0.6052, 0.6047], "E-head": [0.4307, 0.4187, 0.4269], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.0773, 0.0767, 0.0595]}

## R (W-copy* = ('clean', 'copy', None, 36, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|edit|None|None|None|None|E-name | 4 | 100% [51, 100] | 1.12 | {'b': 4} |
| clean|edit|None|None|None|None|E-insert | 4 | 100% [51, 100] | 0.57 | {'b': 4} |
| clean|edit|None|None|None|None|E-cue | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|edit|None|None|None|None|E-unrelated | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|16|0.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|16|0.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|16|0.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|0.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|16|0.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|4.0|r|None | 4 | 50% [15, 85] | 0.49 | {'A': 2, 'b': 2} |
| clean|push|random|16|4.0|r|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|16|4.0|a|None | 4 | 100% [51, 100] | 1.01 | {'b': 4} |
| clean|push|random|16|4.0|a|None | 4 | 0% [0, 49] | -0.01 | {'A': 4} |
| clean|push|lens|16|4.0|b|None | 4 | 100% [51, 100] | 0.96 | {'b': 4} |
| clean|push|random|16|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|8.0|r|None | 4 | 100% [51, 100] | 0.66 | {'b': 4} |
| clean|push|random|16|8.0|r|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|16|8.0|a|None | 4 | 50% [15, 85] | 1.06 | {'b': 2, 'other': 2} |
| clean|push|random|16|8.0|a|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|16|8.0|b|None | 4 | 100% [51, 100] | 1.06 | {'b': 4} |
| clean|push|random|16|8.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|16.0|r|None | 4 | 100% [51, 100] | 0.78 | {'b': 4} |
| clean|push|random|16|16.0|r|None | 4 | 0% [0, 49] | 0.24 | {'A': 3, 'other': 1} |
| clean|push|lens|16|16.0|a|None | 4 | 0% [0, 49] | 0.79 | {'other': 4} |
| clean|push|random|16|16.0|a|None | 4 | 0% [0, 49] | 0.15 | {'A': 3, 'other': 1} |
| clean|push|lens|16|16.0|b|None | 4 | 100% [51, 100] | 1.06 | {'b': 4} |
| clean|push|random|16|16.0|b|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|push|lens|20|0.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|20|0.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|20|0.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|20|0.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|20|0.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|20|4.0|r|None | 4 | 25% [5, 70] | 0.44 | {'b': 1, 'A': 3} |
| clean|push|random|20|4.0|r|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|20|4.0|a|None | 4 | 100% [51, 100] | 1.04 | {'b': 4} |
| clean|push|random|20|4.0|a|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|lens|20|4.0|b|None | 4 | 100% [51, 100] | 0.98 | {'b': 4} |
| clean|push|random|20|4.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|8.0|r|None | 4 | 75% [30, 95] | 0.55 | {'b': 3, 'A': 1} |
| clean|push|random|20|8.0|r|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|20|8.0|a|None | 4 | 75% [30, 95] | 1.11 | {'b': 3, 'other': 1} |
| clean|push|random|20|8.0|a|None | 4 | 0% [0, 49] | 0.10 | {'A': 4} |
| clean|push|lens|20|8.0|b|None | 4 | 100% [51, 100] | 1.04 | {'b': 4} |
| clean|push|random|20|8.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|20|16.0|r|None | 4 | 75% [30, 95] | 0.72 | {'b': 3, 'other': 1} |
| clean|push|random|20|16.0|r|None | 4 | 0% [0, 49] | 0.27 | {'A': 4} |
| clean|push|lens|20|16.0|a|None | 4 | 0% [0, 49] | 0.85 | {'other': 4} |
| clean|push|random|20|16.0|a|None | 4 | 0% [0, 49] | 0.28 | {'other': 3, 'A': 1} |
| clean|push|lens|20|16.0|b|None | 4 | 100% [51, 100] | 1.02 | {'b': 4} |
| clean|push|random|20|16.0|b|None | 4 | 0% [0, 49] | 0.16 | {'A': 3, 'other': 1} |
| clean|push|lens|24|0.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|24|0.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|24|0.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|0.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|24|0.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|4.0|r|None | 4 | 100% [51, 100] | 0.67 | {'b': 4} |
| clean|push|random|24|4.0|r|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|push|lens|24|4.0|a|None | 4 | 100% [51, 100] | 1.10 | {'b': 4} |
| clean|push|random|24|4.0|a|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|lens|24|4.0|b|None | 4 | 100% [51, 100] | 1.02 | {'b': 4} |
| clean|push|random|24|4.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|24|8.0|r|None | 4 | 100% [51, 100] | 0.88 | {'b': 4} |
| clean|push|random|24|8.0|r|None | 4 | 0% [0, 49] | 0.20 | {'A': 4} |
| clean|push|lens|24|8.0|a|None | 4 | 75% [30, 95] | 1.09 | {'b': 3, 'other': 1} |
| clean|push|random|24|8.0|a|None | 4 | 0% [0, 49] | 0.15 | {'A': 4} |
| clean|push|lens|24|8.0|b|None | 4 | 100% [51, 100] | 1.03 | {'b': 4} |
| clean|push|random|24|8.0|b|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|24|16.0|r|None | 4 | 100% [51, 100] | 0.83 | {'b': 4} |
| clean|push|random|24|16.0|r|None | 4 | 25% [5, 70] | 0.36 | {'A': 2, 'other': 1, 'b': 1} |
| clean|push|lens|24|16.0|a|None | 4 | 0% [0, 49] | 0.96 | {'other': 4} |
| clean|push|random|24|16.0|a|None | 4 | 0% [0, 49] | 0.41 | {'other': 4} |
| clean|push|lens|24|16.0|b|None | 4 | 100% [51, 100] | 0.99 | {'b': 4} |
| clean|push|random|24|16.0|b|None | 4 | 0% [0, 49] | 0.34 | {'A': 2, 'other': 2} |
| clean|push|lens|28|0.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|28|0.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|28|0.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|28|0.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|28|0.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|28|4.0|r|None | 4 | 100% [51, 100] | 0.91 | {'b': 4} |
| clean|push|random|28|4.0|r|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|28|4.0|a|None | 4 | 100% [51, 100] | 1.16 | {'b': 4} |
| clean|push|random|28|4.0|a|None | 4 | 0% [0, 49] | 0.10 | {'A': 4} |
| clean|push|lens|28|4.0|b|None | 4 | 100% [51, 100] | 0.90 | {'b': 4} |
| clean|push|random|28|4.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|28|8.0|r|None | 4 | 100% [51, 100] | 0.92 | {'b': 4} |
| clean|push|random|28|8.0|r|None | 4 | 0% [0, 49] | 0.33 | {'A': 4} |
| clean|push|lens|28|8.0|a|None | 4 | 50% [15, 85] | 1.21 | {'b': 2, 'other': 2} |
| clean|push|random|28|8.0|a|None | 4 | 0% [0, 49] | 0.21 | {'A': 3, 'other': 1} |
| clean|push|lens|28|8.0|b|None | 4 | 100% [51, 100] | 1.04 | {'b': 4} |
| clean|push|random|28|8.0|b|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|push|lens|28|16.0|r|None | 4 | 0% [0, 49] | 0.49 | {'other': 1, 'A': 2, 'oc': 1} |
| clean|push|random|28|16.0|r|None | 4 | 0% [0, 49] | 0.38 | {'A': 4} |
| clean|push|lens|28|16.0|a|None | 4 | 0% [0, 49] | 1.05 | {'other': 4} |
| clean|push|random|28|16.0|a|None | 4 | 0% [0, 49] | 0.44 | {'other': 4} |
| clean|push|lens|28|16.0|b|None | 4 | 100% [51, 100] | 0.98 | {'b': 4} |
| clean|push|random|28|16.0|b|None | 4 | 0% [0, 49] | 0.32 | {'A': 3, 'other': 1} |
| clean|push|lens|band|0.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|band|0.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|band|0.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|band|0.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|band|0.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|band|4.0|r|None | 4 | 100% [51, 100] | 1.05 | {'b': 4} |
| clean|push|random|band|4.0|r|None | 4 | 0% [0, 49] | 0.19 | {'A': 4} |
| clean|push|lens|band|4.0|a|None | 4 | 0% [0, 49] | 1.15 | {'other': 4} |
| clean|push|random|band|4.0|a|None | 4 | 0% [0, 49] | 0.11 | {'A': 4} |
| clean|push|lens|band|4.0|b|None | 4 | 100% [51, 100] | 1.08 | {'b': 4} |
| clean|push|random|band|4.0|b|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|band|8.0|r|None | 4 | 100% [51, 100] | 0.78 | {'b': 4} |
| clean|push|random|band|8.0|r|None | 4 | 25% [5, 70] | 0.42 | {'other': 1, 'A': 2, 'b': 1} |
| clean|push|lens|band|8.0|a|None | 4 | 0% [0, 49] | 0.93 | {'other': 4} |
| clean|push|random|band|8.0|a|None | 4 | 0% [0, 49] | 0.33 | {'other': 4} |
| clean|push|lens|band|8.0|b|None | 4 | 100% [51, 100] | 1.07 | {'b': 4} |
| clean|push|random|band|8.0|b|None | 4 | 0% [0, 49] | 0.25 | {'A': 4} |
| clean|push|lens|band|16.0|r|None | 4 | 0% [0, 49] | 0.55 | {'other': 4} |
| clean|push|random|band|16.0|r|None | 4 | 0% [0, 49] | 0.39 | {'A': 3, 'other': 1} |
| clean|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | 1.18 | {'other': 4} |
| clean|push|random|band|16.0|a|None | 4 | 0% [0, 49] | 0.49 | {'other': 4} |
| clean|push|lens|band|16.0|b|None | 4 | 100% [51, 100] | 1.09 | {'b': 4} |
| clean|push|random|band|16.0|b|None | 4 | 0% [0, 49] | 0.45 | {'other': 3, 'A': 1} |
| clean|emb_diff|lens|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_diff|random|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_add|lens|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_add|random|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_diff|lens|-1|1.0|b|None | 4 | 100% [51, 100] | 0.84 | {'b': 4} |
| clean|emb_diff|random|-1|1.0|b|None | 4 | 0% [0, 49] | 0.18 | {'A': 4} |
| clean|emb_add|lens|-1|1.0|b|None | 4 | 100% [51, 100] | 0.82 | {'b': 4} |
| clean|emb_add|random|-1|1.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|emb_diff|lens|-1|4.0|b|None | 4 | 100% [51, 100] | 0.74 | {'b': 4} |
| clean|emb_diff|random|-1|4.0|b|None | 4 | 75% [30, 95] | 0.55 | {'b': 3, 'other': 1} |
| clean|emb_add|lens|-1|4.0|b|None | 4 | 100% [51, 100] | 1.08 | {'b': 4} |
| clean|emb_add|random|-1|4.0|b|None | 4 | 50% [15, 85] | 0.55 | {'other': 2, 'b': 2} |
| clean|copy|None|16|None|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|copy|None|20|None|r|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|copy|None|24|None|r|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|copy|None|28|None|r|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|copy|None|32|None|r|None | 4 | 0% [0, 49] | 0.15 | {'A': 4} |
| clean|copy|None|36|None|r|None | 4 | 75% [30, 95] | 0.57 | {'b': 3, 'A': 1} |
| clean|copy|None|40|None|r|None | 4 | 75% [30, 95] | 0.67 | {'b': 3, 'A': 1} |
| clean|copy|None|44|None|r|None | 4 | 100% [51, 100] | 0.73 | {'b': 4} |
| clean|copy|None|48|None|r|None | 4 | 100% [51, 100] | 0.80 | {'b': 4} |
| clean|patch|None|16|None|a|None | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|patch|None|16|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|16|4.0|a|None | 4 | 0% [0, 49] | 0.08 | {'A': 4} |
| clean|patch|None|16|8.0|a|None | 4 | 100% [51, 100] | 0.96 | {'b': 4} |
| clean|patch|None|16|16.0|a|None | 4 | 50% [15, 85] | 0.93 | {'b': 2, 'other': 2} |
| clean|patch|None|20|None|a|None | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|patch|None|20|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|20|4.0|a|None | 4 | 50% [15, 85] | 0.39 | {'b': 2, 'A': 2} |
| clean|patch|None|20|8.0|a|None | 4 | 100% [51, 100] | 0.96 | {'b': 4} |
| clean|patch|None|20|16.0|a|None | 4 | 25% [5, 70] | 0.94 | {'other': 3, 'b': 1} |
| clean|patch|None|24|None|a|None | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|patch|None|24|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|24|4.0|a|None | 4 | 50% [15, 85] | 0.56 | {'b': 2, 'A': 1, 'other': 1} |
| clean|patch|None|24|8.0|a|None | 4 | 100% [51, 100] | 0.98 | {'b': 4} |
| clean|patch|None|24|16.0|a|None | 4 | 0% [0, 49] | 0.88 | {'other': 4} |
| clean|patch|None|28|None|a|None | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|patch|None|28|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|28|4.0|a|None | 4 | 75% [30, 95] | 0.65 | {'b': 3, 'A': 1} |
| clean|patch|None|28|8.0|a|None | 4 | 100% [51, 100] | 0.97 | {'b': 4} |
| clean|patch|None|28|16.0|a|None | 4 | 0% [0, 49] | 0.90 | {'other': 4} |
| off|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|4.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 4} |
| off|push|lens|16|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 2, 'other': 2} |
| off|push|lens|16|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |
| off|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|4.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 4} |
| off|push|lens|20|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 2, 'other': 2} |
| off|push|lens|20|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |
| off|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|4.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 4} |
| off|push|lens|24|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 3, 'other': 1} |
| off|push|lens|24|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |
| off|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|28|4.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 4} |
| off|push|lens|28|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 2, 'other': 2} |
| off|push|lens|28|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |
| off|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|band|4.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |
| off|push|lens|band|8.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |
| off|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-insert: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-cue: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-unrelated: k -, J - (ref rate 0.00); W-copy*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.75); emb*: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); patch_matched: k -, J - (ref rate 0.00); low_margin: k -
K1 - -> untestable; gate -; K2 nb - a/2 +0.00 [+0.00, +0.00], b - nb +1.00 [+1.00, +1.00] -> inconclusive; K4 +0.02 [-0.03, +0.08]
JS(P*, .) {"clean": 0.491, "E-name": 0.586, "E-insert": 0.442, "E-cue": 0.526, "E-unrelated": 0.402}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [0.2995, 0.2488, 0.2267, 0.3169], "E-insert": [0.1663, 0.2963, 0.3526, 0.4323], "E-cue": [0.2241, 0.2809, 0.2633, 0.3879], "E-unrelated": [0.1782, 0.2101, 0.2495, 0.2181]}
transit proj on C's delta [44, 48, 52]: P*_b [0.5853, 0.6095, 0.6993], P* [0.4314, 0.4827, 0.5495], edits {"E-name": [0.6696, 0.6708, 0.7821], "E-insert": [0.5675, 0.574, 0.6045], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.2077, 0.2335, 0.2092]}

## B (W-copy* = ('clean', 'copy', None, 32, None, 'r', None))

| condition | n | flips [95% CI] | frac | roles |
|---|---|---|---|---|
| clean|none|None|None|None|None|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|edit|None|None|None|None|E-name | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|edit|None|None|None|None|E-insert | 4 | 100% [51, 100] | 0.53 | {'b': 4} |
| clean|edit|None|None|None|None|E-cue | 4 | 100% [51, 100] | 1.00 | {'b': 4} |
| clean|edit|None|None|None|None|E-unrelated | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|lens|16|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|16|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|16|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|16|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|4.0|r|None | 4 | 50% [15, 85] | 0.53 | {'other': 1, 'b': 2, 'A': 1} |
| clean|push|random|16|4.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|16|4.0|a|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|random|16|4.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|4.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|16|4.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|16|8.0|r|None | 4 | 75% [30, 95] | 0.63 | {'b': 3, 'A': 1} |
| clean|push|random|16|8.0|r|None | 4 | 0% [0, 49] | 0.13 | {'A': 3, 'other': 1} |
| clean|push|lens|16|8.0|a|None | 4 | 0% [0, 49] | 0.17 | {'A': 4} |
| clean|push|random|16|8.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|16|8.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|16|8.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|16|16.0|r|None | 4 | 100% [51, 100] | 0.82 | {'b': 4} |
| clean|push|random|16|16.0|r|None | 4 | 0% [0, 49] | 0.26 | {'A': 2, 'other': 2} |
| clean|push|lens|16|16.0|a|None | 4 | 25% [5, 70] | 0.65 | {'b': 1, 'other': 3} |
| clean|push|random|16|16.0|a|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|lens|16|16.0|b|None | 4 | 50% [15, 85] | 0.53 | {'other': 1, 'b': 2, 'A': 1} |
| clean|push|random|16|16.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|20|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|20|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|20|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|4.0|r|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|push|random|20|4.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|20|4.0|a|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|random|20|4.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|20|4.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|20|4.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|8.0|r|None | 4 | 50% [15, 85] | 0.47 | {'A': 2, 'b': 2} |
| clean|push|random|20|8.0|r|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|lens|20|8.0|a|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|push|random|20|8.0|a|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|20|8.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|20|8.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|20|16.0|r|None | 4 | 50% [15, 85] | 0.76 | {'other': 1, 'b': 2, 'A': 1} |
| clean|push|random|20|16.0|r|None | 4 | 0% [0, 49] | 0.20 | {'A': 4} |
| clean|push|lens|20|16.0|a|None | 4 | 0% [0, 49] | 0.21 | {'A': 4} |
| clean|push|random|20|16.0|a|None | 4 | 0% [0, 49] | 0.08 | {'A': 4} |
| clean|push|lens|20|16.0|b|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|random|20|16.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|24|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|24|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|24|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|24|4.0|r|None | 4 | 0% [0, 49] | 0.24 | {'A': 4} |
| clean|push|random|24|4.0|r|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|lens|24|4.0|a|None | 4 | 0% [0, 49] | 0.10 | {'A': 4} |
| clean|push|random|24|4.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|4.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|random|24|4.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|8.0|r|None | 4 | 25% [5, 70] | 0.53 | {'A': 2, 'other': 1, 'b': 1} |
| clean|push|random|24|8.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|24|8.0|a|None | 4 | 0% [0, 49] | 0.24 | {'A': 4} |
| clean|push|random|24|8.0|a|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|lens|24|8.0|b|None | 4 | 0% [0, 49] | 0.07 | {'A': 4} |
| clean|push|random|24|8.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|24|16.0|r|None | 4 | 75% [30, 95] | 0.83 | {'b': 3, 'other': 1} |
| clean|push|random|24|16.0|r|None | 4 | 0% [0, 49] | 0.18 | {'A': 4} |
| clean|push|lens|24|16.0|a|None | 4 | 0% [0, 49] | 0.34 | {'A': 3, 'other': 1} |
| clean|push|random|24|16.0|a|None | 4 | 0% [0, 49] | 0.12 | {'A': 4} |
| clean|push|lens|24|16.0|b|None | 4 | 0% [0, 49] | 0.25 | {'A': 4} |
| clean|push|random|24|16.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|28|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|28|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|28|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|28|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|28|4.0|r|None | 4 | 0% [0, 49] | 0.36 | {'A': 4} |
| clean|push|random|28|4.0|r|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|28|4.0|a|None | 4 | 0% [0, 49] | 0.17 | {'A': 4} |
| clean|push|random|28|4.0|a|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|lens|28|4.0|b|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|push|random|28|4.0|b|None | 4 | 0% [0, 49] | -0.00 | {'A': 4} |
| clean|push|lens|28|8.0|r|None | 4 | 100% [51, 100] | 0.82 | {'b': 4} |
| clean|push|random|28|8.0|r|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|push|lens|28|8.0|a|None | 4 | 25% [5, 70] | 0.40 | {'b': 1, 'A': 2, 'other': 1} |
| clean|push|random|28|8.0|a|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|push|lens|28|8.0|b|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|push|random|28|8.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|28|16.0|r|None | 4 | 75% [30, 95] | 1.03 | {'b': 3, 'other': 1} |
| clean|push|random|28|16.0|r|None | 4 | 0% [0, 49] | 0.30 | {'A': 4} |
| clean|push|lens|28|16.0|a|None | 4 | 75% [30, 95] | 0.77 | {'b': 3, 'other': 1} |
| clean|push|random|28|16.0|a|None | 4 | 0% [0, 49] | 0.13 | {'A': 4} |
| clean|push|lens|28|16.0|b|None | 4 | 0% [0, 49] | 0.26 | {'A': 3, 'other': 1} |
| clean|push|random|28|16.0|b|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|band|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|band|0.0|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|band|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|band|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|random|band|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|band|4.0|r|None | 4 | 100% [51, 100] | 1.02 | {'b': 4} |
| clean|push|random|band|4.0|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|band|4.0|a|None | 4 | 25% [5, 70] | 0.45 | {'b': 1, 'A': 3} |
| clean|push|random|band|4.0|a|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|push|lens|band|4.0|b|None | 4 | 0% [0, 49] | 0.21 | {'A': 4} |
| clean|push|random|band|4.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|push|lens|band|8.0|r|None | 4 | 100% [51, 100] | 1.13 | {'b': 4} |
| clean|push|random|band|8.0|r|None | 4 | 0% [0, 49] | 0.24 | {'A': 3, 'oc': 1} |
| clean|push|lens|band|8.0|a|None | 4 | 25% [5, 70] | 0.97 | {'other': 3, 'b': 1} |
| clean|push|random|band|8.0|a|None | 4 | 0% [0, 49] | 0.13 | {'A': 4} |
| clean|push|lens|band|8.0|b|None | 4 | 100% [51, 100] | 0.82 | {'b': 4} |
| clean|push|random|band|8.0|b|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|push|lens|band|16.0|r|None | 4 | 25% [5, 70] | 0.98 | {'other': 3, 'b': 1} |
| clean|push|random|band|16.0|r|None | 4 | 25% [5, 70] | 0.46 | {'other': 1, 'oc': 1, 'b': 1, 'A': 1} |
| clean|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | 0.99 | {'other': 4} |
| clean|push|random|band|16.0|a|None | 4 | 0% [0, 49] | 0.21 | {'A': 2, 'other': 2} |
| clean|push|lens|band|16.0|b|None | 4 | 100% [51, 100] | 1.02 | {'b': 4} |
| clean|push|random|band|16.0|b|None | 4 | 0% [0, 49] | 0.10 | {'A': 4} |
| clean|emb_diff|lens|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_diff|random|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_add|lens|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_add|random|-1|0.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_diff|lens|-1|1.0|b|None | 4 | 0% [0, 49] | 0.21 | {'A': 4} |
| clean|emb_diff|random|-1|1.0|b|None | 4 | 0% [0, 49] | 0.06 | {'A': 4} |
| clean|emb_add|lens|-1|1.0|b|None | 4 | 25% [5, 70] | 0.34 | {'A': 3, 'b': 1} |
| clean|emb_add|random|-1|1.0|b|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|emb_diff|lens|-1|4.0|b|None | 4 | 100% [51, 100] | 0.77 | {'b': 4} |
| clean|emb_diff|random|-1|4.0|b|None | 4 | 0% [0, 49] | 0.50 | {'other': 4} |
| clean|emb_add|lens|-1|4.0|b|None | 4 | 100% [51, 100] | 0.96 | {'b': 4} |
| clean|emb_add|random|-1|4.0|b|None | 4 | 25% [5, 70] | 0.50 | {'other': 3, 'b': 1} |
| clean|copy|None|16|None|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|copy|None|20|None|r|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|copy|None|24|None|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|copy|None|28|None|r|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|copy|None|32|None|r|None | 4 | 0% [0, 49] | 0.02 | {'A': 4} |
| clean|copy|None|36|None|r|None | 4 | 0% [0, 49] | 0.20 | {'A': 4} |
| clean|copy|None|40|None|r|None | 4 | 100% [51, 100] | 0.59 | {'b': 4} |
| clean|copy|None|44|None|r|None | 4 | 100% [51, 100] | 0.65 | {'b': 4} |
| clean|copy|None|48|None|r|None | 4 | 100% [51, 100] | 0.68 | {'b': 4} |
| clean|patch|None|16|None|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|16|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|16|4.0|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|patch|None|16|8.0|a|None | 4 | 0% [0, 49] | 0.05 | {'A': 4} |
| clean|patch|None|16|16.0|a|None | 4 | 0% [0, 49] | 0.08 | {'A': 4} |
| clean|patch|None|20|None|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|20|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|20|4.0|a|None | 4 | 0% [0, 49] | 0.03 | {'A': 4} |
| clean|patch|None|20|8.0|a|None | 4 | 0% [0, 49] | 0.10 | {'A': 4} |
| clean|patch|None|20|16.0|a|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|patch|None|24|None|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|patch|None|24|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|24|4.0|a|None | 4 | 0% [0, 49] | 0.04 | {'A': 4} |
| clean|patch|None|24|8.0|a|None | 4 | 0% [0, 49] | 0.11 | {'A': 4} |
| clean|patch|None|24|16.0|a|None | 4 | 0% [0, 49] | 0.26 | {'A': 4} |
| clean|patch|None|28|None|a|None | 4 | 0% [0, 49] | 0.01 | {'A': 4} |
| clean|patch|None|28|0.0|a|None | 4 | 0% [0, 49] | 0.00 | {'A': 4} |
| clean|patch|None|28|4.0|a|None | 4 | 0% [0, 49] | 0.09 | {'A': 4} |
| clean|patch|None|28|8.0|a|None | 4 | 0% [0, 49] | 0.24 | {'A': 4} |
| clean|patch|None|28|16.0|a|None | 4 | 0% [0, 49] | 0.52 | {'A': 2, 'other': 2} |
| off|push|lens|16|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|8.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|16|16.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 1, 'other': 3} |
| off|push|lens|20|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|8.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|20|16.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|8.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|24|16.0|a|None | 4 | 0% [0, 49] | nan | {'A': 3, 'other': 1} |
| off|push|lens|28|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|28|4.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|28|8.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 1, 'A': 2, 'other': 1} |
| off|push|lens|28|16.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 3, 'other': 1} |
| off|push|lens|band|0.0|a|None | 4 | 0% [0, 49] | nan | {'A': 4} |
| off|push|lens|band|4.0|a|None | 4 | 0% [0, 49] | nan | {'bO': 2, 'A': 2} |
| off|push|lens|band|8.0|a|None | 4 | 0% [0, 49] | nan | {'other': 3, 'bO': 1} |
| off|push|lens|band|16.0|a|None | 4 | 0% [0, 49] | nan | {'other': 4} |

Agreement with P* (kappa / Jaccard, item bootstrap): E-name: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-insert: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-cue: k -, J +0.00 [+0.00, +0.00] (ref rate 1.00); E-unrelated: k -, J - (ref rate 0.00); W-copy*: k -, J - (ref rate 0.00); emb*: k -, J +0.00 [+0.00, +0.00] (ref rate 0.25); patch_matched: k -, J - (ref rate 0.00); low_margin: k -
K1 - -> untestable; gate -; K2 nb - a/2 +0.00 [+0.00, +0.00], b - nb +0.00 [+0.00, +0.00] -> inconclusive; K4 -0.11 [-0.15, -0.08]
JS(P*, .) {"clean": 0.145, "E-name": 0.581, "E-insert": 0.256, "E-cue": 0.571, "E-unrelated": 0.121}
cos final (b, per down layer [32, 40, 48, 56]): {"E-name": [0.0872, 0.025, 0.0127, 0.0415], "E-insert": [0.2937, 0.4036, 0.3916, 0.3695], "E-cue": [0.1302, 0.1971, 0.1571, 0.1893], "E-unrelated": [0.2688, 0.3016, 0.2853, 0.3204]}
transit proj on C's delta [44, 48, 52]: P*_b [0.3227, 0.2857, 0.2855], P* [0.3936, 0.3604, 0.3633], edits {"E-name": [0.6182, 0.6017, 0.7359], "E-insert": [0.6077, 0.5804, 0.6207], "E-cue": [1.0, 1.0, 1.0], "E-unrelated": [0.1689, 0.169, 0.1019]}

## Plain-text loss under the push (nats)

{"none": 2.3307, "lens/16/x0": 2.3307, "random/16/x0": 2.3307, "lens/16/x4": 2.3511, "random/16/x4": 2.3351, "lens/16/x8": 2.6504, "random/16/x8": 2.3643, "lens/16/x16": 5.8234, "random/16/x16": 2.4904, "lens/20/x0": 2.3307, "random/20/x0": 2.3307, "lens/20/x4": 2.3495, "random/20/x4": 2.3307, "lens/20/x8": 2.4604, "random/20/x8": 2.3486, "lens/20/x16": 3.1034, "random/20/x16": 2.546, "lens/24/x0": 2.3307, "random/24/x0": 2.3307, "lens/24/x4": 2.3807, "random/24/x4": 2.3371, "lens/24/x8": 2.6221, "random/24/x8": 2.3865, "lens/24/x16": 3.2952, "random/24/x16": 2.7003, "lens/28/x0": 2.3307, "random/28/x0": 2.3307, "lens/28/x4": 2.4677, "random/28/x4": 2.3674, "lens/28/x8": 2.9343, "random/28/x8": 2.4559, "lens/28/x16": 4.6083, "random/28/x16": 3.008, "lens/band/x0": 2.3307, "random/band/x0": 2.3307, "lens/band/x4": 3.4106, "random/band/x4": 2.3693, "lens/band/x8": 6.5166, "random/band/x8": 2.7203, "lens/band/x16": 10.0775, "random/band/x16": 5.6564}

## Diagnostics

{"max_none_vs_clean_logit": 0.375, "max_zero_scale_vs_none_logit": 0.0, "n_zero_scale": 1512}
