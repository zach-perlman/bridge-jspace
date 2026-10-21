# write_max v2 / wm2_full3_v1: 213 cases (36 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PPP (n=40, 17 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 35 [19-49] | - | 22 | question, 36, 1 | 14 |
| lens_add | 5 [0-15] | 0 | 5 | final, 32, 0.8 | 56 |
| lens_swap | 2 [0-9] | 0 | 18 | question, joint, 4 | 48 |
| lens_transpl | 2 [0-8] | 5 | 2 | question, 32, 1 | 22 |
| dom_add | 24 [13-33] | 0 | 24 | question, joint, 0.05 | 46 |
| dom_natural | 9 [0-18] | 0 | 6 | question, 34, 2 | 26 |
| early_lens_add | 8 [0-16] | 0 | 22 | question, 16, 0.2 | 3 |
| early_embed_add | 2 [0-9] | 2 | 2 | question, 20, 0.4 | 5 |

## PPM (n=29, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 31 [19-42] | - | 10 | question, 40, 1 | 14 |
| lens_add | 14 [4-29] | 3 | 62 | question, joint, 0.1 | 44 |
| lens_swap | 7 [0-22] | 0 | 7 | question, joint, 1 | 46 |
| lens_transpl | 7 [0-23] | 3 | 7 | question, 38, 2 | 21 |
| dom_add | 7 [0-20] | 4 | 22 | question, 38, 0.4 | 48 |
| dom_natural | 7 [0-20] | 0 | 7 | final, 34, 1 | 26 |
| early_lens_add | 7 [0-21] | 3 | 17 | question, 16, 0.2 | 2 |
| early_embed_add | 3 [0-15] | 3 | 3 | question, 16, 0.2 | 4 |

## PMP (n=40, 13 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 25 [10-40] | - | 2 | question, 40, 1 | 14 |
| lens_add | 10 [0-25] | 5 | 2 | final, 38, 0.8 | 73 |
| lens_swap | 10 [2-22] | 0 | 10 | final, joint, 4 | 48 |
| lens_transpl | 18 [5-35] | 0 | 5 | question, joint, 1 | 30 |
| dom_add | 21 [10-35] | 3 | 3 | final, 36, 0.8 | 75 |
| dom_natural | 18 [7-35] | 0 | 39 | question, joint, 1 | 30 |
| early_lens_add | 25 [14-40] | 0 | 52 | question, 16, 0.4 | 7 |
| early_embed_add | 2 [0-8] | 0 | 5 | question, 20, 0.8 | 7 |

## MPP (n=40, 22 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 48 [31-66] | - | 2 | question, 40, 1 | 14 |
| lens_add | 25 [12-39] | 5 | 8 | question, joint, 0.1 | 59 |
| lens_swap | 18 [8-29] | 2 | 0 | question, joint, 2 | 47 |
| lens_transpl | 10 [2-21] | 2 | 2 | final, joint, 1 | 29 |
| dom_add | 26 [14-38] | 4 | 4 | final, joint, 0.1 | 59 |
| dom_natural | 19 [7-33] | 4 | 11 | final, joint, 1 | 29 |
| early_lens_add | 15 [5-26] | 2 | 0 | question, 24, 0.4 | 7 |
| early_embed_add | 2 [0-9] | 2 | 0 | question, 24, 0.2 | 6 |

## MMP (n=40, 17 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 38 [20-58] | - | 5 | question, 36, 1 | 14 |
| lens_add | 55 [35-68] | 0 | 8 | question, 32, 0.8 | 72 |
| lens_swap | 45 [28-59] | 0 | 2 | question, joint, 1 | 47 |
| lens_transpl | 28 [11-48] | 0 | 5 | final, joint, 1 | 27 |
| dom_add | 21 [9-39] | 0 | 0 | final, 36, 0.4 | 63 |
| dom_natural | 24 [12-45] | 3 | 3 | final, 36, 2 | 30 |
| early_lens_add | 32 [10-51] | 0 | 10 | question, 24, 0.8 | 7 |
| early_embed_add | 5 [0-13] | 2 | 2 | question, 16, 0.4 | 6 |

## MPM (n=24, 16 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 50 [30-68] | - | 4 | final, 36, 1 | 14 |
| lens_add | 17 [0-32] | 4 | 21 | question, joint, 0.1 | 59 |
| lens_swap | 42 [25-59] | 0 | 4 | question, joint, 4 | 48 |
| lens_transpl | 29 [12-52] | 0 | 8 | final, 40, 2 | 26 |
| dom_add | 6 [0-19] | 0 | 6 | question, 34, 0.4 | 37 |
| dom_natural | 6 [0-19] | 0 | 33 | question, joint, 1 | 20 |
| early_lens_add | 8 [0-21] | 4 | 4 | question, 20, 0.4 | 4 |
| early_embed_add | 4 [0-14] | 0 | 0 | question, 24, 0.2 | 2 |

