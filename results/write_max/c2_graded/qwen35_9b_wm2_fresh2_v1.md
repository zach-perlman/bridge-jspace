# C2-graded / qwen35_9b_wm2_fresh2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 3bc4e9e)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 21 [8-36] (lens_add, final, joint, 0.1) | 21 [8-36] (lens_add, final, joint, 0.1) | 12 [3-23] (lens_transpl, final, joint, 1) | 12 [3-23] (lens_transpl, final, joint, 1) | 52 [40-65] (dom_natural, final, 19, 2) | 21 [8-36] (lens_add, final, joint, 0.1) |
| CP | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | 2 [0-6] (lens_transpl, question, joint, 2) | 0 [0-0] (lens_transpl, question, 14, 1) | 19 [5-33] (dom_add, final, 17, 0.8) | 2 [0-6] (lens_transpl, question, joint, 2) |
| M->M | 61 [39-88] (lens_add, final, 18, 0.8) | 61 [39-88] (lens_add, final, 18, 0.8) | 22 [5-47] (lens_transpl, final, joint, 1) | 22 [5-47] (lens_transpl, final, joint, 1) | 90 [62-100] (dom_add, final, 20, 0.8) | 61 [39-88] (lens_add, final, 18, 0.8) |
| M->P | 6 [0-20] (lens_add, final, 14, 0.8) | 6 [0-20] (lens_add, final, 14, 0.8) | 17 [0-40] (lens_transpl, question, joint, 2) | 0 [0-0] (lens_transpl, question, 14, 1) | 60 [14-89] (dom_add, final, joint, 0.2) | 17 [0-40] (lens_transpl, question, joint, 2) |
| P->M | 22 [9-38] (lens_add, final, joint, 0.2) | 22 [9-38] (lens_add, final, joint, 0.2) | 12 [5-22] (lens_transpl, final, joint, 1) | 12 [5-22] (lens_transpl, final, joint, 1) | 51 [36-67] (dom_natural, final, 20, 2) | 22 [9-38] (lens_add, final, joint, 0.2) |
| P->P | 7 [2-13] (lens_add, final, joint, 0.4) | 7 [2-13] (lens_add, final, joint, 0.4) | 2 [0-5] (lens_transpl, question, 15, 1) | 2 [0-5] (lens_transpl, question, 15, 1) | 18 [10-27] (dom_natural, final, 18, 2) | 7 [2-13] (lens_add, final, joint, 0.4) |

Rule: M->M best 61% vs M->P best 6%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 58 | 16 | 27 | 10 | 52 |
| CP | 81 | 0 | 0 | 0 | 11 |
| M->M | 83 | 62 | 74 | 11 | 75 |
| M->P | 78 | 0 | 0 | 13 | 25 |
| P->M | 46 | 16 | 35 | 9 | 49 |
| P->P | 46 | 5 | 11 | 0 | 11 |

C2-relative: ceilings {"MP": 0.78, "MM": 0.83}, relative {"MP": 0.0, "MM": 0.74} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.61} -> passes
