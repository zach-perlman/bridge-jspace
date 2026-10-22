# write_max v2 / qwen3_32b_wm2_full2_late_v1: 294 cases (48 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=55, 31 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 54, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 0 | final, 54, 0.05 | 29 |

## PM (n=55, 31 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 54, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 0 | final, 54, 0.05 | 20 |

## MP (n=40, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 56, 1 | 6 |
| lens_add | 2 [0-7] | 2 | 0 | final, 54, 0.05 | 29 |

## MM (n=40, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 54, 1 | 6 |
| lens_add | 35 [16-54] | 0 | 10 | final, 54, 0.4 | 25 |

## CP (n=52, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 60, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 0 | final, 54, 0.05 | 29 |

## CM (n=52, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 54, 1 | 6 |
| lens_add | 19 [7-33] | 4 | 23 | final, 54, 0.4 | 23 |

