# Mass-mean address (A) and value (V) subspaces: remove or keep only (muse30b_x0_massmean_grid, mode grid)

Descriptive, added after data (Dan, 24 Oct ~20:05; layout-free arm ~21:50); not part of X0's rule. Model muse-glimmer-30b, layer 26, 68 single-change items of muse30b_x0_single (both locker sentences before the pick); A rank 4, V rank 8, span(A, V) rank 12, layout-free A (Alf) rank 4 from 657 states in 31 layout groups (0 single-item groups dropped; A-Alf overlap, mean squared cosine of the principal angles, 0.658), from muse30b_x0_probe_v4 (locker-before, n = 657). Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| reader | S_whole | arm | median share of ‖Δ‖² | S_arm | S_rand | dependence | random dependence | excess |
|---|---|---|---|---|---|---|---|---|
| lookup | 0.99 (67) | remove A | 0.1177 | 0.82 | 0.97 | 0.16 [0.07, 0.27] | 0.01 [0.00, 0.05] | 0.15 [0.06, 0.25] |
| lookup | 0.99 (67) | remove V | 0.0907 | 0.96 | 0.97 | 0.03 [0.00, 0.07] | 0.01 [0.00, 0.05] | 0.01 [0.00, 0.04] |
| lookup | 0.99 (67) | remove Alf | 0.1478 | 0.63 | 0.97 | 0.36 [0.26, 0.47] | 0.01 [0.00, 0.05] | 0.34 [0.24, 0.46] |
| lookup | 0.99 (67) | remove pca | 0.1512 | 0.82 | 0.97 | 0.16 [0.09, 0.26] | 0.01 [0.00, 0.05] | 0.15 [0.07, 0.25] |
| lookup | 0.99 (67) | keep only A | 0.1177 | 0.06 | 0.00 | kept / whole 0.06 [0.00, 0.12] | random kept / whole 0.00 [0.00, 0.00] | 0.06 [0.00, 0.12] |
| lookup | 0.99 (67) | keep only V | 0.0907 | 0.00 | 0.00 | kept / whole 0.00 [0.00, 0.00] | random kept / whole 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| lookup | 0.99 (67) | keep only Alf | 0.1478 | 0.24 | 0.01 | kept / whole 0.24 [0.14, 0.34] | random kept / whole 0.01 [0.00, 0.05] | 0.22 [0.13, 0.33] |
| recall | 0.56 (38) | remove A | 0.1177 | 0.56 | 0.56 | 0.00 [-0.17, 0.14] | 0.00 [-0.11, 0.12] | 0.00 [-0.17, 0.14] |
| recall | 0.56 (38) | remove V | 0.0907 | 0.59 | 0.59 | -0.05 [-0.17, 0.05] | -0.05 [-0.17, 0.05] | 0.00 [-0.08, 0.08] |
| recall | 0.56 (38) | remove Alf | 0.1478 | 0.53 | 0.57 | 0.05 [-0.16, 0.25] | -0.03 [-0.12, 0.07] | 0.08 [-0.10, 0.26] |
| recall | 0.56 (38) | remove pca | 0.1512 | 0.49 | 0.59 | 0.13 [-0.02, 0.28] | -0.05 [-0.17, 0.05] | 0.18 [0.04, 0.34] |
| recall | 0.56 (38) | keep only A | 0.1177 | 0.00 | 0.00 | kept / whole 0.00 [0.00, 0.00] | random kept / whole 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| recall | 0.56 (38) | keep only V | 0.0907 | 0.00 | 0.00 | kept / whole 0.00 [0.00, 0.00] | random kept / whole 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| recall | 0.56 (38) | keep only Alf | 0.1478 | 0.03 | 0.00 | kept / whole 0.05 [0.00, 0.15] | random kept / whole 0.00 [0.00, 0.00] | 0.05 [0.00, 0.15] |

Rule (Dan, 25 Oct ~00:20, the 9B / 27B thresholds; batch 31's Q31.5): Alf removed is (a) lookup-specific iff lookup excess >= 0.20 (lower CI > 0) and recall <= 0.10 or at most half the lookup's; (b) both readers iff both lose >= 0.10 and not (a); (c) neither iff the lookup's lower CI <= 0; else (d). This run: lookup 0.34 [0.24, 0.46], recall 0.08 [-0.10, 0.26] -> (a) lookup-specific.
