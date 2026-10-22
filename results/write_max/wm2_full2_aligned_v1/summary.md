# write_max v2 / wm2_full2_aligned_v1: 482 cases (46 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=87, 35 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 68 [59-76] | - | 0 | final, 60, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 48, 0.05 | 78 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 48, 1 | 48 |
| early_lens_add | 10 [4-18] | 0 | 71 | question, 16, 0.4 | 8 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 8 |

## PM (n=87, 35 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 95 [88-100] | - | 1 | final, 60, 1 | 16 |
| lens_add | 14 [6-22] | 0 | 15 | final, 48, 0.8 | 77 |
| lens_swap | 7 [1-14] | 0 | 9 | final, joint, 1 | 45 |
| early_lens_add | 43 [28-56] | 0 | 48 | question, 16, 0.4 | 6 |
| early_embed_add | 5 [0-11] | 1 | 13 | question, 20, 0.8 | 7 |

## MP (n=72, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 74 [63-84] | - | 0 | final, 60, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 48, 0.05 | 78 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 48, 1 | 48 |
| early_lens_add | 15 [6-27] | 0 | 4 | question, 24, 0.8 | 9 |
| early_embed_add | 1 [0-5] | 0 | 10 | question, 16, 0.8 | 9 |

## MM (n=72, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 94 [88-99] | - | 0 | final, 60, 1 | 16 |
| lens_add | 19 [4-40] | 0 | 22 | final, joint, 0.1 | 71 |
| lens_swap | 14 [1-30] | 0 | 24 | final, joint, 1 | 46 |
| early_lens_add | 3 [0-8] | 0 | 6 | question, 16, 0.2 | 5 |
| early_embed_add | 0 [0-0] | 0 | 3 | question, 16, 0.2 | 8 |

## CP (n=82, 32 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 68 [55-80] | - | 0 | question, joint, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 48, 0.05 | 78 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 48, 1 | 48 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 11 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 11 |

## CM (n=82, 32 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 95 [90-99] | - | 1 | final, 58, 1 | 16 |
| lens_add | 21 [12-31] | 1 | 17 | final, 48, 0.8 | 75 |
| lens_swap | 11 [5-18] | 0 | 13 | final, joint, 1 | 45 |
| early_lens_add | 4 [0-8] | 0 | 4 | question, 20, 0.8 | 8 |
| early_embed_add | 1 [0-4] | 0 | 2 | question, 20, 0.8 | 8 |

