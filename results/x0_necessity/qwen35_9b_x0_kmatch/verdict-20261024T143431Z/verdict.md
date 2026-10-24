# X0 verdict: qwen35_9b_x0_kmatch

Model qwen3.5-9b (c2022362); lens J++ `qwen3.5-9b/jpp/Salesforce-wikitext/Qwen3.5-9B_jpp_lens.pt` sha256 8cda12f7ddf11e70; set d1_topics_v3; predicted layer 12; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.95, 'PM': 0.8683} (greedy text {'PP': 0.95, 'PM': 0.87}, cand {'PP': 0.9417, 'PM': 0.865}) pass=True, eligible 408

## chat: CONFIRMED at layer 12 (lookup around, recall through); H-token: neither: the lookup is around W_E as well as J++; split at layers [12]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 12 | PM | 200 | 0.98 | 0.46 | 0.95 | 0.98 | 0.53 [0.45, 0.61] | 0.04 [0.01, 0.07] | 0.50 [0.41, 0.57] | 0.233 | through |
| 12 | PP | 200 | 0.52 | 0.41 | 0.40 | 0.46 | 0.21 [0.15, 0.28] | 0.23 [0.15, 0.31] | -0.02 [-0.07, 0.04] | 0.233 | around |

Dictionaries at layer 12:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | nonneg | PM | 0.137 | 0.05 [0.02, 0.08] | 0.01 [0.00, 0.02] | 0.04 [0.02, 0.07] | around |
| jpp | 25 | signed | PM | 0.233 | 0.53 [0.45, 0.61] | 0.04 [0.01, 0.07] | 0.50 [0.41, 0.57] | through |
| jpp | 50 | signed | PM | 0.329 | 0.74 [0.65, 0.81] | 0.12 [0.07, 0.19] | 0.62 [0.50, 0.71] | through |
| jpp | 100 | signed | PM | 0.440 | 0.85 [0.77, 0.90] | 0.38 [0.31, 0.46] | 0.47 [0.35, 0.55] | through |
| jpp | 200 | signed | PM | 0.563 | 0.96 [0.94, 0.99] | 0.78 [0.70, 0.86] | 0.18 [0.11, 0.26] | mixed |
| rand | 25 | signed | PM | 0.101 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | around |
| rand | 50 | signed | PM | 0.184 | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | around |
| rand | 100 | signed | PM | 0.323 | 0.07 [0.04, 0.11] | 0.09 [0.05, 0.13] | -0.02 [-0.04, 0.01] | around |
| rand | 200 | signed | PM | 0.531 | 0.72 [0.62, 0.81] | 0.73 [0.65, 0.81] | -0.02 [-0.06, 0.03] | around |
| we | 25 | signed | PM | 0.109 | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | around |
| we | 50 | signed | PM | 0.193 | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.03] | -0.01 [-0.02, 0.00] | around |
| we | 100 | signed | PM | 0.329 | 0.09 [0.05, 0.15] | 0.10 [0.06, 0.15] | -0.01 [-0.04, 0.03] | around |
| we | 200 | signed | PM | 0.531 | 0.77 [0.69, 0.84] | 0.72 [0.63, 0.80] | 0.06 [0.01, 0.10] | around |
| wu | 25 | signed | PM | 0.090 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | around |
| wu | 50 | signed | PM | 0.162 | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | around |
| wu | 100 | signed | PM | 0.284 | 0.02 [-0.00, 0.05] | 0.05 [0.02, 0.08] | -0.03 [-0.05, 0.00] | around |
| wu | 200 | signed | PM | 0.473 | 0.34 [0.25, 0.45] | 0.46 [0.35, 0.58] | -0.12 [-0.18, -0.05] | around |
| jpp | 25 | nonneg | PP | 0.137 | 0.09 [0.02, 0.15] | 0.12 [0.05, 0.18] | -0.03 [-0.09, 0.03] | around |
| jpp | 25 | signed | PP | 0.233 | 0.21 [0.15, 0.28] | 0.23 [0.15, 0.31] | -0.02 [-0.07, 0.04] | around |
| jpp | 50 | signed | PP | 0.329 | 0.31 [0.21, 0.40] | 0.34 [0.25, 0.42] | -0.03 [-0.10, 0.04] | around |
| jpp | 100 | signed | PP | 0.440 | 0.48 [0.37, 0.57] | 0.55 [0.47, 0.62] | -0.08 [-0.15, -0.01] | around |
| jpp | 200 | signed | PP | 0.563 | 0.75 [0.69, 0.81] | 0.92 [0.87, 0.97] | -0.17 [-0.25, -0.11] | around |
| rand | 25 | signed | PP | 0.101 | 0.11 [0.05, 0.17] | 0.08 [0.02, 0.14] | 0.03 [-0.01, 0.08] | around |
| rand | 50 | signed | PP | 0.184 | 0.21 [0.13, 0.29] | 0.20 [0.11, 0.29] | 0.01 [-0.03, 0.05] | around |
| rand | 100 | signed | PP | 0.323 | 0.38 [0.28, 0.46] | 0.34 [0.25, 0.42] | 0.04 [0.01, 0.07] | around |
| rand | 200 | signed | PP | 0.531 | 0.89 [0.83, 0.95] | 0.90 [0.83, 0.96] | -0.01 [-0.06, 0.04] | around |
| we | 25 | signed | PP | 0.109 | 0.12 [0.06, 0.17] | 0.06 [0.01, 0.12] | 0.06 [0.01, 0.11] | around |
| we | 50 | signed | PP | 0.193 | 0.17 [0.11, 0.23] | 0.18 [0.10, 0.28] | -0.01 [-0.07, 0.05] | around |
| we | 100 | signed | PP | 0.329 | 0.34 [0.25, 0.42] | 0.36 [0.26, 0.44] | -0.02 [-0.06, 0.03] | around |
| we | 200 | signed | PP | 0.531 | 0.85 [0.78, 0.92] | 0.89 [0.82, 0.95] | -0.04 [-0.08, 0.00] | around |
| wu | 25 | signed | PP | 0.090 | 0.05 [0.00, 0.10] | 0.06 [0.00, 0.12] | -0.01 [-0.06, 0.04] | around |
| wu | 50 | signed | PP | 0.162 | 0.10 [0.03, 0.16] | 0.17 [0.09, 0.26] | -0.08 [-0.15, -0.01] | around |
| wu | 100 | signed | PP | 0.284 | 0.28 [0.17, 0.38] | 0.30 [0.21, 0.38] | -0.02 [-0.08, 0.04] | around |
| wu | 200 | signed | PP | 0.473 | 0.55 [0.46, 0.64] | 0.72 [0.65, 0.79] | -0.17 [-0.24, -0.10] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.985.
Asked-first subset (descriptive): {"predicted": 12, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "mixed", "split_layers": [12]}}
