# Natural passages: muse30b_x5_natural_pcfnat

Fixed in advance (Dan, 25 Oct ~00:20; spec jobs/c3/x5_natural.yaml; prediction: batch 31, Q31.6). Model muse-glimmer-30b, layer 26, 60 items, 37 bridge entities. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Rule: HOLDS (gap 0.95 [0.65, 1.33])

Rule: gap >= 0.3 with lower CI >= 0.15 holds; <= 0.1 fails; otherwise mixed.

Lookup excess -0.20 [-0.55, 0.00]; recall excess 0.75 [0.63, 0.87].

## By relation and by half (descriptive)

| subset | n | lookup excess | recall excess | gap |
|---|---|---|---|---|
| relation = animals | 2 | nan [nan, nan] | 1.00 [1.00, 1.00] | nan [nan, nan] |
| relation = countries | 22 | -0.25 [-1.00, 0.00] | 0.68 [0.48, 0.87] | 0.93 [0.52, 1.62] |
| relation = languages | 28 | -0.20 [-0.67, 0.00] | 0.83 [0.67, 0.96] | 1.03 [0.69, 1.55] |
| relation = people | 8 | 0.00 [0.00, 0.00] | 0.67 [0.33, 1.00] | 0.67 [0.33, 1.00] |
| half = A | 29 | 0.00 [0.00, 0.00] | 0.77 [0.61, 0.91] | 0.77 [0.61, 0.91] |
| half = B | 31 | -0.33 [-0.80, 0.00] | 0.74 [0.55, 0.90] | 1.07 [0.56, 1.61] |

## The recall's lure (separate outcome)

Share of recall reads on the passage's value for the edited bridge: whole 0.00, no_part 0.10, no_rand 0.00.
