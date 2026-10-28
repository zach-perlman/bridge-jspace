# 48.5: the recall's second route: can an address redirect a recall?

Batch 48, test 48.5 (jobs/c3/batch48.yaml; Q48.5, Dan: 55%). 45m's locker-first scenes (both items' lockers before the asked pick; only the bridge token differs); every arm at the bridge token at the layer fixed in advance, on O. The recall's answer classified by the attribute it matches; the rule counts the informative writes. Cluster bootstrap over bridge items (10000, seed 0). UNVERIFIED.

Rule (fixed in advance): the recall's second route is the address if under (ii) the recall names slot k's item in >= 0.3 of the informative writes with the random vector (iv) <= 0.05 (point estimates), on >= 2 of 3 models.

**Verdict: does not hold** (Q48.5 no; per model {'qwen3.5-9b': 'no', 'qwen3.6-27b': 'no', 'muse-glimmer-30b': 'no'}): 0 of 3 models hold (at least 2 needed).

| model | run | status | informative writes (items) | (ii) write: slot k | (iv) random: slot k | (i) no-J++ alone: slot k | (iii) write alone: slot k | write − random | holds |
|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | qwen35_9b_x48_route2 | tested | 224 (34) | 0.10 [0.06, 0.15] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.03] | 0.06 [0.03, 0.10] | 0.09 [0.05, 0.15] | no |
| qwen3.6-27b | x48_route2_27b | tested | 316 (36) | 0.04 [0.02, 0.07] | 0.02 [0.01, 0.04] | 0.02 [0.01, 0.04] | 0.00 [0.00, 0.00] | 0.02 [0.01, 0.04] | no |
| muse-glimmer-30b | muse30_x48_route2 | tested | 208 (36) | 0.07 [0.03, 0.12] | 0.05 [0.02, 0.09] | 0.03 [0.01, 0.07] | 0.01 [0.00, 0.04] | 0.02 [0.00, 0.05] | no |

Per reader and kind, every class (informative writes; the lookup beside the recall). Collateral: under (ii) the recall's 'original' share is the clean answer kept, 'changed' the no-J++ residual.

| model | reader | kind | n | slot_k | original | changed | other | other_slot (lookup) |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | recall | base | 224 | 0.01 [0.00, 0.03] | 0.24 [0.13, 0.34] | 0.71 [0.62, 0.81] | 0.04 [0.01, 0.07] | - |
| qwen3.5-9b | recall | write | 224 | 0.10 [0.06, 0.15] | 0.33 [0.23, 0.43] | 0.49 [0.41, 0.57] | 0.08 [0.04, 0.11] | - |
| qwen3.5-9b | recall | alone | 224 | 0.06 [0.03, 0.10] | 0.91 [0.84, 0.95] | 0.00 [0.00, 0.01] | 0.03 [0.01, 0.06] | - |
| qwen3.5-9b | recall | random | 224 | 0.01 [0.00, 0.02] | 0.23 [0.13, 0.33] | 0.72 [0.63, 0.81] | 0.04 [0.01, 0.07] | - |
| qwen3.5-9b | lookup | base | 224 | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.99 [0.97, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] |
| qwen3.5-9b | lookup | write | 224 | 0.21 [0.15, 0.28] | 0.01 [0.00, 0.02] | 0.71 [0.64, 0.77] | 0.02 [0.00, 0.05] | 0.05 [0.03, 0.08] |
| qwen3.5-9b | lookup | alone | 224 | 0.21 [0.16, 0.27] | 0.66 [0.58, 0.74] | 0.04 [0.01, 0.07] | 0.04 [0.01, 0.07] | 0.05 [0.01, 0.09] |
| qwen3.5-9b | lookup | random | 224 | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.01] | 0.99 [0.97, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] |
| qwen3.6-27b | recall | base | 316 | 0.02 [0.01, 0.04] | 0.57 [0.47, 0.67] | 0.34 [0.26, 0.44] | 0.06 [0.03, 0.09] | - |
| qwen3.6-27b | recall | write | 316 | 0.04 [0.02, 0.07] | 0.65 [0.54, 0.75] | 0.26 [0.18, 0.35] | 0.05 [0.02, 0.08] | - |
| qwen3.6-27b | recall | alone | 316 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | - |
| qwen3.6-27b | recall | random | 316 | 0.02 [0.01, 0.04] | 0.59 [0.49, 0.70] | 0.33 [0.24, 0.43] | 0.05 [0.02, 0.08] | - |
| qwen3.6-27b | lookup | base | 316 | 0.02 [0.00, 0.03] | 0.01 [0.00, 0.02] | 0.97 [0.94, 0.99] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] |
| qwen3.6-27b | lookup | write | 316 | 0.18 [0.14, 0.23] | 0.05 [0.03, 0.08] | 0.73 [0.67, 0.80] | 0.00 [0.00, 0.00] | 0.03 [0.01, 0.06] |
| qwen3.6-27b | lookup | alone | 316 | 0.13 [0.09, 0.16] | 0.81 [0.74, 0.88] | 0.03 [0.00, 0.07] | 0.00 [0.00, 0.01] | 0.03 [0.01, 0.05] |
| qwen3.6-27b | lookup | random | 316 | 0.02 [0.00, 0.03] | 0.00 [0.00, 0.01] | 0.97 [0.94, 0.99] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] |
| muse-glimmer-30b | recall | base | 208 | 0.03 [0.01, 0.07] | 0.50 [0.36, 0.64] | 0.37 [0.21, 0.50] | 0.11 [0.06, 0.17] | - |
| muse-glimmer-30b | recall | write | 208 | 0.07 [0.03, 0.12] | 0.57 [0.48, 0.66] | 0.21 [0.13, 0.29] | 0.14 [0.09, 0.22] | - |
| muse-glimmer-30b | recall | alone | 208 | 0.01 [0.00, 0.04] | 0.97 [0.93, 0.99] | 0.01 [0.00, 0.03] | 0.01 [0.00, 0.03] | - |
| muse-glimmer-30b | recall | random | 208 | 0.05 [0.02, 0.09] | 0.52 [0.40, 0.65] | 0.32 [0.20, 0.42] | 0.11 [0.06, 0.17] | - |
| muse-glimmer-30b | lookup | base | 208 | 0.04 [0.02, 0.07] | 0.03 [0.01, 0.06] | 0.88 [0.81, 0.93] | 0.00 [0.00, 0.00] | 0.05 [0.02, 0.08] |
| muse-glimmer-30b | lookup | write | 208 | 0.26 [0.20, 0.34] | 0.08 [0.04, 0.13] | 0.53 [0.44, 0.61] | 0.00 [0.00, 0.00] | 0.13 [0.10, 0.17] |
| muse-glimmer-30b | lookup | alone | 208 | 0.23 [0.16, 0.31] | 0.67 [0.59, 0.75] | 0.04 [0.01, 0.07] | 0.00 [0.00, 0.00] | 0.06 [0.03, 0.08] |
| muse-glimmer-30b | lookup | random | 208 | 0.04 [0.02, 0.07] | 0.04 [0.02, 0.07] | 0.87 [0.80, 0.92] | 0.00 [0.00, 0.00] | 0.05 [0.02, 0.08] |

All writes (uninformative ones included; descriptive): the recall's slot k share per kind.

| model | n | base | write | alone | random |
|---|---|---|---|---|---|
| qwen3.5-9b | 453 | 0.36 [0.31, 0.43] | 0.35 [0.29, 0.43] | 0.13 [0.08, 0.19] | 0.35 [0.30, 0.42] |
| qwen3.6-27b | 606 | 0.17 [0.14, 0.21] | 0.19 [0.15, 0.24] | 0.06 [0.03, 0.10] | 0.18 [0.14, 0.22] |
| muse-glimmer-30b | 429 | 0.18 [0.14, 0.24] | 0.17 [0.13, 0.22] | 0.09 [0.05, 0.14] | 0.19 [0.14, 0.24] |

Per slot pair j → k (informative writes; descriptive): the recall's slot k share under the write / the random vector.

| model | pair | n | write | random |
|---|---|---|---|---|
| qwen3.5-9b | 0-1 | 12 | 0.08 [0.00, 0.27] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | 0-2 | 19 | 0.05 [0.00, 0.22] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | 0-3 | 17 | 0.06 [0.00, 0.21] | 0.06 [0.00, 0.14] |
| qwen3.5-9b | 1-0 | 15 | 0.27 [0.06, 0.58] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | 1-2 | 23 | 0.04 [0.00, 0.14] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | 1-3 | 19 | 0.05 [0.00, 0.19] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | 2-0 | 17 | 0.35 [0.14, 0.67] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | 2-1 | 25 | 0.04 [0.00, 0.14] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | 2-3 | 30 | 0.03 [0.00, 0.10] | 0.03 [0.00, 0.10] |
| qwen3.5-9b | 3-0 | 19 | 0.21 [0.05, 0.45] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | 3-1 | 12 | 0.08 [0.00, 0.30] | 0.00 [0.00, 0.00] |
| qwen3.5-9b | 3-2 | 16 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | 0-1 | 21 | 0.14 [0.00, 0.32] | 0.05 [0.00, 0.16] |
| qwen3.6-27b | 0-2 | 26 | 0.12 [0.00, 0.24] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | 0-3 | 28 | 0.00 [0.00, 0.00] | 0.04 [0.00, 0.10] |
| qwen3.6-27b | 1-0 | 19 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | 1-2 | 35 | 0.06 [0.00, 0.16] | 0.03 [0.00, 0.11] |
| qwen3.6-27b | 1-3 | 30 | 0.03 [0.00, 0.12] | 0.03 [0.00, 0.12] |
| qwen3.6-27b | 2-0 | 28 | 0.04 [0.00, 0.12] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | 2-1 | 30 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | 2-3 | 44 | 0.05 [0.00, 0.12] | 0.05 [0.00, 0.12] |
| qwen3.6-27b | 3-0 | 22 | 0.05 [0.00, 0.17] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | 3-1 | 16 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| qwen3.6-27b | 3-2 | 17 | 0.06 [0.00, 0.19] | 0.06 [0.00, 0.19] |
| muse-glimmer-30b | 0-1 | 15 | 0.27 [0.00, 0.50] | 0.07 [0.00, 0.23] |
| muse-glimmer-30b | 0-2 | 18 | 0.11 [0.00, 0.33] | 0.11 [0.00, 0.33] |
| muse-glimmer-30b | 0-3 | 16 | 0.12 [0.00, 0.31] | 0.19 [0.00, 0.33] |
| muse-glimmer-30b | 1-0 | 13 | 0.08 [0.00, 0.19] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | 1-2 | 20 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | 1-3 | 22 | 0.09 [0.00, 0.25] | 0.09 [0.00, 0.25] |
| muse-glimmer-30b | 2-0 | 16 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | 2-1 | 24 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | 2-3 | 24 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| muse-glimmer-30b | 3-0 | 16 | 0.19 [0.00, 0.38] | 0.06 [0.00, 0.17] |
| muse-glimmer-30b | 3-1 | 12 | 0.08 [0.00, 0.30] | 0.08 [0.00, 0.30] |
| muse-glimmer-30b | 3-2 | 12 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

Items, norms and checks (descriptive):

- qwen3.5-9b (qwen35_9b_x48_route2, from qwen35_9b_x45m_fresh, L12): 151 items of 45p's 186 (original locker {'before': 151, 'after': 35}); 453 writes, 224 informative (uninformative: {"the same attribute as the original's or the changed item's": 78, "the changed item's slot": 151}); write norms s = 2: {'0-1': 8.1996, '0-2': 9.6374, '0-3': 11.7068, '1-0': 8.1996, '1-2': 4.86, '1-3': 7.94, '2-0': 9.6374, '2-1': 4.86, '2-3': 4.0502, '3-0': 11.7068, '3-1': 7.94, '3-2': 4.0502}; median change norm 13.5239, median J++ share 0.25024; base arms: {'lookup none': {'n': 151, 'switched': 0.0, 'right': 1.0}, 'lookup whole': {'n': 151, 'switched': 0.9933774834437086, 'right': 0.0}, 'lookup a1': {'n': 151, 'switched': 0.9933774834437086, 'right': 0.0}, 'recall none': {'n': 151, 'switched': 0.006622516556291391, 'right': 0.9933774834437086}, 'recall whole': {'n': 151, 'switched': 0.9867549668874173, 'right': 0.006622516556291391}, 'recall a1': {'n': 151, 'switched': 0.7549668874172185, 'right': 0.2052980132450331}}; checks: lookup whole vs 45m's stored whole: 151 of 151 agree (rerun 150, stored 150); lookup a1 vs 45m's stored no_part: 151 of 151 agree (rerun 150, stored 150); recall whole vs 45m's stored whole: 151 of 151 agree (rerun 149, stored 149); recall a1 vs 45m's stored no_part: 151 of 151 agree (rerun 114, stored 114)
- qwen3.6-27b (x48_route2_27b, from x45m_fresh_27b, L32): 202 items of 45p's 254 (original locker {'before': 202, 'after': 52}); 606 writes, 316 informative (uninformative: {"the same attribute as the original's or the changed item's": 88, "the changed item's slot": 202}); write norms s = 2: {'0-1': 27.137, '0-2': 33.574, '0-3': 42.6312, '1-0': 27.137, '1-2': 16.788, '1-3': 29.2212, '2-0': 33.574, '2-1': 16.788, '2-3': 15.7906, '3-0': 42.6312, '3-1': 29.2212, '3-2': 15.7906}; median change norm 40.69185, median J++ share 0.16181; base arms: {'lookup none': {'n': 202, 'switched': 0.0, 'right': 1.0}, 'lookup whole': {'n': 202, 'switched': 0.9752475247524752, 'right': 0.0}, 'lookup a1': {'n': 202, 'switched': 0.9702970297029703, 'right': 0.0049504950495049506}, 'recall none': {'n': 202, 'switched': 0.0, 'right': 1.0}, 'recall whole': {'n': 202, 'switched': 0.7970297029702971, 'right': 0.1485148514851485}, 'recall a1': {'n': 202, 'switched': 0.33663366336633666, 'right': 0.5891089108910891}}; checks: lookup whole vs 45m's stored whole: 202 of 202 agree (rerun 197, stored 197); lookup a1 vs 45m's stored no_part: 202 of 202 agree (rerun 196, stored 196); recall whole vs 45m's stored whole: 201 of 202 agree (rerun 161, stored 162); recall a1 vs 45m's stored no_part: 201 of 202 agree (rerun 68, stored 69)
- muse-glimmer-30b (muse30_x48_route2, from muse30b_x45m_fresh, L26): 143 items of 45p's 178 (original locker {'before': 143, 'after': 35}); 429 writes, 208 informative (uninformative: {"the same attribute as the original's or the changed item's": 78, "the changed item's slot": 143}); write norms s = 2: {'0-1': 82.7624, '0-2': 101.6898, '0-3': 127.1302, '1-0': 82.7624, '1-2': 49.7362, '1-3': 88.3518, '2-0': 101.6898, '2-1': 49.7362, '2-3': 53.3076, '3-0': 127.1302, '3-1': 88.3518, '3-2': 53.3076}; median change norm 144.5507, median J++ share 0.15817; base arms: {'lookup none': {'n': 143, 'switched': 0.0, 'right': 1.0}, 'lookup whole': {'n': 143, 'switched': 0.8671328671328671, 'right': 0.027972027972027972}, 'lookup a1': {'n': 143, 'switched': 0.8741258741258742, 'right': 0.04195804195804196}, 'recall none': {'n': 143, 'switched': 0.0, 'right': 1.0}, 'recall whole': {'n': 143, 'switched': 0.6013986013986014, 'right': 0.3356643356643357}, 'recall a1': {'n': 143, 'switched': 0.32867132867132864, 'right': 0.5594405594405595}}; checks: lookup whole vs 45m's stored whole: 143 of 143 agree (rerun 124, stored 124); lookup a1 vs 45m's stored no_part: 142 of 143 agree (rerun 125, stored 124); recall whole vs 45m's stored whole: 141 of 143 agree (rerun 86, stored 84); recall a1 vs 45m's stored no_part: 143 of 143 agree (rerun 47, stored 47)
