# 53.6: the recall, lens identity vs address, in conflict

Batch 53, test 53.6 (jobs/c3/batch53.yaml; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). At the bridge word: the lens part toward B (P_J of B's change, k = 25) plus the address swap toward C's slot (s = 2, the probe run's pointer means); x6_routes' C0 scenes with three distinct legs counts. UNVERIFIED.

Rule (Dan's brief): on the recall under lens + address: "the recall follows the lens identity" if B's share >= 2x C's; "follows the address" if C's >= 2x B's; else "both".

Rule across models (Dan 11:25, critic_1125, verbatim): "the recall's pointer use tracks the swap's collateral" if the models whose recall the address swap moved (9B, Lightning) give "both" and the others give "follows the lens identity". As computed: the moved models are Dan's list (qwen3.5-9b, nemotron-3.5-lightning); every other model of the four is wanted at "follows the lens identity"; a model with another label breaks it.

**Across models: does not hold** (per model, label / wanted: qwen3.5-9b None / both; nemotron-3.5-lightning None / both; qwen3.6-27b None / identity; muse-glimmer-30b both / identity).

| model | layer | n | recall B | recall C | recall original | recall other | label |
|---|---|---|---|---|---|---|---|
| muse-glimmer-30b | 26 | 300 | 0.07 [0.04, 0.11] | 0.05 [0.02, 0.08] | 0.85 [0.77, 0.90] | 0.04 [0.02, 0.06] | **both** |

Every arm, both readers (shares, cluster-bootstrap CIs over the bridge item A):

| model | reader | arm | B | C | original | other |
|---|---|---|---|---|---|---|
| muse-glimmer-30b | lookup | none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | lookup | lens | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 1.00 [0.99, 1.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | lookup | addr | 0.14 [0.09, 0.18] | 0.48 [0.42, 0.54] | 0.38 [0.31, 0.45] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | lookup | both | 0.15 [0.10, 0.20] | 0.51 [0.45, 0.57] | 0.35 [0.28, 0.41] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | lookup | both_rand | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.99 [0.97, 1.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | recall | none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | recall | lens | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.99 [0.98, 1.00] | 0.00 [0.00, 0.01] |
| muse-glimmer-30b | recall | addr | 0.02 [0.00, 0.03] | 0.03 [0.01, 0.05] | 0.94 [0.88, 0.98] | 0.02 [0.00, 0.04] |
| muse-glimmer-30b | recall | both | 0.07 [0.04, 0.11] | 0.05 [0.02, 0.08] | 0.85 [0.77, 0.90] | 0.04 [0.02, 0.06] |
| muse-glimmer-30b | recall | both_rand | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.01] | 0.98 [0.96, 0.99] | 0.01 [0.00, 0.02] |

Arms: none = O unedited; lens = the lens part toward B: P_J (h_{S_B} - h_O); addr = the address swap toward C's slot: 2 (mu_{j_C} - mu_{j_A}); both = lens + addr (the rule's arm); both_rand = lens + a random direction of addr's norm (beside). The lookup's classes: B = B's locker digit, C = C's, original = A's.

- muse-glimmer-30b: medians {'norm_delta': 170.9606, 'norm_lens': 61.5802, 'norm_addr': 82.7625, 'share_lens': 0.1157}; gate {'PP': 0.9934354485776805, 'PM': 0.9277899343544858} (pass True), eligible 358, roles {"C's legs equal A's or B's": 943, 'kept': 457}, used 300.

Figure: x53_identity_address.png
