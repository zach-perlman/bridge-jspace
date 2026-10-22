# C2-graded / qwen3_32b_wm2_posctrl_v1 (rule fixed in scripts/c2_graded.py; this output from commit 50be071)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| countries, given | 35 [18-55] (lens_add, question, joint, 0.1) | 7 [0-14] (lens_add, final, joint, 0.4) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 3 [0-9] (dom_add, question, 40, 0.8) | 100 [100-100] (lens_swap, all, 28, 2) |
| countries, recalled | 93 [88-98] (lens_add, question, joint, 0.1) | 18 [11-25] (lens_add, final, joint, 0.2) | 52 [35-68] (lens_transpl, question, joint, 1) | 52 [35-68] (lens_transpl, question, joint, 1) | 5 [0-13] (dom_add, question, 40, 0.8) | 100 [100-100] (lens_transpl, all, 28, 2) |
| M->M | 15 [4-25] (lens_add, question, joint, 0.4) | 10 [3-16] (lens_add, final, joint, 0.2) | 3 [0-8] (lens_transpl, question, joint, 2) | 0 [0-0] (lens_transpl, question, 28, 1) | 17 [9-27] (dom_natural, final, joint, 1) | 100 [100-100] (lens_swap, all, 36, 4) |

Rule: n/a (no M->P / M->M pair in this run)

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| countries, given | 0 | 32 | - | 0 | 2 |
| countries, recalled | 0 | 93 | - | 52 | 3 |
| M->M | 0 | 9 | - | 2 | 12 |
Positive control (reported; binding for no model): {"R": 1, "B": 1, "RR": 1} -> passes
