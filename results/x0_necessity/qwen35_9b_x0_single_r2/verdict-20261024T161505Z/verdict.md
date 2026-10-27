# X0 verdict: qwen35_9b_x0_single_r2

Model qwen3.5-9b (c2022362); lens J++ `qwen3.5-9b/jpp/Salesforce-wikitext/Qwen3.5-9B_jpp_lens.pt` sha256 8cda12f7ddf11e70; set d1_topics_v3; predicted layer 12; non-chat read first; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.95, 'PM': 0.8683} (greedy text {'PP': 0.95, 'PM': 0.87}, cand {'PP': 0.9417, 'PM': 0.865}) pass=True, eligible 412

## chat: CONFIRMED at layer 12 (lookup around, recall through); H-token: neither: the lookup is around W_E as well as J++; split at layers [12, 14]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10 | PM | 200 | 0.97 | 0.47 | 0.95 | 0.97 | 0.52 [0.44, 0.60] | 0.02 [-0.01, 0.05] | 0.49 [0.41, 0.58] | 0.247 | through |
| 10 | PP | 200 | 0.58 | 0.41 | 0.53 | 0.56 | 0.30 [0.21, 0.38] | 0.09 [0.03, 0.15] | 0.21 [0.12, 0.29] | 0.247 | mixed |
| 12 | PM | 200 | 0.95 | 0.56 | 0.92 | 0.96 | 0.41 [0.34, 0.48] | 0.04 [0.02, 0.07] | 0.37 [0.29, 0.43] | 0.186 | through |
| 12 | PP | 200 | 0.53 | 0.48 | 0.47 | 0.52 | 0.09 [0.05, 0.14] | 0.11 [0.06, 0.17] | -0.02 [-0.05, 0.02] | 0.186 | around |
| 14 | PM | 200 | 0.91 | 0.40 | 0.91 | 0.90 | 0.57 [0.49, 0.64] | 0.01 [-0.03, 0.05] | 0.56 [0.48, 0.64] | 0.167 | through |
| 14 | PP | 200 | 0.44 | 0.42 | 0.41 | 0.42 | 0.03 [-0.02, 0.09] | 0.06 [0.00, 0.11] | -0.02 [-0.09, 0.04] | 0.167 | around |

Dictionaries at layer 12:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | nonneg | PM | 0.110 | 0.03 [0.00, 0.06] | 0.00 [-0.02, 0.02] | 0.03 [0.00, 0.06] | around |
| jpp | 25 | signed | PM | 0.186 | 0.41 [0.34, 0.48] | 0.04 [0.02, 0.07] | 0.37 [0.29, 0.43] | through |
| jpp | 50 | signed | PM | 0.269 | 0.57 [0.47, 0.64] | 0.07 [0.03, 0.12] | 0.49 [0.39, 0.57] | through |
| jpp | 100 | signed | PM | 0.373 | 0.72 [0.64, 0.79] | 0.24 [0.18, 0.29] | 0.49 [0.40, 0.56] | through |
| rand | 25 | signed | PM | 0.102 | -0.01 [-0.03, 0.01] | -0.01 [-0.03, 0.01] | 0.00 [-0.02, 0.01] | around |
| we | 25 | signed | PM | 0.107 | 0.00 [-0.02, 0.01] | -0.01 [-0.03, 0.01] | 0.01 [-0.01, 0.02] | around |
| wu | 25 | signed | PM | 0.090 | -0.01 [-0.03, 0.01] | 0.00 [-0.02, 0.02] | -0.01 [-0.03, 0.01] | around |
| jpp | 25 | nonneg | PP | 0.110 | 0.03 [-0.02, 0.08] | 0.08 [0.02, 0.13] | -0.05 [-0.10, 0.00] | around |
| jpp | 25 | signed | PP | 0.186 | 0.09 [0.05, 0.14] | 0.11 [0.06, 0.17] | -0.02 [-0.05, 0.02] | around |
| jpp | 50 | signed | PP | 0.269 | 0.16 [0.10, 0.22] | 0.18 [0.10, 0.26] | -0.02 [-0.06, 0.02] | around |
| jpp | 100 | signed | PP | 0.373 | 0.35 [0.26, 0.44] | 0.23 [0.15, 0.31] | 0.12 [0.05, 0.20] | mixed |
| rand | 25 | signed | PP | 0.102 | 0.03 [-0.01, 0.07] | 0.06 [0.02, 0.10] | -0.03 [-0.06, 0.00] | around |
| we | 25 | signed | PP | 0.107 | 0.08 [0.04, 0.14] | 0.05 [0.01, 0.10] | 0.04 [0.01, 0.07] | around |
| wu | 25 | signed | PP | 0.090 | 0.05 [0.00, 0.10] | 0.05 [0.01, 0.09] | 0.00 [-0.05, 0.05] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9925.
Asked-first subset (descriptive): {"predicted": 12, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "neither: the lookup is around W_E as well as J++", "split_layers": [12, 14]}}
