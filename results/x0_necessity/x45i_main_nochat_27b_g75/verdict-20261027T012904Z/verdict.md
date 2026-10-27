# X0 verdict: x45i_main_nochat_27b_g75

Model qwen3.6-27b (6a9e13bd); lens J++ `qwen3.6-27b/jpp/Salesforce-wikitext/Qwen3.6-27B_jpp_lens.pt` sha256 bbef480b41028e15; set d1_topics_v3; predicted layer 32; non-chat read digit; UNVERIFIED.

DESCRIPTIVE (amendment 3, after data): run on the items each reader gets right whether or not the gate passed; not part of the X0 rule.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): nochat: {'PP': 0.7717, 'PM': 0.9083} (greedy text {'PP': 0.9967, 'PM': 0.905}, cand {'PP': 0.9983, 'PM': 0.9067}) pass=True, eligible 369

## nochat: NOT CONFIRMED at layer 32 (lookup mixed, recall through); H-token: not applicable (the J++ lookup is not around); split at layers []

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 32 | PM | 200 | 0.66 | 0.15 | 0.67 | 0.66 | 0.76 [0.70, 0.83] | -0.02 [-0.08, 0.03] | 0.79 [0.70, 0.86] | 0.151 | through |
| 32 | PP | 200 | 0.41 | 0.32 | 0.39 | 0.40 | 0.23 [0.16, 0.29] | 0.06 [0.01, 0.11] | 0.17 [0.10, 0.24] | 0.151 | mixed |

Dictionaries at layer 32:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 10 | signed | PM | 0.091 | 0.42 [0.34, 0.51] | -0.01 [-0.05, 0.03] | 0.43 [0.34, 0.52] | through |
| jpp | 25 | nonneg | PM | 0.096 | 0.26 [0.18, 0.36] | 0.01 [-0.04, 0.04] | 0.25 [0.18, 0.34] | mixed |
| jpp | 25 | signed | PM | 0.151 | 0.76 [0.70, 0.83] | -0.02 [-0.08, 0.03] | 0.79 [0.70, 0.86] | through |
| jpp | 50 | signed | PM | 0.216 | 0.89 [0.82, 0.94] | -0.01 [-0.07, 0.05] | 0.89 [0.81, 0.97] | through |
| jpp | 100 | signed | PM | 0.301 | 0.95 [0.92, 0.98] | 0.11 [0.02, 0.22] | 0.84 [0.72, 0.94] | through |
| rand | 25 | signed | PM | 0.081 | 0.00 [-0.04, 0.04] | 0.00 [-0.03, 0.03] | 0.00 [-0.03, 0.03] | around |
| we | 10 | signed | PM | 0.038 | -0.02 [-0.05, 0.00] | 0.03 [-0.01, 0.07] | -0.05 [-0.09, 0.00] | around |
| we | 25 | signed | PM | 0.084 | -0.02 [-0.06, 0.00] | 0.02 [-0.02, 0.05] | -0.04 [-0.07, -0.01] | around |
| we | 50 | signed | PM | 0.151 | -0.01 [-0.06, 0.04] | -0.03 [-0.09, 0.03] | 0.02 [-0.01, 0.06] | around |
| we | 100 | signed | PM | 0.264 | 0.02 [-0.04, 0.10] | 0.03 [-0.03, 0.11] | -0.01 [-0.05, 0.03] | around |
| wu | 25 | signed | PM | 0.073 | 0.01 [-0.03, 0.06] | 0.02 [-0.02, 0.06] | -0.01 [-0.04, 0.03] | around |
| jpp | 10 | signed | PP | 0.091 | 0.11 [0.05, 0.17] | 0.02 [-0.03, 0.08] | 0.08 [0.02, 0.17] | around |
| jpp | 25 | nonneg | PP | 0.096 | 0.07 [0.03, 0.13] | 0.02 [-0.03, 0.08] | 0.05 [0.00, 0.11] | around |
| jpp | 25 | signed | PP | 0.151 | 0.23 [0.16, 0.29] | 0.06 [0.01, 0.11] | 0.17 [0.10, 0.24] | mixed |
| jpp | 50 | signed | PP | 0.216 | 0.40 [0.30, 0.49] | 0.04 [-0.03, 0.09] | 0.36 [0.25, 0.48] | through |
| jpp | 100 | signed | PP | 0.301 | 0.67 [0.58, 0.77] | 0.17 [0.11, 0.24] | 0.51 [0.41, 0.60] | through |
| rand | 25 | signed | PP | 0.081 | 0.04 [0.00, 0.08] | 0.02 [-0.03, 0.08] | 0.01 [-0.03, 0.06] | around |
| we | 10 | signed | PP | 0.038 | 0.02 [-0.02, 0.07] | 0.00 [-0.05, 0.05] | 0.02 [0.00, 0.05] | around |
| we | 25 | signed | PP | 0.084 | 0.06 [0.01, 0.11] | 0.02 [-0.03, 0.08] | 0.04 [-0.02, 0.10] | around |
| we | 50 | signed | PP | 0.151 | 0.07 [0.03, 0.12] | 0.04 [-0.02, 0.10] | 0.04 [0.00, 0.10] | around |
| we | 100 | signed | PP | 0.264 | 0.13 [0.07, 0.20] | 0.14 [0.08, 0.21] | -0.01 [-0.06, 0.04] | around |
| wu | 25 | signed | PP | 0.073 | 0.00 [-0.05, 0.05] | 0.04 [-0.02, 0.09] | -0.04 [-0.10, 0.02] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.985.
Asked-first subset (descriptive): {"predicted": 32, "nochat": {"verdict": "can't tell", "lookup_label": "can't tell", "recall_label": "through", "h_token": "can't tell", "split_layers": []}}
