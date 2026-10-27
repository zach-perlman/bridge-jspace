# X0 verdict: x0_single_27b_r2

Model qwen3.6-27b (6a9e13bd); lens J++ `qwen3.6-27b/jpp/Salesforce-wikitext/Qwen3.6-27B_jpp_lens.pt` sha256 bbef480b41028e15; set d1_topics_v3; predicted layer 32; non-chat read first; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9967, 'PM': 0.9767} (greedy text {'PP': 0.9967, 'PM': 0.9767}, cand {'PP': 0.9967, 'PM': 0.975}) pass=True, eligible 566

## chat: CONFIRMED at layer 32 (lookup around, recall through); H-token: neither: the lookup is around W_E as well as J++; split at layers [28, 30, 32]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 28 | PM | 200 | 0.93 | 0.54 | 0.92 | 0.93 | 0.42 [0.33, 0.50] | 0.01 [-0.01, 0.03] | 0.41 [0.32, 0.49] | 0.181 | through |
| 28 | PP | 200 | 0.61 | 0.53 | 0.55 | 0.60 | 0.15 [0.08, 0.21] | 0.11 [0.06, 0.16] | 0.04 [0.00, 0.09] | 0.181 | around |
| 30 | PM | 200 | 0.90 | 0.50 | 0.91 | 0.90 | 0.44 [0.36, 0.51] | -0.01 [-0.04, 0.02] | 0.45 [0.37, 0.53] | 0.139 | through |
| 30 | PP | 200 | 0.56 | 0.49 | 0.53 | 0.54 | 0.12 [0.06, 0.17] | 0.06 [0.03, 0.10] | 0.05 [0.02, 0.09] | 0.139 | around |
| 32 | PM | 200 | 0.73 | 0.28 | 0.73 | 0.73 | 0.61 [0.52, 0.69] | 0.00 [-0.03, 0.03] | 0.61 [0.51, 0.69] | 0.135 | through |
| 32 | PP | 200 | 0.47 | 0.45 | 0.47 | 0.47 | 0.05 [0.01, 0.09] | 0.00 [0.00, 0.00] | 0.05 [0.01, 0.09] | 0.135 | around |
| 34 | PM | 200 | 0.58 | 0.23 | 0.59 | 0.60 | 0.61 [0.50, 0.71] | -0.03 [-0.08, 0.02] | 0.64 [0.52, 0.73] | 0.142 | through |
| 34 | PP | 200 | 0.42 | 0.38 | 0.43 | 0.42 | 0.10 [0.03, 0.16] | -0.04 [-0.09, 0.03] | 0.13 [0.07, 0.19] | 0.142 | mixed |

Dictionaries at layer 32:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | nonneg | PM | 0.082 | 0.17 [0.10, 0.25] | -0.01 [-0.04, 0.02] | 0.18 [0.09, 0.28] | mixed |
| jpp | 25 | signed | PM | 0.135 | 0.61 [0.52, 0.69] | 0.00 [-0.03, 0.03] | 0.61 [0.51, 0.69] | through |
| jpp | 50 | signed | PM | 0.200 | 0.82 [0.72, 0.88] | 0.03 [-0.01, 0.09] | 0.78 [0.68, 0.86] | through |
| jpp | 100 | signed | PM | 0.283 | 0.91 [0.85, 0.96] | 0.18 [0.11, 0.25] | 0.73 [0.65, 0.80] | through |
| rand | 25 | signed | PM | 0.082 | -0.01 [-0.04, 0.03] | -0.01 [-0.04, 0.02] | 0.01 [0.00, 0.02] | around |
| we | 25 | signed | PM | 0.083 | -0.01 [-0.04, 0.01] | -0.01 [-0.04, 0.02] | 0.00 [-0.03, 0.02] | around |
| wu | 25 | signed | PM | 0.075 | -0.01 [-0.04, 0.01] | -0.01 [-0.04, 0.02] | 0.00 [-0.02, 0.02] | around |
| jpp | 25 | nonneg | PP | 0.082 | 0.01 [0.00, 0.04] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.04] | around |
| jpp | 25 | signed | PP | 0.135 | 0.05 [0.01, 0.09] | 0.00 [0.00, 0.00] | 0.05 [0.01, 0.09] | around |
| jpp | 50 | signed | PP | 0.200 | 0.18 [0.12, 0.24] | 0.03 [0.00, 0.07] | 0.15 [0.09, 0.22] | mixed |
| jpp | 100 | signed | PP | 0.283 | 0.55 [0.45, 0.65] | 0.05 [0.01, 0.09] | 0.49 [0.39, 0.61] | through |
| rand | 25 | signed | PP | 0.082 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | around |
| we | 25 | signed | PP | 0.083 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | around |
| wu | 25 | signed | PP | 0.075 | -0.01 [-0.04, 0.00] | 0.00 [0.00, 0.00] | -0.01 [-0.04, 0.00] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9956.
Asked-first subset (descriptive): {"predicted": 32, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "neither: the lookup is around W_E as well as J++", "split_layers": [28, 30, 32]}}
