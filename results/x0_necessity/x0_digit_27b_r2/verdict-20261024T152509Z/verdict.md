# X0 verdict: x0_digit_27b_r2

Model qwen3.6-27b (6a9e13bd); lens J++ `qwen3.6-27b/jpp/Salesforce-wikitext/Qwen3.6-27B_jpp_lens.pt` sha256 bbef480b41028e15; set d1_topics_v3; predicted layer 32; non-chat read first; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9967, 'PM': 0.9767} (greedy text {'PP': 0.9967, 'PM': 0.9767}, cand {'PP': 0.9967, 'PM': 0.975}) pass=True, eligible 569

## chat: NOT CONFIRMED at layer 32 (lookup mixed, recall through); H-token: no W_E rows; split at layers []

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 32 | PM | 200 | 0.75 | 0.18 | 0.72 | - | 0.76 [0.66, 0.84] | 0.03 [-0.01, 0.07] | 0.73 [0.64, 0.80] | 0.155 | through |
| 32 | PP | 200 | 0.42 | 0.35 | 0.41 | - | 0.16 [0.09, 0.24] | 0.02 [0.00, 0.06] | 0.14 [0.08, 0.21] | 0.155 | mixed |

Dictionaries at layer 32:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | nonneg | PM | 0.098 | 0.21 [0.14, 0.29] | 0.00 [-0.03, 0.03] | 0.21 [0.14, 0.29] | mixed |
| jpp | 25 | signed | PM | 0.155 | 0.76 [0.66, 0.84] | 0.03 [-0.01, 0.07] | 0.73 [0.64, 0.80] | through |
| jpp | 50 | signed | PM | 0.221 | 0.89 [0.83, 0.94] | 0.09 [0.02, 0.15] | 0.81 [0.72, 0.88] | through |
| jpp | 100 | signed | PM | 0.305 | 0.95 [0.90, 0.98] | 0.28 [0.20, 0.35] | 0.67 [0.60, 0.74] | through |
| jppall | 25 | signed | PM | 0.156 | 0.77 [0.67, 0.85] | 0.03 [-0.01, 0.07] | 0.74 [0.66, 0.81] | through |
| jppall | 50 | signed | PM | 0.220 | 0.89 [0.83, 0.94] | 0.09 [0.02, 0.16] | 0.80 [0.72, 0.87] | through |
| jppall | 100 | signed | PM | 0.303 | 0.95 [0.91, 0.98] | 0.27 [0.19, 0.34] | 0.68 [0.61, 0.75] | through |
| jppdig | 10 | signed | PM | 0.005 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | around |
| jpp | 25 | nonneg | PP | 0.098 | 0.02 [0.00, 0.06] | 0.01 [0.00, 0.04] | 0.01 [0.00, 0.04] | around |
| jpp | 25 | signed | PP | 0.155 | 0.16 [0.09, 0.24] | 0.02 [0.00, 0.06] | 0.14 [0.08, 0.21] | mixed |
| jpp | 50 | signed | PP | 0.221 | 0.38 [0.28, 0.46] | 0.06 [0.02, 0.10] | 0.32 [0.23, 0.40] | through |
| jpp | 100 | signed | PP | 0.305 | 0.72 [0.60, 0.82] | 0.12 [0.06, 0.18] | 0.60 [0.48, 0.71] | through |
| jppall | 25 | signed | PP | 0.156 | 0.15 [0.08, 0.23] | 0.02 [0.00, 0.06] | 0.13 [0.07, 0.20] | mixed |
| jppall | 50 | signed | PP | 0.220 | 0.35 [0.26, 0.44] | 0.06 [0.02, 0.10] | 0.29 [0.21, 0.38] | through |
| jppall | 100 | signed | PP | 0.303 | 0.71 [0.60, 0.81] | 0.12 [0.06, 0.18] | 0.59 [0.47, 0.70] | through |
| jppdig | 10 | signed | PP | 0.005 | -0.01 [-0.04, 0.00] | -0.01 [-0.04, 0.00] | 0.00 [0.00, 0.00] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 1.
Asked-first subset (descriptive): {"predicted": 32, "chat": {"verdict": "can't tell", "lookup_label": "can't tell", "recall_label": "through", "h_token": "no W_E rows", "split_layers": []}}
