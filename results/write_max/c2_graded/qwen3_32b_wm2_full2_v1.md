# C2-graded / qwen3_32b_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit ab86c4e)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 6 [0-14] (lens_add, question, joint, 0.2) | 4 [0-10] (lens_add, final, joint, 0.1) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 15 [6-25] (dom_add, final, joint, 0.2) | 6 [0-14] (lens_add, question, joint, 0.2) |
| CP | 2 [0-7] (lens_add, question, joint, 0.2) | 0 [0-0] (lens_add, final, 28, 0.05) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 4 [0-11] (dom_add, question, joint, 0.2) | 2 [0-7] (lens_add, question, joint, 0.2) |
| M->M | 10 [0-21] (lens_add, question, joint, 0.4) | 10 [0-23] (lens_add, final, joint, 0.1) | 10 [0-22] (lens_transpl, final, joint, 2) | 2 [0-9] (lens_transpl, question, joint, 1) | 10 [0-23] (dom_add, final, joint, 0.2) | 10 [0-21] (lens_add, question, joint, 0.4) |
| M->P | 12 [2-24] (lens_add, question, joint, 0.2) | 2 [0-7] (lens_add, final, 28, 0.05) | 5 [0-11] (lens_transpl, question, 28, 2) | 5 [0-11] (lens_transpl, question, 30, 1) | 13 [0-32] (dom_add, question, 40, 0.8) | 12 [2-24] (lens_add, question, joint, 0.2) |
| P->M | 16 [5-29] (lens_add, question, joint, 0.1) | 4 [0-9] (lens_add, final, joint, 0.2) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 4 [0-11] (dom_natural, question, joint, 1) | 16 [5-29] (lens_add, question, joint, 0.1) |
| P->P | 9 [2-18] (lens_add, question, joint, 0.2) | 0 [0-0] (lens_add, final, 28, 0.05) | 0 [0-0] (lens_transpl, question, 28, 1) | 0 [0-0] (lens_transpl, question, 28, 1) | 11 [2-20] (dom_natural, question, joint, 2) | 9 [2-18] (lens_add, question, joint, 0.2) |

Rule: M->M best 10% vs M->P best 12%: >= 3x no, >= +30 points no, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 0 | 2 | - | 0 | 12 |
| CP | 0 | 0 | - | 0 | 1 |
| M->M | 8 | 2 | 31 | 4 | 2 |
| M->P | 8 | 7 | 97 | 2 | 8 |
| P->M | 0 | 16 | - | 0 | 2 |
| P->P | 0 | 5 | - | 0 | 8 |

C2-relative: ceilings {"MP": 0.07, "MM": 0.07}, relative {"MP": 0.97, "MM": 0.31} -> inconclusive: sites carry the bridge only partly
Positive control (reported; binding for no model): {"MM": 0.1} -> FAILS
