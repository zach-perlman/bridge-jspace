# 53.8: a binding-ID test for the lookup's identity code

Batch 53, test 53.8 (jobs/c3/batch53.yaml critic_1125, item 6; Dan 11:25, stretch; no prediction (batch 53: the rule fixed in Dan's text, 29 Oct 11:25, before any run)). UNVERIFIED.

Dan's text, verbatim: "Stretch, 53.8, a binding-ID test for the lookup's identity code (9B, then Muse): at L, take the state at item X's mention in its locker sentence minus X's token embedding (mean over scenes, X fixed by slot), add it at the bridge word at 1x / 2x the size of a real identity change, against a random vector of the same norm and against the same with another item Y's mention. Read: lookups sent to X's locker. Rule: "a shared identity code" if X's share minus random >= 0.25 at 2x and minus Y's version >= 0.15; "no" if <= 0.05; else in between."

Rule as computed: at 2x, point estimates (EPS 1e-09): "a shared identity code" if X - random >= 0.25 and X - Y >= 0.15; "no" if X - random <= 0.05 (Dan's "<= 0.05" read as X's share minus random's at 2x); else "in between"; a failed gate: "not tested (gate x < 0.80)".

Centered arm (Dan 12:10, jobs/c3/batch53.yaml decisions_1210b item 1, verbatim; added before any run): "53.8: keep your construction (uncentered, dose 1x = ||Δ|| at the bridge word, as in 52) as the pre-specified arm, rule unchanged. Add, now, before any run: a centered arm (X's vector minus the mean over slots), same doses, same controls (random of the same norm; Y's centered version), the same rule thresholds reported for it beside. Report the slot-vector cosines and the norm of the slot-specific part." The headline is the pre-specified (uncentered) arm's label; the centered arm's label, by the same thresholds, is beside.

Design (fixed before any run):

- scenes: x6_routes.scenes (seed 2510, 1000 per condition, prefix-stable), the C0 scenes in generator order; test pool = C0 scenes 1-700 (the routes runs'), X0's competence, gate and eligibility there, the first 300 eligible; mean pool = C0 scenes 701-1000 (held out: no test scene's own state enters a vector)
- x_vector: per locker slot k: mean over the mean-pool scenes of (the block output at L at the k-th locker sentence's item word in O's chat lookup prompt) - (that token's input-embedding row, raw); X = the item at slot k (X fixed by slot); the item word is one token (the generator's rule, asserted)
- x_and_y: per test scene the two items other than the bridge item A take turns as X and Y (X = slot k, Y = the remaining slot k'); both assignments pooled
- dose: the size of a real identity change = ||Δ||, Δ = h_{S_B} - h_O at the bridge word at L (C0: Iris's pick A -> B, nothing else), per scene: x52_answer_map's ans1 / ans2 (s = ||Δ||); 1x and 2x
- controls: a random Gaussian direction per scene (seed 5308) at the same norm; Y's version = slot k''s vector at the same norm
- centered: Dan 12:10 (decisions_1210b item 1, before any run): a second arm with c~_k = c_k - (c_0 + c_1 + c_2) / 3 (the slot-specific part) in place of c_k, the same doses (d ||Δ||), the same random arm (same norm) and Y's centered version as controls, its own label by the same thresholds, beside; the headline is the uncentered arm's
- read: X0's chat read, both readers; the lookup's top token classed by locker slot (the slot's digit token) or other; X's share = the lookup's top token is X's locker digit
- collateral: the clean answers kept: the lookup's (A's locker) and the recall's (A's legs) top token unchanged
- ci: cluster bootstrap over the bridge item A (10,000 draws, seed 0), arms paired

Headline, the pre-specified arm (uncentered c_k):

| model | layer | n (scene, X) | X's share at 2x | Y's version | random | X - random | X - Y | label (uncentered) |
|---|---|---|---|---|---|---|---|---|
| 9B | 12 | 600 (300 scenes, 31 items) | 0.02 [0.01, 0.03] | 0.01 [0.01, 0.02] | 0.02 [0.01, 0.03] | 0.00 [-0.01, 0.01] | 0.00 [-0.00, 0.01] | **no** |
| 27B | 32 | 600 (300 scenes, 32 items) | 0.11 [0.09, 0.13] | 0.07 [0.05, 0.10] | 0.08 [0.06, 0.09] | 0.03 [0.01, 0.05] | 0.04 [0.02, 0.05] | **no** |
| Muse | 26 | 600 (300 scenes, 32 items) | 0.33 [0.30, 0.36] | 0.27 [0.25, 0.30] | 0.18 [0.16, 0.20] | 0.15 [0.12, 0.18] | 0.06 [0.03, 0.08] | **in between** |
| Lightning | - | - | - | - | - | - | - | not designed (9B, Muse, then 27B: Dan 11:25, 12:22; Lightning not added) |

Beside, the centered arm (c_k - mean over slots; Dan 12:10), same doses, controls and thresholds:

| model | layer | n (scene, X) | X's share at 2x | Y's version | random | X - random | X - Y | label (centered) |
|---|---|---|---|---|---|---|---|---|
| 9B | 12 | 600 (300 scenes, 31 items) | 0.25 [0.21, 0.29] | 0.12 [0.09, 0.15] | 0.02 [0.01, 0.03] | 0.23 [0.19, 0.27] | 0.13 [0.08, 0.17] | in between |
| 27B | 32 | 600 (300 scenes, 32 items) | 0.18 [0.15, 0.21] | 0.14 [0.12, 0.16] | 0.08 [0.06, 0.09] | 0.10 [0.08, 0.13] | 0.04 [0.00, 0.07] | in between |
| Muse | 26 | 600 (300 scenes, 32 items) | 0.45 [0.41, 0.48] | 0.28 [0.26, 0.31] | 0.18 [0.16, 0.20] | 0.27 [0.24, 0.29] | 0.16 [0.13, 0.19] | a shared identity code |
| Lightning | - | - | - | - | - | - | - | not designed (9B, Muse, then 27B: Dan 11:25, 12:22; Lightning not added) |

Slot vectors (Dan 12:10: the cosines and the norm of the slot-specific part c_k - mean over slots; with three slots the centered vectors sum to zero, so their cosines are about -0.5 when their norms are alike):

| model | slot | norm c_k | norm of the slot-specific part | its share of norm c_k |
|---|---|---|---|---|
| 9B | 0 | 34.16 | 10.75 | 0.315 |
| 9B | 1 | 33.65 | 5.98 | 0.178 |
| 9B | 2 | 31.87 | 7.16 | 0.225 |
| Muse | 0 | 246.33 | 110.15 | 0.447 |
| Muse | 1 | 305.67 | 60.04 | 0.196 |
| Muse | 2 | 313.04 | 77.55 | 0.248 |
| 27B | 0 | 79.37 | 26.24 | 0.331 |
| 27B | 1 | 79.42 | 16.40 | 0.206 |
| 27B | 2 | 76.78 | 18.18 | 0.237 |

- 9B: cosines between slot vectors {'0-1': 0.8907, '0-2': 0.8656, '1-2': 0.9743}; between their slot-specific parts {'0-1': -0.779, '0-2': -0.8516, '1-2': 0.3347}; slot differences vs the pointer means' {'0-1': 0.0822, '0-2': 0.019, '1-2': 0.1556}.
- Muse: cosines between slot vectors {'0-1': 0.8543, '0-2': 0.8169, '1-2': 0.9632}; between their slot-specific parts {'0-1': -0.7352, '0-2': -0.8512, '1-2': 0.2701}; slot differences vs the pointer means' {'0-1': 0.1171, '0-2': 0.1002, '1-2': 0.0579}.
- 27B: cosines between slot vectors {'0-1': 0.8743, '0-2': 0.8554, '1-2': 0.9587}; between their slot-specific parts {'0-1': -0.7283, '0-2': -0.786, '1-2': 0.1489}; slot differences vs the pointer means' {'0-1': 0.0219, '0-2': 0.0382, '1-2': 0.0678}.

Every dose: the lookup's answer under each arm kind, by role (X's locker / Y's / A's own = original / other); shares with cluster-bootstrap CIs over the bridge item:

| model | construction | dose | arm | X | Y | original | other |
|---|---|---|---|---|---|---|---|
| 9B | uncentered | 1x | X's vector | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.01] | 1.00 [0.99, 1.00] | 0.00 [0.00, 0.00] |
| 9B | uncentered | 1x | Y's version | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.01] | 1.00 [0.99, 1.00] | 0.00 [0.00, 0.00] |
| 9B | uncentered | 1x | random (same norm) | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.01] | 1.00 [0.99, 1.00] | 0.00 [0.00, 0.00] |
| 9B | uncentered | 2x | X's vector | 0.02 [0.01, 0.03] | 0.01 [0.01, 0.02] | 0.97 [0.95, 0.99] | 0.00 [0.00, 0.00] |
| 9B | uncentered | 2x | Y's version | 0.01 [0.01, 0.02] | 0.02 [0.01, 0.03] | 0.97 [0.95, 0.99] | 0.00 [0.00, 0.00] |
| 9B | uncentered | 2x | random (same norm) | 0.02 [0.01, 0.03] | 0.02 [0.01, 0.03] | 0.96 [0.94, 0.98] | 0.01 [0.00, 0.02] |
| 9B | centered | 1x | X's vector | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.01] | 0.99 [0.97, 1.00] | 0.00 [0.00, 0.00] |
| 9B | centered | 1x | Y's version | 0.00 [0.00, 0.01] | 0.01 [0.00, 0.02] | 0.99 [0.97, 1.00] | 0.00 [0.00, 0.00] |
| 9B | centered | 1x | random (same norm) | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.01] | 1.00 [0.99, 1.00] | 0.00 [0.00, 0.00] |
| 9B | centered | 2x | X's vector | 0.25 [0.21, 0.29] | 0.12 [0.09, 0.15] | 0.63 [0.58, 0.69] | 0.00 [0.00, 0.01] |
| 9B | centered | 2x | Y's version | 0.12 [0.09, 0.15] | 0.25 [0.21, 0.29] | 0.63 [0.58, 0.69] | 0.00 [0.00, 0.01] |
| 9B | centered | 2x | random (same norm) | 0.02 [0.01, 0.03] | 0.02 [0.01, 0.03] | 0.96 [0.94, 0.98] | 0.01 [0.00, 0.02] |
| Muse | uncentered | 1x | X's vector | 0.14 [0.12, 0.17] | 0.12 [0.10, 0.15] | 0.73 [0.68, 0.78] | 0.00 [0.00, 0.00] |
| Muse | uncentered | 1x | Y's version | 0.12 [0.10, 0.15] | 0.14 [0.12, 0.17] | 0.73 [0.68, 0.78] | 0.00 [0.00, 0.00] |
| Muse | uncentered | 1x | random (same norm) | 0.02 [0.01, 0.04] | 0.02 [0.01, 0.04] | 0.95 [0.93, 0.98] | 0.00 [0.00, 0.00] |
| Muse | uncentered | 2x | X's vector | 0.33 [0.30, 0.36] | 0.27 [0.25, 0.30] | 0.40 [0.35, 0.45] | 0.00 [0.00, 0.00] |
| Muse | uncentered | 2x | Y's version | 0.27 [0.25, 0.30] | 0.33 [0.30, 0.36] | 0.40 [0.35, 0.45] | 0.00 [0.00, 0.00] |
| Muse | uncentered | 2x | random (same norm) | 0.18 [0.16, 0.20] | 0.18 [0.16, 0.20] | 0.64 [0.60, 0.68] | 0.00 [0.00, 0.00] |
| Muse | centered | 1x | X's vector | 0.22 [0.19, 0.25] | 0.12 [0.09, 0.14] | 0.66 [0.61, 0.70] | 0.00 [0.00, 0.00] |
| Muse | centered | 1x | Y's version | 0.12 [0.09, 0.14] | 0.22 [0.19, 0.25] | 0.66 [0.61, 0.70] | 0.00 [0.00, 0.00] |
| Muse | centered | 1x | random (same norm) | 0.02 [0.01, 0.04] | 0.02 [0.01, 0.04] | 0.95 [0.93, 0.98] | 0.00 [0.00, 0.00] |
| Muse | centered | 2x | X's vector | 0.45 [0.41, 0.48] | 0.28 [0.26, 0.31] | 0.27 [0.22, 0.32] | 0.00 [0.00, 0.00] |
| Muse | centered | 2x | Y's version | 0.28 [0.26, 0.31] | 0.45 [0.41, 0.48] | 0.27 [0.22, 0.32] | 0.00 [0.00, 0.00] |
| Muse | centered | 2x | random (same norm) | 0.18 [0.16, 0.20] | 0.18 [0.16, 0.20] | 0.64 [0.60, 0.68] | 0.00 [0.00, 0.00] |
| 27B | uncentered | 1x | X's vector | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.98 [0.97, 0.99] | 0.00 [0.00, 0.00] |
| 27B | uncentered | 1x | Y's version | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.98 [0.97, 0.99] | 0.00 [0.00, 0.00] |
| 27B | uncentered | 1x | random (same norm) | 0.01 [0.00, 0.01] | 0.01 [0.00, 0.01] | 0.99 [0.98, 1.00] | 0.00 [0.00, 0.00] |
| 27B | uncentered | 2x | X's vector | 0.11 [0.09, 0.13] | 0.07 [0.05, 0.10] | 0.82 [0.77, 0.86] | 0.00 [0.00, 0.01] |
| 27B | uncentered | 2x | Y's version | 0.07 [0.05, 0.10] | 0.11 [0.09, 0.13] | 0.82 [0.77, 0.86] | 0.00 [0.00, 0.01] |
| 27B | uncentered | 2x | random (same norm) | 0.08 [0.06, 0.09] | 0.08 [0.06, 0.09] | 0.85 [0.82, 0.88] | 0.00 [0.00, 0.00] |
| 27B | centered | 1x | X's vector | 0.04 [0.02, 0.06] | 0.03 [0.02, 0.04] | 0.94 [0.91, 0.96] | 0.00 [0.00, 0.00] |
| 27B | centered | 1x | Y's version | 0.03 [0.02, 0.04] | 0.04 [0.02, 0.06] | 0.94 [0.91, 0.96] | 0.00 [0.00, 0.00] |
| 27B | centered | 1x | random (same norm) | 0.01 [0.00, 0.01] | 0.01 [0.00, 0.01] | 0.99 [0.98, 1.00] | 0.00 [0.00, 0.00] |
| 27B | centered | 2x | X's vector | 0.18 [0.15, 0.21] | 0.14 [0.12, 0.16] | 0.68 [0.64, 0.71] | 0.00 [0.00, 0.01] |
| 27B | centered | 2x | Y's version | 0.14 [0.12, 0.16] | 0.18 [0.15, 0.21] | 0.68 [0.64, 0.71] | 0.00 [0.00, 0.01] |
| 27B | centered | 2x | random (same norm) | 0.08 [0.06, 0.09] | 0.08 [0.06, 0.09] | 0.85 [0.82, 0.88] | 0.00 [0.00, 0.00] |

Collateral (the clean answers kept) and the real change's own effect:

| model | arm | n | lookup kept | recall kept |
|---|---|---|---|---|
| 9B | none | 300 | 1.00 [1.00, 1.00] | 0.99 [0.98, 1.00] |
| 9B | whole | 300 | 0.00 [0.00, 0.01] | 0.01 [0.00, 0.02] |
| 9B | code_x1 | 600 | 1.00 [0.99, 1.00] | 0.99 [0.98, 1.00] |
| 9B | rand_x1 | 300 | 1.00 [0.99, 1.00] | 0.99 [0.97, 1.00] |
| 9B | ccode_x1 | 600 | 0.99 [0.97, 1.00] | 0.93 [0.89, 0.96] |
| 9B | code_x2 | 600 | 0.97 [0.95, 0.99] | 0.96 [0.93, 0.98] |
| 9B | rand_x2 | 300 | 0.96 [0.94, 0.98] | 0.82 [0.77, 0.86] |
| 9B | ccode_x2 | 600 | 0.63 [0.58, 0.69] | 0.64 [0.58, 0.70] |
| 9B | whole: lookup sent to B's locker | - | 0.99 [0.98, 1.00] | - |
| Muse | none | 300 | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] |
| Muse | whole | 300 | 0.00 [0.00, 0.00] | 0.66 [0.57, 0.74] |
| Muse | code_x1 | 600 | 0.73 [0.68, 0.78] | 0.97 [0.92, 1.00] |
| Muse | rand_x1 | 300 | 0.95 [0.93, 0.98] | 0.98 [0.95, 1.00] |
| Muse | ccode_x1 | 600 | 0.66 [0.61, 0.70] | 0.96 [0.93, 0.99] |
| Muse | code_x2 | 600 | 0.40 [0.35, 0.45] | 0.94 [0.87, 0.98] |
| Muse | rand_x2 | 300 | 0.64 [0.60, 0.68] | 0.96 [0.93, 0.98] |
| Muse | ccode_x2 | 600 | 0.27 [0.22, 0.32] | 0.91 [0.86, 0.95] |
| Muse | whole: lookup sent to B's locker | - | 0.84 [0.80, 0.88] | - |
| 27B | none | 300 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| 27B | whole | 300 | 0.00 [0.00, 0.00] | 0.43 [0.32, 0.55] |
| 27B | code_x1 | 600 | 0.98 [0.97, 0.99] | 1.00 [0.99, 1.00] |
| 27B | rand_x1 | 300 | 0.99 [0.98, 1.00] | 1.00 [0.99, 1.00] |
| 27B | ccode_x1 | 600 | 0.94 [0.91, 0.96] | 0.99 [0.97, 1.00] |
| 27B | code_x2 | 600 | 0.82 [0.77, 0.86] | 0.99 [0.98, 1.00] |
| 27B | rand_x2 | 300 | 0.85 [0.82, 0.88] | 0.99 [0.96, 1.00] |
| 27B | ccode_x2 | 600 | 0.68 [0.64, 0.71] | 0.98 [0.95, 1.00] |
| 27B | whole: lookup sent to B's locker | - | 0.98 [0.96, 1.00] | - |

- 9B: per X slot at 2x (X / Y / random) {'uncentered': {'0': {'n': 209, 'X': 0.0096, 'Y': 0.0096, 'R': 0.0048}, '1': {'n': 191, 'X': 0.0366, 'Y': 0.0157, 'R': 0.0209}, '2': {'n': 200, 'X': 0.01, 'Y': 0.015, 'R': 0.03}}, 'centered': {'0': {'n': 209, 'X': 0.1292, 'Y': 0.134, 'R': 0.0048}, '1': {'n': 191, 'X': 0.2775, 'Y': 0.1047, 'R': 0.0209}, '2': {'n': 200, 'X': 0.34, 'Y': 0.12, 'R': 0.03}}}; medians {'norm_delta': 16.4939, 'norm_U_delta': 6.4457, 'cos_delta_codes_b_minus_a': 0.0515}; vectors {'norm': [34.163, 33.648, 31.867], 'cos': {'0-1': 0.8907, '0-2': 0.8656, '1-2': 0.9743}, 'slot_specific_norm': [10.752, 5.982, 7.155], 'slot_specific_share': [0.3147, 0.1778, 0.2245], 'cos_centered': {'0-1': -0.779, '0-2': -0.8516, '1-2': 0.3347}, 'diff_over_norm': {'0-1': 0.4643, '0-2': 0.5052, '1-2': 0.227}, 'cos_diff_vs_pointer_means': {'0-1': 0.0822, '0-2': 0.019, '1-2': 0.1556}, 'n_mean': 300, 'mention_state_norm': [36.752, 35.871, 34.408], 'embedding_norm': [0.943, 0.943, 0.943]}; mean pool 300 scenes; pointer refs qwen35_9b_x0_probe_v4; gate {'PP': 1.0, 'PM': 0.9071428571428571} (pass True), eligible 572 of 700, used 300.
- Muse: per X slot at 2x (X / Y / random) {'uncentered': {'0': {'n': 202, 'X': 0.3069, 'Y': 0.1634, 'R': 0.1089}, '1': {'n': 201, 'X': 0.3284, 'Y': 0.2985, 'R': 0.209}, '2': {'n': 197, 'X': 0.3503, 'Y': 0.3553, 'R': 0.2234}}, 'centered': {'0': {'n': 202, 'X': 0.3812, 'Y': 0.198, 'R': 0.1089}, '1': {'n': 201, 'X': 0.5323, 'Y': 0.3483, 'R': 0.209}, '2': {'n': 197, 'X': 0.4264, 'Y': 0.3096, 'R': 0.2234}}}; medians {'norm_delta': 167.1012, 'norm_U_delta': 54.5316, 'cos_delta_codes_b_minus_a': 0.0571}; vectors {'norm': [246.327, 305.673, 313.039], 'cos': {'0-1': 0.8543, '0-2': 0.8169, '1-2': 0.9632}, 'slot_specific_norm': [110.152, 60.039, 77.549], 'slot_specific_share': [0.4472, 0.1964, 0.2477], 'cos_centered': {'0-1': -0.7352, '0-2': -0.8512, '1-2': 0.2701}, 'diff_over_norm': {'0-1': 0.6478, '0-2': 0.734, '1-2': 0.2757}, 'cos_diff_vs_pointer_means': {'0-1': 0.1171, '0-2': 0.1002, '1-2': 0.0579}, 'n_mean': 300, 'mention_state_norm': [273.357, 328.754, 338.718], 'embedding_norm': [5.098, 5.099, 5.098]}; mean pool 300 scenes; pointer refs muse30b_x0_probe_v4; gate {'PP': 0.9857142857142858, 'PM': 0.94} (pass True), eligible 580 of 700, used 300.
- 27B: per X slot at 2x (X / Y / random) {'uncentered': {'0': {'n': 210, 'X': 0.1286, 'Y': 0.0476, 'R': 0.0286}, '1': {'n': 189, 'X': 0.1534, 'Y': 0.1376, 'R': 0.1534}, '2': {'n': 201, 'X': 0.0448, 'Y': 0.0398, 'R': 0.0547}}, 'centered': {'0': {'n': 210, 'X': 0.0619, 'Y': 0.1714, 'R': 0.0286}, '1': {'n': 189, 'X': 0.2487, 'Y': 0.2169, 'R': 0.1534}, '2': {'n': 201, 'X': 0.2338, 'Y': 0.0398, 'R': 0.0547}}}; medians {'norm_delta': 54.2418, 'norm_U_delta': 17.8499, 'cos_delta_codes_b_minus_a': 0.0268}; vectors {'norm': [79.366, 79.423, 76.785], 'cos': {'0-1': 0.8743, '0-2': 0.8554, '1-2': 0.9587}, 'slot_specific_norm': [26.237, 16.402, 18.181], 'slot_specific_share': [0.3306, 0.2065, 0.2368], 'cos_centered': {'0-1': -0.7283, '0-2': -0.786, '1-2': 0.1489}, 'diff_over_norm': {'0-1': 0.5015, '0-2': 0.5299, '1-2': 0.2846}, 'cos_diff_vs_pointer_means': {'0-1': 0.0219, '0-2': 0.0382, '1-2': 0.0678}, 'n_mean': 300, 'mention_state_norm': [86.853, 86.818, 84.06], 'embedding_norm': [0.985, 0.983, 0.986]}; mean pool 300 scenes; pointer refs x0_probe_v4_27b; gate {'PP': 0.9985714285714286, 'PM': 0.9971428571428571} (pass True), eligible 692 of 700, used 300.

Figure: x53_bindid.png
