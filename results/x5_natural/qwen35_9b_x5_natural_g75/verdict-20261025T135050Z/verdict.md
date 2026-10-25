# Natural passages: qwen35_9b_x5_natural_g75

Fixed in advance (Dan, 25 Oct ~00:20; spec jobs/c3/x5_natural.yaml; prediction: batch 31, Q31.6). Model qwen3.5-9b, layer 12, 83 items, 56 bridge entities. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Rule: HOLDS (gap 0.52 [0.36, 0.68])

Rule: gap >= 0.3 with lower CI >= 0.15 holds; <= 0.1 fails; otherwise mixed.

Lookup excess 0.03 [-0.08, 0.15]; recall excess 0.56 [0.45, 0.66].

## By relation and by half (descriptive)

| subset | n | lookup excess | recall excess | gap |
|---|---|---|---|---|
| relation = animals | 4 | 0.00 [0.00, 0.00] | 0.25 [0.00, 0.75] | 0.25 [0.00, 0.50] |
| relation = cities | 29 | 0.18 [0.00, 0.42] | 0.50 [0.32, 0.68] | 0.32 [0.04, 0.60] |
| relation = companies | 11 | 0.00 [0.00, 0.00] | 0.50 [0.17, 0.77] | 0.50 [0.17, 0.77] |
| relation = countries | 21 | -0.12 [-0.40, 0.00] | 0.67 [0.47, 0.85] | 0.79 [0.55, 1.06] |
| relation = languages | 15 | 0.00 [0.00, 0.00] | 0.67 [0.40, 0.93] | 0.67 [0.40, 0.93] |
| relation = people | 3 | 0.00 [0.00, 0.00] | 0.33 [0.00, 1.00] | 0.33 [0.00, 0.67] |
| half = A | 46 | 0.13 [0.00, 0.29] | 0.48 [0.33, 0.62] | 0.35 [0.14, 0.56] |
| half = B | 37 | -0.07 [-0.25, 0.00] | 0.65 [0.51, 0.79] | 0.72 [0.54, 0.94] |

## The recall's lure (separate outcome)

Share of recall reads on the passage's value for the edited bridge: whole 0.00, no_part 0.08, no_rand 0.00.
