# C2-graded / muse30_wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit 32e2672)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 21 [11-34] (lens_add, final, joint, 0.1) | 21 [11-34] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 21 [11-34] (lens_add, final, joint, 0.1) |
| CP | 8 [2-16] (lens_add, question, joint, 0.2) | 0 [0-0] (lens_add, final, 22, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 8 [2-16] (lens_add, question, joint, 0.2) |
| M->M | 50 [24-70] (lens_add, final, joint, 0.1) | 50 [24-70] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 50 [24-70] (lens_add, final, joint, 0.1) |
| M->P | 10 [2-19] (lens_add, final, 30, 0.8) | 10 [2-19] (lens_add, final, 30, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 10 [2-19] (lens_add, final, 30, 0.8) |
| P->M | 12 [4-22] (lens_add, question, joint, 0.1) | 12 [3-24] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 12 [4-22] (lens_add, question, joint, 0.1) |
| P->P | 13 [5-23] (lens_add, question, joint, 0.2) | 2 [0-5] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 13 [5-23] (lens_add, question, joint, 0.2) |

Rule: M->M best 50% vs M->P best 10%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 81 | 17 | 21 | - | - |
| CP | 96 | 5 | 5 | - | - |
| M->M | 81 | 43 | 53 | - | - |
| M->P | 98 | 7 | 7 | - | - |
| P->M | 55 | 8 | 14 | - | - |
| P->P | 70 | 13 | 19 | - | - |

C2-relative: ceilings {"MP": 0.98, "MM": 0.81}, relative {"MP": 0.07, "MM": 0.53} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.5} -> passes
