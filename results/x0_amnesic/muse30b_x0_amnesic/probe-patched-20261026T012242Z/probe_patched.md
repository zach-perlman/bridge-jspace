# Probe (b), the locker sentence, on single-change pairs and patched states: muse30b_x0_amnesic

Descriptive, added after data (Dan, 24 Oct ~18:45 items 2-3; audit ~19:30 item 4); not part of X0's rule. Probe trained on muse30b_x0_probe_v4 (locker-before, n = 657, penalty 0.01), cross-fitted by entity; test: the 68 single-change items of muse30b_x0_single with both lockers before the pick. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Pair test (identical layout, different labels; a layout-only classifier scores 0 by construction)

| measure | share |
|---|---|
| org right | 0.96 [0.92, 1.00] |
| alt right | 0.50 [0.41, 0.61] |
| pair right | 0.50 [0.41, 0.61] |
| same prediction | 0.03 [0.00, 0.07] |

## The duplicate pick: by where the alt item's other picker's sentence sits (Dan ~20:45)

In the alt, two people pick the alt item. If the alt state's address pointed to the previous occurrence of the same word, alt right would be high when the other pick comes after the asked pick and low when it comes before.

| other pick vs asked pick | n | alt right | pair right | alt state reads the other pick sentence |
|---|---|---|---|---|
| before | 53 | 0.36 [0.24, 0.49] | 0.36 [0.24, 0.49] | 0.40 [0.26, 0.53] |
| after | 15 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] |
| before, the other pick is the latest earlier mention | 27 | 0.59 [0.37, 0.79] | 0.59 [0.37, 0.79] | 0.15 [0.03, 0.30] |
| before, the alt locker is the latest earlier mention | 26 | 0.12 [0.00, 0.24] | 0.12 [0.00, 0.24] | 0.65 [0.44, 0.82] |

## Patched states: which locker sentence the probe reads

| state | reads the alt's | reads the org's |
|---|---|---|
| alt (org + Δ) | 0.50 [0.41, 0.61] | 0.03 [0.00, 0.07] |
| org + J++ part, k = 25 | 0.04 [0.00, 0.08] | 0.96 [0.92, 1.00] |
| org + rest, k = 25 | 0.49 [0.39, 0.60] | 0.06 [0.01, 0.12] |
| org + J++ part, k = 100 | 0.07 [0.02, 0.13] | 0.93 [0.87, 0.98] |
| org + rest, k = 100 | 0.46 [0.36, 0.57] | 0.12 [0.05, 0.19] |

## Each part's share of ||Δ||² vs its share of Δ's energy in the probe's subspace (medians)

| part | share of ||Δ||² | share of Δ's probe-subspace energy |
|---|---|---|
| J++ part, k = 25 | 0.104 | 0.003 |
| rest, k = 25 | 0.896 | 0.929 |
| J++ part, k = 100 | 0.222 | 0.023 |
| rest, k = 100 | 0.778 | 0.739 |
