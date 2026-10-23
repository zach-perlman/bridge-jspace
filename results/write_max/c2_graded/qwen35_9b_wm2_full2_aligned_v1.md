# C2-graded / qwen35_9b_wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit ad711b6)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 10 [3-19] (lens_add, final, joint, 0.1) | 10 [3-19] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 10 [3-19] (lens_add, final, joint, 0.1) |
| CP | 0 [0-0] (lens_add, question, 13, 0.05) | 0 [0-0] (lens_add, final, 13, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 13, 0.05) |
| M->M | 68 [47-85] (lens_add, final, 19, 0.8) | 68 [47-85] (lens_add, final, 19, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 68 [47-85] (lens_add, final, 19, 0.8) |
| M->P | 8 [0-29] (lens_add, final, joint, 0.2) | 8 [0-29] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 8 [0-29] (lens_add, final, joint, 0.2) |
| P->M | 21 [10-35] (lens_add, question, joint, 0.1) | 12 [4-23] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 21 [10-35] (lens_add, question, joint, 0.1) |
| P->P | 3 [0-9] (lens_add, question, 14, 0.4) | 2 [0-6] (lens_add, final, 13, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 3 [0-9] (lens_add, question, 14, 0.4) |

Rule: M->M best 68% vs M->P best 8%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 67 | 4 | 6 | - | - |
| CP | 71 | 0 | 0 | - | - |
| M->M | 68 | 61 | 90 | - | - |
| M->P | 84 | 0 | 0 | - | - |
| P->M | 57 | 17 | 30 | - | - |
| P->P | 60 | 2 | 3 | - | - |

C2-relative: ceilings {"MP": 0.84, "MM": 0.68}, relative {"MP": 0.0, "MM": 0.9} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.68} -> passes
