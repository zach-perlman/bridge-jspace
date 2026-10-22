# C2-graded / wm2_full2_v2 (rule fixed in scripts/c2_graded.py; this output from commit 1249d90)

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
| CM | 12 | 17 | 100 | 10 | 29 |
| CP | 2 | 0 | 0 | 0 | 6 |
| M->M | 24 | 31 | 100 | 35 | 18 |
| M->P | 57 | 31 | 55 | 33 | 12 |
| P->M | 36 | 18 | 52 | 11 | 23 |
| P->P | 28 | 1 | 2 | 44 | 8 |

Copy ceiling from wm2_full2_v2_ceiling (copy-only run on the same cases, the joint copy pasted); this run's own (stacked joint copy): CM 50, CP 40, M->M 53, M->P 71, P->M 53, P->P 59

C2-relative: ceilings {"MP": 0.57, "MM": 0.24}, relative {"MP": 0.55, "MM": 1.0} -> inconclusive: sites carry the bridge only partly
Positive control (reported; binding for no model): {"MM": 0.4} -> FAILS
