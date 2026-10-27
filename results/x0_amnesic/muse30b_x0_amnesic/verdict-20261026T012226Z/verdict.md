# Probe-(b) subspace: remove it, or keep only it (muse30b_x0_amnesic)

Descriptive, added after data (Dan, 24 Oct ~18:45, item 6); not part of X0's rule. Model muse-glimmer-30b, layer 26, single-change items of muse30b_x0_single; probe subspace rank 4 from muse30b_x0_probe_v4 (locker-before, n = 657, CV accuracy 0.97). Bootstrap over bridge entities, 10000 resamples. UNVERIFIED.

| locker vs pick | reader | n | median share of ‖Δ‖² in P | S_whole | S_no_probe | S_no_rand | probe dep. | random dep. | excess | S_probe_only / S_whole | S_rand_only / S_whole | difference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| before | lookup | 95 | 0.0131 | 0.81 (77) | 0.81 | 0.81 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| before | recall | 95 | 0.0131 | 0.54 (51) | 0.56 | 0.57 | -0.04 [-0.10, 0.00] | -0.06 [-0.14, 0.00] | 0.02 [0.00, 0.07] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| after | lookup | 105 | 0.0011 | 0.09 (9 ⚠) | 0.09 | 0.09 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| after | recall | 105 | 0.0011 | 0.60 (63) | 0.60 | 0.60 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

⚠ = fewer than 30 items switched by the whole edit.
