# C2-graded WITHOUT guessable cases (12 dropped; robustness split) / gptoss20j_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit 7c7360d)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 14 [0-29] (lens_swap, final, joint, 2) | 14 [0-29] (lens_swap, final, joint, 2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 14 [0-29] (lens_swap, final, joint, 2) |
| CP | 14 [0-30] (lens_add, question, joint, 0.4) | 0 [0-0] (lens_add, final, 10, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 14 [0-30] (lens_add, question, joint, 0.4) |
| M->M | 12 [0-43] (lens_add, question, 15, 0.8) | 12 [0-43] (lens_add, final, 10, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 12 [0-43] (lens_add, question, 15, 0.8) |
| M->P | 0 [0-0] (lens_add, question, 10, 0.05) | 0 [0-0] (lens_add, final, 10, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 10, 0.05) |
| P->M | 9 [0-24] (lens_add, question, 12, 0.4) | 5 [0-18] (lens_add, final, 10, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 9 [0-24] (lens_add, question, 12, 0.4) |
| P->P | 14 [4-29] (lens_add, question, 12, 0.8) | 0 [0-0] (lens_add, final, 10, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 14 [4-29] (lens_add, question, 12, 0.8) |

Rule: M->M best 12% vs M->P best 0%: >= 3x yes, >= +30 points no, intervals apart yes -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 5 | 4 | 78 | - | - |
| CP | 0 | 6 | - | - | - |
| M->M | 25 | 0 | 0 | - | - |
| M->P | 0 | 0 | - | - | - |
| P->M | 14 | 3 | 23 | - | - |
| P->P | 5 | 7 | 100 | - | - |

C2-relative: ceilings {"MP": 0, "MM": 0.25}, relative {"MP": null, "MM": 0.0} -> inconclusive: sites carry the bridge only partly
Positive control (reported; binding for no model): {"MM": 0.12} -> FAILS
