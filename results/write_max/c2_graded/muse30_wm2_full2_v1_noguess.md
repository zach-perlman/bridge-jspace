# C2-graded WITHOUT guessable cases (51 dropped; robustness split) / muse30_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 6c0760e)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 21 [6-37] (lens_add, final, joint, 0.1) | 21 [6-37] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 21 [6-37] (lens_add, final, joint, 0.1) |
| CP | 5 [0-13] (lens_add, question, joint, 0.2) | 0 [0-0] (lens_add, final, 23, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 5 [0-13] (lens_add, question, joint, 0.2) |
| M->M | 57 [34-77] (lens_add, final, joint, 0.1) | 57 [34-77] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 57 [34-77] (lens_add, final, joint, 0.1) |
| M->P | 7 [0-14] (lens_add, final, 29, 0.8) | 7 [0-14] (lens_add, final, 29, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 7 [0-14] (lens_add, final, 29, 0.8) |
| P->M | 21 [9-33] (lens_add, final, joint, 0.1) | 21 [9-33] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 21 [9-33] (lens_add, final, joint, 0.1) |
| P->P | 14 [4-26] (lens_add, question, joint, 0.2) | 2 [0-6] (lens_add, final, 29, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 14 [4-26] (lens_add, question, joint, 0.2) |

Rule: M->M best 57% vs M->P best 7%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 89 | 16 | 17 | - | - |
| CP | 98 | 2 | 2 | - | - |
| M->M | 84 | 50 | 59 | - | - |
| M->P | 100 | 2 | 2 | - | - |
| P->M | 69 | 15 | 21 | - | - |
| P->P | 76 | 13 | 18 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 0.84}, relative {"MP": 0.02, "MM": 0.59} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.57} -> passes
