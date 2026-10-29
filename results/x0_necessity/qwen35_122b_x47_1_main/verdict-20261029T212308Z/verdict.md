# X0 verdict: qwen35_122b_x47_1_main

Model qwen3.5-122b-a10b (a099dee7); lens J++ `qwen3.5-122b-a10b/jpp/Salesforce-wikitext/Qwen3.5-122B-A10B_jpp_lens.pt` sha256 b771e50244c81a3f; set d1_topics_v3; predicted layer 33; non-chat read first; UNVERIFIED.

Batch 52 coverage: no prediction: coverage run on an already-scored rule (X0's rule unchanged; scenes excluded from the selection: 0).

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9917, 'PM': 0.85} (greedy text {'PP': 0.99, 'PM': 0.8533}, cand {'PP': 0.9917, 'PM': 0.845}) pass=True, eligible 410

## chat: CONFIRMED at layer 33 (lookup around, recall through); H-token: no W_E rows; split at layers [33]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 33 | PM | 200 | 0.92 | 0.56 | 0.84 | - | 0.40 [0.30, 0.49] | 0.08 [0.04, 0.13] | 0.32 [0.22, 0.41] | 0.252 | through |
| 33 | PP | 200 | 0.45 | 0.35 | 0.35 | - | 0.20 [0.11, 0.30] | 0.20 [0.10, 0.31] | 0.00 [-0.06, 0.06] | 0.252 | around |

Dictionaries at layer 33:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | signed | PM | 0.252 | 0.40 [0.30, 0.49] | 0.08 [0.04, 0.13] | 0.32 [0.22, 0.41] | through |
| jpp | 50 | signed | PM | 0.334 | 0.64 [0.54, 0.71] | 0.18 [0.11, 0.26] | 0.45 [0.35, 0.54] | through |
| jpp | 100 | signed | PM | 0.436 | 0.83 [0.74, 0.89] | 0.40 [0.32, 0.48] | 0.43 [0.32, 0.51] | through |
| jpp | 200 | signed | PM | 0.553 | 0.92 [0.85, 0.97] | 0.66 [0.60, 0.73] | 0.26 [0.20, 0.30] | through |
| jpp26_100 | 75 | slice | PM | 0.183 | 0.03 [0.00, 0.06] | 0.03 [0.01, 0.06] | 0.00 [-0.03, 0.03] | around |
| ratoms75 | 75 | scaled | PM | 0.183 | 0.02 [0.00, 0.05] | 0.03 [0.01, 0.06] | -0.02 [-0.05, 0.02] | around |
| ratoms75own | 75 | own | PM | 0.017 | 0.01 [-0.01, 0.03] | -0.01 [-0.03, 0.01] | 0.02 [0.00, 0.05] | around |
| jpp | 25 | signed | PP | 0.252 | 0.20 [0.11, 0.30] | 0.20 [0.10, 0.31] | 0.00 [-0.06, 0.06] | around |
| jpp | 50 | signed | PP | 0.334 | 0.26 [0.15, 0.37] | 0.28 [0.17, 0.39] | -0.02 [-0.09, 0.05] | around |
| jpp | 100 | signed | PP | 0.436 | 0.36 [0.26, 0.45] | 0.48 [0.38, 0.59] | -0.12 [-0.22, -0.04] | around |
| jpp | 200 | signed | PP | 0.553 | 0.58 [0.50, 0.67] | 0.76 [0.69, 0.84] | -0.18 [-0.27, -0.10] | around |
| jpp26_100 | 75 | slice | PP | 0.183 | 0.10 [0.04, 0.18] | 0.12 [0.04, 0.21] | -0.02 [-0.09, 0.04] | around |
| ratoms75 | 75 | scaled | PP | 0.183 | 0.06 [0.01, 0.11] | 0.12 [0.04, 0.21] | -0.07 [-0.13, 0.00] | around |
| ratoms75own | 75 | own | PP | 0.017 | 0.02 [-0.02, 0.07] | 0.02 [-0.02, 0.07] | 0.00 [0.00, 0.00] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.995.
Asked-first subset (descriptive): {"predicted": 33, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "no W_E rows", "split_layers": [33]}}
