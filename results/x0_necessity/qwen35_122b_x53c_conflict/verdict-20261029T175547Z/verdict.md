# X0 verdict: qwen35_122b_x53c_conflict

Model qwen3.5-122b-a10b (a099dee7); lens J++ `qwen3.5-122b-a10b/jpp/Salesforce-wikitext/Qwen3.5-122B-A10B_jpp_lens.pt` sha256 b771e50244c81a3f; set d1_topics_v3; predicted layer 33; non-chat read first; UNVERIFIED.

Batch 52 coverage: no prediction: coverage run on an already-scored rule (X0's rule unchanged; scenes excluded from the selection: 0).

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9917, 'PM': 0.85} (greedy text {'PP': 0.99, 'PM': 0.8533}, cand {'PP': 0.9917, 'PM': 0.845}) pass=True, eligible 410

## chat: CONFIRMED at layer 33 (lookup around, recall through); H-token: no W_E rows; split at layers [33]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PM | 200 | 0.97 | 0.97 | 0.97 | - | 0.00 [-0.01, 0.02] | 0.00 [-0.01, 0.01] | 0.00 [-0.02, 0.02] | 0.131 | around |
| 1 | PP | 200 | 0.99 | 0.99 | 0.99 | - | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | -0.01 [-0.02, 0.00] | 0.131 | around |
| 5 | PM | 200 | 0.97 | 0.81 | 0.96 | - | 0.17 [0.10, 0.24] | 0.01 [-0.01, 0.04] | 0.16 [0.09, 0.23] | 0.234 | mixed |
| 5 | PP | 200 | 0.99 | 0.71 | 0.99 | - | 0.28 [0.21, 0.37] | -0.01 [-0.02, 0.00] | 0.29 [0.21, 0.37] | 0.234 | mixed |
| 9 | PM | 200 | 0.97 | 0.81 | 0.97 | - | 0.17 [0.12, 0.23] | 0.00 [-0.01, 0.01] | 0.17 [0.12, 0.23] | 0.221 | mixed |
| 9 | PP | 200 | 0.99 | 0.63 | 0.99 | - | 0.36 [0.29, 0.44] | -0.01 [-0.02, 0.00] | 0.37 [0.30, 0.45] | 0.221 | through |
| 13 | PM | 200 | 0.98 | 0.72 | 0.98 | - | 0.26 [0.19, 0.33] | 0.00 [-0.02, 0.02] | 0.26 [0.19, 0.33] | 0.210 | mixed |
| 13 | PP | 200 | 0.98 | 0.47 | 0.94 | - | 0.52 [0.43, 0.60] | 0.04 [0.01, 0.07] | 0.47 [0.40, 0.56] | 0.210 | through |
| 17 | PM | 200 | 0.97 | 0.82 | 0.94 | - | 0.16 [0.09, 0.22] | 0.04 [0.01, 0.08] | 0.12 [0.07, 0.16] | 0.211 | mixed |
| 17 | PP | 200 | 0.97 | 0.54 | 0.90 | - | 0.45 [0.37, 0.53] | 0.08 [0.04, 0.12] | 0.37 [0.29, 0.45] | 0.211 | through |
| 21 | PM | 200 | 0.95 | 0.64 | 0.94 | - | 0.33 [0.25, 0.40] | 0.02 [-0.01, 0.04] | 0.31 [0.24, 0.38] | 0.248 | through |
| 21 | PP | 200 | 0.92 | 0.42 | 0.76 | - | 0.54 [0.47, 0.62] | 0.17 [0.11, 0.25] | 0.37 [0.31, 0.43] | 0.248 | through |
| 25 | PM | 200 | 0.96 | 0.43 | 0.92 | - | 0.55 [0.44, 0.64] | 0.05 [0.01, 0.08] | 0.50 [0.39, 0.60] | 0.279 | through |
| 25 | PP | 200 | 0.83 | 0.31 | 0.64 | - | 0.63 [0.55, 0.69] | 0.23 [0.17, 0.31] | 0.40 [0.30, 0.47] | 0.279 | through |
| 29 | PM | 200 | 0.93 | 0.33 | 0.86 | - | 0.65 [0.54, 0.74] | 0.08 [0.03, 0.13] | 0.57 [0.46, 0.67] | 0.320 | through |
| 29 | PP | 200 | 0.69 | 0.26 | 0.53 | - | 0.62 [0.53, 0.70] | 0.23 [0.16, 0.29] | 0.39 [0.30, 0.48] | 0.320 | through |
| 33 | PM | 200 | 0.92 | 0.58 | 0.83 | - | 0.37 [0.26, 0.47] | 0.09 [0.04, 0.15] | 0.28 [0.17, 0.39] | 0.252 | through |
| 33 | PP | 200 | 0.45 | 0.37 | 0.36 | - | 0.18 [0.08, 0.28] | 0.20 [0.10, 0.31] | -0.02 [-0.11, 0.06] | 0.252 | around |
| 37 | PM | 200 | 0.79 | 0.47 | 0.77 | - | 0.39 [0.29, 0.50] | 0.03 [-0.02, 0.08] | 0.37 [0.25, 0.48] | 0.182 | through |
| 37 | PP | 200 | 0.26 | 0.27 | 0.27 | - | -0.04 [-0.13, 0.03] | -0.04 [-0.15, 0.07] | 0.00 [-0.12, 0.10] | 0.182 | can't tell |
| 41 | PM | 200 | 0.50 | 0.23 | 0.47 | - | 0.53 [0.38, 0.69] | 0.05 [-0.05, 0.13] | 0.48 [0.35, 0.63] | 0.186 | through |
| 41 | PP | 200 | 0.01 | 0.01 | 0.01 | - | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.186 | can't tell |
| 45 | PM | 200 | 0.01 | 0.01 | 0.01 | - | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.251 | can't tell |
| 45 | PP | 200 | 0.00 | 0.00 | 0.01 | - | nan [nan, nan] | nan [nan, nan] | nan [nan, nan] | 0.251 | can't tell |

Dictionaries at layer 33:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | signed | PM | 0.252 | 0.37 [0.26, 0.47] | 0.09 [0.04, 0.15] | 0.28 [0.17, 0.39] | through |
| jpp | 25 | signed | PP | 0.252 | 0.18 [0.08, 0.28] | 0.20 [0.10, 0.31] | -0.02 [-0.11, 0.06] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9977.
Asked-first subset (descriptive): {"predicted": 33, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "no W_E rows", "split_layers": [33]}}
