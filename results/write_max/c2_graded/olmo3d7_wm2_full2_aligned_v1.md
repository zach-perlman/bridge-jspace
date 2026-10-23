# C2-graded / olmo3d7_wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit 2d65551)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 7 [0-23] (lens_add, final, 13, 0.8) | 7 [0-23] (lens_add, final, 13, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 7 [0-23] (lens_add, final, 13, 0.8) |
| CP | 7 [0-23] (lens_add, question, joint, 0.8) | 0 [0-0] (lens_add, final, 12, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 7 [0-23] (lens_add, question, joint, 0.8) |
| M->M | 9 [0-25] (lens_add, final, 18, 0.8) | 9 [0-25] (lens_add, final, 18, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 9 [0-25] (lens_add, final, 18, 0.8) |
| M->P | 0 [0-0] (lens_add, question, 12, 0.05) | 0 [0-0] (lens_add, final, 12, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 12, 0.05) |
| P->M | 11 [0-28] (lens_add, final, 18, 0.8) | 11 [0-28] (lens_add, final, 18, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 11 [0-28] (lens_add, final, 18, 0.8) |
| P->P | 0 [0-0] (lens_add, question, 12, 0.05) | 0 [0-0] (lens_add, final, 12, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 12, 0.05) |

Rule: M->M best 9% vs M->P best 0%: >= 3x yes, >= +30 points no, intervals apart yes -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 93 | 0 | 0 | - | - |
| CP | 100 | 0 | 0 | - | - |
| M->M | 91 | 0 | 0 | - | - |
| M->P | 100 | 0 | 0 | - | - |
| P->M | 63 | 2 | 3 | - | - |
| P->P | 63 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 0.91}, relative {"MP": 0.0, "MM": 0.0} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.09} -> FAILS
