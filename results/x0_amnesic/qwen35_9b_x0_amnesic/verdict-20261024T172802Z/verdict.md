# Probe-(b) subspace: remove it, or keep only it (qwen35_9b_x0_amnesic)

Descriptive, added after data (Dan, 24 Oct ~18:45, item 6); not part of X0's rule. Model qwen3.5-9b, layer 12, single-change items of qwen35_9b_x0_single_r2; probe subspace rank 4 from qwen35_9b_x0_probe_v4 (locker-before, n = 758, CV accuracy 0.97). Bootstrap over bridge entities, 10000 resamples. UNVERIFIED.

| locker vs pick | reader | n | median share of ‖Δ‖² in P | S_whole | S_no_probe | S_no_rand | probe dep. | random dep. | excess | S_probe_only / S_whole | S_rand_only / S_whole | difference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| before | lookup | 100 | 0.0219 | 0.87 (87) | 0.83 | 0.87 | 0.05 [0.00, 0.10] | 0.00 [0.00, 0.00] | 0.05 [0.00, 0.10] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| before | recall | 100 | 0.0219 | 0.98 (98) | 0.97 | 0.98 | 0.01 [0.00, 0.04] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.04] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| after | lookup | 100 | 0.0010 | 0.19 (19 ⚠) | 0.17 | 0.19 | 0.11 [0.00, 0.28] | 0.00 [-0.18, 0.14] | 0.11 [0.00, 0.31] | 0.05 [0.00, 0.16] | 0.05 [0.00, 0.16] | 0.00 [0.00, 0.00] |
| after | recall | 100 | 0.0010 | 0.93 (93) | 0.93 | 0.93 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

⚠ = fewer than 30 items switched by the whole edit.
