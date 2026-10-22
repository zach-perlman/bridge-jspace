# C2-graded / qwen3_32b_wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit 50be071)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 29 [19-40] (lens_add, final, joint, 0.1) | 29 [19-40] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 29 [19-40] (lens_add, final, joint, 0.1) |
| CP | 2 [0-6] (lens_add, final, joint, 0.4) | 2 [0-6] (lens_add, final, joint, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 2 [0-6] (lens_add, final, joint, 0.4) |
| M->M | 75 [55-90] (lens_add, final, joint, 0.1) | 75 [55-90] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 75 [55-90] (lens_add, final, joint, 0.1) |
| M->P | 8 [0-14] (lens_add, question, joint, 0.2) | 5 [0-12] (lens_add, final, 48, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 8 [0-14] (lens_add, question, joint, 0.2) |
| P->M | 24 [14-34] (lens_add, final, joint, 0.1) | 24 [14-34] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 24 [14-34] (lens_add, final, joint, 0.1) |
| P->P | 2 [0-6] (lens_add, question, 40, 0.8) | 2 [0-5] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 2 [0-6] (lens_add, question, 40, 0.8) |

Rule: M->M best 75% vs M->P best 8%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 94 | 29 | 30 | - | - |
| CP | 98 | 0 | 0 | - | - |
| M->M | 100 | 75 | 75 | - | - |
| M->P | 100 | 2 | 2 | - | - |
| P->M | 89 | 23 | 26 | - | - |
| P->P | 85 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 1}, relative {"MP": 0.02, "MM": 0.75} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.75} -> passes
