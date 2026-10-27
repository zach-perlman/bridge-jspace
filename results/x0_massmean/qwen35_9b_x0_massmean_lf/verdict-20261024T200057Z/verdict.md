# Mass-mean address (A) and value (V) subspaces: remove or keep only (qwen35_9b_x0_massmean_lf, mode layout_free)

Descriptive, added after data (Dan, 24 Oct ~20:05; layout-free arm ~21:50); not part of X0's rule. Model qwen3.5-9b, layer 12, 73 single-change items of qwen35_9b_x0_single_r2 (both locker sentences before the pick); A rank 4, V rank 8, span(A, V) rank 12, layout-free A (Alf) rank 4 from 758 states in 31 layout groups (0 single-item groups dropped; A-Alf overlap, mean squared cosine of the principal angles, 0.725), from qwen35_9b_x0_probe_v4 (locker-before, n = 758). Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| reader | S_whole | arm | median share of ‖Δ‖² | S_arm | S_rand | dependence | random dependence | excess |
|---|---|---|---|---|---|---|---|---|
| lookup | 0.99 (72) | remove A | 0.1512 | 0.66 | 0.96 | 0.33 [0.20, 0.48] | 0.03 [0.00, 0.07] | 0.31 [0.18, 0.44] |
| lookup | 0.99 (72) | remove Alf | 0.1774 | 0.51 | 0.99 | 0.49 [0.38, 0.59] | 0.00 [0.00, 0.00] | 0.49 [0.38, 0.59] |
| lookup | 0.99 (72) | keep only A | 0.1512 | 0.25 | 0.00 | kept / whole 0.25 [0.15, 0.36] | random kept / whole 0.00 [0.00, 0.00] | 0.25 [0.15, 0.36] |
| lookup | 0.99 (72) | keep only Alf | 0.1774 | 0.36 | 0.00 | kept / whole 0.36 [0.25, 0.48] | random kept / whole 0.00 [0.00, 0.00] | 0.36 [0.25, 0.48] |
| recall | 0.99 (72) | remove A | 0.1512 | 0.86 | 0.97 | 0.12 [0.05, 0.21] | 0.01 [-0.03, 0.06] | 0.11 [0.04, 0.19] |
| recall | 0.99 (72) | remove Alf | 0.1774 | 0.81 | 0.93 | 0.18 [0.10, 0.26] | 0.06 [0.00, 0.12] | 0.12 [0.05, 0.21] |
| recall | 0.99 (72) | keep only A | 0.1512 | 0.04 | 0.00 | kept / whole 0.04 [0.00, 0.09] | random kept / whole 0.00 [0.00, 0.00] | 0.04 [0.00, 0.09] |
| recall | 0.99 (72) | keep only Alf | 0.1774 | 0.07 | 0.00 | kept / whole 0.07 [0.02, 0.13] | random kept / whole 0.00 [0.00, 0.00] | 0.07 [0.02, 0.13] |

Pre-stated reading (Dan, ~21:50; no prediction committed before the run): if the 9B lookup effect disappears with the layout-free A, the reading is 'position information', not 'address'. 'Disappears' (set by the agent before the run, Q28.1's criterion): the lookup's excess with Alf removed has a lower CI <= 0. This run: 0.49 [0.38, 0.59] -> does not disappear.
