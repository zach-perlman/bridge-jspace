# 45d, a pointer outside templates: muse30b_x45d

Model muse-glimmer-30b, layer 26; the held-out half of the varied scenes (per format, the bridge items not used for the fit, x7_pcf/muse30b_x45d_fit). Extra loss = switches lost without the part minus without a random part of its share; cluster bootstrap over bridge items (10000 resamples, seed 0). UNVERIFIED.

Rule (fixed in advance, on the lookup with the refit basis): "Pointer elsewhere" if the refit basis gives a lookup extra loss of at least 0.2, with lower CI above 0.1, in 2 of 3 formats; "No linear pointer found" if all three formats are below 0.1 (point estimate); otherwise neither.

**Outcome: pointer elsewhere** (formats at >= 0.2 with lower CI > 0.1: prose, json, table; below 0.1: none; not tested: none).

| format | part | reader | n | items | switched (whole) | valid | median share | Jdep | Rdep | extra loss |
|---|---|---|---|---|---|---|---|---|---|---|
| prose | the refit basis (rank 4, the other half) | lookup | 270 | 28 | 132 | True | 0.075 | 0.17 [0.09, 0.24] | -0.06 [-0.12, -0.01] | 0.23 [0.16, 0.31] |
| prose | the refit basis (rank 4, the other half) | recall | 270 | 28 | 159 | True | 0.075 | -0.08 [-0.13, -0.01] | -0.03 [-0.06, 0.02] | -0.05 [-0.11, 0.01] |
| prose | U (simple scenes, not refit) | lookup | 270 | 28 | 132 | True | 0.040 | 0.11 [0.03, 0.19] | -0.07 [-0.12, -0.02] | 0.18 [0.11, 0.25] |
| prose | U (simple scenes, not refit) | recall | 270 | 28 | 159 | True | 0.040 | -0.01 [-0.06, 0.05] | -0.04 [-0.07, 0.00] | 0.03 [-0.02, 0.08] |
| json | the refit basis (rank 4, the other half) | lookup | 89 | 13 | 29 | False | 0.057 | 0.31 [0.18, 0.45] | -0.07 [-0.24, 0.06] | 0.38 [0.16, 0.65] |
| json | the refit basis (rank 4, the other half) | recall | 89 | 13 | 12 | False | 0.057 | -0.17 [-0.54, 0.20] | 0.08 [0.00, 0.38] | -0.25 [-0.70, 0.12] |
| json | U (simple scenes, not refit) | lookup | 89 | 13 | 29 | False | 0.023 | 0.17 [0.00, 0.37] | -0.03 [-0.19, 0.08] | 0.21 [0.05, 0.40] |
| json | U (simple scenes, not refit) | recall | 89 | 13 | 12 | False | 0.023 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| table | the refit basis (rank 4, the other half) | lookup | 238 | 24 | 79 | True | 0.037 | 0.42 [0.31, 0.53] | -0.05 [-0.13, 0.03] | 0.47 [0.34, 0.60] |
| table | the refit basis (rank 4, the other half) | recall | 238 | 24 | 89 | True | 0.037 | 0.08 [-0.04, 0.20] | -0.08 [-0.15, -0.01] | 0.16 [0.06, 0.28] |
| table | U (simple scenes, not refit) | lookup | 238 | 24 | 79 | True | 0.016 | 0.06 [-0.02, 0.17] | -0.04 [-0.08, 0.00] | 0.10 [0.03, 0.20] |
| table | U (simple scenes, not refit) | recall | 238 | 24 | 89 | True | 0.016 | -0.08 [-0.17, 0.00] | -0.04 [-0.10, 0.00] | -0.03 [-0.10, 0.02] |

valid (descriptive, not in the rule): S_whole >= 0.30 and >= 30 switched by the whole change. U is the comparison part (simple scenes, not refit); the rule reads only the refit basis on the lookup.
