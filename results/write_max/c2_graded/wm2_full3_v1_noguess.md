# C2-graded WITHOUT guessable cases (51 dropped; robustness split) / wm2_full3_v1 (rule fixed in scripts/c2_graded.py; this output from commit 9683655)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| MMP | 57 [38-70] (lens_add, question, 32, 0.8) | 26 [11-45] (lens_add, final, 36, 0.8) | 29 [10-50] (lens_transpl, final, joint, 1) | 29 [10-50] (lens_transpl, final, joint, 1) | 24 [12-42] (dom_natural, final, 36, 2) | 57 [38-70] (lens_add, question, 32, 0.8) |
| MPM | 27 [8-47] (lens_swap, question, joint, 4) | 27 [0-53] (lens_swap, final, joint, 2) | 20 [0-42] (lens_transpl, final, 40, 1) | 20 [0-42] (lens_transpl, final, 40, 1) | 9 [0-25] (dom_add, question, 34, 0.4) | 27 [8-47] (lens_swap, question, joint, 4) |
| MPP | 25 [10-43] (lens_add, question, 28, 0.8) | 9 [0-21] (lens_add, final, joint, 0.1) | 9 [0-21] (lens_transpl, question, 28, 2) | 3 [0-12] (lens_transpl, question, 32, 1) | 30 [15-50] (dom_add, final, joint, 0.1) | 25 [10-43] (lens_add, question, 28, 0.8) |
| PMP | 10 [0-22] (lens_add, question, joint, 0.1) | 10 [2-26] (lens_swap, final, joint, 4) | 17 [4-38] (lens_transpl, question, joint, 1) | 17 [4-38] (lens_transpl, question, joint, 1) | 25 [15-34] (dom_add, final, 38, 0.8) | 17 [4-38] (lens_transpl, question, joint, 1) |
| PPM | 10 [0-26] (lens_add, question, joint, 0.05) | 10 [0-25] (lens_add, final, joint, 0.1) | 10 [0-29] (lens_transpl, question, 38, 2) | 5 [0-18] (lens_transpl, question, 30, 1) | 10 [0-29] (dom_add, question, 32, 0.4) | 10 [0-29] (lens_transpl, question, 38, 2) |
| PPP | 3 [0-11] (lens_add, final, 32, 0.8) | 3 [0-11] (lens_add, final, 32, 0.8) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 22 [10-36] (dom_add, question, joint, 0.05) | 3 [0-11] (lens_add, final, 32, 0.8) |

Rule: n/a (no M->P / M->M pair in this run)
Positive control (binding for Gemma only): {} -> FAILS
