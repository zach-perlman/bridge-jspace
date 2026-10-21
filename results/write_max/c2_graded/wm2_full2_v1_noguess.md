# C2-graded WITHOUT guessable cases (29 dropped; robustness split) / wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 3693aba)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 21 [9-35] (lens_add, final, 40, 0.8) | 21 [9-35] (lens_add, final, 40, 0.8) | 21 [9-35] (lens_transpl, final, 40, 2) | 12 [3-25] (lens_transpl, final, joint, 1) | 36 [18-57] (dom_add, final, 40, 0.8) | 21 [9-35] (lens_add, final, 40, 0.8) |
| CP | 0 [0-0] (lens_add, question, 28, 0.05) | 0 [0-0] (lens_add, final, 28, 0.05) | 6 [0-16] (lens_transpl, final, joint, 2) | 0 [0-0] (lens_transpl, question, 28, 1) | 18 [7-30] (dom_add, final, 40, 0.8) | 6 [0-16] (lens_transpl, final, joint, 2) |
| M->M | 46 [24-68] (lens_add, question, joint, 0.1) | 40 [20-63] (lens_add, final, 36, 0.8) | 31 [16-48] (lens_transpl, final, joint, 1) | 31 [16-48] (lens_transpl, final, joint, 1) | 28 [5-56] (dom_add, final, 40, 0.8) | 46 [24-68] (lens_add, question, joint, 0.1) |
| M->P | 30 [15-44] (lens_add, question, joint, 0.1) | 10 [0-22] (lens_add, final, joint, 0.1) | 28 [11-49] (lens_transpl, question, joint, 1) | 28 [11-49] (lens_transpl, question, joint, 1) | 25 [9-42] (dom_add, question, 36, 0.8) | 30 [15-44] (lens_add, question, joint, 0.1) |
| P->M | 17 [6-26] (lens_add, question, joint, 0.1) | 8 [0-16] (lens_add, final, joint, 0.1) | 11 [0-25] (lens_transpl, final, 40, 2) | 8 [0-20] (lens_transpl, final, joint, 1) | 29 [11-48] (dom_add, final, 40, 0.8) | 17 [6-26] (lens_add, question, joint, 0.1) |
| P->P | 3 [0-11] (lens_add, question, 30, 0.8) | 0 [0-0] (lens_add, final, 28, 0.05) | 40 [23-59] (lens_transpl, question, joint, 2) | 0 [0-0] (lens_transpl, question, 28, 1) | 12 [0-26] (dom_add, question, 28, 0.8) | 40 [23-59] (lens_transpl, question, joint, 2) |

Rule: M->M best 46% vs M->P best 30%: >= 3x no, >= +30 points no, intervals apart no -> C2-graded FAILS
Positive control (binding for Gemma only): {"MM": 0.46} -> FAILS
