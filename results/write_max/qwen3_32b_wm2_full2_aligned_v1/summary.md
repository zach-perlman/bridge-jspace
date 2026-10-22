# write_max v2 / qwen3_32b_wm2_full2_aligned_v1: 294 cases (48 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=55, 31 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 85 [78-93] | - | 0 | final, 52, 1 | 16 |
| lens_add | 2 [0-6] | 0 | 2 | question, 40, 0.8 | 77 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 40, 1 | 48 |
| early_lens_add | 18 [9-29] | 0 | 60 | question, 16, 1.6 | 10 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 9 |

## PM (n=55, 31 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 89 [81-96] | - | 7 | final, 52, 1 | 16 |
| lens_add | 24 [14-34] | 0 | 33 | final, joint, 0.1 | 52 |
| lens_swap | 2 [0-6] | 0 | 15 | question, joint, 4 | 44 |
| early_lens_add | 0 [0-0] | 0 | 4 | question, 16, 0.2 | 5 |
| early_embed_add | 0 [0-0] | 0 | 4 | question, 16, 0.2 | 5 |

## MP (n=40, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 52, 1 | 16 |
| lens_add | 8 [0-14] | 2 | 8 | question, joint, 0.2 | 74 |
| lens_swap | 5 [0-11] | 0 | 2 | final, joint, 4 | 48 |
| early_lens_add | 8 [0-16] | 2 | 0 | question, 16, 0.8 | 8 |
| early_embed_add | 5 [0-15] | 2 | 8 | question, 24, 1.6 | 9 |

## MM (n=40, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, joint, 1 | 16 |
| lens_add | 75 [55-90] | 0 | 12 | final, joint, 0.1 | 71 |
| lens_swap | 48 [25-70] | 0 | 12 | final, joint, 2 | 47 |
| early_lens_add | 10 [2-21] | 0 | 8 | question, 16, 1.6 | 12 |
| early_embed_add | 2 [0-9] | 0 | 8 | question, 20, 1.6 | 11 |

## CP (n=52, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 98 [94-100] | - | 0 | final, 52, 1 | 16 |
| lens_add | 2 [0-6] | 0 | 71 | final, joint, 0.4 | 78 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 40, 1 | 48 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 12 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 12 |

## CM (n=52, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 94 [88-100] | - | 2 | final, 52, 1 | 16 |
| lens_add | 29 [19-40] | 0 | 40 | final, joint, 0.1 | 61 |
| lens_swap | 10 [2-18] | 0 | 15 | final, 52, 4 | 47 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 8 |
| early_embed_add | 2 [0-6] | 0 | 2 | question, 24, 1.6 | 11 |

