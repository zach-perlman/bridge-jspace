# C2-graded / wm2_full3_v1 (rule fixed in scripts/c2_graded.py; this output from commit 9683655)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| MMP | 55 [35-68] (lens_add, question, 32, 0.8) | 25 [14-38] (lens_add, final, 34, 0.8) | 28 [11-48] (lens_transpl, final, joint, 1) | 28 [11-48] (lens_transpl, final, joint, 1) | 24 [12-45] (dom_natural, final, 36, 2) | 55 [35-68] (lens_add, question, 32, 0.8) |
| MPM | 42 [25-59] (lens_swap, question, joint, 4) | 29 [10-48] (lens_swap, final, joint, 4) | 29 [12-52] (lens_transpl, final, 40, 2) | 29 [12-52] (lens_transpl, final, joint, 1) | 6 [0-19] (dom_add, question, 34, 0.4) | 42 [25-59] (lens_swap, question, joint, 4) |
| MPP | 25 [12-39] (lens_add, question, joint, 0.1) | 8 [0-16] (lens_add, final, joint, 0.1) | 10 [2-21] (lens_transpl, final, joint, 1) | 10 [2-21] (lens_transpl, final, joint, 1) | 26 [14-38] (dom_add, final, joint, 0.1) | 25 [12-39] (lens_add, question, joint, 0.1) |
| PMP | 10 [0-25] (lens_add, final, 38, 0.8) | 10 [0-25] (lens_add, final, 38, 0.8) | 18 [5-35] (lens_transpl, question, joint, 1) | 18 [5-35] (lens_transpl, question, joint, 1) | 21 [10-35] (dom_add, final, 36, 0.8) | 18 [5-35] (lens_transpl, question, joint, 1) |
| PPM | 14 [4-29] (lens_add, question, joint, 0.1) | 7 [0-20] (lens_add, final, joint, 0.1) | 7 [0-23] (lens_transpl, question, 38, 2) | 3 [0-15] (lens_transpl, question, 30, 1) | 7 [0-20] (dom_add, question, 38, 0.4) | 14 [4-29] (lens_add, question, joint, 0.1) |
| PPP | 5 [0-15] (lens_add, final, 32, 0.8) | 5 [0-15] (lens_add, final, 32, 0.8) | 2 [0-8] (lens_transpl, question, 32, 1) | 2 [0-8] (lens_transpl, question, 32, 1) | 24 [13-33] (dom_add, question, joint, 0.05) | 5 [0-15] (lens_add, final, 32, 0.8) |

Rule: n/a (no M->P / M->M pair in this run)
Positive control (binding for Gemma only): {} -> FAILS
