# write_max v2 / qwen35_122b_wm2_full2_v1: 466 cases (56 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=78, 29 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 21, 1 | 22 |
| lens_add | 42 [31-54] | 0 | 31 | question, 24, 0.8 | 107 |
| lens_swap | 10 [2-21] | 0 | 22 | question, joint, 4 | 66 |
| early_lens_add | 35 [25-46] | 0 | 41 | question, 18, 0.8 | 9 |
| early_embed_add | 5 [1-10] | 0 | 4 | question, 15, 0.8 | 9 |

## PM (n=78, 29 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 3 [0-6] | - | 0 | question, 26, 1 | 22 |
| lens_add | 62 [49-74] | 0 | 31 | question, joint, 0.1 | 93 |
| lens_swap | 15 [7-25] | 0 | 29 | question, joint, 4 | 66 |
| early_lens_add | 13 [6-21] | 0 | 19 | question, 12, 0.4 | 5 |
| early_embed_add | 31 [21-41] | 0 | 27 | question, 12, 0.8 | 6 |

## MP (n=75, 26 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 12 [0-25] | - | 5 | question, 30, 1 | 22 |
| lens_add | 28 [13-45] | 1 | 5 | question, 29, 0.8 | 106 |
| lens_swap | 13 [3-24] | 0 | 7 | question, joint, 4 | 66 |
| early_lens_add | 9 [0-24] | 0 | 3 | question, 18, 0.8 | 9 |
| early_embed_add | 9 [0-25] | 0 | 3 | question, 18, 0.8 | 9 |

## MM (n=75, 26 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 8 [0-19] | - | 1 | question, 29, 1 | 22 |
| lens_add | 39 [23-52] | 0 | 11 | question, 30, 0.8 | 107 |
| lens_swap | 12 [5-22] | 0 | 7 | question, joint, 4 | 66 |
| early_lens_add | 8 [3-15] | 0 | 79 | question, 12, 1.6 | 12 |
| early_embed_add | 12 [2-27] | 0 | 45 | question, 18, 1.6 | 11 |

## CP (n=80, 30 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 21, 1 | 22 |
| lens_add | 2 [0-7] | 0 | 79 | question, joint, 0.4 | 108 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 21, 1 | 66 |
| early_lens_add | 2 [0-7] | 0 | 81 | question, 12, 1.6 | 12 |
| early_embed_add | 1 [0-4] | 0 | 46 | question, 12, 1.6 | 12 |

## CM (n=80, 30 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 2 [0-7] | - | 0 | final, 30, 1 | 22 |
| lens_add | 8 [2-14] | 0 | 24 | question, joint, 0.2 | 107 |
| lens_swap | 2 [0-6] | 1 | 1 | question, joint, 4 | 66 |
| early_lens_add | 2 [0-6] | 2 | 8 | question, 12, 0.8 | 9 |
| early_embed_add | 4 [0-9] | 1 | 5 | question, 12, 0.8 | 9 |

