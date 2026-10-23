# C2-graded / gptoss20j_wm2_full2_aligned_v1 (rule fixed in scripts/c2_graded.py; this output from commit 7c7360d)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 13 [0-26] (lens_add, question, 17, 0.4) | 13 [0-32] (lens_add, final, 17, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 13 [0-26] (lens_add, question, 17, 0.4) |
| CP | 9 [0-20] (lens_add, question, 17, 0.4) | 4 [0-12] (lens_add, final, 17, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 9 [0-20] (lens_add, question, 17, 0.4) |
| M->M | 27 [7-62] (lens_add, final, 18, 0.1) | 27 [7-62] (lens_add, final, 18, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 27 [7-62] (lens_add, final, 18, 0.1) |
| M->P | 18 [0-50] (lens_add, question, joint, 0.2) | 0 [0-0] (lens_add, final, 15, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 18 [0-50] (lens_add, question, joint, 0.2) |
| P->M | 8 [0-27] (lens_add, final, 15, 0.2) | 8 [0-27] (lens_add, final, 15, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 8 [0-27] (lens_add, final, 15, 0.2) |
| P->P | 4 [0-12] (lens_add, question, 17, 0.4) | 4 [0-15] (lens_add, final, 15, 0.1) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 4 [0-12] (lens_add, question, 17, 0.4) |

Rule: M->M best 27% vs M->P best 18%: >= 3x no, >= +30 points no, intervals apart no -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 100 | 5 | 5 | - | - |
| CP | 100 | 0 | 0 | - | - |
| M->M | 91 | 7 | 8 | - | - |
| M->P | 100 | 2 | 2 | - | - |
| P->M | 92 | 1 | 1 | - | - |
| P->P | 92 | 0 | 0 | - | - |

C2-relative: ceilings {"MP": 1, "MM": 0.91}, relative {"MP": 0.02, "MM": 0.08} -> FAILS
Positive control (reported; binding for no model): {"MM": 0.27} -> FAILS
