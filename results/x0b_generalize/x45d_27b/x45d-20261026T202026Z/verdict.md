# 45d, a pointer outside templates: x45d_27b

Model qwen3.6-27b, layer 32; the held-out half of the varied scenes (per format, the bridge items not used for the fit, x7_pcf/x45d_fit_27b). Extra loss = switches lost without the part minus without a random part of its share; cluster bootstrap over bridge items (10000 resamples, seed 0). UNVERIFIED.

Rule (fixed in advance, on the lookup with the refit basis): "Pointer elsewhere" if the refit basis gives a lookup extra loss of at least 0.2, with lower CI above 0.1, in 2 of 3 formats; "No linear pointer found" if all three formats are below 0.1 (point estimate); otherwise neither.

**Outcome: neither** (formats at >= 0.2 with lower CI > 0.1: none; below 0.1: prose, json; not tested: none). A format whose lookup has fewer than 30 switches under the whole change does not count (Dan 26 Oct ~21:20, decided after the first 45d results): none.

| format | part | reader | n | items | switched (whole) | valid | median share | Jdep | Rdep | extra loss |
|---|---|---|---|---|---|---|---|---|---|---|
| prose | the refit basis (rank 4, the other half) | lookup | 383 | 31 | 244 | True | 0.074 | 0.08 [0.04, 0.13] | 0.00 [-0.03, 0.03] | 0.08 [0.04, 0.13] |
| prose | the refit basis (rank 4, the other half) | recall | 383 | 31 | 240 | True | 0.074 | 0.03 [-0.01, 0.07] | 0.00 [-0.03, 0.04] | 0.03 [-0.02, 0.07] |
| prose | U (simple scenes, not refit) | lookup | 383 | 31 | 244 | True | 0.048 | 0.07 [0.04, 0.11] | 0.00 [-0.02, 0.03] | 0.07 [0.05, 0.10] |
| prose | U (simple scenes, not refit) | recall | 383 | 31 | 240 | True | 0.048 | 0.02 [-0.02, 0.07] | 0.00 [-0.03, 0.04] | 0.02 [-0.02, 0.07] |
| json | the refit basis (rank 4, the other half) | lookup | 143 | 14 | 97 | True | 0.061 | 0.07 [0.03, 0.11] | -0.02 [-0.05, 0.00] | 0.09 [0.05, 0.12] |
| json | the refit basis (rank 4, the other half) | recall | 143 | 14 | 108 | True | 0.061 | 0.04 [-0.04, 0.12] | 0.01 [-0.03, 0.06] | 0.03 [-0.03, 0.09] |
| json | U (simple scenes, not refit) | lookup | 143 | 14 | 97 | True | 0.027 | 0.01 [-0.03, 0.04] | -0.01 [-0.03, 0.00] | 0.02 [0.00, 0.04] |
| json | U (simple scenes, not refit) | recall | 143 | 14 | 108 | True | 0.027 | 0.02 [0.00, 0.05] | -0.01 [-0.03, 0.00] | 0.03 [0.00, 0.07] |
| table | the refit basis (rank 4, the other half) | lookup | 322 | 30 | 229 | True | 0.054 | 0.14 [0.10, 0.18] | 0.01 [-0.01, 0.04] | 0.13 [0.09, 0.17] |
| table | the refit basis (rank 4, the other half) | recall | 322 | 30 | 232 | True | 0.054 | 0.07 [0.03, 0.13] | 0.04 [0.01, 0.08] | 0.03 [-0.01, 0.08] |
| table | U (simple scenes, not refit) | lookup | 322 | 30 | 229 | True | 0.025 | 0.01 [-0.01, 0.03] | -0.00 [-0.01, 0.00] | 0.01 [0.00, 0.03] |
| table | U (simple scenes, not refit) | recall | 322 | 30 | 232 | True | 0.025 | 0.01 [-0.03, 0.05] | -0.00 [-0.02, 0.02] | 0.02 [-0.02, 0.05] |

valid (descriptive, not in the rule): S_whole >= 0.30 and >= 30 switched by the whole change. U is the comparison part (simple scenes, not refit); the rule reads only the refit basis on the lookup.
