# 48.5: the recall's second route: can an address redirect a recall?

The batch line counts the given runs only (Lightning alone): not a re-score of 48.5's count.

Batch 48, test 48.5 (jobs/c3/batch48.yaml; batch 52 below gate, below gate (exploratory): Lightning's clean one-pick gate fails (recall 0.751 < 0.80, results/x0_necessity/nem35l_x45s_smoke_clean/gate.json); eligible items only; hollow, never in the claims table or grades; rules verbatim, no prediction (Dan's morning queue, 29 Oct)). 45m's locker-first scenes (both items' lockers before the asked pick; only the bridge token differs); every arm at the bridge token at the layer fixed in advance, on O. The recall's answer classified by the attribute it matches; the rule counts the informative writes. Cluster bootstrap over bridge items (10000, seed 0). UNVERIFIED.

Rule (fixed in advance): the recall's second route is the address if under (ii) the recall names slot k's item in >= 0.3 of the informative writes with the random vector (iv) <= 0.05 (point estimates), on >= 2 of 3 models.

**Verdict: does not hold** (Q48.5 no; per model {'nemotron-3.5-lightning': 'no'}): 0 of 1 models hold (at least 2 needed).

| model | run | status | informative writes (items) | (ii) write: slot k | (iv) random: slot k | (i) no-J++ alone: slot k | (iii) write alone: slot k | write − random | holds |
|---|---|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | nem35l_x52_route2_below | tested | 122 (33) | 0.11 [0.06, 0.17] | 0.04 [0.01, 0.09] | 0.02 [0.00, 0.07] | 0.09 [0.04, 0.14] | 0.07 [0.03, 0.11] | no |

Per reader and kind, every class (informative writes; the lookup beside the recall). Collateral: under (ii) the recall's 'original' share is the clean answer kept, 'changed' the no-J++ residual.

| model | reader | kind | n | slot_k | original | changed | other | other_slot (lookup) |
|---|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | recall | base | 122 | 0.02 [0.00, 0.07] | 0.04 [0.00, 0.11] | 0.84 [0.74, 0.92] | 0.10 [0.04, 0.16] | - |
| nemotron-3.5-lightning | recall | write | 122 | 0.11 [0.06, 0.17] | 0.11 [0.04, 0.20] | 0.69 [0.57, 0.78] | 0.10 [0.05, 0.15] | - |
| nemotron-3.5-lightning | recall | alone | 122 | 0.09 [0.04, 0.14] | 0.86 [0.78, 0.93] | 0.01 [0.00, 0.03] | 0.04 [0.00, 0.09] | - |
| nemotron-3.5-lightning | recall | random | 122 | 0.04 [0.01, 0.09] | 0.06 [0.01, 0.12] | 0.80 [0.71, 0.87] | 0.11 [0.04, 0.18] | - |
| nemotron-3.5-lightning | lookup | base | 122 | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.98 [0.95, 1.00] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.03] |
| nemotron-3.5-lightning | lookup | write | 122 | 0.19 [0.13, 0.25] | 0.03 [0.01, 0.07] | 0.73 [0.67, 0.79] | 0.00 [0.00, 0.00] | 0.05 [0.02, 0.08] |
| nemotron-3.5-lightning | lookup | alone | 122 | 0.25 [0.20, 0.31] | 0.64 [0.57, 0.71] | 0.04 [0.01, 0.07] | 0.00 [0.00, 0.00] | 0.07 [0.04, 0.09] |
| nemotron-3.5-lightning | lookup | random | 122 | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.98 [0.95, 1.00] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.03] |

All writes (uninformative ones included; descriptive): the recall's slot k share per kind.

| model | n | base | write | alone | random |
|---|---|---|---|---|---|
| nemotron-3.5-lightning | 267 | 0.41 [0.36, 0.47] | 0.41 [0.35, 0.48] | 0.17 [0.12, 0.23] | 0.41 [0.35, 0.47] |

Per slot pair j → k (informative writes; descriptive): the recall's slot k share under the write / the random vector.

| model | pair | n | write | random |
|---|---|---|---|---|
| nemotron-3.5-lightning | 0-1 | 11 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | 0-2 | 11 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | 0-3 | 12 | 0.17 [0.00, 0.38] | 0.25 [0.06, 0.50] |
| nemotron-3.5-lightning | 1-0 | 6 | 0.17 [0.00, 0.50] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | 1-2 | 10 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | 1-3 | 9 | 0.22 [0.00, 0.56] | 0.11 [0.00, 0.33] |
| nemotron-3.5-lightning | 2-0 | 11 | 0.36 [0.10, 0.64] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | 2-1 | 12 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | 2-3 | 17 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | 3-0 | 8 | 0.38 [0.12, 0.80] | 0.00 [0.00, 0.00] |
| nemotron-3.5-lightning | 3-1 | 8 | 0.12 [0.00, 0.43] | 0.12 [0.00, 0.43] |
| nemotron-3.5-lightning | 3-2 | 7 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

Items, norms and checks (descriptive):

- nemotron-3.5-lightning (nem35l_x52_route2_below, from nem35l_x52_fresh, L14): 89 items of 45p's 119 (original locker {'after': 30, 'before': 89}); 267 writes, 122 informative (uninformative: {"the changed item's slot": 89, "the same attribute as the original's or the changed item's": 56}); write norms s = 2: {'0-1': 6.6864, '0-2': 8.0426, '0-3': 9.306, '1-0': 6.6864, '1-2': 3.5602, '1-3': 6.0142, '2-0': 8.0426, '2-1': 3.5602, '2-3': 3.4906, '3-0': 9.306, '3-1': 6.0142, '3-2': 3.4906}; median change norm 13.589, median J++ share 0.27057; base arms: {'lookup none': {'n': 89, 'switched': 0.0, 'right': 1.0}, 'lookup whole': {'n': 89, 'switched': 0.9887640449438202, 'right': 0.0}, 'lookup a1': {'n': 89, 'switched': 0.9887640449438202, 'right': 0.0}, 'recall none': {'n': 89, 'switched': 0.011235955056179775, 'right': 0.9887640449438202}, 'recall whole': {'n': 89, 'switched': 0.9775280898876404, 'right': 0.011235955056179775}, 'recall a1': {'n': 89, 'switched': 0.8651685393258427, 'right': 0.0449438202247191}}; checks: lookup whole vs 45m's stored whole: 89 of 89 agree (rerun 88, stored 88); lookup a1 vs 45m's stored no_part: 89 of 89 agree (rerun 88, stored 88); recall whole vs 45m's stored whole: 88 of 89 agree (rerun 87, stored 86); recall a1 vs 45m's stored no_part: 86 of 89 agree (rerun 77, stored 76)
