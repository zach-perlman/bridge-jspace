# C2-graded WITHOUT guessable cases (43 dropped; robustness split) / qwen3_32b_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit ab86c4e)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 5 [0-12] (lens_add, question, 30, 0.8) | 5 [0-12] (lens_add, final, joint, 0.1) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 15 [6-27] (dom_add, final, joint, 0.2) | 5 [0-12] (lens_add, question, 30, 0.8) |
| CP | 2 [0-8] (lens_add, question, joint, 0.2) | 0 [0-0] (lens_add, final, 28, 0.05) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 5 [0-13] (dom_add, question, joint, 0.2) | 2 [0-8] (lens_add, question, joint, 0.2) |
| M->M | 9 [0-27] (lens_add, question, 36, 0.8) | 9 [0-25] (lens_add, final, joint, 0.1) | 6 [0-17] (lens_transpl, question, 40, 2) | 3 [0-11] (lens_transpl, question, joint, 1) | 12 [0-25] (dom_add, final, joint, 0.2) | 9 [0-27] (lens_add, question, 36, 0.8) |
| M->P | 8 [0-21] (lens_add, question, 30, 0.8) | 3 [0-9] (lens_add, final, 28, 0.05) | 6 [0-13] (lens_transpl, question, 28, 2) | 6 [0-13] (lens_transpl, question, 30, 1) | 15 [0-39] (dom_add, question, 40, 0.8) | 8 [0-21] (lens_add, question, 30, 0.8) |
| P->M | 16 [5-30] (lens_add, question, joint, 0.1) | 4 [0-10] (lens_add, final, joint, 0.2) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 5 [0-12] (dom_add, question, joint, 0.1) | 16 [5-30] (lens_add, question, joint, 0.1) |
| P->P | 9 [2-19] (lens_add, question, joint, 0.2) | 0 [0-0] (lens_add, final, 28, 0.05) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 5 [0-15] (dom_add, question, joint, 0.2) | 9 [2-19] (lens_add, question, joint, 0.2) |

Rule: M->M best 9% vs M->P best 8%: >= 3x no, >= +30 points no, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 0 | 2 | - | 0 | 12 |
| CP | 0 | 0 | - | 0 | 2 |
| M->M | 9 | 2 | 23 | 0 | 3 |
| M->P | 8 | 3 | 32 | 3 | 10 |
| P->M | 0 | 15 | - | 0 | 3 |
| P->P | 0 | 3 | - | 0 | 2 |

C2-relative: ceilings {"MP": 0.08, "MM": 0.09}, relative {"MP": 0.32, "MM": 0.23} -> inconclusive: sites carry the bridge only partly
Positive control (reported; binding for no model): {"MM": 0.09} -> FAILS
