# Probe-(b) subspace: remove it, or keep only it (x0_amnesic_27b)

Descriptive, added after data (Dan, 24 Oct ~18:45, item 6); not part of X0's rule. Model qwen3.6-27b, layer 32, single-change items of x0_single_27b_r2; probe subspace rank 4 from x0_probe_v4_27b (locker-before, n = 758, CV accuracy 0.99). Bootstrap over bridge entities, 10000 resamples. UNVERIFIED.

| locker vs pick | reader | n | median share of ‖Δ‖² in P | S_whole | S_no_probe | S_no_rand | probe dep. | random dep. | excess | S_probe_only / S_whole | S_rand_only / S_whole | difference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| before | lookup | 103 | 0.0136 | 0.81 (83) | 0.81 | 0.81 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| before | recall | 103 | 0.0136 | 0.73 (75) | 0.73 | 0.74 | 0.00 [-0.04, 0.03] | -0.01 [-0.05, 0.00] | 0.01 [0.00, 0.04] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| after | lookup | 97 | 0.0015 | 0.12 (12 ⚠) | 0.13 | 0.13 | -0.08 [-0.40, 0.00] | -0.08 [-0.40, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| after | recall | 97 | 0.0015 | 0.73 (71) | 0.73 | 0.73 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

⚠ = fewer than 30 items switched by the whole edit.
