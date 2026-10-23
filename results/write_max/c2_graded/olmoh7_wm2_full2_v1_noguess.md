# C2-graded WITHOUT guessable cases (13 dropped; robustness split) / olmoh7_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit cf1a709)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 20 [0-40] (lens_add, final, 18, 0.4) | 20 [0-40] (lens_add, final, 18, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 20 [0-40] (lens_add, final, 18, 0.4) |
| CP | 0 [0-0] (lens_add, question, 14, 0.05) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 14, 0.05) |
| M->M | 50 [9-87] (lens_add, final, 16, 0.8) | 50 [9-87] (lens_add, final, 16, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 50 [9-87] (lens_add, final, 16, 0.8) |
| M->P | 6 [0-23] (lens_add, question, 14, 0.8) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 6 [0-23] (lens_add, question, 14, 0.8) |
| P->M | 6 [0-21] (lens_add, question, 19, 0.8) | 0 [0-0] (lens_add, final, 14, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 6 [0-21] (lens_add, question, 19, 0.8) |
| P->P | 0 [0-0] (lens_add, question, 14, 0.2) | 0 [0-0] (lens_add, final, 14, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 14, 0.2) |

Rule: M->M best 50% vs M->P best 6%: >= 3x yes, >= +30 points yes, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 73 | 10 | 13 | - | - |
| CP | 100 | 0 | 0 | - | - |
| M->M | 100 | 38 | 38 | - | - |
| M->P | 100 | 0 | 0 | - | - |
| P->M | 82 | 0 | 0 | - | - |
| P->P | 89 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 1}, relative {"MP": 0.0, "MM": 0.38} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.5} -> passes
