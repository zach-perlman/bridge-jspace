# X0 verdict: nem35l_x52_x47_1_main

Model nemotron-3.5-lightning (a9904d24); lens J++ `cache/nemotron-3.5-lightning/lenses/jpp/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16_jpp_lens.pt` sha256 3306b6e4f0f4ba03; set d1_topics_v3; predicted layer 14; non-chat read first; UNVERIFIED.

Batch 52 coverage: no prediction: coverage run on an already-scored rule (X0's rule unchanged; scenes excluded from the selection: 60).

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9574, 'PM': 0.8159} (greedy text {'PP': 0.9574, 'PM': 0.8178}, cand {'PP': 0.9554, 'PM': 0.814}) pass=True, eligible 315

## chat: CONFIRMED at layer 14 (lookup around, recall through); H-token: no W_E rows; split at layers [14]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 | PM | 200 | 0.95 | 0.56 | 0.89 | - | 0.42 [0.32, 0.51] | 0.07 [0.03, 0.11] | 0.35 [0.26, 0.45] | 0.270 | through |
| 14 | PP | 200 | 0.46 | 0.38 | 0.38 | - | 0.18 [0.12, 0.25] | 0.17 [0.11, 0.24] | 0.01 [-0.03, 0.05] | 0.270 | around |

Dictionaries at layer 14:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | signed | PM | 0.270 | 0.42 [0.32, 0.51] | 0.07 [0.03, 0.11] | 0.35 [0.26, 0.45] | through |
| jpp | 50 | signed | PM | 0.366 | 0.68 [0.60, 0.76] | 0.17 [0.11, 0.22] | 0.51 [0.45, 0.57] | through |
| jpp | 100 | signed | PM | 0.470 | 0.84 [0.78, 0.90] | 0.47 [0.37, 0.56] | 0.37 [0.29, 0.46] | through |
| jpp | 200 | signed | PM | 0.581 | 0.93 [0.89, 0.96] | 0.80 [0.71, 0.89] | 0.13 [0.06, 0.20] | mixed |
| jpp26_100 | 75 | slice | PM | 0.199 | 0.04 [0.02, 0.07] | 0.04 [0.01, 0.06] | 0.01 [-0.02, 0.04] | around |
| ratoms75 | 75 | scaled | PM | 0.199 | 0.02 [0.00, 0.03] | 0.04 [0.01, 0.06] | -0.02 [-0.05, 0.01] | around |
| ratoms75own | 75 | own | PM | 0.029 | 0.02 [0.00, 0.03] | 0.00 [-0.01, 0.01] | 0.02 [0.00, 0.03] | around |
| jpp | 25 | signed | PP | 0.270 | 0.18 [0.12, 0.25] | 0.17 [0.11, 0.24] | 0.01 [-0.03, 0.05] | around |
| jpp | 50 | signed | PP | 0.366 | 0.26 [0.18, 0.35] | 0.26 [0.17, 0.35] | 0.00 [-0.09, 0.09] | around |
| jpp | 100 | signed | PP | 0.470 | 0.43 [0.34, 0.53] | 0.57 [0.47, 0.67] | -0.13 [-0.21, -0.05] | around |
| jpp | 200 | signed | PP | 0.581 | 0.61 [0.50, 0.72] | 0.78 [0.69, 0.88] | -0.17 [-0.29, -0.07] | around |
| jpp26_100 | 75 | slice | PP | 0.199 | 0.16 [0.09, 0.25] | 0.10 [0.03, 0.17] | 0.07 [0.00, 0.13] | around |
| ratoms75 | 75 | scaled | PP | 0.199 | 0.08 [0.02, 0.13] | 0.10 [0.03, 0.17] | -0.02 [-0.10, 0.04] | around |
| ratoms75own | 75 | own | PP | 0.029 | 0.02 [-0.02, 0.07] | 0.01 [-0.03, 0.05] | 0.01 [0.00, 0.04] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9925.
Asked-first subset (descriptive): {"predicted": 14, "chat": {"verdict": "can't tell", "lookup_label": "can't tell", "recall_label": "through", "h_token": "no W_E rows", "split_layers": []}}
