# Natural passages: qwen35_122b_x5_natural

Fixed in advance (Dan, 25 Oct ~00:20; spec jobs/c3/x5_natural.yaml; prediction: batch 31, Q31.6). Model qwen3.5-122b-a10b, layer 33, 114 items, 68 bridge entities. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Rule: HOLDS (gap 0.44 [0.32, 0.58])

Rule: gap >= 0.3 with lower CI >= 0.15 holds; <= 0.1 fails; otherwise mixed.

Lookup excess -0.11 [-0.20, -0.03]; recall excess 0.34 [0.24, 0.43].

## By relation and by half (descriptive)

| subset | n | lookup excess | recall excess | gap |
|---|---|---|---|---|
| relation = animals | 4 | 0.00 [0.00, 0.00] | 0.50 [0.00, 2.00] | 0.50 [0.00, 2.00] |
| relation = cities | 33 | -0.16 [-0.33, 0.00] | 0.27 [0.13, 0.41] | 0.43 [0.20, 0.71] |
| relation = companies | 16 | -0.12 [-0.31, 0.00] | 0.36 [0.10, 0.62] | 0.48 [0.20, 0.75] |
| relation = countries | 31 | -0.13 [-0.42, 0.00] | 0.27 [0.11, 0.43] | 0.40 [0.19, 0.71] |
| relation = languages | 21 | 0.00 [0.00, 0.00] | 0.52 [0.28, 0.75] | 0.52 [0.28, 0.75] |
| relation = people | 9 | 0.00 [0.00, 0.00] | 0.29 [0.00, 0.71] | 0.29 [0.00, 0.67] |
| half = A | 56 | -0.13 [-0.26, -0.03] | 0.29 [0.15, 0.44] | 0.42 [0.23, 0.64] |
| half = B | 58 | -0.08 [-0.22, 0.00] | 0.38 [0.27, 0.50] | 0.46 [0.33, 0.63] |

## The recall's lure (separate outcome)

Share of recall reads on the passage's value for the edited bridge: whole 0.00, no_part 0.04, no_rand 0.01.
