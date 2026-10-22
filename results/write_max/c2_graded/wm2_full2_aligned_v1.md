# C2-graded / wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit 50be071)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 21 [12-31] (lens_add, final, 48, 0.8) | 21 [12-31] (lens_add, final, 48, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 21 [12-31] (lens_add, final, 48, 0.8) |
| CP | 0 [0-0] (lens_add, question, 48, 0.05) | 0 [0-0] (lens_add, final, 48, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 48, 0.05) |
| M->M | 19 [4-40] (lens_add, final, joint, 0.1) | 19 [4-40] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 19 [4-40] (lens_add, final, joint, 0.1) |
| M->P | 0 [0-0] (lens_add, question, 48, 0.05) | 0 [0-0] (lens_add, final, 48, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 48, 0.05) |
| P->M | 14 [6-22] (lens_add, final, 48, 0.8) | 14 [6-22] (lens_add, final, 48, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 14 [6-22] (lens_add, final, 48, 0.8) |
| P->P | 0 [0-0] (lens_add, question, 48, 0.05) | 0 [0-0] (lens_add, final, 48, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 48, 0.05) |

Rule: M->M best 19% vs M->P best 0%: >= 3x yes, >= +30 points no, intervals apart yes -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 95 | 18 | 19 | - | - |
| CP | 68 | 0 | 0 | - | - |
| M->M | 94 | 11 | 12 | - | - |
| M->P | 74 | 0 | 0 | - | - |
| P->M | 95 | 11 | 11 | - | - |
| P->P | 68 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 0.74, "MM": 0.94}, relative {"MP": 0.0, "MM": 0.12} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.19} -> FAILS
