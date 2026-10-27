# Mass-mean address (A) and value (V) subspaces: remove or keep only (x0_massmean_lf_27b, mode layout_free)

Descriptive, added after data (Dan, 24 Oct ~20:05; layout-free arm ~21:50); not part of X0's rule. Model qwen3.6-27b, layer 32, 70 single-change items of x0_single_27b_r2 (both locker sentences before the pick); A rank 4, V rank 8, span(A, V) rank 12, layout-free A (Alf) rank 4 from 758 states in 31 layout groups (0 single-item groups dropped; A-Alf overlap, mean squared cosine of the principal angles, 0.712), from x0_probe_v4_27b (locker-before, n = 758). Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| reader | S_whole | arm | median share of ‖Δ‖² | S_arm | S_rand | dependence | random dependence | excess |
|---|---|---|---|---|---|---|---|---|
| lookup | 1.00 (70) | remove A | 0.1600 | 0.96 | 1.00 | 0.04 [0.00, 0.09] | 0.00 [0.00, 0.00] | 0.04 [0.00, 0.09] |
| lookup | 1.00 (70) | remove Alf | 0.1520 | 0.84 | 0.99 | 0.16 [0.07, 0.25] | 0.01 [0.00, 0.05] | 0.14 [0.07, 0.22] |
| lookup | 1.00 (70) | keep only A | 0.1600 | 0.00 | 0.00 | kept / whole 0.00 [0.00, 0.00] | random kept / whole 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| lookup | 1.00 (70) | keep only Alf | 0.1520 | 0.09 | 0.01 | kept / whole 0.09 [0.02, 0.17] | random kept / whole 0.01 [0.00, 0.05] | 0.07 [0.02, 0.14] |
| recall | 0.70 (49) | remove A | 0.1600 | 0.61 | 0.69 | 0.12 [0.02, 0.22] | 0.02 [-0.05, 0.09] | 0.10 [0.00, 0.19] |
| recall | 0.70 (49) | remove Alf | 0.1520 | 0.57 | 0.69 | 0.18 [0.07, 0.28] | 0.02 [-0.05, 0.09] | 0.16 [0.02, 0.31] |
| recall | 0.70 (49) | keep only A | 0.1600 | 0.00 | 0.00 | kept / whole 0.00 [0.00, 0.00] | random kept / whole 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| recall | 0.70 (49) | keep only Alf | 0.1520 | 0.00 | 0.01 | kept / whole 0.00 [0.00, 0.00] | random kept / whole 0.02 [0.00, 0.06] | -0.02 [-0.06, 0.00] |

Pre-stated reading (Dan, ~21:50; no prediction committed before the run): if the 9B lookup effect disappears with the layout-free A, the reading is 'position information', not 'address'. 'Disappears' (set by the agent before the run, Q28.1's criterion): the lookup's excess with Alf removed has a lower CI <= 0. This run: 0.14 [0.07, 0.22] -> does not disappear (the reading is stated for the 9B; reported here only).
