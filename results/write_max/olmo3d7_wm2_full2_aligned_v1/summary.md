# write_max v2 / olmo3d7_wm2_full2_aligned_v1: 90 cases (36 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=19, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 63 [40-88] | - | 11 | final, 18, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 12, 0.05 | 69 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 12, 1 | 48 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 7 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 4 |

## PM (n=19, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 63 [40-83] | - | 11 | final, 18, 1 | 16 |
| lens_add | 11 [0-28] | 0 | 21 | final, 18, 0.8 | 61 |
| lens_swap | 11 [0-29] | 0 | 0 | final, joint, 4 | 43 |
| early_lens_add | 21 [5-44] | 0 | 37 | question, 12, 0.8 | 8 |
| early_embed_add | 16 [0-37] | 0 | 16 | question, 10, 0.8 | 6 |

## MP (n=11, 8 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 18, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 12, 0.05 | 60 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 12, 1 | 47 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 7 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 8 |

## MM (n=11, 8 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 91 [70-100] | - | 9 | final, 18, 1 | 16 |
| lens_add | 9 [0-25] | 0 | 9 | final, 18, 0.8 | 71 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 12, 1 | 46 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 9 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 8 |

## CP (n=15, 9 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 18, 1 | 16 |
| lens_add | 7 [0-23] | 0 | 27 | question, joint, 0.8 | 74 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 12, 1 | 48 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 9 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 10 |

## CM (n=15, 9 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 93 [77-100] | - | 7 | final, 18, 1 | 16 |
| lens_add | 7 [0-23] | 0 | 7 | final, 13, 0.8 | 59 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 12, 1 | 45 |
| early_lens_add | 0 [0-0] | 0 | 7 | question, 8, 0.2 | 8 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 9 |

