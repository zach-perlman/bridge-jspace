# X0 verdict: muse30b_x45m_fresh

Model muse-glimmer-30b (cec94fcf); lens J++ `Muse-Glimmer-30B_jpp_lens.pt` sha256 90fc5e52e8d765b7; set d1_topics_v3; predicted layer 26; non-chat read first; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9681, 'PM': 0.885} (greedy text {'PP': 0.9699, 'PM': 0.8779}, cand {'PP': 0.9681, 'PM': 0.885}) pass=True, eligible 409

## chat: CONFIRMED at layer 26 (lookup around, recall through); H-token: no W_E rows; split at layers [26]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 26 | PM | 409 | 0.72 | 0.20 | 0.70 | - | 0.72 [0.63, 0.80] | 0.02 [-0.02, 0.06] | 0.70 [0.60, 0.79] | 0.171 | through |
| 26 | PP | 409 | 0.32 | 0.32 | 0.34 | - | -0.01 [-0.04, 0.03] | -0.07 [-0.12, -0.02] | 0.06 [0.02, 0.11] | 0.171 | around |

Dictionaries at layer 26:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | signed | PM | 0.171 | 0.72 [0.63, 0.80] | 0.02 [-0.02, 0.06] | 0.70 [0.60, 0.79] | through |
| jpp | 25 | signed | PP | 0.171 | -0.01 [-0.04, 0.03] | -0.07 [-0.12, -0.02] | 0.06 [0.02, 0.11] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9939.
Asked-first subset (descriptive): {"predicted": 26, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "no W_E rows", "split_layers": [26]}}
