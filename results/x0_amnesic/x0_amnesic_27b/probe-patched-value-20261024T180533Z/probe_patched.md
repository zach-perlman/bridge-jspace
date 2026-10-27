# Probe (a), the locker number, on single-change pairs and patched states: x0_amnesic_27b

Descriptive, added after data (Dan, 24 Oct ~18:45 items 2-3; audit ~19:30 item 4); not part of X0's rule. Probe trained on x0_probe_v4_27b (locker-before, n = 758, penalty 0.01), cross-fitted by entity; test: the 70 single-change items of x0_single_27b_r2 with both lockers before the pick. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Pair test (identical layout, different labels; a layout-only classifier scores 0 by construction)

| measure | share |
|---|---|
| org right | 0.33 [0.23, 0.45] |
| alt right | 0.20 [0.11, 0.31] |
| pair right | 0.03 [0.00, 0.08] |
| same prediction | 0.11 [0.03, 0.20] |

## Patched states: which locker number the probe reads

| state | reads the alt's | reads the org's |
|---|---|---|
| alt (org + Δ) | 0.20 [0.11, 0.31] | 0.09 [0.01, 0.17] |
| org + J++ part, k = 25 | 0.04 [0.00, 0.09] | 0.40 [0.29, 0.52] |
| org + rest, k = 25 | 0.21 [0.11, 0.33] | 0.13 [0.05, 0.22] |
| org + J++ part, k = 100 | 0.06 [0.01, 0.11] | 0.41 [0.30, 0.54] |
| org + rest, k = 100 | 0.19 [0.11, 0.26] | 0.16 [0.08, 0.24] |

## Each part's share of ||Δ||² vs its share of Δ's energy in the probe's subspace (medians)

| part | share of ||Δ||² | share of Δ's probe-subspace energy |
|---|---|---|
| J++ part, k = 25 | 0.104 | 0.063 |
| rest, k = 25 | 0.896 | 0.869 |
| J++ part, k = 100 | 0.242 | 0.164 |
| rest, k = 100 | 0.758 | 0.711 |
