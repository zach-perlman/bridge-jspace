# write_max v2 / qwen35_9b_wm2_fresh2_v1: 250 cases (48 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=59, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 46 [31-62] | - | 10 | question, joint, 1 | 16 |
| lens_add | 7 [2-13] | 0 | 36 | final, joint, 0.4 | 73 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 14, 1 | 48 |
| lens_transpl | 2 [0-5] | 0 | 0 | question, 15, 1 | 31 |
| dom_add | 14 [8-21] | 0 | 10 | final, 18, 0.4 | 74 |
| dom_natural | 18 [10-27] | 0 | 4 | final, 18, 2 | 32 |
| early_lens_add | 2 [0-6] | 2 | 5 | question, 8, 0.4 | 5 |
| early_embed_add | 2 [0-5] | 2 | 2 | question, 12, 0.4 | 6 |

## PM (n=59, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 46 [33-60] | - | 14 | final, 19, 1 | 16 |
| lens_add | 22 [9-38] | 2 | 14 | final, joint, 0.2 | 62 |
| lens_swap | 10 [3-19] | 0 | 5 | final, joint, 2 | 46 |
| lens_transpl | 12 [5-22] | 2 | 7 | final, joint, 1 | 28 |
| dom_add | 37 [26-50] | 2 | 14 | final, 20, 0.4 | 60 |
| dom_natural | 51 [36-67] | 0 | 22 | final, 20, 2 | 28 |
| early_lens_add | 25 [13-41] | 0 | 22 | question, 10, 0.4 | 4 |
| early_embed_add | 2 [0-6] | 0 | 0 | question, 8, 0.2 | 2 |

## MP (n=18, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 78 [59-94] | - | 0 | final, 18, 1 | 16 |
| lens_add | 6 [0-20] | 0 | 6 | final, 14, 0.8 | 72 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 14, 1 | 48 |
| lens_transpl | 17 [0-40] | 0 | 6 | question, joint, 2 | 30 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 7 |
| early_embed_add | 11 [0-25] | 0 | 17 | question, 10, 0.8 | 7 |
| dom_add | 60 [14-89] | 0 | 0 | final, joint, 0.2 | 78 |
| dom_natural | 50 [14-72] | 0 | 0 | final, 18, 2 | 32 |

## MM (n=18, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 83 [65-100] | - | 0 | final, 20, 1 | 16 |
| lens_add | 61 [39-88] | 0 | 6 | final, 18, 0.8 | 73 |
| lens_swap | 44 [22-71] | 0 | 11 | final, joint, 4 | 48 |
| lens_transpl | 22 [5-47] | 0 | 6 | final, joint, 1 | 29 |
| early_lens_add | 17 [0-40] | 0 | 22 | question, 8, 0.8 | 8 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 9 |
| dom_add | 90 [62-100] | 0 | 10 | final, 20, 0.8 | 76 |
| dom_natural | 70 [50-100] | 0 | 20 | final, 20, 2 | 30 |

## CP (n=48, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 81 [67-92] | - | 0 | final, 20, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 14, 0.05 | 78 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 14, 1 | 48 |
| lens_transpl | 2 [0-6] | 0 | 0 | question, joint, 2 | 32 |
| dom_add | 19 [5-33] | 0 | 5 | final, 17, 0.8 | 78 |
| dom_natural | 12 [3-24] | 0 | 2 | final, 18, 2 | 32 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 9 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 9 |

## CM (n=48, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 58 [44-75] | - | 4 | final, joint, 1 | 16 |
| lens_add | 21 [8-36] | 0 | 8 | final, joint, 0.1 | 66 |
| lens_swap | 15 [6-25] | 4 | 21 | final, joint, 4 | 48 |
| lens_transpl | 12 [3-23] | 0 | 4 | final, joint, 1 | 28 |
| dom_add | 33 [21-43] | 2 | 14 | final, 19, 0.4 | 67 |
| dom_natural | 52 [40-65] | 0 | 17 | final, 19, 2 | 27 |
| early_lens_add | 4 [0-10] | 0 | 4 | question, 12, 0.4 | 4 |
| early_embed_add | 0 [0-0] | 0 | 2 | question, 8, 0.2 | 3 |

Rules (MP vs MM): {"MP_lens_le_control_plus_5": false, "MM_lens_ge_4x_control_and_10pct": true, "C2_holds": false, "MP_early_lens_is_injection": false}
