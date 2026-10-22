# write_max v2 / muse30_wm2_full2_aligned_v1: 312 cases (60 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=60, 28 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 70 [61-80] | - | 3 | final, 32, 1 | 14 |
| lens_add | 13 [5-23] | 0 | 27 | question, joint, 0.2 | 65 |
| lens_swap | 2 [0-6] | 0 | 0 | question, joint, 4 | 42 |
| early_lens_add | 2 [0-6] | 0 | 17 | question, 13, 0.8 | 8 |
| early_embed_add | 2 [0-6] | 0 | 0 | question, 13, 0.4 | 9 |

## PM (n=60, 28 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 55 [45-65] | - | 10 | final, 32, 1 | 14 |
| lens_add | 12 [4-22] | 0 | 25 | question, joint, 0.1 | 55 |
| lens_swap | 5 [0-10] | 0 | 8 | question, joint, 4 | 42 |
| early_lens_add | 7 [0-17] | 0 | 13 | question, 20, 0.4 | 6 |
| early_embed_add | 2 [0-5] | 0 | 5 | question, 13, 0.4 | 6 |

## MP (n=48, 22 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 98 [92-100] | - | 0 | final, 32, 1 | 14 |
| lens_add | 10 [2-19] | 0 | 4 | final, 30, 0.8 | 62 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 22, 1 | 42 |
| early_lens_add | 6 [0-16] | 0 | 4 | question, 16, 0.8 | 9 |
| early_embed_add | 2 [0-6] | 2 | 6 | question, 20, 0.8 | 10 |

## MM (n=48, 22 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 81 [69-92] | - | 2 | final, 32, 1 | 14 |
| lens_add | 50 [24-70] | 0 | 21 | final, joint, 0.1 | 63 |
| lens_swap | 6 [0-18] | 2 | 0 | question, joint, 2 | 42 |
| early_lens_add | 8 [0-22] | 0 | 6 | question, 16, 0.8 | 9 |
| early_embed_add | 2 [0-8] | 0 | 6 | question, 13, 0.8 | 9 |

## CP (n=48, 24 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 96 [91-100] | - | 2 | final, 32, 1 | 14 |
| lens_add | 8 [2-16] | 0 | 10 | question, joint, 0.2 | 68 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 22, 1 | 42 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 13, 0.2 | 11 |
| early_embed_add | 6 [0-14] | 0 | 8 | question, 20, 1.6 | 12 |

## CM (n=48, 24 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 81 [69-93] | - | 8 | final, 32, 1 | 14 |
| lens_add | 21 [11-34] | 0 | 33 | final, joint, 0.1 | 57 |
| lens_swap | 2 [0-7] | 0 | 8 | final, joint, 4 | 42 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 13, 0.2 | 7 |
| early_embed_add | 0 [0-0] | 0 | 2 | question, 13, 0.2 | 8 |

