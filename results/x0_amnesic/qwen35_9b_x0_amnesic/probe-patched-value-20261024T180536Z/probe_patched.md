# Probe (a), the locker number, on single-change pairs and patched states: qwen35_9b_x0_amnesic

Descriptive, added after data (Dan, 24 Oct ~18:45 items 2-3; audit ~19:30 item 4); not part of X0's rule. Probe trained on qwen35_9b_x0_probe_v4 (locker-before, n = 758, penalty 0.1), cross-fitted by entity; test: the 73 single-change items of qwen35_9b_x0_single_r2 with both lockers before the pick. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Pair test (identical layout, different labels; a layout-only classifier scores 0 by construction)

| measure | share |
|---|---|
| org right | 0.33 [0.24, 0.43] |
| alt right | 0.19 [0.11, 0.28] |
| pair right | 0.08 [0.03, 0.14] |
| same prediction | 0.14 [0.06, 0.22] |

## Patched states: which locker number the probe reads

| state | reads the alt's | reads the org's |
|---|---|---|
| alt (org + Δ) | 0.19 [0.11, 0.28] | 0.11 [0.05, 0.18] |
| org + J++ part, k = 25 | 0.12 [0.05, 0.19] | 0.32 [0.22, 0.42] |
| org + rest, k = 25 | 0.16 [0.07, 0.27] | 0.12 [0.05, 0.21] |
| org + J++ part, k = 100 | 0.16 [0.08, 0.25] | 0.18 [0.10, 0.27] |
| org + rest, k = 100 | 0.15 [0.06, 0.25] | 0.05 [0.01, 0.11] |

## Each part's share of ||Δ||² vs its share of Δ's energy in the probe's subspace (medians)

| part | share of ||Δ||² | share of Δ's probe-subspace energy |
|---|---|---|
| J++ part, k = 25 | 0.178 | 0.125 |
| rest, k = 25 | 0.822 | 1.012 |
| J++ part, k = 100 | 0.368 | 0.203 |
| rest, k = 100 | 0.632 | 0.903 |
