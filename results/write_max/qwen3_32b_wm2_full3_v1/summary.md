# write_max v2 / qwen3_32b_wm2_full3_v1: 203 cases (32 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PPP (n=40, 20 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 28, 1 | 16 |
| lens_add | 20 [8-34] | 0 | 52 | question, joint, 0.2 | 67 |
| lens_swap | 20 [8-33] | 2 | 22 | question, joint, 4 | 48 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 28, 1 | 27 |
| dom_add | 44 [26-66] | 3 | 31 | question, joint, 0.1 | 65 |
| dom_natural | 22 [8-37] | 0 | 44 | question, joint, 2 | 30 |
| early_lens_add | 8 [0-16] | 0 | 15 | question, 24, 0.8 | 9 |
| early_embed_add | 0 [0-0] | 0 | 2 | question, 16, 0.2 | 8 |

## PPM (n=39, 21 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 3 [0-8] | - | 0 | question, 38, 1 | 16 |
| lens_add | 23 [11-35] | 0 | 31 | question, joint, 0.1 | 40 |
| lens_swap | 13 [4-24] | 0 | 3 | question, joint, 1 | 39 |
| lens_transpl | 5 [0-13] | 0 | 3 | question, 30, 1 | 19 |
| dom_add | 16 [6-29] | 0 | 6 | final, joint, 0.1 | 44 |
| dom_natural | 16 [6-27] | 3 | 55 | question, joint, 1 | 16 |
| early_lens_add | 3 [0-8] | 0 | 0 | question, 16, 0.2 | 1 |
| early_embed_add | 10 [2-20] | 3 | 3 | question, 24, 0.4 | 4 |

## PMP (n=40, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 28, 1 | 16 |
| lens_add | 15 [7-22] | 2 | 62 | question, joint, 0.2 | 74 |
| lens_swap | 8 [3-12] | 0 | 35 | question, joint, 4 | 48 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 28, 1 | 31 |
| dom_add | 10 [3-19] | 0 | 33 | question, joint, 0.1 | 70 |
| dom_natural | 13 [3-26] | 0 | 56 | question, joint, 2 | 32 |
| early_lens_add | 10 [0-22] | 0 | 20 | question, 24, 0.8 | 9 |
| early_embed_add | 2 [0-11] | 0 | 18 | question, 16, 1.6 | 10 |

## MPM (n=23, 13 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 4 [0-13] | - | 4 | question, 34, 1 | 16 |
| lens_add | 30 [14-45] | 0 | 17 | question, joint, 0.2 | 40 |
| lens_swap | 4 [0-13] | 0 | 0 | question, 28, 4 | 41 |
| lens_transpl | 9 [0-18] | 0 | 4 | question, 32, 1 | 19 |
| dom_add | 16 [0-29] | 0 | 11 | question, joint, 0.1 | 24 |
| dom_natural | 11 [0-22] | 0 | 5 | final, 28, 1 | 9 |
| early_lens_add | 4 [0-13] | 4 | 4 | question, 20, 0.4 | 3 |
| early_embed_add | 4 [0-13] | 4 | 4 | question, 16, 0.2 | 4 |

## MMP (n=40, 16 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 28, 1 | 16 |
| lens_add | 12 [0-26] | 0 | 28 | question, joint, 0.2 | 72 |
| lens_swap | 12 [3-22] | 2 | 5 | final, joint, 4 | 47 |
| lens_transpl | 2 [0-12] | 0 | 2 | question, 30, 2 | 30 |
| dom_add | 21 [9-31] | 3 | 41 | final, joint, 0.2 | 70 |
| dom_natural | 9 [0-20] | 0 | 18 | question, joint, 2 | 31 |
| early_lens_add | 5 [0-12] | 2 | 20 | question, 16, 1.6 | 9 |
| early_embed_add | 5 [0-12] | 2 | 0 | question, 16, 0.8 | 10 |

## MPP (n=21, 15 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 14 [0-32] | - | 5 | question, 40, 1 | 16 |
| lens_add | 38 [20-55] | 0 | 19 | question, joint, 0.2 | 71 |
| lens_swap | 14 [0-27] | 0 | 0 | question, joint, 4 | 48 |
| lens_transpl | 10 [0-24] | 0 | 5 | question, joint, 1 | 30 |
| early_lens_add | 19 [5-37] | 5 | 10 | question, 20, 1.6 | 11 |
| early_embed_add | 10 [0-26] | 5 | 5 | question, 24, 1.6 | 10 |
| dom_add | 56 [33-79] | 0 | 12 | question, joint, 0.2 | 54 |
| dom_natural | 12 [0-33] | 0 | 0 | question, joint, 1 | 24 |

