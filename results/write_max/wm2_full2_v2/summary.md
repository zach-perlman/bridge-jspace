# write_max v2 / wm2_full2_v2: 482 cases (46 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=87, 35 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 59 [49-68] | - | 39 | question, joint, 1 | 16 |
| lens_add | 2 [0-6] | 0 | 9 | question, 30, 0.8 | 77 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 28, 1 | 48 |
| lens_transpl | 44 [35-54] | 0 | 28 | question, joint, 2 | 32 |
| early_lens_add | 10 [4-18] | 0 | 71 | question, 16, 0.4 | 9 |
| early_embed_add | 1 [0-3] | 0 | 17 | question, 16, 0.8 | 9 |
| dom_add | 14 [6-23] | 0 | 59 | question, joint, 0.1 | 77 |
| dom_natural | 8 [3-14] | 0 | 64 | question, joint, 2 | 32 |

## PM (n=87, 35 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 53 [43-62] | - | 40 | question, joint, 1 | 16 |
| lens_add | 22 [14-30] | 0 | 40 | question, joint, 0.1 | 72 |
| lens_swap | 9 [3-16] | 0 | 32 | question, joint, 4 | 48 |
| lens_transpl | 13 [5-21] | 1 | 11 | final, joint, 1 | 30 |
| early_lens_add | 43 [28-56] | 0 | 48 | question, 16, 0.4 | 6 |
| early_embed_add | 2 [0-8] | 2 | 2 | question, 16, 0.4 | 6 |
| dom_add | 28 [16-41] | 1 | 10 | final, 40, 0.8 | 69 |
| dom_natural | 29 [14-47] | 0 | 17 | final, joint, 1 | 31 |

## MP (n=72, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 71 [58-82] | - | 8 | question, joint, 1 | 16 |
| lens_add | 36 [24-48] | 0 | 8 | question, joint, 0.1 | 77 |
| lens_swap | 21 [12-30] | 0 | 11 | question, joint, 1 | 48 |
| lens_transpl | 33 [22-49] | 0 | 4 | question, joint, 1 | 31 |
| early_lens_add | 15 [6-27] | 0 | 4 | question, 24, 0.8 | 9 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 8 |
| dom_add | 16 [6-29] | 0 | 11 | question, 36, 0.8 | 74 |
| dom_natural | 11 [2-21] | 0 | 8 | final, joint, 1 | 32 |

## MM (n=72, 25 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 53 [39-65] | - | 26 | question, joint, 1 | 16 |
| lens_add | 40 [26-56] | 0 | 17 | question, joint, 0.1 | 74 |
| lens_swap | 26 [14-43] | 0 | 3 | question, joint, 2 | 47 |
| lens_transpl | 36 [24-51] | 0 | 8 | question, joint, 1 | 30 |
| early_lens_add | 7 [1-14] | 0 | 8 | question, 20, 0.8 | 7 |
| early_embed_add | 0 [0-0] | 0 | 3 | question, 16, 0.2 | 8 |
| dom_add | 29 [12-47] | 0 | 5 | final, 36, 0.8 | 73 |
| dom_natural | 23 [9-37] | 0 | 2 | final, joint, 1 | 31 |

## CP (n=82, 32 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 40 [30-51] | - | 4 | question, joint, 1 | 16 |
| lens_add | 0 [0-0] | 0 | 0 | question, 28, 0.05 | 78 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 28, 1 | 48 |
| lens_transpl | 2 [0-6] | 0 | 39 | final, joint, 2 | 32 |
| dom_add | 10 [3-19] | 0 | 1 | final, 38, 0.8 | 77 |
| dom_natural | 6 [1-12] | 0 | 6 | final, joint, 1 | 32 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 11 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 11 |

## CM (n=82, 32 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 50 [41-60] | - | 18 | question, joint, 1 | 16 |
| lens_add | 21 [11-33] | 1 | 9 | final, 38, 0.8 | 75 |
| lens_swap | 11 [4-21] | 0 | 2 | final, joint, 1 | 48 |
| lens_transpl | 12 [5-20] | 0 | 10 | final, joint, 1 | 30 |
| dom_add | 31 [20-41] | 0 | 3 | final, 36, 0.8 | 74 |
| dom_natural | 22 [10-33] | 0 | 12 | final, joint, 1 | 31 |
| early_lens_add | 4 [0-8] | 0 | 4 | question, 20, 0.8 | 9 |
| early_embed_add | 1 [0-4] | 0 | 18 | question, 16, 0.8 | 9 |

Rules (MP vs MM): {"MP_lens_le_control_plus_5": false, "MM_lens_ge_4x_control_and_10pct": true, "C2_holds": false, "MP_early_lens_is_injection": false}
