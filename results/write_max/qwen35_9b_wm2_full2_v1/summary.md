# write_max v2 / qwen35_9b_wm2_full2_v1: 262 cases (52 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=58, 29 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 57 [45-69] | - | 5 | final, 19, 1 | 16 |
| lens_add | 2 [0-6] | 0 | 3 | final, 14, 0.8 | 73 |
| lens_swap | 0 [0-0] | 0 | 2 | question, 14, 1 | 48 |
| lens_transpl | 3 [0-9] | 2 | 3 | final, joint, 2 | 30 |
| early_lens_add | 9 [2-16] | 0 | 14 | question, 10, 0.4 | 6 |
| early_embed_add | 0 [0-0] | 0 | 3 | question, 8, 0.2 | 5 |
| dom_add | 24 [14-36] | 0 | 51 | question, joint, 0.4 | 75 |
| dom_natural | 16 [5-27] | 0 | 7 | final, 20, 2 | 32 |

## PM (n=58, 29 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 57 [46-69] | - | 3 | final, 19, 1 | 16 |
| lens_add | 17 [7-31] | 0 | 14 | question, joint, 0.1 | 56 |
| lens_swap | 16 [7-28] | 0 | 9 | final, joint, 4 | 47 |
| lens_transpl | 10 [3-18] | 0 | 16 | final, 20, 2 | 24 |
| early_lens_add | 5 [0-12] | 0 | 2 | question, 8, 0.2 | 2 |
| early_embed_add | 3 [0-9] | 0 | 5 | question, 10, 0.2 | 3 |
| dom_add | 36 [20-51] | 0 | 11 | final, 20, 0.4 | 62 |
| dom_natural | 20 [9-33] | 0 | 13 | final, 17, 2 | 27 |

## MP (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 80 [70-90] | - | 4 | question, joint, 1 | 16 |
| lens_add | 8 [0-20] | 0 | 8 | question, joint, 0.2 | 67 |
| lens_swap | 4 [0-10] | 0 | 0 | question, joint, 4 | 48 |
| lens_transpl | 4 [0-16] | 0 | 8 | question, joint, 1 | 28 |
| early_lens_add | 4 [0-10] | 0 | 4 | question, 10, 0.4 | 5 |
| early_embed_add | 0 [0-0] | 0 | 4 | question, 8, 0.2 | 4 |
| dom_add | 11 [0-27] | 0 | 11 | question, 17, 0.4 | 39 |
| dom_natural | 0 [0-0] | 0 | 0 | question, 14, 1 | 15 |

## MM (n=25, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 76 [61-94] | - | 0 | final, 20, 1 | 16 |
| lens_add | 72 [53-86] | 0 | 8 | final, 20, 0.8 | 77 |
| lens_swap | 32 [14-43] | 0 | 16 | final, joint, 4 | 48 |
| lens_transpl | 24 [5-46] | 0 | 8 | final, joint, 1 | 31 |
| early_lens_add | 20 [4-39] | 0 | 0 | question, 8, 0.8 | 9 |
| early_embed_add | 12 [0-35] | 0 | 0 | question, 12, 0.8 | 9 |
| dom_add | 58 [35-76] | 0 | 16 | final, 20, 0.8 | 66 |
| dom_natural | 68 [50-83] | 0 | 16 | final, 20, 2 | 29 |

## CP (n=48, 24 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 73 [60-85] | - | 0 | final, 20, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 14, 0.05 | 78 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 14, 1 | 48 |
| lens_transpl | 8 [2-16] | 0 | 0 | final, joint, 2 | 32 |
| dom_add | 17 [5-31] | 0 | 7 | final, 18, 0.4 | 79 |
| dom_natural | 15 [5-26] | 0 | 5 | final, 20, 2 | 32 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 9 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 9 |

## CM (n=48, 24 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 71 [51-88] | - | 4 | final, 20, 1 | 16 |
| lens_add | 21 [8-33] | 0 | 15 | final, joint, 0.1 | 67 |
| lens_swap | 15 [5-24] | 0 | 15 | final, joint, 4 | 48 |
| lens_transpl | 15 [7-24] | 2 | 10 | final, 19, 2 | 28 |
| dom_add | 54 [39-68] | 0 | 20 | final, 20, 0.8 | 69 |
| dom_natural | 41 [26-59] | 2 | 24 | final, 19, 2 | 29 |
| early_lens_add | 4 [0-10] | 2 | 6 | question, 10, 0.4 | 6 |
| early_embed_add | 2 [0-7] | 0 | 4 | question, 8, 0.4 | 6 |

Rules (MP vs MM): {"MP_lens_le_control_plus_5": false, "MM_lens_ge_4x_control_and_10pct": true, "C2_holds": false, "MP_early_lens_is_injection": true}
