# X0 verdict: muse30b_x0_necessity

Model muse-glimmer-30b (cec94fcf); lens J++ `Muse-Glimmer-30B_jpp_lens.pt` sha256 90fc5e52e8d765b7; set d1_topics_v3; predicted layer 26; non-chat read first; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.966, 'PM': 0.8906} (greedy text {'PP': 0.9698, 'PM': 0.8925}, cand {'PP': 0.9642, 'PM': 0.8849}) pass=True, eligible 395

## chat: CONFIRMED at layer 26 (lookup around, recall through); H-token: neither: the lookup is around W_E as well as J++; split at layers [26]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 13 | PM | 200 | 0.87 | 0.37 | 0.85 | 0.88 | 0.57 [0.45, 0.68] | 0.02 [0.00, 0.05] | 0.55 [0.43, 0.65] | 0.216 | through |
| 13 | PP | 200 | 0.66 | 0.36 | 0.58 | 0.65 | 0.45 [0.37, 0.53] | 0.12 [0.07, 0.18] | 0.33 [0.24, 0.41] | 0.216 | through |
| 26 | PM | 200 | 0.58 | 0.17 | 0.60 | 0.61 | 0.72 [0.57, 0.81] | -0.03 [-0.12, 0.03] | 0.75 [0.61, 0.87] | 0.142 | through |
| 26 | PP | 200 | 0.35 | 0.34 | 0.31 | 0.34 | 0.01 [-0.04, 0.06] | 0.11 [0.04, 0.18] | -0.10 [-0.15, -0.04] | 0.142 | around |
| 34 | PM | 200 | 0.10 | 0.06 | 0.10 | 0.10 | 0.43 [0.27, 0.61] | 0.05 [-0.17, 0.17] | 0.38 [0.19, 0.67] | 0.078 | can't tell |
| 34 | PP | 200 | 0.00 | 0.00 | 0.00 | 0.00 | nan [nan, nan] | nan [nan, nan] | nan [nan, nan] | 0.078 | can't tell |

Dictionaries at layer 26:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | nonneg | PM | 0.031 | 0.00 [-0.05, 0.04] | -0.03 [-0.08, 0.01] | 0.03 [-0.02, 0.08] | around |
| jpp | 25 | signed | PM | 0.142 | 0.72 [0.57, 0.81] | -0.03 [-0.12, 0.03] | 0.75 [0.61, 0.87] | through |
| jpp | 50 | signed | PM | 0.198 | 0.81 [0.70, 0.89] | -0.02 [-0.11, 0.07] | 0.83 [0.68, 0.96] | through |
| jpp | 100 | signed | PM | 0.276 | 0.88 [0.79, 0.94] | 0.03 [-0.10, 0.15] | 0.85 [0.71, 0.99] | through |
| jpp | 200 | signed | PM | 0.379 | 0.96 [0.89, 0.99] | 0.26 [0.09, 0.41] | 0.70 [0.54, 0.87] | through |
| jppall | 25 | signed | PM | 0.141 | 0.71 [0.56, 0.81] | -0.04 [-0.12, 0.02] | 0.75 [0.61, 0.87] | through |
| jppdig | 10 | signed | PM | 0.004 | -0.02 [-0.05, 0.00] | -0.02 [-0.07, 0.00] | 0.00 [-0.03, 0.03] | around |
| rand | 25 | signed | PM | 0.061 | -0.05 [-0.11, -0.01] | -0.06 [-0.13, -0.02] | 0.01 [-0.04, 0.06] | around |
| we | 25 | signed | PM | 0.072 | 0.01 [-0.03, 0.05] | -0.03 [-0.09, 0.00] | 0.04 [0.01, 0.10] | around |
| wu | 25 | signed | PM | 0.049 | -0.02 [-0.06, 0.01] | -0.03 [-0.06, 0.00] | 0.01 [-0.04, 0.04] | around |
| jpp | 25 | nonneg | PP | 0.031 | 0.01 [0.00, 0.04] | 0.01 [0.00, 0.04] | 0.00 [-0.04, 0.04] | around |
| jpp | 25 | signed | PP | 0.142 | 0.01 [-0.04, 0.06] | 0.11 [0.04, 0.18] | -0.10 [-0.15, -0.04] | around |
| jpp | 50 | signed | PP | 0.198 | 0.13 [0.02, 0.23] | 0.14 [0.03, 0.25] | -0.01 [-0.09, 0.07] | around |
| jpp | 100 | signed | PP | 0.276 | 0.17 [0.05, 0.27] | 0.17 [0.05, 0.28] | 0.00 [-0.06, 0.07] | around |
| jpp | 200 | signed | PP | 0.379 | 0.46 [0.33, 0.58] | 0.27 [0.15, 0.39] | 0.19 [0.08, 0.31] | mixed |
| jppall | 25 | signed | PP | 0.141 | 0.01 [-0.04, 0.06] | 0.10 [0.00, 0.17] | -0.09 [-0.13, -0.02] | around |
| jppdig | 10 | signed | PP | 0.004 | 0.01 [0.00, 0.04] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.04] | around |
| rand | 25 | signed | PP | 0.061 | 0.01 [-0.04, 0.06] | 0.03 [-0.04, 0.10] | -0.01 [-0.08, 0.05] | around |
| we | 25 | signed | PP | 0.072 | 0.07 [0.01, 0.13] | 0.03 [-0.04, 0.10] | 0.04 [-0.05, 0.13] | around |
| wu | 25 | signed | PP | 0.049 | 0.06 [0.00, 0.11] | 0.03 [-0.04, 0.10] | 0.03 [-0.03, 0.08] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9967.
Asked-first subset (descriptive): {"predicted": 26, "chat": {"verdict": "can't tell", "lookup_label": "can't tell", "recall_label": "through", "h_token": "can't tell", "split_layers": []}}
