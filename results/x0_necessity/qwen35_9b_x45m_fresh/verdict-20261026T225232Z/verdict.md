# X0 verdict: qwen35_9b_x45m_fresh

Model qwen3.5-9b (c2022362); lens J++ `qwen3.5-9b/jpp/Salesforce-wikitext/Qwen3.5-9B_jpp_lens.pt` sha256 8cda12f7ddf11e70; set d1_topics_v3; predicted layer 12; non-chat read first; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.97, 'PM': 0.8533} (greedy text {'PP': 0.97, 'PM': 0.855}, cand {'PP': 0.965, 'PM': 0.8483}) pass=True, eligible 417

## chat: CONFIRMED at layer 12 (lookup around, recall through); H-token: no W_E rows; split at layers [12]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 12 | PM | 417 | 0.99 | 0.48 | 0.96 | - | 0.51 [0.44, 0.57] | 0.02 [0.01, 0.04] | 0.48 [0.42, 0.55] | 0.265 | through |
| 12 | PP | 417 | 0.52 | 0.47 | 0.47 | - | 0.09 [0.07, 0.12] | 0.09 [0.05, 0.12] | 0.00 [-0.02, 0.03] | 0.265 | around |

Dictionaries at layer 12:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | signed | PM | 0.265 | 0.51 [0.44, 0.57] | 0.02 [0.01, 0.04] | 0.48 [0.42, 0.55] | through |
| jpp | 25 | signed | PP | 0.265 | 0.09 [0.07, 0.12] | 0.09 [0.05, 0.12] | 0.00 [-0.02, 0.03] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.994.
Asked-first subset (descriptive): {"predicted": 12, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "no W_E rows", "split_layers": [12]}}
