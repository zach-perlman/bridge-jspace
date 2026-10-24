# Mass-mean address (A) and value (V) subspaces: remove or keep only (qwen35_9b_x0_massmean)

Descriptive, added after data (Dan, 24 Oct ~20:05); not part of X0's rule. Model qwen3.5-9b, layer 12, 73 single-change items of qwen35_9b_x0_single_r2 (both locker sentences before the pick); A rank 4, V rank 8, span(A, V) rank 12, from qwen35_9b_x0_probe_v4 (locker-before, n = 758). Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| reader | S_whole | arm | median share of ‖Δ‖² | S_arm | S_rand | dependence | random dependence | excess |
|---|---|---|---|---|---|---|---|---|
| lookup | 0.99 (72) | remove A | 0.1512 | 0.66 | 0.96 | 0.33 [0.20, 0.48] | 0.03 [0.00, 0.07] | 0.31 [0.18, 0.44] |
| lookup | 0.99 (72) | remove V | 0.1271 | 0.97 | 0.97 | 0.01 [0.00, 0.05] | 0.01 [0.00, 0.05] | 0.00 [0.00, 0.00] |
| lookup | 0.99 (72) | remove AV | 0.2295 | 0.51 | 0.96 | 0.49 [0.37, 0.61] | 0.03 [0.00, 0.07] | 0.46 [0.35, 0.58] |
| lookup | 0.99 (72) | keep only (A + V) | 0.2295 | 0.40 | 0.00 | kept / whole 0.40 [0.29, 0.53] | random kept / whole 0.00 [0.00, 0.00] | 0.40 [0.29, 0.53] |
| recall | 0.99 (72) | remove A | 0.1512 | 0.86 | 0.97 | 0.12 [0.05, 0.21] | 0.01 [-0.03, 0.06] | 0.11 [0.04, 0.19] |
| recall | 0.99 (72) | remove V | 0.1271 | 0.96 | 0.97 | 0.03 [-0.03, 0.08] | 0.01 [-0.03, 0.06] | 0.01 [0.00, 0.05] |
| recall | 0.99 (72) | remove AV | 0.2295 | 0.74 | 0.93 | 0.25 [0.14, 0.36] | 0.06 [0.00, 0.12] | 0.19 [0.10, 0.30] |
| recall | 0.99 (72) | keep only (A + V) | 0.2295 | 0.11 | 0.00 | kept / whole 0.11 [0.04, 0.19] | random kept / whole 0.00 [0.00, 0.00] | 0.11 [0.04, 0.19] |

Pre-stated reading (Dan): the lookup loses flips under A (or V) while the recall does not -> 'the lookup uses the address (or the value)'; no arm changes the lookup -> 'the lookup's channel is not a low-rank linear readout of the address or the value; what it is stays open'.
