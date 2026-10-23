# write_max v2 / olmoh7_smoke_wm2_full_1022: 12 cases (12 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 50 | question, 16, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 50 | question, 16, 0.05 | 10 |
| lens_swap | 0 [0-0] | 0 | 50 | question, 16, 4 | 4 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 2 | 8 |
| early_lens_add | - (no cell passes the gate) | | | | 0 |
| early_embed_add | - (no cell passes the gate) | | | | 0 |

## PM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 16, 1 | 6 |
| lens_add | 100 [100-100] | 0 | 0 | final, joint, 0.8 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 16, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 3 |
| early_embed_add | 50 [0-100] | 0 | 50 | question, 12, 1.6 | 4 |

## MP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 17, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.05 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 16, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 1 | 12 |
| early_lens_add | 50 [0-100] | 0 | 0 | question, 12, 1.6 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 4 |

## MM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 16, 1 | 6 |
| lens_add | 50 [0-100] | 0 | 0 | final, joint, 0.8 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 16, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 4 |

## CP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | final, 17, 1 | 6 |
| lens_add | 50 [0-100] | 0 | 0 | final, joint, 0.8 | 29 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 16, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 1 | 12 |
| early_lens_add | 50 [0-100] | 0 | 0 | question, 12, 0.8 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 3 |

## CM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 50 [0-100] | - | 0 | question, 16, 1 | 6 |
| lens_add | 50 [0-100] | 0 | 0 | question, 16, 0.2 | 24 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 16, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 1 | 12 |
| early_lens_add | 100 [100-100] | 0 | 0 | question, 12, 0.8 | 3 |
| early_embed_add | 100 [100-100] | 0 | 0 | question, 12, 0.8 | 3 |

Rules (MP vs MM): {"MP_lens_le_control_plus_5": true, "MM_lens_ge_4x_control_and_10pct": true, "C2_holds": true, "MP_early_lens_is_injection": false}
