# X0 verdict: nem35l_x52_fresh

Model nemotron-3.5-lightning (a9904d24); lens J++ `cache/nemotron-3.5-lightning/lenses/jpp/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16_jpp_lens.pt` sha256 3306b6e4f0f4ba03; set d1_topics_v3; predicted layer 14; non-chat read first; UNVERIFIED.

Batch 52 coverage: no prediction: coverage run on an already-scored rule (X0's rule unchanged; scenes excluded from the selection: 60).

DESCRIPTIVE (amendment 3, after data): run on the items each reader gets right whether or not the gate passed; not part of the X0 rule.

Gate (unedited org accuracy under the decisive read >= 0.80 for both readers): chat: {'PP': 0.9642, 'PM': 0.7513} (greedy text {'PP': 0.9624, 'PM': 0.7531}, cand {'PP': 0.9642, 'PM': 0.7478}) pass=False, eligible 342

## chat: CONFIRMED at layer 14 (lookup around, recall through); H-token: no W_E rows; split at layers [14]

S_noRandOMP = the fitted null, Δ minus its 25-atom OMP over a random Gaussian dictionary (Dan, 24 Oct); S_noRand = Δ minus a random subspace of the J++ part's share (rand_sub).

| layer | reader | n | S_whole | S_noJ | S_noRand | S_noRandOMP | Jdep | Rdep | excess | J share | label |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 | PM | 295 | 0.93 | 0.53 | 0.89 | - | 0.44 [0.37, 0.50] | 0.05 [0.02, 0.07] | 0.39 [0.33, 0.45] | 0.281 | through |
| 14 | PP | 295 | 0.45 | 0.40 | 0.41 | - | 0.11 [0.06, 0.17] | 0.08 [0.02, 0.15] | 0.03 [-0.02, 0.08] | 0.281 | around |

Dictionaries at layer 14:

Each dictionary's Rdep uses its own random part, at that dictionary's share of ||Δ||².

| dict | k | fit | reader | part's share (median) | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|
| jpp | 25 | signed | PM | 0.281 | 0.44 [0.37, 0.50] | 0.05 [0.02, 0.07] | 0.39 [0.33, 0.45] | through |
| jpp | 25 | signed | PP | 0.281 | 0.11 [0.06, 0.17] | 0.08 [0.02, 0.15] | 0.03 [-0.02, 0.08] | around |

Switch: the top token (decisive); the cand read is descriptive. Reads agree (top token vs cand) on the whole edit: 0.9915.
Asked-first subset (descriptive): {"predicted": 14, "chat": {"verdict": "confirmed", "lookup_label": "around", "recall_label": "through", "h_token": "no W_E rows", "split_layers": [14]}}
