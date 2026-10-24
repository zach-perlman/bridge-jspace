# Probe (b) on single-change pairs and patched states: x0_amnesic_27b

Descriptive, added after data (Dan, 24 Oct ~18:45 items 2-3; audit ~19:30 item 4); not part of X0's rule. Probe trained on x0_probe_27b (locker-before, n = 301, penalty 0.01), cross-fitted by entity; test: the 70 single-change items of x0_single_27b_r2 with both lockers before the pick. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Pair test (identical layout, different labels; a layout-only classifier scores 0 by construction)

| measure | share |
|---|---|
| org right | 0.93 [0.87, 0.98] |
| alt right | 0.59 [0.46, 0.72] |
| pair right | 0.54 [0.40, 0.69] |
| same prediction | 0.03 [0.00, 0.08] |

## Patched states: which locker sentence the probe reads

| state | reads the alt's | reads the org's |
|---|---|---|
| alt (org + Δ) | 0.59 [0.46, 0.72] | 0.03 [0.00, 0.08] |
| org + J++ part, k = 25 | 0.00 [0.00, 0.00] | 0.91 [0.85, 0.97] |
| org + rest, k = 25 | 0.60 [0.48, 0.73] | 0.03 [0.00, 0.08] |
| org + J++ part, k = 100 | 0.00 [0.00, 0.00] | 0.93 [0.87, 0.98] |
| org + rest, k = 100 | 0.56 [0.43, 0.69] | 0.07 [0.01, 0.16] |

## Each part's share of ||Δ||² vs its share of Δ's energy in the probe's subspace (medians)

| part | share of ||Δ||² | share of Δ's probe-subspace energy |
|---|---|---|
| J++ part, k = 25 | 0.104 | 0.004 |
| rest, k = 25 | 0.896 | 0.909 |
| J++ part, k = 100 | 0.242 | 0.025 |
| rest, k = 100 | 0.758 | 0.726 |
