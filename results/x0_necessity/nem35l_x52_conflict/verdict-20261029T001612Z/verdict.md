# X0 verdict: nem35l_x52_conflict

Model nemotron-3.5-lightning (a9904d24); lens J++ `cache/nemotron-3.5-lightning/lenses/jpp/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16_jpp_lens.pt` sha256 3306b6e4f0f4ba03; set d1_topics_v3; predicted layer 14; non-chat read first; UNVERIFIED.

Batch 52 coverage: no prediction: coverage run on an already-scored rule (X0's rule unchanged; scenes excluded from the selection: 60).

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9574, 'PM': 0.8159} (greedy text {'PP': 0.9574, 'PM': 0.8178}, cand {'PP': 0.9554, 'PM': 0.814}) pass=True, eligible 315

## chat: CONFIRMED at layer 14 (lookup around, recall through); H-token: no W_E rows; split at layers [14, 18, 22]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | PM | 200 | 0.97 | 0.98 | 0.97 | - | -0.01 [-0.03, 0.00] | 0.00 [0.00, 0.00] | -0.01 [-0.03, 0.00] | 0.094 | around |
| 2 | PP | 200 | 0.97 | 0.97 | 0.97 | - | 0.00 [-0.01, 0.02] | 0.00 [0.00, 0.00] | 0.00 [-0.01, 0.02] | 0.094 | around |
| 6 | PM | 200 | 0.97 | 0.70 | 0.96 | - | 0.28 [0.20, 0.36] | 0.01 [-0.02, 0.03] | 0.27 [0.20, 0.35] | 0.228 | mixed |
| 6 | PP | 200 | 0.77 | 0.45 | 0.69 | - | 0.42 [0.35, 0.48] | 0.10 [0.06, 0.14] | 0.31 [0.24, 0.39] | 0.228 | through |
| 10 | PM | 200 | 0.98 | 0.60 | 0.90 | - | 0.38 [0.30, 0.47] | 0.08 [0.04, 0.13] | 0.30 [0.22, 0.38] | 0.279 | through |
| 10 | PP | 200 | 0.71 | 0.40 | 0.52 | - | 0.44 [0.35, 0.53] | 0.28 [0.22, 0.34] | 0.16 [0.09, 0.24] | 0.279 | mixed |
| 14 | PM | 200 | 0.94 | 0.56 | 0.89 | - | 0.41 [0.32, 0.50] | 0.06 [0.03, 0.10] | 0.34 [0.25, 0.44] | 0.270 | through |
| 14 | PP | 200 | 0.45 | 0.36 | 0.38 | - | 0.19 [0.13, 0.25] | 0.16 [0.09, 0.23] | 0.03 [-0.01, 0.08] | 0.270 | around |
| 18 | PM | 200 | 0.91 | 0.60 | 0.86 | - | 0.33 [0.27, 0.40] | 0.04 [0.01, 0.09] | 0.29 [0.22, 0.35] | 0.226 | through |
| 18 | PP | 200 | 0.41 | 0.40 | 0.38 | - | 0.01 [-0.05, 0.08] | 0.07 [0.03, 0.13] | -0.06 [-0.13, 0.00] | 0.226 | around |
| 22 | PM | 200 | 0.79 | 0.51 | 0.77 | - | 0.36 [0.26, 0.46] | 0.03 [-0.03, 0.08] | 0.34 [0.25, 0.42] | 0.205 | through |
| 22 | PP | 200 | 0.34 | 0.30 | 0.32 | - | 0.12 [0.02, 0.22] | 0.06 [-0.01, 0.13] | 0.06 [-0.03, 0.15] | 0.205 | around |
| 26 | PM | 200 | 0.50 | 0.19 | 0.46 | - | 0.62 [0.48, 0.76] | 0.09 [0.00, 0.19] | 0.53 [0.42, 0.65] | 0.197 | through |
| 26 | PP | 200 | 0.02 | 0.02 | 0.02 | - | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.197 | can't tell |
| 30 | PM | 200 | 0.45 | 0.12 | 0.39 | - | 0.72 [0.60, 0.84] | 0.13 [0.01, 0.27] | 0.59 [0.49, 0.70] | 0.244 | through |
| 30 | PP | 200 | 0.00 | 0.00 | 0.00 | - | nan [nan, nan] | nan [nan, nan] | nan [nan, nan] | 0.244 | can't tell |
| 34 | PM | 200 | 0.01 | 0.01 | 0.01 | - | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.151 | can't tell |
| 34 | PP | 200 | 0.00 | 0.00 | 0.00 | - | nan [nan, nan] | nan [nan, nan] | nan [nan, nan] | 0.151 | can't tell |
| 38 | PM | 200 | 0.01 | 0.01 | 0.01 | - | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.154 | can't tell |
| 38 | PP | 200 | 0.00 | 0.00 | 0.00 | - | nan [nan, nan] | nan [nan, nan] | nan [nan, nan] | 0.154 | can't tell |
| 42 | PM | 200 | 0.01 | 0.01 | 0.01 | - | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.153 | can't tell |
| 42 | PP | 200 | 0.00 | 0.00 | 0.00 | - | nan [nan, nan] | nan [nan, nan] | nan [nan, nan] | 0.153 | can't tell |
| 46 | PM | 200 | 0.01 | 0.01 | 0.01 | - | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.163 | can't tell |
| 46 | PP | 200 | 0.00 | 0.00 | 0.00 | - | nan [nan, nan] | nan [nan, nan] | nan [nan, nan] | 0.163 | can't tell |
| 50 | PM | 200 | 0.01 | 0.01 | 0.01 | - | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.188 | can't tell |
| 50 | PP | 200 | 0.00 | 0.00 | 0.00 | - | nan [nan, nan] | nan [nan, nan] | nan [nan, nan] | 0.188 | can't tell |

Dictionaries at layer 14:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | signed | PM | 0.270 | 0.41 [0.32, 0.50] | 0.06 [0.03, 0.10] | 0.34 [0.25, 0.44] | through |
| jpp | 25 | signed | PP | 0.270 | 0.19 [0.13, 0.25] | 0.16 [0.09, 0.23] | 0.03 [-0.01, 0.08] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9987.
Asked-first subset (descriptive): {"predicted": 14, "chat": {"verdict": "can't tell", "lookup_label": "can't tell", "recall_label": "through", "h_token": "no W_E rows", "split_layers": []}}
