# C2-graded WITHOUT guessable cases (31 dropped; robustness split) / qwen35_122b_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 08ba305)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 7 [2-14] (lens_add, question, 24, 0.8) | 5 [1-11] (lens_add, final, 29, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 7 [2-14] (lens_add, question, 24, 0.8) |
| CP | 3 [0-7] (lens_add, question, joint, 0.4) | 0 [0-0] (lens_add, final, 21, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 3 [0-7] (lens_add, question, joint, 0.4) |
| M->M | 38 [24-52] (lens_add, question, 30, 0.8) | 3 [0-11] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 38 [24-52] (lens_add, question, 30, 0.8) |
| M->P | 25 [11-40] (lens_add, question, 29, 0.8) | 1 [0-5] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 25 [11-40] (lens_add, question, 29, 0.8) |
| P->M | 61 [47-74] (lens_add, question, joint, 0.1) | 5 [1-11] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 61 [47-74] (lens_add, question, joint, 0.1) |
| P->P | 43 [31-55] (lens_add, question, 24, 0.8) | 0 [0-0] (lens_add, final, 21, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 43 [31-55] (lens_add, question, 24, 0.8) |

Rule: M->M best 38% vs M->P best 25%: >= 3x no, >= +30 points no, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 1 | 4 | 100 | - | - |
| CP | 0 | 0 | - | - | - |
| M->M | 9 | 32 | 100 | - | - |
| M->P | 13 | 23 | 100 | - | - |
| P->M | 1 | 58 | 100 | - | - |
| P->P | 0 | 39 | - | - | - |

C2-relative: ceilings {"MP": 0.13, "MM": 0.09}, relative {"MP": 1.0, "MM": 1.0} -> inconclusive: sites carry the bridge only partly
Positive control (reported; binding for no model): {"MM": 0.38} -> FAILS
