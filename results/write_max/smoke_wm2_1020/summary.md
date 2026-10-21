# write_max v2 / smoke_wm2_1020: 12 cases (12 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## BL (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 34, 1 | 4 |
| lens_add | 0 [0-0] | 0 | 0 | question, 34, 0.05 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 34, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 34, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 20, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 20, 0.2 | 4 |

## BR (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 34, 1 | 4 |
| lens_add | 100 [100-100] | 0 | 0 | final, 34, 0.8 | 30 |
| lens_swap | 50 [0-100] | 0 | 0 | final, joint, 4 | 18 |
| lens_transpl | 50 [0-100] | 0 | 0 | final, joint, 2 | 12 |
| early_lens_add | 50 [0-100] | 0 | 50 | question, 20, 1.6 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 20, 0.2 | 4 |

## RL (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | question, 36, 1 | 4 |
| lens_add | 0 [0-0] | 0 | 0 | question, 34, 0.05 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 34, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 34, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 20, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 20, 0.2 | 4 |

## RR (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 34, 1 | 4 |
| lens_add | 100 [100-100] | 0 | 0 | final, 34, 0.8 | 30 |
| lens_swap | 100 [100-100] | 0 | 0 | final, joint, 2 | 18 |
| lens_transpl | 100 [100-100] | 0 | 0 | final, joint, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 20, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 20, 0.2 | 4 |

## R (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 50 [0-100] | - | 0 | question, 34, 1 | 4 |
| lens_add | 100 [100-100] | 0 | 0 | question, 34, 0.4 | 30 |
| lens_swap | 100 [100-100] | 0 | 0 | question, joint, 4 | 18 |
| lens_transpl | 100 [100-100] | 0 | 0 | question, joint, 2 | 12 |
| early_lens_add | 50 [0-100] | 0 | 0 | question, 20, 0.8 | 3 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 20, 0.2 | 3 |

## B (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 34, 1 | 4 |
| lens_add | 100 [100-100] | 0 | 0 | question, 34, 0.4 | 30 |
| lens_swap | 50 [0-100] | 0 | 0 | question, joint, 4 | 18 |
| lens_transpl | 50 [0-100] | 0 | 0 | question, joint, 2 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 20, 0.2 | 3 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 20, 0.2 | 3 |

Rules (RL vs RR): {"MP_lens_le_control_plus_5": true, "MM_lens_ge_4x_control_and_10pct": true, "C2_holds": true, "MP_early_lens_is_injection": true}
