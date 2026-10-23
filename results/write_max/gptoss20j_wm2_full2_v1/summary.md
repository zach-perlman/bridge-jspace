# write_max v2 / gptoss20j_wm2_full2_v1: 118 cases (40 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 4 [0-14] | - | 16 | question, 14, 1 | 14 |
| lens_add | 16 [4-29] | 0 | 68 | question, joint, 0.2 | 59 |
| lens_swap | 4 [0-12] | 0 | 20 | question, joint, 4 | 42 |
| early_lens_add | 0 [0-0] | 0 | 16 | question, 4, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 4, 0.2 | 3 |

## PM (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 12 [0-28] | - | 8 | question, 13, 1 | 14 |
| lens_add | 8 [0-19] | 0 | 28 | question, 12, 0.4 | 42 |
| lens_swap | 0 [0-0] | 0 | 4 | question, 10, 1 | 35 |
| early_lens_add | 4 [0-13] | 0 | 24 | question, 4, 0.2 | 1 |
| early_embed_add | 0 [0-0] | 0 | 20 | question, 6, 0.2 | 2 |

## MP (n=11, 7 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 10, 1 | 14 |
| lens_add | 0 [0-0] | 0 | 0 | question, 10, 0.05 | 52 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 10, 1 | 42 |
| early_lens_add | 9 [0-22] | 0 | 36 | question, 4, 0.4 | 6 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 4, 0.2 | 6 |

## MM (n=11, 7 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 18 [0-44] | - | 0 | question, 12, 1 | 14 |
| lens_add | 9 [0-33] | 0 | 9 | question, 15, 0.8 | 55 |
| lens_swap | 9 [0-27] | 0 | 9 | question, joint, 4 | 42 |
| early_lens_add | 9 [0-27] | 0 | 18 | question, 4, 0.2 | 5 |
| early_embed_add | 18 [0-44] | 0 | 9 | question, 8, 0.8 | 7 |

## CP (n=23, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 4 [0-12] | - | 0 | final, 14, 1 | 14 |
| lens_add | 13 [4-24] | 0 | 22 | question, 12, 0.8 | 60 |
| lens_swap | 4 [0-12] | 0 | 0 | question, 10, 4 | 42 |
| early_lens_add | 17 [5-32] | 4 | 35 | question, 8, 0.8 | 7 |
| early_embed_add | 4 [0-12] | 4 | 0 | question, 8, 0.8 | 7 |

## CM (n=23, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 4 [0-14] | - | 0 | question, 12, 1 | 14 |
| lens_add | 9 [0-23] | 4 | 22 | final, 12, 0.2 | 48 |
| lens_swap | 13 [0-29] | 0 | 48 | final, joint, 2 | 42 |
| early_lens_add | 9 [0-23] | 0 | 22 | question, 4, 0.2 | 5 |
| early_embed_add | 4 [0-14] | 0 | 0 | question, 8, 0.4 | 4 |

