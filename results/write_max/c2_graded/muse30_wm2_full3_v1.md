# C2-graded / muse30_wm2_full3_v1 (rule fixed in scripts/c2_graded.py; this output from commit d67814b)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| MMP | 6 [0-16] (lens_add, question, joint, 0.1) | 3 [0-8] (lens_add, final, joint, 0.1) | 6 [0-14] (lens_transpl, final, joint, 1) | 6 [0-14] (lens_transpl, final, joint, 1) | 37 [8-63] (dom_natural, final, 33, 2) | 6 [0-16] (lens_add, question, joint, 0.1) |
| MPM | 12 [0-27] (lens_add, final, 33, 0.4) | 12 [0-27] (lens_add, final, 33, 0.4) | 12 [0-27] (lens_transpl, final, 33, 1) | 12 [0-27] (lens_transpl, final, 33, 1) | 18 [0-44] (dom_natural, final, 29, 1) | 12 [0-27] (lens_add, final, 33, 0.4) |
| MPP | 15 [4-26] (lens_add, question, joint, 0.1) | 10 [2-18] (lens_add, final, joint, 0.1) | 15 [5-25] (lens_transpl, question, joint, 1) | 15 [5-25] (lens_transpl, question, joint, 1) | 38 [15-61] (dom_add, final, joint, 0.1) | 15 [4-26] (lens_add, question, joint, 0.1) |
| PMP | 8 [0-15] (lens_add, question, joint, 0.2) | 5 [0-11] (lens_add, final, joint, 0.05) | 32 [22-45] (lens_transpl, question, joint, 2) | 8 [0-17] (lens_transpl, final, joint, 1) | 38 [22-48] (dom_add, final, joint, 0.1) | 32 [22-45] (lens_transpl, question, joint, 2) |
| PPM | 10 [0-20] (lens_add, question, joint, 0.05) | 10 [0-21] (lens_swap, final, joint, 2) | 5 [0-10] (lens_transpl, question, 25, 1) | 5 [0-10] (lens_transpl, question, 25, 1) | 11 [0-20] (dom_natural, question, 23, 1) | 10 [0-20] (lens_add, question, joint, 0.05) |
| PPP | 12 [5-22] (lens_add, question, 23, 0.4) | 5 [0-15] (lens_swap, final, joint, 4) | 5 [0-14] (lens_transpl, question, 23, 1) | 5 [0-14] (lens_transpl, question, 23, 1) | 20 [9-40] (dom_add, question, joint, 0.1) | 12 [5-22] (lens_add, question, 23, 0.4) |

Rule: n/a (no M->P / M->M pair in this run)

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| MMP | 94 | 0 | 0 | 3 | 25 |
| MPM | 100 | 2 | 2 | 6 | 8 |
| MPP | 100 | 9 | 9 | 11 | 30 |
| PMP | 92 | 4 | 4 | 34 | 28 |
| PPM | 95 | 1 | 1 | 4 | 4 |
| PPP | 85 | 11 | 13 | 3 | 11 |
Positive control (reported; binding for no model): {} -> FAILS
