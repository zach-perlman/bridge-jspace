# 49.8: DAS for the address

Batch 49, test 49.8 (jobs/c3/batch49.yaml; Q49.8, Dan: (a) · 55%; (b) · 45%). qwen3.5-9b at L12 (qwen35_9b_x49_das_pos). Pairs: 187 routes position counterfactuals (31 bridge entities; per split {'train': 112, 'test': 34, 'select': 41}); test n = 34 (6 entities); cluster bootstrap over bridge entities (10000, seed 0). UNVERIFIED.

**(d) in between** (k = 4: own-IIA 0.94, U's energy in R_pos 0.247 (k/d 0.0010), W's 0.244, the recall's cross-IIA 0.44)

As computed: every rule at k = 4 on the test entities' pairs: own-IIA = the share of test pairs whose lookup top token under R_pos is the position answer (O's locker digit at the slot the bridge's sentence occupies in S); U's energy in R_pos = ||R_pos^T U||_F^2 / rank U (x6_routes.mean_cos2; a random R: k / d); the recall's cross-IIA = the share of test pairs whose recall top token under R_pos is not O's answer (the item is the same in O and S, so any move is collateral); point estimates at the bars (EPS 1e-9), cluster-bootstrap CIs over bridge entities (10,000, seed 0) beside them; exactly one label holds: ours, else two codes, else no mediator (own-IIA < 0.6), else in between; own-IIA / the whole change's rerun position share beside; the select split reported, not used to choose k.

The whole change rerun on the test pairs: position 1.00; O unedited 0.00; the recall moved under the whole change 0.38 [0.12, 0.57], unedited 0.00.

| k | select own-IIA | test own-IIA | random R | shuffled R | own / whole | recall cross (R_pos) | recall (random R) |
|---|---|---|---|---|---|---|---|
| 2 | 1.00 | 0.94 [0.87, 1.00] | 0.00 [0.00, 0.00] | 0.29 [0.20, 0.47] | 0.94 | 0.44 [0.18, 0.69] | 0.00 [0.00, 0.00] |
| 4 (rule) | 1.00 | 0.94 [0.87, 1.00] | 0.00 [0.00, 0.00] | 0.32 [0.19, 0.52] | 0.94 | 0.44 [0.16, 0.74] | 0.00 [0.00, 0.00] |
| 8 | 1.00 | 0.94 [0.76, 1.00] | 0.00 [0.00, 0.00] | 0.32 [0.25, 0.42] | 0.94 | 0.53 [0.22, 0.78] | 0.00 [0.00, 0.00] |

The lookup's routes on the test pairs per arm (shares):

| arm | identity | position | value | original | other |
|---|---|---|---|---|---|
| R_pos_k2 | 0.06 | 0.94 | 0.00 | 0.00 | 0.00 |
| R_pos_k4 | 0.06 | 0.94 | 0.00 | 0.00 | 0.00 |
| R_pos_k8 | 0.03 | 0.94 | 0.00 | 0.00 | 0.03 |
| none | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| rand_k2 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| rand_k4 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| rand_k8 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| shuf_pos_k2 | 0.53 | 0.29 | 0.03 | 0.00 | 0.15 |
| shuf_pos_k4 | 0.56 | 0.32 | 0.00 | 0.00 | 0.12 |
| shuf_pos_k8 | 0.50 | 0.32 | 0.03 | 0.00 | 0.15 |
| whole | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |

Geometry on the test pairs (means [CI]); d = 4096, rank U = 4, rank W = 5:

| R | U's energy in R | W's energy in R | k/d | energy | in J++-25 | in J++-100 | in W_E-25 | in U | in W | in U_fit | outside (J++-25 ∪ U ∪ W_E-25) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R_pos_k2 | 0.248 | 0.244 | 0.0005 | 0.42 [0.40, 0.43] | 0.03 [0.03, 0.03] | 0.10 [0.10, 0.11] | 0.04 [0.04, 0.05] | 0.52 [0.49, 0.53] | 0.59 [0.58, 0.60] | 0.59 [0.57, 0.60] | 0.47 [0.46, 0.50] |
| R_pos_k4 | 0.247 | 0.244 | 0.0010 | 0.42 [0.41, 0.44] | 0.03 [0.03, 0.04] | 0.10 [0.10, 0.11] | 0.04 [0.04, 0.05] | 0.50 [0.47, 0.52] | 0.58 [0.56, 0.59] | 0.58 [0.56, 0.59] | 0.49 [0.47, 0.52] |
| R_pos_k8 | 0.252 | 0.252 | 0.0020 | 0.46 [0.45, 0.47] | 0.03 [0.03, 0.03] | 0.11 [0.10, 0.11] | 0.05 [0.05, 0.05] | 0.45 [0.41, 0.47] | 0.52 [0.50, 0.53] | 0.52 [0.50, 0.54] | 0.54 [0.52, 0.57] |
| rand_k2 | 0.001 | 0.000 | 0.0005 | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.01] | 0.02 [0.02, 0.02] | 0.01 [0.01, 0.01] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.99 [0.99, 0.99] |
| rand_k4 | 0.001 | 0.001 | 0.0010 | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.01] | 0.02 [0.02, 0.03] | 0.01 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.99 [0.99, 0.99] |
| rand_k8 | 0.002 | 0.002 | 0.0020 | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.01] | 0.03 [0.02, 0.03] | 0.01 [0.01, 0.01] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.99 [0.99, 0.99] |
| shuf_pos_k2 | 0.139 | 0.136 | 0.0005 | 0.32 [0.29, 0.33] | 0.03 [0.03, 0.03] | 0.09 [0.09, 0.09] | 0.04 [0.03, 0.04] | 0.36 [0.32, 0.39] | 0.41 [0.38, 0.43] | 0.42 [0.39, 0.45] | 0.63 [0.60, 0.66] |
| shuf_pos_k4 | 0.200 | 0.205 | 0.0010 | 0.40 [0.39, 0.41] | 0.03 [0.03, 0.04] | 0.10 [0.10, 0.11] | 0.04 [0.04, 0.05] | 0.37 [0.34, 0.39] | 0.45 [0.44, 0.46] | 0.45 [0.43, 0.46] | 0.61 [0.60, 0.64] |
| shuf_pos_k8 | 0.183 | 0.196 | 0.0020 | 0.37 [0.35, 0.38] | 0.03 [0.03, 0.04] | 0.11 [0.10, 0.11] | 0.04 [0.04, 0.04] | 0.33 [0.30, 0.35] | 0.40 [0.39, 0.41] | 0.39 [0.38, 0.40] | 0.65 [0.64, 0.67] |

Angles (degrees, principal): U vs W [29.604, 44.846, 68.208, 87.091] (U's energy in W 0.350, W's in U 0.280); R_pos (k = 4) vs U [40.794, 50.103, 86.561, 89.5]; vs W [35.614, 41.934, 85.025, 88.718].

Rules (fixed in advance): (a) the learned address is ours: at k = 4, >= 0.6 of U's energy lies in R_pos (random k/d ~ 0.001), own-IIA >= 0.6 and the recall's cross-IIA <= 0.1; (b) two address codes: own-IIA >= 0.6 but U's energy in R_pos <= 0.2; then report which one the writes used (47.2's slot-specific result: W) and the angle between them; (c) no low-dimensional mediator: own-IIA < 0.6; (d) in between: none of the above.
Detail: {"own_iia": 0.9411764705882353, "U_energy_in_R": 0.247057, "W_energy_in_R": 0.244467, "recall_cross_iia": 0.4411764705882353, "random_expectation": 0.000977}

Figure: qwen35_9b_x49_das_pos.png

