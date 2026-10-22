# C2-graded / muse30_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 6c0760e)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 21 [9-35] (lens_add, final, joint, 0.1) | 21 [9-35] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 21 [9-35] (lens_add, final, joint, 0.1) |
| CP | 6 [0-15] (lens_add, question, joint, 0.2) | 0 [0-0] (lens_add, final, 23, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 6 [0-15] (lens_add, question, joint, 0.2) |
| M->M | 56 [33-74] (lens_add, final, joint, 0.1) | 56 [33-74] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 56 [33-74] (lens_add, final, joint, 0.1) |
| M->P | 6 [0-13] (lens_add, final, 29, 0.8) | 6 [0-13] (lens_add, final, 29, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 6 [0-13] (lens_add, final, 29, 0.8) |
| P->M | 18 [9-30] (lens_add, final, joint, 0.1) | 18 [9-30] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 18 [9-30] (lens_add, final, joint, 0.1) |
| P->P | 12 [4-22] (lens_add, question, joint, 0.2) | 2 [0-6] (lens_add, final, 29, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 12 [4-22] (lens_add, question, joint, 0.2) |

Rule: M->M best 56% vs M->P best 6%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 88 | 17 | 20 | - | - |
| CP | 98 | 3 | 3 | - | - |
| M->M | 85 | 50 | 58 | - | - |
| M->P | 100 | 2 | 2 | - | - |
| P->M | 68 | 14 | 20 | - | - |
| P->P | 75 | 11 | 15 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 0.85}, relative {"MP": 0.02, "MM": 0.58} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.56} -> passes
