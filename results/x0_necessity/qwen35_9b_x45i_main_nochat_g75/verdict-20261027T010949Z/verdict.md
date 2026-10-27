# X0 verdict: qwen35_9b_x45i_main_nochat_g75

Model qwen3.5-9b (c2022362); lens J++ `qwen3.5-9b/jpp/Salesforce-wikitext/Qwen3.5-9B_jpp_lens.pt` sha256 8cda12f7ddf11e70; set d1_topics_v3; predicted layer 12; non-chat read digit; UNVERIFIED.

DESCRIPTIVE (amendment 3, after data): run on the items each reader gets right whether or not the gate passed; not part of the X0 rule.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): nochat: {'PP': 0.9217, 'PM': 0.76} (greedy text {'PP': 0.97, 'PM': 0.76}, cand {'PP': 0.9617, 'PM': 0.8133}) pass=True, eligible 310

## nochat: CONFIRMED at layer 12 (lookup around, recall through); H-token: neither: the lookup is around W_E as well as J++; split at layers [12]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 12 | PM | 200 | 0.93 | 0.45 | 0.90 | 0.92 | 0.52 [0.43, 0.60] | 0.03 [0.00, 0.07] | 0.49 [0.38, 0.57] | 0.234 | through |
| 12 | PP | 200 | 0.43 | 0.36 | 0.35 | 0.41 | 0.16 [0.09, 0.24] | 0.20 [0.13, 0.27] | -0.03 [-0.08, 0.02] | 0.234 | around |

Dictionaries at layer 12:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 10 | signed | PM | 0.141 | 0.15 [0.08, 0.21] | 0.02 [0.00, 0.04] | 0.13 [0.07, 0.19] | mixed |
| jpp | 25 | nonneg | PM | 0.139 | 0.08 [0.03, 0.15] | 0.02 [0.00, 0.04] | 0.06 [0.03, 0.12] | around |
| jpp | 25 | signed | PM | 0.234 | 0.52 [0.43, 0.60] | 0.03 [0.00, 0.07] | 0.49 [0.38, 0.57] | through |
| jpp | 50 | signed | PM | 0.328 | 0.73 [0.63, 0.81] | 0.12 [0.06, 0.21] | 0.61 [0.49, 0.68] | through |
| jpp | 100 | signed | PM | 0.439 | 0.82 [0.73, 0.88] | 0.37 [0.27, 0.48] | 0.45 [0.35, 0.52] | through |
| rand | 25 | signed | PM | 0.102 | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.03] | -0.01 [-0.02, 0.00] | around |
| we | 10 | signed | PM | 0.050 | 0.00 [0.00, 0.00] | 0.00 [-0.02, 0.02] | 0.00 [-0.02, 0.02] | around |
| we | 25 | signed | PM | 0.109 | 0.01 [0.00, 0.03] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | around |
| we | 50 | signed | PM | 0.192 | 0.02 [-0.01, 0.05] | 0.01 [-0.01, 0.03] | 0.01 [-0.02, 0.03] | around |
| we | 100 | signed | PM | 0.328 | 0.10 [0.05, 0.17] | 0.11 [0.05, 0.18] | -0.01 [-0.03, 0.02] | around |
| wu | 25 | signed | PM | 0.090 | -0.01 [-0.02, 0.00] | 0.01 [0.00, 0.02] | -0.01 [-0.03, 0.00] | around |
| jpp | 10 | signed | PP | 0.141 | 0.02 [-0.03, 0.09] | 0.11 [0.06, 0.17] | -0.09 [-0.16, -0.01] | around |
| jpp | 25 | nonneg | PP | 0.139 | 0.09 [0.04, 0.15] | 0.10 [0.06, 0.16] | -0.01 [-0.06, 0.04] | around |
| jpp | 25 | signed | PP | 0.234 | 0.16 [0.09, 0.24] | 0.20 [0.13, 0.27] | -0.03 [-0.08, 0.02] | around |
| jpp | 50 | signed | PP | 0.328 | 0.29 [0.19, 0.40] | 0.28 [0.19, 0.37] | 0.01 [-0.05, 0.09] | around |
| jpp | 100 | signed | PP | 0.439 | 0.48 [0.38, 0.61] | 0.51 [0.40, 0.64] | -0.02 [-0.11, 0.06] | around |
| rand | 25 | signed | PP | 0.102 | 0.05 [-0.02, 0.10] | 0.05 [0.01, 0.08] | 0.00 [-0.05, 0.04] | around |
| we | 10 | signed | PP | 0.050 | 0.03 [0.00, 0.07] | 0.02 [-0.02, 0.06] | 0.01 [0.00, 0.04] | around |
| we | 25 | signed | PP | 0.109 | 0.07 [0.03, 0.12] | 0.06 [0.02, 0.10] | 0.01 [-0.03, 0.06] | around |
| we | 50 | signed | PP | 0.192 | 0.13 [0.07, 0.18] | 0.17 [0.11, 0.23] | -0.05 [-0.09, 0.00] | around |
| we | 100 | signed | PP | 0.328 | 0.26 [0.19, 0.36] | 0.28 [0.20, 0.36] | -0.01 [-0.05, 0.05] | around |
| wu | 25 | signed | PP | 0.090 | 0.03 [0.00, 0.07] | 0.03 [-0.01, 0.08] | 0.00 [-0.03, 0.03] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9925.
Asked-first subset (descriptive): {"predicted": 12, "nochat": {"verdict": "can't tell", "lookup_label": "can't tell", "recall_label": "through", "h_token": "can't tell", "split_layers": []}}
