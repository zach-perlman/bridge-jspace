# write_max v2 / qwen35_122b_wm2_full2_aligned_v1: 466 cases (56 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=78, 29 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 46, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 40, 0.05 | 80 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 40, 1 | 48 |
| early_lens_add | 35 [25-46] | 0 | 41 | question, 18, 0.8 | 9 |
| early_embed_add | 5 [1-10] | 0 | 4 | question, 15, 0.8 | 9 |

## PM (n=78, 29 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 97 [93-100] | - | 3 | final, 46, 1 | 16 |
| lens_add | 32 [22-41] | 0 | 17 | final, joint, 0.2 | 73 |
| lens_swap | 18 [8-26] | 0 | 8 | final, 43, 2 | 44 |
| early_lens_add | 13 [6-21] | 0 | 19 | question, 12, 0.4 | 6 |
| early_embed_add | 24 [15-34] | 3 | 24 | question, 15, 0.8 | 6 |

## MP (n=75, 26 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 97 [93-100] | - | 1 | final, 46, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 40, 0.05 | 80 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 40, 1 | 48 |
| early_lens_add | 9 [0-24] | 0 | 3 | question, 18, 0.8 | 11 |
| early_embed_add | 9 [0-25] | 0 | 3 | question, 18, 0.8 | 11 |

## MM (n=75, 26 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 46, 1 | 16 |
| lens_add | 39 [21-55] | 0 | 16 | final, joint, 0.2 | 77 |
| lens_swap | 28 [10-47] | 0 | 5 | final, 43, 4 | 47 |
| early_lens_add | 8 [0-23] | 0 | 5 | question, 18, 0.8 | 9 |
| early_embed_add | 8 [0-23] | 0 | 7 | question, 12, 0.8 | 9 |

## CP (n=80, 30 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 46, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 40, 0.05 | 80 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 40, 1 | 48 |
| early_lens_add | 2 [0-7] | 1 | 81 | question, 12, 1.6 | 12 |
| early_embed_add | 1 [0-4] | 0 | 46 | question, 12, 1.6 | 12 |

## CM (n=80, 30 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 46, 1 | 16 |
| lens_add | 51 [40-64] | 4 | 10 | final, 41, 0.8 | 76 |
| lens_swap | 26 [15-37] | 1 | 12 | final, 43, 4 | 45 |
| early_lens_add | 2 [0-6] | 1 | 8 | question, 12, 0.8 | 9 |
| early_embed_add | 4 [0-9] | 1 | 5 | question, 12, 0.8 | 9 |

