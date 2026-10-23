# C2-graded WITHOUT guessable cases (28 dropped; robustness split) / qwen35_9b_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 6c0760e)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 22 [9-35] (lens_add, final, joint, 0.1) | 22 [9-35] (lens_add, final, joint, 0.1) | 17 [7-28] (lens_transpl, final, 19, 2) | 2 [0-8] (lens_transpl, final, 19, 1) | 51 [31-70] (dom_add, final, 20, 0.8) | 22 [9-35] (lens_add, final, joint, 0.1) |
| CP | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | 8 [0-18] (lens_transpl, final, joint, 2) | 0 [0-0] (lens_transpl, question, 14, 1) | 21 [7-35] (dom_add, final, 18, 0.4) | 8 [0-18] (lens_transpl, final, joint, 2) |
| M->M | 73 [56-89] (lens_add, final, 20, 0.8) | 73 [56-89] (lens_add, final, 20, 0.8) | 23 [0-47] (lens_transpl, final, joint, 1) | 23 [0-47] (lens_transpl, final, joint, 1) | 71 [50-85] (dom_natural, final, 20, 2) | 73 [56-89] (lens_add, final, 20, 0.8) |
| M->P | 9 [0-20] (lens_add, question, joint, 0.2) | 5 [0-18] (lens_add, final, 15, 0.8) | 9 [0-20] (lens_transpl, question, joint, 2) | 5 [0-18] (lens_transpl, question, joint, 1) | 12 [0-27] (dom_add, question, 17, 0.4) | 9 [0-20] (lens_add, question, joint, 0.2) |
| P->M | 18 [8-31] (lens_add, question, joint, 0.1) | 18 [8-30] (lens_add, final, joint, 0.1) | 11 [3-20] (lens_transpl, final, 20, 2) | 2 [0-6] (lens_transpl, final, 19, 1) | 37 [21-54] (dom_add, final, 20, 0.4) | 18 [8-31] (lens_add, question, joint, 0.1) |
| P->P | 2 [0-7] (lens_add, final, 14, 0.8) | 2 [0-7] (lens_add, final, 14, 0.8) | 4 [0-10] (lens_transpl, final, joint, 2) | 2 [0-7] (lens_transpl, question, joint, 1) | 27 [16-39] (dom_add, question, joint, 0.4) | 4 [0-10] (lens_transpl, final, joint, 2) |

Rule: M->M best 73% vs M->P best 9%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 76 | 14 | 19 | 17 | 51 |
| CP | 72 | 0 | 0 | 6 | 14 |
| M->M | 73 | 61 | 84 | 15 | 63 |
| M->P | 77 | 0 | 0 | 3 | 0 |
| P->M | 57 | 15 | 26 | 8 | 32 |
| P->P | 56 | 0 | 0 | 1 | 20 |

C2-relative: ceilings {"MP": 0.77, "MM": 0.73}, relative {"MP": 0.0, "MM": 0.84} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.73} -> passes
