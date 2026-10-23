# write_max v2 / qwen35_9b_wm2_posctrl_v1: 180 cases (15 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## RR (n=60, 16 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 14, 1 | 23 |
| lens_add | 100 [100-100] | 0 | 0 | all, 14, 0.2 | 114 |
| lens_swap | 100 [100-100] | 0 | 0 | all, 14, 4 | 71 |
| lens_transpl | 100 [100-100] | 0 | 0 | all, joint, 1 | 47 |
| dom_add | 89 [77-98] | 2 | 2 | final, 19, 0.8 | 113 |
| dom_natural | 89 [79-98] | 0 | 4 | final, 20, 2 | 48 |
| early_lens_add | 15 [6-24] | 0 | 12 | question, 10, 0.8 | 9 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 8, 0.2 | 9 |

## R (n=60, 9 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | question, 20, 1 | 23 |
| lens_add | 100 [100-100] | 0 | 0 | question, 17, 0.4 | 111 |
| lens_swap | 100 [100-100] | 2 | 0 | all, 14, 2 | 71 |
| lens_transpl | 98 [95-100] | 0 | 0 | all, 20, 2 | 46 |
| dom_add | 100 [100-100] | 0 | 0 | all, 18, 0.4 | 112 |
| dom_natural | 100 [100-100] | 0 | 0 | all, joint, 2 | 48 |
| early_lens_add | 48 [26-72] | 0 | 2 | question, 12, 0.4 | 6 |
| early_embed_add | 2 [0-5] | 0 | 2 | question, 12, 0.4 | 6 |

## B (n=60, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | all, 14, 1 | 23 |
| lens_add | 100 [100-100] | 0 | 0 | question, 18, 0.4 | 114 |
| lens_swap | 100 [100-100] | 0 | 0 | all, 14, 2 | 71 |
| lens_transpl | 100 [100-100] | 0 | 0 | all, 14, 1 | 47 |
| dom_add | 100 [100-100] | 0 | 0 | all, 20, 0.4 | 114 |
| dom_natural | 92 [84-98] | 0 | 8 | all, joint, 2 | 48 |
| early_lens_add | 65 [46-82] | 0 | 0 | question, 12, 0.4 | 8 |
| early_embed_add | 2 [0-5] | 0 | 32 | question, 8, 0.8 | 7 |

