# X0 verdict: x0_kmatch_27b

Model qwen3.6-27b (6a9e13bd); lens J++ `qwen3.6-27b/jpp/Salesforce-wikitext/Qwen3.6-27B_jpp_lens.pt` sha256 bbef480b41028e15; set d1_topics_v3; predicted layer 32; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9967, 'PM': 0.9767} (greedy text {'PP': 0.9967, 'PM': 0.9767}, cand {'PP': 0.9967, 'PM': 0.975}) pass=True, eligible 569

## chat: NOT CONFIRMED at layer 32 (lookup mixed, recall through); H-token: not applicable (the J++ lookup is not around); split at layers []

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 32 | PM | 200 | 0.74 | 0.17 | 0.73 | 0.74 | 0.78 [0.69, 0.85] | 0.01 [-0.02, 0.05] | 0.77 [0.69, 0.83] | 0.155 | through |
| 32 | PP | 200 | 0.43 | 0.36 | 0.41 | 0.42 | 0.16 [0.09, 0.24] | 0.05 [0.01, 0.09] | 0.12 [0.06, 0.18] | 0.155 | mixed |

Dictionaries at layer 32:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | nonneg | PM | 0.098 | 0.22 [0.16, 0.29] | -0.01 [-0.04, 0.01] | 0.23 [0.16, 0.32] | mixed |
| jpp | 25 | signed | PM | 0.155 | 0.78 [0.69, 0.85] | 0.01 [-0.02, 0.05] | 0.77 [0.69, 0.83] | through |
| jpp | 50 | signed | PM | 0.221 | 0.89 [0.83, 0.94] | 0.09 [0.03, 0.16] | 0.80 [0.72, 0.87] | through |
| jpp | 100 | signed | PM | 0.305 | 0.95 [0.90, 0.98] | 0.28 [0.19, 0.35] | 0.67 [0.60, 0.75] | through |
| jpp | 200 | signed | PM | 0.412 | 0.99 [0.96, 1.00] | 0.49 [0.40, 0.57] | 0.50 [0.41, 0.59] | through |
| rand | 25 | signed | PM | 0.082 | 0.00 [-0.03, 0.03] | -0.01 [-0.03, 0.02] | 0.01 [-0.02, 0.03] | around |
| rand | 50 | signed | PM | 0.149 | 0.00 [-0.04, 0.04] | -0.01 [-0.04, 0.03] | 0.01 [-0.02, 0.04] | around |
| rand | 100 | signed | PM | 0.264 | 0.01 [-0.06, 0.07] | 0.07 [0.02, 0.13] | -0.07 [-0.12, -0.01] | around |
| rand | 200 | signed | PM | 0.446 | 0.47 [0.35, 0.57] | 0.48 [0.37, 0.57] | -0.01 [-0.07, 0.04] | around |
| we | 25 | signed | PM | 0.084 | -0.01 [-0.04, 0.00] | -0.01 [-0.04, 0.01] | 0.00 [-0.03, 0.03] | around |
| we | 50 | signed | PM | 0.151 | 0.01 [-0.03, 0.04] | -0.01 [-0.04, 0.03] | 0.01 [-0.02, 0.05] | around |
| we | 100 | signed | PM | 0.264 | 0.07 [-0.01, 0.14] | 0.06 [0.01, 0.12] | 0.01 [-0.04, 0.05] | around |
| we | 200 | signed | PM | 0.441 | 0.52 [0.40, 0.62] | 0.44 [0.33, 0.54] | 0.07 [0.01, 0.12] | around |
| wu | 25 | signed | PM | 0.073 | 0.00 [-0.03, 0.03] | -0.01 [-0.04, 0.01] | 0.01 [-0.01, 0.04] | around |
| wu | 50 | signed | PM | 0.133 | -0.01 [-0.04, 0.03] | -0.01 [-0.04, 0.02] | 0.00 [-0.03, 0.03] | around |
| wu | 100 | signed | PM | 0.235 | 0.03 [-0.03, 0.08] | 0.05 [-0.01, 0.10] | -0.02 [-0.07, 0.02] | around |
| wu | 200 | signed | PM | 0.399 | 0.21 [0.09, 0.33] | 0.28 [0.15, 0.39] | -0.07 [-0.13, -0.01] | around |
| jpp | 25 | nonneg | PP | 0.098 | 0.03 [0.00, 0.08] | 0.02 [0.00, 0.06] | 0.01 [0.00, 0.04] | around |
| jpp | 25 | signed | PP | 0.155 | 0.16 [0.09, 0.24] | 0.05 [0.01, 0.09] | 0.12 [0.06, 0.18] | mixed |
| jpp | 50 | signed | PP | 0.221 | 0.37 [0.29, 0.45] | 0.07 [0.03, 0.12] | 0.30 [0.22, 0.38] | through |
| jpp | 100 | signed | PP | 0.305 | 0.72 [0.61, 0.82] | 0.12 [0.06, 0.18] | 0.60 [0.49, 0.71] | through |
| jpp | 200 | signed | PP | 0.412 | 0.98 [0.94, 1.00] | 0.40 [0.29, 0.49] | 0.58 [0.48, 0.68] | through |
| rand | 25 | signed | PP | 0.082 | 0.01 [-0.03, 0.05] | 0.02 [0.00, 0.06] | -0.01 [-0.04, 0.00] | around |
| rand | 50 | signed | PP | 0.149 | 0.02 [0.00, 0.06] | 0.03 [0.00, 0.08] | -0.01 [-0.04, 0.00] | around |
| rand | 100 | signed | PP | 0.264 | 0.06 [0.00, 0.12] | 0.09 [0.04, 0.15] | -0.03 [-0.08, 0.00] | around |
| rand | 200 | signed | PP | 0.446 | 0.66 [0.54, 0.77] | 0.58 [0.44, 0.70] | 0.08 [0.01, 0.17] | around |
| we | 25 | signed | PP | 0.084 | 0.01 [-0.03, 0.05] | 0.02 [0.00, 0.06] | -0.01 [-0.04, 0.00] | around |
| we | 50 | signed | PP | 0.151 | 0.03 [0.00, 0.08] | 0.03 [0.00, 0.08] | 0.00 [-0.03, 0.03] | around |
| we | 100 | signed | PP | 0.264 | 0.05 [0.00, 0.10] | 0.08 [0.02, 0.15] | -0.03 [-0.07, 0.00] | around |
| we | 200 | signed | PP | 0.441 | 0.67 [0.55, 0.77] | 0.56 [0.42, 0.68] | 0.12 [0.02, 0.22] | mixed |
| wu | 25 | signed | PP | 0.073 | 0.00 [-0.03, 0.03] | 0.01 [-0.03, 0.05] | -0.01 [-0.04, 0.00] | around |
| wu | 50 | signed | PP | 0.133 | 0.01 [0.00, 0.04] | 0.03 [0.00, 0.08] | -0.02 [-0.06, 0.00] | around |
| wu | 100 | signed | PP | 0.235 | 0.03 [0.00, 0.08] | 0.08 [0.03, 0.14] | -0.05 [-0.08, -0.01] | around |
| wu | 200 | signed | PP | 0.399 | 0.28 [0.18, 0.37] | 0.37 [0.26, 0.47] | -0.09 [-0.18, 0.00] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 1.
Asked-first subset (descriptive): {"predicted": 32, "chat": {"verdict": "can't tell", "lookup_label": "can't tell", "recall_label": "through", "h_token": "can't tell", "split_layers": []}}
