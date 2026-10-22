# C2-graded / qwen3_32b_wm2_full3_v1 (rule fixed in scripts/c2_graded.py; this output from commit 50be071)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| MMP | 12 [0-26] (lens_add, question, joint, 0.2) | 12 [3-22] (lens_swap, final, joint, 4) | 2 [0-12] (lens_transpl, question, 30, 2) | 2 [0-12] (lens_transpl, final, 30, 1) | 21 [9-31] (dom_add, final, joint, 0.2) | 12 [0-26] (lens_add, question, joint, 0.2) |
| MPM | 30 [14-45] (lens_add, question, joint, 0.2) | 0 [0-0] (lens_add, final, 28, 0.05) | 9 [0-18] (lens_transpl, question, 32, 1) | 9 [0-18] (lens_transpl, question, 32, 1) | 16 [0-29] (dom_add, question, joint, 0.1) | 30 [14-45] (lens_add, question, joint, 0.2) |
| MPP | 38 [20-55] (lens_add, question, joint, 0.2) | 14 [0-30] (lens_add, final, joint, 0.2) | 10 [0-24] (lens_transpl, question, joint, 1) | 10 [0-24] (lens_transpl, question, joint, 1) | 56 [33-79] (dom_add, question, joint, 0.2) | 38 [20-55] (lens_add, question, joint, 0.2) |
| PMP | 15 [7-22] (lens_add, question, joint, 0.2) | 2 [0-9] (lens_add, final, 38, 0.8) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 13 [3-26] (dom_natural, question, joint, 2) | 15 [7-22] (lens_add, question, joint, 0.2) |
| PPM | 23 [11-35] (lens_add, question, joint, 0.1) | 10 [3-19] (lens_swap, final, joint, 2) | 5 [0-13] (lens_transpl, question, 30, 1) | 5 [0-13] (lens_transpl, question, 30, 1) | 16 [6-27] (dom_natural, question, joint, 1) | 23 [11-35] (lens_add, question, joint, 0.1) |
| PPP | 20 [8-34] (lens_add, question, joint, 0.2) | 20 [9-33] (lens_add, final, joint, 0.2) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 44 [26-66] (dom_add, question, joint, 0.1) | 20 [8-34] (lens_add, question, joint, 0.2) |

Rule: n/a (no M->P / M->M pair in this run)

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| MMP | 0 | 6 | - | 0 | 16 |
| MPM | 4 | 25 | 100 | 2 | 5 |
| MPP | 14 | 35 | 100 | 3 | 56 |
| PMP | 0 | 12 | - | 0 | 7 |
| PPM | 3 | 22 | 100 | 2 | 10 |
| PPP | 0 | 13 | - | 0 | 43 |
Positive control (reported; binding for no model): {} -> FAILS
