# C2-graded WITHOUT guessable cases (11 dropped; robustness split) / olmo3d7_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 2d65551)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 23 [0-50] (lens_add, final, joint, 0.2) | 23 [0-50] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 23 [0-50] (lens_add, final, joint, 0.2) |
| CP | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 14, 0.05) |
| M->M | 57 [25-86] (lens_add, final, joint, 0.2) | 57 [25-86] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 57 [25-86] (lens_add, final, joint, 0.2) |
| M->P | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 14, 0.05) |
| P->M | 11 [0-29] (lens_add, question, joint, 0.4) | 11 [0-29] (lens_swap, final, joint, 2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 11 [0-29] (lens_add, question, joint, 0.4) |
| P->P | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 14, 0.05) |

Rule: M->M best 57% vs M->P best 0%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 92 | 13 | 14 | - | - |
| CP | 100 | 0 | 0 | - | - |
| M->M | 86 | 52 | 60 | - | - |
| M->P | 100 | 0 | 0 | - | - |
| P->M | 100 | 2 | 2 | - | - |
| P->P | 80 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 0.86}, relative {"MP": 0.0, "MM": 0.6} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.57} -> passes
