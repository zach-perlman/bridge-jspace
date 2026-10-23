# write_max v2 / gptoss20j_wm2_full2_aligned_v1: 118 cases (40 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 92 [83-100] | - | 4 | final, 19, 1 | 12 |
| lens_add | 4 [0-12] | 0 | 36 | question, 17, 0.4 | 45 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 15, 1 | 36 |
| early_lens_add | 4 [0-12] | 0 | 4 | question, 8, 0.4 | 4 |
| early_embed_add | 8 [0-20] | 0 | 16 | question, 8, 0.4 | 5 |

## PM (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 92 [78-100] | - | 8 | final, 19, 1 | 12 |
| lens_add | 8 [0-27] | 0 | 60 | final, 15, 0.2 | 31 |
| lens_swap | 4 [0-13] | 0 | 16 | question, 18, 4 | 32 |
| early_lens_add | 4 [0-13] | 0 | 4 | question, 8, 0.2 | 1 |
| early_embed_add | 0 [0-0] | 0 | 20 | question, 6, 0.2 | 1 |

## MP (n=11, 7 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 18, 1 | 12 |
| lens_add | 18 [0-50] | 0 | 55 | question, joint, 0.2 | 41 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 15, 1 | 36 |
| early_lens_add | 9 [0-22] | 0 | 36 | question, 4, 0.4 | 6 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 4, 0.2 | 7 |

## MM (n=11, 7 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 91 [67-100] | - | 0 | final, 19, 1 | 12 |
| lens_add | 27 [7-62] | 0 | 64 | final, 18, 0.1 | 37 |
| lens_swap | 27 [7-50] | 0 | 73 | final, 19, 2 | 35 |
| early_lens_add | 9 [0-27] | 0 | 18 | question, 4, 0.2 | 6 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 4, 0.2 | 6 |

## CP (n=23, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 18, 1 | 12 |
| lens_add | 9 [0-20] | 0 | 17 | question, 17, 0.4 | 47 |
| lens_swap | 4 [0-12] | 0 | 30 | question, joint, 4 | 36 |
| early_lens_add | 22 [6-35] | 4 | 52 | question, 6, 0.8 | 8 |
| early_embed_add | 4 [0-12] | 0 | 0 | question, 8, 0.8 | 7 |

## CM (n=23, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 19, 1 | 12 |
| lens_add | 13 [0-26] | 0 | 39 | question, 17, 0.4 | 36 |
| lens_swap | 9 [0-23] | 0 | 0 | question, 19, 2 | 34 |
| early_lens_add | 9 [0-23] | 0 | 22 | question, 4, 0.2 | 4 |
| early_embed_add | 4 [0-14] | 0 | 0 | question, 8, 0.2 | 5 |

