# write_max v2 / qwen3_32b_wm2_full2_v1: 294 cases (48 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=55, 31 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 28, 1 | 16 |
| lens_add | 9 [2-18] | 0 | 76 | question, joint, 0.2 | 76 |
| lens_swap | 7 [2-14] | 0 | 22 | question, joint, 4 | 48 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 28, 1 | 31 |
| early_lens_add | 18 [9-29] | 0 | 60 | question, 16, 1.6 | 11 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 10 |
| dom_add | 9 [2-18] | 0 | 82 | question, joint, 0.2 | 77 |
| dom_natural | 11 [2-20] | 0 | 64 | question, joint, 2 | 32 |

## PM (n=55, 31 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 28, 1 | 16 |
| lens_add | 16 [5-29] | 0 | 27 | question, joint, 0.1 | 57 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 28, 1 | 47 |
| lens_transpl | 0 [0-0] | 0 | 5 | question, 28, 1 | 23 |
| early_lens_add | 0 [0-0] | 0 | 4 | question, 16, 0.2 | 5 |
| early_embed_add | 0 [0-0] | 0 | 4 | question, 16, 0.2 | 6 |
| dom_add | 2 [0-8] | 0 | 58 | final, joint, 0.2 | 61 |
| dom_natural | 4 [0-11] | 0 | 29 | question, joint, 1 | 28 |

## MP (n=40, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 8 [0-19] | - | 2 | question, 32, 1 | 16 |
| lens_add | 12 [2-24] | 2 | 15 | question, joint, 0.2 | 73 |
| lens_swap | 2 [0-7] | 2 | 0 | question, 28, 1 | 48 |
| lens_transpl | 5 [0-11] | 0 | 2 | question, 28, 2 | 30 |
| early_lens_add | 12 [0-26] | 5 | 15 | question, 24, 1.6 | 10 |
| early_embed_add | 2 [0-7] | 2 | 0 | question, 16, 0.2 | 8 |
| dom_add | 13 [0-32] | 3 | 0 | question, 40, 0.8 | 63 |
| dom_natural | 7 [0-16] | 3 | 10 | question, joint, 1 | 30 |

## MM (n=40, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 8 [0-20] | - | 0 | question, 32, 1 | 16 |
| lens_add | 10 [0-21] | 0 | 20 | question, joint, 0.4 | 78 |
| lens_swap | 10 [2-19] | 0 | 12 | final, joint, 4 | 48 |
| lens_transpl | 10 [0-22] | 0 | 48 | final, joint, 2 | 31 |
| early_lens_add | 10 [2-21] | 0 | 8 | question, 16, 1.6 | 11 |
| early_embed_add | 2 [0-9] | 0 | 8 | question, 20, 1.6 | 12 |
| dom_add | 10 [0-23] | 0 | 27 | final, joint, 0.2 | 76 |
| dom_natural | 7 [0-16] | 0 | 27 | final, joint, 1 | 31 |

## CP (n=52, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 28, 1 | 16 |
| lens_add | 2 [0-7] | 0 | 19 | question, joint, 0.2 | 78 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 28, 1 | 48 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 28, 1 | 32 |
| dom_add | 4 [0-11] | 0 | 33 | question, joint, 0.2 | 78 |
| dom_natural | 2 [0-7] | 0 | 48 | final, joint, 2 | 32 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 12 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 12 |

## CM (n=52, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 28, 1 | 16 |
| lens_add | 6 [0-14] | 0 | 17 | question, joint, 0.2 | 71 |
| lens_swap | 4 [0-9] | 2 | 4 | question, joint, 4 | 48 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 28, 1 | 28 |
| dom_add | 15 [6-25] | 2 | 48 | final, joint, 0.2 | 70 |
| dom_natural | 4 [0-11] | 0 | 17 | question, joint, 1 | 30 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 9 |
| early_embed_add | 0 [0-0] | 0 | 2 | question, 16, 0.2 | 9 |

Rules (MP vs MM): {"MP_lens_le_control_plus_5": false, "MM_lens_ge_4x_control_and_10pct": true, "C2_holds": false, "MP_early_lens_is_injection": true}
