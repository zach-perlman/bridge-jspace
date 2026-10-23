# C2-graded / qwen35_9b_wm2_posctrl_v1 (rule fixed in scripts/c2_graded.py; this output from commit 6c0760e)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| countries, given | 100 [100-100] (lens_add, question, 18, 0.4) | 95 [88-100] (lens_add, final, 20, 0.8) | 60 [49-72] (lens_transpl, question, joint, 2) | 58 [45-72] (lens_transpl, question, joint, 1) | 88 [78-97] (dom_add, question, 20, 0.8) | 100 [100-100] (lens_add, question, 18, 0.4) |
| countries, recalled | 100 [100-100] (lens_add, question, 17, 0.4) | 82 [73-92] (lens_add, final, 20, 0.8) | 98 [95-100] (lens_transpl, question, joint, 1) | 98 [95-100] (lens_transpl, question, joint, 1) | 93 [88-98] (dom_add, question, 19, 0.8) | 100 [100-100] (lens_add, question, 17, 0.4) |
| M->M | 60 [43-78] (lens_add, final, 19, 0.8) | 60 [43-78] (lens_add, final, 19, 0.8) | 43 [27-60] (lens_transpl, final, joint, 1) | 43 [27-60] (lens_transpl, final, joint, 1) | 89 [77-98] (dom_add, final, 19, 0.8) | 100 [100-100] (lens_add, all, 14, 0.2) |

Rule: n/a (no M->P / M->M pair in this run)

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| countries, given | 50 | 96 | 100 | 54 | 83 |
| countries, recalled | 100 | 98 | 98 | 98 | 87 |
| M->M | 95 | 55 | 58 | 43 | 84 |
Positive control (reported; binding for no model): {"R": 1, "B": 1, "RR": 1} -> passes
