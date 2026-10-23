# C2-graded / qwen35_9b_wm2_full3_v1 (rule fixed in scripts/c2_graded.py; this output from commit d0fdb05)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| MMP | 6 [0-19] (lens_add, question, 17, 0.2) | 6 [0-19] (lens_add, final, 17, 0.8) | 6 [0-21] (lens_transpl, question, 14, 2) | 6 [0-19] (lens_transpl, question, 18, 1) | 17 [0-40] (dom_add, question, 17, 0.4) | 6 [0-21] (lens_transpl, question, 14, 2) |
| MPM | 25 [0-75] (lens_add, final, 14, 0.4) | 25 [0-75] (lens_add, final, 14, 0.4) | 0 [0-0] (lens_transpl, question, 14, 1) | 0 [0-0] (lens_transpl, question, 14, 1) | 100 [100-100] (dom_natural, final, 15, 2) | 25 [0-75] (lens_add, final, 14, 0.4) |
| MPP | 11 [0-30] (lens_swap, question, 15, 4) | 11 [0-30] (lens_swap, final, 17, 2) | 11 [0-30] (lens_transpl, question, 14, 2) | 11 [0-30] (lens_transpl, question, 20, 1) | 50 [0-100] (dom_add, question, 14, 0.4) | 11 [0-30] (lens_transpl, question, 14, 2) |
| PMP | 6 [0-21] (lens_add, question, 14, 0.4) | 6 [0-21] (lens_add, final, 14, 0.8) | 6 [0-21] (lens_transpl, question, 14, 1) | 6 [0-21] (lens_transpl, question, 14, 1) | 9 [0-23] (dom_add, final, 20, 0.8) | 6 [0-21] (lens_add, question, 14, 0.4) |
| PPM | 11 [0-29] (lens_swap, final, 19, 4) | 11 [0-29] (lens_swap, final, 19, 4) | 11 [0-25] (lens_transpl, question, 14, 1) | 11 [0-25] (lens_transpl, question, 14, 1) | 18 [0-60] (dom_add, question, joint, 0.1) | 11 [0-25] (lens_transpl, question, 14, 1) |
| PPP | 18 [0-33] (lens_add, final, joint, 0.2) | 18 [0-33] (lens_add, final, joint, 0.2) | 7 [0-17] (lens_transpl, question, 17, 1) | 7 [0-17] (lens_transpl, question, 17, 1) | 28 [11-45] (dom_add, question, joint, 0.1) | 18 [0-33] (lens_add, final, joint, 0.2) |

Rule: n/a (no M->P / M->M pair in this run)

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| MMP | 69 | 0 | 0 | 3 | 0 |
| MPM | 50 | 0 | 0 | 0 | 0 |
| MPP | 89 | 0 | 0 | 10 | 12 |
| PMP | 75 | 0 | 0 | 6 | 0 |
| PPM | 68 | 3 | 4 | 10 | 2 |
| PPP | 64 | 7 | 12 | 2 | 10 |
Positive control (reported; binding for no model): {} -> FAILS
