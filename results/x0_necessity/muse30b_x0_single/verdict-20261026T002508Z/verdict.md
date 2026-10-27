# X0 verdict: muse30b_x0_single

Model muse-glimmer-30b (cec94fcf); lens J++ `Muse-Glimmer-30B_jpp_lens.pt` sha256 90fc5e52e8d765b7; set d1_topics_v3; predicted layer 26; non-chat read first; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.966, 'PM': 0.8906} (greedy text {'PP': 0.9698, 'PM': 0.8925}, cand {'PP': 0.9642, 'PM': 0.8849}) pass=True, eligible 386

## chat: CONFIRMED at layer 26 (lookup around, recall through); H-token: neither: the lookup is around W_E as well as J++; split at layers [26]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 13 | PM | 200 | 0.88 | 0.52 | 0.87 | 0.89 | 0.41 [0.33, 0.49] | 0.01 [-0.01, 0.03] | 0.40 [0.32, 0.48] | 0.196 | through |
| 13 | PP | 200 | 0.70 | 0.53 | 0.69 | 0.70 | 0.25 [0.19, 0.31] | 0.03 [0.00, 0.07] | 0.22 [0.16, 0.28] | 0.196 | mixed |
| 26 | PM | 200 | 0.56 | 0.21 | 0.58 | 0.59 | 0.62 [0.50, 0.73] | -0.04 [-0.10, 0.02] | 0.66 [0.53, 0.78] | 0.117 | through |
| 26 | PP | 200 | 0.43 | 0.42 | 0.41 | 0.43 | 0.02 [-0.03, 0.06] | 0.03 [-0.02, 0.07] | -0.01 [-0.04, 0.00] | 0.117 | around |
| 34 | PM | 200 | 0.07 | 0.04 | 0.07 | 0.07 | 0.43 [0.21, 0.73] | 0.07 [-0.25, 0.27] | 0.36 [0.10, 0.80] | 0.078 | can't tell |
| 34 | PP | 200 | 0.00 | 0.00 | 0.00 | 0.00 | nan [nan, nan] | nan [nan, nan] | nan [nan, nan] | 0.078 | can't tell |

Dictionaries at layer 26:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | nonneg | PM | 0.023 | -0.01 [-0.05, 0.02] | -0.01 [-0.06, 0.03] | 0.00 [-0.04, 0.03] | around |
| jpp | 25 | signed | PM | 0.117 | 0.62 [0.50, 0.73] | -0.04 [-0.10, 0.02] | 0.66 [0.53, 0.78] | through |
| jpp | 50 | signed | PM | 0.168 | 0.77 [0.66, 0.86] | -0.08 [-0.19, 0.00] | 0.85 [0.72, 0.99] | through |
| jpp | 100 | signed | PM | 0.240 | 0.87 [0.78, 0.93] | -0.03 [-0.18, 0.09] | 0.89 [0.75, 1.07] | through |
| jpp | 200 | signed | PM | 0.340 | 0.93 [0.86, 0.97] | 0.20 [0.04, 0.33] | 0.73 [0.58, 0.90] | through |
| rand | 25 | signed | PM | 0.061 | -0.05 [-0.11, -0.01] | -0.02 [-0.06, 0.03] | -0.04 [-0.10, 0.01] | around |
| we | 25 | signed | PM | 0.067 | -0.04 [-0.09, 0.01] | -0.03 [-0.08, 0.03] | -0.01 [-0.07, 0.04] | around |
| wu | 25 | signed | PM | 0.051 | -0.04 [-0.10, -0.01] | -0.04 [-0.09, 0.02] | -0.01 [-0.08, 0.04] | around |
| jpp | 25 | nonneg | PP | 0.023 | 0.00 [-0.04, 0.03] | -0.01 [-0.04, 0.00] | 0.01 [0.00, 0.04] | around |
| jpp | 25 | signed | PP | 0.117 | 0.02 [-0.03, 0.06] | 0.03 [-0.02, 0.07] | -0.01 [-0.04, 0.00] | around |
| jpp | 50 | signed | PP | 0.168 | 0.08 [0.01, 0.14] | 0.03 [-0.02, 0.09] | 0.05 [0.00, 0.10] | around |
| jpp | 100 | signed | PP | 0.240 | 0.12 [0.03, 0.19] | 0.07 [0.01, 0.12] | 0.05 [0.00, 0.09] | around |
| jpp | 200 | signed | PP | 0.340 | 0.41 [0.30, 0.50] | 0.19 [0.10, 0.26] | 0.22 [0.13, 0.32] | through |
| rand | 25 | signed | PP | 0.061 | 0.00 [-0.04, 0.03] | 0.00 [-0.04, 0.03] | 0.00 [-0.03, 0.03] | around |
| we | 25 | signed | PP | 0.067 | 0.01 [-0.04, 0.06] | 0.00 [-0.04, 0.03] | 0.01 [-0.03, 0.07] | around |
| wu | 25 | signed | PP | 0.051 | 0.03 [-0.02, 0.09] | 0.01 [-0.03, 0.05] | 0.02 [0.00, 0.05] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9983.
Asked-first subset (descriptive): {"predicted": 26, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "neither: the lookup is around W_E as well as J++", "split_layers": [26]}}
