# C2-graded / qwen35_9b_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 6c0760e)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 21 [8-33] (lens_add, final, joint, 0.1) | 21 [8-33] (lens_add, final, joint, 0.1) | 15 [7-24] (lens_transpl, final, 19, 2) | 2 [0-7] (lens_transpl, final, 19, 1) | 54 [39-68] (dom_add, final, 20, 0.8) | 21 [8-33] (lens_add, final, joint, 0.1) |
| CP | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | 8 [2-16] (lens_transpl, final, joint, 2) | 0 [0-0] (lens_transpl, question, 14, 1) | 17 [5-31] (dom_add, final, 18, 0.4) | 8 [2-16] (lens_transpl, final, joint, 2) |
| M->M | 72 [53-86] (lens_add, final, 20, 0.8) | 72 [53-86] (lens_add, final, 20, 0.8) | 24 [5-46] (lens_transpl, final, joint, 1) | 24 [5-46] (lens_transpl, final, joint, 1) | 68 [50-83] (dom_natural, final, 20, 2) | 72 [53-86] (lens_add, final, 20, 0.8) |
| M->P | 8 [0-20] (lens_add, question, joint, 0.2) | 4 [0-16] (lens_add, final, 15, 0.8) | 4 [0-16] (lens_transpl, question, joint, 1) | 4 [0-16] (lens_transpl, question, joint, 1) | 11 [0-27] (dom_add, question, 17, 0.4) | 8 [0-20] (lens_add, question, joint, 0.2) |
| P->M | 17 [7-31] (lens_add, question, joint, 0.1) | 17 [7-30] (lens_add, final, joint, 0.1) | 10 [3-18] (lens_transpl, final, 20, 2) | 2 [0-6] (lens_transpl, final, 19, 1) | 36 [20-51] (dom_add, final, 20, 0.4) | 17 [7-31] (lens_add, question, joint, 0.1) |
| P->P | 2 [0-6] (lens_add, final, 14, 0.8) | 2 [0-6] (lens_add, final, 14, 0.8) | 3 [0-9] (lens_transpl, final, joint, 2) | 2 [0-6] (lens_transpl, question, joint, 1) | 24 [14-36] (dom_add, question, joint, 0.4) | 3 [0-9] (lens_transpl, final, joint, 2) |

Rule: M->M best 72% vs M->P best 8%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 71 | 16 | 22 | 15 | 53 |
| CP | 73 | 0 | 0 | 7 | 10 |
| M->M | 76 | 61 | 80 | 18 | 62 |
| M->P | 80 | 0 | 0 | 0 | 0 |
| P->M | 57 | 13 | 24 | 8 | 31 |
| P->P | 57 | 0 | 0 | 1 | 18 |

C2-relative: ceilings {"MP": 0.8, "MM": 0.76}, relative {"MP": 0.0, "MM": 0.8} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.72} -> passes
