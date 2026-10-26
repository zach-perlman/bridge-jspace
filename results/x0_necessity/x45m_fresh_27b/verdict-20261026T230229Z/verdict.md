# X0 verdict: x45m_fresh_27b

Model qwen3.6-27b (6a9e13bd); lens J++ `qwen3.6-27b/jpp/Salesforce-wikitext/Qwen3.6-27B_jpp_lens.pt` sha256 bbef480b41028e15; set d1_topics_v3; predicted layer 32; non-chat read first; UNVERIFIED.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 1, 'PM': 0.9833} (greedy text {'PP': 1, 'PM': 0.9833}, cand {'PP': 0.9983, 'PM': 0.9817}) pass=True, eligible 574

## chat: CONFIRMED at layer 32 (lookup around, recall through); H-token: no W_E rows; split at layers [32]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 32 | PM | 574 | 0.78 | 0.18 | 0.75 | - | 0.77 [0.70, 0.82] | 0.03 [0.00, 0.06] | 0.74 [0.67, 0.79] | 0.183 | through |
| 32 | PP | 574 | 0.39 | 0.37 | 0.39 | - | 0.03 [0.00, 0.07] | -0.01 [-0.04, 0.01] | 0.05 [0.01, 0.08] | 0.183 | around |

Dictionaries at layer 32:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | signed | PM | 0.183 | 0.77 [0.70, 0.82] | 0.03 [0.00, 0.06] | 0.74 [0.67, 0.79] | through |
| jpp | 25 | signed | PP | 0.183 | 0.03 [0.00, 0.07] | -0.01 [-0.04, 0.01] | 0.05 [0.01, 0.08] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9991.
Asked-first subset (descriptive): {"predicted": 32, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "no W_E rows", "split_layers": [32]}}
