# C2-graded WITHOUT guessable cases (40 dropped; robustness split) / wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit 50be071)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 22 [12-33] (lens_add, final, 48, 0.8) | 22 [12-33] (lens_add, final, 48, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 22 [12-33] (lens_add, final, 48, 0.8) |
| CP | 0 [0-0] (lens_add, question, 48, 0.05) | 0 [0-0] (lens_add, final, 48, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 48, 0.05) |
| M->M | 20 [3-43] (lens_add, final, joint, 0.1) | 20 [3-43] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 20 [3-43] (lens_add, final, joint, 0.1) |
| M->P | 0 [0-0] (lens_add, question, 48, 0.05) | 0 [0-0] (lens_add, final, 48, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 48, 0.05) |
| P->M | 15 [7-24] (lens_add, final, 48, 0.8) | 15 [7-24] (lens_add, final, 48, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 15 [7-24] (lens_add, final, 48, 0.8) |
| P->P | 0 [0-0] (lens_add, question, 48, 0.05) | 0 [0-0] (lens_add, final, 48, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 48, 0.05) |

Rule: M->M best 20% vs M->P best 0%: >= 3x yes, >= +30 points no, intervals apart yes -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 96 | 20 | 21 | - | - |
| CP | 69 | 0 | 0 | - | - |
| M->M | 94 | 10 | 11 | - | - |
| M->P | 74 | 0 | 0 | - | - |
| P->M | 96 | 12 | 12 | - | - |
| P->P | 71 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 0.74, "MM": 0.94}, relative {"MP": 0.0, "MM": 0.11} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.2} -> FAILS
