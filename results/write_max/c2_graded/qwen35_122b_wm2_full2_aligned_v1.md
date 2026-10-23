# C2-graded / qwen35_122b_wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit da2afb2)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 51 [40-64] (lens_add, final, 41, 0.8) | 51 [40-64] (lens_add, final, 41, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 51 [40-64] (lens_add, final, 41, 0.8) |
| CP | 0 [0-0] (lens_add, question, 40, 0.05) | 0 [0-0] (lens_add, final, 40, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 40, 0.05) |
| M->M | 39 [21-55] (lens_add, final, joint, 0.2) | 39 [21-55] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 39 [21-55] (lens_add, final, joint, 0.2) |
| M->P | 0 [0-0] (lens_add, question, 40, 0.05) | 0 [0-0] (lens_add, final, 40, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 40, 0.05) |
| P->M | 32 [22-41] (lens_add, final, joint, 0.2) | 32 [22-41] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 32 [22-41] (lens_add, final, joint, 0.2) |
| P->P | 0 [0-0] (lens_add, question, 40, 0.05) | 0 [0-0] (lens_add, final, 40, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 40, 0.05) |

Rule: M->M best 39% vs M->P best 0%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 100 | 50 | 50 | - | - |
| CP | 100 | 0 | 0 | - | - |
| M->M | 100 | 33 | 33 | - | - |
| M->P | 97 | 0 | 0 | - | - |
| P->M | 97 | 29 | 30 | - | - |
| P->P | 100 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 0.97, "MM": 1}, relative {"MP": 0.0, "MM": 0.33} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.39} -> FAILS
