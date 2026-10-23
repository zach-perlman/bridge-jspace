# write_max v2 / olmoh7_wm2_full2_v1: 108 cases (44 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=20, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 90 [76-100] | - | 5 | final, 20, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 5 | question, 14, 0.05 | 67 |
| lens_swap | 0 [0-0] | 0 | 5 | question, 14, 1 | 47 |
| early_lens_add | 5 [0-14] | 0 | 30 | question, 8, 0.8 | 5 |
| early_embed_add | 5 [0-15] | 0 | 10 | question, 8, 0.8 | 4 |

## PM (n=20, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 85 [68-96] | - | 15 | final, 20, 1 | 16 |
| lens_add | 15 [0-33] | 0 | 20 | question, 14, 0.4 | 48 |
| lens_swap | 25 [6-45] | 0 | 35 | final, joint, 4 | 46 |
| early_lens_add | 20 [4-41] | 5 | 15 | question, 12, 0.8 | 4 |
| early_embed_add | 5 [0-15] | 0 | 5 | question, 8, 0.2 | 4 |

## MP (n=17, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 94 [79-100] | - | 0 | final, 18, 1 | 16 |
| lens_add | 6 [0-20] | 0 | 6 | question, 14, 0.8 | 50 |
| lens_swap | 0 [0-0] | 0 | 6 | question, 14, 1 | 34 |
| early_lens_add | 12 [0-31] | 0 | 12 | question, 8, 0.8 | 5 |
| early_embed_add | 0 [0-0] | 0 | 6 | question, 8, 0.2 | 7 |

## MM (n=17, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 82 [58-100] | - | 6 | final, 20, 1 | 16 |
| lens_add | 41 [12-71] | 0 | 0 | final, 16, 0.8 | 59 |
| lens_swap | 29 [8-47] | 0 | 6 | final, 19, 4 | 44 |
| early_lens_add | 18 [0-37] | 0 | 6 | question, 8, 0.8 | 6 |
| early_embed_add | 12 [0-32] | 0 | 6 | question, 8, 0.4 | 8 |

## CP (n=17, 13 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 18, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 14, 0.05 | 71 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 14, 1 | 48 |
| early_lens_add | 12 [0-25] | 0 | 0 | question, 8, 1.6 | 8 |
| early_embed_add | 6 [0-21] | 0 | 0 | question, 8, 0.8 | 7 |

## CM (n=17, 13 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 71 [55-92] | - | 24 | final, 20, 1 | 16 |
| lens_add | 24 [6-50] | 0 | 6 | final, 20, 0.4 | 51 |
| lens_swap | 6 [0-19] | 0 | 0 | question, joint, 4 | 42 |
| early_lens_add | 12 [0-29] | 0 | 0 | question, 8, 0.8 | 5 |
| early_embed_add | 12 [0-31] | 0 | 0 | question, 12, 0.8 | 4 |

