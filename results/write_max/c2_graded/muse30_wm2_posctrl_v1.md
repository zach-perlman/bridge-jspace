# C2-graded / muse30_wm2_posctrl_v1 (rule fixed in scripts/c2_graded.py; this output from commit 50be071)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| countries, given | 100 [100-100] (lens_add, question, 33, 0.4) | 47 [31-65] (lens_add, final, 33, 0.8) | 58 [41-73] (lens_transpl, question, joint, 1) | 58 [41-73] (lens_transpl, question, joint, 1) | 73 [64-82] (dom_add, question, 33, 0.8) | 100 [100-100] (lens_add, question, 33, 0.4) |
| countries, recalled | 98 [95-100] (lens_add, final, 33, 0.4) | 98 [95-100] (lens_add, final, 33, 0.4) | 0 [0-0] (lens_transpl, question, 23, 1) | 0 [0-0] (lens_transpl, question, 23, 1) | 80 [73-89] (dom_add, final, 33, 0.4) | 100 [100-100] (lens_swap, all, 23, 2) |
| M->M | 42 [23-63] (lens_add, final, 33, 0.8) | 42 [23-63] (lens_add, final, 33, 0.8) | 17 [9-24] (lens_transpl, final, joint, 1) | 17 [9-24] (lens_transpl, final, joint, 1) | 93 [86-100] (dom_natural, final, 33, 2) | 100 [100-100] (lens_swap, all, 25, 4) |

Rule: n/a (no M->P / M->M pair in this run)

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| countries, given | 23 | 97 | 100 | 58 | 66 |
| countries, recalled | 100 | 98 | 98 | 0 | 80 |
| M->M | 100 | 37 | 37 | 16 | 88 |
Positive control (reported; binding for no model): {"R": 1, "B": 1, "RR": 1} -> passes
