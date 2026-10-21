# write_max report / smoke_wm2_1020

Cells: flips to C's answer % (its random control keeps the clean answer %; median frac). `*` = fails the breakage gate (control keeps < 95%). Layer "joint" = every band layer at once.

## Best gated cell per write group (from summary.json) [95% CI over bridge entities]

| family | n | lens (best of add/swap/transplant) | its control flips | dom (best of add/natural) | copy | early lens_add | early embed_add |
|---|---|---|---|---|---|---|---|
| P->P | 2 | 0 [0-0] (lens_add, question, 34, 0.05) | 0 | - | 0 [0-0] (copy, question, 34, 1) | 0 [0-0] (early_lens_add, question, 20, 0.2) | 0 [0-0] (early_embed_add, question, 20, 0.2) |
| P->M | 2 | 100 [100-100] (lens_add, final, 34, 0.8) | 0 | - | 0 [0-0] (copy, question, 34, 1) | 50 [0-100] (early_lens_add, question, 20, 1.6) | 0 [0-0] (early_embed_add, question, 20, 0.2) |
| M->P | 2 | 0 [0-0] (lens_add, question, 34, 0.05) | 0 | - | 100 [100-100] (copy, question, 36, 1) | 0 [0-0] (early_lens_add, question, 20, 0.2) | 0 [0-0] (early_embed_add, question, 20, 0.2) |
| M->M | 2 | 100 [100-100] (lens_add, final, 34, 0.8) | 0 | - | 100 [100-100] (copy, final, 34, 1) | 0 [0-0] (early_lens_add, question, 20, 0.2) | 0 [0-0] (early_embed_add, question, 20, 0.2) |
| countries, recalled | 2 | 100 [100-100] (lens_add, question, 34, 0.4) | 0 | - | 50 [0-100] (copy, question, 34, 1) | 50 [0-100] (early_lens_add, question, 20, 0.8) | 0 [0-0] (early_embed_add, question, 20, 0.2) |
| countries, given | 2 | 100 [100-100] (lens_add, question, 34, 0.4) | 0 | - | 0 [0-0] (copy, question, 34, 1) | 0 [0-0] (early_lens_add, question, 20, 0.2) | 0 [0-0] (early_embed_add, question, 20, 0.2) |

Rules: `{"MP_lens_le_control_plus_5": true, "MM_lens_ge_4x_control_and_10pct": true, "C2_holds": true, "MP_early_lens_is_injection": true}`

## lens_add, question positions, joint

| family | 0.05 | 0.1 | 0.2 | 0.4 | 0.8 |
|---|---|---|---|---|---|
| P->P | 0 (100; -0.01) | 0 (100; 0.02) | 0 (100; 0.10) | 0 (100; 0.31) | 0 (100; 0.39) |
| P->M | 0 (100; 0.04) | 0 (100; 0.14) | 0 (100; 0.35) | 50 (100; 0.45) | 0 (100; 0.24) |
| M->P | 0 (100; -0.01) | 0 (100; -0.00) | 0 (100; 0.17) | 0 (100; 0.28) | 0 (100; 0.24) |
| M->M | 0 (100; 0.05) | 0 (100; 0.14) | 0 (100; 0.31) | 50 (100; 0.36) | 0 (100; 0.14) |
| countries, recalled | 0 (100; 0.30) | 100 (100; 0.71) | 100 (100; 1.00) | 50 (100; 1.05) | 0 (100; 1.00) |
| countries, given | 0 (100; 0.24) | 50 (100; 0.58) | 100 (100; 1.01) | 0 (100; 1.22) | 0 (100; 1.12) |

## lens_add, final positions, joint

| family | 0.05 | 0.1 | 0.2 | 0.4 | 0.8 |
|---|---|---|---|---|---|
| P->P | 0 (100; 0.01) | 0 (100; 0.01) | 0 (100; 0.01) | 0 (100; 0.04) | 0 (100; 0.18) |
| P->M | 0 (100; 0.03) | 0 (100; 0.08) | 100 (100; 0.42) | 100 (100; 0.48) | 50 (100; 0.42) |
| M->P | 0 (100; -0.00) | 0 (100; -0.00) | 0 (100; -0.00) | 0 (100; 0.05) | 0 (100; 0.16) |
| M->M | 0 (100; 0.03) | 0 (100; 0.11) | 100 (100; 0.53) | 100 (100; 0.54) | 50 (100; 0.43) |
| countries, recalled | 0 (100; 0.04) | 0 (100; 0.09) | 0 (100; 0.12) | 0 (100; 0.20) | 0 (100; 0.37) |
| countries, given | 0 (100; 0.04) | 0 (100; 0.09) | 0 (100; 0.17) | 0 (100; 0.34) | 0 (100; 0.46) |

## lens_swap, question positions, joint

| family | 1 | 2 | 4 |
|---|---|---|---|
| P->P | 0 (100; 0.00) | 0 (100; 0.00) | 0 (100; 0.02) |
| P->M | 0 (100; 0.02) | 0 (100; 0.06) | 0 (100; 0.15) |
| M->P | 0 (100; 0.02) | 0 (100; 0.21) | 0 (100; 0.07) |
| M->M | 0 (100; 0.07) | 0 (100; 0.09) | 0 (100; 0.22) |
| countries, recalled | 0 (100; 0.26) | 50 (100; 0.57) | 100 (100; 0.91) |
| countries, given | 0 (100; 0.06) | 0 (100; 0.30) | 50 (100; 0.61) |

## lens_swap, final positions, joint

| family | 1 | 2 | 4 |
|---|---|---|---|
| P->P | 0 (100; 0.01) | 0 (100; 0.01) | 0 (100; 0.01) |
| P->M | 0 (100; 0.01) | 0 (100; 0.06) | 50 (100; 0.27) |
| M->P | 0 (100; -0.01) | 0 (100; -0.01) | 0 (100; -0.01) |
| M->M | 0 (100; 0.12) | 100 (100; 0.54) | 100 (100; 0.53) |
| countries, recalled | 0 (100; -0.00) | 0 (100; -0.00) | 0 (100; -0.00) |
| countries, given | 0 (100; 0.00) | 0 (100; -0.00) | 0 (100; -0.00) |

## lens_transpl, question positions, joint

| family | 1 | 2 |
|---|---|---|
| P->P | 0 (100; 0.02) | 0 (100; 0.12) |
| P->M | 0 (100; 0.08) | 0 (100; 0.18) |
| M->P | 0 (100; 0.06) | 0 (100; 0.21) |
| M->M | 0 (100; 0.12) | 0 (100; 0.24) |
| countries, recalled | 0 (100; 0.39) | 100 (100; 0.66) |
| countries, given | 0 (100; 0.21) | 50 (100; 0.46) |

## lens_transpl, final positions, joint

| family | 1 | 2 |
|---|---|---|
| P->P | 0 (100; 0.01) | 0 (100; 0.02) |
| P->M | 0 (100; 0.09) | 50 (100; 0.40) |
| M->P | 0 (100; 0.01) | 0 (100; 0.02) |
| M->M | 100 (100; 0.53) | 100 (100; 0.46) |
| countries, recalled | 0 (100; 0.00) | 0 (100; 0.01) |
| countries, given | 0 (100; 0.01) | 0 (100; 0.02) |

## lens_add, question positions, single layers: best gated flips % over strength

| family | L34 | L36 |
|---|---|---|
| P->P | 0 | 0 |
| P->M | 50 | 50 |
| M->P | 0 | 0 |
| M->M | 50 | 50 |
| countries, recalled | 100 | 100 |
| countries, given | 100 | 100 |

## lens_add, final positions, single layers: best gated flips % over strength

| family | L34 | L36 |
|---|---|---|
| P->P | 0 | 0 |
| P->M | 100 | 100 |
| M->P | 0 | 0 |
| M->M | 100 | 100 |
| countries, recalled | 0 | 0 |
| countries, given | 0 | 0 |

## dom_add, question positions, single layers: best gated flips % over strength

| family | L34 | L36 |
|---|---|---|
| P->P | - | - |
| P->M | - | - |
| M->P | - | - |
| M->M | - | - |
| countries, recalled | - | - |
| countries, given | - | - |

## dom_add, final positions, single layers: best gated flips % over strength

| family | L34 | L36 |
|---|---|---|
| P->P | - | - |
| P->M | - | - |
| M->P | - | - |
| M->M | - | - |
| countries, recalled | - | - |
| countries, given | - | - |

## copy, question positions, single layers: best gated flips % over strength

| family | L34 | L36 |
|---|---|---|
| P->P | 0 | 0 |
| P->M | 0 | 0 |
| M->P | 50 | 100 |
| M->M | 0 | 0 |
| countries, recalled | 50 | 50 |
| countries, given | 0 | 0 |

## copy, final positions, single layers: best gated flips % over strength

| family | L34 | L36 |
|---|---|---|
| P->P | 0 | 0 |
| P->M | 0 | 0 |
| M->P | 0 | 0 |
| M->M | 100 | 100 |
| countries, recalled | 0 | 0 |
| countries, given | 0 | 0 |

## Injection control (question positions): early lens_add vs embed_add, flips % (control keeps %)

| family | layer | lens 0.2 / embed 0.2 | lens 0.4 / embed 0.4 | lens 0.8 / embed 0.8 | lens 1.6 / embed 1.6 |
|---|---|---|---|---|---|
| P->P | L20 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| P->M | L20 | 0 / 0 | 0 / 0 | 0 / 0 | 50 / 0 |
| M->P | L20 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| M->M | L20 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| countries, recalled | L20 | 0 / 0 | 0 / 0 | 50 / 0 | 0* / 0* |
| countries, given | L20 | 0 / 0 | 0 / 0 | 0 / 0 | 0* / 0* |

