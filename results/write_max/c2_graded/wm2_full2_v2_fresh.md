# C2-graded, FRESH cases only (240 seen ones dropped) / wm2_full2_v2 (rule fixed in scripts/c2_graded.py; this output from commit ce12747)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 17 [6-30] (lens_add, final, 40, 0.8) | 17 [6-30] (lens_add, final, 40, 0.8) | 12 [3-24] (lens_transpl, final, joint, 1) | 12 [3-24] (lens_transpl, final, joint, 1) | 32 [19-49] (dom_add, final, 36, 0.8) | 17 [6-30] (lens_add, final, 40, 0.8) |
| CP | 0 [0-0] (lens_add, question, 28, 0.05) | 0 [0-0] (lens_add, final, 28, 0.05) | 2 [0-8] (lens_transpl, final, 36, 2) | 2 [0-8] (lens_transpl, final, joint, 1) | 12 [4-22] (dom_add, question, 38, 0.8) | 2 [0-8] (lens_transpl, final, 36, 2) |
| M->M | 41 [16-67] (lens_add, question, 34, 0.8) | 16 [3-38] (lens_add, final, joint, 0.1) | 16 [3-32] (lens_transpl, question, 40, 2) | 6 [0-16] (lens_transpl, final, joint, 1) | 28 [4-55] (dom_add, final, 36, 0.8) | 41 [16-67] (lens_add, question, 34, 0.8) |
| M->P | 44 [22-72] (lens_add, question, joint, 0.1) | 6 [0-18] (lens_add, final, joint, 0.1) | 12 [3-26] (lens_transpl, final, joint, 2) | 6 [0-17] (lens_transpl, question, 40, 1) | 21 [4-45] (dom_add, question, 36, 0.8) | 44 [22-72] (lens_add, question, joint, 0.1) |
| P->M | 26 [14-38] (lens_add, question, joint, 0.1) | 17 [8-30] (lens_add, final, 36, 0.8) | 13 [4-24] (lens_transpl, final, 40, 2) | 13 [4-24] (lens_transpl, final, joint, 1) | 29 [13-45] (dom_add, final, 38, 0.8) | 26 [14-38] (lens_add, question, joint, 0.1) |
| P->P | 2 [0-6] (lens_add, question, 28, 0.8) | 2 [0-7] (lens_add, final, joint, 0.4) | 47 [35-61] (lens_transpl, question, joint, 2) | 0 [0-0] (lens_transpl, question, 28, 1) | 12 [3-21] (dom_add, final, 38, 0.8) | 47 [35-61] (lens_transpl, question, joint, 2) |

Rule: M->M best 41% vs M->P best 44%: >= 3x no, >= +30 points no, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 40 | 10 | 26 | 8 | 31 |
| CP | 31 | 0 | 0 | 0 | 8 |
| M->M | 44 | 28 | 64 | 10 | 14 |
| M->P | 69 | 35 | 51 | 7 | 13 |
| P->M | 55 | 21 | 38 | 11 | 19 |
| P->P | 47 | 0 | 0 | 47 | 5 |

C2-relative: ceilings {"MP": 0.69, "MM": 0.44}, relative {"MP": 0.51, "MM": 0.64} -> inconclusive: sites carry the bridge only partly
Positive control (reported; binding for no model): {"MM": 0.41} -> FAILS
