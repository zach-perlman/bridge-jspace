# Natural passages: nem35l_x52_natural_below

**below gate (exploratory): the read gate fails (0.80 per reader on O; Lightning's natural passages: the lookup reads 0.77, results/x5_natural/nem35l_x52_natural/gate.json); the eligible passages only; hollow, never in the claims table or grades; the rule verbatim, no prediction (Dan's morning queue, 29 Oct)**

Fixed in advance (Dan, 25 Oct ~00:20; spec jobs/c3/x5_natural.yaml; prediction: batch 31, Q31.6). Model nemotron-3.5-lightning, layer 14, 36 items, 27 bridge entities. Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Rule: HOLDS (gap 0.56 [0.35, 0.82])

Rule: gap >= 0.3 with lower CI >= 0.15 holds; <= 0.1 fails; otherwise mixed.

Lookup excess -0.08 [-0.27, 0.00]; recall excess 0.49 [0.31, 0.67].

## By relation and by half (descriptive)

| subset | n | lookup excess | recall excess | gap |
|---|---|---|---|---|
| relation = countries | 19 | 0.00 [0.00, 0.00] | 0.44 [0.21, 0.70] | 0.44 [0.21, 0.70] |
| relation = languages | 16 | -0.17 [-0.50, 0.00] | 0.56 [0.29, 0.81] | 0.73 [0.38, 1.10] |
| half = A | 19 | 0.00 [0.00, 0.00] | 0.67 [0.43, 0.89] | 0.67 [0.43, 0.89] |
| half = B | 17 | -0.17 [-0.60, 0.00] | 0.29 [0.06, 0.56] | 0.46 [0.12, 1.01] |

## The recall's lure (separate outcome)

Share of recall reads on the passage's value for the edited bridge: whole 0.00, no_part 0.08, no_rand 0.00.
