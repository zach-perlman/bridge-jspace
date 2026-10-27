# X0 verdict: qwen35_122b_x0_necessity_r2

Model qwen3.5-122b-a10b (a099dee7); lens J++ `qwen3.5-122b-a10b/jpp/Salesforce-wikitext/Qwen3.5-122B-A10B_jpp_lens.pt` sha256 b771e50244c81a3f; set d1_topics_v3; predicted layer 33; non-chat read first; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9917, 'PM': 0.85} (greedy text {'PP': 0.99, 'PM': 0.8533}, cand {'PP': 0.9917, 'PM': 0.845}) pass=True, eligible 410

## chat: CONFIRMED at layer 33 (lookup around, recall through); H-token: neither: the lookup is around W_E as well as J++; split at layers [33]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 24 | PM | 200 | 0.96 | 0.47 | 0.93 | 0.94 | 0.51 [0.41, 0.60] | 0.04 [0.01, 0.07] | 0.47 [0.37, 0.56] | 0.275 | through |
| 24 | PP | 200 | 0.83 | 0.32 | 0.67 | 0.78 | 0.61 [0.53, 0.69] | 0.19 [0.13, 0.27] | 0.42 [0.32, 0.50] | 0.275 | through |
| 27 | PM | 200 | 0.93 | 0.18 | 0.88 | 0.92 | 0.80 [0.71, 0.87] | 0.05 [0.02, 0.10] | 0.75 [0.65, 0.82] | 0.306 | through |
| 27 | PP | 200 | 0.77 | 0.14 | 0.56 | 0.70 | 0.82 [0.73, 0.89] | 0.26 [0.20, 0.33] | 0.56 [0.47, 0.64] | 0.306 | through |
| 30 | PM | 200 | 0.93 | 0.48 | 0.91 | 0.93 | 0.48 [0.37, 0.58] | 0.02 [-0.01, 0.05] | 0.45 [0.36, 0.55] | 0.308 | through |
| 30 | PP | 200 | 0.64 | 0.35 | 0.52 | 0.57 | 0.44 [0.36, 0.51] | 0.18 [0.11, 0.25] | 0.26 [0.18, 0.33] | 0.308 | through |
| 33 | PM | 200 | 0.92 | 0.56 | 0.84 | 0.92 | 0.40 [0.30, 0.49] | 0.08 [0.04, 0.13] | 0.32 [0.22, 0.41] | 0.252 | through |
| 33 | PP | 200 | 0.45 | 0.35 | 0.35 | 0.40 | 0.20 [0.11, 0.30] | 0.20 [0.10, 0.31] | 0.00 [-0.06, 0.06] | 0.252 | around |
| 36 | PM | 200 | 0.77 | 0.48 | 0.77 | 0.78 | 0.37 [0.27, 0.46] | 0.00 [-0.06, 0.06] | 0.37 [0.28, 0.46] | 0.204 | through |
| 36 | PP | 200 | 0.29 | 0.28 | 0.28 | 0.28 | 0.05 [0.00, 0.11] | 0.07 [0.00, 0.15] | -0.02 [-0.10, 0.06] | 0.204 | can't tell |

Dictionaries at layer 33:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | nonneg | PM | 0.090 | 0.02 [0.00, 0.05] | 0.03 [0.00, 0.07] | -0.01 [-0.04, 0.02] | around |
| jpp | 25 | signed | PM | 0.252 | 0.40 [0.30, 0.49] | 0.08 [0.04, 0.13] | 0.32 [0.22, 0.41] | through |
| jpp | 50 | signed | PM | 0.334 | 0.64 [0.54, 0.71] | 0.18 [0.11, 0.26] | 0.45 [0.35, 0.54] | through |
| jpp | 100 | signed | PM | 0.436 | 0.83 [0.74, 0.89] | 0.40 [0.32, 0.48] | 0.43 [0.32, 0.51] | through |
| jppall | 25 | signed | PM | 0.253 | 0.37 [0.27, 0.47] | 0.10 [0.05, 0.15] | 0.27 [0.17, 0.38] | through |
| jppall | 50 | signed | PM | 0.334 | 0.61 [0.50, 0.71] | 0.18 [0.12, 0.25] | 0.43 [0.32, 0.52] | through |
| jppall | 100 | signed | PM | 0.434 | 0.83 [0.75, 0.89] | 0.42 [0.34, 0.51] | 0.41 [0.30, 0.49] | through |
| jppdig | 10 | signed | PM | 0.008 | 0.01 [-0.02, 0.04] | -0.01 [-0.03, 0.02] | 0.01 [-0.01, 0.03] | around |
| rand | 25 | signed | PM | 0.134 | 0.01 [-0.01, 0.03] | 0.01 [-0.01, 0.03] | 0.00 [-0.02, 0.02] | around |
| we | 25 | signed | PM | 0.178 | 0.03 [0.00, 0.06] | 0.03 [0.00, 0.06] | 0.01 [-0.02, 0.03] | around |
| wu | 25 | signed | PM | 0.125 | 0.00 [-0.01, 0.02] | 0.01 [-0.01, 0.03] | -0.01 [-0.02, 0.00] | around |
| jpp | 25 | nonneg | PP | 0.090 | 0.04 [0.01, 0.09] | 0.06 [0.01, 0.11] | -0.01 [-0.06, 0.04] | around |
| jpp | 25 | signed | PP | 0.252 | 0.20 [0.11, 0.30] | 0.20 [0.10, 0.31] | 0.00 [-0.06, 0.06] | around |
| jpp | 50 | signed | PP | 0.334 | 0.26 [0.15, 0.37] | 0.28 [0.17, 0.39] | -0.02 [-0.09, 0.05] | around |
| jpp | 100 | signed | PP | 0.436 | 0.36 [0.26, 0.45] | 0.48 [0.38, 0.59] | -0.12 [-0.22, -0.04] | around |
| jppall | 25 | signed | PP | 0.253 | 0.18 [0.08, 0.28] | 0.18 [0.07, 0.30] | 0.00 [-0.08, 0.08] | around |
| jppall | 50 | signed | PP | 0.334 | 0.21 [0.11, 0.33] | 0.31 [0.20, 0.42] | -0.10 [-0.19, -0.03] | around |
| jppall | 100 | signed | PP | 0.434 | 0.33 [0.21, 0.44] | 0.51 [0.40, 0.62] | -0.18 [-0.30, -0.07] | around |
| jppdig | 10 | signed | PP | 0.008 | 0.00 [-0.06, 0.05] | 0.01 [-0.04, 0.06] | -0.01 [-0.04, 0.00] | around |
| rand | 25 | signed | PP | 0.134 | 0.10 [0.04, 0.17] | 0.09 [0.03, 0.16] | 0.01 [-0.04, 0.06] | around |
| we | 25 | signed | PP | 0.178 | 0.11 [0.04, 0.19] | 0.11 [0.05, 0.19] | 0.00 [-0.06, 0.06] | around |
| wu | 25 | signed | PP | 0.125 | 0.08 [0.02, 0.15] | 0.09 [0.03, 0.16] | -0.01 [-0.05, 0.03] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9955.
Asked-first subset (descriptive): {"predicted": 33, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "neither: the lookup is around W_E as well as J++", "split_layers": [33]}}
