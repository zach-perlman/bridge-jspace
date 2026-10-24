# X0 verdict: qwen35_122b_x0_single

Model qwen3.5-122b-a10b (a099dee7); lens J++ `qwen3.5-122b-a10b/jpp/Salesforce-wikitext/Qwen3.5-122B-A10B_jpp_lens.pt` sha256 b771e50244c81a3f; set d1_topics_v3; predicted layer 33; non-chat read first; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9917, 'PM': 0.85} (greedy text {'PP': 0.99, 'PM': 0.8533}, cand {'PP': 0.9917, 'PM': 0.845}) pass=True, eligible 432

## chat: CONFIRMED at layer 33 (lookup around, recall through); H-token: neither: the lookup is around W_E as well as J++; split at layers [33]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 33 | PM | 200 | 0.91 | 0.60 | 0.84 | 0.91 | 0.33 [0.22, 0.43] | 0.07 [0.03, 0.12] | 0.27 [0.16, 0.36] | 0.211 | through |
| 33 | PP | 200 | 0.47 | 0.43 | 0.42 | 0.42 | 0.09 [0.04, 0.14] | 0.10 [0.03, 0.17] | -0.01 [-0.06, 0.04] | 0.211 | around |

Dictionaries at layer 33:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | nonneg | PM | 0.070 | 0.03 [0.00, 0.07] | 0.02 [-0.01, 0.06] | 0.01 [-0.02, 0.04] | around |
| jpp | 25 | signed | PM | 0.211 | 0.33 [0.22, 0.43] | 0.07 [0.03, 0.12] | 0.27 [0.16, 0.36] | through |
| jpp | 50 | signed | PM | 0.284 | 0.46 [0.35, 0.55] | 0.15 [0.09, 0.21] | 0.31 [0.22, 0.39] | through |
| jpp | 100 | signed | PM | 0.381 | 0.61 [0.51, 0.69] | 0.31 [0.23, 0.40] | 0.29 [0.20, 0.37] | through |
| rand | 25 | signed | PM | 0.134 | 0.00 [-0.02, 0.02] | 0.02 [-0.01, 0.06] | -0.02 [-0.04, 0.01] | around |
| we | 25 | signed | PM | 0.164 | 0.06 [0.02, 0.09] | 0.02 [-0.01, 0.07] | 0.03 [-0.01, 0.08] | around |
| wu | 25 | signed | PM | 0.122 | 0.01 [-0.03, 0.05] | 0.01 [-0.01, 0.04] | -0.01 [-0.03, 0.02] | around |
| jpp | 25 | nonneg | PP | 0.070 | 0.02 [0.00, 0.05] | 0.07 [0.03, 0.12] | -0.05 [-0.10, -0.01] | around |
| jpp | 25 | signed | PP | 0.211 | 0.09 [0.04, 0.14] | 0.10 [0.03, 0.17] | -0.01 [-0.06, 0.04] | around |
| jpp | 50 | signed | PP | 0.284 | 0.10 [0.04, 0.17] | 0.16 [0.09, 0.24] | -0.06 [-0.11, -0.02] | around |
| jpp | 100 | signed | PP | 0.381 | 0.15 [0.08, 0.23] | 0.23 [0.16, 0.32] | -0.09 [-0.16, -0.02] | around |
| rand | 25 | signed | PP | 0.134 | 0.11 [0.05, 0.17] | 0.07 [0.03, 0.12] | 0.03 [0.00, 0.07] | around |
| we | 25 | signed | PP | 0.164 | 0.07 [0.01, 0.13] | 0.07 [0.03, 0.12] | 0.00 [-0.05, 0.04] | around |
| wu | 25 | signed | PP | 0.122 | 0.05 [0.01, 0.10] | 0.09 [0.04, 0.13] | -0.03 [-0.07, 0.00] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.995.
Asked-first subset (descriptive): {"predicted": 33, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "neither: the lookup is around W_E as well as J++", "split_layers": [33]}}
