# C2-graded WITHOUT guessable cases (4 dropped; robustness split) / wm2_ctrl_v1 (rule fixed in scripts/c2_graded.py; this output from commit 66d573b)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| M->M | 57 [31-81] (lens_add, question, 34, 0.8) | 26 [8-48] (lens_add, final, joint, 0.1) | 17 [5-30] (lens_transpl, final, joint, 1) | 17 [5-30] (lens_transpl, final, joint, 1) | 24 [6-44] (dom_natural, final, joint, 1) | 87 [70-100] (lens_transpl, all, 28, 2) |
| M->P | 38 [14-58] (lens_add, question, 34, 0.8) | 4 [0-11] (lens_add, final, 36, 0.8) | 33 [16-59] (lens_transpl, question, joint, 1) | 33 [16-59] (lens_transpl, question, joint, 1) | 12 [0-31] (dom_add, question, 36, 0.8) | 38 [14-58] (lens_add, question, 34, 0.8) |
| P->M | 27 [12-47] (lens_add, question, joint, 0.1) | 21 [8-39] (lens_add, final, 38, 0.8) | 18 [6-35] (lens_transpl, final, 40, 2) | 6 [0-17] (lens_transpl, question, joint, 1) | 31 [8-50] (dom_add, question, joint, 0.1) | 82 [65-97] (lens_transpl, all, 28, 2) |
| P->P | 0 [0-0] (lens_add, question, 28, 0.05) | 0 [0-0] (lens_add, final, 28, 0.05) | 3 [0-9] (lens_transpl, question, joint, 1) | 3 [0-9] (lens_transpl, question, joint, 1) | 13 [0-33] (dom_add, question, 34, 0.8) | 81 [67-96] (lens_transpl, all, joint, 1) |

Rule: M->M best 57% vs M->P best 38%: >= 3x no, >= +30 points no, intervals apart no -> C2-graded FAILS
Positive control (binding for Gemma only): {"MM": 0.87} -> passes
