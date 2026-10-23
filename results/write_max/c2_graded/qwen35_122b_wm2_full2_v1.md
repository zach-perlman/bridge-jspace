# C2-graded / qwen35_122b_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 08ba305)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 8 [2-14] (lens_add, question, joint, 0.2) | 5 [1-11] (lens_add, final, 25, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 8 [2-14] (lens_add, question, joint, 0.2) |
| CP | 2 [0-7] (lens_add, question, joint, 0.4) | 0 [0-0] (lens_add, final, 21, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 2 [0-7] (lens_add, question, joint, 0.4) |
| M->M | 39 [23-52] (lens_add, question, 30, 0.8) | 4 [0-11] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 39 [23-52] (lens_add, question, 30, 0.8) |
| M->P | 28 [13-45] (lens_add, question, 29, 0.8) | 1 [0-4] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 28 [13-45] (lens_add, question, 29, 0.8) |
| P->M | 62 [49-74] (lens_add, question, joint, 0.1) | 5 [1-11] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 62 [49-74] (lens_add, question, joint, 0.1) |
| P->P | 42 [31-54] (lens_add, question, 24, 0.8) | 0 [0-0] (lens_add, final, 21, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 42 [31-54] (lens_add, question, 24, 0.8) |

Rule: M->M best 39% vs M->P best 28%: >= 3x no, >= +30 points no, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 2 | 4 | 100 | - | - |
| CP | 0 | 0 | - | - | - |
| M->M | 8 | 35 | 100 | - | - |
| M->P | 12 | 27 | 100 | - | - |
| P->M | 3 | 62 | 100 | - | - |
| P->P | 0 | 39 | - | - | - |

C2-relative: ceilings {"MP": 0.12, "MM": 0.08}, relative {"MP": 1.0, "MM": 1.0} -> inconclusive: sites carry the bridge only partly
Positive control (reported; binding for no model): {"MM": 0.39} -> FAILS
