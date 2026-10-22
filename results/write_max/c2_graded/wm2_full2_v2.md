# C2-graded / wm2_full2_v2 (rule fixed in scripts/c2_graded.py; this output from commit ce12747)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 21 [11-33] (lens_add, final, 38, 0.8) | 21 [11-33] (lens_add, final, 38, 0.8) | 12 [5-20] (lens_transpl, final, joint, 1) | 12 [5-20] (lens_transpl, final, joint, 1) | 31 [20-41] (dom_add, final, 36, 0.8) | 21 [11-33] (lens_add, final, 38, 0.8) |
| CP | 0 [0-0] (lens_add, question, 28, 0.05) | 0 [0-0] (lens_add, final, 28, 0.05) | 2 [0-6] (lens_transpl, final, joint, 2) | 1 [0-4] (lens_transpl, final, joint, 1) | 10 [3-19] (dom_add, final, 38, 0.8) | 2 [0-6] (lens_transpl, final, joint, 2) |
| M->M | 40 [26-56] (lens_add, question, joint, 0.1) | 28 [14-47] (lens_add, final, joint, 0.1) | 36 [24-51] (lens_transpl, question, joint, 1) | 36 [24-51] (lens_transpl, question, joint, 1) | 29 [12-47] (dom_add, final, 36, 0.8) | 40 [26-56] (lens_add, question, joint, 0.1) |
| M->P | 36 [24-48] (lens_add, question, joint, 0.1) | 8 [2-17] (lens_add, final, joint, 0.1) | 33 [22-49] (lens_transpl, question, joint, 1) | 33 [22-49] (lens_transpl, question, joint, 1) | 16 [6-29] (dom_add, question, 36, 0.8) | 36 [24-48] (lens_add, question, joint, 0.1) |
| P->M | 22 [14-30] (lens_add, question, joint, 0.1) | 15 [7-25] (lens_add, final, 38, 0.8) | 13 [5-21] (lens_transpl, final, joint, 1) | 13 [5-21] (lens_transpl, final, joint, 1) | 29 [14-47] (dom_natural, final, joint, 1) | 22 [14-30] (lens_add, question, joint, 0.1) |
| P->P | 2 [0-6] (lens_add, question, 30, 0.8) | 1 [0-4] (lens_add, final, joint, 0.4) | 44 [35-54] (lens_transpl, question, joint, 2) | 0 [0-0] (lens_transpl, question, 28, 1) | 14 [6-23] (dom_add, question, joint, 0.1) | 44 [35-54] (lens_transpl, question, joint, 2) |

Rule: M->M best 40% vs M->P best 36%: >= 3x no, >= +30 points no, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 50 | 17 | 35 | 10 | 29 |
| CP | 40 | 0 | 0 | 0 | 6 |
| M->M | 53 | 31 | 58 | 35 | 18 |
| M->P | 71 | 31 | 44 | 33 | 12 |
| P->M | 53 | 18 | 35 | 11 | 23 |
| P->P | 59 | 1 | 1 | 44 | 8 |

C2-relative: ceilings {"MP": 0.71, "MM": 0.53}, relative {"MP": 0.44, "MM": 0.58} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.4} -> FAILS
