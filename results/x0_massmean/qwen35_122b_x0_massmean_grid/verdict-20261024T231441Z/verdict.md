# Mass-mean address (A) and value (V) subspaces: remove or keep only (qwen35_122b_x0_massmean_grid, mode grid)

Descriptive, added after data (Dan, 24 Oct ~20:05; layout-free arm ~21:50); not part of X0's rule. Model qwen3.5-122b-a10b, layer 33, 54 single-change items of qwen35_122b_x0_single (both locker sentences before the pick); A rank 4, V rank 8, span(A, V) rank 12, layout-free A (Alf) rank 4 from 758 states in 31 layout groups (0 single-item groups dropped; A-Alf overlap, mean squared cosine of the principal angles, 0.718), from qwen35_122b_x0_probe_v4 (locker-before, n = 758). Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| reader | S_whole | arm | median share of ‖Δ‖² | S_arm | S_rand | dependence | random dependence | excess |
|---|---|---|---|---|---|---|---|---|
| lookup | 1.00 (54) | remove A | 0.1812 | 0.76 | 1.00 | 0.24 [0.13, 0.37] | 0.00 [0.00, 0.00] | 0.24 [0.13, 0.37] |
| lookup | 1.00 (54) | remove V | 0.1232 | 1.00 | 1.00 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| lookup | 1.00 (54) | remove Alf | 0.1751 | 0.69 | 1.00 | 0.31 [0.20, 0.43] | 0.00 [0.00, 0.00] | 0.31 [0.20, 0.43] |
| lookup | 1.00 (54) | remove pca | 0.1774 | 0.94 | 1.00 | 0.06 [0.00, 0.12] | 0.00 [0.00, 0.00] | 0.06 [0.00, 0.12] |
| lookup | 1.00 (54) | keep only A | 0.1812 | 0.22 | 0.00 | kept / whole 0.22 [0.13, 0.30] | random kept / whole 0.00 [0.00, 0.00] | 0.22 [0.13, 0.30] |
| lookup | 1.00 (54) | keep only V | 0.1232 | 0.02 | 0.00 | kept / whole 0.02 [0.00, 0.05] | random kept / whole 0.00 [0.00, 0.00] | 0.02 [0.00, 0.05] |
| lookup | 1.00 (54) | keep only Alf | 0.1751 | 0.24 | 0.00 | kept / whole 0.24 [0.15, 0.32] | random kept / whole 0.00 [0.00, 0.00] | 0.24 [0.15, 0.32] |
| recall | 0.96 (52) | remove A | 0.1812 | 0.89 | 0.96 | 0.08 [0.00, 0.18] | 0.00 [-0.05, 0.06] | 0.08 [0.02, 0.16] |
| recall | 0.96 (52) | remove V | 0.1232 | 0.91 | 0.93 | 0.06 [-0.02, 0.14] | 0.04 [0.00, 0.10] | 0.02 [-0.07, 0.10] |
| recall | 0.96 (52) | remove Alf | 0.1751 | 0.81 | 0.94 | 0.15 [0.06, 0.28] | 0.02 [0.00, 0.07] | 0.13 [0.02, 0.26] |
| recall | 0.96 (52) | remove pca | 0.1774 | 0.87 | 0.94 | 0.10 [0.03, 0.17] | 0.02 [0.00, 0.07] | 0.08 [0.02, 0.14] |
| recall | 0.96 (52) | keep only A | 0.1812 | 0.07 | 0.00 | kept / whole 0.08 [0.02, 0.15] | random kept / whole 0.00 [0.00, 0.00] | 0.08 [0.02, 0.15] |
| recall | 0.96 (52) | keep only V | 0.1232 | 0.02 | 0.00 | kept / whole 0.02 [0.00, 0.07] | random kept / whole 0.00 [0.00, 0.00] | 0.02 [0.00, 0.07] |
| recall | 0.96 (52) | keep only Alf | 0.1751 | 0.09 | 0.00 | kept / whole 0.10 [0.02, 0.17] | random kept / whole 0.00 [0.00, 0.00] | 0.10 [0.02, 0.17] |

Rule (Dan, 25 Oct ~00:20, the 9B / 27B thresholds; batch 31's Q31.5): Alf removed is (a) lookup-specific iff lookup excess >= 0.20 (lower CI > 0) and recall <= 0.10 or at most half the lookup's; (b) both readers iff both lose >= 0.10 and not (a); (c) neither iff the lookup's lower CI <= 0; else (d). This run: lookup 0.31 [0.20, 0.43], recall 0.13 [0.02, 0.26] -> (a) lookup-specific.
