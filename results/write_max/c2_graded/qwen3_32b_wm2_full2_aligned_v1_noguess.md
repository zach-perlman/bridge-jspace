# C2-graded WITHOUT guessable cases (43 dropped; robustness split) / qwen3_32b_wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit 50be071)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 30 [19-41] (lens_add, final, joint, 0.1) | 30 [19-41] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 30 [19-41] (lens_add, final, joint, 0.1) |
| CP | 2 [0-7] (lens_add, final, joint, 0.4) | 2 [0-7] (lens_add, final, joint, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 2 [0-7] (lens_add, final, joint, 0.4) |
| M->M | 75 [50-92] (lens_add, final, joint, 0.1) | 75 [50-92] (lens_add, final, joint, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 75 [50-92] (lens_add, final, joint, 0.1) |
| M->P | 6 [0-13] (lens_add, question, 42, 0.4) | 3 [0-9] (lens_add, final, 40, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 6 [0-13] (lens_add, question, 42, 0.4) |
| P->M | 27 [16-38] (lens_add, final, joint, 0.2) | 27 [16-38] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 27 [16-38] (lens_add, final, joint, 0.2) |
| P->P | 2 [0-8] (lens_add, question, 40, 0.8) | 2 [0-6] (lens_add, final, joint, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 2 [0-8] (lens_add, question, 40, 0.8) |

Rule: M->M best 75% vs M->P best 6%: >= 3x yes, >= +30 points yes, intervals apart yes -> C2-graded HOLDS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 93 | 31 | 33 | - | - |
| CP | 100 | 0 | 0 | - | - |
| M->M | 100 | 75 | 75 | - | - |
| M->P | 100 | 3 | 3 | - | - |
| P->M | 88 | 24 | 27 | - | - |
| P->P | 83 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 1}, relative {"MP": 0.03, "MM": 0.75} -> HOLDS
Positive control (reported; binding for no model): {"MM": 0.75} -> passes
