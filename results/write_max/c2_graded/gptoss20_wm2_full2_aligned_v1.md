# C2-graded / gptoss20_wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit 7c7360d)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 17 [0-41] (lens_add, question, joint, 0.1) | 9 [0-23] (lens_swap, final, 18, 4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 17 [0-41] (lens_add, question, joint, 0.1) |
| CP | 9 [0-21] (lens_add, question, 17, 0.8) | 4 [0-12] (lens_add, final, 19, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 9 [0-21] (lens_add, question, 17, 0.8) |
| M->M | 27 [0-67] (lens_add, question, 17, 0.4) | 27 [0-62] (lens_add, final, 15, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 27 [0-67] (lens_add, question, 17, 0.4) |
| M->P | 9 [0-27] (lens_add, question, 19, 0.2) | 0 [0-0] (lens_add, final, 15, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 9 [0-27] (lens_add, question, 19, 0.2) |
| P->M | 4 [0-12] (lens_add, question, 19, 0.1) | 4 [0-12] (lens_add, final, 18, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 4 [0-12] (lens_add, question, 19, 0.1) |
| P->P | 8 [0-20] (lens_add, final, 18, 0.2) | 8 [0-20] (lens_add, final, 18, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 8 [0-20] (lens_add, final, 18, 0.2) |

Rule: M->M best 27% vs M->P best 9%: >= 3x yes, >= +30 points no, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 100 | 8 | 8 | - | - |
| CP | 100 | 0 | 0 | - | - |
| M->M | 91 | 5 | 6 | - | - |
| M->P | 100 | 0 | 0 | - | - |
| P->M | 92 | 0 | 0 | - | - |
| P->P | 92 | 1 | 1 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 0.91}, relative {"MP": 0.0, "MM": 0.06} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.27} -> FAILS
