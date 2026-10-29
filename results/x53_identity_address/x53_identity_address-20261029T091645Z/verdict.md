# 53.6: the recall, lens identity vs address, in conflict

Batch 53, test 53.6 (jobs/c3/batch53.yaml; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). At the bridge word: the lens part toward B (P_J of B's change, k = 25) plus the address swap toward C's slot (s = 2, the probe run's pointer means); x6_routes' C0 scenes with three distinct legs counts. UNVERIFIED.

Rule (Dan's brief): on the recall under lens + address: "the recall follows the lens identity" if B's share >= 2x C's; "follows the address" if C's >= 2x B's; else "both".

| model | layer | n | recall B | recall C | recall original | recall other | label |
|---|---|---|---|---|---|---|---|
| qwen3.5-9b | 12 | 300 | 0.25 [0.20, 0.32] | 0.30 [0.25, 0.35] | 0.39 [0.31, 0.46] | 0.06 [0.03, 0.10] | **both** |
| nemotron-3.5-lightning | 14 | 300 | 0.25 [0.19, 0.32] | 0.27 [0.21, 0.34] | 0.45 [0.39, 0.52] | 0.02 [0.01, 0.03] | **both** |

Every arm, both readers (shares, cluster-bootstrap CIs over the bridge item A):

| model | reader | arm | B | C | original | other |
|---|---|---|---|---|---|---|
| qwen3.5-9b | lookup | none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | lookup | lens | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | lookup | addr | 0.08 [0.06, 0.11] | 0.44 [0.38, 0.49] | 0.44 [0.39, 0.50] | 0.03 [0.02, 0.05] |
| qwen3.5-9b | lookup | both | 0.14 [0.11, 0.16] | 0.44 [0.38, 0.50] | 0.40 [0.35, 0.46] | 0.02 [0.01, 0.03] |
| qwen3.5-9b | lookup | both_rand | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | recall | none | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 1.00 [0.99, 1.00] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | recall | lens | 0.05 [0.03, 0.08] | 0.02 [0.00, 0.04] | 0.91 [0.86, 0.94] | 0.02 [0.00, 0.03] |
| qwen3.5-9b | recall | addr | 0.03 [0.01, 0.06] | 0.21 [0.16, 0.27] | 0.74 [0.67, 0.80] | 0.02 [0.01, 0.04] |
| qwen3.5-9b | recall | both | 0.25 [0.20, 0.32] | 0.30 [0.25, 0.35] | 0.39 [0.31, 0.46] | 0.06 [0.03, 0.10] |
| qwen3.5-9b | recall | both_rand | 0.06 [0.03, 0.09] | 0.03 [0.01, 0.05] | 0.89 [0.84, 0.93] | 0.02 [0.01, 0.04] |
| nemotron-3.5-lightning | lookup | none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | lookup | lens | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | lookup | addr | 0.08 [0.05, 0.11] | 0.53 [0.47, 0.59] | 0.39 [0.33, 0.45] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | lookup | both | 0.18 [0.13, 0.23] | 0.48 [0.42, 0.54] | 0.35 [0.29, 0.40] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | lookup | both_rand | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | recall | none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [0.99, 1.00] | 0.00 [0.00, 0.01] |
| nemotron-3.5-lightning | recall | lens | 0.04 [0.01, 0.06] | 0.01 [0.00, 0.02] | 0.95 [0.92, 0.98] | 0.01 [0.00, 0.02] |
| nemotron-3.5-lightning | recall | addr | 0.06 [0.04, 0.09] | 0.24 [0.19, 0.30] | 0.67 [0.60, 0.74] | 0.03 [0.01, 0.05] |
| nemotron-3.5-lightning | recall | both | 0.25 [0.19, 0.32] | 0.27 [0.21, 0.34] | 0.45 [0.39, 0.52] | 0.02 [0.01, 0.03] |
| nemotron-3.5-lightning | recall | both_rand | 0.03 [0.02, 0.05] | 0.00 [0.00, 0.01] | 0.96 [0.94, 0.98] | 0.00 [0.00, 0.01] |

Arms: none = O unedited; lens = the lens part toward B: P_J (h_{S_B} - h_O); addr = the address swap toward C's slot: 2 (mu_{j_C} - mu_{j_A}); both = lens + addr (the rule's arm); both_rand = lens + a random direction of addr's norm (beside). The lookup's classes: B = B's locker digit, C = C's, original = A's.

- qwen3.5-9b: medians {'norm_delta': 17.5658, 'norm_lens': 7.0894, 'norm_addr': 8.1996, 'share_lens': 0.1664}; gate {'PP': 1.0, 'PM': 0.8828125} (pass True), eligible 388, roles {"C's legs equal A's or B's": 888, 'kept': 512}, used 300.
- nemotron-3.5-lightning: medians {'norm_delta': 15.2012, 'norm_lens': 7.2919, 'norm_addr': 6.6864, 'share_lens': 0.2343}; gate {'PP': 1.0, 'PM': 0.8590998043052838} (pass True), eligible 383, roles {"C's legs equal A's or B's": 889, 'kept': 511}, used 300.

Figure: x53_identity_address.png
