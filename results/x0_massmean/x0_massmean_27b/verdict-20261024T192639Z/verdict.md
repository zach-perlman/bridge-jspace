# Mass-mean address (A) and value (V) subspaces: remove or keep only (x0_massmean_27b)

Descriptive, added after data (Dan, 24 Oct ~20:05); not part of X0's rule. Model qwen3.6-27b, layer 32, 70 single-change items of x0_single_27b_r2 (both locker sentences before the pick); A rank 4, V rank 8, span(A, V) rank 12, from x0_probe_v4_27b (locker-before, n = 758). Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| reader | S_whole | arm | median share of ‖Δ‖² | S_arm | S_rand | dependence | random dependence | excess |
|---|---|---|---|---|---|---|---|---|
| lookup | 1.00 (70) | remove A | 0.1600 | 0.96 | 1.00 | 0.04 [0.00, 0.09] | 0.00 [0.00, 0.00] | 0.04 [0.00, 0.09] |
| lookup | 1.00 (70) | remove V | 0.1499 | 1.00 | 0.99 | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.05] | -0.01 [-0.05, 0.00] |
| lookup | 1.00 (70) | remove AV | 0.2329 | 0.81 | 0.96 | 0.19 [0.10, 0.28] | 0.04 [0.00, 0.09] | 0.14 [0.06, 0.24] |
| lookup | 1.00 (70) | keep only (A + V) | 0.2329 | 0.06 | 0.01 | kept / whole 0.06 [0.00, 0.13] | random kept / whole 0.01 [0.00, 0.05] | 0.04 [0.00, 0.10] |
| recall | 0.70 (49) | remove A | 0.1600 | 0.61 | 0.69 | 0.12 [0.02, 0.22] | 0.02 [-0.05, 0.09] | 0.10 [0.00, 0.19] |
| recall | 0.70 (49) | remove V | 0.1499 | 0.69 | 0.69 | 0.02 [0.00, 0.07] | 0.02 [-0.05, 0.09] | 0.00 [-0.08, 0.08] |
| recall | 0.70 (49) | remove AV | 0.2329 | 0.51 | 0.66 | 0.27 [0.14, 0.42] | 0.06 [-0.02, 0.14] | 0.20 [0.06, 0.37] |
| recall | 0.70 (49) | keep only (A + V) | 0.2329 | 0.00 | 0.01 | kept / whole 0.00 [0.00, 0.00] | random kept / whole 0.02 [0.00, 0.06] | -0.02 [-0.06, 0.00] |

Pre-stated reading (Dan): the lookup loses flips under A (or V) while the recall does not -> 'the lookup uses the address (or the value)'; no arm changes the lookup -> 'the lookup's channel is not a low-rank linear readout of the address or the value; what it is stays open'.
