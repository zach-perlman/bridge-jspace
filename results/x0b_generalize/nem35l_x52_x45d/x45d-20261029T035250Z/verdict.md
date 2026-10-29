# 45d, a pointer outside templates: nem35l_x52_x45d

Model nemotron-3.5-lightning, layer 14; the held-out half of the varied scenes (per format, the bridge items not used for the fit, x7_pcf/nem35l_x52_x45d_fit). Extra loss = switches lost without the part minus without a random part of its share; cluster bootstrap over bridge items (10000 resamples, seed 0). UNVERIFIED.

Rule (fixed in advance, on the lookup with the refit basis): "Pointer elsewhere" if the refit basis gives a lookup extra loss of at least 0.2, with lower CI above 0.1, in 2 of 3 formats; "No linear pointer found" if all three formats are below 0.1 (point estimate); otherwise neither.

**Outcome: pointer elsewhere** (formats at >= 0.2 with lower CI > 0.1: json, table; below 0.1: none; not tested: none). A format whose lookup has fewer than 30 switches under the whole change does not count (Dan 26 Oct ~21:20, decided after the first 45d results): none.

| format | part | reader | n | items | switched (whole) | valid | median share | Jdep | Rdep | extra loss |
|---|---|---|---|---|---|---|---|---|---|---|
| prose | the refit basis (rank 4, the other half) | lookup | 191 | 20 | 140 | True | 0.069 | 0.17 [0.13, 0.22] | 0.01 [0.00, 0.03] | 0.16 [0.11, 0.21] |
| prose | the refit basis (rank 4, the other half) | recall | 191 | 20 | 186 | True | 0.069 | 0.01 [0.00, 0.04] | -0.01 [-0.03, 0.00] | 0.02 [0.00, 0.06] |
| prose | U (simple scenes, not refit) | lookup | 191 | 20 | 140 | True | 0.051 | 0.14 [0.09, 0.22] | 0.00 [0.00, 0.00] | 0.14 [0.09, 0.22] |
| prose | U (simple scenes, not refit) | recall | 191 | 20 | 186 | True | 0.051 | 0.01 [-0.02, 0.04] | 0.00 [0.00, 0.00] | 0.01 [-0.02, 0.04] |
| json | the refit basis (rank 4, the other half) | lookup | 40 | 4 | 31 | True | 0.076 | 0.29 [0.23, 0.40] | 0.03 [0.00, 0.07] | 0.26 [0.20, 0.40] |
| json | the refit basis (rank 4, the other half) | recall | 40 | 4 | 40 | True | 0.076 | 0.03 [0.00, 0.05] | 0.00 [0.00, 0.00] | 0.03 [0.00, 0.05] |
| json | U (simple scenes, not refit) | lookup | 40 | 4 | 31 | True | 0.052 | 0.03 [-0.20, 0.15] | 0.03 [0.00, 0.07] | 0.00 [-0.20, 0.12] |
| json | U (simple scenes, not refit) | recall | 40 | 4 | 40 | True | 0.052 | 0.03 [0.00, 0.05] | 0.00 [0.00, 0.00] | 0.03 [0.00, 0.05] |
| table | the refit basis (rank 4, the other half) | lookup | 187 | 13 | 146 | True | 0.053 | 0.28 [0.21, 0.37] | 0.03 [0.00, 0.06] | 0.25 [0.19, 0.32] |
| table | the refit basis (rank 4, the other half) | recall | 187 | 13 | 179 | True | 0.053 | 0.02 [-0.01, 0.07] | 0.00 [-0.02, 0.01] | 0.02 [-0.01, 0.08] |
| table | U (simple scenes, not refit) | lookup | 187 | 13 | 146 | True | 0.049 | 0.06 [0.02, 0.11] | 0.02 [0.00, 0.04] | 0.04 [-0.01, 0.08] |
| table | U (simple scenes, not refit) | recall | 187 | 13 | 179 | True | 0.049 | 0.01 [-0.01, 0.02] | -0.01 [-0.02, 0.00] | 0.01 [0.00, 0.02] |

valid (descriptive, not in the rule): S_whole >= 0.30 and >= 30 switched by the whole change. U is the comparison part (simple scenes, not refit); the rule reads only the refit basis on the lookup.
