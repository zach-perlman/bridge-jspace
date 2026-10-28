# 48.4: what the copying heads transmit

Batch 48, test 48.4 (jobs/c3/batch48.yaml; Q48.4, Dan: 40%). Unedited locker-first main-test scenes; the five heads at layers > L with the most attention mass from the last token to the bridge token (lookup prompt, read step); r(x) = ||W_OV x|| / ||x||, W_OV = W_O W_V per head (kv group by repeat_kv), medians over items with cluster-bootstrap CIs over bridge items (10000, seed 0). UNVERIFIED.

Rule (fixed in advance): a head reads the rest if r(rest) >= 2 r(J++) with r(random) between them or below both (r(random) <= r(rest)), medians over items, W_OV = W_O W_V; a model holds on at least 3 of its 5 heads; the batch holds if both models hold.

**Verdict: does not hold** (Q48.4 no): 0 of 2 models hold (both needed).

| model | run | status | items | heads reading the rest | heads with r(address) >= r(rest) | holds |
|---|---|---|---|---|---|---|
| qwen3.5-9b | qwen35_9b_x48_heads | tested | 75 | 0 of 5 | 4 of 5 | no |
| muse-glimmer-30b | muse30_x48_heads | tested | 68 | 1 of 5 | 3 of 5 | no |

Per head, variant ov (the rule's): median r per part [95% CI].

| model | head | lookup mass (mean) | recall mass (mean) | r(J++) | r(rest) | r(address) | r(random) | reads the rest |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | L19:h11 | 0.858 | 0.462 | 0.527 [0.518, 0.540] | 0.518 [0.512, 0.529] | 0.520 [0.504, 0.536] | 0.427 [0.421, 0.434] | no |
| qwen3.5-9b | L19:h02 | 0.831 | 0.174 | 0.432 [0.420, 0.443] | 0.365 [0.359, 0.367] | 0.364 [0.355, 0.374] | 0.319 [0.313, 0.323] | no |
| qwen3.5-9b | L19:h10 | 0.482 | 0.155 | 0.423 [0.412, 0.436] | 0.431 [0.424, 0.435] | 0.476 [0.472, 0.489] | 0.365 [0.359, 0.368] | no |
| qwen3.5-9b | L19:h01 | 0.403 | 0.198 | 0.468 [0.459, 0.478] | 0.366 [0.363, 0.371] | 0.373 [0.366, 0.383] | 0.328 [0.322, 0.332] | no |
| qwen3.5-9b | L19:h00 | 0.387 | 0.481 | 0.432 [0.425, 0.441] | 0.371 [0.369, 0.377] | 0.382 [0.378, 0.396] | 0.323 [0.321, 0.325] | no |
| muse-glimmer-30b | L33:h01 | 0.563 | 0.395 | 0.045 [0.043, 0.046] | 0.035 [0.034, 0.036] | 0.038 [0.037, 0.040] | 0.030 [0.029, 0.031] | no |
| muse-glimmer-30b | L30:h26 | 0.550 | 0.248 | 0.046 [0.044, 0.048] | 0.104 [0.101, 0.108] | 0.128 [0.119, 0.141] | 0.052 [0.050, 0.054] | yes |
| muse-glimmer-30b | L28:h15 | 0.475 | 0.060 | 0.028 [0.027, 0.029] | 0.034 [0.033, 0.036] | 0.031 [0.030, 0.033] | 0.033 [0.033, 0.034] | no |
| muse-glimmer-30b | L31:h09 | 0.434 | 0.310 | 0.041 [0.040, 0.045] | 0.061 [0.059, 0.065] | 0.064 [0.058, 0.070] | 0.037 [0.036, 0.038] | no |
| muse-glimmer-30b | L31:h04 | 0.412 | 0.216 | 0.047 [0.044, 0.054] | 0.063 [0.060, 0.069] | 0.062 [0.058, 0.069] | 0.038 [0.037, 0.039] | no |

Per head, variant ov_gain (the input norm's gain folded in; beside): median r per part [95% CI].

| model | head | lookup mass (mean) | recall mass (mean) | r(J++) | r(rest) | r(address) | r(random) | reads the rest |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | L19:h11 | 0.858 | 0.462 | 0.544 [0.533, 0.559] | 0.552 [0.541, 0.561] | 0.559 [0.540, 0.578] | 0.445 [0.441, 0.453] | no |
| qwen3.5-9b | L19:h02 | 0.831 | 0.174 | 0.451 [0.438, 0.461] | 0.388 [0.381, 0.390] | 0.391 [0.382, 0.404] | 0.332 [0.326, 0.338] | no |
| qwen3.5-9b | L19:h10 | 0.482 | 0.155 | 0.437 [0.424, 0.449] | 0.455 [0.447, 0.460] | 0.512 [0.501, 0.526] | 0.381 [0.374, 0.383] | no |
| qwen3.5-9b | L19:h01 | 0.403 | 0.198 | 0.487 [0.481, 0.500] | 0.392 [0.387, 0.394] | 0.402 [0.393, 0.414] | 0.343 [0.337, 0.347] | no |
| qwen3.5-9b | L19:h00 | 0.387 | 0.481 | 0.450 [0.442, 0.461] | 0.399 [0.391, 0.404] | 0.412 [0.406, 0.429] | 0.336 [0.335, 0.340] | no |
| muse-glimmer-30b | L33:h01 | 0.563 | 0.395 | 0.056 [0.054, 0.059] | 0.046 [0.045, 0.047] | 0.050 [0.048, 0.052] | 0.038 [0.038, 0.039] | no |
| muse-glimmer-30b | L30:h26 | 0.550 | 0.248 | 0.057 [0.055, 0.059] | 0.132 [0.128, 0.136] | 0.161 [0.150, 0.177] | 0.065 [0.064, 0.068] | yes |
| muse-glimmer-30b | L28:h15 | 0.475 | 0.060 | 0.037 [0.036, 0.038] | 0.047 [0.046, 0.049] | 0.043 [0.041, 0.045] | 0.046 [0.045, 0.047] | no |
| muse-glimmer-30b | L31:h09 | 0.434 | 0.310 | 0.047 [0.046, 0.051] | 0.071 [0.069, 0.076] | 0.075 [0.068, 0.083] | 0.042 [0.042, 0.043] | no |
| muse-glimmer-30b | L31:h04 | 0.412 | 0.216 | 0.052 [0.050, 0.060] | 0.074 [0.070, 0.081] | 0.073 [0.068, 0.080] | 0.043 [0.043, 0.045] | no |

Items and layers (descriptive):

- qwen3.5-9b (qwen35_9b_x48_heads, from qwen35_9b_x0_necessity, L12): 75 items of 200 at L (locker vs asked pick {'org after, alt after': 68, 'org before, alt before': 75, 'org after, alt before': 32, 'org before, alt after': 25}); candidate layers [15, 19, 23, 27, 31] (config full_attention [15, 19, 23, 27, 31]; layer types {'linear_attention': 24, 'full_attention': 8}; sliding window None, longest read 77); 16 query heads, 4 kv heads, head dim 256; per head: L19:h11 r(rest) = 0.5180 < 2.0 x r(J++) = 1.0538; r(random) = 0.4274 <= r(rest); L19:h02 r(rest) = 0.3648 < 2.0 x r(J++) = 0.8641; r(random) = 0.3188 <= r(rest); L19:h10 r(rest) = 0.4306 < 2.0 x r(J++) = 0.8469; r(random) = 0.3646 <= r(rest); L19:h01 r(rest) = 0.3661 < 2.0 x r(J++) = 0.9358; r(random) = 0.3276 <= r(rest); L19:h00 r(rest) = 0.3714 < 2.0 x r(J++) = 0.8643; r(random) = 0.3231 <= r(rest)
- muse-glimmer-30b (muse30_x48_heads, from muse30b_x0_necessity, L26): 68 items of 200 at L (locker vs asked pick {'org after, alt after': 69, 'org after, alt before': 39, 'org before, alt before': 68, 'org before, alt after': 24}); candidate layers [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51] (config full_attention [27, 31, 35, 39, 43, 47, 51]; layer types {'sliding_attention': 39, 'full_attention': 13}; sliding window 2048, longest read 112); 32 query heads, 2 kv heads, head dim 128; per head: L33:h01 r(rest) = 0.0350 < 2.0 x r(J++) = 0.0890; r(random) = 0.0300 <= r(rest); L30:h26 r(rest) = 0.1042 >= 2.0 x r(J++) = 0.0917; r(random) = 0.0522 <= r(rest); L28:h15 r(rest) = 0.0342 < 2.0 x r(J++) = 0.0557; r(random) = 0.0334 <= r(rest); L31:h09 r(rest) = 0.0607 < 2.0 x r(J++) = 0.0822; r(random) = 0.0369 <= r(rest); L31:h04 r(rest) = 0.0630 < 2.0 x r(J++) = 0.0936; r(random) = 0.0375 <= r(rest)
