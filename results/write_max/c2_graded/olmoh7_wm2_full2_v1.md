# C2-graded / olmoh7_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit cf1a709)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 24 [6-50] (lens_add, final, 20, 0.4) | 24 [6-50] (lens_add, final, 20, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 24 [6-50] (lens_add, final, 20, 0.4) |
| CP | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 14, 0.05) |
| M->M | 41 [12-71] (lens_add, final, 16, 0.8) | 41 [12-71] (lens_add, final, 16, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 41 [12-71] (lens_add, final, 16, 0.8) |
| M->P | 6 [0-20] (lens_add, question, 14, 0.8) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 6 [0-20] (lens_add, question, 14, 0.8) |
| P->M | 25 [6-45] (lens_swap, final, joint, 4) | 25 [6-45] (lens_swap, final, joint, 4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 25 [6-45] (lens_swap, final, joint, 4) |
| P->P | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 14, 0.05) |

Rule: M->M best 41% vs M->P best 6%: >= 3x yes, >= +30 points yes, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 71 | 14 | 20 | - | - |
| CP | 100 | 0 | 0 | - | - |
| M->M | 82 | 34 | 41 | - | - |
| M->P | 94 | 0 | 0 | - | - |
| P->M | 85 | 15 | 18 | - | - |
| P->P | 90 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 0.94, "MM": 0.82}, relative {"MP": 0.0, "MM": 0.41} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.41} -> FAILS
