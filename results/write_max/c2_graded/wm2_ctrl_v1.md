# C2-graded / wm2_ctrl_v1 (rule fixed in scripts/c2_graded.py; this output from commit 66d573b)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| M->M | 54 [29-78] (lens_add, question, 34, 0.8) | 25 [8-46] (lens_add, final, joint, 0.1) | 17 [4-29] (lens_transpl, final, joint, 1) | 17 [4-29] (lens_transpl, final, joint, 1) | 24 [6-44] (dom_natural, final, joint, 1) | 88 [71-100] (lens_transpl, all, 28, 2) |
| M->P | 38 [14-58] (lens_add, question, 34, 0.8) | 4 [0-11] (lens_add, final, 36, 0.8) | 33 [16-59] (lens_transpl, question, joint, 1) | 33 [16-59] (lens_transpl, question, joint, 1) | 12 [0-31] (dom_add, question, 36, 0.8) | 38 [14-58] (lens_add, question, 34, 0.8) |
| P->M | 26 [12-46] (lens_add, question, joint, 0.1) | 21 [8-37] (lens_add, final, 38, 0.8) | 18 [6-35] (lens_transpl, final, 40, 2) | 6 [0-16] (lens_transpl, question, joint, 1) | 31 [8-50] (dom_add, question, joint, 0.1) | 82 [67-97] (lens_transpl, all, 28, 2) |
| P->P | 0 [0-0] (lens_add, question, 28, 0.05) | 0 [0-0] (lens_add, final, 28, 0.05) | 3 [0-8] (lens_transpl, question, joint, 1) | 3 [0-8] (lens_transpl, question, joint, 1) | 12 [0-30] (dom_add, question, 34, 0.8) | 76 [61-90] (lens_transpl, all, joint, 1) |

Rule: M->M best 54% vs M->P best 38%: >= 3x no, >= +30 points no, intervals apart no -> C2-graded FAILS
Positive control (binding for Gemma only): {"MM": 0.88} -> passes
