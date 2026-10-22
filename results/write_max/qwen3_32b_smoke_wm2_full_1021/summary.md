# write_max v2 / qwen3_32b_smoke_wm2_full_1021: 12 cases (12 without a dom direction)

Best flips to C's answer (%) per write, over sites x layers x strengths, among cells whose random control keeps the clean answer on >= 95% of cases. [95% CI over bridge entities]

## PP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 32, 1 | 8 |
| lens_add | 0 [0-0] | 0 | 0 | question, 32, 0.05 | 40 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 32, 1 | 24 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 32, 1 | 16 |
| early_lens_add | 100 [100-100] | 0 | 0 | question, 24, 1.6 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 24, 0.2 | 4 |

## PM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 32, 1 | 8 |
| lens_add | 50 [0-100] | 0 | 50 | question, 34, 0.8 | 40 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 32, 1 | 24 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 32, 1 | 15 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 24, 0.2 | 3 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 24, 0.2 | 3 |

## MP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 32, 1 | 8 |
| lens_add | 0 [0-0] | 0 | 0 | question, 32, 0.05 | 40 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 32, 1 | 24 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 32, 1 | 16 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 24, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 24, 0.2 | 4 |

## MM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 32, 1 | 8 |
| lens_add | 0 [0-0] | 0 | 0 | question, 32, 0.05 | 40 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 32, 1 | 24 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 32, 1 | 16 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 24, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 24, 0.2 | 4 |

## CP (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 32, 1 | 8 |
| lens_add | 0 [0-0] | 0 | 0 | question, 32, 0.05 | 40 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 32, 1 | 24 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 32, 1 | 16 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 24, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 24, 0.2 | 4 |

## CM (n=2, 2 bridges)

| write | best flips [CI] | its control | other | site (pos, layer, strength) | gated cells |
|---|---|---|---|---|---|
| copy | 0 [0-0] | - | 0 | question, 32, 1 | 8 |
| lens_add | 0 [0-0] | 0 | 0 | question, 32, 0.05 | 37 |
| lens_swap | 0 [0-0] | 0 | 0 | question, 32, 1 | 24 |
| lens_transpl | 0 [0-0] | 0 | 0 | question, 32, 1 | 16 |
| early_lens_add | 0 [0-0] | 0 | 0 | question, 24, 0.2 | 4 |
| early_embed_add | 0 [0-0] | 0 | 0 | question, 24, 0.2 | 4 |

Rules (MP vs MM): {"MP_lens_le_control_plus_5": true, "MM_lens_ge_4x_control_and_10pct": false, "C2_holds": false, "MP_early_lens_is_injection": true}
