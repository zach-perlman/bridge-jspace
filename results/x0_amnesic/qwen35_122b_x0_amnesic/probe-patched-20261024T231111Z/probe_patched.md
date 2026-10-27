# Probe (b), the locker sentence, on single-change pairs and patched states: qwen35_122b_x0_amnesic

Descriptive, added after data (Dan, 24 Oct ~18:45 items 2-3; audit ~19:30 item 4); not part of X0's rule. Probe trained on qwen35_122b_x0_probe_v4 (locker-before, n = 758, penalty 0.1), cross-fitted by entity; test: the 54 single-change items of qwen35_122b_x0_single with both lockers before the pick. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Pair test (identical layout, different labels; a layout-only classifier scores 0 by construction)

| measure | share |
|---|---|
| org right | 0.89 [0.80, 0.97] |
| alt right | 0.50 [0.36, 0.65] |
| pair right | 0.44 [0.30, 0.60] |
| same prediction | 0.02 [0.00, 0.06] |

## The duplicate pick: by where the alt item's other picker's sentence sits (Dan ~20:45)

In the alt, two people pick the alt item. If the alt state's address pointed to the previous occurrence of the same word, alt right would be high when the other pick comes after the asked pick and low when it comes before.

| other pick vs asked pick | n | alt right | pair right | alt state reads the other pick sentence |
|---|---|---|---|---|
| before | 42 | 0.36 [0.20, 0.52] | 0.31 [0.16, 0.48] | 0.55 [0.37, 0.71] |
| after | 12 | 1.00 [1.00, 1.00] | 0.92 [0.73, 1.00] | 0.00 [0.00, 0.00] |
| before, the other pick is the latest earlier mention | 18 | 0.83 [0.57, 1.00] | 0.72 [0.44, 0.94] | 0.00 [0.00, 0.00] |
| before, the alt locker is the latest earlier mention | 24 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.96 [0.85, 1.00] |

## Patched states: which locker sentence the probe reads

| state | reads the alt's | reads the org's |
|---|---|---|
| alt (org + Δ) | 0.50 [0.36, 0.65] | 0.02 [0.00, 0.06] |
| org + J++ part, k = 25 | 0.06 [0.00, 0.11] | 0.83 [0.74, 0.93] |
| org + rest, k = 25 | 0.50 [0.36, 0.65] | 0.02 [0.00, 0.06] |
| org + J++ part, k = 100 | 0.09 [0.02, 0.16] | 0.78 [0.69, 0.87] |
| org + rest, k = 100 | 0.46 [0.32, 0.63] | 0.02 [0.00, 0.06] |

## Each part's share of ||Δ||² vs its share of Δ's energy in the probe's subspace (medians)

| part | share of ||Δ||² | share of Δ's probe-subspace energy |
|---|---|---|
| J++ part, k = 25 | 0.182 | 0.005 |
| rest, k = 25 | 0.818 | 0.933 |
| J++ part, k = 100 | 0.343 | 0.025 |
| rest, k = 100 | 0.657 | 0.767 |
