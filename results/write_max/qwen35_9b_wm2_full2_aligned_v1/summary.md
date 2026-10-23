# write_max v2 / qwen35_9b_wm2_full2_aligned_v1: 262 cases (52 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=58, 29 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 60 [46-75] | - | 7 | question, joint, 1 | 16 |
| lens_add | 3 [0-9] | 3 | 3 | question, 14, 0.4 | 72 |
| lens_swap | 0 [0-0] | 0 | 3 | question, 13, 1 | 48 |
| early_lens_add | 9 [2-16] | 2 | 14 | question, 10, 0.4 | 6 |
| early_embed_add | 2 [0-6] | 0 | 24 | question, 8, 0.8 | 6 |

## PM (n=58, 29 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 57 [46-69] | - | 3 | final, 19, 1 | 16 |
| lens_add | 21 [10-35] | 0 | 19 | question, joint, 0.1 | 54 |
| lens_swap | 10 [2-21] | 0 | 12 | question, joint, 4 | 48 |
| early_lens_add | 16 [7-26] | 0 | 21 | question, 8, 0.4 | 4 |
| early_embed_add | 3 [0-9] | 2 | 9 | question, 8, 0.4 | 2 |

## MP (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 84 [73-96] | - | 4 | question, joint, 1 | 16 |
| lens_add | 8 [0-29] | 0 | 12 | final, joint, 0.2 | 67 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 13, 1 | 48 |
| early_lens_add | 12 [0-26] | 0 | 8 | question, 12, 0.8 | 7 |
| early_embed_add | 8 [0-20] | 0 | 8 | question, 12, 0.8 | 5 |

## MM (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 68 [53-84] | - | 4 | final, joint, 1 | 16 |
| lens_add | 68 [47-85] | 0 | 12 | final, 19, 0.8 | 75 |
| lens_swap | 32 [10-47] | 0 | 12 | final, joint, 4 | 48 |
| early_lens_add | 20 [4-39] | 0 | 0 | question, 8, 0.8 | 9 |
| early_embed_add | 12 [0-35] | 0 | 0 | question, 12, 0.8 | 9 |

## CP (n=48, 24 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 71 [58-83] | - | 0 | final, 18, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 13, 0.05 | 78 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 13, 1 | 48 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 9 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 9 |

## CM (n=48, 24 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 67 [47-84] | - | 4 | final, 19, 1 | 16 |
| lens_add | 10 [3-19] | 2 | 19 | final, joint, 0.1 | 65 |
| lens_swap | 6 [0-17] | 0 | 0 | final, 19, 4 | 48 |
| early_lens_add | 19 [7-32] | 2 | 27 | question, 10, 0.8 | 7 |
| early_embed_add | 2 [0-7] | 0 | 4 | question, 8, 0.4 | 5 |

