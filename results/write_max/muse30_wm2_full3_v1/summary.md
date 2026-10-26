# write_max v2 / muse30_wm2_full3_v1: 194 cases (41 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PPP (n=40, 19 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 85 [71-97] | - | 8 | final, 33, 1 | 14 |
| lens_add | 12 [5-22] | 2 | 8 | question, 23, 0.4 | 48 |
| lens_swap | 5 [0-15] | 0 | 0 | final, joint, 4 | 42 |
| lens_transpl | 5 [0-14] | 2 | 0 | question, 23, 1 | 21 |
| dom_add | 20 [9-40] | 3 | 30 | question, joint, 0.1 | 46 |
| dom_natural | 13 [0-36] | 0 | 17 | final, 27, 2 | 22 |
| early_lens_add | 18 [7-29] | 0 | 22 | question, 13, 0.8 | 6 |
| early_embed_add | 5 [0-14] | 5 | 2 | question, 16, 0.4 | 5 |

## PMP (n=40, 15 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 92 [83-100] | - | 2 | final, 33, 1 | 14 |
| lens_add | 8 [0-15] | 0 | 18 | question, joint, 0.2 | 58 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 23, 1 | 42 |
| lens_transpl | 32 [22-45] | 2 | 15 | question, joint, 2 | 27 |
| dom_add | 38 [22-48] | 0 | 35 | final, joint, 0.1 | 56 |
| dom_natural | 26 [11-38] | 0 | 15 | final, 33, 2 | 24 |
| early_lens_add | 8 [0-15] | 2 | 15 | question, 13, 0.8 | 6 |
| early_embed_add | 8 [0-17] | 0 | 12 | question, 16, 0.8 | 7 |

## PPM (n=21, 8 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 95 [90-100] | - | 5 | final, 33, 1 | 14 |
| lens_add | 10 [0-20] | 0 | 10 | question, joint, 0.05 | 34 |
| lens_swap | 10 [0-21] | 0 | 10 | final, joint, 2 | 37 |
| lens_transpl | 5 [0-10] | 0 | 5 | question, 25, 1 | 12 |
| dom_add | 11 [0-27] | 0 | 5 | final, 31, 0.2 | 15 |
| dom_natural | 11 [0-20] | 0 | 0 | question, 23, 1 | 10 |
| early_lens_add | - (no cell passes the gate) | | | | 0 |
| early_embed_add | 5 [0-10] | 5 | 0 | question, 13, 0.2 | 1 |

## MPM (n=17, 11 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 33, 1 | 14 |
| lens_add | 12 [0-27] | 0 | 0 | final, 33, 0.4 | 18 |
| lens_swap | 12 [0-27] | 0 | 0 | final, 33, 4 | 22 |
| lens_transpl | 12 [0-27] | 0 | 0 | final, 33, 1 | 4 |
| dom_add | 9 [0-23] | 0 | 0 | question, 23, 0.05 | 11 |
| dom_natural | 18 [0-44] | 0 | 0 | final, 29, 1 | 6 |
| early_lens_add | - (no cell passes the gate) | | | | 0 |
| early_embed_add | - (no cell passes the gate) | | | | 0 |

## MMP (n=36, 12 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 94 [86-100] | - | 3 | final, 33, 1 | 14 |
| lens_add | 6 [0-16] | 0 | 0 | question, joint, 0.1 | 52 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 23, 1 | 41 |
| lens_transpl | 6 [0-14] | 0 | 0 | final, joint, 1 | 23 |
| dom_add | 33 [11-56] | 0 | 33 | final, 29, 0.4 | 52 |
| dom_natural | 37 [8-63] | 0 | 33 | final, 33, 2 | 23 |
| early_lens_add | 6 [0-16] | 0 | 0 | question, 20, 0.4 | 7 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 13, 0.2 | 6 |

## MPP (n=40, 20 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 33, 1 | 14 |
| lens_add | 15 [4-26] | 2 | 2 | question, joint, 0.1 | 54 |
| lens_swap | 8 [0-20] | 0 | 2 | question, joint, 4 | 42 |
| lens_transpl | 15 [5-25] | 0 | 0 | question, joint, 1 | 25 |
| dom_add | 38 [15-61] | 0 | 10 | final, joint, 0.1 | 47 |
| dom_natural | 21 [3-45] | 0 | 7 | final, 25, 2 | 23 |
| early_lens_add | 5 [0-12] | 2 | 0 | question, 13, 0.8 | 8 |
| early_embed_add | 0 [0-0] | 2 | 0 | question, 13, 0.2 | 8 |

