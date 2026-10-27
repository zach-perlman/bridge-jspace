# Natural passages: x5_natural_ptr_27b

Fixed in advance (Dan, 25 Oct ~00:20; spec jobs/c3/x5_natural.yaml; prediction: batch 31, Q31.6). Model qwen3.6-27b, layer 32, 137 items, 71 bridge entities. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Rule: MIXED (gap 0.23 [0.07, 0.37])

Rule: gap >= 0.3 with lower CI >= 0.15 holds; <= 0.1 fails; otherwise mixed.

Lookup excess 0.34 [0.23, 0.47]; recall excess 0.57 [0.49, 0.65].

## By relation and by half (descriptive)

| subset | n | lookup excess | recall excess | gap |
|---|---|---|---|---|
| relation = animals | 5 | 1.00 [0.00, 2.00] | 1.00 [1.00, 1.00] | 0.00 [-1.00, 1.00] |
| relation = cities | 37 | 0.64 [0.38, 1.00] | 0.57 [0.42, 0.73] | -0.07 [-0.41, 0.20] |
| relation = companies | 17 | 0.14 [0.00, 0.44] | 0.73 [0.47, 1.00] | 0.59 [0.30, 0.88] |
| relation = countries | 39 | 0.45 [0.25, 0.65] | 0.51 [0.34, 0.68] | 0.06 [-0.20, 0.34] |
| relation = languages | 29 | 0.00 [0.00, 0.00] | 0.54 [0.41, 0.67] | 0.54 [0.41, 0.67] |
| relation = people | 10 | 0.00 [0.00, 0.00] | 0.56 [0.12, 0.86] | 0.56 [0.12, 0.86] |
| half = A | 67 | 0.38 [0.22, 0.55] | 0.53 [0.40, 0.66] | 0.15 [-0.07, 0.38] |
| half = B | 70 | 0.30 [0.14, 0.54] | 0.61 [0.51, 0.71] | 0.31 [0.07, 0.49] |

## The recall's lure (separate outcome)

Share of recall reads on the passage's value for the edited bridge: whole 0.01, no_part 0.08, no_rand 0.01.
