# write_max v2 / gptoss20_wm2_full2_v1: 118 cases (40 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 4 [0-14] | - | 16 | question, 14, 1 | 14 |
| lens_add | 16 [0-29] | 0 | 48 | question, 12, 0.8 | 59 |
| lens_swap | 4 [0-14] | 0 | 8 | question, joint, 4 | 42 |
| early_lens_add | 4 [0-14] | 0 | 12 | question, 8, 0.4 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 4, 0.2 | 3 |

## PM (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 12 [0-28] | - | 8 | question, 13, 1 | 14 |
| lens_add | 4 [0-13] | 0 | 36 | question, 12, 0.4 | 42 |
| lens_swap | 0 [0-0] | 0 | 4 | question, 10, 1 | 36 |
| early_lens_add | 0 [0-0] | 0 | 40 | question, 4, 0.2 | 1 |
| early_embed_add | 0 [0-0] | 0 | 20 | question, 6, 0.2 | 2 |

## MP (n=11, 7 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 10, 1 | 14 |
| lens_add | 0 [0-0] | 0 | 0 | question, 10, 0.05 | 52 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 10, 1 | 42 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 4, 0.2 | 6 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 4, 0.2 | 6 |

## MM (n=11, 7 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 18 [0-44] | - | 0 | question, 12, 1 | 14 |
| lens_add | 27 [0-62] | 0 | 27 | final, 15, 0.2 | 55 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 10, 1 | 42 |
| early_lens_add | 27 [0-67] | 0 | 0 | question, 8, 0.4 | 5 |
| early_embed_add | 18 [0-44] | 0 | 9 | question, 8, 0.8 | 7 |

## CP (n=23, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 4 [0-12] | - | 0 | final, 14, 1 | 14 |
| lens_add | 4 [0-12] | 0 | 0 | question, 10, 0.1 | 60 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 10, 1 | 42 |
| early_lens_add | 9 [0-20] | 4 | 43 | question, 8, 0.8 | 7 |
| early_embed_add | 4 [0-12] | 4 | 0 | question, 8, 0.8 | 7 |

## CM (n=23, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 4 [0-14] | - | 0 | question, 12, 1 | 14 |
| lens_add | 13 [0-25] | 4 | 87 | final, 13, 0.4 | 48 |
| lens_swap | 9 [0-23] | 0 | 30 | final, joint, 2 | 42 |
| early_lens_add | 9 [0-23] | 0 | 26 | question, 4, 0.4 | 5 |
| early_embed_add | 4 [0-14] | 0 | 0 | question, 8, 0.4 | 4 |

