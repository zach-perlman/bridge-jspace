# C2-graded WITHOUT guessable cases (12 dropped; robustness split) / gptoss20_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit b8eb92f)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 14 [0-26] (lens_add, final, 13, 0.4) | 14 [0-26] (lens_add, final, 13, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 14 [0-26] (lens_add, final, 13, 0.4) |
| CP | 5 [0-16] (lens_add, question, 11, 0.8) | 5 [0-13] (lens_add, final, 12, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 5 [0-16] (lens_add, question, 11, 0.8) |
| M->M | 38 [0-70] (lens_add, final, 15, 0.2) | 38 [0-70] (lens_add, final, 15, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 38 [0-70] (lens_add, final, 15, 0.2) |
| M->P | 0 [0-0] (lens_add, question, 10, 0.05) | 0 [0-0] (lens_add, final, 10, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 10, 0.05) |
| P->M | 5 [0-18] (lens_add, question, 12, 0.4) | 5 [0-18] (lens_add, final, 11, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 5 [0-18] (lens_add, question, 12, 0.4) |
| P->P | 19 [5-33] (lens_add, question, 12, 0.8) | 5 [0-16] (lens_add, final, 12, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 19 [5-33] (lens_add, question, 12, 0.8) |

Rule: M->M best 38% vs M->P best 0%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 5 | 4 | 82 | - | - |
| CP | 0 | 0 | - | - | - |
| M->M | 25 | 12 | 48 | - | - |
| M->P | 0 | 0 | - | - | - |
| P->M | 14 | 0 | 0 | - | - |
| P->P | 5 | 13 | 100 | - | - |

C2-relative: ceilings {"MP": 0, "MM": 0.25}, relative {"MP": null, "MM": 0.47} -> inconclusive: sites carry the bridge only partly
Positive control (reported; binding for no model): {"MM": 0.38} -> FAILS
