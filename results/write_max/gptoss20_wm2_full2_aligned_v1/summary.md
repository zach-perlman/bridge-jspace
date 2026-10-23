# write_max v2 / gptoss20_wm2_full2_aligned_v1: 118 cases (40 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 92 [83-100] | - | 4 | final, 19, 1 | 12 |
| lens_add | 8 [0-20] | 0 | 84 | final, 18, 0.2 | 45 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 15, 1 | 36 |
| early_lens_add | 4 [0-14] | 0 | 12 | question, 8, 0.4 | 4 |
| early_embed_add | 8 [0-20] | 0 | 16 | question, 8, 0.4 | 5 |

## PM (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 92 [78-100] | - | 8 | final, 19, 1 | 12 |
| lens_add | 4 [0-12] | 0 | 24 | question, 19, 0.1 | 31 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 15, 1 | 36 |
| early_lens_add | 4 [0-13] | 0 | 12 | question, 8, 0.2 | 1 |
| early_embed_add | 0 [0-0] | 0 | 20 | question, 6, 0.2 | 1 |

## MP (n=11, 7 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 18, 1 | 12 |
| lens_add | 9 [0-27] | 0 | 55 | question, 19, 0.2 | 41 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 15, 1 | 36 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 4, 0.2 | 6 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 4, 0.2 | 7 |

## MM (n=11, 7 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 91 [67-100] | - | 0 | final, 19, 1 | 12 |
| lens_add | 27 [0-67] | 0 | 9 | question, 17, 0.4 | 37 |
| lens_swap | 18 [0-44] | 0 | 36 | final, 19, 2 | 36 |
| early_lens_add | 27 [0-67] | 0 | 0 | question, 8, 0.4 | 6 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 4, 0.2 | 6 |

## CP (n=23, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 18, 1 | 12 |
| lens_add | 9 [0-21] | 0 | 57 | question, 17, 0.8 | 47 |
| lens_swap | 4 [0-12] | 0 | 0 | question, joint, 2 | 36 |
| early_lens_add | 9 [0-20] | 4 | 43 | question, 8, 0.8 | 7 |
| early_embed_add | 4 [0-12] | 0 | 0 | question, 8, 0.8 | 7 |

## CM (n=23, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 19, 1 | 12 |
| lens_add | 17 [0-41] | 4 | 26 | question, joint, 0.1 | 36 |
| lens_swap | 9 [0-23] | 0 | 9 | final, 18, 4 | 36 |
| early_lens_add | 9 [0-23] | 0 | 26 | question, 4, 0.4 | 5 |
| early_embed_add | 4 [0-14] | 0 | 0 | question, 8, 0.2 | 5 |

