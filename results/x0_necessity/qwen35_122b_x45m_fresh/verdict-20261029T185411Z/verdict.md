# X0 verdict: qwen35_122b_x45m_fresh

Model qwen3.5-122b-a10b (a099dee7); lens J++ `qwen3.5-122b-a10b/jpp/Salesforce-wikitext/Qwen3.5-122B-A10B_jpp_lens.pt` sha256 b771e50244c81a3f; set d1_topics_v3; predicted layer 33; non-chat read first; UNVERIFIED.

Batch 52 coverage: no prediction: coverage run on an already-scored rule (X0's rule unchanged; scenes excluded from the selection: 0).

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9883, 'PM': 0.8433} (greedy text {'PP': 0.9933, 'PM': 0.845}, cand {'PP': 0.9883, 'PM': 0.8433}) pass=True, eligible 435

## chat: CONFIRMED at layer 33 (lookup around, recall through); H-token: no W_E rows; split at layers [33]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 33 | PM | 435 | 0.94 | 0.52 | 0.85 | - | 0.44 [0.37, 0.52] | 0.10 [0.06, 0.15] | 0.34 [0.28, 0.41] | 0.276 | through |
| 33 | PP | 435 | 0.43 | 0.42 | 0.41 | - | 0.02 [0.00, 0.05] | 0.05 [0.00, 0.10] | -0.03 [-0.07, 0.02] | 0.276 | around |

Dictionaries at layer 33:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | signed | PM | 0.276 | 0.44 [0.37, 0.52] | 0.10 [0.06, 0.15] | 0.34 [0.28, 0.41] | through |
| jpp | 25 | signed | PP | 0.276 | 0.02 [0.00, 0.05] | 0.05 [0.00, 0.10] | -0.03 [-0.07, 0.02] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9989.
Asked-first subset (descriptive): {"predicted": 33, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "no W_E rows", "split_layers": [33]}}
