# C2-graded WITHOUT guessable cases (51 dropped; robustness split) / muse30_wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit 32e2672)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 21 [8-36] (lens_add, final, joint, 0.1) | 21 [8-36] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 21 [8-36] (lens_add, final, joint, 0.1) |
| CP | 5 [0-13] (lens_add, question, joint, 0.2) | 0 [0-0] (lens_add, final, 22, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 5 [0-13] (lens_add, question, joint, 0.2) |
| M->M | 51 [27-73] (lens_add, final, joint, 0.1) | 51 [27-73] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 51 [27-73] (lens_add, final, joint, 0.1) |
| M->P | 11 [3-20] (lens_add, final, 30, 0.8) | 11 [3-20] (lens_add, final, 30, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 11 [3-20] (lens_add, final, 30, 0.8) |
| P->M | 19 [8-32] (lens_add, question, 28, 0.8) | 12 [2-25] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 19 [8-32] (lens_add, question, 28, 0.8) |
| P->P | 16 [6-28] (lens_add, question, joint, 0.2) | 0 [0-0] (lens_add, final, 22, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 16 [6-28] (lens_add, question, joint, 0.2) |

Rule: M->M best 51% vs M->P best 11%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 82 | 15 | 19 | - | - |
| CP | 95 | 1 | 1 | - | - |
| M->M | 81 | 45 | 56 | - | - |
| M->P | 98 | 6 | 6 | - | - |
| P->M | 56 | 15 | 27 | - | - |
| P->P | 73 | 16 | 22 | - | - |

C2-relative: ceilings {"MP": 0.98, "MM": 0.81}, relative {"MP": 0.06, "MM": 0.56} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.51} -> passes
