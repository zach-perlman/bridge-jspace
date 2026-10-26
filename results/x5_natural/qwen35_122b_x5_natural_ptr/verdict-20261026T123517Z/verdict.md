# Natural passages: qwen35_122b_x5_natural_ptr

Fixed in advance (Dan, 25 Oct ~00:20; spec jobs/c3/x5_natural.yaml; prediction: batch 31, Q31.6). Model qwen3.5-122b-a10b, layer 33, 114 items, 68 bridge entities. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Rule: HOLDS (gap 0.40 [0.28, 0.52])

Rule: gap >= 0.3 with lower CI >= 0.15 holds; <= 0.1 fails; otherwise mixed.

Lookup excess -0.07 [-0.16, 0.00]; recall excess 0.32 [0.23, 0.41].

## By relation and by half (descriptive)

| subset | n | lookup excess | recall excess | gap |
|---|---|---|---|---|
| relation = animals | 4 | 0.00 [0.00, 0.00] | 0.50 [0.00, 2.00] | 0.50 [0.00, 2.00] |
| relation = cities | 33 | -0.16 [-0.33, 0.00] | 0.27 [0.13, 0.41] | 0.43 [0.20, 0.71] |
| relation = companies | 16 | -0.12 [-0.40, 0.00] | 0.36 [0.10, 0.62] | 0.48 [0.20, 0.75] |
| relation = countries | 31 | 0.00 [-0.19, 0.23] | 0.28 [0.12, 0.44] | 0.28 [0.00, 0.53] |
| relation = languages | 21 | 0.00 [0.00, 0.00] | 0.48 [0.25, 0.70] | 0.48 [0.25, 0.70] |
| relation = people | 9 | 0.00 [0.00, 0.00] | 0.17 [0.00, 0.60] | 0.17 [0.00, 0.60] |
| half = A | 56 | -0.17 [-0.31, -0.04] | 0.27 [0.15, 0.42] | 0.44 [0.25, 0.67] |
| half = B | 58 | 0.04 [0.00, 0.14] | 0.37 [0.25, 0.49] | 0.33 [0.19, 0.46] |

## The recall's lure (separate outcome)

Share of recall reads on the passage's value for the edited bridge: whole 0.01, no_part 0.04, no_rand 0.01.
