# C2-graded / gptoss20_wm2_full2_v1 (rule fixed in scripts/c2_graded.py; this output from commit b8eb92f)

Best gated flips to C's answer % [95% CI over bridge entities] (write, positions, layer, strength).

| family | own lens direction (add, swap), question/final (THE RULE) | own direction, final only | transplant, question/final | transplant at 1x | difference of means, question/final | any lens write, any positions |
|---|---|---|---|---|---|---|
| CM | 13 [0-25] (lens_add, final, 13, 0.4) | 13 [0-25] (lens_add, final, 13, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 13 [0-25] (lens_add, final, 13, 0.4) |
| CP | 4 [0-12] (lens_add, question, 10, 0.1) | 4 [0-12] (lens_add, final, 12, 0.4) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 4 [0-12] (lens_add, question, 10, 0.1) |
| M->M | 27 [0-62] (lens_add, final, 15, 0.2) | 27 [0-62] (lens_add, final, 15, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 27 [0-62] (lens_add, final, 15, 0.2) |
| M->P | 0 [0-0] (lens_add, question, 10, 0.05) | 0 [0-0] (lens_add, final, 10, 0.05) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 0 [0-0] (lens_add, question, 10, 0.05) |
| P->M | 4 [0-13] (lens_add, question, 12, 0.4) | 4 [0-13] (lens_add, final, 11, 0.2) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 4 [0-13] (lens_add, question, 12, 0.4) |
| P->P | 16 [0-29] (lens_add, question, 12, 0.8) | 4 [0-12] (lens_add, final, 12, 0.8) | - (no gated cell) | - (no gated cell) | - (no gated cell) | 16 [0-29] (lens_add, question, 12, 0.8) |

Rule: M->M best 27% vs M->P best 0%: >= 3x yes, >= +30 points no, intervals apart yes -> C2-graded FAILS

Ceiling and cross-validated estimates (best cell chosen on half the bridge entities, scored on the other half):

| family | copy ceiling, question/final | own direction (CV) | relative to ceiling | transplant (CV) | dom (CV) |
|---|---|---|---|---|---|
| CM | 4 | 4 | 83 | - | - |
| CP | 4 | 0 | 0 | - | - |
| M->M | 18 | 10 | 56 | - | - |
| M->P | 0 | 0 | - | - | - |
| P->M | 12 | 0 | 0 | - | - |
| P->P | 4 | 11 | 100 | - | - |

C2-relative: ceilings {"MP": 0, "MM": 0.18}, relative {"MP": null, "MM": 0.56} -> inconclusive: sites carry the bridge only partly
Positive control (reported; binding for no model): {"MM": 0.27} -> FAILS
