# write_max v2 / qwen35_122b_smoke_wm2_1023: 12 cases (12 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 24, 1 | 6 |
| lens_add | 50 [0-100] | 0 | 0 | question, joint, 0.8 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 24, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 24, 1 | 12 |
| early_lens_add | 100 [100-100] | 0 | 0 | question, 15, 1.6 | 4 |
| early_embed_add | 50 [0-100] | 0 | 0 | question, 15, 1.6 | 4 |

## PM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 24, 1 | 6 |
| lens_add | 100 [100-100] | 0 | 0 | question, 24, 0.8 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 24, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 24, 1 | 12 |
| early_lens_add | 50 [0-100] | 0 | 50 | question, 15, 0.8 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 15, 0.2 | 3 |

## MP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 24, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 0 | question, 24, 0.05 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 24, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 24, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 15, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 15, 0.2 | 4 |

## MM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 24, 1 | 6 |
| lens_add | 50 [0-100] | 0 | 0 | question, joint, 0.8 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 24, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 24, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 15, 0.2 | 4 |
| early_embed_add | 50 [0-100] | 0 | 50 | question, 15, 1.6 | 4 |

## CP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 24, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 0 | question, 24, 0.05 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 24, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 24, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 15, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 15, 0.2 | 4 |

## CM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 24, 1 | 6 |
| lens_add | 50 [0-100] | 0 | 0 | question, 24, 0.8 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 24, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 24, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 15, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 15, 0.2 | 3 |

Rules (MP vs MM): {"MP_lens_le_control_plus_5": true, "MM_lens_ge_4x_control_and_10pct": true, "C2_holds": true, "MP_early_lens_is_injection": true}
