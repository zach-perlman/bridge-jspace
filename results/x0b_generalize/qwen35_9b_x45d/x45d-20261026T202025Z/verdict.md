# 45d, a pointer outside templates: qwen35_9b_x45d

Model qwen3.5-9b, layer 12; the held-out half of the varied scenes (per format, the bridge items not used for the fit, x7_pcf/qwen35_9b_x45d_fit). Extra loss = switches lost without the part minus without a random part of its share; cluster bootstrap over bridge items (10000 resamples, seed 0). UNVERIFIED.

Rule (fixed in advance, on the lookup with the refit basis): "Pointer elsewhere" if the refit basis gives a lookup extra loss of at least 0.2, with lower CI above 0.1, in 2 of 3 formats; "No linear pointer found" if all three formats are below 0.1 (point estimate); otherwise neither.

**Outcome: pointer elsewhere** (formats at >= 0.2 with lower CI > 0.1: prose, json; below 0.1: none; not tested: none). A format whose lookup has fewer than 30 switches under the whole change does not count (Dan 26 Oct ~21:20, decided after the first 45d results): none.

| format | part | reader | n | items | switched (whole) | valid | median share | Jdep | Rdep | extra loss |
|---|---|---|---|---|---|---|---|---|---|---|
| prose | the refit basis (rank 4, the other half) | lookup | 223 | 24 | 167 | True | 0.078 | 0.24 [0.16, 0.32] | 0.00 [-0.02, 0.02] | 0.24 [0.16, 0.32] |
| prose | the refit basis (rank 4, the other half) | recall | 223 | 24 | 217 | True | 0.078 | 0.06 [0.02, 0.10] | 0.01 [0.00, 0.03] | 0.05 [0.02, 0.08] |
| prose | U (simple scenes, not refit) | lookup | 223 | 24 | 167 | True | 0.048 | 0.17 [0.12, 0.24] | 0.00 [0.00, 0.00] | 0.17 [0.12, 0.24] |
| prose | U (simple scenes, not refit) | recall | 223 | 24 | 217 | True | 0.048 | 0.05 [0.02, 0.09] | 0.01 [0.00, 0.03] | 0.04 [0.01, 0.07] |
| json | the refit basis (rank 4, the other half) | lookup | 70 | 12 | 51 | True | 0.045 | 0.20 [0.09, 0.24] | -0.04 [-0.12, 0.00] | 0.24 [0.16, 0.30] |
| json | the refit basis (rank 4, the other half) | recall | 70 | 12 | 62 | True | 0.045 | 0.05 [-0.03, 0.14] | 0.00 [0.00, 0.00] | 0.05 [-0.03, 0.14] |
| json | U (simple scenes, not refit) | lookup | 70 | 12 | 51 | True | 0.030 | 0.06 [-0.03, 0.12] | -0.02 [-0.07, 0.00] | 0.08 [-0.03, 0.17] |
| json | U (simple scenes, not refit) | recall | 70 | 12 | 62 | True | 0.030 | 0.03 [-0.02, 0.11] | 0.02 [0.00, 0.06] | 0.02 [-0.05, 0.10] |
| table | the refit basis (rank 4, the other half) | lookup | 138 | 17 | 114 | True | 0.040 | 0.18 [0.13, 0.24] | 0.00 [0.00, 0.00] | 0.18 [0.13, 0.24] |
| table | the refit basis (rank 4, the other half) | recall | 138 | 17 | 132 | True | 0.040 | 0.04 [0.00, 0.07] | 0.00 [0.00, 0.00] | 0.04 [0.00, 0.07] |
| table | U (simple scenes, not refit) | lookup | 138 | 17 | 114 | True | 0.027 | 0.08 [0.03, 0.13] | -0.01 [-0.04, 0.00] | 0.09 [0.04, 0.14] |
| table | U (simple scenes, not refit) | recall | 138 | 17 | 132 | True | 0.027 | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] |

valid (descriptive, not in the rule): S_whole >= 0.30 and >= 30 switched by the whole change. U is the comparison part (simple scenes, not refit); the rule reads only the refit basis on the lookup.
