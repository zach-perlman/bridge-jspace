# Probe (b) on single-change pairs and patched states: qwen35_9b_x0_amnesic

Descriptive, added after data (Dan, 24 Oct ~18:45 items 2-3; audit ~19:30 item 4); not part of X0's rule. Probe trained on qwen35_9b_x0_probe (locker-before, n = 301, penalty 0.1), cross-fitted by entity; test: the 73 single-change items of qwen35_9b_x0_single_r2 with both lockers before the pick. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Pair test (identical layout, different labels; a layout-only classifier scores 0 by construction)

| measure | share |
|---|---|
| org right | 0.88 [0.82, 0.94] |
| alt right | 0.55 [0.45, 0.65] |
| pair right | 0.48 [0.38, 0.58] |
| same prediction | 0.01 [0.00, 0.05] |

## Patched states: which locker sentence the probe reads

| state | reads the alt's | reads the org's |
|---|---|---|
| alt (org + Δ) | 0.55 [0.45, 0.65] | 0.01 [0.00, 0.05] |
| org + J++ part, k = 25 | 0.03 [0.00, 0.07] | 0.85 [0.78, 0.92] |
| org + rest, k = 25 | 0.52 [0.42, 0.63] | 0.01 [0.00, 0.05] |
| org + J++ part, k = 100 | 0.03 [0.00, 0.07] | 0.84 [0.76, 0.90] |
| org + rest, k = 100 | 0.48 [0.38, 0.59] | 0.08 [0.02, 0.15] |

## Each part's share of ||Δ||² vs its share of Δ's energy in the probe's subspace (medians)

| part | share of ||Δ||² | share of Δ's probe-subspace energy |
|---|---|---|
| J++ part, k = 25 | 0.178 | 0.005 |
| rest, k = 25 | 0.822 | 0.899 |
| J++ part, k = 100 | 0.368 | 0.027 |
| rest, k = 100 | 0.632 | 0.718 |
