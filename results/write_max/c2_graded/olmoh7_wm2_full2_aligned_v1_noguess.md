# C2-graded WITHOUT guessable cases (13 dropped; robustness split) / olmoh7_wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit cf1a709)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 40 [12-71] (lens_add, final, joint, 0.2) | 40 [12-71] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 40 [12-71] (lens_add, final, joint, 0.2) |
| CP | 0 [0-0] (lens_add, question, 13, 0.05) | 0 [0-0] (lens_add, final, 13, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 13, 0.05) |
| M->M | 67 [33-91] (lens_add, final, 19, 0.8) | 67 [33-91] (lens_add, final, 19, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 67 [33-91] (lens_add, final, 19, 0.8) |
| M->P | 6 [0-23] (lens_add, question, 13, 0.8) | 0 [0-0] (lens_add, final, 13, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 6 [0-23] (lens_add, question, 13, 0.8) |
| P->M | 6 [0-16] (lens_add, question, 15, 0.2) | 6 [0-16] (lens_add, final, 19, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 6 [0-16] (lens_add, question, 15, 0.2) |
| P->P | 0 [0-0] (lens_add, question, 13, 0.05) | 0 [0-0] (lens_add, final, 13, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 13, 0.05) |

Rule: M->M best 67% vs M->P best 6%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 53 | 35 | 66 | - | - |
| CP | 100 | 0 | 0 | - | - |
| M->M | 75 | 50 | 66 | - | - |
| M->P | 100 | 0 | 0 | - | - |
| P->M | 65 | 0 | 0 | - | - |
| P->P | 83 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 0.75}, relative {"MP": 0.0, "MM": 0.66} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.67} -> passes
