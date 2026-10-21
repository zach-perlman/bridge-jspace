# write_max v2 / wm2_full2_v1: 240 cases (58 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=40, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 12 [5-20] | - | 0 | question, 40, 1 | 14 |
| lens_add | 2 [0-8] | 0 | 2 | question, 30, 0.8 | 77 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 28, 1 | 48 |
| lens_transpl | 35 [20-52] | 0 | 22 | question, joint, 2 | 32 |
| early_lens_add | 18 [5-31] | 0 | 55 | question, 16, 0.4 | 11 |
| early_embed_add | 2 [0-8] | 0 | 10 | question, 16, 0.8 | 10 |
| dom_add | 12 [3-23] | 0 | 3 | final, 36, 0.8 | 78 |
| dom_natural | 9 [0-20] | 0 | 3 | final, 40, 2 | 32 |

## PM (n=40, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 22 [12-33] | - | 8 | question, 40, 1 | 14 |
| lens_add | 18 [7-30] | 2 | 38 | question, 28, 0.8 | 73 |
| lens_swap | 5 [0-12] | 0 | 12 | question, joint, 2 | 48 |
| lens_transpl | 10 [0-23] | 0 | 8 | final, 40, 2 | 30 |
| early_lens_add | 35 [17-53] | 0 | 48 | question, 16, 0.4 | 6 |
| early_embed_add | 2 [0-9] | 0 | 8 | question, 20, 0.8 | 7 |
| dom_add | 25 [9-43] | 0 | 12 | final, 40, 0.8 | 71 |
| dom_natural | 19 [6-33] | 0 | 9 | final, 40, 2 | 31 |

## MP (n=40, 19 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 35 [21-54] | - | 2 | question, 40, 1 | 14 |
| lens_add | 30 [15-44] | 0 | 10 | question, joint, 0.1 | 76 |
| lens_swap | 18 [7-29] | 0 | 8 | question, joint, 2 | 48 |
| lens_transpl | 28 [11-49] | 0 | 8 | question, joint, 1 | 31 |
| early_lens_add | 20 [5-38] | 2 | 0 | question, 24, 0.8 | 8 |
| early_embed_add | 5 [0-12] | 0 | 45 | question, 20, 1.6 | 9 |
| dom_add | 25 [9-42] | 0 | 11 | question, 36, 0.8 | 73 |
| dom_natural | 14 [0-32] | 0 | 0 | final, 38, 2 | 32 |

## MM (n=40, 19 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 32 [15-56] | - | 0 | final, 40, 1 | 14 |
| lens_add | 45 [23-70] | 0 | 15 | question, joint, 0.1 | 76 |
| lens_swap | 22 [10-39] | 0 | 8 | question, joint, 2 | 48 |
| lens_transpl | 48 [32-68] | 2 | 2 | question, joint, 1 | 29 |
| early_lens_add | 10 [2-22] | 2 | 10 | question, 20, 0.8 | 7 |
| early_embed_add | 0 [0-0] | 0 | 5 | question, 16, 0.2 | 6 |
| dom_add | 29 [6-56] | 0 | 4 | final, 40, 0.8 | 69 |
| dom_natural | 21 [3-47] | 0 | 29 | question, joint, 2 | 30 |

## CP (n=40, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 2 [0-8] | - | 0 | final, 40, 1 | 14 |
| lens_add | 0 [0-0] | 0 | 0 | question, 28, 0.05 | 78 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 28, 1 | 48 |
| lens_transpl | 5 [0-15] | 0 | 40 | final, joint, 2 | 32 |
| dom_add | 16 [4-27] | 0 | 0 | final, 40, 0.8 | 78 |
| dom_natural | 3 [0-10] | 0 | 3 | final, 38, 2 | 32 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 10 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 11 |

## CM (n=40, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 15 [5-26] | - | 0 | final, 40, 1 | 14 |
| lens_add | 18 [6-32] | 0 | 5 | final, 36, 0.8 | 72 |
| lens_swap | 10 [2-21] | 0 | 0 | final, 40, 4 | 48 |
| lens_transpl | 18 [7-31] | 0 | 2 | final, 40, 2 | 30 |
| dom_add | 39 [22-58] | 0 | 3 | final, 40, 0.8 | 77 |
| dom_natural | 32 [14-52] | 0 | 0 | final, 40, 2 | 31 |
| early_lens_add | 5 [0-13] | 2 | 90 | question, 16, 0.8 | 8 |
| early_embed_add | 2 [0-9] | 0 | 15 | question, 16, 0.8 | 9 |

Rules (MP vs MM): {"MP_lens_le_control_plus_5": false, "MM_lens_ge_4x_control_and_10pct": true, "C2_holds": false, "MP_early_lens_is_injection": false}
