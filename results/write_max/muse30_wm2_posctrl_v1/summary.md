# write_max v2 / muse30_wm2_posctrl_v1: 180 cases (14 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## RR (n=60, 14 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 31, 1 | 20 |
| lens_add | 100 [100-100] | 0 | 0 | all, 27, 0.4 | 99 |
| lens_swap | 100 [100-100] | 0 | 0 | all, 25, 4 | 63 |
| lens_transpl | 68 [55-80] | 0 | 17 | all, joint, 1 | 41 |
| dom_add | 85 [74-93] | 0 | 11 | all, joint, 0.05 | 95 |
| dom_natural | 93 [86-100] | 0 | 4 | final, 33, 2 | 41 |
| early_lens_add | 17 [3-34] | 0 | 3 | question, 16, 1.6 | 12 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 13, 0.2 | 12 |

## R (n=60, 10 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | question, 31, 1 | 20 |
| lens_add | 100 [100-100] | 0 | 0 | all, 27, 0.2 | 57 |
| lens_swap | 100 [100-100] | 0 | 0 | all, 23, 2 | 61 |
| lens_transpl | 73 [61-86] | 0 | 5 | all, 27, 2 | 27 |
| dom_add | 85 [75-94] | 0 | 15 | all, joint, 0.05 | 60 |
| dom_natural | 97 [91-100] | 0 | 2 | all, joint, 2 | 39 |
| early_lens_add | 0 [0-0] | 0 | 5 | question, 13, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 13, 0.2 | 5 |

## B (n=60, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 23, 1 | 20 |
| lens_add | 100 [100-100] | 0 | 0 | question, 33, 0.4 | 96 |
| lens_swap | 100 [100-100] | 0 | 0 | all, 23, 2 | 62 |
| lens_transpl | 100 [100-100] | 0 | 0 | all, 23, 2 | 40 |
| dom_add | 100 [100-100] | 0 | 0 | all, 31, 0.4 | 96 |
| dom_natural | 98 [94-100] | 0 | 0 | all, joint, 2 | 42 |
| early_lens_add | 63 [47-78] | 0 | 18 | question, 16, 0.8 | 9 |
| early_embed_add | 2 [0-5] | 0 | 0 | question, 16, 0.8 | 8 |

