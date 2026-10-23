# C2-graded / muse30_wm2_fresh2_v1 (rule fixed in scripts/c2_graded.py; this output from commit da2afb2)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 19 [10-29] (lens_add, final, joint, 0.1) | 19 [10-29] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 19 [10-29] (lens_add, final, joint, 0.1) |
| CP | 4 [0-8] (lens_add, final, 27, 0.8) | 4 [0-8] (lens_add, final, 27, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 4 [0-8] (lens_add, final, 27, 0.8) |
| M->M | 42 [18-65] (lens_add, final, joint, 0.1) | 42 [18-65] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 42 [18-65] (lens_add, final, joint, 0.1) |
| M->P | 9 [0-19] (lens_add, final, 27, 0.8) | 9 [0-19] (lens_add, final, 27, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 9 [0-19] (lens_add, final, 27, 0.8) |
| P->M | 19 [9-33] (lens_add, final, joint, 0.1) | 19 [9-33] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 19 [9-33] (lens_add, final, joint, 0.1) |
| P->P | 2 [0-7] (lens_add, final, 29, 0.8) | 2 [0-7] (lens_add, final, 29, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 2 [0-7] (lens_add, final, 29, 0.8) |

Rule: M->M best 42% vs M->P best 9%: >= 3x yes, >= +30 points yes, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 98 | 17 | 17 | - | - |
| CP | 100 | 1 | 1 | - | - |
| M->M | 86 | 35 | 40 | - | - |
| M->P | 100 | 6 | 6 | - | - |
| P->M | 56 | 14 | 25 | - | - |
| P->P | 69 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 0.86}, relative {"MP": 0.06, "MM": 0.4} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.42} -> FAILS
