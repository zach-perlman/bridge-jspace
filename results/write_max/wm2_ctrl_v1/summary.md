# write_max v2 / wm2_ctrl_v1: 116 cases (50 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=34, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 21 |
| lens_add | 9 [0-18] | 0 | 18 | all, joint, 0.1 | 110 |
| lens_swap | 3 [0-9] | 0 | 21 | all, joint, 2 | 71 |
| lens_transpl | 76 [61-90] | 0 | 21 | all, joint, 1 | 46 |
| early_lens_add | 9 [0-21] | 0 | 76 | question, 16, 0.4 | 8 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 9 |
| dom_add | 12 [0-30] | 0 | 25 | question, 34, 0.8 | 111 |
| dom_natural | 12 [0-22] | 0 | 0 | final, 40, 2 | 46 |

## PM (n=34, 23 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 21 |
| lens_add | 47 [29-69] | 0 | 21 | all, 36, 0.4 | 94 |
| lens_swap | 53 [34-71] | 3 | 24 | all, 28, 4 | 66 |
| lens_transpl | 82 [67-97] | 0 | 12 | all, 28, 2 | 41 |
| early_lens_add | 24 [9-37] | 0 | 18 | question, 16, 0.2 | 5 |
| early_embed_add | 3 [0-10] | 0 | 9 | question, 16, 0.4 | 5 |
| dom_add | 31 [8-50] | 0 | 56 | question, joint, 0.1 | 75 |
| dom_natural | 6 [0-25] | 0 | 0 | final, 36, 1 | 35 |

## MP (n=24, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 21 |
| lens_add | 38 [14-58] | 0 | 8 | question, 34, 0.8 | 105 |
| lens_swap | 21 [0-43] | 0 | 12 | question, joint, 1 | 64 |
| lens_transpl | 33 [19-50] | 0 | 8 | all, 32, 2 | 41 |
| dom_add | 12 [0-31] | 0 | 18 | question, 36, 0.8 | 94 |
| dom_natural | 6 [0-15] | 0 | 6 | final, 40, 1 | 44 |
| early_lens_add | 12 [0-29] | 0 | 0 | question, 24, 0.8 | 9 |
| early_embed_add | 4 [0-16] | 0 | 0 | question, 16, 0.8 | 10 |

## MM (n=24, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 96 [88-100] | - | 4 | all, 28, 1 | 21 |
| lens_add | 83 [64-96] | 0 | 12 | all, 32, 0.4 | 110 |
| lens_swap | 75 [54-93] | 0 | 17 | all, joint, 1 | 69 |
| lens_transpl | 88 [71-100] | 0 | 4 | all, 28, 2 | 41 |
| dom_add | 18 [0-45] | 0 | 29 | question, 40, 0.8 | 107 |
| dom_natural | 24 [6-44] | 0 | 12 | final, joint, 1 | 45 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 8 |
| early_embed_add | 4 [0-15] | 0 | 4 | question, 24, 0.8 | 8 |

Rules (MP vs MM): {"MP_lens_le_control_plus_5": false, "MM_lens_ge_4x_control_and_10pct": true, "C2_holds": false, "MP_early_lens_is_injection": true}
