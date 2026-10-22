# write_max v2 / qwen3_32b_wm2_posctrl_v1: 180 cases (13 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## RR (n=60, 15 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 23 |
| lens_add | 63 [47-79] | 2 | 12 | all, 40, 0.2 | 96 |
| lens_swap | 100 [100-100] | 3 | 0 | all, 36, 4 | 71 |
| lens_transpl | 100 [100-100] | 3 | 0 | all, 36, 2 | 46 |
| dom_add | 19 [7-33] | 0 | 9 | all, 36, 0.2 | 95 |
| dom_natural | 60 [45-73] | 0 | 34 | all, joint, 2 | 48 |
| early_lens_add | 13 [5-24] | 0 | 5 | question, 24, 1.6 | 12 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 12 |

## R (n=60, 9 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 23 |
| lens_add | 97 [92-100] | 0 | 0 | all, 36, 0.1 | 97 |
| lens_swap | 100 [100-100] | 0 | 0 | all, 34, 4 | 71 |
| lens_transpl | 100 [100-100] | 0 | 0 | all, 28, 2 | 44 |
| dom_add | 75 [64-89] | 0 | 12 | all, 34, 0.2 | 94 |
| dom_natural | 72 [60-84] | 0 | 8 | all, joint, 1 | 48 |
| early_lens_add | 38 [21-62] | 0 | 18 | question, 16, 1.6 | 10 |
| early_embed_add | 2 [0-5] | 0 | 0 | question, 16, 0.8 | 11 |

## B (n=60, 13 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 28, 1 | 23 |
| lens_add | 100 [100-100] | 0 | 0 | all, 32, 0.2 | 99 |
| lens_swap | 100 [100-100] | 0 | 0 | all, 28, 2 | 71 |
| lens_transpl | 100 [100-100] | 0 | 0 | all, 28, 2 | 46 |
| dom_add | 27 [15-39] | 0 | 5 | all, 32, 0.2 | 99 |
| dom_natural | 78 [65-90] | 0 | 22 | all, joint, 2 | 48 |
| early_lens_add | 55 [42-68] | 0 | 20 | question, 16, 1.6 | 11 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 16, 0.2 | 10 |

