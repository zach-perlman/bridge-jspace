# write_max v2 / muse30_wm2_full2_v1: 312 cases (60 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=60, 28 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 75 [66-84] | - | 3 | final, 33, 1 | 14 |
| lens_add | 12 [4-22] | 0 | 20 | question, joint, 0.2 | 66 |
| lens_swap | 2 [0-6] | 0 | 0 | question, joint, 4 | 42 |
| early_lens_add | 2 [0-6] | 0 | 17 | question, 13, 0.8 | 8 |
| early_embed_add | 2 [0-6] | 0 | 0 | question, 13, 0.4 | 9 |

## PM (n=60, 28 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 68 [61-77] | - | 8 | final, 33, 1 | 14 |
| lens_add | 18 [9-30] | 0 | 25 | final, joint, 0.1 | 55 |
| lens_swap | 7 [2-13] | 0 | 3 | question, joint, 4 | 42 |
| early_lens_add | 7 [0-17] | 0 | 13 | question, 20, 0.4 | 6 |
| early_embed_add | 2 [0-5] | 0 | 5 | question, 13, 0.4 | 6 |

## MP (n=48, 22 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, joint, 1 | 14 |
| lens_add | 6 [0-13] | 0 | 15 | final, 29, 0.8 | 65 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 23, 1 | 42 |
| early_lens_add | 6 [0-16] | 0 | 4 | question, 16, 0.8 | 9 |
| early_embed_add | 2 [0-6] | 2 | 6 | question, 20, 0.8 | 10 |

## MM (n=48, 22 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 85 [74-95] | - | 4 | final, 33, 1 | 14 |
| lens_add | 56 [33-74] | 0 | 19 | final, joint, 0.1 | 63 |
| lens_swap | 10 [2-20] | 0 | 6 | final, joint, 2 | 42 |
| early_lens_add | 8 [0-22] | 0 | 6 | question, 16, 0.8 | 9 |
| early_embed_add | 2 [0-8] | 0 | 6 | question, 13, 0.8 | 9 |

## CP (n=48, 24 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 98 [94-100] | - | 2 | final, 33, 1 | 14 |
| lens_add | 6 [0-15] | 0 | 6 | question, joint, 0.2 | 68 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 23, 1 | 42 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 13, 0.2 | 11 |
| early_embed_add | 6 [0-14] | 0 | 8 | question, 20, 1.6 | 12 |

## CM (n=48, 24 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 88 [76-98] | - | 6 | final, 33, 1 | 14 |
| lens_add | 21 [9-35] | 0 | 35 | final, joint, 0.1 | 56 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 23, 1 | 42 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 13, 0.2 | 7 |
| early_embed_add | 0 [0-0] | 0 | 2 | question, 13, 0.2 | 8 |

