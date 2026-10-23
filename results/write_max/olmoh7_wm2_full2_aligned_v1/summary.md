# write_max v2 / olmoh7_wm2_full2_aligned_v1: 108 cases (44 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=20, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 85 [70-100] | - | 5 | final, 19, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 5 | question, 13, 0.05 | 65 |
| lens_swap | 0 [0-0] | 0 | 5 | question, 13, 1 | 48 |
| early_lens_add | 5 [0-14] | 0 | 30 | question, 8, 0.8 | 5 |
| early_embed_add | 5 [0-15] | 0 | 10 | question, 8, 0.8 | 4 |

## PM (n=20, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 70 [52-88] | - | 20 | final, 19, 1 | 16 |
| lens_add | 5 [0-15] | 0 | 5 | question, 13, 0.2 | 51 |
| lens_swap | 10 [0-24] | 0 | 10 | final, 19, 4 | 47 |
| early_lens_add | 20 [4-41] | 5 | 15 | question, 12, 0.8 | 4 |
| early_embed_add | 5 [0-15] | 0 | 5 | question, 8, 0.2 | 4 |

## MP (n=17, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 94 [79-100] | - | 0 | final, 18, 1 | 16 |
| lens_add | 6 [0-20] | 0 | 6 | question, 13, 0.8 | 49 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 13, 1 | 26 |
| early_lens_add | 12 [0-31] | 0 | 12 | question, 8, 0.8 | 5 |
| early_embed_add | 0 [0-0] | 0 | 6 | question, 8, 0.2 | 7 |

## MM (n=17, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 59 [31-84] | - | 0 | final, 19, 1 | 16 |
| lens_add | 59 [29-81] | 0 | 29 | final, 19, 0.8 | 63 |
| lens_swap | 29 [14-44] | 0 | 18 | final, joint, 4 | 45 |
| early_lens_add | 18 [0-37] | 0 | 6 | question, 8, 0.8 | 6 |
| early_embed_add | 12 [0-32] | 0 | 6 | question, 8, 0.4 | 8 |

## CP (n=17, 13 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 18, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 13, 0.05 | 72 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 13, 1 | 48 |
| early_lens_add | 12 [0-25] | 0 | 0 | question, 8, 1.6 | 8 |
| early_embed_add | 6 [0-21] | 0 | 0 | question, 8, 0.8 | 7 |

## CM (n=17, 13 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 53 [32-79] | - | 24 | final, 18, 1 | 16 |
| lens_add | 41 [16-75] | 0 | 18 | final, joint, 0.2 | 57 |
| lens_swap | 6 [0-19] | 0 | 6 | question, joint, 4 | 44 |
| early_lens_add | 12 [0-29] | 0 | 0 | question, 8, 0.8 | 5 |
| early_embed_add | 12 [0-31] | 0 | 0 | question, 12, 0.8 | 4 |

