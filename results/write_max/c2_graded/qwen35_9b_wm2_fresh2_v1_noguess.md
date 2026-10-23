# C2-graded WITHOUT guessable cases (38 dropped; robustness split) / qwen35_9b_wm2_fresh2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 3bc4e9e)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 35 [18-53] (lens_add, final, 20, 0.8) | 35 [18-53] (lens_add, final, 20, 0.8) | 12 [2-23] (lens_transpl, final, joint, 1) | 12 [2-23] (lens_transpl, final, joint, 1) | 18 [3-32] (dom_add, final, joint, 0.1) | 35 [18-53] (lens_add, final, 20, 0.8) |
| CP | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | 2 [0-7] (lens_transpl, question, joint, 2) | 0 [0-0] (lens_transpl, question, 14, 1) | 20 [6-34] (dom_add, final, 17, 0.8) | 2 [0-7] (lens_transpl, question, joint, 2) |
| M->M | 77 [56-100] (lens_add, final, 19, 0.8) | 77 [56-100] (lens_add, final, 19, 0.8) | 15 [0-40] (lens_transpl, question, joint, 1) | 15 [0-40] (lens_transpl, question, joint, 1) | 89 [50-100] (dom_add, final, 20, 0.8) | 77 [56-100] (lens_add, final, 19, 0.8) |
| M->P | 7 [0-23] (lens_add, final, 14, 0.8) | 7 [0-23] (lens_add, final, 14, 0.8) | 20 [0-46] (lens_transpl, question, joint, 2) | 0 [0-0] (lens_transpl, question, 14, 1) | 56 [14-87] (dom_add, final, joint, 0.2) | 20 [0-46] (lens_transpl, question, joint, 2) |
| P->M | 27 [10-44] (lens_add, final, joint, 0.2) | 27 [10-44] (lens_add, final, joint, 0.2) | 13 [4-26] (lens_transpl, final, joint, 1) | 13 [4-26] (lens_transpl, final, joint, 1) | 38 [25-56] (dom_add, final, 20, 0.4) | 27 [10-44] (lens_add, final, joint, 0.2) |
| P->P | 7 [2-14] (lens_add, final, joint, 0.4) | 7 [2-14] (lens_add, final, joint, 0.4) | 2 [0-6] (lens_transpl, question, 15, 1) | 2 [0-6] (lens_transpl, question, 15, 1) | 20 [10-28] (dom_natural, final, 18, 2) | 7 [2-14] (lens_add, final, joint, 0.4) |

Rule: M->M best 77% vs M->P best 7%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 58 | 34 | 59 | 8 | 9 |
| CP | 82 | 0 | 0 | 0 | 12 |
| M->M | 77 | 75 | 98 | 8 | 73 |
| M->P | 87 | 0 | 0 | 18 | 26 |
| P->M | 51 | 19 | 38 | 9 | 34 |
| P->P | 46 | 6 | 12 | 0 | 10 |

C2-relative: ceilings {"MP": 0.87, "MM": 0.77}, relative {"MP": 0.0, "MM": 0.98} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.77} -> passes
