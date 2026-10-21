# C2-graded / wm2_suite_v1 (rule fixed in scripts/c2_graded.py; this output from commit 624cf82)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| countries, given | 100 [100-100] (lens_add, question, 38, 0.4) | 3 [0-9] (lens_add, final, 38, 0.8) | 98 [95-100] (lens_transpl, question, joint, 1) | 98 [95-100] (lens_transpl, question, joint, 1) | 72 [61-84] (dom_add, question, 40, 0.4) | 100 [100-100] (lens_add, question, 38, 0.4) |
| P->P | 3 [0-8] (lens_add, question, 30, 0.8) | 0 [0-0] (lens_add, final, 28, 0.05) | 42 [31-51] (lens_transpl, question, joint, 2) | 2 [0-5] (lens_transpl, question, joint, 1) | 60 [45-74] (dom_add, question, joint, 0.1) | 97 [92-100] (lens_transpl, all, joint, 1) |
| P->M | 63 [46-79] (lens_add, question, 36, 0.8) | 53 [32-70] (lens_add, final, 36, 0.8) | 67 [45-82] (lens_transpl, question, joint, 1) | 67 [45-82] (lens_transpl, question, joint, 1) | 100 [100-100] (dom_add, question, 40, 0.8) | 100 [100-100] (lens_add, all, 28, 0.4) |
| countries, recalled | 100 [100-100] (lens_add, question, 38, 0.4) | 2 [0-5] (lens_add, final, 28, 0.8) | 98 [95-100] (lens_transpl, question, joint, 1) | 98 [95-100] (lens_transpl, question, joint, 1) | 80 [71-90] (dom_add, question, 40, 0.4) | 100 [100-100] (lens_add, question, 38, 0.4) |
| M->P | 8 [2-16] (lens_add, question, joint, 0.1) | 0 [0-0] (lens_add, final, 28, 0.05) | 68 [53-84] (lens_transpl, question, joint, 2) | 12 [4-20] (lens_transpl, question, joint, 1) | 40 [27-55] (dom_add, question, 32, 0.8) | 100 [100-100] (lens_transpl, all, joint, 1) |
| M->M | 65 [46-84] (lens_add, final, joint, 0.05) | 65 [46-84] (lens_add, final, joint, 0.05) | 60 [43-74] (lens_transpl, question, joint, 2) | 52 [33-71] (lens_transpl, question, joint, 1) | 95 [89-100] (dom_add, question, joint, 0.1) | 100 [100-100] (lens_add, all, 28, 0.4) |

Rule: M->M best 65% vs M->P best 8%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| countries, given | 82 | 96 | 100 | 96 | 72 |
| P->P | 13 | 2 | 12 | 42 | 53 |
| P->M | 47 | 53 | 100 | 64 | 98 |
| countries, recalled | 93 | 91 | 98 | 98 | 80 |
| M->P | 67 | 5 | 7 | 69 | 34 |
| M->M | 62 | 57 | 93 | 52 | 90 |

C2-relative: ceilings {"RL": 0.67, "RR": 0.62}, relative {"RL": 0.07, "RR": 0.93} -> HOLDS
Positive control (binding for Gemma only): {"R": 1, "B": 1, "RR": 1} -> passes
