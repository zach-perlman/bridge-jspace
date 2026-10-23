# C2-graded / olmo3d7_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 2d65551)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 7 [0-23] (lens_add, final, 18, 0.4) | 7 [0-23] (lens_add, final, 18, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 7 [0-23] (lens_add, final, 18, 0.4) |
| CP | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 14, 0.05) |
| M->M | 36 [11-55] (lens_add, final, joint, 0.2) | 36 [11-55] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 36 [11-55] (lens_add, final, joint, 0.2) |
| M->P | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 14, 0.05) |
| P->M | 11 [0-26] (lens_add, question, joint, 0.4) | 11 [0-29] (lens_swap, final, joint, 2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 11 [0-26] (lens_add, question, joint, 0.4) |
| P->P | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 14, 0.05) |

Rule: M->M best 36% vs M->P best 0%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 93 | 0 | 0 | - | - |
| CP | 100 | 0 | 0 | - | - |
| M->M | 91 | 25 | 28 | - | - |
| M->P | 100 | 0 | 0 | - | - |
| P->M | 100 | 2 | 2 | - | - |
| P->P | 84 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 0.91}, relative {"MP": 0.0, "MM": 0.28} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.36} -> FAILS
