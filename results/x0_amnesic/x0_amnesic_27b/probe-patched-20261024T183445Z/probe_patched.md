# Probe (b), the locker sentence, on single-change pairs and patched states: x0_amnesic_27b

Descriptive, added after data (Dan, 24 Oct ~18:45 items 2-3; audit ~19:30 item 4); not part of X0's rule. Probe trained on x0_probe_v4_27b (locker-before, n = 758, penalty 0.01), cross-fitted by entity; test: the 70 single-change items of x0_single_27b_r2 with both lockers before the pick. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Pair test (identical layout, different labels; a layout-only classifier scores 0 by construction)

| measure | share |
|---|---|
| org right | 0.99 [0.95, 1.00] |
| alt right | 0.59 [0.46, 0.73] |
| pair right | 0.57 [0.44, 0.71] |
| same prediction | 0.10 [0.04, 0.16] |

## The duplicate pick: by where the alt item's other picker's sentence sits (Dan ~20:45)

In the alt, two people pick the alt item. If the alt state's address pointed to the previous occurrence of the same word, alt right would be high when the other pick comes after the asked pick and low when it comes before.

| other pick vs asked pick | n | alt right | pair right | alt state reads the other pick sentence |
|---|---|---|---|---|
| before | 53 | 0.45 [0.31, 0.62] | 0.45 [0.31, 0.62] | 0.34 [0.20, 0.47] |
| after | 17 | 1.00 [1.00, 1.00] | 0.94 [0.80, 1.00] | 0.00 [0.00, 0.00] |
| before, the other pick is the latest earlier mention | 28 | 0.64 [0.45, 0.83] | 0.64 [0.45, 0.83] | 0.14 [0.03, 0.27] |
| before, the alt locker is the latest earlier mention | 25 | 0.24 [0.10, 0.40] | 0.24 [0.10, 0.40] | 0.56 [0.38, 0.74] |

## Patched states: which locker sentence the probe reads

| state | reads the alt's | reads the org's |
|---|---|---|
| alt (org + Δ) | 0.59 [0.46, 0.73] | 0.10 [0.04, 0.16] |
| org + J++ part, k = 25 | 0.00 [0.00, 0.00] | 0.99 [0.95, 1.00] |
| org + rest, k = 25 | 0.51 [0.40, 0.65] | 0.14 [0.08, 0.21] |
| org + J++ part, k = 100 | 0.04 [0.00, 0.09] | 0.94 [0.89, 0.99] |
| org + rest, k = 100 | 0.50 [0.38, 0.63] | 0.16 [0.09, 0.22] |

## Each part's share of ||Δ||² vs its share of Δ's energy in the probe's subspace (medians)

| part | share of ||Δ||² | share of Δ's probe-subspace energy |
|---|---|---|
| J++ part, k = 25 | 0.104 | 0.005 |
| rest, k = 25 | 0.896 | 0.905 |
| J++ part, k = 100 | 0.242 | 0.028 |
| rest, k = 100 | 0.758 | 0.734 |
