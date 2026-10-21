# write_max v2 / wm2_suite_v1: 360 cases (14 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## BL (n=60, 16 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 21 |
| lens_add | 12 [6-18] | 0 | 87 | all, joint, 0.2 | 115 |
| lens_swap | 17 [8-27] | 2 | 22 | all, joint, 4 | 72 |
| lens_transpl | 97 [92-100] | 0 | 0 | all, joint, 1 | 47 |
| dom_add | 60 [45-74] | 0 | 23 | question, joint, 0.1 | 116 |
| dom_natural | 37 [25-48] | 0 | 7 | question, joint, 2 | 48 |
| early_lens_add | 20 [10-32] | 0 | 12 | question, 16, 0.4 | 11 |
| early_embed_add | 3 [0-7] | 3 | 58 | question, 24, 1.6 | 11 |

## BR (n=60, 16 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 21 |
| lens_add | 100 [100-100] | 0 | 0 | all, 28, 0.4 | 115 |
| lens_swap | 100 [100-100] | 0 | 0 | all, 30, 4 | 71 |
| lens_transpl | 100 [100-100] | 0 | 0 | all, 28, 2 | 47 |
| dom_add | 100 [100-100] | 0 | 0 | question, 40, 0.8 | 114 |
| dom_natural | 96 [91-100] | 0 | 4 | question, joint, 2 | 48 |
| early_lens_add | 43 [30-58] | 0 | 40 | question, 16, 0.4 | 9 |
| early_embed_add | 3 [0-8] | 2 | 72 | question, 20, 1.6 | 10 |

## RL (n=60, 16 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 21 |
| lens_add | 13 [2-27] | 0 | 3 | all, 28, 0.8 | 116 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 28, 1 | 71 |
| lens_transpl | 100 [100-100] | 0 | 0 | all, joint, 1 | 48 |
| dom_add | 40 [27-55] | 0 | 5 | question, 32, 0.8 | 116 |
| dom_natural | 30 [21-40] | 0 | 2 | question, joint, 2 | 48 |
| early_lens_add | 3 [0-8] | 0 | 55 | question, 24, 1.6 | 11 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 11 |

## RR (n=60, 16 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 21 |
| lens_add | 100 [100-100] | 0 | 0 | all, 28, 0.4 | 116 |
| lens_swap | 100 [100-100] | 0 | 0 | all, 28, 4 | 71 |
| lens_transpl | 100 [100-100] | 0 | 0 | all, 40, 2 | 46 |
| dom_add | 96 [91-100] | 0 | 0 | all, 40, 0.8 | 116 |
| dom_natural | 84 [71-95] | 0 | 12 | all, joint, 2 | 48 |
| early_lens_add | 18 [6-33] | 0 | 80 | question, 16, 0.8 | 10 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 9 |

## R (n=60, 9 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 21 |
| lens_add | 100 [100-100] | 0 | 0 | question, 38, 0.4 | 111 |
| lens_swap | 100 [100-100] | 0 | 0 | all, 28, 2 | 68 |
| lens_transpl | 98 [95-100] | 0 | 2 | question, joint, 1 | 44 |
| dom_add | 100 [100-100] | 0 | 0 | all, 28, 0.4 | 112 |
| dom_natural | 100 [100-100] | 0 | 0 | all, joint, 1 | 48 |
| early_lens_add | 57 [38-78] | 0 | 13 | question, 24, 0.8 | 8 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 8 |

## B (n=60, 13 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 21 |
| lens_add | 100 [100-100] | 0 | 0 | question, 38, 0.4 | 113 |
| lens_swap | 100 [100-100] | 0 | 0 | question, 40, 4 | 71 |
| lens_transpl | 100 [100-100] | 0 | 0 | all, 28, 1 | 46 |
| dom_add | 100 [100-100] | 0 | 0 | all, 40, 0.4 | 113 |
| dom_natural | 97 [89-100] | 0 | 3 | all, joint, 1 | 48 |
| early_lens_add | 22 [11-35] | 0 | 65 | question, 16, 0.4 | 9 |
| early_embed_add | 2 [0-5] | 0 | 68 | question, 16, 0.8 | 9 |

Rules (RL vs RR): {"MP_lens_le_control_plus_5": false, "MM_lens_ge_4x_control_and_10pct": true, "C2_holds": false, "MP_early_lens_is_injection": true}
