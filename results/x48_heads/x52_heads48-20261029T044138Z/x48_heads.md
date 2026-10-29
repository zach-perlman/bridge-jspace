# 48.4: what the copying heads transmit

Batch 48, test 48.4 (jobs/c3/batch48.yaml; batch 52 C coverage, no prediction: coverage run on an already-scored rule; rule first scored in results/x48_heads/x48_heads-20261028T113126Z; the both-models count covers the given runs only, not re-scored). Unedited locker-first main-test scenes; the five heads at layers > L with the most attention mass from the last token to the bridge token (lookup prompt, read step); r(x) = ||W_OV x|| / ||x||, W_OV = W_O W_V per head (kv group by repeat_kv), medians over items with cluster-bootstrap CIs over bridge items (10000, seed 0). UNVERIFIED.

Rule (fixed in advance): a head reads the rest if r(rest) >= 2 r(J++) with r(random) between them or below both (r(random) <= r(rest)), medians over items, W_OV = W_O W_V; a model holds on at least 3 of its 5 heads; the batch holds if both models hold.

**Verdict: does not hold** (Q48.4 no): 0 of 1 models hold (both needed).

| model | run | status | items | heads reading the rest | heads with r(address) >= r(rest) | holds |
|---|---|---|---|---|---|---|
| qwen3.6-27b | x48_heads_27b | tested | 69 | 0 of 5 | 1 of 5 | no |

Per head, variant ov (the rule's): median r per part [95% CI].

| model | head | lookup mass (mean) | recall mass (mean) | r(J++) | r(rest) | r(address) | r(random) | reads the rest |
|---|---|---|---|---|---|---|---|---|
| qwen3.6-27b | L35:h04 | 0.742 | 0.100 | 0.444 [0.434, 0.460] | 0.357 [0.349, 0.366] | 0.330 [0.322, 0.353] | 0.325 [0.319, 0.329] | no |
| qwen3.6-27b | L35:h03 | 0.737 | 0.267 | 0.466 [0.459, 0.483] | 0.365 [0.358, 0.376] | 0.333 [0.325, 0.361] | 0.330 [0.325, 0.338] | no |
| qwen3.6-27b | L35:h17 | 0.713 | 0.330 | 0.374 [0.369, 0.384] | 0.505 [0.496, 0.516] | 0.519 [0.510, 0.536] | 0.370 [0.365, 0.375] | no |
| qwen3.6-27b | L35:h20 | 0.667 | 0.497 | 0.707 [0.684, 0.731] | 0.512 [0.505, 0.527] | 0.488 [0.470, 0.519] | 0.349 [0.345, 0.365] | no |
| qwen3.6-27b | L35:h02 | 0.577 | 0.109 | 0.457 [0.448, 0.474] | 0.355 [0.344, 0.362] | 0.333 [0.322, 0.363] | 0.327 [0.323, 0.333] | no |

Per head, variant ov_gain (the input norm's gain folded in; beside): median r per part [95% CI].

| model | head | lookup mass (mean) | recall mass (mean) | r(J++) | r(rest) | r(address) | r(random) | reads the rest |
|---|---|---|---|---|---|---|---|---|
| qwen3.6-27b | L35:h04 | 0.742 | 0.100 | 0.427 [0.413, 0.447] | 0.366 [0.357, 0.373] | 0.343 [0.332, 0.369] | 0.329 [0.323, 0.331] | no |
| qwen3.6-27b | L35:h03 | 0.737 | 0.267 | 0.450 [0.438, 0.470] | 0.373 [0.368, 0.384] | 0.345 [0.337, 0.376] | 0.334 [0.330, 0.339] | no |
| qwen3.6-27b | L35:h17 | 0.713 | 0.330 | 0.367 [0.360, 0.377] | 0.521 [0.508, 0.535] | 0.536 [0.525, 0.558] | 0.378 [0.373, 0.383] | no |
| qwen3.6-27b | L35:h20 | 0.667 | 0.497 | 0.565 [0.535, 0.579] | 0.508 [0.501, 0.520] | 0.506 [0.480, 0.529] | 0.341 [0.336, 0.346] | no |
| qwen3.6-27b | L35:h02 | 0.577 | 0.109 | 0.438 [0.429, 0.457] | 0.365 [0.353, 0.372] | 0.345 [0.331, 0.375] | 0.331 [0.328, 0.336] | no |

Items and layers (descriptive):

- qwen3.6-27b (x48_heads_27b, from x0_necessity_27b_chat, L32): 69 items of 200 at L (locker vs asked pick {'org before, alt before': 69, 'org after, alt after': 61, 'org after, alt before': 38, 'org before, alt after': 32}); candidate layers [35, 39, 43, 47, 51, 55, 59, 63] (config full_attention [35, 39, 43, 47, 51, 55, 59, 63]; layer types {'linear_attention': 48, 'full_attention': 16}; sliding window None, longest read 77); 24 query heads, 4 kv heads, head dim 256; per head: L35:h04 r(rest) = 0.3569 < 2.0 x r(J++) = 0.8888; r(random) = 0.3247 <= r(rest); L35:h03 r(rest) = 0.3647 < 2.0 x r(J++) = 0.9312; r(random) = 0.3302 <= r(rest); L35:h17 r(rest) = 0.5049 < 2.0 x r(J++) = 0.7476; r(random) = 0.3701 <= r(rest); L35:h20 r(rest) = 0.5117 < 2.0 x r(J++) = 1.4145; r(random) = 0.3494 <= r(rest); L35:h02 r(rest) = 0.3548 < 2.0 x r(J++) = 0.9141; r(random) = 0.3274 <= r(rest)
