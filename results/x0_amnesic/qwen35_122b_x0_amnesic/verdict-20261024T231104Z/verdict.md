# Probe-(b) subspace: remove it, or keep only it (qwen35_122b_x0_amnesic)

Descriptive, added after data (Dan, 24 Oct ~18:45, item 6); not part of X0's rule. Model qwen3.5-122b-a10b, layer 33, single-change items of qwen35_122b_x0_single; probe subspace rank 4 from qwen35_122b_x0_probe_v4 (locker-before, n = 758, CV accuracy 0.92). Bootstrap over bridge entities, 10000 resamples. UNVERIFIED.

| locker vs pick | reader | n | median share of ‖Δ‖² in P | S_whole | S_no_probe | S_no_rand | probe dep. | random dep. | excess | S_probe_only / S_whole | S_rand_only / S_whole | difference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| before | lookup | 85 | 0.0204 | 0.95 (81) | 0.94 | 0.94 | 0.01 [0.00, 0.04] | 0.01 [0.00, 0.04] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| before | recall | 85 | 0.0204 | 0.94 (80) | 0.96 | 0.95 | -0.03 [-0.06, 0.00] | -0.01 [-0.05, 0.00] | -0.01 [-0.04, 0.00] | 0.01 [0.00, 0.05] | 0.01 [0.00, 0.05] | 0.00 [0.00, 0.00] |
| after | lookup | 115 | 0.0011 | 0.11 (13 ⚠) | 0.10 | 0.13 | 0.08 [0.00, 0.22] | -0.15 [-0.67, 0.11] | 0.23 [0.00, 0.70] | 0.00 [0.00, 0.00] | 0.08 [0.00, 0.27] | -0.08 [-0.27, 0.00] |
| after | recall | 115 | 0.0011 | 0.86 (99) | 0.87 | 0.86 | -0.01 [-0.05, 0.02] | 0.00 [-0.04, 0.04] | -0.01 [-0.05, 0.02] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

⚠ = fewer than 30 items switched by the whole edit.
