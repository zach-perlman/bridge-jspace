# C2-graded / wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 624cf82)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 18 [6-32] (lens_add, final, 36, 0.8) | 18 [6-32] (lens_add, final, 36, 0.8) | 18 [7-31] (lens_transpl, final, 40, 2) | 12 [3-24] (lens_transpl, final, joint, 1) | 39 [22-58] (dom_add, final, 40, 0.8) | 18 [6-32] (lens_add, final, 36, 0.8) |
| CP | 0 [0-0] (lens_add, question, 28, 0.05) | 0 [0-0] (lens_add, final, 28, 0.05) | 5 [0-15] (lens_transpl, final, joint, 2) | 0 [0-0] (lens_transpl, question, 28, 1) | 16 [4-27] (dom_add, final, 40, 0.8) | 5 [0-15] (lens_transpl, final, joint, 2) |
| M->M | 45 [23-70] (lens_add, question, joint, 0.1) | 38 [20-59] (lens_add, final, joint, 0.1) | 48 [32-68] (lens_transpl, question, joint, 1) | 48 [32-68] (lens_transpl, question, joint, 1) | 29 [6-56] (dom_add, final, 40, 0.8) | 48 [32-68] (lens_transpl, question, joint, 1) |
| M->P | 30 [15-44] (lens_add, question, joint, 0.1) | 10 [0-22] (lens_add, final, joint, 0.1) | 28 [11-49] (lens_transpl, question, joint, 1) | 28 [11-49] (lens_transpl, question, joint, 1) | 25 [9-42] (dom_add, question, 36, 0.8) | 30 [15-44] (lens_add, question, joint, 0.1) |
| P->M | 18 [7-30] (lens_add, question, 28, 0.8) | 10 [0-21] (lens_add, final, 34, 0.8) | 10 [0-23] (lens_transpl, final, 40, 2) | 8 [0-18] (lens_transpl, final, joint, 1) | 25 [9-43] (dom_add, final, 40, 0.8) | 18 [7-30] (lens_add, question, 28, 0.8) |
| P->P | 2 [0-8] (lens_add, question, 30, 0.8) | 0 [0-0] (lens_add, final, 28, 0.05) | 35 [20-52] (lens_transpl, question, joint, 2) | 0 [0-0] (lens_transpl, question, 28, 1) | 12 [3-23] (dom_add, final, 36, 0.8) | 35 [20-52] (lens_transpl, question, joint, 2) |

Rule: M->M best 45% vs M->P best 30%: >= 3x no, >= +30 points no, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 15 | 13 | 84 | 14 | 34 |
| CP | 2 | 0 | 0 | 0 | 9 |
| M->M | 32 | 31 | 96 | 47 | 15 |
| M->P | 35 | 23 | 66 | 26 | 19 |
| P->M | 22 | 12 | 54 | 6 | 14 |
| P->P | 12 | 0 | 0 | 34 | 4 |

C2-relative: ceilings {"MP": 0.35, "MM": 0.33}, relative {"MP": 0.66, "MM": 0.96} -> inconclusive: sites carry the bridge only partly
Positive control (binding for Gemma only): {"MM": 0.47} -> FAILS
