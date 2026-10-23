# write_max v2 / qwen35_9b_smoke_wm2_full_1021: 12 cases (12 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 50 [0-100] | - | 0 | question, 16, 1 | 6 |
| lens_add | 50 [0-100] | 0 | 0 | question, joint, 0.8 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 16, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 3 |
| early_embed_add | 50 [0-100] | 0 | 0 | question, 12, 0.8 | 4 |

## PM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 16, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.05 | 28 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 16, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 1 | 12 |
| early_lens_add | 50 [0-100] | 0 | 0 | question, 12, 0.4 | 2 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 1 |

## MP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 100 [100-100] | - | 0 | question, joint, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.05 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 16, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 3 |

## MM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 50 [0-100] | - | 0 | question, joint, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.05 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 16, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 3 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 3 |

## CP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 50 [0-100] | - | 0 | final, 17, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.05 | 30 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 16, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 4 |

## CM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 16, 1 | 6 |
| lens_add | 0 [0-0] | 0 | 0 | question, 16, 0.05 | 28 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 16, 1 | 18 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 16, 1 | 12 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 3 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 12, 0.2 | 3 |

Rules (MP vs MM): {"MP_lens_le_control_plus_5": true, "MM_lens_ge_4x_control_and_10pct": false, "C2_holds": false, "MP_early_lens_is_injection": true}
