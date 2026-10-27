# Probe (b), the locker sentence, on single-change pairs and patched states: qwen35_9b_x0_amnesic

Descriptive, added after data (Dan, 24 Oct ~18:45 items 2-3; audit ~19:30 item 4); not part of X0's rule. Probe trained on qwen35_9b_x0_probe_v4 (locker-before, n = 758, penalty 0.1), cross-fitted by entity; test: the 73 single-change items of qwen35_9b_x0_single_r2 with both lockers before the pick. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Pair test (identical layout, different labels; a layout-only classifier scores 0 by construction)

| measure | share |
|---|---|
| org right | 0.95 [0.89, 0.99] |
| alt right | 0.55 [0.44, 0.65] |
| pair right | 0.51 [0.40, 0.61] |
| same prediction | 0.03 [0.00, 0.07] |

## The duplicate pick: by where the alt item's other picker's sentence sits (Dan ~20:45)

In the alt, two people pick the alt item. If the alt state's address pointed to the previous occurrence of the same word, alt right would be high when the other pick comes after the asked pick and low when it comes before.

| other pick vs asked pick | n | alt right | pair right | alt state reads the other pick sentence |
|---|---|---|---|---|
| before | 58 | 0.43 [0.32, 0.54] | 0.40 [0.29, 0.51] | 0.48 [0.35, 0.60] |
| after | 15 | 1.00 [1.00, 1.00] | 0.93 [0.79, 1.00] | 0.00 [0.00, 0.00] |
| before, the other pick is the latest earlier mention | 28 | 0.86 [0.70, 0.97] | 0.79 [0.64, 0.92] | 0.04 [0.00, 0.12] |
| before, the alt locker is the latest earlier mention | 30 | 0.03 [0.00, 0.09] | 0.03 [0.00, 0.09] | 0.90 [0.80, 1.00] |

## Patched states: which locker sentence the probe reads

| state | reads the alt's | reads the org's |
|---|---|---|
| alt (org + Δ) | 0.55 [0.44, 0.65] | 0.03 [0.00, 0.07] |
| org + J++ part, k = 25 | 0.00 [0.00, 0.00] | 0.96 [0.92, 1.00] |
| org + rest, k = 25 | 0.55 [0.44, 0.66] | 0.04 [0.00, 0.10] |
| org + J++ part, k = 100 | 0.03 [0.00, 0.06] | 0.92 [0.86, 0.97] |
| org + rest, k = 100 | 0.48 [0.37, 0.60] | 0.12 [0.06, 0.20] |

## Each part's share of ||Δ||² vs its share of Δ's energy in the probe's subspace (medians)

| part | share of ||Δ||² | share of Δ's probe-subspace energy |
|---|---|---|
| J++ part, k = 25 | 0.178 | 0.005 |
| rest, k = 25 | 0.822 | 0.906 |
| J++ part, k = 100 | 0.368 | 0.032 |
| rest, k = 100 | 0.632 | 0.695 |
