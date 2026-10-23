# C2-graded WITHOUT guessable cases (44 dropped; robustness split) / muse30_wm2_fresh2_v1 (rule fixed in scripts/c2_graded.py; this output from commit da2afb2)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 21 [10-33] (lens_add, final, joint, 0.1) | 21 [10-33] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 21 [10-33] (lens_add, final, joint, 0.1) |
| CP | 5 [0-10] (lens_add, final, 27, 0.8) | 5 [0-10] (lens_add, final, 27, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 5 [0-10] (lens_add, final, 27, 0.8) |
| M->M | 42 [19-68] (lens_add, final, joint, 0.1) | 42 [19-68] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 42 [19-68] (lens_add, final, joint, 0.1) |
| M->P | 7 [0-16] (lens_add, question, 27, 0.8) | 7 [0-18] (lens_add, final, 27, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 7 [0-16] (lens_add, question, 27, 0.8) |
| P->M | 13 [4-28] (lens_add, final, joint, 0.1) | 13 [4-28] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 13 [4-28] (lens_add, final, joint, 0.1) |
| P->P | 2 [0-8] (lens_add, final, 29, 0.8) | 2 [0-8] (lens_add, final, 29, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 2 [0-8] (lens_add, final, 29, 0.8) |

Rule: M->M best 42% vs M->P best 7%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 98 | 18 | 19 | - | - |
| CP | 100 | 1 | 1 | - | - |
| M->M | 85 | 38 | 45 | - | - |
| M->P | 100 | 4 | 4 | - | - |
| P->M | 60 | 6 | 10 | - | - |
| P->P | 70 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 0.85}, relative {"MP": 0.04, "MM": 0.45} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.42} -> FAILS
