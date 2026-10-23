# write_max v2 / qwen35_9b_wm2_full3_v1: 92 cases (41 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PPP (n=28, 15 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 64 [43-76] | - | 7 | question, 15, 1 | 16 |
| lens_add | 18 [0-33] | 0 | 4 | final, joint, 0.2 | 36 |
| lens_swap | 11 [0-18] | 0 | 0 | final, joint, 4 | 44 |
| lens_transpl | 7 [0-17] | 4 | 0 | question, 17, 1 | 8 |
| early_lens_add | - (no cell passes the gate) | | | | 0 |
| early_embed_add | - (no cell passes the gate) | | | | 0 |
| dom_add | 28 [11-45] | 0 | 33 | question, joint, 0.1 | 33 |
| dom_natural | 22 [0-43] | 0 | 11 | final, 18, 1 | 12 |

## PPM (n=19, 13 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 68 [50-86] | - | 5 | final, 20, 1 | 16 |
| lens_add | 11 [0-29] | 0 | 5 | question, joint, 0.05 | 28 |
| lens_swap | 11 [0-29] | 0 | 5 | final, 19, 4 | 41 |
| lens_transpl | 11 [0-25] | 0 | 0 | question, 14, 1 | 4 |
| early_lens_add | - (no cell passes the gate) | | | | 0 |
| early_embed_add | 5 [0-18] | 0 | 0 | question, 12, 0.2 | 1 |
| dom_add | 18 [0-60] | 0 | 18 | question, joint, 0.1 | 40 |
| dom_natural | 18 [0-60] | 0 | 9 | question, joint, 1 | 17 |

## PMP (n=16, 9 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 75 [56-100] | - | 6 | question, joint, 1 | 16 |
| lens_add | 6 [0-21] | 0 | 0 | question, 14, 0.4 | 65 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 14, 1 | 48 |
| lens_transpl | 6 [0-21] | 0 | 0 | question, 14, 1 | 27 |
| dom_add | 9 [0-23] | 0 | 9 | final, 20, 0.8 | 74 |
| dom_natural | 9 [0-23] | 0 | 9 | final, 20, 2 | 32 |
| early_lens_add | 12 [0-31] | 0 | 0 | question, 12, 0.4 | 5 |
| early_embed_add | 6 [0-21] | 0 | 0 | question, 10, 0.4 | 5 |

## MPP (n=9, 6 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 89 [70-100] | - | 0 | final, 20, 1 | 16 |
| lens_add | 11 [0-38] | 0 | 0 | question, 16, 0.8 | 28 |
| lens_swap | 11 [0-30] | 0 | 0 | question, 15, 4 | 31 |
| lens_transpl | 11 [0-30] | 0 | 11 | question, 14, 2 | 9 |
| dom_add | 50 [0-100] | 0 | 25 | question, 14, 0.4 | 39 |
| dom_natural | 50 [0-75] | 0 | 0 | final, 20, 2 | 13 |
| early_lens_add | 33 [10-57] | 0 | 0 | question, 8, 0.4 | 5 |
| early_embed_add | 22 [0-50] | 0 | 0 | question, 8, 0.4 | 3 |

## MMP (n=16, 11 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 69 [44-93] | - | 6 | question, joint, 1 | 16 |
| lens_add | 6 [0-19] | 0 | 12 | question, 17, 0.2 | 45 |
| lens_swap | 0 [0-0] | 0 | 6 | question, 14, 4 | 32 |
| lens_transpl | 6 [0-21] | 0 | 12 | question, 14, 2 | 11 |
| early_lens_add | 0 [0-0] | 0 | 12 | question, 12, 0.2 | 1 |
| early_embed_add | 0 [0-0] | 0 | 6 | question, 8, 0.2 | 3 |
| dom_add | 17 [0-40] | 0 | 33 | question, 17, 0.4 | 51 |
| dom_natural | 17 [0-40] | 0 | 33 | final, 18, 2 | 19 |

## MPM (n=4, 4 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 50 [0-100] | - | 0 | final, 16, 1 | 16 |
| lens_add | 25 [0-75] | 0 | 25 | final, 14, 0.4 | 65 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 14, 1 | 48 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 14, 1 | 27 |
| early_lens_add | 50 [0-100] | 0 | 25 | question, 8, 0.4 | 4 |
| early_embed_add | 0 [0-0] | 0 | 25 | question, 8, 0.2 | 4 |
| dom_add | 0 [0-0] | 0 | 0 | question, 14, 0.05 | 66 |
| dom_natural | 100 [100-100] | 0 | 0 | final, 15, 2 | 28 |

