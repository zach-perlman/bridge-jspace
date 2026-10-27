# The switch as a probability, and how shares of the change are aggregated (descriptive, after the data)

## T0.3: extra loss with the switch replaced by p_alt (expected switches when sampling at T = 1)

Main test (two people swap), the layer fixed in advance, J++ at 25 signed-OMP directions against a random part of the same share; cluster bootstrap over bridge entities (10,000, seed 0). UNVERIFIED.

| model | n | lookup, p_alt | recall, p_alt | gap, p_alt | gap, switches (pre-registered) |
|---|---|---|---|---|---|
| qwen3.5-9b | 200 | -0.05 [-0.07, -0.03] | 0.46 [0.39, 0.53] | 0.51 [0.44, 0.58] | 0.53 [0.42, 0.61] |
| qwen3.6-27b | 200 | 0.17 [0.13, 0.22] | 0.70 [0.63, 0.76] | 0.53 [0.46, 0.59] | 0.60 [0.50, 0.69] |
| qwen3.5-122b-a10b | 200 | -0.01 [-0.05, 0.02] | 0.33 [0.26, 0.40] | 0.34 [0.27, 0.41] | 0.32 [0.20, 0.43] |
| muse-glimmer-30b | 200 | -0.03 [-0.05, -0.01] | 0.70 [0.57, 0.79] | 0.73 [0.59, 0.82] | 0.85 [0.68, 0.98] |

## T0.4: a share of the change, three ways

Every '% of the change' in the README is the median over items of ||P Δ||² / ||Δ||². Pooled: sum ||P Δ||² / sum ||Δ||²; mean: the mean of the per-item ratios.

| model | part | scenes | n | median (the README's) | mean of per-item ratios | pooled |
|---|---|---|---|---|---|---|
| qwen3.5-9b | J++ + pointer + identity outside J++ | sanity swap | 300 | 56% | 50% | 46% |
| qwen3.6-27b | J++ + pointer + identity outside J++ | sanity swap | 300 | 35% | 37% | 32% |
| muse-glimmer-30b | J++ + pointer + identity outside J++ | sanity swap | 290 | 38% | 35% | 29% |
| qwen3.5-9b | J++ (25 directions) | main test | 200 | 23% | 24% | – |
| qwen3.6-27b | J++ (25 directions) | main test | 200 | 16% | 18% | – |
| qwen3.5-122b-a10b | J++ (25 directions) | main test | 200 | 25% | 26% | – |
| muse-glimmer-30b | J++ (25 directions) | main test | 200 | 14% | 16% | – |
