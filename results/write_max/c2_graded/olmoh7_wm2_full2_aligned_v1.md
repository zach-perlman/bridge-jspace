# C2-graded / olmoh7_wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit cf1a709)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 41 [16-75] (lens_add, final, joint, 0.2) | 41 [16-75] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 41 [16-75] (lens_add, final, joint, 0.2) |
| CP | 0 [0-0] (lens_add, question, 13, 0.05) | 0 [0-0] (lens_add, final, 13, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 13, 0.05) |
| M->M | 59 [29-81] (lens_add, final, 19, 0.8) | 59 [29-81] (lens_add, final, 19, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 59 [29-81] (lens_add, final, 19, 0.8) |
| M->P | 6 [0-20] (lens_add, question, 13, 0.8) | 0 [0-0] (lens_add, final, 13, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 6 [0-20] (lens_add, question, 13, 0.8) |
| P->M | 10 [0-24] (lens_swap, final, 19, 4) | 10 [0-24] (lens_swap, final, 19, 4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 10 [0-24] (lens_swap, final, 19, 4) |
| P->P | 0 [0-0] (lens_add, question, 13, 0.05) | 0 [0-0] (lens_add, final, 13, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 13, 0.05) |

Rule: M->M best 59% vs M->P best 6%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 53 | 39 | 73 | - | - |
| CP | 100 | 0 | 0 | - | - |
| M->M | 59 | 51 | 87 | - | - |
| M->P | 94 | 0 | 0 | - | - |
| P->M | 70 | 1 | 1 | - | - |
| P->P | 85 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 0.94, "MM": 0.59}, relative {"MP": 0.0, "MM": 0.87} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.59} -> passes
